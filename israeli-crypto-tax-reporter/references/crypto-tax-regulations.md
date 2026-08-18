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
- Capital gains from assets acquired after January 1, 2012: 25%
- For "significant shareholders" (baal meniayot mahuti, holding 10%+ of a project): 30%

**Section 2(1) - Business Income:**
- If crypto trading constitutes a "business" (esek), gains are taxed as ordinary income
- Marginal tax rates apply: 10% to 50% depending on the income bracket
- Plus social insurance (bituach leumi) and health tax (mas briut)

**Section 2(4) - Passive Income:**
- Interest, dividends, and similar passive returns from crypto (e.g., lending interest, staking rewards)
- Taxed at 25% for individuals (passive income rate)

### Circular 2018/05 (Chozar 05/2018)

Published by the Israeli Tax Authority on January 17, 2018 (updated November 14, 2018), this is the primary guidance document for cryptocurrency taxation.

**Key determinations:**

1. **Classification**: Virtual currencies (matbeot virtualiyim) are not considered "currency" (matbea) or "foreign currency" (matbea chutz) under Israeli law. They are classified as assets.

2. **Tax treatment**: Gains from the sale or exchange of virtual currencies are subject to capital gains tax under Chapter E of the Income Tax Ordinance.

3. **Business vs. investment**: The circular acknowledges that in some cases, crypto activity may constitute a business. Factors for determination include:
   - Frequency and volume of transactions
   - Whether the taxpayer devotes significant time to trading
   - Whether the taxpayer uses leverage or sophisticated strategies
   - Whether the taxpayer has other sources of income
   - The taxpayer's professional knowledge of the market

4. **Mining**: Mining income may be classified as business income (if conducted as a business) or as creation of an asset (capital treatment). The cost basis for mined coins includes electricity, equipment depreciation, and direct costs.

5. **ICOs and token offerings**: Tokens received in an ICO are treated as an asset acquisition. The cost basis is the amount paid for the tokens. For project founders, token distribution may be treated as income.

6. **Cost basis**: FIFO method is the default. Other methods may be used if consistently applied and documented.

7. **Currency conversion**: All amounts must be converted to NIS for reporting purposes, using Bank of Israel exchange rates.

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
| Capital gains (significant shareholder) | 30% | Holding 10%+ of a project |
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

### Form 1322 + Form 1325 (Annual Capital Gains Schedule)

Filed with the annual tax return for capital gain events:
- **Form 1322** (Nispach Gimel) is the primary capital-gains appendix to the annual return; totals land here.
- **Form 1325** (Nispach Gimel(1)) is the auxiliary detail form for negotiable-securities sales where tax was NOT withheld at source. Most crypto sales (no Israeli source-withholding) are itemised on Form 1325 and totals carry to Form 1322.
- Lists acquisition date, disposal date, cost basis, proceeds, and gain/loss for each disposal.
- All amounts must be in NIS.

### Form 1301 (Annual Individual Tax Return)

The comprehensive annual return that includes:
- All income sources (salary, business, capital gains, passive income)
- Forms 1322 and 1325 attached as appendices
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

A distinct, very common Israeli problem: a commercial bank refuses (in writing) to accept crypto-derived deposits, so the taxpayer cannot fund the tax payment through a normal account. The ITA, jointly with the Bank of Israel and the Anti-Money-Laundering Authority, published a temporary procedure (Hora'at Sha'a, ITA Instruction 06/2024, first issued 31 December 2023) for this case:

- **Who**: an individual (NOT a company) who realised a crypto gain and has no alternative funding source, after at least one Israeli commercial bank refused the funds (including refusing to open an account).
- **Form**: **Form 909** ("דיווח על פעילות במטבעות וירטואליים ובקשה לתשלום המס המגיע במימוש המטבעות").
- **Required attachments**: written bank-refusal letter; working paper computing the taxable income and tax; proof of the legal source of the funds used to buy the coins; a money-trail working paper for the coins over the holding period; deposit/account-management confirmations from the financial-service provider.
- **How**: filed to the assessing officer either online via the ITA CRM together with the annual return, or physically.
- **Outcome**: after a money-laundering-risk review and a tax assessment under Section 145, the tax is paid in NIS directly into the ITA's account at the Bank of Israel.

