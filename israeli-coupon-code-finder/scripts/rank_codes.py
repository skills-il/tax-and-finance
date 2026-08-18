#!/usr/bin/env python3
"""Rank candidate coupon codes and print one summary table.

This script does NOT find codes. It takes codes you already gathered from a
live web search and orders them, so the final answer is a single ranked table
instead of a messy list. It deliberately refuses to invent anything: a code
with no source or no date is pushed to the bottom and marked low confidence.

Input JSON (a list of objects):
  [
    {
      "code": "STRING",
      "source": "link to where the code was found",
      "date_seen": "YYYY-MM-DD",
      "discount": "human text, e.g. ten percent off",
      "conditions": "min cart / new-customer-only / exclusions",
      "confidence": "high | medium | low"   (optional; inferred if missing)
    }
  ]

Usage:
  python scripts/rank_codes.py --file candidates.json
  echo '[...]' | python scripts/rank_codes.py
  python scripts/rank_codes.py --example
"""

import argparse
import json
import sys

CONFIDENCE_RANK = {"high": 0, "medium": 1, "low": 2}


def infer_confidence(item):
    """A code is only as trustworthy as its provenance."""
    explicit = (item.get("confidence") or "").strip().lower()
    if explicit in CONFIDENCE_RANK:
        return explicit
    has_source = bool((item.get("source") or "").strip())
    has_date = bool((item.get("date_seen") or "").strip())
    has_terms = bool((item.get("conditions") or "").strip())
    if has_source and has_date and has_terms:
        return "high"
    if has_source and has_date:
        return "medium"
    return "low"


def sort_key(item):
    conf = CONFIDENCE_RANK[infer_confidence(item)]
    # Newer date_seen first within the same confidence tier.
    date = item.get("date_seen") or ""
    return (conf, _negated(date))


def _negated(date_str):
    # Reverse lexical order for ISO dates so newer sorts first.
    return tuple(-ord(c) for c in date_str)


def cell(value):
    text = str(value if value not in (None, "") else "-")
    return text.replace("|", "/").replace("\n", " ").strip()


def render(items):
    if not items:
        return ("No verified codes to show. Do NOT invent any. "
                "Fall back to store-direct levers (newsletter, app, loyalty club) "
                "and tell the shopper to verify at checkout.")
    ranked = sorted(items, key=sort_key)
    header = ["Code", "Source", "Date seen", "Discount", "Conditions", "Confidence"]
    rows = [header, ["---"] * len(header)]
    for it in ranked:
        rows.append([
            cell(it.get("code")),
            cell(it.get("source")),
            cell(it.get("date_seen")),
            cell(it.get("discount")),
            cell(it.get("conditions")),
            infer_confidence(it),
        ])
    table = "\n".join("| " + " | ".join(r) + " |" for r in rows)
    best = ranked[0]
    note = (f"\n\nTry this first: {cell(best.get('code'))} "
            f"(confidence: {infer_confidence(best)}).\n"
            "Verify at checkout: codes expire fast. If it is rejected, try the next row.")
    return table + note


EXAMPLE = [
    {"code": "REAL-FROM-SEARCH-A", "source": "aggregator link", "date_seen": "2026-06-07",
     "discount": "fifteen percent off", "conditions": "min cart, new customers only",
     "confidence": "high"},
    {"code": "REAL-FROM-SEARCH-B", "source": "store newsletter", "date_seen": "2026-06-01",
     "discount": "free shipping", "conditions": "no minimum"},
    {"code": "REAL-FROM-SEARCH-C", "source": "", "date_seen": "",
     "discount": "claims big discount", "conditions": ""},
]


def main():
    p = argparse.ArgumentParser(description="Rank candidate coupon codes into one summary table.")
    p.add_argument("--file", help="Path to a JSON file with candidate codes.")
    p.add_argument("--example", action="store_true", help="Print a worked example.")
    args = p.parse_args()

    if args.example:
        print(render(EXAMPLE))
        return 0

    raw = open(args.file, encoding="utf-8").read() if args.file else sys.stdin.read()
    if not raw.strip():
        print("No input. Pass --file, pipe JSON to stdin, or use --example.", file=sys.stderr)
        return 1
    try:
        items = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"Input is not valid JSON: {e}", file=sys.stderr)
        return 1
    if not isinstance(items, list):
        print("Input must be a JSON list of candidate-code objects.", file=sys.stderr)
        return 1
    print(render(items))
    return 0


if __name__ == "__main__":
    sys.exit(main())
