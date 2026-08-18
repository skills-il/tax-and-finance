# Section 102 Tax Tracks - Detailed Comparison

## Overview

Section 102 of the Israeli Income Tax Ordinance (Pkudat Mas Hachnasa) provides a tax-advantaged framework for employee stock option plans (ESOPs). The section defines multiple "tracks" (mislulim) that determine how the gain from exercising and selling shares is taxed.

## Track Comparison Matrix

| Feature | 102 Capital Gains (Honi) | 102 Income (Peiroti) | 102 Non-Trustee | 3(i) Non-102 |
|---------|-------------------------|---------------------|-----------------|--------------|
| Tax rate on gain | 25% flat (30% for 10%+ holders) | Split: marginal + 25% | Marginal (10%-47%) | Marginal (10%-47%) |
| Trustee required | Yes | Yes | No | No |
| Holding period | 24 months from the end of the tax year of grant | 24 months from the end of the tax year of grant | None | None |
| Employer deduction | No | Yes | Yes | Yes |
| Bituach Leumi | No | Yes (on employment portion) | Yes | Yes |
| Health insurance | No | Yes (on employment portion) | Yes | Yes |
| Surtax (above threshold) | 5% (3% + 2%) | 3% on all + 2% on capital | 3% on all | 3% on all |
| Common usage | ~90% of Israeli ESOPs | Rare | Rare | Foreign employers |

## Capital Gains Track (Mislul Honi) - Detailed

### Requirements
1. Company files Section 102 plan with ITA (Reshut HaMisim). Grants under the plan can only be made starting 30 days after the plan is submitted to the ITA.
2. ITA-approved trustee (ne'eman) appointed to hold shares
3. Plan specifies capital gains track election
4. Board resolution approving the grant forwarded to the trustee within 45 days of the date of grant; signed option agreement delivered to the trustee within 90 days of the date of grant (deemed-compliance safe harbors; both clocks anchor on the grant date, not the board-resolution date)
5. Trustee holds for a minimum of 24 months counted from the end of the tax year of grant
6. Company does NOT claim tax deduction for the option expense

### Tax Calculation
- Entire gain (sale price minus exercise price) taxed at 25%
- No split between employment income and capital gain
- No Bituach Leumi or health insurance
- Surtax: 5% (3% general + 2% capital) on annual income above 721,560 NIS

### Effective Rate Examples (2026)
Formula: 25% on the entire gain, plus 5% surtax on the portion of total annual income above 721,560 NIS (when the gain itself is the only income above the threshold, the surtax portion equals gain - 721,560).

- Gain of 500,000 NIS, no other income: 25% × 500,000 = 125,000 NIS tax (gain stays below threshold, no surtax)
- Gain of 1,000,000 NIS, no other income: 25% × 1,000,000 + 5% × (1,000,000 - 721,560) = 250,000 + 13,922 = 263,922 NIS tax
- Gain of 2,000,000 NIS, no other income: 25% × 2,000,000 + 5% × (2,000,000 - 721,560) = 500,000 + 63,922 = 563,922 NIS tax

## Income Track (Mislul Peiroti) - Detailed

### Requirements
Same as capital gains track, but company elects income track in the plan filing.

### Tax Calculation
The gain is split at the exercise date:
1. Employment income = FMV at exercise - Exercise price (taxed at marginal rate)
2. Capital gain = Sale price - FMV at exercise (taxed at 25%)

### When Income Track Might Be Preferred
- Very rare. Only benefits companies that want the tax deduction.
- Employee almost always pays more tax under income track.
- Some companies with large operating losses may prefer the deduction.

## Early Sale Penalty

If shares are sold before the 24-month holding period expires:
- The ENTIRE gain is reclassified as employment income
- Taxed at marginal rates (up to 47%)
- Plus Bituach Leumi (up to 7%) and health insurance (up to ~5.17%)
- Plus 3% surtax if above threshold
- The capital gains track election is voided

This can nearly DOUBLE the tax bill compared to waiting.

## Section 3(i) - Non-102 Grants

Applies when:
- Foreign parent company grants directly to Israeli employees without 102 plan
- Company fails to meet Section 102 filing requirements
- Options granted to consultants (not employees)
- Plans that don't comply with Section 102 rules

Tax treatment:
- Entire gain taxed as employment income at marginal rates
- Full Bituach Leumi and health insurance apply
- No capital gains treatment available
- Tax is due at exercise (not at sale)

## Key Dates and Deadlines

| Event | Deadline | Consequence of Missing |
|-------|----------|----------------------|
| File 102 plan with ITA | Before first grant | Grants default to 3(i); grants only effective starting 30 days after ITA plan filing |
| Forward board resolution to trustee | 45 days after date of grant | May invalidate 102 treatment (deemed-compliance safe harbor) |
| Deliver signed option agreement to trustee | 90 days after date of grant | May invalidate 102 treatment (deemed-compliance safe harbor) |
| Form 146 (quarterly) | End of quarter | Reporting violation, possible plan disqualification |
| Form 156 (annual) | March 31 of following year | Reporting violation |
| 24-month holding | 24 months counted from the end of the tax year of grant | Gain reclassified as employment income |

## 2025 Section 102 Plan-Submission Amendment

The ITA published a professional circular on December 9, 2024 that changed how
Section 102 plans are filed, effective for plans submitted from January 1, 2025:

- **Online-only submission:** Section 102 plan filings are now online-only. The
  submitter must complete a detailed questionnaire describing the plan and its
  terms.
- **Red-flag screening:** the ITA uses the questionnaire data to detect possible
  deficiencies and "red flags" that a plan, or a specific grant within it, may
  fail to meet the Section 102 conditions.
- **Pre-approval for Put/Call plans:** plans that contain Put and/or Call options
  can obtain advance approval from the ITA's professional division, on conditions
  the division sets.

This changes the company-side filing mechanics, not the employee-side tax tracks
or the 24-month rule.
