#!/usr/bin/env python3
"""Calculate Israeli pension contributions and projections.

Computes mandatory pension contributions, keren hishtalmut benefits,
and basic retirement savings projections based on 2026 Israeli rates.

Usage:
    python scripts/calculate_pension.py --salary 20000
    python scripts/calculate_pension.py --salary 20000 --hishtalmut
    python scripts/calculate_pension.py --salary 15000 --self-employed
    python scripts/calculate_pension.py --example
"""

import sys
import argparse
from dataclasses import dataclass


PENSION_EMPLOYEE = 0.06          # 6%
PENSION_EMPLOYER = 0.065         # 6.5%
PENSION_SEVERANCE = 0.06         # 6%

HISHTALMUT_EMPLOYEE = 0.025      # 2.5%
HISHTALMUT_EMPLOYER = 0.075      # 7.5%

SELF_PENSION_LOW_RATE = 0.0445
SELF_PENSION_HIGH_RATE = 0.1255
SELF_HISHTALMUT_MAX = 20566      # Tax-free profit ceiling (2026)
SELF_HISHTALMUT_DEDUCT = 13203   # Tax deduction ceiling (2026)

AVG_WAGE = 13769                 # Average wage 2026 (BL §2 definition)
# NOTE: this is the salary implied by the tax-favoured DEPOSIT ceiling
# (20.5% x 2 x average wage = 5,645/month). It is NOT the mandatory-pension
# insurable ceiling, which is the average wage itself (13,769), and NOT the
# fund's maximum determining salary (about 41,307 = 3 x average wage).
COMPREHENSIVE_FUND_DEPOSIT_IMPLIED_SALARY = 2 * AVG_WAGE  # 27,538
MANDATORY_PENSION_INSURABLE_MAX = AVG_WAGE               # 13,769, tzav harchava
COMPREHENSIVE_FUND_INSURABLE_SALARY_MAX = 2 * AVG_WAGE   # kept for compatibility
COMPREHENSIVE_FUND_DEPOSIT_MAX = 5645  # Monthly deposit ceiling 2026 (20.5% of 2x avg wage)
HISHTALMUT_TAX_FREE_SALARY_CAP = 15712  # Monthly salary cap for tax-free employer hishtalmut (2026)


@dataclass
class PensionBreakdown:
    """Monthly pension contribution breakdown."""
    gross_salary: float
    insurable_salary: float
    employee_pension: float
    employer_pension: float
    employer_severance: float
    total_pension: float
    employee_hishtalmut: float
    employer_hishtalmut: float
    employer_hishtalmut_tax_free: float
    employer_hishtalmut_taxable: float
    total_hishtalmut: float
    total_monthly_savings: float
    annual_savings: float


def calculate_pension_contributions(
    monthly_salary: float,
    include_hishtalmut: bool = False,
) -> PensionBreakdown:
    """Calculate monthly pension and savings contributions.

    Uses the real comprehensive-fund insurable salary cap (2x average wage),
    and enforces the 15,712 NIS hishtalmut tax-free salary ceiling.
    """
    insurable = min(monthly_salary, COMPREHENSIVE_FUND_INSURABLE_SALARY_MAX)

    employee_pension = round(insurable * PENSION_EMPLOYEE, 2)
    employer_pension = round(insurable * PENSION_EMPLOYER, 2)
    employer_severance = round(insurable * PENSION_SEVERANCE, 2)
    total_pension = employee_pension + employer_pension + employer_severance

    employee_hish = 0.0
    employer_hish = 0.0
    employer_hish_tax_free = 0.0
    employer_hish_taxable = 0.0
    if include_hishtalmut:
        employee_hish = round(monthly_salary * HISHTALMUT_EMPLOYEE, 2)
        employer_hish = round(monthly_salary * HISHTALMUT_EMPLOYER, 2)
        tax_free_basis = min(monthly_salary, HISHTALMUT_TAX_FREE_SALARY_CAP)
        employer_hish_tax_free = round(tax_free_basis * HISHTALMUT_EMPLOYER, 2)
        employer_hish_taxable = round(employer_hish - employer_hish_tax_free, 2)

    total_hish = employee_hish + employer_hish
    total_monthly = total_pension + total_hish
    annual = round(total_monthly * 12, 2)

    return PensionBreakdown(
        gross_salary=monthly_salary,
        insurable_salary=insurable,
        employee_pension=employee_pension,
        employer_pension=employer_pension,
        employer_severance=employer_severance,
        total_pension=total_pension,
        employee_hishtalmut=employee_hish,
        employer_hishtalmut=employer_hish,
        employer_hishtalmut_tax_free=employer_hish_tax_free,
        employer_hishtalmut_taxable=employer_hish_taxable,
        total_hishtalmut=total_hish,
        total_monthly_savings=total_monthly,
        annual_savings=annual,
    )


