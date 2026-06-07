# Domain Checklist: boi-economic-data

Scope: fetch and present Bank of Israel + CBS economic data (interest rate, exchange rates, CPI). Category: tax-and-finance (developer/data skill).

## Must cover (core)
- The CORRECT, working BOI data API path: edge.boi.gov.il/FusionEdgeServer/ws/public/sdmxapi/rest/data/{DATAFLOW}/{series}, with the User-Agent + startPeriod/endPeriod requirements and the flat <Obs TIME_PERIOD OBS_VALUE> response shape.
- Exchange rates (sha'ar yatzig): EXR dataflow, RER_<CUR>_ILS series, representative rate (DATA_TYPE OF00), published once per business day (~15:30), Sun-Thu only.
- Interest rate: BIR dataflow + the authoritative Monetary Committee decision for the headline policy rate.
- CPI: PRI dataflow / CBS, ~15th-of-following-month release, approximate basket weights, CPI-linkage uses (bonds, rent, tax brackets).
- A working helper script that fetches real data (correct URL, correct parser, browser User-Agent, TLS verification ON).
- Gotchas: weekend/holiday gaps, representative-vs-realtime rate, CPI lag.

## Should cover (advanced)
- Cross-analysis (mortgage, business, investment, import/export).
- CBS / TASE / data.gov.il alternative sources.
- Structure/metadata path to discover dataflow ids.

## Out of scope (explicit)
- Stock-market data (tase-stock-analysis).
- Currency conversion as a product (shekel-currency-converter).

## Authoritative sources
- BOI new series database (Fusion Edge Server) + "Extracting representative exchange rates" PDF.
- boi.org.il statistical-information / monetary-policy / press-releases.
- cbs.gov.il Consumer Price Index.
