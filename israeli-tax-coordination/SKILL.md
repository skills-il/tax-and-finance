---
name: israeli-tax-coordination
description: "Not tax advice. Mid-year Israeli tax coordination (teum mas, תיאום מס) for a salaried person with two or more payers, such as two jobs, salary plus pension, or salary plus a taxable Bituach Leumi payment (maternity, unemployment) or stipend. Recommends which payer gets the credit points on Form 101, estimates the over-withholding when the second payer withholds 47% versus the annual liability on the 2026 brackets, routes to the free online service or Form 116 at the assessing office, and flags the separate Bituach Leumi coordination. Can stop months of excess withholding. Use when someone has a second job or pension, asks about תיאום מס, Form 101 credit points, or 47% tax on a second salary. Do NOT use for refunds for past years (israeli-employee-tax-refund), freelancer or osek withholding (israeli-tax-withholding), annual returns (israeli-tax-returns), or net salary of a single job (israeli-payroll-calculator)."
license: MIT
allowed-tools: Bash(python:*) WebFetch
compatibility: "Works on every agent. The helper script needs a shell; agents without one use the inline tables and worked examples in Step 5."
---

# Israeli Tax Coordination (Teum Mas)

## Legal notice

This is a free information tool operated by an AI model. It explains the tax-coordination rules and helps you organise your own figures. All of its outputs are produced automatically by an AI model, with no involvement, review, or approval by a tax adviser or accountant. The output is not a tax opinion, not a coordination request prepared or filed by a licensed representative, and not professional advice, but a general calculation and explanation only: it does not examine the full extent of your income or your complete documents. An AI model may err, omit data, or present a wrong conclusion.

The tool does not file anything and does not act on your behalf before the Tax Authority. Responsibility for reporting and for paying the tax is yours, the binding computation is the Tax Authority's, and representation before the Tax Authority is reserved to those permitted by law. This tool is not a substitute for advice that takes account of the particular circumstances and needs of each person. Consult a tax adviser or accountant before filing or paying. All use of its output is the user's sole responsibility.

## Problem

Israelis with two jobs, a salary and a pension, or a salary and maternity or unemployment pay often see 47% income tax taken from the second payment. Each payer withholds as if it were the only one, and the one that does not hold the credit points must take the maximal rate. Tax coordination fixes this during the year, for free, but people do not know it exists, which payer should get the credit points, or what to do with the certificates.

## Instructions

### Step 1: Confirm this is the right skill

This skill handles the **current tax year** for a **salaried** person (or pensioner) with income from more than one payer. Route elsewhere when:

| Situation | Skill |
|---|---|
| Over-withholding in a year that already ended | `israeli-employee-tax-refund` |
| Freelancer or osek, withholding on invoices | `israeli-tax-withholding` |
| Needs a full annual income-tax return | `israeli-tax-returns` |
| Net salary of one job, payslip deductions | `israeli-payroll-calculator` |

Coordination is for the current year only. If the tax turns out higher than needed after the year ends, a refund request can be filed up to six years back from the end of the tax year (gov.il service page).

### Step 2: Collect the payers

For each payer ask for: payer type (employer, pension payer, Bituach Leumi), monthly gross, **which months it pays in this tax year**, and the deductions-file number (מספר תיק ניכויים) from the payslip.

Count as a payer:
- A second job, even if the jobs did not overlap in time. Maternity pay at the start of the year followed by work, or unemployment pay followed by a new job, both require coordination (kolzchut).
- A pension. Pensioners with salary, or with several pension payers, need coordination. Only the taxable part counts: a "qualifying pension" (קיצבה מזכה) has an exempt share under s.9A, in 2026 up to 5,422 NIS a month at 57.5% of a 9,430 NIS ceiling (ITA booklet), and the rate rises to 62.5% in 2027 and 67% from 2028. The exemption is fixed through קיבוע זכויות (Form 161ד); pensioners at eligibility age without it cannot use the online system (Step 6).
- Taxable BL payments that replace salary. Form 101 states that maternity pay and unemployment pay are taxable income; the gov.il guide asks to report BL payments that are taxable.
- A stipend, only if it is taxable. Under s.9(29) of the Ordinance a stipend given to a **student** during the study period, with no consideration from the student, is exempt, so it is **not a payer** for coordination. The exempt study period is the institution's, but no more than four tax years from the start of a master's degree and eight from the start of a doctorate (s.9(29)); after that the stipend is taxable. A **researcher's** stipend (research period up to 12 years) is exempt only up to a ceiling, 109,000 NIS a year in 2026 (ITA booklet); the part above it counts. A stipend given in return for a service or a role (s.9(29) defines that as consideration, for example teaching) is not exempt and IS a payer. Form 101 note (1) defines "מלגה" broadly, as a grant, prize or exemption from payment to a student or researcher.

