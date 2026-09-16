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

Two different year ends. A calculator using one date for both is wrong whenever the balance sheet moved.

Where the highest shield equals or exceeds taxable accumulated profits, excess profits are nil and there is nothing for the 2% to attach to. Report that as zero exposure. Quick screen: if taxable accumulated profits do not exceed the magen kaspi available to this company, stop here, since the highest shield is at least that. In a group the available amount is this company's equal share, or the share under the division the companies notified; a company that waived its share has none (Step 3). Do not carry a negative figure forward or treat it as a credit; the primary sources describe no such carryforward.

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

**The carve-outs are as load-bearing as the list.** Not every right in land or every cash balance is
special. Excluded: land held for **self-use** as a fixed asset under GAAP, even where another group
entity uses it (a building leased to third parties, such as a mall, is NOT self-use); a rental
building under section 53(a3), or an institutional-rental building under section 53A, of the
Encouragement of Capital Investments Law; and cash pledged or deposited under a Sale (Apartments)
Law financial-accompaniment agreement, as approved by the company's accountant. And the asset shield
runs on **tax cost** (business-inventory cost, the original-price balance under section 88, or the
acquisition-value balance under section 47 of the Real Estate Taxation Law), not on book or fair
value. Full list and the circular's worked example in `references/computation.md`.

Two exclusions that remove a shield or shrink one:

- **Second exempt-profits alternative: no magen nechasim.** A company that chose the second alternative for computing exempt accumulated profits cannot use the asset shield when computing excess profits (section 81C(c), circular 2.13). Compare only the magen kaspi and the magen hotzaot.
- **The magen hotzaot counts only tax-deductible expenses** (circular 4.3). It excludes expenses capitalised to the balance sheet and not yet released to profit and loss, and expenses for acquiring special assets or tied to them, for example depreciation on a special asset or financing costs on a loan that funded one.

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
| The 50% alternative | Taxed dividends distributed exceed 50% | **Excess** profits "to the end of the preceding tax year" (circular 3.6.2). Which year end the shields inside this base are read at is unresolved, see below. Reduced for a company in the 20% route, see Step 6 |
| The 6% alternative | Taxed dividends distributed are 6% or more | **Accumulated** profits, end of preceding year |

Accumulated profits and excess profits are different, usually very different, numbers: excess profits are accumulated profits less exempt profits less the highest shield. Presenting "6% or 50%" as two rates on one base is wrong.

**The 50% base has an open dating question.** Circular 3.6.2 measures it against "הרווחים העודפים של חברת המעטים לתום שנת המס הקודמת" (excess profits to the end of the preceding tax year), while the charging computation reads the shields at the end of the examined year. The circular does not say, on its face, whether the shields inside the 50% base are read at the preceding or the examined year end. Compute the base both ways, report both, and flag the gap to the user's representative rather than picking one.

**Price the escape against the charge before presenting either, and price it correctly.** For a company whose profits will be distributed eventually, escaping does not ADD the shareholder's dividend tax; it mostly brings that tax FORWARD. The 2%, by contrast, is a permanent cost that repeats in every year it applies. So compare:

```
  cost of escaping     = time value of paying the shareholder tax earlier
                         + any rate or surtax difference between distributing now and later
                         + the lost use of that cash inside the company
  cost of not escaping = the cumulative 2% charges over the years the charge would apply
```

Quote no shareholder rate or surtax (not verified against the Ordinance); take them from the user's representative. Where the profits would genuinely never be distributed, say so and treat that as a separate assumption. Detail in `references/computation.md`.

**Price it over several years, not one.** The 2% recurs every tax year while excess profits remain,
so test the escapes year by year. The primary sources used here do not carry one year's
qualifying distribution into a later year, except the section 5(a) treatment a company earns
through a protection band (Step 6). Outside that, assume an escape relied on in a later year must
be met again in that year, and flag it as an assumption. Lay the comparison out year by year over the planning
horizon, with the base shrinking as distributions leave the company.

