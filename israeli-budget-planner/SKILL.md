---
name: israeli-budget-planner
description: Not tax, pension or investment advice, and not a mortgage approval. Plan household and personal budgets with Israeli-specific costs, rates, and financial products. Use when user asks about budgeting in Israel, mortgage (mashkanta) calculations, arnona rates, cost of living, takciv, or monthly expense planning. Covers Bank of Israel prime rate, mashkanta tracks, arnona, household health costs (mas briut / health-tax), and Israeli household benchmarks.
license: MIT
compatibility: Works with Claude Code, Cursor, GitHub Copilot, Windsurf, OpenCode, Codex, Antigravity, Gemini CLI.
---

# Israeli Budget Planner

## Legal notice
This is a free information tool operated by an artificial-intelligence model. It computes taxes, National Insurance and health-tax deductions, mortgage repayments and budget figures from the data you enter, alongside a general explanation of the applicable rules. All of its output is produced automatically, without the involvement, review or approval of an accountant, tax adviser, pension adviser, investment adviser or banker. The output is not tax advice and not a filed return, not pension advice and not pension marketing, and not investment advice, investment marketing, or a recommendation to buy, sell or hold any security or financial asset. It is a raw budgeting indication only.

Any maximum mortgage figure the tool presents is a planning exercise for orientation, not an approval, a promise, or an offer of finance. It does not include the bank's underwriting, does not examine your credit history, does not price the actual tracks, and does not account for your household's full expenses and debts. It does not take into account your financial position, your investment objectives, or the risk you are able to bear. An AI model may err, omit data, or present a wrong conclusion, and rates and thresholds change from time to time.

Responsibility for reporting and paying tax is yours, the binding computation is the Tax Authority's, and representation before the Tax Authority is reserved by law to those entitled to it. Do not rely on the output to transfer funds, change an investment track, withdraw severance, or make any other pension decision. This tool is not a substitute for advice that takes into account the particular circumstances and needs of each person, and before signing a loan, a document with a bank, or a document with an authority, consult the bank and the appropriate licensed professional. All use of the output is at the user's sole responsibility.

