---
name: israeli-trapped-profits-planner
description: "Not tax advice. Computes a closely-held Israeli company's exposure under the two Amendment 277 regimes: the Section 81B 2% addition to tax on undistributed excess profits, and Section 62A attribution of company income to an active shareholder. Works out excess profits, tests all three shields and takes the highest, checks the three statutory escapes on their correct and different bases (6% of accumulated profits, 50% of excess profits, the 10% loss test), applies the transitional 20% route and the protection bands earned in 2025, and names the reporting vehicle (Form 1214 with Annex 2B). Use when a chevrat me'atim has retained earnings and you need its 2% exposure, are deciding how much to distribute before year end, or are testing Section 62A wallet-company classification. Do NOT use for comparing profit-extraction methods (use israeli-corporate-tax-strategy) or for filing the annual return (use israeli-tax-returns)."
license: MIT
compatibility: Works with Claude Code, Cursor, Windsurf, Codex, GitHub Copilot, opencode, OpenClaw, antigravity, Gemini CLI, Gemini Spark, Grok, ChatGPT, Claude.ai, Claude Desktop, Manus. No bundled scripts, so every listed host runs the full workflow.
---

# Israeli Trapped Profits Planner

## Legal notice

This is a free information tool operated by an AI model. It explains the trapped-profits and wallet-company rules and helps you organise your own figures. All of its outputs are produced automatically by an AI model, with no involvement, review, or approval by a tax adviser or accountant. The output is not a tax opinion, not a computation prepared by a licensed representative, and not professional advice. It is a general explanation and arithmetic aid only: it does not examine the company's full financial position or its complete documents. An AI model may err, omit data, or present a wrong conclusion.

Any figure or worksheet this tool produces is an automatic draft for your own preparation. It is not a filed return and not a distribution decision. Responsibility for the computation, the reporting and the tax is yours, the binding assessment is the Tax Authority's, and representation before the Tax Authority is reserved to those permitted by law. Whether a distribution is lawful under the Companies Law is a separate question from whether it is tax-effective, and belongs to counsel. Consult a tax adviser or accountant before distributing or filing. All use of its output is the user's sole responsibility.

## Problem

Amendment 277 created two separate regimes on the same commencement date, and the guidance in circulation collapses them. Section 62A attributes company income to an active shareholder at marginal rates. Sections 81A to 81F impose a 2% addition to tax on undistributed excess profits. They use different bases, different escape routes, and both use the number NIS 750,000 for opposite purposes. The published shorthand compounds this: "distribute 6% to avoid the tax" attaches the right rate to the wrong base, "choose between 50% or paying 6%" turns a distribution into a tax, and the 2% is routinely described as falling on retained earnings rather than on excess profits net of the year's dividend. A company that sizes its distribution off any of those gets the wrong answer.

## Instructions

### Step 1: Gate on the entity and the year

Both regimes reach only a **chevrat me'atim** as defined in section 76: controlled by not more than five individuals, not a subsidiary, and not a company in which the public has a substantial interest. Section 81B additionally reaches only a company **resident in Israel**, even where some or all of its share capital is held by foreign residents. Foreign shareholding does not exempt the company.

Both apply from 1 January 2025. Establish the examined tax year before anything else, because two of the computation's inputs are read at different year ends.

If the company is not a chevrat me'atim, answer that and stop. There is no computation to run.

### Step 2: Compute excess profits, and respect the two measurement dates

Section 81C computes excess profits as:

```
  taxable accumulated profits  at the end of the year PRECEDING the examined year
- the HIGHEST of the three shields, computed at the end of the EXAMINED year
= excess profits
```

Two different year ends. A calculator that reads both legs at the same date is wrong for any company whose balance sheet moved during the year.

Where the highest shield equals or exceeds taxable accumulated profits, excess profits are nil and there is nothing for the 2% to attach to. Report that as zero exposure. Do not carry a negative figure forward or treat it as a credit; the primary sources describe no such carryforward.

**Taxable accumulated profits** are accumulated profits less exempt accumulated profits. The exempt-profits apparatus exists only to produce this figure; see `references/computation.md` for the alternatives and their deductions.

### Step 3: Compute all three shields and take the highest, never the sum

| Shield | Definition |
|---|---|
| **Magen kaspi** | A flat NIS 750,000 |
| **Magen hotzaot** | The **higher** of the tax-deductible expenses in the tax year, or the **average** of tax-deductible expenses in the tax year and the two preceding tax years |
| **Magen nechasim** | Cost of the company's assets, **less** the cost of special assets, **less** equity (share capital including premium and reserves), **less** the balance of a loan from a related party, **plus** the cost of a held body corporate |

