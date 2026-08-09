---
name: israeli-stock-options-tax
description: "Calculate tax on stock options and RSUs for Israeli tech employees under Section 102. Use when user asks about option exercise tax, RSU taxation, startup exit proceeds, Section 102 tracks, trustee holding period, capital gains vs income track comparison, or 'how much tax on my options'. Walks through a detailed tax breakdown with net proceeds. Do NOT use for crypto tax (use israeli-crypto-tax-reporter), ESOP plan setup (use israeli-startup-toolkit), controlling shareholder profit extraction (use israeli-corporate-tax-strategy), annual tax returns (use israeli-tax-returns), or payroll (use israeli-payroll-calculator)."
license: MIT
---

# Israeli Stock Options Tax Calculator

## Legal notice

This is a free information tool operated by an AI model. It explains the tax rules and helps you organise your own figures. All of its outputs are produced automatically by an AI model, with no involvement, review, or approval by a tax adviser or accountant. The output is not a tax opinion, not a return prepared by a licensed representative, and not professional advice, but a general calculation and explanation only: it does not examine the full extent of your income or your complete documents. An AI model may err, omit data, or present a wrong conclusion.

Any form or text this tool produces is an automatic draft for your personal preparation only, and is not a filed return. Responsibility for reporting and for paying the tax is yours, the binding computation is the Tax Authority's, and representation before the Tax Authority is reserved to those permitted by law. This tool is not a substitute for advice that takes account of the particular circumstances and needs of each person. Consult a tax adviser or accountant before filing or paying. All use of its output is the user's sole responsibility.


## Problem

Israeli tech employees receive stock options or RSUs as a significant part of their compensation, but most have no idea how much tax they will actually pay when they exercise or sell. The rules under Section 102 are complex: different tracks (capital gains vs income), a 24-month trustee holding period, surtax thresholds, and Bituach Leumi interactions all affect the final number. Getting it wrong can mean paying tens of thousands of shekels more than necessary, or worse, facing unexpected tax bills at exit.

## Instructions

### Step 1: Identify the Grant Type

Ask the user what type of equity they hold:

| Grant Type | How It Works | Common In |
|------------|-------------|-----------|
| Stock options (ISOs) | Right to buy shares at a fixed strike price | Private startups |
| RSUs (Restricted Stock Units) | Promise to receive shares upon vesting, no strike price | Public companies, late-stage startups |
| Restricted shares | Actual shares with vesting restrictions | Founders, early employees |

Also determine:
- **Grant date** (affects 24-month clock)
- **Exercise price / strike price** (for options; 0 for RSUs)
- **Fair market value (FMV) at grant date** (critical for RSU split calculation)
- **Current FMV or expected exit price** (for tax modeling)
- **Number of shares/options**
- **Vesting schedule** (standard: 4 years with 1-year cliff)

### Step 2: Determine the Tax Track

Section 102 of the Israeli Income Tax Ordinance (Pkudat Mas Hachnasa) offers several paths. The track is chosen by the COMPANY when setting up the ESOP plan. Employees cannot choose their track after the fact.

| Track | Tax Rate | Holding Period | Employer Deduction | When Used |
|-------|----------|---------------|-------------------|-----------|
| **102 Capital Gains (Honi)** | 25% flat on entire gain | 24 months from grant via trustee | No | Most common. Best for employees |
| **102 Income (Peiroti)** | Marginal rate (up to 47%) | 24 months from grant via trustee | Yes | Rarely chosen. Benefits employer |
| **102 Non-Trustee** | Marginal rate (up to 47%) | None | Yes | Uncommon. No trustee required |
| **3(i) (non-102)** | Marginal rate (up to 47%) | None | Yes | Foreign companies without 102 plan, non-compliant plans |

