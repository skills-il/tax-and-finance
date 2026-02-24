# Bank of Israel Exchange Rate API Guide

## Current Rates
- **URL:** `https://www.boi.org.il/currency.xml`
- **Method:** GET (no authentication required)
- **Format:** XML
- **Update time:** Daily, around 15:30 Israel time (IST/IDT)
- **Published days:** Sunday through Thursday (no Shabbat/holidays)

## XML Response Structure
```xml
<CURRENCIES>
  <LAST_UPDATE>2026-01-15</LAST_UPDATE>
  <CURRENCY>
    <NAME>Dollar</NAME>
    <UNIT>1</UNIT>
    <CURRENCYCODE>USD</CURRENCYCODE>
    <COUNTRY>USA</COUNTRY>
    <RATE>3.6500</RATE>
    <CHANGE>0.120</CHANGE>
  </CURRENCY>
  ...
</CURRENCIES>
```

## Historical Rates
- **URL:** `https://www.boi.org.il/PublicApi/GetExchangeRates`
- **Parameters:**
  - `date` (required): YYYY-MM-DD format
  - `curr` (optional): Specific currency code
- **Example:** `?date=2026-01-01&curr=USD`

## Understanding Rates
- Rate = NIS per UNIT of foreign currency
- UNIT varies by currency (usually 1, but 100 for JPY, etc.)
- CHANGE = percentage change from previous business day
- Representative rate (shaar yatzig) is the official rate for:
  - Tax calculations
  - Legal/contractual obligations
  - Financial reporting

## Available Currencies (Partial List)
USD, EUR, GBP, JPY, CHF, CAD, AUD, ZAR, SEK, NOK, DKK, JOD, EGP,
LBP, GIP, HKD, TWD, KRW, SGD, THB, INR, CNY, TRY, RUB, BRL, MXN

## Rate Limitations
- Weekends (Friday-Saturday): No new rates published
- Israeli holidays: No rates published
- Bank of Israel may delay publication due to market conditions
- For missing dates, use the last available business day rate
