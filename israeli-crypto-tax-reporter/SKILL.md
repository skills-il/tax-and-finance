---
name: israeli-crypto-tax-reporter
description: Calculate cryptocurrency capital gains tax per Israeli Tax Authority (Reshut HaMisim) regulations and generate Form 1322/1325 reporting data and Form 1399י advance-payment data (within 30 days of disposal). Use when a user needs to compute crypto tax obligations using FIFO cost basis, classify DeFi income (staking, liquidity mining, airdrops) for Israeli tax purposes, prepare annual tax filing data, understand reporting thresholds and advance payment (mikdamot) requirements, or evaluate the 2025-2026 Voluntary Disclosure Procedure (open until 31 Aug 2026). Covers Section 88 of the Income Tax Ordinance, Circular 2018/05, the 25% capital gains rate for individuals, and the 5% surtax on capital income above NIS 721,560 (threshold frozen through 2027). Do NOT use for non-Israeli tax jurisdictions, general income tax calculations, or VAT (maam) on crypto business activities, which require separate professional consultation.
license: MIT
allowed-tools: Bash(python:*) Read Edit Write WebFetch
compatibility: Requires Python 3.8+ for calculator script
---

# Israeli Crypto Tax Reporter

## Instructions

### Step 1: Understand the Israeli Crypto Tax Framework

Before performing any calculations, ensure you understand the key regulatory principles:

**Core legal basis:**
- Cryptocurrency is classified as an **asset** (neches) under Section 88 of the Income Tax Ordinance (Pekudat Mas Hachnasa), not as currency.
- Gains from selling crypto are taxed as **capital gains** (revach hon) under Chapter E of the Ordinance.
- The Israeli Tax Authority published **Circular 2018/05** (chozar 05/2018) which provides the primary guidance on crypto taxation.
- The circular was reinforced by subsequent guidance and court rulings establishing that crypto is a taxable asset.

**Tax rates:**
- **Individuals**: 25% capital gains tax on profits. If the seller is a "significant shareholder" (baal meniayot mahuti) of a crypto project, the rate is 30%.
- **Business/traders**: If crypto activity constitutes a business (esek), gains are taxed as ordinary income at marginal rates (up to 47%, plus the surtax) instead of the 25% capital rate. This is the single highest-stakes determination in crypto tax. Circular 05/2018 sets out the "badge of trade" factors the assessing officer weighs - walk the user through them rather than guessing: (1) frequency and volume of trades, (2) holding period (short flips lean business), (3) time and attention devoted to trading, (4) use of leverage or sophisticated strategies, (5) the taxpayer's professional knowledge of the market, (6) financing method, and (7) whether crypto is held as inventory vs. long-term investment. No single factor decides it; the overall pattern does. When the answer is genuinely borderline, recommend a pre-ruling (hachlatat misui) or CPA review. Business classification also pulls in National Insurance + health tax (see references) and, for miners and dealers, **VAT at 18% plus osek registration** - which is outside this skill's scope and needs separate professional consultation.
- **Companies**: Standard corporate tax rate (**23%**, since 2018) applies to capital gains.
- **Surtax (mas yesafim)**: the 2025 budget reform restructured the surtax from a flat 3% on labor income into a two-component charge that explicitly reaches passive and capital income, including crypto capital gains. For 2026 the structure is **3% base on all taxable income above NIS 721,560 PLUS an additional 2% on capital-source income (capital gains, dividends, interest, rentals) above the same threshold** - effective **5% on crypto gains in the band above the threshold**. The threshold (NIS 721,560 / monthly NIS 60,130) is **frozen through tax year 2027** by the December 2024 indexation-pause amendment, so do not apply CPI uplifts. The pre-2025 framing of "3% surtax on labor income only" is obsolete; **crypto capital gains are now within the surtax base**, materially raising the effective rate on large realizations.

**Cost basis method:**
- Israel mandates **FIFO** (First In, First Out) for calculating cost basis unless the taxpayer can demonstrate a different method was consistently applied.

**Currency conversion:**
- All transactions must be converted to **New Israeli Shekel (NIS)** at the exchange rate on the transaction date.
- For crypto-to-crypto trades, the NIS value of both sides must be determined at the time of trade.

### Step 2: Collect Transaction Data

Gather the user's complete transaction history. The following data points are needed for each transaction:

