# Bank of Israel Exchange Rate API Guide

## Current Rates (live JSON endpoint)
- **URL:** `https://www.boi.org.il/PublicApi/GetExchangeRates`
- **Method:** GET (no authentication required)
- **Format:** JSON
- **Update time:** Monday to Thursday soon after 15:15 Israel time; Friday and holiday eves soon after 12:15. No rate on Saturday, Sunday, or Israeli holidays.

The legacy XML feed at `https://www.boi.org.il/currency.xml` no longer serves XML. It now redirects to the JSON endpoint above, so do NOT try to parse XML.

## JSON Response Structure
```json
{
  "exchangeRates": [
    {
      "key": "USD",
      "currentExchangeRate": 2.872,
      "currentChange": 1.66,
      "unit": 1,
      "lastUpdate": "2026-06-03T12:22:02Z"
    }
  ]
}
```

Fields:
- `key` - currency code (e.g., USD, EUR, JPY).
- `currentExchangeRate` - NIS per `unit` of the foreign currency.
- `unit` - number of foreign-currency units the rate is quoted per (1 for most, 100 for JPY, 10 for LBP).
- `currentChange` - percentage move versus the previous publication (a percent, NOT an absolute NIS delta). Not used in conversion math.
- `lastUpdate` - ISO timestamp of when the rates were set.

## Historical Rates (SDMX EXR series)
The JSON endpoint's `?date=` parameter is ignored: it always returns the latest rate regardless of the date supplied. For a specific historical date (the rate that matters for tax), use the Bank of Israel SDMX EXR series.

- **URL pattern:** `https://edge.boi.gov.il/FusionEdgeServer/sdmx/v2/data/dataflow/BOI.STATISTICS/EXR/1.0/RER_<CUR>_ILS`
- **Parameters:**
  - `startPeriod` (YYYY-MM-DD)
  - `endPeriod` (YYYY-MM-DD)
  - `format=csv`
- **Example:** `.../RER_USD_ILS?startPeriod=2026-01-01&endPeriod=2026-01-15&format=csv`

Parse the CSV: read `OBS_VALUE` (the rate) keyed by `TIME_PERIOD` (the date). The series omits non-publication days. If the exact requested date has no row, walk back to the most recent published date on or before it.

## Understanding Rates
- Rate = NIS per UNIT of foreign currency.
- UNIT varies by currency (usually 1, but 100 for JPY, 10 for LBP).
- Bank of Israel sets a single representative rate (shaar yatzig) per currency per day. There are no separate buy/sell rates.
- The representative rate is the official rate for:
  - Income tax calculations (transaction-date rate)
  - Legal/contractual obligations
  - Financial reporting

## Import VAT and the customs rate (caveat)
For import VAT and customs duty, the value of goods priced in foreign currency is NOT converted at the bare BOI representative rate. The Israel Tax Authority sets a weekly customs rate (shaar hamekhes) used on the import declaration (rashimon); it is based on the BOI representative rate plus 0.5%. Use the customs rate for import VAT, not the plain representative rate.

## Published Currencies (14 total)
USD, GBP, JPY, EUR, AUD, CAD, DKK, NOK, ZAR, SEK, CHF, JOD, LBP, EGP.

This is the full set the Bank of Israel publishes a representative rate for. The skill is not a general FX converter for every world currency.

## Rate Limitations
- Saturday, Sunday: no rate published.
- Israeli holidays: no rate published.
- Bank of Israel may delay publication due to market conditions.
- For missing dates, use the most recent published date on or before the requested date.
