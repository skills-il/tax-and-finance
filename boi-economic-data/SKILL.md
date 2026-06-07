---
name: boi-economic-data
description: "Fetch and analyze Bank of Israel (BOI) economic data: interest rates, CPI (madad hamchirim), exchange rates (sha'ar yatzig), and CBS statistics. Use when user asks about BOI interest rate, ribit Bank Israel, exchange rates, sha'ar yatzig, CPI index, madad, inflation data, or Israeli economic indicators. Foundation skill for Israeli financial analytics. Provides API access to the BOI SDMX API at edge.boi.gov.il and CBS data. Do NOT use for stock market data (use tase-stock-analysis instead) or for currency conversion (use shekel-currency-converter instead)."
license: MIT
compatibility: "Requires network access for Bank of Israel API. Works with Claude Code, Cursor, GitHub Copilot, Windsurf, OpenCode, Codex."
version: 1.2.0
---

# BOI Economic Data

## Instructions

### Step 1: Identify the Data Type
Ask the user what economic data they need:

| Data Type | Hebrew | Source | Update Frequency |
|-----------|--------|--------|-----------------|
| Interest rate | ריבית בנק ישראל | BOI Monetary Committee | Announced ~6 times/year |
| Exchange rates | שערי חליפין (שער יציג) | BOI | Daily (published ~15:30) |
| CPI (Consumer Price Index) | מדד המחירים לצרכן | CBS (Lishkat HaStatistika) | Monthly (around 15th of following month) |
| Inflation expectations | ציפיות אינפלציה | BOI | Monthly |
| Government bonds yield | תשואת אג"ח ממשלתי | BOI / TASE | Daily |
| Monetary aggregates | אגרגטים מוניטריים | BOI | Monthly |

### Step 2: Fetch Data from BOI API
The Bank of Israel serves public data from its "new series database" (Fusion Edge Server) using the SDMX 2.1 REST API. The working data path is `https://edge.boi.gov.il/FusionEdgeServer/ws/public/sdmxapi/rest/data/{DATAFLOW}/{series}` (the older `sdmx/v2/data/dataflow/BOI/...` path returns 404). The API returns SDMX-XML; observations come as `<Obs TIME_PERIOD="..." OBS_VALUE="..."/>` elements. The server rejects the default urllib User-Agent, so send a normal browser User-Agent. The canonical endpoint reference is `references/boi-api.md`.

