# Section 102 Tax Tracks - Detailed Comparison

## Overview

Section 102 of the Israeli Income Tax Ordinance (Pkudat Mas Hachnasa) provides a tax-advantaged framework for employee stock option plans (ESOPs). The section defines multiple "tracks" (mislulim) that determine how the gain from exercising and selling shares is taxed.

## Track Comparison Matrix

| Feature | 102 Capital Gains (Honi) | 102 Income (Peiroti) | 102 Non-Trustee | 3(i) Non-102 |
|---------|-------------------------|---------------------|-----------------|--------------|
| Tax rate on gain | 25% flat (a 10%+ holder is excluded from the section, see below) | Split: marginal + 25% | Marginal (10%-47%) | Marginal (10%-47%) |
| Trustee required | Yes | Yes | No | No |
| Holding period | 24 months from allotment and deposit with the trustee | 12 months from allotment and deposit with the trustee | None | None |
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
5. Trustee holds for a minimum of 24 months counted from the day the shares were allotted and deposited with the trustee (the income track requires 12 months)
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

## Who is NOT an "employee" for Section 102

Section 102(a) defines the beneficiary as "'employee' - including an office holder in the company, but excluding a controlling shareholder", and the trustee-allocation definition adds "provided that the employee is not a controlling shareholder in it at the date of the allocation or as a result of it". "Controlling shareholder" takes its Section 32(9) meaning: holding, directly or indirectly, alone or together with a relative, at least 10% of the issued share capital or of the voting power, a right to hold or acquire either, a right to at least 10% of the profits, or a right to appoint a director.

Consequences:

- A 10%+ holder does not get a reduced or increased Section 102 rate. The section simply does not apply. The grant is ordinary income under Section 3(i) / Section 2(1)-(2): marginal rates up to 47%, plus Bituach Leumi and health tax, plus the 3% surtax above 721,560 NIS, an effective load around 50%.
- The test bites at the date of the allocation OR as a result of it, so a grant that itself pushes the holder through 10% is caught.
- Relatives' holdings count, so a founding couple or a parent-child pair can cross 10% without either one individually holding it.
- The 30% rate quoted in some guides is the Section 91(b) capital gains rate and the Section 125B dividend rate for a substantial shareholder on ordinary share dealings. It is not a Section 102 rate and must not be applied to a Section 102 grant.

## Section 3(i) - Non-102 Grants

Applies when:
- The recipient is a controlling shareholder (10%+ under Section 32(9)) and is therefore outside Section 102
- Foreign parent company grants directly to Israeli employees without 102 plan
- Company fails to meet Section 102 filing requirements
- Options granted to consultants (not employees)
- Plans that don't comply with Section 102 rules

Tax treatment:
- Entire gain taxed as employment income at marginal rates
- Full Bituach Leumi and health insurance apply
- No capital gains treatment available
- Tax is due at exercise (not at sale)

## Non-Trustee Track (102(c)): when the tax event falls

The non-trustee track is not simply "marginal rates". The TIMING differs by instrument:

| Instrument, no trustee | At allocation | At realisation |
|---|---|---|
| Shares (102(c)(1)) | Taxed as Section 2(1)/2(2) income at the date of allocation | Taxed again under Part E (capital gains) on the further appreciation |
| Right to acquire a share, NOT listed for trading (102(c)(2)) | Not taxed | Whole benefit taxed as Section 2(1)/2(2) income |

The practical consequence is a DRY TAX CHARGE: a non-trustee share grant creates a liability on day one, before the employee has any cash or any liquidity. A non-trustee unlisted option grant does not.

## Section 102(f): exit-tax rate override

Section 102(f) provides that, notwithstanding Section 100A, the rate on the taxable portion of the gain of an employee who ceased to be an Israeli resident is the ordinary Section 121 rate in three cases:

1. A trustee allocation on the income track.
2. A trustee allocation on the capital gains track where the share was realised before the end of the period.
3. A non-trustee allocation to which 102(c)(2) applies.

A capital-track trustee allocation that ran the full 24 months is NOT on that list, so it keeps the 25% capital gains rate on exit.

## Key Dates and Deadlines

| Event | Deadline | Consequence of Missing |
|-------|----------|----------------------|
| File 102 plan with ITA | Before first grant | Grants default to 3(i); grants only effective starting 30 days after ITA plan filing |
| Forward board resolution to trustee | 45 days after date of grant | May invalidate 102 treatment (deemed-compliance safe harbor) |
| Deliver signed option agreement to trustee | 90 days after date of grant | May invalidate 102 treatment (deemed-compliance safe harbor) |
| Form 146 (quarterly) | End of quarter | Reporting violation, possible plan disqualification |
| Form 156 (annual) | March 31 of following year | Reporting violation |
| Trustee holding period | 24 months (capital track) or 12 months (income track) counted from allotment and deposit with the trustee | Gain reclassified as employment income |

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
