#!/usr/bin/env python3
"""Calculate Israeli payroll: gross to net salary with all deductions.

Computes income tax (progressive brackets), Bituach Leumi (National Insurance),
health tax, and pension contributions based on 2025 Israeli rates.

Usage:
    python scripts/calculate_payroll.py --gross 20000
    python scripts/calculate_payroll.py --gross 20000 --credits 2.75 --pension
    python scripts/calculate_payroll.py --gross 15000 --employer-cost
    python scripts/calculate_payroll.py --example
"""

import sys
import argparse
from dataclasses import dataclass


# 2025 Israeli Income Tax Brackets (monthly)
TAX_BRACKETS = [
    (7010, 0.10),
    (10060, 0.14),
    (16150, 0.20),
    (22440, 0.31),
    (46690, 0.35),
    (60130, 0.47),
    (float("inf"), 0.50),
]

# Tax credit point value (monthly, 2025)
CREDIT_POINT_VALUE = 242  # NIS per month

# Bituach Leumi (National Insurance) rates for employees
NI_REDUCED_CEILING = 7122       # NIS/month
NI_FULL_CEILING = 49030         # NIS/month (max insurable salary)
NI_REDUCED_RATE = 0.004         # 0.4% employee NI
NI_FULL_RATE = 0.07             # 7.0% employee NI
HEALTH_REDUCED_RATE = 0.031     # 3.1% employee health
HEALTH_FULL_RATE = 0.05         # 5.0% employee health

# Employer rates
EMPLOYER_NI_REDUCED = 0.038     # 3.8% employer NI (reduced bracket)
EMPLOYER_NI_FULL = 0.076        # 7.6% employer NI (full bracket)
EMPLOYER_HEALTH_REDUCED = 0.034 # 3.4% employer health (reduced)
EMPLOYER_HEALTH_FULL = 0.0345   # 3.45% employer health (full)

# Pension rates
PENSION_EMPLOYEE = 0.06         # 6% employee
PENSION_EMPLOYER = 0.065        # 6.5% employer
PENSION_SEVERANCE = 0.06        # 6% employer severance (pitzuim)


@dataclass
class PayrollResult:
    """Complete payroll calculation result."""
    gross_salary: float
    income_tax: float
    bituach_leumi: float
    health_tax: float
    pension_employee: float
    net_salary: float
    # Employer costs
    employer_ni: float = 0.0
    employer_health: float = 0.0
    employer_pension: float = 0.0
    employer_severance: float = 0.0
    total_employer_cost: float = 0.0


def calculate_income_tax(monthly_gross: float, credit_points: float = 2.25) -> float:
    """Calculate monthly income tax using progressive brackets.

    Args:
        monthly_gross: Gross monthly salary in NIS.
        credit_points: Number of tax credit points (nekudot zikui).

    Returns:
        Monthly income tax amount in NIS.
    """
    tax = 0.0
    prev_ceiling = 0

    for ceiling, rate in TAX_BRACKETS:
        if monthly_gross <= prev_ceiling:
            break
        taxable = min(monthly_gross, ceiling) - prev_ceiling
        tax += taxable * rate
        prev_ceiling = ceiling

    # Apply credit points
    credit_value = credit_points * CREDIT_POINT_VALUE
    tax = max(0, tax - credit_value)

    return round(tax, 2)


def calculate_bituach_leumi(monthly_gross: float) -> tuple[float, float]:
    """Calculate employee National Insurance and Health Tax.

    Args:
        monthly_gross: Gross monthly salary in NIS.

    Returns:
        Tuple of (national_insurance, health_tax) in NIS.
    """
    insurable = min(monthly_gross, NI_FULL_CEILING)

    # Reduced bracket
    reduced_portion = min(insurable, NI_REDUCED_CEILING)
    ni = reduced_portion * NI_REDUCED_RATE
    health = reduced_portion * HEALTH_REDUCED_RATE

    # Full bracket
    if insurable > NI_REDUCED_CEILING:
        full_portion = insurable - NI_REDUCED_CEILING
        ni += full_portion * NI_FULL_RATE
        health += full_portion * HEALTH_FULL_RATE

    return round(ni, 2), round(health, 2)


def calculate_employer_contributions(monthly_gross: float) -> tuple[float, float]:
    """Calculate employer NI and health contributions.

    Args:
        monthly_gross: Gross monthly salary in NIS.

    Returns:
        Tuple of (employer_ni, employer_health) in NIS.
    """
    insurable = min(monthly_gross, NI_FULL_CEILING)

    reduced_portion = min(insurable, NI_REDUCED_CEILING)
    ni = reduced_portion * EMPLOYER_NI_REDUCED
    health = reduced_portion * EMPLOYER_HEALTH_REDUCED

    if insurable > NI_REDUCED_CEILING:
        full_portion = insurable - NI_REDUCED_CEILING
        ni += full_portion * EMPLOYER_NI_FULL
        health += full_portion * EMPLOYER_HEALTH_FULL

    return round(ni, 2), round(health, 2)


