# Bank of Israel API Reference

## Overview

The Bank of Israel provides public economic data through its "new series database" (Fusion Edge Server) using the SDMX 2.1 REST API. The data API is available at `edge.boi.gov.il`.

## Base URL

Data is served from the SDMX REST `data` path (the older `sdmx/v2/data/dataflow/BOI/...` path returns 404):

```
https://edge.boi.gov.il/FusionEdgeServer/ws/public/sdmxapi/rest/data/
```

The structure/metadata path (to list available dataflows) is separate:
```
https://edge.boi.gov.il/FusionEdgeServer/sdmx/v2/structure/dataflow/BOI.STATISTICS
```

**Notes that apply to every call:** send a normal browser `User-Agent` header (the server rejects the default urllib agent); use `startPeriod` / `endPeriod` (capital P); the response is SDMX-XML with observations as flat `<Obs TIME_PERIOD="..." OBS_VALUE="..."/>` elements.

## Endpoints

### Exchange Rates (EXR)

Representative rates (sha'ar yatzig) are per-currency series named `RER_<CUR>_ILS` inside the `EXR` dataflow.

```
GET https://edge.boi.gov.il/FusionEdgeServer/ws/public/sdmxapi/rest/data/EXR/RER_USD_ILS
```

**Parameters:**
| Parameter | Description | Example |
|-----------|-------------|---------|
| startPeriod | Start date (YYYY-MM-DD) | 2026-01-01 |
| endPeriod | End date (YYYY-MM-DD) | 2026-01-31 |

**Example:**
```
GET .../data/EXR/RER_USD_ILS?startPeriod=2026-01-01&endPeriod=2026-01-31
```
Common series: `RER_USD_ILS`, `RER_EUR_ILS`, `RER_GBP_ILS`, `RER_JPY_ILS` (per 100 JPY), `RER_CHF_ILS`. Omit the series segment (`.../data/EXR/`) to get all currencies.

### Interest Rate (BIR)

```
GET https://edge.boi.gov.il/FusionEdgeServer/ws/public/sdmxapi/rest/data/BIR/?startPeriod=2026-01-01&endPeriod=2026-12-31
```
The `BIR` dataflow contains multiple Bank-of-Israel-rate series. For the single headline policy rate, the authoritative source is the Monetary Committee decision (boi.org.il monetary-policy / press-release pages).

### Price Indices / CPI (PRI)

CPI and other price indices live in the `PRI` dataflow:
```
GET https://edge.boi.gov.il/FusionEdgeServer/ws/public/sdmxapi/rest/data/PRI/?startPeriod=2026-01&endPeriod=2026-05
```

## Response Format

The API returns SDMX XML. Each series carries its metadata as attributes on the `<Series>` element, and each observation is an `<Obs>` element with the date and value as `TIME_PERIOD` / `OBS_VALUE` attributes:

```xml
<Series SERIES_CODE="RER_USD_ILS" FREQ="D" BASE_CURRENCY="USD"
        COUNTER_CURRENCY="ILS" UNIT_MEASURE="ILS" DATA_TYPE="OF00">
  <Obs TIME_PERIOD="2026-06-05" OBS_VALUE="2.908" RELEASE_STATUS="YP"/>
  <Obs TIME_PERIOD="2026-06-04" OBS_VALUE="2.895" RELEASE_STATUS="YP"/>
</Series>
```

Parse by iterating `<Obs>` elements and reading the `TIME_PERIOD` and `OBS_VALUE` attributes (handle a namespace prefix on the tag). `DATA_TYPE="OF00"` marks the official representative rate.

## Rate Limits

- No authentication required for public data
- Reasonable rate limiting (no official limit published)
- Recommended: cache responses, avoid more than 1 request/second
- Business hours may have higher latency

## Data Availability

| Data | Publication Time | Frequency | Days |
|------|-----------------|-----------|------|
| Exchange rates | ~15:30 Israel time | Business days (Sun-Thu) | No Fri/Sat |
| Interest rate | After committee decision | ~6 times/year | Decision dates |
| CPI | ~15th of following month | Monthly | CBS publication |

## Alternative Data Sources

- **CBS (Lishkat HaStatistika):** https://www.cbs.gov.il/he/pages/default.aspx
  - CPI data, economic indicators, demographic data
- **TASE (Tel Aviv Stock Exchange):** https://info.tase.co.il/
  - Market data, index composition, bond yields
- **data.gov.il:** https://data.gov.il/
  - Open government data portal

## Common Issues

- Weekend queries return empty data (no rates published Friday/Saturday)
- Holiday calendar affects publication schedule (Jewish holidays)
- SDMX XML parsing requires namespace-aware parser
- Historical data may have different format versions
