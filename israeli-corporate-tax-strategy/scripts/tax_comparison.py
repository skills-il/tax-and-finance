#!/usr/bin/env python3
"""
Israeli Corporate Tax Strategy Calculator (2026)

Compares salary, dividend, shareholder loan, and management fees
extraction methods for Israeli company owners (baalei shlita).

Usage:
    python tax_comparison.py --profit 500000
    python tax_comparison.py --profit 500000 --current-salary 180000
    python tax_comparison.py --profit 1000000 --current-salary 228000 --credit-points 2.75
    python tax_comparison.py --example
"""

import argparse
import sys

# --- 2026 Tax Constants ---

CORPORATE_TAX_RATE = 0.23
DIVIDEND_TAX_CONTROLLING = 0.30
SURTAX_THRESHOLD = 721_560
SURTAX_RATE = 0.03
SURTAX_NON_LABOR_RATE = 0.02
CREDIT_POINT_ANNUAL = 2_904
SECTION_3TET_RATE = 0.0653

# Income tax brackets (annual, earned income, 2026)
INCOME_TAX_BRACKETS = [
    (84_120, 0.10),
    (120_720, 0.14),
    (228_000, 0.20),
    (301_200, 0.31),
    (560_280, 0.35),
    (721_560, 0.47),
    (float("inf"), 0.50),
]

# Bituach Leumi thresholds (annual)
NI_THRESHOLD_LOW = 7_122 * 12   # 85,464
NI_THRESHOLD_HIGH = 47_465 * 12  # 569,580

# Employee NI + Health rates
EMPLOYEE_NI_LOW = 0.004 + 0.031   # 3.5%
EMPLOYEE_NI_HIGH = 0.07 + 0.05    # 12%

# Employer NI rates (controlling shareholder)
EMPLOYER_NI_LOW = 0.0446
EMPLOYER_NI_HIGH = 0.0738


def calc_income_tax(annual_income: float) -> float:
    tax = 0.0
    prev_limit = 0
    for limit, rate in INCOME_TAX_BRACKETS:
        if annual_income <= prev_limit:
            break
        taxable = min(annual_income, limit) - prev_limit
        tax += taxable * rate
        prev_limit = limit
    return tax


def calc_employee_ni(annual_salary: float) -> float:
    if annual_salary <= NI_THRESHOLD_LOW:
        return annual_salary * EMPLOYEE_NI_LOW
    elif annual_salary <= NI_THRESHOLD_HIGH:
        return (NI_THRESHOLD_LOW * EMPLOYEE_NI_LOW
                + (annual_salary - NI_THRESHOLD_LOW) * EMPLOYEE_NI_HIGH)
    else:
        return (NI_THRESHOLD_LOW * EMPLOYEE_NI_LOW
                + (NI_THRESHOLD_HIGH - NI_THRESHOLD_LOW) * EMPLOYEE_NI_HIGH)


def calc_employer_ni(annual_salary: float) -> float:
    if annual_salary <= NI_THRESHOLD_LOW:
        return annual_salary * EMPLOYER_NI_LOW
    elif annual_salary <= NI_THRESHOLD_HIGH:
        return (NI_THRESHOLD_LOW * EMPLOYER_NI_LOW
                + (annual_salary - NI_THRESHOLD_LOW) * EMPLOYER_NI_HIGH)
    else:
        return (NI_THRESHOLD_LOW * EMPLOYER_NI_LOW
                + (NI_THRESHOLD_HIGH - NI_THRESHOLD_LOW) * EMPLOYER_NI_HIGH)


def calc_surtax(total_income: float, non_labor_income: float = 0) -> float:
    if total_income <= SURTAX_THRESHOLD:
        return 0.0
    excess = total_income - SURTAX_THRESHOLD
    surtax = excess * SURTAX_RATE
    if non_labor_income > 0:
        non_labor_excess = min(non_labor_income, excess)
        surtax += non_labor_excess * SURTAX_NON_LABOR_RATE
    return surtax


