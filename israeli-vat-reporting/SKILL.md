---
name: israeli-vat-reporting
description: Prepare, validate, and guide submission of Israeli VAT reports (Doch Maam) per Tax Authority standards. Use when user asks about VAT reporting, VAT calculation, "doch maam", "maam", Israeli VAT filing, VAT deadlines, or input/output VAT reconciliation. Supports monthly, bi-monthly, and annual reporting. Handles zero-rated exports and exempt transactions. Do NOT use for income tax, corporate tax, non-Israeli VAT systems, or bookkeeping statements such as profit and loss, balance sheet or trial balance (use israeli-financial-reports).
license: MIT
compatibility: Works with Claude Code, Claude.ai, Cursor.
---

# Israeli VAT Reporting

## Legal notice

This is a free information tool operated by an AI model. It explains the tax rules and helps you organise your own figures. All of its outputs are produced automatically by an AI model, with no involvement, review, or approval by a tax adviser or accountant. The output is not a tax opinion, not a return prepared by a licensed representative, and not professional advice, but a general calculation and explanation only: it does not examine the full extent of your income or your complete documents. An AI model may err, omit data, or present a wrong conclusion.

Any form or text this tool produces is an automatic draft for your personal preparation only, and is not a filed return. Responsibility for reporting and for paying the tax is yours, the binding computation is the Tax Authority's, and representation before the Tax Authority is reserved to those permitted by law. This tool is not a substitute for advice that takes account of the particular circumstances and needs of each person. Consult a tax adviser or accountant before filing or paying. All use of its output is the user's sole responsibility.


## Instructions

### Step 1: Determine Business Type and Reporting Frequency
Ask the user about their business registration:

| Type | Hebrew | Annual Turnover | Reporting Period |
|------|--------|----------------|-----------------|
| Osek Morsheh (Licensed Dealer) | osek morsheh | > 122,833 NIS, or any turnover for a section 13 group (see below) | Monthly or Bi-monthly |
| Osek Patur (Exempt Dealer) | osek patur | Up to 122,833 NIS (2026) | Annual summary only |
| Amuta (Non-profit) | amuta | Separate regime | Non-profits have a separate VAT regime, confirm with an accountant |
| Company (Ltd) | chevra | Any | Monthly or Bi-monthly (see the order below) |

Decide the frequency in this order (it is set by the Tax Authority, not by choice or legal form, so a company is not automatically monthly):
1. **Required to file the detailed report (PCN874)?** (see Step 4: turnover above NIS 500,000 or double-entry books, individuals from period 1/2026 unless granted the deferral to 1 January 2027) Then **monthly**: a dealer who becomes required to file the detailed report moves to monthly reporting under section 67A(a) of the VAT Law.
2. Otherwise, **monthly** if turnover in the determining year (the 12 months ending 31 August of the previous year, reg. 20) is above the threshold, and **bi-monthly** if it is not. The threshold is NIS 1,775,000 for 2026, and from 1 January 2027 it is NIS 1,805,000, so frequency for 2027 is set by turnover from 1.9.2025 to 31.8.2026. It is re-indexed every 1 September (VAT Law s.126(d)).

The osek patur ceiling (NIS 122,833 for 2026) is indexed every 1 January to the CPI published for 15 December (s.126(a)), so the 2027 figure does not exist before mid-December 2026. Do not guess it.

