---
name: il-invoice-organizer
description: "Parse and organize Hebrew invoices for Israeli bookkeeping: VAT 1/6 extraction, Tax Authority expense categories, Osek Murshe/Patur recognition, and accountant-ready export. Use when user asks about organizing invoices, cheshbonit, expense categorization, sivug hotza'ot, VAT extraction from totals, Osek Murshe vs Osek Patur rules, or preparing documents for their accountant (ro'eh cheshbon). Supports Hebrew OCR text parsing and automatic categorization per Tax Authority standards. Do NOT use for invoice generation (use israeli-e-invoice instead) or for VAT report filing (use israeli-vat-reporting instead)."
license: MIT
compatibility: "Works with Claude Code, Cursor, GitHub Copilot, Windsurf, OpenCode, Codex. Python 3.8+ for helper scripts."
---

# IL Invoice Organizer

## Legal notice

This is a free information tool operated by an AI model. It explains the tax rules and helps you organise your own figures. All of its outputs are produced automatically by an AI model, with no involvement, review, or approval by a tax adviser or accountant. The output is not a tax opinion, not a return prepared by a licensed representative, and not professional advice, but a general calculation and explanation only: it does not examine the full extent of your income or your complete documents. An AI model may err, omit data, or present a wrong conclusion.

Any form or text this tool produces is an automatic draft for your personal preparation only, and is not a filed return. Responsibility for reporting and for paying the tax is yours, the binding computation is the Tax Authority's, and representation before the Tax Authority is reserved to those permitted by law. This tool is not a substitute for advice that takes account of the particular circumstances and needs of each person. Consult a tax adviser or accountant before filing or paying. All use of its output is the user's sole responsibility.


## Instructions

### Step 1: Identify Invoice Type and Source
Determine what documents the user has:

| Document Type | Hebrew | VAT Reclaimable | Categorization |
|---------------|--------|----------------|----------------|
| Tax Invoice | חשבונית מס | Yes, extract VAT | Full categorization |
| Tax Invoice/Receipt | חשבונית מס/קבלה | Yes, extract VAT | Full categorization |
| **Transaction invoice** | **חשבונית עסקה** | **No, it is NOT a tax document** | **Reference only, chase the חשבונית מס** |
| Receipt only | קבלה | No VAT to reclaim | Payment record only |
| Credit Invoice | חשבונית זיכוי | Yes, NEGATIVE VAT | Reverse the original category |
| Proforma | חשבונית פרופורמה | No, not a tax document | For reference only |

Key: only a חשבונית מס or חשבונית מס/קבלה allows input-VAT deduction.

**The חשבונית עסקה is the trap in a pile of paperwork.** It looks like an invoice, is often headed "חשבונית", and carries a VAT line, but it is a demand for payment rather than a tax document. Its VAT is not deductible and it must not be entered as an input. If the supplier is on a cash basis they issue it BEFORE payment and the חשבונית מס follows once they are paid, so the fix is to chase the real document rather than to book this one. Sort every "חשבונית" in the pile on this distinction before doing anything else.

A **חשבונית זיכוי** reverses an earlier invoice, so carry it as a NEGATIVE amount. Entering it as a positive inflates the reclaim by twice its VAT.

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
| 5 May 2024 to 31 Dec 2024 | NIS 25,000 |
| 2025 (full year) | NIS 20,000 |
| 1 Jan 2026 to 31 May 2026 | NIS 10,000 |
| From 1 Jun 2026 | NIS 5,000 |

