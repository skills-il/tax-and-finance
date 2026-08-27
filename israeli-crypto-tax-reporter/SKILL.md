---
name: israeli-crypto-tax-reporter
description: Calculate cryptocurrency capital gains tax per Israeli Tax Authority (Reshut HaMisim) regulations and generate capital-gains reporting data and Form 1399י advance-payment data (within 30 days of disposal). Use when a user needs to compute crypto tax obligations using FIFO cost basis, classify DeFi income (staking, liquidity mining, airdrops) for Israeli tax purposes, prepare annual tax filing data, understand reporting thresholds and advance payment (mikdamot) requirements, or evaluate the Voluntary Disclosure Procedure (Nohal Gilui Mirtzon) for unreported crypto, checking whether the window is currently open before relying on it. Covers Section 88 of the Income Tax Ordinance, Circular 2018/05, the 25% capital gains rate for individuals, and the 5% surtax on capital income above NIS 721,560 (threshold frozen through 2027). Do NOT use for non-Israeli tax jurisdictions, general income tax calculations, or VAT (maam) on crypto business activities, which require separate professional consultation.
license: MIT
allowed-tools: Bash(python:*) Read Edit Write WebFetch
compatibility: Requires Python 3.8+ for calculator script
---

# Israeli Crypto Tax Reporter

## Legal notice

This is a free information tool operated by an AI model. It explains the tax rules and helps you organise your own figures. All of its outputs are produced automatically by an AI model, with no involvement, review, or approval by a tax adviser or accountant. The output is not a tax opinion, not a return prepared by a licensed representative, and not professional advice, but a general calculation and explanation only: it does not examine the full extent of your income or your complete documents. An AI model may err, omit data, or present a wrong conclusion.

Any form or text this tool produces is an automatic draft for your personal preparation only, and is not a filed return. Responsibility for reporting and for paying the tax is yours, the binding computation is the Tax Authority's, and representation before the Tax Authority is reserved to those permitted by law. This tool is not a substitute for advice that takes account of the particular circumstances and needs of each person. Consult a tax adviser or accountant before filing or paying. All use of its output is the user's sole responsibility.

The Voluntary Disclosure Procedure is a process in which you hand the Tax Authority information about your own past reporting, and it concerns criminal exposure: while the procedure is open it may confer immunity from criminal proceedings, and once it has closed such an approach is an admission with no immunity. This tool does not test your eligibility for the procedure, does not examine the full extent of your years and documents, and does not decide whether you should apply. Whether to apply, on which track and at what time is a legal question, and legal advice and legal opinions are reserved by law to a licensed advocate. Consult a tax-specialist lawyer before lodging a voluntary-disclosure application or a corrected return under Section 131, even if the deadline is close.


## Instructions

### Step 1: Understand the Israeli Crypto Tax Framework

Before performing any calculations, ensure you understand the key regulatory principles:

**Core legal basis:**
- Cryptocurrency is classified as an **asset** (neches) under Section 88 of the Income Tax Ordinance (Pekudat Mas Hachnasa), not as currency.
- Gains from selling crypto are taxed as **capital gains** (revach hon) under Chapter E of the Ordinance.
- **Circular 05/2018**, "מיסוי פעילות באמצעי תשלום מבוזר", dated 17 January 2018, is the primary ITA guidance and remains in force.

