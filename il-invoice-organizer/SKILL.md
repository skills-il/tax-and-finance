---
name: il-invoice-organizer
description: >-
  Parse and organize Hebrew invoices for Israeli bookkeeping: VAT 1/6
  extraction, Tax Authority expense categories, Osek Murshe/Patur recognition,
  and accountant-ready export. Use when user asks about organizing invoices,
  "cheshbonit", expense categorization, "sivug hotza'ot", VAT extraction from
  totals, Osek Murshe vs Osek Patur rules, or preparing documents for their
  accountant ("ro'eh cheshbon"). Supports Hebrew OCR text parsing and automatic
  categorization per Tax Authority standards. Do NOT use for invoice generation
  (use israeli-e-invoice instead) or for VAT report filing (use
  israeli-vat-reporting instead).
license: MIT
compatibility: >-
  Works with Claude Code, Cursor, GitHub Copilot, Windsurf, OpenCode, Codex.
  Python 3.8+ for helper scripts.
metadata:
  author: skills-il
  version: 1.0.1
  category: tax-and-finance
  tags:
    he:
      - חשבוניות
      - מע"מ
      - עוסק-מורשה
      - הנהלת-חשבונות
      - רואה-חשבון
      - ישראל
    en:
      - invoices
      - vat
      - bookkeeping
      - tax-authority
      - accountant
      - israel
  display_name:
    he: מארגן חשבוניות ישראלי
    en: IL Invoice Organizer
  display_description:
    he: >-
      ניתוח וארגון חשבוניות בעברית להנהלת חשבונות ישראלית: חילוץ מע"מ 1/6,
      קטגוריות רשות המסים, זיהוי עוסק מורשה/פטור, וייצוא מוכן לרואה חשבון.
    en: >-
      Parse and organize Hebrew invoices for Israeli bookkeeping: VAT 1/6
      extraction, Tax Authority expense categories, Osek Murshe/Patur
      recognition, and accountant-ready export. Use when user asks about
      organizing invoices, expense categorization, VAT extraction, or preparing
      documents for their accountant. Do NOT use for invoice generation (use
      israeli-e-invoice instead) or for VAT report filing (use
      israeli-vat-reporting instead).
  supported_agents:
    - claude-code
    - cursor
    - github-copilot
    - windsurf
    - opencode
    - codex
    - antigravity
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
| Allocation number | מספר הקצאה | If above threshold | SHAAM allocated |

### Step 3: Extract VAT (1/6 Rule)
For Israeli invoices where only the total (gross) amount is visible:

```python
# VAT extraction from gross amount (כלל השישית)
vat_rate = 0.18  # 18% standard rate
gross_amount = 1180  # סכום כולל מע"מ

# Method: VAT = gross * (rate / (1 + rate)) = gross * (18/118)
vat_amount = gross_amount * (vat_rate / (1 + vat_rate))
# = 1170 * (0.18 / 1.18) = 1180 * 0.1525 = 180

net_amount = gross_amount - vat_amount
# = 1180 - 180 = 1000
```

Shortcut: VAT = Total / 6.556 (approximately 1/6 of the gross, hence "klal hashishit")

### Step 4: Categorize by Tax Authority Standards
Assign each expense to a Tax Authority category:

| Category | Hebrew | Expense Code | Common Examples |
|----------|--------|-------------|-----------------|
| Salary & wages | שכר עבודה | 10 | Employee salaries, bonuses |
| Subcontractors | קבלני משנה | 20 | Freelancer invoices |
| Rent | שכירות | 30 | Office, warehouse rent |
| Office supplies | חומרי משרד | 40 | Paper, toner, supplies |
| Communications | תקשורת | 50 | Phone, internet, hosting |
| Professional services | שירותים מקצועיים | 60 | Legal, accounting, consulting |
| Vehicle expenses | רכב | 70 | Fuel, maintenance, insurance |
| Travel | נסיעות | 80 | Flights, hotels, per diem |
| Marketing | שיווק ופרסום | 90 | Advertising, events |
| Insurance | ביטוח | 100 | Business insurance |
| Depreciation | פחת | 110 | Equipment, computers |
| Other | אחר | 999 | Miscellaneous |

Use `scripts/categorize_invoices.py` for automatic categorization.

### Step 5: Identify Business Type
Determine supplier and customer business status:

| Status | Hebrew | VAT Treatment | Invoice Type |
|--------|--------|--------------|--------------|
| Osek Murshe | עוסק מורשה | Charges VAT, can deduct input VAT | Tax Invoice (300/305) |
| Osek Patur | עוסק פטור | No VAT charged (under threshold) | Receipt only (320) |
| Amuta (Non-profit) | עמותה | Usually no VAT | Receipt |
| Malkar (Non-profit) | מלכ"ר | No VAT | Receipt |