Three details that decide real cases:

- **The loss test runs on the net loss.** To avoid the addition, the loss after offsetting losses from the company's other sources must reduce accumulated profits by at least 10%.
- **The dividend is deducted in the charge but not in the 50% test.** The circular says so expressly: in the 50% alternative, the dividends distributed during the year are not to be deducted from the excess profits against which the 50% is measured. The same dividend therefore behaves differently in the two computations, and a naive implementation double-counts it and wrongly clears the safe harbour.
- **Not every dividend counts.** A "dividend on which tax was paid in respect of its distribution" is either a dividend other than one excluded from the recipient's income by section 126(b), or a section 126(b)-excluded dividend for which the distributing company **elected** that tax be paid at the highest rate applicable under sections 125B and 121B. That two-limb definition sits in the 6% paragraph (circular 3.6.3.1 and 3.6.3.2), so on the circular's face an elected 126(b) dividend counts toward the **6%** alternative. The 50% alternative's own wording (3.6.2) covers dividends "שהוא אינו דיבידנד שחלות עליו הוראות סעיף 126(ב)", which excludes 126(b) dividends. Whether an elected 126(b) dividend also counts toward the 50% test is **unresolved**; flag it, and never rely on it to clear the 50% test.

### Step 6: Apply the transitional provisions, which are the live question for 2026

Two separate mechanisms, plus one that has closed. Do not merge them.

**A possible precondition (circular 6.4).** The circular states that the transitional provisions apply only if the company distributed 50% of the excess profits accumulated from tax year 2025. It is the circular's condition, not section 5's wording, and its effect on 2025 and on a company that earned a 5(b) band is unclear. Compute the relief with and without it and flag the gap; never call a company disqualified on this ground alone. And the circular defines "profits remaining from commencement-day profits" two ways: from accumulated profits at 31.12.2024 (6.3), and from excess profits at the end of 2025 (6.8.2). It is internally inconsistent; compute both and flag. See `references/transitional.md`.

**The 20% route, section 5(a). It has TWO limbs and both change a number.** A company with undistributed accumulated profits on the eve of commencement day that distributes taxed dividends of 20% or more of its profits remaining from commencement day, in a year of tax years **2025 to 2030**, gets both of these for that year. The rate does not change by year.

- **Limb (1):** excess profits for the year are reduced by those remaining profits.
- **Limb (2), easy to miss:** the 50% escape is read with "less the profits remaining from the profits at the end of tax year 2024" appended, so the **denominator of the 50% test is reduced**. Sizing off the unreduced base overstates the required distribution.

**The protection bands, section 5(b).** Measured **once**, on a distribution inside the Determining Period ending **30 November 2025**, **both paid by the company AND received by the recipient** in that window. A band extends the section 5(a) treatment without a further distribution:

| Distributed in the Determining Period | Provisions apply in |
|---|---|
| Between 35% and 60% | 2026 |
| Between 60% and 75% | 2026 and 2027 |
| Between 75% and 90% | 2026 to 2028 |
| 90% or more | 2026 to 2029 |

**All four bands cover 2026**, as an independent trigger ("without derogating from subsection (a)"), not a condition on the annual 20% route. **"Covered" does NOT mean the 2% disappears:** limb (1) only reduces excess profits by the remaining profits; compute it. The bands are open ranges with no tie-break at 60%, 75% or 90%; a distribution exactly on a boundary is unresolved, route it out.

**The 5% escape, section 5(c), 2025 only and closed.** Taxed dividends of 5% or more of accumulated profits at the end of the preceding year, distributed in the Determining Period, **with the tax paid by 31 December 2025**. A distinct provision from the standing 6% alternative, not its predecessor; see `references/transitional.md`.

### Step 7: Section 62A, the separate attribution regime

Run this alongside, not instead. A company can be caught by section 62A and still owe the section 81B addition. Full detail in `references/section-62a.md`.

