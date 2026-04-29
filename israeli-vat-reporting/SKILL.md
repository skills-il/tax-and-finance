---
name: israeli-vat-reporting
description: Prepare, validate, and guide submission of Israeli VAT reports (Doch Maam) per Tax Authority standards. Use when user asks about VAT reporting, VAT calculation, "doch maam", "maam", Israeli VAT filing, VAT deadlines, or input/output VAT reconciliation. Supports monthly, bi-monthly, and annual reporting. Handles zero-rated exports, exempt transactions, and Eilat zone rules. Do NOT use for income tax, corporate tax, or non-Israeli VAT systems.
license: MIT
compatibility: Works with Claude Code, Claude.ai, Cursor. Network access optional for SHAAM API.
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

Monthly reporting: Annual turnover > NIS 1,500,000 (per Section 69A(g) of the VAT Law)
Bi-monthly reporting: Annual turnover < NIS 1,500,000

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
2. Input VAT claims supported by valid tax invoices with allocation numbers (required for invoices >= NIS 5,000 from June 2026, >= NIS 10,000 from January 2026)
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
1. Determine: Monthly reporter (turnover > NIS 1,500,000 or company)
2. Collect: January sales and purchase invoices
3. Calculate: Output VAT 34,000 - Input VAT 22,000 = Net 12,000 NIS owed
4. Prepare: Form 874 with all fields mapped
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
- `scripts/calculate_vat.py` — Computes net VAT liability from sales (output) and purchase (input) records, applies Israeli deduction rules for non-deductible and partially deductible expenses, and maps results to Form 874 fields. Run: `python scripts/calculate_vat.py --help`

### References
- `references/vat-regulations.md` — Summary of Israeli VAT law including current and historical VAT rates, registration types (Osek Morsheh, Osek Patur), and filing obligations. Consult when verifying VAT rate or registration rules.
- `references/reporting-calendar.md` — Filing deadlines for monthly and bi-monthly VAT reporters, including the 15th (manual) and 19th (online) deadline rules. Consult when determining reporting period and deadline for a specific month.
- `references/special-cases.md` — Rules for zero-rated transactions (exports, tourism, Eilat zone), exempt transactions (financial services, residential rent), and the distinction between zero-rated and exempt for input VAT recovery. Consult when handling exports or unusual transaction types.

## Gotchas
- Agents frequently use the old 17% VAT rate. The current Israeli VAT rate is **18%** (effective January 1, 2025, per the 2025 Budget Law). This single error cascades through all calculations. Always verify the rate before computing.
- Israeli VAT reports are filed bi-monthly (every two months), not quarterly as in many European countries. Agents may suggest quarterly filing, which will result in missed deadlines and penalties.
- Osek Patur businesses (annual revenue approximately 120,000 NIS, subject to annual updates) do not charge or report VAT. Agents may generate VAT reports for businesses that should not be filing them.
- Input VAT (mas tsumot) from car purchases is only 2/3 deductible in Israel. Agents may claim full VAT deduction on vehicle-related expenses.
- From 2026, input VAT deduction requires a valid allocation number (mispar haktzaa) on invoices above the threshold (NIS 10,000 from January 2026, NIS 5,000 from June 2026). Agents may ignore this requirement, leading to rejected deductions.

## Troubleshooting

### Error: "Reporting period mismatch"
Cause: Submitting for wrong period (e.g., single month when registered as bi-monthly)
Solution: Check business registration. Bi-monthly periods: Jan-Feb, Mar-Apr, May-Jun, Jul-Aug, Sep-Oct, Nov-Dec.

### Error: "Input VAT not deductible"
Cause: Claiming VAT from non-deductible expenses (entertainment, non-business)
Solution: Review deduction rules in Step 3. Only business expenses with valid tax invoices qualify.

### Error: "Late filing penalty"
Cause: Filing after the deadline (15th manual / 19th online) of the following month
Solution: File immediately. Late penalty is NIS 239 per two-week period of delay, plus linkage differentials and interest (Bank of Israel rate + 4%).