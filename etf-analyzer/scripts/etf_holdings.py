#!/usr/bin/env python3
"""Fetch ETF holdings, expense ratio, and AUM as JSON (via the robust provider).

Expense ratio is resolved PROPERLY (provider.get_expense_ratio): across .info
synonyms, then yfinance funds_data, tagged with expense_ratio_source; it is null
only when every source is genuinely absent ('unavailable -- see issuer factsheet').

Usage:
    python scripts/etf_holdings.py --ticker QQQ
    python scripts/etf_holdings.py --ticker VTI --compare VOO
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import provider


def main() -> int:
    ap = argparse.ArgumentParser(
        description="ETF holdings / expense ratio / overlap (JSON)."
    )
    ap.add_argument("--ticker", required=True)
    ap.add_argument("--compare", help="second ETF ticker for overlap")
    a = ap.parse_args()

    if a.compare:
        pa = provider.get_etf_profile(a.ticker)
        pb = provider.get_etf_profile(a.compare)
        ka, kb = pa["ticker"], pb["ticker"]
        out: dict[str, Any] = {
            "pair": [ka, kb],
            "overlap": provider.holdings_overlap(pa["holdings"], pb["holdings"]),
            "expense_ratio": {ka: pa["expense_ratio"], kb: pb["expense_ratio"]},
            "expense_ratio_source": {
                ka: pa["expense_ratio_source"],
                kb: pb["expense_ratio_source"],
            },
        }
    else:
        out = provider.get_etf_profile(a.ticker)

    json.dump(out, sys.stdout, indent=2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
