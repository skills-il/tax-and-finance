#!/usr/bin/env python3
"""
broker-gains-ils.py: per-trade shekel capital-gain working figures for an
Israeli resident individual who holds shares at a foreign broker.

What it does (stdlib only, no network):
  1. Reads one or more trades CSVs (one per broker account, --trades repeated)
     with user-mappable column names (--map). Lots are matched per account.
  2. Reads rates CSVs: "date,rate[,currency]" or the Bank of Israel SDMX CSV
     export (TIME_PERIOD, OBS_VALUE, BASE_CURRENCY, UNIT_MULT).
  3. Matches every sale to purchase lots in order of purchase (first in,
     first out) per symbol, unless the sale row names a specific lot by
     lot_ref (the buy row's lot_ref is that lot's id) or by open_date
     (regulation 5 of the 2002 Regulations on computing capital gain lets
     the seller prove a specific lot).
  4. Converts cost at the representative rate of the purchase day and the
     consideration at the rate of the sale day (Conversion Rules 2003, rule 7).
     A day with no published rate takes the last rate published before it
     (rule 1), but only inside the range the rates file covers: a file that
     ends before the date is an open item, not a fallback.
  5. Splits each match into real gain and allowable loss:
       C = cost in ILS at the purchase rate (commissions included)
       P = consideration in ILS at the sale rate (commissions deducted)
       A = cost in foreign currency x sale-day rate (Section 88 index rule)
       real gain      = max(0, P - max(A, C))
       allowable loss = max(0, min(A, C) - P)
     This reproduces Civil Appeal 3555/15 (Moses).
  6. Offsets losses: current-year losses against this year's real gains
     (highest-rate column first, an assumption), then against Israeli-account
     gains you pass in, then against dividends from securities taxed at no
     more than 25% (or paid on the loss-making security itself), never against
     cash interest; then a brought-forward loss (--carryforward-in) against
     capital gain only.
  7. Nets dividends, reversals and refunds per symbol and year, converts each
     row at its own payment-day rate (rules 3 and 6), caps the foreign tax
     credit at the treaty rate and at the Israeli tax on that income
     (s.204(b)), and reports any s.205A excess separately.

Every total is marked INCOMPLETE when any row could not be computed.
The output is a WORKING PAPER, not a filed return and not tax advice.

Examples:
  python3 broker-gains-ils.py --trades trades.csv --rates usd.csv --year 2025
  python3 broker-gains-ils.py --trades ibkr.csv --trades schwab.csv --rates boi.csv \\
      --year 2025 --income income.csv --carryforward-in 12000 --csv-out per-trade.csv
"""

import argparse
import csv
import datetime as dt
import json
import os
import sys
from collections import defaultdict, deque

CANONICAL = ['date', 'symbol', 'side', 'quantity', 'price', 'fee', 'currency', 'instrument', 'open_date', 'lot_ref']
ETORO_CANONICAL = ['position_id', 'symbol', 'units', 'open_date', 'close_date', 'open_price', 'close_price', 'instrument', 'currency', 'direction']
EXCLUDED_INSTRUMENTS = {'SHORT': 'a short position: not computed here (a long-only engine would reverse its sign); ask a CPA',
                        'UNTYPED': 'of unknown type (no instrument column mapped): not computed',
                        'CFD': 'a CFD: its tax treatment is not covered by this skill; ask a CPA',
                        'CRYPTO': 'crypto: not a security here; use the israeli-crypto-tax-reporter skill'}
INCOME_CANONICAL = ['date', 'symbol', 'type', 'amount', 'currency', 'tax_withheld', 'country']

RATE_REAL_GAIN = 0.25          # s.91(b)(1), individual, real gain
RATE_SUBSTANTIAL = 0.30        # s.91(b)(2), substantial shareholder
RATE_PRE_2005_FOREIGN = 0.35   # Form 1322: foreign-security real gain for days up to 31.12.2004
RATE_DIVIDEND = 0.25           # s.125B(1)
RATE_DIVIDEND_SUBSTANTIAL = 0.30  # s.125B(2)
RATE_INTEREST_DEFAULT = 0.25   # s.125C(b); a foreign-currency asset is indexed to the currency
OFFSET_RATE_CAP = 0.25         # s.92(a)(4)(b): other securities' dividends only if taxed at no more than this
TREATY_DIVIDEND = {'US': 0.25}  # US-Israel treaty Article 12(2)(a), individual
SURTAX_THRESHOLD = 721560      # s.121B, fixed for 2024 through 2027
SURTAX_ALL_YEARS = (2024, 2025, 2026, 2027)   # 3% limb, threshold above
SURTAX_CAPITAL_FROM = 2025     # 2% limb (s.121B(a1)) applies from tax year 2025
SURTAX_ALL = 0.03              # s.121B(a)
SURTAX_CAPITAL = 0.02          # s.121B(a1)
FOREIGN_SPLIT_DATE = dt.date(2004, 12, 31)
MAX_RATE_LOOKBACK_DAYS = 10
DISCLAIMER = 'WORKING FIGURES ONLY. Not tax advice and not a filed return.'


def die(msg):
    print(f'ERROR: {msg}', file=sys.stderr)
    sys.exit(2)


def parse_date(s, where):
    s = (s or '').strip()
    if not s:
        die(f'empty date in {where}')
    s = s.split(' ')[0].split('T')[0].split(',')[0].strip()
    for fmt in ('%Y-%m-%d', '%Y%m%d', '%d/%m/%Y', '%d.%m.%Y'):
        try:
            return dt.datetime.strptime(s, fmt).date()
        except ValueError:
            pass
    die(f'cannot parse date {s!r} in {where} (use YYYY-MM-DD; DD/MM/YYYY is read day-first)')


def parse_num(s, where, allow_empty=False):
    s = (s or '').strip().replace(',', '')
    if s == '':
        if allow_empty:
            return 0.0
        die(f'empty number in {where}')
    try:
        return float(s)
    except ValueError:
        die(f'cannot parse number {s!r} in {where}')


def parse_map(text, canon):
    mapping = {c: c for c in canon}
    if not text:
        return mapping
    for part in text.split(','):
        if '=' not in part:
            die(f'--map entry {part!r} must look like canonical=YourColumn')
        k, v = part.split('=', 1)
        k = k.strip().lower()
        if k not in canon:
            die(f'--map key {k!r} is not one of {canon}')
        mapping[k] = v.strip()
    return mapping


