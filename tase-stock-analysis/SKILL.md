---
name: tase-stock-analysis
description: Analyze Israeli stocks on TASE (Tel Aviv Stock Exchange), track TA-35 and TA-125 indices, and evaluate dual-listed companies (TASE + NASDAQ). Use when user asks about Israeli stocks, "boorsa", "TA-35", "TASE", Maya filings, dual-listed companies, or Israeli capital gains tax on securities. Provides index composition, Maya (TASE disclosure) filings lookup, capital gains tax calculations (25% on securities), and Bank of Israel interest rate context for valuation. Do NOT use for general international stock analysis unrelated to Israel, or for cryptocurrency trading.
license: MIT
---

# TASE Stock Analysis

## Legal notice

This is a free information tool operated by an AI model. It gathers data that has been published to the public and presents it in an organised form. The operators of this tool hold no personal interest in the securities or financial assets it mentions, and receive no consideration, commission, or benefit of any kind for presenting them. All of its outputs are produced automatically by an AI model, with no involvement, review, or approval by a licensed investment adviser.

The output is not investment advice, not investment marketing, and not a recommendation to buy, sell, or hold any security or financial asset. It is not a substitute for advice that takes account of the particular circumstances and needs of each person, and it does not consider your financial position, your investment objectives, or the risk you are able to bear. Market data may be partial, delayed, or wrong, and an AI model may err, omit data, or present a wrong conclusion. Consult a licensed adviser before any investment decision and verify every figure against the official source. All use of its output is the user's sole responsibility.


## Instructions

### Step 1: Identify the Analysis Type
Ask the user what kind of analysis they need:

| Type | Hebrew | Description | Key Data |
|------|--------|-------------|----------|
| Index tracking | מעקב מדד | TA-35 or TA-125 index performance | Index composition, weight, performance |
| Single stock | ניתוח מניה | Individual TASE-listed stock analysis | Price, volume, fundamentals |
| Dual-listed | חברה דואלית | Companies listed on TASE + NASDAQ/NYSE | Arbitrage, currency effect, tax implications |
| Maya filing | דיווח מאי"ה | TASE disclosure filings lookup | Material events, financial reports, insider trades |
| Capital gains | רווחי הון | Tax calculation on securities gains | 25% tax rate, exemptions, offsetting losses |

### Step 2: Gather Market Data
Depending on the analysis type, collect:
- **Index data:** Use `scripts/fetch_tase_data.py` to retrieve TA-35 or TA-125 composition and weights
- **Stock data:** Ticker symbol (TASE uses Hebrew names or numeric codes), current price, volume
- **Dual-listed data:** Both TASE ticker and US ticker (e.g., NICE on TASE and NICE on NASDAQ)
- **Maya filings:** Company name or securities number, date range for filings

### Step 3: Apply Israeli Context
For any stock analysis, layer in Israeli-specific factors:
- **Bank of Israel interest rate:** Current BOI rate affects valuations and sector rotation
- **Shekel/Dollar exchange rate:** Critical for dual-listed arbitrage and foreign exposure
- **Sector composition:** Israeli market heavy in banking (Hapoalim, Leumi, Discount), pharma (Teva), tech
- **Market hours:** TASE trades Monday-Friday. Monday-Thursday 09:59-17:14, Friday shortened session 09:59-13:50. No trading on Saturday (Shabbat) or Jewish holidays

### Step 4: Calculate Capital Gains Tax (Mas Revach Hon)
When the user has sold or plans to sell securities:

| Scenario | Tax Rate | Notes |
|----------|----------|-------|
| Individual, non-substantial shareholder | 25% | Standard rate on the real gain |
| Substantial shareholder (10% or more) | 30% | On the real gain, where the seller held 10%+ at the sale or during any of the 12 months before it |
| High-income individual | + surtax (mas yesef) | A separate surtax applies above an annual threshold that is indexed each year (ILS 721,560 in 2026): 3% on total taxable income above the threshold, plus a further 2% from 2025 on the capital-source part above it = up to 5% on the slice over the threshold, on top of the 25%/30%. On the slice above the threshold, the marginal rate on securities gains is the base rate plus that 5% (so ~30% for a 25% payer, more for a substantial shareholder). |
| Bonds and funds (not shares) | 15% or 25% | Non-CPI-linked shekel bonds and makam: 15% on the nominal gain. CPI-linked bonds: 25% on the real gain. ETFs (kranot sal): 25%. See `references/capital-gains.md`. |
| Inflationary amount (CPI rise, or the exchange rate for a foreign-currency security) | Exempt | Only the real gain is taxed; pre-2003 holdings follow transition rules |
| Offsetting losses (kizuz hefsedim) | Allowed | Offset capital gains in the same year; unused losses carry forward and later offset only capital gains |
| Foreign resident | Treaty-dependent | Check double taxation treaty |

Calculation:
```
net_gain = sale_price - purchase_price - transaction_costs
real_gain = net_gain - inflationary_amount  # CPI rise on the cost (FX rate for a foreign-currency security); take it from the broker's tax statement
tax = real_gain * 0.25  # or 0.30 for substantial shareholder (10%+)
```

### Step 4b: Dividend Tax (Mas al Dividend)
Dividends are taxed separately from capital gains, and every stock analysis should account for them:
- **25%** for an individual non-substantial shareholder, **30%** for a substantial shareholder (10%+). The same surtax (mas yesef) applies to dividend income above the annual threshold.
- Dividends are withheld at source (nikui mas bemakor) by the paying company or broker, the investor receives the net amount.

