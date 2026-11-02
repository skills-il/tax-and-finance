# Forms and filing (טפסים וחובת דיווח)

Consult when assembling the summary block. Form numbers and fields are read from the Tax Authority's 2025 forms; check the year's form before transcribing, since field codes can move.

## Where each figure goes

| Figure | Form | Notes |
|---|---|---|
| Per-trade computation | Form 1325 (Appendix C1, נספח ג1) | One form per tax rate. Columns: original price (a), 1 + rate of index rise (b), adjusted price (c = a x b), consideration (d), real gain (d - c), loss (d - a). Securities sold abroad not through Israeli withholding agents go here (Form 1322 explanation 2b). |
| Gains by rate, offsets | Form 1322 (Appendix C, נספח ג) | Totals carried from Form 1325. Tick "נכס בחו"ל". Separate forms for each half-year without withholding (transaction code 65, code 56 = 30.6 or 31.12). A separate form for sales eligible for a foreign tax credit (note 3). |
| Total sales | Form 1301 field 256 | Form 1322 note 11. |
| Dividends, interest, foreign tax | Form 1324 (Appendix D, נספח ד) | Dividends at 25% in the row also included in Form 1301 fields 141, 241, 341. On the 2025 form that row carries 462 (income) and 431 (foreign tax). Foreign tax on attached certificates only. Includes unused excess credit under Section 205A. |
| Sales total of traded securities, foreign | Form 1324, capital-gain line | "as recorded on Form 1322"; on the 2025 form 439 and 422. |
| Losses carried forward | Form 1344 | In shekels. |
| Sale to a relative | Form 1399י or Form 1399ח | Not Form 1322. |
| Securities under the repealed section 6 transition | Form 1326 (Appendix C2) | Not Form 1325. |

## Form 1301: what this skill maps

| Item | Where | Status |
|---|---|---|
| Total sales of traded securities | Form 1301 field 256 (line 39), from Appendices C, C1, C2; includes the Form 867 accounts' sales (pass `--israeli-sales`) | Mapped |
| Dividends at 25% | Form 1301 fields 141, 241, 341, through Form 1324 | Mapped |
| Securities turnover above NIS 2,810,000 | Yes/no question at the top of Form 1301 | Mapped |
| Whose securities | Form 1322 ownership box (שייכות): individual, registered spouse, spouse; a separate Form 1322 for inherited or pre-marriage securities (note 5); Form 1301 section H by spouse | Mapped |
| Net real gain lines, tax computation, interest fields, advances paid | Carried from Form 1322 and Form 1324 into the return | Not mapped: check the year's form, or `israeli-tax-returns` |

Form 1301 line 87 (tax withheld at source) excludes advances and foreign tax, so do not put a half-year advance there.

## Israeli accounts (Form 867)

When an Israeli withholding agent withheld the full tax, the gain is taken from Forms 867A and 867B (Form 1322 explanation 2a), not from Form 1325. Those gains and losses still meet the foreign-broker figures on the same Form 1322: a foreign loss goes first against foreign gains, then against Israeli gains (Section 92(a)(3)).

## Do I have to file?

The Filing-Exemption Regulations 1988 (תקנות מס הכנסה (פטור מהגשת דין וחשבון)):

- "Income from a security" is exempt only if it was exempt or the full tax was withheld (regulation 1). A foreign broker does not withhold Israeli tax.
- "Foreign income" is exempt only up to NIS 375,000 (2023 to 2026, Schedule D) AND only if an advance tax payment (מקדמת מס) was paid on it.
- The exemption never applies (regulation 3) if the individual, spouse or a child under 18: held, on any day of the year, foreign assets of NIS 2,086,000 or more (2023 to 2026); held foreign bank balances of the same amount; held a right in a foreign company whose securities are not exchange-traded; or is liable to the Section 121B surtax.

## Half-year report

Section 91(d)(2c)(b): no withholding at source plus an obligation to file under Section 131 means a capital-gain report on 31 July (sales January to June) and 31 January (sales July to December), with an advance in the amount of the tax. Section 91(d)(2c)(a) exempts only sales where tax was withheld under Section 164. The surtax is outside the advance (Section 121B(b)).

- A loss-only half has no advance to pay; record it on that half's Form 1322.
- Late: report and pay now. Section 91(d)(3) charges linkage differentials and interest on an advance paid late or short. This skill gives no fine figure; route to a CPA.
- Credit: tax withheld on the gain counts as paid on account of the advance (Section 91(d)(6)); advances paid are credited against the year's tax. Keep the payment confirmations.
- Channel: not named here; ask the Tax Authority or a representative.

## Dividends and the credit

- Israeli rate: 25% for an individual, 30% for a substantial shareholder in the payer (Section 125B).
- US treaty: US tax on dividends to an Israeli-resident individual capped at 25 percent of the gross (Article 12(2)(a)); IRS Table 1 lists Israel at 25. The broker applies it only with a W-8BEN (IRS: give it to the withholding agent if you are a foreign person and the beneficial owner).
- Credit (Sections 200, 204(b)): foreign tax, translated to shekels, credited up to the Israeli tax on the same income. Excess carries forward 5 years against foreign income from the same source (Section 205A).
- Other countries: the script also caps the credit at that treaty's dividend rate and labels tax above it "likely not creditable", kept apart from s.205A excess. This cap is not stated in the evidence this skill carries; confirm the treatment with a CPA, and ask the broker whether the excess can be corrected or reclaimed. The script takes `--treaty COUNTRY=rate` and flags a dividend withheld above 15% when no rate is given.
- Reversals and refunds: net them per symbol and year, each row at its own payment-day rate, before applying the caps.
- Share gains: the US exempts an Israeli resident (treaty Article 15(1)), subject to the exceptions listed there, among them real property, property described in Article 14(2), a permanent establishment, and 183 days or more of presence. Read the article for the full list.

## Interest on broker cash

Up to 25% for an individual (Section 125C(b)); 15% applies to an asset not linked to the index (Section 125C(c)(1)), but for an asset in foreign currency the index is the currency rate (Section 125C definition). Reported on Form 1324 and the 1301. A securities loss offsets only interest and dividends from securities (Section 92(a)(4)), so it does not reach deposit interest.

## Surtax

For 2024 to 2027 the threshold is NIS 721,560: 3% on total taxable income above it (Section 121B(a)). From tax year 2025 a further 2% applies to capital-source income above it (Section 121B(a1); Tax Authority instruction 5/2025); it does not apply to 2024. Inflationary amounts are excluded (Section 121B(e)). A liability also removes the filing exemption.
