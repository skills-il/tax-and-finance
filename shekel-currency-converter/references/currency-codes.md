# Currency Codes and NIS Conversion Notes

## Published Currencies (14 total)
The Bank of Israel publishes a representative rate for exactly these 14 currencies:
USD, GBP, JPY, EUR, AUD, CAD, DKK, NOK, ZAR, SEK, CHF, JOD, LBP, EGP.

## Primary Currencies

| Code | Currency | Hebrew | Illustrative Rate (NIS) | Unit |
|------|----------|--------|-------------------------|------|
| ILS | Israeli New Shekel | shekel chadash | 1.0000 | 1 |
| USD | US Dollar | dolar | about 2.87 | 1 |
| EUR | Euro | euro | about 3.34 | 1 |
| GBP | British Pound | lira sterling | about 3.86 | 1 |
| JPY | Japanese Yen | yen | about 1.80 | 100 |
| CHF | Swiss Franc | frank shveitzi | about 3.64 | 1 |

NOTE: These figures are illustrative snapshots (mid-2026) and move daily. Always fetch the live or dated rate from the API; never quote these as the actual rate.

## Tax-Relevant Uses
- **Foreign income:** Report at the representative rate on the income accrual / receipt date.
- **Foreign expenses:** Deduct at the representative rate on the payment date.
- **End-of-year revaluation:** Use the December 31 representative rate for balance sheet items.
- **VAT and customs on imports:** Do NOT use the bare BOI representative rate. Customs value uses the weekly customs rate (shaar hamekhes), set by the Israel Tax Authority on the import declaration (rashimon), based on the BOI representative rate plus 0.5%.

## NIS Symbol and Formatting
- Currency code: ILS (ISO 4217)
- Symbol: shekel sign (Unicode U+20AA)
- Common display: NIS or ILS
- Format: 1,234.56 NIS (thousands separator: comma, decimal: period)
- Hebrew format: 1,234.56 (symbol before number)
