#!/usr/bin/env python3
"""Project US self-employment tax for a US person freelancing in Israel.

Not tax advice and not a filed return. This follows the Schedule SE and Form 8959 order of
operations on figures you supply and prints a projection worksheet to take to a licensed
preparer. It does not model Israeli tax or Bituach Leumi, does not decide any structure, and
does not file anything.

Figures are those in ../references/se-tax-mechanics.md and ../evidence.json.

Usage:
  python3 se_tax_projection.py --example
  python3 se_tax_projection.py --net-earnings-usd 100000 --year 2026 --filing single
  python3 se_tax_projection.py --net-earnings-usd 150000 --wages-usd 100000 \\
      --medicare-wages-usd 100000 --filing mfs
"""

import argparse
import sys

SE_FACTOR = 0.9235          # Schedule SE line 4a
SS_RATE = 0.124             # Schedule SE line 10
MEDICARE_RATE = 0.029       # Schedule SE line 11, uncapped
ADDL_MEDICARE_RATE = 0.009  # Form 8959 lines 7 and 13, NOT part of Schedule SE
SE_MIN_LINE_4C = 400        # Schedule SE line 4c: tested AFTER the 92.35% factor

# Social security wage base by tax year. 2025 from the Schedule SE instructions, 2026 from
# the 2026 Form 1040-ES (published before that year's Schedule SE instructions). Add each new
# year from its own source; do NOT carry a prior year forward.
WAGE_BASE = {2025: 176_100, 2026: 184_500}

ADDL_MEDICARE_THRESHOLD = {
    "mfj": 250_000,
    "mfs": 125_000,
    "single": 200_000,
}


def schedule_se(net_usd, year, ss_wages_usd):
    """Return (rows, notes, line6, se_tax). line6 is 0 when no SE tax is owed."""
    out, notes = [], []
    base = net_usd * SE_FACTOR if net_usd > 0 else net_usd
    out.append(f"1. Net profit from Schedule C              USD {net_usd:>12,.0f}")
    out.append(f"2. Times 92.35% (Schedule SE 4a to 6)     USD {base:>12,.2f}")
    if base < SE_MIN_LINE_4C:
        out.append(f"   Line 4c is below USD {SE_MIN_LINE_4C}, so no SE tax is owed.")
        return out, notes, 0.0, 0.0

    wb = WAGE_BASE.get(year)
    if wb is None:
        notes.append(f"No social security wage base on file for {year}. The 12.4% portion is "
                     "shown UNCAPPED below, which overstates it for higher earners. Look up "
                     f"the {year} base (Form 1040-ES or Schedule SE instructions) and re-run.")
        ss_base = base
    else:
        room = max(0, wb - ss_wages_usd)      # Schedule SE lines 7, 8a, 9
        ss_base = min(base, room)             # Schedule SE line 10
        if ss_wages_usd:
            notes.append(f"Wage base of USD {wb:,} reduced by USD {ss_wages_usd:,.0f} of "
                         f"your own social security wages to USD {room:,.0f} "
                         "(Schedule SE line 9).")
        if base > room:
            notes.append(f"Social security portion capped under the {year} wage base. "
                         "The Medicare portion is NOT capped.")
    ss = ss_base * SS_RATE
    med = base * MEDICARE_RATE
    out.append(f"3. Social security 12.4% on USD {ss_base:>10,.0f}  USD {ss:>12,.0f}")
    out.append(f"4. Medicare 2.9% (uncapped) on USD {base:>11,.0f}  USD {med:>12,.0f}")
    return out, notes, base, ss + med