**Tax rates:**
- **Individuals**: 25% capital gains tax on the real gain, under Section 91(b)(1).
- **The 30% rate almost certainly does NOT apply to ordinary tokens.** Section 91(b)(2) charges up to 30% on the sale of a **"נייר ערך בחבר-בני-אדם"**, a security in a body corporate, by a material shareholder. A fungible token is not one, and Circular 05/2018 never invokes 91(b)(2). Do not apply 30% just because the holder owns a large stake in a project; an equity-like token in an incorporated entity is a question for a CPA or a pre-ruling.
- **Business/traders**: If crypto activity constitutes a business (esek), gains are taxed as ordinary income at marginal rates (up to 47%, plus the surtax) instead of the 25% capital rate. This is the single highest-stakes determination in crypto tax. Circular 05/2018 does NOT enumerate the test: section 3.1.4 says only that classification "ייקבע בהתאם למבחני עסק כפי שנקבעו **בפסיקה**", delegating to the case law. Cite the badge-of-trade factors as case law, not as the circular, and walk the user through them rather than guessing: trade frequency and volume, holding period, time and attention devoted, use of leverage, the taxpayer's professional knowledge, financing method, and inventory-versus-investment intent. No single factor decides it. When it is genuinely borderline, recommend a pre-ruling (hachlatat misui) or CPA review. Business classification also pulls in National Insurance + health tax and a VAT consequence that is routinely got wrong. **Circular 05/2018 section 3.2.3.2.3 registers a business-level crypto trader as a "מוסד כספי" (financial institution) under Section 4 of the VAT Law, NOT as an osek charging 18% output VAT.** Section 3.2.3.2.4 carves out the **miner** separately as an osek, and 3.2.3.1 leaves a non-business investor outside VAT entirely. Three regimes, not one: do not say "18% VAT plus osek registration". Implementation needs professional advice.
- **Companies**: Standard corporate tax rate (**23%**, since 2018) applies to capital gains.
- **Surtax (mas yesafim)**: two components, not one. Section 121B(a) charges **3%** on taxable income above **NIS 721,560**, and Section 121B(a1) adds **2%** on income **from capital sources** above the same threshold, so crypto gains in that band bear an effective **5%**. The Ordinance fixes 721,560 for tax years **2024 through 2027**, so do not apply CPI uplifts. The pre-2025 framing of "3% on labor income only" is obsolete.

**Cost basis method:**
- **FIFO** (First In, First Out) is the customary default. Circular 05/2018 prescribes **no** cost-basis method, so another may be used where applied consistently and documented. What the circular DOES prescribe, and agents routinely miss: section 3.1.5.1 makes the consideration in a barter trade the **same figure on both sides**, the seller's proceeds and the buyer's original cost, at the crypto's fair value in shekels **unless the asset bought carries a stated price (מחיר נקוב), which then fixes the crypto's disposal value**. The circular states no representative-rate requirement and no retention period either, so do not attribute those to it.

**Currency conversion:** convert every transaction to shekels at the rate on the transaction date, and determine the shekel value of **both** sides of a crypto-to-crypto trade at the time of the trade.

### Step 2: Collect Transaction Data

Gather the user's complete transaction history. The following data points are needed for each transaction:

1. **Date and time** of the transaction
2. **Transaction type**: buy, sell, trade, receive (airdrop, staking, mining), send, gift
3. **Asset**: Which cryptocurrency (BTC, ETH, etc.)
4. **Amount**: Quantity of the asset
5. **`price_nis`, the TOTAL shekel consideration for the row, never the per-unit price.** Two ETH bought at 8,000 each is `price_nis=16000`. Reversing it rescales every gain by the quantity and no gate can catch it. Convert foreign-fiat legs to shekels yourself; the calculator does not
6. **Exchange/platform**: where it occurred (Bits of Gold, Binance, Coinbase)
7. **Fees**: transaction, gas and exchange fees (deductible from gains)
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
| Buy and hold, then sell | Capital gain | 25% | Form 1399י |
| Crypto-to-crypto swap | Capital gain (disposal + acquisition) | 25% | Form 1399י |
| Staking rewards | Ordinary income at receipt, then capital gain on sale | 25-50% | 1301 for the receipt; 1399י only on the later sale |
| Liquidity mining/yield farming | Ordinary income | Marginal rates | Form 1301 |
| Airdrops (free tokens) | Income at receipt, capital gain on sale | Marginal + 25% | 1301 for the receipt; 1399י on the sale |
| Mining | Business income, categorically | Marginal rates | Form 1301 |
| NFT sales (creator) | Business income | Marginal rates | Form 1301 |
| NFT sales (collector) | Capital gain | 25% | Form 1399י |
| Hard fork tokens | Zero cost basis, capital gain on sale | 25% | Form 1399י |
| Lending interest (CeFi/DeFi) | Interest income | 25% (passive) | Form 1301 |

