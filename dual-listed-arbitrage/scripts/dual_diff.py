#!/usr/bin/env python3
"""Compute the currency-adjusted TASE/US price gap for a dual-listed pair.

Usage:
    python scripts/dual_diff.py --pair CHKP --tase-agorot 145000 --us-usd 190.50 --boi-rate 3.65
"""
import argparse, json, sys


def gap(tase_agorot: float, us_usd: float, boi_rate: float, adr: float = 1.0) -> dict:
    tase_ils = tase_agorot / 100.0
    us_in_ils = us_usd * boi_rate * adr
    gap_pct = (tase_ils - us_in_ils) / us_in_ils * 100.0
    return {
        "tase_ils": round(tase_ils, 2),
        "us_in_ils": round(us_in_ils, 2),
        "gap_pct": round(gap_pct, 2),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Dual-listed gap calculator.")
    ap.add_argument("--pair", required=True)
    ap.add_argument("--tase-agorot", type=float, required=True)
    ap.add_argument("--us-usd", type=float, required=True)
    ap.add_argument("--boi-rate", type=float, required=True)
    ap.add_argument("--adr", type=float, default=1.0)
    a = ap.parse_args()
    out = {"pair": a.pair}
    out.update(gap(a.tase_agorot, a.us_usd, a.boi_rate, a.adr))
    json.dump(out, sys.stdout, indent=2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
