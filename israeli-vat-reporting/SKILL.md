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
| Osek Patur (Exempt Dealer) | osek patur | < ~122,833 NIS | Annual summary only |
| Amuta (Non-profit) | amuta | Separate regime | Non-profits have a separate VAT regime, confirm with an accountant |
| Company (Ltd) | chevra | Any | Monthly or Bi-monthly (see the order below) |

Decide the frequency in this order (it is set by the Tax Authority, not by choice or legal form, so a company is not automatically monthly):
1. **Required to file the detailed report (PCN874)?** (see Step 4: turnover above NIS 500,000 or double-entry books, individuals from period 1/2026 unless granted the deferral to 1 January 2027) Then **monthly**: a dealer who becomes required to file the detailed report moves to monthly reporting under section 67A(a) of the VAT Law.
2. Otherwise, **monthly** if annual turnover is above NIS 1,775,000 (value as of 01.01.2026), and **bi-monthly** if below.

**Osek patur status is not decided by turnover alone.** Certain professions and activities must register as osek morsheh regardless of turnover under section 13 of the VAT (Registration) Regulations ([Nevo](https://www.nevo.co.il/law_html/law01/271_004.htm)). Confirm the business's status with an accountant before treating it as osek patur.

### Step 2: Collect Transaction Data
For the reporting period, gather:
- **Sales (output):** All invoices issued with VAT amounts
- **Purchases (input):** All purchase invoices with VAT amounts
- **Special transactions:** Exports (zero-rated), exempt services, fixed asset purchases

### Step 3: Calculate VAT Liability

```
Output VAT (mas asakot, מס עסקאות)    = Sum of VAT on all sales invoices
Input VAT (mas tsumot, מס תשומות)     = Sum of VAT on deductible purchase invoices
Net VAT                   = Output VAT - Input VAT

If Net > 0: Business owes the Tax Authority (payment due)
If Net < 0: The Tax Authority owes the business (refund claim)
```

**Input VAT deduction rules:**
- Buying or importing a private car: input VAT NOT deductible (VAT Regulations, reg. 14; exceptions such as driving schools and car rental)
- Mixed-use costs where the Director set no ratio: 2/3 deductible if use is mainly business, 1/4 if mainly private (reg. 18(b)). Car running costs such as fuel and upkeep are a common illustration, not a quoted rule: verify with your accountant which rule applies. If the Director set a ratio for the business, that ratio applies instead
- Entertainment: NOT deductible, except entertaining a person from abroad (reg. 16)

### Step 4: Fill the Periodic VAT Return Fields
The regular periodic VAT return (doch tkufati) is a summary report. Map the calculated values to its fields:
- Taxable sales (the net base, EXCLUDING VAT)
- Zero-rated sales (exports)
- Exempt sales
- Total output VAT
- Taxable purchases / inputs (the net base, EXCLUDING VAT; report equipment/fixed-asset inputs separately from other inputs on the real form)
- Input VAT claimed
- Net VAT
- Adjustments (if any)
- Amount to pay / refund

**Detailed report (PCN874 / doch mefurat) is a SEPARATE filing.** Do not confuse the summary return above with PCN874, the line-by-line structured file that businesses above the detailed-report threshold must submit IN ADDITION. The Tax Authority announced that from reporting period 9/2025 the obligation applies to every dealer with annual turnover above NIS 500,000, or who must keep double-entry books. For a dealer who is an individual (self-employed) it applies from period 1/2026 instead, and an individual for whom at least 90% of 2025 input-invoice value came from invoices of up to NIS 5,000 each (pre-VAT) may apply to the regional VAT office to defer it to 1 January 2027. The Tax Authority new-dealer guide page still shows an older NIS 5,000,000 figure; do not rely on it.

### Step 5: Validate and Submit
Before submission, verify:
1. All sales invoices accounted for (cross-reference with e-invoice allocation numbers)
2. Input VAT claims supported by valid tax invoices with allocation numbers (mispar haktzaa), required above a pre-VAT transaction threshold that steps down on a schedule: NIS 20,000 (2025), NIS 10,000 (from Jan 2026), NIS 5,000 (from 1 June 2026, in effect now). A valid allocation number is a condition for the buyer to deduct input VAT on an invoice above the threshold, so from 1 June 2026 it applies to invoices above NIS 5,000 pre-VAT. Always check the threshold in force on the invoice date
3. Correct reporting period selected
4. Deadline not passed (see below)

**Filing deadlines:**
- Manual filing: 15th of the month following the reporting period
- Online filing: 19th of the following month (by 6:30 PM), only for dealers NOT required to file the detailed report
- Detailed report filers: file and pay by the 23rd of the following month

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
Result: Complete VAT report ready for filing

### Example 2: Bi-monthly Report with Exports
User says: "I need to file my VAT for November-December, I had some exports"
Actions:
1. Determine: Bi-monthly reporter
2. Identify: Export sales are zero-rated (0% VAT, but still reported)
3. Calculate: Domestic output VAT - Input VAT = Net
4. Note: Exports are reported as zero-rated sales, no VAT but supports input VAT recovery
Result: VAT report with zero-rated export handling

## Bundled Resources

### Scripts
- `scripts/calculate_vat.py`, Computes net VAT liability from sales (output) and purchase (input) records, applies Israeli deduction rules for non-deductible and partially deductible expenses, and maps results to the periodic VAT return fields. Run: `python scripts/calculate_vat.py --help`

### References
- `references/vat-regulations.md`, Summary of Israeli VAT law including current and historical VAT rates, registration types (Osek Morsheh, Osek Patur), and filing obligations. Consult when verifying VAT rate or registration rules.
- `references/reporting-calendar.md`, Filing deadlines for monthly and bi-monthly VAT reporters, including the 15th (manual), 19th (online, non-detailed filers) and 23rd (detailed-report filers) deadline rules. Consult when determining reporting period and deadline for a specific month.
- `references/special-cases.md`, Zero-rated and exempt transactions, and the distinction between zero-rated and exempt for input VAT recovery. Consult when handling exports or unusual transaction types.

## Gotchas
- Agents frequently use the old 17% VAT rate. The current Israeli VAT rate is **18%** (effective January 1, 2025). This single error cascades through all calculations. Always verify the rate before computing.
- Israeli VAT reports are filed monthly or bi-monthly, never quarterly as in many European countries. Agents also default small businesses to bi-monthly, although any dealer required to file the detailed report reports monthly (see Step 1).
- Osek Patur businesses (annual revenue approximately 122,833 NIS, subject to annual updates) do not charge or report VAT. Agents may generate VAT reports for businesses that should not be filing them, or treat a low-turnover business as osek patur even though certain professions and activities must register as osek morsheh regardless of turnover (see Step 1).
- Agents conflate the two vehicle rules. Input VAT on BUYING a private car is not deductible (reg. 14); the 2/3 share is for mixed-use costs when use is mainly business (1/4 if mainly private, reg. 18(b)). Claiming 2/3 on the purchase price is wrong.
- Input VAT deduction requires a valid allocation number (mispar haktzaa) on invoices above the threshold (NIS 5,000 pre-VAT from 1 June 2026, currently in force; it stepped down from NIS 10,000 in January 2026). Agents may ignore this requirement, leading to rejected deductions.

## Troubleshooting

### Error: "Reporting period mismatch"
Cause: Submitting for wrong period (e.g., single month when registered as bi-monthly)
Solution: Check business registration. Bi-monthly periods: Jan-Feb, Mar-Apr, May-Jun, Jul-Aug, Sep-Oct, Nov-Dec.

### Error: "Input VAT not deductible"
Cause: Claiming VAT from non-deductible expenses (entertainment, non-business)
Solution: Review deduction rules in Step 3. Only business expenses with valid tax invoices qualify.

### Error: "Late filing penalty"
Cause: Filing after the deadline of the following month (15th manual, 19th online for non-detailed filers, 23rd for detailed-report filers)
Solution: File immediately. Late filing triggers late-payment fines, a debt fine, and linkage differentials and interest, and may also draw an administrative fine. Verify the current-year amounts with the Tax Authority.