def solve_gross_salary(budget: float, current_salary: float) -> float:
    """Find gross salary that fits within budget including employer NI."""
    low, high = 0, budget
    for _ in range(100):
        mid = (low + high) / 2
        cost = mid + calc_employer_ni(mid + current_salary) - calc_employer_ni(current_salary)
        if cost < budget:
            low = mid
        else:
            high = mid
    return low


def analyze_salary(profit: float, credit_points: float, current_salary: float = 0) -> dict:
    gross = solve_gross_salary(profit, current_salary)
    total_salary = current_salary + gross
    employer_ni = calc_employer_ni(total_salary) - calc_employer_ni(current_salary)
    income_tax = calc_income_tax(total_salary) - calc_income_tax(current_salary)
    employee_ni = calc_employee_ni(total_salary) - calc_employee_ni(current_salary)
    credit_reduction = credit_points * CREDIT_POINT_ANNUAL if current_salary == 0 else 0
    net_tax = max(0, income_tax - credit_reduction)
    surtax = calc_surtax(total_salary) - calc_surtax(current_salary)
    total_tax = net_tax + surtax + employee_ni + employer_ni
    net = gross - net_tax - surtax - employee_ni
    return {
        "method": "Salary",
        "total_tax": total_tax,
        "net_to_shareholder": net,
        "effective_rate": total_tax / profit * 100 if profit > 0 else 0,
    }


def analyze_dividend(profit: float, current_salary: float = 0) -> dict:
    corp_tax = profit * CORPORATE_TAX_RATE
    distributable = profit - corp_tax
    div_tax = distributable * DIVIDEND_TAX_CONTROLLING
    total_income = current_salary + distributable
    surtax = calc_surtax(total_income, non_labor_income=distributable) - calc_surtax(current_salary)
    total_tax = corp_tax + div_tax + surtax
    net = distributable - div_tax - surtax
    return {
        "method": "Dividend",
        "total_tax": total_tax,
        "net_to_shareholder": net,
        "effective_rate": total_tax / profit * 100 if profit > 0 else 0,
    }


def analyze_optimal_mix(profit: float, credit_points: float, current_salary: float = 0) -> dict:
    best_net = 0
    best_cost = 0
    step = 10_000
    for salary_cost in range(step, int(profit), step):
        gross = solve_gross_salary(salary_cost, current_salary)
        total_sal = current_salary + gross
        emp_ni = calc_employer_ni(total_sal) - calc_employer_ni(current_salary)
        inc_tax = calc_income_tax(total_sal) - calc_income_tax(current_salary)
        ee_ni = calc_employee_ni(total_sal) - calc_employee_ni(current_salary)
        cr = credit_points * CREDIT_POINT_ANNUAL if current_salary == 0 else 0
        net_tax = max(0, inc_tax - cr)
        s_surtax = calc_surtax(total_sal) - calc_surtax(current_salary)
        net_sal = gross - net_tax - s_surtax - ee_ni

        rem = profit - salary_cost
        ct = rem * CORPORATE_TAX_RATE
        dist = rem - ct
        dt = dist * DIVIDEND_TAX_CONTROLLING
        tot_inc = total_sal + dist
        d_surtax = calc_surtax(tot_inc, non_labor_income=dist) - calc_surtax(total_sal)
        net_div = dist - dt - d_surtax

        total_net = net_sal + net_div
        if total_net > best_net:
            best_net = total_net
            best_cost = salary_cost

    # Recalculate best
    gross = solve_gross_salary(best_cost, current_salary)
    rem = profit - best_cost
    ct = rem * CORPORATE_TAX_RATE
    dist = rem - ct
    total_tax = profit - best_net
    return {
        "method": "Optimal Mix (Salary + Dividend)",
        "salary_annual": gross,
        "dividend_amount": dist,
        "total_tax": total_tax,
        "net_to_shareholder": best_net,
        "effective_rate": total_tax / profit * 100 if profit > 0 else 0,
    }


