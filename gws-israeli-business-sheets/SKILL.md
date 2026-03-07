---
name: gws-israeli-business-sheets
description: >-
  Google Sheets financial tracking and automation for Israeli freelancers and small
  businesses using the Google Workspace CLI (gws). Use when user asks to create
  income/expense sheets with Shekel formatting, track VAT (17%) calculations,
  generate tax-period summaries for accountants, backup spreadsheets as CSV, or
  auto-log payments. Do NOT use for direct bank API integrations, payroll processing,
  or filing taxes with the Israel Tax Authority.
license: MIT
allowed-tools: "Bash(gws:*) Bash(npx:*) Bash(node:*) Bash(python:*) Read Write Edit"
compatibility: >-
  Requires Node.js 18+ and the Google Workspace CLI (npm install -g @google/gws).
  Requires Google OAuth setup via gws auth login. Works with Claude Code, Cursor,
  GitHub Copilot, Windsurf, OpenCode, and Codex.
metadata:
  author: choroshin
  version: 1.0.0
  category: tax-and-finance
  tags:
    he:
      - גוגל-וורקספייס
      - גוגל-שיטס
      - מעקב-הוצאות
      - מע"מ
      - פרילנסר
      - הנהלת-חשבונות
    en:
      - google-workspace
      - google-sheets
      - expense-tracking
      - vat
      - freelancer
      - accounting
  display_name:
    he: "גיליונות עסקיים ישראליים עם GWS"
    en: "GWS Israeli Business Sheets"
  display_description:
    he: >-
      אוטומציית תהליכי גיליונות אלקטרוניים פיננסיים לעסקים ישראליים באמצעות
      Google Workspace CLI -- מעקב הוצאות, חישובי מע"מ, סיכומי תקופות מס
      וייצוא CSV לרואה חשבון.
    en: >-
      Automate Google Sheets financial workflows for Israeli businesses using the
      Google Workspace CLI -- expense tracking, VAT calculations, tax-period
      summaries, and accountant-ready CSV exports.
  supported_agents:
    - claude-code
    - cursor
    - github-copilot
    - windsurf
    - opencode
    - codex
---

# GWS Israeli Business Sheets

## Instructions

### Step 1: Verify GWS CLI Installation and Authentication

Before performing any Google Sheets operations, confirm the Google Workspace CLI is installed and authenticated.

```bash
# Check if gws is installed
gws --version

# If not installed, install globally
npm install -g @google/gws

# Authenticate with Google OAuth
gws auth login

# Verify authentication status
gws auth status
```

If the user has not configured a Google Cloud project, guide them through `gws auth setup` to create OAuth credentials.

### Step 2: Create a New Financial Tracking Spreadsheet

When the user wants to set up a new income/expense tracking sheet, create it with proper Israeli financial structure.

**Sheet structure for Israeli freelancers:**

