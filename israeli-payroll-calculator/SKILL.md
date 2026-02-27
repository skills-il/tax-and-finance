---
name: israeli-payroll-calculator
description: >-
  Calculate Israeli payroll including income tax, Bituach Leumi (National
  Insurance), health tax, pension contributions, and net salary. Use when user
  asks to calculate salary, "tlush maskoret", payroll deductions, "bruto to
  neto", employer cost, tax credits (nekudot zikui), or needs help understanding
  Israeli payslip items. Covers employees, freelancers (atzmai), and employer
  cost calculations. Do NOT use for US, UK, or other countries' payroll
  calculations.
license: MIT
allowed-tools: 'Bash(python:*)'
compatibility: 'Works with Claude Code, Claude.ai, Cursor. No network access required.'
metadata:
  author: skills-il
  version: 1.0.0
  category: tax-and-finance
  tags:
    he:
      - שכר
      - משכורת
      - מיסים
      - ביטוח-לאומי
      - פנסיה
      - ישראל
    en:
      - payroll
      - salary
      - tax
      - bituach-leumi
      - pension
      - israel
  display_name:
    he: מחשבון שכר ישראלי
    en: Israeli Payroll Calculator
  display_description:
    he: 'חישוב משכורת כולל מס הכנסה, ביטוח לאומי, פנסיה והפרשות'
    en: >-
      Calculate Israeli payroll including income tax, Bituach Leumi (National
      Insurance), health tax, pension contributions, and net salary. Use when
      user asks to calculate salary, "tlush maskoret", payroll deductions,
      "bruto to neto", employer cost, tax credits (nekudot zikui), or needs help
      understanding Israeli payslip items. Covers employees, freelancers
      (atzmai), and employer cost calculations. Do NOT use for US, UK, or other
      countries' payroll calculations.
  supported_agents:
    - claude-code
    - cursor
    - github-copilot
    - windsurf
    - opencode
    - codex
    - openclaw
---

# Israeli Payroll Calculator

## Instructions

### Step 1: Gather Employee Information
Collect from user:
- **Gross monthly salary** (bruto) in NIS
- **Tax credit points** (nekudot zikui): Default 2.25 for male resident, 2.75 for female
- **Pension arrangement:** Yes/No, contribution percentages
- **Employment type:** Employee (sachir), Freelancer (atzmai)
- **Age:** Affects NI rates (under/over 18, retirement age)

### Step 2: Calculate Income Tax
Apply progressive tax brackets to monthly gross salary:

1. Calculate annual equivalent: monthly_gross * 12
2. Apply brackets progressively (see references/tax-brackets.md)
3. Subtract tax credit value: credit_points * 242 NIS/month
4. Monthly tax = max(0, calculated_tax - credits)

IMPORTANT: Tax credits cannot create a negative tax (no refund through payroll).

### Step 3: Calculate Bituach Leumi (National Insurance)
For employees:
- On first 7,122 NIS: 0.4% NI + 3.1% health = 3.5%
- On amount 7,123 to 49,030 NIS: 7.0% NI + 5.0% health = 12.0%
- Maximum insurable salary: 49,030 NIS/month

### Step 4: Calculate Pension Deductions
If pension applies (mandatory for most employees):
- Employee: 6% of salary (up to pension ceiling)
- This amount is deducted from gross but provides tax benefits

### Step 5: Calculate Net Salary (Neto)
```
Net = Gross
    - Income Tax
    - Bituach Leumi (employee share)
    - Health Tax (employee share)
    - Pension (employee contribution)
    - Other deductions (union dues, etc.)
```

### Step 6: Calculate Employer Total Cost (if requested)
```
Employer Cost = Gross
    + Employer NI (~7.6%)
    + Employer Health (~3.45%)
    + Employer Pension (6.5%)
    + Employer Severance (6%)
    + Vacation accrual
    + Sick leave accrual
```

### Step 7: Present Clear Breakdown
Present results as a payslip-style table:
| Item | Amount (NIS) |
|------|-------------|
| Gross Salary | XX,XXX |
| Income Tax | -X,XXX |
| Bituach Leumi | -XXX |
| Health Tax | -XXX |
| Pension (employee) | -X,XXX |
| **Net Salary** | **XX,XXX** |

CAVEAT: Always note "This is an estimate. Actual amounts may vary based on specific tax rulings, additional credits, or employer agreements. Consult a certified Israeli accountant (roeh cheshbon) for exact figures."

## Examples

### Example 1: Standard Employee
User says: "Calculate net salary for 20,000 NIS gross, male, no special credits"
Result: Detailed breakdown showing approximately 15,800-16,200 NIS net

### Example 2: Employer Cost
User says: "How much does it cost an employer to pay 15,000 NIS gross?"
Result: Total employer cost approximately 19,500-20,000 NIS including all contributions

### Example 3: Salary Comparison
User says: "Compare a 25,000 NIS offer with a 22,000 NIS + car offer"
Result: Side-by-side comparison accounting for car tax benefit (shovi rechev)

## Bundled Resources

### Scripts
- `scripts/calculate_payroll.py` — Calculates Israeli gross-to-net salary with progressive income tax brackets, Bituach Leumi, health tax, and pension contributions. Supports employee and employer cost views. Run: `python scripts/calculate_payroll.py --help`

### References
- `references/tax-brackets.md` — 2025 Israeli income tax brackets (annual and monthly) with progressive rates from 10% to 50%. Also referenced in Step 2 and Troubleshooting below. Consult when computing income tax or verifying bracket thresholds.
- `references/bituach-leumi-rates.md` — 2025 Bituach Leumi (National Insurance) and health tax rates for employees and employers, covering both the reduced bracket (up to 7,122 NIS) and full bracket (up to 49,030 NIS). Consult when calculating NI and health deductions in Step 3.
- `references/credit-points.md` — Israeli tax credit points (nekudot zikui) value and full eligibility table covering base credits, gender, new immigrants, children, single parents, and disability. Consult when determining a taxpayer's total credit points beyond the defaults in Step 1.

## Troubleshooting

### Error: "Tax brackets may be outdated"
Cause: Tax brackets update annually (usually January 1)
Solution: Verify current brackets at Tax Authority website. Skill uses 2025 brackets -- check references/tax-brackets.md for updates.

### Error: "Credit points don't match"
Cause: Various life circumstances affect credit points
Solution: Review full credit point table. Common additions: female (+0.5), new immigrant (up to +3), children, single parent, disabled.