def calculate_payroll(
    gross_salary: float,
    credit_points: float = 2.25,
    has_pension: bool = True,
    calc_employer: bool = False,
) -> PayrollResult:
    """Calculate complete payroll breakdown.

    Args:
        gross_salary: Monthly gross salary in NIS.
        credit_points: Tax credit points (default 2.25 for male resident).
        has_pension: Whether pension deductions apply.
        calc_employer: Whether to calculate employer cost.

    Returns:
        PayrollResult with all deduction details.
    """
    income_tax = calculate_income_tax(gross_salary, credit_points)
    ni, health = calculate_bituach_leumi(gross_salary)

    pension_employee = round(gross_salary * PENSION_EMPLOYEE, 2) if has_pension else 0.0

    net_salary = round(
        gross_salary - income_tax - ni - health - pension_employee, 2
    )

    result = PayrollResult(
        gross_salary=gross_salary,
        income_tax=income_tax,
        bituach_leumi=ni,
        health_tax=health,
        pension_employee=pension_employee,
        net_salary=net_salary,
    )

    if calc_employer:
        emp_ni, emp_health = calculate_employer_contributions(gross_salary)
        emp_pension = round(gross_salary * PENSION_EMPLOYER, 2) if has_pension else 0.0
        emp_severance = round(gross_salary * PENSION_SEVERANCE, 2) if has_pension else 0.0

        result.employer_ni = emp_ni
        result.employer_health = emp_health
        result.employer_pension = emp_pension
        result.employer_severance = emp_severance
        result.total_employer_cost = round(
            gross_salary + emp_ni + emp_health + emp_pension + emp_severance, 2
        )

    return result


def format_payslip(result: PayrollResult, show_employer: bool = False) -> str:
    """Format payroll result as a readable payslip."""
    lines = [
        "=== Israeli Payroll Calculation (Tlush Maskoret) ===",
        "",
        f"  Gross Salary (Bruto):      {result.gross_salary:>10,.2f} NIS",
        f"  Income Tax (Mas Hachnasa): -{result.income_tax:>10,.2f} NIS",
        f"  Bituach Leumi (NI):        -{result.bituach_leumi:>10,.2f} NIS",
        f"  Health Tax (Mas Briut):    -{result.health_tax:>10,.2f} NIS",
        f"  Pension (Employee 6%):     -{result.pension_employee:>10,.2f} NIS",
        f"  {'─' * 42}",
        f"  Net Salary (Neto):          {result.net_salary:>10,.2f} NIS",
    ]

    if show_employer and result.total_employer_cost > 0:
        lines.extend([
            "",
            "  === Employer Cost ===",
            f"  Gross Salary:               {result.gross_salary:>10,.2f} NIS",
            f"  Employer NI:               +{result.employer_ni:>10,.2f} NIS",
            f"  Employer Health:           +{result.employer_health:>10,.2f} NIS",
            f"  Employer Pension (6.5%):   +{result.employer_pension:>10,.2f} NIS",
            f"  Employer Severance (6%):   +{result.employer_severance:>10,.2f} NIS",
            f"  {'─' * 42}",
            f"  Total Employer Cost:        {result.total_employer_cost:>10,.2f} NIS",
        ])

    lines.extend([
        "",
        "NOTE: Estimate based on 2025 rates. Consult a certified",
        "      accountant (roeh cheshbon) for exact figures.",
    ])
    return "\n".join(lines)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Calculate Israeli payroll (gross to net)"
    )
    parser.add_argument("--gross", type=float, help="Monthly gross salary in NIS")
    parser.add_argument(
        "--credits", type=float, default=2.25,
        help="Tax credit points (default: 2.25 for male resident)"
    )
    parser.add_argument(
        "--no-pension", action="store_true", help="Exclude pension deductions"
    )
    parser.add_argument(
        "--employer-cost", action="store_true",
        help="Include employer cost calculation"
    )
    parser.add_argument(
        "--example", action="store_true", help="Show example calculation"
    )

    args = parser.parse_args()

    if args.example:
        print("Example: 20,000 NIS gross, male resident (2.25 credits), with pension")
        print()
        result = calculate_payroll(20000, 2.25, True, True)
        print(format_payslip(result, show_employer=True))
        return

    if args.gross is None:
        parser.print_help()
        sys.exit(1)

    result = calculate_payroll(
        args.gross,
        args.credits,
        not args.no_pension,
        args.employer_cost,
    )
    print(format_payslip(result, show_employer=args.employer_cost))


if __name__ == "__main__":
    main()
