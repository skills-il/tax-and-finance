#!/usr/bin/env python3
"""
Rough refund estimator for Israeli salaried employees.

Given total taxable salary, total tax withheld (sum of field 042 across all
Form 106 documents for the year), and detected refund triggers, produce a
ballpark estimate range. NOT a binding calculation. The Tax Authority's
real review may differ once supporting documents are evaluated.

Usage:
    python estimate_refund.py --year 2026 --salary 282000 --withheld 47200 \
        --points 2.75 --miluim-days 0 --donations 0 --yishuv-pct 0
    python estimate_refund.py --year 2022 --salary 150000 --withheld 20000 \
        --points 2.75 --child-ages 0,7,14 --parent-side mother

Pass --year to select that tax year's bracket table, credit-point value and
surtax threshold. Supported years are 2020 through 2026, which covers the
six-year retroactive window under Section 160 ITO. An unsupported year is
rejected rather than silently computed against another year's brackets.
2021-2026 come from the Israel Tax Authority deductions booklets served on
gov.il (2021 under the file name itc_itc_necuyim2021-1.pdf); 2020 matches a
mirror copy of the ITA 2020 booklet and Kol-Zchut's history table, and the
estimator flags it in its notes.

--child-ages adds the child credit points for the claim year's own regime
(2020-2021, 2022-2023 temporary order, 2024 onward), so a 2024 table is never
applied to a 2022 claim. Pass the age each child REACHES during the tax year
(0 = birth year, 18 = the year the child turns 18) and --parent-side
(mother / father / sole). --year is required.
"""
from __future__ import annotations
import argparse
import sys
from dataclasses import dataclass

# Per-year monthly tax brackets. Top employment rung per Section 121 ITO is 47%.
# Mas yesafim (Section 121B) is a SEPARATE surtax modeled in surtax() below. Do NOT
# bake it into the bracket table or it double-counts for high earners. The statute's
# top rung is 47%; the higher headline rate quoted in popular tables is that rung plus
# the separate surtax, not a bracket in its own right.
#
# 2021-2026 read from the Israel Tax Authority "לוח עזר לחישוב מס הכנסה ממשכורת
# ושכר עבודה" booklet PDFs (pdftotext text layer). The ITA no longer serves the 2020
# booklet; the 2020 rows match a mirror copy of it (prisha.co.il) and Kol-Zchut's
# history table, and the estimator warns when 2020 is used.
BRACKETS_BY_YEAR_MONTHLY = {
    2020: [(6330, 0.10), (9080, 0.14), (14580, 0.20), (20260, 0.31), (42160, 0.35), (float("inf"), 0.47)],
    2021: [(6290, 0.10), (9030, 0.14), (14490, 0.20), (20140, 0.31), (41910, 0.35), (float("inf"), 0.47)],
    2022: [(6450, 0.10), (9240, 0.14), (14840, 0.20), (20620, 0.31), (42910, 0.35), (float("inf"), 0.47)],
    2023: [(6790, 0.10), (9730, 0.14), (15620, 0.20), (21710, 0.31), (45180, 0.35), (float("inf"), 0.47)],
    2024: [(7010, 0.10), (10060, 0.14), (16150, 0.20), (22440, 0.31), (46690, 0.35), (float("inf"), 0.47)],
    2025: [(7010, 0.10), (10060, 0.14), (16150, 0.20), (22440, 0.31), (46690, 0.35), (float("inf"), 0.47)],
    2026: [(7010, 0.10), (10060, 0.14), (19000, 0.20), (25100, 0.31), (46690, 0.35), (float("inf"), 0.47)],
}

# Annual value of a credit point (monthly value x 12).
CREDIT_POINT_ANNUAL_BY_YEAR = {
    2020: 2628, 2021: 2616, 2022: 2676, 2023: 2820, 2024: 2904, 2025: 2904, 2026: 2904,
}

