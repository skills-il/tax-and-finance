# Supported Israeli Banks and Credit Card Companies

Authoritative list reflects the `CompanyTypes` enum in [eshaham/israeli-bank-scrapers](https://github.com/eshaham/israeli-bank-scrapers/blob/master/src/definitions.ts). The library is the foundation for both `israeli-bank-mcp` and `il-bank-mcp`. Library version pin: `israeli-bank-scrapers >=6.7.x` (current release 6.7.8, 2026-06-15).

BOI Code column shows Bank of Israel identification codes from the [BOI identification-code page](https://www.boi.org.il/en/economic-roles/supervision-and-regulation/payment-systems-oversight/access-to-payment-systems/). `-` means no separately-assigned BOI code (the entity shares a parent's code or is not listed as an independent payment-system participant). Note: BOI is expanding identification codes from 2 to 3 digits, with implementation by the end of December 2026, so these 2-digit codes may change format.

## Banks

| Bank | Hebrew | BOI Code | israeli-bank-scrapers ID | Notes |
|------|--------|----------|--------------------------|-------|
| Bank Hapoalim | bank hapoalim | 12 | `hapoalim` | Largest bank |
| Bank Leumi | bank leumi | 10 | `leumi` | Second largest |
| Israel Discount Bank | bank discount | 11 | `discount` | Separate scraper from Mercantile |
| Mercantile Bank | bank mercantile | 17 | `mercantile` | Separate scraper (own loginFields: id, password, num); subsidiary of Discount but not subsumed |
| Mizrahi-Tefahot | mizrahi tefahot | 20 | `mizrahi` | Fourth largest |
| FIBI (First International) | benleumi rishon | 31 | `beinleumi` | Separate scraper from Otsar HaHayal |
| Bank Otsar Hahayal | bank otsar hahayal | 14 | `otsarHahayal` | Separate scraper (own loginFields: username, password); part of FIBI group but not subsumed |
| Pagi Bank | bank pagi | 52 | `pagi` | Charedi-focused, part of FIBI group, separate scraper |
| Union Bank | bank igud | 13 | `union` | Acquired by Mizrahi-Tefahot in 2020 but still listed as separate BOI participant and separate scraper |
| Bank Yahav | bank yahav | 04 | `yahav` | Public-sector employees, owned by Hapoalim |
| Bank Massad | bank masad | 46 | `massad` | Teachers/education sector |
| OneZero Digital Bank | onezero | 18 | `oneZero` | Israel's first all-digital bank (launched 2022) |
| Behatsdaa | bank behatsdaa | - | `behatsdaa` | Smaller institutional scraper |
| Beyahad Bishvilha | beyahad bishvilha | - | `beyahadBishvilha` | Smaller institutional scraper |

## Credit Card Companies

| Company | Hebrew | israeli-bank-scrapers ID | Notes |
|---------|--------|--------------------------|-------|
| Visa Cal (CAL) | visa cal | `visaCal` | Visa/Mastercard/Diners. Verify current ownership against Bank of Israel filings; card-issuer ownership has been shifting under BOI competition rulings |
| Max (formerly Leumi Card) | max | `max` | Mastercard/Visa |
| Isracard | isracard | `isracard` | Isracard/Mastercard |
| American Express Israel | amex | `amex` | Amex cards (issued via Isracard) |

## MCP Server Coverage

Not every scraper in the upstream library is exposed by every MCP wrapper. Check the specific MCP's tool list before assuming an account is reachable.

### israeli-bank-mcp (Motti Bechhofer)
- Most comprehensive coverage of upstream library
- Directly wraps `israeli-bank-scrapers`
- Supports 2FA
- Active maintenance
- Repo: <https://github.com/mottibec/israeli-bank-mcp>

### il-bank-mcp (Gilad Lekner)
- Docker-based deployment
- Adds transaction analysis features (spending breakdowns, recurring charge detection)
- Uses SQLite for local data storage
- Best when running headless / serverless via the puppeteer-core variant
- Repo: <https://github.com/glekner/il-bank-mcp>

## Authentication Notes
- Most Israeli bank logins may require 2FA (two-factor authentication); OneZero notably uses an OTP/token setup. israeli-bank-scrapers handles the prompt when it appears
- Bank scrapers use headless browser automation
- Sessions expire after ~15-30 minutes
- Some banks may temporarily block automated access
- Rate limiting varies by bank

## Data Available
- Account balances
- Transaction history (bank-dependent window; Hapoalim and Leumi typically expose shorter than 12 months, FIBI group exposes 12+ months)
- Credit card transactions
- Standing orders
- Loan information (limited)
