#!/usr/bin/env python3
"""Dual-listed pair registry: TASE symbol -> US ticker, ratio, alert threshold.

Mirrors references/dual-listed-pairs.md, which is the documented source of truth.
The TASE symbol and the US ticker are NOT always the same string: after Palo
Alto Networks acquired CyberArk, the Tel-Aviv line kept the symbol CYBR while
the US leg is PANW. Always resolve the US ticker here; never reuse the TASE
symbol for the US leg.

Every pair listed has ratio 1 (a fungible ordinary share, or a 1:1 ADS such as
Teva). Dual listings whose US line is an ADS with a non-1 ratio are deliberately
NOT in this table, because their ratio must be read from the depositary
agreement / SEC Form F-6 and has not been verified here.

Thresholds are a skill-internal heuristic, not an external figure: 2.0% for
liquid large caps, 3.0% for thinly traded names whose TASE last price can be
hours old.
"""

from __future__ import annotations

from typing import NamedTuple


class Pair(NamedTuple):
    us: str
    ratio: float
    threshold: float
    name: str


PAIRS: dict[str, Pair] = {
    "ALLT": Pair("ALLT", 1.0, 3.0, "Allot"),
    "ARBE": Pair("ARBE", 1.0, 3.0, "Arbe Robotics"),
    "AUDC": Pair("AUDC", 1.0, 3.0, "AudioCodes"),
    "BWAY": Pair("BWAY", 1.0, 3.0, "BrainsWay"),
    "CAMT": Pair("CAMT", 1.0, 2.0, "Camtek"),
    "CGEN": Pair("CGEN", 1.0, 3.0, "Compugen"),
    "CYBR": Pair("PANW", 1.0, 2.0, "Palo Alto Networks (TASE symbol CYBR)"),
    "DRTS": Pair("DRTS", 1.0, 3.0, "Alpha Tau"),
    "ELLO": Pair("ELLO", 1.0, 3.0, "Ellomay"),
    "ENLT": Pair("ENLT", 1.0, 2.0, "Enlight Energy"),
    "ESLT": Pair("ESLT", 1.0, 2.0, "Elbit Systems"),
    "EVGN": Pair("EVGN", 1.0, 3.0, "Evogene"),
    "FORTY": Pair("FORTY", 1.0, 3.0, "Formula Systems"),
    "GILT": Pair("GILT", 1.0, 3.0, "Gilat"),
    "ICL": Pair("ICL", 1.0, 2.0, "ICL"),
    "INCR": Pair("INCR", 1.0, 3.0, "InterCure"),
    "KEN": Pair("KEN", 1.0, 3.0, "Kenon"),
    "KMDA": Pair("KMDA", 1.0, 3.0, "Kamada"),
    "NICE": Pair("NICE", 1.0, 2.0, "NICE"),
    "NVMI": Pair("NVMI", 1.0, 2.0, "Nova"),
    "NYAX": Pair("NYAX", 1.0, 3.0, "Nayax"),
    "OPK": Pair("OPK", 1.0, 3.0, "OPKO Health"),
    "ORA": Pair("ORA", 1.0, 2.0, "Ormat Technologies"),
    "ORMP": Pair("ORMP", 1.0, 3.0, "Oramed"),
    "PERI": Pair("PERI", 1.0, 3.0, "Perion Network"),
    "PLUR": Pair("PLUR", 1.0, 3.0, "Pluri"),
    "TATT": Pair("TATT", 1.0, 3.0, "TAT Technologies"),
    "TEVA": Pair("TEVA", 1.0, 2.0, "Teva (1:1 ADS)"),
    "TSEM": Pair("TSEM", 1.0, 2.0, "Tower Semiconductor"),
}


def lookup(tase_symbol: str) -> Pair:
    """Resolve a TASE symbol. Raises for an unregistered symbol rather than
    guessing that the US ticker is the same string or that the ratio is 1."""
    sym = tase_symbol.upper().removesuffix(".TA")
    if sym not in PAIRS:
        raise KeyError(
            f"{sym} is not in the dual-listed registry (not dual-listed, delisted, "
            f"or a non-1 ADS whose ratio is unverified); see "
            f"references/dual-listed-pairs.md"
        )
    return PAIRS[sym]
