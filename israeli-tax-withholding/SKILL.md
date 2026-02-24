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

### Step 5: Certificate Types
| Certificate | Hebrew | Purpose |
|------------|--------|---------|
| Ishur Nikui Mas BeMakor | ishur nikui mas bemakor | Reduced/zero withholding on payments |
| Ishur Tium Mas | ishur tium mas | Tax coordination for multiple employers |
| Ishur Nikui Mas Rechisha | ishur nikui mas rechisha | Real estate purchase tax withholding |

### Step 6: How to Obtain a Certificate
1. Apply via SHAAM portal (https://www.misim.gov.il)
2. Provide: TIN, financial statements, tax returns
3. Processing time: 2-4 weeks
4. Certificate valid for current tax year (January-December)
5. Renewal required annually

## Examples

### Example 1: Payment to Freelancer
User says: "I need to pay a freelancer 10,000 NIS for consulting"
Result: Default 20% withholding = 2,000 NIS withheld, 8,000 NIS net payment + 1,700 NIS VAT (if osek morsheh). Recommend asking freelancer for their withholding certificate.

### Example 2: Certificate Check
User says: "A vendor gave me a 0% withholding certificate, is it valid?"
Result: Verify certificate year, check SHAAM, confirm vendor TIN matches certificate.

### Example 3: Cross-border Payment
User says: "I need to pay a US company for software licenses"
Result: Default 25% withholding on payments to non-residents. Check if tax treaty applies (US-Israel treaty may reduce to 10-15%). Recommend consulting tax advisor for treaty benefits.

## Troubleshooting

### Error: "Certificate expired"
Cause: Withholding certificates are annual, expire December 31
Solution: Ask vendor for renewed certificate for current tax year.

### Error: "Wrong withholding rate applied"
Cause: Using default rate when certificate exists, or vice versa
Solution: Always request certificate before first payment. Apply certificate rate only during its validity period.

### Error: "Late reporting penalty"
Cause: Withholding report (Form 856) not filed by the 15th
Solution: File immediately. Penalties apply for late reporting and late payment of withheld amounts.
