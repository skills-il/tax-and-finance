---
name: israeli-crypto-tax-reporter
description: >-
  Calculate cryptocurrency capital gains tax per Israeli Tax Authority (Reshut HaMisim)
  regulations and generate Form 1325 reporting data. Use when a user needs to compute
  crypto tax obligations using FIFO cost basis, classify DeFi income (staking, liquidity
  mining, airdrops) for Israeli tax purposes, prepare annual tax filing data, or understand
  reporting thresholds and advance payment (mikdamot) requirements. Covers Section
  2(1) of the Income Tax Ordinance, Circular 2018/05, and the 25% capital gains rate
  for individuals. Do NOT use for non-Israeli tax jurisdictions, general income tax
  calculations, or VAT (maam) on crypto business activities, which require separate
  professional consultation.
license: MIT
allowed-tools: Bash(python:*) Read Edit Write WebFetch
compatibility: Requires Python 3.8+ for calculator script
metadata:
  author: skills-il
  version: 1.0.1
  category: tax-and-finance
  tags:
    he:
    - מס-קריפטו
    - מטבעות-דיגיטליים
    - רווחי-הון
    - דיווח-מס
    - בלוקצ'יין
    en:
    - crypto-tax
    - cryptocurrency
    - capital-gains
    - tax-reporting
    - blockchain
  display_name:
    he: דיווח מס קריפטו ישראלי
    en: Israeli Crypto Tax Reporter
  display_description:
    he: >-
      חישוב מס רווחי הון על מטבעות דיגיטליים, הפקת נתוני טופס 1325, וסיווג הכנסות
      DeFi לפי רשות המסים הישראלית
    en: >-
      Calculate cryptocurrency capital gains tax per Israeli Tax Authority (Reshut
      HaMisim) regulations and generate Form 1325 reporting data. Use when a user
      needs to compute crypto tax obligations using FIFO cost basis, classify DeFi
      income (staking, liquidity mining, airdrops) for Israeli tax purposes, prepare
      annual tax filing data, or understand reporting thresholds and advance payment
      (mikdamot) requirements. Covers Section 2(1) of the Income Tax Ordinance, Circular
      2018/05, and the 25% capital gains rate for individuals. Do NOT use for non-Israeli
      tax jurisdictions, general income tax calculations, or VAT (maam) on crypto
      business activities, which require separate professional consultation.
  supported_agents:
  - claude-code
  - cursor
  - github-copilot
  - windsurf
  - opencode
  - codex
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
- **Business/traders**: If crypto activity constitutes a business (esek), gains are taxed as ordinary income at marginal rates (up to 50%). The classification depends on frequency, volume, and whether the taxpayer holds crypto as inventory vs. investment.
- **Companies**: Standard corporate tax rate (23%) applies to capital gains.
- **Surtax (mas yesafim)**: For individuals with annual income exceeding 733,000 NIS (2026 threshold, CPI-adjusted), an additional 3% surtax applies to the excess.

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

### Step 5: Generate Form 1325 Data

Form 1325 (Tofes 1325) is the Israeli capital gains reporting form, filed as part of the annual tax return. Generate the required data:

```bash
python scripts/crypto-gains-calculator.py --input transactions.csv --year 2024 --form-1325
```

The form requires for each disposal:
1. **Asset description**: "Bitcoin (BTC)" or similar
2. **Date of acquisition**: Purchase date (FIFO-determined)
3. **Date of disposal**: Sale date
4. **Acquisition cost** (in NIS): Original purchase price + fees
5. **Disposal proceeds** (in NIS): Sale price - fees
6. **Capital gain or loss** (in NIS): Proceeds minus cost
7. **Holding period**: Short-term (under 12 months) vs. long-term (12+ months). Note: for crypto, both are taxed at 25% for individuals, but the distinction matters for loss offsetting rules.

