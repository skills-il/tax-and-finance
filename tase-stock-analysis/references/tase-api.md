# TASE API Reference (Tel Aviv Stock Exchange)

## Authentication
- **Developer Portal:** https://openapi.tase.co.il/tase/prod/
- **Data Hub:** https://datahub.tase.co.il/
- **Method:** OAuth2 client credentials flow. Obtain access token from `https://openapigw.tase.co.il/tase/prod/oauth/oauth2/token`, then pass as `Authorization: Bearer {token}`.
- **Registration:** Required for live data access. Some API products require paid subscription.
- **Free tier:** Delayed data (15-minute delay), limited endpoints

## API Gateway
- **Base URL:** `https://openapigw.tase.co.il/tase/prod/`
- Consult the official TASE API documentation at the Developer Portal for exact endpoint paths, request parameters, and response schemas.

## Index IDs
| Index | ID | Hebrew |
|-------|----|--------|
| TA-35 | 142 | ת"א-35 |
| TA-125 | 143 | ת"א-125 |
| TA-90 | 164 | ת"א-90 |
| TA-Banks | 145 | ת"א-בנקים |
| TA-Real Estate | 146 | ת"א-נדל"ן |
| TA-Tech | 147 | ת"א-טכנולוגיה |

## Maya (Disclosure) System
- **URL:** https://maya.tase.co.il
- **Search:** Filter by company, date range, report type
- **Report types:** Immediate reports, periodic reports, shelf offerings, insider trades
- **API:** Limited public API; scraping not recommended

## Market Hours (effective January 2026)
- **Pre-open:** Monday-Friday from approximately 09:00
- **Continuous trading:** Monday-Thursday 09:59-17:14, Friday 09:59-13:50
- **Closing auction:** Monday-Thursday 17:14-17:25, Friday 13:50-14:00
- **No trading:** Saturday (Shabbat), Sunday, Jewish holidays

Note: TASE switched from Sunday-Thursday to Monday-Friday trading on January 5, 2026.
