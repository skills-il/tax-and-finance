---
name: israeli-bank-connector
description: Analyze Israeli bank transactions, spending patterns, and financial data across Israeli banks and credit card companies. Use when user asks about bank transactions, spending analysis, "cheshbon bank", budget tracking, or needs to categorize Israeli banking data. Pairs with israeli-bank-mcp and il-bank-mcp servers (which wrap the israeli-bank-scrapers library) to add financial-analysis workflows. Supports Hapoalim, Leumi, Discount, Mercantile, Mizrahi-Tefahot, First International (FIBI), Otsar HaHayal, Pagi, Union, Yahav, Massad, OneZero, Visa Cal, Max, Isracard, and Amex. Do NOT use for payment initiation, money transfers, or investment advice.
license: MIT
compatibility: Requires israeli-bank-mcp or il-bank-mcp MCP server. Claude Code recommended.
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
| Housing | דיור (diur) | Rent, arnona, vaad bayit |
| Groceries | מזון (mazon) | Shufersal, Rami Levy, Victory |
| Transportation | תחבורה (tahaburah) | Rav-Kav, fuel, Gett |
| Utilities | שירותים (shartuim) | Electric Company, Mekorot, Bezeq |
| Healthcare | בריאות (briut) | Kupat Cholim, pharmacy |
| Education | חינוך (chinuch) | Gan, school, courses |
| Entertainment | בילוי (bilui) | Restaurants, cinema, streaming |
| Insurance | ביטוח (bituach) | Health, car, home insurance |
| Savings | חיסכון (chisachon) | Pension, keren hishtalmut |

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
- `scripts/categorize_transactions.py`, Categorizes Israeli bank transactions by spending category using Israeli-specific merchant pattern matching (Shufersal, Rami Levy, Rav-Kav, etc.). Accepts transaction JSON and outputs categorized spending summaries. Run: `python scripts/categorize_transactions.py --example` for a demo, or `python scripts/categorize_transactions.py --json transactions.json` for real data. Add `--output-json` for machine-readable output.

### References
- `references/spending-categories.md`, Israeli spending category definitions with Hebrew terms and common merchant examples for each category (housing/diur, groceries/mazon, transportation/tahaburah, utilities/shartuim, etc.). Consult when customizing categorization rules or explaining categories to users.
- `references/supported-banks.md`, Full list of 14 banks (Hapoalim, Leumi, Discount, Mercantile, Mizrahi-Tefahot, FIBI, Otsar HaHayal, Pagi, Union, Yahav, Massad, OneZero, Behatsdaa, Beyahad Bishvilha) and 4 credit card companies (Visa Cal, Max, Isracard, Amex) from the `israeli-bank-scrapers` `CompanyTypes` enum, with BOI bank codes, library scraper IDs, and MCP server coverage notes. Consult when setting up bank connections or troubleshooting missing accounts.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| israeli-bank-scrapers (npm library) | https://github.com/eshaham/israeli-bank-scrapers | Authoritative list of supported banks, breaking changes, scraper limitations |
| israeli-bank-mcp (Motti Bechhofer) | https://github.com/mottibec/israeli-bank-mcp | Most comprehensive MCP wrapper; install/config and tool reference |
| il-bank-mcp (Gilad Lekner) | https://github.com/glekner/il-bank-mcp | Docker-based MCP with built-in spending analysis and SQLite storage (less actively maintained, last updated mid-2025; pins an older scraper version) |
| Bank of Israel: Consumer Enquiries | https://www.boi.org.il/en/information-and-service-to-the-public/consumer-enquiries-and-inspections/ | Official BOI Public Inquiries Unit, banking customer service, complaint workflow |
| Bank of Israel: Access to Payment Systems | https://www.boi.org.il/en/economic-roles/supervision-and-regulation/payment-systems-oversight/access-to-payment-systems/ | BOI section that assigns bank identification (participant) codes; codes are being expanded from 2 to 3 digits by end of 2026 |

## Gotchas
- Israel's Open Banking regulation is based on the Berlin Group NextGenPSD2 framework but adapted for Israel with its own timeline and implementation. Full rollout across all banks is still ongoing (as of 2026). Agents may reference UK Open Banking or generic PSD2 endpoints that do not exist in Israel. In practice, israeli-bank-scrapers uses headless browser scraping, not official Open Banking APIs.
- Bank Leumi, Hapoalim, Discount, Mizrahi-Tefahot, and First International each have different API implementations. There is no single unified API across all Israeli banks.
- Mercantile and Otsar HaHayal are SEPARATE scrapers in the upstream library even though they are subsidiaries of Discount and FIBI respectively. Treat them as their own connection (each has its own loginFields shape). Do not assume Discount credentials cover Mercantile or that FIBI credentials cover Otsar HaHayal.
- Transaction history depth is bank-specific. Hapoalim and Leumi typically expose less than 12 months via scraping; FIBI-group banks (FIBI, Otsar HaHayal, Pagi) often expose 12+ months. Treat "up to 12 months" as a ceiling, not a promise.
- Israeli bank account numbers include a branch number (snif) prefix. Agents may validate account numbers using international IBAN format, but Israeli domestic transfers use the local branch+account format.
- Credit card statements in Israel are issued by separate companies (Isracard, Max, CAL) and not directly by the banks. Agents may try to fetch credit card data from the bank API instead of the card company.

## Troubleshooting

### Error: "2FA required"
Cause: the bank login may require two-factor authentication
Solution: Complete 2FA through your bank's app/SMS when prompted by the MCP server. This is a one-time setup per session.

### Error: "Scraper timeout"
Cause: Bank website slow or blocking automated access
Solution: Retry after a few minutes. If persistent, check israeli-bank-scrapers GitHub issues for known bank-specific issues.

### Error: "Missing credit card transactions"
Cause: Credit card company is separate from bank in Israel
Solution: Add credit card company (Visa Cal, Max, Isracard) as a separate connection in the MCP server configuration.