---
name: israeli-employee-tax-refund
description: "Walk salaried Israeli employees through the voluntary tax-refund process with Reshut HaMisim. Reads Form 106, detects refund triggers (job change, unemployment, maternity leave, reserve duty, Section 46 donations, yishuv mezakeh, missed credit points, disability, alimony, early keren hishtalmut withdrawal), estimates the refund using 2026 brackets and credit-point values, generates a per-trigger document checklist, and fills Form 135 or routes the user to the online refund portal. Knows the 6-year window (Section 160 ITO). Use when a salaried employee asks about Israeli tax refund, החזר מס לשכירים, טופס 135, miluim refund, or refunds for previous tax years. Do NOT use for self-employed Form 1301 filers (use israeli-tax-returns), payroll math (use israeli-payroll-calculator), stock options (use israeli-stock-options-tax), crypto (use israeli-crypto-tax-reporter), or VAT (use israeli-vat-reporting)."
license: MIT
allowed-tools: Bash(python:*) WebFetch
compatibility: Works with Claude Code, OpenClaw, Cursor, Windsurf, Codex, GitHub Copilot, opencode, antigravity.
---

# Israeli Employee Tax Refund

## Legal notice

This is a free information tool operated by an AI model. It explains the tax rules and helps you organise your own figures. All of its outputs are produced automatically by an AI model, with no involvement, review, or approval by a tax adviser or accountant. The output is not a tax opinion, not a return prepared by a licensed representative, and not professional advice, but a general calculation and explanation only: it does not examine the full extent of your income or your complete documents. An AI model may err, omit data, or present a wrong conclusion.

Any form or text this tool produces is an automatic draft for your personal preparation only, and is not a filed return. Responsibility for reporting and for paying the tax is yours, the binding computation is the Tax Authority's, and representation before the Tax Authority is reserved to those permitted by law. This tool is not a substitute for advice that takes account of the particular circumstances and needs of each person. Consult a tax adviser or accountant before filing or paying. All use of its output is the user's sole responsibility.


## Problem

Hundreds of thousands of salaried Israelis overpay income tax every year and never claim the refund they are entitled to. Mid-year job changes, periods of unemployment, maternity leave, reserve duty, donations, residency in a settled area, and missed credit points all create gaps between what the employer withheld and what the employee actually owed. The voluntary refund track (Form 135 or the online portal at the Tax Authority) is the way to recover that money, but the rules, forms, and 6-year retroactive window are opaque. This skill detects refund triggers from the employee's Form 106, estimates the refund using current-year brackets and credit-point values, generates a per-trigger document checklist, and produces a filled Form 135 or guides the user through the online portal.

## Instructions

### Step 1: Confirm This Is the Right Skill

This skill is for **salaried employees (שכירים) voluntarily seeking a refund** for tax years that have already ended. Use a different skill if the user is:

| Situation | Skill to use |
|-----------|-------------|
| Self-employed (osek murshe / osek patur) or business owner | `israeli-tax-returns` |
| Required to file Form 1301 (mixed income, very high income, foreign assets) | `israeli-tax-returns` |
| Asks about gross-to-net or payslip math (not a closed tax year) | `israeli-payroll-calculator` |
| Has stock options, RSUs, or Section 102 income | `israeli-stock-options-tax` |
| Has crypto disposals | `israeli-crypto-tax-reporter` |
| Has foreign-source income in any year being claimed (US W-2, foreign rental, foreign brokerage) | `israeli-tax-returns`. Foreign income usually triggers a Form 1301 obligation, and Section 14 olim/returning residents need a specialist. Never fold it into a Form 135 refund. This routing is about FOREIGN income only: an oleh or תושב חוזר ותיק with Israeli salary alone stays here, including for the 2026 aliya exemption in trigger 18. |
| Has a פיצויי פיטורים / severance / Form 161 event in any year being claimed | `israeli-tax-returns`. Severance carries Section 9(7A) math, the תקרת פטור, and the רצף קצבה / רצף פיצויים choice. Form 161 appears here only as an OCR target. |
| Wants prospective mid-year withholding adjustment | The Tax Authority's online תיאום מס at `gov.il/he/service/tax-coordination-online`, NOT this skill |

