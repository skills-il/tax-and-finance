---
name: israeli-bank-connector
description: Analyze Israeli bank transactions, spending patterns, and financial data across Israeli banks and credit card companies. Use when user asks about bank transactions, spending analysis, "cheshbon bank", budget tracking, or needs to categorize Israeli banking data. Pairs with israeli-bank-mcp and il-bank-mcp servers (which wrap the israeli-bank-scrapers library) to add financial-analysis workflows. Supports Hapoalim, Leumi, Discount, Mercantile, Mizrahi-Tefahot, First International (FIBI), Otsar HaHayal, Pagi, Union, Yahav, Massad, OneZero, Behatsdaa, Beyahad Bishvilha, Visa Cal, Max, Isracard, and Amex. Do NOT use for payment initiation, money transfers, or investment advice.
license: MIT
compatibility: Requires israeli-bank-mcp or il-bank-mcp MCP server. Claude Code recommended.
---

# Israeli Bank Connector

## Instructions

### Step 1: Identify Connected Banks
Check which MCP server is available and what accounts are connected:
- israeli-bank-mcp: direct scraper integration
- il-bank-mcp: Docker-based with persistent analysis
- If no MCP: guide the user through a CSV or Excel export from the bank website

**Neither MCP is installable with `npx`.** `israeli-bank-mcp` is not published to npm and
declares no `bin`, so any instruction to run `npx israeli-bank-mcp` is wrong and will fail.
The real shapes, taken from each repository:

| Server | How it is actually installed and run |
|---|---|
| `israeli-bank-mcp` | Clone the repo, `npm install`, `npm run build`, then point the MCP client at `node /path/to/israeli-bank-mcp/build/server.js` |
| `il-bank-mcp` | Docker. `docker compose up -d` with the bank env vars set, and the client runs `docker compose -f /path/to/il-bank-mcp/docker-compose.yml run --rm -i mcp-server` |

**Node 22 or newer is required for the MCP servers, and Python 3.9 or newer for the bundled script.** `israeli-bank-scrapers` declares `engines.node >= 22.22.2`.
On an older Node the install or the run fails before any bank is ever contacted, and the
error will not mention the bank. Check `node --version` first when a user reports that
nothing works at all.

**`israeli-bank-mcp` exposes two tools and one resource, and that is the whole surface**:
`fetch-transactions`, `two-factor-auth`, and the `banks://list` resource that reports which
credential fields each bank needs. Everything in Steps 3 to 5 below is work the agent does
on the returned data. Do not expect the server to categorize, total, or export anything.

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

**Do not report money moved into savings as spending.** A pension contribution, keren
hishtalmut deposit or gemel transfer is the user's own money changing pocket, not an
expense. The script reports three figures for this reason: Total Spending (excluding
savings), Into Savings, and Total Outflow (the two combined). Quoting the outflow figure
as "you spent X" overstates spending by whatever the user is putting away, which for a
typical Israeli salary deduction is a substantial share.

**Categorisation is keyword matching, so review it before presenting it as fact.** The
script matches merchant descriptions against Hebrew and English keyword patterns, guarded on
both scripts so a pattern matches a whole token rather than a fragment: Hebrew-letter
lookbehind so `פז` does not fire inside `פזגז`, and Latin-letter guards on both sides so
`hot` does not fire inside `Hotel` or `PHOTO`. Hebrew one-letter prefixes are handled by
matching a de-prefixed copy of each token as well, which is why `הפקדה לפנסיה` reaches the
savings rule; without that the guard blocks the most natural Hebrew phrasing and files a
pension deposit as an insurance expense.

**Misclassifications remain, and this is a CLASS of failure, not a fixed list.** Any Hebrew
merchant string that contains a pattern token as a real word will match it: a mall called
קניון מגדל שלום matches the insurer מגדל, and מלון הוט matches the cable company הוט. Those
two are named because they are common, not because they are the only ones. Show the user the
category breakdown and invite corrections rather than asserting it is their spending, and
never present a category total as a fact about the person without them having seen the rows
behind it.

**Money coming in is not netted off spending, and no net view is offered.** Any positive
amount, whether a refund, a reversal, a salary, a transfer in or a loan drawdown, is reported
on its own `Credits In` line and excluded from every category total and every percentage.
Nothing in the data distinguishes a refund from a salary, so a "net" figure built from that
bucket subtracts the user's salary from a spending category and reports a negative total. If
the user wants refunds netted, net the specific rows they point at, by hand. Check the sign
convention of your source first: a feed that reports every line as positive produces an empty
spending total.

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
- `scripts/categorize_transactions.py`, Categorizes Israeli bank transactions by spending category using Israeli-specific merchant pattern matching (Shufersal, Rami Levy, Rav-Kav, etc.). Accepts transaction JSON and outputs categorized spending summaries. Run: `python3 scripts/categorize_transactions.py --example` for a demo, or `python3 scripts/categorize_transactions.py --json transactions.json` for real data. Add `--output-json` for machine-readable output.

