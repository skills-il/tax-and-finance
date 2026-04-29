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

Published by the Israeli Tax Authority on February 19, 2018, this is the primary guidance document for cryptocurrency taxation.

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
| Surtax (mas yesafim) | +5% (post-2025 reform; verify 2026 figure) | On income (now including capital gains) exceeding the CPI-adjusted threshold (~721,560 NIS for 2025; verify 2026 on mas.gov.il) |

### For Companies (Chevra)

| Income Type | Rate | Notes |
|------------|------|-------|
| Capital gains | 23% | Corporate tax rate |
| Business income | 23% | Corporate tax rate |
| Dividend distribution | 25-30% | Additional tax when distributing to shareholders |

### National Insurance and Health Tax

If crypto income is classified as business income:
- **Bituach Leumi**: 5.97-12.83% depending on income level
- **Mas Briut (health tax)**: 3.1-5% depending on income level
- These do NOT apply to capital gains (investment classification)

## Reporting Requirements

### Form 1325 (Capital Gains Report)

Filed with the annual tax return for capital gain events:
- Required for each disposal (sale or exchange) of crypto
- Lists acquisition date, disposal date, cost basis, proceeds, and gain/loss
- Must be in NIS

### Form 1301 (Annual Individual Tax Return)

The comprehensive annual return that includes:
- All income sources (salary, business, capital gains, passive income)
- Form 1325 is attached as a schedule
- Filing deadline (Form 1301 individual annual return): **May 31** of the following year for online filing (paper filing earlier in May); extensions to end of July or even September available via רואה חשבון. The "April 30" deadline is outdated.

### Advance Tax Payments (Mikdamot)

**Regulation 7 of the Income Tax (Capital Gains Tax) Regulations:**
- Within 30 days of a capital gain event, the taxpayer must file Form 7002 and pay 25% of the gain as an advance
- Applies to gains exceeding a minimal threshold
- Failure to file: interest (ribit) and linkage differences (hafreshei hatzamda) accrue from the 30-day deadline
- The advance is credited against the final annual tax liability

### Reporting Thresholds

- **Any capital gain**: Technically reportable regardless of amount
- **Advance payment**: Required for gains with tax liability exceeding approximately 1,000 NIS
- **Annual filing**: Required for individuals with income from sources other than salary, or with annual income exceeding the filing threshold
- **Record retention**: All transaction records must be retained for 7 years minimum

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
- However, large crypto transactions (over 50,000 NIS) may trigger anti-money laundering (AML) reporting by exchanges
- Israeli banks may request documentation for large crypto-related deposits

### Tax Treaties
- Israel has tax treaties with 50+ countries
- Capital gains from crypto are generally taxable in the country of residence (Israel, for Israeli residents)
- Foreign tax credits may be available if tax was paid in another jurisdiction

### OECD Crypto-Asset Reporting Framework (CARF)
- Israel has committed to implementing CARF
- Expected to require automatic exchange of crypto transaction data between jurisdictions
- Implementation timeline: 2027 (expected)

## Compliance Best Practices

1. **Maintain detailed records**: Every transaction, including dates, amounts, prices, fees, and exchange rates
2. **Convert to NIS**: Keep a running record of NIS values for all transactions
3. **File advance payments**: Within 30 days of significant gain events
4. **Separate wallets**: Consider using separate wallets for different tax classifications (investment vs. business)
5. **Professional advice**: Consult with a tax advisor familiar with crypto for complex situations
6. **Voluntary disclosure**: If past years were not reported, consider the Tax Authority's voluntary disclosure procedure (gilui da'at mirtzon) before they initiate an audit
