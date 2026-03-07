# Crypto Tax Scenarios: Worked Examples for Israeli Taxpayers

## Scenario 1: Simple Buy and Sell (Bitcoin)

**Facts:**
- January 15, 2024: Bought 1 BTC for 150,000 NIS on Bits of Gold (fee: 750 NIS)
- September 20, 2024: Sold 1 BTC for 230,000 NIS on Bits of Gold (fee: 1,150 NIS)

**Calculation:**
```
Acquisition cost:    150,000 + 750 = 150,750 NIS
Disposal proceeds:   230,000 - 1,150 = 228,850 NIS
Capital gain:        228,850 - 150,750 = 78,100 NIS
Tax (25%):           78,100 x 0.25 = 19,525 NIS
```

**Reporting:**
- Form 1325 entry with acquisition date Jan 15 and disposal date Sep 20
- Advance payment (mikdama) due by Oct 20, 2024 (30 days after sale)
- Holding period: 8 months (short-term, but still 25% for crypto)

## Scenario 2: Multiple Purchases, Partial Sale (FIFO)

**Facts:**
- March 1, 2024: Bought 2 ETH at 8,000 NIS each = 16,000 NIS (fee: 160 NIS)
- May 15, 2024: Bought 3 ETH at 10,000 NIS each = 30,000 NIS (fee: 300 NIS)
- August 10, 2024: Bought 1 ETH at 12,000 NIS (fee: 120 NIS)
- November 1, 2024: Sold 4 ETH at 15,000 NIS each = 60,000 NIS (fee: 600 NIS)

**FIFO application:**

Lot 1: 2 ETH @ 8,080 NIS each (including proportional fee)
Lot 2: 3 ETH @ 10,100 NIS each (including proportional fee)
Lot 3: 1 ETH @ 12,120 NIS (including fee)

Selling 4 ETH using FIFO:
- Use all of Lot 1: 2 ETH
- Use 2 ETH from Lot 2

```
Sale proceeds per ETH: (60,000 - 600) / 4 = 14,850 NIS

Lot 1 (2 ETH):
  Gain per ETH: 14,850 - 8,080 = 6,770 NIS
  Total gain: 6,770 x 2 = 13,540 NIS

Lot 2 partial (2 of 3 ETH):
  Gain per ETH: 14,850 - 10,100 = 4,750 NIS
  Total gain: 4,750 x 2 = 9,500 NIS

Total capital gain: 13,540 + 9,500 = 23,040 NIS
Tax (25%): 23,040 x 0.25 = 5,760 NIS
```

**Remaining positions after sale:**
- 1 ETH from Lot 2 (cost: 10,100 NIS)
- 1 ETH from Lot 3 (cost: 12,120 NIS)

## Scenario 3: Crypto-to-Crypto Trade

**Facts:**
- April 1, 2024: Bought 5 SOL at 400 NIS each = 2,000 NIS
- July 15, 2024: Traded 5 SOL for 0.02 BTC when SOL was 600 NIS each and BTC was 150,000 NIS

**This is TWO events:**

**Event 1: Disposal of SOL**
```
Acquisition cost:    2,000 NIS (5 SOL @ 400)
Disposal proceeds:   5 x 600 = 3,000 NIS (NIS value of SOL at trade time)
Capital gain:        3,000 - 2,000 = 1,000 NIS
Tax (25%):           1,000 x 0.25 = 250 NIS
```

**Event 2: Acquisition of BTC**
```
Cost basis of 0.02 BTC: 3,000 NIS (the NIS value paid, i.e., the SOL disposal value)
```

**Form 1325:** Report the SOL disposal. The BTC acquisition is not reported until the BTC is sold.

## Scenario 4: DeFi Staking Rewards

**Facts:**
- January 1, 2024: Staked 100 MATIC (cost basis: 300 NIS total)
- Throughout 2024: Received 5 MATIC in staking rewards across multiple distributions
- Average MATIC price at time of each reward receipt: approximately 4 NIS per MATIC
- December 31, 2024: Still holding all MATIC (original 100 + 5 rewards)