def read_csv(path):
    if path.lower().endswith(('.xlsx', '.xls')):
        die(f'{path} is a spreadsheet. Open it and save the relevant sheet as CSV (UTF-8), then pass the CSV')
    with open(path, newline='', encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))


# ---------------------------------------------------------------- rates
def load_rates(paths, default_ccy):
    """Return {currency: {date: ILS per 1 unit}}."""
    rates = defaultdict(dict)
    for path in paths:
        rows = read_csv(path)
        if not rows:
            die(f'rates file {path} is empty')
        cols = {c.strip().upper(): c for c in rows[0].keys()}
        boi = 'TIME_PERIOD' in cols and 'OBS_VALUE' in cols
        for i, r in enumerate(rows, 2):
            where = f'{path} line {i}'
            if boi:
                d = parse_date(r[cols['TIME_PERIOD']], where)
                v = parse_num(r[cols['OBS_VALUE']], where)
                mult = int(parse_num(r.get(cols.get('UNIT_MULT', ''), '0') or '0', where, True))
                v = v / (10 ** mult)   # BoI quotes some currencies per 100 units
                ccy = (r.get(cols.get('BASE_CURRENCY', ''), '') or default_ccy).strip().upper()
            else:
                low = {k.strip().lower(): k for k in r.keys()}
                if 'date' not in low or 'rate' not in low:
                    die(f'{path}: need columns date,rate[,currency] or a Bank of Israel SDMX CSV')
                d = parse_date(r[low['date']], where)
                v = parse_num(r[low['rate']], where)
                ccy = (r.get(low.get('currency', ''), '') or default_ccy).strip().upper()
            if v <= 0:
                die(f'non-positive rate in {where}')
            rates[ccy][d] = v
    return rates


def rate_on(rates, ccy, day, issues, label):
    table = rates.get(ccy)
    if not table:
        issues.append(f'NO RATES for currency {ccy} ({label}); add a rates file for it')
        return None
    if day in table:
        return table[day]
    if day > max(table):
        issues.append(f'MISSING RATE: the {ccy} rates file ends on {max(table)}, before {day} ({label}). Extend the file; this is not a non-publication day')
        return None
    for back in range(1, MAX_RATE_LOOKBACK_DAYS + 1):
        d = day - dt.timedelta(days=back)
        if d in table:
            issues.append(f'{label}: no {ccy} rate published on {day}, used the last published rate of {d} (rule 1 of the Conversion Rules)')
            return table[d]
    issues.append(f'MISSING RATE: {ccy} on {day} and the {MAX_RATE_LOOKBACK_DAYS} days before ({label})')
    return None


# ---------------------------------------------------------------- trades
def load_trades(path, mapping, default_ccy, issues):
    rows = read_csv(path)
    if not rows:
        return []
    header = set(rows[0].keys())
    for k in ('date', 'symbol', 'quantity', 'price'):
        if mapping[k] not in header:
            die(f'{path} has no column {mapping[k]!r} for {k}; columns are {sorted(header)}. Use --map. '
                'An IBKR Activity Statement stacks several sections in one CSV: export a Flex Query trade report, '
                'or copy only the Trades section (with its header row) into its own file')
    if mapping['instrument'] not in header:
        issues.append(f'{path}: no instrument / asset-class column, so CFD and crypto rows cannot be detected. Every row was computed '
                      'as a share; confirm the file holds only shares and ETFs, or map the column with --map instrument=...')
    trades = []
    for i, r in enumerate(rows, 2):
        where = f'{path} line {i}'
        qty = parse_num(r[mapping['quantity']], where)
        side = (r.get(mapping['side'], '') or '').strip().upper()
        if side in ('BUY', 'B', 'BOT', 'קנייה'):
            side = 'BUY'
        elif side in ('SELL', 'S', 'SLD', 'מכירה'):
            side = 'SELL'
        elif side == '':
            side = 'BUY' if qty > 0 else 'SELL'
        else:
            side = 'OTHER:' + side
        instrument = (r.get(mapping['instrument'], '') or '').strip().upper()
        od = (r.get(mapping['open_date'], '') or '').strip()
        lref = (r.get(mapping['lot_ref'], '') or '').strip()
        trades.append({
            'file': path, 'line': i,
            'date': parse_date(r[mapping['date']], where),
            'symbol': (r[mapping['symbol']] or '').strip().upper(),
            'side': side, 'instrument': instrument,
            'open_date': parse_date(od, where) if od else None,
            'lot_ref': lref if side == 'SELL' else '', 'ref': lref if side == 'BUY' else '',
            'quantity': abs(qty),
            'price': abs(parse_num(r[mapping['price']], where)),
            'fee': abs(parse_num(r.get(mapping['fee'], ''), where, allow_empty=True)),
            'currency': ((r.get(mapping['currency'], '') or default_ccy).strip().upper()),
        })
    # Same-day rows listed SELL before BUY may be a short sale or a day trade.
    seen = defaultdict(list)
    for t in trades:
        seen[(t['symbol'], t['date'])].append(t)
    for (sym, d), ts in seen.items():
        sides = [t['side'] for t in ts]
        if 'SELL' in sides and 'BUY' in sides and sides.index('SELL') < sides.index('BUY'):
            issues.append(f'{path}: on {d} {sym} has a SELL listed before a BUY. The script matches the BUY first; '
                          'if this was a short sale or the order matters, handle it by hand')
    trades.sort(key=lambda t: (t['date'], 0 if t['side'] == 'BUY' else 1, t['line']))
    return trades