**Exchange Rates (Sha'ar Yatzig):** representative rates live in the `EXR` dataflow as per-currency series `RER_<CUR>_ILS` (e.g. `RER_USD_ILS`, `RER_EUR_ILS`):
```
GET https://edge.boi.gov.il/FusionEdgeServer/ws/public/sdmxapi/rest/data/EXR/RER_USD_ILS?startPeriod={date}&endPeriod={date}
```

**Interest Rate:** the Bank of Israel rate data lives in the `BIR` dataflow:
```
GET https://edge.boi.gov.il/FusionEdgeServer/ws/public/sdmxapi/rest/data/BIR/?startPeriod={date}&endPeriod={date}
```
For the headline policy-rate value the most reliable source is the Monetary Committee decision (see the press-release / monetary-policy links in Reference Links). Use `scripts/fetch_boi_rates.py` for simplified data fetching.

### Step 3: Process Exchange Rate Data
BOI publishes representative exchange rates (sha'ar yatzig) daily:

| Currency | Code | Typical Use |
|----------|------|-------------|
| US Dollar | USD | Primary foreign currency, investment pricing |
| Euro | EUR | EU trade, travel |
| British Pound | GBP | UK trade |
| Japanese Yen | JPY | Per 100 JPY |
| Swiss Franc | CHF | Safe haven |

Key points:
- Representative rate published once daily at approximately 15:30
- Used as official rate for tax calculations, contracts, financial reporting
- Weekend and holiday rates use last published rate
- For intraday rates, use forex platforms (BOI rate is indicative)

### Step 4: Analyze CPI Data
The Consumer Price Index (Madad HaMchirim LaTzarchan) from CBS:

| CPI Component | Hebrew | Weight (approx) | Notes |
|---------------|--------|-----------------|-------|
| Housing | דיור | ~25% | Rent component (not home prices) |
| Food | מזון | ~17% | Including dining out |
| Transportation | תחבורה | ~17% | Fuel, public transit, vehicles |
| Education & culture | חינוך ותרבות | ~11% | Tuition, books, entertainment |
| Health | בריאות | ~6% | Medical services, medications |
| Clothing | הלבשה והנעלה | ~3% | Seasonal adjustments |

CPI uses:
- **CPI-linked bonds (Galil):** Index-linked government bonds adjust by CPI
- **Rent adjustments:** Many Israeli leases are CPI-linked (tzmud madad)
- **Tax brackets:** Updated annually by CPI
- **Alimony and legal judgments:** Often CPI-linked

Note: CBS publication schedule may vary. CPI data is typically published around the 15th of the following month, but verify current CBS publication schedules.

### Step 5: Track Interest Rate Decisions
BOI Monetary Committee sets the interest rate:

| Rate Level | Typical Context | Impact |
|------------|----------------|--------|
| Rising | Inflation above target (1-3%) | Higher mortgage rates, stronger NIS |
| Stable | Inflation within target | Predictable borrowing costs |
| Falling | Low inflation or economic slowdown | Lower mortgage rates, weaker NIS |

Historical context helps interpret current decisions. Use `scripts/fetch_boi_rates.py --interest-history` for recent rate changes.

### Step 6: Combine Data for Analysis
Cross-reference multiple data points for comprehensive analysis:
1. **Mortgage planning:** Interest rate + CPI trend + exchange rate outlook
2. **Business planning:** Exchange rate + CPI for cost projections
3. **Investment analysis:** Bond yields + inflation expectations
4. **Import/export pricing:** Exchange rates + CPI for contract negotiations

## Examples

### Example 1: Current Exchange Rate
User says: "What is today's dollar-shekel exchange rate?"
Actions:
1. Run `python scripts/fetch_boi_rates.py --currency USD`
2. Display representative rate (sha'ar yatzig) with date
3. Note: Rate published at approximately 15:30, before that yesterday's rate applies
Result: Current USD/NIS representative rate with context

### Example 2: Interest Rate Impact
User says: "What is the current BOI interest rate and how does it affect mortgages?"
Actions:
1. Run `python scripts/fetch_boi_rates.py --interest`
2. Show current rate and recent history
3. Explain: Variable-rate mortgages (mashkanta priim) directly affected
4. Note: Fixed-rate mortgages set at time of signing, not affected by changes
Result: Interest rate with mortgage impact analysis

### Example 3: CPI Trend for Rent Adjustment
User says: "My lease says rent adjusts by CPI. How much did it go up?"
Actions:
1. Determine: Lease start date and adjustment period
2. Fetch: CPI values for start and current period
3. Calculate: Percentage change = (CPI_current - CPI_base) / CPI_base * 100
4. Apply: New rent = original_rent * (1 + percentage_change / 100)
Result: Exact CPI adjustment with new rent calculation

## Bundled Resources

### Scripts
- `scripts/fetch_boi_rates.py` -- Fetches Bank of Israel data: exchange rates, interest rates, and CPI. Run: `python scripts/fetch_boi_rates.py --help`

### References
- `references/boi-api.md` -- Bank of Israel API endpoints (SDMX format), authentication, rate limits, and data structure. Consult when building integrations or troubleshooting API calls.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| BOI Statistical Information | https://www.boi.org.il/en/economic-roles/statistical-information/ | Official portal for interest rates, exchange rates, monetary aggregates |
| BOI SDMX data API root | https://edge.boi.gov.il/FusionEdgeServer/ws/public/sdmxapi/rest/data/ | Live data path used by `scripts/fetch_boi_rates.py` (append `EXR/RER_USD_ILS`, `BIR/`, `PRI/`) |
| BOI Press Releases | https://www.boi.org.il/en/communication-and-publications/press-releases/ | Most recent Monetary Committee rate decisions and accompanying minutes |
| CBS Consumer Price Index | https://www.cbs.gov.il/en/subjects/Pages/Consumer-Price-Index.aspx | Current monthly CPI release schedule, historical index, weighting structure |

## Gotchas
- Agents often query BOI exchange rates for Friday or Saturday, but the representative rate (sha'ar yatzig) is only published on business days (Sunday-Thursday). Use the last available Thursday rate for weekends.
- The BOI SDMX API returns XML by default, not JSON. Agents must either parse XML or add the correct Accept header for JSON format.
- Agents may confuse the BOI representative rate (indicative, published once daily at approximately 15:30) with real-time forex rates. The BOI rate is not suitable for intraday trading decisions.
- CPI data from CBS lags by about 6 weeks: January's CPI is published around February 15th. Agents may try to fetch current-month CPI that does not exist yet.

## Troubleshooting

### Error: "BOI API returned empty data"
Cause: Querying for weekend/holiday date when no rate was published
Solution: BOI publishes rates on business days only (Sunday-Thursday). For Friday/Saturday, use the last published rate (Thursday). Use the API date range query to get the most recent available rate.

### Error: "CPI data not yet available"
Cause: CBS publishes CPI around the 15th of the following month
Solution: If current month's CPI is not available, use the latest published index. Check CBS publication calendar for exact release dates.

### Error: "Exchange rate seems stale"
Cause: Using representative rate before daily publication time
Solution: BOI representative rate is published at approximately 15:30 Israel time. Before that, the previous day's rate is the official rate. For intraday indicative rates, use bank or forex feeds.