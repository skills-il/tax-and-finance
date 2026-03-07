# GWS CLI Sheets Recipes

Common recipes for Google Sheets operations using the Google Workspace CLI (gws).

## Installation and Setup

```bash
# Install globally
npm install -g @google/gws

# Or use via npx (no install needed)
npx @google/gws sheets read --help

# Authenticate
gws auth login

# Check auth status
gws auth status

# Set up Google Cloud project (first time)
gws auth setup
```

## Core Commands

### Create a New Spreadsheet

```bash
# Create with title
gws sheets create --title "My Spreadsheet"

# Output includes the new spreadsheet ID
```

### Read Data

```bash
# Read a range (default table output)
gws sheets read --spreadsheet-id SHEET_ID --range "Sheet1!A1:D10"

# Read as JSON
gws sheets read --spreadsheet-id SHEET_ID --range "Sheet1!A:J" --output json

# Read as CSV
gws sheets read --spreadsheet-id SHEET_ID --range "Sheet1!A:J" --output csv

# Read entire sheet
gws sheets read --spreadsheet-id SHEET_ID --range "Sheet1"
```

### Append Data

```bash
# Append a single row
gws sheets append --spreadsheet-id SHEET_ID --range "Sheet1!A:D" \
  --values '[["value1","value2","value3","value4"]]'

# Append multiple rows
gws sheets append --spreadsheet-id SHEET_ID --range "Sheet1!A:D" \
  --values '[["row1col1","row1col2","row1col3","row1col4"],["row2col1","row2col2","row2col3","row2col4"]]'

# Dry run (preview without writing)
gws sheets append --spreadsheet-id SHEET_ID --range "Sheet1!A:D" \
  --values '[["test","data"]]' --dry-run
```

## Recipes

### Recipe: Backup All Tabs as CSV

```bash
# List all sheet tabs, then export each
for tab in "Sheet1" "Sheet2" "Summary"; do
  gws sheets read --spreadsheet-id SHEET_ID --range "$tab" --output csv > "${tab}.csv"
done
```

### Recipe: Copy Monthly Sheet

Create a template for next month by reading current month structure:

```bash
# Read headers from current month
HEADERS=$(gws sheets read --spreadsheet-id SHEET_ID --range "Jan-2026!A1:J1" --output json)

# Write headers to new month tab
gws sheets append --spreadsheet-id SHEET_ID --range "Feb-2026!A1:J1" \
  --values "$HEADERS"
```

### Recipe: Compare Two Sheet Tabs

```bash
# Export both tabs as CSV and diff
gws sheets read --spreadsheet-id SHEET_ID --range "Sheet1!A:J" --output csv > tab1.csv
gws sheets read --spreadsheet-id SHEET_ID --range "Sheet2!A:J" --output csv > tab2.csv
diff tab1.csv tab2.csv
```

### Recipe: Search for Entries

```bash
# Read all data as JSON, then filter with jq
gws sheets read --spreadsheet-id SHEET_ID --range "Sheet1!A:J" --output json \
  | jq '.[] | select(.Category == "Professional Services")'
```

### Recipe: Count Rows by Type

```bash
# Read data and count income vs expense entries
gws sheets read --spreadsheet-id SHEET_ID --range "Sheet1!G:G" --output json \
  | jq 'group_by(.[0]) | map({type: .[0][0], count: length})'
```

## Common Range Notations

| Range | Meaning |
|-------|---------|
| `Sheet1!A1:J1` | First row, columns A through J |
| `Sheet1!A:J` | All rows, columns A through J |
| `Sheet1!A2:J` | All rows starting from row 2 (skip headers) |
| `Sheet1` | Entire sheet |
| `'VAT Period 1'!A:D` | Sheet with spaces in name (use quotes) |

## Tips

- Always use `--dry-run` before appending to production sheets
- Use `--output json` when you need to process data programmatically
- Use `--output csv` when exporting for accountants or external tools
- Spreadsheet ID is the long string in the Google Sheets URL between `/d/` and `/edit`
- All output from gws is structured JSON by default, making it easy to parse
