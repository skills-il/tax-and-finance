# Israeli VAT Reporting Skill — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a skill that teaches Claude to prepare, validate, and guide submission of Israeli VAT reports (Doch Maam) per Tax Authority requirements.

**Architecture:** Workflow Automation skill with Domain-Specific Intelligence pattern. Embeds Israeli VAT regulations, reporting periods, calculation rules, and SHAAM API submission guidance.

**Tech Stack:** SKILL.md, Python calculation scripts, SHAAM API reference docs.

---

## Research

### Israeli VAT System
- **Standard Rate:** 17% (as of 2025)
- **Reporting Frequency:**
  - Monthly: Businesses with annual turnover > 1.5M NIS
  - Bi-monthly: Businesses with turnover < 1.5M NIS
  - Annual: Osek Patur (exempt dealers) below ~120K NIS threshold
- **Reporting Deadline:** 15th of the month following the reporting period
- **Online submission:** via SHAAM portal or API
- **Key Form:** Form 874 (Doch Maam Tkufati — Periodic VAT Report)

### SHAAM API Endpoints for VAT
- `POST /api/tax/vat/report` — Submit periodic VAT report
- `GET /api/tax/vat/report/{period}` — Check report status
- `POST /api/tax/vat/calculate` — Pre-calculate VAT liability

### VAT Calculation Rules
- **Output VAT (mas etzot):** VAT collected on sales
- **Input VAT (mas tsmachot):** VAT paid on business purchases (deductible)
- **Net liability:** Output VAT - Input VAT
- **Adjustments:** Bad debts, fixed assets, mixed-use assets (proportional deduction)
- **Special rates:** Zero-rated exports, exempt financial services, Eilat zone (no VAT)

### Use Cases
1. **Prepare VAT report** — Calculate net VAT from sales/purchase records
2. **Determine reporting period** — Identify if monthly/bi-monthly/annual
3. **Validate calculations** — Check VAT arithmetic and deduction eligibility
4. **Explain regulations** — Answer questions about VAT rules, rates, exemptions
5. **Filing guidance** — Walk through SHAAM submission process

---

## Design

### Skill Category
Workflow Automation (Category 2) + Domain-Specific Intelligence (Pattern 5)

### Progressive Disclosure
- **Frontmatter:** Trigger on "VAT report", "doch maam", "maam", "VAT filing", "Israeli VAT"
- **SKILL.md body:** Calculation workflow, reporting rules, filing guidance
- **references/:** Full VAT regulation summary, special cases, Eilat zone rules

### File Structure
```
israeli-vat-reporting/
  SKILL.md
  scripts/
    calculate-vat.py           # VAT calculation helper
  references/
    vat-regulations.md         # Israeli VAT law summary
    special-cases.md           # Zero-rated, exempt, Eilat rules
    reporting-calendar.md      # Deadlines by business type
```

### Success Criteria
- Triggers on 90%+ of VAT-related queries
- Correctly calculates net VAT liability from input/output data
- Identifies correct reporting period and deadline
- Does NOT trigger on income tax or non-Israeli VAT queries

---

## Build Steps

### Task 1: Create SKILL.md

**Files:**
- Create: `repos/tax-and-finance/israeli-vat-reporting/SKILL.md`

**Step 1: Write SKILL.md**

```markdown
---
name: israeli-vat-reporting
description: >-
  Prepare, validate, and guide submission of Israeli VAT reports (Doch Maam)
  per Tax Authority standards. Use when user asks about VAT reporting, VAT
  calculation, "doch maam", "maam", Israeli VAT filing, VAT deadlines, or
  input/output VAT reconciliation. Supports monthly, bi-monthly, and annual
  reporting. Handles zero-rated exports, exempt transactions, and Eilat zone
  rules. Do NOT use for income tax, corporate tax, or non-Israeli VAT systems.
license: MIT
compatibility: "Works with Claude Code, Claude.ai, Cursor. Network access optional for SHAAM API."
metadata:
  author: skills-il
  version: 1.0.0
  category: tax-and-finance
  tags: [vat, maam, tax, reporting, shaam, israel]
---

# Israeli VAT Reporting

## Instructions

### Step 1: Determine Business Type and Reporting Frequency
Ask the user about their business registration:

| Type | Hebrew | Annual Turnover | Reporting Period |
|------|--------|----------------|-----------------|
| Osek Morsheh (Licensed Dealer) | osek morsheh | > 120K NIS | Monthly or Bi-monthly |
| Osek Patur (Exempt Dealer) | osek patur | < ~120K NIS | Annual summary only |
| Amuta (Non-profit) | amuta | Any | Monthly or Bi-monthly |
| Company (Ltd) | chevra | Any | Monthly |

Monthly reporting: Annual turnover > 1.5M NIS
Bi-monthly reporting: Annual turnover < 1.5M NIS

### Step 2: Collect Transaction Data
For the reporting period, gather:
- **Sales (output):** All invoices issued with VAT amounts
- **Purchases (input):** All purchase invoices with VAT amounts
- **Special transactions:** Exports (zero-rated), exempt services, fixed asset purchases

### Step 3: Calculate VAT Liability

```
Output VAT (mas etzot)    = Sum of VAT on all sales invoices
Input VAT (mas tsmachot)  = Sum of VAT on deductible purchase invoices
Net VAT                   = Output VAT - Input VAT

