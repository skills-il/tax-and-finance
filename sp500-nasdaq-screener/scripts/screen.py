#!/usr/bin/env python3
"""Screen an index universe by a technical/fundamental filter (ranked JSON).

Primary text-path output of the skill. Batch-fetches the universe via the
robust provider, applies the filter, ranks the matches, and prints a JSON
table with the constituent-snapshot date. Symbols with no EOD data are skipped
honestly and reported under `skipped` -- never assigned a fabricated value.

Usage:
    python scripts/screen.py --index sp500 --filter "rsi<30"
    python scripts/screen.py --index nasdaq100 --filter "price>ema200" --top 20
"""

from __future__ import annotations

import argparse
import json
import sys

import provider


def main() -> int:
    ap = argparse.ArgumentParser(description="Ranked index-universe screener.")
    ap.add_argument("--index", choices=["sp500", "nasdaq100"], required=True)
    ap.add_argument("--filter", required=True, help="e.g. 'rsi<30' or 'price>ema200'")
    ap.add_argument("--period", default="1y")
    ap.add_argument("--top", type=int, default=25)
    a = ap.parse_args()

    screen = provider.run_screen(a.index, a.period)
    matched, meta = provider.apply_filter(screen["rows"], a.filter)
    top = matched[: a.top]
    out = {
        "index": a.index,
        "filter": a.filter,
        "metric": meta["metric_label"],
        "as_of": screen["as_of"],
        "matched": meta["count"],
        "skipped": len(screen["skipped"]),
        "rows": [
            {
                "symbol": r["symbol"],
                "name": r["name"],
                "sector": r["sector"],
                "value": r["rank_display"],
            }
            for r in top
        ],
    }
    json.dump(out, sys.stdout, indent=2)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
