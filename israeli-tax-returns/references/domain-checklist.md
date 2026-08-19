# Domain coverage checklist: israeli-tax-returns

Bootstrapped 2026-08-19 (v1.9.0). Anchored on the ITA's own collection instruments (Form 101
part ח and Form 1301), the Income Tax Ordinance, and the ITA 2026 deductions booklet, rather
than on a secondary summary.

**Rate-table completeness rule for this skill.** Several items below are multi-row official
tables. A checklist row that names the topic without enumerating its rows is what let the
credit-point schedule ship with three age bands when the statute has six. Where a row says
"full table", the skill must carry or point at every row of the official table.

## Must cover (core)

| Item | Why it is core | Source |
|---|---|---|
| Which form applies (1301, 135, 1214, 126, 856, 6111, 1322/1325, Mas Shevach, mikdamot) and its deadline | The first decision every user makes | ITA forms index |
| Mandatory-filing triggers, **full Regulation 134A table** (all eight ceilings, and Reg. 3(a)(6)-(8) exclusions) | A user under one ceiling and over another still owes a return | Regs (Exemption from Filing a Return) 1988; ITA booklet ch. ג |
| Online-filing exemption s.131(b2)(4), distinguished from the filing exemption itself | Conflating the two tells a filer they need not file at all | ITA booklet ch. ג |
| Income tax brackets, **full table**, current year | Every computation | s.121; ITA booklet ch. ב |
| Surtax s.121B, both the 3% active and 5% capital limbs, and that the 47% band does not stop at the threshold | The most common structural error | s.121B |
| Nekudot zikui, **full schedule** | See the sub-rows below; this is the single largest source of understated refunds | Ordinance ss.34-40C, 45; Form 101 part ח |
| Credit points, children: **all six age bands**, and the mother/father split from age 6 | Form 101 has six separate boxes | ss.66(c)(4), 66(c)(5), 40(b) |
| Credit points, oleh: **54-month window keyed to the aliyah date**, 8.5 points total | Entitlement is not calendar-year based | s.35(a), (c) |
| Credit points, toshav chozer: that s.35 covers **only** the 16.5.2010-30.9.2012 cohort | Otherwise the skill invents an entitlement for every returnee | s.35(d) |
| Credit points, discharged soldier / national service: 2.0 or 1.0 per year for 36 months | Routinely unclaimed; nothing on the return prompts for it | s.39A; Form 101 box 14 |
| Credit points, combat reserve: **both band tables in full**, the 4.0 cap, and that days are counted on the PRECEDING tax year | Two live regimes selected by tax year | s.39B; ITA circular 2025-001368 |
| Credit points, netul yecholet child: 2.0 per child, and its exclusivity with s.44 | A materially large, commonly missed entitlement | s.45(a), (c) |
| Section 44 institution credit: 35% of the excess over 12.5% of taxable income | Distinct mechanism from s.45(a) | s.44 |
| Single-parent, only-parent, split-keep, and mezonot credit points | Form 101 boxes 6, 9, 10, 12 all exist | ss.40(b)(1b), 40(b)(2), 40A |
| Section 45A pension credit and Section 47 pension deduction, with the employee ceiling | Two benefits, both claimable, routinely half-claimed | ss.45A, 47; ITA booklet ch. ג |
| Section 46 donation credit: rate, the **combined** 207 NIS floor, and the ceiling | The floor-per-donation error disqualifies valid claims | s.46 |
| Section 17(11) professional-fee deduction, including for salaried filers | Commonly and wrongly denied to salaried filers | s.17(11) |
| Rental income: the three tracks and the exempt ceiling | Every landlord | s.122; ITA booklet |
| Mas Shevach: computation, single-apartment exemption, linear method | Per-transaction obligation with a 30-day clock | Real Estate Taxation Law |
| Securities capital gains: 25% / 30%, loss offset and carry-forward | Per-transaction and annual | s.91 |
| Mikdamot: rate basis, the six payment dates, year-end reconciliation, rate adjustment | Every self-employed filer | s.175 |
| SHAAM filing mechanics and yipui koach | The delivery step | ITA portal |
| Legal notice, immediately after the H1 in both language files | Regulated-profession gate | legal-review skill |

## Should cover (advanced)

| Item | Source |
|---|---|
| Aliyah / return incentive hora'at sha'a, in force 31.3.2026, five-year exemption ceilings | Economic Efficiency Law 2026 ch. ד |
| Section 11 yishuv mutav: that the rate and ceiling are per-yishuv and change annually, plus the 2026 additions and the mixed-urban 12% track | s.11; ITA booklet ch. ח |
| Education credit points s.40C, including the internship election | s.40C; Form 119 |
| Form 135 short return and the six-year s.160 refund window | s.160 |
| Havraa-day reduction, Form 106 field 011/012, tax years 2024-2025, and that it is informational | ITA circular 2025-000583 |
| Closely held company 2% undistributed-profits tax and the 6% distribution test | s.77 |
| Form 6111 threshold and structure | ITA |
| Spouse-related credit points ss.37, 38, 39 and the separate-computation rules in s.66 | ss.37-39, 66 |

## Out of scope (explicit)

| Item | Rationale | Re-litigated |
|---|---|---|
| VAT reporting | Covered by `israeli-vat-reporting`; a user asking about VAT is routed there by the description's "Do NOT use for" clause | 2026-08-19: still correct, a separate skill exists and is named |
| Withholding tax mechanics | Covered by `israeli-tax-withholding` | 2026-08-19: still correct |
| Payroll computation and payslip construction | Covered by `israeli-payroll-calculator`, which carries the same credit-point table; both must stay in step | 2026-08-19: still correct, and the two tables were reconciled against the statute in this cycle |
| Crypto tax | Covered by `israeli-crypto-tax-reporter` | 2026-08-19: still correct |
| Section 102 employee stock options | Covered by `israeli-stock-options-tax` | 2026-08-19: still correct |
| The full per-yishuv s.11 rate and ceiling list | Roughly 500 rows that change annually; the skill points at chapter ח of the current booklet and tells the agent never to quote a rate from memory. A user WOULD ask "what is my yishuv's rate", and the honest answer is the current official list, not a frozen copy | 2026-08-19: re-opened and re-closed. Capturing it would guarantee staleness within a year; the pointer plus the 2026 changes is the better answer |
| Bituach Leumi and health tax computation for the self-employed | A separate levy with its own base; the skill notes it affects advance-payment reconciliation and stops there | 2026-08-19: still correct |

## Authoritative sources

| Source | URL |
|---|---|
| Income Tax Ordinance (consolidated) | https://www.nevo.co.il/law_html/law00/84255.htm |
| ITA 2026 deductions booklet | https://www.gov.il/BlobFolder/generalpage/income-tax-monthly-deductions-booklet/he/generalInformation_income-tax-monthly-deductions-booklet_monthly-deductions-booklet-2026.pdf |
| ITA circular 2025-001368 (s.39B combat reserve) | https://www.gov.il/BlobFolder/dynamiccollectorresultitem/employers-info161225-1/he/IncomeTax_employers-info161225-1.pdf |
| Form 101 | https://www.gov.il/BlobFolder/service/itc101/he/Service_Pages_Income_tax_annual-report-2024_itc101.pdf |
| Israel Tax Authority | https://www.gov.il/he/departments/israel_tax_authority |
| SHAAM portal | https://www.misim.gov.il |
