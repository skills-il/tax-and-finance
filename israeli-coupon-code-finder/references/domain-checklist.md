# Domain Coverage Checklist - israeli-coupon-code-finder

Generated: 2026-06-08. Domains below are written without a scheme on purpose; only the live URLs cited in SKILL.md and evidence.json carry full https links.

## Must cover (core)
- [x] Hebrew coupon-aggregator search playbook (query patterns that surface aggregator pages) - source: couponim.co.il
- [x] Store-direct coupon levers (newsletter/SMS first-order, app-only, member-club price, abandoned-cart, student/military) - why core: most reliable non-scam path
- [x] Israeli seasonal sale windows (Black Friday, Cyber Monday, Singles Day, end-of-season, holiday sales) - why core: timing often beats any code
- [x] Per-candidate verification rubric (expiry, minimum cart, new-customer-only, exclusions, single-use vs reusable, stacking) - why core: verification is the skill's core value
- [x] Consumer-protection: 14-day remote-sale cancellation, fee cap 5% or 100 NIS, 4-month extension for 65+/disabled/olim - source: kolzchut.org.il (remote-sale cancellation page) - why core: the shopper's real backstop against a bad coupon-driven purchase
- [x] Inflated-baseline / fake-discount heuristic (judge a discount against the genuine recent price, not an inflated "original") - why core: spots fake big-percentage deals
- [x] Scam / fake-coupon-site red flags (card-before-code, survey-to-unlock, forced extension, typosquat, no business details, fake countdown) - why core: protects non-technical shoppers

## Should cover (advanced / edge cases)
- [x] Cashback stacking layer (route through an IL cashback platform on top of a code where terms allow) - source: cashback.co.il - note: ongoing cashback setup is israeli-smart-saver
- [x] Credit-card benefit hubs (a cardholder discount can beat a public code) - source: max.co.il/benefits
- [x] Gift-card stacking (discounted BuyMe / club reload paid at checkout) - source: buyme.co.il
- [x] Consumer / employee clubs (Moadon Chaver for career soldiers + retirees; works-council portals) - source: hvr.co.il
- [x] Cross-border-to-IL stores (weigh customs/VAT threshold + shipping against the code) - note: deep price math is israeli-product-price-comparator
- [x] Telegram coupon channels as a live-search surface (category only, never name a specific channel)

## Out of scope (explicit, with rationale)
- Ongoing savings strategy, cashback-account setup, subscription auditing - recurring behavior, not point-of-checkout - related skill: israeli-smart-saver
- Cross-store price comparison ("who sells this cheapest") - product-matching, not coupon-finding - related skill: israeli-product-price-comparator
- Grocery / supermarket basket pricing - recurring grocery optimization - related skill: israeli-grocery-price-intelligence

## Verified named entities (the source map the skill may safely name)
| Entity | Domain | What it is |
|--------|--------|-----------|
| Couponim | couponim.co.il | Hebrew coupon-aggregator listing per-store codes |
| Cashback.co.il | cashback.co.il | IL cashback platform |
| BuyMe | buyme.co.il | Largest IL gift-card / experiences platform |
| Max benefits | max.co.il/benefits | Max cardholder benefits/discounts hub |
| Moadon Chaver | hvr.co.il | Career-soldier + retiree consumer club |
| Ivory | ivory.co.il | IL computers/electronics retailer |
| Bug | bug.co.il | IL electronics/digital retailer |
| Terminal X | terminalx.com | IL fashion online store |
| Kol-Zchut | kolzchut.org.il | Authoritative IL consumer-rights wiki |

## Authoritative source (verified, cited with full URL in SKILL.md + evidence.json)
- kolzchut.org.il remote-sale cancellation page - the 14-day window, the 5% / 100 NIS fee cap, the 4-month extension for seniors / people with disabilities / new immigrants

## Could NOT verify (DO NOT name these in the skill)
- "gocoupon" - no live Israeli brand by this name. EXCLUDE.
- Bidurit employee-perk portal - not confirmed operating in 2026. EXCLUDE.
- Any specific Telegram coupon-channel handle - category is real, no durable named channel verified. Reference generically only.
- Rav-Tav as a single branded site - it is a voucher format, not one production URL. Mention as a format only.
- castro.co.il redirects to a .com host, super-pharm.co.il redirects to a shop subdomain, and the Cal benefits page returned an error at fetch time. Re-verify the live destination before naming any of them.
