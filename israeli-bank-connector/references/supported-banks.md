# Supported Israeli Banks and Credit Card Companies

Authoritative list reflects the `CompanyTypes` enum in [eshaham/israeli-bank-scrapers](https://github.com/eshaham/israeli-bank-scrapers/blob/master/src/definitions.ts). The library is the foundation for both `israeli-bank-mcp` and `il-bank-mcp`. Library version pin: `israeli-bank-scrapers >=6.9.x` (current release 6.9.0, 2026-07-22, re-verified against the npm registry on 27 August 2026). The package declares `engines.node >= 22.22.2`, so Node 22 or newer is a hard requirement and an older Node fails before any bank is contacted.

Two capabilities landed in 6.9.0 that change what you can retrieve, so an older pin will
silently return less than the user expects: Leumi now exposes **savings accounts**, and Max
now exposes **credit card balances**. If a user says a Leumi savings account or a Max
balance is missing, check the installed version before debugging the scrape. 6.8.0
completed the Visa Cal frame implementation, and 6.7.9/6.7.10 fixed a Max login-page
failure and an Isracard bot-detection workaround, so anything older than 6.7.10 is likely
to fail outright on those two providers rather than merely return less.

BOI Code column shows Bank of Israel bank identification codes. `-` means no separately-assigned code (the entity shares a parent's code or is not listed as an independent payment-system participant). **Sourcing caveat, added 27 August 2026:** the BOI page previously cited for this column ([Access to Payment Systems](https://www.boi.org.il/en/economic-roles/supervision-and-regulation/payment-systems-oversight/access-to-payment-systems/)) was rendered in a browser this cycle and is a landing page last updated 19/11/2023 that does not contain an identification-code list at all. The codes below are the conventional two-digit Israeli bank numbers and are useful for recognising a bank, but they are **not verified against a BOI publication in this skill**, and the previously-stated expansion from two to three digits by the end of December 2026 is likewise unverified and has been withdrawn as a factual claim. Never use a code from this table to construct a payment instruction; take it from the bank or from a current BOI publication.

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
- Directly wraps `israeli-bank-scrapers`. Declares `israeli-bank-scrapers ^6.7.3`, a floor rather than a hard pin, so a fresh install resolves to the current release.
- **Coverage tracks the library, not its own README.** Its README bank list omits Pagi, but the server calls `SCRAPERS[bankId]` from the library rather than carrying a hardcoded list, so every entry in `CompanyTypes` is reachable. Do not treat the README omission as a coverage gap; it has been re-raised as one before.
- Two tools (`fetch-transactions`, `two-factor-auth`) and one resource (`banks://list`). It fetches. It does not analyse.
- Supports 2FA.
- **Not published to npm** (the registry returns 404) and declares no `bin`, so it cannot be run with `npx`. Clone, `npm install`, `npm run build`, then run `node build/server.js`.
- Credentials come from environment variables only, never from tool arguments, so they stay out of the conversation history. Names are `<BANK_ID>_<FIELD>` derived by camelCase-to-upper-snake: `LEUMI_USERNAME`, `OTSAR_HAHAYAL_USERNAME`, `HAPOALIM_USERCODE`.
- Last pushed May 2026.
- Repo: <https://github.com/mottibec/israeli-bank-mcp>

### il-bank-mcp (Gilad Lekner)
- Docker-based deployment: `docker compose up -d` with the bank env vars set, and the MCP client runs `docker compose -f /path/to/il-bank-mcp/docker-compose.yml run --rm -i mcp-server`
- A monorepo: the scraper dependency lives in `packages/scraper`, which declares `israeli-bank-scrapers ^6.1.4`. That is a low floor, not a hard pin, so a fresh build still resolves to the current release. A stale image or a committed lockfile is what actually freezes it.
- Last pushed June 2025
- Adds transaction analysis features (spending breakdowns, recurring charge detection)
- Uses SQLite for local data storage
- Best when running headless / serverless via the puppeteer-core variant
- Repo: <https://github.com/glekner/il-bank-mcp>

## Sourcing note on the Notes column and the operational figures below

The Notes column carries background context (ownership, sector, launch dates) and the
Authentication and Data sections carry operational figures (session lifetimes, per-bank
history depth). **None of that is verified against a primary source in this skill**, and it
is recorded here so the next cycle does not mistake it for sourced fact. What IS verified is
the scraper id column, which is diffed row by row against the library's `CompanyTypes` enum
each cycle. Treat everything else in this file as orientation, and confirm anything
load-bearing with the bank or with the upstream repository's issues.

## Authentication Notes
- Most Israeli bank logins may require 2FA (two-factor authentication); OneZero notably uses an OTP/token setup. israeli-bank-scrapers handles the prompt when it appears
- Bank scrapers use headless browser automation
- Sessions expire after a short window, commonly reported as roughly 15 to 30 minutes. Unverified; treat as an order of magnitude, not a limit to design against
- Some banks may temporarily block automated access
- Rate limiting varies by bank

## Data Available
- Account balances
- Transaction history. The window is bank-dependent and the per-bank depths reported here (Hapoalim and Leumi shorter than 12 months, FIBI group 12 or more) are **unverified**: check what the scrape actually returns rather than promising a window
- Credit card transactions
- Standing orders
- Loan information (limited)