def load_etoro(path, mapping, default_ccy, issues, assume_real):
    """eToro-style closed positions: one row per position -> a BUY and a SELL row.

    Column names are mapped with --etoro-map; check them against your own file.
    Spread and overnight fees are NOT read: add them by hand if they are in the file.
    """
    rows = read_csv(path)
    if not rows:
        return []
    header = set(rows[0].keys())
    for k in ('symbol', 'units', 'open_date', 'close_date', 'open_price', 'close_price'):
        if mapping[k] not in header:
            die(f'{path} has no column {mapping[k]!r} for {k}; columns are {sorted(header)}. Use --etoro-map')
    has_inst = mapping['instrument'] in header
    has_dir = mapping['direction'] in header
    if not has_inst and not assume_real:
        issues.append(f'{path}: no instrument / type column mapped, so CFD, crypto and leveraged rows cannot be told apart. '
                      'Nothing in this file was computed. Map --etoro-map instrument=<column>, or pass --assume-real-shares '
                      'only if every row is a real (unleveraged, long) share')
    out = []
    for i, r in enumerate(rows, 2):
        where = f'{path} line {i}'
        units = abs(parse_num(r[mapping['units']], where))
        raw_sym = (r[mapping['symbol']] or '').strip().upper()
        sym = raw_sym
        for pre in ('BUY ', 'SELL '):
            if sym.startswith(pre):
                sym = sym[len(pre):].strip()
        direction = (r.get(mapping['direction'], '') or '').strip().upper() if has_dir else ''
        short = 'SHORT' in direction or (not has_dir and raw_sym.startswith('SELL '))
        pid = (r.get(mapping['position_id'], '') or '').strip() or f'{path}:{i}'
        inst = (r.get(mapping['instrument'], '') or '').strip().upper() if has_inst else ''
        if not has_inst and not assume_real:
            inst = 'UNTYPED'
        if short:
            inst = 'SHORT ' + inst
        ccy = (r.get(mapping['currency'], '') or default_ccy).strip().upper()
        od = parse_date(r[mapping['open_date']], where)
        cd = parse_date(r[mapping['close_date']], where)
        base = {'file': path, 'etoro': True, 'symbol': sym, 'instrument': inst, 'quantity': units, 'fee': 0.0, 'currency': ccy}
        out.append(dict(base, line=i, side='BUY', date=od, price=abs(parse_num(r[mapping['open_price']], where)),
                        open_date=None, lot_ref='', ref=pid))
        out.append(dict(base, line=i, side='SELL', date=cd, price=abs(parse_num(r[mapping['close_price']], where)),
                        open_date=od, lot_ref=pid))
    issues.append(f'{path}: positions split into BUY and SELL rows and matched by position (regulation 5 specific lot). '
                  'Spread and overnight fees were not read; check whether your statement shows them. Symbols come from the '
                  'symbol column with any leading BUY/SELL word removed; use the same name in --substantial and in the income file')
    out.sort(key=lambda t: (t['date'], 0 if t['side'] == 'BUY' else 1, t['line']))
    return out


def half_of(d):
    return 'H1' if d.month <= 6 else 'H2'


def match(trades, rates, year, substantial, issues, account):
    lots = defaultdict(deque)
    out = []
    for t in trades:
        tag = f"{account} line {t['line']}"
        excl = next((k for k in EXCLUDED_INSTRUMENTS if k in t['instrument']), None)
        if excl:
            issues.append(f"{tag}: {t['symbol']} is {EXCLUDED_INSTRUMENTS[excl]}. Left out of every total")
            if t['side'] == 'SELL' and t['date'].year == year:
                out.append({'account': account, 'symbol': t['symbol'], 'buy_date': '', 'sell_date': str(t['date']),
                            'quantity': t['quantity'], 'status': f'{excl} EXCLUDED'})
            continue
        if t['side'].startswith('OTHER'):
            issues.append(f"{tag}: side {t['side'][6:]!r} for {t['symbol']} is not BUY or SELL (split, merger, spin-off, transfer?). Handle it by hand: it can change lot cost and dates")
            if t['date'].year == year:
                out.append({'account': account, 'symbol': t['symbol'], 'buy_date': '', 'sell_date': str(t['date']),
                            'quantity': t['quantity'], 'status': 'NOT A BUY OR SELL'})
            continue
        if t['side'] == 'BUY':
            lots[t['symbol']].append({'date': t['date'], 'qty': t['quantity'],
                                      'cost_fx': t['quantity'] * t['price'] + t['fee'],
                                      'currency': t['currency'], 'line': t['line'], 'ref': t.get('ref', '')})
            continue
        remaining = t['quantity']
        proceeds_total = t['quantity'] * t['price'] - t['fee']
        q = lots[t['symbol']]
        lot_failed = False
        found_ref = False
        if t.get('lot_ref'):
            specific = [l for l in q if l.get('ref') == t['lot_ref']]
            if specific:
                found_ref = True
                have = sum(l['qty'] for l in specific)
                if have + 1e-9 < t['quantity']:
                    issues.append(f"{tag}: lot {t['lot_ref']} holds {have:g} {t['symbol']} but {t['quantity']:g} were sold; "
                                  f"the other {t['quantity'] - have:g} were matched FIFO. Check the lot reference")
                if not t.get('etoro'):
                    issues.append(f"{tag}: {t['symbol']} matched to lot {t['lot_ref']} (regulation 5). Keep the records that prove the lot")
                for l in specific:
                    q.remove(l)
                for l in reversed(specific):
                    q.appendleft(l)
            elif not t['open_date']:
                lot_failed = True
                issues.append(f"{tag}: lot reference {t['lot_ref']} not found for {t['symbol']}; FIFO used and the row is excluded (totals INCOMPLETE)")
        if t['open_date'] and not found_ref:
            specific = [l for l in q if l['date'] == t['open_date']]
            if len({round(l['cost_fx'] / l['qty'], 6) for l in specific}) > 1:
                issues.append(f"{tag}: several {t['symbol']} lots opened on {t['open_date']} at different prices; matched by date only, FIFO between them. Use a lot_ref column to pick the lot")
            if specific:
                for l in specific:
                    q.remove(l)
                for l in reversed(specific):
                    q.appendleft(l)
                issues.append(f"{tag}: {t['symbol']} matched to the specific lot of {t['open_date']} (regulation 5). Keep the records that prove the lot")
            else:
                lot_failed = True
                issues.append(f"{tag}: open_date {t['open_date']} does not match any {t['symbol']} lot; FIFO used and the row is excluded (totals INCOMPLETE)")
        while remaining > 1e-9:
            if not q:
                issues.append(f"UNMATCHED SALE {tag}: {remaining:g} {t['symbol']} sold on {t['date']} with no purchase lot in the file (missing earlier years, a transfer-in, or a short sale)")
                if t['date'].year == year:
                    out.append({'account': account, 'symbol': t['symbol'], 'buy_date': '', 'sell_date': str(t['date']),
                                'quantity': round(remaining, 6), 'status': 'UNMATCHED'})
                break
            lot = q[0]
            take = min(remaining, lot['qty'])
            cost_fx = lot['cost_fx'] * take / lot['qty']
            proceeds_fx = proceeds_total * take / t['quantity']
            lot['cost_fx'] -= cost_fx
            lot['qty'] -= take
            if lot['qty'] <= 1e-9:
                q.popleft()
            remaining -= take
            if t['date'].year != year:
                continue
            row = {'account': account, 'symbol': t['symbol'], 'buy_date': str(lot['date']), 'sell_date': str(t['date']),
                   'quantity': round(take, 6), 'currency': t['currency'],
                   'cost_fx': round(cost_fx, 2), 'proceeds_fx': round(proceeds_fx, 2), 'half': half_of(t['date'])}
            if lot_failed:
                row['status'] = 'SPECIFIC LOT NOT FOUND'
                out.append(row)
                continue
            if lot['currency'] != t['currency']:
                issues.append(f"{tag}: {t['symbol']} bought in {lot['currency']} and sold in {t['currency']}; not computed, handle by hand")
                row['status'] = 'CURRENCY MISMATCH'
                out.append(row)
                continue
            rb = rate_on(rates, lot['currency'], lot['date'], issues, f"buy {t['symbol']} {account} line {lot['line']}")
            rs = rate_on(rates, t['currency'], t['date'], issues, f"sell {t['symbol']} {tag}")
            row.update({'rate_buy': rb, 'rate_sell': rs})
            if rb is None or rs is None:
                row['status'] = 'MISSING RATE'
                out.append(row)
                continue
            C = cost_fx * rb
            P = proceeds_fx * rs
            A = cost_fx * rs
            real_gain = max(0.0, P - max(A, C))
            loss = max(0.0, min(A, C) - P)
            nominal = P - C
            inflationary = max(0.0, nominal - real_gain) if nominal > 0 else 0.0
            if real_gain > 0:
                if A > C:
                    case = 'gain, currency rose'
                elif A < C:
                    case = 'gain, currency fell (taxed at nominal)'
                else:
                    case = 'gain, no currency change'
            elif loss > 0:
                case = 'loss, currency rose or unchanged (nominal loss)' if A >= C else 'loss, currency fell (real loss only)'
            else:
                case = 'no gain, no loss (currency movement absorbed it)'
            bucket = '30%' if t['symbol'] in substantial else '25%'
            pre05 = 0.0
            if lot['date'] <= FOREIGN_SPLIT_DATE and real_gain > 0:
                held = (t['date'] - lot['date']).days
                before = (FOREIGN_SPLIT_DATE - lot['date']).days
                if held > 0:
                    pre05 = real_gain * before / held
                issues.append(f"{t['symbol']} lot bought {lot['date']}: the part of the real gain for days up to 31.12.2004 goes in the 35% column of Form 1322. "
                              "Day count used: calendar days from the purchase date to 31.12.2004, purchase day not counted, over calendar days from purchase to sale; confirm")
            row.update({'cost_ils': round(C, 2), 'adjusted_cost_ils': round(A, 2), 'proceeds_ils': round(P, 2),
                        'nominal_ils': round(nominal, 2), 'inflationary_ils': round(inflationary, 2),
                        'real_gain_ils': round(real_gain - pre05, 2), 'real_gain_pre2005_ils': round(pre05, 2),
                        'allowable_loss_ils': round(loss, 2), 'bucket': bucket, 'case': case, 'status': 'ok'})
            out.append(row)
    open_pos = {}
    for sym, q in lots.items():
        qty = sum(l['qty'] for l in q)
        if qty > 1e-9:
            open_pos[sym] = round(qty, 6)
    return out, open_pos


