# Dual-Listed Pair Registry

A registry of 43 dual-listed pairs. Each pair maps a TASE symbol to its US
listing, with a conversion ratio and an alert threshold.

## The ratio is 1:1 for dual-listed ordinary shares
Under Israel's dual-listing arrangement, a dual-listed company registers the SAME
ordinary share on both TASE and its US exchange, so the two legs are fungible and
the conversion ratio is 1:1 by construction. There is no depositary receipt and no
depositary ratio for these names. A non-1 ratio applies ONLY to a genuine ADR
program (a depositary receipt bundling N ordinaries) and must be read from that
program's depositary agreement / SEC Form F-6, never assumed. Every pair below is a
fungible dual-listed ordinary (or, for Teva, a 1:1 ADR), so all ratios are 1.

## Fields
    tase        TASE alpha symbol
    us          US ticker (NASDAQ / NYSE)
    ratio       ordinary shares per US line (1 for dual-listed ordinaries; only a
                true ADR carries a non-1 ratio, sourced from its F-6)
    threshold   |gap%| that triggers an alert (default 2.0)

## Excerpt
    tase   us     ratio  threshold
    CHKP   CHKP   1      2.0     # Check Point
    NICE   NICE   1      2.0     # NICE
    CYBR   CYBR   1      2.5     # CyberArk
    TEVA   TEVA   1      2.0     # Teva (1:1 ADR)
    SPNS   SPNS   1      3.0     # Sapiens

Never hardcode a pair from memory; the registry is the source of truth.
