# Domain coverage checklist, tase-stock-analysis

Anchor for expert review. Scope: analyzing Israeli equities on TASE, indices, dual-listed companies, Maya filings, and securities capital-gains tax.

## Must cover (core)
- TASE trading week Monday-Friday (since 5 Jan 2026) + hours; T+1 settlement; agorot price quoting.
- Index IDs (TA-35=142, TA-125=137, TA-90=143, TA-Bank=194, TA-RealEstate=149, TA-Technology=169) for the OpenAPI / market pages.
- Securities lookup by number/alpha symbol (POLI, LUMI, etc.); never hardcode numbers from memory.
- Capital gains on securities: 25% individual, 30% substantial shareholder (>10%, sec 91(b)(2)), 23% corporate, plus surtax (mas yesef) above ~721,560 NIS/yr; loss offsetting; inflationary adjustment.
- Dual-listed handling (NIS vs USD, BoI representative rate, tax-treaty/Israeli-resident tax).
- Maya disclosure system; TASE Data Hub OpenAPI (OAuth2 client credentials, paid products).

## Out of scope (explicit)
- General non-Israel stock analysis, crypto (per description).

## Authoritative sources
- TASE market data: https://market.tase.co.il/en/market_data
- TASE OpenAPI / Data Hub: https://datahub.tase.co.il/
- Maya: https://maya.tase.co.il
- Israeli capital gains (PwC summary / ITA): https://taxsummaries.pwc.com/israel
