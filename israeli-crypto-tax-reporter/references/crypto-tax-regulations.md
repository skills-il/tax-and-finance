# Israeli Cryptocurrency Tax Regulations

## Primary Legal Sources

### Income Tax Ordinance (Pekudat Mas Hachnasa)

The Income Tax Ordinance is the foundational tax law in Israel. Key sections relevant to cryptocurrency:

**Section 88 - Definitions:**
- Defines "asset" (neches) broadly to include "any type of property, whether tangible or intangible"
- Cryptocurrency falls under this definition as an intangible asset
- This classification was affirmed in Circular 2018/05

**Section 91 - Capital Gains Tax:**
- Capital gains on the sale of assets are taxable
- The gain is calculated as the difference between the sale price (tmura) and the cost basis (mechir mekorri)
- Adjustable for inflation (hatzmada) in certain cases, though for crypto this is typically not applied

**Section 91(b)(1) - Tax Rate for Individuals:**
- Capital gains for an individual: **25%** on the real gain. Do not state this conditionally on a post-1.1.2012 acquisition: that מועד השינוי split lives in Section 91(b1) and cannot apply to any crypto lot, and phrasing it as a condition invites a hunt for a pre-2012 split rate that does not exist here.
- The 30% rate in Section 91(b)(2) applies to the sale of a **נייר ערך בחבר-בני-אדם**, a security in a body corporate, by a material shareholder. A fungible token is not one, and Circular 05/2018 never invokes 91(b)(2), so do NOT apply 30% to an ordinary crypto disposal. Treat an equity-like token in an incorporated entity as a CPA / pre-ruling question.

**Section 2(1) - Business Income:**
- If crypto trading constitutes a "business" (esek), gains are taxed as ordinary income
- Marginal tax rates apply: 10% to 50% depending on the income bracket
- Plus social insurance (bituach leumi) and health tax (mas briut)

**Section 2(4) - Passive Income:**
- Interest, dividends and similar passive returns from crypto (lending interest, staking rewards)
- **Section 2(4) is a charging section and fixes no rate.** The rate on interest is in Section 125C, whose structure is three-tiered. **125C(b)** sets the general 25%. **125C(c)(1)** charges **15%** where the interest is paid on an asset that is not index-linked, or is only partly linked, or is unlinked to redemption; crypto- and stablecoin-denominated lending is not CPI-linked, so 15% is at least as arguable as 25%. **125C(d)** overrides BOTH and charges the full marginal rate under Section 121 where the interest is income under s.2(1) or is recorded (or required to be recorded) in the recipient's books, where he claimed interest and linkage expenses on the asset, where he is a material shareholder in the payer, or where he is an employee, supplier or other special-relations party of the payer unless the rate is shown to have been set at arm's length. That last limb covers most yield-platform positions. Establish which limb applies rather than defaulting to 25%.

### Circular 2018/05 (Chozar 05/2018)

Published by the Israeli Tax Authority on January 17, 2018 (updated November 14, 2018), this is the primary guidance document for cryptocurrency taxation.

**Key determinations:**

1. **Classification**: Virtual currencies (matbeot virtualiyim) are not considered "currency" (matbea) or "foreign currency" (matbea chutz) under Israeli law. They are classified as assets.

2. **Tax treatment**: Gains from the sale or exchange of virtual currencies are subject to capital gains tax under Chapter E of the Income Tax Ordinance.

3. **Business vs. investment**: the circular acknowledges that crypto activity may constitute a business, but **section 3.1.4 does NOT enumerate a test**. Its whole statement is that classification "ייקבע בהתאם למבחני עסק כפי שנקבעו **בפסיקה**", i.e. by the badge-of-trade tests established in the CASE LAW. Cite the factors (trade frequency and volume, holding period, time and attention, leverage, professional knowledge, financing, inventory-versus-investment intent) as case law, never as this circular. Earlier versions of this file listed them as the circular's own factors; that attribution was wrong and was removed on 2026-08-27.

