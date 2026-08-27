---
name: shekel-currency-converter
description: Convert currencies to/from Israeli New Shekel (NIS/ILS) using Bank of Israel official representative rates (shaar yatzig). Use when user asks to convert shekels, NIS, ILS, asks about exchange rates, "shaar yatzig" (representative rate), or needs currency conversion for Israeli tax or business purposes. Covers the official Bank of Israel published currencies (14 currencies) with current and historical (tax-date) rates. Do NOT use for cryptocurrency or unofficial money exchange rates.
license: MIT
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
Example object: `{"key":"USD","currentExchangeRate":2.972,"unit":1,"currentChange":-0.47,"lastUpdate":"2026-08-26T12:22:04Z"}`. Here `currentChange` is a percentage daily move, not an absolute NIS delta, and it is NOT used in conversion math.

**Take the rate's date from `lastUpdate`, never from the system clock.** "Most recently published" is not the same as "today". The endpoint keeps serving the previous publication until the next one lands, so any call made before the day's publication returns the PREVIOUS business day's rate. Because the shaar yatzig is date-attributed for tax, stamping it with today's date misstates which day's rate was used, which is exactly the error a tax conversion cannot afford. If a response carries no `lastUpdate`, do not report a date at all: say the publication date could not be established.

**Historical / tax-date rate (SDMX series):**
The JSON endpoint's `?date=` parameter is IGNORED, it always returns the most recently published rate. For a specific past date (the rate that matters for tax), use the Bank of Israel SDMX EXR series instead:
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

**Converting between two FOREIGN currencies is a derived number, not a published rate.** The Bank of Israel publishes a shekel rate per currency and nothing else, so a USD/EUR figure obtained by dividing two shekel rates was never set, published or date-attributed by the Bank of Israel. Label it as derived, never as the shaar yatzig, and for a tax figure translate each foreign amount into shekels against its own representative rate instead of cross-converting. If a dated cross conversion would draw its two legs from different publication days, do not stamp one date on it: quote each leg separately.

Some low-value currencies are published at very coarse precision. The Lebanese pound is published as 0.0003 per 10 units, a single significant figure, which bounds any converted total to roughly plus or minus 17 percent. That published figure is the official representative rate, so it is not wrong to use it, but do not present the converted total as precise to the agora.

Note: Bank of Israel rates express how many NIS per unit(s) of foreign currency.
Example (illustrative; fetch the live/dated rate): USD rate around 2.97, unit = 1 means 1 USD is about 2.97 NIS.
Example (illustrative): JPY rate around 1.87, unit = 100 means 100 JPY is about 1.87 NIS.
Watch the precision on a small-unit currency: the Lebanese pound prints as 0.0000 NIS at four decimal places even though the converted total is correct, so widen the precision rather than reporting a zero rate.

### Step 4: Present Results
Format the result with:
- Converted amount (2 decimal places for NIS, appropriate precision for other currencies)
- Exchange rate used and the date it was PUBLISHED (from `lastUpdate` or the SDMX `TIME_PERIOD`), not the date of the query. If the caller asked for today and today is not published yet, say so explicitly rather than presenting the previous publication as today's rate
- This skill is not a trading feed, not a bank or credit-card conversion rate, and does not cover cryptocurrency. The representative rate is published once per business day for reference and reporting
- Source: "Bank of Israel representative rate (shaar yatzig)"
- Caveat: "Representative rate for reference. Actual bank rates may differ."

### Which date's rate applies (tax)
- **Foreign income:** representative rate on the income accrual / receipt date.
- **Foreign expenses:** representative rate on the payment date.
- **End-of-year revaluation:** the December 31 representative rate for balance-sheet items. This is the books answer; an individual who is not required to keep books is in a different regime, so do not push a private client to report an exchange gain on a personal foreign deposit on this basis.
- **Capital gain on a foreign security or other foreign asset:** TWO different dates, not one. Translate the COST at the representative rate on the acquisition date and the PROCEEDS at the rate on the disposal date, then compute the shekel gain from those two shekel figures. Converting a net foreign-currency gain at a single date is a different, usually understated, number and is the most common error in this whole area.
- **Foreign-currency loan:** translate each event (drawdown, each repayment) at that event's rate rather than converting the balance once at year end; the exchange differences on a business loan are a financing item, not a single annual adjustment.
- **Import VAT (caveat, depends on goods vs. services):**
  - **Imported GOODS** cleared on an import declaration (rashimon): the customs value uses the customs rate (shaar hamekhes), which the Israel Tax Authority publishes weekly and which is NOT the bare representative rate. **Read the published customs rate for the relevant week from the Tax Authority rather than deriving it.** The uplift over the representative rate is commonly cited as 0.5%, but the Tax Authority's exchange-rate service is bot-blocked and cannot be machine-verified from this skill, so treat any derived figure as unconfirmed and quote the published rate instead. Never quote the plain shaar yatzig as the import-VAT rate for goods.
  - **Imported SERVICES** (reverse-charge VAT, e.g. foreign SaaS or overseas contractors): VAT is computed at the PLAIN BOI representative rate on the relevant date, with no customs uplift at all. The customs rate applies only to goods on a rashimon.

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

When the `boi-exchange` MCP is available, use its tools for real-time conversions instead of the static reference tables above. The MCP provides the official representative rate (shaar yatzig) which is the rate Israeli tax rules require for the transaction date.

## Gotchas
- The official NIS currency code is ILS (ISO 4217), but Israelis colloquially say "shekel" or "shekalim". Agents may not recognize "NIS" as a valid currency code or confuse it with the pre-1985 "Old Shekel" (IS).
- Bank of Israel publishes ONE representative rate per currency per day (no separate buy/sell rates), Monday to Thursday soon after 15:15 and Friday (and holiday eves) soon after 12:15. No rate is set on Saturday, Sunday, or Israeli holidays. Agents may fetch a rate before publication time and get the previous publication's rate without indicating it is stale.
- Only the official Bank of Israel published currencies have a representative rate (currently 14: USD, GBP, JPY, EUR, AUD, CAD, DKK, NOK, ZAR, SEK, CHF, JOD, LBP, EGP). The skill is not a general FX converter for every world currency.
- NIS formatting uses the shekel sign before the number, with comma for thousands and period for decimals (e.g., 1,234.56). Agents may use the European convention (1.234,56) or place the symbol after the number.
- When converting for tax purposes, Israeli law requires using the BOI representative rate (sha'ar yatzig) for the specific transaction date, not a live forex rate. For import VAT on goods use the weekly customs rate published by the Tax Authority; imported services (reverse-charge VAT) use the plain representative rate. Agents may use real-time rates that are not legally valid for tax reporting.

## Troubleshooting

### Error: "Rate not available for date"
Cause: Requested date is Saturday, Sunday, an Israeli holiday, or a future date.
Solution: Use the most recent published date on or before the requested date from the SDMX series. Bank of Israel publishes rates Monday to Thursday (soon after 15:15) and Friday (soon after 12:15), not on Saturday, Sunday, or holidays.

### Error: "Currency not supported"
Cause: Bank of Israel does not publish a representative rate for this currency (only the 14 listed currencies are covered).
Solution: Suggest using USD or EUR as an intermediate currency for conversion.
