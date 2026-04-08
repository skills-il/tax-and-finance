#!/usr/bin/env python3
"""Calculate Israeli pension contributions and projections.

Computes mandatory pension contributions, keren hishtalmut benefits,
and basic retirement savings projections based on Israeli rates.

Usage:
    python scripts/calculate_pension.py --salary 20000
    python scripts/calculate_pension.py --salary 20000 --hishtalmut
    python scripts/calculate_pension.py --salary 15000 --self-employed
    python scripts/calculate_pension.py --example
"""

import sys
import argparse
from dataclasses import dataclass


# Pension contribution rates (2026)
PENSION_EMPLOYEE = 0.06          # 6%
PENSION_EMPLOYER = 0.065         # 6.5%
PENSION_SEVERANCE = 0.06         # 6%

# Keren Hishtalmut rates
HISHTALMUT_EMPLOYEE = 0.025      # 2.5%
HISHTALMUT_EMPLOYER = 0.075      # 7.5%

# Self-employed rates (2026)
SELF_PENSION_LOW_RATE = 0.0445   # Up to half avg wage
SELF_PENSION_HIGH_RATE = 0.1255  # Half to full avg wage
SELF_HISHTALMUT_MAX = 20566      # Tax-free profit ceiling (2026)
SELF_HISHTALMUT_DEDUCT = 13203   # Tax deduction ceiling (2026)

# Reference wage and fund ceiling (2026)
AVG_WAGE = 13769                 # Average wage 2026
COMPREHENSIVE_FUND_MAX = 5645    # Max monthly pension deposit (20.5% of 2x avg wage, 2026)


@dataclass
class PensionBreakdown:
    """Monthly pension contribution breakdown."""
    gross_salary: float
    # Employee pension
    employee_pension: float
    employer_pension: float
    employer_severance: float
    total_pension: float
    # Keren hishtalmut
    employee_hishtalmut: float
    employer_hishtalmut: float
    total_hishtalmut: float
    # Totals
    total_monthly_savings: float
    annual_savings: float


def calculate_pension_contributions(
    monthly_salary: float,
    include_hishtalmut: bool = False,
) -> PensionBreakdown:
    """Calculate monthly pension and savings contributions.

    Args:
        monthly_salary: Gross monthly salary in NIS.
        include_hishtalmut: Include keren hishtalmut calculation.

    Returns:
        PensionBreakdown with all contribution details.
    """
    total_contribution_rate = PENSION_EMPLOYEE + PENSION_EMPLOYER + PENSION_SEVERANCE
    max_insurable = COMPREHENSIVE_FUND_MAX / total_contribution_rate
    insurable = min(monthly_salary, max_insurable)

    employee_pension = round(insurable * PENSION_EMPLOYEE, 2)
    employer_pension = round(insurable * PENSION_EMPLOYER, 2)
    employer_severance = round(insurable * PENSION_SEVERANCE, 2)
    total_pension = employee_pension + employer_pension + employer_severance

    employee_hish = 0.0
    employer_hish = 0.0
    if include_hishtalmut:
        employee_hish = round(monthly_salary * HISHTALMUT_EMPLOYEE, 2)
        employer_hish = round(monthly_salary * HISHTALMUT_EMPLOYER, 2)

    total_hish = employee_hish + employer_hish
    total_monthly = total_pension + total_hish
    annual = round(total_monthly * 12, 2)

    return PensionBreakdown(
        gross_salary=monthly_salary,
        employee_pension=employee_pension,
        employer_pension=employer_pension,
        employer_severance=employer_severance,
        total_pension=total_pension,
        employee_hishtalmut=employee_hish,
        employer_hishtalmut=employer_hish,
        total_hishtalmut=total_hish,
        total_monthly_savings=total_monthly,
        annual_savings=annual,
    )


def project_retirement(
    monthly_salary: float,
    current_age: int,
    gender: str = "male",
    retirement_age: int = None,
    annual_return: float = 0.04,
    existing_balance: float = 0,
) -> dict:
    """Project retirement savings based on current contributions.

    Args:
        monthly_salary: Current gross monthly salary.
        current_age: Current age in years.
        gender: "male" or "female" (affects default retirement age).
        retirement_age: Target retirement age (defaults by gender: male 67, female 64).
        annual_return: Expected annual investment return rate.
        existing_balance: Current pension balance.

    Returns:
        Dictionary with projection details.
    """
    if retirement_age is None:
        retirement_age = 67 if gender == "male" else 64

    years = retirement_age - current_age
    if years <= 0:
        return {"error": "Already at or past retirement age"}

    total_contribution_rate = PENSION_EMPLOYEE + PENSION_EMPLOYER + PENSION_SEVERANCE
    max_insurable = COMPREHENSIVE_FUND_MAX / total_contribution_rate
    insurable = min(monthly_salary, max_insurable)
    monthly_contribution = insurable * (PENSION_EMPLOYEE + PENSION_EMPLOYER + PENSION_SEVERANCE)
    monthly_return = (1 + annual_return) ** (1 / 12) - 1

    balance = existing_balance
    for _ in range(years * 12):
        balance = balance * (1 + monthly_return) + monthly_contribution

    # Estimate monthly pension (approximate annuity factor)
    life_expectancy_months = (85 - retirement_age) * 12
    if life_expectancy_months > 0:
        monthly_pension = balance / life_expectancy_months
    else:
        monthly_pension = 0

    return {
        "years_to_retirement": years,
        "monthly_contribution": round(monthly_contribution, 2),
        "projected_balance": round(balance, 2),
        "estimated_monthly_pension": round(monthly_pension, 2),
        "assumptions": f"{annual_return*100:.1f}% annual return, retirement at {retirement_age}",
    }


