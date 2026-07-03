# Example — Fundamentals snapshot with an explicit chart request

The user asks for valuation context *and* explicitly wants to see the price
history, so the optional chart is warranted.

## User request

> Give me a fundamental snapshot of MSFT versus its sector, and show me the last
> year on a chart.

## Steps the skill takes

1. **Resolve the ticker.** MSFT is NASDAQ-listed and in scope.
2. **Fetch fundamentals.** `python scripts/fetch_market_data.py --ticker MSFT --period 1y --fundamentals`
   returns P/E, P/S, gross/operating margin, and revenue growth alongside OHLCV.
   `scripts/provider.py` uses `resolve()` across candidate keys, so a single
   unpopulated field name does not read as a false zero — a genuinely missing
   value is reported as "unavailable from source".
3. **Compare to the sector.** Line up each ratio against the sector median and
   note the deltas (premium or discount).
4. **Layer one technical line.** Add price vs EMA200 for a one-line trend call so
   the valuation view has market context.
5. **Render the chart** — the user asked to see it, so this is warranted:
   `python scripts/chart.py --ticker MSFT --period 1y --out MSFT.html`.

## Expected output shape

A compact fundamentals table plus a one-line trend read:

| Metric      | MSFT  | Sector median | Delta      |
|-------------|-------|---------------|------------|
| P/E         | 34.1  | 27.5          | +24% (rich)|
| P/S         | 12.0  | 6.8           | +76%       |
| Gross margin| 69%   | 55%           | +14 pts    |
| Rev growth  | 15%   | 9%            | +6 pts     |

> Trades at a premium to the sector on richer margins and faster growth; price is
> above EMA200 (primary uptrend). Data is delayed EOD, as of the fetched date.

## The chart (requested)

`scripts/chart.py` chains `scripts/provider.py -> scripts/indicators.py ->
scripts/viz.py` and writes `MSFT.html`: a single self-contained interactive file
(inline SVG, colour-blind-safe palette, hover crosshair + tooltip built with
textContent, sortable table view, light/dark toggle). Use `--period 1y` or longer
so EMA200 has the ~200 sessions it needs to render.

## When the chart would be skipped

If the user had only asked "is MSFT expensive?", the table above answers it and no
chart would be produced — the visualization is a bonus, not a default.