def project_retirement(
    monthly_salary: float,
    current_age: int,
    gender: str = "male",
    retirement_age: float = None,
    annual_return: float = 0.04,
    existing_balance: float = 0,
) -> dict:
    """Project retirement savings based on current contributions.

    Uses realistic mekadem hamara annuity factors approximated from
    industry tables (male 67: ~205; female age 63y3m in 2026: ~230).
    These are approximations; real fund-specific factors vary by track
    and survivor coverage.

    Female retirement age in 2026 defaults to 63.25 (63 years 3 months);
    the year-of-birth schedule means the actual age may differ by cohort.
    """
    if retirement_age is None:
        retirement_age = 67 if gender == "male" else 63.25

    years = retirement_age - current_age
    if years <= 0:
        return {"error": "Already at or past retirement age"}

    insurable = min(monthly_salary, COMPREHENSIVE_FUND_INSURABLE_SALARY_MAX)
    monthly_contribution = insurable * (PENSION_EMPLOYEE + PENSION_EMPLOYER + PENSION_SEVERANCE)
    monthly_return = (1 + annual_return) ** (1 / 12) - 1

    balance = existing_balance
    n_months = int(round(years * 12))
    for _ in range(n_months):
        balance = balance * (1 + monthly_return) + monthly_contribution

    if gender == "male":
        mekadem = 205.0  # ~17 years
    else:
        mekadem = 230.0  # ~19 years; women have longer life expectancy + earlier retirement

    monthly_pension_gross = balance / mekadem if mekadem > 0 else 0

    KITZBAH_MEZAKAH_2026 = 9430.0
    EXEMPT_RATIO_2026 = 0.575
    exempt_amount = KITZBAH_MEZAKAH_2026 * EXEMPT_RATIO_2026
    taxable_amount = max(0.0, monthly_pension_gross - exempt_amount)
    monthly_pension_net = monthly_pension_gross - taxable_amount * 0.31

    return {
        "years_to_retirement": round(years, 2),
        "monthly_contribution": round(monthly_contribution, 2),
        "projected_balance": round(balance, 2),
        "estimated_monthly_pension_gross": round(monthly_pension_gross, 2),
        "estimated_monthly_pension_net_est": round(monthly_pension_net, 2),
        "assumptions": (
            f"{annual_return*100:.1f}% annual real return; retirement at age "
            f"{retirement_age}; mekadem hamara ~{mekadem:.0f}; tax estimated at 31% "
            f"marginal on the portion above the 2026 exempt amount ({exempt_amount:,.0f} NIS)."
        ),
    }