- Reserve-duty pay with several employers: the pay for the main employer's salary comes through that employer; for the other employers' salary the reservist files a personal claim with BL, and BL pays it after deducting income tax (kolzchut). That BL payment is another payer in the same tax year: list it in the coordination.

Do not count an exempt BL allowance or a fully exempt survivors pension (Form 101 note 6).

### Step 3: Collect the credit points and reliefs

Ask for gender and every status below. Do not default to one number.

- **Basic points:** a resident gets two points (s.34) plus a quarter point (s.36), so **2.25 for a man**, and a woman gets another half point (s.36A), so **2.75 for a woman** (Income Tax Ordinance).
- **Additional reliefs** are claimed in Form 101 section ח and in the online request ("בקשת הקלה בניכויי המס"): children, single parent, child with disabilities receiving גמלת ילד נכה, new immigrant, resident of a qualifying settlement (Form 1312א), academic degree or vocational studies (Form 119), discharged soldier or national-service graduate, alimony to a former spouse, donations, and combat reserve duty.
- **Combat reserve duty (s.39B, Amendment 283, published 23.11.2025):** points in the tax year after the service year: half a point for 30 to 39 days, three quarters for 40 to 49, one point for 50 or more, plus a quarter point for every further 5 days, capped at 4 points. Form 101 section ח item 16 takes the days served in the previous tax year with an IDF confirmation.
- **Children (parents in a couple, Ordinance s.66(ג)(4) for the mother and s.66(ג)(5) for the father, as in force on Nevo):** points per child by the year the child turns that age. The ITA booklet has no child table, only the 242 point value.

  | Child's age in the tax year | Mother | Father |
  |---|---|---|
  | birth year | 2.5 | 2.5 |
  | year turning 1 to year turning 2 | 4.5 | 4.5 |
  | year turning 3 | 3.5 | 3.5 |
  | years turning 4 and 5 | 2.5 | 2.5 |
  | year turning 6 to the year before maturity | 2 | 1 |
  | maturity year | 0.5 | none |

  Example: a mother of children turning 3 and 8 this year has 2.75 + 3.5 + 2 = 8.25 points. A single parent has a different, larger schedule (s.40(ב)(1)); do not use this table for one, route to the ITA credit-point calculator or the assessing office.
- Point values for the other categories are not tabulated here; take them from the source the category names. Pass the total as `--points`, or `--gender` plus `--extra-points` (never both `--points` and `--extra-points`).

On the employer route (Form 101) all reliefs are claimed at the main employer only: the gov.il guide says reliefs are given by the main employer only. In the online coordination you report every income and request the reliefs yourself, and the system computes the expected annual income and issues a certificate per payer (gov.il service page). In a request to the assessing officer (Form 116), the officer sets the annual rate to withhold from all your income (gov.il guide). Either way, the reliefs go into the coordination request. A relief the user forgets is withheld at full tax until a coordination update or a refund request after the year.