Important: You can only deduct input VAT (mas tsumos) from tax invoices issued by Osek Murshe suppliers. Receipts from Osek Patur do not have VAT to deduct.

### Step 6: Generate Accountant-Ready Export
Organize the data for the accountant (ro'eh cheshbon):

Output format (CSV/Excel):
```
Date, Supplier, TIN, Invoice#, Category, Net, VAT, Total, Notes
15/01/2025, חברת אלפא, 515000000, 1234, קבלני משנה, 10000, 1700, 11700, שירותי פיתוח
```

Include summary:
- Total expenses by category
- Total input VAT (mas tsumos) to reclaim
- Missing invoices or data gaps flagged
- Separate section for non-deductible items

## Examples

### Example 1: Monthly Invoice Organization
User says: "I have 30 invoices from this month. Help me organize them for my accountant"
Actions:
1. Collect: Invoice images or text data from user
2. Parse: Extract supplier, amount, VAT, date from each
3. Categorize: Assign Tax Authority category per Step 4
4. Validate: Check TIN format, VAT calculation, allocation numbers
5. Run `python scripts/categorize_invoices.py --input invoices.csv`
6. Export: Generate accountant-ready CSV with summary
Result: Organized expense report with VAT summary ready for accountant

### Example 2: VAT Extraction from Receipts
User says: "I paid 5,850 NIS total for cloud services. What is the VAT portion?"
Actions:
1. Apply 1/6 rule: VAT = 5,850 * (0.18 / 1.18) = 892.37 NIS
2. Net amount: 5,850 - 892.37 = 4,957.63 NIS
3. Categorize: Communications (code 50) for cloud services
4. Note: Verify supplier is Osek Murshe and issued tax invoice
Result: VAT of 892.37 NIS extractable, net expense 4,957.63 NIS in Communications category

### Example 3: Osek Patur Invoice Handling
User says: "I got an invoice from a freelance designer, but there is no VAT line"
Actions:
1. Check: Is the supplier Osek Patur (עוסק פטור)?
2. If Osek Patur: No VAT to deduct, record full amount as expense
3. Categorize: Professional services (code 60) or Marketing (code 90)
4. Note: Request the supplier's TIN and verify their status
Result: Full amount recorded as expense with no VAT deduction, flagged for accountant

## Bundled Resources

### Scripts
- `scripts/categorize_invoices.py` -- Categorizes Israeli invoices by Tax Authority expense codes, extracts VAT, and generates accountant-ready reports. Run: `python scripts/categorize_invoices.py --help`

### References
- `references/expense-categories.md` -- Complete list of Tax Authority expense categories with codes, common examples, and special rules for deductibility (vehicle 2/3 rule, entertainment limits). Consult when categorizing unusual expenses.

## Gotchas
- Agents often calculate VAT as `amount * 0.18` when extracting from a total, but the correct formula to extract VAT from a VAT-inclusive amount is `total / 1.18 * 0.18` (or equivalently `total * 18/118`). This "1/6 rule" is specific to Israeli bookkeeping.
- Osek Patur (exempt dealer) invoices have no VAT component. Agents may still try to extract VAT from these invoices, producing incorrect bookkeeping entries.
- Israeli invoice numbers are not globally unique. Different suppliers can have the same invoice number. Always index by supplier + invoice number combination.
- Hebrew OCR on scanned invoices frequently misreads the characters vav (ו) and zayin (ז), and confuses final-mem (ם) with samekh (ס). Verify extracted amounts and names.

## Troubleshooting

### Error: "VAT amount doesn't match"
Cause: Rounding differences between line-item VAT and total VAT
Solution: Israeli invoices may have rounding differences of up to 1 NIS. Use the VAT amount printed on the invoice (not recalculated). If no VAT line exists, use the 1/6 rule from Step 3.

### Error: "Cannot determine business type"
Cause: Invoice does not clearly state Osek Murshe or Osek Patur
Solution: Look for "עוסק מורשה" on the invoice. Check TIN on Tax Authority website. If unclear, treat as Osek Patur (no VAT deduction) and flag for accountant review.

### Error: "Expense category unclear"
Cause: Invoice description is vague or multi-category
Solution: Use the primary purpose of the expense. When in doubt, assign to "Other" (code 999) and let the accountant reclassify. Common confusion: software subscriptions (Communications 50, not Office supplies 40).
