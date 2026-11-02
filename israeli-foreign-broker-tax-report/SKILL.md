---
name: israeli-foreign-broker-tax-report
description: >-
  Not tax advice and not a filed return. Turns a foreign-broker statement (Interactive Brokers,
  eToro, Schwab, Fidelity CSV or pasted trades, dividends and withholding) into Israeli working
  figures for a resident individual, with per-trade shekel gains at Bank of Israel representative
  rates, real versus inflationary amount, Form 1325, 1322 and 1324 lines, loss offsets and open
  items. Use when the user asks "how do I report my IBKR account in Israel", "revach hon al
  menayot b'chul", "tofes 1322 broker zar", or which exchange rate applies. Prevents broker FX
  rate errors, offsetting currency-driven losses and a missed half-year report. Do NOT use for the
  whole annual return (israeli-tax-returns), crypto (israeli-crypto-tax-reporter), employee
  options or RSUs (israeli-stock-options-tax), analysing Israeli stocks (tase-stock-analysis), US
  citizens (us-israel-dual-tax-navigator, us-person-israeli-investment-check), or investment
  advice.
license: MIT
allowed-tools: "Bash(python3:*) Read Write"
compatibility: "Python 3.8+ for the optional bundled script (stdlib only, no network). Chat-only hosts (Claude.ai, ChatGPT, Claude Desktop without a shell, Manus, Grok) follow the inline route in Step 4; Gemini Spark can run the script but cannot fetch rates, so the user supplies the rates file."
---

# Israeli Foreign Broker Tax Report

## Legal notice

This is a free information tool operated by an AI model. It explains the tax rules and helps you organise your own figures. All of its outputs are produced automatically by an AI model, with no involvement, review, or approval by a tax adviser or accountant. The output is not a tax opinion, not a return prepared by a licensed representative, and not professional advice, but a general calculation and explanation only: it does not examine the full extent of your income or your complete documents. An AI model may err, omit data, or present a wrong conclusion.

Any form or text this tool produces is an automatic draft for your personal preparation only, and is not a filed return. Responsibility for reporting and for paying the tax is yours, the binding computation is the Tax Authority's, and representation before the Tax Authority is reserved to those permitted by law. This tool is not a substitute for advice that takes account of the particular circumstances and needs of each person. Consult a tax adviser or accountant before filing or paying. All use of its output is the user's sole responsibility.

The tool does not recommend buying, selling or holding any security, and its operators have no interest in the securities named in your statement. It never suggests selling, or the timing of a sale, for its tax effect (no loss harvesting and no timing advice), even when the user does not ask.

## Problem

