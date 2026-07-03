# Example — Technical read: "Is NVDA overbought right now?"

A realistic momentum question that the text answer fully resolves; a chart is
offered only if the user wants to see the levels.

## User request

> Is NVDA overbought right now?

## Steps the skill takes

1. **Resolve the ticker.** NVDA is NASDAQ-listed and alphabetic — in scope. No
   `.TA` suffix, so no reroute to tase-stock-analysis.
2. **Fetch history.** `python scripts/fetch_market_data.py --ticker NVDA --period 1y`
   pulls daily OHLCV. The fetch goes through `scripts/provider.py`, which retries
   transient 429s with backoff and raises on persistent failure rather than
   returning a silent null.
3. **Compute indicators.** `scripts/indicators.py` gives RSI(14), the MACD(12,26,9)
   histogram, and EMA 20/50/200. Read the thresholds from
   `references/indicators.md`: RSI > 70 = overbought, < 30 = oversold.
4. **Read the tape.** Combine the RSI level, the MACD histogram direction
   (expanding vs contracting), and price vs EMA200 for the trend call.
5. **State freshness.** yfinance quotes are delayed and split-adjusted — flag
   the as-of date; do not present as real-time.

## Expected output shape

A short prose answer, for example:

- **RSI(14):** 74.2 — above 70, so technically overbought.
- **MACD histogram:** still positive but flattening — momentum cooling, not yet
  reversed.
- **Trend:** price ~18% above EMA200 — primary uptrend intact; overbought in an
  uptrend can persist.
- **Level to watch:** first support near EMA20 (~cited price).
- **Caveat:** delayed EOD data, as of the fetched date.

## Optional chart

Only if the user then asks to *see* it:

    python scripts/chart.py --ticker NVDA --period 1y --out NVDA.html

Produces one self-contained interactive HTML file — Close + EMA 20/50/200 with a
dedicated RSI(14) panel (30/70 band), a hover crosshair + tooltip, a table view,
and a light/dark toggle. It is not generated unless it adds something the prose
did not.
