---
name: israeli-pension-advisor
description: >-
  Navigate the Israeli pension and savings system including pension funds (keren
  pensia), manager's insurance (bituach menahalim), training funds (keren
  hishtalmut), and retirement planning. Use when user asks about Israeli
  pension, "pensia", "keren hishtalmut", retirement savings, "bituach
  menahalim", pension contributions, or tax benefits from savings. Covers
  mandatory pension, voluntary savings, and withdrawal rules. Do NOT provide
  specific investment recommendations or fund performance comparisons.
license: MIT
compatibility: No network required.
metadata:
  author: skills-il
  version: 1.0.0
  category: tax-and-finance
  tags:
    he:
      - פנסיה
      - פרישה
      - חיסכון
      - קרן-השתלמות
      - ישראל
    en:
      - pension
      - retirement
      - savings
      - keren-hishtalmut
      - israel
  display_name:
    he: יועץ פנסיה ישראלי
    en: Israeli Pension Advisor
  display_description:
    he: 'ניווט בין קרנות פנסיה, קופות גמל וחיסכון לפרישה'
    en: >-
      Navigate the Israeli pension and savings system including pension funds
      (keren pensia), manager's insurance (bituach menahalim), training funds
      (keren hishtalmut), and retirement planning. Use when user asks about
      Israeli pension, "pensia", "keren hishtalmut", retirement savings,
      "bituach menahalim", pension contributions, or tax benefits from savings.
      Covers mandatory pension, voluntary savings, and withdrawal rules. Do NOT
      provide specific investment recommendations or fund performance
      comparisons.
  supported_agents:
    - claude-code
    - cursor
    - github-copilot
    - windsurf
    - opencode
    - codex
    - antigravity
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
| Bituach Menahalim | bituach menahalim | Retirement (insurance-based) | Tax credit + deduction |
| Keren Hishtalmut | keren hishtalmut | Medium-term savings (6 years) | Tax-free gains for employees |
| Kupat Gemel | kupat gemel | General savings/investment | Various |
| Kranot Neemanot | kranot neemanot | Mutual funds | Capital gains tax |

### Step 2: Mandatory Pension Contributions
Since 2008, all employees must have pension:
- **Employee:** 6% of salary
- **Employer pension:** 6.5% of salary
- **Employer severance (pitzuim):** 6% of salary
- **Total:** 18.5% of salary goes to pension
- **Insurable salary ceiling:** ~44,000 NIS/month (2025, verify)

### Step 3: Keren Hishtalmut (Training Fund)
Most popular Israeli savings vehicle:
- **Employee contribution:** Up to 2.5% of salary
- **Employer contribution:** Up to 7.5% of salary
- **Tax benefit:** Employer contribution up to ceiling is tax-free
- **Withdrawal after 6 years:** Tax-free on gains (unique Israeli benefit)
- **Withdrawal after 3 years:** For education/training purposes
- **Self-employed:** Can contribute up to ~20,520 NIS/year with tax benefits

### Step 4: Tax Benefits Summary
- **Pension contribution:** Tax credit (35% of employee share up to ceiling) + tax deduction on employer share
- **Keren hishtalmut:** Gains tax-free after 6 years
- **Self-employed:** Multiple deductions available (consult accountant)

### Step 5: Withdrawal Rules
- **Pension:** Age 67 (men) / 62-65 (women, gradually increasing), or early pension with reduction
- **Keren hishtalmut:** After 6 years (tax-free), or 3 years (education only)
- **Severance (pitzuim):** Upon termination, subject to Section 14 arrangement
- **Disability:** Immediate access if meeting medical criteria

### Step 6: Choosing Between Pension Types
**Keren Pensia (Pension Fund):**
- Lower management fees (typically 0.2-0.5%)
- Includes disability and survivors insurance built-in
- Balanced investment portfolio
- Preferred for most employees

**Bituach Menahalim (Manager's Insurance):**
- Separate insurance component (risk premium)
- More investment flexibility
- Higher management fees (typically 0.5-1.5%)
- Better for high earners wanting more control

## Examples

### Example 1: New Employee
User says: "I just started a new job, what pension should I choose?"
Result: Explain mandatory pension (keren pensia vs bituach menahalim), recommend checking fees, suggest keren hishtalmut if employer offers it.

### Example 2: Self-Employed Savings
User says: "I'm a freelancer, how should I save for retirement?"
Result: Explain self-employed pension obligations, keren hishtalmut benefits, tax deduction calculations.

### Example 3: Approaching Retirement
User says: "I'm 60, when can I start withdrawing pension?"
Result: Explain retirement ages, early pension options and reduction rates, lump sum vs monthly pension tradeoffs.

## Bundled Resources

### Scripts
- `scripts/calculate_pension.py` — Computes mandatory pension contributions (employee, employer, severance), keren hishtalmut benefits, and basic retirement savings projections for both employees and self-employed. Run: `python scripts/calculate_pension.py --help`

### References
- `references/pension-fund-types.md` — Detailed comparison of Israeli pension vehicles: Keren Pensia, Bituach Menahalim, Kupat Gemel, and Kranot Neemanot, including fee structures, insurance components, and major fund providers. Consult when advising on pension fund selection in Step 6.
- `references/tax-benefits.md` — Israeli pension tax benefits including the 35% tax credit on employee contributions, employer contribution exclusions, keren hishtalmut tax-free gains, and self-employed deduction rules. Consult when calculating tax savings from pension and savings contributions.

## Troubleshooting

### Error: "Pension fund not transferring"
Cause: Switching pension funds requires specific process
Solution: Contact new fund to initiate transfer. Old fund must complete within 10 business days. No penalties for switching.

### Error: "Employer not contributing"
Cause: Employer legally required to contribute pension from day one (after probation)
Solution: Employer must contribute retroactively. Contact Ministry of Labor or pension fund for enforcement.

### Error: "Cannot withdraw keren hishtalmut"
Cause: Lock-in period not completed
Solution: Standard lock-in is 6 years from first deposit. Early withdrawal (3 years) only for education/training with documentation.