**Branches where the estimator does not apply. Explain and route:**
- **Blind, or disabled under s.9(5):** Form 101 section ח item 2א. If section ה does not mark "no other income from salary, pension or stipend", the employee is referred to the assessing officer for coordination. Two tiers (Ordinance s.9(5)(א) and (א1); 2026 ceilings from the ITA booklet), both for a disability set for 365 days or more: **684,000 NIS a year** for a blind or disabled person who is entitled to a monthly benefit under the Disabled Persons law or the hostile-action victims law (a disabled person also needs 100% disability, or 90% by a combined calculation); **445,200 NIS a year** for a blind or disabled person who is NOT entitled to that benefit (a disabled person needs at least 90% disability and at least 40% from one impairment). The booklet's 684,000 row carries a footnote limiting it to those benefit recipients. A disability set for 185 to 364 days carries a much lower ceiling; route to the assessing office.
- **Olim and veteran returning residents who arrived between 5/11/2025 and 31/12/2026:** a temporary order exempts personal-exertion income up to 600,000 NIS for tax year 2026. The ITA says a circular with the conditions will be published later. Route to the assessing office.
- **Qualifying settlement:** a credit at the locality's rate on income up to the locality's annual ceiling, given only by the payer holding the reliefs. 2026 changed the list mid-year (Kedem Arava, Yonadav and Batron added; a 2026-2029 temporary order for parts of Hevel Tkuma and Ashkelon; a mixed-urban credit of 12% up to 226,560 NIS with Nof HaGalil added). Look the locality up in chapter ח of the 2026 booklet (the list of qualifying localities); the estimator ignores the credit, so it overstates the tax.

### Step 4: Recommend which payer gets the credit points

On Form 101 section ה the employee chooses ONE payer for credit points and tax brackets: "אבקש לקבל נקודות זיכוי ומדרגות מס כנגד הכנסתי זו" at that payer, and "אני מקבל/ת נקודות זיכוי ומדרגות מס בהכנסה אחרת" at every other payer. At the others, notes (7) and (8) bar withholding by the deductions table: they withhold maximal tax, 47% per the gov.il guide, from all their payments.

Recommendation rule, **month by month** (it follows from the bracket table, since no marginal rate is above 47%): **in each month the credit points and brackets sit at the largest payer paying in that month; on equal pay they stay where they are; every switch means a new Form 101.** This is the cheapest arrangement when every payer not holding the points withholds 47%. If a payer documents a lower rate of its own (for example a daily-table worker), it is not guaranteed: compare the "points stay where they are" alternative the script prints, and pick the lower total. While a payer holds the points, the script taxes it by the monthly table; a daily-table worker is really withheld by the daily table, so treat that figure as an estimate. When a larger payer starts, or the payer holding the points stops, the points move, and the new Form 101 has section ה "אבקש לקבל נקודות זיכוי ומדרגות מס כנגד הכנסתי זו" at the payer taking them over, and "אני מקבל/ת ... בהכנסה אחרת" at the other. Example: an 8,000 job all year and a 15,000 job from June: the points sit at the 8,000 job in January to May and move to the 15,000 job in June. Credit points that exceed the tax at the chosen payer are not applied by its withholding, so tax is over-withheld until a coordination or a refund request after the year; they are not lost.

**When the main job ends mid-year** (or a larger job starts), the payer that should now hold the points keeps withholding 47% until it receives that new Form 101. Form 101 says a change must be declared within a week, and section ז records changes during the year. Update the coordination too.

**Not every secondary payslip is 47%.** Form 101 defines the pay categories: monthly salary (at least 18 days a month), salary for an additional job (more than 5 hours a day, on top of a salary or taxable pension elsewhere; note 3 lets the employee choose which workplace this is), partial salary (withheld at the maximal rate unless it is the only income), and שכר עבודה for a daily worker (under 18 days a month but at least 8 hours a week), which is withheld by the **daily table** unless it is the only income. The 2026 daily table: 10% up to 280.40, 14% to 402.40, 20% to 760.00, 31% to 1,004.00, 35% to 1,867.60, 47% above. Check the category on the second payslip before assuming 47%; if a payer documents another rate, pass it to the script as a decimal.

**Why the second payslip looks like half the pay:** 47% income tax, plus BL and health dues at the full rate (a secondary employer has no reduced bracket without a BL certificate, Step 8), plus the pension deductions. Only the income-tax part is solved by tax coordination.

Form 101 section ט also lets the employee: box 1, declare no income from the start of the tax year until starting at this employer (with proof; maternity and unemployment pay are taxable income, so they do not count as "no income"); box 2, list other salary income (payer, deductions file, monthly income, tax withheld); box 3, attach the assessing officer's certificate. The form describes itself as the employer's basis for relief and for "עריכת תיאומי מס". If payroll will not coordinate from box 2, use the online service.