# Mas yesafim: annual threshold and the rate on EARNED income.
SURTAX_THRESHOLD_BY_YEAR = {
    2020: 651600, 2021: 647640, 2022: 663240, 2023: 698280,
    2024: 721560, 2025: 721560, 2026: 721560,
}
SURTAX_RATE_EARNED = 0.03
# From 2025 a SECOND 2% add-on applies to CAPITAL-source income above the same
# threshold (3% + 2% = 5%). It does NOT apply to earned income and did NOT exist
# before 2025, so it is never applied to a salary-only estimate.
SURTAX_CAPITAL_ADDON_RATE = 0.02
SURTAX_CAPITAL_ADDON_FIRST_YEAR = 2025

# Years with brackets sourced from a primary ITA booklet text layer.
PRIMARY_SOURCED_YEARS = {2021, 2022, 2023, 2024, 2025, 2026}
SUPPORTED_YEARS = sorted(BRACKETS_BY_YEAR_MONTHLY)

# Section 46 donation credit. The minimum qualifying donation AND the annual ceiling are both
# index-adjusted every tax year, so applying 2026's figures to a 2022 claim silently disqualifies
# a donation that did qualify. Values read from that year's ITA deductions booklet text layer
# (2020 from the mirror copy of the 2020 booklet).
SECTION_46_CREDIT_RATE = 0.35

# Section 39B (Amendment 283): COMBAT reserve service only, points in the tax year after the
# service. The 30/40/50-day schedule is a temporary order for tax years 2026 and 2027.
MILUIM_FIRST_TAX_YEAR = 2026
MILUIM_LAST_SCHEDULE_YEAR = 2027
SECTION_46_MIN_BY_YEAR = {2020: 190, 2021: 190, 2022: 190, 2023: 200, 2024: 207, 2025: 207, 2026: 207}
SECTION_46_CEILING_BY_YEAR = {
    2020: 9350000, 2021: 9294000, 2022: 9517000, 2023: 10019808,
    2024: 10354816, 2025: 10354816, 2026: 10354816,
}


def child_points(year: int, age: int, side: str) -> float:
    """Credit points for ONE child in tax year `year` (s.66(ג)(4)-(5), s.40(ב)).

    `age` is the age the child reaches during the tax year: 0 = birth year,
    18 = maturity year (שנת בגרות). `side` is "mother" (the mother, or the
    parent the children live with, including a single parent under
    s.40(ב)(1)) or "father" (the other parent). Three regimes:
      2020-2021: birth year 1.5 each; ages 1-5 2.5 each; 6-17 mother 1 / father 0.
      2022-2023: as above, but ages 6-12 mother 2 / father 1 (temporary order).
      2024 on:   2.5 / 4.5 / 4.5 / 3.5 / 2.5 / 2.5 each for ages 0-5;
                 6-17 mother 2 / father 1.
    Maturity year: 0.5 to the mother side only, in every regime.
    """
    if side not in ("mother", "father"):
        raise ValueError("side must be 'mother' or 'father'")
    if age < 0 or age > 18:
        return 0.0
    if age == 18:
        return 0.5 if side == "mother" else 0.0
    if year >= 2024:
        if age <= 5:
            return {0: 2.5, 1: 4.5, 2: 4.5, 3: 3.5, 4: 2.5, 5: 2.5}[age]
        return 2.0 if side == "mother" else 1.0
    if age == 0:
        return 1.5
    if age <= 5:
        return 2.5
    if 2022 <= year <= 2023 and age <= 12:
        return 2.0 if side == "mother" else 1.0
    return 1.0 if side == "mother" else 0.0


@dataclass
class RefundEstimate:
    tax_due_estimate: float
    tax_withheld: float
    refund_low: float
    refund_high: float
    notes: list[str]


