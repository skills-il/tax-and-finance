---
name: il-invoice-organizer
description: >-
  Parse, validate, and organize Israeli invoices (heshbonit mas, kabala,
  heshbonit zikui) with automatic VAT extraction using the 1/6 rule
  (17% VAT = amount * 17/117). Use when user asks about Israeli invoices,
  "heshbonit", "kabala", "osek murshe", "mas erech musaf", VAT calculation,
  expense categorization, or bookkeeping for Israeli businesses. Identifies
  Osek Murshe (authorized dealer), Osek Patur (exempt dealer), and Hevra
  Peratit (private company) numbers. Categorizes expenses per Tax Authority
  (Rashut HaMisim) official categories and generates summary reports for
  accountants. Do NOT use for payroll processing, annual tax filing, or
  non-Israeli invoice formats.
license: MIT
compatibility: >-
  Requires Python 3.8+ for categorization script. Works with Claude Code,
  Cursor, GitHub Copilot, Windsurf, OpenCode, Codex.
metadata:
  author: skills-il
  version: 1.0.0
  category: tax-and-finance
  tags:
    he:
      - חשבוניות
      - מע"מ
      - עוסק-מורשה
      - הנהלת-חשבונות
      - ישראל
    en:
      - invoices
      - vat
      - bookkeeping
      - tax-authority
      - israel
  display_name:
    he: ארגון חשבוניות ישראלי
    en: IL Invoice Organizer
  display_description:
    he: >-
      ניתוח, אימות וארגון חשבוניות ישראליות עם חילוץ מע"מ אוטומטי לפי כלל
      1/6, זיהוי עוסק מורשה/פטור/ח"פ, וסיווג הוצאות לפי קטגוריות רשות
      המסים. כולל הפקת דוחות סיכום לרואה חשבון.
    en: >-
      Parse, validate, and organize Israeli invoices with automatic VAT
      extraction using the 1/6 rule, Osek Murshe/Patur/HP number recognition,
      and Tax Authority expense categorization. Generates summary reports for
      accountants.
  supported_agents:
    - claude-code
    - cursor
    - github-copilot
    - windsurf
    - opencode
    - codex
---

# IL Invoice Organizer

## Instructions

### Step 1: Identify Invoice Type and Business Entity
Determine the type of document and the issuing business entity:

| Document Type | Hebrew | Description | VAT Implications |
|---------------|--------|-------------|------------------|
| Tax Invoice (heshbonit mas) | חשבונית מס | Issued by Osek Murshe, includes VAT | Full VAT deduction allowed |
| Tax Invoice Receipt (heshbonit mas / kabala) | חשבונית מס / קבלה | Combined invoice + payment confirmation | Full VAT deduction allowed |
| Receipt (kabala) | קבלה | Payment confirmation only | No VAT deduction |
| Credit Invoice (heshbonit zikui) | חשבונית זיכוי | Cancellation or reduction of prior invoice | Reverses original VAT |
| Proforma Invoice (heshbonit proforma) | חשבונית פרופורמה | Quote or estimate, not a fiscal document | No VAT implications |

Identify the issuing entity by their business number format:

| Entity Type | Hebrew | Number Format | VAT Status |
|-------------|--------|---------------|------------|
| Osek Murshe (authorized dealer) | עוסק מורשה | 9-digit number (TZ or business) | Charges and reports VAT |
| Osek Patur (exempt dealer) | עוסק פטור | 9-digit number (TZ-based) | Does not charge VAT |
| Hevra Peratit / HP (private company) | חברה פרטית (ח"פ) | 51-xxxxxxx or 52-xxxxxxx | Charges and reports VAT |
| Amuta (non-profit) | עמותה | 58-xxxxxxx | Usually VAT exempt |

### Step 2: Extract Invoice Data
Parse the following fields from each invoice:

- **Invoice number** (mispar heshbonit) -- sequential, unique per business
- **Issue date** (ta'arich) -- DD/MM/YYYY format (Israeli standard)
- **Business name and number** (shem ha'esek ve'mispar osek)
- **Customer details** (pirtei ha'lakoch)
- **Line items** -- description, quantity, unit price
- **Subtotal before VAT** (sach lifnei ma'am)
- **VAT amount** (sechum ma'am)
- **Total including VAT** (sach kolel ma'am)
- **Payment method** (emtza'ei tashlum) -- cash, bank transfer, check, credit card

Validate that the invoice number, business number, and date are present. Flag any missing required fields.

### Step 3: Calculate and Verify VAT (Mas Erech Musaf)
Israeli VAT is currently 17%. Apply the 1/6 extraction rule:

**When you have the total amount (including VAT):**
```
vat_amount = total_with_vat * 17 / 117
amount_before_vat = total_with_vat - vat_amount
```

**When you have the amount before VAT:**
```
vat_amount = amount_before_vat * 0.17
total_with_vat = amount_before_vat * 1.17
```

**Verification formula:**
```
# These must match (within rounding tolerance of 1 NIS):
stated_vat ≈ total_with_vat * 17 / 117
stated_total ≈ amount_before_vat * 1.17
```

| Scenario | VAT Deductible? | Notes |
|----------|-----------------|-------|
| Tax invoice from Osek Murshe | Yes | Standard deduction |
| Receipt from Osek Patur | No | No VAT was charged |
| Invoice for mixed use (business + personal) | Partial | Proportional deduction only |
| Vehicle expenses (non-commercial) | Partial (2/3) | 1/3 of VAT is non-deductible for private vehicles |
| Entertainment/meals | 80% deductible | Income tax: only 80% recognized as expense |
| Invoice missing business number | No | Invalid for VAT deduction |

### Step 4: Categorize Expenses per Tax Authority Categories
Use `scripts/categorize_invoices.py` to classify each invoice into official Tax Authority expense categories. The categories are defined in `references/expense-categories.md`.

Primary expense categories (Rashut HaMisim official list):

| Category Code | Hebrew | English | Common Examples |
|---------------|--------|---------|-----------------|
| 1 | חומרי גלם | Raw materials | Materials for production |
| 2 | קבלני משנה | Subcontractors | Outsourced services |
| 3 | שכר עבודה | Wages and salaries | Employee payroll |
| 4 | ביטוח לאומי מעסיק | Employer NII | Bituach Leumi employer share |
| 5 | שכירות | Rent | Office/warehouse rent |
| 6 | ביטוח | Insurance | Business insurance policies |
| 7 | חשמל ומים | Utilities | Electricity, water |
| 8 | תקשורת | Communications | Phone, internet |
| 9 | הוצאות רכב | Vehicle expenses | Fuel, maintenance, insurance |
| 10 | פחת | Depreciation | Equipment, computers, furniture |
| 11 | הוצאות משרד | Office expenses | Supplies, printing |
| 12 | הוצאות אחרות | Other expenses | Miscellaneous |

Run categorization:
```bash
python scripts/categorize_invoices.py --input invoices.json --output categorized.json
```

### Step 5: Validate Invoice Compliance
Check each invoice against Israeli legal requirements:

1. **Mandatory fields present:** business name, business number, invoice number, date, amounts
2. **VAT calculation correct:** Stated VAT matches 17% calculation (tolerance: 1 NIS rounding)
3. **Business number valid:** 9-digit format, passes check-digit validation
4. **Sequential numbering:** Invoice numbers should be sequential (flag gaps)
5. **Date reasonable:** Not future-dated, within current or previous reporting period
6. **E-invoice compliance (from 2024):** For businesses above threshold, verify digital signature and Tax Authority allocation number (mispar hiktzaot)

### Step 6: Generate Summary Report
Produce a structured report for the accountant (ro'eh heshbon):

```
=== Invoice Summary Report / דוח סיכום חשבוניות ===
Period: MM/YYYY
Business: [Name] | Osek Number: [Number]

--- Expense Breakdown by Category ---
Category          | Count | Before VAT  | VAT        | Total
Raw materials     |     5 | 12,500 NIS  | 2,125 NIS  | 14,625 NIS
Rent              |     1 |  8,000 NIS  | 1,360 NIS  |  9,360 NIS
Office expenses   |     8 |  3,200 NIS  |   544 NIS  |  3,744 NIS
...

--- VAT Summary ---
Total input VAT (mas tsumos):    4,029 NIS
Non-deductible VAT:                340 NIS
Net deductible VAT:              3,689 NIS

--- Flagged Items ---
! Invoice #1234: VAT mismatch (stated 850, calculated 843)
! Invoice #1567: Missing business number
```

## Examples

### Example 1: Parse a Single Invoice
User says: "I have an invoice from a supplier. Total is 5,850 NIS including VAT. Break it down."
Actions:
1. Apply VAT extraction: 5,850 * 17 / 117 = 850 NIS (VAT)
2. Amount before VAT: 5,850 - 850 = 5,000 NIS
3. Verify: 5,000 * 1.17 = 5,850 NIS (matches)
4. Present breakdown with category suggestion
Result: Before VAT: 5,000 NIS | VAT: 850 NIS | Total: 5,850 NIS. VAT is deductible if this is a valid tax invoice from an Osek Murshe.

### Example 2: Categorize Monthly Invoices
User says: "I have 15 invoices from this month. Categorize them for my accountant."
Actions:
1. Parse each invoice to extract amounts and vendor details
2. Run `python scripts/categorize_invoices.py --input invoices.json --output categorized.json`
3. Map each invoice to Tax Authority categories based on vendor type and description
4. Generate summary report with totals per category
Result: Categorized report with expense breakdown, VAT summary, and flagged items for accountant review.

### Example 3: Verify Osek Murshe Number
User says: "Is this a valid business number: 514567890? Is it an HP?"
Actions:
1. Check format: 9 digits starting with 51 indicates Hevra Peratit (HP / private company)
2. Validate check digit using Luhn-like algorithm for Israeli business numbers
3. Confirm: This is a company number (HP), not a personal Osek Murshe number
4. Note: HP companies are always Osek Murshe (authorized dealer) and must charge VAT
Result: Valid HP (private company) number. This entity is an authorized dealer and should issue tax invoices with 17% VAT.

### Example 4: Handle Mixed-Use Vehicle Invoice
User says: "I got a 2,340 NIS fuel invoice for my car that I use for both business and personal."
Actions:
1. Extract VAT: 2,340 * 17 / 117 = 340 NIS (total VAT)
2. Apply vehicle rule: For non-commercial vehicles, only 2/3 of VAT is deductible
3. Deductible VAT: 340 * 2/3 = 226.67 NIS
4. Non-deductible VAT: 340 * 1/3 = 113.33 NIS
5. Categorize under "Vehicle expenses" (category 9)
Result: Total VAT 340 NIS, but only 226.67 NIS is deductible. The remaining 113.33 NIS is a non-deductible expense.

## Bundled Resources

### Scripts
- `scripts/categorize_invoices.py` -- Parses invoice data (JSON input) and categorizes expenses per Tax Authority categories. Calculates VAT amounts, flags compliance issues, and generates summary reports. Run: `python scripts/categorize_invoices.py --help`

### References
- `references/expense-categories.md` -- Complete list of Tax Authority (Rashut HaMisim) official expense categories with codes, descriptions, and common examples. Consult when mapping invoices to categories.

## Troubleshooting

### Error: "VAT amount does not match calculated value"
Cause: Rounding differences or incorrect VAT rate applied on the invoice
Solution: Israeli VAT is 17%. Use `total * 17 / 117` for extraction. Allow 1 NIS rounding tolerance. If the difference exceeds 1 NIS, the invoice may have an error -- contact the supplier for a corrected invoice (heshbonit metukenet).

### Error: "Business number validation failed"
Cause: Invalid check digit, wrong number of digits, or using an old/cancelled registration
Solution: Verify the number on the Tax Authority website (taxes.gov.il). Osek numbers are 9 digits. HP numbers start with 51/52. Amuta numbers start with 58. If the business recently registered, it may take a few days to appear in the registry.

### Error: "Cannot determine if Osek Murshe or Patur"
Cause: The invoice does not clearly state the business type, or VAT is missing
Solution: Check if VAT is itemized separately on the invoice. Osek Murshe must show VAT; Osek Patur must state "osek patur" (exempt dealer) on the invoice. Verify on the Tax Authority dealer lookup (sheiltat osek). Only Osek Murshe invoices qualify for VAT (mas tsumos) deduction.

### Error: "E-invoice allocation number missing"
Cause: Since 2024, businesses above the threshold must issue e-invoices with a Tax Authority allocation number
Solution: Check if the invoice has a mispar hiktzaot (allocation number) from the Tax Authority. Without it, invoices above the threshold amount are not valid for VAT deduction. Contact the supplier to reissue as a proper e-invoice.