# ---------------------------------------------------------------- income
def read_income_file(path, mapping, default_ccy, tax_sign, amount_is_net, year, issues, dropped):
    """Rows of one income file, with the withheld tax as a positive 'paid' figure.

    `amount` must be the GROSS payment before withholding (or pass --income-net).
    """
    rows = read_csv(path)
    raw = []
    for i, r in enumerate(rows, 2):
        where = f'{path} line {i}'
        d = parse_date(r[mapping['date']], where)
        if d.year != year:
            continue
        typ = (r.get(mapping['type'], '') or 'dividend').strip().lower()
        if 'withholding' in typ or typ in ('tax', 'wht'):
            typ = 'withholding'
        elif 'dividend' in typ:
            typ = 'dividend'
        elif 'interest' in typ:
            typ = 'interest'
        if typ not in ('dividend', 'interest', 'withholding'):
            issues.append(f'{where}: income type {typ!r} is not dividend, interest or withholding; left out (totals INCOMPLETE)')
            dropped[0] += 1
            continue
        raw.append({'d': d, 'typ': typ, 'where': where, 'sep_wht': typ == 'withholding',
                    'amt': parse_num(r[mapping['amount']], where),
                    'tax': parse_num(r.get(mapping['tax_withheld'], ''), where, allow_empty=True),
                    'ccy': (r.get(mapping['currency'], '') or default_ccy).strip().upper(),
                    'sym': (r.get(mapping['symbol'], '') or '').strip().upper(),
                    'country': (r.get(mapping['country'], '') or '').strip().upper()})
    for x in raw:
        if x['typ'] == 'withholding':
            x['tax'], x['amt'] = x['amt'], 0.0
            x['typ'] = 'dividend' if x['sym'] else 'interest'
    if tax_sign == 'auto':
        # Probe only rows that carry a positive payment, plus separate withholding rows.
        # Zero-amount refund rows are ignored here, so a large refund cannot flip the reading.
        probe = sum(x['tax'] for x in raw if x['amt'] > 0 or x['sep_wht'])
        tax_sign = 'negative' if probe < 0 else 'positive'
        if any(x['tax'] < 0 for x in raw) and any(x['tax'] > 0 for x in raw):
            issues.append(f'{path}: both positive and negative tax values; read as "{tax_sign} = withheld" from the sign of the '
                          'total on payment rows. If that is wrong, rerun with --tax-sign')
    for x in raw:
        x['paid'] = -x['tax'] if tax_sign == 'negative' else x['tax']
        if amount_is_net and x['amt'] > 0:
            x['amt'] += max(0.0, x['paid'])
    return raw