### Step 5: Estimate the over-withholding

**2026 tables (after the bracket-widening law; ITA 2026 deductions booklet, chapter ב).** Section 121 was amended on 31.3.2026 with effect from 1 January 2026, so the widening is retroactive to the whole year.

| Monthly income (NIS) | Annual income (NIS) | Rate |
|---|---|---|
| up to 7,010 | up to 84,120 | 10% |
| 7,011 to 10,060 | 84,121 to 120,720 | 14% |
| 10,061 to 19,000 | 120,721 to 228,000 | 20% |
| 19,001 to 25,100 | 228,001 to 301,200 | 31% |
| 25,101 to 46,690 | 301,201 to 560,280 | 35% |
| above 46,690 | above 560,280 | 47% |

Surtax (section 121B): 3% on income above 721,560 a year (60,130 a month). An employer paying more than 60,130 a month withholds the extra 3% on that salary. Credit point: 242 NIS a month.

**2025 table (tax year 2025 only):** 10% up to 7,010; 14% up to 10,060; 20% up to 16,150; 31% up to 22,440; 35% up to 46,690; 47% above (annual 84,120 / 120,720 / 193,800 / 269,280 / 560,280). Same surtax threshold and credit point. Many commercial sites still print the 2025 limits as "2026": never use 16,150 or 22,440 for 2026.

Method (per tax year):
1. **Withheld without coordination,** month by month for the months each payer actually pays: the main payer applies the monthly table to its own pay, minus points x 242 (not below zero), plus 3% above 60,130; each other payer takes 47% of its pay, plus 3% of its pay above 60,130.
2. **Annual liability:** the annual table on the combined annual income, minus points x 242 x 12, plus 3% above 721,560.
3. **Difference** = 1 minus 2. Positive is over-withholding; negative means tax will be owed. Divide by 12 only when every payer pays all year.

```
Worked example 1 (2026, all year): salary A 12,000 + salary B 6,000, 2.25 points (544.50/month)
Main payer A:  7,010 x 10% = 701 ; 3,050 x 14% = 427 ; 1,940 x 20% = 388
               1,516 - 544.50 = 971.50 a month
Payer B:       6,000 x 47% = 2,820 a month
Without coordination: 3,791.50 a month = 45,498 a year
Liability on 216,000: 8,412 + 5,124 + 95,280 x 20% (19,056) = 32,592 - 6,534 = 26,058
Over-withholding: 19,440 a year = 1,620.00 a month
Points at B instead of A: 68,346 withheld a year. Keep them at A.
Same incomes on the 2025 table: monthly coordinated figure 2,375.00 (31% starts at 16,151).

Worked example 2 (2026, all year): salary A 50,000 + salary B 20,000, 2.25 points
Main payer A:  701 + 427 + 1,788 + 1,891 + 7,556.50 + 3,310 x 47% (1,555.70)
               = 13,919.20 - 544.50 = 13,374.70 a month (A is below 60,130: no surtax)
Payer B:       20,000 x 47% = 9,400 a month
Without coordination: 22,774.70 a month
Coordinated on 70,000: 22,774.70 + surtax 9,870 x 3% (296.10) = 23,070.80 a month
Difference: -296.10 a month (-3,553.20 a year). Tax is UNDER-withheld.

Worked example 3 (2026): salary A 12,000 all year + second job B 6,000 from July (months 7-12), 2.25 points
Withheld:  A 971.50 x 12 = 11,658 ; B 2,820 x 6 = 16,920 ; total 28,578
Liability on 180,000: 8,412 + 5,124 + 59,280 x 20% (11,856) = 25,392 - 6,534 = 18,858
Over-withholding for the year: 9,720 (not 19,440: B pays only six months)
```

Example 2 is the high-earner case: once the main payer is in the 47% bracket, the second payer's 47% matches the true marginal rate, so coordination saves nothing, and the surtax on combined income is not withheld by either payer. The coordination rate is not final; the final tax is fixed on an annual return (gov.il guide), so the shortfall should be set aside, not ignored.