**Classification notes:**
- **Mining is not a scale question.** Circular 05/2018 s.3.1.4 treats mined crypto as business income categorically; offer no hobby-versus-business test for it.
- **Staking** has no definitive ITA guidance. Conservative treatment: income at receipt at market value, then gain or loss on sale. Some advisers argue the 25% passive rate.
- **Airdrops**: income at market value on receipt, which becomes the basis.
- **Hard forks**: zero cost basis here is a conservative CHOICE, not a sourced rule, and it sits oddly beside the airdrop treatment (income at receipt, becoming basis). State the position you take.
- **Business rows also carry National Insurance and health tax**, which the rate column does not show. Combined rates: see the reference file.
- **Lending interest is not automatically 25%.** Section 2(4) fixes no rate. 125C(b) sets 25%, **125C(c)(1) charges 15%** on a NON-index-linked asset (which covers crypto and stablecoin lending), and **125C(d) pushes it to the full marginal rate** where the interest is business income or in the books, or the recipient is a material shareholder, employee or supplier of the payer. See the reference file.
- **DeFi yields** (liquidity provision, farming): ordinary income at marginal rates.

See `references/crypto-tax-regulations.md` and `references/crypto-tax-scenarios.md`.

### Step 5: Choose the Right Reporting Form



**Check the form's own scope before routing a crypto disposal onto it.** Form **1399י** is "הודעה על מכירת נכס", the notice of an **asset** sale, and is the form Section 91(d)(1) requires within 30 days. Forms **1322, 1325 and 1326** are all titled as **ניירות ערך** forms, and 1322 is expressly scoped to securities **הנסחרים בבורסה**; crypto is a נכס, not an exchange-traded security. The "Nispach Gimel" labels earlier versions of this skill attached to 1322 and 1325 are not the ITA's, which attaches נספח labels to 1320.

So: report the disposal on **1399י within 30 days**, and before attaching a securities schedule to the annual return, confirm with the assessing officer or a CPA which appendix the ITA expects for a non-securities asset. Full published titles are in `references/crypto-tax-regulations.md`.

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
7. **Holding period**: under or over 12 months. Individuals pay 25% either way, with no US-style long-term preference. Duration matters mainly for the inflationary-amount split under Sections 88 and 91(c), which the calculator does NOT apply. Do not cite 91(b)(3) for it; that is the non-index-linked bond rate.

**Loss offsetting rules:**
- Capital losses from crypto can offset capital gains from crypto in the same tax year
- Capital losses from crypto can offset capital gains from other assets (stocks, real estate) in the same year
- Capital losses can be carried forward to offset capital gains in future years under Section 92 of the Income Tax Ordinance (but cannot offset ordinary income)
- Losses from one spouse can offset gains of the other spouse if filing jointly

### Step 6: Calculate Advance Tax Payments (Mikdamot)

If the user has crypto gains during the year, they generally need to file and pay advance tax (mikdama) ahead of the annual return:

- **Form**: **Form 1399י** (1399-yod) for individuals - the dedicated capital gains advance-payment form. Virtual-currency disposals are filed with transaction codes **77** (sale) and **71** (virtual currency). Form 1399ח is the equivalent for companies.
- **Reporting deadline**: within **30 days** of the capital gain event for one-off disposals; the form is filed to the assessing officer (pakid shuma).
- **Payment**: 25% of the real gain for individuals. **The surtax is NOT part of this advance.** Section 121B(b) says expressly that Section 91(d)'s advance-payment rules "לא יחולו" to income chargeable to the surtax, so the 3% and 2% are settled annually in the return, not in the 30-day mikdama. A user who adds 5% to the advance overpays it.
- **If the deadline is missed**, Section 91(d)(2e) lets the assessing officer extend the date or reduce the advance on reasonable grounds; that is a route to ask about, not only "pay late and accrue interest". Conversely, under Section 91(d)(2a) the officer may **increase** the advance where he has reasonable grounds to think it is understated by 20% or more, payable within 30 days of his decision.
- **Annual reconciliation**: advance payments are credited against the final annual tax liability when filing the annual return.
- **Penalties for non-payment**: interest (ribit) and linkage differences (hafreshei hatzmada) accrue from the 30-day deadline.