def analyze_loan(amount: float, current_salary: float = 0) -> dict:
    deemed = amount * SECTION_3TET_RATE
    total_inc = current_salary + deemed
    tax = calc_income_tax(total_inc) - calc_income_tax(current_salary)
    surtax = calc_surtax(total_inc) - calc_surtax(current_salary)
    return {
        "method": "Shareholder Loan (1 year)",
        "deemed_interest": deemed,
        "annual_cost": tax + surtax,
        "effective_annual_rate": (tax + surtax) / amount * 100,
    }


def fmt(n: float) -> str:
    return f"{n:,.0f}"


def print_comparison(profit: float, credit_points: float, current_salary: float):
    sal = analyze_salary(profit, credit_points, current_salary)
    div = analyze_dividend(profit, current_salary)
    opt = analyze_optimal_mix(profit, credit_points, current_salary)
    loan = analyze_loan(profit, current_salary)

    print("=" * 70)
    print(f"  ISRAELI CORPORATE TAX STRATEGY COMPARISON (2026)")
    print(f"  Company Profit: {fmt(profit)} NIS")
    if current_salary > 0:
        print(f"  Current Annual Salary: {fmt(current_salary)} NIS")
    print(f"  Credit Points: {credit_points}")
    print("=" * 70)
    print(f"\n{'Method':<35} {'Total Tax':>12} {'Net':>12} {'Rate':>8}")
    print("-" * 70)

    for r in [sal, div, opt]:
        print(f"  {r['method']:<33} {fmt(r['total_tax']):>12} "
              f"{fmt(r['net_to_shareholder']):>12} {r['effective_rate']:>7.1f}%")

    print(f"\n  Shareholder Loan (Section 3(tet)):")
    print(f"    Deemed interest: {fmt(loan['deemed_interest'])} NIS/year")
    print(f"    Tax cost: {fmt(loan['annual_cost'])} NIS/year "
          f"({loan['effective_annual_rate']:.1f}% of principal)")
    print(f"    Note: Must be repaid or converted to dividend/salary")

    methods = [sal, div, opt]
    best = max(methods, key=lambda x: x["net_to_shareholder"])
    worst = min(methods, key=lambda x: x["net_to_shareholder"])
    print(f"\n{'=' * 70}")
    print(f"  BEST: {best['method']} (saves {fmt(best['net_to_shareholder'] - worst['net_to_shareholder'])} NIS vs worst)")
    if "salary_annual" in opt:
        print(f"  Optimal: salary {fmt(opt['salary_annual'])} "
              f"({fmt(opt['salary_annual'] / 12)}/month) + dividend {fmt(opt['dividend_amount'])}")
    print(f"{'=' * 70}")
    print(f"\n  Consult a licensed Israeli CPA before acting on these estimates.")


def main():
    parser = argparse.ArgumentParser(description="Israeli Corporate Tax Strategy Calculator (2026)")
    parser.add_argument("--profit", type=float, help="Company profit for extraction (NIS)")
    parser.add_argument("--current-salary", type=float, default=0, help="Current annual salary (NIS)")
    parser.add_argument("--credit-points", type=float, default=2.25, help="Tax credit points (default: 2.25)")
    parser.add_argument("--example", action="store_true", help="Show example calculations")
    args = parser.parse_args()

    if args.example:
        for p in [200_000, 500_000, 1_000_000]:
            print_comparison(p, 2.25, 0)
            print()
        return

    if args.profit is None:
        parser.print_help()
        sys.exit(1)
    if args.profit <= 0:
        print("Error: profit must be positive")
        sys.exit(1)

    print_comparison(args.profit, args.credit_points, args.current_salary)


if __name__ == "__main__":
    main()