**Tax treatment (conservative approach):**

Income recognition at receipt of each reward:
```
Staking rewards received:   5 MATIC
Value at receipt:           5 x 4 = 20 NIS income
Tax rate:                   25% (passive income) = 5 NIS
                            OR marginal rate (up to 50%) if classified as ordinary income
```

**Cost basis for future sales:**
- Original 100 MATIC: 300 NIS (unchanged)
- 5 reward MATIC: 20 NIS (market value at receipt)
- Total holdings: 105 MATIC, total cost basis: 320 NIS

**Note:** If the user later sells the 5 reward MATIC for 30 NIS:
```
Capital gain: 30 - 20 = 10 NIS
Tax (25%): 10 x 0.25 = 2.5 NIS
```
Total tax on these 5 MATIC: 5 NIS (income) + 2.5 NIS (capital gain) = 7.5 NIS

## Scenario 5: NFT Sale (Collector)

**Facts:**
- February 2024: Bought an NFT for 0.5 ETH when ETH = 9,000 NIS (cost: 4,500 NIS, plus 0.01 ETH gas = 90 NIS)
- October 2024: Sold the NFT for 1.5 ETH when ETH = 12,000 NIS

**Calculation:**
```
Acquisition cost:    4,500 + 90 = 4,590 NIS
Disposal proceeds:   1.5 x 12,000 = 18,000 NIS
Capital gain:        18,000 - 4,590 = 13,410 NIS
Tax (25%):           13,410 x 0.25 = 3,352.50 NIS
```

**Note:** The 1.5 ETH received has a cost basis of 18,000 NIS for future disposals.

If the user were a professional NFT artist selling their own creations, this would be business income at marginal rates instead of capital gains.

## Scenario 6: Mining Income

**Facts (hobbyist miner):**
- Mined 0.001 BTC per month throughout 2024 (0.012 BTC total)
- Average BTC price at time of mining: 160,000 NIS per BTC
- Electricity costs attributable to mining: 2,400 NIS/year
- Equipment cost: 15,000 NIS (3-year useful life = 5,000 NIS depreciation/year)

**If classified as business income:**
```
Mining income:       0.012 x 160,000 = 1,920 NIS
Less: electricity:   -2,400 NIS
Less: depreciation:  -5,000 NIS
Net business loss:   -5,480 NIS
```
The loss can offset other business income (but not capital gains, unless special circumstances).

**If classified as asset creation (capital treatment):**
```
Cost basis of 0.012 BTC: 1,920 NIS (market value at time of mining)
Income at mining:        1,920 NIS (taxable as income)
Tax (25% passive):       480 NIS
```
Mining costs (electricity, depreciation) may be deductible against the mining income.

**Note:** At commercial scale (dedicated mining operation), the Tax Authority will almost certainly classify this as business income.

## Scenario 7: Airdrop Tokens

**Facts:**
- June 2024: Received 1,000 AIRDROP tokens via airdrop (claimed from a DeFi protocol)
- Market value at receipt: 2 NIS per token = 2,000 NIS total
- October 2024: Sold 500 tokens at 5 NIS each = 2,500 NIS
- Still holding 500 tokens at year-end

**Income at receipt:**
```
Airdrop income:      1,000 x 2 = 2,000 NIS
Tax rate:            Marginal (ordinary income), e.g., 35% = 700 NIS
```

**Capital gain on partial sale:**
```
Cost basis (FIFO, 500 tokens): 500 x 2 = 1,000 NIS
Sale proceeds:                  500 x 5 = 2,500 NIS
Capital gain:                   2,500 - 1,000 = 1,500 NIS
Tax (25%):                      1,500 x 0.25 = 375 NIS
```

**Total 2024 tax on this airdrop:** 700 + 375 = 1,075 NIS

**Remaining position:** 500 tokens with cost basis of 1,000 NIS (2 NIS each)

