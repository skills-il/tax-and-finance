# Israeli Tax Withholding Skill — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a skill for Israeli tax withholding certificates (ishur nikui mas bemakor), withholding rates, and SHAAM certificate retrieval guidance.

**Architecture:** Domain-Specific Intelligence + Workflow Automation. Embeds withholding tax rules and SHAAM certificate process.

**Tech Stack:** SKILL.md, references for withholding rates and certificate types.

---

## Research

### Israeli Tax Withholding System (Nikui Mas BeMakor)
- **Concept:** Payer withholds tax from payment before transferring to payee
- **Default rate:** Varies by payment type (services: 20-30%, rent: 35%, royalties: 23%)
- **Reduced rate:** Certificate from Tax Authority allows lower rate (ishur nikui mas bemakor)
- **Zero rate:** Some businesses get 0% withholding certificates
- **SHAAM API:** Supports certificate lookup and validation

### Certificate Types
- **Ishur Nikui Mas BeMakor:** Withholding tax exemption/reduction certificate
- **Ishur Nikui Mas Rechisha:** Purchase tax withholding (real estate)
- **Ishur Tium Mas:** Tax coordination certificate (multiple employers)

### Use Cases
1. **Determine withholding rate** — What rate applies to a specific payment type
2. **Certificate guidance** — How to obtain/renew withholding certificates
3. **Certificate validation** — Verify a business's certificate status
4. **Withholding calculation** — Calculate amount to withhold from a payment
5. **Tax coordination** — Guide for employees with multiple employers

---

## Build Steps

### Task 1: Create SKILL.md

```markdown
---
name: israeli-tax-withholding
description: >-
  Israeli tax withholding (nikui mas bemakor) rates, certificates, and
  calculations. Use when user asks about withholding tax, "nikui mas",
  withholding certificates, "ishur nikui", tax coordination (tium mas),
  or needs to calculate withholding amounts. Covers payments to suppliers,
  freelancers, landlords, and cross-border payments. Do NOT use for employee
  payroll tax (see israeli-payroll-calculator) or VAT reporting.
license: MIT
compatibility: "Network access helpful for SHAAM certificate lookup."
metadata:
  author: skills-il
  version: 1.0.0
  category: tax-and-finance
  tags: [tax, withholding, nikui-mas, certificates, shaam, israel]
---

# Israeli Tax Withholding

## Instructions

### Step 1: Identify Payment Type and Default Rate
| Payment Type | Hebrew | Default Rate | Section |
|-------------|--------|-------------|---------|
| Services (individuals) | shlumim | 20% | 164 |
| Services (companies) | shlumim | 20-30% | 164 |
| Rent (business property) | schirut | 35% | 170 |
| Royalties | tamlugim | 23% | 170 |
| Interest | ribit | 25% | 164 |
| Dividends | dividendim | 25-30% | 164 |
| Payments to non-residents | tishlumin lechul | 25% | 170 |

### Step 2: Check for Withholding Certificate
A valid withholding certificate (ishur nikui mas bemakor) may reduce or eliminate the withholding:
- Certificate shows: Business name, TIN, approved rate, validity period
- **Verify:** Certificate year matches current tax year
- **Verify:** Certificate is from Tax Authority (not a fake)
- **SHAAM lookup:** Can verify certificate status via SHAAM portal/API

### Step 3: Calculate Withholding
```
Payment amount (before VAT): X NIS
Withholding rate: Y% (from certificate, or default)
Withholding amount: X * Y%
Net payment to payee: X - withholding
VAT (if applicable): Calculated separately on full amount
```

### Step 4: Reporting and Payment
- Withholding must be reported and paid to Tax Authority monthly
- Form 856: Monthly withholding report
- Form 856A: Annual summary of all withholdings
- Deadline: 15th of following month

## Examples

### Example 1: Payment to Freelancer
User says: "I need to pay a freelancer 10,000 NIS for consulting"
Result: Default 20% withholding = 2,000 NIS withheld, 8,000 NIS net payment + 1,700 NIS VAT (if osek morsheh). Recommend asking freelancer for their withholding certificate.

### Example 2: Certificate Check
User says: "A vendor gave me a 0% withholding certificate, is it valid?"
Result: Verify certificate year, check SHAAM, confirm vendor TIN matches certificate.

## Troubleshooting

### Error: "Certificate expired"
Cause: Withholding certificates are annual, expire December 31
Solution: Ask vendor for renewed certificate for current tax year.
```
