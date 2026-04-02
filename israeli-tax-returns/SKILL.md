---
name: israeli-tax-returns
description: Prepare and file Israeli tax returns with Reshut HaMisim. Covers Form 1301 (individual), Form 1214 (corporate), Form 126 (employer salary), Form 856 (supplier payments), Form 6111 (financial statements), mikdamot (advance payments), Mas Shevach (real estate capital gains), and securities capital gains (Forms 1322/1325). Use when user asks about "doch shnati", "tax return Israel", "Form 1301", "Form 1214", "mas hachnasa", "mikdamot", "mas shevach declaration", "capital gains report", "nekudot zikui", "mas yesafim", or "דוח שנתי". Guides income classification, deductions, tax credits, surtax, deadlines, and SHAAM submission. Do NOT use for VAT reporting (use israeli-vat-reporting), withholding tax (use israeli-tax-withholding), crypto tax (use israeli-crypto-tax-reporter), payroll (use israeli-payroll-calculator), or invoicing (use israeli-e-invoice).
license: MIT
allowed-tools: Bash(python:*) WebFetch
compatibility: Works with Claude Code, OpenClaw, Cursor, Windsurf, Codex, GitHub Copilot, opencode, antigravity.
---

# Israeli Tax Returns

## Instructions

### Step 1: Identify the Return Type

Determine which tax return or report the user needs to prepare. Israeli tax law requires different forms for different situations:

| Form | Hebrew Name | Who Files | Deadline | Frequency |
|------|-------------|-----------|----------|-----------|
| 1301 | דוח שנתי ליחיד | Individuals, sole proprietors, freelancers | April 30 (extensions possible via CPA) | Annual |
| 1214 | דוח שנתי לחברה | Companies (Chevra Ba'am, Chevra Pratit) | May 31 (5 months after tax year end) | Annual |
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

**Who must file Form 1301:**
- Self-employed individuals (osek murshe or osek patur)
- Individuals whose gross salary exceeded 721,560 NIS (surtax threshold, 2025)
- Individuals with income from multiple employers
- Individuals with foreign income or assets abroad exceeding reporting thresholds
- Anyone who received capital gains during the tax year
- Individuals who received rental income exceeding the exempt threshold

**Main sections of Form 1301:**

| Section | Content |
|---------|---------|
| Personal details | Name, ID (teudat zehut), address, marital status, dependents |
| Income from employment | Salary, bonuses, benefits-in-kind (from Form 106 provided by employer) |
| Income from business/profession | Revenue, expenses, net profit (from Appendix Aleph / Form 1320) |
| Income from rentals | Residential and commercial rental income, chosen tax track |
| Income from capital and investments | Interest, dividends, capital gains |
| Foreign income | All income sourced outside Israel (Appendix 1327) |
| Deductions and credits | Pension contributions (Section 47), donations (Section 46), life insurance |
| Nekudot zikui (tax credit points) | See Step 3 for full calculation |

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
| Academic degree (BA) | 1.0 | For one year after completion |
| Academic degree (MA) | 0.5 | For one year after completion |
| Vocational certificate | 1.0 | For one year after completion |
| Disability (100% or blind) | 2.0 | Permanent |
| Combat reserve soldiers | 0.5-1.0 | Based on reserve days (from 2026: 0.5 points for 20+ days, 0.75 for 45+ days, 1.0 for 60+ days) |

**Calculation example:**
A married woman (2.75 points) with two children aged 3 and 7 (2.5 + 1.0 = 3.5 points) = 6.25 total points = 6.25 x 2,904 = 18,150 NIS annual tax reduction.

### Step 4: Income Tax Brackets and Surtax

Apply the progressive income tax rates to taxable income. Brackets for 2026 (brackets 1-2 and 6 frozen at 2025 values; brackets 3-5 expanded by the Economic Efficiency Law 2026, approved March 30, 2026, retroactive to January 1, 2026):

| Bracket | Annual Income Range (NIS) | Rate |
|---------|--------------------------|------|
| 1 | 0 - 84,120 | 10% |
| 2 | 84,121 - 120,720 | 14% |
| 3 | 120,721 - 228,000 | 20% |
| 4 | 228,001 - 301,200 | 31% |
| 5 | 301,201 - 560,280 | 35% |
| 6 | 560,281 - 721,560 | 47% |
| Surtax | Above 721,560 | See below |

**Surtax (mas yesafim), two-tier system from 2026:**
- Employment and active income: 3% above 721,560 NIS (effective top rate: 50%)
- Capital and passive income (dividends, interest, rent, capital gains): 5% above 721,560 NIS (3% base + 2% additional surcharge)
- From 2026, Mas Shevach on investment properties is included in the surtax income calculation

**Corporate tax rate:** 23% flat rate on taxable profits for companies (Chevra).

**Closely held companies (Chevra Me'atim):** Subject to a 2% annual tax on accumulated undistributed profits unless at least 6% of accumulated profits are distributed as dividends.

**Self-employed additional levies:**
In addition to income tax, self-employed individuals pay Bituach Leumi (National Insurance) and health tax on their business income. These are calculated separately and are not part of the income tax return itself, but the amounts paid during the year may affect advance payment reconciliation.

### Step 5: Financial Statements Attachment (Form 6111)

Required for any business (individual or corporate) with annual turnover exceeding 300,000 NIS (including VAT).

Form 6111 uses standardized codes to report financial data in a uniform format for the Tax Authority's computerized systems. The form has two main sections:

**Section A: Profit and Loss Statement**
- Revenue by source type (sales, services, other income)
- Cost of goods sold / cost of services
- Operating expenses (salaries, rent, utilities, professional services)
- Financial expenses and income
- Depreciation and amortization
- Net profit / loss before tax
- Tax adjustments (non-deductible expenses, timing differences)

**Section B: Balance Sheet**
- Current assets (cash, receivables, inventory)
- Fixed assets (equipment, vehicles, real estate)
- Current liabilities (payables, short-term loans, accrued expenses)
- Long-term liabilities (loans, mortgages)
- Equity (share capital, retained earnings)

**Preparation guidelines:**
- All amounts must be in NIS
- Use the Tax Authority's standardized item codes (available at misim.gov.il)
- Data must match the audited financial statements exactly
- Submit electronically via the SHAAM online portal
- The form is typically prepared by the CPA using accounting software (Hashavshevet, iCount, Rivhit) that supports Form 6111 export

### Step 6: Employer and Supplier Reports (Forms 126 and 856)

**Form 126 (Annual Employer Salary Report):**
Employers must file Form 126 summarizing all employee compensation and withholdings for the tax year.

| Field | Description |
|-------|-------------|
| Employee details | ID number (teudat zehut), name, start/end dates |
| Gross salary (sachar bruto) | Total annual compensation per employee |
| Tax withheld (mas shenukah) | Income tax deducted at source |
| Bituach Leumi withheld | Employee's National Insurance contribution |
| Health tax withheld | Employee's health insurance contribution |
| Pension contributions | Employee and employer pension contributions |
| Keren Hishtalmut | Employee and employer training fund contributions |
| Benefits in kind | Car, phone, meals, other taxable benefits |
| Exempt payments | Severance (pitzuim), convalescence pay (dmei havra'a) |

Deadline: April 30 of the following year. Must also issue Form 106 (annual salary summary) to each employee by March 1.

**Form 856 (Annual Supplier Payments Report):**
Businesses must report payments to suppliers and service providers exceeding the reporting threshold.

| Field | Description |
|-------|-------------|
| Supplier details | ID/company number, name, address |
| Total payments | Gross amount paid during the year |
| Tax withheld | Amount withheld at source (nikui mas bemakor) |
| Payment type | Services, goods, rent, commissions, etc. |

Deadline: April 30 of the following year. Required for payments to freelancers, contractors, consultants, landlords, and other non-employee recipients.

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

**Adjusting the rate:**
If the business's income changes significantly, request a rate adjustment (shinui shiur mikdamot) from the Tax Authority. This is common when:
- Revenue drops substantially compared to prior year
- A new large contract significantly increases revenue
- The business type or activity changes

### Step 9: Filing via SHAAM Online Portal

All returns are submitted electronically via the Tax Authority's online system (SHAAM):

**Registration and access:**
1. Register at the Tax Authority website (misim.gov.il) with ID number (teudat zehut) or company number
2. Set up digital credentials (username + password + two-factor authentication)
3. CPAs use their own credentials with authorization (yipui koach) for each client

**Submission workflow:**
1. Log in to SHAAM portal
2. Select the relevant form and tax year
3. Enter data or upload from accounting software
4. The system validates data and flags errors
5. Review the calculated tax liability
6. Submit electronically (receive confirmation number)
7. Pay any tax owed via the payment portal (bank transfer, credit card, or reference number at post office bank)

**CPA authorization (yipui koach):**
- The taxpayer grants power of attorney to the CPA via the SHAAM portal
- The CPA can then submit returns, view assessments, and communicate with the Tax Authority on behalf of the client
- Authorization is per-client, per-year

**Filing extensions:**
- Individual returns (Form 1301): standard deadline April 30, CPA clients typically receive automatic extensions through the CPA association's agreement with the Tax Authority (usually extending to September 30 or later, based on quota system)
- Company returns (Form 1214): standard deadline May 31, extensions available
- Extension requests must be filed before the original deadline

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

User says: "Our company needs to file the annual report for tax year 2025"

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
- `references/form-guide.md` - Overview of all Israeli tax forms covered by this skill, including form numbers, who must file, deadlines, and key fields. Covers Forms 1301, 1214, 126, 856, 6111, 1322, 1325. Consult when the user asks about a specific form or needs to determine which forms apply to their situation.
- `references/tax-brackets-credits.md` - Current income tax brackets (2025, frozen through 2027), nekudot zikui point values and eligibility categories, surtax thresholds, and corporate tax rates. Consult for any income tax calculation or when verifying tax credit point entitlements.

## Gotchas
- Israeli annual tax returns (doch shnati) have a standard deadline of April 30 for all filers, with May 31 for electronic/double-entry filing. Self-employed with CPA representation get extensions via the CPA association agreement with the Tax Authority (typically September 30). Agents may use the US April 15 deadline.
- Israeli tax returns use Form 1301 for individuals, not 1040. Agents may reference US form numbers and fields that do not exist in the Israeli system.
- Capital gains in Israel are reported on a separate schedule and may have different rates (25% for financial assets, up to 50% for real estate depending on holding period and property count). Agents may apply a single capital gains rate.
- Tax credit points (neku'dot zikui) must be claimed annually and vary by personal status (marital, children, new oleh, discharged soldier). Agents may use a default value without checking eligibility.

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