**Sequential payers** (one stops before the other starts) are not concurrent. If the later payer withholds 47% because the earlier income was declared, the over-withholding can be large; if the later payer gets the points by a new Form 101, withholding comes close to the liability. Kolzchut still expects coordination for sequential sources, and anything left over is settled by a refund request after the year.

With a shell: `python3 scripts/coordination_estimate.py --main 12000 --secondary 6000@7-12 --gender m`. Payer syntax is `AMOUNT[@FROM-TO][:RATE]`: months 1-12 (default all year), RATE only for a secondary payer that documents another rate, as a decimal between 0 and 0.5 (0.31, not 31). Give `--points` (total) or `--gender f|m` with `--extra-points` (both `--points` and `--extra-points` is rejected); `--year 2025` for the old table; `--example` reproduces all three examples. The script's RECOMMENDED scenario applies the month-by-month rule (points each month at the largest payer paying that month) and names the holder by month; it also prints the "points stay where they are now" scenario and the annual liability. An under-withholding message names the surtax only when combined income is above 721,560; otherwise it points to a secondary rate below the marginal rate. The script models taxable gross only. Pension-contribution credits and deductions and benefits in kind are not modelled, so payslip figures will differ.

### Step 6: Choose the filing path

| Path | Who | How |
|---|---|---|
| Online service "עריכת תיאום מס באופן מקוון" | Employees with salary from more than one employer, employees asking for relief | Free. Login to the Tax Authority personal area. Current year only, no income ceiling, no limit on updates during the year. |
| Form 116 at the assessing office (פקיד שומה) | Anyone the online system excludes: reached eligibility age without קיבוע זכויות, 9 or more income sources, early withdrawal from a קופת גמל for medical expenses, kibbutz residents. Also the s.9(5) referral (Step 3). | Fill Form 116 with documents; hand it in at the information desk with a self-addressed envelope, or book a MYVISIT appointment. With an open income-tax file, go to that file's office; otherwise the office for the residence area. |

The gov.il service page links Form 116 in the edition updated 12.2024; no newer edition was found. Download it from the service page rather than a third-party copy.

What to prepare (gov.il): deductions-file numbers of all payers; a payslip from each payer (gross monthly pay, one-off payments); the BL payment confirmation for unemployment or maternity pay; a BL employer-continuity confirmation (אישור רצף מעסיקים) for a period without work; for pensioners without a set exemption percentage, Form 161; a קיבוע זכויות approval where relevant; documents for each relief claimed.

**The user files, not the agent.** The online system can authorise a licensed representative (מייצג) to coordinate on the user's behalf. This skill never takes that role, never logs in or submits for the user, and never drafts an objection (השגה). It explains, computes, and lists what to enter.

### Step 7: What to do with the certificates

- The system issues **one certificate per payer**. Give each payroll department its own certificate; the employee side is Form 101 section ט box 3, "פקיד השומה אישר תיאום לפי אישור מצורף".
- Turnaround: some certificates are immediate; others go to office review and arrive within a few business days (gov.il). Kolzchut gives 5 business days for office handling.
- Validity: one tax year, until 31.12.2026 for the current year. If the data behind it changes (new job, raise, job ended), do a new coordination; the online system allows updates during the year.
- Extensions: if the Tax Authority sent an extension letter for last year's certificates and nothing changed, the extended certificates can be given to the payers. The letter is in the "letters" page of the personal area.
- Excess already withheld: once payroll gets the certificate, the next payslip recalculates and the excess from earlier months comes back in the net pay, no refund request needed (kolzchut). Coordination is possible until 31 December. This works only through a payer that is **still paying** this year: if the payer that over-withheld has stopped (maternity pay ended, a job that finished), the excess comes back only through a refund request after the year (`israeli-employee-tax-refund`).

**2026 transition.** The Tax Authority notice of 30.03.2026 said employees who had already coordinated for 2026 need not update; expected annual income below 193,800 is unaffected, and above it the Tax Authority updates proactively. It extended 2025 coordinations until 13.5.2026, a date that has passed. The later gov.il guide adds that anyone whose 2026 income exceeds 193,800 benefits from the widening and must coordinate for 2026, and that existing 2026 coordinations were corrected and wait in the personal area. If an early-2026 payslip looks computed on the 2025 table, ask payroll whether the correction was applied (an inference, not a published rule).

