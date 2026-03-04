# Bank of Israel API Reference

## Overview

The Bank of Israel provides public economic data through a REST API using the SDMX (Statistical Data and Metadata eXchange) format. The API is available at `edge.boi.gov.il`.

## Base URL

```
https://edge.boi.gov.il/FusionEdgeServer/sdmx/v2/data/dataflow/BOI/
```

## Endpoints

### Exchange Rates (EXR)

**Dataflow:** `EXR/1.0`

```
GET https://edge.boi.gov.il/FusionEdgeServer/sdmx/v2/data/dataflow/BOI/EXR/1.0
```

**Parameters:**
| Parameter | Description | Example |
|-----------|-------------|---------|
| startperiod | Start date (YYYY-MM-DD) | 2025-01-01 |
| endperiod | End date (YYYY-MM-DD) | 2025-01-31 |
| c[CURRENCY] | Currency filter | USD, EUR, GBP |
| c[DATA_TYPE] | Rate type | OF (official/representative) |

**Example:**
```
GET .../EXR/1.0?startperiod=2025-01-01&endperiod=2025-01-31&c[CURRENCY]=USD
```

### Interest Rate (IR_INTEREST)

**Dataflow:** `IR_INTEREST/1.0`

```
GET https://edge.boi.gov.il/FusionEdgeServer/sdmx/v2/data/dataflow/BOI/IR_INTEREST/1.0
```

**Parameters:**
| Parameter | Description | Example |
|-----------|-------------|---------|
| startperiod | Start date | 2024-01-01 |
| endperiod | End date | 2025-12-31 |

### Price Indices (Series)

For CPI and other price indices, use the BOI statistical series:
```
GET https://edge.boi.gov.il/FusionEdgeServer/sdmx/v2/data/dataflow/BOI/SERIES/1.0
```

## Response Format

The API returns SDMX XML by default. Key elements:

```xml
<message:GenericData>
  <message:DataSet>
    <generic:Series>
      <generic:SeriesKey>
        <generic:Value id="CURRENCY" value="USD"/>
      </generic:SeriesKey>
      <generic:Obs>
        <generic:ObsDimension value="2025-01-15"/>
        <generic:ObsValue value="3.6120"/>
      </generic:Obs>
    </generic:Series>
  </message:DataSet>
</message:GenericData>
```

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
