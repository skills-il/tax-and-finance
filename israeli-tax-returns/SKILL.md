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
| 1301 | דוח שנתי ליחיד | Individuals, sole proprietors, freelancers | June 30 for online filers; 29 May 2026 for paper filers (CPA-represented filers get the later quota extension) | Annual |
| 135 | דוח שנתי מקוצר | Salaried individuals filing a short return to claim a refund | Within 6 years of the relevant tax year (Section 160 refund window) | Annual / on demand |
| 1214 | דוח שנתי לחברה | Companies (Chevra Ba'am, Chevra Pratit) | May 31 (5 months after tax year end), extensions available | Annual |
| 126 | דוח מעסיק על משכורות | Employers reporting employee salaries and withholdings | April 30 | Annual |
| 856 | דוח על תשלומים לספקים | Businesses reporting payments to suppliers/freelancers | April 30 | Annual |
| 6111 | דוח כספי אחיד | Businesses with turnover above 300,000 NIS (incl. VAT) | Submitted with 1301 or 1214 | Annual |
| Mikdamot | מקדמות מס הכנסה | Self-employed and businesses with advance payment assessments | 15th of the month after the period | Bi-monthly |
| Mas Shevach | הצהרת מס שבח | Anyone selling real estate in Israel | 30 days from sale date (40 days if requesting exemption) | Per transaction |
| 1322/1325 | דוח רווח הון מניירות ערך | Anyone with capital gains from securities sales | 30 days from sale (or annual with Form 1301) | Per transaction or annual |

Ask the user:
- Which return type do they need?
- Tax year (shnat mas) being reported
- Entity type: individual (yachid), sole proprietor (atzmai), or company (chevra)
- Whether they have a CPA (roeh heshbon) handling submission

### Step 2: Annual Individual Tax Return (Form 1301)

Form 1301 is the main annual income tax return for individuals and non-corporate business owners. It covers all income sources for the calendar year (January 1 to December 31).

**Who must file Form 1301:** (mandatory-filing triggers are set by the Income Tax Regulations (Exemption from Filing a Return), 1988, under Section 131(a) of the Ordinance, a salaried employee is exempt only if they stay under every threshold below)
- Self-employed individuals (osek murshe or osek patur)
- Individuals whose gross salary exceeded 721,560 NIS (the surtax / high-salary mandatory-filing threshold, frozen 2025-2027)
- Individuals with income from multiple employers
- Individuals with foreign income or assets abroad exceeding reporting thresholds (including a foreign securities/brokerage account)
- Anyone who received capital gains during the tax year
- Individuals with rental income above the exempt threshold; in particular, annual residential rent above **375,000 NIS** requires a return even on the 10% track (below that, the 10% track can be settled without a full return)

**Main sections of Form 1301:** personal details; employment income (from Form 106); business/profession income (Appendix Aleph / Form 1320); rental income and chosen track; capital and investment income; foreign income (Appendix 1327); deductions and credits (pension Sections 45A/47, donations Section 46, life insurance); and nekudot zikui (Step 3).

**Key appendices to prepare:**
- Form 1320 (Appendix Aleph): Profit and loss statement for self-employed
- Form 1321: Calculation of non-business taxable income
- Form 1322/1325: Capital gains from securities (see Step 7)
- Form 1327: Foreign income and assets declaration
- Form 1343: Depreciation and amortization schedule
- Form 6111: Standardized financial statements (if turnover > 300,000 NIS, see Step 5)

**Rental income tax tracks:**
Israeli law offers three options for taxing residential rental income:

| Track | Rate | Conditions |
|-------|------|------------|
| Exempt | 0% | Monthly rent below the exempt ceiling (5,654 NIS/month, 2025-2027, frozen, no longer indexed) |
| Flat rate | 10% | On gross rent, no deductions allowed. Payment by January 31 of following year |
| Marginal | Progressive rates (10%-50%) | Full deduction of expenses (depreciation, mortgage interest, maintenance). Filed with Form 1301 |

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
  refunds for tax years 2020-2025.
- If the person has business income, foreign income, capital gains, or crosses
  the mandatory-filing thresholds, they must file the full Form 1301 instead.

### Step 2.6: Havraa-Day Reduction on Form 106 (Fields 011/012, tax years 2024-2025 only)

For tax years 2024 and 2025 ONLY, temporary legislation reduced employees' convalescence pay (dmei havra'a) to help fund Iron Swords reserve-duty benefits: a separate 2024 law, then the חוק הקפאה והפחתה של דמי הבראה (Havraa Freeze-and-Reduction Law) published 27 March 2025 for tax year 2025. It produces a value on the Form 106 and Form 1301 of most salaried filers for those two years. Per Reshut HaMisim circular 2025-000583 (14 May 2025):

