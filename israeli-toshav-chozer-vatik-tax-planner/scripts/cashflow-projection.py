#!/usr/bin/env python3
"""
cashflow-projection.py

Plain-text 10-year cash-flow projector for an Israeli returning resident,
classifying income streams as EXEMPT vs. TAXABLE under three tracks:

  - vatik       (10 years foreign-resident, section 14 full exemption)
  - regular     (6-10 years foreign-resident, 5-year passive + 10-year capital gains)
  - none        (no track, regular Israeli taxation from day 1)

CRITICAL DISCLAIMER
-------------------
This script does NOT compute tax owed (no NIS amount, no marginal rate).
It classifies gross income as exempt vs. taxable. It is a planning aid,
not tax advice. A CPA must review your specific case before any filing.

Usage:
  python3 cashflow-projection.py                       # interactive prompts
  python3 cashflow-projection.py --json input.json     # batch mode

JSON shape:
{
  "track": "vatik" | "regular" | "none",
  "residency_start": "YYYY-MM-DD",       # date became Israeli tax resident
  "us_person": true | false,             # holds US citizenship or green card
  "income_streams": [
    {
      "label": "US W-2 salary",
      "source": "foreign" | "israeli",
      "kind":   "active" | "passive" | "capital-gain",
      "annual_amount": 250000,            # in whatever currency, no conversion done
      "currency": "USD",
      "asset_acquired_before_return": true,   # for regular track only
      "years_active": [1,2,3,4,5,6,7,8,9,10]  # which of the 10 years this stream exists
    }
  ]
}
"""
import argparse
import json
import sys
from datetime import date, datetime
from typing import List, Dict

DISCLAIMER = (
    "PLANNING AID, NOT TAX ADVICE. This output classifies each income stream as exempt "
    "vs. taxable under section 14 of the Income Tax Ordinance. It does NOT compute the "
    "shekel amount of tax owed. A CPA must review before any filing. From 1.1.2026, "
    "vatikim must REPORT foreign income to Mas Hachnasa even though it remains exempt."
)


def classify_stream(track: str, source: str, kind: str, year_idx: int,
                    asset_acquired_before_return: bool) -> str:
    """Return 'EXEMPT' or 'TAXABLE' for a given (track, stream, year) tuple."""
    # Israeli-source income is taxable under every track.
    if source == "israeli":
        return "TAXABLE"

    # Foreign-source income classification depends on track.
    if track == "none":
        return "TAXABLE"

    if track == "vatik":
        # Full 10-year exemption on active, passive, capital gains. Years 1-10 inclusive.
        if 1 <= year_idx <= 10:
            return "EXEMPT"
        return "TAXABLE"

    if track == "regular":
        # 5 years on passive, 10 years on capital gains, NEVER on active. Must be
        # foreign asset acquired during the period abroad for capital gains exemption.
        if kind == "active":
            return "TAXABLE"
        if kind == "passive":
            if 1 <= year_idx <= 5 and asset_acquired_before_return:
                return "EXEMPT"
            return "TAXABLE"
        if kind == "capital-gain":
            if 1 <= year_idx <= 10 and asset_acquired_before_return:
                return "EXEMPT"
            return "TAXABLE"
        return "TAXABLE"

    return "TAXABLE"


