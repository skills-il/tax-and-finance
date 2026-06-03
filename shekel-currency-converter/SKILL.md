---
name: shekel-currency-converter
description: Convert currencies to/from Israeli New Shekel (NIS/ILS) using Bank of Israel official representative rates (shaar yatzig). Use when user asks to convert shekels, NIS, ILS, asks about exchange rates, "shaar yatzig" (representative rate), or needs currency conversion for Israeli tax or business purposes. Covers the official Bank of Israel published currencies (14 currencies) with current and historical (tax-date) rates. Do NOT use for cryptocurrency or unofficial money exchange rates.
license: MIT
version: 2.0.0
allowed-tools: Bash(python:*) WebFetch
compatibility: Requires network access for Bank of Israel API. Works with Claude Code, Claude.ai, Cursor.
---

# Shekel Currency Converter

## Instructions

### Step 1: Identify Conversion Request
Parse the user's request for:
- **Source currency** and **target currency** (at least one should be NIS/ILS)
- **Amount** to convert
- **Date** (current or specific historical date, important for tax conversions)
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

**Current rate (live JSON endpoint):**
The legacy XML feed at `currency.xml` is gone (it now redirects to the JSON API), so do NOT parse XML. Fetch the JSON endpoint and read the `exchangeRates` array.
```
Fetch: https://www.boi.org.il/PublicApi/GetExchangeRates
Parse JSON: response.exchangeRates is an array of objects.
Each object: key (currency code), currentExchangeRate (NIS per "unit"),
             unit (1, 10, or 100), currentChange (percent move vs. previous
             publication), lastUpdate (ISO timestamp).
```
Example object: `{"key":"USD","currentExchangeRate":2.872,"unit":1,"currentChange":1.66,"lastUpdate":"..."}`. Here `currentChange` is a percentage daily move, not an absolute NIS delta, and it is NOT used in conversion math.

**Historical / tax-date rate (SDMX series):**
The JSON endpoint's `?date=` parameter is IGNORED, it always returns today's rate. For a specific past date (the rate that matters for tax), use the Bank of Israel SDMX EXR series instead:
```
Fetch: https://edge.boi.gov.il/FusionEdgeServer/sdmx/v2/data/dataflow/BOI.STATISTICS/EXR/1.0/RER_<CUR>_ILS?startPeriod=YYYY-MM-DD&endPeriod=YYYY-MM-DD&format=csv
Replace <CUR> with the currency code (e.g., RER_USD_ILS, RER_EUR_ILS).
Parse CSV: read OBS_VALUE keyed by TIME_PERIOD.
```
The series omits non-publication days (Saturday, Sunday, holidays). If there is no row for the exact requested date, walk back to the most recent published date on or before it, and tell the user which date's rate you used.

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
Example (illustrative; fetch the live/dated rate): USD rate around 2.87, unit = 1 means 1 USD is about 2.87 NIS.
Example (illustrative): JPY rate around 1.80, unit = 100 means 100 JPY is about 1.80 NIS.

### Step 4: Present Results
Format the result with:
- Converted amount (2 decimal places for NIS, appropriate precision for other currencies)
- Exchange rate used and its date
- Source: "Bank of Israel representative rate (shaar yatzig)"
- Caveat: "Representative rate for reference. Actual bank rates may differ."

### Which date's rate applies (tax)
- **Foreign income:** representative rate on the income accrual / receipt date.
- **Foreign expenses:** representative rate on the payment date.
- **End-of-year revaluation:** the December 31 representative rate for balance-sheet items.
- **Import VAT (caveat):** import VAT and customs are NOT computed at the bare BOI representative rate. Customs value uses the customs rate (shaar hamekhes), which the Israel Tax Authority sets weekly on the import declaration (rashimon) and is based on the BOI representative rate plus 0.5%. Do not quote the plain shaar yatzig as the import-VAT rate.

## Examples

### Example 1: Simple USD to NIS
User says: "Convert 1000 dollars to shekels"
Result: "1,000 USD = X NIS (at the live Bank of Israel representative rate; fetch the dated rate before quoting a figure)."

### Example 2: Historical Rate
User says: "What was the dollar rate on January 1, 2026?"
Result: Fetch the SDMX RER_USD_ILS series. Jan 1, 2026 is a non-publication day, so report the most recent published date on or before it (the first 2026 observation is Jan 2, 2026) and say which date you used.

