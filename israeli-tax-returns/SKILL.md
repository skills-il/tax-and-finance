---
name: israeli-tax-returns
description: Prepare and file Israeli tax returns with Reshut HaMisim. Covers Form 1301 (individual), Form 1214 (corporate), Form 126 (employer salary), Form 856 (supplier payments), Form 6111 (financial statements), mikdamot (advance payments), Mas Shevach (real estate capital gains), and securities capital gains (Forms 1322/1325). Use when user asks about "doch shnati", "tax return Israel", "Form 1301", "Form 1214", "mas hachnasa", "mikdamot", "mas shevach declaration", "capital gains report", "nekudot zikui", "mas yesafim", or "דוח שנתי". Guides income classification, deductions, tax credits, surtax, deadlines, and SHAAM submission. Do NOT use for VAT reporting (use israeli-vat-reporting), withholding tax (use israeli-tax-withholding), crypto tax (use israeli-crypto-tax-reporter), payroll (use israeli-payroll-calculator), invoicing (use israeli-e-invoice), or Section 102 employee stock options (use israeli-stock-options-tax).
license: MIT
allowed-tools: Bash(python:*) WebFetch
compatibility: Works with Claude Code, OpenClaw, Cursor, Windsurf, Codex, GitHub Copilot, opencode, antigravity.
---

# Israeli Tax Returns

## Legal notice

This is a free information tool operated by an AI model. It explains the tax rules and helps you organise your own figures. All of its outputs are produced automatically by an AI model, with no involvement, review, or approval by a tax adviser or accountant. The output is not a tax opinion, not a return prepared by a licensed representative, and not professional advice, but a general calculation and explanation only: it does not examine the full extent of your income or your complete documents. An AI model may err, omit data, or present a wrong conclusion.

Any form or text this tool produces is an automatic draft for your personal preparation only, and is not a filed return. Responsibility for reporting and for paying the tax is yours, the binding computation is the Tax Authority's, and representation before the Tax Authority is reserved to those permitted by law. This tool is not a substitute for advice that takes account of the particular circumstances and needs of each person. Consult a tax adviser or accountant before filing or paying. All use of its output is the user's sole responsibility.


## Instructions

### Step 1: Identify the Return Type

Determine which tax return or report the user needs to prepare. Israeli tax law requires different forms for different situations:

| Form | Hebrew Name | Who Files | Deadline | Frequency |
|------|-------------|-----------|----------|-----------|
| 1301 | דוח שנתי ליחיד | Individuals, sole proprietors, freelancers | 2025 return: 30.6.2026 online, end of May 2026 on paper; CPA-represented filers follow the quota schedule, final stage 28.2.2027 (Step 9) | Annual |
| 135 | דוח שנתי מקוצר | Salaried individuals filing a short return to claim a refund | Within 6 years after the end of the tax year (Section 160): the tax-year 2020 request closes 31.12.2026 | Annual / on demand |
| 1214 | דוח שנתי לחברה | Companies (Chevra Ba'am, Chevra Pratit) | Statutory 31 May; 2025 returns got a general extension to 30.7.2026, and CPA-represented companies follow the quota schedule, final stage 31.3.2027 | Annual |
| 126 | דוח מעסיק על משכורות | Employers reporting employee salaries and withholdings | April 30 | Annual |
| 856 | דוח על תשלומים לספקים | Businesses reporting payments to suppliers/freelancers | April 30 | Annual |
| 6111 | דוח כספי אחיד | Businesses and companies, except those with business turnover below 300,000 NIS (as defined in the bookkeeping instructions) | Submitted with 1301 or 1214 | Annual |
| Mikdamot | מקדמות מס הכנסה | Self-employed and businesses with advance payment assessments | 15th of the month after the period | Bi-monthly |
| Mas Shevach | הצהרת מס שבח | Anyone selling real estate in Israel | Declaration within 30 days of the sale, exemption claims included; tax payable within 60 days of the sale | Per transaction |
| 1322/1325, 1399 | דוח רווח הון | Anyone with capital gains | 1322/1325 are appendices to the annual Form 1301; a sale on which no tax was withheld is reported on Form 1399 within 30 days, with an advance payment (s.91(d)(1)) | Per transaction and annual |

Ask the user:
- Which return type do they need?
- Tax year (shnat mas) being reported
- Entity type: individual (yachid), sole proprietor (atzmai), or company (chevra)
- Whether they have a CPA (roeh heshbon) handling submission

### Step 2: Annual Individual Tax Return (Form 1301)

Form 1301 is the main annual income tax return for individuals and non-corporate business owners. It covers all income sources for the calendar year (January 1 to December 31).

**Who must file Form 1301:** (mandatory-filing triggers are set by the Income Tax Regulations (Exemption from Filing a Return), 1988, under Section 131(a) of the Ordinance, a salaried employee is exempt only if they stay under every threshold below)
- Self-employed individuals (osek murshe or osek patur)
- Individuals whose annual salary exceeded the Regulation 134A filing-exemption ceiling. **Two different ceilings get conflated here and they are not the same number.** For tax year 2025 the salary ceiling in Addition A is **723,000 NIS**; separately, Regulation 3(a)(8) withdraws the exemption from anyone whose income is chargeable to surtax under Section 121B, at **721,560 NIS**. Either one crossed means a return is due.
- Individuals with income from multiple employers
- Individuals with foreign income or assets abroad exceeding reporting thresholds (including a foreign securities/brokerage account)
- Anyone who received capital gains during the tax year
- Individuals with rental income above the exempt threshold; in particular, annual residential rent above **375,000 NIS** requires a return even on the 10% track (below that, the 10% track can be settled without a full return)

**All eight Regulation 134A filing-exemption ceilings for tax year 2025 are tabulated in `references/form-guide.md`.** Crossing any one of them removes the exemption.

A separate exemption from filing the return **online** (Section 131(b2)(4)) applies below 95,820 NIS for an individual or 191,640 NIS for a couple, tax year 2025. That is an exemption from the online channel, not from filing.

**Main sections of Form 1301:** personal details; employment income (from Form 106); business/profession income (Appendix Aleph / Form 1320); rental income and chosen track; capital and investment income; foreign income (Appendix 1327); deductions and credits (pension Sections 45A/47, donations Section 46, life insurance); and nekudot zikui (Step 3).

**Key appendices to prepare:**
- Form 1320 (Appendix Aleph): Profit and loss statement for self-employed
- Form 1321: Calculation of non-business taxable income
- Form 1322/1325: Capital gains from securities (see Step 7)
- Form 1327: Foreign income and assets declaration
- Form 1343: Depreciation and amortization schedule
- Form 6111: Standardized financial statements (if turnover > 300,000 NIS, see Step 5)

**Rental income:** three tracks for residential rent (exempt below 5,654 NIS/month, a flat 10% on gross rent paid within 30 days after the tax year ends (s.122(a1)), or regular rates with expenses, which for a filer under 60 start at 31% because rent is not personal-exertion income). Conditions are in `references/tax-brackets-credits.md`.

### Step 2.5: Short Return for Salaried Refund-Seekers (Form 135)

Form 135 (דוח שנתי מקוצר, the short annual return) is the common entry point for
salaried employees who are not required to file a full Form 1301 but want to
claim a refund. Typical cases: nekudot zikui that the employer did not apply, a
mid-year job change, donations under Section 46, or pension contributions that
were never credited.

- A salaried filer who only wants a refund usually files Form 135, not the full
  1301.
- **Refund-claim window:** under Section 160 of the Income Tax Ordinance, a
  refund can be claimed for up to 6 years back. A filer in 2026 can still claim
  refunds for tax years 2020-2025, and the **tax-year 2020 request must be filed by
  31.12.2026**, after which that year's refund is lost.
- Compute each claimed year with THAT year's brackets and credit-point value from
  its ITA annual booklet: 2,904 NIS is the value for 2024 through 2026, and years before 2024 differ.
- File it online through the ITA service at https://www.gov.il/he/service/itc135,
  which is fully online (documents included) for tax years 2019 onward and opens a
  refund-only file, not an active tax file.
- If the person has business income, foreign income, capital gains, or crosses
  the mandatory-filing thresholds, they must file the full Form 1301 instead.

### Step 2.6: Havraa-Day Reduction on Form 106 (Fields 011/012, tax years 2024-2025 only)

The temporary havraa reduction puts a value in Form 106 field 011/012 and Form 1301 line 60 for tax years 2024 and 2025 only. **It is informational, not a deduction or a credit:** it was already netted out of gross salary (field 158), so entering it in Part YB double-counts it. The law was not renewed, so a 2026 form carrying such a value should be queried with the employer. Amounts and the half-day track are in `references/form-guide.md`.

### Step 3: Nekudot Zikui (Tax Credit Points) Calculation

Each nekudot zikui point reduces the annual tax liability by 2,904 NIS (2026, 242 NIS/month). Points reduce the tax itself, not taxable income, and cannot take the liability below zero.

**The full schedule, with every category and every band, is in `references/credit-points.md`. Read it before quoting a number.** The summary below is the shape of the calculation, not a substitute for the table.

| Category | Points | Notes |
|----------|--------|-------|
| Israeli resident | 2.25 | Section 34 (2.0) plus Section 36 travel credit (0.25) |
| Woman, additional | 0.5 | Section 36A, so a resident woman is 2.75 |
| Children | **Six age bands, not three** | Year of birth 2.5; ages 1-2 **4.5**; age 3 **3.5**; ages 4-5 2.5; ages 6-17 **2.0 mother / 1.0 father**; year the child turns 18 0.5 mother only. Sections 66(c)(4) and 66(c)(5) |
| Child who is paralysed, blind, or has an intellectual-developmental disability | 2.0 per child | Section 45(a), on top of the age band. Mutually exclusive with the Section 44 credit |
| Single parent | 1.0 | Section 40(b)(2), additional |
| New immigrant (oleh chadash) | 1 / 3 / 2 / 1 per year across a **54-month** window from the aliyah date, **8.5 points total** | Section 35(a). Keyed to the aliyah date, not the calendar year |
| Returning resident (toshav chozer) | **Not the oleh track.** Section 35(d) covers only those who resumed Israeli residency between 16.5.2010 and 30.9.2012 | A person returning today gets no Section 35 points on that basis |
| Discharged soldier / national service | **2.0 per year for 3 years** if regular service was 23+ months (man) or 22+ months (woman), otherwise 1.0 per year | Section 39A, 1/6 or 1/12 point per month for the 36 months after discharge. Form 101 box 14 |
| Combat reserve service | **Up to 4.0**, on the previous year's days | Section 39B. 2026-2027: 0.5 at 30-39 days, 0.75 at 40-49, 1.0 at 50-54, then +0.25 per extra 5 days to 4.0 at 110+. From 2028: 0.75 from 20 days, +0.25 per extra 5 days to 4.0 at 85+ |
| Divorced filer who remarried and pays mezonot | 1.0 | Section 40A |
| Aged 16-17 in the tax year | 1.0 | Section 40B |
| Academic degree (BA) | 1.0 | For as many tax years as the degree took, capped at 3. Section 40C |
| Academic degree (MA) | 0.5 | Capped at 2 tax years. Section 40C |
| Vocational studies certificate | 1.0 | Form 101 box 15 claims it alongside the academic credit, on a Form 119 declaration. Confirm the year count for vocational studies before quoting it |
| Blind, or 100% disabled (90% in some cases) | **Not credit points** | Section 9(5) income EXEMPTION on personal-exertion income up to the year's ceiling in the ITA booklet. Form 101 box 2A |

**Section 44 institution credit (not a credit point):** where the filer paid to maintain a child, spouse, or parent who is completely paralysed, permanently bedridden, blind, or not of sound mind in a special institution, the credit is 35 percent of the part of the payments exceeding 12.5 percent of taxable income.

**Section 11 yishuv mutav (not a credit point):** a percentage discount on tax on personal-exertion income, capped at an annual ceiling. The rate and the ceiling differ **per yishuv** and change annually. Read the row for the specific yishuv in chapter H of the ITA deductions booklet; never quote a rate from memory.

**Calculation example:**
A married woman (2.75 points) with two children aged 3 and 7 in the tax year: age 3 gives 3.5 points, age 7 gives 2.0 points for the mother. Total 2.75 + 5.5 = 8.25 points = 8.25 x 2,904 = 23,958 NIS annual tax reduction.

### Step 3.1: Aliyah and Return Incentive (temporary provision, in force 31.3.2026)

Chapter D of the Economic Efficiency Law 2026 exempts an **oleh chadash or toshav chozer vatik who arrived in Israel between 5 November 2025 and 31 December 2026** from tax on personal-exertion income (business and salary) produced in Israel, up to an annual ceiling that runs 600,000 NIS in 2026, 1,000,000 in 2027 and 2028, 350,000 in 2029, and 150,000 in 2030. It is given **in addition** to every other relief such a person has, including Section 35 credit points. The ITA implementing circular had not been published as of the 2026 deductions booklet, so confirm the detailed conditions before relying on them. Full table and citation in `references/credit-points.md`.

### Step 3.5: Pension and Donation Credits (Sections 45A, 47, 46)

Three benefits that are among the most commonly missed on a return, and the two most common sources of a salaried refund claim.

- **Section 45A pension credit:** 35 percent of the qualifying pension contribution, reducing tax directly. For an employee the qualifying deposit is 7 percent of hachnasa mezaka, and hachnasa mezaka from employment is capped at 9,700 NIS/month for 2026, so the maximum credited deposit is 679 NIS/month. An amit mutav has a separate track whose 2026 ceiling the Tax Authority publishes as 19,400 NIS/month.
- **Section 47 pension deduction:** reduces taxable income rather than tax. A self-employed filer can deduct up to 11 percent of annual business income within the qualifying ceiling; employee contributions above the 7 percent 45A threshold can qualify here. The same shekel cannot be counted under both.
- **Section 46 donation credit:** 35 percent for individuals (23 percent, the corporate rate, for companies), only to an institution holding a valid Section 46 recognition. Minimum floor **207 NIS** applied to the year's COMBINED donations, not to each donation separately, which is the point most often got wrong. Ceiling is the lower of 10,354,816 NIS (2026) or 30 percent of taxable income; the excess carries forward 3 years.

Worked examples, the self-employed 5.5 / 11 / 16.5 percent structure, and the documentation requirements are in `references/form-guide.md`.

### Step 3.7: Return-Preparation and Professional Fee Deduction (Section 17(11))

Fees paid to a CPA or tax advisor for the return are deductible under Section 17(11), for **salaried filers too** (a contested area for pure salaried filers, so document it), in the year they were **paid**. There is no dedicated Form 1301 field, and field 158 must not be reduced. Detail in `references/form-guide.md`.

### Step 4: Income Tax Brackets and Surtax

**Use the brackets of the tax YEAR being reported, never those of the year you are filing in.** A return filed during 2026 is almost always for tax year 2025, and a Form 135 refund claim can reach back to 2020. Brackets 3-5 differ between the two years:

| Bracket | Tax year 2025 (NIS) | Tax year 2026 (NIS) | Rate |
|---------|---------------------|---------------------|------|
| 1 | 0 - 84,120 | 0 - 84,120 | 10% |
| 2 | 84,121 - 120,720 | 84,121 - 120,720 | 14% |
| 3 | 120,721 - 193,800 | 120,721 - 228,000 | 20% |
| 4 | 193,801 - 269,280 | 228,001 - 301,200 | 31% |
| 5 | 269,281 - 560,280 | 301,201 - 560,280 | 35% |
| 6 | 560,281 and above | 560,281 and above | 47% |
| Surtax | Above 721,560 | Above 721,560 | 47% + surtax, see below |

2025 values are frozen at their 2024 levels (ITA 2025 annual booklet). The 2026 widening of brackets 3-5 is Amendment 288 (Economic Efficiency Law 2026, published 31.3.2026, retroactive to 1.1.2026). For tax years before 2025, take the values from that year's ITA annual booklet. 47% applies to every shekel above 560,280 and does not stop at 721,560: the surtax is charged ON TOP, which is why the effective top rate is 50%.

**These brackets are for personal-exertion income** (salary, business) and for all income of a filer aged 60 or over. Other income of a filer under 60, such as rent on the regular track or interest, starts at 31%: in 2025, 31% up to 269,280, then 35% and 47% (s.121(a)).

**Surtax (mas yesafim), two tiers from tax year 2025** (Section 121B(a1), added by Amendment 276, in force 1.1.2025):
- All taxable income above 721,560 NIS: 3% (effective top rate on employment income: 50%)
- Taxable income from capital sources (anything other than salary and personal-exertion income) above 721,560 NIS, measured on the capital-source income alone: a further 2%, so 5% in total
- Real-estate gain (shevach) is part of surtax income. For a **residential apartment** it counts only if the sale value exceeds 5,382,285 NIS (2025) AND the sale is not exempt, so an exempt single-residence sale never counts. This is long-standing law, not a 2026 change: a proposal to drop the apartment carve-out was removed from the final 2025 law.

**Corporate tax rate:** 23% flat rate on taxable profits for companies (Chevra).

**Closely held companies (Chevra Me'atim):** Subject to a 2% annual tax on accumulated undistributed profits unless at least 6% of accumulated profits are distributed as dividends.

**Self-employed additional levies:** self-employed individuals also pay Bituach Leumi and health tax on business income, calculated separately from the income tax return, though amounts paid during the year may affect advance-payment reconciliation.

### Step 5: Financial Statements Attachment (Form 6111)

Form 6111 reports the profit and loss and balance sheet in the Tax Authority's standardized item codes, matching the audited statements, and is usually exported by the CPA's accounting software. Who is exempt and the code list are in `references/form-guide.md` and the ITA's 6111 explanatory notes for the tax year.

### Step 6: Employer and Supplier Reports (Forms 126 and 856)

Employers file Form 126 (annual salary report) and issue Form 106 to each employee by 31 March; businesses file Form 856 for payments to non-employee suppliers. Both are due 30 April. See `references/form-guide.md` for the full per-field breakdown of both forms.

### Step 7: Capital Gains Reports

**Real Estate Capital Gains (Mas Shevach):**
When selling real property in Israel, the seller must file a Mas Shevach declaration with Reshut HaMisim (Israel Tax Authority) via the misim.gov.il portal or real estate taxation offices (Misrad Misui Mekarkein) **within 30 days of the sale** (Section 73(a) of the Real Estate Taxation Law). An exemption claim is made inside that same declaration; there is no separate 40-day track. The tax itself is payable **within 60 days of the sale** (Section 90A), after which linkage and interest accrue.

Calculation:

```
Sale price
- Original purchase price (adjusted for inflation via CPI index)
- Allowable deductions (purchase tax paid, legal fees, agent commission, renovation costs with receipts)
= Real capital gain (shevach re'ali)
x 25% tax rate (the rate for gain from 1.1.2012 on)
= Mas Shevach payable
```

For an individual who bought before 1.1.2012 the real gain is split linearly by period (s.48A(b1)): the part up to 7.11.2001 at the top Section 121 rate, the part from then to 1.1.2012 at up to 20%, and the rest at 25%. Do not apply a flat 25% to an older purchase.

**Single apartment exemption (ptur dira yechida):**
Full exemption from Mas Shevach if ALL conditions are met:
- This is the seller's only residential property in Israel
- Owned for at least 18 months
- Sale price is below the exemption ceiling (5,008,000 NIS, 2024-2027, frozen)
- Seller is an Israeli resident
- Partial exemption applies proportionally above the ceiling

**Linear method (shita liniarit):**
For a qualifying residential apartment (dirat megurim mezaka) bought before 1 January 2014 that does not get the full exemption, the real gain attributable to the period up to 1.1.2014 is exempt and the rest is taxed at the regular rate (s.48A(b2)). A phase-out was proposed by the Ministry of Finance in 2024; the provision is still in the consolidated statute as of October 2026.

**Securities Capital Gains (Forms 1322/1325):**
Capital gains from selling stocks, bonds, mutual funds, and other securities:
- 25% tax rate for individuals on traded securities
- 30% tax rate if the seller holds 10% or more of the company
- Every sale goes on the annual return (Forms 1322/1325). Where no tax was withheld at source (for example at a foreign broker), a Form 1399 report and advance payment are ALSO due within 30 days of the sale (s.91(d)(1)); the annual return does not replace them
- Losses can offset gains from the same category within the tax year
- Carry forward of capital losses to future years (capital losses only offset capital gains, not ordinary income)

### Step 8: Advance Tax Payments (Mikdamot)

Self-employed individuals and businesses are typically assessed advance income tax payments (mikdamot) by the Tax Authority. These are periodic prepayments against the expected annual tax liability.

The Tax Authority sets a percentage rate from the business's prior-year returns (industry statistics and projected turnover for a new business), applied to bi-monthly turnover excluding VAT, due by the 15th of the month after each bi-monthly period: 15 March, 15 May, 15 July, 15 September, 15 November, 15 January.

At year end the total paid is reconciled on Form 1301 or 1214 against the actual liability: an excess is refunded (hechzer mas), a shortfall is owed plus possible interest.

**Adjusting the rate:** if the business's income changes significantly (revenue drops sharply, a large new contract, or a change in business activity), request a rate adjustment (shinui shiur mikdamot) from the Tax Authority.

### Step 9: Filing via SHAAM Online Portal

All returns are submitted electronically via the Tax Authority's online system (SHAAM):

Register at misim.gov.il with a teudat zehut or company number and two-factor credentials. Log in, pick the form and tax year, enter or upload the data, review the calculated liability, submit for a confirmation number, then pay via the payment portal (bank transfer, credit card, or post-office reference).

CPA authorization (yipui koach) is granted by the taxpayer in the SHAAM portal, per client and per year, and lets the CPA submit returns, view assessments, and correspond with the Tax Authority.

**Filing extensions:**
- Form 1301, 2025 return, unrepresented: 30.6.2026 online (end of May 2026 on paper), already passed as of October 2026. The 2025 online filing service: https://www.gov.il/he/service/reporting-and-payment-2025-annual-tax-report-for-individuals
- CPA-represented filers, 2025 returns (ITA representatives' arrangement of 28.4.2026): individuals 10% of the representative's files by 23.9.2026 (moved from 31.8.2026), 50% by 30.11.2026, 100% by **28.2.2027**; companies 10% by 29.10.2026, 40% by 31.12.2026, 100% by **31.3.2027**. Quotas can move again; confirm the current stage
- Form 1214: statutory 31 May, extended for 2025 returns to 30.7.2026 for companies filing without a representative
- Request any extension BEFORE the original deadline

**Deadline already missed:** file anyway, the obligation does not lapse. Section 188(a) sets an indexed fine for every month of delay (s.188(h)); quote the Tax Authority's current figure, and unpaid tax keeps accruing linkage and interest. Whether a return handed to a representative after the deadline can still ride the quota schedule is for that representative to confirm; do not promise it.

## Examples

### Example 1: Freelancer Filing Annual Tax Return (Form 1301)

User says: "I'm a freelance developer (osek murshe), I need to prepare my annual tax return for 2025"

Actions:
1. Collect income details: Total business revenue from invoices, any employment income (Form 106 from employer), rental income, investment income
2. Prepare Appendix Aleph (Form 1320): List all business expenses (office rent, equipment, software subscriptions, internet, phone) to calculate net business profit
3. Calculate nekudot zikui: Male resident (2.25) + 2 children aged 4 and 8 (2.5 + 1.0) = 5.75 points = 16,698 NIS credit
4. Apply income tax brackets to total taxable income
5. Subtract nekudot zikui credit from tax liability
6. Reconcile against mikdamot (advance payments) made during the year
7. Prepare Form 6111 if turnover exceeds 300,000 NIS
8. Result: net tax due or refund figures for the user to review and enter in SHAAM themselves

### Example 3: Real Estate Capital Gains Declaration (Mas Shevach)

User says: "I just sold my investment apartment for 2.8 million shekels, I bought it in 2018 for 1.6 million"

Actions:
1. Determine if single-apartment exemption applies (investment apartment = likely not the only property, so no exemption)
2. Calculate real gain: 2,800,000 - 1,600,000 = 1,200,000 NIS gross gain
3. Adjust for inflation: Apply CPI index change from purchase date to sale date
4. Deduct allowable expenses: purchase tax (mas rechisha) paid, legal fees, agent commission, documented renovation costs
5. Calculate Mas Shevach: Real gain x 25% = tax payable
6. Prepare declaration for filing within 30 days of sale
7. The buyer also files a Mas Rechisha declaration (purchase tax) independently
8. Result: Mas Shevach liability with supporting calculation breakdown

## Bundled Resources

### References
- `references/form-guide.md` - Forms 1301, 1214, 126, 856, 6111, 1322, 1325: who files, deadlines, key fields, plus worked examples for a company return (Form 1214) and for mikdamot. Consult for a specific form or to decide which forms apply.
- `references/credit-points.md` - The full nekudot zikui schedule: every child age band, oleh, returning resident, discharged soldier, both combat-reserve regimes, netul yecholet, Section 44, Section 11. Consult before quoting any credit-point number.
- `references/tax-brackets-credits.md` - 2026 brackets (1-2 and the 47% band frozen at 2025 values, 3-5 widened for 2026), nekudot zikui values and categories, surtax thresholds, corporate rates. Consult for any tax calculation.

## Gotchas
- Form 1301 for tax year 2025, filed in 2026: 30 June online, end of May on paper. April 30 is the statutory baseline, not the extended date, and April 15 is American. A CPA-represented filer is on the representatives' quota schedule, final stage 28.2.2027, not on 30 June.
- Brackets follow the tax year of the return. Computing a 2025 return on the widened 2026 brackets understates tax for anyone whose taxable income passes 193,800 NIS: 193,801-228,000 is 31% in 2025 against 20% in 2026, and 269,281-301,200 is 35% against 31%, so up to about 5,039 NIS.
- Individuals file Form 1301, not a 1040. US form numbers and fields do not exist here.
- Capital gains go on separate schedules with their own rates: 25% on most individuals' securities gains (30% for a 10% holder), and a Mas Shevach real gain split by purchase period (Step 7). Do not apply one blanket rate, and do not tax an under-60 filer's rent or interest from the 10% bracket.
- The child credit-point schedule has SIX age bands, not three, and Form 101 part H has a separate box for each. A one-year-old is worth 4.5 points, not 2.5: quoting the flat "ages 1-5" band understates a parent's credit by 5,808 NIS. From age 6 the mother gets 2.0 and the father 1.0, so a single "per child" figure is wrong for one of them whichever you pick.
- Combat-reserve points (Section 39B) run to a maximum of 4.0, not 1.0, and they are counted on the PREVIOUS tax year's days. There are two band tables: one for 2026-2027 starting at 30 days, a different permanent one from 2028 starting at 20 days. Picking the wrong table, or capping at 1.0, can understate a heavy reservist by 8,712 NIS.
- A returning resident is not on the oleh credit-point track. Section 35(d) defines toshav chozer for this purpose as someone who resumed residency between 16.5.2010 and 30.9.2012 only. Telling a returnee they get "the same points as an oleh" invents an entitlement.
- Discharged-soldier points (Section 39A) are worth up to 2.0 points a year for three years and are routinely never claimed, because nothing on the return prompts for them. Ask.
- Nekudot zikui must be claimed annually and vary by status (marital, children, new oleh, discharged soldier, combat reservist). Do not assume a default count.
- The 2% capital-income surtax started in tax year 2025, not 2026, and real-estate gain has long been part of surtax income (a residential apartment only above a 5,382,285 NIS sale value and only when not exempt). Treating Mas Shevach and surtax as separate under-reports the liability.
- Return-preparation fees are deductible under Section 17(11) for SALARIED filers too, not only the self-employed. There is no dedicated Form 1301 field: keep the invoice and attach an explanation.
- The havraa-reduction figure on Form 106/1301 (field 011/012, "מחיר יום ההבראה שהופחת ממשכורת העובד", tax years 2024-2025 only) is informational: it was already netted out of gross salary and is not income to the employee. Agents reasoning from the form's visual structure may wrongly treat it as a Part יב deduction and mis-state tax.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Israel Tax Authority (Reshut HaMisim) | https://www.gov.il/en/departments/israel_tax_authority | Forms, filing guides, announcements |
| SHAAM online filing portal | https://www.misim.gov.il | Electronic submission of returns |
| Form 1301 online service, tax year 2025 | https://www.gov.il/he/service/reporting-and-payment-2025-annual-tax-report-for-individuals | 2025 deadlines, online filing, 2025 PDFs |
| Form 135 online refund service | https://www.gov.il/he/service/itc135 | Six-year refund window, online refund request |
| ITA 2025 annual deductions booklet | https://www.gov.il/BlobFolder/generalpage/income-tax-annual-deductions-booklet/he/generalInformation_income-tax-yearly-deductions-booklet_yearly-deductions-booklet-2025.pdf | Tax-year 2025 brackets, surtax, credit-point value |
| Kol-Zchut income tax brackets | https://www.kolzchut.org.il/he/מדרגות_מס_הכנסה | Current-year bracket thresholds |
| Kol-Zchut tax credit points | https://www.kolzchut.org.il/he/נקודת_זיכוי | Nekudot zikui value and eligibility |
| Kol-Zchut Mas Shevach calculation | https://www.kolzchut.org.il/he/חישוב_מס_שבח | Capital gains, exemptions, linear method |
| Israel Real Estate Taxation office | https://www.gov.il/he/departments/topics/land_taxation | Mas Shevach and Rechisha forms and rates |
| Income Tax Ordinance (consolidated, Nevo) | https://www.nevo.co.il/law_html/law00/84255.htm | Sections 11, 34-40C, 44, 45, 66(c) credit-point text |
| ITA 2026 deductions booklet (luach nikuyim) | https://www.gov.il/BlobFolder/generalpage/income-tax-monthly-deductions-booklet/he/generalInformation_income-tax-monthly-deductions-booklet_monthly-deductions-booklet-2026.pdf | Credit-point value, Regulation 134A ceilings, yishuv rates |
| ITA circular 2025-001368 (16.12.2025), Section 39B | https://www.gov.il/BlobFolder/dynamiccollectorresultitem/employers-info161225-1/he/IncomeTax_employers-info161225-1.pdf | Combat-reserve credit-point bands, both regimes |
| Form 101 (kartis oved) | https://www.gov.il/BlobFolder/service/itc101/he/Service_Pages_Income_tax_annual-report-2024_itc101.pdf | The boxes an employee actually claims credits through |
| ITA havraa-reduction circular 2025-000583 | https://www.gov.il/BlobFolder/dynamiccollectorresultitem/employers-info-140525-1/he/IncomeTax_employers-info-140525-1.pdf | Havraa reduction (418-471.4 NIS), field 011/012 |

## Troubleshooting

See `references/troubleshooting.md`.
