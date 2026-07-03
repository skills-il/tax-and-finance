---
name: global-stock-analysis
license: MIT
description: >-
  Analyze US and global stocks (NASDAQ, NYSE, S&P 500 constituents) with technical, fundamental, and sentiment signals. Use when the user asks about international stocks, tickers like AAPL/NVDA/MSFT, S&P 500 or NASDAQ names, or wants RSI/MACD/moving-average or valuation analysis on a non-Israeli symbol. Provides indicator computation (RSI, MACD, Bollinger Bands, EMA 20/50/200, CCI), fundamental ratios, and a structured buy/hold/sell rationale. Do NOT use for Israeli TASE stocks (use tase-stock-analysis) or cryptocurrency.
allowed-tools: "Bash(python:*) WebFetch"
metadata:
  author: yonyon-ai
  version: 1.0.0
  category: tax-and-finance
  display_name: { he: "ניתוח מניות גלובלי", en: "Global Stock Analysis" }
  tags:
    en: [stock, us-market, nasdaq, sp500]
    he: [מניות, שוק-הון, נאסדק, גלובלי]
---

# Global Stock Analysis

## Instructions

### Step 1 — Resolve the ticker and market
Confirm the symbol and its exchange (NASDAQ, NYSE, or S&P 500 membership).
US symbols are alphabetic (AAPL, NVDA). If the user gives a company name,
resolve to a ticker first. Any Israeli (.TA) symbol is out of scope — route
those to tase-stock-analysis.

### Step 2 — Fetch market data
Run: python scripts/fetch_market_data.py --ticker AAPL --period 1y
This returns OHLCV JSON from yfinance. yfinance is unofficial and
rate-limited; cache results and back off on HTTP 429. Add --fundamentals
for P/E, P/S, margins, and growth.

### Step 3 — Compute technical indicators
See references/indicators.md for formulas and thresholds. Compute
RSI(14), MACD(12,26,9), Bollinger(20,2), EMA 20/50/200, CCI(20).
Flag: RSI > 70 overbought / RSI < 30 oversold; price vs EMA200 = trend.

### Step 4 — Layer fundamentals
P/E, P/S, gross/operating margin, revenue growth (YoY). Compare to the
sector median when available.

### Step 5 — Synthesize a rationale
Give a buy / hold / sell view with the 2-3 signals that drove it and one
contrary signal. Always state assumptions and data freshness.

## Examples

User says: "Is NVDA overbought right now?"
Result: RSI(14) read + MACD histogram direction + the level to watch, with
a one-line trend call from EMA200.

User says: "Fundamental snapshot of MSFT vs its sector"
Result: P/E, P/S, margins, growth table with sector-median deltas.

User says: "Show me AAPL's last year with the moving averages"
Result: a text trend read (price vs EMA stack) plus an optional interactive
HTML chart — Close + EMA 20/50/200 and an RSI(14) panel — written via
scripts/chart.py. See examples/technical-read.md and examples/fundamentals-snapshot.md.

## Visualization (optional)
A chart is a bonus, not a default. Render one only when it makes the answer
clearer or the user asks to "see", "show", or "chart" the data — otherwise the
text analysis stands on its own. There is no ASCII fallback, and the chart is
not forced onto answers that read fine as prose.

When a chart helps, run:
    python scripts/chart.py --ticker AAPL --period 1y --out AAPL.html
This writes one self-contained interactive HTML file (inline SVG, hover
crosshair + tooltip, sortable table view, light/dark toggle) via scripts/chart.py,
which chains scripts/provider.py -> scripts/indicators.py -> scripts/viz.py.
Use --period 1y or longer so EMA200 has enough history to draw. The colours come
from a colour-blind-safe palette and the tooltip DOM is built with textContent
(no injected markup).

## Gotchas
- yfinance quotes are delayed and unofficial; never present as real-time.
- Historical prices are split-adjusted — intraday levels differ from a broker.
- After-hours / pre-market moves are not in the daily bar.
- S&P 500 / NASDAQ membership drifts; the reference list is dated.

## Troubleshooting

### Error: "Ticker not found"
Cause: wrong exchange suffix, or a foreign line quoted as an ADR.
Solution: confirm the US listing symbol; for non-US firms use the ADR ticker.

### Error: "Rate limited (429)"
Cause: yfinance throttling on rapid requests.
Solution: back off, batch, and cache EOD data locally.

## Bundled Resources
- scripts/fetch_market_data.py — OHLCV + fundamentals via yfinance.
- scripts/provider.py — robust market-data fetch: retry-with-backoff then raise (transient errors are not swallowed), multi-key resolve(), and the only yfinance importer so a paid source can swap in untouched.
- scripts/indicators.py — pure-Python, fully typed indicators (SMA, EMA, RSI, MACD, Bollinger, CCI) shared by the fetch and chart paths.
- scripts/viz.py — self-contained interactive HTML/SVG renderer (hover crosshair + tooltip, table view, light/dark toggle); no third-party deps, colour-blind-safe palette.
- scripts/chart.py — optional-chart orchestrator: provider -> indicators -> viz.
- references/indicators.md — indicator formulas, periods, interpretation.
- references/data-sources.md — yfinance limits + provider-abstraction note.
- examples/technical-read.md, examples/fundamentals-snapshot.md — two worked end-to-end walkthroughs.
