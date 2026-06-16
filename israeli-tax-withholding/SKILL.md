---
name: israeli-tax-withholding
description: Israeli tax withholding (nikui mas bemakor) rates, certificates, and calculations. Use when user asks about withholding tax, "nikui mas", withholding certificates, "ishur nikui", tax coordination (tium mas), or needs to calculate withholding amounts. Covers payments to suppliers, freelancers, landlords, and cross-border payments. Do NOT use for employee payroll tax (see israeli-payroll-calculator) or VAT reporting.
license: MIT
---

# Israeli Tax Withholding

## Instructions

### Step 1: Identify Payment Type and Default Rate
| Payment Type | Hebrew | Default Rate | Section |
|-------------|--------|-------------|---------|
| Services/assets (payee keeps acceptable books, no certificate) | shlumim avur sherutim o nechasim | 20% | reg. 1977 |
| Services/assets (payee without acceptable books, no certificate) | shlumim avur sherutim o nechasim | 30% | reg. 1977 |
| Services (companies, no certificate) | shlumim avur sherutim | 20-30% by tax-office classification | reg. 1977 |
| Rent (real estate, where the tenant deducts the rent as a business expense) | schar dira | 35% (uniform, no residential/commercial split) | reg. 1998 |
| Royalties | tamlugim | 23% | 170 |
| Interest | ribit | 25% | 164 |
| Dividends | dividendim | 25-30% | 164 |
| Payments to non-residents | tishlumin letoshvei chutz | 25% | 170 |

For a service/asset payment with no certificate, the statutory default under the 1977 regulations is **20% where the payee keeps acceptable books** and **30% where the payee does not** (the 30% is the penalty rate for an unverified/no-books payee, not a separate "high" rate, there is no ~47% service-withholding rate). A valid certificate is what brings the rate down further (often to 0-5%). Rent on real estate that the tenant deducts as a business expense is withheld at a uniform **35%** (there is no separate residential vs. commercial rate); a private residential tenant who cannot deduct the rent is generally not a withholding agent at all.

There is a one-time de-minimis floor: a single payment to a payee below roughly
4,920-5,040 NIS including VAT (the annually-indexed threshold, verify the current
year) does not require withholding, unless your cumulative payments to that payee
cross the threshold.

### Step 2: Check for Withholding Certificate
A valid withholding certificate (ishur nikui mas bemakor) may reduce or eliminate
the withholding:
- Certificate shows: business name, TIN, approved rate, validity period
- **Verify:** certificate year matches the current tax year
- **Verify:** certificate is genuine, issued by the ITA
- **Online lookup:** verify the payee's certificate status through the ITA's
  gmishurim service (see Reference Links)

### Step 3: Calculate Withholding
```
Payment amount (before VAT): X NIS
Withholding rate: Y% (from certificate, or default)
Withholding amount: X * Y%
Net payment to payee: X - withholding
VAT (if applicable): calculated separately on the full pre-withholding amount
```

### Step 4: Periodic Reporting and Payment (Form 102)
- Amounts withheld must be reported and paid to the ITA periodically, monthly or
  bi-monthly depending on your business size.
- **Form 102** is the periodic deductions report and payment. It summarises the
  wages/payments and the income tax (and, on the National Insurance side, the
  parallel 102) withheld in the period.
- **Deadline:** the 15th of the month following the reporting period. Late
  reporting and late payment carry penalties and indexation.

### Step 5: Annual Reconciliation (Form 856)
- **Form 856** is the ANNUAL withholding reconciliation for payments to
  suppliers and service providers. It is a detailed file listing every payee,
  the total paid, and the total withheld during the year, reconciled against the
  Form 102 deposits made through the year.
- **Deadline:** April 30 of the year following the reporting year.
- Workflow: deposit withheld amounts periodically via Form 102 -> at year end,
  compile the per-payee detail file -> submit Form 856 by April 30.
- Form 856 is separate from the payee's own annual return; it is the payer's
  obligation as the withholding agent.
- **Form 126** is the salary-side counterpart: the annual report of employee
  salaries and the tax withheld from them, filed alongside Form 856 (same April
  30 baseline, commonly extended by ITA notice). A payer with both suppliers and
  employees files both: 856 for suppliers/service providers, 126 for salaries.

### Step 6: Certificate Types
| Certificate | Hebrew | Purpose |
|------------|--------|---------|
| Ishur Nikui Mas BeMakor | ishur nikui mas bemakor | Reduced/zero withholding on payments |
| Ishur Tium Mas | ishur tium mas | Tax coordination for multiple payers/employers |
| Ishur Nikui Mas Rechisha | ishur nikui mas rechisha | Real estate purchase tax withholding |

### Step 7: How to Obtain a Certificate
1. Apply through the ITA online services (the gmishurim system).
2. Provide: TIN, financial statements, tax returns.
3. Certificate valid for the current tax year (January-December).
4. Renewal required annually.

### Step 8: Mandatory Withholder Threshold
Not every payer must withhold. A business becomes a mandatory withholding agent
for service/asset payments once its turnover crosses the ITA's turnover
threshold (indexed annually). Below the threshold, withholding on service
payments may not be required, but a business with employees still files Form 102
for payroll. Check the current-year turnover threshold before concluding a payer
is exempt.

## Examples