**Osek patur status is not decided by turnover alone.** Certain professions and activities must register as osek morsheh regardless of turnover under section 13 of the VAT (Registration) Regulations ([Nevo](https://www.nevo.co.il/law_html/law01/271_004.htm)). Confirm the business's status with an accountant before treating it as osek patur.

### Step 2: Collect Transaction Data
First fix the period. If the user asks for one month but reports bi-monthly, the return covers the two-month period (January-February, March-April and so on, reg. 20), so ask for both months' documents.

For that period, gather:
- **Sales (output):** transactions whose invoicing date fell in the period, plus every tax invoice actually issued in it even if early, and nothing already reported (VAT Law s.69(a)). For services the tax arises when payment is received, on the amount received (s.24), so an unpaid transaction invoice (heshbon iska) for a service is not yet output, and a payment received this period on an earlier demand is output of this period
- **Purchases (input):** tax invoices issued to the business before the period ended (s.69(c)). Check each one: addressed to this business and its VAT number, issued by an osek morsheh, a tax invoice and not a receipt, transaction invoice or proforma, and showing Israeli VAT. A receipt from an osek patur, an invoice from a foreign supplier and an exempt or zero-rated purchase carry no Israeli VAT to deduct (services from a foreign supplier: route to an accountant)
- **Credit notes:** a credit note you RECEIVE reduces input VAT in the period it was received (reg. 24(b)); output VAT on an invoice you issued stays due until the invoice is cancelled or corrected as prescribed (s.49)
- **Special transactions:** exports (zero-rated), exempt services, fixed asset purchases

### Step 3: Calculate VAT Liability

```
Output VAT (mas asakot, מס עסקאות)    = Sum of VAT on all sales invoices
Input VAT (mas tsumot, מס תשומות)     = Sum of VAT on deductible purchase invoices
Net VAT                   = Output VAT - Input VAT

If Net > 0: Business owes the Tax Authority (payment due)
If Net < 0: The Tax Authority owes the business (refund claim)
```

**Input VAT deduction rules:**
- Only a tax invoice issued to the business (or an import declaration) supports a deduction, not a receipt or a transaction invoice (heshbon iska), and it must be deducted within six months of the document date (VAT Law s.38(a))
- Buying or importing a private car: input VAT NOT deductible (VAT Regulations, reg. 14; exceptions such as driving schools and car rental). "Private car" here also covers a dual-use car and a commercial vehicle with a permitted total weight of up to 3,500 kg (reg. 1), so ask the vehicle type and weight before deducting VAT on a van or pickup
- Mixed-use costs where the business share can be determined (for example an itemised phone line): deduct that share (reg. 18(a))
- Mixed-use costs where the share cannot be determined and the Director set no ratio: 2/3 deductible if use is mainly business, 1/4 if mainly private (reg. 18(b)). Car running costs such as fuel and upkeep are a common illustration, not a quoted rule: verify with your accountant which rule applies. If the Director set a ratio for the business, that ratio applies instead
- Entertainment: NOT deductible, except entertaining a person from abroad (reg. 16)
- Inputs used for exempt transactions: NOT deductible (s.41). When the business has both taxable and exempt sales, the apportionment belongs with an accountant
- Benefits for employees, owners or managers (meals, housing, gifts, entertainment): NOT deductible unless sold or supplied to them and reported as a taxable transaction (reg. 15A)
- Buying or building the dealer's own home, even when it is also the place of business: NOT deductible (reg. 15)

### Step 4: Fill the Periodic VAT Return Fields
The regular periodic VAT return (doch tkufati) is a summary report. Map the calculated values to its fields:
- Taxable sales (the net base, EXCLUDING VAT)
- Zero-rated sales (exports)
- Exempt sales
- Total output VAT
- Input VAT on equipment and fixed assets, and input VAT on other inputs, as separate figures
- Total input VAT claimed
- Net VAT
- Adjustments (if any)
- Amount to pay / refund

**Detailed report (PCN874 / doch mefurat) is a SEPARATE filing.** Do not confuse the summary return above with PCN874, the line-by-line structured file that businesses above the detailed-report threshold must submit IN ADDITION. The Tax Authority announced that from reporting period 9/2025 the obligation applies to every dealer with annual turnover above NIS 500,000, or who must keep double-entry books. For a dealer who is an individual (self-employed) it applies from period 1/2026 instead, and an individual for whom at least 90% of 2025 input-invoice value came from invoices of up to NIS 5,000 each (pre-VAT) may apply to the regional VAT office to defer it to 1 January 2027. The statute sets the NIS 500,000 test (VAT Law s.69A(g)(1)); if a page or summary shows another figure, follow the statute.

### Step 5: Validate and Submit
Before submission, verify:
1. All sales invoices accounted for (cross-reference with e-invoice allocation numbers)
2. Input VAT claims supported by valid tax invoices with allocation numbers (mispar haktzaa) above the pre-VAT threshold in force on the invoice date: NIS 25,000 (from 5 May 2024), NIS 20,000 (2025), NIS 10,000 (from 1 January 2026), NIS 5,000 (from 1 June 2026, in force now). The threshold is measured on the WHOLE invoice before VAT, not per line or per deductible part. VAT Law s.38(a1) bars the buyer from deducting input VAT on an invoice above NIS 5,000 that has no allocated number, whoever is at fault; the only statutory relief is the Director's order after a Tax Authority system failure (s.40B). The issuer requests the number (on the buyer's demand above the threshold) and prints it on the invoice. The full number is long (the official examples are 26 digits), and the printed short form is its rightmost 9 digits. An invoice made up only of zero-rated or exempt transactions gets no number and needs none. An "allocation approval" (ishur haktzaa) printed on a proforma or transaction invoice is not an allocation number and does not support a deduction. No further step-down after NIS 5,000 is scheduled
3. Every input invoice is within six months of its date (s.38(a)); an older one needs an extension from the Director
4. Correct reporting period selected
5. Deadline not passed (see below). A return is due even for a period with no activity, unless the business ceased and the Director was notified (s.67(b))

**Filing deadlines:**
- Manual filing: 15th of the month following the reporting period
- Online filing: 19th of the following month (by 6:30 PM), only for dealers NOT required to file the detailed report
- Detailed report filers: file and pay by the 23rd of the following month
- Rest days: if at least three rest days (Shabbat, holidays, chol hamoed) fall in the five days before the deadline, it moves to the fourth working day after them (s.67(b1), s.67A(e)). The Tax Authority publishes the actual dates for each period every year; check that calendar. The Director also moves a 15th, 16th or 23rd that falls on a Friday, Saturday or Sunday to the next business day, usually Monday: the manual-filing date for the October 2026 return is 16 November 2026 (15 November is a Sunday), and the detailed-report date is 23 November 2026

**Where to file:** the Tax Authority website (https://www.misim.gov.il now leads to the Tax Authority page on gov.il).

## Examples

### Example 1: Monthly VAT Report
User says: "Help me prepare my VAT report for January 2026"
Actions:
1. Determine: Monthly reporter (required to file the detailed report, or turnover > NIS 1,775,000)
2. Collect: January sales and purchase invoices
3. Calculate: Output VAT 34,000 - Input VAT 22,000 = Net 12,000 NIS owed
4. Prepare: the periodic VAT return with all fields mapped
5. Guide: If the business is required to file the detailed report (confirm it has not been granted the deferral to 2027), file and pay by February 23rd; otherwise the 19th online date (or the 15th manually) applies
Result: Draft calculation of the periodic return for you to review before filing

### Example 2: Bi-monthly Report with Exports
User says: "I need to file my VAT for November-December, I had some exports"
Actions:
1. Determine: Bi-monthly reporter
2. Identify: Export sales are zero-rated (0% VAT, but still reported)
3. Calculate: Domestic output VAT - Input VAT = Net
4. Note: Exports are reported as zero-rated sales, no VAT but supports input VAT recovery. Confirm the conditions first: goods need an export declaration and release (s.30(a)(1)); a service to a foreign resident is zero-rated only if it is not actually given in Israel to an Israeli resident as well, and not in a category the Minister excluded (s.30(a)(5)). If in doubt, route to an accountant
Result: VAT report with zero-rated export handling

## Bundled Resources

### Scripts
- `scripts/calculate_vat.py`, Computes net VAT liability from sales (output) and purchase (input) records, applies Israeli deduction rules for non-deductible and partially deductible expenses, and maps results to the periodic VAT return fields. Amounts are pre-VAT by default; `--inclusive` (or `"vat_included": true` on a record) splits a VAT-inclusive gross back into base and VAT (base = gross / 1.18). Give the VAT printed on the invoice as `vat` when you have it, and `"vat_type": "none"` for a document with no Israeli VAT. Lines of one invoice share `supplier`, `invoice` (the supplier's invoice number) and `date`, so the allocation threshold is tested on the whole invoice and one allocation number on any line covers it. A record that totals several documents takes `"aggregate": true` (the `--purchases` total is one), which skips the per-invoice checks with a warning; use it only for a sum of several documents, never for one invoice. An input above the threshold for its date with no `allocation_number` is HELD and not deducted, as is an undated one above NIS 5,000 and one dated after the period; inputs older than six months and credit notes on a held invoice are flagged. `actual_business_share` with `business_ratio` applies reg. 18(a). Rounding is half up, and every box is also shown in whole shekels. Run: `python scripts/calculate_vat.py --help`

### References
- `references/vat-regulations.md`, Summary of Israeli VAT law including current and historical VAT rates, registration types (Osek Morsheh, Osek Patur), and filing obligations. Consult when verifying VAT rate or registration rules.
- `references/reporting-calendar.md`, Filing deadlines for monthly and bi-monthly VAT reporters, including the 15th (manual), 19th (online, non-detailed filers) and 23rd (detailed-report filers) deadline rules. Consult when determining reporting period and deadline for a specific month.
- `references/special-cases.md`, Zero-rated and exempt transactions, and the distinction between zero-rated and exempt for input VAT recovery. Consult when handling exports or unusual transaction types.

## Gotchas
- Agents frequently use the old 17% VAT rate. The current Israeli VAT rate is **18%** (effective January 1, 2025). This single error cascades through all calculations. Always verify the rate before computing.
- Israeli VAT reports are filed monthly or bi-monthly, never quarterly as in many European countries. Agents also default small businesses to bi-monthly, although any dealer required to file the detailed report reports monthly (see Step 1).
- Osek Patur businesses (annual revenue approximately 122,833 NIS, subject to annual updates) do not charge or report VAT. Agents may generate VAT reports for businesses that should not be filing them, or treat a low-turnover business as osek patur even though certain professions and activities must register as osek morsheh regardless of turnover (see Step 1).
- Agents conflate the two vehicle rules. Input VAT on BUYING a private car is not deductible (reg. 14); the 2/3 share is for mixed-use costs when use is mainly business (1/4 if mainly private, reg. 18(b)). Claiming 2/3 on the purchase price is wrong.
- Input VAT deduction requires a valid allocation number (mispar haktzaa) on invoices above the threshold (NIS 5,000 pre-VAT from 1 June 2026, currently in force; it was NIS 10,000 from 1 January to 31 May 2026). Agents may ignore this requirement, leading to rejected deductions. Agents also quote the ORIGINAL schedule (NIS 15,000 in 2026, 10,000 in 2027, 5,000 in 2028), which the accelerated schedule replaced and which some Tax Authority documents still print. Do not use it.
- Agents treat a VAT-inclusive total as the net base and add 18% on top. When the user's figures include VAT, the base is gross / 1.18 and the VAT is gross minus base (NIS 11,800 gross is NIS 10,000 plus NIS 1,800 VAT).

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| VAT Law (Nevo) | https://www.nevo.co.il/law_html/law01/271_001.htm | s.38 input VAT and allocation number, s.67 and s.67A periods and deadlines, s.126 indexation |
| VAT Regulations (Nevo) | https://www.nevo.co.il/law_html/law01/271_005.htm | Regs. 14, 15, 15A, 16, 18 deduction limits, reg. 20 determining year |
| Kol Zchut, periodic VAT returns | https://www.kolzchut.org.il/he/%D7%94%D7%92%D7%A9%D7%AA_%D7%93%D7%95%22%D7%97%D7%95%D7%AA_%D7%AA%D7%A7%D7%95%D7%A4%D7%AA%D7%99%D7%99%D7%9D_%D7%95%D7%AA%D7%A9%D7%9C%D7%95%D7%9D_%D7%9E%D7%A1_%D7%A2%D7%A8%D7%9A_%D7%9E%D7%95%D7%A1%D7%A3 | Monthly or bi-monthly threshold, 15th / 19th deadlines |
| Kol Zchut, osek patur | https://www.kolzchut.org.il/he/%D7%A2%D7%95%D7%A1%D7%A7_%D7%A4%D7%98%D7%95%D7%A8 | Ceiling for the current year, 31 January declaration |
| Tax Authority directive 01/2025 (allocation numbers) | https://www.gov.il/BlobFolder/policy/inst-071225-1/he/vat_inst-071225-1.pdf | Threshold schedule by invoice date |
| Tax Authority Israel Invoices API spec | https://www.gov.il/BlobFolder/generalpage/hor-software-other/he/vat_software-houses-180724.pdf | Allocation number format and the 9-digit short form |

## Troubleshooting

### Error: "Reporting period mismatch"
Cause: Submitting for wrong period (e.g., single month when registered as bi-monthly)
Solution: Check business registration. Bi-monthly periods: Jan-Feb, Mar-Apr, May-Jun, Jul-Aug, Sep-Oct, Nov-Dec.

### Error: "Input VAT not deductible"
Cause: Claiming VAT from non-deductible expenses (entertainment, non-business)
Solution: Review deduction rules in Step 3. Only business expenses with valid tax invoices qualify.

### Error: "Late filing penalty"
Cause: Filing after the deadline of the following month (15th manual, 19th online for non-detailed filers, 23rd for detailed-report filers)
Solution: File immediately. Filing late carries a fixed fine for every two weeks or part of them (VAT Law s.94); paying late adds a weekly percentage of the unpaid tax plus linkage differentials and interest (s.96, s.97); an administrative fine may also be imposed. Verify the current amounts with the Tax Authority.