| Column | Header (EN) | Header (HE) | Format | Purpose |
|--------|------------|-------------|--------|---------|
| A | Date | תאריך | DD/MM/YYYY | Transaction date |
| B | Description | תיאור | Text | What the transaction is |
| C | Category | קטגוריה | Text | Tax-deductible category |
| D | Amount (excl. VAT) | סכום (ללא מע"מ) | ILS currency | Net amount |
| E | VAT (17%) | מע"מ (17%) | ILS currency | Calculated VAT |
| F | Total (incl. VAT) | סכום כולל מע"מ | ILS currency | Gross amount |
| G | Type | סוג | Income/Expense | Direction of money |
| H | Invoice # | מספר חשבונית | Text | Invoice reference |
| I | Payment Method | אמצעי תשלום | Text | Bank/PayPal/Cash |
| J | Notes | הערות | Text | Additional details |

**Tax-deductible categories for Israeli businesses:**

| Category (EN) | Category (HE) | Deduction Rate |
|---------------|---------------|----------------|
| Office Rent | שכירות משרד | 100% |
| Equipment | ציוד | 100% |
| Phone & Internet | טלפון ואינטרנט | 100% (if business-only) |
| Professional Services | שירותים מקצועיים | 100% |
| Car Expenses | הוצאות רכב | Limited (45% or fixed) |
| Meals & Entertainment | ארוחות ואירוח | 80% |
| Travel | נסיעות | 100% |
| Software & Subscriptions | תוכנה ומנויים | 100% |
| Marketing | שיווק | 100% |
| Insurance | ביטוח | 100% |

To create the spreadsheet with headers:

```bash
# Create a new spreadsheet (returns spreadsheet ID)
gws sheets create --title "Business Tracker 2026"

# Set up headers in the first row
gws sheets append --spreadsheet-id SPREADSHEET_ID --range "Sheet1!A1:J1" \
  --values '[["Date","Description","Category","Amount (excl. VAT)","VAT (17%)","Total (incl. VAT)","Type","Invoice #","Payment Method","Notes"]]'
```

### Step 3: Append Income and Expense Entries

When the user wants to log a transaction, calculate the VAT automatically and append the row.

**For income entries (user received payment):**

```bash
# Calculate: if user received 5,850 ILS total, the breakdown is:
# Amount excl. VAT = Total / 1.17 = 5,000 ILS
# VAT = Amount * 0.17 = 850 ILS
gws sheets append --spreadsheet-id SPREADSHEET_ID --range "Sheet1!A:J" \
  --values '[["15/01/2026","Web Development Project","Professional Services","5000","850","5850","Income","INV-2026-001","Bank Transfer",""]]'
```

**For expense entries:**

```bash
# Example: Office internet bill of 234 ILS (200 + 34 VAT)
gws sheets append --spreadsheet-id SPREADSHEET_ID --range "Sheet1!A:J" \
  --values '[["20/01/2026","Bezeq Internet","Phone & Internet","200","34","234","Expense","","Direct Debit",""]]'
```

**VAT calculation formulas:**

| Scenario | Formula | Example |
|----------|---------|---------|
| Have total (incl. VAT), need breakdown | Amount = Total / 1.17, VAT = Total - Amount | 1170 / 1.17 = 1000, VAT = 170 |
| Have net amount, need total | VAT = Amount * 0.17, Total = Amount + VAT | 1000 * 0.17 = 170, Total = 1170 |
| Meal expense (80% deductible) | Deductible = Amount * 0.80 | 500 * 0.80 = 400 |

### Step 4: Read and Summarize Financial Data

When the user needs a financial overview, read the data and compute summaries.

```bash
# Read all entries from the sheet
gws sheets read --spreadsheet-id SPREADSHEET_ID --range "Sheet1!A:J"

# Read entries with JSON output for programmatic processing
gws sheets read --spreadsheet-id SPREADSHEET_ID --range "Sheet1!A:J" --output json
```

After reading the data, calculate and present:
- Total income for the period
- Total expenses for the period
- Net profit (income minus expenses)
- Total VAT collected (on income)
- Total VAT paid (on expenses, input VAT)
- VAT liability (collected minus paid, amount to report to tax authority)

**Bi-monthly VAT reporting periods (Israel):**

| Period | Months | Report Due By |
|--------|--------|---------------|
| 1 | January-February | March 15 |
| 2 | March-April | May 15 |
| 3 | May-June | July 15 |
| 4 | July-August | September 15 |
| 5 | September-October | November 15 |
| 6 | November-December | January 15 |

### Step 5: Generate Tax-Period Summary Reports

When the user needs to prepare data for their accountant or for VAT reporting, create a summary sheet.

```bash
# Read all data
gws sheets read --spreadsheet-id SPREADSHEET_ID --range "Sheet1!A:J" --output json
```

After reading, use Python (via `scripts/vat-summary.py`) to:
1. Filter transactions by the bi-monthly period
2. Group by income vs. expenses
3. Calculate total VAT collected and input VAT
4. Generate a summary suitable for the accountant

Then write the summary to a new tab:

```bash
# Create summary headers in a new sheet tab
gws sheets append --spreadsheet-id SPREADSHEET_ID --range "VAT-Period-1!A1:D1" \
  --values '[["Category","Total Amount","Total VAT","Transaction Count"]]'

# Append summary rows
gws sheets append --spreadsheet-id SPREADSHEET_ID --range "VAT-Period-1!A:D" \
  --values '[["Total Income","50000","8500","15"],["Total Expenses","20000","3400","25"],["VAT Liability","","5100",""],["Net Profit","30000","",""]]'
```

### Step 6: Backup Sheets as CSV

When the user wants to create local backups or share data with their accountant, export to CSV.

```bash
# Export the main tracking sheet as CSV
gws sheets read --spreadsheet-id SPREADSHEET_ID --range "Sheet1!A:J" --output csv > business-tracker-2026.csv

# Export a specific VAT period
gws sheets read --spreadsheet-id SPREADSHEET_ID --range "VAT-Period-1!A:D" --output csv > vat-period-1-2026.csv
```

Use the `scripts/backup-sheets.py` script for automated multi-sheet backup:

```bash
python scripts/backup-sheets.py --spreadsheet-id SPREADSHEET_ID --output-dir ./backups/2026-01
```

### Step 7: Auto-Log Payments from Structured Input

When the user provides transaction data in bulk (from a bank statement or invoice list), parse and append multiple entries at once.

```bash
# Append multiple rows in one call
gws sheets append --spreadsheet-id SPREADSHEET_ID --range "Sheet1!A:J" \
  --values '[
    ["01/02/2026","Client A - Monthly Retainer","Professional Services","10000","1700","11700","Income","INV-2026-010","Bank Transfer",""],
    ["03/02/2026","AWS Hosting","Software & Subscriptions","450","76.50","526.50","Expense","","Credit Card",""],
    ["05/02/2026","Business Lunch - Client B","Meals & Entertainment","300","51","351","Expense","","Credit Card","80% deductible"]
  ]'
```

### Step 8: Use Dry-Run Mode for Validation

Before making changes, always offer the user a dry-run preview.

```bash
# Preview what would be appended without writing
gws sheets append --spreadsheet-id SPREADSHEET_ID --range "Sheet1!A:J" \
  --values '[["15/03/2026","Test Entry","Office Rent","5000","850","5850","Expense","","Bank Transfer",""]]' \
  --dry-run
```

## Examples

### Example 1: Israeli Freelancer Sets Up Monthly Tracking

User says: "Create a Google Sheet to track my freelance income and expenses with VAT"

Actions:
1. Run `gws sheets create --title "Freelance Tracker 2026"` to create the spreadsheet
2. Append header row with all 10 columns (Date through Notes)
3. Show the user the spreadsheet ID and link
4. Explain the column structure and how VAT will be calculated for each entry

Result: A new Google Sheet with proper Israeli freelancer financial structure, ready for entries.

### Example 2: Generate Bi-Monthly VAT Summary for Accountant

User says: "Create a VAT summary for January-February 2026 and export it as CSV"

Actions:
1. Run `gws sheets read` to pull all entries from the tracking sheet
2. Run `python scripts/vat-summary.py` to filter Jan-Feb transactions and compute totals
3. Write summary to a new "VAT-Period-1-2026" tab in the spreadsheet
4. Export the summary tab as CSV with `gws sheets read --output csv`
5. Display the summary: total income, total expenses, VAT collected, input VAT, net VAT liability

Result: A clean VAT period summary both in the Google Sheet and as a local CSV file ready to send to the accountant.

### Example 3: Auto-Log Bank Transfers into Expense Sheet

User says: "I got these payments this month: Client A paid 11,700 for consulting, I paid 526.50 for hosting, and 351 for a business lunch"

Actions:
1. Parse each transaction, calculate VAT breakdown (divide totals by 1.17)
2. Categorize: consulting = Professional Services (income), hosting = Software & Subscriptions (expense), lunch = Meals & Entertainment (expense, 80% deductible)
3. Use `gws sheets append` with multi-row values array
4. Confirm all entries were logged with correct VAT calculations

Result: Three new rows appended to the tracking sheet with proper categorization, VAT breakdown, and deductibility notes.

## Bundled Resources

### Scripts
- `scripts/vat-summary.py` -- Generate bi-monthly VAT summary reports from sheet data. Run: `python scripts/vat-summary.py --help`
- `scripts/backup-sheets.py` -- Backup Google Sheets tabs as local CSV files. Run: `python scripts/backup-sheets.py --help`

### References
- `references/israeli-tax-categories.md` -- Complete list of Israeli tax-deductible expense categories with deduction rates. Consult when categorizing a business expense.
- `references/gws-sheets-recipes.md` -- Common gws CLI recipes for Google Sheets operations. Consult when performing sheet operations beyond basic read/append.

## Troubleshooting

### Error: "gws: command not found"
Cause: The Google Workspace CLI is not installed or not in PATH.
Solution: Install with `npm install -g @google/gws`. If using npx, prefix commands with `npx @google/gws`.

### Error: "Authentication required" or "Token expired"
Cause: The user has not authenticated or the OAuth token has expired.
Solution: Run `gws auth login` to re-authenticate. If the Google Cloud project is not configured, run `gws auth setup` first.

### Error: "Spreadsheet not found" or "404"
Cause: The spreadsheet ID is incorrect or the user does not have access.
Solution: Verify the spreadsheet ID from the Google Sheets URL (the string between /d/ and /edit). Ensure the authenticated Google account has edit access to the sheet.

### Error: "VAT calculation mismatch"
Cause: Rounding differences between manual calculation and sheet formulas.
Solution: Always round VAT to 2 decimal places. Use the formula: `Math.round(amount * 17) / 100` for precise Shekel calculations. Israeli tax authority accepts rounding to the nearest agora.
