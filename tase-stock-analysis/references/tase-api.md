# TASE API Reference (Tel Aviv Stock Exchange)

## Authentication
- **Entry point:** https://www.tase.co.il/he/content/products_lobby/data_services (the older
  `datahub.tase.co.il` and `openapi.tase.co.il/tase/prod/` addresses now redirect here, so do not
  hardcode them)
- **Official guide:** https://content.tase.co.il/media/l5xjhjmz/2000_api_guide_eng.pdf
- **Method:** API Key. Register for the Developers' Portal, create an App under 'My Apps',
  click '+Generate Credential' to be assigned an API Key, then supply it through 'Authorize'
  on the product page. The current official guide documents no OAuth2 flow and no token
  endpoint. Older third-party write-ups describe an OAuth2 client-credentials exchange
  against `openapigw.tase.co.il`; that host sits behind a bot filter that returns 503 to
  anything scriptable, so treat any OAuth2 instructions as legacy and unverified, and take
  the exact request shape from the Authorize dialog and the sample code on the product page
  you actually registered for.
- **Registration:** Required for live data access. Some products are paid and need commercial
  approval before activation; the sales contact is marketdatateam@tase.co.il and API support
  is apisupport@tase.co.il.
- **Rate limits:** 10 requests per 2 seconds (rate and burst) unless the product documentation
  says otherwise. Exceeding them returns HTTP 429.

## API Gateway
- Do not hardcode a gateway base URL from a blog post. Read the base URL and the endpoint
  paths off the product page in the Developers' Portal, which also generates sample code.

## Index IDs
| Index | ID | Hebrew |
|-------|----|--------|
| TA-35 | 142 | ת"א-35 |
| TA-125 | 137 | ת"א-125 |
| TA-90 | 143 | ת"א-90 |
| TA-Bank | 194 | ת"א-בנקים |
| TA-RealEstate | 149 | ת"א-נדל"ן |
| TA-Technology | 169 | ת"א-טכנולוגיה |

Verify a current ID by opening the index page (e.g. market.tase.co.il/en/market_data/index/137/about for TA-125) before hardcoding.

## Maya (Disclosure) System
- **URL:** https://maya.tase.co.il
- **Search:** Filter by company, date range, report type
- **Report types:** Immediate reports, periodic reports, shelf offerings, insider trades
- **API:** Limited public API; scraping not recommended

## Market Hours (effective January 2026)
- **Pre-open:** Monday-Friday from approximately 09:00
- **Continuous trading:** Monday-Thursday 09:59-17:14, Friday 09:59-13:50
- **Closing auction:** Monday-Thursday pre-close 17:14-17:15, closing auction 17:24-17:25,
  end of Trading-at-Last 17:30. Friday pre-close 13:34-13:35, closing auction 13:44-13:45,
  end of trading 13:50
- **No trading:** Saturday (Shabbat), Sunday, Jewish holidays

Note: TASE switched from Sunday-Thursday to Monday-Friday trading on January 5, 2026.