### Step 8: Flag Bituach Leumi separately

Tax coordination covers income-tax withholding only and does **not** update Bituach Leumi (kolzchut). BL has its own coordination (BTL 2026 employer letter):
- When income at the main employer is below the reduced collection bracket, 7,703 NIS gross, or total income from all employers is above the maximum insurable income, 51,910 NIS gross, the worker can get a current-year BL coordination certificate from the BL website. It arrives as a letter to hand to the secondary employer or pension payer.
- In the first case only (main-employer income below 7,703), a worker without internet access can instead give the secondary employer Form בל/644 declaring the income at the main employer. In the second case (total above 51,910) the letter offers only the BL certificate, and the secondary employer may not exempt the worker without a BL approval.
- Otherwise the secondary employer always deducts BL and health dues at the full rate.
- BL dues are computed monthly, each month separately. Prior years: a request within 7 years from the end of the tax year; BL does not initiate the check (kolzchut).

Do not compute BL dues here; flag the route and the thresholds.

### Step 9: When coordination is not worth much, and what happens without it

- Not worth much: the main payer is already in the 47% bracket (example 2), or the second payment is tiny and short. Over-withholding is still recoverable: mid-year via coordination while the payer is still paying, or after the year via a refund request up to 6 years back with `israeli-employee-tax-refund`.
- Without coordination, Form 101 notes (7) and (8) apply: the payer that does not hold the points withholds maximal tax from all its payments. Partial salary (note 4) is withheld at the maximal rate unless it is the only income. A mandatory referral to the assessing officer applies only to the s.9(5) disabled or blind employee (section ח item 2א).
- Under-withholding (example 2) is not cancelled by skipping coordination: the final tax is fixed on an annual return.
- Users do not need to pay anyone: kolzchut notes coordination is short, free, and can be done alone.

## Bundled Resources

### References
- `references/domain-checklist.md`: coverage contract, both bracket tables, the temporal split, known bad figures and out-of-scope rows.

### Scripts
- `scripts/coordination_estimate.py`: month-by-month withholding against the annual liability, sequential payers, and which payer should hold the credit points. Stdlib only; `--help`, `--example`.

## Recommended MCP Servers

| MCP | Why pair it |
|---|---|
| `kolzchut` | Live rights pages for re-checking dates and BL thresholds against the current publication. |

## Gotchas

- Agents apply the pre-widening table to 2026. The 2026 limits are 19,000 (20%) and 25,100 (31%) a month; 16,150 and 22,440 belong to 2025.
- Agents default every user to 2.25 points. A woman's basic entitlement is 2.75, and children, a degree, reserve duty and the other reliefs add more.
- Agents multiply a monthly gap by 12 for a job that started mid-year. Use the months each payer actually pays.
- Agents assume coordination always lowers withholding. For a main payer already above 46,690 a month it saves nothing, and two payers each below 60,130 leave the combined surtax unwithheld.
- Agents promise the excess back "in the next payslip" when the over-withholding payer has already stopped paying. Then only a refund request after the year recovers it.
- Agents treat jobs that did not overlap as one income, or as concurrent. They still need coordination, but the gap depends on how the later payer withheld.
- Agents list a student's stipend as a taxable payer. Under s.9(29) a stipend to a student during the studies, with no service in return, is exempt and is not a payer; only a researcher's stipend is capped.
- Agents assume the tax certificate fixes Bituach Leumi too. It does not; BL coordination is a separate request.
- Agents quote kolzchut's 13.04.2026 / 13.05.2026 extension dates. The later gov.il notice set 13.5.2026, and both have passed.
- Agents offer to "submit the coordination for you". Filing on someone's behalf is a representative's role; the skill guides the user to file.

## Reference Links

