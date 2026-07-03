# NASDAQ-100 Constituents

Membership is a DATED SNAPSHOT. The NASDAQ-100 reconstitutes annually (with
interim additions/removals); always surface the snapshot date in output.

## Refreshing
The canonical source is the Nasdaq index methodology and the published
component list. A maintenance script regenerates this file; never hardcode a
stale list into skill logic.

## Snapshot (excerpt, 2026-Q2)
    AAPL   Apple       Information Technology
    MSFT   Microsoft   Information Technology
    NVDA   Nvidia      Information Technology
    AVGO   Broadcom    Information Technology
    AMZN   Amazon      Consumer Discretionary
    META   Meta        Communication Services
    GOOGL  Alphabet    Communication Services

## Note
Membership does not imply tradability. Some constituents have low float or a
dual-class structure; screening output must not imply a recommendation.
