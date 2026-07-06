---
name: israeli-employee-tax-refund
description: "Walk salaried Israeli employees through the voluntary tax-refund process with Reshut HaMisim. Reads Form 106, detects refund triggers (job change, unemployment, maternity leave, reserve duty, Section 46 donations, yishuv mezakeh, missed credit points, disability, alimony, early keren hishtalmut withdrawal), estimates the refund using 2026 brackets and credit-point values, generates a per-trigger document checklist, and fills Form 135 or routes the user to the online refund portal. Knows the 6-year window (Section 160 ITO). Use when a salaried employee asks about Israeli tax refund, החזר מס לשכירים, טופס 135, miluim refund, or refunds for previous tax years. Do NOT use for self-employed Form 1301 filers (use israeli-tax-returns), payroll math (use israeli-payroll-calculator), stock options (use israeli-stock-options-tax), crypto (use israeli-crypto-tax-reporter), or VAT (use israeli-vat-reporting)."
license: MIT
allowed-tools: Bash(python:*) WebFetch
compatibility: Works with Claude Code, OpenClaw, Cursor, Windsurf, Codex, GitHub Copilot, opencode, antigravity.
---

# Israeli Employee Tax Refund

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
| Has foreign-source income in any year being claimed (US W-2, foreign rental, foreign brokerage) | `israeli-tax-returns`. Foreign income usually triggers a Form 1301 obligation; olim and returning residents in the Section 14 10-year window need a specialist. Do not auto-fold foreign income into a Form 135 refund. |
| Has a פיצויי פיטורים / severance / Form 161 event in any year being claimed | `israeli-tax-returns`. Severance carries Section 9(7A) exemption math, the תקרת פטור, and the רצף קצבה / רצף פיצויים choice. This skill mentions Form 161 only as an OCR target; the actual severance refund track belongs to israeli-tax-returns. |
| Wants prospective mid-year withholding adjustment | Use the Tax Authority's online תיאום מס at `gov.il/he/service/tax-coordination-online` (handles the current year), NOT this skill |

Ask the user:
- Tax year(s) in question (must be 2020 or later as of 2026, see Step 3)
- Were they salaried only during those years (no self-employment income)?
- Do they have all relevant Form 106 documents from each employer for each year?

### Step 2: Read Form 106 (אישור שנתי על משכורת ומס שנוכה)

Form 106 is the annual income summary the employer issues by March 31 of the following year (e.g., 106 for tax year 2025 is issued by 31.3.2026). Identify these fields:

| Field | Hebrew label | What it tells you |
|-------|--------------|-------------------|
| 042 | סה"כ מס שנוכה במקור | Total income tax withheld by this employer for the year. Sums across multiple 106s to get total withholding. |
| 158 / 172 | משכורת חייבת | Taxable salary. The base for the tax-due calculation. |
| 218 / 219 | הפקדה לקרן השתלמות | Keren hishtalmut deposit. Relevant for the early-withdrawal refund and the deduction cap check. |
| Months worked | חודשי עבודה | If less than 12, the user did not work the full year for this employer; common refund trigger. |

If the user has multiple Form 106s from the same tax year (job change), sum field 042 across them. The most common single refund driver is when each employer ran the withholding calculation as if its salary was the worker's only income for the year, producing cumulative over-withholding.

**Bituach Leumi annual confirmation feeds the same fields as Form 106.** If the user had any of these BTL income-replacement payments during the year, ask for the corresponding annual confirmation (אישור שנתי למס הכנסה) from Bituach Leumi (orderable from btl.gov.il) and aggregate it into the same totals you compute from Form 106:

