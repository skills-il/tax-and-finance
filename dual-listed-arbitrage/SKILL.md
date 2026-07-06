---
name: dual-listed-arbitrage
license: MIT
description: >-
  Detect price gaps between TASE and US listings of the same dual-listed company (Check Point, NICE, CyberArk, Teva, and 40+ pairs), converting via the Bank of Israel representative rate and flagging gaps above a threshold. Use when the user asks to compare a dual-listed stock's Tel Aviv vs NASDAQ/NYSE price, spot cross-listing arbitrage, or understand a premium/discount between exchanges. Provides per-pair gap %, trading-hours-overlap confidence, and currency-adjusted comparison. Do NOT use for single-market analysis (use tase-stock-analysis or global-stock-analysis).
allowed-tools: "Bash(python:*) WebFetch"
metadata:
  author: yonyon-ai
  version: 1.0.0
  category: tax-and-finance
  display_name: { he: "ארביטראז' חברות דואליות", en: "Dual-Listed Arbitrage" }
  tags:
    en: [dual-listed, arbitrage, tase]
    he: [דואליות, ארביטראז, בורסה]
---

# Dual-Listed Arbitrage

## Instructions

### Step 1 — Load the pair registry
references/dual-listed-pairs.md lists 43 TASE/US pairs with ADR ratios and
per-pair alert thresholds.

### Step 2 — Fetch both legs
TASE price in agorot (divide by 100 for shekels) and the US price in USD.

### Step 3 — Convert via the BoI representative rate
Use the Bank of Israel sha'ar yatzig (published ~15:30). See
references/boi-fx.md. Do not use an intraday indicative rate for the headline.

### Step 4 — Compute the gap
    tase_ils  = tase_agorot / 100
    us_in_ils = us_usd * boi_rate * adr_ratio
    gap_pct   = (tase_ils - us_in_ils) / us_in_ils * 100

### Step 5 — Score and flag
Confidence rises when both markets trade simultaneously (Mon-Thu overlap; Fri
TASE closes 13:50). Flag pairs whose |gap| exceeds the per-pair threshold
(default 2%). Note settlement (T+1) and FX-conversion caveats.

## Examples
User says: "Compare Check Point on TASE vs NASDAQ"
Result: TASE price (ILS), NASDAQ price converted to ILS at the representative
rate, gap %, and an overlap-confidence note.

User says: "Scan CHKP, NICE, and TEVA for cross-listing gaps and show me a chart"
Result: per-pair gap % (premium or discount) each checked against its threshold,
plus an optional interactive HTML diverging-bar chart written via
scripts/chart.py. Any pair whose Tel-Aviv leg is missing from the free source is
listed as unavailable, not estimated.

## Visualization (optional)
A chart is produced ONLY when it helps the answer or the user asks — never
forced, never ASCII. To compare several pairs at once, scripts/chart.py renders
a self-contained interactive HTML diverging-bar chart: premium (TASE above US)
in blue and discount (TASE below US) in red, measured from a neutral zero
baseline, with hover detail, a table view, and a light/dark toggle.

    python scripts/chart.py --pairs CHKP,NICE,TEVA --out gaps.html
    python scripts/chart.py --pairs CHKP,NICE --boi-rate 3.65 --out gaps.html

Omit --boi-rate to fetch USDILS=X live; supply it to pin the representative
rate. A pair whose Tel-Aviv leg is unavailable is reported as skipped.

## Gotchas
- Agorot vs shekel: TASE quotes in agorot — divide by 100 or prices look 100x.
- ADR ratios differ across pairs — never assume 1:1.
- Friday TASE ends 13:50; US opens later — low overlap = lower confidence.
- The gap is not risk-free profit: settlement timing and FX costs erode it.

## Troubleshooting

### Error: "Gap looks implausibly large"
Cause: agorot not converted, or wrong ADR ratio.
Solution: divide TASE by 100; check the pair ADR ratio in the registry.

### Error: "Stale / mismatched FX"
Cause: intraday indicative rate instead of the representative rate.
Solution: use the daily BoI sha'ar yatzig; mark intraday as indicative only.

## Bundled Resources
- scripts/dual_diff.py — currency-adjusted gap for one pair from manual inputs.
- scripts/provider.py — robust US + Tel-Aviv (.TA) fetch and USD/ILS rate;
  retries then raises, and never fabricates a missing leg or rate.
- scripts/chart.py — optional orchestrator: diverging-bar gap chart (HTML).
- scripts/viz.py — self-contained interactive HTML/SVG chart generator.
- references/dual-listed-pairs.md — the 43-pair registry with ADR ratios.
- references/boi-fx.md — representative-rate usage and timing.
