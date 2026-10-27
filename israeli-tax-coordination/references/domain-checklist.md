# Domain Coverage Checklist: israeli-tax-coordination

Generated: 2026-10-27 via research on: gov.il (Tax Authority service page "עריכת תיאום מס באופן מקוון", Tax Authority guide "מדריך מס הכנסה להגשת בקשה להקלה במס ולתיאום מס", notice of 30.03.2026), the ITA 2026 and 2025 monthly deductions booklets, Form 101 (edition updated 11.2025) and Form 116 (edition updated 12.2024) as linked from gov.il, the Bituach Leumi 2026 employer letter (בל/651), kolzchut.org.il (תיאום מס הכנסה, החזר דמי ביטוח לאומי ודמי ביטוח בריאות לשכירים, נקודות זיכוי ממס הכנסה).

Aggregator sweep (Step A): the kolzchut "תיאום מס הכנסה" page (target population, process, certificates, renewal, FAQ) was swept in full in a browser. A CPA-firm category page was searched for; the search surfaced news items, a payroll-vendor clarification (malam-payroll) and the BTL employer letter rather than a CPA firm's own guide. The BTL letter was adopted as a primary source; news items were not used for any figure.

## Must cover (core)

- [x] Who needs coordination: income from more than one payer in the same tax year, including non-overlapping periods (maternity pay then work, unemployment pay then work), salary plus pension, several pension payers. Source: gov.il service page; kolzchut FAQ.
- [x] What happens without it: the non-main payer withholds maximal tax, 47%, with no credit points (Form 101 notes 7 and 8; gov.il guide). Partial salary withheld at the maximal rate unless it is the only income (Form 101 note 4).
- [x] Form 101 section ה: the one payer that gets credit points and brackets, and the declaration of other income. Section ט box 3 (certificate attached). Without coordination the general consequence is notes (7)-(8): the other payers withhold maximal tax. The referral to the assessing officer for not marking "no other income" applies only to the s.9(5) blind/disabled employee (section ח item 2א).
- [x] Which payer should hold the credit points (structural reasoning from the bracket table: the larger regular payer minimises withholding when there is no certificate).
- [x] 2026 bracket table IN FULL, monthly and annual (after the bracket-widening law): 10% to 7,010; 14% to 10,060; 20% to 19,000; 31% to 25,100; 35% to 46,690; 47% above. Annual 84,120 / 120,720 / 228,000 / 301,200 / 560,280. Source: ITA 2026 booklet ch. ב.
- [x] Temporal dimension (C.1a): section 121 amended 31.3.2026 with effect from 1.1.2026. The 2025 table (20% to 16,150, 31% to 22,440, annual 193,800 / 269,280) still governs tax year 2025 and explains early-2026 payslips computed before the change. Both tables enumerated. Source: ITA 2025 and 2026 booklets.
- [x] Surtax (section 121B): 3% above 721,560 a year / 60,130 a month, same in 2025 and 2026; an employer paying above 60,130 a month withholds it on that salary. Consequence: two payers each below 60,130 under-withhold the surtax on combined income.
- [x] Credit point value: 242 NIS a month in 2025 and 2026; basic points 2.25 for a man, 2.75 for a woman (s.34, s.36, s.36A), plus the reliefs below.
- [x] Filing path: free online service (current year only, no income ceiling, unlimited updates) vs Form 116 at the assessing office for the four excluded groups (eligibility age without kibua zchuyot, 9+ income sources, early medical withdrawal from a kupat gemel, kibbutz residents).
- [x] Documents: deductions-file numbers, payslip per payer, BL payment proof for unemployment or maternity, BL employer-continuity confirmation for a gap, Form 161 for pensioners without an exemption percentage, kibua zchuyot approval.
- [x] The certificate: one per payer, given to each payroll, valid to 31.12 of the tax year, a change in data needs a new coordination, extension letters in the personal area, turnaround immediate or a few business days.
- [x] 2026 transition: the 30.03.2026 notice (threshold 193,800, extension of 2025 coordinations to 13.5.2026) and the later guide text (income above 193,800 must coordinate for 2026; existing 2026 coordinations corrected by the ITA).
- [x] Recovering past over-withholding: mid-year coordination refunds through the next payslip; after the year, a refund request up to 6 years back (sibling `israeli-employee-tax-refund`).
- [x] Bituach Leumi is separate: tax coordination does not update BL. BL coordination thresholds 7,703 (main employer below) and 51,910 (total above), certificate letter from the BL website, Form בל/644 without internet, secondary employer deducts full rate otherwise, prior years up to 7 years, BL does not initiate.
- [x] Basic credit points by gender (round 1): 2.25 for a man (s.34 two points + s.36 a quarter), 2.75 for a woman (s.36A half a point). Source: Income Tax Ordinance on nevo. The script requires --points or --gender.
- [x] Relief categories claimed at ONE payer (Form 101 section ח and the online "בקשת הקלה בניכויי המס"): children, single parent, disabled child (item 11), oleh (item 4), qualifying settlement (item 3, Form 1312א), degree or vocational studies (item 15, Form 119), discharged soldier or national service (item 14), alimony, donations, combat reservist (item 16). Children's values are tabulated from s.66(ג)(4)-(5) (Nevo) and kolzchut (2026 examples); the booklet has no per-category point table, only the 242 value. Other categories: take the value from the section the category names.
- [x] Combat reservist s.39B (Amendment 283, published 23.11.2025): half a point for 30-39 days, three quarters for 40-49, one point for 50+, plus a quarter per 5 further days, max 4, in the tax year after service. Source: nevo s.39B, 2026 booklet item 5.
- [x] Months per payer and sequential payers: annual liability vs month-by-month withholding; no x12 unless all payers pay all year (round 1, arithmetic review).
- [x] Rule: in each month the credit points and brackets sit at the largest payer paying in that month; on equal pay they stay where they are; every switch means a new Form 101 (main job ends, larger job starts; includes a payer with its own documented rate) (Form 101: changes declared within a week; section ז).
- [x] Payslip refund only while the over-withholding payer still pays; otherwise a refund request after the year.
- [x] Self-help only: the skill never files, never acts as representative (the online system allows authorising a מייצג; that is a licensed role), never drafts an objection.