| BTL payment | ITO treatment | Where on the refund form |
|---|---|---|
| דמי לידה (maternity) | Fully taxable as personal-exertion income; no Section 9 exemption | Gross goes to field 158/172; BTL-withheld tax to field 042 |
| דמי אבטלה (unemployment) | Fully taxable; no Section 9 exemption | Same: 158/172 + 042 |
| דמי פגיעה (short-term work injury, up to 91 days) | Fully taxable; distinct from later נכות מעבודה pension | Same: 158/172 + 042 |
| דמי שמירת היריון (pregnancy preservation) | Fully taxable; no Section 9 exemption | Same: 158/172 + 042 |
| תגמולי מילואים (reserve duty) | Usually paid via the employer, so already inside Form 106. Direct-from-BTL payments are the exception and produce their own BTL annual confirmation. | Already in 106 fields; only direct-paid portion adds to 158/172 + 042 |

The Section 9(6) family of exemptions (קצבת ילדים, זקנה, שאירים, נכות כללית, מענק לידה, ניידות) covers permanent or family-status BTL allowances, not income-replacement payments while temporarily out of work. Do not assume "BTL paid me, so it must be exempt" for maternity, unemployment, or work-injury per-diem.

A common misconception: the refund usually originates from the **salary side**, not the BTL side. BTL typically **under-withholds** on דמי לידה / דמי אבטלה, so the BTL portion alone can leave the recipient owing tax. The refund appears because the employer over-withheld during the months actually worked (monthly withholding assumed a full 12-month salary, but the year ended with fewer paid months). Once the year is reconciled, the net is usually a refund whose **source** is the salary withholding, not BTL.

### Step 3: Determine the Refund Window

The retroactive refund window is 6 calendar years from the end of the tax year, per Section 160 of the Income Tax Ordinance.

| Tax year | Last day to claim a refund |
|----------|---------------------------|
| 2020 | 31.12.2026 |
| 2021 | 31.12.2027 |
| 2022 | 31.12.2028 |
| 2023 | 31.12.2029 |
| 2024 | 31.12.2030 |
| 2025 | 31.12.2031 |

Years older than 2020 can no longer be claimed in 2026. Tell the user explicitly which years are still open and which have closed.

### Step 4: Detect Refund Triggers

Walk through this trigger list with the user. For each detected trigger, record it and the year(s) it applies to. Each trigger maps to a document requirement in Step 6.

