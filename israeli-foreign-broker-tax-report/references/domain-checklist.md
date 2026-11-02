# Domain Coverage Checklist: israeli-foreign-broker-tax-report

Generated: 2026-11-02. Aggregator sweep: Kol Zchut (capital gains, age-60 relief, olim exemptions) and practitioner bulletins (Alex Shapira and Co., Mas Fax, BSH) used only to surface topics. Every rule below was then read in a primary text: the Income Tax Ordinance (consolidated text on Wikisource), the Conversion Rules 2003, the Regulations on computing capital gain on traded securities 2002, the Filing-Exemption Regulations 1988, the Tax Authority's 2025 forms 1322, 1324, 1325, 1344, the US-Israel treaty and IRS tables. Wikisource is a volunteer consolidation; confirm a section on Nevo or the official gazette before relying on it in a dispute.

## Must cover (core)

- [x] Which exchange rate: the Bank of Israel representative rate, the rate published that day or the last one published before it. Source: Conversion Rules 2003, rule 1. Why core: the single most common error (users take the broker's FX rate or a monthly average).
- [x] Which date: cost at the purchase day (or payment date if earlier), consideration at the sale day (or receipt date if earlier). Source: Conversion Rules, rule 7. Why core: trade date vs settlement date shifts every figure.
- [x] Index for a foreign-currency security held by an individual is the currency rate, not the CPI. Source: Section 88, definition of "מדד"; Form 1325 explanation 4.
- [x] Real gain = gain less inflationary amount; inflationary amount = excess of adjusted cost over cost. Source: Section 88.
- [x] Currency fell between purchase and sale (temporal/direction dimension of the index): gain taxed at the smaller nominal shekel gain (no negative inflationary amount); a loss is allowed only at its real part. Currency rose: loss allowed at nominal; gain is real (dollar gain at the sale rate). Source: Civil Appeal 3555/15 Moses (12.9.16), further hearing denied. Why core: in 2025 the shekel strengthened, so most users are in the "fell" branch.
- [x] FIFO per symbol per portfolio manager (account), unless the seller proves a specific lot. Source: Regulations on computing capital gain (2002), regulations 1 and 5.
- [x] Commissions: added to cost and deducted from consideration; periodic fees excluded from both; management and custody fees deductible from consideration in the year incurred. Source: Form 1325 explanations 3 and 5; Regulations 2002, regulations 1 and 6.
- [x] Rate table BY seller status and asset type: 25% real gain (individual); 30% substantial shareholder (10% of a means of control, at sale or in the 12 months before); 15% unlinked bond, 20% for a substantial shareholder; 35% on the part of a foreign-security real gain for days held up to 31.12.2004 (day-weighted). Source: Sections 88, 91(b); Form 1322 rate list.
- [x] Foreign bonds held by an individual: the currency is the index, so the 15% "unlinked" row should not be assumed; flagged as an open item, not computed.
- [x] Forms: Form 1325 (per-trade, Appendix C1) for securities sold abroad without Israeli withholding; totals to Form 1322 (Appendix C); sales total to field 256 of Form 1301; Form 1324 (Appendix D) for foreign income and foreign tax; Form 1344 for carried-forward losses. Source: 2025 forms.
- [x] Separate Form 1322 for sales whose foreign tax is creditable (sections 203/204). Source: Form 1322 note 3.
- [x] Half-year reporting: no withholding plus a filing obligation means a capital-gain report on 31 July and 31 January for the six months before, with an advance. Source: Section 91(d)(2c)(b); Form 1322 note 6 (separate forms per half, transaction code 65, code 56 with 30.6 or 31.12).
- [x] Loss offset order: current-year capital loss first against real gain; a foreign-asset loss first against foreign gain; a securities loss also against dividends or interest from securities taxed at no more than 25%; not against cash interest. Carry forward against capital gain only, only if a return was filed for the loss year; carried-forward securities losses (2006 onward) not against interest or dividends; carried in shekels. Source: Section 92; Form 1322 note 10; Conversion Rules rule 8.
- [x] Dividends: 25% (30% substantial shareholder); converted at the payment-day rate; US treaty cap 25% with W-8BEN; credit capped at the Israeli tax on that income; excess credit carried 5 years against same-source foreign income. Source: Sections 125B, 200, 204(b), 205A; Conversion Rules rules 3 and 6; treaty Article 12; IRS Table 1; Form 1324 note 5.
- [x] Interest on broker cash: up to 25%; for a foreign-currency asset the index is the currency rate (s.125C definition), so the 15% unlinked row should not be assumed. Goes to Form 1324, not 1322. Source: Section 125C; Form 1324 rows.
- [x] US generally does not tax an Israeli resident's share gains (treaty Article 15(1)), subject to the listed exceptions (among them real property, Article 14(2) property, a permanent establishment, 183 days presence); the list in the skill is not presented as complete.
- [x] Surtax (temporal dimension): 3% on total taxable income above NIS 721,560 (2024 to 2027, Section 121B(a)). The 2% on capital-source income above the same threshold (Section 121B(a1)) applies from tax year 2025 only: Tax Authority execution instruction 5/2025 states the amendment applies to income produced or received from 1 January 2025; for 2024 only the 3% applies. Inflationary amount excluded; outside the advance payment.
- [x] Filing obligation: the "income from a security" exemption needs full withholding, which a foreign broker does not do; the "foreign income" exemption needs an advance payment and a cap of NIS 375,000 (2023 to 2026); the exemption is lost with foreign assets or foreign bank balances of NIS 2,086,000 or more on any day (2023 to 2026), a right in an unlisted foreign company, or surtax liability. Source: Filing-Exemption Regulations 1988, regulations 1 to 3 and schedules.

- [x] Loss brought forward from earlier years (Form 1344): after the current-year loss, against capital gain only, foreign gains first, never against dividends or interest. Source: Section 92(b); Form 1322 note 10.
- [x] All accounts on one Form 1322, including Israeli accounts whose figures come from Form 867 (the 867 route applies when the full tax was withheld). Source: Section 92(a)(1), (3); Form 1322 explanation 2a.
- [x] Gate: Israeli withholding on the account (Form 867) changes the route and removes the half-year report for sales taxed at source. Source: Section 91(d)(2c)(a).
- [x] Half-year report: loss-only half, late reports (Section 91(d)(3) linkage and interest; no fine figure), withheld tax counted toward the advance (Section 91(d)(6)), channel not named (route).
- [x] Dividend netting: reversals and refunds netted per symbol and year before the credit cap; credit capped at the Israeli tax (s.204(b)); the script also caps at the treaty rate and labels the rest "likely not creditable" (unsourced; confirm with a CPA). Sign convention detected from the total, not from a single row.
- [x] Form 1301 mapping: field 256; dividend fields through Form 1324; ownership box and the separate form for inherited or pre-marriage securities (Form 1322 note 5); Form 1301 section H by spouse; securities-turnover question (NIS 2,810,000). Other fields: route to `israeli-tax-returns`.
- [x] Never suggest a sale or its timing for tax effect (legal review).

## Should cover (advanced / edge cases)

- [x] eToro: closed positions split into buy and sale per position (`--etoro`), CFD and crypto rows excluded and routed (crypto to `israeli-crypto-tax-reporter`), position id as specific-lot proof (regulation 5); spreadsheets saved as CSV; export layouts not asserted (check the file).
- [x] Surtax base includes Israeli-account gains and other capital-source income passed in; anything not passed in is excluded and said so.
- [x] US Treasury bills: the discount is interest (Section 125C), Form 1324, not a share sale; flagged.
- [x] IBKR exports may stack sections in one CSV; copy the trades section (check the file). Separate withholding rows folded into the dividend.

- [x] Multi-currency accounts and BoI per-100-unit quotes (UNIT_MULT). Source: BoI SDMX API.
- [x] Sale to a relative goes on Form 1399י, not Form 1322. Source: Form 1322.
- [x] Corporate actions (splits, mergers, spin-offs), transfers between brokers, options and short sales: flagged, not computed.
- [x] Age 60 or over: reduced rates may apply; routed. Source: Kol Zchut.
- [x] New immigrants: 10-year exemption on foreign-source income (Kol Zchut); routed, not decided. Senior returning residents: no statement on the exemption is made (not sourced here); routed to a CPA.
- [x] Lots bought before 1.1.2012 (change date): Section 91(b1) does not apply to securities listed on an exchange before that date; ordinary listed shares stay on the 25% / 35% split of the forms. Source: Section 88, 91(b1)(1b).

## Out of scope (explicit, with rationale)

- Whole annual return and other income: `israeli-tax-returns`.
- Crypto: `israeli-crypto-tax-reporter`.
- Employee options and RSUs: `israeli-stock-options-tax`.
- Analysing Israeli stocks: `tase-stock-analysis`.
- US citizens or green-card holders (dual filing, PFIC): `us-israel-dual-tax-navigator`, `us-person-israeli-investment-check`. A user may well ask; the answer is a route, because a US person's US-side treatment changes the computation.
- Business-level trading (badges of trade): the user may ask; the skill states the question and routes to a CPA, since the answer moves the income out of the capital-gain regime entirely.
- Investment advice: never.

## Authoritative sources

- https://he.wikisource.org/wiki/פקודת_מס_הכנסה (Sections 1, 88, 91, 92, 121B, 125B, 125C, 200 to 205A)
- https://he.wikisource.org/wiki/כללי_מס_הכנסה_(המרה_לשקלים_חדשים_של_סכומים_שמקורם_מחוץ_לישראל)
- https://he.wikisource.org/wiki/תקנות_מס_הכנסה_(חישוב_רווח_הון_במכירת_נייר_ערך_הנסחר_בבורסה,_מילווה_המדינה_או_יחידה_בקרן_נאמנות)
- https://he.wikisource.org/wiki/תקנות_מס_הכנסה_(פטור_מהגשת_דין_וחשבון)
- https://www.gov.il/he/service/reporting-and-payment-2025-annual-tax-report-for-individuals (forms, rendered in a browser)
- http://www.masfax.co.il/%D7%A4%D7%A1%D7%A7%D7%90%D7%95%D7%AA/%D7%94%D7%A2%D7%9C%D7%99%D7%95%D7%9F-%D7%9C%D7%90-%D7%99%D7%95%D7%AA%D7%A8-%D7%A7%D7%99%D7%96%D7%95%D7%96-%D7%94%D7%A4%D7%A1%D7%93%D7%99%D7%9D-%D7%9E%D7%94%D7%A4%D7%A8%D7%A9%D7%99-%D7%A9%D7%A2%D7%A8-%D7%91%D7%A0%D7%99%D7%99%D7%A8%D7%95%D7%AA-%D7%A2%D7%A8%D7%9A (Moses summary)
- https://www.irs.gov/pub/irs-trty/israel.pdf (treaty Articles 12 and 15)

## Known bad figures (do not regress)

- "Convert at the broker's FX rate" or "use the annual average rate": wrong for capital gains; rule 7 sets day rates.
- "A currency-driven loss can be offset": rejected in Moses.
- "Foreign tax goes on Form 1322": the foreign tax column is on Form 1324; Form 1322 only needs a separate form for sales that carry a creditable foreign tax.
- "Cash interest at the broker is a securities item on Form 1322": it is interest on a deposit, reported on Form 1324 and the 1301, and a securities loss does not offset it.
