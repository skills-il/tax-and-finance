# Domain Checklist: Shekel Currency Converter

Scope: converting foreign-currency amounts to/from NIS at the Bank of Israel
representative rate (sha'ar yatzig) for Israeli tax, VAT, and accounting use.
Used to review the skill for correctness and completeness.

## Must cover (a wrong answer here causes a wrong tax filing)

1. **Correct live current-rate source.** Use the live BOI JSON endpoint
   `https://www.boi.org.il/PublicApi/GetExchangeRates`. The legacy
   `currency.xml` no longer serves XML (it redirects to the JSON API).
   Source: live curl 2026-06-03 (HTTP 200, JSON body); evidence.json claim 1-2.
2. **Correct historical / tax-date rate source.** The JSON endpoint's `?date=`
   is ignored (always returns today). A specific past date must come from the
   BOI SDMX EXR series `RER_<CUR>_ILS` (CSV, `OBS_VALUE` keyed by
   `TIME_PERIOD`). Source: live curl 2026-06-03; evidence.json claim 6-7.
3. **Weekend/holiday walk-back.** The SDMX series omits Saturdays, Sundays, and
   Israeli holidays. For a non-publication date, use the most recent published
   rate on or before it, and tell the user which date was used. Verified:
   2026-01-01 (holiday) -> 2025-12-31 rate 3.19.
   Source: live curl; evidence.json claim 8.
4. **Correct unit basis.** Rate is NIS per `unit` foreign-currency units;
   unit is 1 for most, 100 for JPY, 10 for LBP, both in the JSON feed and in
   the SDMX series (`UNIT_MULT` exponent: USD=0, JPY=2, LBP=1). Conversion math
   must divide/multiply by unit. Source: live curl (JPY SDMX OBS_VALUE 1.7968 =
   per 100, matches JSON); evidence.json claim 5.
5. **Tax-date rule.** Israeli law converts foreign-currency amounts at the
   representative rate on the relevant date: income at accrual/receipt date,
   expenses at payment date, balance-sheet items at the Dec 31 rate. Income Tax
   Rules (Conversion to NIS of amounts originating outside Israel), 5764-2003.
   Source: nevo.co.il 999_233; evidence.json claim 13.
6. **Import VAT uses the customs rate, NOT the bare representative rate.** For
   goods priced in foreign currency, customs value is converted at the weekly
   customs rate (sha'ar ha-mekhes) set by the Israel Tax Authority on the
   rashimon = BOI representative rate + 0.5%. Do not quote the plain
   representative rate as the import-VAT rate. Source: gov.il/he/service/
   exchange-rate; evidence.json claim 12.
7. **Single representative rate per currency per day** (no buy/sell split),
   published soon after 15:15 on regular days and soon after 12:15 on Fridays /
   holiday eves; none on Sat/Sun/Israeli holidays. Source: BOI explanatory
   notes; evidence.json claim 10-11.

## Should cover

- **Supported-currency set is exactly 14** (USD, GBP, JPY, EUR, AUD, CAD, DKK,
  NOK, ZAR, SEK, CHF, JOD, LBP, EGP); not a general FX converter.
  Source: live JSON (14 keys); evidence.json claim 4.
- **Stale-rate awareness:** a rate fetched before the afternoon publication is
  the previous day's; flag it as not-yet-updated. Source: BOI explanatory notes.
- **NIS formatting:** symbol before the number, comma thousands / period
  decimal (1,234.56), not the European 1.234,56. evidence.json claim 15.
- **Cross-currency via NIS** for two foreign currencies (both must be published).
- **Fail-loud on fetch failure** so a stale/sample rate is never presented as an
  authoritative "shaar yatzig" figure for a tax computation.

## Out of scope

- Cryptocurrency and unofficial/grey-market exchange rates.
- Currencies BOI does not publish (outside the 14).
- Bank buy/sell spreads and card-network conversion fees (skill quotes the
  representative reference rate only).
- Live machine-lookup of the weekly customs rate: the Tax Authority customs
  query system (shaarolami-query.customs.mof.gov.il) is a session-based web app
  with no clean public JSON API, so the skill points to it in prose rather than
  computing the import-VAT rate. Reasonable deferral.

## Authoritative sources

- BOI live JSON rates: https://www.boi.org.il/PublicApi/GetExchangeRates
- BOI SDMX EXR series: https://edge.boi.gov.il/FusionEdgeServer/sdmx/v2/data/dataflow/BOI.STATISTICS/EXR/1.0/RER_USD_ILS
- BOI representative-rate explanatory notes (schedule, single-rate): https://www.boi.org.il/en/economic-roles/financial-markets/explanatory-notes-to-the-representative-exchange-rates/
- Israel Tax Authority customs/exchange rate (+0.5%): https://www.gov.il/he/service/exchange-rate
- Income Tax Rules (Conversion to NIS), 5764-2003: https://www.nevo.co.il/law_html/law01/999_233.htm

The Tax Authority customs-rate query system (host shaarolami-query.customs.mof.gov.il) is a session-based web app with no clean public JSON API, so it is referenced in prose rather than linked or machine-queried.