| # | Trigger | When it applies | Statutory anchor |
|---|---------|----------------|------------------|
| 1 | Mid-year job change / multiple employers in same year | Two or more Form 106s for the same tax year and no תיאום מס was filed mid-year | Section 164 ITO (withholding mechanics) |
| 2 | Partial-year work / unemployment period | Less than 12 months worked in the year (Form 106 months field) | Withholding over-projection |
| 3 | Maternity / paternity leave | Received דמי לידה from Bituach Leumi during the year | Section 9(6) ITO; דמי לידה are taxable but at a different effective rate |
| 4 | Military reserve duty (מילואים) | 30+ days of reserve service in the prior tax year | Section 39B ITO (per Amendment 283, התשפ"ו-2025) |
| 5 | Charitable donations to recognized institutions | Total donations to Section 46-approved institutions ≥ 207 ₪ in the year (2026 minimum) | Section 46 ITO |
| 6 | Resident of yishuv mezakeh (settled area / periphery) | Center of life in an eligible locality for 12+ consecutive months; the locality appears on the annual official list | Section 11 ITO + Negev/Galilee Law |
| 7 | New immigrant credit points (סעיף 35) | Oleh chadash within the first 4.5 years of aliyah (54 months for olim arriving 2022 or later, 42 months for earlier arrivals). Per-month allotment is shown in Step 5. | Section 35 ITO + Amendment 262 of 2022 (note: this is the credit-points benefit, not a mortgage interest deduction) |
| 8 | Completed a bachelor's or master's degree | First bachelor's grants 1 credit point per study year up to 3 years (graduates 2023+), or 1 point for one tax year (graduates 2014-2022). First master's grants 0.5 point for 2 years (2023+) or 0.5 point for one year (2014-2022). | Section 40g ITO |
| 9 | Single-parent or paying alimony | Court judgment establishing single-parent status or paying child support | Sections 64, 65, 66 ITO |
| 10 | Disability tax exemption | Recognized 100% medical disability, blindness, or 90%+ disability under the multi-organ-injury calculation (פגיעה באיברים שונים); requires medical-board determination. 2026 ceiling on earned income exempt under the section: 445,200 ₪/year for disability lasting 365 days or more; 81,960 ₪/year for short-term disability (185-364 days). Higher 684,000 ₪ ceiling applies when the income is from a חוק הנכים / חוק נפגעי פעולות איבה pension. | Section 9(5) ITO |
| 11 | Self-deposit to pension or life insurance beyond the employer's deposit | Additional deposit by the employee directly to a pension fund or life insurance product. The credit rate under Section 45A is currently 35% of the qualifying deposit, applied to "insured salary" contributions. | Sections 45A and 47 ITO |
| 12 | Early keren hishtalmut withdrawal | Withdrew from a keren hishtalmut before 6 years; bank withheld 47% at source but real marginal rate is lower | Section 9(16a) + Section 164 ITO |
| 13 | Salaried employee paid more child credit points than employer recognized | Custody arrangement changed; employer's 101 form was not updated | Section 40 ITO |
| 14 | One-time bonus or 13th salary pushed a single month into a higher bracket | Israeli withholding is computed month by month. A December bonus, options exercise, or 13th-salary payment can land that month in the 35% or 47% band even though the annual marginal rate is much lower. Sum the bonus into the annual reconciliation. | Regulation 6 of תקנות מס הכנסה (ניכוי ממשכורת ומשכר עבודה) |
| 15 | Discharged soldier / national-service graduate credit points | Within 36 months of discharge, the חייל משוחרר box on the employer's Form 101 was not ticked, so the soldier's credit points were never applied at source. Very common for a first job taken soon after release. | Section per הטבת נקודות זיכוי לחיילים משוחררים (הוראת שעה) ITO |
| 16 | Child or spouse who is נטול יכולת (severely disabled) | The taxpayer (or their spouse) has a child who is paralyzed, blind, or has an intellectual-developmental disability. 2 credit points, never applied at source (needs Form 116א). Distinct from trigger 10 (the taxpayer's OWN disability). | Section 45(a) ITO |
| 17 | Maintaining a disabled relative in an institution | The taxpayer funds the institutional care (מוסד) of an incapacitated child, spouse, or parent. A 35% credit, claimed on Form 116. Choose EITHER this (trigger 17) OR trigger 16 for the same child, whichever is larger, not both. | Section 44 ITO + תקנות תשנ"ו-1996 |

Triggers 16 and 17 are mutually exclusive for the same relative: a taxpayer cannot take both the Section 45(a) 2 credit points and the Section 44 institution credit for the same child. Compute both and keep the larger. Both require Form 116/116א with medical certification, so they are almost never applied at source and are high-yield retroactive claims.

Separately, if the user is a low-income worker (the two-job, low-wage, reserve-duty persona), also check מענק עבודה (the earned-income / negative-income-tax grant). It is NOT a Form 135 refund; it is a separate claim paid by Bituach Leumi, so route the user to `btl.gov.il` (מענק עבודה) in addition to any Form 135 refund. Do not fold it into the refund estimate.

Trigger 7 clarification (common misinformation): there is no "Section 35 mortgage interest deduction for olim". Section 35 grants credit points on a declining schedule (the per-month rates are in Step 5's allotment table and `references/2026-rates.md`): 8.5 points over 54 months for olim arriving 1.1.2022 or later, or 7.5 points over 42 months for pre-2022 arrivals. Do not promise the user a "mortgage interest refund" under Section 35. Section 35 points are NOT available to ordinary returning residents (תושב חוזר), who instead get the Section 14 foreign-income exemption; route returning residents and veteran returning residents (תושב חוזר ותיק) to `israeli-tax-returns`.



### Step 5: Estimate the Refund

Estimate the refund as (correct tax under the brackets and credits) minus (tax actually withheld per the sum of field 042 across all Form 106s for the year). Use these 2026 figures.

**2026 monthly tax brackets for employees:**

| Monthly salary band | Annual band | Marginal rate |
|---------------------|-------------|---------------|
| Up to 7,010 ₪ | Up to 84,120 ₪ | 10% |
| 7,011 - 10,060 ₪ | 84,121 - 120,720 ₪ | 14% |
| 10,061 - 19,000 ₪ | 120,721 - 228,000 ₪ | 20% |
| 19,001 - 25,100 ₪ | 228,001 - 301,200 ₪ | 31% |
| 25,101 - 46,690 ₪ | 301,201 - 560,280 ₪ | 35% |
| 46,691 ₪ and above | 560,281 ₪ and above | 47% (Section 121 ITO top bracket) |
| Plus mas yesafim | Annual income above 721,560 ₪ | Additional 3% surtax (Section 121B ITO), applied on top of the 47% |

For prior tax years, look up the brackets that applied to that year (do not extrapolate the 2026 brackets backward).

**2026 credit-point (נקודת זיכוי) values:**

| Period | Value |
|--------|-------|
| Per month | 242 ₪ |
| Per year | 2,904 ₪ |

**Default credit-point allotment for a salaried resident:**

| Recipient | Points per year |
|-----------|-----------------|
| Israeli resident (base) | 2.25 |
| Female resident (additional 0.5) | 2.75 |
| Each child up to age 5 (2024+ schedule, per parent) | 2.5 in birth year, 4.5 age 1, 4.5 age 2, 3.5 age 3, 2.5 age 4, 2.5 age 5 |
| Each child age 6-17 (to mother, post-2022) | 2 |
| Each child age 6-17 (to father) | 1 |
| Each child age 6-17 (pre-2022) | 1 (mother) / 0 (father) |
| Single parent (חד-הורי) | Additional points per scheme |
| New immigrant (post-2022 arrival) | 1 point year 1, 3 points years 1.5-2.5, 2 points year 3, 1 point year 4 (per Step 4 trigger 7 table) |
| Master's graduate (2023+) | 0.5 point per year for 2 years after graduation |
| Bachelor's graduate (2023+) | 1 point per study year, capped at 3 years |
| Discharged soldier / national-service graduate | 2 points/year (full service: 23+ months men, 22+ months women) or 1 point/year (shorter service over 1 year), for 36 months from the month after discharge. 2 points = 5,808 ₪/year; 1 point = 2,904 ₪/year at the 2026 value |
| Parent of a נטול יכולת child (Section 45(a)) | 2 points/year (5,808 ₪) per paralyzed / blind / intellectual-developmental-disability child, including the spouse's child; claimed on Form 116א, not applied at source |

**Section 44 institution credit (not a credit point):** a taxpayer funding a relative's stay in an institution (מוסד) may claim 35% of the amount paid above 12.5% of the taxpayer's income, provided the disabled relative's annual taxable income is under 188,000 ₪ (or 301,000 ₪ for a couple) in 2026. Claimed on Form 116.

**Reserve-duty credit-point bonus (Section 39B, Amendment 283 התשפ"ו-2025):**

| Days served in the tax year | Points awarded | Annual value at 2,904 ₪/point |
|-----------------------------|----------------|-------------------------------|
| 30-39 | 0.5 | 1,452 ₪ |
| 40-49 | 0.75 | 2,178 ₪ |
| 50-54 | 1.0 | 2,904 ₪ |
| Each additional 5 days | +0.25 | +726 ₪ |
| Maximum | 4.0 | 11,616 ₪ |

The reserve-duty points are realized in the tax year **after** the service, so a soldier who served 60 days in 2025 claims them on the 2026 refund.

**Donation credit (Section 46):**

A donation of 207 ₪ or more (2026 minimum) to a Section-46-approved institution returns 35% of the donated amount as a credit. The annual ceiling is 10,354,816 ₪ or 30% of taxable income, whichever is lower. Receipts may be original, certified copy, or electronic (the latter marked מסמך ממוחשב). Always confirm the receiving institution still holds an active Section 46 approval for the year of the donation by checking the Tax Authority's approved-institutions list.

**Yishuv mezakeh credit:**

Residents of eligible localities receive a percentage discount on tax due, capped at a NIS ceiling. The list of eligible localities and the per-locality percentage is published annually by the Tax Authority. Always check the current list against the user's residence year by year, since localities are added and removed over time.

Present the estimate as a range, not a single number, and remind the user that the Tax Authority's actual calculation may differ once the supporting documents are reviewed.

### Step 6: Generate the Document Checklist

Based on the detected triggers, build a personalized document list. Common items by trigger:

| Trigger | Required documents |
|---------|-------------------|
| All claims | Form 106 from every employer for the year; teudat zehut + ספח; bank account confirmation (אישור ניהול חשבון) for the refund payout |
| Multiple employers | Sum field 042 across all 106s; show pay-by-pay reconciliation if the gap is large |
| Partial year / unemployment | Bituach Leumi annual confirmation (אישור על קצבאות) listing months and amounts of unemployment / חל"ת |
| Maternity/paternity leave | Bituach Leumi דמי לידה annual confirmation |
| Reserve duty | טופס 3010 (אישור על ימי מילואים) from the IDF reserve unit |
| Section 46 donations | Original signed receipts from each Section-46-approved institution; confirm the institution's number appears on the Tax Authority's approved list for that year |
| Yishuv mezakeh | אישור תושבות from the local authority for each year claimed (12+ months residence) |
| New immigrant | Teudat oleh + date of aliyah |
| Section 40g (academic) | Diploma + transcript (verifies completion year) |
| Single parent / alimony | Court judgment + bank transfer records for alimony payments |
| Section 9(5) disability | Medical-board determination (ועדה רפואית) + ratification by the Tax Authority's disability committee |
| Sections 45A / 47 pension and life insurance | Annual deposit certificate (אישור הפקדה שנתי) from the pension/insurance provider |
| Keren hishtalmut early withdrawal | תלוש משיכה from the keren showing 47% withholding |
| Discharged soldier (trigger 15) | תעודת שחרור / אישור שירות showing discharge date and service length; the employer's Form 101 for the year |
| נטול יכולת child/spouse (trigger 16, Section 45(a)) | Form 116א + medical certification of the paralysis / blindness / intellectual-developmental disability |
| Institution care (trigger 17, Section 44) | Form 116 + institution payment receipts + the disabled relative's income confirmation |

Always remind the user to keep copies; the Tax Authority can request originals later.

### Step 7: Choose the Submission Channel

There are two main channels for an employee voluntary refund.

| Channel | When to use | Where |
|---------|-------------|-------|
| Online refund portal (השכיר המקוון / מערכת מקוונת להחזר מס לשכירים) | The user is not obligated to file a Form 1301; they have a digital government identity (Government Identity Document or smart-card); they have scanned PDFs of their supporting documents | `secapp.taxes.gov.il` (see Reference Links) |
| Manual Form 135 | The user prefers paper, the online portal does not support their case, or the user's identity verification cannot be completed online | Fill Form 135 (available at `gov.il/he/service/itc135`) and submit at the appropriate משרד שומה / pekid shuma assigned to the user's address |

If the user is required to file a Form 1301 (e.g., income above the surtax threshold for that year, foreign income, or capital gains in the same year), neither track applies for that year, route them to `israeli-tax-returns` and include the refund calculation inside Form 1301.

### Step 7.5: Prospective Fix via Form 101 (Highly Important)

If you found a refund trigger that is **ongoing** (the user is still a single parent, still an oleh inside the credit-points window, still resides in a yishuv mezakeh, still has children in the right age band, still actively serving reserve duty), tell the user to update their Form 101 at the employer for the CURRENT and following year. Form 101 is the document that sets the credit-points basis the employer uses for withholding.

Without this prospective fix, the user will file the same refund every year for the same missed credit. The retrospective refund (this skill's output) returns last year's over-withholding; updating Form 101 stops the over-withholding going forward.

The user should submit the updated 101 to their HR / payroll department, attach the same supporting documents the refund used (תעודת עולה, אישור תושבות, custody court order, etc.), and ask payroll to recompute withholding starting the next pay period.

### Step 8: Submit and Track

After submission:

- The Tax Authority must process and pay the refund within one year from the assessment date, or two years from the end of the tax year, whichever is later.
- Refunds paid after that statutory window accrue הצמדה (CPI linkage) plus 4% annual interest, paid on top of the principal.
- The user can check status at the same portal where they submitted.
- If the user receives a "drisha להשלמת מסמכים" (request to supplement documents), respond within the stated deadline or the request closes and a new application is required.

## Examples

### Example 1: Refund After Two Jobs in 2024

A salaried developer worked 6 months at Employer A (gross 25,000 ₪/month) and then 6 months at Employer B (gross 22,000 ₪/month) in 2024. No mid-year תיאום מס was filed.

1. Collect Form 106 from both employers. Field 042: 24,800 ₪ withheld at A; 22,400 ₪ withheld at B; total 47,200 ₪.
2. Compute the correct annual tax based on aggregate income of 282,000 ₪ and the 2024 brackets. The estimator script with default points (2.75) returns a tax due of about 43,700 ₪.
3. Trigger 1 detected: mid-year job change. Estimated refund range: 3,100 to 3,800 ₪.
4. Document checklist: both Form 106s, teudat zehut, bank confirmation.
5. Channel: online portal (no Form 1301 obligation).
6. Year 2024 deadline: 31.12.2030.

### Example 2: Reserve Duty Refund for 2025 Service

A salaried teacher served 65 days of reserve duty in 2025. Reserve-duty credit points are claimed on the 2026 tax return (or via refund request) because they are realized the year after the service.

1. Section 39B / Amendment 283 schedule: 50 days = 1.0 point. The 15 additional days (over 50) at +0.25 per 5 days = +0.75 points. Total = 1.75 points.
2. Value: 1.75 × 2,904 ₪ = 5,082 ₪ refund expected for 2026.
3. Document: Form 3010 from the reserve unit listing 65 days served in 2025.
4. Submit via online portal for tax year 2026 after the 2026 Form 106 is issued (by 31.3.2027).

### Example 3: Section 46 Donations for 2022

An employee donated 6,000 ₪ to three Section-46-approved nonprofits in 2022 but never claimed the credit.

1. Trigger 5 detected. Amount 6,000 ₪ × 35% = 2,100 ₪ credit.
2. Deadline check: 2022 closes 31.12.2028. Still open.
3. Document checklist: signed original receipts from each institution; verify each institution's Section-46 approval was active in 2022 against the Tax Authority's historical approved list.
4. Channel: online portal or Form 135.
5. Note: the 1.1.2026 digital-reporting rule does not apply retroactively to 2022 donations; paper receipts are sufficient for that year.

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
| `kolzchut` | Live authoritative rights pages for every refund trigger (current-year credit-point values, donation ceiling, miluim points table, yishuv mezakeh list, disability criteria). Use it whenever a figure in this skill needs to be re-verified against the latest Kol-Zchut publication. |

Companion skill: `hebrew-ocr-forms` can extract field 042 / 158 / 172 / 218 from scanned Form 106 and Form 161 PDFs before this skill consumes them.

## Gotchas

- The 6-year window is measured from the **end** of the tax year (Section 160 ITO), not from the date the employer issued Form 106. The 2020 deadline is 31.12.2026, not 31.3.2026.
- Reserve-duty credit points (Section 39B / Amendment 283) are realized in the year **after** the service. A soldier who served in 2024 claims them on the 2025 refund, not the 2024 refund.
- Section 35 (oleh credit points) is not "mortgage interest deduction". Do not promise the user a mortgage refund under Section 35.
- Section 46 receipts are valid as original, certified copy, or electronic (מסמך ממוחשב). Confirm the receiving institution held an active Section 46 approval for the donation year.
- Filing a refund request opens the whole tax year to assessment: a marginal case can come back as a **demand to pay**, and any refund is first offset against existing income-tax, Bituach Leumi, מזונות, or הוצאה לפועל debts.
- If the user is obligated to file a Form 1301 (income above the surtax threshold, foreign assets, mixed income), neither Form 135 nor the online refund portal applies. Route them to `israeli-tax-returns` and integrate the refund computation inside the 1301.
- Prospective mid-year withholding adjustment (תיאום מס) and retrospective refund (Form 135 / online portal) are different mechanisms. תיאום מס handles the current year before it closes; refund handles years that already closed. Users frequently conflate them.
- Yishuv mezakeh requires center of life in the locality for 12 consecutive months. Spending part of the year elsewhere can disqualify the year.

## Reference Links

| Source | URL | What to check |
|--------|-----|---------------|
| Tax Authority Form 135 official page | https://www.gov.il/he/service/itc135 | Current Form 135 PDF, who files, attachments |
| Online refund portal | https://secapp.taxes.gov.il | Authentication flow, supported document uploads |
| Online refund landing page | https://www.gov.il/he/pages/sa300821-2 | Eligibility for the online track |
| Kol-Zchut: refund overview | https://www.kolzchut.org.il/he/%D7%94%D7%97%D7%96%D7%A8_%D7%9E%D7%A1_%D7%94%D7%9B%D7%A0%D7%A1%D7%94 | 6-year window, statutory processing time, 4% interest + הצמדה |
| Kol-Zchut: 2026 credit points | https://www.kolzchut.org.il/he/%D7%A0%D7%A7%D7%95%D7%93%D7%95%D7%AA_%D7%96%D7%99%D7%9B%D7%95%D7%99_%D7%9E%D7%9E%D7%A1_%D7%94%D7%9B%D7%A0%D7%A1%D7%94 | Current monthly point value (242 ₪) and category list |
| Kol-Zchut: reserve-duty points | https://www.kolzchut.org.il/he/%D7%A0%D7%A7%D7%95%D7%93%D7%95%D7%AA_%D7%96%D7%99%D7%9B%D7%95%D7%99_%D7%9E%D7%9E%D7%A1_%D7%94%D7%9B%D7%A0%D7%A1%D7%94_%D7%9C%D7%9C%D7%95%D7%97%D7%9E%D7%99_%D7%9E%D7%99%D7%9C%D7%95%D7%90%D7%99%D7%9D | Section 39B schedule per Amendment 283 |
| Kol-Zchut: Section 46 donations | https://www.kolzchut.org.il/he/%D7%96%D7%99%D7%9B%D7%95%D7%99_%D7%9E%D7%9E%D7%A1_%D7%94%D7%9B%D7%A0%D7%A1%D7%94_%D7%91%D7%A9%D7%9C_%D7%AA%D7%A8%D7%95%D7%9E%D7%94_(%D7%A1%D7%A2%D7%99%D7%A3_46) | 207 ₪ minimum, 10,354,816 ₪ ceiling, 35% credit rate, 2026 digital-reporting rule |
| Kol-Zchut: yishuv mezakeh | https://www.kolzchut.org.il/he/%D7%96%D7%99%D7%9B%D7%95%D7%99_%D7%9E%D7%9E%D7%A1_%D7%94%D7%9B%D7%A0%D7%A1%D7%94_%D7%9C%D7%AA%D7%95%D7%A9%D7%91%D7%99%D7%9D_%D7%91%D7%A4%D7%A8%D7%99%D7%A4%D7%A8%D7%99%D7%94 | Annual settled-area list and per-locality percentages |
| Kol-Zchut: Form 106 overview | https://www.kolzchut.org.il/he/%D7%98%D7%95%D7%A4%D7%A1_106 | What Form 106 is, when it is issued, who issues it |
| Claltax: Form 106 field map | https://claltax.com/%D7%98%D7%95%D7%A4%D7%A1-106-%D7%A9%D7%9B%D7%99%D7%A8-%D7%95%D7%92%D7%9E%D7%9C%D7%90%D7%99/ | Field 042 / 158 / 172 / 218 / 219 explainer with Hebrew labels |
| Kol-Zchut: income tax brackets | https://www.kolzchut.org.il/he/%D7%9E%D7%93%D7%A8%D7%92%D7%95%D7%AA_%D7%9E%D7%A1_%D7%94%D7%9B%D7%A0%D7%A1%D7%94 | 2026 monthly and annual bracket table |
| Kol-Zchut: Section 9(5) disability exemption | https://www.kolzchut.org.il/he/%D7%A4%D7%98%D7%95%D7%A8_%D7%9E%D7%9E%D7%A1_%D7%94%D7%9B%D7%A0%D7%A1%D7%94_%D7%9C%D7%90%D7%A0%D7%A9%D7%99%D7%9D_%D7%A2%D7%9D_%D7%A0%D7%9B%D7%95%D7%AA | 2026 ceilings: 445,200 / 81,960 / 684,000 ₪ |
| Kol-Zchut: discharged-soldier credit points | https://www.kolzchut.org.il/he/%D7%A0%D7%A7%D7%95%D7%93%D7%95%D7%AA_%D7%96%D7%99%D7%9B%D7%95%D7%99_%D7%9E%D7%9E%D7%A1_%D7%94%D7%9B%D7%A0%D7%A1%D7%94_%D7%9C%D7%97%D7%99%D7%99%D7%9C%D7%99%D7%9D_%D7%9E%D7%A9%D7%95%D7%97%D7%A8%D7%A8%D7%99%D7%9D_%D7%95%D7%9E%D7%A1%D7%99%D7%99%D7%9E%D7%99_%D7%A9%D7%99%D7%A8%D7%95%D7%AA_%D7%9C%D7%90%D7%95%D7%9E%D7%99-%D7%90%D7%96%D7%A8%D7%97%D7%99 | 1 vs 2 points, 36-month window, 2026 value |
| Tax Authority: Form 116א disabled-relative credit | https://www.gov.il/he/service/itc-request-for-tax-credits-disabled-relative | Section 45(a) / Section 44 claim, medical certification, 2026 income caps |
| Bituach Leumi: annual confirmation for income tax | https://www.btl.gov.il | Order the annual אישור שנתי למס הכנסה for maternity, unemployment, work-injury, pregnancy-preservation payments |
| FinBiz Academy: maternity tax pattern | https://finbizacademy.co.il/baby_born/ | Why the salary side is the typical refund source after maternity / unpaid leave (BTL typically under-withholds) |

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
Confirm three details before computing:
1. Disability duration. Under 185 days does not qualify. 185-364 days uses the short-term ceiling of 81,960 ₪/year exempt earned income. 365 days and over uses the long-term ceiling of 445,200 ₪/year.
2. Income source. Pensions paid under חוק הנכים or חוק נפגעי פעולות איבה use the higher 684,000 ₪/year ceiling instead.
3. Qualification basis. 100% medical disability, blindness, OR 90%+ via the multi-organ-injury calculation all qualify. Anything less does not, even if the user has a Bituach Leumi disability rating.

For any case that is not clearly inside one of the standard ceilings, route the user to a Roeh Cheshbon experienced with Section 9(5) determinations.