1. **Date and time** of the transaction
2. **Transaction type**: buy, sell, trade (crypto-to-crypto), receive (airdrop, staking reward, mining), send, gift
3. **Asset**: Which cryptocurrency (BTC, ETH, etc.)
4. **Amount**: Quantity of the asset
5. **Price in NIS** (or USD/other fiat for conversion): The value at the time of transaction
6. **Exchange/platform**: Where the transaction occurred (Bits of Gold, Binance, Coinbase, etc.)
7. **Fees**: Transaction fees, gas fees, exchange fees (deductible from gains)
8. **Wallet addresses** (optional, for verification)

Common data sources:
- **Israeli exchanges**: Bits of Gold (bits.co.il), Bit2C (bit2c.co.il) provide transaction history exports
- **International exchanges**: Binance, Coinbase, Kraken, KuCoin provide CSV exports
- **DeFi protocols**: On-chain transaction history from Etherscan, BscScan, etc.
- **Hardware wallets**: Ledger Live, Trezor Suite export functions

### Step 3: Calculate Capital Gains Using FIFO

Use the crypto gains calculator script to process transactions:

```bash
python scripts/crypto-gains-calculator.py --input transactions.csv --year 2024 --currency ILS
```

The calculator applies FIFO methodology:

1. **Queue all purchases** by date (oldest first)
2. **For each sale**, match against the oldest available purchase lots
3. **Calculate gain/loss** for each matched lot: (sale price - purchase price - fees) per unit
4. **Sum all gains and losses** for the tax year
5. **Convert to NIS** using Bank of Israel exchange rates for the transaction dates

**Key FIFO rules for Israel:**
- When selling a portion of holdings, the cost basis comes from the earliest (oldest) acquisition
- If a lot is partially consumed, the remainder stays in the queue
- Crypto-to-crypto trades are treated as a disposal (sale) of one asset and acquisition (purchase) of the other
- The NIS value at the time of the trade determines both the sale price and new acquisition cost

### Step 4: Classify DeFi and Special Income

Different crypto activities have different tax treatments in Israel:

| Activity | Classification | Tax Rate | Reporting |
|----------|---------------|----------|-----------|
| Buy and hold, then sell | Capital gain | 25% | Form 1325 |
| Crypto-to-crypto swap | Capital gain (disposal + acquisition) | 25% | Form 1325 |
| Staking rewards | Ordinary income or capital gain (debated) | 25-50% | Form 1301 or 1325 |
| Liquidity mining/yield farming | Ordinary income | Marginal rates | Form 1301 |
| Airdrops (free tokens) | Income at receipt, capital gain on sale | Marginal + 25% | Form 1301 + 1325 |
| Mining | Business income or capital gain | Depends on scale | Form 1301 or 1325 |
| NFT sales (creator) | Business income | Marginal rates | Form 1301 |
| NFT sales (collector) | Capital gain | 25% | Form 1325 |
| Hard fork tokens | Zero cost basis, capital gain on sale | 25% | Form 1325 |
| Lending interest (CeFi/DeFi) | Interest income | 25% (passive) | Form 1301 |

**Important classification notes:**
- **Staking**: The Tax Authority has not issued definitive guidance on staking. Conservative approach treats rewards as income at receipt (valued at market price), then capital gain/loss on subsequent sale. Some tax advisors argue it is similar to dividends (25% rate).
- **Airdrops**: Received tokens are considered income at the market value on the date of receipt. Cost basis for future sale is that market value.
- **Hard forks**: New tokens from hard forks (e.g., BCH from BTC) have a zero cost basis. The entire sale proceeds are treated as capital gain.
- **DeFi yields**: Liquidity provision rewards, farming rewards, and similar DeFi income are generally classified as ordinary income, taxed at marginal rates.

Consult `references/crypto-tax-regulations.md` for detailed regulatory analysis.
Consult `references/crypto-tax-scenarios.md` for worked examples of each scenario.

### Step 5: Generate Form 1322 / 1325 Data

Crypto capital gains for individuals are reported on Appendix ג to the annual tax return. Two related forms are involved:

- **Form 1322** (Nispach Gimel) - the primary capital gains schedule attached to the annual return; this is where totals land.
- **Form 1325** (Nispach Gimel(1)) - an auxiliary detail form for negotiable-securities sales where tax was not withheld at source. It feeds line totals into Form 1322. Most crypto sales (no Israeli source-withholding) belong here.

Generate the required data:

```bash
python scripts/crypto-gains-calculator.py --input transactions.csv --year 2025 --form-1325
```

