# Screening Criteria

Filters the screener understands. Combined with AND semantics.

## Technical
    rsi < N          e.g. rsi < 30  (oversold)
    rsi > N          e.g. rsi > 70  (overbought)
    price > ema200   primary uptrend
    price < ema50    short-term weakness
    macd_cross up    bullish crossover last session

## Fundamental
    pe < N           valuation screen
    ps < N
    rev_growth > N   revenue growth YoY

## Meta
    sector = X       restrict to a GICS sector
    sort   = metric  ranking key (market_cap, rsi, ...)

Indicator math lives in scripts/indicators.py (pure-Python RSI/EMA/MACD).