**Key questions to determine the track:**
- Does the company have an approved Section 102 plan filed with the ITA? If no, it is 3(i).
- Is a trustee (ne'eman) holding the options/shares? If no trustee, it is 102 Non-Trustee or 3(i).
- Which track did the company elect: capital gains (honi) or income (peiroti)? Check the grant letter or ask HR.

**The 24-month rule:** Under both 102 trustee tracks, the trustee must hold the options AND the exercised shares for at least 24 months counted from the END OF THE TAX YEAR in which the options were granted. If the employee sells before that period ends, the entire gain is taxed as employment income at marginal rates. This is the most expensive mistake an employee can make.

**Correction for a common misconception:** The 24-month clock does NOT run from the grant date itself, the vesting date, or the exercise date. It runs from the end of the tax year of grant (December 31 of the grant year). If options were granted on March 15, 2024, the clock starts December 31, 2024, so the earliest sale date for capital gains treatment is December 31, 2026, not March 15, 2026.

### Step 3: Calculate Tax per Track

#### Track A: Section 102 Capital Gains (Honi)

This is the most favorable track for employees. The entire gain is taxed at 25% flat (or 30% for controlling shareholders with 10%+ holdings).

```
Gain = Sale Price - Exercise Price
Tax = Gain x 25%
Surtax = (only if total annual income > 721,560 NIS)
  - 3% surtax on all income above threshold
  - 2% additional surtax on capital income above threshold
  - Total surtax rate: 5% on capital gains above threshold
Net = Sale Price - Exercise Price - Tax - Surtax
```

No Bituach Leumi applies on the capital gains track.

**Controlling shareholder exception:** If the employee holds (or held at any point) 10% or more of the company's shares, the capital gains rate is 30% instead of 25%.

**Publicly-traded company exception (Section 102(b)(3)) - critical for RSU holders at public companies:** The "entire gain at 25%" rule holds only when the company is PRIVATE at the date of grant (the typical startup-M&A exit). If the company's shares are LISTED on a stock exchange at grant, OR the shares are registered for trading on an exchange within 90 days AFTER the grant (the classic late-stage-startup-grant-shortly-before-IPO case), the capital gains track still applies but the gain is mandatorily SPLIT even here: the ordinary-income component, equal to the average closing share price over the 30 trading days PRECEDING the grant date minus any exercise price paid, is taxed as employment income at marginal rates (up to 47%) plus Bituach Leumi, health, and surtax; only the gain ABOVE that grant-date average is taxed at 25%. This is the common case for employees at Google, Meta, Nvidia, Microsoft, Intel, any post-IPO company, and anyone granted in the 90 days before an IPO, so do not tell such a holder they pay a flat 25% on the whole amount.

#### Track B: Section 102 Income (Peiroti)

The gain is split into two parts:

```
Employment Income = FMV at exercise date - Exercise Price
Capital Gain = Sale Price - FMV at exercise date

Tax on Employment Income = Marginal income tax rate (10%-47%)
  + Bituach Leumi (up to 7% employee share)
  + Health Insurance (up to ~5.17%)

Tax on Capital Gain = 25% flat

Surtax: 3% on all income above 721,560 NIS/year
  + 2% on capital income above 721,560 NIS/year
```

#### Track C: Section 3(i) / Non-102

Entire gain taxed as employment income at marginal rates. No capital gains portion.

```
Gain = Sale Price - Exercise Price
Tax = Marginal income tax (10%-47%)
  + Bituach Leumi (up to 7%)
  + Health Insurance (up to ~5.17%)
  + 3% surtax if above threshold
```

#### RSU-Specific Calculation

RSUs under Section 102 capital gains track are taxed identically to options, but with exercise price = 0:

```
Gain = Sale Price - 0 = Sale Price (entire value is gain)
Tax = Gain x 25%
```

For RSUs there is a split in two DIFFERENT situations, measured on two DIFFERENT bases:

```
Income (peiroti) track, any company:
  Employment Income = FMV at exercise/vesting date - Exercise Price
  Capital Gain      = Sale Price - FMV at exercise/vesting date

Capital gains track, LISTED company (Section 102(b)(3)):
  Employment Income = avg closing price over the 30 TRADING DAYS
                      PRECEDING the GRANT date - Exercise Price
  Capital Gain      = Sale Price - that grant-date average (taxed at 25%)
```

Do not use the vesting-date FMV for the listed-company capital-track split, it is the 30-trading-day pre-grant average.

### Step 4: Income Tax Brackets (2026)

When calculating marginal tax on the employment income portion (income track, non-trustee, or 3(i)):

| Monthly Income (NIS) | Annual (NIS) | Rate |
|----------------------|-------------|------|
| Up to 7,010 | Up to 84,120 | 10% |
| 7,011 - 10,060 | 84,121 - 120,720 | 14% |
| 10,061 - 19,000 | 120,721 - 228,000 | 20% |
| 19,001 - 25,100 | 228,001 - 301,200 | 31% |
| 25,101 - 46,690 | 301,201 - 560,280 | 35% |
| 46,691 - 60,130 | 560,281 - 721,560 | 47% |

Plus 3% surtax on annual income above 721,560 NIS (total top rate: 50%).

**Important:** Stock option income from a single exit event is added to the employee's annual salary. If an employee earns 30,000 NIS/month salary and exercises options with 500,000 NIS gain under the income track, their total annual income becomes 860,000 NIS, pushing them into surtax territory.

### Step 5: Bituach Leumi on Employment Income Portion

Bituach Leumi (National Insurance) and health tax apply ONLY to the employment income portion (income track, non-trustee, 3(i)). They do NOT apply to capital gains track.

| Component | Reduced Rate (up to 7,703/month) | Full Rate (7,703-51,910/month) |
|-----------|----------------------------------|-------------------------------|
| Bituach Leumi (employee) | 1.04% | 7.0% |
| Health Insurance (employee) | 3.23% | 5.17% |
| **Total employee** | **4.27%** | **12.17%** |

Maximum monthly ceiling: 51,910 NIS (2026). Income above this ceiling does not incur additional BL/health contributions. These employee rates (reduced-tier total 4.27%, full-tier total 12.17%) reflect the temporary order in force for 2025-2026 and apply to a resident employee aged 18 to retirement. For a lump-sum option exercise, the employment income portion is spread over the vesting period for BL calculation purposes.

### Step 6: Generate the Tax Comparison Report

Always produce a side-by-side comparison to show the employee the difference between tracks. Use this format:

```
=== STOCK OPTIONS TAX BREAKDOWN ===
Employee: [name]
Company: [company]
Grant date: [date]
Exercise price: [price] NIS
Sale/exit price: [price] NIS
Number of shares: [N]
Gross gain per share: [gain] NIS
Total gross gain: [total] NIS

--- CAPITAL GAINS TRACK (Section 102 Honi) ---
Capital gains tax (25%):       [amount] NIS
Surtax (if applicable):       [amount] NIS
Bituach Leumi:                 0 NIS
Health Insurance:              0 NIS
TOTAL TAX:                     [amount] NIS
NET PROCEEDS:                  [amount] NIS
Effective tax rate:            [rate]%

--- INCOME TRACK (Section 102 Peiroti) ---
Income tax (marginal):         [amount] NIS
Capital gains tax (25%):       [amount] NIS
Surtax (if applicable):       [amount] NIS
Bituach Leumi:                 [amount] NIS
Health Insurance:              [amount] NIS
TOTAL TAX:                     [amount] NIS
NET PROCEEDS:                  [amount] NIS
Effective tax rate:            [rate]%

--- DIFFERENCE ---
Additional tax on income track: [amount] NIS
Capital gains track saves:      [percentage]%

Note: This is an estimate. Consult a licensed Israeli
tax advisor (yo'etz mas) for binding guidance.
```

### Step 7: Model Exit Scenarios

When the user is facing a potential exit, model multiple price scenarios:

| Scenario | Exit Price | Gross Gain | Tax (CG Track) | Net Proceeds |
|----------|-----------|------------|-----------------|-------------|
| Conservative | $X | NIS Y | NIS Z | NIS W |
| Base case | $X | NIS Y | NIS Z | NIS W |
| Optimistic | $X | NIS Y | NIS Z | NIS W |

Convert USD to NIS using the BOI representative rate (sha'ar yatzig) on the exercise/sale date. Use the `boi-exchange` MCP server if available for current rates.

### Step 8: Exercise Timing Considerations

Help the employee think about WHEN to exercise:

| Strategy | Pros | Cons |
|----------|------|------|
| **Early exercise** (exercise before exit, start 24-month clock) | Locks in lower FMV as cost basis. Starts the 24-month clock earlier. | Requires paying exercise price out of pocket. Risk if company fails. |
| **Exercise at exit** (exercise and sell simultaneously) | No out-of-pocket cost. Guaranteed liquidity. | If 24-month period has not elapsed, entire gain is taxed as income. |
| **Staged exercise** (exercise in batches over multiple tax years) | Spreads income across years, may avoid surtax. | Complexity. Multiple 24-month clocks. |

**Critical warning for early exercise:** If the employee exercises options early (pays the exercise price to get shares), they must ensure the trustee continues to hold the shares for the full 24-month period counted from the end of the tax year of grant. Early exercise does NOT restart or shorten the 24-month clock.

## Examples

### Example 1: Capital-Gains-Track Exit (held past 24 months)

User says: "I have 10,000 options, strike 2 NIS, granted June 2022. Our company is being acquired and my shares sell for 50 NIS each. They were held by a trustee the whole time. How much tax?"

Walkthrough:
1. Track: trustee held the shares, company elected the capital gains track, so this is Section 102 Capital Gains (Honi).
2. 24-month check: granted June 2022, so the clock started December 31, 2022. The sale in 2026 is well past 24 months. Capital gains treatment is preserved.
3. Gross gain: (50 - 2) x 10,000 = 480,000 NIS.
4. Tax: 480,000 x 25% = 120,000 NIS.
5. Surtax: if the employee's total annual income (salary plus this gain) stays below 721,560 NIS, no surtax. If it crosses the threshold, 5% applies to the portion of capital gain above it.
6. Bituach Leumi and health tax: 0 on the capital gains track.
7. Net proceeds: 480,000 - 120,000 = 360,000 NIS (before any surtax).

Result: about 120,000 NIS tax, 360,000 NIS net, an effective rate of 25% on the gain.

### Example 2: Early Sale Before 24 Months (reclassification)

User says: "I sold my Section 102 shares 14 months after grant because I needed the cash. Strike was 1 NIS, I sold at 21 NIS, 5,000 shares. My salary is 28,000 NIS/month."

Walkthrough:
1. 24-month check: 14 months is short of the required period (counted from the end of the grant tax year, the gap is even larger than 14 months). The capital gains track election is voided.
2. Reclassification: the ENTIRE gain is treated as employment income, not capital gain.
3. Gross gain: (21 - 1) x 5,000 = 100,000 NIS, added on top of the 336,000 NIS annual salary.
4. Tax on the 100,000 NIS: marginal rates, landing largely in the 35% bracket given the salary base (up to 47% for any portion above 560,280 NIS annual).
5. Bituach Leumi and health tax: now apply to this employment income portion (subject to the monthly ceiling).
6. Surtax: 3% if total annual income crosses 721,560 NIS.

Result: the early sale roughly doubles the tax versus the 25% capital gains rate. There is no way to reverse the reclassification once the shares are sold early.

## Recommended MCP Servers

| MCP Server | Use For |
|------------|---------|
| `tase-mcp` | Current TASE stock prices for Israeli-listed companies |
| `boi-exchange` | USD/ILS exchange rates for converting option values |

### Step 9: US Dual Citizens and Relocators

Many Israeli tech employees are US citizens or green card holders (or relocate to/from the US). Two extra layers apply:

**For US citizens employed in Israel under Section 102:**
- Israel taxes the gain under Section 102 (25% capital gains track, or marginal income track).
- The US still taxes the same gain on the US 1040 because US citizens are taxed on worldwide income. US ISO/NSO labels do NOT control Israeli characterization, Section 102 governs the Israeli side regardless.
- For NSOs and RSUs, the US taxes ordinary income at exercise/vest, while Israel under the capital gains track defers tax until sale. This creates a TIMING MISMATCH where the employee owes US tax years before Israel's tax event, making the Foreign Tax Credit hard to claim against US income that has already been taxed.
- Practical mitigation: file Form 1116 (Foreign Tax Credit) in the year of Israeli sale, treat the Israeli tax as a credit against US capital gains. Be aware that under the US-Israel tax treaty (1995), Israel has primary taxing rights for Israeli-source employment income.
- For ISOs granted by a US parent: AMT may apply at US exercise even though Israel taxes nothing under Section 102 trustee track until sale. Always model both sides.

**For employees who relocate OUT OF Israel:**
- Section 100A (the Israeli exit tax) treats all unsold assets, including unvested options and unsold 102 shares, as deemed-sold one day before the cessation of Israeli residency.
- The employee can elect to defer the tax until actual sale (no interest charge until sale, but the Israeli portion is locked in based on residency-end values).
- The Israeli portion of the gain is usually allocated based on days of work performed in Israel vs abroad over the vesting period.
- This is a frequent double-taxation trap, the new country of residence often does not credit the Israeli exit tax. Get a CPA who handles relocation.

### Step 10: Stock-for-Stock Acquisitions (Section 104H)

If the exit is structured as a stock-for-stock merger (e.g., your startup is acquired by Acquirer Inc., and you receive Acquirer shares in exchange for your 102 shares), Section 104H provides a TAX-DEFERRED ROLLOVER:

- The exchange itself is not a taxable event.
- The cost basis of the old 102 shares carries over to the new Acquirer shares.
- The original grant date (and the 24-month clock) is preserved.
- The capital gains track election is preserved.
- Tax is deferred until the Acquirer shares are actually sold for cash.

If the deal is a mix of cash + stock, the cash portion is taxed immediately and the stock portion rolls over. The trustee usually continues to hold the new Acquirer shares for the remainder of the 24-month period.

## Gotchas

1. **24-month clock starts at the END OF THE TAX YEAR OF GRANT, not at exercise or at the grant date itself.** Agents commonly assume the holding period starts when options are exercised, or on the grant date. It starts from the end of the tax year in which the options were granted (December 31 of the grant year). Getting this wrong means telling the employee they can sell earlier than they actually can without losing capital gains treatment.

2. **Surtax is 5% on capital gains, not 3%.** Since 2025, capital income above 721,560 NIS/year is subject to both the 3% general surtax AND an additional 2% surtax on capital income. Agents often cite only the 3% figure. The correct combined surtax on capital gains above the threshold is 5%.

3. **RSU "exercise price" is zero, not the grant-date FMV.** For a PRIVATE company under the Section 102 capital gains track, the entire RSU value at sale is the taxable gain at 25% (since there was no purchase price). Agents sometimes mistakenly use the grant-date FMV as the cost basis, which understates the tax. But for a LISTED company, the Section 102(b)(3) split applies even on the capital gains track: the 30-day-pre-grant average value is an ordinary-income component taxed at marginal rates, and only the excess is taxed at 25%. Do not apply the flat-25%-on-everything rule to a public-company RSU holder.

4. **The employee cannot choose their track.** The company selects the track (capital gains or income) when filing the 102 plan with the ITA. Agents sometimes present this as an employee decision. The employee can only optimize timing and amounts, not the track itself.

5. **Foreign parent company shares have different rules.** When an Israeli subsidiary grants options on the PARENT company's shares (e.g., a US-listed parent), Section 102 still applies if properly structured, but withholding and reporting mechanics differ. The employer must withhold tax at source upon sale, and Form 867 from the trustee may show different fields than domestic grants.

6. **US citizens face phantom-income timing mismatch.** A US-citizen Israeli employee owes US tax on NSO exercise and RSU vest under US rules, while Israeli tax under Section 102 capital gains track is deferred until sale. Without active Foreign Tax Credit planning, this leads to double taxation. Section 102 cannot override the US worldwide-income rule.

7. **Exit tax (Section 100A) applies to relocators.** An employee who leaves Israel triggers a deemed sale of unsold 102 shares and unvested options one day before ceasing Israeli residency. The Israeli portion is allocated by Israeli vs foreign workdays during vesting. The new country of residence often does not credit this tax, creating a double-taxation trap.

8. **The 30-day clock is the PLAN-FILING clock, not the deposit clock.** Grants under a 102 plan can only be made starting 30 days after the plan is submitted to the ITA. Deposit-with-trustee deadlines are different and both anchor on the DATE OF GRANT (not the board-resolution date): 45 days from the date of grant for the board-resolution copy, and 90 days from the date of grant for the signed option agreement.

9. **A foreign broker does NOT withhold Israeli tax, so the employee must self-report.** When 102/RSU shares are held at a US broker (E*Trade, Schwab, Morgan Stanley, Fidelity) instead of by an Israeli trustee, no one withholds the Israeli capital gains tax at sale, and the trustee's Form 867 does not settle it. The Israeli-resident employee must file an annual income tax return (Form 1301) reporting the gain and, once securities gains cross the reporting threshold, pay semi-annual advance payments (mikdamot) on securities gains. Assuming "the tax was already withheld" is the single most common way public-company RSU holders miss a deadline and incur interest and penalties. This applies to any Israeli resident, not only US citizens.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Income Tax Ordinance full text (Hebrew, Section 102 lives in the ordinance) | https://www.nevo.co.il/law_html/law01/255_001.htm | Exact legal requirements for each track |
| ITA ESOP circulars | https://www.gov.il/he/departments/israel_tax_authority | Latest professional circulars on Section 102 |
| PWC Israel Individual Tax | https://taxsummaries.pwc.com/israel/individual/taxes-on-personal-income | Current tax brackets and rates |
| CWS Israel Tax Guide 2026 | https://www.cwsisrael.com/israeli-tax-changes-2026-complete-guide/ | 2026 bracket changes and surtax thresholds |
| Bituach Leumi Rates (salaried employees) | https://www.btl.gov.il/Insurance/Rates/Pages/לעובדים%20שכירים.aspx | Current BL + health employee contribution rates by category |
| RSU Calculator Israel | https://www.rsu-calculator.com/explanation | RSU taxation methodology and examples |

## Troubleshooting

### "I don't know which track my options are on"
Ask the employee to check their grant letter (kitvei haktzaa) or contact HR. The grant letter specifies "mislul honi" (capital gains track) or "mislul peiroti" (income track). If the company used a trustee (ne'eman), it is almost always the capital gains track.

### "My company is foreign (Delaware C-Corp) with an Israeli subsidiary"
Section 102 applies to Israeli employees of Israeli companies. If the Israeli subsidiary is the employer and has a filed 102 plan, Section 102 applies to options on the parent's shares. If the employee is employed directly by the foreign parent, Section 3(i) applies instead.

### "The exit is a stock-for-stock deal (not cash)"
In a stock-for-stock acquisition, the tax event occurs when the employee SELLS the acquired shares, not at the merger itself. The cost basis carries over. However, if the employee receives cash as part of the deal, that cash portion triggers an immediate tax event.

### "I exercised before 24 months, what now?"
The entire gain is reclassified as employment income, taxed at marginal rates (up to 47% + 3% surtax) plus Bituach Leumi and health insurance. This is significantly more expensive than the 25% capital gains rate. There is no way to reverse this.

### "I'm a US citizen working in Israel, do I pay tax twice?"
Both Israel and the US tax the gain, but you can claim a Foreign Tax Credit (Form 1116) on the US side for the Israeli tax actually paid. The challenge is timing: under Israeli Section 102 capital gains track, tax is paid at sale; under US rules, NSO exercise and RSU vest are taxable events that can occur years earlier. Coordinate with a CPA who handles US-Israel cross-border employees. Under the US-Israel tax treaty, Israel has primary taxing rights on Israeli-source employment income, including stock-based compensation earned while working in Israel.

### "I'm leaving Israel, what about my options?"
Section 100A treats unsold 102 shares and unvested options as deemed-sold one day before you cease Israeli residency. You can pay the Israeli tax at exit OR elect to defer to actual sale (no interest accrues during deferral, but the Israeli portion is locked in to residency-end values). Israel allocates the gain based on Israeli vs foreign workdays during vesting. The new country of residence may not credit the Israeli exit tax, so this is a known double-taxation risk that needs cross-border planning before you board the plane.

### "We are being acquired in a stock-for-stock deal, what is my tax event?"
Under Section 104H, a stock-for-stock acquisition is a tax-deferred rollover: no Israeli tax at the merger, the original cost basis carries over to the new acquirer shares, and the 24-month clock + capital gains track election are preserved. Tax is triggered only when you eventually sell the acquirer shares for cash. If the deal is mixed (some cash, some stock), the cash portion triggers an immediate Israeli tax event on its proportional share of the gain.