**"Special assets" is a defined term, and it is the most variable input.** It comprises securities,
financial assets, intangible assets, rights in land, loans and cash equivalents. Watch the
loan boundary in particular: the circular gives indicia for treating a customers balance as really
a loan, namely a credit period longer than usual for that kind of transaction, interest or linkage
charged on the unsettled balance, a structure of fixed payments over time, and the provision of
security or guarantees. Getting this wrong moves the largest of the three shields.

Three points that change the result:

- The computation subtracts the **highest** of the three. Summing them is the largest possible overstatement.
- The magen hotzaot is a maximum-of-two, not simply this year's expenses. Using only the current year understates the shield for a company with a shrinking cost base.
- The magen nechasim has **two positive terms and three negative ones**. The held-body-corporate cost is added, not subtracted. Mis-signing any single term changes the answer.

**The magen kaspi is not per company.** Where the controlling shareholder, alone or together with a relative, is an individual who controls further closely-held companies, the NIS 750,000 is divided **equally** among the held companies unless the company notifies a different division. The other held companies must notify the assessing officer, on the section 131 return, that they waive their pro-rata share and did not elect it for that year. Control for this rule means holding 50% or more of the means of control. A group owner who assumes NIS 750,000 per company overstates the shield by a multiple.

### Step 4: Apply the charge

Section 81B charges an addition to tax, for every tax year, at **2% of the excess profits as computed under section 81C, after deducting the amount of dividend distributed during the tax year**.

The base is not the accumulated balance, not retained earnings, and not a shortfall against any required distribution.

Two consequences that must appear in any effective-rate figure:

- Section 81D: amounts paid as the addition are **not deductible** from the company's taxable income.
- Section 81F(a): the addition is treated as corporate tax, but is **not part of corporate tax** for computing tax under the Ordinance. So it sits on top of the section 126(a) rate and cannot be credited against it. Quote 23% plus 2% on the relevant base, never a netted number.
- Section 81F(b): the advance-payment provisions do **not** apply to the addition. Users expecting mikdamot will not find them.

### Step 5: Test the three escapes, each on its own base

Under section 81B(b) the addition is not imposed in any of these cases. The bases differ and this is where most published guidance goes wrong.

| Escape | Test | Base |
|---|---|---|
| Loss test | Current-year losses under sections 28, 29 and 92 exceed 10% | **Accumulated** profits, end of preceding year |
| The 50% alternative | Taxed dividends distributed exceed 50% | **Excess** profits, end of preceding year (itself a two-date construct: accumulated profits at the preceding year end, shields at the examined year end). Reduced for a company in the 20% route, see Step 6 |
| The 6% alternative | Taxed dividends distributed are 6% or more | **Accumulated** profits, end of preceding year |

Accumulated profits and excess profits are different, usually very different, numbers: excess profits are accumulated profits less exempt profits less the highest shield. Presenting "6% or 50%" as two rates on one base is wrong.

**Price the escape against the charge before recommending either.** The skill's job is not to help
the user satisfy an escape; it is to tell them whether satisfying one is worth it. Escaping a
company-level charge of 2% of excess profits costs the shareholder tax on the WHOLE distribution at
their dividend rate, plus any surtax. For a company with a large accumulated balance and modest
excess profits, paying the 2% is often cheaper than escaping it, and the correct answer is
"distribute nothing and accrue the addition". Frame it as a comparison and let the figures decide:

```
  cost of escaping  = the required distribution  x  the shareholder's dividend rate (plus surtax)
  cost of not escaping = 2%  x  excess profits, net of any dividend distributed in the year
```

No rate needs to be quoted to set this up, and this skill does not quote the shareholder-level
surtax because it was not verified against the Ordinance during authoring. Ask the user's
representative for the applicable shareholder rate and run the comparison with it.

Three details that decide real cases:

- **The loss test runs on the net loss.** To avoid the addition, the loss after offsetting losses from the company's other sources must reduce accumulated profits by at least 10%.
- **The dividend is deducted in the charge but not in the 50% test.** The circular says so expressly: in the 50% alternative, the dividends distributed during the year are not to be deducted from the excess profits against which the 50% is measured. The same dividend therefore behaves differently in the two computations, and a naive implementation double-counts it and wrongly clears the safe harbour.
- **Not every dividend counts.** A "dividend on which tax was paid in respect of its distribution" is either a dividend other than one excluded from the recipient's income by section 126(b), or a section 126(b)-excluded dividend for which the distributing company **elected** that tax be paid at the highest rate applicable under sections 125B and 121B. An ordinary tax-exempt inter-company dividend does not count toward either safe harbour unless that election is made and the tax paid.