## Key Financial Rates
| Rate | Value (Reference) |
|------|-------------------|
| BOI Interest Rate | 3.50%, lowered 6 Jul 2026. Next rate decision 1 Sep 2026, so re-verify at boi.org.il before quoting |
| Prime Rate | BOI + 1.50% = ~5.00% |
| VAT (Ma'am) | 18% |
| Minimum Wage | 6,443.85 NIS/month (35.40 NIS/hr), from 1 Apr 2026 |
| Average Wage | 13,566 NIS/month under section 1 (drives benefits and minimum wage); 13,769 NIS/month under section 2 (the basis for insurance-contribution ceilings). Pick per use |

## Mashkanta (Mortgage) Tracks
| Track | Rate Type | Indicative range |
|-------|-----------|-------|
| Prime-linked | Variable | Prime +/- 0.5% |
| Fixed unlinked | Fixed | 4.5%-6.5% |
| CPI-linked fixed | Fixed + CPI | 3.0%-5.0% + CPI |
| CPI-linked variable | Resets every 5 yrs | 2.5%-4.5% + CPI |

The ranges above are indicative market levels for orientation, not published or regulated figures; price the actual tracks with the bank.

BOI rules (Proper Conduct of Banking Business directives on housing loans): Max LTV 75% first (only) home, 70% replacement apartment (dira chalifit), 50% investment. Mix rule: at least 1/3 of the total loan must be in a FIXED-interest track; up to 2/3 may be variable. The fixed third does NOT have to be unlinked, a CPI-linked fixed track satisfies it too, which is often the cheaper way to meet the rule. Maximum term: 30 years on any track.

## Arnona (Municipal Property Tax)
Arnona is set by each municipality and updated annually, so per-city numbers go stale fast. Do not rely on a static table. Fetch the city's current-year arnona order (tzav arnona, 2026) from the municipality's website (or via the israeli-cbs MCP for indices). Rates are quoted per square meter and vary by zone and property classification.

Illustrative only: a mid-size Tel Aviv residential property may run roughly 500-1,500 NIS/month depending on size and zone (2026, verify with the municipality).

## Payroll Deductions: Bituach Leumi + Health-Tax (Employee)
Both are withheld together. Two thresholds apply to everyone: the reduced-collection step at 7,703 NIS/month (from 1 Jan 2026) and the maximum insurable income of 51,910 NIS/month (from 1 Jan 2026). Salary above the ceiling is not charged at all, so a high earner budgeting by hand must cap these deductions there.

**The employee rate is NOT one number.** It varies by age and pension status, and the default row applies only to a resident aged 18 to retirement age. Budgeting a working pensioner or a working teenager at the default rates overstates their deductions by the entire amount. Combined employee rates (Bituach Leumi + health-tax), per the Bituach Leumi rate table:

| Employee category | Reduced band (to 7,703) | Full band (7,703 to 51,910) |
|---|---|---|
| Resident aged 18 to retirement age (default) | 4.27% (1.04% BL + 3.23% health) | 12.17% (7% BL + 5.17% health) |
| Under 18 | 0% | 0% |
| Receiving old-age pension (kitzvat ezrach vatik) | 0% | 0% |
| Receiving disability pension, with annual BL approval | 3.23% (health only, BL 0%) | 5.17% (health only, BL 0%) |
| Aged 67 to 70, not receiving old-age pension | 3.93% | 10.03% |
| Woman between retirement age and the male retirement age, not receiving a pension | 3.95% | 10.24% |
| Controlling shareholder in a close company (baal shlita) | 4.25% | 11.96% |
| First became resident after age 62, below retirement age | 3.6% | 7.45% |

The percentages themselves did not change for 2026 (they carry 2025 effective dates); only the two thresholds did. Employer contributions are separate and are not deducted from the employee.

Also budget kupat cholim supplemental insurance (bituach mashlim, e.g. Maccabi Zahav / Clalit Mushlam): an optional monthly line on top of the basic health basket (sal briut) that these taxes already fund.

`scripts/budget_calculator.py --category` applies the correct row; it defaults to the resident-18-to-retirement row.

### What the net-pay estimate does NOT include
The calculator models a salaried employee with ONE employer. It is not a payslip. Before using its net figure for affordability, correct for:
- **Credit points for children.** Parents are entitled to additional credit points per child beyond the 2.25 resident base, and for a family this is usually the largest single correction. Look up the current entitlement for each parent and pass the real total via `--credit-points`. Omitting it overstates tax by hundreds of shekels a month.
- **The tax credit on the employee's own pension contribution.** The calculator taxes gross and then subtracts pension as cash, so its income-tax line is conservative (too high).
- **Keren hishtalmut**, if the employee has one: the employee's share is deducted from take-home before the money is saved, so do not budget it twice.
- **A second employer.** With two jobs the reduced band and the credit points cannot both be claimed twice: the secondary employer withholds at the full band and the top tax rate until a tiaum (both tiaum dmei bituach and tiaum mas) is filed. Running each job separately through the tool overstates combined net pay and can produce a year-end tax bill.
- **Taxable benefits added to salary**, such as a company car (shovi shimush), which raise taxable income above gross.
- **The self-employed are out of scope.** An osek patur or osek murshe pays different Bituach Leumi and health rates, has deductible expenses and mikdamot, and must not be run through `--salary`. Route them to a self-employed skill.

## Surtax (Mas Yesef)
The top of the bracket table hides a surtax, and it is easy to miss because it is not an ordinary bracket:
- The 50% top row above 721,560 NIS/year (60,130 NIS/month) is the 47% bracket plus a 3% surtax. The Tax Authority's own bracket table stops at 47%, so a budget built from that table alone understates the marginal rate for a high earner.
- Since 2025 a further 2% applies to high income that is NOT from employment or a business, taking the top rate on that income to 52%. A household with significant investment or rental income should budget for this separately from salary.

## Monthly Budget Template (Couple + 1 Child)
These are this skill's own planning heuristics for orientation, not published CBS survey figures. For real distributions use the CBS household expenditure survey.
- Housing: 4,000-8,000 (25-35%)
- Food: 2,500-4,500 (15-25%)
- Education: 1,500-3,500 (8-15%)
- Transportation: 500-1,500 (3-8%)
- Arnona: 400-800 (3-5%)

## Household Benefits (Income Side)
A budget must count recurring inflows, not just expenses:
- **Child allowance (kitzvat yeladim):** Bituach Leumi pays a monthly allowance per child; the total rises with the number of children. It lands automatically in the parent's account and should be added to household income (check btl.gov.il for the current per-child figure).
- **Subsidized daycare (ma'on / mishpachton):** working parents may qualify for a means-tested ma'on subsidy that sharply cuts the childcare line, one of the largest young-family costs. Check eligibility and the subsidy tier via the Economy Ministry's ma'onot-yom system before budgeting full-price daycare.
- **Work grant (ma'anak avoda / negative income tax):** lower-income working households (employees and self-employed) may be entitled to an annual work grant paid by the Tax Authority. Check eligibility at the tax authority; it is a recurring income-side inflow like the two above.

## Savings Vehicles
- Keren Pensia: contributions attract tax relief and the money is locked until retirement age
- Keren Hishtalmut: the main Israeli medium-term vehicle; withdrawals become available after six years, with tax advantages subject to statutory ceilings
- Kupat Gemel: comes in distinct forms with different rules, including a kupat gemel le'kitzba locked to retirement age and a kupat gemel le'hashkaa that is withdrawable at any time. Confirm which form is on offer and its exact tax treatment with the provider or the tax authority before budgeting around it
- Emergency fund: hold 3-6 months of essential expenses in an accessible account before locking money into any of the above. The locked vehicles are tax-efficient precisely because you cannot reach them in a bad month.

## Examples

### Example 1: Create a Monthly Household Budget
User says: "Help me plan a monthly budget for a family in Tel Aviv"
Actions:
1. Input gross salary, calculate net after tax (brackets: 10%-50%)
2. Deduct Bituach Leumi + health-tax at the row matching the person's age and pension status (default resident 18-to-retirement: 4.27% combined to 7,703, 12.17% above, capped at 51,910). Ask before assuming the default row. Then pension: the employee's statutory share is 6% (the 6.5% figure often quoted is the EMPLOYER's tagmulim leg, not a deduction from the employee)
3. Budget categories: rent/mortgage (30-40%), groceries (15%), transport (10%), utilities (8%), childcare
4. Include arnona estimate for Tel Aviv (fetch the municipality's current-year rate)
5. Savings target: keren hishtalmut + pension + emergency fund
Result: Complete monthly budget with Israeli-specific deductions and savings plan

### Example 2: Evaluate a Mashkanta (Mortgage) Option
User says: "Should I take a fixed or variable rate mortgage in Israel?"
Actions:
1. Compare mortgage tracks: Prime-linked, fixed (kvua), CPI-linked (tzamud madad)
2. Calculate a blended-track payment. A single prime-only run (e.g. the script default 5.00%) is illustrative and understates reality: at least 1/3 must sit in a fixed track, so compute 1/3 fixed plus 2/3 prime and sum, or label the single-rate result "prime-only, blended will be higher". The fixed third may be unlinked (4.5-6.5%) or CPI-linked fixed (3.0-5.0% plus CPI); price both, the linked option is usually cheaper on the headline rate but carries index risk
3. Apply Bank of Israel's PTI cap: a mortgage may not be taken where the monthly repayment exceeds 50% of disposable income (including the mortgage insurance and associated costs). That is the regulatory ceiling, not a target. Individual banks apply their own stricter underwriting below it, so ask the bank what ratio it will actually approve rather than planning to the legal maximum
4. Budget mortgage life insurance and structural insurance (bituach chaim / bituach mavne) as a recurring required cost, not a one-off: the bank may require both as a condition of the loan. The premium is individually underwritten, so get a quote rather than assuming a figure; early repayment, refinancing, or a change in personal or medical status can lower it later
5. Compare total cost over 15/20/25 year terms (30 years is the regulatory maximum)
Result: Mortgage comparison with monthly payments, the insurance line, and total cost per track

### Example 3: Work Out What Mortgage a Household Can Actually Afford
User says: "We earn 22,000 gross between us, how big a mortgage can we take?"
Actions:
1. Convert gross to net for each earner separately, using the Bituach Leumi row that matches each person's age and pension status, plus income tax after credit points (2.25 base, women 2.75) and the 6% employee pension share. Two earners at 11,000 each net far more than one earner at 22,000, because the brackets and the reduced band apply per person
2. Subtract committed non-housing debt (car loan, credit lines). What remains is disposable income for PTI purposes
3. Apply the PTI cap: monthly repayment must stay under 50% of disposable income. Plan well below that ceiling, since the ratio the bank will actually approve is set by its own underwriting and is stricter
4. Convert the affordable monthly payment back into a loan size at a blended rate, not the prime rate alone. Run `--mortgage` per track and sum
5. Check the result against the LTV cap: a 75% first-home LTV means the household still needs 25% in equity, and that equity requirement, not PTI, is the binding constraint for most first-time buyers. The 25% is not the whole cash requirement: purchase tax (mas rechisha), lawyer, broker, appraiser, registration and moving all fall outside the loan and are paid in cash at closing. Price them for the specific property before treating 25% as the target, or the household arrives at closing short
6. Add the recurring costs the payment excludes: mortgage life and structural insurance, arnona, va'ad bayit
Result: A maximum loan figure with the binding constraint named, plus the true monthly housing cost rather than the bare repayment

## Bundled Resources

### Scripts
- `scripts/budget_calculator.py` -- Calculates Israeli household budget including income tax, Bituach Leumi, health tax, pension deductions, and mashkanta payments. Run: `python scripts/budget_calculator.py --help`

### References
- `references/domain-checklist.md` -- The coverage contract this skill is audited against: what it must cover, what it should cover, and what is explicitly out of scope. Read it when deciding whether a question is in scope.
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
- Agents apply the headline 4.27%/12.17% Bituach Leumi and health-tax rates to everyone. They are the rates for a resident aged 18 to retirement age only. A working pensioner and an under-18 employee pay ZERO employee contributions, and a disability-pension recipient pays health-tax only. Ask for age and pension status before computing net pay.
- Agents treat 6.5% as an employee pension rate. The employee's statutory share is 6%; 6.5% is the employer's tagmulim contribution, and a further 6% employer severance leg brings the total to 18.5%. Deducting 6.5% from the employee understates net pay.
- The Hishtalmut fund (keren hishtalmut) is a unique Israeli savings vehicle with tax benefits. Agents unfamiliar with Israeli financial products may suggest generic savings accounts instead.

## Troubleshooting

### Error: "Tax calculation doesn't match pay slip"
Cause: Tax credits (nekudot zikui) not properly applied
Solution: Every Israeli resident gets 2.25 base credit points. Women get 0.5 additional (2.75 total). New immigrants get extra credits for 3.5 years. Each point is worth 242 NIS/month (2026; verify the current value with the tax authority). Apply credits before calculating tax. If the gap remains and the salary is high, check whether surtax (mas yesef) is in play: the pay slip may show 50% marginal rather than the 47% top bracket.

### Error: "Net pay is far higher on the pay slip than the calculator says"
Cause: the calculator used the default Bituach Leumi row for someone who is not in it (most often a working pensioner, an employee under 18, or a disability-pension recipient).
Solution: Re-run against the correct category row. A pensioner and an under-18 employee pay 0% employee Bituach Leumi AND 0% health-tax; a disability-pension recipient with annual approval pays health-tax only. Verified not to be a credit-point issue when the discrepancy is a clean 4.27% or 12.17% of gross, that shape points at the category row, not at credits.

### Error: "Arnona amount seems wrong"
Cause: Arnona varies significantly by city, zone, and property classification
Solution: Arnona is municipality-set and updated annually. Do not use a static table. Fetch the relevant municipality's current-year tzav arnona (2026) for the exact per-square-meter rate by zone and property class.