Ask the user:
- Tax year(s) in question (must be 2020 or later as of 2026, see Step 3)
- Were they salaried only during those years (no self-employment income)?
- Do they have all relevant Form 106 documents from each employer for each year?

### Step 2: Read Form 106 (אישור שנתי על משכורת ומס שנוכה)

Form 106 is the annual income summary the employer issues by March 31 of the following year. Identify these fields:

| Field | Hebrew label | What it tells you |
|-------|--------------|-------------------|
| 042 | סה"כ מס שנוכה במקור | Total income tax withheld by this employer for the year. Sums across multiple 106s to get total withholding. |
| 158 / 172 | משכורת חייבת | Taxable salary. The base for the tax-due calculation. |
| 218 / 219 | הפקדה לקרן השתלמות | Keren hishtalmut deposit. Relevant for the early-withdrawal refund and the deduction cap check. |
| Months worked | חודשי עבודה | If less than 12, the user did not work the full year for this employer; common refund trigger. |

With multiple Form 106s in one tax year, sum field 042 across them. The commonest refund driver is each employer withholding as if its salary were the worker's only income.

**Bituach Leumi annual confirmation feeds the same fields as Form 106.** If the user received דמי לידה, דמי אבטלה, דמי פגיעה (short-term work injury, up to 91 days) or דמי שמירת היריון during the year, ask for the annual אישור שנתי למס הכנסה from btl.gov.il and aggregate it with the Form 106 totals: gross into field 158/172, BTL-withheld tax into field 042. All four are fully taxable personal-exertion income with no Section 9 exemption. תגמולי מילואים are usually paid via the employer and so already sit inside Form 106; only a portion paid direct from BTL adds its own confirmation. `references/document-requirements.md` lists which confirmation to order for each.

The Section 9(6) exemptions (קצבת ילדים, זקנה, שאירים, נכות כללית, מענק לידה, ניידות) cover permanent or family-status allowances, not income replacement while temporarily out of work. Do not assume "BTL paid me, so it is exempt" for maternity, unemployment, or work-injury per-diem.

A common misconception: the refund usually originates from the **salary side**, not BTL. BTL typically under-withholds on דמי לידה / דמי אבטלה, so that portion alone can leave the recipient owing tax. The refund appears because the employer over-withheld during the months actually worked.

### Step 3: Determine the Refund Window

The retroactive refund window is 6 calendar years from the end of the tax year, per Section 160 of the Income Tax Ordinance.

The deadline is 31 December of the sixth year after the tax year, so 2020 closes 31.12.2026, 2021 closes 31.12.2027, and so on through 2025 closing 31.12.2031. The full table is in `references/2026-rates.md`.

Years before 2020 can no longer be claimed in 2026. Tell the user which years are open and which have closed.

### Step 4: Detect Refund Triggers

Walk through this trigger list with the user. For each detected trigger, record it and the year(s) it applies to. Each trigger maps to a document requirement in Step 6.

