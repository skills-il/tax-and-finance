#!/usr/bin/env python3
"""Apply the FBAR and Form 8938 threshold tests and print a filing-obligation map.

This is a threshold calculator, not tax advice and not a filed return. It reports which
forms appear to be triggered by the inputs you give it. Every decision and every signature
belongs to you or your licensed adviser.

Figures are those documented in ../references/filing-matrix.md and ../evidence.json.
Verify against the primary sources before relying on the output.

Usage:
  python3 filing_map.py --example
  python3 filing_map.py --year 2025 --status single --abroad \
      --peak-accounts 42000 --assets-year-end 90000 --assets-peak 150000
"""

import argparse
import sys

FBAR_THRESHOLD = 10_000

# Form 8938: (last_day, any_time) keyed by (lives_abroad, married_filing_jointly)
F8938 = {
    (True, False): (200_000, 300_000),
    (True, True): (400_000, 600_000),
    (False, False): (50_000, 75_000),
    (False, True): (100_000, 150_000),
}

FEIE = {2023: 120_000, 2024: 126_500, 2025: 130_000, 2026: 132_900, 2027: 137_300}

# Pub 501 Table 1, filer(s) under 65; MFS is USD 5 at ANY age. TY2026 Pub 501 not yet published.
FILING_THRESHOLD = {
    2023: {"single": 13_850, "hoh": 20_800, "mfj": 27_700, "mfs": 5},
    2024: {"single": 14_600, "hoh": 21_900, "mfj": 29_200, "mfs": 5},
    2025: {"single": 15_750, "hoh": 23_625, "mfj": 31_500, "mfs": 5},
}
SE_TRIGGER = 400  # Pub 501: net earnings from self-employment of at least USD 400 -> must file

FBAR_PENALTY = {"non_willful": (10_000, 16_536), "willful": (100_000, 165_353)}


def fbar_required(peak_aggregate):
    """FBAR turns on the aggregate peak across ALL foreign accounts, not per account."""
    return peak_aggregate > FBAR_THRESHOLD


def f8938_required(assets_year_end, assets_peak, lives_abroad, mfj):
    last_day, any_time = F8938[(lives_abroad, mfj)]
    return assets_year_end > last_day or assets_peak > any_time, (last_day, any_time)


def deadlines(lives_abroad):
    rows = [
        ("15 April", "1040 due; interest on unpaid tax runs from here", "Any extension (Israel relief aside)"),
        ("15 April", "FBAR due", "Filed to FinCEN"),
    ]
    if lives_abroad:
        rows += [
            ("15 June", "1040 and payment on the 2 month abroad extension", "Automatic, attach statement"),
            ("15 October", "1040 if Form 4868 filed BY 15 June", "Must be requested in time"),
            ("15 December", "1040, discretionary extension beyond 4868", "Letter by 15 October"),
        ]
    else:
        rows += [("--", "Extension rules for US residents are out of scope", "See irs.gov")]
    rows += [("15 October", "FBAR extended date", "Automatic")]
    return rows


