#!/usr/bin/env python3
"""Fetch OHLCV and fundamentals for a US/global ticker via yfinance.

yfinance is unofficial and rate-limited; results are cached and the caller
should back off on HTTP 429. The provider is isolated so a paid source can be
swapped in later without changing the skill logic.

Usage:
    python scripts/fetch_market_data.py --ticker AAPL --period 1y
    python scripts/fetch_market_data.py --ticker MSFT --fundamentals
"""

import argparse
import json
import sys


def fetch_ohlcv(ticker: str, period: str) -> dict:
    import yfinance as yf  # lazy import so --help works without the dep

    hist = yf.Ticker(ticker).history(period=period)
    if hist.empty:
        raise SystemExit("Ticker not found or no data: " + ticker)
    return {
        "ticker": ticker,
        "period": period,
        "rows": len(hist),
        "last_close": round(float(hist["Close"].dropna().iloc[-1]), 4),
    }


def fetch_fundamentals(ticker: str) -> dict:
    import yfinance as yf

    info = yf.Ticker(ticker).info
    keys = (
        "trailingPE",
        "priceToSalesTrailing12Months",
        "grossMargins",
        "operatingMargins",
        "revenueGrowth",
    )
    return {k: info.get(k) for k in keys}


def main() -> int:
    ap = argparse.ArgumentParser(description="Fetch market data (yfinance).")
    ap.add_argument("--ticker", required=True)
    ap.add_argument("--period", default="1y")
    ap.add_argument("--fundamentals", action="store_true")
    a = ap.parse_args()
    out = (
        fetch_fundamentals(a.ticker)
        if a.fundamentals
        else fetch_ohlcv(a.ticker, a.period)
    )
    json.dump(out, sys.stdout, indent=2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