## Should cover (advanced / edge cases)

- [x] High earner where the main payer is already in the 47% bracket: coordination saves little and the combined surtax is under-withheld (worked example 2).
- [x] Taxable stipend counts as other income (Form 101 note 1); an exempt BL allowance and a fully exempt survivors pension are not reported (note 6).
- [x] Form 101 note 3: the employee chooses which workplace counts as the "additional job".
- [x] Coordination rate is not final; the final tax is fixed by an annual return if one is filed.
- [x] Form 101 pay categories (notes 2-5) and the 2026 daily table (280.40 / 402.40 / 760.00 / 1,004.00 / 1,867.60, 47% above) for שכר עבודה.
- [x] Form 101 section ט boxes 1-3.
- [x] Pension s.9A exempt share: 2026 ceiling 9,430/month, exemption 5,422 at 57.5%; 57% 2025, 62.5% 2027, 67% from 2028; קיבוע זכויות on Form 161ד. Script takes taxable pay only.
- [x] s.9(5) blind/disabled: Form 101 section ח item 2א referral to the assessing officer. Ceilings for a disability set for 365+ days (2026): 684,000 for a blind or disabled person entitled to a monthly benefit under the Disabled Persons law or the hostile-action victims law (s.9(5)(א); booklet footnote); 445,200 for a blind or disabled person NOT entitled to it, a disabled person needing 90%+ with 40%+ from one impairment (s.9(5)(א1)); 185-364 days a much lower ceiling. Estimator not applied.
- [x] Olim / veteran returning residents arriving 5/11/2025-31/12/2026: temporary-order exemption, 600,000 for 2026; circular pending. Estimator not applied.
- [x] Qualifying settlement: rate on income up to a per-locality ceiling, given by the relief-holding payer; 2026 list changes. Estimator not applied.
- [x] Stipends s.9(29) (nevo): a student's stipend during the studies with no consideration is exempt and is not a payer (study period capped at four tax years for a master's, eight for a doctorate, 12 years for a researcher); a researcher's is exempt up to 109,000 a year in 2026 (booklet); a stipend for a service or role is consideration, taxable, and a payer.
- [x] Child credit points for parents in a couple (s.66(ג)(4) mother, s.66(ג)(5) father; nevo): 2.5 birth year, 4.5 years turning 1-2, 3.5 year turning 3, 2.5 years turning 4-5, then 2 (mother) / 1 (father) from 6 to the year before maturity, 0.5 to the mother in the maturity year. Single parents s.40(ב)(1) routed.
- [x] Reserve-duty pay with several employers: the non-main part is a personal claim paid by BL after income-tax deduction (kolzchut), so BL is another payer.
- [x] Qualifying-settlement list: chapter ח of the 2026 booklet.
- [x] With an open income-tax file, the coordination is handled at that file's office; otherwise the office of the residence area.