If Net > 0: Business owes SHAAM (payment due)
If Net < 0: SHAAM owes business (refund claim)
```

**Input VAT deduction rules:**
- Only from valid tax invoices (hashbonit mas) with seller's TIN
- Vehicle expenses: 2/3 deductible (1/3 non-deductible for private use)
- Entertainment: NOT deductible
- Mixed business/personal: Proportional deduction only

### Step 4: Fill Form 874 Fields
Map calculated values to form fields:
- Field 1: Total sales (including VAT)
- Field 2: Zero-rated sales (exports)
- Field 3: Exempt sales
- Field 4: Total output VAT
- Field 5: Total purchases (including VAT)
- Field 6: Input VAT claimed
- Field 7: Net VAT (Field 4 - Field 6)
- Field 8: Adjustments (if any)
- Field 9: Amount to pay / refund

### Step 5: Validate and Submit
Before submission, verify:
1. All sales invoices accounted for (cross-reference with e-invoice allocation numbers)
2. Input VAT claims supported by valid tax invoices
3. Correct reporting period selected
4. Deadline not passed (15th of following month)

**Filing options:**
- SHAAM online portal: `https://www.misim.gov.il`
- Accountant submission via SHAAM API
- Paper form (being phased out)

## Examples

### Example 1: Monthly VAT Report
User says: "Help me prepare my VAT report for January 2026"
Actions:
1. Determine: Monthly reporter (turnover > 1.5M or company)
2. Collect: January sales and purchase invoices
3. Calculate: Output VAT 34,000 - Input VAT 22,000 = Net 12,000 NIS owed
4. Prepare: Form 874 with all fields mapped
5. Guide: Submit via SHAAM portal by February 15th
Result: Complete VAT report ready for filing

### Example 2: Bi-monthly Report with Exports
User says: "I need to file my VAT for November-December, I had some exports"
Actions:
1. Determine: Bi-monthly reporter
2. Identify: Export sales are zero-rated (0% VAT, but still reported)
3. Calculate: Domestic output VAT - Input VAT = Net
4. Note: Exports reported in Field 2, no VAT but supports input VAT recovery
Result: VAT report with zero-rated export handling

## Troubleshooting

### Error: "Reporting period mismatch"
Cause: Submitting for wrong period (e.g., single month when registered as bi-monthly)
Solution: Check business registration. Bi-monthly periods: Jan-Feb, Mar-Apr, May-Jun, Jul-Aug, Sep-Oct, Nov-Dec.

### Error: "Input VAT not deductible"
Cause: Claiming VAT from non-deductible expenses (entertainment, non-business)
Solution: Review deduction rules in Step 3. Only business expenses with valid tax invoices qualify.

### Error: "Late filing penalty"
Cause: Filing after the 15th of the following month
Solution: File immediately. Late penalty is 0.25% of net VAT per week of delay, plus linkage differentials.
```

**Step 2: Validate**
Run: `./repos/tax-and-finance/scripts/validate-skill.sh repos/tax-and-finance/israeli-vat-reporting/SKILL.md`

**Step 3: Commit**
```bash
git add repos/tax-and-finance/israeli-vat-reporting/
git commit -m "feat(tax): add israeli-vat-reporting skill with Form 874 workflow"
```

### Task 2: Create calculation script and references

Create `scripts/calculate-vat.py` for automated VAT arithmetic and `references/` for regulation details. Follow same pattern as e-invoice skill.

### Task 3: Test triggering and update README

Test 10+ trigger queries, verify no false triggers on income tax queries, update category README.