### Example 1: Payment to Freelancer
User says: "I need to pay a freelancer 10,000 NIS for consulting"
Result: With no certificate, the default is 30% withholding = 3,000 NIS withheld,
7,000 NIS net payment, plus 1,800 NIS VAT (if the payee is an osek murshe).
Recommend asking the freelancer for their withholding certificate, which usually
brings the rate down to 0-5%.

### Example 2: Certificate Check
User says: "A vendor gave me a 0% withholding certificate, is it valid?"
Result: Verify the certificate year, check the ITA gmishurim lookup, and confirm
the vendor's TIN matches the certificate.

### Example 3: Cross-border Payment
User says: "I need to pay a US company for software licenses"
Result: Default 25% withholding on payments to non-residents. Check if a tax
treaty applies (the US-Israel treaty may reduce the rate). Recommend consulting a
tax advisor for treaty benefits and the required documentation.

## Bundled Resources

### Scripts
- `scripts/calculate_withholding.py` -- Calculates Israeli tax withholding (nikui mas bemakor) amounts for various payment types (services, rent, royalties, dividends, non-resident payments). Supports certificate-based reduced rates and outputs net payment plus VAT breakdown. Run: `python scripts/calculate_withholding.py --help`

### References
- `references/withholding-rates.md` -- Default withholding rates by payment type under Section 164 (income payments) and Section 170 (special payments), including rates for individuals, companies, major shareholders, and non-residents. Consult when determining the correct default rate for a payment.
- `references/certificate-guide.md` -- Guide to Israeli withholding certificates: types (Ishur Nikui Mas BeMakor, Ishur Tium Mas), application process, validity periods, and verification through the ITA gmishurim service. Consult when a vendor presents a withholding certificate or when guiding users through the certificate application process.

## Recommended MCP Servers
- **israel-law** -- look up the Income Tax Ordinance sections (164, 170) and the cash-use law text when you need the primary legal source behind a withholding rule.

## Gotchas
- Israeli withholding rates are set by the regulations and by the ITA per business, not as one flat rate. With no certificate the service/asset default is **20% where the payee keeps acceptable books and 30% where they do not**; there is no ~47% service-withholding rate (that figure is not in the regulations, do not cite it). An established payee may hold a certificate for 0-5%. Do not hardcode a single rate.
- Withholding exemption/reduction certificates (ishur nikui mas bemakor) expire annually and must be renewed. Do not rely on a certificate without checking its validity period.
- When paying a foreign contractor, Israel requires withholding unless a tax treaty provides a reduced rate. Do not apply domestic rates to international payments or skip withholding entirely.
- Withholding on rent that the tenant deducts as a business expense is a uniform **35%**, there is NO separate residential vs. commercial rate, and no "30% residential" rate exists. A private residential tenant who cannot deduct the rent is generally not a withholding agent at all. The reduced/zero rate applies only with a valid certificate.
- **2026 black-market legislation (Income Tax Circular 3/2026, effective for payments made from 1.1.2026):** an expense or input-VAT deduction is disallowed where the payer failed to withhold tax or to report it as required, or where the payment breached the Law for Reduction of the Use of Cash. The cash-use law caps cash in a business-to-business transaction at 6,000 NIS. Treat a missed withholding or a cash-law breach as a deduction risk, not just a reporting issue.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Israel Tax Authority (ITA) | `https://www.gov.il/he/departments/israel_tax_authority` | Default withholding rates per activity, annual updates |
| Withholding certificate lookup (gmishurim) | `https://www.gov.il/he/service/itc-gmishurim` | Verify a vendor's certificate status and validity period |
| gmishurim direct lookup tool | `https://taxinfo.taxes.gov.il/gmishurim/firstPage.aspx` | Direct online check of a payee's withholding/bookkeeping status |
| Form 856 filing | `https://www.gov.il/he/service/form-856` | Annual withholding reconciliation (supplier/service-provider detail file) |
| Income Tax Ordinance s.164/170 | `https://www.nevo.co.il/law_html/law01/255_001.htm` | Legal basis for withholding on services, rent, non-residents |
| Tax treaty list | `https://www.gov.il/he/departments/guides/taxation-agreements` | Reduced rates for payments to foreign contractors |

## Troubleshooting

### Error: "Certificate expired"
Cause: withholding certificates are annual and expire December 31.
Solution: ask the vendor for a renewed certificate for the current tax year.

### Error: "Wrong withholding rate applied"
Cause: using the default rate when a certificate exists, or vice versa; or
confusing the with-books (20%) and no-books (30%) service defaults.
Solution: always request the certificate before the first payment, apply the
certificate rate only during its validity period, and for a no-certificate
service payment use 20% if the payee keeps acceptable books, 30% if they do not.

### Error: "Late reporting penalty"
Cause: the periodic deductions report (Form 102) was not filed by the 15th.
Solution: file immediately. Penalties and indexation apply for late reporting and
late payment of withheld amounts. Remember the separate annual Form 856
reconciliation is due April 30.

### Error: "Deduction disallowed by the tax office"
Cause: under Circular 3/2026, an expense or input-VAT deduction is disallowed
when the payer did not withhold or report as required, or breached the cash-use
law (cash over 6,000 NIS in a business-to-business transaction).
Solution: withhold and report correctly on Form 102, keep the per-payee detail
for Form 856, and pay above-threshold amounts by non-cash means.