def render(plan: Dict) -> str:
    track = plan["track"]
    residency_start = plan["residency_start"]
    streams = plan["income_streams"]
    us_person = plan.get("us_person", False)

    lines = []
    lines.append("=" * 72)
    lines.append("ISRAELI RETURNING-RESIDENT CASH-FLOW PROJECTION")
    lines.append("=" * 72)
    lines.append(f"Track: {track}")
    lines.append(f"Israeli tax-residency start date: {residency_start}")
    lines.append(f"US person (citizen / green card): {us_person}")
    lines.append(f"Streams: {len(streams)}")
    lines.append("")
    lines.append("DISCLAIMER: " + DISCLAIMER)
    lines.append("")

    # Per-year breakdown
    for year_idx in range(1, 11):
        lines.append(f"--- Year {year_idx} ---")
        exempt_total = {}
        taxable_total = {}
        for s in streams:
            if year_idx not in s.get("years_active", []):
                continue
            verdict = classify_stream(
                track=track,
                source=s["source"],
                kind=s["kind"],
                year_idx=year_idx,
                asset_acquired_before_return=s.get("asset_acquired_before_return", False),
            )
            currency = s.get("currency", "?")
            amount = s["annual_amount"]
            label = s["label"]
            bucket = exempt_total if verdict == "EXEMPT" else taxable_total
            bucket[currency] = bucket.get(currency, 0) + amount
            lines.append(f"  [{verdict:7}] {label}: {amount:,} {currency}  ({s['source']}/{s['kind']})")
        if exempt_total or taxable_total:
            lines.append(f"  TOTAL EXEMPT:  " + ", ".join(f"{v:,} {k}" for k, v in exempt_total.items()))
            lines.append(f"  TOTAL TAXABLE: " + ", ".join(f"{v:,} {k}" for k, v in taxable_total.items()))
        else:
            lines.append("  (no streams active this year)")
        lines.append("")

    # Reporting-obligation reminder
    try:
        rstart = datetime.fromisoformat(residency_start).date()
    except Exception:
        rstart = None
    if rstart and rstart >= date(2026, 1, 1):
        lines.append("REPORTING NOTE: Your residency start is on/after 1.1.2026.")
        lines.append("Amendment 272 applies: foreign income above is EXEMPT but must be")
        lines.append("REPORTED annually on Form 1301 + Schedule D-1. Capital declarations")
        lines.append("(hatzharat hon) on Tax Authority request. Trust + CFC disclosures may apply.")
    elif rstart:
        lines.append("REPORTING NOTE: Your residency start is before 1.1.2026.")
        lines.append("Legacy regime: foreign income above is EXEMPT and NOT reportable for")
        lines.append("the remainder of your 10-year window. Verify the residency-start date")
        lines.append("with a CPA before relying on this position.")
    lines.append("")
    if us_person:
        lines.append("US-PERSON WARNING: You hold US citizenship or a green card.")
        lines.append("The Israeli section 14 exemption above does NOT relieve US tax.")
        lines.append("The US-Israel treaty saving clause (Article 6(3)) lets the US tax")
        lines.append("its citizens as if the treaty did not exist. No foreign tax credit")
        lines.append("offsets the US bill because no Israeli tax was paid on exempt income.")
        lines.append("Route every 'EXEMPT' line above through a US-Israel cross-border CPA.")
        lines.append("")
    lines.append("=" * 72)
    lines.append(DISCLAIMER)
    lines.append("=" * 72)
    return "\n".join(lines)


def interactive() -> Dict:
    print("Interactive mode. Press Ctrl+C to exit.\n")
    track = input("Track [vatik/regular/none]: ").strip().lower()
    if track not in ("vatik", "regular", "none"):
        print(f"Unknown track: {track}", file=sys.stderr)
        sys.exit(1)
    residency_start = input("Israeli tax-residency start (YYYY-MM-DD): ").strip()
    us_person = input("US citizen or green-card holder? [y/n]: ").strip().lower() == "y"
    n = int(input("How many income streams? ").strip())
    streams = []
    for i in range(n):
        print(f"\nStream #{i+1}")
        label = input("  Label: ").strip()
        source = input("  Source [foreign/israeli]: ").strip().lower()
        kind = input("  Kind [active/passive/capital-gain]: ").strip().lower()
        amt = int(input("  Annual amount (integer, no commas): ").strip())
        cur = input("  Currency [e.g. USD, EUR, NIS]: ").strip().upper()
        acquired = input("  Asset acquired before return? [y/n] (for regular track only): ").strip().lower() == "y"
        years_raw = input("  Years active [e.g. 1-10 or 1,2,5-8]: ").strip()
        years = parse_years(years_raw)
        streams.append({
            "label": label, "source": source, "kind": kind,
            "annual_amount": amt, "currency": cur,
            "asset_acquired_before_return": acquired,
            "years_active": years,
        })
    return {"track": track, "residency_start": residency_start, "us_person": us_person, "income_streams": streams}


def parse_years(s: str) -> List[int]:
    out = set()
    for part in s.split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-")
            out.update(range(int(a), int(b) + 1))
        elif part:
            out.add(int(part))
    return sorted(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", help="Path to JSON input file")
    args = ap.parse_args()
    if args.json:
        with open(args.json) as f:
            plan = json.load(f)
    else:
        plan = interactive()
    print(render(plan))


if __name__ == "__main__":
    main()