4. **Mining is business income, categorically.** Section 3.1.4: crypto reaching a person through mining, "יש לראות את ההכנסות המתקבלות בידיו - **כהכנסה עסקית**". There is no hobby-versus-scale alternative in the circular, and earlier versions of this file offered one. For VAT the miner is separately registered as an **עוסק** under section 3.2.3.2.4, which is a different regime again from the מוסד כספי registration that applies to a business-level trader. The cost basis for mined coins includes electricity, equipment depreciation and direct costs.

5. **ICOs and token offerings**: Tokens received in an ICO are treated as an asset acquisition. The cost basis is the amount paid for the tokens. For project founders, token distribution may be treated as income.

6. **Cost basis**: the circular prescribes **no** method. FIFO is the customary Israeli default and another method may be used if applied consistently and documented, but do not attribute FIFO to this circular; earlier versions of this file did.

7. **Currency conversion**: amounts are reported in shekels, but the circular does **not** require the Bank of Israel representative rate and the word יציג does not appear in it. Its actual rule, section 3.1.5.1, is the **fair value in shekels** of the crypto, with an override: where the asset or goods bought carry a **stated price (מחיר נקוב)**, that stated price fixes the crypto's disposal value. The same section requires the SAME figure to serve as the seller's proceeds and the buyer's original cost. The representative rate is a defensible documented choice, not a legal requirement; earlier versions of this file asserted the circular required it.

8. **Record retention**: section 3.1.3 requires documents to be kept "ככול שיידרש להנחת דעתו של פקיד השומה" and fixes **no** period.

9. **VAT**: section 3.2.3.2.3 registers a business-level trader as a **"מוסד כספי"** under **Section 4 of the VAT Law**, not as an osek charging 18% output VAT; 3.2.3.2.4 registers the miner as an **עוסק**; 3.2.3.1 leaves a non-business investor outside VAT entirely.

### Subsequent Guidance and Court Rulings

**ITA Circular 07/2018 ("Taxation of Token Issuance for Services / Products in Development"):**
- Addressed taxation of utility-token vs security-token issuances
- Utility tokens: treated as prepaid service rights (may carry VAT implications for the issuer)
- Security tokens: treated as securities under existing tax rules