The form requires for each disposal:
1. **Asset description**: "Bitcoin (BTC)" or similar
2. **Date of acquisition**: Purchase date (FIFO-determined)
3. **Date of disposal**: Sale date
4. **Acquisition cost** (in NIS): Original purchase price + fees
5. **Disposal proceeds** (in NIS): Sale price - fees
6. **Capital gain or loss** (in NIS): Proceeds minus cost
7. **Holding period**: Records whether the lot was held under or over 12 months. For crypto, individuals pay 25% in both cases - there is no US-style long-term-rate preference. The duration matters mainly for the inflation-component (sechum hatzmada) calculation under Section 91(b)(3), which the calculator does NOT yet apply (see Gotchas).

**Loss offsetting rules:**
- Capital losses from crypto can offset capital gains from crypto in the same tax year
- Capital losses from crypto can offset capital gains from other assets (stocks, real estate) in the same year
- Capital losses can be carried forward to offset capital gains in future years under Section 92 of the Income Tax Ordinance (but cannot offset ordinary income)
- Losses from one spouse can offset gains of the other spouse if filing jointly

### Step 6: Calculate Advance Tax Payments (Mikdamot)

If the user has crypto gains during the year, they generally need to file and pay advance tax (mikdama) ahead of the annual return:

- **Form**: **Form 1399י** (1399-yod) for individuals - the dedicated capital gains advance-payment form. Virtual-currency disposals are filed with transaction codes **77** (sale) and **71** (virtual currency). Form 1399ח is the equivalent for companies.
- **Reporting deadline**: within **30 days** of the capital gain event for one-off disposals; the form is filed to the assessing officer (pakid shuma).
- **Payment**: 25% of the gain for individuals (or 30% for significant-shareholder cases).
- **Annual reconciliation**: advance payments are credited against the final annual tax liability when filing the annual return.
- **Penalties for non-payment**: interest (ribit) and linkage differences (hafreshei hatzmada) accrue from the 30-day deadline.

The legacy "Form 7002" reference in older guides is outdated for crypto reporting - use Form 1399י.

```bash
python scripts/crypto-gains-calculator.py --input transactions.csv --year 2025 --advance-payments
```

### Step 7: Provide Filing Guidance

Guide the user through the tax filing process:

1. **Compile capital gains schedule**: list all disposals on Form 1325 (auxiliary), with totals carried into Form 1322 (Appendix ג of the annual return).
2. **File annual tax return**: submit Form 1301 (the individual annual return, doch shnati) with Forms 1322 and 1325 attached as appendices. A crypto disposal generally creates a filing obligation, but check the TY2025 exemption first: a draft amendment to the exemption-from-filing regulations (טיוטת תקנות מס הכנסה (פטור מהגשת דין וחשבון), published for comment Jan 2025) exempts a salaried taxpayer from the annual return on crypto gains when the crypto was traded through a **supervised Israeli platform that withheld the tax at source** AND total income stays under the Section 131 ceilings (roughly NIS 723,000 gross from work/business, or NIS 721,560 total taxable income from all sources). Exceeding either ceiling, incomplete withholding, or trading through an unsupervised/foreign venue restores the full Section 131 filing duty. Paying an advance (mikdama) does NOT by itself remove the annual-return obligation. Verify the final regulation text before relying on the exemption, since it was still in draft as of mid-2026.
3. **Filing deadline**: for tax year 2025 (filed in 2026), the deadlines published by the Israeli Tax Authority are **30 June 2026 for online filing via the gov.il portal** and **29 May 2026 for paper filing**. Returns filed via a representing accountant typically receive extensions through July or September. Always verify the current year's deadlines on gov.il/he/service before filing.
4. **Self-assessment of surtax**: individuals whose total taxable income (including crypto gains) exceeds NIS 721,560 must also self-assess surtax (mas yesafim) - 3% base on income above the threshold plus an additional 2% on capital-source income above the same threshold. The threshold is frozen through 2027.
5. **Voluntary Disclosure window**: prior-year unreported crypto gains can be regularised under the **2025-2026 Voluntary Disclosure Procedure (Nohal Gilui Mirtzon)**, which expressly covers digital assets and grants criminal immunity. **Deadline: 31 August 2026**. Two tracks: a Green Track for smaller cases (annual income up to NIS 500k and cumulative crypto assets up to NIS 1.5M as of 31 Dec 2024) and a Regular Track for larger cases. Anonymity is no longer available; all applications are filed with identifying details.
6. **Paying tax when a bank refuses the funds (Form 909)**: a recurring Israeli pain point is that a commercial bank refuses (in writing) to accept crypto-derived deposits, leaving the taxpayer unable to fund the tax payment from a normal account. For this case the ITA, with the Bank of Israel and the Anti-Money-Laundering Authority, runs a special procedure (Hora'at Sha'a, ITA Instruction 06/2024) under which an **individual (not a company)** files **Form 909** ("דיווח על פעילות במטבעות וירטואליים ובקשה לתשלום המס המגיע במימוש המטבעות") to the assessing officer and pays the tax in NIS directly into the ITA's account at the Bank of Israel. Required attachments include a written bank-refusal letter, a taxable-income working paper, a full money-trail of the coins, and proof of the legal source of the original funds. Filed online via the ITA CRM together with the annual return, or physically at the assessing officer. The request undergoes a money-laundering-risk review before payment is accepted.
7. **Record keeping**: maintain all transaction records, exchange exports, and wallet data for at least 7 years.