### Step 6: Apply the transitional provisions, which are the live question for 2026

Two separate mechanisms, plus one that has closed. Do not merge them.

**The 20% route, section 5(a). It has TWO limbs and both change a number.** A company with undistributed accumulated profits on the eve of commencement day that distributes taxed dividends of 20% or more of its profits remaining from commencement day, in a year of tax years **2025 to 2030**, gets both of these for that year. The rate does not change by year.

- **Limb (1):** excess profits for the year are reduced by those remaining profits.
- **Limb (2), easy to miss and it moves the safe harbour:** section 81B(b)(2), the 50% escape, is read with "less the profits remaining from the profits at the end of tax year 2024" appended. That quantity is the company's excess profits at the end of 2024, less profits already distributed to shareholders as taxed dividends. So for a company in the 20% route the **denominator of the 50% test is reduced**, and a company sized off the unreduced base is told to distribute more than the Law requires, or is told it fails a safe harbour it actually clears.

**The protection bands, section 5(b).** These are not annual rates. They are measured **once**, on a distribution inside the Determining Period, which ran to
**30 November 2025**. The dividend must have been **both paid by the company AND received by the
recipient** inside that window; a dividend declared or paid out late in November but received after
it does not count. Meeting a band extends the section 5(a) treatment into later years without a
further distribution:

| Distributed in the Determining Period | Provisions apply in |
|---|---|
| Between 35% and 60% | 2026 |
| Between 60% and 75% | 2026 and 2027 |
| Between 75% and 90% | 2026 to 2028 |
| 90% or more | 2026 to 2029 |

**All four bands cover 2026.** So a company that met even the lowest band last year gets the section
5(a) treatment this year **without distributing again**. Section 5(b) opens "without derogating from
subsection (a)" and makes the paragraph (1) and (2) provisions apply ALSO in the listed years, so the
band is an independent trigger for the same benefit, not a further condition on top of the annual
20% route.

**Be precise about what "covered" means.** It does NOT mean the 2% disappears. The paragraph (1)
benefit is that excess profits for the year are **reduced by the profits remaining from
commencement-day profits**. A company that distributed heavily in the Determining Period has little
remaining, so its reduction is correspondingly small, though its exposure is smaller too. Compute the
reduction; do not report the band as an exemption.

The Law drafts the bands as open ranges, "between X and Y", with no tie-breaking rule at 60%, 75% or 90%. A distribution landing exactly on a boundary is genuinely unresolved on the face of the Law. Say so and route it to a professional rather than picking a side.

**The 5% escape, section 5(c), 2025 only and now closed.** A company was not liable to the addition in 2025 where taxed dividends distributed in the Determining Period were 5% or more of accumulated profits at the end of the preceding year, **provided the tax on the distribution was paid by 31 December 2025**. This is a **distinct provision** from the standing 6% alternative under section 81B(b)(3), which remains available every year. Be precise about how they differ, because they are not unrelated: both are measured on the **same base**, accumulated profits at the end of the preceding tax year, and both require dividends on which tax was paid. What differs is the **rate** (5% against 6%), the **window** (the Determining Period, against the tax year itself), and section 5(c)'s extra condition that the tax be paid by 31 December 2025. So a source describing the relief as "5% until November 2025 then 6% from 2026" is wrong about the structure, not merely about the dates: one is a closed transitional escape, the other a standing alternative, and neither replaced the other.

### Step 7: Section 62A, the separate attribution regime

Run this alongside, not instead. A company can be caught by section 62A and still owe the section 81B addition.

**Classification.** Amendment 277 changed two tests and left the four-or-more-employees exclusion intact:

- The officeholder limb now turns on a holder of **25% or more** of one of the means of control in the **other** body corporate, **on any day in the tax year**. Note it is "25% or more", not "more than 25%".
- The single-client window became **at least 22 months out of a period of three years**, replacing 30
  months out of four years. **This limb also has a percentage element that this skill does not state,**
  because it could not be quoted from primary text during authoring. So the limb cannot be concluded
  here: satisfying the duration test alone does not tell you whether it bites. Establish the
  percentage from the consolidated Ordinance, or route the classification to the user's
  representative. Do not report a negative on the strength of the months test by itself.

The Ordinance calls the person a **baal shlita** (controlling shareholder) in this section. Text describing a "baal menayot mahuti" here is quoting repealed drafting.

**Status caveat.** The replacement circular for section 62A was published as a draft for public
comment and no final version was located during authoring, so the older circular remains the
standing published interpretation. Do not present draft positions as settled, and re-check this
before relying on a classification.