## Scenario 8: Hard Fork

**Facts:**
- Pre-fork: Held 2 BTC
- August 2017: Bitcoin Cash (BCH) hard fork, received 2 BCH
- January 2024: Sold 2 BCH at 1,000 NIS each = 2,000 NIS

**Tax treatment:**
```
Cost basis of BCH from hard fork: 0 NIS (zero cost basis)
Sale proceeds:                     2 x 1,000 = 2,000 NIS
Capital gain:                      2,000 - 0 = 2,000 NIS
Tax (25%):                         2,000 x 0.25 = 500 NIS
```

**Note:** The original BTC cost basis is unchanged. The new fork tokens receive a zero cost basis.

## Scenario 9: Liquidity Provision (DeFi)

**Facts:**
- March 2024: Deposited 1 ETH (10,000 NIS) + 10,000 USDC (37,000 NIS) into a liquidity pool
- Received LP tokens representing the position
- Throughout 2024: Earned 500 USDC in trading fees (approximately 1,850 NIS)
- December 2024: Withdrew from pool: received 0.8 ETH (12,000 NIS) + 12,000 USDC (44,400 NIS)

**Fee income:**
```
Trading fees earned:  1,850 NIS
Tax (as income):      Marginal rate, e.g., 35% = 647.50 NIS
```

**Position closure (withdrawal):**
```
Total deposited:     10,000 + 37,000 = 47,000 NIS
Total withdrawn:     12,000 + 44,400 = 56,400 NIS
Gain on position:    56,400 - 47,000 = 9,400 NIS

This 9,400 NIS may be split between:
- ETH price appreciation (capital gain, 25%)
- Pool rebalancing (may be treated differently)

Conservative approach: treat entire 9,400 NIS as capital gain
Tax (25%): 9,400 x 0.25 = 2,350 NIS
```

**Total tax:** 647.50 + 2,350 = 2,997.50 NIS

**Note:** Impermanent loss is embedded in the withdrawal amounts. It reduces the gain but is not separately deductible.

## Scenario 10: Loss Offsetting

**Facts for 2024:**
- Sold Bitcoin: 30,000 NIS capital gain
- Sold Ethereum: 15,000 NIS capital loss
- Sold stocks on TASE: 10,000 NIS capital gain

**Loss offsetting:**
```
Crypto capital gains:    30,000 NIS
Crypto capital losses:   -15,000 NIS
Net crypto gain:         15,000 NIS

Stock capital gains:     10,000 NIS

Total net capital gain:  15,000 + 10,000 = 25,000 NIS
Tax (25%):               25,000 x 0.25 = 6,250 NIS
```

**The crypto loss offsets the crypto gain first, then can offset stock gains in the same year.**

If the situation were reversed (net crypto loss after offsetting crypto gains), the remaining crypto loss could still offset the stock gains:
```
Example: 30,000 loss - 15,000 gain = 15,000 net crypto loss
This 15,000 loss can offset the 10,000 stock gain
Remaining loss: 5,000 NIS (cannot be carried forward for individuals)
```

## Scenario 11: USD-Denominated Trades Converted to NIS

**Facts:**
- January 10, 2024: Bought 1 BTC for $40,000 on Binance (USD/NIS rate: 3.65)
- August 5, 2024: Sold 1 BTC for $60,000 on Binance (USD/NIS rate: 3.70)

**Calculation:**
```
Acquisition cost in NIS:    40,000 x 3.65 = 146,000 NIS
Disposal proceeds in NIS:   60,000 x 3.70 = 222,000 NIS
Capital gain:               222,000 - 146,000 = 76,000 NIS
Tax (25%):                  76,000 x 0.25 = 19,000 NIS
```

**Note:** The NIS gain includes both the crypto appreciation AND the USD/NIS exchange rate change. Both are taxable as part of the capital gain. Use Bank of Israel representative rate (shaar yatzig) for the conversion dates.
