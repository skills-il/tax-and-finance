---
name: israeli-bank-connector
description: >-
  Analyze Israeli bank transactions, spending patterns, and financial data
  across Israeli banks and credit card companies. Use when user asks about bank
  transactions, spending analysis, "cheshbon bank", budget tracking, or needs to
  categorize Israeli banking data. Enhances israeli-bank-mcp, il-bank-mcp, and
  asher-mcp servers with financial analysis workflows. Supports Hapoalim, Leumi,
  Discount, Mizrahi, Visa Cal, Max, Isracard. Do NOT use for payment initiation,
  money transfers, or investment advice.
license: MIT
compatibility: Requires israeli-bank-mcp or il-bank-mcp MCP server. Claude Code recommended.
metadata:
  author: skills-il
  version: 1.0.1
  category: tax-and-finance
  tags:
    he:
      - בנקאות
      - עסקאות
      - פיננסים
      - הוצאות
      - ישראל
    en:
      - banking
      - transactions
      - finance
      - spending
      - israel
  mcp-server: israeli-bank-mcp
  display_name:
    he: מחבר בנקאות ישראלי
    en: Israeli Bank Connector
  display_description:
    he: 'ניתוח עו"ש, כרטיסי אשראי והוצאות מול הבנקים הישראליים'
    en: >-
      Analyze Israeli bank transactions, spending patterns, and financial data
      across Israeli banks and credit card companies. Use when user asks about
      bank transactions, spending analysis, "cheshbon bank", budget tracking, or
      needs to categorize Israeli banking data. Enhances israeli-bank-mcp,
      il-bank-mcp, and asher-mcp servers with financial analysis workflows.
      Supports Hapoalim, Leumi, Discount, Mizrahi, Visa Cal, Max, Isracard. Do
      NOT use for payment initiation, money transfers, or investment advice.
  supported_agents:
    - claude-code
    - cursor
    - github-copilot
    - windsurf
    - opencode
    - codex
    - antigravity
---

# Israeli Bank Connector

## Instructions

### Step 1: Identify Connected Banks
Check which MCP server is available and what accounts are connected:
- israeli-bank-mcp: Direct scraper integration
- il-bank-mcp: Docker-based with persistent analysis
- If no MCP: Guide user through CSV/Excel import from bank website

### Step 2: Retrieve Transactions
Fetch transaction data for the requested period:
- Default: Current month
- Supported: Up to 12 months history (bank-dependent)
- Include: Bank accounts AND credit card transactions

### Step 3: Categorize and Analyze
Apply Israeli-specific categorization:
| Category | Hebrew | Examples |
|----------|--------|---------|
| Housing | diur | Rent, arnona, vaad bayit |
| Groceries | mazon | Shufersal, Rami Levy, Victory |
| Transportation | tahaburah | Rav-Kav, fuel, Gett |
| Utilities | shartuim | Electric Company, Mekorot, Bezeq |
| Healthcare | briut | Kupat Cholim, pharmacy |
| Education | chinuch | Gan, school, courses |
| Entertainment | bilui | Restaurants, cinema, streaming |
| Insurance | bituach | Health, car, home insurance |
| Savings | chisachon | Pension, keren hishtalmut |

### Step 4: Present Insights
Provide:
1. Monthly spending summary by category
2. Top 10 merchants by spending
3. Month-over-month trends
4. Recurring charges identified
5. Unusual transactions flagged

### Step 5: Export for Tax (if requested)
Format transactions for Israeli tax purposes:
- Separate business vs personal expenses
- Flag VAT-deductible purchases
- Export in format compatible with Israeli accounting software

## Examples

### Example 1: Monthly Spending Summary
User says: "Show me my spending breakdown for January"
Result: Categorized breakdown with NIS amounts per category, top merchants, and comparison to December.

### Example 2: Subscription Audit
User says: "What recurring payments am I making?"
Result: List of detected recurring charges with amounts, frequency, and suggestion for potential savings.

### Example 3: Tax Expense Export
User says: "Export my business expenses for my accountant"
Result: Filtered and categorized business transactions with VAT amounts, ready for import into accounting software.

## Bundled Resources

### Scripts
- `scripts/categorize_transactions.py` — Categorizes Israeli bank transactions by spending category using Israeli-specific merchant pattern matching (Shufersal, Rami Levy, Rav-Kav, etc.). Accepts transaction JSON and outputs categorized spending summaries. Run: `python scripts/categorize_transactions.py --help`

### References
- `references/spending-categories.md` — Israeli spending category definitions with Hebrew terms and common merchant examples for each category (housing/diur, groceries/mazon, transportation/tahaburah, utilities/shartuim, etc.). Consult when customizing categorization rules or explaining categories to users.
- `references/supported-banks.md` — List of supported Israeli banks (Hapoalim, Leumi, Discount, Mizrahi-Tefahot, FIBI) and credit card companies (Visa Cal, Max, Isracard) with bank codes and MCP server compatibility notes. Consult when setting up bank connections or troubleshooting missing accounts.

## Gotchas
- Israeli banks use the "Open Banking" standard mandated by the Bank of Israel, not the European PSD2 standard. Agents may reference PSD2 APIs or UK Open Banking endpoints that do not exist in Israel.
- Bank Leumi, Hapoalim, Discount, Mizrahi-Tefahot, and First International each have different API implementations. There is no single unified API across all Israeli banks.
- Israeli bank account numbers include a branch number (snif) prefix. Agents may validate account numbers using international IBAN format, but Israeli domestic transfers use the local branch+account format.
- Credit card statements in Israel are issued by separate companies (Isracard, Max, CAL) and not directly by the banks. Agents may try to fetch credit card data from the bank API instead of the card company.

## Troubleshooting

### Error: "2FA required"
Cause: Israeli banks require two-factor authentication
Solution: Complete 2FA through your bank's app/SMS when prompted by the MCP server. This is a one-time setup per session.

### Error: "Scraper timeout"
Cause: Bank website slow or blocking automated access
Solution: Retry after a few minutes. If persistent, check israeli-bank-scrapers GitHub issues for known bank-specific issues.

### Error: "Missing credit card transactions"
Cause: Credit card company is separate from bank in Israel
Solution: Add credit card company (Visa Cal, Max, Isracard) as a separate connection in the MCP server configuration.