def annual_tax_under_brackets(taxable_annual: float, brackets_monthly: list[tuple[float, float]]) -> float:
    """Tax due assuming bracket thresholds are MONTHLY (Israeli convention).

    Convert brackets to annual by multiplying thresholds by 12 and apply.
    """
    remaining = max(taxable_annual, 0.0)
    tax = 0.0
    prev_threshold_annual = 0.0
    for monthly_threshold, rate in brackets_monthly:
        annual_threshold = monthly_threshold * 12 if monthly_threshold != float("inf") else float("inf")
        slice_width = max(0.0, annual_threshold - prev_threshold_annual)
        slice_used = min(remaining, slice_width)
        tax += slice_used * rate
        remaining -= slice_used
        prev_threshold_annual = annual_threshold
        if remaining <= 0:
            break
    return tax


def surtax(taxable_annual: float, year: int) -> float:
    """Section 121B ITO mas yesafim on EARNED income, using that year's threshold.

    The extra 2% introduced in 2025 applies only to capital-source income, which
    this salary-based estimator does not model, so it is deliberately not added.
    """
    threshold = SURTAX_THRESHOLD_BY_YEAR.get(year)
    if threshold is None or taxable_annual <= threshold:
        return 0.0
    return (taxable_annual - threshold) * SURTAX_RATE_EARNED


