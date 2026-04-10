---
name: israeli-stock-options-tax
description: "Calculate tax on stock options and RSUs for Israeli tech employees under Section 102. Use when user asks about option exercise tax, RSU taxation, startup exit proceeds, Section 102 tracks, trustee holding period, capital gains vs income track comparison, or 'how much tax on my options'. Produces a detailed tax breakdown with net proceeds. Do NOT use for crypto tax (use israeli-crypto-tax-reporter), ESOP plan setup (use israeli-startup-toolkit), controlling shareholder profit extraction (use israeli-corporate-tax-strategy), annual tax returns (use israeli-tax-returns), or payroll (use israeli-payroll-calculator)."
license: MIT
allowed-tools: Bash(python:*) WebFetch
compatibility: Works with Claude Code, OpenClaw, Cursor, Windsurf, Codex, GitHub Copilot, opencode, antigravity.
---

# Israeli Stock Options Tax Calculator

## Problem

Israeli tech employees receive stock options or RSUs as a significant part of their compensation, but most have no idea how much tax they will actually pay when they exercise or sell. The rules under Section 102 are complex: different tracks (capital gains vs income), a 24-month trustee holding period, surtax thresholds, and Bituach Leumi interactions all affect the final number. Getting it wrong can mean paying tens of thousands of shekels more than necessary, or worse, facing unexpected tax bills at exit.

## Instructions

### Privacy & Data Security

> [!CAUTION]
> This skill handles sensitive financial and personal data (PII) including salaries, grant amounts, and employer names.
> - **Local Calculation Only**: You MUST perform all monetary and tax calculations locally using Python. Never send specific financial amounts (e.g., "the tax on 500k NIS") or personal names to `WebFetch` or external search tools.
> - **Data Minimization**: Only ask the user for the data required for the specific calculation. Do not log or persist sensitive financial numbers.
> - **External Reference**: Use `WebFetch` only to retrieve generic data like USD/ILS exchange rates or current tax brackets, but never include user-specific values in the query URL.

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

**The 24-month rule:** Under both 102 trustee tracks, the trustee must hold the options AND the exercised shares for at least 24 months from the END OF THE TAX YEAR in which the options were granted. If the employee sells before 24 months, the entire gain is taxed as employment income at marginal rates. This is the most expensive mistake an employee can make.

**Correction for common misconception:** The 24-month period starts from the GRANT date (not the vesting date or exercise date). If options were granted on March 15, 2024, the earliest sale date for capital gains treatment is March 15, 2026.

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

#### Track B: Section 102 Income (Peiroti)

The gain is split into two parts:

```
Employment Income = FMV at exercise date - Exercise Price
Capital Gain = Sale Price - FMV at exercise date

Tax on Employment Income = Marginal income tax rate (10%-47%)
  + Bituach Leumi (up to 7% employee share)
  + Health Insurance (up to 5%)

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
  + Health Insurance (up to 5%)
  + 3% surtax if above threshold
```

#### RSU-Specific Calculation

RSUs under Section 102 capital gains track are taxed identically to options, but with exercise price = 0:

```
Gain = Sale Price - 0 = Sale Price (entire value is gain)
Tax = Gain x 25%
```

For RSUs under income track or listed companies, there is a split:

```
Employment Income = FMV at vesting date (or 30-day average for listed shares)
Capital Gain = Sale Price - FMV at vesting date
```

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

| Component | Reduced Rate (up to 7,122/month) | Full Rate (7,122-47,465/month) |
|-----------|----------------------------------|-------------------------------|
| Bituach Leumi (employee) | 0.4% | 7.0% |
| Health Insurance (employee) | 3.1% | 5.0% |
| **Total employee** | **3.5%** | **12.0%** |

Maximum monthly ceiling: 47,465 NIS. Income above this ceiling does not incur additional BL/health contributions. For a lump-sum option exercise, the employment income portion is spread over the vesting period for BL calculation purposes.

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

**Critical warning for early exercise:** If the employee exercises options early (pays the exercise price to get shares), they must ensure the trustee continues to hold the shares for the full 24-month period from grant date. Early exercise does NOT restart or shorten the 24-month clock.


## Gotchas

1. **24-month clock starts at GRANT, not exercise.** Agents commonly assume the holding period starts when options are exercised. It starts from the date the options were granted (or more precisely, the end of the tax year in which they were granted). Getting this wrong means telling the employee they can sell earlier than they actually can without losing capital gains treatment.

2. **Surtax is 5% on capital gains, not 3%.** Since 2025, capital income above 721,560 NIS/year is subject to both the 3% general surtax AND an additional 2% surtax on capital income. Agents often cite only the 3% figure. The correct combined surtax on capital gains above the threshold is 5%.

3. **RSU "exercise price" is zero, not the grant-date FMV.** For Section 102 capital gains track, the entire RSU value at sale is the taxable gain (since there was no purchase price). Agents sometimes mistakenly use the grant-date FMV as the cost basis, which understates the tax.

4. **The employee cannot choose their track.** The company selects the track (capital gains or income) when filing the 102 plan with the ITA. Agents sometimes present this as an employee decision. The employee can only optimize timing and amounts, not the track itself.

5. **Foreign parent company shares have different rules.** When an Israeli subsidiary grants options on the PARENT company's shares (e.g., a US-listed parent), Section 102 still applies if properly structured, but withholding and reporting mechanics differ. The employer must withhold tax at source upon sale, and Form 867 from the trustee may show different fields than domestic grants.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Section 102 full text (Hebrew) | https://www.nevo.co.il/law_html/law01/073_004.htm | Exact legal requirements for each track |
| ITA ESOP circulars | https://www.gov.il/he/departments/israel_tax_authority | Latest professional circulars on Section 102 |
| PWC Israel Individual Tax | https://taxsummaries.pwc.com/israel/individual/taxes-on-personal-income | Current tax brackets and rates |
| CWS Israel Tax Guide 2026 | https://www.cwsisrael.com/israeli-tax-changes-2026-complete-guide/ | 2026 bracket changes and surtax thresholds |
| Bituach Leumi Rates | https://www.btl.gov.il/English%20Homepage/Insurance/Ratesandamount/Pages/forSalaried.aspx | Current BL contribution rates |
| RSU Calculator Israel | https://www.rsu-calculator.com/explanation | RSU taxation methodology and examples |

## Troubleshooting

### "I don't know which track my options are on"
Ask the employee to check their grant letter (kitvei haktzaa) or contact HR. The grant letter specifies "mislul honi" (capital gains track) or "mislul peiroti" (income track). If the company used a trustee (ne'eman), it is almost always the capital gains track.

### "My company is foreign (Delaware C-Corp) with an Israeli subsidiary"
Section 102 applies to Israeli employees of Israeli companies. If the Israeli subsidiary is the employer and has a filed 102 plan, Section 102 applies to options on the parent's shares. If the employee is employed directly by the foreign parent, Section 3(i) applies instead.

### "The exit is a stock-for-stock deal (not cash)"
In a stock-for-stock acquisition, the tax event occurs when the employee SELLS the acquired shares, not at the merger itself. The cost basis carries over. However, if the employee receives cash as part of the deal, that cash portion triggers an immediate tax event.

### "I exercised before 24 months -- what now?"
The entire gain is reclassified as employment income, taxed at marginal rates (up to 47% + 3% surtax) plus Bituach Leumi and health insurance. This is significantly more expensive than the 25% capital gains rate. There is no way to reverse this.
