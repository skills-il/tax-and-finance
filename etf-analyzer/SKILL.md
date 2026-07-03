---
name: etf-analyzer
license: MIT
description: >-
  Analyze ETFs — holdings composition, sector and geographic exposure, expense ratio, and index-tracking error. Use when the user asks about an ETF ticker (SPY, QQQ, VTI, etc.), wants to compare two ETFs, check overlap between funds, or understand what an ETF holds and costs. Provides top-holdings breakdown, overlap percentage, cost comparison, and tracking-error context. Do NOT use for individual-stock analysis (use global-stock-analysis) or Israeli mutual funds.
allowed-tools: "Bash(python:*) WebFetch"
metadata:
  author: yonyon-ai
  version: 1.0.0
  category: tax-and-finance
  display_name: { he: "מנתח קרנות סל", en: "ETF Analyzer" }
  tags:
    en: [etf, holdings, funds]
    he: [קרנות-סל, ETF, השקעות]
---

# ETF Analyzer

## Instructions

### Step 1 — Resolve the ETF and issuer
Confirm the ticker (SPY, QQQ, VTI). Distinguish plain index ETFs from
leveraged / inverse / synthetic products (they behave differently).

### Step 2 — Pull holdings, expense ratio, AUM
Run: python scripts/etf_holdings.py --ticker QQQ
Top holdings and weights, net expense ratio, assets under management. The expense
ratio is resolved across candidate keys and yfinance funds_data and tagged with
an expense_ratio_source; it is null (with source "unavailable — see issuer
factsheet") only when every source is genuinely absent. Add --compare VOO for
weight-based overlap between two funds.

### Step 3 — Exposure
Sector and geographic breakdown; top-10 concentration.

### Step 4 — Compare (two ETFs)
Overlap % by shared-holding weight; cost delta; tracking-error context. See
references/etf-metrics.md.

## Examples
User says: "How much does VTI overlap with VOO?"
Result: overlap % + the shared mega-cap weight + expense-ratio delta.

User says: "Show me what QQQ holds."
Result: top holdings with weights, expense ratio (with its source) and AUM — plus,
if a visual helps, an optional interactive holdings chart via
`python scripts/chart.py --ticker QQQ --out QQQ.html`.

## Visualization (optional)
A chart is produced only when it makes the answer clearer or the user asks to see
one — it is never forced and never ASCII. When useful, run:
    python scripts/chart.py --ticker QQQ --out QQQ.html
    python scripts/chart.py --ticker VTI --compare VOO --out vti-voo.html
Each writes one self-contained interactive HTML file (inline SVG): a top-holdings
composition bar chart with an expense-ratio + AUM readout, or a two-ETF overlap
view with the overlap % and cost delta. It has a hover tooltip, a table view, and
a light/dark toggle. The text answer stands on its own without it.

## Gotchas
- Holdings disclosure lags (daily for many; monthly for some).
- Leveraged / inverse ETFs reset daily — not buy-and-hold proxies.
- Expense ratio is not total cost (spread and tracking error matter).

## Troubleshooting

### Error: "No holdings data"
Cause: some issuers disclose on a delay.
Solution: use the latest available disclosure and note the as-of date.

## Bundled Resources
- scripts/etf_holdings.py — holdings, expense ratio (+ source), AUM, and pair overlap as JSON.
- scripts/provider.py — robust yfinance provider: retry-then-raise, resolve() across expense-ratio synonyms, funds_data fallback, overlap math.
- scripts/viz.py — optional self-contained interactive HTML holdings/overlap chart generator.
- scripts/htmlshell.py — shared palette + CSS/JS + XSS-safe page assembler reused by viz.py.
- scripts/chart.py — optional chart orchestrator (see Visualization above).
- references/etf-metrics.md — overlap, tracking error, cost methodology.
