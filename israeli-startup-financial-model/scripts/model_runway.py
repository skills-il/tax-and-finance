#!/usr/bin/env python3
"""Calculate startup runway with Israeli employment cost structure.

Models burn rate with Israeli employer overhead (pension, Keren Hishtalmut,
Bituach Leumi, severance), dual-currency costs (NIS/USD), and optional
IIA grant impact.

Usage:
    python scripts/model_runway.py --employees 5 --avg-salary 30000 --funding 500000
    python scripts/model_runway.py --employees 10 --avg-salary 35000 --funding 5000000 --grant-rate 0.3
    python scripts/model_runway.py --example
"""

import sys
import json
import argparse
from dataclasses import dataclass, asdict
from typing import Optional


# Israeli employer cost rates (2024-2025)
# שיעורי עלות מעסיק ישראליים
PENSION_RATE = 0.065          # פנסיה - 6.5%
SEVERANCE_RATE = 0.0833       # פיצויים - 8.33%
KEREN_HISHTALMUT_RATE = 0.075 # קרן השתלמות - 7.5%
BITUACH_LEUMI_RATE = 0.035    # ביטוח לאומי מעסיק - ~3.5%
RECREATION_MONTHLY = 380      # דמי הבראה - monthly average in NIS

# Default exchange rate (Bank of Israel representative rate)
DEFAULT_EXCHANGE_RATE = 3.6   # שער יציג - NIS per USD

# Default monthly USD costs per employee
DEFAULT_USD_COSTS_PER_EMPLOYEE = 200  # ענן, כלים - cloud, tools


@dataclass
class RunwayResult:
    """Result of runway calculation."""
    employees: int
    avg_gross_salary_nis: float
    employer_overhead_pct: float
    monthly_cost_per_employee_nis: float
    total_monthly_nis: float
    monthly_usd_costs: float
    total_monthly_burn_usd: float
    cash_balance_usd: float
    grant_monthly_offset_usd: float
    net_monthly_burn_usd: float
    runway_months: float
    exchange_rate: float


def calculate_employer_cost(
    gross_salary: float,
    include_keren_hishtalmut: bool = True,
) -> tuple:
    """Calculate total employer cost for an Israeli employee.

    Args:
        gross_salary: Monthly gross salary in NIS (שכר ברוטו).
        include_keren_hishtalmut: Whether employer pays Keren Hishtalmut
            (common in tech/startup sector).

    Returns:
        Tuple of (total employer cost in NIS, overhead percentage).
    """
    overhead = PENSION_RATE + SEVERANCE_RATE + BITUACH_LEUMI_RATE
    if include_keren_hishtalmut:
        overhead += KEREN_HISHTALMUT_RATE

    employer_cost = gross_salary * (1 + overhead) + RECREATION_MONTHLY
    overhead_pct = ((employer_cost / gross_salary) - 1) * 100

    return employer_cost, overhead_pct


def calculate_runway(
    num_employees: int,
    avg_salary_nis: float,
    cash_balance_usd: float,
    exchange_rate: float = DEFAULT_EXCHANGE_RATE,
    monthly_usd_costs: Optional[float] = None,
    grant_annual_nis: float = 0.0,
    include_keren_hishtalmut: bool = True,
) -> RunwayResult:
    """Calculate startup runway in months.

    Args:
        num_employees: Total number of employees.
        avg_salary_nis: Average monthly gross salary in NIS.
        cash_balance_usd: Current cash balance in USD.
        exchange_rate: NIS/USD exchange rate (שער חליפין).
        monthly_usd_costs: Monthly USD-denominated costs (cloud, tools).
            If None, uses default per-employee estimate.
        grant_annual_nis: Annual IIA grant amount in NIS (מענק שנתי).
        include_keren_hishtalmut: Whether to include Keren Hishtalmut.

    Returns:
        RunwayResult with detailed breakdown.
    """
    # חישוב עלות מעסיק לעובד
    cost_per_employee, overhead_pct = calculate_employer_cost(
        avg_salary_nis, include_keren_hishtalmut
    )

    # סה"כ עלויות חודשיות בש"ח
    total_monthly_nis = cost_per_employee * num_employees

    # עלויות חודשיות בדולר
    if monthly_usd_costs is None:
        monthly_usd_costs = DEFAULT_USD_COSTS_PER_EMPLOYEE * num_employees

    # שריפה חודשית כוללת בדולר
    total_burn_usd = (total_monthly_nis / exchange_rate) + monthly_usd_costs

    # קיזוז מענק (מחושב חודשי)
    grant_monthly_usd = (grant_annual_nis / 12) / exchange_rate

    # שריפה נטו לאחר מענק
    net_burn_usd = total_burn_usd - grant_monthly_usd

    # חישוב runway
    if net_burn_usd <= 0:
        runway = float("inf")
    else:
        runway = cash_balance_usd / net_burn_usd

    return RunwayResult(
        employees=num_employees,
        avg_gross_salary_nis=avg_salary_nis,
        employer_overhead_pct=round(overhead_pct, 1),
        monthly_cost_per_employee_nis=round(cost_per_employee, 0),
        total_monthly_nis=round(total_monthly_nis, 0),
        monthly_usd_costs=round(monthly_usd_costs, 0),
        total_monthly_burn_usd=round(total_burn_usd, 0),
        cash_balance_usd=cash_balance_usd,
        grant_monthly_offset_usd=round(grant_monthly_usd, 0),
        net_monthly_burn_usd=round(net_burn_usd, 0),
        runway_months=round(runway, 1),
        exchange_rate=exchange_rate,
    )


