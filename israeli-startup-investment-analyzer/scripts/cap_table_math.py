#!/usr/bin/env python3
"""Cap-table and dilution math for investment-memo sanity checks.

Deterministic helpers an investor can use to sanity-check the numbers in a
deck: priced-round dilution with an explicit pre-money vs post-money option
pool, SAFE / convertible conversion (valuation cap + discount, pre vs
post-money SAFE), STACKED SAFEs converting together, and pro-rata to maintain
ownership.

This computes ownership arithmetic only. It does NOT value the company, judge
the terms, or model liquidation preferences (preferences affect proceeds at
exit, not ownership percentages). Use the memo template for the qualitative
judgment and for the preference-stack walkthrough.

Usage:
  python3 cap_table_math.py priced --pre 8000000 --invest 2000000 --pool-pct 10 --pool-timing pre
  python3 cap_table_math.py priced --pre 8000000 --invest 2000000 --pool-pct 10 --pool-timing post
  python3 cap_table_math.py safe --safe 500000 --cap 6000000 --discount 20 --price-pre 8000000
  python3 cap_table_math.py safe --safe 500000 --cap 6000000 --post-money
  python3 cap_table_math.py stacked --price-pre 8000000 --invest 2000000 \
      --safe 500000:6000000:20 --safe 250000:8000000:0 --pool-pct 10
  python3 cap_table_math.py prorata --owned-pct 12 --pre 8000000 --invest 2000000 --pool-pct 10
"""

import argparse
import sys

# Percentage points within which two conversion factors are treated as a tie.
_TIE_EPS = 1e-9


def priced_round(pre_money, investment, new_pool_pct=0.0, pool_timing="pre"):
    """Priced round with an option-pool top-up taken pre-money or post-money.

    pool_timing="pre"  -> the "pool shuffle". The pool is carved out of the
      pre-money, so existing holders absorb ALL of the pool dilution and the
      new investor's percentage is unaffected by the pool.
    pool_timing="post" -> the pool is created after the money goes in, so the
      pool dilutes the new investor and existing holders proportionally.

    This distinction is the whole point of asking where the pool sits, and it
    is invisible unless the two cases produce different numbers.
    """
    if pool_timing not in ("pre", "post"):
        raise ValueError("pool_timing must be 'pre' or 'post'")
    pool_frac = new_pool_pct / 100.0
    if pool_frac >= 1.0:
        raise ValueError("--pool-pct must be under 100")
    post_money = pre_money + investment

    if pool_timing == "pre":
        # Investor buys investment/post_money of the company; the pool is carved
        # out of what remains, i.e. entirely from existing holders.
        investor_pct = investment / post_money * 100.0
        pool_pct = new_pool_pct
        existing_pct = 100.0 - investor_pct - pool_pct
        if existing_pct < 0:
            raise ValueError(
                "Pool plus new money exceeds the whole cap table; check --pool-pct")
        pool_borne_by = "existing holders only (pool carved out of pre-money)"
    else:
        # Pool created post-close: everyone is diluted pro-rata by the pool.
        investor_pct_pre_pool = investment / post_money * 100.0
        investor_pct = investor_pct_pre_pool * (1.0 - pool_frac)
        pool_pct = new_pool_pct
        existing_pct = 100.0 - investor_pct - pool_pct
        pool_borne_by = "investor and existing holders pro-rata (pool created post-money)"

    return {
        "pool_timing": pool_timing,
        "post_money": post_money,
        "investor_pct": investor_pct,
        "new_pool_pct": pool_pct,
        "existing_holders_pct": existing_pct,
        "dilution_of_existing_pct": 100.0 - existing_pct,
        "pool_dilution_borne_by": pool_borne_by,
    }


def safe_conversion(safe_amount, valuation_cap, discount_pct, price_round_pre,
                    post_money_safe=False):
    """Convert a single SAFE / convertible at the next priced round.

    The SAFE converts at the LOWER of the cap-based price and the
    discount-based price. post_money_safe=True treats the cap as a post-money
    cap (YC post-money SAFE): ownership is safe_amount / cap, locked before the
    new money dilutes it.
    """
    if post_money_safe:
        cap_ownership = safe_amount / valuation_cap * 100.0
        result = {
            "conversion_basis": "post-money cap (ownership locked before new money dilutes it)",
            "safe_holder_pct_of_cap": cap_ownership,
            "note": "Post-money SAFE: this percentage is fixed at the cap; the new round "
                    "money dilutes founders and employees, not this holder, "
                    "until the priced round closes.",
        }
        if discount_pct:
            result["discount_ignored"] = (
                "A post-money SAFE cap sets ownership directly, so --discount "
                "%.4g%% was NOT applied. If the instrument really has both a "
                "post-money cap and a discount, model the discount leg "
                "separately and take the better of the two for the holder."
                % discount_pct
            )
        return result

    if not price_round_pre or price_round_pre <= 0:
        raise ValueError(
            "--price-pre (pre-money of the priced round the SAFE converts into) "
            "is required for a pre-money SAFE. Pass --post-money for a YC-style "
            "post-money SAFE cap instead."
        )

    discount_price_factor = 1.0 - (discount_pct / 100.0)
    cap_factor = valuation_cap / price_round_pre
    if cap_factor < discount_price_factor - _TIE_EPS:
        basis = "cap"
        effective_factor = cap_factor
    elif discount_price_factor < cap_factor - _TIE_EPS:
        basis = "discount"
        effective_factor = discount_price_factor
    else:
        basis = "cap and discount tie"
        effective_factor = cap_factor

    effective_pre = price_round_pre * effective_factor
    safe_holder_pct = safe_amount / (effective_pre + safe_amount) * 100.0
    return {
        "conversion_basis": basis,
        "effective_valuation_for_safe": effective_pre,
        "safe_holder_pct_pre_new_money": safe_holder_pct,
        "note": "Single-SAFE view, before the new money and any pool. If more "
                "than one SAFE is outstanding, use the 'stacked' subcommand: "
                "SAFEs converting together dilute far more than any one of "
                "them read alone.",
    }


