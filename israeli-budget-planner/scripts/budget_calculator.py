#!/usr/bin/env python3
"""Calculate Israeli household budget and mortgage estimates.

Provides tools for monthly budget planning, mortgage calculations,
and tax estimation for Israeli households.

SCOPE AND LIMITS. This models a SALARIED employee with ONE employer. It is not a
payslip and will not match one exactly. In particular it does NOT model:
  * credit points beyond the number you pass in --credit-points. Parents are
    entitled to additional credit points for their children, which for a family
    is usually the single largest correction to this figure. Look up the current
    entitlement and pass the real total.
  * the tax credit granted on the employee's own pension contribution, so the
    income-tax line here is conservative (too high).
  * a keren hishtalmut deduction, if the employee has one.
  * a second employer. With two jobs the reduced band and the credit points
    cannot both be claimed twice: the secondary employer withholds at the full
    band and top tax rate until a tiaum (dmei bituach and mas) is filed. Running
    each job through this tool separately will overstate combined net pay.
  * taxable benefits added to salary, such as a company car.
  * the SELF-EMPLOYED. Osek patur and osek murshe pay different Bituach Leumi and
    health rates and have deductible expenses and mikdamot; do not use --salary
    for them, the answer will be wrong.

Usage:
    python budget_calculator.py --salary 15000
    python budget_calculator.py --mortgage --amount 1500000 --years 25
    python budget_calculator.py --help
"""

import argparse
from decimal import Decimal, ROUND_HALF_UP

# 2026 annual income-tax brackets (widened retroactively from 1 Jan 2026 under
# the Economic Efficiency Law; the 20% step now runs to 228,000 and the 31% step
# to 301,200 NIS/year). Source: kolzchut מדרגות מס הכנסה, ITA 2026 table.
TAX_BRACKETS = [
    (84120, Decimal("0.10")), (120720, Decimal("0.14")),
    (228000, Decimal("0.20")), (301200, Decimal("0.31")),
    (560280, Decimal("0.35")), (721560, Decimal("0.47")),
    (999999999, Decimal("0.50")),
]

# Employee (salaried) Bituach Leumi + health-tax rates.
# The rate is NOT one number: it varies by age and pension status. The BTL table
# "לעובדים שכירים" publishes a row per category; the default row below applies only
# to a resident aged 18 to retirement age. Percentages carry 2025 effective dates
# and did not change for 2026; only the two thresholds did.
# Each entry: (bituach_leumi_low, bituach_leumi_high, health_low, health_high).
# Rows where the combined employee rate is health-tax only carry BL 0.
CATEGORIES = {
    "default": (Decimal("0.0104"), Decimal("0.07"), Decimal("0.0323"), Decimal("0.0517")),
    "under18": (Decimal("0"), Decimal("0"), Decimal("0"), Decimal("0")),
    "old-age-pension": (Decimal("0"), Decimal("0"), Decimal("0"), Decimal("0")),
    "disability-pension": (Decimal("0"), Decimal("0"), Decimal("0.0323"), Decimal("0.0517")),
    "age67-70": (Decimal("0.007"), Decimal("0.0486"), Decimal("0.0323"), Decimal("0.0517")),
    "controlling-shareholder": (Decimal("0.0102"), Decimal("0.0679"), Decimal("0.0323"), Decimal("0.0517")),
    "woman-between-retirement-ages": (Decimal("0.0072"), Decimal("0.0507"), Decimal("0.0323"), Decimal("0.0517")),
    "new-resident-over-62": (Decimal("0.0037"), Decimal("0.0228"), Decimal("0.0323"), Decimal("0.0517")),
}
# Published COMBINED employee rates per category (reduced band, full band). These are
# the authoritative figures from the BTL table; the split above is derived by
# subtracting the health-tax leg, so report combined totals when they are what matters.
CATEGORY_COMBINED = {
    "default": (Decimal("0.0427"), Decimal("0.1217")),
    "under18": (Decimal("0"), Decimal("0")),
    "old-age-pension": (Decimal("0"), Decimal("0")),
    "disability-pension": (Decimal("0.0323"), Decimal("0.0517")),
    "age67-70": (Decimal("0.0393"), Decimal("0.1003")),
    "controlling-shareholder": (Decimal("0.0425"), Decimal("0.1196")),
    "woman-between-retirement-ages": (Decimal("0.0395"), Decimal("0.1024")),
    "new-resident-over-62": (Decimal("0.036"), Decimal("0.0745")),
}
# Reduced-collection step from 1 Jan 2026. Published as an absolute amount; do not
# restate it as a fraction of the average wage, it matches neither section 1 nor 2.
BL_THRESHOLD = Decimal("7703")
# Maximum monthly income subject to Bituach Leumi + health insurance (from 1 Jan 2026).
# Salary above this ceiling is NOT charged BL/health, so the high band must be capped here.
BL_CEILING = Decimal("51910")
# Base credit points for a resident. Women get +0.5 (2.75); new immigrants get extra
# for 3.5 years. Point value 242 NIS/month (2026); verify with the tax authority.
CREDIT_POINTS = Decimal("2.25")
CREDIT_VALUE = Decimal("242")