**When to recommend professional help:**
- Transaction volume exceeds 100 trades per year
- DeFi activities involve complex protocols (multi-chain, bridging, wrapping)
- User is unsure whether activity constitutes a business vs. investment
- Total gains exceed 500,000 NIS
- User received tokens from an ICO, IEO, or similar offering
- Cross-border transactions involving Israeli and foreign tax obligations

## Examples

### Example 1: Simple Bitcoin Buy and Sell

User says: "I bought 0.5 BTC in January 2025 for 80,000 NIS and sold it in August 2025 for 120,000 NIS. What's my tax?"

Actions:
1. Identify the transaction: single buy, single sell.
2. Calculate capital gain: 120,000 - 80,000 = 40,000 NIS.
3. Apply 25% capital gains tax: 40,000 x 0.25 = 10,000 NIS.
4. Check surtax threshold: a 40,000 NIS gain is well below NIS 721,560, so no surtax (assuming no other income above the threshold).
5. Note the holding period: 7 months. The 25% rate applies regardless, but the inflation-component split (sechum hatzmada) is negligible for such a short hold.

Result: capital gain 40,000 NIS, tax liability 10,000 NIS. The user should have filed Form 1399י (transaction codes 77/71) within 30 days of the August sale and paid the 10,000 NIS as a mikdama. If the deadline is missed, the user should still file and pay as soon as possible to minimise interest and linkage penalties. The gain is then reported on Forms 1325/1322 as part of the **2025 annual tax return**, due **30 June 2026 (online) or 29 May 2026 (paper)**.

### Example 2: Crypto-to-Crypto Trade with FIFO

User says: "I bought 2 ETH at 5,000 NIS each in March 2024, then 3 ETH at 7,000 NIS each in June 2024. In October I traded 3 ETH for 0.5 BTC when ETH was worth 9,000 NIS each. What's my tax situation?"

Actions:
1. Build the FIFO queue: Lot 1: 2 ETH @ 5,000 NIS (March), Lot 2: 3 ETH @ 7,000 NIS (June)
2. Process the disposal: 3 ETH traded in October (crypto-to-crypto = taxable disposal)
3. Apply FIFO: First consume Lot 1 (2 ETH @ 5,000), then 1 ETH from Lot 2 (@ 7,000)
4. Calculate gains:
   - Lot 1: 2 ETH x (9,000 - 5,000) = 8,000 NIS gain
   - Lot 2 partial: 1 ETH x (9,000 - 7,000) = 2,000 NIS gain
   - Total gain: 10,000 NIS
5. Tax at 25%: 10,000 x 0.25 = 2,500 NIS
6. Note remaining position: 2 ETH from Lot 2 (@ 7,000 NIS cost) + 0.5 BTC (@ 27,000 NIS total cost, which is 3 x 9,000 NIS)

Result: The crypto-to-crypto trade triggers a taxable event of 10,000 NIS capital gain (2,500 NIS tax). The new BTC position has a cost basis of 27,000 NIS (the NIS value of 3 ETH at the time of trade). The remaining 2 ETH retain their original cost basis of 7,000 NIS each. The agent generates a Form 1325 entry for this disposal.

### Example 3: DeFi Staking Rewards Classification

User says: "I staked 10 ETH on a DeFi protocol and earned 0.5 ETH in staking rewards over 2024. The ETH was worth 8,000 NIS when I received the rewards. I haven't sold anything yet. Do I owe taxes?"