**The excess-profitability limb, 62A(a1).** The attributed amount is:

```
  taxable income from labour-intensive personal-exertion activity
- 25% x ( INCOME from that activity  -  payments to a related company )
```

Two different income quantities appear in one formula: taxable income in the first term, gross income inside the bracket, and the bracket is net of payments to a related company. It is not "the portion above a 25% margin". Attribution is pro rata to each active shareholder's share in the rights to the company's profits.

Paragraph (1) has only two conditions: activity income below thirty million shekels multiplied by the number of controlling shareholders (a controlling shareholder and their relative counting as one), and a profitability rate exceeding 25%.

**The NIS 750,000 in section 62A is not a condition of paragraph (1).** It sits in the exclusion at 62A(a1)(2)(c), which is framed negatively, is gated on the company having a substantial holder, and offers two independent escapes. One of them aggregates accumulated profits **across all companies** in which that person is a substantial holder. So a person with several companies, each individually below the figure but jointly above it, fails the aggregate escape while passing a naive per-company test. Do not flatten this into "accumulated profits must exceed 750,000".

The same number in section 81C is a **shield subtracted from the base**. Same figure, opposite job.

### Step 7a: The 35% inter-company route

Where a dividend would be excluded from an Israeli corporate recipient's income under section
126(b), it does not count toward either dividend escape unless the distributing company elects to
pay tax on it. The mechanism is withholding at **35%** of the dividend distributed by the close
company, under which the dividend is treated as if distributed indirectly to all its shareholders,
with a deemed dividend imputed to each of them. This is the route a holding structure reaches for
when profits need to move up a chain, and it is what turns an otherwise-exempt inter-company
dividend into one that counts toward the safe harbours.

Circular 2/2026 also provides an alternative route that avoids immediate 35% withholding where the
dividend is passed through to the final shareholders in the same year with advance written
confirmation. It is conditional and confirmation-dependent, not available on demand. Model a group
chain-wide before quoting any figure; a computation correct for a single company is wrong for a group.

### Step 8: Name the reporting route and the dates

There is **no dedicated standalone form** for the trapped-profits declaration. It rides on the company's annual return:

- **Form 1214 with Annex 2B**, the report under the Dividends on which Tax was Paid Regulations 5785-2025.
- The section 131 return also carries the magen kaspi waiver notice for held companies.
- Form 856 is the annual withholding reconciliation. It belongs in the withholding row, not the declaration row. Any source telling you the declaration is filed on 856 is wrong.

**The 16 January date.** Where the company reports an election of the section 81B(b)(2) or (3) alternative, the distribution is deemed made on the **last day of the examined tax year**, and the tax on it is due per regulation 13 for a December distribution, that is by **16 January of the year following the examined year**. So 16 January 2026 for tax year 2025, 16 January 2027 for 2026. It recurs annually and is not a one-off transitional deadline.

## Examples

### Example 1: Single company, deciding whether to distribute before year end

Take the company's accumulated profits at the previous year end, subtract exempt accumulated
profits to get taxable accumulated profits, then compute all three shields at the examined year
end and subtract only the highest. That gives excess profits, and the untreated charge is the 2%
on it.

Now price the two dividend escapes side by side, and note they run on different figures: the 6%
alternative is measured on **accumulated** profits, while the 50% alternative is measured on
**excess** profits. Because excess profits are accumulated profits less exempt profits less the
highest shield, the two tests can point to very different distributions. Work both, present both,
and let the user's representative choose. The difference between the two bases is the whole
decision, and it is the point most published guidance gets wrong.

### Example 2: Group owner assuming the shield is per company

The same owner controls four closely-held companies outright. The magen kaspi is divided equally, so each company shields 187,500, not 750,000. Three of the four must also notify the assessing officer on their section 131 return that they waive their pro-rata share. Recompute every company's excess profits on the divided shield before quoting any exposure.

### Example 3: Company that distributed in the Determining Period

The company made a Determining Period distribution falling in the 60% to 75% band, so the section 5(a)
treatment applies in **2026 and 2027** with no further distribution required. Do not stop there and
report the company as having no exposure. The paragraph (1) benefit is a **reduction** of excess
profits by the profits remaining from commencement-day profits, so compute the residual: a company
whose excess profits exceed those remaining profits still pays 2% on the balance. Then flag that 2028
will need either a fresh 20% distribution or one of the standing escapes.

### Example 4: Section 62A attribution, using the Tax Authority's own worked figures

