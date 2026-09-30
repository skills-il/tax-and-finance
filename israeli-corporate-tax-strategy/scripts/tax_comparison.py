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

# Employee NI + Health rates for a CONTROLLING-SHAREHOLDER employee (BTL rate table, column 2,
# "בעל שליטה בחברת מעטים"): NI 1.02%/6.79%, health 3.23%/5.17%.
# A regular employee pays NI 1.04%/7.0% instead; do not use those figures here.
EMPLOYEE_NI_LOW = 0.0102 + 0.0323   # 4.25%
EMPLOYEE_NI_HIGH = 0.0679 + 0.0517  # 11.96%

# Employer NI rates (controlling shareholder)
EMPLOYER_NI_LOW = 0.0446
EMPLOYER_NI_HIGH = 0.0738

# Self-employed NI + Health (management fees billed by the shareholder personally)
SELF_EMPLOYED_NI_LOW, SELF_EMPLOYED_HEALTH_LOW = 0.0447, 0.0323    # 7.70%
SELF_EMPLOYED_NI_HIGH, SELF_EMPLOYED_HEALTH_HIGH = 0.1283, 0.0517  # 18.00%
# Section 47A: 52% of the self-employed NATIONAL INSURANCE contribution (not the health
# contribution) is deductible for income tax.
SELF_EMPLOYED_NI_DEDUCTIBLE_SHARE = 0.52


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
    """Section 121B surtax.

    3% (s.121B(a)) on TOTAL taxable income above the threshold, plus 2% (s.121B(a1)) on the
    part of CAPITAL-source income ALONE that exceeds the same threshold. The two limbs are
    measured separately: salary does not use up the threshold for the 2% limb (ITA
    execution instruction 5/2025, example 3.2).
    """
    surtax = max(0.0, total_income - SURTAX_THRESHOLD) * SURTAX_RATE
    surtax += max(0.0, non_labor_income - SURTAX_THRESHOLD) * SURTAX_NON_LABOR_RATE
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
                     div_rate: float = DIVIDEND_TAX_CONTROLLING,
                     company_recipient: bool = False) -> dict:
    corp_tax = profit * corp_rate
    distributable = profit - corp_tax
    div_tax = distributable * div_rate
    total_income = current_salary + distributable
    # s.121B surtax applies to individuals only; a body-corporate shareholder pays none.
    surtax = 0.0 if company_recipient else (
        calc_surtax(total_income, non_labor_income=distributable) - calc_surtax(current_salary))
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
    best_net = float("-inf")
    best_cost = 0
    step = 10_000
    cr = credit_points * CREDIT_POINT_ANNUAL
    # Grid over the salary budget, including both ends (all-dividend and all-salary).
    for salary_cost in list(range(0, int(profit), step)) + [profit]:
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


def calc_self_employed_ni(annual_income: float, salary_already_insured: float = 0) -> tuple:
    """Self-employed NI and health on management-fee income, returned as (ni, health).

    Approximation: salary already drawn is treated as filling the reduced band and the
    ceiling first, so the fee is charged only on the room left under 51,910/month.
    """
    lo, hi = NI_THRESHOLD_LOW, NI_THRESHOLD_HIGH
    start = min(salary_already_insured, hi)
    end = min(salary_already_insured + annual_income, hi)
    low_part = max(0.0, min(end, lo) - start)
    high_part = max(0.0, end - max(start, lo))
    ni = low_part * SELF_EMPLOYED_NI_LOW + high_part * SELF_EMPLOYED_NI_HIGH
    health = low_part * SELF_EMPLOYED_HEALTH_LOW + high_part * SELF_EMPLOYED_HEALTH_HIGH
    return ni, health


def analyze_management_fees(profit: float, credit_points: float, current_salary: float = 0,
                            business_expenses: float = 0) -> dict:
    """Management fees billed by the shareholder personally as an osek murshe.

    The company deducts the fee, so there is no corporate tax on it. VAT is ignored on the
    assumption the company is itself an osek murshe and reclaims it. business_expenses are
    the shareholder's own deductible costs against the fee. Section 62A attribution and
    s.85A arm's-length limits are NOT modelled; check them first (Step 1a, Step 6).
    """
    fee = profit
    business_profit = max(0.0, fee - business_expenses)
    ni, health = calc_self_employed_ni(business_profit, current_salary)
    taxable = business_profit - ni * SELF_EMPLOYED_NI_DEDUCTIBLE_SHARE
    total_inc = current_salary + taxable
    cr = credit_points * CREDIT_POINT_ANNUAL
    net_tax = (max(0, calc_income_tax(total_inc) - cr)
               - max(0, calc_income_tax(current_salary) - cr))
    surtax = calc_surtax(total_inc) - calc_surtax(current_salary)
    total_tax = net_tax + surtax + ni + health
    net = business_profit - total_tax
    return {
        "method": "Management Fees (osek murshe)",
        "total_tax": total_tax,
        "net_to_shareholder": net,
        "effective_rate": total_tax / profit * 100 if profit > 0 else 0,
    }