An Israeli resident with an account at Interactive Brokers, eToro, Schwab or Fidelity gets a statement in dollars, but the Tax Authority wants every trade in shekels, split into a real gain and an inflationary amount, on Forms 1325, 1322 and 1324. When no Israeli withholding agent is involved, the conversion rule, the lot order, the loss limits and the half-year report are all on the investor. The usual mistakes (using the broker's FX rate, deducting a loss that only came from a falling dollar, putting broker cash interest with the securities) cost money or invite an assessment.

## What you need from the user

1. **The trades for the tax year AND every earlier purchase still being sold**: date, symbol, buy or sell, quantity, price per unit, commission, currency. A CSV export or pasted lines are both fine. Lot matching needs the old buys; a sale with no buy in the file cannot be computed.
2. **Dividends, interest and tax withheld** for the year, with payment dates, one file per broker (repeat `--income`). The amount must be the **gross** payment before withholding; for a report that shows only the net amount plus the tax, add `amount_is_net=yes` to that file's `--income-map` (with a single income file, `--income-net` also works; with several it is refused). See `references/broker-exports.md`.
3. **One file per broker account**, each with its own `--trades` (and its own `--map`, in the same order, when headers differ), or `--etoro` for a closed-positions report with one row per position. Lots are matched per portfolio manager, so do not merge brokers into one lot queue. Export layouts vary and change: read the user's actual file, save spreadsheets as CSV, and see `references/broker-exports.md`.
4. **Corporate actions**: splits, mergers, spin-offs, transfers in from another broker.
5. **Gate answers** (Step 1): Israeli resident individual? US citizen or green-card holder? 10% or more of any company in the statement? New immigrant or senior returning resident? Age 60 or over? Trading as a business?
6. **Is Israeli tax withheld on this account?** (an Israeli introducing broker, bank or member firm that issues Form 867). Branches in Step 1.
7. **Every other securities account** for the year, including Israeli bank accounts with Form 867: their gains and losses go on the same Form 1322.
8. **Loss brought forward** from earlier years (last year's Form 1344, in shekels), and whether the return for the loss year was filed.
9. **Half-year reports or advances already paid** for this year.
10. Optional: other taxable income for the year, for a surtax estimate.

If something is missing, say what it changes and ask; never fill a missing purchase price or date with a guess.

## Instructions

### Step 1: Gate the user before computing

Ask the gate questions and branch:

| Answer | What to do |
|---|---|
| US citizen or green-card holder | Stop and route to `us-israel-dual-tax-navigator` or `us-person-israeli-investment-check`: the US side (PFIC, foreign tax credit ordering) changes the numbers. |
| Holds 10% or more of a means of control in a company in the statement (at the sale or in the 12 months before) | Substantial shareholder: real gain on that company's shares is taxed at up to 30% (Section 91(b)(2)), dividends at 30% (Section 125B(2)). Pass `--substantial SYMBOL`. |
| Israeli tax is withheld on this account (Form 867 issued) | The gains reach Form 1322 from Form 867, not from Form 1325, and the half-year report does not apply to sales taxed at source (Section 91(d)(2c)(a)). Use this skill only to check the 867 figures; carry them with `--israeli-gain` / `--israeli-loss`. |
| New immigrant or senior returning resident | For new immigrants, Kol Zchut describes a 10-year exemption on foreign-source income, including capital gains on assets abroad. For a senior returning resident this skill makes no statement about the exemption: ask a CPA. In both cases do not decide eligibility, and do not read a tax exemption as an exemption from reporting: whether a report is still due depends on the aliyah or return date. Route to a CPA. |
| Age 60 or over | Reduced rates may apply to capital gains and interest (Kol Zchut). Compute at the standard rates and flag it as an open item. |
| Many trades, leverage, trading as a living | Business income is outside this skill: the capital-gain regime may not apply at all. Name the question and route to a CPA. |
| Wants to know what to buy or sell | Decline. This skill never recommends a trade. |

Check: every gate answer is recorded in the open-items list, even when it routes nowhere.

### Step 2: Normalise the statement

Map the export to the canonical columns `date, symbol, side, quantity, price, fee, currency`. Do not assume a broker's column names: read the header the user actually has and pass it with `--map`, for example `--map "date=TradeDate,symbol=Symbol,side=Buy/Sell,quantity=Quantity,price=TradePrice,fee=IBCommission,currency=CurrencyPrimary"` after confirming those headers exist in the file.

- Use the **trade date**, not the settlement date. Rule 7 of the Conversion Rules converts the cost at the purchase day or the payment date, whichever is earlier, and the consideration at the sale day or receipt date, whichever is earlier; the trade date is normally the earlier one.
- Commissions go INTO the cost and OUT of the consideration; periodic fees are excluded from both (Form 1325 explanations 3 and 5). Management and custody fees of the year are deductible from the consideration (Regulations on computing capital gain, 2002, regulation 6); list them separately.
- Rows that are not a plain buy or sell (split, merger, spin-off, transfer, option exercise, short sale) go to the open-items list. The script refuses them on purpose.
- CFD positions, crypto and shorts: map the type or asset-class column to `instrument`. CFD rows are excluded (treatment not covered; route to a CPA), Crypto rows are excluded and routed to `israeli-crypto-tax-reporter`, and short positions are excluded; all are open items that mark the totals INCOMPLETE and none is ever computed here. With `--etoro` the type mapping is required (or `--assume-real-shares`); a plain `--trades` file without one is computed and flagged. Reader details, symbol cleanup and currencies: `references/broker-exports.md`.
- Specific lots: when the records prove which lot was sold, map the lot's open date to `open_date`, or a position or lot id to `lot_ref` (the `--etoro` reader does this per position), and the script matches that lot (regulation 5). Without proof, FIFO.
- Withholding on separate rows: some brokers put dividends and withholding tax on separate lines. Map the type column so withholding rows read as `withholding`; the script folds them into the same symbol's dividend (or interest when the row has no symbol).
- US Treasury bills: the discount is interest (Section 125C counts discount as interest), reported on Form 1324, not a share sale. Keep T-bills out of the trades file and flag them; Treasury and other bonds stay open items.

Check: the number of shares bought minus sold per symbol matches the broker's year-end position. If it does not, a lot or a corporate action is missing.

### Step 3: Get the representative rates

The rate is the **Bank of Israel representative rate (שער יציג) of the day**, and if the Bank published no rate that day, the last rate it published before that day (Conversion Rules 2003, rule 1). Not the broker's FX rate, not a monthly or annual average.

Routes, in order of preference:

1. **`boi-exchange` MCP**: fetch the daily representative rate for each purchase, sale and payment date.
2. **Bank of Israel SDMX CSV** (agent with network): `https://edge.boi.gov.il/FusionEdgeServer/sdmx/v2/data/dataflow/BOI.STATISTICS/EXR/1.0/RER_USD_ILS?startperiod=2025-01-01&endperiod=2025-01-10&format=csv`, with the series code changed for another currency (`RER_EUR_ILS`) and the dates widened to cover the oldest purchase. The script reads this file as is.
3. **No network**: ask the user to download the rates from the Bank of Israel page https://www.boi.org.il/roles/markets/exchangerates/ (Excel or CSV) or to paste `date,rate` lines.

Check: the BoI file has a `UNIT_MULT` column. For the yen it is 2, so the published figure is per 100 yen; divide before use (the script does).

### Step 4: Compute each matched lot

Match sales to purchases **first in, first out**, per symbol, within one account. Regulation 5 deems identical securities sold in order of purchase unless the seller proves the purchase date and price of a specific lot; if the user has specific-lot records and wants to use them, say that the proof burden is theirs and compute FIFO alongside.

For each matched lot:

- **C** = cost in foreign currency (commissions in) x rate on the purchase day
- **P** = consideration in foreign currency (commissions out) x rate on the sale day
- **A** = cost in foreign currency x rate on the sale day. This is the cost adjusted by the currency, because Section 88 makes the currency rate the index for a foreign-currency security held by an individual (Form 1325 explanation 4 says the same).

Then apply the four cases settled in Civil Appeal 3555/15 (Moses, 12.9.16, further hearing denied):

| Currency between buy and sell | Result in shekels | Formula |
|---|---|---|
| Rose, and P is above A | Real gain; the rest of the nominal gain is the exempt inflationary amount | P - A |
| Fell, and P is above C | Gain taxed at the smaller **nominal** amount (no negative inflationary amount) | P - C |
| Rose, and P is below C | Loss allowed at its **nominal** amount | C - P |
| Fell, and P is below A | Only the **real** loss is allowed; the part caused by the falling currency is not | A - P |
| P between C and A (either direction) | No gain and no loss | 0 |

In one line: real gain = max(0, P - max(A, C)); allowable loss = max(0, min(A, C) - P).

**Shell hosts:** `python3 scripts/broker-gains-ils.py --trades trades.csv --rates usd.csv --year 2025 --income income.csv --csv-out per-trade.csv`.
**Chat-only hosts:** do the same arithmetic inline, lot by lot, showing C, A and P for every row so the user can check it. Above roughly 30 sales, tell the user the inline route is error-prone and suggest running the script on a computer.

Check: re-add the per-lot quantities to the sale quantity; recompute one row by hand before handing over the table.

### Step 5: Put each gain in its rate column

Form 1322 and Form 1325 keep one column (and one Form 1325) per tax rate:

- **25%**: real gain of an individual (Section 91(b)(1)).
- **30%**: substantial shareholder (Section 91(b)(2)).
- **35%**: for a foreign security bought before 2005, the part of the real gain for the days held up to 31.12.2004, computed as real gain x (days from purchase to 31.12.2004) / (days from purchase to sale); the rest stays at 25% (Form 1322 rate list). Day count used: calendar-day differences, the purchase day not counted. The form does not state a convention, so the lot is flagged.
- **15% / 20%**: unlinked bonds. For a foreign-currency bond held by an individual the currency is the index, so do not assume this row; flag the bond as an open item.

### Step 6: Offset losses in the statutory order

All of the year's accounts meet on one Form 1322: every foreign broker, plus Israeli accounts whose figures come from Form 867.

1. A current-year capital loss is set off first against real gain (Section 92(a)(1)); a loss on an asset abroad is set off first against capital gain abroad (Section 92(a)(3)), then against Israeli gains (`--israeli-gain`). A current-year Israeli-account loss (`--israeli-loss`) goes against Israeli gains, then foreign gains.
2. Left-over securities loss of the year must also offset ("יקוזז גם") dividends or interest paid on the same security, and dividends or interest from other securities only when taxed at no more than 25% (Section 92(a)(4); Form 1322 note 10). A 30% substantial-shareholder dividend from another company is outside the base. It never offsets interest on broker cash, which is not income from a security. When the offset dividend already bore foreign tax, the Israeli saving is only the top-up that would have been due; the unused credit becomes s.205A excess credit. The script prints both. The law fixes neither the order nor the attribution of this offset. The script's documented default: a dividend taxed above 25% first takes the net loss of that same security (after that security's own gains), then dividends at 25% or less take the rest, in symbol order. It prints this as an ASSUMPTION, with the lower figure that would result if earlier offsets used that security's loss first; a CPA may allocate differently.
3. A loss brought forward (`--carryforward-in`) comes after the current-year loss and goes against capital gain only, never against dividends or interest (Section 92(b); Form 1322 note 10), foreign gains first.
4. Whatever is left carries forward on Form 1344, in shekels (Conversion Rules, rule 8), and only survives if a return is filed for this year (Section 92(b)).
5. Across rate columns the script applies a loss to the highest-rate column first and labels that as an assumption; the user or their accountant decides the allocation on the form.

### Step 7: Dividends, interest and the foreign tax credit

- Convert each dividend and interest payment at the rate of the **day it was paid**, and the foreign tax at the rate of the day it was paid (Conversion Rules, rules 3 and 6). Never convert the annual total at a year-end rate.
- Keep the signs of reversals and refunds. Files differ: many brokers book withholding as a negative and a refund as a positive, while hand-made lists often do the opposite. `--tax-sign auto` reads the convention from the sign of the total tax on the payment rows and raises an open item when both signs appear; a negative net foreign tax on a positive dividend is refused as a likely sign error. Pass `--tax-sign negative` or `positive` when you know the convention. The script nets every symbol for the year before applying the credit caps, so a cancelled dividend leaves zero, and a dividend reversed and rebooked counts its tax once.
- Israeli rate: dividends 25% (30% substantial shareholder, Section 125B); interest up to 25% (Section 125C(b)). For a foreign-currency deposit the index is the currency rate (Section 125C definition), so do not assume the 15% unlinked-interest row; if the user's accountant says otherwise, rerun with `--interest-rate 0.15`.
- US dividends: the US-Israel treaty caps US tax on dividends to an individual at 25 percent of the gross (Article 12(2)(a)) when a valid W-8BEN is on file. If the broker withheld 30%, the most common cause is a missing or expired W-8BEN (REIT, partnership and some fund distributions follow other rates). This is the likely cause, not a certainty: confirm with the broker. Tax withheld above the treaty rate is likely not creditable in Israel (the script caps the credit at the treaty rate and labels the rest "likely not creditable"): confirm with a CPA, and ask the broker whether the withholding can be corrected or reclaimed. For other countries pass the treaty rate (`--treaty DE=0.15` or `DE=15%`, after checking the treaty); without it the script flags any dividend withheld above 15% and marks the totals INCOMPLETE.
- Credit: foreign tax is credited against the Israeli tax (Section 200) but never above the Israeli tax on that same income (Section 204(b)). Unused excess carries 5 years against foreign income from the same source (Section 205A), and Form 1324 has a column for it.
- Report on **Form 1324** (Appendix D): the 25% dividend row and the matching interest row, with the foreign tax beside each, on the basis of attached certificates. Foreign tax does NOT go on Form 1322; Form 1322 only needs a separate copy for sales that carry a creditable foreign tax (note 3).
- The US generally does not tax an Israeli resident's share gains (treaty Article 15(1)), subject to the exceptions that article lists (among them real property, property described in Article 14(2), a permanent establishment, and 183 days or more of presence), so ordinary share sales normally carry no foreign tax to credit.

### Step 8: Filing obligation, half-year report and surtax

**Annual return.** A foreign broker withholds no Israeli tax, so the filing exemption for "income from a security" (which needs full withholding) does not apply. The "foreign income" exemption needs an advance payment and a total of no more than NIS 375,000 (2023 to 2026), and is lost anyway with foreign assets or foreign bank balances of NIS 2,086,000 or more on any day, an unlisted foreign company, or surtax liability (Filing-Exemption Regulations 1988). In practice: unless an advance was paid, assume a return (Form 1301) is due. Details in `references/forms-and-filing.md`.

**Half-year report.** With no tax withheld and a duty to file under Section 131, the gain is reported on **31 July** (sales January to June) and **31 January** (sales July to December), with an advance (Section 91(d)(2c)(b)); Form 1322 note 6 wants a separate form per half (transaction code 65, code 56 = 30.6 or 31.12). The script's `by_half_year` gives the net per half; a loss-only half has no advance but is still recorded. The filing channel is not named here (ask the Tax Authority or a representative). If a deadline has passed: report and pay now and see a CPA; Section 91(d)(3) charges linkage and interest; do not estimate a fine. Advances paid, and tax withheld on the gain (Section 91(d)(6)), are credited against the year's tax; keep the confirmations. More in `references/forms-and-filing.md`.

**Surtax (mas yesef).** For 2024 to 2027: 3% on total taxable income above NIS 721,560 (Section 121B(a)). From 2025 only: a further 2% on capital-source income above the same threshold (Section 121B(a1); Tax Authority instruction 5/2025). For 2024 the 2% does not apply. Inflationary amounts are excluded (Section 121B(e)), and the surtax is settled in the annual return, not in the advance (Section 121B(b)). The script's capital-source base is this skill's net gains, dividends and interest, plus Israeli-account gains (`--israeli-gain`) and any other capital-source income you pass with `--other-capital-income` (Israeli dividends, interest, rent); anything not passed in is left out of the estimate.

**Form 1301 mapping.** Mapped: field 256 (total sales; pass `--israeli-sales` to include the Form 867 accounts), the dividend fields 141, 241, 341 through Form 1324, the Form 1322 ownership box (individual, registered spouse, spouse), the separate Form 1322 for inherited or pre-marriage securities (note 5), and Form 1301 section H by spouse. Other fields are not mapped: check the year's form or use `israeli-tax-returns`. Table in `references/forms-and-filing.md`.

### Step 9: Assemble the artifact

Produce the output below, then re-read the open items with the user. Anything there can change the totals. If any lot could not be computed, every total in the summary is marked INCOMPLETE with the number of rows left out; never copy an INCOMPLETE figure onto a form.

## Output

```
WORKING FIGURES ONLY. Not tax advice and not a filed return. Tax year: YYYY. Account: <broker, account>.
Rates: Bank of Israel representative rate of each day (Conversion Rules 2003, rules 1, 3, 6, 7).

A. Per-lot table (one row per matched lot; this is the Form 1325 working paper)
symbol | buy date | sell date | qty | cost FX | cost ILS (C) | adjusted cost ILS (A) | proceeds ILS (P) | real gain | allowable loss | rate column | case

B. Summary of form lines
Form 1325 (one per rate column): total real gain, total loss, total sales
Form 1322 (all accounts, Form 867 figures included): gains by rate column -> current-year loss -> dividend offset -> brought-forward loss -> loss carried forward
Form 1301 field 256: total sales
Half-year reports (Section 91(d)(2c)(b)): H1 net / H2 net
Form 1324: dividends at 25% + foreign tax (netted); interest + foreign tax; credit; above-treaty tax (likely not creditable, confirm); s.205A excess; Israeli top-up
Form 1344: loss brought in and used; loss carried forward (ILS)
Open positions at year end, per account (to reconcile with the broker)
Every total: "INCOMPLETE, N open row(s) excluded" when any row could not be computed
Surtax estimate (if other income given)

C. Open items
missing rates | unmatched sales | CFDs, crypto and shorts | currency mismatches | corporate actions | bonds and T-bills | gate flags (age 60+, oleh, substantial shareholder) | allocation assumptions
```

## Examples

### Example 1: IBKR account, shekel strengthened during the year

User says: "I have an IBKR account. In 2025 I sold 12 AAPL and 3 MSFT. Here are my trades and the dividend line."

Actions: gate (resident, not a US person, no 10% holdings); include the 2024 buys; fetch BoI rates; run the script.

```
Input: BUY 10 AAPL 2024-03-12 @173 +1 fee | BUY 5 AAPL 2024-08-05 @209 +1 | BUY 3 MSFT 2024-03-12 @400 +1
       SELL 3 MSFT 2025-04-07 @395 -1 fee | SELL 12 AAPL 2025-06-10 @202 -1
BoI USD rates: 2024-03-12 3.649 | 2024-08-05 3.824 | 2025-04-07 3.771 | 2025-06-10 3.495
MSFT 2024-03-12 -> 2025-04-07  C 4,382.45  A 4,528.97  P 4,464.86  gain 0.00  loss 0.00   no gain, no loss
AAPL 2024-03-12 -> 2025-06-10  C 6,316.42  A 6,049.85  P 7,056.99  gain 740.57            gain, currency fell (nominal)
AAPL 2024-08-05 -> 2025-06-10  C 1,599.96  A 1,462.31  P 1,411.40  loss 50.91             loss, currency fell (real only)
Net 25% column 689.66 | estimated tax 172.42 | sales total 12,933.25 | H1 net 689.66
```

Result: the AAPL second lot shows a nominal shekel loss of 188.56 but only 50.91 is allowable; the rest came from the falling dollar (Moses).

### Example 2: chat-only host, two pasted lines

User says (in Claude.ai): "Bought 10 VTI on 1.6.2004 at 55 dollars, sold them on 2.1.2025 at 300. Commission 1 dollar each way."

Actions: no script; ask the user for the two BoI rates or take them from the BoI page; compute inline and show the day split.

```
C = 551 x 4.552 = 2,508.15   A = 551 x 3.65 = 2,011.15   P = 2,999 x 3.65 = 10,946.35
Currency fell -> gain = P - C = 8,438.20
Days 1.6.2004-31.12.2004 = 213 of 7,520 held -> 239.01 in the 35% column, 8,199.19 in the 25% column
```

Result: two Form 1325 sheets (35% and 25%), plus an open item to confirm the day count.

### Example 3: loss year

User says: "I lost money on eToro this year and have dividends. Can I use the loss?"

Actions: ask for last year's Form 1344 and every other account (including Form 867); compute; apply the year's securities loss to real gains, then to dividends paid on that same security (at any rate, up to its own loss) and to dividends from other securities taxed at 25% or less; never to cash interest; show the real Israeli saving and any s.205A excess; carry the rest forward on Form 1344 and warn that the carry-forward survives only if this year's return is filed. Do not suggest selling anything to use the loss.

## Bundled Resources

### Scripts
- `scripts/broker-gains-ils.py`: FIFO matching per symbol, BoI-rate conversion with the last-published fallback, the four Moses cases, the 35% day split, loss offset, half-year totals, dividend and interest credit, surtax estimate, open items. Stdlib only, no network. Run: `python3 scripts/broker-gains-ils.py --help`.

### References
- `references/foreign-currency-gain-method.md`: the conversion rules, the index rule, the Moses cases with worked numbers, and what the script does not handle. Consult when a user disputes a figure or the currency moved during the holding period.
- `references/forms-and-filing.md`: Forms 1325, 1322, 1324, 1344 and 1301, the filing-obligation test, the half-year report, the dividend credit. Consult when assembling the summary block.
- `references/broker-exports.md`: how each kind of broker file is read (trades, closed positions, income), lot references, shorts, gross vs net income. Consult when mapping a new export.
- `references/domain-checklist.md`: coverage contract and known bad figures. Consult before updating the skill.

## Recommended MCP Servers

| MCP | Use it for | Without it |
|---|---|---|
| `boi-exchange` | Daily Bank of Israel representative rates for every trade and payment date | BoI SDMX CSV URL in Step 3, or the user downloads from the BoI page |
| `tase-mcp` | Only for an Israeli company dual-listed abroad (dual-listing flags), to confirm what the security is; needs a TASE API key | Ask the user or check the issuer's filings |

## Reference Links

| Source | URL | What to Check |
|---|---|---|
| Income Tax Ordinance (consolidated) | https://he.wikisource.org/wiki/פקודת_מס_הכנסה | Sections 88, 91, 92, 121B, 125B, 125C, 200 to 205A |
| Conversion Rules 2003 | https://he.wikisource.org/wiki/כללי_מס_הכנסה_(המרה_לשקלים_חדשים_של_סכומים_שמקורם_מחוץ_לישראל) | Which rate and which day |
| Tax Authority, 2025 annual report forms | https://www.gov.il/he/service/reporting-and-payment-2025-annual-tax-report-for-individuals | Forms 1322, 1324, 1325, 1344 for the year being filed |
| Bank of Israel representative rates | https://www.boi.org.il/roles/markets/exchangerates/ | Daily rates, CSV export |
| US-Israel income tax treaty (IRS) | https://www.irs.gov/pub/irs-trty/israel.pdf | Article 12 dividends, Article 15 capital gains |
| IRS, About Form W-8BEN | https://www.irs.gov/forms-pubs/about-form-w-8-ben | Treaty-rate withholding at a US broker |

## Gotchas

- Agents convert at the broker's FX rate or at an annual average. The law sets the Bank of Israel representative rate of the purchase day and of the sale day.
- Agents compute the gain once in shekels, or index the cost by the Israeli CPI. A foreign-currency share needs C, A and P with the currency as the index: when the shekel strengthened, a nominal shekel loss can be mostly a currency loss that cannot be offset.
- Agents put broker cash interest on Form 1322 and offset securities losses against it. It is deposit interest: Form 1324 and the 1301, and a securities loss does not reach it.
- Agents forget the loss brought forward, the Israeli accounts (Form 867) that share the same Form 1322, the filed-return condition for carrying a loss, and the half-year report.
- Agents suggest selling a losing position before year end to save tax. Never: no timing or loss-harvesting advice.

## Troubleshooting

### "MISSING RATE" in the per-lot table
Cause: the rates file does not cover that date (it ends before it, or starts after it, for example a 2004 purchase in a 2025 file). The last-published fallback is used only for a non-publication day inside the file's range. Solution: widen `startperiod` in the BoI CSV URL, or add a second `--rates` file.

### "UNMATCHED SALE"
Cause: the file has no purchase lot for part of a sale. Verified causes: buys from earlier years left out of the export, or shares transferred in from another broker. Solution: add the earlier buys (with the original date and cost) and rerun. A short sale also produces this; it is outside the script.

### US dividend tax withheld at 30%
Most often (not verifiable from the statement alone): no valid W-8BEN on file at the broker. REIT, partnership and some fund distributions can be withheld at other rates even with a valid form. The script credits only up to the treaty rate and the Israeli tax; whether the excess is creditable is a question for a CPA. Ask the broker about the W-8BEN and whether a reclaim is possible.

### Totals differ from the broker's "realized P&L"
Cause: the broker reports in dollars, at its own lot method, with no currency split. Expected: the shekel figures will not match. Check lot method (FIFO) and the trade dates first.