def calc_monthly_tax(monthly_salary, credit_points=CREDIT_POINTS):
    annual = Decimal(str(monthly_salary)) * 12
    tax = Decimal("0")
    prev = Decimal("0")
    for limit, rate in TAX_BRACKETS:
        if annual <= prev:
            break
        taxable = min(annual, Decimal(str(limit))) - prev
        tax += taxable * rate
        prev = Decimal(str(limit))
    credit = Decimal(str(credit_points)) * CREDIT_VALUE * 12
    annual_tax = max(Decimal("0"), tax - credit)
    return (annual_tax / 12).quantize(Decimal("0.01"), ROUND_HALF_UP)

def _banded(monthly_salary, low_rate, high_rate):
    """Apply a two-band rate, capped at the maximum insurable income."""
    sal = Decimal(str(monthly_salary))
    if sal <= BL_THRESHOLD:
        return (sal * low_rate).quantize(Decimal("0.01"))
    capped = min(sal, BL_CEILING)
    return (BL_THRESHOLD * low_rate + (capped - BL_THRESHOLD) * high_rate).quantize(Decimal("0.01"))

def calc_bituach_leumi(monthly_salary, category="default"):
    bl_low, bl_high, _, _ = CATEGORIES[category]
    return _banded(monthly_salary, bl_low, bl_high)

def calc_health_tax(monthly_salary, category="default"):
    _, _, h_low, h_high = CATEGORIES[category]
    return _banded(monthly_salary, h_low, h_high)

def show_salary_breakdown(salary, category="default", credit_points=CREDIT_POINTS):
    if salary < 0:
        raise SystemExit("error: --salary must be zero or positive.")
    if category not in CATEGORIES:
        raise SystemExit("error: unknown --category. Choose one of: " + ", ".join(CATEGORIES))
    if credit_points < 0:
        raise SystemExit("error: --credit-points must be zero or positive.")
    tax = calc_monthly_tax(salary, credit_points)
    bl = calc_bituach_leumi(salary, category)
    health = calc_health_tax(salary, category)
    # Employee pension contribution: 6% minimum; 6.5% is also common.
    pension = Decimal(str(salary)) * Decimal("0.06")
    net = Decimal(str(salary)) - tax - bl - health - pension

    print(f"\nSalary Breakdown: {salary:,.0f} NIS/month")
    print("=" * 40)
    lo, hi = CATEGORY_COMBINED[category]
    print(f"  BL/health category:  {category} "
          f"({lo * 100:.2f}% to {BL_THRESHOLD:,.0f}, {hi * 100:.2f}% above, ceiling {BL_CEILING:,.0f})")
    print(f"  Credit points:       {credit_points}")
    print(f"  Gross salary:        {salary:>10,.2f} NIS")
    print(f"  Income tax:          {tax:>10,.2f} NIS")
    print(f"  Bituach Leumi:       {bl:>10,.2f} NIS")
    print(f"  Health tax:          {health:>10,.2f} NIS")
    print(f"  Pension (6%, min):   {pension:>10,.2f} NIS")
    print(f"  --------------------------------")
    print(f"  Net salary:          {net:>10,.2f} NIS")

