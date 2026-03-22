---
name: shekel-currency-converter
description: >-
  Convert currencies to/from Israeli New Shekel (NIS/ILS) using Bank of Israel
  official exchange rates. Use when user asks to convert shekels, NIS, ILS, asks
  about exchange rates, "shaar yatzig" (representative rate), or needs currency
  conversion for Israeli tax or business purposes. Supports 30+ currencies with
  current and historical rates. Do NOT use for cryptocurrency or unofficial
  money exchange rates.
license: MIT
allowed-tools: 'Bash(python:*) WebFetch'
compatibility: >-
  Requires network access for Bank of Israel API. Works with Claude Code,
  Claude.ai, Cursor.
metadata:
  author: skills-il
  version: 1.1.0
  category: tax-and-finance
  tags:
    he:
      - מטבע
      - שקל
      - ש״ח
      - שער-חליפין
      - בנק-ישראל
    en:
      - currency
      - shekel
      - nis
      - exchange-rate
      - bank-of-israel
  display_name:
    he: ממיר מטבע שקל
    en: Shekel Currency Converter
  display_description:
    he: המרת מטבעות בזמן אמת מול בנק ישראל עם תמיכה בכל המטבעות
    en: >-
      Convert currencies to/from Israeli New Shekel (NIS/ILS) using Bank of
      Israel official exchange rates. Use when user asks to convert shekels,
      NIS, ILS, asks about exchange rates, "shaar yatzig" (representative rate),
      or needs currency conversion for Israeli tax or business purposes.
      Supports 30+ currencies with current and historical rates. Do NOT use for
      cryptocurrency or unofficial money exchange rates.
  supported_agents:
    - claude-code
    - cursor
    - github-copilot
    - windsurf
    - opencode
---

# Shekel Currency Converter

## Instructions

### Step 1: Identify Conversion Request
Parse the user's request for:
- **Source currency** and **target currency** (at least one should be NIS/ILS)
- **Amount** to convert
- **Date** (current or specific historical date)
- **Purpose** (general info vs. tax-relevant representative rate)

Common currency codes:
| Code | Currency | Hebrew |
|------|----------|--------|
| ILS | Israeli New Shekel | shekel chadash |
| USD | US Dollar | dolar |
| EUR | Euro | euro |
| GBP | British Pound | lira sterling |
| JPY | Japanese Yen | yen |
| CHF | Swiss Franc | frank shveitzi |

### Step 2: Fetch Exchange Rate
Use Bank of Israel API to get the rate:

**Current rate:**
```
Fetch: https://boi.org.il/currency.xml
Parse XML for the requested currency code
Extract: rate, unit, change from previous day
```

**Historical rate:**
```
Fetch: https://boi.org.il/PublicApi/GetExchangeRates?date=YYYY-MM-DD
Parse response for requested currency
Note: Rates not available for Shabbat/holidays -- use last available business day
```

### Step 3: Calculate Conversion
```
If converting FROM NIS:
  result = amount / rate * unit

If converting TO NIS:
  result = amount * rate / unit

If converting between two foreign currencies:
  nis_amount = amount * rate_source / unit_source
  result = nis_amount / rate_target * unit_target
```

Note: Bank of Israel rates express how many NIS per unit(s) of foreign currency.
Example: USD rate = 3.65, unit = 1 means 1 USD = 3.65 NIS.
JPY rate = 2.45, unit = 100 means 100 JPY = 2.45 NIS.

### Step 4: Present Results
Format the result with:
- Converted amount (2 decimal places for NIS, appropriate precision for other currencies)
- Exchange rate used and its date
- Source: "Bank of Israel representative rate (shaar yatzig)"
- Change from previous day (if available)
- Caveat: "Representative rate for reference. Actual bank rates may differ."

## Examples

### Example 1: Simple USD to NIS
User says: "Convert 1000 dollars to shekels"
Result: "1,000 USD = 3,650.00 NIS (at Bank of Israel rate of 3.6500, published Feb 24, 2026)"

### Example 2: Historical Rate
User says: "What was the dollar rate on January 1, 2026?"
Result: "USD/ILS representative rate on Jan 1, 2026: 3.5800 (Bank of Israel shaar yatzig)"

### Example 3: Tax-Relevant Rate
User says: "I need the EUR rate for my VAT report for December 2025"
Result: Provides the representative rate for the relevant date, noting it is the official rate for tax purposes.

## Bundled Resources

### Scripts
- `scripts/fetch_rates.py` — Fetches official Bank of Israel representative exchange rates (shaar yatzig) and performs currency conversions to/from NIS. Supports current rates, historical date lookups, and listing all available currencies. Run: `python scripts/fetch_rates.py --help`

### References
- `references/boi-api-guide.md` — Bank of Israel exchange rate API documentation including endpoints, XML response structure, update schedule (daily ~15:30 IST), and historical rate query parameters. Consult when troubleshooting API calls or understanding rate publication timing.
- `references/currency-codes.md` — Supported currency codes with Hebrew names, typical NIS rate ranges, and unit values (important for JPY and other multi-unit currencies). Consult when parsing user currency requests or handling unit-based conversions.

## Gotchas
- The official NIS currency code is ILS (ISO 4217), but Israelis colloquially say "shekel" or "shekalim". Agents may not recognize "NIS" as a valid currency code or confuse it with the pre-1985 "Old Shekel" (IS).
- Bank of Israel exchange rates are published once daily at ~15:30. Agents may fetch rates before publication time and get yesterday's rate without indicating it is stale.
- NIS formatting uses the shekel sign before the number, with comma for thousands and period for decimals (e.g., 1,234.56). Agents may use the European convention (1.234,56) or place the symbol after the number.
- When converting for tax purposes, Israeli law requires using the BOI representative rate (sha'ar yatzig) for the specific transaction date, not a live forex rate. Agents may use real-time rates that are not legally valid for tax reporting.

## Troubleshooting

### Error: "Rate not available for date"
Cause: Requested date is Shabbat, holiday, or future date
Solution: Use the last available business day rate. Bank of Israel publishes rates Sunday-Thursday.

### Error: "Currency not supported"
Cause: Bank of Israel does not publish a rate for this currency
Solution: Suggest using USD or EUR as intermediate currency for conversion.