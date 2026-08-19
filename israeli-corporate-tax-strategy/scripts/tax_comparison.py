#!/usr/bin/env python3
"""
Israeli Corporate Tax Strategy Calculator (2026)

Compares salary, dividend, shareholder loan, and management fees
extraction methods for Israeli company owners (baalei shlita).

Usage:
    python tax_comparison.py --profit 500000
    python tax_comparison.py --profit 500000 --current-salary 180000
    python tax_comparison.py --profit 1000000 --current-salary 228000 --credit-points 2.75
    python tax_comparison.py --profit 1000000 --benefit-track pte
    python tax_comparison.py --profit 1000000 --benefit-track pte --dividend-rate 0.04
    python tax_comparison.py --example
"""

import argparse
import sys

# --- 2026 Tax Constants ---

CORPORATE_TAX_RATE = 0.23
DIVIDEND_TAX_CONTROLLING = 0.30

# Benefit tracks under the Law for Encouragement of Capital Investments, 5719-1959.
# key -> (corporate rate, dividend withholding rate, label)
# Corporate rates: s.51tet-zayin (PFE), s.51kaf-alef(a) (SPFE), s.51kaf-hey (PTE, SPTE).
# Dividend rates: s.51yod-het (PFE, SPFE), s.51kaf-vav(1) (PTE, SPTE),
#                 s.51kaf-vav(2) for the 4% foreign-company rate.
# These rates apply ONLY to the track's qualifying income, and for the technology
# tracks only to the Israel-developed share of the intangible asset (nexus).
BENEFIT_TRACKS = {
    "standard": (0.23, 0.30, "Standard company (s.126(a))"),
    "pfe-a":    (0.075, 0.20, "Preferred Enterprise, Development Area A"),
    "pfe":      (0.16, 0.20, "Preferred Enterprise, elsewhere"),
    "spfe-a":   (0.05, 0.20, "Special Preferred Enterprise, Development Area A"),
    "spfe":     (0.08, 0.20, "Special Preferred Enterprise, elsewhere"),
    "pte-a":    (0.075, 0.20, "Preferred Technology Enterprise, Development Area A"),
    "pte":      (0.12, 0.20, "Preferred Technology Enterprise, elsewhere"),
    "spte":     (0.06, 0.20, "Special Preferred Technology Enterprise"),
}

# Rate for a dividend out of qualifying technological income paid to a foreign-resident
# body corporate where 90% or more of the payer's shares are held directly by one or more
# foreign-resident bodies corporate (s.51kaf-vav(2)). Further conditions apply.
DIVIDEND_TECH_FOREIGN_90 = 0.04
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
    (float("inf"), 0.47),  # base rate only; calc_surtax() adds the 3% Section 121B surtax above 721,560 (47% + 3% = 50% combined)
]

# Bituach Leumi thresholds (annual, 2026)
NI_THRESHOLD_LOW = 7_703 * 12   # 92,436
NI_THRESHOLD_HIGH = 51_910 * 12  # 622,920

# Employee NI + Health rates (2026: NI 1.04%/7.0% per 2024 budget; health 3.23%/5.17% per 2025 amendment)
EMPLOYEE_NI_LOW = 0.0104 + 0.0323  # 4.27%
EMPLOYEE_NI_HIGH = 0.07 + 0.0517   # 12.17%

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
    income_tax_total = calc_income_tax(total_salary)
    income_tax_current = calc_income_tax(current_salary)
    employee_ni = calc_employee_ni(total_salary) - calc_employee_ni(current_salary)
    credit_reduction = credit_points * CREDIT_POINT_ANNUAL
    # Credit points reduce total tax owed up to zero (applies regardless of current_salary).
    # Marginal incremental tax = (total_tax_after_credits) - (current_tax_after_credits)
    net_total = max(0, income_tax_total - credit_reduction)
    net_current = max(0, income_tax_current - credit_reduction)
    net_tax = net_total - net_current
    surtax = calc_surtax(total_salary) - calc_surtax(current_salary)
    total_tax = net_tax + surtax + employee_ni + employer_ni
    net = gross - net_tax - surtax - employee_ni
    return {
        "method": "Salary",
        "total_tax": total_tax,
        "net_to_shareholder": net,
        "effective_rate": total_tax / profit * 100 if profit > 0 else 0,
    }


