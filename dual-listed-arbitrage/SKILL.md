---
name: dual-listed-arbitrage
license: MIT
description: >-
  Detect price gaps between TASE and US listings of the same dual-listed company (NICE, Teva, Elbit, Tower, Palo Alto Networks, and about 30 registered pairs), converting via the Bank of Israel representative rate and flagging gaps above a threshold. Use when the user asks to compare a dual-listed stock's Tel Aviv vs NASDAQ/NYSE price, spot cross-listing arbitrage, or understand a premium/discount between exchanges. Provides per-pair gap %, trading-hours-overlap confidence, and currency-adjusted comparison. Do NOT use for single-market analysis (use tase-stock-analysis).
allowed-tools: "Bash(python:*) WebFetch"
---

# Dual-Listed Price Gap Tracker

## Legal notice

This is a free information tool operated by an AI model. It gathers data that has been published to the public and presents it in an organised form. The operators of this tool hold no personal interest in the securities or financial assets it mentions, and receive no consideration, commission, or benefit of any kind for presenting them. All of its outputs are produced automatically by an AI model, with no involvement, review, or approval by a licensed investment adviser.

The output is not investment advice, not investment marketing, and not a recommendation to buy, sell, or hold any security or financial asset. It is not a substitute for advice that takes account of the particular circumstances and needs of each person, and it does not consider your financial position, your investment objectives, or the risk you are able to bear. Market data may be partial, delayed, or wrong, and an AI model may err, omit data, or present a wrong conclusion. Consult a licensed adviser before any investment decision and verify every figure against the official source. All use of its output is the user's sole responsibility.


Compare the Tel Aviv and US prints of the same dual-listed company and report the
currency-adjusted premium/discount. Treat the headline number as a monitor, not a
free-money signal: for these fungible shares most of the gap is quote-timing, FX
timing, and bid/ask, and closing a real gap means transferring shares between the
registers (days of settlement plus cost).

## Instructions

### Step 1 - Load the pair registry
references/dual-listed-pairs.md (mirrored in scripts/registry.py) lists 29 TASE/US
pairs with their US ticker, conversion ratio and per-pair alert threshold, drawn
from the TASE "Dual Listed" securities list (52 records on 15 Sep 2026). Never
hardcode a pair from memory, and never assume the US ticker equals the TASE
symbol: the Tel-Aviv line CYBR is Palo Alto Networks, whose US ticker is PANW. A
famous Israeli name is not necessarily dual-listed: Check Point trades on Nasdaq
only, so there is no Tel-Aviv leg to compare. If a requested company is not in
the registry, say so instead of estimating.

### Step 2 - Fetch both legs
TASE price in agorot (divide by 100 for shekels) and the US price in USD. yfinance
is occasionally inconsistent about the Tel-Aviv leg's currency tag (it may report
ILS while the number is still agorot); if the converted TASE price differs from the
US-implied shekel price by roughly a factor of 100, treat it as a scaling error and
skip the pair rather than charting a fake ~100x gap.

### Step 3 - Convert via the BoI representative rate
Use the Bank of Israel sha'ar yatzig, published once per foreign-currency business
day and based on the market rate at the time it is set. See references/boi-fx.md.
Do not use an intraday indicative rate for the headline. The rate is set during the
Israeli business day, hours before the US close, so it is already stale relative
to a US close; use it as the reconciliation reference, not as a same-instant FX
for a US print. Check the exact setting time on the BoI site rather than stating
one.

### Step 4 - Apply the conversion ratio (usually 1:1)
Dual-listed ordinary shares (Elbit Systems, Tower, Nova) are the SAME
fungible security registered on both exchanges under Israel's dual-listing
arrangement, so the ratio is 1:1 by construction, there is no depositary ratio.
Only a true ADR program (a depositary receipt bundling N ordinaries) carries a
non-1 ratio; Teva's ADS is 1:1, and any TASE dual listing whose US line did not
match at ratio 1 is left out of the registry until its ratio is read from the F-6.
Use the registry ratio; apply a non-1 ratio ONLY for a genuine ADR, read from its
depositary agreement / SEC Form F-6, never assumed.

    tase_ils  = tase_agorot / 100
    us_in_ils = us_usd * boi_rate * ratio      # ratio = 1 for dual-listed ordinaries
    gap_pct   = (tase_ils - us_in_ils) / us_in_ils * 100

### Step 5 - Check that the two legs are synchronous
The gap is only meaningful if both prints are from the same session. The US regular
session (9:30 to 16:00 New York time) runs almost entirely after the TASE pre-close
(17:14-17:15 Israel time), so a naive last-close-vs-last-close comparison can pull the two legs from
different calendar days, and the measured gap is then an overnight move, not a live
dislocation. If the
two legs' as-of dates differ (or one exchange was closed on that date, e.g. a US
holiday or an Israeli chag), mark the pair non-synchronous and low-confidence rather
than flagging it as a real gap. Surface BOTH as-of dates. Even when both dates
match, two daily closes are hours apart, because the whole US afternoon trades
after TASE closes, so a close-to-close gap is never simultaneous. scripts/chart.py
therefore marks every close-to-close pair non-synchronous and says whether the
dates also differ.

### Step 6 - Score and flag
Confidence rises when both markets trade live at the same moment. Since TASE moved
to a Monday-Friday week, Friday enters pre-closing at 13:34-13:35 Israel time,
before the US open, so Friday has no live overlap at all. Even Mon-Thu the live
overlap is only the stretch from the US open to the TASE pre-close, under an hour on most days (the US regular session
opens at 9:30 New York time, normally 16:30 Israel time, but the Israel-time
equivalent shifts by an hour for a few weeks a year because the US and Israel
change clocks on different dates, so convert with that day's real offsets; TASE
enters pre-closing at 17:14-17:15), so for most of the
TASE day the US market is closed and the TASE print is being compared to the prior US
close. Flag pairs whose |gap| exceeds the per-pair threshold (default 2%), but treat
a flag on a non-synchronous or thinly-traded leg as a likely artifact. Because every close-to-close pair is non-synchronous, confirming a real gap needs two intraday prices taken inside that overlap window. Note
settlement and FX-conversion caveats.