The legacy "Form 7002" reference in older guides is outdated for crypto reporting - use Form 1399י.

```bash
python scripts/crypto-gains-calculator.py --input transactions.csv --year 2025 --advance-payments
```

### Step 7: Provide Filing Guidance

Guide the user through the tax filing process:

1. **Compile the disposal schedule**: every disposal with acquisition date, cost, proceeds and real gain, in the 1399י columns. There is no ITA crypto appendix (see Step 5); this is your working paper.
2. **File the annual tax return**: submit Form 1301 with the appendices the ITA requires. **There is no crypto appendix**: the gain goes into the 1301's own capital-gains fields at the 25% line, supported by copies of the 1399י notices already filed (their tax is credited against the advance) and your disposal schedule. `references/crypto-tax-regulations.md` sets out the packaging. **Form 1344** is the appendix for losses carried forward from an earlier year, which matters here because Section 92 allows an unused capital loss to be carried forward indefinitely. A crypto disposal generally creates a filing obligation, but check the proposed exemption first, still only a **draft**: טיוטת תקנות מס הכנסה (פטור מהגשת דין וחשבון) (תיקון) (נכס דיגיטלי), published for comment January 2025 under **Section 134A**. It would exempt a salaried taxpayer where the crypto was traded through a **supervised Israeli platform that withheld tax at source** and the year's digital-asset sales stay under a **digital-asset-specific ceiling in תוספת ו** of those regulations. **Do not quote a shekel figure for that ceiling from this skill**; earlier versions gave the general Section 131 ceilings, which is a different mechanism. Read it out of the regulation text, and verify the regulation was actually enacted before relying on it. Paying an advance (mikdama) does NOT by itself remove the annual-return obligation.
3. **Filing deadline**: for TY2025 the ITA publishes **30 June 2026 online**, **29 May 2026 on paper**. Representing accountants usually get extensions. Verify the current year on gov.il.
4. **Self-assessment of surtax**: above NIS 721,560 of total taxable income, 3% under Section 121B(a) plus 2% on capital-source income under 121B(a1). The Ordinance fixes 721,560 for 2024 through 2027, so no CPI uplift. 121B(e) excludes the inflationary amount from the base, and 121B(b) keeps the surtax out of the 30-day advance.
5. **Voluntary Disclosure. Check today's date FIRST, because the answer changes on 1 September 2026.** The Tax Authority declared the procedure on 25 August 2025 with an end date of **31 August 2026**.

   **While it is open** (up to and including 31.8.2026) it grants immunity from criminal proceedings to a taxpayer who corrects his reports and pays the tax in full, on two tracks: a Regular Track settled by an assessment agreement, and a **Green Track** for small cases. The Green Track's digital-asset limb covers income from digital assets **not exceeding NIS 500,000 for the entire disclosure period** (not per year), where the fair value of ALL the applicant's digital assets at **31 December 2024** does not exceed **NIS 1,500,000**. The Tax Authority, not the applicant, chooses the track. If the deadline is days away, say so plainly and treat it as urgent: identify the track, assemble the prior-year figures and file the application before the deadline even if the computation is still provisional, and involve a tax-specialist lawyer in that filing; the immunity turns on the application, not on the arithmetic.

   **Once it has closed**, there is no immunity to obtain and you must not imply otherwise. The route is then an ordinary correction through the assessing officer under Section 131, with the deficiency and offence exposure that normally attaches to a late or amended return, and the taxpayer should take advice before filing. Check whether a successor procedure has been declared rather than assuming one has.