NIS 5,000 is the terminal step. **Nothing below 5,000 is legislated or announced**, so do not tell a user a further cut is coming, and do not state a schedule the Tax Authority page does not carry.

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
Assign each expense to a working bookkeeping category. **The 1-12 numbering below is this skill's own convention, not a Tax Authority code list**, so do not tell an accountant an expense is "code 4" and expect to be understood. Use the category NAME when you talk to them. These 12 categories map onto the Tax Authority income-statement structure (the דוח רווח והפסד / form 6111 groupings), with `references/expense-categories.md`, and with the keyword-based auto-categorizer in `scripts/categorize_invoices.py`:

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
| Osek Murshe | עוסק מורשה | Charges VAT, can deduct input VAT | חשבונית מס or חשבונית מס/קבלה |
| Osek Patur | עוסק פטור | No VAT charged (under threshold) | קבלה only, may not issue a חשבונית מס |
| Hevra Peratit (HP) | חברה פרטית (ח"פ) | Usually charges VAT; a 51 or 52 prefix SUGGESTS a company but does not establish it, and other ranges exist | Tax Invoice |
| Amuta (Non-profit) | עמותה | Usually no VAT, TIN starts 58 | Receipt |
| Malkar (Non-profit) | מלכ"ר | No VAT | Receipt |

Important: You can only deduct input VAT (mas tsumos) from tax invoices issued by Osek Murshe (or Hevra Peratit) suppliers. Receipts from Osek Patur do not have VAT to deduct.

**Osek Patur turnover ceiling (2026): NIS 122,833** (raised from NIS 120,000 in 2024 and 2025). Once a freelancer crosses this annual turnover, they must convert to Osek Murshe from the date of the breach and notify the VAT office. Certain professions (lawyers, doctors, architects, engineers, accountants and a few others) are barred from Osek Patur status regardless of turnover.

**Invoice issuance timing**: section 46(א) requires a tax invoice (Heshbonit Mas) within 14 days of מועד החיוב במס, the charge event, NOT within 14 days of delivery. The charge event is set by sections 22 to 29: for a SERVICE it is receipt of payment, so a cash-basis freelancer who has not been paid is not late. For goods it is delivery, unless the dealer is on the cash basis. "Supply or payment, whichever comes first" is a rough paraphrase that lands near the right answer in most cases but is not the rule. Invoices dated more than 14 days after the charge event may be challenged by the Tax Authority.

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
| VAT return (Doch Tkufati) | Bi-monthly | Annual turnover ≤ NIS 1,775,000 | 15th of the month after the period (online filers get an extension, confirm the current date) |
| VAT return | Monthly | Annual turnover > NIS 1,775,000 | 15th of the next month (same online extension) |
| Detailed VAT report (Doch Meforat) | Per VAT period | Annual turnover > NIS 500,000, OR required to keep double-entry books regardless of turnover | With the periodic VAT return |
| Income tax annual return (Doch Shnati) | Annual | All self-employed | 30 April (paper) / 31 May (online); via מייצג can extend to November or December |
| Bituach Leumi advances | Monthly | All self-employed | 15th of next month |

Hand the categorized batch to the accountant at least 7-10 days before the VAT deadline so they have time to reconcile and file. For invoices over the SHAAM threshold without an allocation number, flag urgently: the deadline to request a corrected invoice from the supplier is before that period's VAT filing.

**Osek Zair (Small Dealer) option**: a self-employed individual with annual revenue ≤ NIS 122,833 may elect the "Small Dealer" track on the annual return and deduct a **flat 30% of revenue as expenses** instead of actual expenses. The election is **not available** (section 87ה(א)) if the freelancer employs workers, does not keep admissible books, has business income not from personal exertion (יגיעה אישית), received part of the income from someone who is their employer in the tax year, had income attributed from a תאגיד שקוף under section 64(א), is a controlling shareholder as defined in section 32(9) (NOT the 10% substantial-shareholder test), or received more than 25% of the income from a קרוב as defined in section 88 or from someone who was their employer at any time in the previous three tax years (NOT "a related party" generally). Further Finance Minister conditions may also apply. Under 87ה(ב), skipping the election in a year with business income bars it for the following TWO tax years as well. When this election is in play, this skill should still organize invoices for backup and Bituach Leumi purposes, but the categorized totals will not flow to the income tax return.

## Examples

### Example 1: Monthly Invoice Organization
User says: "I have 30 invoices from this month. Help me organize them for my accountant"
Actions:
1. Collect: Invoice images or text data from user
2. Parse: Extract supplier, amount, VAT, date from each
3. Categorize: assign a working category per Step 4
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
2. **Ask which use predominates before computing anything.** "Both work and personal" does not answer the Regulation 18 question, and the two answers differ by a factor of 2.7. Ask: has the Director set a proportion for this vehicle, and if not, is the MAIN use business or private?
3. If the main use is business (Reg 18(ב)(2)): deductible 356.95 * 2/3 = 237.97 NIS, non-deductible 118.98 NIS.
4. If the main use is private (Reg 18(ב)(3)): deductible 356.95 * 1/4 = 89.24 NIS, non-deductible 267.71 NIS.
5. If the Director has set a proportion, that determination governs both of the above.
6. Categorize: Vehicle expenses (code 9)
Result: state which limb you applied and why. If the user cannot say which use predominates, take the 1/4 limb and tell them the answer is provisional, because over-deducting is the error the Tax Authority reverses. The bundled script does exactly this: it applies 1/4 and says the main use was not stated.

## Bundled Resources

### Scripts
- `scripts/categorize_invoices.py` -- Categorizes Israeli invoices into the 12 working categories, extracts VAT at the rate in force on the invoice date (18% from 2025, 17% before), validates business numbers by check digit, applies the Regulation 18 vehicle ladder, flags missing allocation numbers against the issue-date threshold, zeroes VAT on foreign-supplier and non-VAT documents, and carries credit invoices as negatives. Flags: `--input/-i` (required), `--output/-o`, `--report/-r`, `--validate/-v` (exits 1 on issues), `--format json|text`. Per-invoice fields it reads beyond the obvious: `foreign_supplier`, `mainly_business_use`, `director_determined_business_share`, `allocation_number`, `invoice_type`. Run `--help` for the full list.

### References
- `references/expense-categories.md` -- The 12 working expense categories (this skill's own numbering, not an ITA code list) with descriptions and common examples, plus the special rules: the Regulation 18 vehicle ladder, the כיבוד קל 80% income-tax cap, mixed-use apportionment, retention periods, and depreciation rates. Consult when categorizing an unusual expense.

## Gotchas
- Agents often calculate VAT as `amount * 0.18` when extracting from a total, but the correct formula to extract VAT from a VAT-inclusive amount is `total / 1.18 * 0.18` (or equivalently `total * 18/118`). This "1/6 rule" is specific to Israeli bookkeeping and the divisor changed from 117 to 118 when the rate moved to 18% in 2025.
- Osek Patur (exempt dealer) invoices have no VAT component. Agents may still try to extract VAT from these invoices, producing incorrect bookkeeping entries.
- Israeli invoice numbers are not globally unique. Different suppliers can have the same invoice number. Always index by supplier + invoice number combination.
- Hebrew OCR on scanned invoices frequently misreads the characters vav (ו) and zayin (ז), and confuses final-mem (ם) with samekh (ס). Verify extracted amounts and names.
- The allocation-number threshold is staged (NIS 25,000 from 5 May 2024, NIS 20,000 in 2025, NIS 10,000 from 1 Jan 2026, NIS 5,000 from 1 Jun 2026). Apply the threshold in force on the invoice ISSUE date, not today's. An invoice from March 2026 is tested against 10,000, not 5,000. There is no announced step below 5,000, so do not invent one.
- The Ministry of Finance proposed a VAT rise to 19% for January 2026 during the 2026 budget talks. That proposal was rejected; the rate **remains 18%** through 2026. Do not pre-apply a 19% rate to invoices regardless of how confident the source looks.
- The Osek Patur turnover ceiling rose from NIS 120,000 to NIS 122,833 starting 2026. Agents that hardcode 120,000 will flag legitimate Osek Patur status as "over threshold" for revenues between 120,001 and 122,833.
- An invoice dated more than 14 days after the CHARGE EVENT (מועד החיוב במס, which for a service is receipt of payment) can be challenged by the Tax Authority. Do not measure the 14 days from delivery, and see Step 5 before telling a cash-basis freelancer they are late. Flag genuinely late invoices for the accountant.
- Input VAT can only be deducted in the invoice's VAT period or within 6 months after it (section 38(א) of the VAT Law, not תקנה 23א, which is an unrelated extra return for Gaza and Jericho transactions).​ Flag invoices older than 6 months in the batch: their VAT is no longer freely reclaimable and needs VAT-office approval.
- A tax invoice must be issued in the name of the claiming business (על שם העוסק) to deduct input VAT. Reject invoices addressed to the owner personally, a spouse, or a different entity, this is the most common reason an accountant disallows an invoice.
- The vehicle 2/3 rule applies to running costs (fuel, maintenance, repairs) under Regulation 18, and it is a DEFAULT, not a flat rate. Where the Director has set the proportional non-business use, that determination governs. Where he has not: if the MAIN use is for business the dealer may deduct two thirds; if the main use is NOT for business the dealer may deduct only a QUARTER. Applying 2/3 to a mainly-private vehicle over-deducts. VAT on buying or importing a private (non-commercial) vehicle is fully non-deductible under Regulation 14(a), even at 100% business use.
- Input VAT on business hospitality/entertainment (אירוח) is NOT deductible (תקנה 16, except hosting a guest from abroad). Do not reclaim VAT on restaurant/hosting invoices meant to entertain clients or employees; only genuine business inputs qualify.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Israel Tax Authority | https://www.gov.il/he/departments/israel_tax_authority | Current VAT rate (18%), e-invoice regulations |
| Israel Invoice (חשבונית ישראל) | https://www.gov.il/he/departments/topics/israel-invoice | The allocation-number threshold ladder and its effective dates, stated verbatim |
| Request an allocation number | https://www.gov.il/he/service/request-assignment-number-for-tax-invoice | How a supplier obtains a number, and the current threshold |
| Verify a supplier's invoice | https://www.gov.il/he/service/verify-vendor-invoice-information | Check a supplier's invoice against its allocation number |
| Vehicle input-tax guide | https://www.gov.il/he/pages/instructions-for-deduction-of-input-tax-for-vehicles-and-motorcycles | The vehicle rules under Regulations 14 and 18, including mixed use |

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
Solution: Determine the threshold in force on the invoice issue date (NIS 25,000 from 5 May 2024; NIS 20,000 in 2025; NIS 10,000 from 1 Jan 2026; NIS 5,000 from 1 Jun 2026). If the invoice is above the threshold and lacks an allocation number, the invoice is still a valid document, but its input VAT is not deductible by the buyer until the number is supplied. Ask the supplier to reissue with an allocation number, or record the invoice without claiming the input VAT and flag for the accountant.
