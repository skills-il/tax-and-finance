---
name: israeli-budget-planner
description: Plan household and personal budgets with Israeli-specific costs, rates, and financial products. Use when user asks about budgeting in Israel, mortgage (mashkanta) calculations, arnona rates, cost of living, takciv, or monthly expense planning. Covers Bank of Israel prime rate, mashkanta tracks, arnona, household health costs (mas briut / health-tax), and Israeli household benchmarks.
license: MIT
compatibility: Works with Claude Code, Cursor, GitHub Copilot, Windsurf, OpenCode, Codex.
version: 1.3.0
---

# Israeli Budget Planner

## Key Financial Rates
| Rate | Value (Reference) |
|------|-------------------|
| BOI Interest Rate | 3.75% (as of May 2026; verify at boi.org.il) |
| Prime Rate | BOI + 1.50% = ~5.25% |
| VAT (Ma'am) | 18% |
| Minimum Wage | 6,443.85 NIS/month (35.40 NIS/hr), from 1 Apr 2026 |
| Average Wage | ~13,566 NIS/month (Jan 2026) |

## Mashkanta (Mortgage) Tracks
| Track | Rate Type | Range |
|-------|-----------|-------|
| Prime-linked | Variable | Prime +/- 0.5% |
| Fixed unlinked | Fixed | 4.5%-6.5% |
| CPI-linked fixed | Fixed + CPI | 3.0%-5.0% + CPI |
| CPI-linked variable | Resets every 5 yrs | 2.5%-4.5% + CPI |

BOI rules: Max LTV 75% first home, 70% home replacement, 50% investment. Mix rule: a minimum of 1/3 must be fixed-unlinked; up to 2/3 may be variable/prime (the old 1/3-prime cap was removed in January 2021).

## Arnona (Municipal Property Tax)
Arnona is set by each municipality and updated annually, so per-city numbers go stale fast. Do not rely on a static table. Fetch the city's current-year arnona order (tzav arnona, 2026) from the municipality's website (or via the israeli-cbs MCP for indices). Rates are quoted per square meter and vary by zone and property classification.

Illustrative only: a mid-size Tel Aviv residential property may run roughly 500-1,500 NIS/month depending on size and zone (2026, verify with the municipality).

## Household Health Costs (Mas Briut / Health-Tax)
Israeli budgets must include the mandatory health-tax (mas briut / dmei briut) deducted from salary, plus optional supplemental insurance:
- Health-tax (employee, 2026): 3.23% of salary up to the reduced-collection step (7,703 NIS/month), 5.17% above it (deducted with Bituach Leumi).
- Kupat cholim supplemental insurance (bituach mashlim, e.g. Maccabi Zahav / Clalit Mushlam): an optional monthly budget line on top of the basic health basket (sal briut) that taxes already fund.
The `scripts/budget_calculator.py` script applies the 3.23% / 5.17% health-tax rates automatically.

## Monthly Budget Template (Couple + 1 Child)
- Housing: 4,000-8,000 (25-35%)
- Food: 2,500-4,500 (15-25%)
- Education: 1,500-3,500 (8-15%)
- Transportation: 500-1,500 (3-8%)
- Arnona: 400-800 (3-5%)

## Savings Vehicles
- Keren Pensia: Tax-deductible, locked until retirement
- Keren Hishtalmut: Tax-free after 6 years
- Kupat Gemel: Capital gains exempt, 6-year lock

## Examples

### Example 1: Create a Monthly Household Budget
User says: "Help me plan a monthly budget for a family in Tel Aviv"
Actions:
1. Input gross salary, calculate net after tax (brackets: 10%-50%)
2. Deduct Bituach Leumi employee rate (1.04% reduced / 7% full, split at 7,703 NIS/month), health tax (3.23% / 5.17%), pension (6% min, 6.5% common)
3. Budget categories: rent/mortgage (30-40%), groceries (15%), transport (10%), utilities (8%), childcare
4. Include arnona estimate for Tel Aviv (fetch the municipality's current-year rate)
5. Savings target: keren hishtalmut + pension + emergency fund
Result: Complete monthly budget with Israeli-specific deductions and savings plan

### Example 2: Evaluate a Mashkanta (Mortgage) Option
User says: "Should I take a fixed or variable rate mortgage in Israel?"
Actions:
1. Compare mortgage tracks: Prime-linked, fixed (kvua), CPI-linked (tzamud madad)
2. Calculate a blended-track payment. A single prime-only run (e.g. the script default 5.25%) is illustrative and understates reality: BOI rules force at least 1/3 fixed-unlinked (4.5-6.5%), so compute 1/3 fixed at ~5.5% plus 2/3 prime at 5.25% and sum, or label the single-rate result "prime-only, blended will be higher"
3. Apply Bank of Israel's PTI cap (max 50% of disposable income; banks usually decline above 40%)
4. Budget mandatory mortgage life insurance and structural insurance (bituach chaim / bituach mavne) as a recurring required cost (typically ~100-300 NIS/month, varies by loan size, age, and property), not just a one-off
5. Compare total cost over 15/20/25 year terms
Result: Mortgage comparison with monthly payments, the insurance line, and total cost per track

## Bundled Resources

### Scripts
- `scripts/budget_calculator.py` -- Calculates Israeli household budget including income tax, Bituach Leumi, health tax, pension deductions, and mashkanta payments. Run: `python scripts/budget_calculator.py --help`

### References
- `references/israeli-financial-rates.md` -- Current BOI interest rates, mortgage guidelines, arnona guidance, cost of living benchmarks, and savings vehicle comparisons. Consult when calculating specific financial figures or comparing options.

## Recommended MCP Servers

For live financial data, pair this skill with:

| MCP Server | What it provides | Install |
|------------|-----------------|---------|
| **boi-exchange** | Live Bank of Israel exchange rates and interest rate data | [Install](https://agentskills.co.il/en/mcp/boi-exchange) |
| **israeli-cbs** | Consumer Price Index (CPI), housing indices, and economic statistics from the Central Bureau of Statistics | [Install](https://agentskills.co.il/en/mcp/israeli-cbs) |
| **israel-statistics** | Additional CBS price indices and inflation-adjusted price calculations | [Install](https://agentskills.co.il/en/mcp/israel-statistics) |
| **il-budget** | Israeli government budget data, procurement contracts, and support payment information | [Install](https://agentskills.co.il/en/mcp/il-budget) |
| **budgetkey** | Comprehensive Israeli State Budget data (1997-2025) with full SQL query support | [Install](https://agentskills.co.il/en/mcp/budgetkey) |

When these MCPs are available, use them for real-time rates and indices instead of the static reference tables above.

## Reference Links
| Source | What it covers | URL |
|--------|----------------|-----|
| Bank of Israel | Interest rate, prime, monetary policy | https://www.boi.org.il |
| Central Bureau of Statistics | CPI, housing indices, average wage | https://www.cbs.gov.il |
| Kol Zchut | Mortgage rules, minimum wage, credit points | https://www.kolzchut.org.il |
| Israel Tax Authority | Income tax brackets, VAT, credit points | https://www.gov.il/taxes |

## Gotchas
- Agents often use US mortgage conventions (30-year fixed rate) for Israeli mortgages. Israeli mashkantaot use a mix of tracks (maslulim): Prime-linked, CPI-linked fixed, CPI-linked variable, and fixed-rate unlinked, with typical terms of 15-30 years.
- Bituach Leumi (National Insurance) deductions are mandatory for all Israeli workers and reduce take-home pay significantly. Agents may omit these from budget calculations, using gross salary as available income.
- Israeli rent is commonly quoted as monthly amounts excluding arnona and va'ad bayit (building maintenance). Agents may compare rents without accounting for these additional fixed costs that can add 500-2,000 NIS/month.
- The Hishtalmut fund (keren hishtalmut) is a unique Israeli savings vehicle with tax benefits. Agents unfamiliar with Israeli financial products may suggest generic savings accounts instead.

## Troubleshooting

### Error: "Tax calculation doesn't match pay slip"
Cause: Tax credits (nekudot zikui) not properly applied
Solution: Every Israeli resident gets 2.25 base credit points. Women get 0.5 additional. New immigrants get extra credits for 3.5 years. Each point is worth 242 NIS/month (2026; verify current value with the tax authority). Apply credits before calculating tax.

### Error: "Arnona amount seems wrong"
Cause: Arnona varies significantly by city, zone, and property classification
Solution: Arnona is municipality-set and updated annually. Do not use a static table. Fetch the relevant municipality's current-year tzav arnona (2026) for the exact per-square-meter rate by zone and property class.
