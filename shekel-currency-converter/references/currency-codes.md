# Currency Codes and NIS Conversion Notes

## Published Currencies (14 total)
The Bank of Israel publishes a representative rate for exactly these 14 currencies:
USD, GBP, JPY, EUR, AUD, CAD, DKK, NOK, ZAR, SEK, CHF, JOD, LBP, EGP.

## Primary Currencies

| Code | Currency | Hebrew | Illustrative Rate (NIS) | Unit |
|------|----------|--------|-------------------------|------|
| ILS | Israeli New Shekel | shekel chadash | 1.0000 | 1 |
| USD | US Dollar | dolar | about 2.97 | 1 |
| EUR | Euro | euro | about 3.47 | 1 |
| GBP | British Pound | lira sterling | about 4.05 | 1 |
| JPY | Japanese Yen | yen | about 1.87 | 100 |
| CHF | Swiss Franc | frank shveitzi | about 3.70 | 1 |

NOTE: These figures are illustrative snapshots of the 2026-08-26 publication and move daily. Always fetch the live or dated rate from the API; never quote these as the actual rate.

## Tax-Relevant Uses
- **Foreign income:** Report at the representative rate on the income accrual / receipt date.
- **Foreign expenses:** Deduct at the representative rate on the payment date.
- **End-of-year revaluation:** Use the December 31 representative rate for balance sheet items.
- **VAT and customs on imported GOODS:** Do NOT use the bare BOI representative rate. Customs value uses the weekly customs rate (shaar hamekhes), set by the Israel Tax Authority on the import declaration (rashimon), and published weekly by the Tax Authority. Read the published customs rate rather than deriving it: the uplift over the representative rate is commonly cited as 0.5%, but the Tax Authority service is bot-blocked and this skill cannot machine-verify it. Imported SERVICES (reverse-charge VAT) instead use the plain representative rate, with no customs uplift.

## NIS Symbol and Formatting
- Currency code: ILS (ISO 4217)
- Symbol: shekel sign (Unicode U+20AA)
- Common display: NIS or ILS
- Format: 1,234.56 NIS (thousands separator: comma, decimal: period)
- Hebrew format: 1,234.56 (symbol before number)