def build(args):
    mfj = args.status == "mfj"
    out = []
    out.append("FILING OBLIGATION MAP")
    out.append("Not tax advice. A worksheet to take to a licensed adviser.")
    out.append("")
    out.append(f"Tax year: {args.year}   Status: {args.status}   "
               f"Residence: {'outside the US' if args.abroad else 'in the US'}")
    out.append("")

    out.append("-- Form 1040 --")
    out.append("  Required if gross income, INCLUDING income the exclusion would remove, meets")
    out.append("  the Pub 501 threshold for status and age, OR if net self-employment earnings")
    out.append(f"  were at least USD {SE_TRIGGER} (an osek patur or murshe below the threshold")
    out.append("  still files). This script does not test either.")
    row = FILING_THRESHOLD.get(args.year)
    if row:
        out.append(f"  TY{args.year} under 65, {args.status}: USD {row[args.status]:,}"
                   + (" (any age)" if args.status == "mfs" else "") + ".")
    else:
        out.append(f"  No TY{args.year} row on file. Use that year's Pub 501; do not guess.")
    out.append("  The FBAR below can apply even when no 1040 is required.")
    out.append("")

    out.append("-- FBAR (FinCEN 114) --")
    need = fbar_required(args.peak_accounts)
    out.append(f"  Peak aggregate across ALL foreign accounts: USD {args.peak_accounts:,}")
    out.append(f"  Threshold: more than USD {FBAR_THRESHOLD:,} at ANY point in the year")
    out.append(f"  REQUIRED: {'YES' if need else 'no'}")
    if not need:
        out.append("  Note: this is an aggregate PEAK test. Do not clear the user unless the figure")
        out.append("        includes kupat gemel and keren hishtalmut (provisionally, until the")
        out.append("        preparer confirms), dormant and signature-authority accounts, and is")
        out.append("        the highest point in the year, not year end.")
    out.append("")

    out.append("-- Form 8938 (FATCA) --")
    need8938, (last_day, any_time) = f8938_required(
        args.assets_year_end, args.assets_peak, args.abroad, mfj)
    out.append(f"  Specified assets at year end: USD {args.assets_year_end:,}")
    out.append(f"  Specified assets at peak:     USD {args.assets_peak:,}")
    out.append(f"  Thresholds for this filer: more than USD {last_day:,} on the last day, "
               f"or more than USD {any_time:,} at any time")
    out.append(f"  REQUIRED: {'YES, if a 1040 is required (no 1040 duty, no 8938 duty)' if need8938 else 'no'}")
    out.append("")

    if need and need8938:
        out.append("  Both are triggered (8938 only if a 1040 is required). SEPARATE forms, separate penalties;")
        out.append("  filing one does not satisfy the other.")
        out.append("")

    if args.year in FEIE:
        out.append("-- Foreign earned income exclusion --")
        out.append(f"  Cap for tax year {args.year}: USD {FEIE[args.year]:,}")
        out.append("  The exclusion and the Foreign Tax Credit cannot both be used on the same")
        out.append("  income, and switching can revoke the election for 5 years. Route the")
        out.append("  election itself to a licensed preparer.")
        out.append("")
    else:
        out.append(f"-- Foreign earned income exclusion: no cap on file for {args.year}. "
                   "Look it up in the Revenue Procedure for that year, not the IRS landing page.")
        out.append("")

    out.append("-- Deadlines --")
    for date, item, mech in deadlines(args.abroad):
        out.append(f"  {date:<12} {item:<52} {mech}")
    out.append("  An extension to file is not an extension to pay. Interest runs from 15 April,")
    out.append("  unless the payment falls due inside a disaster postponement you qualify for,")
    out.append("  in which case that period is disregarded for interest and penalties.")
    out.append("  Arrival-year oleh not yet meeting the residence test: ask about Form 2350.")
    out.append("  Israel relief: IRS Notice 2026-63 gives affected taxpayers (e.g. principal")
    out.append("  residence in Israel, the West Bank or Gaza) until 30 Sep 2027 for returns and")
    out.append("  payments due on or after 30 Sep 2026 and before 30 Sep 2027, and re-postpones")
    out.append("  acts already postponed under Notice 2025-53. It does not move the FBAR, which")
    out.append("  is FinCEN's; FinCEN Israel FBAR relief was found only for 2022 and 2023.")
    out.append("  Check irs.gov for any later notice.")
    out.append("")

    if need:
        nw_s, nw_a = FBAR_PENALTY["non_willful"]
        w_s, w_a = FBAR_PENALTY["willful"]
        out.append("-- FBAR exposure if not filed --")
        out.append(f"  Non-willful, per REPORT:    USD {nw_s:,} statutory, USD {nw_a:,} adjusted")
        out.append("                              (per report, not per account: Bittner, 2023)")
        out.append(f"  Willful, per violation:     USD {w_s:,} statutory, USD {w_a:,} adjusted,")
        out.append("                              or 50% of the account balance, WHICHEVER IS")
        out.append("                              GREATER. On a large account the 50% prong")
        out.append("                              dominates.")
        out.append("")

    out.append("Next step: take this to a licensed adviser. This script does not decide the")
    out.append("exclusion-versus-credit election, does not judge whether any past failure was")
    out.append("willful, and does not prepare or sign anything.")
    return "\n".join(out)


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--year", type=int, default=2025)
    p.add_argument("--status", choices=["single", "mfs", "mfj", "hoh"], default="single",
                   help="hoh uses the unmarried Form 8938 row")
    where = p.add_mutually_exclusive_group()
    where.add_argument("--abroad", action="store_true", help="filer lives outside the US")
    where.add_argument("--in-us", action="store_true", help="filer lives in the US")
    p.add_argument("--peak-accounts", type=int, default=0,
                   help="highest AGGREGATE balance across all foreign accounts, USD")
    p.add_argument("--assets-year-end", type=int, default=0)
    p.add_argument("--assets-peak", type=int, default=0)
    p.add_argument("--example", action="store_true", help="run a worked example")
    a = p.parse_args()
    if min(a.peak_accounts, a.assets_year_end, a.assets_peak) < 0:
        p.error("balances cannot be negative")
    if a.example and a.in_us:
        p.error("--example is a couple living abroad; drop --in-us")
    if not a.example and not (a.abroad or a.in_us):
        p.error("say where the filer lives: --abroad or --in-us (it selects the Form 8938 row)")
    if a.assets_peak < a.assets_year_end:
        p.error("--assets-peak is the highest value in the year, so it cannot be below "
                "--assets-year-end")

    if a.example:
        a.year, a.status, a.abroad = 2025, "mfj", True
        a.peak_accounts, a.assets_year_end, a.assets_peak = 145_000, 380_000, 640_000
        print("(example: married oleh couple, Israeli bank plus keren hishtalmut)\n")

    print(build(a))
    return 0


if __name__ == "__main__":
    sys.exit(main())
