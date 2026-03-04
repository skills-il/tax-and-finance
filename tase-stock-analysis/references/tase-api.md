# TASE API Reference (Tel Aviv Stock Exchange)

## Authentication
- **Portal:** https://info.tase.co.il/heb/marketdata/pages/api.aspx
- **Method:** API key via header `Authorization: Bearer {token}`
- **Registration:** Required for live data access
- **Free tier:** Delayed data (15-minute delay), limited endpoints

## Endpoints

### Index Composition
```
GET https://api.tase.co.il/api/index/{index_id}/components
Authorization: Bearer {token}

Response:
{
  "indexId": 142,
  "indexName": "TA-35",
  "components": [
    {
      "securitiesNumber": "662577",
      "securityName": "בנק הפועלים",
      "weightPercent": 8.2,
      "lastPrice": 35.50,
      "changePercent": 1.2
    }
  ]
}
```

### Index IDs
| Index | ID | Hebrew |
|-------|----|--------|
| TA-35 | 142 | ת"א-35 |
| TA-125 | 143 | ת"א-125 |
| TA-90 | 164 | ת"א-90 |
| TA-Banks | 145 | ת"א-בנקים |
| TA-Real Estate | 146 | ת"א-נדל"ן |
| TA-Tech | 147 | ת"א-טכנולוגיה |

### Security Quote
```
GET https://api.tase.co.il/api/security/{securities_number}
Authorization: Bearer {token}

Response:
{
  "securitiesNumber": "662577",
  "securityName": "בנק הפועלים",
  "lastPrice": 35.50,
  "openPrice": 35.20,
  "highPrice": 35.80,
  "lowPrice": 35.10,
  "volume": 5230000,
  "changePercent": 1.2,
  "marketCap": 45200000000
}
```

## Maya (Disclosure) System
- **URL:** https://maya.tase.co.il
- **Search:** Filter by company, date range, report type
- **Report types:** Immediate reports, periodic reports, shelf offerings, insider trades
- **API:** Limited public API; scraping not recommended

## Market Hours
- **Pre-open:** Sunday-Thursday 09:02-09:59
- **Continuous trading:** Sunday-Thursday 09:59-17:14
- **Closing auction:** 17:14-17:25
- **No trading:** Friday, Saturday, Jewish holidays