def calc_mortgage(amount, years, rate=0.05):
    if amount <= 0:
        raise SystemExit("error: --amount must be positive.")
    if years <= 0:
        raise SystemExit("error: --years must be a positive number of years.")
    if years > 30:
        raise SystemExit("error: --years may not exceed 30. A mortgage will not be "
                         "approved, on any track, for longer than 30 years.")
    if rate < 0:
        raise SystemExit("error: --rate must be zero or positive.")
    if rate == 0:
        payment = Decimal(str(amount)) / (years * 12)
        total = Decimal(str(amount))
        _print_mortgage(amount, years, rate, payment, total)
        return
    monthly_rate = Decimal(str(rate)) / 12
    n_payments = years * 12
    amt = Decimal(str(amount))
    payment = amt * (monthly_rate * (1 + monthly_rate) ** n_payments) / ((1 + monthly_rate) ** n_payments - 1)
    total = payment * n_payments
    _print_mortgage(amount, years, rate, payment, total)

def _print_mortgage(amount, years, rate, payment, total):
    amt = Decimal(str(amount))
    print(f"\nMortgage Calculator")
    print("=" * 40)
    print(f"  Loan amount:     {amt:>12,.0f} NIS")
    print(f"  Term:            {years:>12} years")
    print(f"  Interest rate:   {rate*100:>11.2f}%")
    print(f"  Monthly payment: {payment:>12,.2f} NIS")
    print(f"  Total paid:      {total:>12,.0f} NIS")
    print(f"  Total interest:  {total - amt:>12,.0f} NIS")
    print(f"  Note: single-rate run is illustrative, prime-only. At least 1/3 of the")
    print(f"  loan must sit in a FIXED track (unlinked 4.5-6.5%, or CPI-linked fixed")
    print(f"  3.0-5.0% plus CPI), so a real blended payment differs. Re-run per track")
    print(f"  and sum, or pass --rate. Regulatory maximum term is 30 years.")

def main():
    parser = argparse.ArgumentParser(description="Israeli budget calculator")
    parser.add_argument("--salary", type=float, help="Monthly gross salary in NIS")
    parser.add_argument("--mortgage", action="store_true", help="Calculate mortgage")
    parser.add_argument("--amount", type=float, help="Mortgage amount in NIS")
    parser.add_argument("--years", type=int, default=25, help="Mortgage term in years")
    parser.add_argument("--rate", type=float, default=0.05,
                        help="Annual interest rate (default 0.05 = prime as of July 2026). "
                             "Illustrative, prime-only: at least 1/3 of the loan must be in a "
                             "fixed track, so a real blended payment differs. Override per track.")
    parser.add_argument("--category", default="default", choices=sorted(CATEGORIES),
                        help="Bituach Leumi / health-tax category. The default row covers a "
                             "resident aged 18 to retirement age. Under-18s and old-age-pension "
                             "recipients pay nothing; disability-pension recipients pay health-tax only.")
    parser.add_argument("--credit-points", type=float, default=float(CREDIT_POINTS),
                        help="Income-tax credit points (default 2.25 resident base; women 2.75).")
    args = parser.parse_args()

    if args.salary is not None:
        show_salary_breakdown(args.salary, args.category, args.credit_points)
    elif args.mortgage and args.amount is not None:
        calc_mortgage(args.amount, args.years, args.rate)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
