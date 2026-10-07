# Domain Coverage Checklist, israeli-price-quote-generator

Generated: 2026-05-19, revised 2026-10-07, via research on: mas.gov.il, btl.gov.il, kolzchut.org.il, nevo.co.il, gov.il, knesset.gov.il, greeninvoice.co.il, taxsummaries.pwc.com

## Must cover (core)

- [x] **Israel VAT rate is 18%** (raised from 17% on 2025-01-01), source: https://taxsummaries.pwc.com/israel/corporate/other-taxes, why core: every quote must compute VAT correctly; a rounding or rate miscalc on a 50k₪ project is real money that disappears.
- [x] **Oseik patur 2026 threshold = 122,833 ₪/year**, source: https://www.kolzchut.org.il/he/עוסק_פטור, why core: oseik patur quotes have different labeling/VAT rules; crossing mid-year forces status change.
- [x] **Oseik patur may NOT issue חשבונית מס, may NOT charge VAT**, source: https://www.kolzchut.org.il/he/עוסק_פטור, why core: mislabeling = tax violation. Must use חשבונית עסקה + קבלה instead.
- [x] **Late Payment Law (חוק מוסר תשלומים לספקים תשע"ז-2017) caps**: state authority = 45 days from invoice; local authority = 45 days from month-end (80 for construction); B2B = 45 days from month-end (shotef+45). Source: https://www.nevo.co.il/law_html/law00/144599.htm. Why core: quote must cite the law and default to a freelancer-friendly term within the cap.
- [x] **Quote validity period (תוקף ההצעה)**: standard 14-30 days, up to 40 for enterprise. Source: industry conventions + Contracts Law section 8 (vague "reasonable time" if unstated). Why core: open-ended quotes create legal exposure.
- [x] **Offer becomes irrevocable once delivered with a stated period** (Contracts Law §3(b)), source: https://www.nevo.co.il/law_html/law00/71888.htm. Why core: freelancer must understand a posted quote with a validity window cannot be withdrawn mid-window.
- [x] **Contract formation via offer + acceptance** (Contracts Law §1), source: https://www.nevo.co.il/law_html/law00/71888.htm. Why core: a definite quote that the client accepts in writing = binding contract under Israeli law, even without a separate signed agreement.
- [x] **Document type taxonomy**: הצעת מחיר vs חשבונית עסקה vs חשבונית מס vs הזמנת רכש, source: https://www.greeninvoice.co.il/magazine/hazat-mechir/. Why core: quotes are NOT accounting documents; confusing them with חשבונית עסקה is the #1 freelancer mistake.
- [x] **Mandatory quote fields**: business + client details, itemized pricing (with a VAT line only where the issuer charges VAT; an oseik patur quote carries no VAT line or "+ מע"מ" wording anywhere), timeline, payment terms, validity date, exclusions.
- [x] **Occupations barred from oseik patur**: regulation 13 of the VAT (Registration) Regulations requires listed occupations (lawyers, accountants, engineers, architects, doctors, interpreters, management consultants and others) to register as oseik morshe regardless of turnover. Source: https://www.kolzchut.org.il/he/עוסק_פטור
- [x] **Client type drives the clauses**: Israeli business, private individual, public body or foreign resident. A private individual is on no Late Payment Law row and is not a withholding payer; whether the law binds a foreign payer is unsettled, so a foreign quote states the agreed term only. Source: https://www.nevo.co.il/law_html/law00/144599.htm and the withholding order on he.wikisource. Script tiers `consumer` and `foreign`. Why core: vague quotes are the source of most freelancer-client disputes.
- [x] **"shotef + N" semantics** = end-of-month + N days, NOT N days from invoice. Source: https://hyp.co.il/blog/current-month-plus-30-days/. Why core: Israeli SMB convention; freelancers fluent in English copy "Net 30" and lose 15-30 days of float.

## Should cover (advanced)

- [x] **VAT rounding convention** (agorot, 2 decimal places), each line rounded, VAT on the rounded subtotal, an exact half agora rounded up.
- [x] **VAT-exempt services (export to non-resident)**: 0% under VAT Law §30(a)(5), still appears on the return.
- [x] **The §30(c) foreign-resident test**: for section 30 a foreign resident counts only when outside Israel with no business or activity in Israel. Source: VAT Law on he.wikisource.
- [x] **The §30(a)(5) dual-beneficiary exception**: not zero-rated where the agreement's subject is that the service is actually rendered, in addition to the foreign resident, also to an Israeli resident in Israel, an Israeli-majority partnership or a company treated as an Israeli resident.
- [x] **Allocation numbers (מספר הקצאה)**: from 01.06.2026 a tax invoice above 5,000 ₪ needs one for the BUYER's input-VAT deduction (10,000 ₪ in H1 2026, 20,000 ₪ in 2025, 25,000 ₪ in 2024). It does not invalidate the invoice; it can be requested retroactively up to a year.
- [x] **Late Payment Law full payer table**: sections 3(a), 3(b), 3(e), 3(f), 3(g), plus the 3(h) incomplete-invoice rule and the two-stage section 4 interest.
- [x] **Late payment interest (ריבית פיגורים)** under Late Payment Law §4 + Interest and Linkage Law 5721-1961.
- [x] **Bit/PayBox B2B payments**: Bit charges 0.8% on the portion of receipts exceeding a cumulative 25,000 ₪ per calendar year (its own pages disagree on the fee's start date, so state the rate and not the date), and caps P2P receipts at 100,000 ₪ per calendar year since 14.11.2024. PayBox's own FAQ (payboxapp.com/faq) lists fee-free receipts up to 100,000 ₪/year on PayBox Plus and 50,000 ₪/year on Basic.
- [x] **Construction quote variant**: the 3(b) and 3(f) construction rows are in the payment table and the script tiers (`state-construction`, `construction`), including the 60-day examination period in 3(h). A full construction-contract workflow (חוק המכר, bank guarantees, retention) stays out of scope.
- [x] **Withholding at source line**: shown for Israeli business and public payers, omitted for private individuals and foreign clients (withholding order, he.wikisource).
- [x] **Retainer quotes**: Template 5 (billing anchor, minimum term, unused hours).
- [x] **Status conversion mid-year**: when crossing 122,833 ₪ threshold, must visit regional VAT office to convert oseik patur, oseik morshe.

## Out of scope (explicit)

- Issuing actual חשבונית מס / receipts, related skill: `green-invoice`
- SHAAM allocation numbers / Tax Authority e-invoice compliance, related skill: `israeli-e-invoice`
- Payment processing (charging the client), related skills: `cardcom-payment-gateway`, `tranzila-payment-gateway`
- Bookkeeping / invoice aging, related skill: `israeli-freelancer-ops`
- Chasing unpaid invoices, related skill: `israeli-client-payment-chaser`
- Government tender proposals, related skill: `israeli-tender-proposal-builder`
- Computing income tax or Bituach Leumi on the freelancer's income, related skills: `israeli-pension-advisor`, `israeli-bituach-leumi`. (Re-checked 2026-10-07: users do ask about withholding on the quote, so the quote-level withholding LINE is in scope; the tax computation is not.)


## Authoritative sources

- https://taxsummaries.pwc.com/israel/corporate/other-taxes, VAT rate (18% as of 2026)
- https://www.kolzchut.org.il/he/עוסק_פטור, oseik patur threshold + labeling rules
- https://www.nevo.co.il/law_html/law00/144599.htm, full text of חוק מוסר תשלומים לספקים, תשע"ז-2017
- https://www.kolzchut.org.il/he/המועד_האחרון_לתשלום_תמורה_לספקים_עבור_סחורה_או_שירות, plain-language summary
- https://www.nevo.co.il/law_html/law00/71888.htm, full text of חוק החוזים (חלק כללי), תשל"ג-1973
- https://www.greeninvoice.co.il/magazine/hazat-mechir/, Israeli SMB quote-writing guide
- https://hyp.co.il/blog/current-month-plus-30-days/, shotef+N semantics
- https://www.bitpay.co.il/he/private-faq, Bit receipt fee (0.8% above a cumulative 25,000 ₪/year) and the 100,000 ₪/year P2P receipt cap