def form_8959(line6, filing, medicare_wages_usd):
    """Return (part1, part2) Additional Medicare Tax, per Form 8959 lines 1 to 13."""
    thr = ADDL_MEDICARE_THRESHOLD[filing]               # lines 5 and 9
    part1 = max(0, medicare_wages_usd - thr) * ADDL_MEDICARE_RATE        # lines 6, 7
    se_thr = max(0, thr - medicare_wages_usd)                            # lines 10, 11
    part2 = max(0, line6 - se_thr) * ADDL_MEDICARE_RATE                  # lines 12, 13
    return part1, part2, se_thr


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--net-earnings-usd", type=float, default=0,
                   help="Net profit from Schedule C, in USD, before the 92.35%% step.")
    p.add_argument("--year", type=int, default=2026)
    p.add_argument("--filing", choices=["single", "mfj", "mfs"], default="single",
                   help="single also covers head of household and qualifying surviving "
                        "spouse, which share the USD 200,000 threshold.")
    p.add_argument("--wages-usd", type=float, default=0,
                   help="YOUR OWN social security wages on US Form(s) W-2 (boxes 3 and 7). "
                        "Never include a spouse's wages here. Reduces the wage base on "
                        "Schedule SE line 9.")
    p.add_argument("--medicare-wages-usd", type=float, default=None,
                   help="Medicare wages on US Form(s) W-2, box 5 (can differ from boxes 3 "
                        "and 7). On a joint return enter YOUR box 5 PLUS your "
                        "spouse's box 5. Required whenever --wages-usd is given.")
    p.add_argument("--example", action="store_true")
    a = p.parse_args()

    if a.example:
        a.net_earnings_usd, a.year, a.filing = 100_000, 2026, "single"
        print("(example: USD 100,000 of net profit, single, tax year 2026)\n")
    if a.medicare_wages_usd is None:
        if a.wages_usd:
            p.error("--wages-usd was given without --medicare-wages-usd. Box 5 can differ from "
                    "boxes 3 and 7, so it must be entered separately. Enter box 5 "
                    "(and, on a joint return, add your spouse's box 5).")
        a.medicare_wages_usd = 0.0

    print("US SELF-EMPLOYMENT TAX PROJECTION")
    print("Not tax advice. A worksheet for a licensed preparer.\n")
    print("Why this applies at all: there is no US-Israel totalization agreement, and the")
    print("foreign earned income exclusion does not reduce SE tax. Israeli tax and Bituach")
    print("Leumi do not offset the amount below.\n")

    rows, notes, line6, se_tax = schedule_se(a.net_earnings_usd, a.year, a.wages_usd)
    for r in rows:
        print("  " + r)
    part1, part2, se_thr = form_8959(line6, a.filing, a.medicare_wages_usd)

    print(f"\n  SE TAX (Schedule SE line 12)              USD {se_tax:>12,.0f}")
    print(f"  Half of it, deductible for income tax     USD {se_tax * 0.5:>12,.0f}  "
          "(line 13, does NOT reduce the SE tax)")
    print(f"  Form 8959 Part I, on Medicare wages       USD {part1:>12,.0f}")
    print(f"  Form 8959 Part II, on SE income           USD {part2:>12,.0f}  "
          f"(threshold after wages USD {se_thr:,.0f})")
    total = se_tax + part1 + part2
    print(f"  TOTAL of SE tax and Additional Medicare   USD {total:>12,.0f}")
    if part1:
        notes.append("Part I is tax on the wages themselves. An employer withholds it only "
                     "on wages above USD 200,000 that it pays, regardless of filing status, "
                     "so some or all of Part I may be unwithheld. Ask the preparer to "
                     "reconcile withholding on Form 8959.")
    if a.filing == "mfj":
        notes.append("Married filing jointly: the USD 250,000 threshold applies to BOTH "
                     "spouses combined. --medicare-wages-usd must be both spouses' box 5 "
                     "added together, and a spouse's own self-employment income must be "
                     "added by a preparer; this script models one person's Schedule SE.")

    if a.net_earnings_usd > 0 and total > 0:
        pct = (se_tax + part2) / a.net_earnings_usd * 100
        print(f"  SE-related share of net profit            {pct:>15.1f}%")
        print(f"\n  Set aside roughly {pct:.1f}% of net profit as income comes in, converted")
        print("  to shekels at the rate on the day you are paid, so the money exists when")
        print("  the quarterly instalment falls due. This covers the SE-related taxes only,")
        print("  not US income tax, and holds only for the income mix entered.")
    for n in notes:
        print(f"\n  NOTE: {n}")
    print("\n  This projection ignores US income tax, Israeli income tax and Bituach Leumi.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