**Classification.** Amendment 277 changed two tests and left the four-or-more-employees exclusion intact:

- The officeholder limb turns on a holder of **25% or more** (not "more than 25%") of one of the means of control in the **other** body corporate, **on any day in the tax year**.
- The single-client window became **at least 22 months out of three years**, replacing 30 months out of four. Its percentage element is **not stated** here (not quotable from primary text), so the months test alone never supports a negative. Establish it from the consolidated Ordinance or route it out.

The Ordinance calls the person a **baal shlita** in this section; "baal menayot mahuti" is repealed drafting. The replacement 62A circular was located only as a draft for comment, so the older circular remains the standing interpretation; re-check before relying on a classification.

**The excess-profitability limb, 62A(a1).** The attributed amount is:

```
  taxable income from labour-intensive personal-exertion activity
- 25% x ( INCOME from that activity  -  payments to a related company )
```

Taxable income in the first term, gross income inside the bracket, net of payments to a related company. It is not "the portion above a 25% margin". Attribution is pro rata to each active shareholder's share in profits. Paragraph (1) has two conditions: activity income below thirty million shekels multiplied by the number of controlling shareholders (with a relative counting as one), and a profitability rate exceeding 25%.

**Two gaps this skill does not close:** the numerator and denominator of the profitability rate, and whether the four-or-more-employees exclusion reaches this new limb. Establish both or route them out.

**The NIS 750,000 in section 62A is not a condition of paragraph (1).** It sits in the negatively framed exclusion at 62A(a1)(2)(c), gated on a substantial holder, with two independent escapes, one of which aggregates accumulated profits **across all companies** the person substantially holds. Several companies each below the figure but jointly above it fail that escape. In section 81C the same number is a **shield subtracted from the base**.

### Step 7a: The 35% inter-company route

Where a dividend would be excluded from an Israeli corporate recipient's income under section
126(b), it does not count toward the 6% alternative unless the distributing company elects to
pay tax on it, and whether even the election qualifies it for the 50% alternative is unresolved (Step 5). The mechanism is withholding at **35%** of the dividend distributed by the close
company, under which the dividend is treated as if distributed indirectly to all its shareholders,
with a deemed dividend imputed to each of them. This is the route a holding structure reaches for
when profits need to move up a chain, and it is what turns an otherwise-exempt inter-company
dividend into one that counts toward the 6% alternative.

Circular 2/2026 also has a conditional pass-through route that avoids immediate 35% withholding. Model a group chain-wide before quoting any figure.

### Step 8: Name the reporting route and the dates

There is **no dedicated standalone form** for the trapped-profits declaration. It rides on the company's annual return:

- **Form 1214 with Annex 2B**, the report under the Dividends on which Tax was Paid Regulations 5785-2025.
- The section 131 return also carries the magen kaspi waiver notice for held companies.
- Form 856 is the annual withholding reconciliation. It belongs in the withholding row, not the declaration row. Any source telling you the declaration is filed on 856 is wrong.

**Two different payment dates, do not merge them.**

- **The 2% addition itself** (circular 5.2 and 5.3) is due by the date for filing the section 132 return (31 May, or per an extension granted to the representative, whichever is later) or by the end of the tax year following the examined year, **whichever is earlier**. Linkage and interest differences under section 159A(a) run from that date until actual payment. No advances are paid on it (Step 4).
- **The tax on a dividend relied on for an escape** belongs to the distribution, not to the 2%, and its date depends on the route (circular 5.4 and 5.5). An ordinary dividend under section 81B(b)(3)(a): by the 16th of the month following the distribution. A section 81B(b)(3)(b) distribution to an intermediate company with 35% withheld: by 16 January of the following year, but only where the distribution report is attributed to December. A distribution reported as an election under 5.5: by 16 January, as below.