Actions:
1. Classify the staking rewards: under conservative interpretation, treated as income at receipt
2. Calculate income: 0.5 ETH x 8,000 NIS = 4,000 NIS taxable income
3. Determine the applicable rate: this could be 25% (if treated as passive income/interest) or marginal rate (if treated as ordinary income)
4. Consult `references/crypto-tax-regulations.md` for the latest guidance on staking classification
5. Note: the 10 staked ETH have not been disposed of, so no capital gain event on those
6. Establish cost basis for the 0.5 reward ETH: 8,000 NIS per ETH (4,000 NIS total)

Result: Under the conservative approach recommended by most Israeli tax advisors, the 0.5 ETH staking reward is taxable income of 4,000 NIS in the year received, regardless of whether it was sold. The tax rate depends on classification: 25% if treated as passive income (1,000 NIS tax), or marginal rates if treated as ordinary income (potentially up to 50%). The agent recommends consulting a tax advisor for classification, as the Tax Authority has not issued definitive guidance. The 0.5 ETH has a cost basis of 4,000 NIS for future capital gains calculation.

## Bundled Resources

### Scripts
- `scripts/crypto-gains-calculator.py` -- FIFO capital gains calculator with NIS conversion, supporting multiple exchanges and generating Form 1325 data. Run: `python scripts/crypto-gains-calculator.py --help`

### References
- `references/crypto-tax-regulations.md` -- Israeli Tax Authority circulars, relevant Income Tax Ordinance sections, classification rules for different crypto activities, and reporting deadlines. Consult when determining the correct tax treatment for specific crypto activities.
- `references/crypto-tax-scenarios.md` -- Worked examples covering simple trades, crypto-to-crypto swaps, DeFi staking, NFT sales, mining income, airdrops, and hard forks. Consult when calculating tax for specific transaction types.

## Recommended MCP Servers