def load_income(files, default_ccy, rates, substantial, interest_rate, treaty, tax_sign, year, issues):
    dropped = [0]
    raw = []
    for path, mapping, amount_is_net in files:
        raw += read_income_file(path, mapping, default_ccy, tax_sign, amount_is_net, year, issues, dropped)
    groups = {}
    for x in raw:
        rate = rate_on(rates, x['ccy'], x['d'], issues, f"{x['typ']} {x['sym']} {x['d']}")
        if rate is None:
            issues.append(f"{x['where']}: no rate, {x['typ']} left out (totals INCOMPLETE)")
            dropped[0] += 1
            continue
        country = x['country'] or ('US' if x['ccy'] == 'USD' else 'UNKNOWN')
        key = (x['sym'], x['typ'], country)
        g = groups.setdefault(key, {'gross_ils': 0.0, 'tax_ils': 0.0, 'gross_fx': 0.0, 'tax_fx': 0.0, 'rows': 0,
                                    'reversal': False, 'assumed_us': not x['country'] and x['ccy'] == 'USD'})
        g['gross_ils'] += x['amt'] * rate
        g['tax_ils'] += x['paid'] * rate
        g['gross_fx'] += x['amt']
        g['tax_fx'] += x['paid']
        g['rows'] += 1
        if x['amt'] < 0 or x['paid'] < 0:
            g['reversal'] = True
    res = []
    for (sym, typ, country), g in groups.items():
        gross, ftax = g['gross_ils'], g['tax_ils']
        if gross > 0 and ftax < -0.005:
            issues.append(f'{typ} {sym}: net foreign tax is negative on a positive payment. The sign convention is probably wrong; '
                          'rerun with --tax-sign. Item left out (totals INCOMPLETE)')
            dropped[0] += 1
            continue
        if gross <= 0.005 and ftax < -0.005:
            issues.append(f'{typ} {sym}: a tax refund ({-ftax:,.2f} ILS) with no payment this year. It probably belongs to an earlier '
                          'year; it was not credited here. Check whether that year needs correcting')
        if g['reversal']:
            issues.append(f'{typ} {sym}: reversal or refund rows netted ({g["rows"]} rows). Check the net against the broker\'s annual tax report')
        if typ == 'dividend':
            il_rate = RATE_DIVIDEND_SUBSTANTIAL if sym in substantial else RATE_DIVIDEND
        else:
            il_rate = interest_rate
        il_tax = max(0.0, gross) * il_rate
        cap_treaty = None
        if typ == 'dividend' and country in treaty:
            cap_treaty = max(0.0, gross) * treaty[country]
        elif typ == 'dividend' and gross > 0 and ftax > 0.15 * gross:
            dropped[0] += 1   # credit not capped at a treaty rate: mark totals INCOMPLETE
            issues.append(f'dividend {sym} ({country}): withheld {ftax / gross:.1%} and no treaty rate given. '
                          'The credit shown is capped only at the Israeli tax; pass --treaty COUNTRY=rate. Tax withheld above the '
                          'treaty rate is likely not creditable in Israel; confirm with a CPA')
        creditable = max(0.0, ftax) if cap_treaty is None else min(max(0.0, ftax), cap_treaty)
        above_treaty = max(0.0, ftax) - creditable
        credit = min(creditable, il_tax)
        res.append({'symbol': sym, 'type': typ, 'country': country, 'assumed_country': g['assumed_us'],
                    'gross_fx': round(g['gross_fx'], 2), 'gross_ils': round(gross, 2),
                    'foreign_tax_ils': round(ftax, 2), 'treaty_cap_ils': None if cap_treaty is None else round(cap_treaty, 2),
                    'above_treaty_likely_not_creditable_ils': round(above_treaty, 2),
                    'creditable_ils': round(creditable, 2), 'israeli_rate': il_rate,
                    'israeli_tax_ils': round(il_tax, 2), 'credit_ils': round(credit, 2),
                    's205a_excess_ils': round(creditable - credit, 2), 'top_up_ils': round(il_tax - credit, 2)})
        tolerance = max(1.0, 0.005 * max(0.0, gross))   # broker cent rounding is not a treaty problem
        if above_treaty > tolerance:
            gfx, tfx = g['gross_fx'], g['tax_fx']
            if cap_treaty is not None and gfx > 0 and tfx > 0 and abs(tfx / (gfx + tfx) - treaty[country]) < 0.005:
                dropped[0] += 1   # the dividend figure itself is probably wrong: mark totals INCOMPLETE
                issues.append(f'{typ} {sym}: the tax is exactly the treaty rate of (amount + tax), so the amount column looks NET of '
                              'withholding. The amount must be the GROSS payment; remap it or add amount_is_net=yes to that '
                              "file's --income-map (totals INCOMPLETE)")
            else:
                issues.append(f'{typ} {sym}: foreign tax above the treaty rate ({above_treaty:,.2f} ILS) is likely not creditable in Israel; '
                              'confirm with a CPA, and ask the broker whether it can be corrected or reclaimed. For US payments the most '
                              'common cause is a missing or expired W-8BEN, though REIT, partnership and some fund distributions follow other rates')
    if any(i['assumed_country'] for i in res):
        issues.append('USD payments without a country column were treated as US-source; correct the country where that is wrong')
    return res, dropped[0]


# ---------------------------------------------------------------- summary
def tag(value, n):
    v = f'{value:,.2f}'
    return v if not n else f'{v}  (INCOMPLETE, {n} open row(s) or item(s) excluded)'