**District-court line of decisions, 2020-2024:**
- Multiple Israeli district-court rulings (including Be'er Sheva District) have classified frequent crypto trading (high transaction volume relative to portfolio size, sustained over multiple years, with active position management) as a business activity, taxing the gains at marginal income rates instead of 25% capital gains. Specific case names (Copel, Norkin and others) should be looked up by the agent on `psakdin.co.il` or `nevo.co.il` before being cited.
- The ITA's position that crypto is a taxable asset (not foreign currency) has been consistently upheld; agents should never cite specific case docket numbers without first verifying them on a legal database.

**Note on case citations:** never invent or fabricate ruling numbers. If a specific docket is needed, look it up on `nevo.co.il`, `psakdin.co.il`, or the Israeli Tax Authority's published rulings (`mas.gov.il/החלטות-מיסוי`); otherwise, describe the line of authority generically.

## Tax Rates Summary

### For Individuals (Yachid)

| Income Type | Rate | Notes |
|------------|------|-------|
| Capital gains (investment) | 25% | Standard rate for assets held as investment |
| Capital gains, material shareholder, Section 91(b)(2) | up to 30% | Applies to a **security in a body corporate**, not to a fungible token. Do not default crypto here |
| Business income | 10-50% | Marginal rates based on total income |
| Passive income (interest/dividends) | 25% | From crypto lending, some staking |
| Surtax (mas yesafim) - 2026 | 3% base + 2% additional on capital-source income (effective 5% on crypto gains in the band above threshold) | Threshold NIS 721,560 / monthly NIS 60,130, **frozen through tax year 2027** by the Dec 2024 indexation-pause amendment. The 2025 reform brought capital gains into the surtax base. |

### For Companies (Chevra)

| Income Type | Rate | Notes |
|------------|------|-------|
| Capital gains | 23% | Corporate tax rate |
| Business income | 23% | Corporate tax rate |
| Dividend distribution | 25-30% | Additional tax when distributing to shareholders |

### National Insurance and Health Tax (2026)

If crypto income is classified as business income (not investment):
- **Bituach Leumi (self-employed, 2026)**: **4.47% on income up to ~NIS 7,703/month; 12.83% on the portion above** (per btl.gov.il). Verify the current bracket and ceiling at the start of each tax year.
- **Mas Briut (health tax, 2026)**: **3.23% on income up to the same threshold; 5.17% on the portion above**.
- Combined effective rate (BL + Mas Briut): roughly **7.7% / 18%** across the two bands.
- These rates do NOT apply to capital gains (investment classification) - only to income classified as a business under Section 2(1).

## Reporting Requirements

### Reporting forms: the ITA's own published titles

Taken from the Tax Authority's annual-return service page. The titles are narrower than this skill previously assumed, so read them before routing a crypto disposal onto a form.

| Form | ITA title | What it actually covers |
|---|---|---|
| 1399י | הודעה על מכירת נכס וחישוב המס המגיע | Sale of an **asset**. The Section 91(d)(1) 30-day notice, and the right vehicle for a crypto disposal. 1399ח is the company equivalent |
| 1322 | רווחי הון מניירות ערך סחירים **(הנסחרים בבורסה)** | Gains on **exchange-traded** securities |
| 1325 | טופס עזר לריכוז מכירות של ניירות ערך **על פי שיעורי המס** | Auxiliary aggregating securities sales **by tax rate**. Nothing in the title concerns withholding |
| 1326 | רווחי הון מניירות ערך סחירים | A further securities form |
| 1326א | טופס עזר לחישוב רווח או הפסד ריאלי ממניות שליטה | The ITA's own real-gain / inflationary-amount split helper |
| 1320 | דוח רווח והפסד לבעלי עסק עצמאי **(נספח א)** | The only one of these carrying a נספח label |
| 1344 | דיווח על הפסדים מועברים משנת מס קודמת | Losses brought forward, which is where a Section 92 carry-forward lands |

**The "Nispach Gimel" labels earlier versions of this skill attached to 1322 and 1325 are not the ITA's.** On the ITA's page the נספח labels belong to 1320. Since 1322, 1325 and 1326 are all titled as securities forms and crypto is a נכס, confirm with the assessing officer or a CPA which appendix the ITA expects for a non-securities asset rather than asserting one.

### Retracted: the old Form 1322 + Form 1325 routing

Earlier versions of this file told the reader to itemise crypto disposals on Form 1325 and carry the totals to Form 1322 as "Nispach Gimel". **That routing is withdrawn.** Both forms are titled by the ITA as ניירות ערך forms, 1322 expressly as securities הנסחרים בבורסה, and neither carries a נספח label on the ITA's page. Use the table above.
- Lists acquisition date, disposal date, cost basis, proceeds, and gain/loss for each disposal.
- All amounts must be in NIS.

### Form 1301 (Annual Individual Tax Return)

The comprehensive annual return that includes:
- All income sources (salary, business, capital gains, passive income)
- **For a crypto gain there is no ITA "crypto appendix", so do not attach 1322 or 1325**, which the ITA titles as securities forms. The gain is entered in the 1301's own capital-gains fields at the 25% line, supported by: a copy of each Form 1399י already filed with the assessing officer (its tax paid is credited against the s.91(d) advance); a self-prepared disposal schedule in the 1399י columns, one line per FIFO-matched disposal (asset, יום הרכישה, יום המכירה, מחיר מקורי, תמורה, real gain); and **Form 1344** where a loss is brought forward, which s.92(b) allows only if a return was filed for the loss year. Where the same taxpayer also disposed of exchange-traded securities, 1322 and 1325 carry THOSE, and only those. Confirm the final packaging with the assessing officer or a CPA
- **Filing deadline for tax year 2025 (filed in 2026): 30 June 2026 for online filing via the gov.il portal; 29 May 2026 for paper filing.** Extensions to end of July or September are available for returns filed by a representing accountant. The "April 30" or "May 31" dates that appeared in older guides are outdated; verify the current-year deadline on gov.il/he/service.

### Advance Tax Payments (Mikdamot)

**Form 1399י (1399-yod) - capital gains advance payment for individuals:**
- Within 30 days of a capital gain event, the taxpayer files Form 1399י with the assessing officer (pakid shuma) and pays 25% of the gain as an advance.
- Virtual-currency disposals are filed with transaction codes **77** (sale) and **71** (virtual currency).
- Form 1399ח is the equivalent form for companies.
- Applies to gains exceeding a minimal de minimis threshold; for non-trivial crypto gains assume the form is required.
- Failure to file: interest (ribit) and linkage differences (hafreshei hatzamda) accrue from the 30-day deadline.
- The advance is credited against the final annual tax liability.
- The "Form 7002" reference in older guides is outdated for crypto reporting - use Form 1399י.

### Form 909 (Paying Tax When a Bank Refuses Crypto Funds)

A distinct, very common Israeli problem: a commercial bank refuses (in writing) to accept crypto-derived deposits, so the taxpayer cannot fund the tax payment through a normal account. The ITA, jointly with the Bank of Israel and the Anti-Money-Laundering Authority, published a temporary procedure (Hora'at Sha'a, ITA Instruction 06/2024, "נוהל לקבלת כספי מסים בשל רווח ממימוש אמצעי תשלום מבוזר", published 03.04.2024 and updated 22.10.2025) for this case:

- **Who**: an individual (NOT a company) who realised a crypto gain and has no alternative funding source, after at least one Israeli commercial bank refused the funds (including refusing to open an account).
- **Form**: **Form 909** ("דיווח על פעילות במטבעות וירטואליים ובקשה לתשלום המס המגיע במימוש המטבעות").
- **Required attachments**: written bank-refusal letter; working paper computing the taxable income and tax; proof of the legal source of the funds used to buy the coins; a money-trail working paper for the coins over the holding period; deposit/account-management confirmations from the financial-service provider.
- **How**: filed to the assessing officer either online via the ITA CRM together with the annual return, or physically.
- **Outcome**: after a money-laundering-risk review and a tax assessment under Section 145, the tax is paid in NIS directly into the ITA's account at the Bank of Israel.

### Reporting Thresholds

- **Any capital gain**: technically reportable regardless of amount.
- **Advance payment (mikdama)**: required for non-trivial gains. Verify current-year de minimis amounts on the ITA service portal; do not rely on a fixed historical NIS figure.
- **Annual filing**: required for individuals with income from sources other than salary, or with annual income exceeding the filing threshold. A crypto disposal generally creates a filing obligation, but a TY2025 draft amendment to the exemption-from-filing regulations (טיוטת תקנות מס הכנסה (פטור מהגשת דין וחשבון), published for public comment January 2025) would exempt a salaried taxpayer from filing on crypto gains where the crypto was traded through a supervised Israeli platform that withheld the tax at source AND the year's digital-asset sales stay under a **digital-asset-specific ceiling set in תוספת ו** of the exemption regulations. The enabling power is **Section 134A**; Section 131 is the filing duty being exempted FROM. **Do not quote the general Section 131 ceilings for this**, which earlier versions of this file did: they are a different mechanism. Incomplete withholding or trading through an unsupervised or foreign venue restores the full filing duty; paying an advance does not by itself remove it. Still a draft, so verify enactment and read the ceiling out of the regulation text.
- **Record retention**: Circular 05/2018 section 3.1.3 requires documents to be kept "ככול שיידרש להנחת דעתו של פקיד השומה" and fixes **no period**. The seven-year figure comes from the bookkeeping directives, not from this circular. Confirm the applicable period rather than citing the circular for it.

### Voluntary Disclosure Procedure 2025-2026 (Crypto Track)

Published 25 August 2025 by the ITA, this procedure expressly covers digital assets and provides a route to regularise prior-year unreported crypto gains in exchange for criminal immunity:

- **Two tracks**:
  - **Green Track** - for the digital-asset limb, income from digital assets **not exceeding NIS 500,000 for the entire disclosure period** (NOT per year, which earlier versions of this file said), where the fair value of ALL the applicant's digital assets at **31 December 2024** did not exceed **NIS 1,500,000**. The Tax Authority, not the applicant, decided the track. Anonymity removed.
  - **Regular Track** - for cases above those thresholds.
- **Deadline**: declared 25 August 2025, end date **31 August 2026**. **Check today's date before advising anyone to use it, because the answer flips on 1 September 2026.** Up to and including 31.8.2026 the window is OPEN and immunity is available; after it, there is no immunity to obtain and the route is an ordinary Section 131 correction through the assessing officer, with the exposure that normally attaches to a late or amended return. Do not assume a successor procedure has been declared; check.
- **Anonymity**: not available; all applications include the taxpayer's identifying details.
- Use this procedure for clients who held crypto without reporting in prior years and want to come into compliance before CARF data-sharing surfaces them.

### CARF (OECD Crypto-Asset Reporting Framework)

- Israel committed to CARF; Israeli RCASPs (Reporting Crypto-Asset Service Providers - exchanges, wallet providers) **collect customer data from 1 January 2026**.
- **First international exchange: 2028.** The OECD Global Forum's CARF commitments list places Israel in the group of "Jurisdictions undertaking first exchanges by **2028**", alongside Australia, Canada, Hong Kong, Singapore, Switzerland and the UAE; the 2027 group is a different list of jurisdictions. Earlier versions of this file hedged to "2027-2028"; the primary source resolves it to 2028. Re-verify against the current commitments list, since the Global Forum revises it.
- For taxpayers, this means: crypto held on an Israeli or foreign CARF-participating exchange becomes visible to the ITA once exchanges begin, on data already being collected from 2026. Past-year non-compliance is increasingly likely to surface during routine matching.

## DeFi-Specific Guidance

The Israeli Tax Authority has not published comprehensive DeFi guidance. The following represents the conservative consensus among Israeli tax professionals:

### Staking
- **Conservative view**: Income at receipt (market value), taxed at 25% (passive income) or marginal rates (if part of business)
- **Alternative view**: Capital gain treatment (similar to stock splits), taxed at 25% upon sale
- **Recommended approach**: Report as income at receipt to avoid penalties, claim as capital gain if challenged

### Liquidity Provision
- Providing liquidity to a pool: generally not a taxable event
- Receiving LP tokens: not taxable (represents the existing position)
- Impermanent loss: not deductible until the position is closed
- Withdrawing from pool: may trigger a taxable event if the composition differs from the deposit
- Yield/fee rewards: income at receipt

### Airdrops
- Unsolicited airdrops: income at market value on receipt date
- Airdrops requiring action (claiming, staking): still income at receipt
- Airdrop tokens that are worthless at receipt: zero income, zero cost basis
- Cost basis for future sale: market value at receipt

### NFTs
- Creating and selling NFTs: business income for artists/creators
- Purchasing and reselling NFTs: capital gain (or business income if frequent)
- Receiving NFTs as rewards: income at market value
- NFT-to-NFT trades: taxable as crypto-to-crypto exchanges

### Wrapped Tokens
- Wrapping (e.g., ETH to WETH): generally not a taxable event (same economic exposure)
- Cross-chain bridges: may be taxable if involving a swap mechanism
- Synthetic assets: treated based on the underlying asset's tax treatment

## International Considerations

### Foreign Exchange Controls
- Israel does not have strict foreign exchange controls
- Crypto service providers in Israel operate under the Prohibition on Money Laundering Order for financial-asset-service providers, which sets a ceiling on "casual customer" activity before full identification and recording duties attach, and requires reports on suspicious or threshold activity. **The specific shekel ceiling is UNVERIFIED here**: the figure this file previously stated could not be confirmed against any reachable primary source, so read it out of the Order itself before relying on it. Note this is AML reporting by the PROVIDER, separate from the taxpayer's own tax-reporting duty
- Israeli banks may request documentation for large crypto-related deposits

### Tax Treaties
- Israel has tax treaties with 50+ countries
- Capital gains from crypto are generally taxable in the country of residence (Israel, for Israeli residents)
- Foreign tax credits may be available if tax was paid in another jurisdiction

### OECD Crypto-Asset Reporting Framework (CARF) - see Reporting Requirements above
- See the dedicated CARF block under "Reporting Requirements" for current dates: collection from 1 January 2026, first international exchange **2028** per the OECD commitments list.

## Compliance Best Practices

1. **Maintain detailed records**: Every transaction, including dates, amounts, prices, fees, and exchange rates
2. **Convert to NIS**: Keep a running record of NIS values for all transactions
3. **File advance payments**: Within 30 days of significant gain events
4. **Separate wallets**: Consider using separate wallets for different tax classifications (investment vs. business)
5. **Professional advice**: Consult with a tax advisor familiar with crypto for complex situations
6. **Voluntary disclosure**: If past years were not reported, consider the Tax Authority's voluntary disclosure procedure (nohal gilui mirtzon) before they initiate an audit


## Section 100A: the exit tax on ceasing Israeli residency

Quoted from the Income Tax Ordinance. The section has five subsections, (a) to (e), and there is **no subsection (b1)**; the separate section **100A1** deals with distributions out of revaluation profits and is a different provision entirely.

- **(a)** An asset of an Israeli resident who ceases to be an Israeli resident **is deemed sold on the day before** residency ends.
- **(b)** A person who **did not pay** the tax at that point **"יראו אותו כאילו ביקש לדחות"**, is deemed to have requested deferral, to the date of realization. **Deferral is a deeming rule, not an election**: there is no form and no choice. He then pays the tax on the "chargeable portion of the gain". The provision closes: **"ואולם, הפרשי הצמדה וריבית, כהגדרתם בסעיף 159א ייווספו רק החל במועד המימוש ועד לתשלום המס בפועל"**, so **neither interest nor linkage differentials accrue during the deferral period**; they run only from realization to actual payment.
- **(c)** Where the sale is in any event chargeable to Israeli tax at realization, the ordinary capital-gains tax applies **instead of** (b).
- **(d)** **"חלק הרווח החייב"** is the **real** capital gain **at the date of realization**, multiplied by the holding period from acquisition to cessation of residency, divided by the whole period from acquisition to realization. Three consequences: it is apportioned by **elapsed time**, not by a valuation at exit; it is measured at **realization**, so post-emigration appreciation enlarges the Israeli base pro rata; and it is the **real** gain, net of the inflationary amount. **"מימוש"** is defined as the actual sale of the asset.
- **(e)** The Finance Minister may make implementing regulations, including on double-tax relief and reporting.

The FIFO calculator does not model any of this. Route relocation scenarios to a CPA.

## Form 909: paying when a bank refuses crypto-derived funds

Where a commercial bank refuses **in writing** to accept crypto-derived deposits, an **individual** (not a company) may file **Form 909**, "דיווח על פעילות במטבעות וירטואליים ובקשה לתשלום המס המגיע במימוש המטבעות", with the assessing officer and pay the tax in shekels directly into the Tax Authority's account at the Bank of Israel. The route is a temporary procedure (הוראת שעה) under ITA Instruction 06/2024, run with the Bank of Israel and the Anti-Money-Laundering Authority.

Required attachments: the written bank-refusal letter, a taxable-income working paper, a full money-trail of the coins, and proof of the legal source of the original funds. Filed online through the ITA CRM with the annual return, or physically at the assessing officer. The request goes through a money-laundering risk review before the payment is accepted.
