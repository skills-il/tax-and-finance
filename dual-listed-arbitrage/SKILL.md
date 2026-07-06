---
name: dual-listed-arbitrage
license: MIT
description: >-
  Detect price gaps between TASE and US listings of the same dual-listed company (Check Point, NICE, CyberArk, Teva, and 40+ pairs), converting via the Bank of Israel representative rate and flagging gaps above a threshold. Use when the user asks to compare a dual-listed stock's Tel Aviv vs NASDAQ/NYSE price, spot cross-listing arbitrage, or understand a premium/discount between exchanges. Provides per-pair gap %, trading-hours-overlap confidence, and currency-adjusted comparison. Do NOT use for single-market analysis (use tase-stock-analysis).
allowed-tools: "Bash(python:*) WebFetch"
---

# Dual-Listed Arbitrage

Compare the Tel Aviv and US prints of the same dual-listed company and report the
currency-adjusted premium/discount. Treat the headline number as a monitor, not a
free-money signal: for these fungible shares most of the gap is quote-timing, FX
timing, and bid/ask, and closing a real gap means transferring shares between the
registers (days of settlement plus cost).

## Instructions

### Step 1 - Load the pair registry
references/dual-listed-pairs.md lists 43 TASE/US pairs with their conversion ratio
and per-pair alert thresholds. Never hardcode a pair from memory.

### Step 2 - Fetch both legs
TASE price in agorot (divide by 100 for shekels) and the US price in USD. yfinance
is occasionally inconsistent about the Tel-Aviv leg's currency tag (it may report
ILS while the number is still agorot); if the converted TASE price differs from the
US-implied shekel price by roughly a factor of 100, treat it as a scaling error and
skip the pair rather than charting a fake ~100x gap.

### Step 3 - Convert via the BoI representative rate
Use the Bank of Israel sha'ar yatzig (a single daily fix, reference data around
midday, published ~15:30 Israel time). See references/boi-fx.md. Do not use an
intraday indicative rate for the headline. Note that the representative rate is
itself timed near midday, hours before the US session, so it is already stale
relative to a US close; use it as the reconciliation reference, not as a
same-instant FX for a US print.

### Step 4 - Apply the conversion ratio (usually 1:1)
Dual-listed ordinary shares (Check Point, NICE, CyberArk, Sapiens) are the SAME
fungible security registered on both exchanges under Israel's dual-listing
arrangement, so the ratio is 1:1 by construction, there is no depositary ratio.
Only a true ADR program (a depositary receipt bundling N ordinaries) carries a
non-1 ratio, and even Teva's ADR is 1:1. Default to 1:1; apply a non-1 ratio ONLY
for a genuine ADR, read from its depositary agreement / SEC Form F-6, never assumed.

    tase_ils  = tase_agorot / 100
    us_in_ils = us_usd * boi_rate * ratio      # ratio = 1 for dual-listed ordinaries
    gap_pct   = (tase_ils - us_in_ils) / us_in_ils * 100

### Step 5 - Check that the two legs are synchronous
The gap is only meaningful if both prints are from the same session. The US regular
session (about 16:30 to 23:00 Israel time) runs almost entirely after the TASE close
(~17:15), so a naive last-close-vs-last-close comparison can pull the two legs from
different calendar days, and the measured gap is then an overnight move, not a live
dislocation. If the
two legs' as-of dates differ (or one exchange was closed on that date, e.g. a US
holiday or an Israeli chag), mark the pair non-synchronous and low-confidence rather
than flagging it as a real gap. Surface BOTH as-of dates.

### Step 6 - Score and flag
Confidence rises when both markets trade live at the same moment. Since TASE moved
to a Monday-Friday week (5 Jan 2026), Friday closes early (~14:00 Israel time),
before the US open, so Friday has no live overlap at all. Even Mon-Thu the live
overlap is only the last ~45 minutes of the TASE session (the US regular session
opens ~16:30 Israel time; TASE continuous trading closes ~17:15), so for most of the
TASE day the US market is closed and the TASE print is being compared to the prior US
close. Flag pairs whose |gap| exceeds the per-pair threshold (default 2%), but treat
a flag on a non-synchronous or thinly-traded leg as a likely artifact. Note
settlement and FX-conversion caveats.

## Examples
User says: "Compare Check Point on TASE vs NASDAQ"
Result: TASE price (ILS), NASDAQ price converted to ILS at the representative rate
(ratio 1:1), gap %, both as-of dates, and an overlap-confidence note.

User says: "Scan CHKP, NICE, and TEVA for cross-listing gaps and show me a chart"
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

    python scripts/chart.py --pairs CHKP,NICE,TEVA --out gaps.html
    python scripts/chart.py --pairs CHKP,NICE --boi-rate 3.65 --out gaps.html

Omit --boi-rate to fetch USDILS=X live; supply it to pin the representative rate. A
pair whose Tel-Aviv leg is unavailable is reported as skipped.

## Gotchas
- Agorot vs shekel: TASE quotes in agorot, divide by 100 or prices look 100x. If the TASE leg comes out ~100x off, the agorot/shekel scaling is wrong.
- Dual-listed ordinaries are the same fungible share (1:1); only a true ADR carries a depositary ratio, verify it from the F-6, never assume a non-1 ratio.
- Non-synchronous legs: a TASE close and a US close from different sessions produce an overnight-move "gap", not a live dislocation. Check both as-of dates before trusting a flag.
- Friday TASE closes early (~14:00), before the US open, so no live overlap that day; even Mon-Thu the live overlap is only the last ~45 minutes of the TASE session.
- The gap is not risk-free profit: it is mostly a quote-timing and FX-timing artifact, and capturing a real gap means transferring shares between registers (days plus cost).

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| TASE trading & vacation schedule | https://www.tase.co.il/en/content/knowledge_center/trading_vacation_schedule | Current Mon-Fri session times and the Friday early close |
| Bank of Israel exchange rates | https://www.boi.org.il/en/economic-roles/financial-markets/exchange-rates/ | The daily representative (sha'ar yatzig) USD/ILS rate |

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
- scripts/viz.py - self-contained interactive HTML/SVG chart generator.
- references/dual-listed-pairs.md - the 43-pair registry with conversion ratios.
- references/boi-fx.md - representative-rate usage and timing.
- references/domain-checklist.md - the coverage contract for this skill.
