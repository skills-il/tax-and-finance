---
name: sp500-nasdaq-screener
license: MIT
description: >-
  Screen the S&P 500 and NASDAQ-100 universe by technical and fundamental criteria to surface candidate stocks. Use when the user wants to filter or rank US stocks — 'S&P 500 names with RSI below 30', 'NASDAQ stocks above their 200-day average', oversold/overbought scans, or sector-relative screens. Returns a ranked table with the matched criteria per symbol. Do NOT use for single-symbol deep analysis (use global-stock-analysis) or Israeli TASE screening.
allowed-tools: "Bash(python:*) WebFetch"
metadata:
  author: yonyon-ai
  version: 1.0.0
  category: tax-and-finance
  display_name: { he: "סורק מניות S&P 500 / נאסד\"ק", en: "S&P 500 / NASDAQ Screener" }
  tags:
    en: [screener, sp500, nasdaq]
    he: [סינון, מדדים, שוק-הון]
---

# S&P 500 / NASDAQ Screener

## Instructions

### Step 1 — Load the universe
references/sp500-constituents.md and references/nasdaq100-constituents.md hold
dated snapshots; scripts/provider.py parses them into the symbol list.

### Step 2 — Parse the filter
Supported: indicator thresholds (RSI < 30), moving-average relations
(price > EMA200), fundamentals (P/E < 15), sector filters. See
references/screening-criteria.md.

### Step 3 — Batch-compute per symbol
Run: python scripts/screen.py --index sp500 --filter "rsi<30"
It batch-fetches EOD closes via scripts/provider.py (retry-with-backoff then
raise; a symbol with no data is skipped, not faked) and computes RSI/EMA per
symbol with scripts/indicators.py.

### Step 4 — Rank and return
Table: symbol, matched criteria, the ranking metric, sector. Note the
constituent-snapshot date.

## Examples
User says: "S&P 500 names oversold on RSI, sorted by market cap"
Result: ranked table of symbols with RSI < 30, largest first.

User says: "chart the 15 most-oversold NASDAQ-100 names"
Result: the ranked table plus an optional interactive HTML bar chart
(scripts/chart.py) — one accent-hued bar per symbol, direct-labelled with the
RSI value, with per-bar hover and a table view.

## Visualization (optional)
A chart is produced only when it clarifies the answer or the user asks — never
forced, never as ASCII. When it helps, scripts/chart.py renders a
self-contained interactive HTML bar chart: the matched symbols ranked by the
filter metric, one accent-hued (--s1) bar each with a direct symbol + value
label, a recessive axis, per-bar hover, a table view, and a light/dark toggle.
The ranked text table stays the primary output.

## Gotchas
- Constituent lists drift on rebalance — output notes the snapshot date.
- A full 500-symbol scan is heavy; cap and cache.

## Troubleshooting

### Error: "Scan too slow / rate limited"
Cause: per-symbol live calls across the whole universe.
Solution: batch, cache EOD locally, cap universe size per query.

## Bundled Resources
- scripts/screen.py — ranked JSON screen over an index universe (primary path).
- scripts/provider.py — robust batch fetch + universe load + filter/rank.
- scripts/indicators.py — pure-Python RSI/EMA/MACD used by the screen.
- scripts/chart.py — optional interactive HTML ranked-bar chart.
- scripts/viz.py — self-contained HTML/SVG chart generator (reused palette).
- references/sp500-constituents.md, references/nasdaq100-constituents.md — dated snapshots.
- references/screening-criteria.md — supported filter grammar.