| MCP | What It Adds |
|-----|-------------|
| [BOI Exchange Rates](https://agentskills.co.il/he/mcp/boi-exchange) | Provides the official Bank of Israel daily representative rate (sha'ar yatzig) for USD, EUR, and 30+ other currencies - the rate this skill requires for converting non-NIS legs of every transaction. Live access removes the need to scrape boi.org.il manually and ensures the FIFO calculator sees authoritative same-day NIS values. |

## Gotchas
- Israel taxes crypto as property (capital gains), not as currency. Agents may apply currency-exchange rules or VAT to crypto transactions, which is incorrect under Israeli tax law.
- The Israeli capital gains tax rate on crypto is 25% for individuals (mas revach hon), not the US 15%/20% rates. Agents trained on US tax data will use the wrong rate.
- Israeli crypto tax reporting uses FIFO (First In, First Out) as the default cost basis method. Agents may default to average cost or LIFO, which are not standard practice in Israel.
- Crypto-to-crypto swaps are taxable events in Israel. Agents may treat them as non-taxable exchanges (the old US rule), but this has never been the case in Israel.
- **Stablecoins (USDT, USDC, DAI) are still "asset" under Section 88 of the Income Tax Ordinance**, not foreign currency. Every USDT-to-USDC swap, every conversion-leg of a DeFi trade, and every USDT off-ramp to fiat is a taxable disposal valued in NIS. Users frequently treat stablecoins as "cash equivalents" and skip them, missing the majority of taxable events for active DeFi participants.
- **Inflation indexation (sechum hatzmada) is not yet applied by the calculator.** Section 91(b)(3) splits any capital gain into a "real gain" (taxed at 25%) and an "inflation-component gain" (taxed at 0% for individuals on assets acquired after 1.1.1994). The current calculator multiplies total gain by 25% with no CPI step, so it overstates tax on lots held longer than ~12 months in inflationary years. For long-held lots, agents should flag this limitation to the user and recommend a manual indexation pass or a CPA review before filing.
- **Israel has no wash-sale rule.** Unlike the US 30-day rule, Israeli tax law allows a taxpayer to realise a December capital loss and re-buy the same crypto in January with the loss fully recognised. Agents trained on US tools may incorrectly disallow such losses.
- **Gifts and inheritance use carryover basis** under Section 97(a)(5) - the recipient inherits the donor's original cost basis and acquisition date. Treating an inherited 1 BTC as zero-basis or as fair-market-value at inheritance produces wildly wrong numbers. Document the donor's records.
- **Crypto lost to exchange insolvency (FTX, Celsius pattern), theft, or lost private keys** is recognised as a capital loss only when the loss is final and documented (e.g., bankruptcy court order, police report). Agents should not write off frozen-but-not-bankrupt balances and should not treat loss-of-keys as deductible without supporting evidence.
- **Leaving Israel triggers an exit tax (deemed sale, Section 100A).** A resident who ceases Israeli residency (yerida, or an oleh who later leaves) is treated as having sold all assets, crypto included, one day before residency ends. The tax can be paid at exit or deferred to the actual future sale, with the gain apportioned over the Israeli-residency period. This is a distinct event from a normal disposal and the FIFO calculator here does NOT model it. For any relocation scenario, flag Section 100A and route the user to a CPA (and the relocation/aliyah skills) rather than producing a plain disposal figure.

## Troubleshooting

### Error: "Cannot determine NIS exchange rate for date"
Cause: The calculator could not find the NIS/USD or NIS/crypto exchange rate for the specified transaction date. This often happens with weekends or Israeli holidays when the Bank of Israel does not publish rates.
Solution: For dates when the Bank of Israel does not publish rates (Shabbat, holidays), use the rate from the most recent business day prior to the transaction. The calculator attempts this automatically, but if it fails, specify the rate manually with the `--manual-rate` flag. For crypto-to-NIS conversion, the calculator uses the exchange's reported NIS price when available, or the USD price multiplied by the USD/NIS rate from Bank of Israel.

### Error: "FIFO queue exhausted - more sold than purchased"
Cause: The transaction history shows more crypto being sold than was purchased. This usually indicates missing purchase transactions (e.g., deposits from another exchange, transfers from a personal wallet, or an incomplete transaction history export).
Solution: Review the transaction history for completeness. Check if crypto was transferred in from another exchange or wallet (these transfers are not taxable events but must be recorded to maintain accurate cost basis). Add the missing purchase records. If the original purchase records are unavailable, Israeli tax law allows using the earliest available market price as a fallback cost basis, but this should be documented and disclosed.

### Error: "Transaction type not recognized for tax classification"
Cause: The calculator encountered a transaction type it cannot automatically classify for tax purposes (e.g., a complex DeFi interaction, bridge transaction, or wrapped token conversion).
Solution: Review the transaction manually. Common DeFi operations and their classifications: wrapping (ETH to WETH) is generally not a taxable event; bridging between chains may be a taxable event if it involves a swap; providing liquidity is not taxable until withdrawal (but LP token movements may trigger events). For complex DeFi operations, consult `references/crypto-tax-scenarios.md` and consider professional tax advice.

### Error: "Form 1325 generation failed - missing required fields"
Cause: Some transactions are missing data required for Form 1325 (typically the acquisition date or the NIS value at acquisition).
Solution: Review the error output which lists the specific transactions with missing data. For each, provide the acquisition date (FIFO-determined) and the NIS value at that date. If the acquisition was a gift or airdrop, the cost basis rules differ: gifts use the donor's cost basis (Section 97(a)(5) carryover), and airdrops use the market value at receipt. Update the transaction CSV with the corrected data and re-run.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Israeli Tax Authority - annual return service (Form 1301) | https://www.gov.il/he/service/reporting-and-payment-2025-annual-tax-report-for-individuals | Current-year filing deadlines, links to Forms 1322 and 1325, online filing portal |
| Bank of Israel - representative rates (sha'ar yatzig) | https://www.boi.org.il/roles/markets/exchangerates/ | Daily NIS reference rates for currency conversion of foreign-fiat legs of crypto trades |
| ITA Circular 05/2018 (crypto classification, FIFO, virtual currency definition) | https://www.gov.il/BlobFolder/policy/income-tax-professional-inst-5-2018/he/Policy_ProfessionalInstIncomeTax_hor_acc%2015.2.18.pdf | Foundational tax-treatment guidance for virtual currencies |
| Voluntary Disclosure Procedure 2025-2026 (crypto track) | https://www.gov.il/he/pages/pa010925-1 | Eligibility, Green vs Regular Track, deadline 31 Aug 2026, required documentation |
| Form 909 - paying crypto tax when a bank refuses the funds | https://www.gov.il/he/service/reporting-cryptocurrency-activity | Bank-refusal payment procedure, required attachments, individuals only |
| Bituach Leumi self-employed rates (2026) | https://www.btl.gov.il/Insurance/National%20Insurance/type_list/Self_Employed/Pages/rates.aspx | Current National Insurance + health-tax rates for business-classified crypto traders |
| OECD Crypto-Asset Reporting Framework (CARF) - committed jurisdictions | https://www.oecd.org/content/dam/oecd/en/networks/global-forum-tax-transparency/commitments-carf.pdf | Israel among committed jurisdictions; collection from 2026, first exchange expected 2027-2028 (verify the year against the latest OECD monitoring update) |