### Example 3: Tax-Relevant Rate
User says: "I need the EUR rate for my VAT report for December 2025"
Result: Provides the representative rate for the relevant transaction date from the SDMX series, noting it is the official rate for tax purposes. For import VAT specifically, point the user to the weekly customs rate.

## Bundled Resources

### Scripts
- `scripts/fetch_rates.py` - Fetches official Bank of Israel representative exchange rates (shaar yatzig) and performs currency conversions to/from NIS. Uses the live JSON endpoint for current rates and the SDMX EXR series for historical date lookups (with publication-day walk-back). On a fetch failure it fails loud (prints an error, exits non-zero) and never substitutes sample rates for a real conversion; illustrative sample output is only available behind the explicit `--demo` flag. Run: `python scripts/fetch_rates.py --help`

### References
- `references/boi-api-guide.md` - Bank of Israel exchange rate API documentation: the live JSON endpoint and its fields, the SDMX EXR historical series, update schedule, and the import-VAT customs-rate caveat. Consult when troubleshooting API calls or understanding rate publication timing.
- `references/currency-codes.md` - Supported currency codes with Hebrew names, typical NIS rate ranges, and unit values (important for JPY and other multi-unit currencies). Consult when parsing user currency requests or handling unit-based conversions.

## Reference Links

| Resource | URL |
|----------|-----|
| BOI exchange rates page | https://www.boi.org.il/en/economic-roles/financial-markets/exchange-rates/ |
| Live JSON rates endpoint | https://www.boi.org.il/PublicApi/GetExchangeRates |
| BOI SDMX EXR historical series | https://edge.boi.gov.il/FusionEdgeServer/sdmx/v2/data/dataflow/BOI.STATISTICS/EXR/1.0/RER_USD_ILS |

## Recommended MCP Servers

For live exchange rate data, pair this skill with:

| MCP Server | What it provides | Install |
|------------|-----------------|---------|
| **boi-exchange** | Official Bank of Israel daily representative rates (sha'ar yatzig) for the published currencies, historical rate series, rate change calculations, and direct currency conversion via BOI SDMX API. No API key required. | [Install boi-exchange](https://agentskills.co.il/en/mcp/boi-exchange) |

When the `boi-exchange` MCP is available, use its tools for real-time conversions instead of the static reference tables above. The MCP provides the official representative rate (shaar yatzig) which is the legally binding rate for tax purposes.

## Gotchas
- The official NIS currency code is ILS (ISO 4217), but Israelis colloquially say "shekel" or "shekalim". Agents may not recognize "NIS" as a valid currency code or confuse it with the pre-1985 "Old Shekel" (IS).
- Bank of Israel publishes ONE representative rate per currency per day (no separate buy/sell rates), Monday to Thursday soon after 15:15 and Friday (and holiday eves) soon after 12:15. No rate is set on Saturday, Sunday, or Israeli holidays. Agents may fetch a rate before publication time and get the previous publication's rate without indicating it is stale.
- Only the official Bank of Israel published currencies have a representative rate (currently 14: USD, GBP, JPY, EUR, AUD, CAD, DKK, NOK, ZAR, SEK, CHF, JOD, LBP, EGP). The skill is not a general FX converter for every world currency.
- NIS formatting uses the shekel sign before the number, with comma for thousands and period for decimals (e.g., 1,234.56). Agents may use the European convention (1.234,56) or place the symbol after the number.
- When converting for tax purposes, Israeli law requires using the BOI representative rate (sha'ar yatzig) for the specific transaction date, not a live forex rate. For import VAT use the weekly customs rate, not the bare representative rate. Agents may use real-time rates that are not legally valid for tax reporting.

## Troubleshooting

### Error: "Rate not available for date"
Cause: Requested date is Saturday, Sunday, an Israeli holiday, or a future date.
Solution: Use the most recent published date on or before the requested date from the SDMX series. Bank of Israel publishes rates Monday to Thursday (soon after 15:15) and Friday (soon after 12:15), not on Saturday, Sunday, or holidays.

### Error: "Currency not supported"
Cause: Bank of Israel does not publish a representative rate for this currency (only the 14 listed currencies are covered).
Solution: Suggest using USD or EUR as an intermediate currency for conversion.
