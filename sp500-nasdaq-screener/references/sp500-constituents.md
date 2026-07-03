# S&P 500 / NASDAQ-100 Constituents

Membership is a DATED SNAPSHOT. Lists change on quarterly rebalance; always
surface the snapshot date in output.

## Refreshing
Canonical sources are the index providers (S&P Dow Jones, Nasdaq). A
maintenance script regenerates this file; never hardcode a stale list into
skill logic.

## Snapshot (excerpt, 2026-Q2)
    AAPL   Apple       Information Technology
    MSFT   Microsoft   Information Technology
    NVDA   Nvidia      Information Technology
    AMZN   Amazon      Consumer Discretionary
    GOOGL  Alphabet    Communication Services

## Note
Membership does not imply tradability. Some constituents have low float or a
dual-class structure; screening output must not imply a recommendation.