**Tax withheld at source (nikui b'makor):** For securities held through an Israeli broker, BOTH capital-gains tax and dividend tax are auto-withheld at source. A return may still be required to offset losses across different brokers, reclaim over-withholding, or when other mandatory-filing rules apply, so "withheld at source" does not always mean "nothing to file". For a FOREIGN brokerage (e.g. Interactive Brokers), nothing is withheld locally: the investor must pay a semi-annual capital-gains advance (mikdama) by 31 January and 31 July on gains realized in the preceding half-year, and report the gains in the annual income-tax return (its capital-gains appendix). Missing the advance accrues interest and CPI linkage. So the practical answer to "what's my tax?" depends on where the securities are held.

**Losses (kizuz hefsedim):** A capital loss offsets all capital gains, including gains from Israeli or foreign securities and from the sale of property (a loss on a non-Israeli asset first offsets foreign-source gains). A securities loss can also offset interest and dividend income from securities, where that income was taxed at no more than 25%. Unused losses carry forward indefinitely, but in later years they offset only capital gains, not dividends or interest. There is NO annual tax-free capital-gains allowance in Israel (unlike the UK/US), every shekel of net real gain is taxable.

**Tax-advantaged vehicles:** A keren hishtalmut, kupat gemel, or pension fund has its own tax regime, different from a direct brokerage account. When comparing an investment held directly vs. inside such a vehicle, check the vehicle's current tax terms rather than assuming the 25% direct-account rate.

### Step 5: Evaluate Dual-Listed Opportunities
For dual-listed companies (e.g., NICE on NASDAQ, Teva and ICL on NYSE). Confirm the listing is still live before comparing: companies leave the dual-listed set through mergers and take-privates, and some well-known Israeli tech companies (e.g. Check Point) trade only in the US and have no TASE price at all:
1. Compare TASE price (in NIS) vs. US price (in USD) using current exchange rate
2. Account for ADR ratio (some dual-listed have different share ratios)
3. Factor in different trading hours (TASE and US markets now overlap on Monday-Friday, but Friday TASE closes early at 13:50)
4. Note tax treaty implications -- Israeli residents pay Israeli capital gains tax regardless of which exchange. For a security held by an individual that is denominated in a foreign currency (e.g. a share bought in USD), the Ordinance uses that currency's exchange rate as the index (Section 88), so the part of the shekel gain that comes only from the dollar strengthening against the shekel is the exempt inflationary amount, not taxable gain. Do not tax the FX movement. US tax withheld is generally creditable against the Israeli tax under the Israel-US treaty (zikui mas zar) to avoid double taxation. The same applies to US dividends on dual-listed shares: US withholding (file a W-8BEN with the broker so the treaty rate applies) is credited against the Israeli 25%/30% dividend tax. The credit is capped at the Israeli tax on that same foreign income, so foreign tax above that cap is not refunded; the excess can only be carried forward under the Ordinance's conditions

### Step 6: Review Maya Filings
Check relevant disclosures on the Maya system (TASE disclosure platform):
- **Immediate reports:** Material events that affect stock price
- **Periodic reports:** Quarterly and annual financial statements
- **Related party transactions:** Insider trades and holdings changes
- **Shelf offerings:** Potential dilution events

Summarize key findings and flag any material items.

### MCP Integration: Live TASE Data

For live market data, use the **TASE MCP Server** ([tase-mcp](https://agentskills.co.il/he/mcp/tase-mcp), source in [skills-il/mcps](https://github.com/skills-il/mcps/tree/master/tase-mcp)).

**Prerequisites:**
- A TASE Data Hub developer account: sign in at https://datahubapi.tase.co.il, create an application, and register it for each product you need (some products are paid and need TASE commercial approval). Calling a product your key is not registered for returns HTTP 403.
- MCP server: `npx -y @skills-il/tase-mcp` (Node.js 18+)

**Setup:**
Set the environment variable `TASE_API_KEY` to the `apikey` of your application.

**Selected MCP Tools** (the server exposes 36; these are the ones this skill uses most):
| Tool | What it does |
|------|-------------|
| `tase_list_indices` | List all TASE indices with their IDs |
| `tase_get_index_components` | Constituents and weights of an index on a trade date |
| `tase_get_index_last_rate` | Most recent rate of an index |
| `tase_list_companies` | Companies with TASE-traded securities, including dual-listing flags |
| `tase_list_traded_securities` | Securities that traded on a given date |
| `tase_list_delisted_securities` | Securities delisted in a given year/month |
| `tase_get_trading_schedule` | Trading and vacation schedule |
| `tase_list_funds` | Mutual funds registered on TASE |

**Note:** The MCP does not read Maya filings; look those up at https://maya.tase.co.il. Without MCP, this skill provides analysis guidance using general market knowledge. With MCP, the agent fetches live market data directly from the official TASE Data Hub.

## Examples

### Example 1: TA-35 Index Overview
User says: "Show me the current TA-35 composition and top performers"
Actions:
1. Run `python scripts/fetch_tase_data.py --index TA35`
2. Display top holdings by weight (Bank Hapoalim, Bank Leumi, ICL, Teva, etc.)
3. Show recent performance vs. BOI interest rate context
4. Note upcoming ex-dividend dates for major components
Result: Summary table of TA-35 with weights, performance, and key metrics

### Example 2: Dual-Listed Arbitrage Check
User says: "Compare NICE stock price on TASE vs NASDAQ"
Actions:
1. Fetch NICE TASE price (in agorot, divide by 100 to get shekels) and NASDAQ price (in USD)
2. Convert using current BOI representative rate (sha'ar yatzig)
3. Calculate premium/discount between exchanges
4. Note that arbitrage is limited by settlement timing and currency conversion costs
Result: Price comparison with exchange rate analysis and practical arbitrage assessment

### Example 3: Capital Gains Tax on Stock Sale
User says: "I sold Teva shares for 120,000 NIS, bought them for 80,000 NIS. What's my tax?"
Actions:
1. Identify: Net gain = 120,000 - 80,000 = ILS 40,000
2. Check: Standard rate (25%) assuming non-substantial shareholder, and assuming no CPI rise over the holding period (otherwise subtract the inflationary amount first)
3. Calculate: Tax = 40,000 * 0.25 = ILS 10,000
4. Note: Capital losses (hefsedei hon) from the same year, or carried forward from earlier years, can be offset against this gain
Result: Capital gains tax of 10,000 NIS, with guidance on loss offsetting and filing

### Example 4: Maya Filing Lookup
User says: "Check recent Maya filings for Bank Hapoalim"
Actions:
1. Look up Bank Hapoalim on Maya (securities number 662577)
2. Filter recent immediate reports and periodic filings
3. Summarize material events (dividends, board decisions, regulatory actions)
4. Flag any insider trading reports
Result: Summary of recent disclosures with material items highlighted

## Bundled Resources

### Scripts
- `scripts/fetch_tase_data.py` -- Fetches TASE index data (TA-35, TA-125), stock quotes, and market status. Run: `python scripts/fetch_tase_data.py --help`

### References
- `references/tase-api.md` -- TASE API endpoints for market data, index composition, and Maya filings search. Consult when integrating live market data.
- `references/capital-gains.md` -- Israeli capital gains tax rules for securities: rates, exemptions, loss offsetting, substantial shareholder rules, and foreign resident treaty considerations.

## Gotchas
- Since January 2026, TASE trades Monday through Friday (previously Sunday-Thursday). Friday sessions are shortened (09:59-13:50). Agents trained on pre-2026 data may still assume Sunday-Thursday trading and schedule queries on Sundays, which are now non-trading days.
- TASE ticker symbols follow a different format than US exchanges. Israeli stocks use numeric securities codes alongside short Hebrew names. **Always verify a security number before using it** by opening https://market.tase.co.il/en/market_data/security/662577 and swapping the final path segment for the code you want (662577 = Bank Hapoalim, 604611 = Bank Leumi). TASE securities also carry long-standing English alpha symbols (e.g. POLI = Hapoalim, LUMI = Leumi, TEVA, NICE, ICL) alongside the numeric codes; prefer the alpha symbol for clarity (note Leumi's symbol is LUMI, not LEUMI). These symbols are not new, they have existed for years. Never hardcode security numbers from memory; fetch them from the TASE OpenAPI by company name.
- Israeli stock prices on TASE are quoted in agorot (1/100 of a shekel), not in shekels. Agents may display raw prices without dividing by 100, showing prices 100x too high.
- Dual-listed Israeli companies (e.g., NICE, Teva) trade on both TASE and a US exchange with different prices due to exchange rate fluctuations. Agents may not reconcile the price difference. Agents also assume a company is dual-listed because it is Israeli: Check Point, for example, has no TASE listing, and Sapiens stopped trading after being taken private. Check the listing before quoting a TASE price.

## Troubleshooting

### Error: "TASE ticker not found"
Cause: TASE uses numeric securities numbers and Hebrew names, not US-style tickers
Solution: Search by company Hebrew name or securities number (mispar niyar erech). Use Maya search for lookup.

### Error: "Exchange rate mismatch for dual-listed"
Cause: Using stale or non-representative exchange rate for comparison
Solution: Use the Bank of Israel representative rate (sha'ar yatzig), and check its publication time on the Bank of Israel site rather than assuming one. For intraday, note rates are indicative only.

### Error: "Capital gains calculation unclear"
Cause: Complex scenarios like partial sales, inflationary adjustments, or inherited shares
Solution: For shares eligible for inflationary adjustment (varies by acquisition date and asset type), consult current tax regulations for specific dates. Inheritance is not a taxable sale, and inherited shares get NO step-up to market value: when the deceased died after 31 March 1981, the heir takes the deceased's original cost and acquisition date (Section 88 of the Income Tax Ordinance), so the gain on a later sale runs from the deceased's purchase. Consult a tax advisor (yo'etz mas) for complex cases.