The Tax Authority's published example takes a closely-held company with taxable income of NIS 1,000,000 in 2025 on which it paid corporate tax at 23%. Work the attribution and the shareholder's return fields from that example rather than inventing figures; the credit is grossed on the attributed income while the withholding is on the net dividend, and field 084 on the individual's return carries income transferred under section 62A(a) on the dividend alternative.

## Bundled Resources

### References

- `references/computation.md`: excess profits, the accumulated-profits alternatives, the four deduction mechanisms, and the shields in full.
- `references/transitional.md`: sections 5(a), 5(b) and 5(c), year by year to 2030.
- `references/section-62a.md`: the classification limbs, the attribution formula, and the reporting fields.
- `references/domain-checklist.md`: the coverage contract this skill is maintained against.

## Recommended MCP Servers

| MCP | Use for |
|---|---|
| `israel-amutot` | Confirming a company's registration details from the Corporations Authority registry |
| `israeli-cbs` | The index used where a figure is linked, and general macro context |

No MCP supplies a company's own accumulated profits or expenses. Those come from the financial statements the user provides.

## Gotchas

1. **Attaching the 6% to excess profits.** The 6% runs on **accumulated** profits, expressly before deducting exempt profits and before deducting the shields. Six percent of accumulated profits is normally a much larger cheque than 6% of excess profits, so a user who sizes the distribution off the wrong base under-distributes and fails the safe harbour.
2. **Deducting the dividend twice.** It reduces the 2% charging base and does **not** reduce the denominator of the 50% test. Deducting it in both places wrongly clears the safe harbour.
3. **Reading both legs of the excess-profits formula at the same date.** Accumulated profits at the preceding year end, shields at the examined year end.
4. **Summing the shields.** Take the highest.
5. **Assuming the NIS 750,000 shield is per company.** It divides equally across a group under one controlling individual at 50% or more.
6. **Treating the two NIS 750,000 figures as the same threshold.** In section 62A it is an exclusion that switches attribution off; in section 81C it is a shield subtracted from the base.
7. **Calling the 2% an alternative to distributing.** It is a charge on excess profits net of the year's dividend; distributing reduces the base and, at the right level, triggers a separate statutory escape.
8. **Quoting a netted effective rate.** The addition is not deductible and not creditable, so it is 23% plus 2% on the relevant base.
9. **Sending the user to form 856 for the declaration.** The declaration rides on form 1214 with Annex 2B.

## Reference Links

| Source | URL | What to check |
|---|---|---|
| Income Tax Circular 7/2025 as amended 08.02.2026 | https://www.gov.il/BlobFolder/policy/professional-directives-191025/he/IncomeTax_professional-directives-080226.pdf | The charging section, the three shields, the anti-splitting rule, the three escapes at para 3.6, sections 81D and 81F, the transitional provisions |
| Income Tax Circular 2/2026 | https://www.gov.il/BlobFolder/policy/professional-directives-250126-1/he/IncomeTax_professional-directives-250126-1.pdf | Annex 2B and form 1214, the 35% inter-company route, withholding dates and certificates |
| Amendment 277, Reshumot, 31.12.2024 | https://fs.knesset.gov.il/25/law/25_lsr_5396731.pdf | Sections 5(a), 5(b) and 5(c); the section 62A amendments including the 22-month window and the 25% test |
| Tax Authority guidance letter 2025-001394 | https://www.gov.il/BlobFolder/dynamiccollectorresultitem/represent-info-231225-1/he/spokesman_announcment_pa231225-1.pdf | The section 62A reporting mechanisms, the worked example, and the new return fields |

## Troubleshooting

### "The user does not have the exempt-profits split"

Taxable accumulated profits require accumulated profits less exempt accumulated profits, and the exempt figure depends on which alternative the company used. Without it the excess-profits figure cannot be computed. Ask for the financial statements and the prior year's computation rather than assuming the whole balance is taxable.

### "The distribution lands exactly on a band boundary"

The Law says "between 35% and 60%" and so on, with no tie-breaking rule at the boundaries. Do not pick a side. State that the point is unresolved on the face of the Law and route it to the company's representative.

### "The company is caught by both section 62A and section 81B"

Both can apply in the same year. Apply section 62A first to fix attributed income and the company's taxable income, establish whether the attributed amounts were removed from retained earnings, and only then compute accumulated profits for the section 81 machinery. Whether a section 62A dividend can simultaneously count toward the section 81B safe harbours is not addressed in the primary sources; flag it as requiring professional advice rather than asserting an answer.

### "Should the company liquidate to escape the regime?"

The statutory window for that route closed at the end of tax year 2025. Explain it as history, not as a live option, and note that a liquidation decision is a corporate-law matter for counsel in any event.
