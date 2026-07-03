# Example: NASDAQ-100 names trading above their 200-day average

## User request
"Which NASDAQ-100 stocks are above their 200-day moving average, and by how
much? Chart the top 15."

## Steps the skill takes
1. Load the universe from references/nasdaq100-constituents.md (surface the
   snapshot date).
2. Parse the request into the filter `price>ema200` (last close above EMA200 =
   primary uptrend). See references/screening-criteria.md for the grammar.
3. Run the screen:
   `python scripts/screen.py --index nasdaq100 --filter "price>ema200"`
   provider computes the last close and EMA200 per symbol; apply_filter keeps
   matches and ranks them by the percentage gap `(close-ema200)/ema200*100`,
   largest gap first. Symbols still inside the EMA200 warm-up (not enough
   history) are skipped honestly, not treated as matches.
4. Present a ranked table: symbol, name, sector, % above EMA200.

## Expected output shape
A ranked markdown table, e.g.:

| # | Symbol | Name    | Sector | % vs EMA200 |
|---|--------|---------|--------|-------------|
| 1 | NVDA   | Nvidia  | Tech   | +18.42%     |
| 2 | AVGO   | Broadcom| Tech   | +11.07%     |

Plus a note: "snapshot 2026-Q2 · N matched · M skipped · delayed data · not advice."

## Optional chart
Because the user asked to chart it, also run
`python scripts/chart.py --index nasdaq100 --filter "price>ema200" --top 15 --out nasdaq-uptrend.html`
which writes a self-contained interactive HTML ranked-bar chart: one accent-hued
bar per symbol grown from a zero baseline, direct-labelled with the % gap,
recessive axis, per-bar hover tooltip (name + sector + value), a table view, and
a light/dark toggle.
