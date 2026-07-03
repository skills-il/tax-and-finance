# Technical Indicators Reference

Formulas, default periods, and interpretation thresholds. Market-agnostic;
shared with sp500-nasdaq-screener. Standard, well-documented indicator
definitions — implement in scripts/ against your chosen data source.

## RSI — Relative Strength Index (14)
    RS  = avg_gain(14) / avg_loss(14)
    RSI = 100 - 100 / (1 + RS)
Interpretation: > 70 overbought, < 30 oversold. In strong trends RSI can
stay extended; confirm with price structure.

## MACD (12, 26, 9)
    MACD   = EMA(12) - EMA(26)
    signal = EMA(MACD, 9)
    hist   = MACD - signal
Bullish when MACD crosses above signal and the histogram turns positive.

## Bollinger Bands (20, 2)
    mid   = SMA(20)
    upper = mid + 2 * stdev(20)
    lower = mid - 2 * stdev(20)
Band width proxies volatility; closes outside a band are mean-reversion cues.

## EMA 20 / 50 / 200
Trend: price > EMA200 = primary uptrend; EMA50/EMA200 cross = golden/death
cross; EMA20 for short-term momentum.

## CCI — Commodity Channel Index (20)
    TP  = (H + L + C) / 3
    CCI = (TP - SMA(TP)) / (0.015 * mean_dev)
Interpretation: > +100 strong up, < -100 strong down.