## Out of scope (explicit, with rationale)

- Refund for closed tax years. Users ask; the answer is the refund request, handled by `israeli-employee-tax-refund`.
- Withholding on freelancer / osek invoices and micro-business coordination. Handled by `israeli-tax-withholding`.
- Full annual income-tax return. `israeli-tax-returns`.
- Gross-to-net payroll of a single job, pension and keren hishtalmut deductions. `israeli-payroll-calculator`.
- Point VALUES per non-child category (children are tabulated). The skill takes the user's total and points to the Ordinance section the category names (e.g. s.39B for reservists) or kolzchut; the booklet carries only the 242 point value.
- Shift-work credit (s.10). Not on Form 101 section ח; deferred.
- Pension-contribution credits and deductions, benefits in kind. Payslip figures will differ; stated in the skill.
- BL dues rates per column (בל/651 table). The skill flags the coordination and routes; it does not compute BL dues.

## Known bad figures (do not regress)

- Old 2026 tables on commercial sites and news: 20% up to 16,150 and 31% up to 22,440 are the 2025 table. The 2026 booklet shows 19,000 and 25,100.
- Kolzchut "תיאום מס הכנסה" still shows the 2025 extension as 13.04.2026 (non-pensioners) and 13.05.2026 (pensioners); the later gov.il notice set 13.5.2026 for all. Both have passed.
- The 30.03.2026 notice prints "193,800 אלף ₪"; the figure is 193,800 NIS (it equals the 2025 annual top of the 20% bracket).

## Authoritative sources

- https://www.gov.il/he/service/tax-coordination-online (online service, exclusions, certificates)
- https://www.gov.il/he/departments/guides/income-tax-guide-for--tax-relief-and-tax-coordination (47% rule, Form 116, documents, validity)
- https://www.gov.il/he/pages/sa300326-2 (30.03.2026 notice)
- https://www.gov.il/BlobFolder/generalpage/income-tax-monthly-deductions-booklet/he/generalInformation_income-tax-monthly-deductions-booklet_monthly-deductions-booklet-2026.pdf (2026 tables)
- https://www.gov.il/BlobFolder/generalpage/income-tax-monthly-deductions-booklet/he/generalInformation_income-tax-monthly-deductions-booklet_monthly-deductions-booklet-2025.pdf (2025 tables)
- https://www.gov.il/BlobFolder/service/itc101/he/Service_Pages_Income_tax_annual-report-2024_itc101.pdf (Form 101)
- https://www.gov.il/BlobFolder/service/tax-coordination-online/he/Service_Pages_Income_tax_annual-report-2024_itc116-2024.pdf (Form 116)
- https://www.btl.gov.il/Insurance/HozrimBituah/Hozrim/%d7%90%d7%99%d7%92%d7%a8%d7%aa%20%d7%9c%d7%9e%d7%a2%d7%a1%d7%99%d7%a7%20%d7%9c%d7%a9%d7%a0%d7%aa%202026.pdf (BL coordination)
- https://www.nevo.co.il/law_html/law00/84255.htm (Income Tax Ordinance: s.9(5), 9(29), 34, 36, 36A, 39B, 40, 66)
- https://www.kolzchut.org.il/he/%D7%A0%D7%A7%D7%95%D7%93%D7%95%D7%AA_%D7%96%D7%99%D7%9B%D7%95%D7%99_%D7%9E%D7%9E%D7%A1_%D7%94%D7%9B%D7%A0%D7%A1%D7%94_%D7%9C%D7%94%D7%95%D7%A8%D7%94_%D7%9C%D7%99%D7%9C%D7%93_%D7%A2%D7%93_%D7%92%D7%99%D7%9C_5 (Kol-Zchut child credit points, updated 11.2.2026: schedule from 2024, 2026 examples)
