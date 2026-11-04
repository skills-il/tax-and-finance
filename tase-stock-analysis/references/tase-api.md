# TASE API Reference (Tel Aviv Stock Exchange)

## Authentication
- **Entry point:** https://www.tase.co.il/he/content/products_lobby/data_services (the older
  `datahub.tase.co.il` address redirects here; the `openapi.tase.co.il` and `openapigw.tase.co.il`
  hosts no longer resolve at all as of 2026-11-04, so do not use them)
- **Official guide:** https://content.tase.co.il/media/l5xjhjmz/2000_api_guide_eng.pdf
- **Method:** API Key. Register for the Developers' Portal, create an App under 'My Apps',
  click '+Generate Credential' to be assigned an API Key, then supply it through 'Authorize'
  on the product page. The current official guide documents no OAuth2 flow and no token
  endpoint. Older third-party write-ups describe an OAuth2 client-credentials exchange
  against `openapigw.tase.co.il`; that host no longer resolves, so treat any OAuth2
  instructions as obsolete, and take the exact request shape from the Authorize dialog and the sample code on the product page
  you actually registered for.
- **Registration:** Required for live data access. Some products are paid and need commercial
  approval before activation; the sales contact is marketdatateam@tase.co.il and API support
  is apisupport@tase.co.il.
- **Rate limits:** 10 requests per 2 seconds (rate and burst) unless the product documentation
  says otherwise. Exceeding them returns HTTP 429.

## API Gateway
- **Base URL:** `https://datawise.tase.co.il` (verified 2026-11-04: real paths answer 401 without a
  valid key, an unknown path answers 403). It is not printed in the official guide, so if it
  ever stops answering, read it off the product page in the Developers' Portal.
- **Header:** the key goes in the `apikey` HTTP header, as the tase-mcp client sends it.
- **Index paths used by `scripts/fetch_tase_data.py` and tase-mcp:**
  `/api/v2/basic-indices/indices-list` and
  `/api/v2/basic-indices/index-components-basic?IndexId=<id>&TradeDate=YYYY-MM-DD`.

## Index IDs
| Index | ID | Hebrew |
|-------|----|--------|
| TA-35 | 142 | ת"א-35 |
| TA-125 | 137 | ת"א-125 |
| TA-90 | 143 | ת"א-90 |
| TA-Bank | 194 | ת"א-בנקים |
| TA-RealEstate | 149 | ת"א-נדל"ן |
| TA-Technology | 169 | ת"א-טכנולוגיה |

IDs re-confirmed 2026-11-04 against each index's market.tase.co.il about page. TA-Banks5 (164) is a separate index from TA-Bank (194). Newer indices (TA-Technology 35, TA-Israel Energy, launched February 2026) are not listed here: get their IDs from `indices-list`. Verify a current ID by opening the index page (e.g. market.tase.co.il/en/market_data/index/137/about for TA-125) before hardcoding.

## Maya (Disclosure) System
- **URL:** https://maya.tase.co.il
- **Search:** Filter by company, date range, report type
- **Report types:** Immediate reports, periodic reports, shelf offerings, insider trades

## Market Hours (effective January 2026)
- **Pre-open:** 09:25, Monday-Thursday and Friday
- **Continuous trading:** Monday-Thursday 09:59-17:14, Friday 09:59-13:50
- **Closing auction:** Monday-Thursday pre-close 17:14-17:15, closing auction 17:24-17:25,
  end of Trading-at-Last 17:30. Friday pre-close 13:34-13:35, closing auction 13:44-13:45,
  end of trading 13:50
- **No trading:** Saturday (Shabbat), Sunday, Jewish holidays

Note: TASE switched from Sunday-Thursday to Monday-Friday trading on January 5, 2026.
