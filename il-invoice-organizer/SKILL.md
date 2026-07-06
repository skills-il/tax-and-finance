---
name: il-invoice-organizer
description: "Parse and organize Hebrew invoices for Israeli bookkeeping: VAT 1/6 extraction, Tax Authority expense categories, Osek Murshe/Patur recognition, and accountant-ready export. Use when user asks about organizing invoices, cheshbonit, expense categorization, sivug hotza'ot, VAT extraction from totals, Osek Murshe vs Osek Patur rules, or preparing documents for their accountant (ro'eh cheshbon). Supports Hebrew OCR text parsing and automatic categorization per Tax Authority standards. Do NOT use for invoice generation (use israeli-e-invoice instead) or for VAT report filing (use israeli-vat-reporting instead)."
license: MIT
compatibility: "Works with Claude Code, Cursor, GitHub Copilot, Windsurf, OpenCode, Codex. Python 3.8+ for helper scripts."
---

# IL Invoice Organizer

## Instructions

### Step 1: Identify Invoice Type and Source
Determine what documents the user has:

| Document Type | Hebrew | VAT Reclaimable | Categorization |
|---------------|--------|----------------|----------------|
| Tax Invoice (300) | חשבונית מס | Yes - extract VAT | Full categorization |
| Tax Invoice/Receipt (305) | חשבונית מס/קבלה | Yes - extract VAT | Full categorization |
| Receipt only (320) | קבלה | No VAT to reclaim | Payment record only |
| Credit Invoice (310) | חשבונית זיכוי | Yes - negative VAT | Reverse original category |
| Proforma (330) | חשבונית פרופורמה | No - not a tax document | For reference only |

Key: Only tax invoices (300, 305) allow VAT input deduction (nikui mas tsumos).

### Step 2: Extract Invoice Data
Parse the following fields from each invoice:

| Field | Hebrew | Where to Find | Validation |
|-------|--------|---------------|------------|
| Supplier name | שם הספק | Header | Must match TIN |
| Supplier TIN | מספר עוסק | Header | 9 digits with check digit |
| Invoice number | מספר חשבונית | Header | Sequential |
| Date | תאריך | Header | DD/MM/YYYY format |
| Net amount | סכום לפני מע"מ | Line items sum | Before VAT |
| VAT amount | סכום מע"מ | VAT line | = Net * 0.18 |
| Total amount | סכום כולל | Bottom | = Net + VAT |
| Allocation number | מספר הקצאה | B2B invoices above SHAAM threshold | SHAAM allocation required |

SHAAM allocation threshold timeline (Israel Tax Authority, accelerated rollout):

| Period | Threshold (pre-VAT) |
|--------|---------------------|
| 2025 (full year) | NIS 20,000 |
| 1 Jan 2026 to 31 May 2026 | NIS 10,000 |
| From 1 Jun 2026 | NIS 5,000 (further reductions planned for 2027) |

A B2B tax invoice above the threshold without a valid SHAAM allocation number (מספר הקצאה) is not eligible for VAT input deduction. Always check the threshold for the invoice issue date, not today's date.

### Step 3: Extract VAT (1/6 Rule)

**First confirm the supplier is an Israeli VAT-registered dealer.** Foreign suppliers (AWS, Google, OpenAI, Figma, Upwork, and most overseas SaaS) charge NO Israeli VAT. Do NOT apply the 18/118 rule to a foreign-supplier invoice, or you will fabricate a reclaimable input-VAT figure that does not exist. Import VAT on goods is reclaimed only through the customs import entry (רשימון יבוא), not the foreign supplier's invoice. Convert any foreign-currency amount to shekels at the invoice-date exchange rate before booking. For imports and purchases from foreign/unregistered suppliers, self-invoicing / reverse charge (חשבונית עצמית) may apply, route the accountant to that mechanism.

Israeli VAT is 18% (raised from 17% effective 1 January 2025). For an Israeli-supplier invoice where only the total (gross) is visible:

```python
# VAT extraction from gross amount (כלל השישית)
vat_rate = 0.18  # 18% standard rate (effective 1 Jan 2025)
gross_amount = 1180  # סכום כולל מע"מ

# Method: VAT = gross * (rate / (1 + rate)) = gross * (18/118)
vat_amount = gross_amount * (vat_rate / (1 + vat_rate))
# = 1180 * (0.18 / 1.18) = 1180 * 0.1525... = 180.00

net_amount = gross_amount - vat_amount
# = 1180 - 180 = 1000
```