**The 16 January date.** Where the company reports an election of the section 81B(b)(2) or (3) alternative, the distribution is deemed made on the **last day of the examined tax year**, and the tax on it is due per regulation 13 for a December distribution, that is by **16 January of the year following the examined year**. So 16 January 2026 for tax year 2025, 16 January 2027 for 2026. It recurs annually and is not a one-off transitional deadline.

## Examples

### Example 1: Single company, deciding whether to distribute (illustrative figures)

All figures are **invented for illustration**, in shekels, for one company with no group and no
transitional route, and no dividend yet in the year.

1. Accumulated profits at the preceding year end: 3,000,000. Exempt accumulated profits: 200,000.
   Taxable accumulated profits: 3,000,000 - 200,000 = **2,800,000**.
2. Magen kaspi: 750,000 (single company, no division).
3. Magen hotzaot: expenses of 400,000 this year and 350,000 and 300,000 in the two preceding years.
   Average (400,000 + 350,000 + 300,000) / 3 = 350,000. Higher of 400,000 and 350,000: **400,000**.
4. Magen nechasim, net at tax cost: **500,000**.
5. Highest shield: max(750,000, 400,000, 500,000) = **750,000**. Never the sum (1,650,000).
6. Excess profits: 2,800,000 - 750,000 = **2,050,000**.
7. Untreated charge: 2% x 2,050,000 = **41,000**, due on the Step 8 payment date.
8. 6% escape: 6% x 3,000,000 (accumulated, before exempt profits and shields) = **180,000** of taxed dividends.
9. 50% escape: dividends must **exceed** 50% x 2,050,000 = 1,025,000, so more than **1,025,000**
   (here the shields did not move between year ends; where they do, compute both, Step 5).
10. Result: distributing 180,000 of taxed dividends meets the 6% alternative, so **no addition is
    imposed at all** for the year.
11. Price it: the 41,000 is a permanent cost. Distributing 180,000 mainly brings the shareholder
    tax on it forward. Compare that timing cost (plus any rate difference and lost use of the cash)
    with the 2% charges over every year they would apply (Step 5).

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

The Tax Authority's published example takes a closely-held company with taxable income of NIS 1,000,000 in 2025 on which it paid corporate tax at 23%. Work from that example rather than inventing figures: the credit is grossed on the attributed income, the withholding is on the net dividend, and field 084 carries income transferred under section 62A(a) on the dividend alternative.

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
3. **Reading both legs of the excess-profits formula at the same date.** For the charge: accumulated profits at the preceding year end, shields at the examined year end. For the 50% base the shields' date is not resolved by the circular; compute both (Step 5).
4. **Summing the shields.** Take the highest.
5. **Assuming the NIS 750,000 shield is per company.** It divides equally across a group under one controlling individual at 50% or more.
6. **Treating the two NIS 750,000 figures as the same threshold.** In section 62A it is an exclusion that switches attribution off; in section 81C it is a shield subtracted from the base.
7. **Calling the 2% an alternative to distributing.** It is a charge on excess profits net of the year's dividend; distributing reduces the base and, at the right level, triggers a separate statutory escape.
8. **Quoting a netted effective rate.** The addition is not deductible and not creditable, so it is 23% plus 2% on the relevant base.
9. **Sending the user to form 856 for the declaration.** The declaration rides on form 1214 with Annex 2B.
10. **Treating a tax-effective distribution as a lawful one.** The Companies Law profit and solvency tests are separate from every test in this skill; clearing the 6% alternative says nothing about whether the company may distribute.

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

### "The company has fewer than two preceding tax years"

The circular defines the magen hotzaot average over the tax year and the two preceding tax years, and does not say how to compute it for a younger company. Do not invent a shorter average. Use the current-year deductible expenses as the floor for the magen hotzaot (the first limb of the maximum is always available), and flag the average as undefined for the representative.

### "Should the company liquidate to escape the regime?"

The statutory window for that route closed at the end of tax year 2025. Explain it as history, not as a live option, and note that a liquidation decision is a corporate-law matter for counsel in any event.