def stacked_safes(safes, price_round_pre, investment, new_pool_pct=0.0,
                  pool_timing="pre"):
    """Convert several SAFEs together into one priced round.

    safes: list of (amount, cap, discount_pct) tuples.

    Each SAFE converts at its own effective price, so each buys its own share
    count. Modelling them one at a time against the same pre-money (the naive
    approach) understates total dilution, which is exactly the trap the deck
    usually hides.
    """
    if not price_round_pre or price_round_pre <= 0:
        raise ValueError("--price-pre is required for stacked SAFE conversion")

    # Work in notional shares. Assume the pre-money represents 100 shares held
    # by existing holders, so one share costs price_round_pre / 100.
    base_shares = 100.0
    round_price_per_share = price_round_pre / base_shares

    rows = []
    safe_shares_total = 0.0
    for amount, cap, discount_pct in safes:
        discount_factor = 1.0 - (discount_pct / 100.0)
        cap_factor = cap / price_round_pre
        if cap_factor < discount_factor - _TIE_EPS:
            basis, factor = "cap", cap_factor
        elif discount_factor < cap_factor - _TIE_EPS:
            basis, factor = "discount", discount_factor
        else:
            basis, factor = "cap and discount tie", cap_factor
        safe_price_per_share = round_price_per_share * factor
        shares = amount / safe_price_per_share
        safe_shares_total += shares
        rows.append({
            "amount": amount,
            "cap": cap,
            "discount_pct": discount_pct,
            "basis": basis,
            "effective_pre_for_this_safe": price_round_pre * factor,
            "shares": shares,
        })

    new_money_shares = investment / round_price_per_share
    subtotal = base_shares + safe_shares_total + new_money_shares

    pool_frac = new_pool_pct / 100.0
    if pool_frac >= 1.0:
        raise ValueError("--pool-pct must be under 100")

    if pool_timing == "pre":
        # Pool carved out of the pre-money: NO new shares are issued on top, the
        # pool is taken out of the existing holders' stake alone. Issuing pool
        # shares AND deducting them from the existing base would charge existing
        # holders for the pool twice.
        total = subtotal
        pool_shares = pool_frac * total
        existing_shares = base_shares - pool_shares
        if existing_shares < 0:
            raise ValueError(
                "Pool is larger than the existing holders' stake; check --pool-pct"
            )
    else:
        # Pool created post-close: new shares issued, diluting everyone pro-rata.
        total = subtotal / (1.0 - pool_frac) if pool_frac else subtotal
        pool_shares = total - subtotal
        existing_shares = base_shares

    out = {
        "safe_count": len(safes),
        "total_safe_money": sum(s[0] for s in safes),
        "pool_timing": pool_timing,
        "existing_holders_pct": existing_shares / total * 100.0,
        "all_safes_pct": safe_shares_total / total * 100.0,
        "new_money_pct": new_money_shares / total * 100.0,
        "pool_pct": pool_shares / total * 100.0,
        "total_dilution_of_existing_pct": 100.0 - (existing_shares / total * 100.0),
    }
    for i, r in enumerate(rows, 1):
        out["safe_%d" % i] = (
            "%.0f at cap %.0f / %.4g%% discount -> %s basis, %.2f%% of post"
            % (r["amount"], r["cap"], r["discount_pct"], r["basis"],
               r["shares"] / total * 100.0)
        )
    out["note"] = ("Ownership only. Preferences, MFN clauses and side letters "
                   "are not modelled; read them in the documents.")
    return out