- **Amount:** for a full-time employee, one havraa day is reduced, not less than 418 NIS and not more than 471.4 NIS. (A reduced half-day track applies to lower earners, see `references/form-guide.md`.)
- **Where it appears:** Form 106 reports it in field 011/012, "מחיר יום ההבראה שהופחת ממשכורת העובד" (price of the havraa day reduced from the employee's salary). On Form 1301 it appears at line 60, "השתתפות זמנית הפחתת דמי הבראה", printed inside Part יב (the personal-deductions section).
- **It is informational only, NOT a deduction and NOT a credit.** The reduced amount was already netted out of the gross salary reported in field 158, and the employer's participation amount is not income to the employee (per the circular). Do NOT enter field 011/012 as a Part יב deduction or as a tax credit, even though it is printed inside the deductions section of the form. Treating it as a deduction double-counts the benefit and understates tax.
- **Exemption:** a home/domestic employer (an individual employing someone outside a business, for example a household employing a caregiver) is exempt from the reduction.
- **Sunset, resolved as of 27 July 2026: the law was NOT renewed.** Both the freeze and the reduction expired with tax year 2025 and are not in force for 2026, so a 2026 Form 106 should carry no field 011/012 value and a 2026 Form 1301 no line 60 value. If one appears, question it rather than transcribing it.
- **This step is still live work, not history.** Returns for tax years 2024 and 2025 are exactly what is being filed during 2026, so the reduction still has to be handled correctly on the return in front of you. Read the step as scoped to the tax YEAR of the return, not to the year you are filing in.

### Step 3: Nekudot Zikui (Tax Credit Points) Calculation

Each nekudot zikui point reduces the annual tax liability by 2,904 NIS (2025-2027, frozen, approximately 242 NIS/month). Calculate the taxpayer's total points:

| Category | Points | Notes |
|----------|--------|-------|
| Israeli resident (male) | 2.25 | Base entitlement |
| Israeli resident (female) | 2.75 | Base entitlement (0.5 additional) |
| New immigrant (oleh chadash) | 3.0 in year 1, 2.0 in year 2, 1.0 in year 3 | For 3.5 years from aliyah date |
| Returning resident (toshav chozer) | Same as oleh chadash | After 10+ years abroad |
| Child born during tax year | 1.5 | For each child born that year |
| Children aged 1-5 | 2.5 per child | For each child |
| Children aged 6-17 | 1.0 per child | For each child |
| Child aged 18 | 0.5 | Last year of child credit |
| Single parent | 1.0 | Divorced, widowed, or separated with custody |
| Academic degree (BA) | 1.0 | Per year, for up to 3 years matching study duration (graduates 2023+). Graduates 2014-2022: 1 year only |
| Academic degree (MA) | 0.5 | For 2 years after completion (graduates 2023+). Graduates 2014-2022: 1 year only |
| Vocational certificate | 1.0 | Per year, for up to 3 years matching study duration (graduates 2023+). Graduates 2014-2022: 1 year only |
| Disability (100% or blind) | 2.0 | Permanent |
| Combat reserve soldiers | 0.5-1.0 | Based on reserve days (from 2026: 0.5 points for 20+ days, 0.75 for 45+ days, 1.0 for 60+ days) |

**Calculation example:**
A married woman (2.75 points) with two children aged 3 and 7 (2.5 + 1.0 = 3.5 points) = 6.25 total points = 6.25 x 2,904 = 18,150 NIS annual tax reduction.

### Step 3.5: Pension Contribution Credit (Section 45A) and Deduction (Section 47)

Pension contributions receive two separate tax benefits that must both be claimed on Form 1301. Missing either is one of the most common filing errors.

**Section 45A: 35 percent income tax credit (zikui)**
- Reduces tax liability directly by 35 percent of the qualifying pension contribution
- Applies to both employees and self-employed who deposit into a pension fund, insurance policy with a pension component, or kupat gemel l-kitzba
- Employee (sachir) ceiling: qualifying contribution up to 7 percent of eligible salary (capped at 23,232 NIS/month for 2026, so maximum monthly credited deposit is 1,626 NIS).
- Self-employed (atzmai) eligibility: 5.5 percent of business income is the ceiling used for the 45A credit (verify the exact annual figure each year on kolzchut.org.il or pensuni.com before applying to a return)
- Claim on Form 1301 in the credits section, separate line from nekudot zikui

**Section 47: pension deduction (nikui)**
- Reduces taxable income (not tax directly) by the contribution amount
- Self-employed can deduct up to 11 percent of annual business income (capped at the qualifying ceiling)
- Employee contributions above the 7 percent 45A threshold can qualify under Section 47
- Always preferred for high marginal-rate taxpayers; verify whether a self-employed filer benefits more from 45A (credit) or 47 (deduction) based on their marginal bracket

**Combined rule:** the same shekel cannot double-count. Self-employed filers typically structure deposits so that part qualifies for 45A (credit) and part for 47 (deduction) within the 16.5 percent combined ceiling.

**Calculation example (self-employed, 300,000 NIS annual business income):**
- Pension deposit: 33,000 NIS (11 percent of income)
- Section 47 deduction: reduces taxable income by up to 33,000 NIS (marginal benefit depends on bracket)
- Section 45A credit: 35 percent of up to 5.5 percent of income = up to 16,500 NIS eligible, so up to 5,775 NIS direct tax reduction
- Always verify the exact current ceilings at kolzchut.org.il before quoting a number

### Step 3.6: Donation Credit (Section 46)

Donations to a recognized public institution qualify for a tax credit under Section 46 of the Income Tax Ordinance. This is a frequently-missed refund source for salaried filers (often claimed via Form 135).

- **Credit rate:** 35 percent of the eligible donation amount for individuals (companies get the corporate-rate credit). The credit reduces tax liability directly, like nekudot zikui, not taxable income.
- **Recognized institution requirement:** the recipient must hold a valid Section 46 recognition (mosad tziburi mukar lefi seif 46). A donation to a charity without 46 recognition does NOT qualify. Verify the institution's 46 status (the Tax Authority publishes the approved list).
- **Minimum floor: 207 NIS** of total donations in the year (it was 200 NIS in 2023 and 190 NIS in 2020-2022, so an older figure will wrongly disqualify a claim). The floor applies to the COMBINED total of separate donations to Section 46 institutions, not to each donation individually, which is the point most often got wrong: four 60 NIS donations qualify, and treating them one at a time says none do.
- **Ceiling: the lower of 10,354,816 NIS (2026) or 30 percent of the donor's taxable income for that year.** In practice the percentage limb binds for almost everyone. Anything above the ceiling carries forward to the next 3 tax years.
- **Company donors get the credit at the corporate rate (23 percent), not 35 percent.**
- **Documentation:** keep the original donation receipts marked with the institution's 46 recognition; the ITA may require them.
- Figures are indexed; re-check them for the return's tax year.

### Step 3.7: Return-Preparation and Professional Fee Deduction (Section 17(11))

Fees paid to a CPA (roeh heshbon) or tax advisor for preparing the return and handling the tax matter are deductible under Section 17(11) of the Income Tax Ordinance, and are claimable by salaried employees (sachirim), not only the self-employed.

- **What qualifies:** preparing the annual return(s) and handling the tax matter in all assessment (shuma) and appeal (irur) proceedings: return-preparation and CPA / tax-advisor fees, and representation before the pakid shuma and in tax appeals.
- **Salaried vs self-employed:** the deduction is well accepted for filers with business income. For a pure salaried filer it is claimable under 17(11) but is a contested area the assessor may disallow, so document it and have a CPA claim it. Do not flatly tell a salaried filer the fee is non-deductible.
- **Which year:** the fee is deductible in the tax year it was actually paid. A return-preparation fee is usually paid the year AFTER the year the return reports, so it reduces that later year, not the income of the year being filed.
- **Carve-outs:** disallowed for business or profession income where no books (pinkasim) were kept (does not affect salaried filers); legal costs on an objection or appeal found frivolous are disallowed, and any costs awarded to the taxpayer reduce the claim.
- **Placement on Form 1301:** there is no dedicated field for a salaried filer's Section 17(11) deduction, and SHAAM online filing has no free-form attachment for a pure salaried 1301/135, so this deduction usually needs a CPA-assisted filing to be captured. Keep the CPA invoice and attach an explanation. Do NOT reduce field 158 (the gross-salary line), which the Tax Authority cross-checks against Form 106; confirm placement with a CPA.

### Step 4: Income Tax Brackets and Surtax

Apply the progressive income tax rates to taxable income. Brackets for 2026 (brackets 1-2 and 6 frozen at 2025 values; brackets 3-5 expanded by the Economic Efficiency Law 2026 (Amendment 288 to the Income Tax Ordinance), approved March 31, 2026, retroactive to January 1, 2026):

| Bracket | Annual Income Range (NIS) | Rate |
|---------|--------------------------|------|
| 1 | 0 - 84,120 | 10% |
| 2 | 84,121 - 120,720 | 14% |
| 3 | 120,721 - 228,000 | 20% |
| 4 | 228,001 - 301,200 | 31% |
| 5 | 301,201 - 560,280 | 35% |
| 6 | 560,281 and above | 47% |
| Surtax | Above 721,560 | 47% + surtax, see below |

Note the last two rows: 47% applies to every shekel above 560,280 and does not stop at 721,560. The surtax is charged ON TOP of the 47%, which is why the effective top rate is 50% and not 3%.

**Surtax (mas yesafim), two-tier system from 2026:**
- Employment and active income: 3% above 721,560 NIS (effective top rate: 50%)
- Capital and passive income (dividends, interest, rent, capital gains): 5% above 721,560 NIS (3% base + 2% additional surcharge)
- From 2026, Mas Shevach on investment properties is included in the surtax income calculation

**Corporate tax rate:** 23% flat rate on taxable profits for companies (Chevra).

**Closely held companies (Chevra Me'atim):** Subject to a 2% annual tax on accumulated undistributed profits unless at least 6% of accumulated profits are distributed as dividends.

**Self-employed additional levies:** self-employed individuals also pay Bituach Leumi and health tax on business income, calculated separately from the income tax return, though amounts paid during the year may affect advance-payment reconciliation.

### Step 5: Financial Statements Attachment (Form 6111)

Required for any business (individual or corporate) with annual turnover exceeding 300,000 NIS (including VAT).

Form 6111 uses standardized codes to report financial data in a uniform format for the Tax Authority's computerized systems. The form has two main sections:

**Section A (Profit and Loss):** revenue by source, cost of goods/services, operating expenses, financial income and expenses, depreciation, net profit/loss before tax, and tax adjustments (non-deductible expenses, timing differences).

**Section B (Balance Sheet):** current and fixed assets, current and long-term liabilities, and equity (share capital, retained earnings).

**Preparation guidelines:**
- All amounts must be in NIS
- Use the Tax Authority's standardized item codes (available at misim.gov.il)
- Data must match the audited financial statements exactly
- Submit electronically via the SHAAM online portal
- The form is typically prepared by the CPA using accounting software (Hashavshevet, iCount, Rivhit) that supports Form 6111 export

### Step 6: Employer and Supplier Reports (Forms 126 and 856)

**Form 126 (Annual Employer Salary Report):** employers file Form 126 by April 30 summarizing each employee's gross salary, tax withheld, Bituach Leumi and health tax, pension and keren hishtalmut contributions, benefits in kind, and exempt payments such as severance up to the exempt ceiling (dmei havra'a / convalescence pay is taxable salary, not an exempt payment). They must also issue Form 106 (annual salary summary) to each employee by March 1.

**Form 856 (Annual Supplier Payments Report):** businesses report payments to non-employee recipients (freelancers, contractors, consultants, landlords) by April 30, listing each supplier's ID, gross payments, tax withheld at source, and payment type.

See `references/form-guide.md` for the full per-field breakdown of both forms.

### Step 7: Capital Gains Reports

**Real Estate Capital Gains (Mas Shevach):**
When selling real property in Israel, the seller must file a Mas Shevach declaration with Reshut HaMisim (Israel Tax Authority) via the misim.gov.il portal or real estate taxation offices (Misrad Misui Mekarkein) within:
- 30 days from the sale date (standard)
- 40 days from the sale date (if requesting an exemption)

Calculation:

```
Sale price
- Original purchase price (adjusted for inflation via CPI index)
- Allowable deductions (purchase tax paid, legal fees, agent commission, renovation costs with receipts)
= Real capital gain (shevach re'ali)
x 25% tax rate
= Mas Shevach payable
```

**Single apartment exemption (ptur dira yechida):**
Full exemption from Mas Shevach if ALL conditions are met:
- This is the seller's only residential property in Israel
- Owned for at least 18 months
- Sale price is below the exemption ceiling (5,008,000 NIS, 2024-2027, frozen)
- Seller is an Israeli resident
- Partial exemption applies proportionally above the ceiling

**Linear method (shita liniarit):**
For properties purchased before January 7, 2014, only the portion of gain attributable to the period after that date is taxed at 25%. The pre-2014 portion may be exempt or taxed at a lower historical rate. A phase-out of this benefit was proposed by the Ministry of Finance in 2024; not yet enacted into law as of April 2026.

**Securities Capital Gains (Forms 1322/1325):**
Capital gains from selling stocks, bonds, mutual funds, and other securities:
- 25% tax rate for individuals on traded securities
- 30% tax rate if the seller holds 10% or more of the company
- Report within 30 days of the sale, or include in the annual Form 1301
- Losses can offset gains from the same category within the tax year
- Carry forward of capital losses to future years (capital losses only offset capital gains, not ordinary income)

### Step 8: Advance Tax Payments (Mikdamot)

Self-employed individuals and businesses are typically assessed advance income tax payments (mikdamot) by the Tax Authority. These are periodic prepayments against the expected annual tax liability.

**How mikdamot work:**
- The Tax Authority sets a percentage rate based on the business's prior year returns
- Applied to bi-monthly turnover (total revenue excluding VAT)
- Due by the 15th of the month following the bi-monthly period
- New businesses receive a percentage based on industry statistics and projected turnover

**Payment schedule:**

| Period | Months | Payment Due |
|--------|--------|-------------|
| 1 | January - February | March 15 |
| 2 | March - April | May 15 |
| 3 | May - June | July 15 |
| 4 | July - August | September 15 |
| 5 | September - October | November 15 |
| 6 | November - December | January 15 |

**Reconciliation at year-end:**
When filing the annual return (Form 1301 or 1214), the total advance payments made during the year are reconciled against the actual tax liability:
- If mikdamot paid > actual tax: the taxpayer receives a refund (hechzer mas)
- If mikdamot paid < actual tax: the taxpayer owes the difference (plus possible interest)

**Adjusting the rate:** if the business's income changes significantly (revenue drops sharply, a large new contract, or a change in business activity), request a rate adjustment (shinui shiur mikdamot) from the Tax Authority.

### Step 9: Filing via SHAAM Online Portal

All returns are submitted electronically via the Tax Authority's online system (SHAAM):

**Registration:** register at misim.gov.il with a teudat zehut or company number and set up credentials with two-factor. CPAs use their own credentials plus per-client yipui koach.

**Submission:** log in, pick the form and tax year, enter or upload data, review the calculated liability, submit for a confirmation number, then pay via the payment portal (bank transfer, credit card, or post-office reference).

**CPA authorization (yipui koach):** granted by the taxpayer in the SHAAM portal, per client and per year. It lets the CPA submit returns, view assessments, and correspond with the Tax Authority for that client.

**Filing extensions:**
- Form 1301: see Step 1 for the 2025-return deadlines. CPA clients usually get automatic extensions under the association quota agreement, often to 30 September or later
- Form 1214: standard deadline 31 May, extensions available
- Request any extension BEFORE the original deadline

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
8. Result: Net tax due or refund amount, ready for SHAAM submission

### Example 2: Company Filing Corporate Tax Return (Form 1214)

User says: "Our company needs to file the annual report for the most recently closed tax year"

Actions:
1. Gather audited financial statements (profit and loss, balance sheet)
2. Prepare Form 6111 (standardized financial statements attachment)
3. Calculate taxable income: Net profit + non-deductible expenses (fines, entertainment above limits, excess car expenses) - exempt income
4. Apply 23% corporate tax rate
5. Reconcile against advance payments (mikdamot) made during the year
6. Check closely held company rules: if applicable, verify 6% dividend distribution requirement to avoid 2% accumulated profits tax
7. Prepare Form 126 (employer salary report) and Form 856 (supplier payments) as companion filings
8. Submit all forms via SHAAM by May 31

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

### Example 4: Calculating Advance Tax Payments (Mikdamot)

User says: "I started a new consulting business, how much mikdamot should I expect to pay?"

Actions:
1. Determine business type and projected annual turnover
2. For new businesses, the Tax Authority assigns an initial percentage based on industry type and projected income
3. Calculate bi-monthly payment: (bi-monthly revenue) x (assigned percentage rate)
4. Explain the 6 bi-monthly payment dates (March 15, May 15, July 15, September 15, November 15, January 15)
5. Note that the rate can be adjusted mid-year if actual income differs significantly from projections
6. At year end, total mikdamot paid will be reconciled against actual tax liability on Form 1301
7. Result: Estimated bi-monthly payment schedule with option to request rate adjustment

## Bundled Resources

### References
- `references/form-guide.md` - Forms 1301, 1214, 126, 856, 6111, 1322, 1325: who files, deadlines, key fields. Consult for a specific form or to decide which forms apply.
- `references/tax-brackets-credits.md` - 2026 brackets (1-2 and the 47% band frozen at 2025 values, 3-5 widened for 2026), nekudot zikui values and categories, surtax thresholds, corporate rates. Consult for any tax calculation.

## Gotchas
- Form 1301 for tax year 2025, filed in 2026: 30 June online, 29 May on paper. April 30 is a legacy paper baseline, not the online deadline, and April 15 is American. Filers represented by a CPA get later extensions under the CPA-association quota agreement, often 30 September or later.
- Individuals file Form 1301, not a 1040. US form numbers and fields do not exist here.
- Capital gains go on a separate schedule with their own rates (25% financial assets, up to 50% on real estate by holding period and property count). Do not apply one blanket rate.
- Nekudot zikui must be claimed annually and vary by status (marital, children, new oleh, discharged soldier). Do not assume a default count.
- From 2026 Mas Shevach on a non-exempt investment property counts toward surtax income (5% above 721,560 NIS). Treating the two as separate under-reports the liability.
- Return-preparation fees are deductible under Section 17(11) for SALARIED filers too, not only the self-employed. There is no dedicated Form 1301 field: keep the invoice and attach an explanation.
- The havraa-reduction figure on Form 106/1301 (field 011/012, "מחיר יום ההבראה שהופחת ממשכורת העובד", tax years 2024-2025 only) is informational: it was already netted out of gross salary and is not income to the employee. Agents reasoning from the form's visual structure may wrongly treat it as a Part יב deduction and mis-state tax.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Israel Tax Authority (Reshut HaMisim) | https://www.gov.il/en/departments/israel_tax_authority | Forms, filing guides, announcements |
| SHAAM online filing portal | https://www.misim.gov.il | Electronic submission of returns |
| Kol-Zchut income tax brackets | https://www.kolzchut.org.il/he/מדרגות_מס_הכנסה | Current-year bracket thresholds |
| Kol-Zchut tax credit points | https://www.kolzchut.org.il/he/נקודת_זיכוי | Nekudot zikui value and eligibility |
| Kol-Zchut Mas Shevach calculation | https://www.kolzchut.org.il/he/חישוב_מס_שבח | Capital gains, exemptions, linear method |
| Israel Real Estate Taxation office | https://www.gov.il/he/departments/topics/land_taxation | Mas Shevach and Rechisha forms and rates |
| ITA havraa-reduction circular 2025-000583 | https://www.gov.il/BlobFolder/dynamiccollectorresultitem/employers-info-140525-1/he/IncomeTax_employers-info-140525-1.pdf | Havraa reduction (418-471.4 NIS), field 011/012 |

## Troubleshooting

### Error: "Not sure which form to file"
Cause: The user does not know whether they need Form 1301 (individual) or 1214 (corporate), or which additional forms apply.
Solution: Determine the entity type first. Individuals and sole proprietors file 1301. Companies (Chevra) file 1214. Both may also need Forms 126, 856, and 6111 depending on the business activity. Use the table in Step 1 to map the correct forms.

### Error: "Tax calculation does not match expected amount"
Cause: Common mistakes include applying wrong bracket thresholds, forgetting the surtax (mas yesafim) on income above 721,560 NIS, or miscounting nekudot zikui.
Solution: Verify the income is being split across brackets correctly (each bracket applies only to the income within its range). Verify all applicable nekudot zikui are included. Check whether the surtax applies (3% on active income, 5% on passive/capital income above 721,560 NIS). Cross-reference with references/tax-brackets-credits.md for current values.

### Error: "Mas Shevach deadline missed"
Cause: The 30-day (or 40-day) filing deadline from the sale date has passed.
Solution: File immediately. Late filing incurs interest (ribit) and linkage differences (hefsherey hatzamada) on the tax owed, plus potential fines. If requesting an exemption, the 40-day deadline applies. Consult a CPA for penalty mitigation options.

### Error: "Mikdamot rate seems too high"
Cause: The Tax Authority's assessed rate is based on prior year income that may not reflect current business conditions.
Solution: Submit a request to adjust the mikdamot rate (shinui shiur mikdamot) via the SHAAM portal or through the CPA. Provide supporting documentation showing the change in business conditions (lower revenue, business restructuring, etc.).

### Error: "Form 6111 codes not matching accounting software output"
Cause: Different accounting software versions may use outdated standardized codes.
Solution: Verify that the accounting software is updated to the latest Form 6111 specifications from the Tax Authority. Cross-reference the exported codes against the official code list published at misim.gov.il. CPAs can also manually map codes if the software export format differs.