### Reporting Thresholds

- **Any capital gain**: technically reportable regardless of amount.
- **Advance payment (mikdama)**: required for non-trivial gains. Verify current-year de minimis amounts on the ITA service portal; do not rely on a fixed historical NIS figure.
- **Annual filing**: required for individuals with income from sources other than salary, or with annual income exceeding the filing threshold. A crypto disposal generally creates a filing obligation, but a TY2025 draft amendment to the exemption-from-filing regulations (טיוטת תקנות מס הכנסה (פטור מהגשת דין וחשבון), published for public comment January 2025) would exempt a salaried taxpayer from filing on crypto gains where the crypto was traded through a supervised Israeli platform that withheld the tax at source AND total income stays under the Section 131 ceilings (about NIS 723,000 gross from work/business, or NIS 721,560 total taxable income from all sources). Exceeding either ceiling, incomplete withholding, or trading through an unsupervised/foreign venue restores the full Section 131 filing duty; paying an advance does not by itself remove it. The regulation was still in draft as of mid-2026 - verify the enacted text before relying on the exemption.
- **Record retention**: all transaction records must be retained for 7 years minimum.

### Voluntary Disclosure Procedure 2025-2026 (Crypto Track)

Published 25 August 2025 by the ITA, this procedure expressly covers digital assets and provides a route to regularise prior-year unreported crypto gains in exchange for criminal immunity:

- **Two tracks**:
  - **Green Track** - annual income up to NIS 500,000 and cumulative crypto assets up to NIS 1.5M as of 31 December 2024. Faster processing, anonymity removed.
  - **Regular Track** - for cases above those thresholds.
- **Deadline**: applications must be submitted by **31 August 2026**.
- **Anonymity**: not available; all applications include the taxpayer's identifying details.
- Use this procedure for clients who held crypto without reporting in prior years and want to come into compliance before CARF data-sharing surfaces them.

### CARF (OECD Crypto-Asset Reporting Framework)

- Israel committed to CARF; Israeli RCASPs (Reporting Crypto-Asset Service Providers - exchanges, wallet providers) **collect customer data from 1 January 2026**.
- **First international exchange**: expected 2027-2028. Israel is among the committed jurisdictions, but the exact first-exchange year has shifted between OECD monitoring updates, so verify it against the latest OECD CARF commitments list before relying on it.
- For taxpayers, this means: any crypto held on an Israeli or foreign-but-CARF-participating exchange will be visible to the ITA from 2027 onwards. Past-year non-compliance is increasingly likely to surface during routine matching.

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
- Crypto service providers in Israel operate under the Prohibition on Money Laundering Order for financial-asset-service providers: a NIS 50,000 per-six-months ceiling applies to "casual customer" activity before full identification/recording duties attach, and providers file reports on suspicious or threshold activity. Note this is AML reporting by the provider, which is separate from the taxpayer's own tax-reporting duty
- Israeli banks may request documentation for large crypto-related deposits

### Tax Treaties
- Israel has tax treaties with 50+ countries
- Capital gains from crypto are generally taxable in the country of residence (Israel, for Israeli residents)
- Foreign tax credits may be available if tax was paid in another jurisdiction

### OECD Crypto-Asset Reporting Framework (CARF) - see Reporting Requirements above
- See the dedicated CARF block under "Reporting Requirements" for current dates: collection from 1 January 2026, first international exchange expected 2027-2028.

## Compliance Best Practices

1. **Maintain detailed records**: Every transaction, including dates, amounts, prices, fees, and exchange rates
2. **Convert to NIS**: Keep a running record of NIS values for all transactions
3. **File advance payments**: Within 30 days of significant gain events
4. **Separate wallets**: Consider using separate wallets for different tax classifications (investment vs. business)
5. **Professional advice**: Consult with a tax advisor familiar with crypto for complex situations
6. **Voluntary disclosure**: If past years were not reported, consider the Tax Authority's voluntary disclosure procedure (gilui da'at mirtzon) before they initiate an audit