def analyze_dividend(profit: float, current_salary: float = 0,
                     corp_rate: float = CORPORATE_TAX_RATE,
                     div_rate: float = DIVIDEND_TAX_CONTROLLING) -> dict:
    corp_tax = profit * corp_rate
    distributable = profit - corp_tax
    div_tax = distributable * div_rate
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


def analyze_optimal_mix(profit: float, credit_points: float, current_salary: float = 0,
                        corp_rate: float = CORPORATE_TAX_RATE,
                        div_rate: float = DIVIDEND_TAX_CONTROLLING) -> dict:
    best_net = 0
    best_cost = 0
    step = 10_000
    cr = credit_points * CREDIT_POINT_ANNUAL
    for salary_cost in range(step, int(profit), step):
        gross = solve_gross_salary(salary_cost, current_salary)
        total_sal = current_salary + gross
        emp_ni = calc_employer_ni(total_sal) - calc_employer_ni(current_salary)
        ee_ni = calc_employee_ni(total_sal) - calc_employee_ni(current_salary)
        net_total = max(0, calc_income_tax(total_sal) - cr)
        net_current = max(0, calc_income_tax(current_salary) - cr)
        net_tax = net_total - net_current
        s_surtax = calc_surtax(total_sal) - calc_surtax(current_salary)
        net_sal = gross - net_tax - s_surtax - ee_ni

        rem = profit - salary_cost
        ct = rem * corp_rate
        dist = rem - ct
        dt = dist * div_rate
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
    ct = rem * corp_rate
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


def print_comparison(profit: float, credit_points: float, current_salary: float,
                     track: str = "standard", div_rate_override: float = None):
    corp_rate, div_rate, label = BENEFIT_TRACKS[track]
    if div_rate_override is not None:
        div_rate = div_rate_override
    sal = analyze_salary(profit, credit_points, current_salary)
    div = analyze_dividend(profit, current_salary, corp_rate, div_rate)
    opt = analyze_optimal_mix(profit, credit_points, current_salary, corp_rate, div_rate)
    loan = analyze_loan(profit, current_salary)

    print("=" * 70)
    print(f"  ISRAELI CORPORATE TAX STRATEGY COMPARISON (2026)")
    print(f"  Regime: {label} -- corporate {corp_rate * 100:g}%, dividend {div_rate * 100:g}%")
    if track != "standard":
        print(f"  Reduced rates apply to QUALIFYING income only; other income stays at 23%.")
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
    parser.add_argument("--benefit-track", default="standard", choices=sorted(BENEFIT_TRACKS),
                        help="Encouragement-Law benefit track held by the company "
                             "(default: standard, 23%%). Use pte/pte-a/spte for technology "
                             "enterprises, pfe/pfe-a/spfe/spfe-a for industrial ones.")
    parser.add_argument("--dividend-rate", type=float, default=None,
                        help="Override the dividend withholding rate as a decimal, e.g. 0.25 for a "
                             "non-controlling shareholder or 0.04 for the s.51kaf-vav(2) "
                             "foreign-company rate on technological income.")
    args = parser.parse_args()

    if args.dividend_rate is not None and not 0 <= args.dividend_rate <= 1:
        print("Error: --dividend-rate must be a decimal between 0 and 1")
        sys.exit(1)

    if args.example:
        for p in [200_000, 500_000, 1_000_000]:
            print_comparison(p, 2.25, 0, args.benefit_track, args.dividend_rate)
            print()
        return

    if args.profit is None:
        parser.print_help()
        sys.exit(1)
    if args.profit <= 0:
        print("Error: profit must be positive")
        sys.exit(1)

    print_comparison(args.profit, args.credit_points, args.current_salary,
                     args.benefit_track, args.dividend_rate)


if __name__ == "__main__":
    main()