def summarise(rows, income, year, a):
    s = {'year': year}
    ok = [r for r in rows if r.get('status') == 'ok']
    n_open = len(rows) - len(ok) + a._income_dropped
    s['incomplete_rows'] = n_open
    s['sales_total_ils'] = round(sum(r['proceeds_ils'] for r in ok) + (a.israeli_sales or 0.0), 2)
    if a.israeli_sales is None and (a.israeli_gain or a.israeli_loss):
        s['note_field_256'] = 'sales_total excludes the Israeli (Form 867) accounts; pass --israeli-sales or add their sales total by hand'
    by = defaultdict(float)
    for r in ok:
        by[r['bucket']] += r['real_gain_ils']
        by['35%'] += r['real_gain_pre2005_ils']
    by = {k: v for k, v in by.items() if v}
    losses = sum(r['allowable_loss_ils'] for r in ok)
    own_loss = defaultdict(float)
    for r in ok:   # ASSUMPTION: a security's own loss is its net loss, after its own gains
        own_loss[r['symbol']] += r['allowable_loss_ils'] - r['real_gain_ils'] - r['real_gain_pre2005_ils']
    own_loss = defaultdict(float, {k: max(0.0, v) for k, v in own_loss.items()})
    s['real_gain_by_rate_before_losses'] = {k: round(v, 2) for k, v in by.items()}
    s['current_year_losses_ils'] = round(losses, 2)
    order = sorted(by, key=lambda x: -float(x.rstrip('%')))

    def apply(amount, columns):
        for k in order:
            use = min(amount, columns.get(k, 0.0))
            columns[k] = columns.get(k, 0.0) - use
            amount -= use
        return amount

    net = dict(by)
    # 1. Current-year foreign loss: foreign gains first (s.92(a)(3)), highest rate first (ASSUMPTION).
    left = apply(losses, net)
    # 2. Then Israeli-account gains passed in (Form 867).
    il_gain = a.israeli_gain or 0.0
    use_il = min(left, il_gain)
    left -= use_il
    il_gain -= use_il
    # 3. Israeli-account current-year loss: Israeli gains, then foreign gains (ASSUMPTION on order).
    il_loss = a.israeli_loss or 0.0
    use = min(il_loss, il_gain)
    il_loss -= use
    il_gain -= use
    il_loss = apply(il_loss, net)
    left += il_loss
    s['foreign_loss_set_against_israeli_gains_ils'] = round(use_il, 2)
    # 4. Dividends from securities taxed at no more than 25%, or paid on a loss-making security (s.92(a)(4)).
    #    A dividend taxed above 25% may take only the loss of that same security (s.92(a)(4)(a)),
    #    so those go first and are capped at the symbol's own loss; then dividends at 25% or less
    #    (s.92(a)(4)(b)), in symbol order. The law fixes neither order nor attribution: ASSUMPTION, printed.
    high = sorted([i for i in income if i['type'] == 'dividend' and i['gross_ils'] > 0
                   and i['israeli_rate'] > OFFSET_RATE_CAP and own_loss.get(i['symbol'], 0) > 0], key=lambda i: i['symbol'])
    low = sorted([i for i in income if i['type'] == 'dividend' and i['gross_ils'] > 0
                  and i['israeli_rate'] <= OFFSET_RATE_CAP], key=lambda i: i['symbol'])
    used_before = losses + (a.israeli_loss or 0.0) - left   # loss already used against gains
    saving, new_excess, used_div = 0.0, 0.0, 0.0
    for i in high + low:
        cap = own_loss[i['symbol']] if i['israeli_rate'] > OFFSET_RATE_CAP else i['gross_ils']
        off = min(left, i['gross_ils'], cap)
        if i['israeli_rate'] > OFFSET_RATE_CAP:
            own_loss[i['symbol']] -= off
            if used_before > 0.005:
                s.setdefault('assumption_notes', []).append(
                    f"{i['symbol']}: its own loss is taken as still available after {used_before:,.2f} of losses went against gains. "
                    f"If that offset is attributed to {i['symbol']}'s loss first, its dividend offset could be as low as "
                    f"{max(0.0, min(off, cap - used_before)):,.2f}")
        if off <= 0:
            continue
        left -= off
        used_div += off
        new_il = (i['gross_ils'] - off) * i['israeli_rate']
        new_credit = min(i['creditable_ils'], new_il)
        saving += i['top_up_ils'] - (new_il - new_credit)
        new_excess += i['credit_ils'] - new_credit
        i['offset_by_loss_ils'] = round(off, 2)
    s['loss_set_against_dividends_ils'] = round(used_div, 2)
    if used_div:
        s['ASSUMPTION_dividend_offset'] = ('the law does not fix how a loss is spread between dividends. Used here: each dividend taxed '
                                           'above 25% first takes the NET loss of that same security (after its own gains), then dividends '
                                           'at 25% or less take the rest, in symbol order. A CPA may allocate differently')
    if used_div:
        s['israeli_tax_saved_by_dividend_offset_ils'] = round(saving, 2)
        s['s205a_excess_credit_created_by_offset_ils'] = round(new_excess, 2)
    s['current_year_loss_to_carry_forward_ils'] = round(left, 2)
    # 5. Brought-forward loss: capital gain only (s.92(b)); not against dividends or interest.
    cf = a.carryforward_in or 0.0
    cf_left = apply(cf, net)
    use_cf_il = min(cf_left, il_gain)
    cf_left -= use_cf_il
    il_gain -= use_cf_il
    s['brought_forward_loss_used_ils'] = round(cf - cf_left, 2)
    s['loss_to_carry_forward_ils'] = round(left + cf_left, 2)
    s['net_gain_by_rate_after_losses'] = {k: round(v, 2) for k, v in net.items() if v > 0.004}
    if a.israeli_gain or a.israeli_loss:
        s['israeli_account_gain_left_ils'] = round(il_gain, 2)
        s['note_israeli_accounts'] = 'Israeli-account figures were taken as given (Form 867); tax already withheld there is credited on the return'
    s['estimated_tax_on_gains_ils'] = round(sum(v * float(k.rstrip('%')) / 100 for k, v in net.items()), 2)
    halves = defaultdict(lambda: [0.0, 0.0])
    for r in ok:
        halves[r['half']][0] += r['real_gain_ils'] + r['real_gain_pre2005_ils']
        halves[r['half']][1] += r['allowable_loss_ils']
    s['by_half_year'] = {h: {'real_gain_ils': round(g, 2), 'loss_ils': round(l, 2), 'net_ils': round(g - l, 2),
                             'note': ('no advance due for this half; still record it on that half\'s Form 1322' if g - l <= 0
                                      else 'whether an earlier-half or brought-forward loss reduces this advance is not determined here; ask a CPA')}
                         for h, (g, l) in sorted(halves.items())}
    if income:
        s['dividends_ils'] = round(sum(i['gross_ils'] for i in income if i['type'] == 'dividend'), 2)
        s['interest_ils'] = round(sum(i['gross_ils'] for i in income if i['type'] == 'interest'), 2)
        s['foreign_tax_ils'] = round(sum(i['foreign_tax_ils'] for i in income), 2)
        s['foreign_tax_credit_ils'] = round(sum(i['credit_ils'] for i in income), 2)
        s['above_treaty_likely_not_creditable_ils'] = round(sum(i['above_treaty_likely_not_creditable_ils'] for i in income), 2)
        s['s205a_excess_before_offset_ils'] = round(sum(i['s205a_excess_ils'] for i in income), 2)
        s['israeli_top_up_on_income_before_offset_ils'] = round(sum(i['top_up_ils'] for i in income), 2)
    if a.other_income is None and (a.other_capital_income or a.israeli_gain):
        s['surtax_basis'] = 'no surtax estimate: pass --other-income (0 if none) to get one'
    if a.other_income is not None:
        cap = (sum(v for v in net.values() if v > 0) + sum(max(0.0, i['gross_ils']) for i in income) - used_div
               + max(0.0, il_gain) + (a.other_capital_income or 0.0))
        total = a.other_income + cap
        if year in SURTAX_ALL_YEARS:
            sur = max(0.0, total - SURTAX_THRESHOLD) * SURTAX_ALL
            basis = f'3% on total taxable income above {SURTAX_THRESHOLD:,}'
            if year >= SURTAX_CAPITAL_FROM:
                sur += max(0.0, cap - SURTAX_THRESHOLD) * SURTAX_CAPITAL
                basis += ' plus 2% on capital-source income above it'
            else:
                basis += ' (the 2% capital-income limb starts in 2025)'
            s['surtax_estimate_ils'] = round(sur, 2)
            s['surtax_basis'] = (f'{basis}; inflationary amounts excluded; capital base includes Israeli-account gains and '
                                 f'--other-capital-income ({a.other_capital_income or 0:,.0f}); other (non-capital) income = {a.other_income:,.0f}')
        else:
            s['surtax_estimate_ils'] = None
            s['surtax_basis'] = f'threshold for {year} not carried by this script; check s.121B'
    return s