6. **Bank refuses the funds (Form 909)**: where a bank refuses in writing to accept crypto-derived deposits, an **individual** (not a company) files **Form 909** and pays in shekels directly into the ITA's Bank of Israel account, under ITA Instruction 06/2024. Attachments and the AML review: see `references/crypto-tax-regulations.md`.
7. **Record keeping**: keep all transaction records, exchange exports and wallet data. Circular 05/2018 s.3.1.3 says only "ככול שיידרש להנחת דעתו של פקיד השומה" and fixes no period; the seven-year figure comes from the bookkeeping directives, not from this circular.

**When to recommend professional help:** over 100 trades a year, complex DeFi (multi-chain, bridging, wrapping), an unclear business-versus-investment call, gains over 500,000 NIS, tokens from an ICO or IEO, or any cross-border position.

## Examples

### Example 1: Simple Bitcoin Buy and Sell

User says: "I bought 0.5 BTC in January 2025 for 80,000 NIS and sold it in August 2025 for 120,000 NIS. What's my tax?"

Actions:
1. Identify the transaction: single buy, single sell.
2. Calculate capital gain: 120,000 - 80,000 = 40,000 NIS.
3. Apply 25% capital gains tax: 40,000 x 0.25 = 10,000 NIS.
4. Check surtax threshold: a 40,000 NIS gain is well below NIS 721,560, so no surtax (assuming no other income above the threshold).
5. Note the holding period: 7 months. The 25% rate applies regardless, but the inflation-component split (sechum hatzmada) is negligible for such a short hold.

Result: capital gain 40,000 NIS, tax liability 10,000 NIS. The user should have filed Form 1399י (transaction codes 77/71) within 30 days of the August sale and paid the 10,000 NIS as a mikdama. If the deadline is missed, the user should still file and pay as soon as possible to minimise interest and linkage penalties. The gain is then carried into the **2025 annual tax return**, due **30 June 2026 (online) or 29 May 2026 (paper)**.

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

Result: The crypto-to-crypto trade triggers a taxable event of 10,000 NIS capital gain (2,500 NIS tax). The new BTC position has a cost basis of 27,000 NIS (the NIS value of 3 ETH at the time of trade). The remaining 2 ETH retain their original cost basis of 7,000 NIS each. The agent generates a disposal entry for the 30-day Form 1399י notice.

## Bundled Resources

### Scripts
- `scripts/crypto-gains-calculator.py` -- FIFO capital-gains calculator over a transaction CSV. It refuses to compute on impossible data (negative or zero quantities, dates before the Bitcoin genesis block or in the future) rather than returning a silent zero, and a disposal with no matching purchase lot is reported as UNPRICED and excluded from the totals rather than being given a zero cost basis. Exit code 3 means the report is incomplete. It performs NO currency conversion: convert foreign-currency legs to shekels before the file reaches it. Run: `python scripts/crypto-gains-calculator.py --help`

### References
- `references/crypto-tax-regulations.md` -- ITA circulars, the Ordinance sections with their verbatim text (including the Section 100A formula), the ITA's own published form titles, classification rules and deadlines.
- `references/crypto-tax-scenarios.md` -- worked examples: simple trades, crypto-to-crypto swaps, DeFi staking, NFT sales, mining, airdrops, hard forks.

## Recommended MCP Servers

