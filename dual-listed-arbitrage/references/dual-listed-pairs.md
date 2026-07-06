# Dual-Listed Pair Registry

A registry of 43 dual-listed pairs. Each pair maps a TASE symbol to its US
listing, with an ADR ratio and an alert threshold.

## Fields
    tase        TASE alpha symbol
    us          US ticker (NASDAQ / NYSE)
    adr_ratio   US shares per TASE share (often 1, not always)
    threshold   |gap%| that triggers an alert (default 2.0)

## Excerpt
    tase   us     adr_ratio  threshold
    CHKP   CHKP   1          2.0     # Check Point
    NICE   NICE   1          2.0     # NICE
    CYBR   CYBR   1          2.5     # CyberArk
    TEVA   TEVA   1          2.0     # Teva
    SPNS   SPNS   1          3.0     # Sapiens

Never hardcode a pair from memory; the registry is the source of truth.
