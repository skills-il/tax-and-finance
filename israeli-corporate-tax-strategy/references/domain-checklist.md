# Domain Coverage Checklist: Israeli Corporate Tax Strategy

Scope: how a controlling shareholder of an Israeli company extracts value from it, and what each
route costs in tax. Not company formation, not annual filing, not VAT compliance.

## Must cover (core)

| Item | Why it is core | Status |
|---|---|---|
| Standard corporate tax rate, 23% | s.126(a) of the Ordinance; the base layer of every dividend comparison | Covered, Step 2 |
| Encouragement-Law benefit tracks, all five rate sets | A company on a benefit track pays 5% to 16%, not 23%. Modelling it at 23% roughly doubles the corporate layer. PFE s.51טז, SPFE s.51כא, PTE and SPTE s.51כה | Covered, Step 1b and references/tax-rates-2026.md |
| Qualifying-income and nexus limits on the benefit rates | The reduced rate never applies to the whole profit; non-qualifying income stays at 23% and technology tracks are limited to Israel-developed IP | Covered, Step 1b rule 1 |
| Dividend rate out of benefit-track profits, 20% | s.51יח and s.51כו(1) displace s.125B, so the 25%/30% holding split does not apply to this income | Covered, Step 1b and Step 8 |
| Reduced 4% dividend rate to a qualifying foreign company | s.51כו(2); the single largest remaining rate the skill could omit for foreign-held tech companies | Covered, Step 1b rule 2 |
| Temporal cohort selection for benefit entitlement | Amendment 68 transitional s.39. Entitlement follows the approval or election date, not the tax year. A pre-2011 מפעל מוטב or מפעל מאושר is on a different schedule and the skill would otherwise answer it confidently and wrongly | Covered, Step 1b rule 3 and references/tax-rates-2026.md |
| Superseded Preferred Enterprise rate tables | 2011-2012, 2013, 2014-2016 and the 15% dividend rate to 2017; needed for an assessment, objection, or restatement of an earlier year | Covered, references/tax-rates-2026.md |
| Dividend rates by holding percentage, 25% and 30% | s.125B; the controlling-shareholder split is the most-missed ordinary-company rate | Covered, Step 3 |
| Surtax, threshold and both limbs, measured separately | s.121B(a) 3% on total income plus s.121B(a1) 2% on capital income alone above 721,560 (Amendment 276; ITA execution instruction 5/2025 ex. 3.2). Sharing the threshold with salary overstates the 2% | Covered, Step 3 and scripts/tax_comparison.py calc_surtax |
| Income tax brackets, current year | Drives the salary side of every comparison | Covered, Step 4 |
| Bituach Leumi rates, controlling shareholder vs regular employee, and the ceiling | Controlling-shareholder rates differ on BOTH sides (employee 1.02/6.79, employer 4.46/7.38; BTL column 2); the ceiling changes the breakeven | Covered, Step 4 |
| Controlling shareholder excluded from unemployment insurance | Otherwise the skill overstates what the NI premium buys | Covered, Step 4 |
| Section 3(tet) deemed interest rate and 3(yod) | The cost of the loan route | Covered, Step 5 |
| Section 3(tet1) automatic reclassification deadline and cascade | End of the tax year following withdrawal, not 90 days. Amendment 235, Circular 7/2017 | Covered, Step 5 |
| Section 3(tet1) use-of-asset limb | A deemed withdrawal accrues with no cash loan at all | Covered, Step 8 and Gotcha 10 |
| Section 62A look-through for personal-services companies, all three routes | Where it applies the whole comparison is moot. Controlling-holder test (s.75B(a)(3)), s.62A(a)(1) 25% client exit, 70%/22-of-36-months one-client rule with the 4-employee exclusion, s.62A(a1) 25% margin with the 30M and 750k exclusions | Covered, Step 1a and references/tax-rates-2026.md |
| Trapped-profits 2% surcharge (ss.81A-81F), the 750k shield, and all three exits (6%, 50%, 10% loss) | The exits, not the 2%, are the planning lever; only a dividend whose tax was paid counts. Circular 7/2025 and update 1 | Covered, Step 8 and references/tax-rates-2026.md |
| Withholding deposit date and monthly return | Regs. 13 and 14(a) of the 2005 deduction regulations: the 16th, on Form 0102. The 15th is the superseded pre-2018 date and the Bituach Leumi date | Covered, Step 8 |
| Management fees, VAT and s.85A transfer pricing | The fourth extraction route; modelled in the script as analyze_management_fees() since v1.4.0 | Covered, Step 6 and scripts/tax_comparison.py |
| Family Company election, s.64A | Collapses the corporate layer entirely. Election only within 3 months of incorporation; withdrawal by a month before the tax year, no re-election | Covered, Troubleshooting |
| Non-resident shareholder and treaty override | Domestic 25%/30% is not the answer for a foreign holder | Covered, Step 8 |
| Section 126(b) inter-company dividend exemption | Holding-company structures differ from the single-tier model | Covered, Step 8 |

## Should cover (advanced)

| Item | Status |
|---|---|
| Section 77 deemed-distribution risk on accumulated earnings | Covered, Step 8 |
| Section 32(9) as a reasonableness ceiling rather than a salary floor | Covered, Step 8 |
| Bituach Leumi minimum for a zero-salary controlling shareholder | Covered, Step 8 |
| Pension and keren hishtalmut ceilings on the salary route | Covered, references/tax-rates-2026.md |
| Companies Law ss.301-303 profit and solvency tests for a distribution | Covered, Step 8 |

## Out of scope (explicit)

| Item | Rationale | Reviewed |
|---|---|---|
| Detailed eligibility tests for each Encouragement-Law track (R&D spend, headcount, group revenue, Innovation Authority approvals) | The skill's job is to price the extraction once the applicable corporate rate is known. Eligibility is a determination a company already has or does not have, made with its CPA and the Innovation Authority, not something a user can self-assess here. The four gate questions in Step 1b are enough to route a user who does not know their status to ask. | 2026-10-01 |
| Pre-2011 Approved Enterprise alternative-benefits track (מסלול הטבות חלופי) rate schedule | A shrinking cohort whose rates depend on the individual approval document rather than a published table, so the skill cannot state a rate for them. Step 1b rule 3 routes them out explicitly rather than answering. | 2026-10-01 |
| Capital gains on sale of a beneficial intangible asset (s.51כז) | An IP-migration transaction, not a profit extraction. `israeli-company-valuation` covers the valuation side. | 2026-10-01 |
| Tax treaty rate tables for non-resident shareholders | Per-country and changes independently of Israeli law. The skill flags that a treaty overrides and routes to the treaty. | 2026-10-01 |
| Payroll mechanics, VAT returns, annual return filing | Separate skills, named in the description's Do NOT list. | 2026-10-01 |

## Authoritative sources

| Source | URL |
|---|---|
| Law for Encouragement of Capital Investments, 5719-1959 | https://www.nevo.co.il/law_html/law01/p181_001.htm |
| Income Tax Ordinance | https://www.nevo.co.il/law_html/law00/84255.htm |
| Income Tax Regulations (Deduction from Interest, Dividend and Certain Gains), 5766-2005 | https://www.nevo.co.il/law_html/law01/999_549.htm |
| Bituach Leumi contribution rates, employees | https://www.btl.gov.il/Insurance/Rates/Pages/%D7%9C%D7%A2%D7%95%D7%91%D7%93%D7%99%D7%9D%20%D7%A9%D7%9B%D7%99%D7%A8%D7%99%D7%9D.aspx |
| Israel Tax Authority | https://www.gov.il/he/departments/israel_tax_authority |