def fmt(n: float) -> str:
    return f"{n:,.0f}"


def print_comparison(profit: float, credit_points: float, current_salary: float,
                     track: str = "standard", div_rate_override: float = None,
                     company_recipient: bool = False):
    corp_rate, div_rate, label = BENEFIT_TRACKS[track]
    if div_rate_override is not None:
        div_rate = div_rate_override
    if company_recipient:
        # A body-corporate shareholder has no salary, credit points, fees or surtax:
        # only the corporate layer and the dividend withholding are meaningful.
        div = analyze_dividend(profit, 0, corp_rate, div_rate, company_recipient=True)
        print("=" * 70)
        print(f"  DIVIDEND TO A BODY-CORPORATE SHAREHOLDER (2026)")
        print(f"  Regime: {label} -- corporate {corp_rate * 100:g}%, dividend {div_rate * 100:g}%")
        print(f"  Company Profit: {fmt(profit)} NIS")
        print("=" * 70)
        print(f"  Total tax: {fmt(div['total_tax'])}  Net: {fmt(div['net_to_shareholder'])}  "
              f"Rate: {div['effective_rate']:.1f}%")
        print(f"  No s.121B surtax (individuals only). Salary, fees and loan routes do not apply.")
        print(f"  Dividend rate used: {div_rate * 100:g}%. For an Israeli parent pass --dividend-rate 0 "
              f"(s.126(b)); for a foreign parent pass the treaty or s.51kaf-vav rate.")
        print(f"\n  Consult a licensed Israeli CPA before acting on these estimates.")
        return
    sal = analyze_salary(profit, credit_points, current_salary)
    div = analyze_dividend(profit, current_salary, corp_rate, div_rate)
    opt = analyze_optimal_mix(profit, credit_points, current_salary, corp_rate, div_rate)
    loan = analyze_loan(profit, current_salary)
    fees = analyze_management_fees(profit, credit_points, current_salary)

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

    for r in [sal, div, opt, fees]:
        print(f"  {r['method']:<33} {fmt(r['total_tax']):>12} "
              f"{fmt(r['net_to_shareholder']):>12} {r['effective_rate']:>7.1f}%")

    print(f"\n  Shareholder Loan (Section 3(tet)):")
    print(f"    Deemed interest: {fmt(loan['deemed_interest'])} NIS/year")
    print(f"    Tax cost: {fmt(loan['annual_cost'])} NIS/year "
          f"({loan['effective_annual_rate']:.1f}% of principal)")
    print(f"    Note: Must be repaid or converted to dividend/salary")

    print(f"  (Management fees: no expenses deducted, VAT assumed reclaimed, s.62A not modelled)")

    methods = [sal, div, opt, fees]
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
    parser.add_argument("--company-recipient", action="store_true",
                        help="The shareholder is a body corporate (e.g. the foreign parent in the "
                             "s.51kaf-vav(2) 4%% case): no surtax, dividend route only. Implied by "
                             "--dividend-rate 0.04.")
    parser.add_argument("--dividend-rate", type=float, default=None,
                        help="Override the dividend withholding rate as a decimal, e.g. 0.25 for a "
                             "non-controlling shareholder or 0.04 for the s.51kaf-vav(2) "
                             "foreign-company rate on technological income.")
    args = parser.parse_args()

    if args.dividend_rate is not None and not 0 <= args.dividend_rate <= 1:
        print("Error: --dividend-rate must be a decimal between 0 and 1")
        sys.exit(1)

    company = args.company_recipient or (
        args.dividend_rate is not None and abs(args.dividend_rate - DIVIDEND_TECH_FOREIGN_90) < 1e-9)

    if args.example:
        for p in [200_000, 500_000, 1_000_000]:
            print_comparison(p, 2.25, 0, args.benefit_track, args.dividend_rate, company)
            print()
        return

    if args.profit is None:
        parser.print_help()
        sys.exit(1)
    if args.profit <= 0:
        print("Error: profit must be positive")
        sys.exit(1)

    print_comparison(args.profit, args.credit_points, args.current_salary,
                     args.benefit_track, args.dividend_rate, company)


if __name__ == "__main__":
    main()
