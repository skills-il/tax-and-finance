---
name: israeli-vat-reporting
description: Prepare, validate, and guide submission of Israeli VAT reports (Doch Maam) per Tax Authority standards. Use when user asks about VAT reporting, VAT calculation, "doch maam", "maam", Israeli VAT filing, VAT deadlines, or input/output VAT reconciliation. Supports monthly, bi-monthly, and annual reporting. Handles zero-rated exports, exempt transactions, and Eilat zone rules. Do NOT use for income tax, corporate tax, or non-Israeli VAT systems.
license: MIT
compatibility: Works with Claude Code, Claude.ai, Cursor. Network access optional for SHAAM API.
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
| Osek Morsheh (Licensed Dealer) | osek morsheh | > 122,833 NIS | Monthly or Bi-monthly |
| Osek Patur (Exempt Dealer) | osek patur | < ~122,833 NIS | Annual summary only |
| Amuta (Non-profit) | amuta | Any | Monthly or Bi-monthly |
| Company (Ltd) | chevra | Any | Monthly |

Monthly reporting: Annual turnover > NIS 1,775,000 (threshold set in the VAT Regulations and indexed annually; value as of 01.01.2026)
Bi-monthly reporting: Annual turnover < NIS 1,775,000

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

If Net > 0: Business owes SHAAM (payment due)
If Net < 0: SHAAM owes business (refund claim)
```

**Input VAT deduction rules:**
- Only from valid tax invoices (hashbonit mas) with seller's TIN
- Vehicle expenses: 2/3 deductible (1/3 non-deductible for private use)
- Entertainment: NOT deductible
- Mixed business/personal: Proportional deduction only

### Step 4: Fill the Periodic VAT Return Fields
The regular periodic VAT return (doch tkufati) is a summary report. Map the calculated values to its fields:
- Field 1: Taxable sales (the net base, EXCLUDING VAT; the VAT on them goes in Field 4)
- Field 2: Zero-rated sales (exports)
- Field 3: Exempt sales
- Field 4: Total output VAT
- Field 5: Taxable purchases / inputs (the net base, EXCLUDING VAT; report equipment/fixed-asset inputs separately from other inputs on the real form)
- Field 6: Input VAT claimed
- Field 7: Net VAT (Field 4 - Field 6)
- Field 8: Adjustments (if any)
- Field 9: Amount to pay / refund

**Detailed report (PCN874 / doch mefurat) is a SEPARATE filing.** Do not confuse the summary return above with PCN874, the line-by-line structured file (one row per invoice: number, date, pre-VAT amount, VAT, counterparty business number, allocation number) that businesses above the detailed-report threshold must submit IN ADDITION. Per the Tax Authority new-dealer guide, from reporting period 9/2025 the detailed-report obligation applies to all businesses (self-employed and companies) with annual turnover above NIS 5,000,000 (NPOs above 20 million, financial institutions above 4 million).

### Step 5: Validate and Submit
Before submission, verify:
1. All sales invoices accounted for (cross-reference with e-invoice allocation numbers)
2. Input VAT claims supported by valid tax invoices with allocation numbers (mispar haktzaa), required above a pre-VAT transaction threshold that steps down on a schedule: NIS 25,000 (from May 2024), NIS 20,000 (from Jan 2025), NIS 10,000 (from Jan 2026), NIS 5,000 (from 1 June 2026, in effect now). A valid allocation number has been the precondition for the buyer to deduct input VAT on any invoice above the current threshold since the model launched, only the invoice size changes at each step, so from 1 June 2026 it applies to B2B invoices above NIS 5,000 pre-VAT. Always check the threshold in force on the invoice date
3. Correct reporting period selected
4. Deadline not passed (see below)

**Filing deadlines:**
- Manual filing: 15th of the month following the reporting period
- Online filing via SHAAM portal: 19th of the following month (by 6:30 PM)
- Detailed report filers: Payment extended to 23rd of the following month

**Filing options:**
- SHAAM online portal: https://www.misim.gov.il
- Accountant submission via SHAAM API
- Paper form (being phased out)

## Examples

### Example 1: Monthly VAT Report
User says: "Help me prepare my VAT report for January 2026"
Actions:
1. Determine: Monthly reporter (turnover > NIS 1,775,000 or company)
2. Collect: January sales and purchase invoices
3. Calculate: Output VAT 34,000 - Input VAT 22,000 = Net 12,000 NIS owed
4. Prepare: the periodic VAT return with all fields mapped
5. Guide: Submit via SHAAM portal by February 19th (online deadline)
Result: Complete VAT report ready for filing

### Example 2: Bi-monthly Report with Exports
User says: "I need to file my VAT for November-December, I had some exports"
Actions:
1. Determine: Bi-monthly reporter
2. Identify: Export sales are zero-rated (0% VAT, but still reported)
3. Calculate: Domestic output VAT - Input VAT = Net
4. Note: Exports reported in Field 2, no VAT but supports input VAT recovery
Result: VAT report with zero-rated export handling

## Bundled Resources

### Scripts
- `scripts/calculate_vat.py`, Computes net VAT liability from sales (output) and purchase (input) records, applies Israeli deduction rules for non-deductible and partially deductible expenses, and maps results to the periodic VAT return fields. Run: `python scripts/calculate_vat.py --help`

### References
- `references/vat-regulations.md`, Summary of Israeli VAT law including current and historical VAT rates, registration types (Osek Morsheh, Osek Patur), and filing obligations. Consult when verifying VAT rate or registration rules.
- `references/reporting-calendar.md`, Filing deadlines for monthly and bi-monthly VAT reporters, including the 15th (manual) and 19th (online) deadline rules. Consult when determining reporting period and deadline for a specific month.
- `references/special-cases.md`, Rules for zero-rated transactions (exports, tourism, Eilat zone), exempt transactions (financial services, residential rent), and the distinction between zero-rated and exempt for input VAT recovery. Consult when handling exports or unusual transaction types.

## Gotchas
- Agents frequently use the old 17% VAT rate. The current Israeli VAT rate is **18%** (effective January 1, 2025, per the 2025 Budget Law). This single error cascades through all calculations. Always verify the rate before computing.
- Israeli VAT reports are filed bi-monthly (every two months), not quarterly as in many European countries. Agents may suggest quarterly filing, which will result in missed deadlines and penalties.
- Osek Patur businesses (annual revenue approximately 122,833 NIS, subject to annual updates) do not charge or report VAT. Agents may generate VAT reports for businesses that should not be filing them.
- Input VAT (mas tsumot) from car purchases is only 2/3 deductible in Israel. Agents may claim full VAT deduction on vehicle-related expenses.
- From 2026, input VAT deduction requires a valid allocation number (mispar haktzaa) on invoices above the threshold (NIS 5,000 pre-VAT from 1 June 2026, currently in force; it stepped down from NIS 10,000 in January 2026). Agents may ignore this requirement, leading to rejected deductions.

## Troubleshooting

### Error: "Reporting period mismatch"
Cause: Submitting for wrong period (e.g., single month when registered as bi-monthly)
Solution: Check business registration. Bi-monthly periods: Jan-Feb, Mar-Apr, May-Jun, Jul-Aug, Sep-Oct, Nov-Dec.

### Error: "Input VAT not deductible"
Cause: Claiming VAT from non-deductible expenses (entertainment, non-business)
Solution: Review deduction rules in Step 3. Only business expenses with valid tax invoices qualify.

### Error: "Late filing penalty"
Cause: Filing after the deadline (15th manual / 19th online) of the following month
Solution: File immediately. Late filing triggers late-payment fines, a debt fine, and linkage differentials and interest, and may also draw an administrative fine. Verify the current-year amounts with the Tax Authority.