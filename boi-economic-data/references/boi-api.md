# Bank of Israel SDMX API Reference

## Base URL
```
https://edge.boi.gov.il/FusionEdgeServer/sdmx/v2/data/dataflow/BOI.STAT
```

## Authentication
- No authentication required for public data
- Rate limited: be respectful with request frequency
- Data available Sunday-Thursday (Israeli business days)

## Exchange Rates (Sha'ar Yatzig)

### Endpoint
```
GET /EXR/1.0/{series_key}?startperiod={date}&endperiod={date}
Accept: application/json
```

### Series Keys
| Currency | Series Key | Notes |
|----------|-----------|-------|
| USD/ILS | RER_USD_ILS | US Dollar |
| EUR/ILS | RER_EUR_ILS | Euro |
| GBP/ILS | RER_GBP_ILS | British Pound |
| JPY/ILS | RER_JPY_ILS | Japanese Yen (per 100) |
| CHF/ILS | RER_CHF_ILS | Swiss Franc |
| AUD/ILS | RER_AUD_ILS | Australian Dollar |
| CAD/ILS | RER_CAD_ILS | Canadian Dollar |

### Example Request
```
GET https://edge.boi.gov.il/FusionEdgeServer/sdmx/v2/data/dataflow/BOI.STAT/EXR/1.0/RER_USD_ILS?startperiod=2026-01-01&endperiod=2026-01-31
Accept: application/json
```

### Response Structure (SDMX JSON)
```json
{
  "data": {
    "dataSets": [{
      "observations": {
        "0": [3.62],
        "1": [3.63]
      }
    }],
    "structure": {
      "dimensions": {
        "observation": [{
          "values": [
            {"id": "2026-01-02"},
            {"id": "2026-01-05"}
          ]
        }]
      }
    }
  }
}
```

## Interest Rate

### Endpoint
```
GET /DIR/1.0/DIR_BOI
Accept: application/json
```

### Notes
- Returns full history of BOI monetary interest rate decisions
- Rate set by Monetary Committee (monthly, except August)
- Published after each committee meeting

## Data Portal
- **Website:** https://data.boi.org.il
- **SDMX documentation:** https://edge.boi.gov.il/FusionEdgeServer/sdmx/v2
- **Alternative:** BOI also publishes CSV/Excel downloads
- **CBS data:** https://www.cbs.gov.il (for CPI, GDP, employment)

## Common Issues
- Weekend dates return no data (use previous Thursday)
- Jewish holidays: no data published
- JPY rate is per 100 yen (divide by 100 for single unit)
- Data publication time: approximately 15:30 Israel time
- Historical data available from 1948 for major currencies
