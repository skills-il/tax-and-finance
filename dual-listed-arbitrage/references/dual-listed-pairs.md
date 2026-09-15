# Dual-Listed Pair Registry

Source of the listing universe: TASE Market Data, Shares, "Dual Listed – Sec. Law"
(https://market.tase.co.il/en/market_data/securities/data/all?dType=1&cl1=1&cl2=7),
which showed 52 records on 15 Sep 2026. The list changes as companies list, delist
or are acquired, so re-check it before trusting any row. The same data lives in
scripts/registry.py, which the chart script reads.

## What changed in September 2026

- Check Point (CHKP) is NOT listed on TASE. It trades on Nasdaq only, so it has no
  second leg. Earlier versions of this skill used it as the main example.
- CyberArk was acquired by Palo Alto Networks. The Tel-Aviv line now shows the name
  PALO ALTO but kept the symbol CYBR, and its US leg is PANW. The TASE symbol and
  the US ticker are different strings.
- Sapiens (SPNS) is not on the current TASE dual-listed list, and Yahoo returned no
  data for either leg on 15 Sep 2026.

## The ratio is 1:1 for dual-listed ordinary shares, but not for every listing

Under the dual-listing arrangement the same ordinary share is registered on both
exchanges, so the two legs are fungible and the ratio is 1:1 by construction. A
dual listing whose US line is an ADS bundling several ordinaries would carry a
ratio other than 1. Their ratio must be read from the depositary
agreement / SEC Form F-6 and must never be assumed. Those listings are kept out of
the table below.

## Fields
    tase        TASE symbol (the .TA line on Yahoo)
    us          US ticker (Nasdaq / NYSE); may differ from the TASE symbol
    ratio       ordinary shares per US line
    threshold   |gap%| that triggers an alert; a skill-internal heuristic, 2.0
                for liquid large caps, 3.0 for thinly traded names

## Registered pairs (ratio 1, both legs checked 15 Sep 2026)
    tase   us     ratio  threshold  name
    CAMT   CAMT   1      2.0        Camtek
    CYBR   PANW   1      2.0        Palo Alto Networks
    ENLT   ENLT   1      2.0        Enlight Energy
    ESLT   ESLT   1      2.0        Elbit Systems
    ICL    ICL    1      2.0        ICL
    NICE   NICE   1      2.0        NICE
    NVMI   NVMI   1      2.0        Nova
    ORA    ORA    1      2.0        Ormat Technologies
    TEVA   TEVA   1      2.0        Teva (1:1 ADS)
    TSEM   TSEM   1      2.0        Tower Semiconductor
    ALLT   ALLT   1      3.0        Allot
    ARBE   ARBE   1      3.0        Arbe Robotics
    AUDC   AUDC   1      3.0        AudioCodes
    BWAY   BWAY   1      3.0        BrainsWay
    CGEN   CGEN   1      3.0        Compugen
    DRTS   DRTS   1      3.0        Alpha Tau
    ELLO   ELLO   1      3.0        Ellomay
    EVGN   EVGN   1      3.0        Evogene
    FORTY  FORTY  1      3.0        Formula Systems
    GILT   GILT   1      3.0        Gilat
    INCR   INCR   1      3.0        InterCure
    KEN    KEN    1      3.0        Kenon
    KMDA   KMDA   1      3.0        Kamada
    NYAX   NYAX   1      3.0        Nayax
    OPK    OPK    1      3.0        OPKO Health
    ORMP   ORMP   1      3.0        Oramed
    PERI   PERI   1      3.0        Perion Network
    PLUR   PLUR   1      3.0        Pluri
    TATT   TATT   1      3.0        TAT Technologies

"Checked" means the two legs' last closes agreed within a few percent at ratio 1
on that date, which rules out a mismatched ticker or a hidden ADS ratio. It is not
a claim that the gap was small on any other day.

## Dual-listed but NOT registered (ratio not verified)

In a Yahoo check on 15 Sep 2026 their US line did not agree with the TASE line at
ratio 1. The cause (an ADS with a non-1 ratio, a stale thin quote, or a different US
instrument) has not been verified. Do not compute a gap for them until the ratio is
read from the F-6: ALAR (Alarum), BLRX (BioLineRx), CANF (Can-Fite),
FRSX (Foresight), PPBT (Purple Biotech), XTLB (XTL), TURB (TurboGen), CION.

Also out of the table: the remaining listings on the TASE list, for which no US leg
was found on the free data source.

Never hardcode a pair from memory; the registry is the source of truth.