**Loss offsetting rules:**
- Capital losses from crypto can offset capital gains from crypto in the same tax year
- Capital losses from crypto can offset capital gains from other assets (stocks, real estate) in the same year
- Capital losses can be carried forward to offset capital gains in future years under Section 92 of the Income Tax Ordinance (but cannot offset ordinary income)
- Losses from one spouse can offset gains of the other spouse if filing jointly

### Step 6: Calculate Advance Tax Payments (Mikdamot)

If the user has significant crypto gains during the year, they may need to make advance tax payments (mikdamot):

- **Reporting deadline**: Within 30 days of a capital gain event that creates a tax liability exceeding a minimal threshold
- **Payment**: The advance payment is calculated at 25% of the gain (for individuals)
- **Annual reconciliation**: Advance payments are credited against the annual tax liability when filing the annual return
- **Penalties for non-payment**: Interest and linkage differences (hatzamada) apply to late advance payments

```bash
python scripts/crypto-gains-calculator.py --input transactions.csv --year 2024 --advance-payments
```

### Step 7: Provide Filing Guidance

Guide the user through the tax filing process:

1. **Compile Form 1325**: List all capital gain events with the data from Step 5
2. **File annual tax return**: Include Form 1325 as an appendix to the annual tax return (doch shnati)
3. **Filing deadline**: Generally April 30 of the following year for individuals (extensions may apply for accountant-filed returns, typically until July 31)
4. **Self-assessment**: Individuals with crypto gains exceeding 733,000 NIS must also account for surtax (mas yesafim)
5. **Record keeping**: Maintain all transaction records, exchange exports, and wallet data for at least 7 years

**When to recommend professional help:**
- Transaction volume exceeds 100 trades per year
- DeFi activities involve complex protocols (multi-chain, bridging, wrapping)
- User is unsure whether activity constitutes a business vs. investment
- Total gains exceed 500,000 NIS
- User received tokens from an ICO, IEO, or similar offering
- Cross-border transactions involving Israeli and foreign tax obligations

## Examples

### Example 1: Simple Bitcoin Buy and Sell

User says: "I bought 0.5 BTC in January 2024 for 80,000 NIS and sold it in August 2024 for 120,000 NIS. What's my tax?"

Actions:
1. Identify the transaction: single buy, single sell
2. Calculate capital gain: 120,000 - 80,000 = 40,000 NIS
3. Apply 25% capital gains tax: 40,000 x 0.25 = 10,000 NIS
4. Check surtax threshold: 40,000 NIS gain is well below the 733,000 NIS threshold, so no surtax
5. Note the holding period: 7 months (short-term, but rate is still 25% for crypto)

Result: The capital gain is 40,000 NIS. The tax liability is 10,000 NIS (25% rate). The user should have filed an advance payment (mikdama) within 30 days of the August sale. If not yet filed, the user should file and pay as soon as possible to minimize interest penalties. The gain should be reported on Form 1325 as part of the 2024 annual tax return (due April 30, 2025).

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

## Gotchas
- Israel taxes crypto as property (capital gains), not as currency. Agents may apply currency exchange rules or VAT to crypto transactions, which is incorrect under Israeli tax law.
- The Israeli capital gains tax rate on crypto is 25% for individuals (mas revach hon), not the US 15%/20% rates. Agents trained on US tax data will use the wrong rate.
- Israeli crypto tax reporting uses FIFO (First In, First Out) as the default cost basis method. Agents may default to average cost or LIFO, which are not standard practice in Israel.
- Crypto-to-crypto swaps are taxable events in Israel. Agents may treat them as non-taxable exchanges, which was the old US rule but has never been the case in Israel.

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
Solution: Review the error output which lists the specific transactions with missing data. For each, provide the acquisition date (FIFO-determined) and the NIS value at that date. If the acquisition was a gift or airdrop, the cost basis rules differ: gifts use the giver's cost basis, and airdrops use the market value at receipt. Update the transaction CSV with the corrected data and re-run.
