# Domain Coverage Checklist, israeli-price-quote-generator

Generated: 2026-05-19 via research on: mas.gov.il, btl.gov.il, kolzchut.org.il, nevo.co.il, gov.il, knesset.gov.il, greeninvoice.co.il, taxsummaries.pwc.com

## Must cover (core)

- [x] **Israel VAT rate is 18%** (raised from 17% on 2025-01-01; 2026 raise to 19% rejected), source: https://taxsummaries.pwc.com/israel/corporate/other-taxes, why core: every quote must compute VAT correctly; a rounding or rate miscalc on a 50k₪ project is real money that disappears.
- [x] **Oseik patur 2026 threshold = 122,833 ₪/year**, source: https://www.kolzchut.org.il/he/עוסק_פטור, why core: oseik patur quotes have different labeling/VAT rules; crossing mid-year forces status change.
- [x] **Oseik patur may NOT issue חשבונית מס, may NOT charge VAT**, source: https://www.kolzchut.org.il/he/עוסק_פטור, why core: mislabeling = tax violation. Must use חשבונית עסקה + קבלה instead.
- [x] **Late Payment Law (חוק מוסר תשלומים לספקים תשע"ז-2017) caps**: state authority = 45 days from invoice; local authority = 45 days from month-end (80 for construction); B2B = 45 days from month-end (shotef+45). Source: https://www.nevo.co.il/law_html/law00/144599.htm. Why core: quote must cite the law and default to a freelancer-friendly term within the cap.
- [x] **Quote validity period (תוקף ההצעה)**: standard 14-30 days, up to 40 for enterprise. Source: industry conventions + Contracts Law section 8 (vague "reasonable time" if unstated). Why core: open-ended quotes create legal exposure.
- [x] **Offer becomes irrevocable once delivered with a stated period** (Contracts Law §3(b)), source: https://www.nevo.co.il/law_html/law00/71888.htm. Why core: freelancer must understand a posted quote with a validity window cannot be withdrawn mid-window.
- [x] **Contract formation via offer + acceptance** (Contracts Law §1), source: https://www.nevo.co.il/law_html/law00/71888.htm. Why core: a definite quote that the client accepts in writing = binding contract under Israeli law, even without a separate signed agreement.
- [x] **Document type taxonomy**: הצעת מחיר vs חשבונית עסקה vs חשבונית מס vs הזמנת רכש, source: https://www.greeninvoice.co.il/magazine/hazat-mechir/. Why core: quotes are NOT accounting documents; confusing them with חשבונית עסקה is the #1 freelancer mistake.
- [x] **Mandatory quote fields**: business + client details, itemized pricing with VAT line, timeline, payment terms, validity date, exclusions. Why core: vague quotes are the source of most freelancer-client disputes.
- [x] **"shotef + N" semantics** = end-of-month + N days, NOT N days from invoice. Source: https://hyp.co.il/blog/current-month-plus-30-days/. Why core: Israeli SMB convention; freelancers fluent in English copy "Net 30" and lose 15-30 days of float.

## Should cover (advanced)

- [x] **VAT rounding convention** (agorot, 2 decimal places), banker's rounding to avoid 0.005 inconsistencies.
- [x] **VAT-exempt services (export to non-resident)**: 0% under VAT Law §30(a)(5), still appears on the return.
- [x] **Late payment interest (ריבית פיגורים)** under Late Payment Law §4 + Interest and Linkage Law 5721-1961.
- [x] **Bit/PayBox B2B payments**: 0.6% fee from Jan 2025 (0.8% for Bit from May 2026) on the portion of receipts exceeding 25,000 ₪ per year. Quote can offer Bit but disclose the fee threshold.
- [ ] **Construction quote variant**: late-payment caps differ (80 days local). Skill mentions in the table but doesn't deep-dive (out of scope for general freelancer use case).
- [x] **Status conversion mid-year**: when crossing 122,833 ₪ threshold, must visit regional VAT office to convert oseik patur, oseik morshe.

## Out of scope (explicit)

- Issuing actual חשבונית מס / receipts, related skill: `green-invoice`
- SHAAM allocation numbers / Tax Authority e-invoice compliance, related skill: `israeli-e-invoice`
- Payment processing (charging the client), related skills: `cardcom-payment-gateway`, `tranzila-payment-gateway`
- Bookkeeping / invoice aging, related skill: `israeli-freelancer-ops`
- Chasing unpaid invoices, related skill: `israeli-client-payment-chaser`
- Government tender proposals, related skill: `israeli-tender-proposal-builder`
- Income tax / Bituach Leumi withholding, related skills: `israeli-pension-advisor`, `israeli-bituach-leumi`

## Authoritative sources

- https://taxsummaries.pwc.com/israel/corporate/other-taxes, VAT rate (18% as of 2026)
- https://www.kolzchut.org.il/he/עוסק_פטור, oseik patur threshold + labeling rules
- https://www.nevo.co.il/law_html/law00/144599.htm, full text of חוק מוסר תשלומים לספקים, תשע"ז-2017
- https://www.kolzchut.org.il/he/המועד_האחרון_לתשלום_תמורה_לספקים_עבור_סחורה_או_שירות, plain-language summary
- https://www.nevo.co.il/law_html/law00/71888.htm, full text of חוק החוזים (חלק כללי), תשל"ג-1973
- https://www.greeninvoice.co.il/magazine/hazat-mechir/, Israeli SMB quote-writing guide
- https://hyp.co.il/blog/current-month-plus-30-days/, shotef+N semantics
- https://www.calcalist.co.il/investing/article/rjwfsrxm1x, Bit/PayBox 0.6% fee rules (0.8% Bit from May 2026)
