#!/usr/bin/env python3
"""Calculate Israeli household budget and mortgage estimates.

Provides tools for monthly budget planning, mortgage calculations,
and tax estimation for Israeli households.

Usage:
    python budget_calculator.py --salary 15000
    python budget_calculator.py --mortgage --amount 1500000 --years 25
    python budget_calculator.py --help
"""

import argparse
from decimal import Decimal, ROUND_HALF_UP

TAX_BRACKETS = [
    (84120, Decimal("0.10")), (120720, Decimal("0.14")),
    (193800, Decimal("0.20")), (269280, Decimal("0.31")),
    (560280, Decimal("0.35")), (721560, Decimal("0.47")),
    (999999999, Decimal("0.50")),
]

BITUACH_LEUMI_LOW = Decimal("0.004")
BITUACH_LEUMI_HIGH = Decimal("0.07")
HEALTH_TAX_LOW = Decimal("0.031")
HEALTH_TAX_HIGH = Decimal("0.05")
BL_THRESHOLD = Decimal("7122")
CREDIT_POINTS = Decimal("2.25")
CREDIT_VALUE = Decimal("242")

def calc_monthly_tax(monthly_salary):
    annual = Decimal(str(monthly_salary)) * 12
    tax = Decimal("0")
    prev = Decimal("0")
    for limit, rate in TAX_BRACKETS:
        if annual <= prev:
            break
        taxable = min(annual, Decimal(str(limit))) - prev
        tax += taxable * rate
        prev = Decimal(str(limit))
    credit = CREDIT_POINTS * CREDIT_VALUE * 12
    annual_tax = max(Decimal("0"), tax - credit)
    return (annual_tax / 12).quantize(Decimal("0.01"), ROUND_HALF_UP)

def calc_bituach_leumi(monthly_salary):
    sal = Decimal(str(monthly_salary))
    if sal <= BL_THRESHOLD:
        return (sal * BITUACH_LEUMI_LOW).quantize(Decimal("0.01"))
    low_part = BL_THRESHOLD * BITUACH_LEUMI_LOW
    high_part = (sal - BL_THRESHOLD) * BITUACH_LEUMI_HIGH
    return (low_part + high_part).quantize(Decimal("0.01"))

def calc_health_tax(monthly_salary):
    sal = Decimal(str(monthly_salary))
    if sal <= BL_THRESHOLD:
        return (sal * HEALTH_TAX_LOW).quantize(Decimal("0.01"))
    low_part = BL_THRESHOLD * HEALTH_TAX_LOW
    high_part = (sal - BL_THRESHOLD) * HEALTH_TAX_HIGH
    return (low_part + high_part).quantize(Decimal("0.01"))

def show_salary_breakdown(salary):
    tax = calc_monthly_tax(salary)
    bl = calc_bituach_leumi(salary)
    health = calc_health_tax(salary)
    pension = Decimal(str(salary)) * Decimal("0.06")
    net = Decimal(str(salary)) - tax - bl - health - pension

    print(f"\nSalary Breakdown: {salary:,.0f} NIS/month")
    print("=" * 40)
    print(f"  Gross salary:        {salary:>10,.2f} NIS")
    print(f"  Income tax:          {tax:>10,.2f} NIS")
    print(f"  Bituach Leumi:       {bl:>10,.2f} NIS")
    print(f"  Health tax:          {health:>10,.2f} NIS")
    print(f"  Pension (6%):        {pension:>10,.2f} NIS")
    print(f"  --------------------------------")
    print(f"  Net salary:          {net:>10,.2f} NIS")

def calc_mortgage(amount, years, rate=0.055):
    monthly_rate = Decimal(str(rate)) / 12
    n_payments = years * 12
    amt = Decimal(str(amount))
    payment = amt * (monthly_rate * (1 + monthly_rate) ** n_payments) / ((1 + monthly_rate) ** n_payments - 1)
    total = payment * n_payments

    print(f"\nMortgage Calculator")
    print("=" * 40)
    print(f"  Loan amount:     {amount:>12,} NIS")
    print(f"  Term:            {years:>12} years")
    print(f"  Interest rate:   {rate*100:>11.2f}%")
    print(f"  Monthly payment: {payment:>12,.2f} NIS")
    print(f"  Total paid:      {total:>12,.0f} NIS")
    print(f"  Total interest:  {total - amt:>12,.0f} NIS")

def main():
    parser = argparse.ArgumentParser(description="Israeli budget calculator")
    parser.add_argument("--salary", type=float, help="Monthly gross salary in NIS")
    parser.add_argument("--mortgage", action="store_true", help="Calculate mortgage")
    parser.add_argument("--amount", type=float, help="Mortgage amount in NIS")
    parser.add_argument("--years", type=int, default=25, help="Mortgage term in years")
    parser.add_argument("--rate", type=float, default=0.055, help="Annual interest rate")
    args = parser.parse_args()

    if args.salary:
        show_salary_breakdown(args.salary)
    elif args.mortgage and args.amount:
        calc_mortgage(args.amount, args.years, args.rate)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