| Source | URL | What to check |
|---|---|---|
| ITA online tax coordination service | https://www.gov.il/he/service/tax-coordination-online | Who may use it, exclusions, reliefs, certificates, extensions |
| ITA guide: relief and tax coordination | https://www.gov.il/he/departments/guides/income-tax-guide-for--tax-relief-and-tax-coordination | 47% rule, Form 116 path, documents, validity |
| ITA notice 30.03.2026 | https://www.gov.il/he/pages/sa300326-2 | 2026 transition after the bracket widening |
| ITA 2026 deductions booklet | https://www.gov.il/BlobFolder/generalpage/income-tax-monthly-deductions-booklet/he/generalInformation_income-tax-monthly-deductions-booklet_monthly-deductions-booklet-2026.pdf | 2026 brackets, daily table, surtax, credit point, s.9A, s.9(5), s.9(29), olim order, settlements |
| ITA 2025 deductions booklet | https://www.gov.il/BlobFolder/generalpage/income-tax-monthly-deductions-booklet/he/generalInformation_income-tax-monthly-deductions-booklet_monthly-deductions-booklet-2025.pdf | 2025 brackets |
| Income Tax Ordinance (Nevo) | https://www.nevo.co.il/law_html/law00/84255.htm | Sections 9(5), 9(29), 34, 36, 36A, 39B, 40, 66 |
| Kol-Zchut: child credit points (updated 11.2.2026) | https://www.kolzchut.org.il/he/%D7%A0%D7%A7%D7%95%D7%93%D7%95%D7%AA_%D7%96%D7%99%D7%9B%D7%95%D7%99_%D7%9E%D7%9E%D7%A1_%D7%94%D7%9B%D7%A0%D7%A1%D7%94_%D7%9C%D7%94%D7%95%D7%A8%D7%94_%D7%9C%D7%99%D7%9C%D7%93_%D7%A2%D7%93_%D7%92%D7%99%D7%9C_5 | Child point schedule from 2024, 2026 worked examples |
| Form 101 | https://www.gov.il/BlobFolder/service/itc101/he/Service_Pages_Income_tax_annual-report-2024_itc101.pdf | Sections ה, ז, ח, ט and notes 1 to 8 |
| Form 116 | https://www.gov.il/BlobFolder/service/tax-coordination-online/he/Service_Pages_Income_tax_annual-report-2024_itc116-2024.pdf | Manual coordination request |
| Bituach Leumi 2026 employer letter | https://www.btl.gov.il/Insurance/HozrimBituah/Hozrim/%d7%90%d7%99%d7%92%d7%a8%d7%aa%20%d7%9c%d7%9e%d7%a2%d7%a1%d7%99%d7%a7%20%d7%9c%d7%a9%d7%a0%d7%aa%202026.pdf | BL coordination thresholds, Form בל/644 |
| Kol-Zchut: tax coordination | https://www.kolzchut.org.il/he/%D7%AA%D7%99%D7%90%D7%95%D7%9D_%D7%9E%D7%A1_%D7%94%D7%9B%D7%A0%D7%A1%D7%94 | Who needs it, FAQ |
| Kol-Zchut: BL dues coordination | https://www.kolzchut.org.il/he/%D7%94%D7%97%D7%96%D7%A8_%D7%93%D7%9E%D7%99_%D7%91%D7%99%D7%98%D7%95%D7%97_%D7%9C%D7%90%D7%95%D7%9E%D7%99_%D7%95%D7%93%D7%9E%D7%99_%D7%91%D7%99%D7%98%D7%95%D7%97_%D7%91%D7%A8%D7%99%D7%90%D7%95%D7%AA_%D7%9C%D7%A9%D7%9B%D7%99%D7%A8%D7%99%D7%9D | Monthly basis, 7-year window |

## Troubleshooting

### "The online system will not let me in or will not accept my case"
First check the exclusions in Step 6; those cases go to the assessing office with Form 116. Otherwise the likely cause is the personal-area login, which the service requires; this is an inference, not a confirmed diagnosis.

### "I coordinated but the second payslip still shows 47%"
Check that each payer received its own certificate and that the certificate is for the current tax year. A certificate given to the wrong payroll, or last year's certificate without an extension letter, leaves the payer withholding the maximal rate.

### "The estimate and my payslip disagree"
The estimate uses taxable gross and the months you gave. Pension-contribution credits and deductions, benefits in kind, bonuses, a pension's exempt share and the reliefs in Step 3 change the picture; the Tax Authority's certificate, not this estimate, is what payroll applies.