## Examples
User says: "Compare NICE on TASE vs NASDAQ"
Result: TASE price (ILS), NASDAQ price converted to ILS at the representative rate
(ratio 1:1), gap %, both as-of dates, and an overlap-confidence note.

User says: "Compare Check Point in Tel Aviv and New York"
Result: a plain statement that Check Point is listed on Nasdaq only and has no
Tel-Aviv leg, so there is no gap to compute. No number is estimated.

User says: "Scan NICE, TEVA, and CYBR for cross-listing gaps and show me a chart"
Result: per-pair gap % (premium or discount) each checked against its threshold,
plus an optional interactive HTML diverging-bar chart written via scripts/chart.py.
Any pair whose Tel-Aviv leg is missing from the free source is listed as unavailable,
not estimated; any pair whose two legs are from different sessions is marked
non-synchronous.

## Visualization (optional)
A chart is produced ONLY when it helps the answer or the user asks, never forced,
never ASCII. To compare several pairs at once, scripts/chart.py renders a
self-contained interactive HTML diverging-bar chart: premium (TASE above US) in blue
and discount (TASE below US) in red, measured from a neutral zero baseline, with
hover detail, a table view, and a light/dark toggle. Non-synchronous pairs are called
out in a caveat note.

    python scripts/chart.py --pairs NICE,TEVA,CYBR --out gaps.html
    python scripts/chart.py --pairs NICE,ESLT --boi-rate 3.05 --out gaps.html

--pairs takes TASE symbols and the US ticker is resolved from the registry. Omit
--boi-rate to fetch USDILS=X live; supply it to pin the representative rate. A
pair whose Tel-Aviv leg is unavailable, or a symbol not in the registry, is
reported as skipped.

## Gotchas
- Agorot vs shekel: TASE quotes in agorot, divide by 100 or prices look 100x. If the TASE leg comes out ~100x off, the agorot/shekel scaling is wrong.
- Dual-listed ordinaries are the same fungible share (1:1); only a true ADR carries a depositary ratio, verify it from the F-6, never assume a non-1 ratio.
- The TASE symbol is not always the US ticker (TASE CYBR is US PANW), and acquisitions and delistings change the universe (Sapiens is not on the current list; Check Point trades on Nasdaq only). Resolve every pair through the registry.
- Non-synchronous legs: a TASE close and a US close from different sessions produce an overnight-move "gap", not a live dislocation. Check both as-of dates before trusting a flag.
- Friday TASE enters pre-closing at 13:34-13:35, before the US open, so no live overlap that day; even Mon-Thu the live overlap is only the stretch between the US open and the TASE pre-close at 17:14-17:15, and the US open's Israel time shifts by an hour in the weeks when the two countries' clock changes do not coincide.
- The gap is not risk-free profit: it is mostly a quote-timing and FX-timing artifact, and capturing a real gap means moving shares between the Tel-Aviv and US lines (days plus cost). Where the US line is an ADS (Teva), that move goes through the depositary, which charges its own fees under the deposit agreement, on top of commissions on both legs and the FX spread.
- A flag can also come from an ex-dividend date that falls on different sessions, a trading halt on one exchange, a TASE holiday or shortened interim-holiday session, or a thin TASE last price that is hours old. Rule these out before calling a gap a dislocation.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| TASE trading & vacation schedule | https://www.tase.co.il/en/content/knowledge_center/trading_vacation_schedule | Current Mon-Fri session times and the Friday early close |
| Bank of Israel exchange rates | https://www.boi.org.il/en/economic-roles/financial-markets/exchange-rates/ | The daily representative (sha'ar yatzig) USD/ILS rate |
| TASE dual-listed securities list | https://market.tase.co.il/en/market_data/securities/data/all?dType=1&cl1=1&cl2=7 | Which companies are currently dual-listed, and their TASE symbols |

## Troubleshooting

### Error: "Gap looks implausibly large"
Cause: agorot not converted (a ~100x scaling error), or a non-1 ratio wrongly applied to a fungible 1:1 ordinary.
Solution: divide the TASE leg by 100; use ratio 1 for dual-listed ordinaries and reserve a non-1 ratio for genuine ADRs read from the F-6.

### Error: "Stale / mismatched FX or legs"
Cause: an intraday indicative rate instead of the representative rate, or two legs from different sessions.
Solution: use the daily BoI sha'ar yatzig (marking intraday as indicative only); compare the two legs' as-of dates and treat a non-synchronous pair as low-confidence.

## Bundled Resources
- scripts/dual_diff.py - currency-adjusted gap for one pair from manual inputs.
- scripts/provider.py - robust US + Tel-Aviv (.TA) fetch and USD/ILS rate; retries then raises, and never fabricates a missing leg or rate.
- scripts/chart.py - optional orchestrator: diverging-bar gap chart (HTML), with a non-synchronous-legs guard.
- scripts/registry.py - TASE symbol to US ticker, ratio and threshold; raises for an unregistered symbol.
- scripts/viz.py - self-contained interactive HTML/SVG chart generator.
- references/dual-listed-pairs.md - the pair registry, its source, and the unregistered listings.
- references/boi-fx.md - representative-rate usage and timing.
- references/domain-checklist.md - the coverage contract for this skill.
