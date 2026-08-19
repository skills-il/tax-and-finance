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

Pass --year to select that tax year's bracket table, credit-point value and
surtax threshold. Supported years are 2020 through 2026, which covers the
six-year retroactive window under Section 160 ITO. An unsupported year is
rejected rather than silently computed against another year's brackets.
2021-2026 come from the Israel Tax Authority deductions booklets; 2020 is
secondary-sourced and the estimator says so in its notes.
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
# ושכר עבודה" booklet PDFs (pdftotext text layer). 2020 is from a secondary source
# (Kol-Zchut historical table) because the ITA no longer serves the 2020 booklet;
# the estimator warns when 2020 is used.
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
# a donation that did qualify. Values read from that year's ITA deductions booklet text layer.
# The ITA no longer serves the 2020 and 2021 booklets, so those two years are deliberately absent:
# the estimator warns and declines to disqualify rather than guessing a minimum.
SECTION_46_CREDIT_RATE = 0.35
SECTION_46_MIN_BY_YEAR = {2022: 190, 2023: 200, 2024: 207, 2025: 207, 2026: 207}
SECTION_46_CEILING_BY_YEAR = {
    2022: 9517000, 2023: 10019808, 2024: 10354816, 2025: 10354816, 2026: 10354816,
}


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

    total_points = points + miluim_points_bonus
    credit_value = total_points * CREDIT_POINT_ANNUAL_BY_YEAR[year]

    donation_credit = 0.0
    section_46_min = SECTION_46_MIN_BY_YEAR.get(year)
    section_46_ceiling = SECTION_46_CEILING_BY_YEAR.get(year, 10354816)
    if donations_annual > 0 and section_46_min is None:
        # No primary-sourced minimum for this year. Grant the credit rather than disqualify,
        # and say so, because a wrongly-applied later-year minimum wipes out a real entitlement.
        notes.append(
            f"Section 46 minimum donation for {year} is not in this table (the ITA no longer publishes "
            f"the {year} deductions booklet). The credit was applied WITHOUT the minimum test. Look the "
            f"{year} minimum up before relying on this figure for a donation under about 200 NIS."
        )
        eligible = min(donations_annual, section_46_ceiling, salary_annual * 0.30)
        donation_credit = eligible * SECTION_46_CREDIT_RATE
    elif section_46_min is not None and donations_annual >= section_46_min:
        eligible = min(donations_annual, section_46_ceiling, salary_annual * 0.30)
        donation_credit = eligible * SECTION_46_CREDIT_RATE
    elif donations_annual > 0:
        notes.append(
            f"Donations of {donations_annual:,.0f} NIS are below the {year} Section 46 minimum of "
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
        # The locality ceiling caps the INCOME the credit applies to, not the credit amount.
        # Compute tax on income up to the ceiling, then take the percentage of that.
        if yishuv_ceiling and yishuv_ceiling > 0:
            capped_income = min(salary_annual, yishuv_ceiling)
            tax_on_capped = annual_tax_under_brackets(capped_income, BRACKETS_BY_YEAR_MONTHLY[year])
            base_for_yishuv = max(0.0, tax_on_capped - credit_value - donation_credit)
            yishuv_credit = base_for_yishuv * (yishuv_pct / 100.0)
            if salary_annual > yishuv_ceiling:
                notes.append(
                    f"Yishuv mutav credit applied to tax on income up to the locality ceiling of "
                    f"{yishuv_ceiling:,.0f} NIS, not to the full {salary_annual:,.0f} NIS."
                )
        else:
            yishuv_credit = max(0.0, gross_tax - credit_value - donation_credit) * (yishuv_pct / 100.0)
            notes.append(
                "Yishuv mutav credit applied to the WHOLE tax bill because no --yishuv-ceiling was given. "
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

    return RefundEstimate(
        tax_due_estimate=tax_due_estimate,
        tax_withheld=withheld_annual,
        refund_low=refund_low,
        refund_high=refund_high,
        notes=notes,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Estimate Israeli employee tax refund.")
    parser.add_argument("--year", type=int, default=2026, help="Tax year (default 2026).")
    parser.add_argument("--salary", type=float, required=True, help="Annual taxable salary in NIS (sum across all employers).")
    parser.add_argument("--withheld", type=float, required=True, help="Total tax withheld in NIS (sum of field 042 across all Form 106 documents).")
    parser.add_argument("--points", type=float, default=2.25, help="Base credit points for the year (default 2.25 = Israeli resident male; female resident gets 2.75; add child/oleh/single-parent/Section 39B miluim points separately).")
    parser.add_argument("--miluim-days", type=int, default=0, help="Reserve duty days served in the prior tax year.")
    parser.add_argument("--donations", type=float, default=0.0, help="Total Section 46 donations in NIS.")
    parser.add_argument("--yishuv-pct", type=float, default=0.0, help="Yishuv mutav credit percentage for the locality (0 if not an eligible resident).")
    parser.add_argument("--yishuv-ceiling", type=float, default=0.0, help="Annual earned-income ceiling for that locality. Without it the credit is applied to the whole tax bill and is overstated for anyone earning above the ceiling.")
    args = parser.parse_args()

    miluim_bonus = 0.0
    days = args.miluim_days
    if days >= 50:
        miluim_bonus = 1.0 + max(0, (days - 50) // 5) * 0.25
        miluim_bonus = min(miluim_bonus, 4.0)
    elif days >= 40:
        miluim_bonus = 0.75
    elif days >= 30:
        miluim_bonus = 0.5

    try:
        result = estimate(
            year=args.year,
            salary_annual=args.salary,
            withheld_annual=args.withheld,
            points=args.points,
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
    if miluim_bonus > 0:
        print(f"Reserve duty bonus applied: {miluim_bonus} points = {miluim_bonus * CREDIT_POINT_ANNUAL_BY_YEAR[args.year]:,.0f} ₪")
    print("\nNotes:")
    for n in result.notes:
        print(f"- {n}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