Shortcut at 18%: VAT ≈ Total / 6.556 (the divisor is 118/18). The colloquial name "klal hashishit" (the 1/6 rule) predates the rate hike and is now an approximation, not a literal sixth.

### Step 4: Categorize by Expense Category
Assign each expense to a standard bookkeeping category. These 12 working categories align with the Tax Authority income-statement structure (the דוח רווח והפסד / form 6111 groupings), with `references/expense-categories.md`, and with the keyword-based auto-categorizer in `scripts/categorize_invoices.py`:

| Code | Hebrew | English | Common Examples |
|:----:|--------|---------|-----------------|
| 1 | חומרי גלם | Raw materials | Production materials, components |
| 2 | קבלני משנה | Subcontractors | Freelancer invoices, outsourced services |
| 3 | שכר עבודה | Wages and salaries | Employee salaries, bonuses, commissions |
| 4 | ביטוח לאומי מעסיק | Employer NII | Employer share of Bituach Leumi |
| 5 | שכירות | Rent | Office, warehouse, shop, workshop rent |
| 6 | ביטוח | Insurance | Liability, professional, property, inventory |
| 7 | חשמל ומים | Utilities | Electricity, water |
| 8 | תקשורת | Communications | Phone, mobile, internet, cloud services |
| 9 | הוצאות רכב | Vehicle expenses | Fuel, maintenance, vehicle insurance, parking |
| 10 | פחת | Depreciation | Computers, furniture, equipment, vehicles |
| 11 | הוצאות משרד | Office expenses | Stationery, paper, toner, postage |
| 12 | הוצאות אחרות | Other expenses | Representation, travel, training, subscriptions |

Use `scripts/categorize_invoices.py` for automatic categorization.

### Step 5: Identify Business Type
Determine supplier and customer business status:

| Status | Hebrew | VAT Treatment | Invoice Type |
|--------|--------|--------------|--------------|
| Osek Murshe | עוסק מורשה | Charges VAT, can deduct input VAT | Tax Invoice (300/305) |
| Osek Patur | עוסק פטור | No VAT charged (under threshold) | Receipt only (320) |
| Hevra Peratit (HP) | חברה פרטית (ח"פ) | Charges VAT, TIN starts 51/52 | Tax Invoice |
| Amuta (Non-profit) | עמותה | Usually no VAT, TIN starts 58 | Receipt |
| Malkar (Non-profit) | מלכ"ר | No VAT | Receipt |

Important: You can only deduct input VAT (mas tsumos) from tax invoices issued by Osek Murshe (or Hevra Peratit) suppliers. Receipts from Osek Patur do not have VAT to deduct.

**Osek Patur turnover ceiling (2026): NIS 122,833** (raised from NIS 120,000 in 2024–2025). Once a freelancer crosses this annual turnover, they must convert to Osek Murshe from the date of the breach and notify the VAT office. Certain professions (lawyers, doctors, architects, engineers, accountants and a few others) are barred from Osek Patur status regardless of turnover.

**Invoice issuance timing**: Israeli tax law requires a tax invoice (Heshbonit Mas) to be issued within 14 days of the taxable supply or of payment, whichever comes first. Invoices dated more than 14 days after the supply may be challenged by the Tax Authority.

### Step 6: Generate Accountant-Ready Export
Organize the data for the accountant (ro'eh cheshbon).

Output format (CSV/Excel):
```
Date, Supplier, TIN, Invoice#, Category, Net, VAT, Total, Notes
15/01/2026, חברת אלפא, 515000000, 1234, קבלני משנה, 10000, 1800, 11800, שירותי פיתוח
```

Include summary:
- Total expenses by category
- Total input VAT (mas tsumos) to reclaim
- Missing invoices or data gaps flagged
- Separate section for non-deductible items

### Step 7: Align with Filing Deadlines
Surface the relevant filing windows so the user knows when the accountant needs the organized batch.

| Filing | Frequency | Threshold / Trigger | Deadline |
|--------|-----------|--------------------|----------|
| VAT return (Doch Tkufati) | Bi-monthly | Annual turnover ≤ NIS 1,775,000 | 15th of the month after the period |
| VAT return | Monthly | Annual turnover > NIS 1,775,000 | 15th of the next month |
| Detailed VAT report (Doch Meforat) | Per VAT period | Annual turnover > NIS 500,000 (from 1 Jan 2026) | With the periodic VAT return |
| Income tax annual return (Doch Shnati) | Annual | All self-employed | 30 April (paper) / 31 May (online); via מייצג can extend to Nov–Dec |
| Bituach Leumi advances | Monthly | All self-employed | 15th of next month |

Hand the categorized batch to the accountant at least 7-10 days before the VAT deadline so they have time to reconcile and file. For invoices over the SHAAM threshold without an allocation number, flag urgently: the deadline to request a corrected invoice from the supplier is before that period's VAT filing.

**Osek Zair (Small Dealer) option**: a self-employed individual with annual revenue ≤ NIS 122,833 may elect the "Small Dealer" track on the annual return and deduct a **flat 30% of revenue as expenses** instead of actual expenses. The election is **not available** if the freelancer has employees, has inadequate books, more than 25% of revenue is from a related party, the freelancer is a 10%+ shareholder in a company, or other Finance Minister exclusions apply. When this election is in play, this skill should still organize invoices for backup and Bituach Leumi purposes, but the categorized totals will not flow to the income tax return.

## Examples

### Example 1: Monthly Invoice Organization
User says: "I have 30 invoices from this month. Help me organize them for my accountant"
Actions:
1. Collect: Invoice images or text data from user
2. Parse: Extract supplier, amount, VAT, date from each
3. Categorize: Assign Tax Authority category per Step 4
4. Validate: Check TIN format, VAT calculation, allocation numbers
5. Run `python scripts/categorize_invoices.py --input invoices.json --output categorized.json`
6. Export: Generate accountant-ready CSV with summary
Result: Organized expense report with VAT summary ready for accountant

### Example 2: VAT Extraction from a Receipt
User says: "I paid 5,850 NIS total to an Israeli hosting company (Osek Murshe) for server hosting. What is the VAT portion?"
Actions:
1. Confirm the supplier is Israeli VAT-registered. (A foreign provider such as AWS or Google carries NO Israeli VAT, in that case skip the 18/118 extraction and record the full amount with zero reclaimable VAT.)
2. Apply the 18/118 rule: VAT = 5,850 * (18 / 118) = 892.37 NIS
3. Net amount: 5,850 - 892.37 = 4,957.63 NIS
4. Categorize: Communications (code 8)
Result: VAT of 892.37 NIS extractable, net expense 4,957.63 NIS in Communications (8). Had the supplier been foreign, reclaimable VAT would be 0.

### Example 3: Osek Patur Invoice Handling
User says: "I got an invoice from a freelance designer, but there is no VAT line"
Actions:
1. Check: Is the supplier Osek Patur (עוסק פטור)?
2. If Osek Patur: No VAT to deduct, record full amount as expense
3. Categorize: Subcontractors (code 2) for freelance design work
4. Note: Request the supplier's TIN and verify their status
Result: Full amount recorded as expense with no VAT deduction, flagged for accountant

### Example 4: Mixed-Use Vehicle Expense
User says: "I got a fuel receipt for 2,340 NIS for a car I use for both work and personal trips"
Actions:
1. Extract VAT: 2,340 * 18 / 118 = 356.95 NIS (total VAT)
2. Apply the vehicle rule: only 2/3 of VAT is deductible on a non-commercial vehicle
3. Deductible VAT: 356.95 * 2/3 = 237.97 NIS
4. Non-deductible VAT: 356.95 * 1/3 = 118.98 NIS
5. Categorize: Vehicle expenses (code 9)
Result: Total VAT 356.95 NIS, but only 237.97 NIS is deductible. The remaining 118.98 NIS is a non-deductible expense.

## Bundled Resources

### Scripts
- `scripts/categorize_invoices.py` -- Categorizes Israeli invoices by Tax Authority expense codes (1–12), extracts VAT at 18%, validates business numbers (Luhn-like check digit), applies the vehicle 2/3 rule, and generates accountant-ready reports. Run: `python scripts/categorize_invoices.py --help`

### References
- `references/expense-categories.md` -- Complete list of Tax Authority expense categories (codes 1–12) with descriptions and common examples, plus special rules: vehicle 2/3 deduction, entertainment 80% income-tax cap, mixed-use proportional deductions, depreciation rates by asset type. Consult when categorizing unusual expenses.

## Gotchas
- Agents often calculate VAT as `amount * 0.18` when extracting from a total, but the correct formula to extract VAT from a VAT-inclusive amount is `total / 1.18 * 0.18` (or equivalently `total * 18/118`). This "1/6 rule" is specific to Israeli bookkeeping and the divisor changed from 117 to 118 when the rate moved to 18% in 2025.
- Osek Patur (exempt dealer) invoices have no VAT component. Agents may still try to extract VAT from these invoices, producing incorrect bookkeeping entries.
- Israeli invoice numbers are not globally unique. Different suppliers can have the same invoice number. Always index by supplier + invoice number combination.
- Hebrew OCR on scanned invoices frequently misreads the characters vav (ו) and zayin (ז), and confuses final-mem (ם) with samekh (ס). Verify extracted amounts and names.
- The SHAAM allocation-number threshold is staged (NIS 10,000 from 1 Jan 2026, dropping to NIS 5,000 from 1 Jun 2026, with further reductions planned for 2027). Apply the threshold that was in force on the invoice issue date, not today.
- The Ministry of Finance proposed a VAT rise to 19% for January 2026 during the 2026 budget talks. That proposal was rejected; the rate **remains 18%** through 2026. Do not pre-apply a 19% rate to invoices regardless of how confident the source looks.
- The Osek Patur turnover ceiling rose from NIS 120,000 to NIS 122,833 starting 2026. Agents that hardcode 120,000 will flag legitimate Osek Patur status as "over threshold" for revenues between 120,001 and 122,833.
- An invoice dated more than 14 days after the underlying supply or payment can be challenged by the Tax Authority. Flag suspiciously late invoices for the accountant.
- Input VAT can only be deducted in the invoice's VAT period or within 6 months after it (תקנה 23א). Flag invoices older than 6 months in the batch: their VAT is no longer freely reclaimable and needs VAT-office approval.
- A tax invoice must be issued in the name of the claiming business (על שם העוסק) to deduct input VAT. Reject invoices addressed to the owner personally, a spouse, or a different entity, this is the most common reason an accountant disallows an invoice.
- The vehicle 2/3 rule applies to running costs (fuel, maintenance, repairs). VAT on buying or importing a private (non-commercial) vehicle is fully non-deductible, even at 100% business use.
- Input VAT on business hospitality/entertainment (אירוח) is NOT deductible (תקנה 16, except hosting a guest from abroad). Do not reclaim VAT on restaurant/hosting invoices meant to entertain clients or employees; only genuine business inputs qualify.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Israel Tax Authority | https://www.gov.il/he/departments/israel_tax_authority | Current VAT rate (18%), e-invoice regulations, expense categories |
| SHAAM e-invoice portal | https://www.gov.il/he/service/digital-invoices-service | Allocation number threshold, how to verify a supplier's allocation |
| Invoice compliance rules | https://www.gov.il/he/pages/invoices-format | Required fields and formats for a tax invoice |
| Business lookup | https://www.gov.il/he/service/business-id-search | Verify a supplier's TIN and status (Osek Murshe / Osek Patur) |
| Expense deduction rules | https://www.gov.il/he/departments/guides/income-tax-allowed-expenses | Vehicle 2/3 rule, entertainment 80% rule, mixed-use deductions |

## Troubleshooting

### Error: "VAT amount doesn't match"
Cause: Rounding differences between line-item VAT and total VAT
Solution: Israeli invoices may have rounding differences of up to 1 NIS. Use the VAT amount printed on the invoice (not recalculated). If no VAT line exists, use the 18/118 rule from Step 3. Differences greater than 1 NIS usually indicate either the wrong rate (legacy 17%) or a real invoice error, contact the supplier for a corrected invoice.

### Error: "Cannot determine business type"
Cause: Invoice does not clearly state Osek Murshe or Osek Patur
Solution: Look for "עוסק מורשה" or "עוסק פטור" on the invoice. Check the TIN on the Tax Authority business lookup. If unclear, treat as Osek Patur (no VAT deduction) and flag for accountant review.

### Error: "Expense category unclear"
Cause: Invoice description is vague or multi-category
Solution: Use the primary purpose of the expense. When in doubt, assign to "Other expenses" (code 12) and let the accountant reclassify. Common confusion: software subscriptions belong in Communications (8), not Office expenses (11).

### Error: "Missing SHAAM allocation number on a B2B invoice"
Cause: A B2B tax invoice above the active threshold was issued without a SHAAM allocation number (מספר הקצאה)
Solution: Determine the threshold in force on the invoice issue date (NIS 20,000 in 2025; NIS 10,000 from 1 Jan 2026; NIS 5,000 from 1 Jun 2026). If the invoice is above the threshold and lacks an allocation number, it is not valid for VAT input deduction. Ask the supplier to reissue with an allocation number, or record the invoice without claiming the input VAT and flag for the accountant.
