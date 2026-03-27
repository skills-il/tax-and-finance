---
name: israeli-pension-advisor
description: "Navigate the Israeli pension and savings system including pension funds (keren pensia), manager's insurance (bituach menahalim), training funds (keren hishtalmut), and retirement planning. Use when user asks about Israeli pension, \"pensia\", \"keren hishtalmut\", retirement savings, \"bituach menahalim\", pension contributions, or tax benefits from savings. Uninformed pension decisions cost hundreds of thousands of NIS over a lifetime. Covers mandatory pension, voluntary savings, and withdrawal rules. Do NOT provide specific investment recommendations or fund performance comparisons."
license: MIT
compatibility: No network required.
---

# Israeli Pension Advisor

## Critical Note
This skill provides general pension INFORMATION. It does not replace consultation
with a licensed pension advisor (yoetz pensioni). Recommend professional advice
for specific decisions.

## Instructions

### Step 1: Identify Savings Type
| Type | Hebrew | Purpose | Tax Benefit |
|------|--------|---------|-------------|
| Keren Pensia | keren pensia | Retirement + disability + survivors | Tax credit + deduction |
| Bituach Menahalim | bituach menahalim | Retirement (insurance-based, declining for new policies since 2013) | Tax credit + deduction |
| Keren Hishtalmut | keren hishtalmut | Medium-term savings (6 years) | Tax-free gains for employees |
| Kupat Gemel | kupat gemel | General savings/investment | Various |
| Kranot Neemanot | kranot neemanot | Mutual funds | Capital gains tax |

### Step 2: Mandatory Pension Contributions
Since 2008, all employees must have pension. Average wage (2026): 13,769 NIS/month -- this is the base figure for most pension ceilings.

**Employee contributions:**
- **Employee:** 6% of salary
- **Employer pension:** 6.5% of salary (includes disability insurance component up to 2.5%)
- **Employer severance (pitzuim):** 6% of salary (mandatory minimum)
- **Total mandatory minimum:** 18.5% of salary
- **Comprehensive pension fund max deposit:** 5,645 NIS/month (67,768 NIS/year, 2026). Contributions above this go to a supplementary fund.

**Section 14 (most common arrangement):**
- Full severance obligation is 8.33% of salary (one month per year of service)
- Mandatory pension law only requires 6% for severance
- The 2.33% gap: if employer contributes only 6%, they owe the difference on termination, calculated at the employee's final salary
- Most modern contracts use full Section 14 (8.33%) to eliminate this gap
- Tax-exempt severance ceiling: 13,750 NIS per year of service (2026)

**Self-employed mandatory pension:**
- 4.45% on income up to 6,884.50 NIS/month (half average wage)
- 12.55% on income from 6,884.50 to 13,769 NIS/month (full average wage)
- Maximum annual mandatory obligation: 14,044 NIS

**Default pension fund system (since June 2025):**
- Employees without an active pension choice are assigned to one of 4 selected default funds based on their ID number check digit
- Default fund fees are capped at 0.22% of balance + 1% of deposits, locked for 10 years
- Employees can switch funds at any time after assignment

**Pension contribution timing for new employees:**
- Employee with existing pension: contributions begin after 3 months, retroactive to day 1
- Employee without existing pension: contributions begin after 6 months (not retroactive)

### Step 3: Keren Hishtalmut (Training Fund)
Most popular Israeli savings vehicle:

**For employees:**
- **Employee contribution:** Up to 2.5% of salary
- **Employer contribution:** Up to 7.5% of salary
- **Tax-free ceiling:** Employer contribution up to salary of 15,712 NIS/month (2026) is tax-free to the employee
- **Withdrawal after 6 years:** Tax-free on gains (unique Israeli benefit)
- **Withdrawal after 3 years:** For education/training purposes only

**For self-employed (two separate ceilings):**
- **Tax deduction from income:** Up to 13,202 NIS/year (4.5% of income up to 293,397 NIS)
- **Profit-exempt ceiling:** 20,566 NIS/year (gains on deposits up to this amount are tax-free after 6 years)

**Note:** In 2024 the Treasury proposed eliminating keren hishtalmut tax-free status for future deposits. As of 2026, this has not been enacted and the tax benefit remains in place.

### Step 4: Tax Benefits Summary

**For employees:**
- **Pension tax credit:** 35% credit on employee contributions up to 679 NIS/month (7% of qualifying salary 9,700 NIS). Maximum credit: 2,852 NIS/year (2026)
- **Employer exclusion:** Employer's pension contribution is not taxed as employee income

**For self-employed:**
- Tax credit (35%) on up to 12,804 NIS/year of pension contributions
- Tax deduction on up to 25,608 NIS/year of pension contributions
- Maximum deductible pension contribution: 38,412 NIS/year (16.5% of income up to 232,800 NIS)

**Pension payout (at retirement):**
- Monthly pension is partially tax-exempt
- 2026 exemption rate: 57.5% (rising to 62.5% in 2027, 67% from 2028)
- Tax-free pension amount: up to 5,422 NIS/month (2026)
- Qualifying pension threshold: 9,430 NIS/month