def estimate(
    year: int,
    salary_annual: float,
    withheld_annual: float,
    points: float,
    miluim_points_bonus: float,
    donations_annual: float,
    yishuv_pct: float,
    yishuv_ceiling: float = 0.0,
) -> RefundEstimate:
    notes: list[str] = []
    if year not in BRACKETS_BY_YEAR_MONTHLY:
        raise ValueError(
            f"Year {year} is not supported. This estimator carries bracket tables for "
            f"{SUPPORTED_YEARS[0]}-{SUPPORTED_YEARS[-1]} only. Section 160 ITO allows refund "
            "claims six years back, so anything older than that window is out of scope; for a "
            "year inside the window that is missing here, look up that year's ITA deductions "
            "booklet rather than substituting another year's brackets."
        )
    if year not in PRIMARY_SOURCED_YEARS:
        notes.append(
            f"Year {year}: brackets and credit-point value come from a secondary source "
            "(the ITA no longer publishes that year's deductions booklet). Confirm against "
            "the assessment before relying on the number."
        )

    gross_tax = annual_tax_under_brackets(salary_annual, BRACKETS_BY_YEAR_MONTHLY[year])
    gross_tax += surtax(salary_annual, year)
    if surtax(salary_annual, year) > 0:
        notes.append(
            "Income is above the mas yesafim threshold. Check whether this year carries a Form 1301 "
            "filing obligation; if it does, the refund belongs inside Form 1301 (israeli-tax-returns), "
            "not Form 135."
        )

    total_points = points + miluim_points_bonus
    credit_value = total_points * CREDIT_POINT_ANNUAL_BY_YEAR[year]

    donation_credit = 0.0
    section_46_min = SECTION_46_MIN_BY_YEAR[year]
    section_46_ceiling = SECTION_46_CEILING_BY_YEAR[year]
    if donations_annual > section_46_min:
        eligible = min(donations_annual, section_46_ceiling, salary_annual * 0.30)
        donation_credit = eligible * SECTION_46_CREDIT_RATE
    elif donations_annual > 0:
        notes.append(
            f"Donations of {donations_annual:,.0f} NIS do not exceed the {year} Section 46 minimum of "
            f"{section_46_min} NIS, so no donation credit was applied."
        )

    yishuv_credit = 0.0
    if yishuv_pct <= 0:
        notes.append(
            "No yishuv mutav credit applied (--yishuv-pct is 0). If the user's centre of life was in a "
            "preferred locality for 12+ continuous months, look the rate and ceiling up per locality in "
            "chapter ח of that year's ITA deductions booklet and re-run. Leaving this at 0 for an eligible "
            "resident silently understates the refund."
        )
    if yishuv_pct > 0:
        # Section 11 credit = the locality's rate x earned INCOME up to the locality ceiling
        # (Kol Zchut worked example: 11% x 168,000 = 18,480 NIS). It is a percentage of
        # income, not of tax; the max(0, ...) below stops it taking the tax under zero.
        if yishuv_ceiling and yishuv_ceiling > 0:
            capped_income = min(salary_annual, yishuv_ceiling)
            yishuv_credit = capped_income * (yishuv_pct / 100.0)
            if salary_annual > yishuv_ceiling:
                notes.append(
                    f"Yishuv mutav credit computed on income up to the locality ceiling of "
                    f"{yishuv_ceiling:,.0f} NIS, not on the full {salary_annual:,.0f} NIS."
                )
        else:
            yishuv_credit = salary_annual * (yishuv_pct / 100.0)
            notes.append(
                "Yishuv mutav credit applied to the WHOLE salary because no --yishuv-ceiling was given. "
                "Each locality has its own annual earned-income ceiling; above it the credit does not apply, "
                "so this OVERSTATES the credit for anyone earning more than their locality's ceiling. "
                "Look the ceiling up in chapter ח of that year's ITA deductions booklet and pass it."
            )

    tax_due_estimate = max(0.0, gross_tax - credit_value - donation_credit - yishuv_credit)
    refund = withheld_annual - tax_due_estimate

    # Present as a +/- 10% range to convey uncertainty.
    band = abs(refund) * 0.10
    refund_low = refund - band
    refund_high = refund + band

    if refund < 0:
        notes.append("Estimate is NEGATIVE: the user appears to OWE additional tax, not be owed a refund.")
    elif refund < 200:
        notes.append("Refund under 200 ₪. Worth confirming, but the Tax Authority sometimes does not process tiny refunds quickly.")

    notes.append(
        "This is an estimate based on aggregate annual figures and standard brackets. "
        "The Tax Authority's calculation uses month-by-month withholding histories that "
        "this estimator does not see, and may differ."
    )
    notes.append(
        "This models ONE taxpayer. For a married couple, run it once per spouse with that spouse's "
        "own Form 106 figures and credit points (separate computation on salary, Section 66(a)(1) "
        "and 66(c)(1) ITO); never sum both salaries into one --salary."
    )

    return RefundEstimate(
        tax_due_estimate=tax_due_estimate,
        tax_withheld=withheld_annual,
        refund_low=refund_low,
        refund_high=refund_high,
        notes=notes,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Estimate Israeli employee tax refund.")
    parser.add_argument("--year", type=int, required=True, help="Tax year being claimed (required: each year has its own brackets, point value and rules).")
    parser.add_argument("--salary", type=float, required=True, help="Annual taxable salary in NIS (sum across all employers).")
    parser.add_argument("--withheld", type=float, required=True, help="Total tax withheld in NIS (sum of field 042 across all Form 106 documents).")
    parser.add_argument("--points", type=float, default=2.25, help="Credit points for the year EXCLUDING children and Section 39B (default 2.25 = Israeli resident male; female resident gets 2.75; add oleh/single-parent/degree points here).")
    parser.add_argument("--child-ages", type=str, default="", help="Comma-separated ages each child REACHES during --year (0 = birth year, 18 = year the child turns 18). Adds that year's own child points.")
    parser.add_argument("--parent-side", choices=["mother", "father", "sole"], default="mother", help="mother = the mother (for parents living apart, the parent the children live with; also a single parent under s.40(b)(1)); father = the other parent; sole = a single parent under s.40(b)(1) (not married, not living with a partner) whose child's other parent died or is not registered (s.40(b)(1b)): both columns plus one point per family. Do not use after remarriage; list only the qualifying children.")
    parser.add_argument("--miluim-days", type=int, default=0, help="COMBAT reserve duty days served in the year before --year (Section 39B; counts only for tax year 2026 onward).")
    parser.add_argument("--donations", type=float, default=0.0, help="Total Section 46 donations in NIS.")
    parser.add_argument("--yishuv-pct", type=float, default=0.0, help="Yishuv mutav credit percentage for the locality (0 if not an eligible resident).")
    parser.add_argument("--yishuv-ceiling", type=float, default=0.0, help="Annual earned-income ceiling for that locality. Without it the credit is computed on the whole salary and is overstated for anyone earning above the ceiling.")
    args = parser.parse_args()

    miluim_bonus = 0.0
    days = args.miluim_days
    miluim_note = None
    if days > 0 and args.year < MILUIM_FIRST_TAX_YEAR:
        # Section 39B points first apply in tax year 2026 (for 2025 service); there is
        # nothing to add for an earlier claim year.
        days = 0
        miluim_note = (
            f"Section 39B reserve-duty points start with tax year {MILUIM_FIRST_TAX_YEAR} "
            f"(for service in {MILUIM_FIRST_TAX_YEAR - 1}); none were added to {args.year}."
        )
    elif days > 0 and args.year > MILUIM_LAST_SCHEDULE_YEAR:
        days = 0
        miluim_note = (
            f"The 30-day Section 39B schedule covers tax years {MILUIM_FIRST_TAX_YEAR}-"
            f"{MILUIM_LAST_SCHEDULE_YEAR} only; from 2028 the minimum drops to 20 days. "
            "No reserve-duty points were added."
        )
    if days >= 50:
        miluim_bonus = 1.0 + max(0, (days - 50) // 5) * 0.25
        miluim_bonus = min(miluim_bonus, 4.0)
    elif days >= 40:
        miluim_bonus = 0.75
    elif days >= 30:
        miluim_bonus = 0.5

    child_total = 0.0
    child_note = None
    if args.child_ages.strip():
        try:
            ages = [int(a) for a in args.child_ages.split(",") if a.strip()]
        except ValueError:
            print("error: --child-ages takes whole numbers, e.g. 0,7,14", file=sys.stderr)
            return 1
        if args.parent_side == "sole":
            per_child = [child_points(args.year, a, "mother") + child_points(args.year, a, "father") for a in ages]
        else:
            per_child = [child_points(args.year, a, args.parent_side) for a in ages]
        child_total = sum(per_child)
        sole_extra = args.parent_side == "sole" and any(0 <= a <= 18 for a in ages)
        if sole_extra:
            child_total += 1.0  # s.40(b)(1b): one additional point per family
        child_note = (
            f"Child points for {args.year} ({args.parent_side} side): "
            + ", ".join(f"age {a} = {pt:g}" for a, pt in zip(ages, per_child))
            + (" plus 1 point per family for a sole parent" if sole_extra else "")
            + f"; total {child_total:g}. The mother may move one birth-year point to the next tax year "
            "(s.66(ג)(4)(א1)); this run keeps it in the birth year."
        )

    try:
        result = estimate(
            year=args.year,
            salary_annual=args.salary,
            withheld_annual=args.withheld,
            points=args.points + child_total,
            miluim_points_bonus=miluim_bonus,
            donations_annual=args.donations,
            yishuv_pct=args.yishuv_pct,
            yishuv_ceiling=args.yishuv_ceiling,
        )
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(f"Year: {args.year}")
    print(f"Annual salary: {args.salary:,.0f} ₪")
    print(f"Tax withheld (sum of field 042): {args.withheld:,.0f} ₪")
    print(f"Tax due estimate: {result.tax_due_estimate:,.0f} ₪")
    print(f"Estimated refund range: {result.refund_low:,.0f} - {result.refund_high:,.0f} ₪")
    if miluim_note:
        result.notes.insert(0, miluim_note)
    if child_note:
        result.notes.insert(0, child_note)
    if miluim_bonus > 0:
        print(
            f"Reserve duty bonus applied: {miluim_bonus} points, worth up to "
            f"{miluim_bonus * CREDIT_POINT_ANNUAL_BY_YEAR[args.year]:,.0f} ₪ "
            "(credit points only reduce tax to zero, so the usable part can be less)"
        )
    print("\nNotes:")
    for n in result.notes:
        print(f"- {n}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
