# Israeli Payroll Calculator Skill — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a skill that teaches Claude to calculate Israeli payroll including income tax brackets, Bituach Leumi (National Insurance) contributions, health tax, pension deductions, and net salary.

**Architecture:** Domain-Specific Intelligence skill. Embeds Israeli tax brackets, NI rates, pension rules, and employment law specifics. Uses scripts for accurate calculation.

**Tech Stack:** SKILL.md, Python payroll calculation script, references for tax brackets and NI rates.

---

## Research

### Israeli Income Tax Brackets (2025, verify annually)
| Bracket | Annual Income (NIS) | Monthly | Tax Rate |
|---------|-------------------|---------|----------|
| 1 | 0 - 84,120 | 0 - 7,010 | 10% |
| 2 | 84,121 - 120,720 | 7,011 - 10,060 | 14% |
| 3 | 120,721 - 193,800 | 10,061 - 16,150 | 20% |
| 4 | 193,801 - 269,280 | 16,151 - 22,440 | 31% |
| 5 | 269,281 - 560,280 | 22,441 - 46,690 | 35% |
| 6 | 560,281 - 721,560 | 46,691 - 60,130 | 47% |
| 7 | 721,561+ | 60,131+ | 50% |

### Bituach Leumi (National Insurance) Rates — Employee
- **Reduced rate bracket:** Up to 7,122 NIS/month (2025)
  - Employee NI: 0.4%
  - Employee Health: 3.1%
- **Full rate bracket:** 7,123 - 49,030 NIS/month
  - Employee NI: 7%
  - Employee Health: 5%
- **Employer contributions:** Additional ~7.6% NI + ~3.45% health on top

### Pension (Mandatory since 2008)
- Employee contribution: 6% of salary
- Employer contribution: 6.5% of salary
- Employer severance (pitzuim): 6% of salary
- Tax-exempt pension contribution ceiling exists

### Tax Credits (Nekudot Zikui)
- Each credit point worth ~2,904 NIS/year (242 NIS/month) in 2025
- Base: 2.25 points for every resident
- Additional: Woman +0.5, new immigrant (years 1-1.5: +3, 1.5-2: +2, 2-3.5: +1)
- Children, single parent, disabled, military service credits

### Use Cases
1. **Calculate net salary** — From gross to net with all deductions
2. **Employer cost calculation** — Total cost to employer for a given gross salary
3. **Tax optimization** — Suggest credit points and deductions
4. **Payslip explanation** — Explain each line of an Israeli payslip (tlush maskoret)
5. **Salary comparison** — Compare offers accounting for benefits

---

## Build Steps

### Task 1: Create SKILL.md

**Files:**
- Create: `repos/tax-and-finance/israeli-payroll-calculator/SKILL.md`

```markdown
---
name: israeli-payroll-calculator
description: >-
  Calculate Israeli payroll including income tax, Bituach Leumi (National
  Insurance), health tax, pension contributions, and net salary. Use when
  user asks to calculate salary, "tlush maskoret", payroll deductions, "bruto
  to neto", employer cost, tax credits (nekudot zikui), or needs help
  understanding Israeli payslip items. Covers employees, freelancers (atzmai),
  and employer cost calculations. Do NOT use for US, UK, or other countries'
  payroll calculations.
license: MIT
allowed-tools: "Bash(python:*)"
compatibility: "Works with Claude Code, Claude.ai, Cursor. No network access required."
metadata:
  author: skills-il
  version: 1.0.0
  category: tax-and-finance
  tags: [payroll, salary, tax, bituach-leumi, pension, israel]
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
Result: Detailed breakdown showing ~15,800-16,200 NIS net (approximate)

### Example 2: Employer Cost
User says: "How much does it cost an employer to pay 15,000 NIS gross?"
Result: Total employer cost ~19,500-20,000 NIS including all contributions

### Example 3: Salary Comparison
User says: "Compare a 25,000 NIS offer with a 22,000 NIS + car offer"
Result: Side-by-side comparison accounting for car tax benefit (shovi rechev)

## Troubleshooting

### Error: "Tax brackets may be outdated"
Cause: Tax brackets update annually (usually January 1)
Solution: Verify current brackets at Tax Authority website. Skill uses 2025 brackets — check references/tax-brackets.md for updates.

### Error: "Credit points don't match"
Cause: Various life circumstances affect credit points
Solution: Review full credit point table. Common additions: female (+0.5), new immigrant (up to +3), children, single parent, disabled.
```

**Step 2: Create Python calculation script**
`scripts/calculate-payroll.py` — Takes gross salary + parameters, outputs full breakdown.

**Step 3: Create references**
- `references/tax-brackets.md` — Current year brackets with update instructions
- `references/bituach-leumi-rates.md` — NI and health tax rate tables
- `references/credit-points.md` — Full credit point eligibility table

**Step 4: Validate and commit**
