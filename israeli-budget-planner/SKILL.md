---
name: israeli-budget-planner
description: Plan household and personal budgets with Israeli-specific costs, rates, and financial products. Use when user asks about budgeting in Israel, mortgage (mashkanta) calculations, arnona rates, cost of living, takciv, or monthly expense planning. Covers Bank of Israel prime rate, mashkanta tracks, arnona by city, Sal Briut costs, and Israeli household benchmarks.
license: MIT
compatibility: Works with Claude Code, Cursor, GitHub Copilot, Windsurf, OpenCode, Codex.
---

# Israeli Budget Planner

## Key Financial Rates
| Rate | Value (Reference) |
|------|-------------------|
| BOI Interest Rate | 4.50% (check boi.org.il) |
| Prime Rate | BOI + 1.50% = ~6.00% |
| VAT (Ma'am) | 18% |
| Minimum Wage | Verify current 2026 rate with government sources |
| Average Wage | ~12,500 NIS/month |

## Mashkanta (Mortgage) Tracks
| Track | Rate Type | Range |
|-------|-----------|-------|
| Prime-linked | Variable | Prime +/- 0.5% |
| Fixed unlinked | Fixed | 4.5%-6.5% |
| CPI-linked fixed | Fixed + CPI | 3.0%-5.0% + CPI |
| CPI-linked variable | Resets every 5 yrs | 2.5%-4.5% + CPI |

BOI rules: Max LTV 75% first home, max 33.33% variable rate, max 33.33% CPI-linked.

## Arnona by City (NIS/sqm/month, 2024 rates - verify current)
- Tel Aviv: 85-130
- Jerusalem: 55-80
- Haifa: 45-65
- Beer Sheva: 35-50
- Raanana: 70-95
- Herzliya: 75-100

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
2. Deduct Bituach Leumi (3.5%/12%), health tax (3.1%/5%), pension (6.5%)
3. Budget categories: rent/mortgage (30-40%), groceries (15%), transport (10%), utilities (8%), childcare
4. Include arnona estimate for Tel Aviv (varies by zone, ~500-1500 NIS/month)
5. Savings target: keren hishtalmut + pension + emergency fund
Result: Complete monthly budget with Israeli-specific deductions and savings plan

### Example 2: Evaluate a Mashkanta (Mortgage) Option
User says: "Should I take a fixed or variable rate mortgage in Israel?"
Actions:
1. Compare mortgage tracks: Prime-linked, fixed (kvua), CPI-linked (tzamud madad)
2. Calculate monthly payment for each track at current BOI rate
3. Apply Bank of Israel's PTI limit (max 40% of income)
4. Factor in life insurance and structural insurance requirements
5. Compare total cost over 15/20/25 year terms
Result: Mortgage comparison with monthly payments and total cost per track

## Bundled Resources

### Scripts
- `scripts/budget_calculator.py` -- Calculates Israeli household budget including income tax, Bituach Leumi, health tax, pension deductions, and mashkanta payments. Run: `python scripts/budget_calculator.py --help`

### References
- `references/israeli-financial-rates.md` -- Current BOI interest rates, mortgage guidelines, arnona rates by city, cost of living benchmarks, and savings vehicle comparisons. Consult when calculating specific financial figures or comparing options.

## Gotchas
- Agents often use US mortgage conventions (30-year fixed rate) for Israeli mortgages. Israeli mashkantaot use a mix of tracks (maslulim): Prime-linked, CPI-linked fixed, CPI-linked variable, and fixed-rate unlinked, with typical terms of 15-30 years.
- Bituach Leumi (National Insurance) deductions are mandatory for all Israeli workers and reduce take-home pay significantly. Agents may omit these from budget calculations, using gross salary as available income.
- Israeli rent is commonly quoted as monthly amounts excluding arnona and va'ad bayit (building maintenance). Agents may compare rents without accounting for these additional fixed costs that can add 500-2,000 NIS/month.
- The Hishtalmut fund (keren hishtalmut) is a unique Israeli savings vehicle with tax benefits. Agents unfamiliar with Israeli financial products may suggest generic savings accounts instead.

## Troubleshooting

### Error: "Tax calculation doesn't match pay slip"
Cause: Tax credits (nekudot zikui) not properly applied
Solution: Every Israeli resident gets 2.25 base credit points. Women get 0.5 additional. New immigrants get extra credits for 3.5 years. Each point is worth approximately 250 NIS/month (verify current 2026 rate). Apply credits before calculating tax.

### Error: "Arnona amount seems wrong"
Cause: Arnona varies significantly by city, zone, and property classification
Solution: Arnona is calculated per square meter and varies by municipality. Tel Aviv residential ranges from 45-120 NIS/sqm/year depending on zone. Check the specific municipality's rate table.