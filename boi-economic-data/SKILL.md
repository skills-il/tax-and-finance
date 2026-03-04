---
name: boi-economic-data
description: >-
  Fetch and analyze economic data from Bank of Israel (data.boi.org.il) and
  the Central Bureau of Statistics (CBS). Use when user asks about Israeli
  interest rates ("ribit"), exchange rates ("sha'ar yatzig"), CPI
  ("madad hamechirim"), inflation, BOI monetary policy, USD/ILS or EUR/ILS
  rates, or CBS economic indicators. Provides BOI API integration for
  real-time and historical rates, CPI calculations, and economic trend
  analysis with Israeli fiscal context. Do NOT use for stock market data
  (use tase-stock-analysis instead) or for tax calculations.
license: MIT
allowed-tools: 'Bash(python:*) WebFetch'
compatibility: >-
  Requires network access for BOI and CBS APIs. Works with Claude Code,
  Cursor, GitHub Copilot, Windsurf, OpenCode, Codex. Python 3.8+ for
  helper scripts.
metadata:
  author: skills-il
  version: 1.0.0
  category: tax-and-finance
  tags:
    he:
      - בנק-ישראל
      - ריבית
      - שע"ח
      - מדד-המחירים
      - ישראל
    en:
      - boi
      - interest-rate
      - exchange-rate
      - cpi
      - israel
  display_name:
    he: נתוני בנק ישראל
    en: BOI Economic Data
  display_description:
    he: >-
      שליפה וניתוח נתונים כלכליים מבנק ישראל (data.boi.org.il) והלשכה
      המרכזית לסטטיסטיקה. כולל ריבית בנק ישראל, שערי חליפין יציגים, מדד
      המחירים לצרכן וניתוח מגמות כלכליות.
    en: >-
      Fetch and analyze economic data from Bank of Israel (data.boi.org.il)
      and the Central Bureau of Statistics (CBS). Use when user asks about
      Israeli interest rates ("ribit"), exchange rates ("sha'ar yatzig"),
      CPI ("madad hamechirim"), inflation, BOI monetary policy, USD/ILS or
      EUR/ILS rates, or CBS economic indicators. Provides BOI API integration
      for real-time and historical rates, CPI calculations, and economic
      trend analysis with Israeli fiscal context. Do NOT use for stock
      market data (use tase-stock-analysis instead) or for tax calculations.
  supported_agents:
    - claude-code
    - cursor
    - github-copilot
    - windsurf
    - opencode
    - codex
---

# BOI Economic Data

## Instructions

### Step 1: Identify the Data Type
Determine what economic data the user needs:

| Data Type | Hebrew | Source | Update Frequency | Key Endpoint |
|-----------|--------|--------|------------------|--------------|
| BOI interest rate | ריבית בנק ישראל | Bank of Israel | After each monetary committee meeting | BOI API |
| Exchange rates | שערי חליפין יציגים | Bank of Israel | Daily at 15:30 (sha'ar yatzig) | BOI API |
| CPI (Consumer Price Index) | מדד המחירים לצרכן | CBS | Monthly (15th of following month) | CBS API |
| Inflation | אינפלציה | CBS / BOI | Monthly | Derived from CPI |
| Money supply | היצע כסף | Bank of Israel | Monthly | BOI API |
| Government bonds | אג"ח ממשלתי | Bank of Israel | Daily | BOI API |

### Step 2: Fetch Data from BOI API
Use `scripts/fetch_boi_rates.py` or make direct API calls:

Base URL: `https://edge.boi.gov.il/FusionEdgeServer/sdmx/v2/data/dataflow/BOI.STATISTICS/`

Key series identifiers:

| Metric | Series ID | Example URL Path |
|--------|-----------|------------------|
| BOI interest rate | ERI.SOD_ZOD.-INTEREST | `ERI_C01.H` |
| USD/ILS rate | ER_USD_ILS | `ER?startperiod=2024-01-01&endperiod=2024-12-31` |
| EUR/ILS rate | ER_EUR_ILS | Same pattern as USD |
| CPI (all items) | CP.M.IL | CBS data series |

API call pattern:
```python
import requests

# Fetch BOI representative exchange rate (sha'ar yatzig)
url = "https://edge.boi.gov.il/FusionEdgeServer/sdmx/v2/data/dataflow/BOI.STATISTICS/ER"
params = {
    "startperiod": "2024-01-01",
    "endperiod": "2024-12-31",
    "format": "csv"
}
response = requests.get(url, params=params)
```

### Step 3: Process Exchange Rates (Sha'ar Yatzig)
Bank of Israel publishes representative exchange rates daily:

| Currency | Hebrew | Code | Typical Use |
|----------|--------|------|-------------|
| US Dollar | דולר אמריקאי | USD | Primary foreign currency, import/export pricing |
| Euro | אירו | EUR | EU trade, travel |
| British Pound | לירה שטרלינג | GBP | UK trade |
| Japanese Yen | ין יפני | JPY | Technology imports |
| Swiss Franc | פרנק שוויצרי | CHF | Financial instruments |

Key rules:
- **Representative rate (sha'ar yatzig):** Published daily at approximately 15:30 IST
- **Used for:** Tax calculations, contract settlements, import duty calculations
- **Friday rate:** Valid through Saturday and Sunday (no weekend updates)
- **Holiday rates:** Last pre-holiday rate applies until next business day

### Step 4: Analyze Interest Rate Decisions
BOI Monetary Committee decisions context:

| Factor | Hebrew | Impact |
|--------|--------|--------|
| Inflation target | יעד אינפלציה | BOI targets 1-3% annual inflation |
| Housing prices | מחירי דיור | Key input for monetary policy |
| Shekel strength | חוזק השקל | Strong shekel may prompt rate cuts |
| Global rates | ריבית עולמית | Fed/ECB decisions influence BOI |
| GDP growth | צמיחת תמ"ג | Strong growth may prompt rate hikes |
| Geopolitical risk | סיכון גיאופוליטי | Security situation affects policy |

Analyzing rate decisions:
```python
# Get historical BOI rate decisions
rates = fetch_boi_rates.get_interest_history(
    start_date="2020-01-01",
    end_date="2024-12-31"
)
# Typical output: list of (date, rate) tuples
# e.g., [("2024-01-01", 4.50), ("2024-04-08", 4.50), ...]
```

### Step 5: Calculate CPI and Inflation
CPI (Madad HaMechirim LaTzarchan) data from CBS:

| Component | Hebrew | Weight (approx.) | Notes |
|-----------|--------|-------------------|-------|
| Housing | דיור | ~25% | Largest component, includes rent |
| Food | מזון | ~17% | Volatile, seasonal effects |
| Transportation | תחבורה | ~16% | Fuel prices, public transit |
| Education | חינוך | ~8% | Tuition, school supplies |
| Health | בריאות | ~6% | Copays, medications |
| Clothing | הלבשה | ~4% | Seasonal patterns |

CPI-based calculations:
```python
# Inflation-adjusted value calculation
def adjust_for_inflation(amount, from_date, to_date, cpi_data):
    """Adjust NIS amount for inflation using CPI.
    
    Common uses:
    - Rental agreements (tiu'um madad)
    - Alimony adjustments
    - Contract escalation clauses
    - Tax bracket adjustments
    """
    from_cpi = cpi_data[from_date]
    to_cpi = cpi_data[to_date]
    return amount * (to_cpi / from_cpi)
```

### Step 6: Generate Reports and Visualizations
Compile findings into actionable reports:
1. **Rate summary:** Current BOI rate, last change date, next decision date
2. **Exchange rate trends:** 30/90/365 day trends for requested currencies
3. **CPI analysis:** Current inflation rate, component breakdown, forecast implications
4. **Comparison:** Israeli rates vs. major economies (US Fed, ECB)
5. **Context:** Explain impact on mortgages (mashkantaot), savings, business costs

## Examples

### Example 1: Current Exchange Rate Lookup
User says: "What is today's dollar exchange rate?"
Actions:
1. Run `python scripts/fetch_boi_rates.py --rate USD`
2. Return current representative rate (sha'ar yatzig)
3. Show 30-day trend for context
4. Note: Rate published at 15:30, before that yesterday's rate applies
Result: Current USD/ILS rate with trend context

### Example 2: BOI Interest Rate History
User says: "Show me BOI interest rate changes this year"
Actions:
1. Run `python scripts/fetch_boi_rates.py --interest --period 2024`
2. List all rate decisions with dates and changes
3. Add context: inflation at time of decision, global rate environment
4. Note next scheduled monetary committee meeting
Result: Interest rate timeline with economic context

### Example 3: CPI-Based Rent Adjustment
User says: "My rent is 5,000 NIS, adjust it for the last year's CPI change"
Actions:
1. Fetch CPI values for start and end months
2. Calculate: adjusted_rent = 5000 * (current_cpi / year_ago_cpi)
3. Show: percentage change and new rent amount
4. Note: Standard Israeli rental contracts use "hatzamada lamadad" (CPI linkage)
Result: Adjusted rent amount with CPI calculation breakdown

### Example 4: Multi-Currency Rate Comparison
User says: "Compare USD, EUR, and GBP rates over the last 3 months"
Actions:
1. Run `python scripts/fetch_boi_rates.py --rate USD EUR GBP --period 90d`
2. Display rates in table format with dates
3. Calculate percentage changes over the period
4. Note any significant BOI interventions or events affecting rates
Result: Multi-currency comparison table with trends

## Bundled Resources

### Scripts
- `scripts/fetch_boi_rates.py` -- Fetches Bank of Israel data: exchange rates (sha'ar yatzig), interest rates, and historical series. Run: `python scripts/fetch_boi_rates.py --help`

### References
- `references/boi-api.md` -- Bank of Israel API endpoints, data formats, series identifiers, and query parameters. Consult when building integrations with BOI data services.

## Troubleshooting

### Error: "BOI API rate not available"
Cause: Querying rate before daily publication time (15:30 IST) or on Shabbat/holiday
Solution: Before 15:30, use previous day's rate. On weekends/holidays, last business day rate applies. Check Israeli holiday calendar.

### Error: "CPI data not yet published"
Cause: CBS publishes CPI around the 15th of the following month
Solution: For the most recent month, data may not be available yet. Use previous month's data and note the expected publication date.

### Error: "Exchange rate mismatch between sources"
Cause: Different sources report different rates (bank rate vs. BOI representative rate)
Solution: Always use BOI representative rate (sha'ar yatzig) for official calculations. Commercial bank rates include spreads and differ from the representative rate.

### Error: "Historical data series gap"
Cause: BOI API may have gaps during system transitions or data restructuring
Solution: For older data (pre-2000), check BOI statistical publications. For recent gaps, try alternative date ranges or contact BOI data services.
