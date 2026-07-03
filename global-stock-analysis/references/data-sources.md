# Data Sources & Provider Abstraction

## Primary: yfinance (unofficial)
Used by scripts/fetch_market_data.py. Free, no key, but:
- Rate-limited (HTTP 429 under load) — back off and cache.
- Quotes delayed ~15 min; not for execution decisions.
- History is split/dividend-adjusted.

## Membership lists
S&P 500 and NASDAQ-100 constituents change on rebalance. Treat the reference
lists as dated snapshots and note staleness in output.

## Provider abstraction (future-proofing)
fetch_market_data.py isolates the provider behind one function so a paid
source (polygon.io, finnhub, alpha vantage) can be swapped in later without
touching skill logic. Pass any key via an env var — never inline a secret.

## Israeli symbols
Any .TA symbol is out of scope — route to tase-stock-analysis (agorot, Maya,
Bank of Israel context).