### References
- `references/spending-categories.md`, Israeli spending category definitions with Hebrew terms and common merchant examples for each category (housing/diur, groceries/mazon, transportation/tahaburah, utilities/shartuim, etc.). Consult when customizing categorization rules or explaining categories to users.
- `references/supported-banks.md`, Full list of 14 banks (Hapoalim, Leumi, Discount, Mercantile, Mizrahi-Tefahot, FIBI, Otsar HaHayal, Pagi, Union, Yahav, Massad, OneZero, Behatsdaa, Beyahad Bishvilha) and 4 credit card companies (Visa Cal, Max, Isracard, Amex) from the `israeli-bank-scrapers` `CompanyTypes` enum, with BOI bank codes, library scraper IDs, and MCP server coverage notes. Consult when setting up bank connections or troubleshooting missing accounts.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| israeli-bank-scrapers (npm library) | https://github.com/eshaham/israeli-bank-scrapers | Authoritative list of supported banks, breaking changes, scraper limitations |
| israeli-bank-scrapers on npm | https://registry.npmjs.org/israeli-bank-scrapers | Current release, and the `engines.node` floor. Latest is 6.9.0 (2026-07-22), Node >= 22.22.2 |
| israeli-bank-mcp (Motti Bechhofer) | https://github.com/mottibec/israeli-bank-mcp | The more current MCP wrapper (last pushed May 2026). Not on npm: clone and build. Its README bank list is stale, but the server iterates the library's `SCRAPERS` map, so it covers whatever the installed library covers |
| il-bank-mcp (Gilad Lekner) | https://github.com/glekner/il-bank-mcp | Docker-based MCP with built-in spending analysis and SQLite storage. Last pushed June 2025. Its `packages/scraper` declares `israeli-bank-scrapers ^6.1.4`, a low floor rather than a hard pin, so a fresh build still resolves to the current release; a committed lockfile or a stale image is what actually freezes it |
| Bank of Israel: Consumer Enquiries | https://www.boi.org.il/en/information-and-service-to-the-public/consumer-enquiries-and-inspections/ | Official BOI Public Inquiries Unit, banking customer service, complaint workflow |
| Bank of Israel: Access to Payment Systems | https://www.boi.org.il/en/economic-roles/supervision-and-regulation/payment-systems-oversight/access-to-payment-systems/ | Payment-system access terms. NOTE: rendered in a browser on 27 August 2026 this is a landing page last updated 19/11/2023 with no identification-code list, so do not cite it for bank codes |

## Handling credentials and transaction data

This skill sits on top of a scraper that takes live Israeli bank usernames, passwords and
one-time codes, and it produces a complete transaction history. Treat both as sensitive.

- Credentials belong in the MCP server's own configuration or environment, never in the
  chat, never in a file you create, and never in a command you echo back to the user.
- `israeli-bank-mcp` reads credentials from environment variables and deliberately never
  from tool arguments, precisely so they do not end up in the LLM conversation history. Its
  variable names are derived from the bank id and the login field by camelCase-to-upper-snake,
  so `leumi` plus `username` gives `LEUMI_USERNAME`, and `otsarHahayal` plus `username` gives
  `OTSAR_HAHAYAL_USERNAME`. Ask the `banks://list` resource which fields a given bank needs
  rather than guessing, because the shape differs per bank (Hapoalim wants a usercode, not a
  username). If a bank fails with a missing-credential error, it names the exact variables.
- Do not print, log, or repeat a credential, an OTP, or a card number, even partially, and
  do not ask the user to paste one into the conversation.
- Do not persist raw transaction dumps beyond what the current task needs, and tell the
  user where anything you do write is stored. Note that `il-bank-mcp` keeps scraped data in
  a local SQLite database, so the history outlives the session by design.
- Transaction descriptions reveal health providers, political donations, and religious
  institutions. Summarise; do not volunteer inferences about the person from their
  spending.

## Gotchas
- The operational point, which IS load-bearing: `israeli-bank-scrapers` uses headless browser scraping, not an official Open Banking API, and agents routinely reach for UK Open Banking or generic PSD2 endpoints that do not exist in Israel. Israel's own open-banking regime is reported to derive from the Berlin Group NextGenPSD2 framework on its own timeline, but that characterisation is **unverified in this skill** and should not be repeated to a user as fact.
- Bank Leumi, Hapoalim, Discount, Mizrahi-Tefahot, and First International each have different API implementations. There is no single unified API across all Israeli banks.
- Mercantile and Otsar HaHayal are SEPARATE scrapers in the upstream library even though they are subsidiaries of Discount and FIBI respectively. Treat them as their own connection (each has its own loginFields shape). Do not assume Discount credentials cover Mercantile or that FIBI credentials cover Otsar HaHayal.
- Transaction history depth is bank-specific and this skill does not have a sourced table of it. Reports put Hapoalim and Leumi below 12 months and the FIBI group at 12 or more, but that is **unverified**. Treat "up to 12 months" as a ceiling, never a promise, and tell the user what the scrape actually returned rather than what you expected.
- What the library can retrieve depends on the installed version, so pin before you debug. As of `israeli-bank-scrapers` 6.9.0 (2026-07-22) Leumi exposes savings accounts and Max exposes credit card balances; neither existed in the 6.7.x line. If a user reports a missing Leumi savings account or a missing Max balance, check the version before assuming the scrape failed. Anything older than 6.7.10 will also fail outright on Max (login page) and Isracard (bot detection) rather than just return less.
- Both MCP wrappers declare the scraper as a caret range (`^6.7.3` and `^6.1.4`), not a hard
  pin, so a fresh install resolves to the current release. What actually freezes a user on an
  old scraper is a committed lockfile or a stale Docker image, so check the INSTALLED version
  rather than the declared range when you are diagnosing a capability gap.
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