def format_breakdown(breakdown: PensionBreakdown) -> str:
    lines = [
        "=== Israeli Pension Contributions (2026) ===",
        "",
        f"  Gross Salary:               {breakdown.gross_salary:>10,.2f} NIS/month",
        f"  Insurable Salary (capped):  {breakdown.insurable_salary:>10,.2f} NIS/month",
    ]
    if breakdown.insurable_salary < breakdown.gross_salary:
        lines.append(
            f"    Note: salary above 2x avg wage ({COMPREHENSIVE_FUND_INSURABLE_SALARY_MAX:,} NIS) "
            "routes to a supplementary fund."
        )
    lines.extend([
        "",
        "  --- Pension (Keren Pensia) ---",
        f"  Employee (6%):              {breakdown.employee_pension:>10,.2f} NIS",
        f"  Employer Pension (6.5%):    {breakdown.employer_pension:>10,.2f} NIS",
        f"  Employer Severance (6%):    {breakdown.employer_severance:>10,.2f} NIS",
        f"  Total Pension:              {breakdown.total_pension:>10,.2f} NIS/month",
    ])

    if breakdown.total_hishtalmut > 0:
        lines.extend([
            "",
            "  --- Keren Hishtalmut ---",
            f"  Employee (2.5%):            {breakdown.employee_hishtalmut:>10,.2f} NIS",
            f"  Employer (7.5%):            {breakdown.employer_hishtalmut:>10,.2f} NIS",
            f"    Tax-free portion:         {breakdown.employer_hishtalmut_tax_free:>10,.2f} NIS",
            f"    Taxable portion:          {breakdown.employer_hishtalmut_taxable:>10,.2f} NIS",
            f"  Total Hishtalmut:           {breakdown.total_hishtalmut:>10,.2f} NIS/month",
        ])
        if breakdown.employer_hishtalmut_taxable > 0:
            lines.append(
                f"    Note: employer contribution on salary above "
                f"{HISHTALMUT_TAX_FREE_SALARY_CAP:,} NIS is taxable to the employee."
            )

    lines.extend([
        "",
        f"  Total Monthly Savings:      {breakdown.total_monthly_savings:>10,.2f} NIS",
        f"  Total Annual Savings:       {breakdown.annual_savings:>10,.2f} NIS",
        "",
        "  NOTE: Consult a licensed pension advisor (yoetz pensioni)",
        "        for personalized recommendations.",
    ])

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Calculate Israeli pension contributions (2026 rates)"
    )
    parser.add_argument("--salary", type=float, help="Monthly gross salary in NIS")
    parser.add_argument(
        "--hishtalmut", action="store_true",
        help="Include keren hishtalmut calculation (with 15,712 NIS salary cap)"
    )
    parser.add_argument(
        "--self-employed", action="store_true",
        help="Calculate for self-employed (atzmai); first business year is exempt"
    )
    parser.add_argument(
        "--project", action="store_true",
        help="Include retirement projection (with realistic mekadem hamara)"
    )
    parser.add_argument("--age", type=int, default=30, help="Current age for projection")
    parser.add_argument(
        "--female", action="store_true",
        help="Use female retirement age (63.25 in 2026, rising to 65 by 2032; year-of-birth schedule applies)"
    )
    parser.add_argument(
        "--first-business-year", action="store_true",
        help="Apply self-employed first-year exemption (no mandatory pension obligation)"
    )
    parser.add_argument(
        "--example", action="store_true", help="Show example calculation"
    )

    args = parser.parse_args()

    if args.example:
        print("Example: 20,000 NIS salary with keren hishtalmut (2026 rates)")
        print()
        breakdown = calculate_pension_contributions(20000, include_hishtalmut=True)
        print(format_breakdown(breakdown))
        print()
        print("  --- Retirement Projection (age 30, male, to 67) ---")
        projection = project_retirement(20000, 30)
        print(f"  Monthly contribution:        {projection['monthly_contribution']:>10,.2f} NIS")
        print(f"  Projected balance at 67:     {projection['projected_balance']:>10,.2f} NIS")
        print(f"  Est. monthly pension (gross):{projection['estimated_monthly_pension_gross']:>10,.2f} NIS")
        print(f"  Est. monthly pension (net):  {projection['estimated_monthly_pension_net_est']:>10,.2f} NIS")
        print(f"  Assumptions: {projection['assumptions']}")
        return

    if args.salary is None:
        parser.print_help()
        sys.exit(1)

    gender = "female" if args.female else "male"

    if args.self_employed:
        annual_income = args.salary * 12

        if args.first_business_year:
            mandatory = 0.0
            note_first_year = (
                "  Note: first calendar year of business is exempt from mandatory pension.\n"
            )
        else:
            half_avg = AVG_WAGE / 2
            if args.salary <= half_avg:
                mandatory = args.salary * SELF_PENSION_LOW_RATE
            elif args.salary <= AVG_WAGE:
                mandatory = (
                    half_avg * SELF_PENSION_LOW_RATE
                    + (args.salary - half_avg) * SELF_PENSION_HIGH_RATE
                )
            else:
                mandatory = (
                    half_avg * SELF_PENSION_LOW_RATE
                    + half_avg * SELF_PENSION_HIGH_RATE
                )
            note_first_year = ""

        print("=== Self-Employed Pension (2026) ===")
        print()
        print(f"  Monthly Income:                {args.salary:>10,.2f} NIS")
        print(f"  Annual Income:                 {annual_income:>10,.2f} NIS")
        print()
        print(f"  Mandatory Pension (monthly):   {mandatory:>10,.2f} NIS")
        print(f"  Mandatory Pension (annual):    {mandatory * 12:>10,.2f} NIS")
        if note_first_year:
            print()
            print(note_first_year, end="")
        if args.salary > AVG_WAGE and not args.first_business_year:
            print(
                f"  Note: income above full average wage ({AVG_WAGE:,} NIS/month) "
                "carries no additional mandatory obligation."
            )
        print()
        print("  Keren Hishtalmut (two separate ceilings):")
        print(f"    Tax deduction ceiling:       {SELF_HISHTALMUT_DEDUCT:>10,} NIS/year")
        print(f"    Profit-exempt ceiling:       {SELF_HISHTALMUT_MAX:>10,} NIS/year")
        print()
        print("  Obligation applies between age 21 and legal retirement age.")
        print("  NOTE: Consult a licensed pension advisor (yoetz pensioni)")
        print("        for personalized recommendations.")
        return

    breakdown = calculate_pension_contributions(args.salary, args.hishtalmut)
    print(format_breakdown(breakdown))

    if args.project:
        retirement_age = 63.25 if args.female else 67
        print()
        print(f"  --- Retirement Projection (age {args.age} -> {retirement_age}, {gender}) ---")
        projection = project_retirement(args.salary, args.age, gender=gender)
        if "error" in projection:
            print(f"  {projection['error']}")
        else:
            print(f"  Monthly contribution:         {projection['monthly_contribution']:>10,.2f} NIS")
            print(f"  Projected balance:            {projection['projected_balance']:>10,.2f} NIS")
            print(f"  Est. monthly pension (gross): {projection['estimated_monthly_pension_gross']:>10,.2f} NIS")
            print(f"  Est. monthly pension (net):   {projection['estimated_monthly_pension_net_est']:>10,.2f} NIS")
            print(f"  Assumptions: {projection['assumptions']}")


if __name__ == "__main__":
    main()