def print_report(rows, income, summary, issues, open_pos):
    n = summary['incomplete_rows']
    print('WORKING FIGURES ONLY. Not tax advice and not a filed return.\n')
    print('Per-lot (ILS):')
    hdr = f"{'account':14} {'symbol':8} {'buy':10} {'sell':10} {'qty':>8} {'cost':>11} {'adj.cost':>11} {'proceeds':>11} {'real gain':>10} {'loss':>9}  case"
    print(hdr)
    print('-' * len(hdr))
    for r in rows:
        acct = r['account'][:14]
        if r.get('status') != 'ok':
            print(f"{acct:14} {r['symbol']:8} {r['buy_date']:10} {r['sell_date']:10} {r['quantity']:>8g}  {r['status']}")
            continue
        g = r['real_gain_ils'] + r['real_gain_pre2005_ils']
        print(f"{acct:14} {r['symbol']:8} {r['buy_date']:10} {r['sell_date']:10} {r['quantity']:>8g} {r['cost_ils']:>11,.2f} "
              f"{r['adjusted_cost_ils']:>11,.2f} {r['proceeds_ils']:>11,.2f} {g:>10,.2f} {r['allowable_loss_ils']:>9,.2f}  {r['case']}")
    if income:
        print('\nDividends and interest, netted per symbol (ILS, each row at its payment-day rate):')
        for i in income:
            print(f"  {i['symbol']:8} {i['type']:8} {i['country']:7} gross {i['gross_ils']:>10,.2f}  foreign tax {i['foreign_tax_ils']:>9,.2f}  "
                  f"Israeli {int(round(i['israeli_rate'] * 100))}% {i['israeli_tax_ils']:>9,.2f}  credit {i['credit_ils']:>9,.2f}  top-up {i['top_up_ils']:>9,.2f}")
    print('\nSummary:')
    for k, v in summary.items():
        if v in ('', None, {}):
            continue
        if k in ('year', 'incomplete_rows') or isinstance(v, str):
            print(f'  {k}: {v}')
        elif isinstance(v, (int, float)):
            print(f'  {k}: {tag(v, n)}')
        else:
            print(f'  {k}: {v}' + (f'  (INCOMPLETE, {n} open row(s) or item(s) excluded)' if n else ''))
    print('\nOpen positions at the end of the file (compare with the broker\'s year-end position):')
    if not open_pos:
        print('  none')
    for acct, pos in open_pos.items():
        for sym, q in sorted(pos.items()):
            print(f'  {acct}: {sym} {q:g}')
    print('\nOpen items:')
    if not issues:
        print('  none found by the script (corporate actions, other accounts and residency are still yours to check)')
    for x in dict.fromkeys(issues):
        print(f'  - {x}')