| MCP | What It Adds |
|-----|-------------|
| [BOI Exchange Rates](https://agentskills.co.il/he/mcp/boi-exchange) | The Bank of Israel daily representative rate, for converting foreign-currency legs to shekels **before** they reach the calculator, which does no conversion itself. Circular 05/2018 does not mandate the representative rate (its rule is fair value in shekels, with a stated-price override), so it is a defensible documented choice rather than a legal requirement. |

## Gotchas
- Israel taxes crypto as property (capital gains), not as currency. Agents may apply currency-exchange rules to crypto transactions, which is incorrect under Israeli tax law.
- The Israeli rate is 25% for individuals, not the US 15%/20%. Agents trained on US data will use the wrong one.
- Israeli practice defaults to FIFO. Agents may default to average cost or LIFO, which are not standard here.
- Crypto-to-crypto swaps are taxable events in Israel. Agents may treat them as non-taxable exchanges (the old US rule), which has never been the Israeli position. Circular 05/2018 section 3.1.5.1 also requires the SAME shekel figure to serve as the seller's proceeds and the buyer's original cost, so the two CSV legs of a swap must carry identical values.
- **Stablecoins are still an "asset" under Section 88**, not foreign currency. Every USDT-to-USDC swap, every conversion leg of a DeFi trade and every off-ramp is a taxable disposal in shekels. Users treat them as cash equivalents and skip them, missing most of an active DeFi participant's taxable events.
- **Inflation indexation (sechum hatzmada) is not applied by the calculator, and the rate is not 0%.** A capital gain splits into a real gain, taxed under Section 91(b), and an inflationary amount. Section 91(c) taxes the **chargeable** inflationary amount at **10%**; it comes out at nil for crypto only because Section 88 defines the chargeable part as the portion that would have arisen had the asset been sold on 31.12.1993, which no crypto lot can satisfy. Do not state a "0% rate", which is not in the Ordinance. The calculator applies 25% to the whole gain with no CPI step, so it overstates tax on long-held lots in inflationary years. Form 1326א is the ITA's own real-gain/inflation helper. Flag the limitation and recommend a manual indexation pass or CPA review before filing.
- **Israel has no wash-sale rule.** A taxpayer may realise a December loss and re-buy in January with the loss fully recognised. Agents trained on US tools may wrongly disallow it.
- **Gifts and inheritance carry the donor's basis, but Section 97(a)(5) is not the authority for it.** 97(a)(5) is an EXEMPTION for a good-faith gift where the recipient is not a foreign resident; it says nothing about basis, which runs through Section 88's מחיר מקורי and יום הרכישה. Treating gifted or inherited crypto as zero-basis or as market value at receipt is wrong both ways.
- **Crypto lost to insolvency, theft or lost keys** is a capital loss only once the loss is final and documented (bankruptcy order, police report). Do not write off frozen-but-solvent balances or undocumented key loss.
- **A capital loss offsets more than the real gain, and the carry-forward has a condition.** Section 92(a)(1) offsets the loss against the real gain first, then each remaining shekel offsets **three and a half shekels** of chargeable inflationary amount. Section 92(b) carries the unused amount forward against capital gains in the following years, **but only if a return was filed for the year the loss arose**, so a client who skipped that year has lost the carry-forward. The calculator performs neither offset nor carry-forward; Form 1344 is the appendix for the brought-forward figure.
- **Leaving Israel triggers an exit tax (deemed sale, Section 100A), and the deferral is NOT an election.** s.100A(a) deems all assets sold one day before residency ends, and s.100A(b) deems anyone who does not pay then to have **requested** deferral to realization: no form, no choice. What he pays is the "chargeable portion of the gain", measured at realization and apportioned by elapsed time, and **no interest or linkage accrues during the deferral**. The formula and the full subsection text are in `references/crypto-tax-regulations.md`. The calculator does NOT model this; route relocation scenarios to a CPA and the aliyah skills.
- **An oleh or toshav chozer vatik may hold a 10-year exemption on foreign-acquired crypto**: Section 14(a) for income, **Section 97(b)(1)** for capital gains, running ten years from becoming a resident. The calculator does not model it and will overstate tax.

## Troubleshooting

### Problem: no NIS rate available for a transaction date
Cause: the Bank of Israel publishes no rate on Shabbat and holidays.
Solution: use the rate from the most recent prior business day, and **do it in the CSV, not in the tool**. The calculator performs no rate lookup of any kind and has no `--manual-rate` flag; it consumes `price_nis` exactly as given. Earlier versions of this skill described an automatic lookup and a manual-rate flag; neither exists.

### Error: "FIFO queue exhausted - more sold than purchased"
Cause: the history sells more than it bought, usually because purchases are missing (deposits from another exchange or wallet, or a partial export).
Solution: review the history for completeness; a transfer in from another exchange or wallet is not a taxable event but must be recorded to carry the cost basis. Add the missing purchases. Where the original records are genuinely unavailable, establish a basis from the earliest available market price, document it, and disclose it. The calculator will not do this for you: it marks such disposals UNPRICED and excludes them, so the printed totals UNDERSTATE the gain until you supply a basis.

### Error: "Transaction type not recognized for tax classification"
Cause: The calculator encountered a transaction type it cannot automatically classify for tax purposes (e.g., a complex DeFi interaction, bridge transaction, or wrapped token conversion).
Solution: Review the transaction manually. Common DeFi operations and their classifications: wrapping (ETH to WETH) is generally not a taxable event; bridging between chains may be a taxable event if it involves a swap; providing liquidity is not taxable until withdrawal (but LP token movements may trigger events). For complex DeFi operations, consult `references/crypto-tax-scenarios.md` and consider professional tax advice.

### Error: the report says UNPRICED, or exits with code 3
Cause: one or more disposals have no matching purchase lot in the file, so their cost basis is unknown. The calculator deliberately does NOT assume a zero basis, because that overstates the gain and manufactures an acquisition fact for the return.
Solution: Review the error output which lists the specific transactions with missing data. For each, provide the acquisition date (FIFO-determined) and the NIS value at that date. If the acquisition was a gift or airdrop, the cost basis rules differ: gifts use the donor's cost basis (Section 97(a)(5) carryover), and airdrops use the market value at receipt. Update the transaction CSV with the corrected data and re-run.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Israeli Tax Authority - annual return service (Form 1301) | https://www.gov.il/he/service/reporting-and-payment-2025-annual-tax-report-for-individuals | Current-year filing deadlines, links to Forms 1322 and 1325, online filing portal |
| Bank of Israel - representative rates (sha'ar yatzig) | https://www.boi.org.il/roles/markets/exchangerates/ | Daily NIS reference rates for currency conversion of foreign-fiat legs of crypto trades |
| ITA Circular 05/2018 (crypto classification, FIFO, virtual currency definition) | https://www.gov.il/BlobFolder/policy/income-tax-professional-inst-5-2018/he/Policy_ProfessionalInstIncomeTax_hor_acc%2015.2.18.pdf | Foundational tax-treatment guidance for virtual currencies |
| Voluntary Disclosure Procedure, ITA announcement | https://www.gov.il/he/pages/sa250825-1 | The declaration of 25 Aug 2025, the 31 Aug 2026 end date, and the Green Track digital-asset limits. **Check whether the window is still open before advising anyone to use it.** The earlier-cited page pa010925-1 is a two-paragraph clarification that carries none of these details |
| Form 909 - paying crypto tax when a bank refuses the funds | https://www.gov.il/he/service/reporting-cryptocurrency-activity | Bank-refusal payment procedure, required attachments, individuals only |
| Bituach Leumi self-employed rates (2026) | https://www.btl.gov.il/Insurance/National%20Insurance/type_list/Self_Employed/Pages/rates.aspx | Current National Insurance + health-tax rates for business-classified crypto traders |
| OECD Crypto-Asset Reporting Framework (CARF) - committed jurisdictions | https://www.oecd.org/content/dam/oecd/en/networks/global-forum-tax-transparency/commitments-carf.pdf | Israel is listed under "Jurisdictions undertaking first exchanges by **2028**", not the 2027 group. Collection from 2026. Re-check the list, which the Global Forum revises |
