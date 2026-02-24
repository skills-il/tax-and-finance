# Israeli Pension Advisor Skill — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a skill for navigating the Israeli pension system — keren pensia, bituach menahalim, keren hishtalmut, and retirement planning.

**Architecture:** Domain-Specific Intelligence skill. Embeds Israeli pension regulations, fund types, contribution rules, and tax benefits.

**Tech Stack:** SKILL.md, references for pension fund types and tax benefits.

---

## Build Steps

### Task 1: Create SKILL.md

```markdown
---
name: israeli-pension-advisor
description: >-
  Navigate the Israeli pension and savings system including pension funds
  (keren pensia), manager's insurance (bituach menahalim), training funds
  (keren hishtalmut), and retirement planning. Use when user asks about
  Israeli pension, "pensia", "keren hishtalmut", retirement savings,
  "bituach menahalim", pension contributions, or tax benefits from savings.
  Covers mandatory pension, voluntary savings, and withdrawal rules. Do NOT
  provide specific investment recommendations or fund performance comparisons.
license: MIT
compatibility: "No network required."
metadata:
  author: skills-il
  version: 1.0.0
  category: tax-and-finance
  tags: [pension, retirement, savings, keren-hishtalmut, israel]
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
- **Pension:** Age 67 (men) / 62-65 (women), or early pension with reduction
- **Keren hishtalmut:** After 6 years (tax-free), or 3 years (education)
- **Severance (pitzuim):** Upon termination, subject to Section 14 arrangement

## Examples

### Example 1: New Employee
User says: "I just started a new job, what pension should I choose?"
Result: Explain mandatory pension (keren pensia vs bituach menahalim), recommend checking fees, suggest keren hishtalmut if employer offers it.

### Example 2: Self-Employed Savings
User says: "I'm a freelancer, how should I save for retirement?"
Result: Explain self-employed pension obligations, keren hishtalmut benefits, tax deduction calculations.

## Troubleshooting

### Error: "Pension fund not transferring"
Cause: Switching pension funds requires specific process
Solution: Contact new fund to initiate transfer. Old fund must complete within 10 business days. No penalties for switching.
```