def prorata(owned_pct, pre_money, investment, new_pool_pct=0.0,
            pool_timing="pre"):
    """Amount needed in the new round to maintain current ownership %.

    A naive pro-rata check (your % times the round size) holds your ownership
    ONLY when no new option pool is created. With a pre-money pool the pool
    dilutes you too, so the naive check leaves you short.
    """
    pool_frac = new_pool_pct / 100.0
    if pool_frac >= 1.0:
        raise ValueError("--pool-pct must be under 100")
    post_money = pre_money + investment
    target = owned_pct / 100.0
    naive_check = target * investment

    # `scale` is what an existing holder's stake shrinks to if they sit out.
    new_money_frac = investment / post_money
    if pool_timing == "pre":
        # Pool carved out of the pre-money: existing holders alone absorb it.
        scale = 1.0 - new_money_frac - pool_frac
    else:
        # Pool created post-close: it dilutes everyone, including the new money.
        scale = (1.0 - new_money_frac) * (1.0 - pool_frac)
    if scale < 0:
        raise ValueError("Pool plus new money exceeds the whole cap table; check --pool-pct")

    adjusted_check = target * (1.0 - scale) * post_money

    if pool_frac:
        pool_note = ("A %s-money pool of %.4g%% dilutes you as an existing holder, "
                     "so the naive check is short by %.2f. Sitting out leaves you "
                     "at %.2f%% instead of %.4g%%."
                     % (pool_timing, new_pool_pct, adjusted_check - naive_check,
                        target * scale * 100.0, owned_pct))
    else:
        pool_note = "No new pool modelled; the naive pro-rata check is correct."

    return {
        "post_money": post_money,
        "pool_timing": pool_timing if pool_frac else "n/a",
        "prorata_check_naive": naive_check,
        "prorata_check_to_maintain": adjusted_check,
        "note": pool_note,
    }


def _parse_safe_spec(spec):
    """Parse 'amount:cap:discount' into a tuple of floats."""
    parts = spec.split(":")
    if len(parts) not in (2, 3):
        raise argparse.ArgumentTypeError(
            "SAFE spec must be amount:cap or amount:cap:discount, got %r" % spec)
    try:
        amount = float(parts[0])
        cap = float(parts[1])
        discount = float(parts[2]) if len(parts) == 3 else 0.0
    except ValueError:
        raise argparse.ArgumentTypeError("SAFE spec fields must be numbers: %r" % spec)
    if amount <= 0 or cap <= 0:
        raise argparse.ArgumentTypeError("SAFE amount and cap must be positive: %r" % spec)
    return (amount, cap, discount)


def _fmt(d):
    for k, v in d.items():
        if isinstance(v, float):
            print("  %s: %s" % (k, format(v, ",.2f")))
        else:
            print("  %s: %s" % (k, v))


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    pr = sub.add_parser("priced", help="priced-round dilution")
    pr.add_argument("--pre", type=float, required=True, help="pre-money valuation")
    pr.add_argument("--invest", type=float, required=True, help="investment amount")
    pr.add_argument("--pool-pct", type=float, default=0.0,
                    help="new option pool as %% of post-money fully diluted")
    pr.add_argument("--pool-timing", choices=("pre", "post"), default="pre",
                    help="is the pool carved out of the pre-money (default, the "
                         "'pool shuffle', founders absorb it) or created "
                         "post-money (everyone absorbs it)?")

    sf = sub.add_parser("safe", help="single SAFE / convertible conversion")
    sf.add_argument("--safe", type=float, required=True, help="SAFE amount")
    sf.add_argument("--cap", type=float, required=True, help="valuation cap")
    sf.add_argument("--discount", type=float, default=0.0, help="discount %%")
    sf.add_argument("--price-pre", type=float, default=0.0,
                    help="pre-money of the priced round it converts into "
                         "(REQUIRED unless --post-money)")
    sf.add_argument("--post-money", action="store_true",
                    help="treat cap as a post-money (YC) SAFE cap")

    st = sub.add_parser("stacked", help="several SAFEs converting together")
    st.add_argument("--safe", type=_parse_safe_spec, action="append", required=True,
                    metavar="AMOUNT:CAP[:DISCOUNT]",
                    help="repeat once per outstanding SAFE, e.g. 500000:6000000:20")
    st.add_argument("--price-pre", type=float, required=True,
                    help="pre-money of the priced round they convert into")
    st.add_argument("--invest", type=float, required=True, help="new money in the round")
    st.add_argument("--pool-pct", type=float, default=0.0,
                    help="new option pool as %% of post-money fully diluted")
    st.add_argument("--pool-timing", choices=("pre", "post"), default="pre")

    pp = sub.add_parser("prorata", help="pro-rata check to hold ownership")
    pp.add_argument("--owned-pct", type=float, required=True)
    pp.add_argument("--pre", type=float, required=True)
    pp.add_argument("--invest", type=float, required=True)
    pp.add_argument("--pool-pct", type=float, default=0.0,
                    help="new option pool as %% of post-money fully diluted")
    pp.add_argument("--pool-timing", choices=("pre", "post"), default="pre")

    a = p.parse_args()
    try:
        if a.cmd == "priced":
            _fmt(priced_round(a.pre, a.invest, a.pool_pct, a.pool_timing))
        elif a.cmd == "safe":
            _fmt(safe_conversion(a.safe, a.cap, a.discount, a.price_pre, a.post_money))
        elif a.cmd == "stacked":
            _fmt(stacked_safes(a.safe, a.price_pre, a.invest, a.pool_pct, a.pool_timing))
        elif a.cmd == "prorata":
            _fmt(prorata(a.owned_pct, a.pre, a.invest, a.pool_pct, a.pool_timing))
    except ValueError as e:
        print("error: %s" % e, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
