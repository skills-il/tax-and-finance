#!/usr/bin/env python3
"""Project US self-employment tax for a US person freelancing in Israel.

Not tax advice and not a filed return. This follows the Schedule SE order of operations on
figures you supply and prints a projection worksheet to take to a licensed preparer. It does
not model Israeli tax or Bituach Leumi, does not decide any structure, and does not file
anything.

Figures are those in ../references/se-tax-mechanics.md and ../evidence.json.

Usage:
  python3 se_tax_projection.py --example
  python3 se_tax_projection.py --net-earnings-usd 100000 --year 2025 --filing single
"""

import argparse
import sys

SE_FACTOR = 0.9235          # Schedule SE line 4a
SS_RATE = 0.124             # social security portion of the 15.3% total
MEDICARE_RATE = 0.029       # Medicare portion, uncapped
ADDL_MEDICARE_RATE = 0.009
SE_MIN_NET_EARNINGS = 400

# Social security wage base by tax year. Add the current year from that year's
# Schedule SE instructions; do NOT carry a prior year forward.
WAGE_BASE = {2025: 176_100}

ADDL_MEDICARE_THRESHOLD = {
    "mfj": 250_000,
    "mfs": 125_000,
    "single": 200_000,
}


def project(net_usd, year, filing, wages_usd):
    out, notes = [], []
    if net_usd < SE_MIN_NET_EARNINGS:
        out.append(f"Net earnings of USD {net_usd:,} are below the USD "
                   f"{SE_MIN_NET_EARNINGS} threshold, so SE tax does not apply.")
        return out, notes, 0.0

    base = net_usd * SE_FACTOR
    out.append(f"1. Net earnings from self-employment      USD {net_usd:>12,.0f}")
    out.append(f"2. Multiply by 92.35% (Schedule SE 4a)    USD {base:>12,.0f}")

    wb = WAGE_BASE.get(year)
    if wb is None:
        notes.append(f"No social security wage base on file for {year}. The 12.4% portion is "
                     "shown UNCAPPED below, which overstates it for higher earners. Look up "
                     f"the {year} base in that year's Schedule SE instructions and re-run.")
        ss_base = base
    else:
        ss_base = min(base, wb)
        if base > wb:
            notes.append(f"Social security portion capped at the {year} wage base of "
                         f"USD {wb:,}. The Medicare portion is NOT capped.")
    ss = ss_base * SS_RATE
    med = base * MEDICARE_RATE
    out.append(f"3. Social security 12.4% on USD {ss_base:>10,.0f}  USD {ss:>12,.0f}")
    out.append(f"4. Medicare 2.9% (uncapped) on USD {base:>11,.0f}  USD {med:>12,.0f}")

    total = ss + med
    thr = ADDL_MEDICARE_THRESHOLD[filing]
    effective_thr = max(0, thr - wages_usd)
    if wages_usd:
        notes.append(f"Threshold reduced by USD {wages_usd:,} of wages, to USD "
                     f"{effective_thr:,}.")
    if base > effective_thr:
        addl = (base - effective_thr) * ADDL_MEDICARE_RATE
        out.append(f"5. Additional Medicare 0.9% over USD {effective_thr:>8,.0f}  "
                   f"USD {addl:>12,.0f}")
        total += addl
    else:
        out.append(f"5. Additional Medicare Tax                 not triggered "
                   f"(threshold USD {effective_thr:,})")
    return out, notes, total


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--net-earnings-usd", type=float, default=0)
    p.add_argument("--year", type=int, default=2025)
    p.add_argument("--filing", choices=["single", "mfj", "mfs"], default="single")
    p.add_argument("--wages-usd", type=float, default=0,
                   help="W-2 style wages, which reduce the Additional Medicare threshold")
    p.add_argument("--example", action="store_true")
    a = p.parse_args()

    if a.example:
        a.net_earnings_usd, a.year, a.filing = 100_000, 2025, "single"
        print("(example: USD 100,000 of net earnings, single, tax year 2025)\n")

    print("US SELF-EMPLOYMENT TAX PROJECTION")
    print("Not tax advice. A worksheet for a licensed preparer.\n")
    print("Why this applies at all: there is no US-Israel totalization agreement, and the")
    print("foreign earned income exclusion does not reduce SE tax. Israeli tax and Bituach")
    print("Leumi do not offset the amount below.\n")

    rows, notes, total = project(a.net_earnings_usd, a.year, a.filing, a.wages_usd)
    for r in rows:
        print("  " + r)
    print(f"\n  TOTAL projected SE tax                    USD {total:>12,.0f}")
    if a.net_earnings_usd:
        pct = total / a.net_earnings_usd * 100
        print(f"  As a share of net earnings                {pct:>15.1f}%")
        print(f"\n  Set aside roughly {pct:.1f}% of each payment as it arrives, converted to")
        print("  shekels at the rate on the day you are paid, so the money exists when the")
        print("  quarterly instalment falls due.")
    for n in notes:
        print(f"\n  NOTE: {n}")
    print("\n  The employer-equivalent half of this is deductible against INCOME tax only.")
    print("  It does not reduce the figure above.")
    print("\n  This projection ignores US income tax, Israeli income tax and Bituach Leumi.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