| # | Trigger | When it applies | Statutory anchor |
|---|---------|----------------|------------------|
| 1 | Mid-year job change / multiple employers in same year | Two or more Form 106s for the same tax year and no תיאום מס was filed mid-year | Section 164 ITO (withholding mechanics) |
| 2 | Partial-year work / unemployment period | Less than 12 months worked in the year (Form 106 months field) | Withholding over-projection |
| 3 | Maternity / paternity leave | Received דמי לידה from Bituach Leumi during the year | Section 164 ITO. דמי לידה are FULLY taxable; the refund comes from employer over-withholding, not an exemption. Section 9(6) does NOT cover it, see Step 2. |
| 4 | Military reserve duty (מילואים) | 30+ days of reserve service in the prior tax year | Section 39B ITO (per Amendment 283, התשפ"ו-2025) |
| 5 | Charitable donations to recognized institutions | Total donations to Section 46-approved institutions ≥ 207 ₪ in the year (2026 minimum) | Section 46 ITO |
| 6 | Resident of yishuv mezakeh (settled area / periphery) | Center of life in an eligible locality for 12+ consecutive months; the locality appears on the annual official list | Section 11 ITO + Negev/Galilee Law |
| 7 | New immigrant credit points (סעיף 35) | Oleh chadash within the first 4.5 years of aliyah (54 months for olim arriving 2022 or later, 42 months for earlier arrivals). Per-month allotment is shown in Step 5. | Section 35 ITO + Amendment 262 of 2022 (note: this is the credit-points benefit, not a mortgage interest deduction) |
| 8 | Completed a bachelor's or master's degree | Bachelor's: 1 point per study year up to 3 years (2023+ graduates) or 1 point for one tax year (2014-2022). Master's: 0.5 point for 2 years (2023+) or one year (2014-2022). See also trigger 19's sibling entitlement for vocational certificates in Step 5. | Section 40ג ITO |
| 9 | Single parent, parents living apart, or paying maintenance to a former spouse | Court judgment establishing single-parent status, a split-custody arrangement, or maintenance paid to a former spouse while remarried. Each is a separate entitlement with its own point count, listed in Step 5. | Sections 40(ב)(1), 40(ב)(1ב), 40(ב)(2) and 40א ITO |
| 10 | Disability tax exemption | 100% medical disability, blindness, or 90%+ under the multi-organ-injury calculation (פגיעה באיברים שונים), on a medical-board determination. 2026 exempt-income ceilings: 445,200 ₪ (365+ days), 81,960 ₪ (185-364 days), 684,000 ₪ for a חוק הנכים / נפגעי פעולות איבה pension. | Section 9(5) ITO |
| 11 | Self-deposit to pension or life insurance beyond the employer's deposit | A deposit made by the employee directly. Section 45A gives a 35% credit on the qualifying deposit against "insured salary" contributions. | Sections 45A and 47 ITO |
| 12 | Early keren hishtalmut withdrawal | Withdrew from a keren hishtalmut before 6 years; bank withheld 47% at source but real marginal rate is lower | Section 9(16a) + Section 164 ITO |
| 13 | Salaried employee paid more child credit points than employer recognized | Custody arrangement changed; employer's 101 form was not updated | Section 40 ITO |
| 14 | One-time bonus or 13th salary pushed a single month into a higher bracket | Withholding is computed month by month, so a December bonus or 13th salary can land that month in the 35% or 47% band even though the annual marginal rate is far lower. Sum it into the annual reconciliation. | Regulation 6 of תקנות מס הכנסה (ניכוי ממשכורת ומשכר עבודה) |
| 15 | Discharged soldier / national-service graduate credit points | The חייל משוחרר box on Form 101 was not ticked within 36 months of discharge, so the points were never applied at source. Very common in a first job. | Section 39א ITO |
| 16 | Child who is נטול יכולת (paralyzed, blind, or with an intellectual-developmental disability), the taxpayer's or their spouse's | 2 credit points, never applied at source (needs Form 116א). Distinct from trigger 10, which is the taxpayer's OWN disability. | Section 45(א) ITO |
| 17 | Funding a relative's institutional care (מוסד) | 35% credit on Form 116. Mutually exclusive with trigger 16 for the same child; compute both and keep the larger. | Section 44 ITO |

| 18 | Oleh chadash or תושב חוזר ותיק who arrived 5.11.2025 - 31.12.2026 | Full income-tax EXEMPTION on Israeli personal-exertion income for tax years 2026-2030, up to an annual ceiling (600,000 ₪ for 2026). Given IN ADDITION to the trigger 7 credit points, not instead of them. Cannot be taken through payroll yet, so a salaried claimant realises it by filing a refund request once 2026 closes. Ceilings, the lower relative-income limb, the 2026 pro-rating and the residency anti-abuse rule are in `references/2026-rates.md`. | חוק עידוד עלייה לישראל וחזרה אליה (הוראת שעה), התשפ"ו-2026, section 2(a) |
| 19 | Second- or third-shift work at an industrial production plant | 15% credit on the shift pay, capped at 12,540 ₪ of credit against at most 143,040 ₪ of income for 2026. The regulations run to 31.12.2026 and reach only plants whose main activity is productive; a shift worker in retail, security or healthcare is outside them. | Section 10 ITO + תקנות מס הכנסה (שיעור המס על הכנסה בעד עבודה במשמרות), התשמ"ז-1986 |

Triggers 16 and 17 are mutually exclusive for the same relative: a taxpayer cannot take both the Section 45(a) 2 credit points and the Section 44 institution credit for the same child. Compute both and keep the larger. Both require Form 116/116א with medical certification, so they are almost never applied at source and are high-yield retroactive claims.

Separately, if the user is a low-income worker (the two-job, low-wage, reserve-duty persona), also check מענק עבודה (the earned-income / negative-income-tax grant). It is NOT a Form 135 refund; it is a separate claim paid by Bituach Leumi, so route the user to `btl.gov.il` (מענק עבודה) in addition to any Form 135 refund. Do not fold it into the refund estimate.

Trigger 7 clarification (common misinformation): there is no "Section 35 mortgage interest deduction for olim". Section 35 grants credit points on a declining schedule (rates in Step 5 and `references/2026-rates.md`): 8.5 points over 54 months for olim arriving 1.1.2022 or later, 7.5 points over 42 months for earlier arrivals. Section 35 points are not available to an ordinary תושב חוזר, who gets the Section 14 foreign-income exemption instead. A תושב חוזר ותיק with foreign income still belongs in `israeli-tax-returns`, but one with Israeli salary who arrived inside the trigger 18 window is claimed here.



### Step 5: Estimate the Refund

Estimate the refund as (correct tax under that year's brackets and credits) minus (tax withheld, the sum of field 042 across all Form 106s for the year).

**2026 monthly tax brackets for employees:**

| Monthly salary band | Annual band | Marginal rate |
|---------------------|-------------|---------------|
| Up to 7,010 ₪ | Up to 84,120 ₪ | 10% |
| 7,011 - 10,060 ₪ | 84,121 - 120,720 ₪ | 14% |
| 10,061 - 19,000 ₪ | 120,721 - 228,000 ₪ | 20% |
| 19,001 - 25,100 ₪ | 228,001 - 301,200 ₪ | 31% |
| 25,101 - 46,690 ₪ | 301,201 - 560,280 ₪ | 35% |
| 46,691 ₪ and above | 560,281 ₪ and above | 47% (Section 121 ITO top bracket) |
| Plus mas yesafim | Annual income above 721,560 ₪ | Additional 3% surtax (Section 121B ITO), on top of the 47% |

For prior tax years use that year's brackets; `scripts/estimate_refund.py` carries them for 2020-2026 and rejects any other year rather than silently substituting. The 2026 credit point is worth **242 ₪ per month, 2,904 ₪ per year**.

**Credit-point allotment.** The base is 2.25 points for an Israeli resident and 2.75 for a woman. On top of that sit the child schedule, the single-parent and separated-parent rows, the s.40א maintenance point, the 16-17 age point, the oleh, discharged-soldier, academic and vocational points, and the 2 points for a נטול יכולת child. The full table, with the statutory anchor for each row, is in `references/2026-rates.md`. Three rows the employer almost never applies at source, and which therefore drive most retroactive claims: the half point in the year a child turns 18 (mother or single parent only, never the father), the extra point for a single parent's ילד להורה אחד, and the s.40ד vocational-certificate point.

**Section 44 institution credit (not a credit point):** 35% of the amount paid above 12.5% of the taxpayer's income, if the relative's 2026 annual taxable income is under 188,000 ₪ (301,000 ₪ for a couple). Claimed on Form 116.

**Reserve-duty credit-point bonus (Section 39B, Amendment 283 התשפ"ו-2025, published 23.11.2025):** 0.5 point for 30-39 days of combat reserve service in the previous tax year, 0.75 for 40-49, 1.0 for 50 or more, plus 0.25 for every further 5 days beyond 50, capped at 4 points (11,616 ₪ at the 2026 value). The full table is in `references/2026-rates.md`. There is one schedule only; the points are realized in the tax year **after** the service, so 60 days served in 2025 are claimed on the 2026 refund.

**Donation credit (Section 46):**

A donation to a Section-46-approved institution returns 35% of the donated amount as a credit, above an annual minimum and below an annual ceiling that are BOTH index-adjusted each year: for 2026, a 207 ₪ minimum and a ceiling of 10,354,816 ₪ or 30% of taxable income, whichever is lower. Earlier claim years use their own figures (the 2022 minimum was 190 ₪, the 2023 minimum 200 ₪); the per-year table is in `references/2026-rates.md`. Receipts may be original, certified copy, or electronic (מסמך ממוחשב). Confirm the institution held an active Section 46 approval in the donation year.

**Yishuv mezakeh credit:**

Residents of eligible localities get a percentage credit on earned income, capped at a per-locality annual ceiling, after 12 continuous months of centre of life there. Rate and ceiling are both PER LOCALITY.

Do not guess the percentage and do not leave it at zero: look the locality up in chapter ח of that year's ITA deductions booklet and pass BOTH `--yishuv-pct` and `--yishuv-ceiling`. The 2026 table has 15 rate/ceiling combinations, and the rate does not imply the ceiling (12% appears against four different ceilings, 14% against four), so never infer one from the other. Three הוראת שעה regimes new for 2026 add אשקלון (חבל תקומה, capped 14% / 180,000 ₪), נוף הגליל (mixed urban, 12% / 226,560 ₪) and the eastern confrontation line, and קדם ערבה, יונדב, בתרון and אדוריים joined the list. `references/2026-rates.md` carries all 15 rows, the new localities and the separate Eilat (10% / 268,560 ₪) and security-forces (5% / 178,320 ₪) regimes. Leaving the default silently returns zero credit, a missed entitlement for a periphery resident.

Present the estimate as a range, not a single number, and say that the Tax Authority's own calculation may differ once the documents are reviewed.

### Step 6: Generate the Document Checklist

Build the list from the triggers detected in Step 4. Three items are always required: Form 106 from every employer for each year claimed, teudat zehut plus ספח, and a bank account confirmation (אישור ניהול חשבון) for the payout.

The full per-trigger checklist lives in `references/document-requirements.md`. Read it and emit only the rows matching the detected triggers. Trigger 18 additionally needs the תעודת עולה or the residency-start confirmation fixing the arrival date inside the 5.11.2025 - 31.12.2026 window; trigger 19 needs the employer's confirmation of second- or third-shift pay. Remind the user to keep copies; the Tax Authority can request originals later.

### Step 7: Choose the Submission Channel

There are two main channels for an employee voluntary refund.

| Channel | When to use | Where |
|---------|-------------|-------|
| Online refund portal (השכיר המקוון / מערכת מקוונת להחזר מס לשכירים) | The user is not obligated to file a Form 1301; they have a digital government identity (Government Identity Document or smart-card); they have scanned PDFs of their supporting documents | `secapp.taxes.gov.il` (see Reference Links) |
| Manual Form 135 | The user prefers paper, the online portal does not support their case, or the user's identity verification cannot be completed online | Fill Form 135 (available at `gov.il/he/service/itc135`) and submit at the appropriate משרד שומה / pekid shuma assigned to the user's address |

If the user is required to file a Form 1301 (e.g., income above the surtax threshold for that year, foreign income, or capital gains in the same year), neither track applies for that year, route them to `israeli-tax-returns` and include the refund calculation inside Form 1301.

### Step 7.5: Prospective Fix via Form 101 (Highly Important)

If a trigger is **ongoing** (still a single parent, still an oleh inside the window, still in a yishuv mutav, children still in the right age band, still serving reserve duty), tell the user to update Form 101 at the employer, whose part ז is where each of these entitlements is claimed. Without this the user files the same refund every year for the same missed credit: the refund returns last year's over-withholding, the 101 stops it going forward.

Submit the updated 101 to HR / payroll with the same supporting documents the refund used (תעודת עולה, אישור תושבות, custody court order) and ask payroll to recompute withholding from the next pay period. The trigger 18 aliya exemption is the one entitlement that cannot yet be taken this way.

### Step 8: Submit and Track

After submission:

- The refund must be paid within one year from the assessment date, or two years from the end of the tax year, whichever is later. Later payment accrues הצמדה (CPI linkage) plus 4% annual interest on top of the principal.
- Status is checked at the same portal where the claim was submitted.
- A "drisha להשלמת מסמכים" must be answered within the stated deadline or the request closes and a new application is needed.

## Examples

### Example 1: Refund After Two Jobs in 2024

A salaried developer worked 6 months at Employer A (25,000 ₪/month) then 6 months at Employer B (22,000 ₪/month) in 2024, with no mid-year תיאום מס and no Form 101 at B, so B withheld at the maximum rate.

1. Field 042 across both 106s: 27,158 ₪ at A (regular withholding, 2.75 points) plus 62,040 ₪ at B (47% on 22,000 ₪ for 6 months) = 89,198 ₪.
2. `python scripts/estimate_refund.py --year 2024 --salary 282000 --withheld 89198 --points 2.75` returns a tax due of about 48,017 ₪ on the 282,000 ₪ aggregate.
3. Trigger 1 detected. Estimated refund range: 37,063 to 45,299 ₪.

This refund size comes from the missing Form 101 at the second employer, not the job change. With normal withholding at both, a mid-year move can even leave tax owed: 282,000 ₪ with 47,200 ₪ withheld comes out to roughly 800 ₪ owed. Always run the numbers before promising a refund.
4. Document checklist: both Form 106s, teudat zehut, bank confirmation.
5. Channel: online portal (no Form 1301 obligation).
6. Year 2024 deadline: 31.12.2030.

### Example 2: Reserve Duty Refund for 2025 Service

A salaried teacher served 65 days of reserve duty in 2025. Reserve-duty credit points are claimed on the 2026 tax return (or via refund request) because they are realized the year after the service.

1. Section 39B / Amendment 283 schedule: 50 days = 1.0 point. The 15 additional days (over 50) at +0.25 per 5 days = +0.75 points. Total = 1.75 points.
2. Value: 1.75 × 2,904 ₪ = 5,082 ₪ refund expected for 2026.
3. Document: Form 3010 from the reserve unit listing 65 days served in 2025.
4. Submit via online portal for tax year 2026 after the 2026 Form 106 is issued (by 31.3.2027).

## Bundled Resources

### References

- `references/domain-checklist.md`: canonical coverage list with statutory anchors for every Must-cover and Should-cover item.
- `references/2026-rates.md`: snapshot of 2026 brackets, credit-point value, donation ceiling, miluim points table, yishuv mezakeh notes, and refund window dates.
- `references/document-requirements.md`: per-trigger document list with Hebrew names and where to obtain each.

### Scripts

- `scripts/estimate_refund.py`: rough refund estimator given Form 106 numbers and detected triggers. Output is an estimate range, not a binding figure.

## Recommended MCP Servers

| MCP | Why pair it |
|-----|-------------|
| `kolzchut` | Live rights pages for every refund trigger. Use it whenever a figure here needs re-verifying against the current-year publication. |

Companion skill: `hebrew-ocr-forms` extracts fields 042 / 158 / 172 / 218 from scanned Form 106 and Form 161 PDFs.

## Gotchas

- The 6-year window is measured from the **end** of the tax year (Section 160 ITO), not from the date the employer issued Form 106. The 2020 deadline is 31.12.2026, not 31.3.2026.
- Reserve-duty credit points (Section 39B / Amendment 283) are realized in the year **after** the service. A soldier who served in 2024 claims them on the 2025 refund, not the 2024 refund.
- Section 35 (oleh credit points) is not "mortgage interest deduction". Do not promise the user a mortgage refund under Section 35.
- The 2026 aliya exemption (trigger 18) is a temporary order that sunsets after tax year 2030, and it stacks ON TOP of the Section 35 points rather than replacing them. Offering an oleh who arrived inside the window only a credit-point refund understates the claim by an order of magnitude.
- Where the trigger 18 exemption applies, it removes income from the tax base before credit points are applied, so points can end up worth less than their headline value in an exempt year. Compute the exempt tranche first, then apply the points to what remains.
- The yishuv mutav rate does not determine the ceiling. Read both values for the user's own locality from the current year's booklet; a rate looked up against the wrong ceiling silently over- or under-states the credit.
- Section 46's minimum donation and ceiling are index-adjusted every year. A 195 ₪ donation qualifies in a 2022 claim (minimum 190 ₪) but not in a 2026 one (minimum 207 ₪). Never apply the current year's minimum to an earlier claim year.
- Section 46 receipts are valid as original, certified copy, or electronic (מסמך ממוחשב). Confirm the receiving institution held an active Section 46 approval for the donation year.
- Filing a refund request opens the whole tax year to assessment: a marginal case can come back as a **demand to pay**, and any refund is first offset against existing income-tax, Bituach Leumi, מזונות, or הוצאה לפועל debts.
- Prospective mid-year withholding adjustment (תיאום מס) and retrospective refund (Form 135 / online portal) are different mechanisms. תיאום מס handles the current year before it closes; refund handles years that already closed. Users frequently conflate them.
- Yishuv mutav requires centre of life in the locality for 12 consecutive months. Moving between two eligible localities is fine (the 12 months accumulate) but the credit is pro-rated across them.

## Reference Links

| Source | URL | What to check |
|--------|-----|---------------|
| ITA deductions booklet 2026 (לוח ניכויים) | https://www.gov.il/BlobFolder/generalpage/income-tax-monthly-deductions-booklet/he/generalInformation_income-tax-monthly-deductions-booklet_monthly-deductions-booklet-2026.pdf | Authoritative source for every 2026 amount here: chapter ה has the 15 yishuv rate/ceiling rows, chapter ח the full locality list, and the amounts chapter the Section 46 and shift-work figures |
| Tax Authority Form 135 official page | https://www.gov.il/he/service/itc135 | Form 135 PDF, who files, attachments |
| Online refund portal | https://secapp.taxes.gov.il | Auth flow, document uploads |
| Income Tax Ordinance, consolidated | https://www.nevo.co.il/law_html/law00/84255.htm | Sections 10, 11, 35, 39B, 40, 40א, 40ג, 40ד, 44, 45, 46, 160 as currently in force |
| Kol-Zchut: refund overview | https://www.kolzchut.org.il/he/%D7%94%D7%97%D7%96%D7%A8_%D7%9E%D7%A1_%D7%94%D7%9B%D7%A0%D7%A1%D7%94 | 6-year window, processing time, interest + הצמדה |
| Kol-Zchut: 2026 credit points | https://www.kolzchut.org.il/he/%D7%A0%D7%A7%D7%95%D7%93%D7%95%D7%AA_%D7%96%D7%99%D7%9B%D7%95%D7%99_%D7%9E%D7%9E%D7%A1_%D7%94%D7%9B%D7%A0%D7%A1%D7%94 | Monthly point value and category list |
| Kol-Zchut: oleh / returning-resident exemption | https://www.kolzchut.org.il/he/%D7%A4%D7%98%D7%95%D7%A8_%D7%9E%D7%9E%D7%A1_%D7%94%D7%9B%D7%A0%D7%A1%D7%94_%D7%9C%D7%A2%D7%95%D7%9C%D7%99%D7%9D_%D7%97%D7%93%D7%A9%D7%99%D7%9D_%D7%95%D7%9C%D7%AA%D7%95%D7%A9%D7%91%D7%99%D7%9D_%D7%97%D7%95%D7%96%D7%A8%D7%99%D7%9D_%D7%95%D7%AA%D7%99%D7%A7%D7%99%D7%9D | Arrival window, per-year ceilings, relative-income limb |
| Kol-Zchut: yishuv mezakeh | https://www.kolzchut.org.il/he/%D7%96%D7%99%D7%9B%D7%95%D7%99_%D7%9E%D7%9E%D7%A1_%D7%94%D7%9B%D7%A0%D7%A1%D7%94_%D7%9C%D7%AA%D7%95%D7%A9%D7%91%D7%99%D7%9D_%D7%91%D7%A4%D7%A8%D7%99%D7%A4%D7%A8%D7%99%D7%94 | 12-month rule, Eilat regime, moving between localities |
| Kol-Zchut: Section 9(5) disability exemption | https://www.kolzchut.org.il/he/%D7%A4%D7%98%D7%95%D7%A8_%D7%9E%D7%9E%D7%A1_%D7%94%D7%9B%D7%A0%D7%A1%D7%94_%D7%9C%D7%90%D7%A0%D7%A9%D7%99%D7%9D_%D7%A2%D7%9D_%D7%A0%D7%9B%D7%95%D7%AA | Current Section 9(5) ceilings |
| Claltax: Form 106 field map | https://claltax.com/%D7%98%D7%95%D7%A4%D7%A1-106-%D7%A9%D7%9B%D7%99%D7%A8-%D7%95%D7%92%D7%9E%D7%9C%D7%90%D7%99/ | Field 042 / 158 / 172 / 218 / 219 explainer |

## Troubleshooting

### Error: "User claims refund for 2019 tax year"
The 6-year window (Section 160 ITO) closed for tax year 2019 on 31.12.2025. Explain that 2019 can no longer be claimed in 2026 and offer to check 2020 onward.

### Error: "Estimated refund is much larger than the user's expectations"
Re-check field 042 totals across all Form 106s and confirm whether the user actually had a תיאום מס in place for that year. Employer-side coordination significantly reduces the refund. Also verify the brackets used match that tax year, not 2026.

### Error: "Online portal rejects the user"
Most common cause is missing or expired digital identity. Direct the user to set up a Government Identity Document or smart-card identity at `gov.il`. If that fails, fall back to paper Form 135.

### Error: "Section 46 receipt, institution Section 46 approval expired during the year"
Section 46 approvals are issued for a defined period. If the institution's approval expired before the donation was made, the donation does not qualify. Ask the user to obtain a fresh confirmation from the institution stating the approval was active on the donation date.

### Error: "Disability exemption (Section 9(5)), refund estimate seems off"
Confirm the duration band (under 185 days does not qualify; 185-364 days uses the 81,960 ₪ short-term ceiling; 365 days and over uses 445,200 ₪), the income source (a pension under חוק הנכים or חוק נפגעי פעולות איבה uses the higher 684,000 ₪ ceiling), and the qualification basis (100% medical disability, blindness, or 90%+ via the multi-organ-injury calculation; a Bituach Leumi disability rating on its own is not enough). The full ceiling table is in `references/2026-rates.md`. For anything outside those bands, route the user to a Roeh Cheshbon experienced with Section 9(5) determinations.
