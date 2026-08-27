# Domain Checklist: boi-economic-data

Scope: fetch and present Bank of Israel + CBS economic data (policy rate, exchange rates, CPI). Category: tax-and-finance (developer/data skill).

## Must cover (core)
- The CORRECT, working BOI data paths: `ws/public/sdmxapi/rest/data/{DATAFLOW}/{series}` and `sdmx/v2/data/dataflow/BOI.STATISTICS/{DATAFLOW}/1.0/{series}`, both live, both accepting `format=csv`, with the explicit User-Agent and startPeriod/endPeriod requirements and the `<Obs TIME_PERIOD OBS_VALUE></Obs>` response shape.
- Queries must be bounded: a dataflow queried with no date filter returns every series with full history (EXR is ~20 MB back to 1948). Naming the series, or adding startPeriod/endPeriod or lastNObservations, is what keeps a call cheap. A date-bounded dataflow query is the correct way to get all currencies at once.
- `lastNObservations` limits the result; `lastNPeriods` is accepted and silently ignored. Documenting the wrong one is a silent full-history download.
- Exchange rates (sha'ar yatzig): EXR dataflow, RER_<CUR>_ILS series, representative rate (DATA_TYPE OF00), UNIT_MULT read from the response (JPY per 100), published once per business day (Mon-Thu ~15:30, Fri ~12:30), Mon-Fri only (weekend Sat-Sun, since the Israeli week moved to Mon-Fri in Jan 2026).
- Policy interest rate: BR dataflow, daily series MNT_RIB_BOI_D. NOT the BIR dataflow, which is bank credit rates excluding housing and returns plausible wrong numbers.
- CPI: the CBS index API, id 120010 ("מדד המחירים לצרכן - כללי"), with its base period. The BOI PRI dataflow is explicitly NOT the headline index.
- CPI-linkage conventions: madad yadua vs madad bagin, the base period and the need for a CBS linking coefficient across a rebase, and the floor clause (taniyat ritzpa).
- Failure semantics: the CBS index API returns HTTP 200 for an unknown id and for an undefined path, so payloads must be validated rather than status codes.
- A working helper script that fetches real data (correct URLs, correct parser, explicit User-Agent, TLS verification ON) and exits non-zero rather than emitting placeholder numbers.
- Gotchas: weekend/holiday gaps, representative-vs-realtime rate, CPI lag, BIR/BR confusion.

## Should cover (advanced)
- Cross-analysis (mortgage, business, investment, import/export).
- CBS / TASE / data.gov.il alternative sources.
- Structure/metadata path to discover dataflow ids, with the ids named outright (EXR, BR, BIR, PRI, ZCM, MAG, TLB).

## Out of scope (explicit)
- Stock-market data (tase-stock-analysis). Re-litigated 2026-08-27: still out of scope, the sibling skill owns it and a user asking about share prices is not asking a BOI question.
- Currency conversion as a product (shekel-currency-converter). Re-litigated 2026-08-27: still out of scope; this skill supplies the representative rate, the sibling skill does the conversion UX.
- Inflation-expectations and zero-curve series (ZCM) and monetary aggregates (MAG) as computed outputs. Re-litigated 2026-08-27: an ordinary user of this skill would plausibly ask, so the dataflow ids are now NAMED in the Reference Links and reference file so a caller can reach them, but the skill does not add fetch flags for them. Reconsider if usage shows demand.
- CPI basket component weights as stated figures. Re-litigated 2026-08-27: the previous table carried "n/a" in every row, which conveyed nothing. Weights are revised periodically by the CBS and are not worth freezing into the skill; the skill now names the CBS basket publication as the place to read them.

## Authoritative sources
- BOI new series database (Fusion Edge Server), dataflow list at sdmx/v2/structure/dataflow/BOI.STATISTICS.
- boi.org.il statistical-information / monetary-policy / press-releases and the reprate methodology page.
- CBS index API (api.cbs.gov.il/index) and cbs.gov.il Consumer Price Index.