### Step 5: Withdrawal Rules
- **Pension:** Age 67 (men) / ~63.5 (women, 2026, rising to 65 by 2032)
- **Early pension:** Available before retirement age with 35% tax on withdrawal. Exceptions for disability, low income, or terminal illness
- **Keren hishtalmut:** After 6 years (tax-free), or 3 years (education only)
- **Severance (pitzuim):** Upon termination, subject to Section 14 arrangement. Tax-exempt up to 13,750 NIS per year of service
- **Disability:** Immediate access if meeting medical criteria

### Step 6: Choosing Between Pension Types
**Keren Pensia (Pension Fund):**
- Lower management fees (default funds: 0.22% balance + 1% deposits; non-default: up to 0.5% balance + 6% deposits)
- Includes disability and survivors insurance built-in
- Multiple investment tracks available (age-based, general, shares-focused, bonds-focused, halacha-compliant)
- Preferred for most employees
- Since 2013, most new employees are directed to keren pensia over bituach menahalim

**Bituach Menahalim (Manager's Insurance):**
- Separate insurance component (risk premium)
- More investment track flexibility
- Higher management fees (typically 0.5-1.5% balance + up to 4% deposits)
- Declining for new policies since 2013
- May be suitable for high earners with existing policies wanting more control

## Examples

### Example 1: New Employee
User says: "I just started a new job, what pension should I choose?"
Result: Explain mandatory pension (keren pensia vs bituach menahalim), mention default fund assignment system, recommend comparing management fees, suggest keren hishtalmut if employer offers it. Note that most new employees go to keren pensia.

### Example 2: Self-Employed Savings
User says: "I'm a freelancer, how should I save for retirement?"
Result: Explain mandatory pension rates (4.45% + 12.55%), keren hishtalmut two ceilings (13,202 deduction vs 20,566 profit-exempt), maximum deductible pension (38,412 NIS/year). Recommend maximizing keren hishtalmut first.

### Example 3: Approaching Retirement
User says: "I'm 60, when can I start withdrawing pension?"
Result: Explain retirement ages (67 men, ~63.5 women in 2026), early withdrawal 35% tax, pension payout tax exemption (57.5% exempt, up to 5,422 NIS/month tax-free), lump sum vs monthly pension tradeoffs.

## Bundled Resources

### Scripts
- `scripts/calculate_pension.py` -- Computes mandatory pension contributions (employee, employer, severance), keren hishtalmut benefits, and basic retirement savings projections for both employees and self-employed. Run: `python scripts/calculate_pension.py --help`

### References
- `references/pension-fund-types.md` -- Detailed comparison of Israeli pension vehicles: Keren Pensia, Bituach Menahalim, Kupat Gemel, and Kranot Neemanot, including fee structures, insurance components, default fund system, and major fund providers. Consult when advising on pension fund selection in Step 6.
- `references/tax-benefits.md` -- Israeli pension tax benefits including the 35% tax credit on employee contributions, employer contribution exclusions, keren hishtalmut tax-free gains, self-employed deduction rules, Section 14 details, and pension payout tax exemption rates. Consult when calculating tax savings from pension and savings contributions.

## Gotchas
- Israeli pension has three distinct product types: comprehensive pension fund (keren pensia makifa), provident fund (kupat gemel), and managers' insurance (bituach menahalim). Agents may treat them as interchangeable, but they have different fee structures, insurance components, and withdrawal rules.
- Pension fund management fees in Israel have two components: from deposits (up to 6% for non-default funds) and from accumulated savings (up to 0.5% annually). Agents may quote only one component. Default selected funds cap at 0.22% balance + 1% deposits.
- The retirement age in Israel is 67 for men and ~63.5 for women in 2026 (gradually rising to 65 by 2032). Agents may use the US retirement age of 67 for both genders, or cite the outdated 62 for women.
- Israeli pension funds invest significantly in local government bonds (igrot chov mimshaltiiot), which means returns are partially linked to Israeli economic performance. Agents should not compare Israeli pension returns directly to US 401(k) S&P 500 benchmarks.
- Self-employed keren hishtalmut has TWO separate ceilings: the tax deduction ceiling (13,202 NIS/year) and the profit-exempt ceiling (20,566 NIS/year). Agents often conflate these into a single figure.

## Troubleshooting

### Error: "Pension fund not transferring"
Cause: Switching pension funds requires specific process
Solution: Contact new fund to initiate transfer. Old fund must complete within 10 business days. No penalties for switching.

### Error: "Employer not contributing"
Cause: Employer legally required to contribute pension after 6 months (no prior pension) or 3 months retroactive (with prior pension)
Solution: Employer must contribute retroactively from the applicable start date. Contact Ministry of Labor (Misrad HaAvoda) or the pension fund for enforcement.

### Error: "Cannot withdraw keren hishtalmut"
Cause: Lock-in period not completed
Solution: Standard lock-in is 6 years from first deposit. Early withdrawal (3 years) only for education/training with documentation. Withdrawal before maturity is taxed at the marginal income tax rate (up to 47%).
