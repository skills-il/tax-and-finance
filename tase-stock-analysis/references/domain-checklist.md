# Domain coverage checklist, tase-stock-analysis

Anchor for expert review. Scope: analyzing Israeli equities on TASE, indices, dual-listed companies, Maya filings, and securities capital-gains tax.

## Must cover (core)
- TASE trading week Monday-Friday (since 5 Jan 2026) + hours; agorot price quoting.
- Index IDs (TA-35=142, TA-125=137, TA-90=143, TA-Bank=194, TA-RealEstate=149, TA-Technology=169) for the Data Hub API / market pages.
- Securities lookup by number/alpha symbol (POLI, LUMI, etc.); never hardcode numbers from memory.
- Capital gains on securities: 25% individual and 30% for a 10%+ shareholder on the real gain, plus the separate surtax (mas yesef): 3% on total income above ILS 721,560 and, from 2025, 2% on capital-source income that itself exceeds ILS 721,560 (threshold fixed for 2024 to 2027); loss offsetting; inflationary adjustment.
- 25% is a ceiling (s.91(b)(1)): the gain is the top slice at ordinary brackets; individuals 60+ get the reduced brackets from 10%, so a low-income retiree pays less and reclaims the broker's 25% withholding via a return.
- Real-gain arithmetic: inflationary amount is part of the gain, never negative, never above the gain; a capital loss is nominal (s.88). Loss carry-forward requires a return for the loss year (s.92(b)).
- Surtax mechanics: base excludes the inflationary amount and counts all capital-source income (incl. rent, shevach; residential apartment shevach only above a ILS 5,385,285 sale value); not part of the s.91(d) advance (s.121B(b)); surtax liability removes the exemption from filing.
- Scope guardrail in the body: no view on whether a specific security is worth buying (Investment Advice Law 1995).
- Dual-listed handling (NIS vs USD, BoI representative rate, tax-treaty/Israeli-resident tax, Israel-US treaty dividend rate 25% for individuals). TASE symbol can differ from the US ticker (Palo Alto: CYBR on TASE, PANW on Nasdaq); Sapiens delisted Dec 2025; Check Point is US-only.
- Index membership is dynamic: semi-annual update plus fast-track entries; new indices launched Feb 2026 (TA-Technology 35, TA-Israel Energy). Fetch constituents for a trade date, never from memory.
- Maya disclosure system; TASE Data Hub API (apikey per registered application and product, some products paid); tase-mcp v2 tool names (no Maya tool).

## Out of scope (explicit)
- General non-Israel stock analysis, crypto (per description). Re-checked 2026-11-04: users do ask about crypto and foreign-broker filing, and both have dedicated skills (israeli-crypto-tax-reporter, israeli-foreign-broker-tax-report), so they stay out of scope here.
- Personalised buy/sell/hold recommendations (ייעוץ השקעות is licensed under the Investment Advice Law 1995). Re-checked 2026-11-04: users will ask; the answer is data, analysis and tax mechanics, never a recommendation.

## Authoritative sources
- TASE market data: https://market.tase.co.il/en/market_data
- TASE Data Hub / Data Services: https://www.tase.co.il/he/content/products_lobby/data_services
- Maya: https://maya.tase.co.il
- Israeli capital gains (PwC summary / ITA): https://taxsummaries.pwc.com/israel/individual/income-determination
