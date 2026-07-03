# Example: oversold S&P 500 names by RSI

## User request
"Show me the S&P 500 stocks that are oversold right now, most oversold first."

## Steps the skill takes
1. Load the universe from references/sp500-constituents.md (note the snapshot
   date so the answer states which membership was used).
2. Parse the request into the filter `rsi<30` (RSI(14) below 30 = oversold).
3. Run the screen:
   `python scripts/screen.py --index sp500 --filter "rsi<30"`
   provider.run_screen batch-fetches EOD closes (retry-then-raise), computes
   RSI(14) per symbol, and apply_filter keeps matches ranked ascending by RSI
   (most oversold first). Symbols with no data are skipped and counted, never
   assigned a fake RSI.
4. Present a ranked table: symbol, name, sector, RSI value; note the snapshot
   date, the number matched, and the number skipped.

## Expected output shape
A ranked markdown table, e.g.:

| # | Symbol | Name  | Sector | RSI(14) |
|---|--------|-------|--------|---------|
| 1 | CCC    | Gamma | Health | 24.1    |
| 2 | AAA    | Alpha | Tech   | 27.8    |

Plus a one-line note: "snapshot 2026-Q2 · 2 matched · 0 skipped · not advice."

## Optional chart
If the user asks to "see" or "chart" it, also run
`python scripts/chart.py --index sp500 --filter "rsi<30" --out sp500-oversold.html`
which writes a self-contained interactive HTML bar chart (one accent-hued bar
per symbol, direct-labelled with the RSI value, per-bar hover, table view,
light/dark toggle). The chart is optional — the table is the answer.