def main():
    ap = argparse.ArgumentParser(description='Per-trade ILS capital gain working figures for foreign-broker trades (Israeli resident individual).',
                                 formatter_class=argparse.RawDescriptionHelpFormatter, epilog=__doc__)
    ap.add_argument('--trades', action='append', default=[], help='trades CSV, one per broker account; repeat for more accounts. Include earlier-year buys')
    ap.add_argument('--etoro', action='append', default=[], help='closed-positions CSV, one row per position (open and close dates); repeatable')
    ap.add_argument('--etoro-map', default='', help='canonical=YourColumn pairs for ' + ','.join(ETORO_CANONICAL) +
                    '. instrument (type) is required unless --assume-real-shares; direction (Long/Short) is used when present')
    ap.add_argument('--etoro-currency', default=None, help='currency of eToro open/close prices when the file has none (default --currency)')
    ap.add_argument('--assume-real-shares', action='store_true', help='eToro file has no type column and every row is a real long share')
    ap.add_argument('--rates', required=True, action='append', help='rates CSV: date,rate[,currency] or Bank of Israel SDMX CSV; repeat per currency')
    ap.add_argument('--year', required=True, type=int, help='tax year to report')
    ap.add_argument('--map', action='append', default=[], help='canonical=YourColumn pairs for ' + ','.join(CANONICAL) +
                    '. One --map applies to every --trades file; or give one --map per --trades, in the same order')
    ap.add_argument('--income', action='append', default=[], help='dividends/interest CSV: date,symbol,type,amount,currency,tax_withheld[,country]. '
                    'amount must be the GROSS payment before withholding. Repeat for each broker')
    ap.add_argument('--income-map', action='append', default=[], help='canonical=YourColumn pairs for ' + ','.join(INCOME_CANONICAL) +
                    '. One for all --income files, or one per file in the same order')
    ap.add_argument('--income-net', action='store_true', help='the amount column of the ONLY --income file is NET of withholding; '
                    'with several files put amount_is_net=yes in that file\'s --income-map instead')
    ap.add_argument('--tax-sign', choices=['auto', 'negative', 'positive'], default='auto',
                    help='how withheld tax is signed: negative = withheld is negative; auto = read from the sign of the total tax on payment rows, per file')
    ap.add_argument('--treaty', default='', help='extra treaty dividend caps as COUNTRY=rate pairs, e.g. DE=0.15 (US=0.25 built in)')
    ap.add_argument('--currency', default='USD', help='default currency when a row has none (default USD)')
    ap.add_argument('--substantial', default='', help='comma list of symbols where you hold 10%% or more of a means of control')
    ap.add_argument('--interest-rate', type=float, default=RATE_INTEREST_DEFAULT, help='Israeli rate on interest as a fraction (default 0.25)')
    ap.add_argument('--carryforward-in', type=float, help='capital loss brought forward from earlier years, ILS (Form 1344)')
    ap.add_argument('--israeli-gain', type=float, help='real capital gain this year in Israeli accounts (Form 867), ILS')
    ap.add_argument('--israeli-loss', type=float, help='capital loss this year in Israeli accounts (Form 867), ILS')
    ap.add_argument('--israeli-sales', type=float, help='total sales in Israeli accounts (Form 867), ILS, for field 256')
    ap.add_argument('--other-capital-income', type=float, help='other capital-source taxable income for the surtax (Israeli dividends, interest, rent...), ILS')
    ap.add_argument('--other-income', type=float, help='other taxable income in ILS, for a surtax estimate')
    ap.add_argument('--csv-out', help='write the per-lot table to this CSV')
    ap.add_argument('--json', action='store_true', help='print JSON instead of the text report')
    a = ap.parse_args()

    issues = []
    sub = {x.strip().upper() for x in a.substantial.split(',') if x.strip()}
    treaty = dict(TREATY_DIVIDEND)
    for part in [p for p in a.treaty.split(',') if p.strip()]:
        if '=' not in part:
            die(f'--treaty entry {part!r} must look like COUNTRY=rate')
        k, v = part.split('=', 1)
        v = v.strip()
        try:
            if v.endswith('%'):
                pct = float(v[:-1])
                if not (pct == 0 or 1 <= pct <= 100):
                    raise ValueError
                rate = pct / 100
            else:
                if '.' not in v and v != '0':
                    raise ValueError
                rate = float(v)
                if not 0 <= rate < 1:
                    raise ValueError
        except ValueError:
            die(f'--treaty {k}={v}: ambiguous. Give a decimal fraction such as 0.15, or a percent such as 15%')
        treaty[k.strip().upper()] = rate
    rates = load_rates(a.rates, a.currency.upper())
    if not a.trades and not a.etoro:
        die('give at least one --trades or --etoro file')
    if len(a.map) > 1 and len(a.map) != len(a.trades):
        die(f'{len(a.map)} --map values for {len(a.trades)} --trades files: give one --map, or one per file in the same order')
    maps = [parse_map(m, CANONICAL) for m in a.map] or [parse_map('', CANONICAL)]
    rows, open_pos, labels = [], {}, set()
    sources = [(p, 'trades', maps[idx] if len(maps) > 1 else maps[0]) for idx, p in enumerate(a.trades)]
    sources += [(p, 'etoro', parse_map(a.etoro_map, ETORO_CANONICAL)) for p in a.etoro]
    for path, kind, mapping in sources:
        if kind == 'trades':
            trades = load_trades(path, mapping, a.currency.upper(), issues)
        else:
            trades = load_etoro(path, mapping, (a.etoro_currency or a.currency).upper(), issues, a.assume_real_shares)
        acct = os.path.basename(path)
        if acct in labels:
            acct = path
        labels.add(acct)
        r, op = match(trades, rates, a.year, sub, issues, acct)
        rows += r
        if op:
            open_pos[acct] = op
    income, a._income_dropped = [], 0
    if a.income:
        if len(a.income_map) > 1 and len(a.income_map) != len(a.income):
            die(f'{len(a.income_map)} --income-map values for {len(a.income)} --income files: give one, or one per file in order')
        if a.income_net and len(a.income) > 1:
            die('--income-net is ambiguous with several --income files. Put amount_is_net=yes in the --income-map of the '
                'file whose amount column is net, and give one --income-map per file')
        imaps, nets = [], []
        for m in (a.income_map or ['']):
            parts = [x for x in m.split(',') if x.strip()]
            net = any(x.split('=', 1)[0].strip().lower() == 'amount_is_net' and x.split('=', 1)[1].strip().lower() in ('yes', 'true', '1')
                      for x in parts if '=' in x)
            rest = ','.join(x for x in parts if x.split('=', 1)[0].strip().lower() != 'amount_is_net')
            imaps.append(parse_map(rest, INCOME_CANONICAL))
            nets.append(net)
        if len(imaps) == 1 and len(a.income) > 1 and nets[0]:
            die('amount_is_net=yes in a single --income-map would apply to every --income file; give one --income-map per file')
        files = [(p, imaps[i] if len(imaps) > 1 else imaps[0], (nets[i] if len(imaps) > 1 else nets[0]) or a.income_net)
                 for i, p in enumerate(a.income)]
        income, a._income_dropped = load_income(files, a.currency.upper(), rates, sub, a.interest_rate, treaty,
                                                a.tax_sign, a.year, issues)
    summary = summarise(rows, income, a.year, a)
    if summary.get('ASSUMPTION_dividend_offset'):
        issues.append('ASSUMPTION: ' + summary['ASSUMPTION_dividend_offset'])
    for note in summary.get('assumption_notes', []):
        issues.append('ASSUMPTION: ' + note + '. A CPA may attribute the loss differently')
    if a.csv_out and rows:
        keys = sorted({k for r in rows for k in r})
        with open(a.csv_out, 'w', newline='', encoding='utf-8') as f:
            f.write(f'# {DISCLAIMER}\n')
            w = csv.DictWriter(f, fieldnames=keys)
            w.writeheader()
            w.writerows(rows)
    if a.json:
        print(json.dumps({'disclaimer': DISCLAIMER, 'rows': rows, 'income': income, 'summary': summary, 'open_positions': open_pos,
                          'open_items': list(dict.fromkeys(issues))}, indent=2, ensure_ascii=False))
    else:
        print_report(rows, income, summary, issues, open_pos)
    return 0


if __name__ == '__main__':
    sys.exit(main())