def print_result(result: RunwayResult) -> None:
    """Print runway calculation results in a readable format."""
    print("=" * 60)
    print("  Startup Runway Calculator / מחשבון Runway לסטארטאפ")
    print("=" * 60)
    print()
    print(f"  Employees (עובדים):              {result.employees}")
    print(f"  Avg gross salary (שכר ברוטו):    {result.avg_gross_salary_nis:,.0f} NIS")
    print(f"  Employer overhead (תקורה):        {result.employer_overhead_pct}%")
    print(f"  Cost per employee (עלות לעובד):  {result.monthly_cost_per_employee_nis:,.0f} NIS")
    print()
    print(f"  Monthly NIS costs (הוצאות ש\"ח):  {result.total_monthly_nis:,.0f} NIS")
    print(f"  Monthly USD costs (הוצאות $):    ${result.monthly_usd_costs:,.0f}")
    print(f"  Exchange rate (שער חליפין):       {result.exchange_rate} NIS/USD")
    print()
    print(f"  Total monthly burn (שריפה):      ${result.total_monthly_burn_usd:,.0f}")
    if result.grant_monthly_offset_usd > 0:
        print(f"  Grant offset (קיזוז מענק):      -${result.grant_monthly_offset_usd:,.0f}")
        print(f"  Net monthly burn (שריפה נטו):   ${result.net_monthly_burn_usd:,.0f}")
    print()
    print(f"  Cash balance (יתרת מזומן):       ${result.cash_balance_usd:,.0f}")
    print(f"  *** Runway: {result.runway_months} months ***")
    print("=" * 60)


def generate_example() -> None:
    """Generate example calculation for demonstration."""
    print("Example: Pre-seed startup with 3 developers + 2 founders")
    print("-" * 60)
    result = calculate_runway(
        num_employees=5,
        avg_salary_nis=25000,
        cash_balance_usd=500000,
        exchange_rate=3.6,
    )
    print_result(result)
    print()
    print("Example: Series A with 15 employees + IIA grant")
    print("-" * 60)
    result = calculate_runway(
        num_employees=15,
        avg_salary_nis=32000,
        cash_balance_usd=5000000,
        exchange_rate=3.6,
        grant_annual_nis=2000000,
    )
    print_result(result)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Calculate startup runway with Israeli cost structure "
                    "(מחשבון runway עם מבנה עלויות ישראלי)"
    )
    parser.add_argument(
        "--employees", type=int,
        help="Number of employees (מספר עובדים)"
    )
    parser.add_argument(
        "--avg-salary", type=float, default=30000,
        help="Average monthly gross salary in NIS (שכר ברוטו ממוצע, default: 30000)"
    )
    parser.add_argument(
        "--funding", type=float,
        help="Cash balance in USD (יתרת מזומן בדולר)"
    )
    parser.add_argument(
        "--exchange-rate", type=float, default=DEFAULT_EXCHANGE_RATE,
        help=f"NIS/USD exchange rate (שער חליפין, default: {DEFAULT_EXCHANGE_RATE})"
    )
    parser.add_argument(
        "--usd-costs", type=float, default=None,
        help="Monthly USD costs - cloud, tools (הוצאות דולריות חודשיות)"
    )
    parser.add_argument(
        "--grant-annual", type=float, default=0,
        help="Annual IIA grant in NIS (מענק שנתי מרשות החדשנות)"
    )
    parser.add_argument(
        "--grant-rate", type=float, default=0,
        help="IIA grant rate (0-1) applied to NIS costs (שיעור מענק)"
    )
    parser.add_argument(
        "--no-keren-hishtalmut", action="store_true",
        help="Exclude Keren Hishtalmut from employer costs"
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Output as JSON"
    )
    parser.add_argument(
        "--example", action="store_true",
        help="Show example calculations"
    )

    args = parser.parse_args()

    if args.example:
        generate_example()
        return

    if not args.employees or not args.funding:
        parser.print_help()
        print("\nError: --employees and --funding are required.")
        sys.exit(1)

    # If grant-rate is provided, calculate annual grant from costs
    grant_annual = args.grant_annual
    if args.grant_rate > 0 and grant_annual == 0:
        # Estimate annual NIS costs for grant calculation
        cost_per_emp, _ = calculate_employer_cost(
            args.avg_salary, not args.no_keren_hishtalmut
        )
        annual_nis = cost_per_emp * args.employees * 12
        grant_annual = annual_nis * args.grant_rate

    result = calculate_runway(
        num_employees=args.employees,
        avg_salary_nis=args.avg_salary,
        cash_balance_usd=args.funding,
        exchange_rate=args.exchange_rate,
        monthly_usd_costs=args.usd_costs,
        grant_annual_nis=grant_annual,
        include_keren_hishtalmut=not args.no_keren_hishtalmut,
    )

    if args.json:
        print(json.dumps(asdict(result), indent=2, ensure_ascii=False))
    else:
        print_result(result)


if __name__ == "__main__":
    main()