def format_breakdown(breakdown: PensionBreakdown) -> str:
    """Format pension breakdown for display."""
    lines = [
        "=== Israeli Pension Contributions (2026) ===",
        "",
        f"  Gross Salary:            {breakdown.gross_salary:>10,.2f} NIS/month",
        "",
        "  --- Pension (Keren Pensia) ---",
        f"  Employee (6%):           {breakdown.employee_pension:>10,.2f} NIS",
        f"  Employer Pension (6.5%): {breakdown.employer_pension:>10,.2f} NIS",
        f"  Employer Severance (6%): {breakdown.employer_severance:>10,.2f} NIS",
        f"  Total Pension:           {breakdown.total_pension:>10,.2f} NIS/month",
    ]

    if breakdown.total_hishtalmut > 0:
        lines.extend([
            "",
            "  --- Keren Hishtalmut ---",
            f"  Employee (2.5%):         {breakdown.employee_hishtalmut:>10,.2f} NIS",
            f"  Employer (7.5%):         {breakdown.employer_hishtalmut:>10,.2f} NIS",
            f"  Total Hishtalmut:        {breakdown.total_hishtalmut:>10,.2f} NIS/month",
        ])

    lines.extend([
        "",
        f"  Total Monthly Savings:   {breakdown.total_monthly_savings:>10,.2f} NIS",
        f"  Total Annual Savings:    {breakdown.annual_savings:>10,.2f} NIS",
        "",
        "  NOTE: Consult a licensed pension advisor (yoetz pensioni)",
        "        for personalized recommendations.",
    ])

    return "\n".join(lines)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Calculate Israeli pension contributions"
    )
    parser.add_argument("--salary", type=float, help="Monthly gross salary in NIS")
    parser.add_argument(
        "--hishtalmut", action="store_true",
        help="Include keren hishtalmut calculation"
    )
    parser.add_argument(
        "--self-employed", action="store_true",
        help="Calculate for self-employed (atzmai)"
    )
    parser.add_argument(
        "--project", action="store_true",
        help="Include retirement projection"
    )
    parser.add_argument("--age", type=int, default=30, help="Current age for projection")
    parser.add_argument(
        "--female", action="store_true",
        help="Use female retirement age (~64 in 2026)"
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
        print("  --- Retirement Projection (age 30 -> 67) ---")
        projection = project_retirement(20000, 30)
        print(f"  Monthly contribution:     {projection['monthly_contribution']:>10,.2f} NIS")
        print(f"  Projected balance at 67:  {projection['projected_balance']:>10,.2f} NIS")
        print(f"  Est. monthly pension:     {projection['estimated_monthly_pension']:>10,.2f} NIS")
        print(f"  Assumptions: {projection['assumptions']}")
        return

    if args.salary is None:
        parser.print_help()
        sys.exit(1)

    gender = "female" if args.female else "male"

    if args.self_employed:
        annual_income = args.salary * 12
        half_avg = AVG_WAGE / 2
        if args.salary <= half_avg:
            mandatory = args.salary * SELF_PENSION_LOW_RATE
        else:
            mandatory = (half_avg * SELF_PENSION_LOW_RATE
                         + min(args.salary - half_avg, AVG_WAGE - half_avg) * SELF_PENSION_HIGH_RATE)

        print("=== Self-Employed Pension (2026) ===")
        print()
        print(f"  Monthly Income:                {args.salary:>10,.2f} NIS")
        print(f"  Annual Income:                 {annual_income:>10,.2f} NIS")
        print()
        print(f"  Mandatory Pension (monthly):   {mandatory:>10,.2f} NIS")
        print(f"  Mandatory Pension (annual):    {mandatory * 12:>10,.2f} NIS")
        print()
        print(f"  Keren Hishtalmut:")
        print(f"    Tax deduction ceiling:       {SELF_HISHTALMUT_DEDUCT:>10,} NIS/year")
        print(f"    Profit-exempt ceiling:       {SELF_HISHTALMUT_MAX:>10,} NIS/year")
        print()
        print("  NOTE: Consult a licensed pension advisor (yoetz pensioni)")
        print("        for personalized recommendations.")
        return

    breakdown = calculate_pension_contributions(args.salary, args.hishtalmut)
    print(format_breakdown(breakdown))

    if args.project:
        retirement_age = 64 if args.female else 67
        print()
        print(f"  --- Retirement Projection (age {args.age} -> {retirement_age}) ---")
        projection = project_retirement(args.salary, args.age, gender=gender)
        if "error" in projection:
            print(f"  {projection['error']}")
        else:
            print(f"  Monthly contribution:     {projection['monthly_contribution']:>10,.2f} NIS")
            print(f"  Projected balance at {retirement_age}:  {projection['projected_balance']:>10,.2f} NIS")
            print(f"  Est. monthly pension:     {projection['estimated_monthly_pension']:>10,.2f} NIS")
            print(f"  Assumptions: {projection['assumptions']}")


if __name__ == "__main__":
    main()
