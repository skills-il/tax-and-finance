---
name: tase-stock-analysis
description: >-
  Analyze Israeli stocks on TASE (Tel Aviv Stock Exchange), track TA-35 and
  TA-125 indices, and evaluate dual-listed companies (TASE + NASDAQ). Use when
  user asks about Israeli stocks, "boorsa", "TA-35", "TASE", Maya filings,
  dual-listed companies, or Israeli capital gains tax on securities. Provides
  index composition, Maya (TASE disclosure) filings lookup, capital gains tax
  calculations (25% on securities), and Bank of Israel interest rate context
  for valuation. Do NOT use for general international stock analysis unrelated
  to Israel, or for cryptocurrency trading.
license: MIT
compatibility: >-
  Requires network access for TASE API and Maya filings. Works with Claude
  Code, Cursor, GitHub Copilot, Windsurf, OpenCode, Codex.
metadata:
  author: skills-il
  version: 1.1.0
  category: tax-and-finance
  tags:
    he:
      - בורסה
      - מניות
      - ת"א-35
      - השקעות
      - שוק-הון
      - ישראל
    en:
      - stock
      - tase
      - ta-35
      - investments
      - capital-market
      - israel
  display_name:
    he: ניתוח מניות בורסת ת"א
    en: TASE Stock Analysis
  display_description:
    he: >-
      ניתוח מניות בבורסת תל אביב, מעקב אחר מדדי ת"א-35 ות"א-125, והערכת
      חברות דואליות. כולל חישוב מס רווחי הון ושילוב דיווחי מאי"ה.
    en: >-
      Analyze Israeli stocks on TASE (Tel Aviv Stock Exchange), track TA-35 and
      TA-125 indices, and evaluate dual-listed companies (TASE + NASDAQ). Use
      when user asks about Israeli stocks, "boorsa", "TA-35", "TASE", Maya
      filings, dual-listed companies, or Israeli capital gains tax on
      securities. Provides index composition, Maya filings lookup, capital gains
      tax calculations (25% on securities), and Bank of Israel interest rate
      context for valuation. Do NOT use for general international stock analysis
      unrelated to Israel, or for cryptocurrency trading.
  supported_agents:
    - claude-code
    - cursor
    - github-copilot
    - windsurf
    - opencode
    - codex
    - antigravity
---

# TASE Stock Analysis

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
- **Market hours:** TASE trades Sunday-Thursday, 09:59-17:14 (pre-open from 09:02)

### Step 4: Calculate Capital Gains Tax (Mas Revach Hon)
When the user has sold or plans to sell securities:

| Scenario | Tax Rate | Notes |
|----------|----------|-------|
| Individual, non-substantial shareholder | 25% | Standard rate on net gain |
| Substantial shareholder (over 10%) | 25% up to NIS 650,000, then 30% | Graduated rate structure |
| Shares eligible for inflationary adjustment (varies by acquisition date and asset type) | Exempt | Only real gain is taxed, consult current regulations |
| Offsetting losses (kizuz hefsedim) | Allowed | Losses offset gains in same tax year |
| Foreign resident | Treaty-dependent | Check double taxation treaty |

Calculation:
```
net_gain = sale_price - purchase_price - transaction_costs
tax = net_gain * 0.25  # or graduated rate for substantial shareholder
```

### Step 5: Evaluate Dual-Listed Opportunities
For dual-listed companies (e.g., Check Point, CyberArk, NICE, Sapiens):
1. Compare TASE price (in NIS) vs. US price (in USD) using current exchange rate
2. Account for ADR ratio (some dual-listed have different share ratios)
3. Factor in different trading hours (TASE closes before US opens)
4. Note tax treaty implications -- Israeli residents pay Israeli capital gains tax regardless of which exchange

### Step 6: Review Maya Filings
Check relevant disclosures on the Maya system (TASE disclosure platform):
- **Immediate reports:** Material events that affect stock price
- **Periodic reports:** Quarterly and annual financial statements
- **Related party transactions:** Insider trades and holdings changes
- **Shelf offerings:** Potential dilution events

Summarize key findings and flag any material items.

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
User says: "Compare Check Point stock price on TASE vs NASDAQ"
Actions:
1. Fetch Check Point TASE price (in NIS) and NASDAQ price (in USD)
2. Convert using current BOI representative rate (sha'ar yatzig)
3. Calculate premium/discount between exchanges
4. Note that arbitrage is limited by settlement timing and currency conversion costs
Result: Price comparison with exchange rate analysis and practical arbitrage assessment

### Example 3: Capital Gains Tax on Stock Sale
User says: "I sold Teva shares for 120,000 NIS, bought them for 80,000 NIS. What's my tax?"
Actions:
1. Identify: Net gain = 120,000 - 80,000 = 40,000 NIS
2. Check: Standard rate (25%) assuming non-substantial shareholder
3. Calculate: Tax = 40,000 * 0.25 = 10,000 NIS
4. Note: Can offset against any capital losses (hefsedei hon) from same tax year
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
- The Tel Aviv Stock Exchange (TASE) trades Sunday through Thursday, not Monday through Friday. Agents may schedule market queries or expect data for Fridays and Saturdays, which are non-trading days.
- TASE ticker symbols follow a different format than US exchanges. Israeli stocks use numeric codes (e.g., 604611 for Teva) alongside short Hebrew names. Agents may try to use US-style letter tickers.
- Israeli stock prices on TASE are quoted in agorot (1/100 of a shekel), not in shekels. Agents may display raw prices without dividing by 100, showing prices 100x too high.
- Dual-listed Israeli companies (e.g., Teva, Check Point) trade on both TASE and NASDAQ with different prices due to exchange rate fluctuations. Agents may not reconcile the price difference.

## Troubleshooting

### Error: "TASE ticker not found"
Cause: TASE uses numeric securities numbers and Hebrew names, not US-style tickers
Solution: Search by company Hebrew name or securities number (mispar niyar erech). Use Maya search for lookup.

### Error: "Exchange rate mismatch for dual-listed"
Cause: Using stale or non-representative exchange rate for comparison
Solution: Use Bank of Israel representative rate (sha'ar yatzig) published daily at 15:30. For intraday, note rates are indicative only.

### Error: "Capital gains calculation unclear"
Cause: Complex scenarios like partial sales, inflationary adjustments, or inherited shares
Solution: For shares eligible for inflationary adjustment (varies by acquisition date and asset type), consult current tax regulations for specific dates. For inherited shares, acquisition cost is market value at inheritance date. Consult a tax advisor (yo'etz mas) for complex cases.