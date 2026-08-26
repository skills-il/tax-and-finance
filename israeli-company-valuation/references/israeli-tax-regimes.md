# Israeli Tax Regimes for Valuation

The effective tax rate is the input generic valuation models get wrong most often. This file is the decision tree. Every rate here is sourced in `evidence.json`.

## Why this matters to the valuation

The tax rate enters in two places that must agree:

1. The tax on EBIT inside free cash flow to firm.
2. The tax shield on debt inside the WACC.

Using the standard rate in one and a preferred rate in the other is a silent inconsistency. Using the standard rate for a company that actually pays a preferred rate overstates the tax drag by more than half and understates the company.

## Decision tree

Ask in this order.

**1. Is the company part of a multinational group large enough to fall under the minimum top-up tax?**
Israel enacted a domestic minimum top-up tax on 31 December 2025, applying to fiscal years beginning on or after 1 January 2026, to groups with consolidated revenue above EUR 750 million in at least two of the four preceding fiscal years. For such a group, the Israeli effective rate on Israeli-located profit cannot sit below 15%, so a model projecting 6% to 12% for it is projecting a rate that no longer survives.

Note what Israel did NOT enact. There is no income inclusion rule and no undertaxed profits rule at this stage. The consequence is directional: Israel tops up low-taxed profit located in Israel, and does not top up an Israeli-parented group's low-taxed foreign subsidiaries, which remain exposed to top-up abroad. So the domestic tax mainly changes WHERE the top-up is collected, not whether it exists.

**2. Does the company hold a status under the Encouragement of Capital Investments Law?**
Ask for the approval, do not infer it from the sector. Then place it:

| Status | Development area A | Rest of country |
|---|---|---|
| Preferred Enterprise | 7.5% | 16% |
| Special Preferred Enterprise | 5% | 8%, for ten years |
| Preferred Technology Enterprise | 7.5% | 12% |
| Special Preferred Technology Enterprise | 6% | 6% |

Technology-enterprise rates apply only to the portion of intellectual property developed in Israel, on a nexus basis. A company with mixed IP origin has a blended rate, not the headline rate.

After ten years, Special Preferred Enterprise rates revert to Preferred Enterprise rates unless a new investment program requalifies the company.

**3. If no preferred status, is it a closely held company?**
Three rules, all introduced or reshaped by Amendment 277 (published 31 December 2024, in force from tax year 2025). None of them changes the corporate rate on ordinary trading income, but all three change how much cash the company can retain, which is a cash-flow input and affects the treatment of surplus cash on the balance sheet.

**(a) The 2% charge on undistributed profits, sections 81א to 81ו.** The base is NOT flat accumulated profits. It is accumulated taxable profits, less dividends already distributed, less the HIGHEST of three shields (a monetary shield, an allowable-expenses shield, and an asset-cost shield). The monetary shield is split among commonly controlled closely held companies, so it is not a per-company allowance. Read the current shield amounts out of circular 7/2025 rather than from any summary, including this one. Two escape routes are set in section 81ב(ב): distribute 6% of accumulated profits, or 50% of the EXCESS profits (the shielded figure, not accumulated profits). The two bases differ by a wide margin, so read the route off the section rather than off any summary, including this one. The election used to have to be reported by 30 April of the following tax year; the Israel Tax Authority replaced that in its 8 February 2026 update with the earlier of the filing date of the return for the examined year or the end of the following tax year. A source still quoting 30 April is quoting superseded guidance.

Critically for this skill: profits sourced from Encouragement-Law income (preferred income, technological income, approved-enterprise income) are excluded from the base. That exclusion operates at the level of the PROFITS, not the company, so a preferred enterprise's passive or other non-qualifying profits remain fully inside the charge. Do not model a preferred enterprise as exempt from it. Governing guidance is ITA circular 7/2025 of 19 October 2025, as updated 8 February 2026.

**(b) Excess profitability, section 62א(א1).** The 25% does two jobs at once, and treating it as only a trigger is the common error. It is an entry condition (the profitability rate must exceed 25%) AND the deducted normal return: take the company's income from personal-exertion-intensive activity, subtract payments to a related company, deduct 25% of that difference, and the remainder is the excess profitability. That remainder is deemed the active shareholder's own section 2(1) earned income, pro rata to their rights in profits, at marginal rates. A later distribution of it is not taxed again. Two conditions must BOTH hold. The company's income from personal-exertion-intensive activity in the tax year must be below ILS 30 million multiplied by the number of controlling shareholders that year, with a controlling shareholder and his relative counted as one. And the company's profitability rate that year must exceed 25%. So the 25% is doing two jobs at once, as the entry trigger and as the deducted normal return, and the section is aimed at owner-managed companies rather than large ones.

**(c) Attribution to the individual, section 62א(א).** Two DIFFERENT limbs, with different tests and different escapes. Summaries routinely merge them, and merging them is what produces false positives.

- **Paragraph (1), the officer and management-services limb.** Where the company's income arises from the individual acting as an officer (נושא משרה) of another body, or supplying management and similar services to it, that income is attributed to the individual. This is the limb that carries the 25% escape: it does not apply to an individual holding, directly or indirectly, 25% or more of one of the means of control in that other body on any day in the tax year.
- **Paragraph (3), the employee-like-services limb.** Income is attributed where 70% or more of the company's total or taxable income for the year, excluding defined special income and gains, arises from services supplied by the individual or a relative to ONE person or their relative, for at least 22 months out of a three-year period. Amendment 277 shortened that window from 30 months out of 48, so a summary citing 30/48 is quoting repealed text. Note the retroactive bite: once the 22 months are up, the individual's activity is treated as employment from the day the service began.

Two things follow that are easy to get wrong. The 25% escape belongs to paragraph (1) and does NOT rescue a company from paragraph (3). And paragraph (3) has its own escape, in paragraph (5): it does not apply at all to a closely held company employing four or more workers, counting someone employed up to four hours a day as half, pro-rating part-year employment, and counting a person together with a relative as one.

A single dominant customer in one year is NOT enough to trigger paragraph (3). The duration test and the four-employee exclusion are what stop that false positive, and both are the limbs most often dropped from summaries.

**3b. Is the company on a PRE-2017 grandfathered status?**
The five current tracks are not the whole population. Amendment 68 closed the Approved Enterprise and Beneficiary Enterprise regimes to new entrants, but a company with a pre-reform election year continues under its original terms for the remainder of its benefit period, and a company can waive that status onto the current regime by filing with the Israel Tax Authority. So a long-established Israeli industrial company, which is squarely this skill's target profile, may be on none of the five rows above.

Two consequences for the model. The corporate rates on those legacy tracks differ from the current ones, and the alternative track can carry a full exemption for a set number of years. And the dividend withholding is 15%, not 20%, for an enterprise whose election year precedes 2014. From 1 January 2014 preferred income distributes at 20% even where the income arose earlier, because the rate attaches to the distribution date rather than the earning year, so ask for the election year and the distribution date separately.

Ask for the approval document and the election year. Do not infer the regime from the sector or from the founding date.

**4. Otherwise:** the standard corporate rate of 23%.

## Eligibility gates worth verifying before accepting a reduced rate

| Status | Gates |
|---|---|
| Preferred Technology Enterprise | FOUR cumulative conditions, not two. (1) Group revenue under ILS 10 billion. (2) R&D over the three preceding years at or above 7% of company income on average, or exceeding ILS 75 million a year. (3) The competitiveness test, by reference to section 18א(ג)(1) or (2). (4) EITHER one of the secondary tests below OR an Israel Innovation Authority certification that the enterprise promotes innovation. Secondary tests, any one suffices: at least 20% of employees are ones whose entire salary was booked as R&D, or at least 200 such employees; a venture capital fund invested at least ILS 8 million and the company has not since changed its field of activity; average revenue growth of at least 25% a year over three years with at least ILS 10 million of turnover in each; or average headcount growth of at least 25% a year with at least 50 employees in each. A company that clears revenue and R&D but fails all of these and holds no certification pays 23%, not 12%. Governing guidance is ITA circular 9/2017 on Amendment 73. |
| Special Preferred Technology Enterprise | Meets the technology conditions, and group revenue of at least ILS 10 billion. |
| Special Preferred Enterprise | Revenue of at least ILS 1 billion, in a group generating at least ILS 10 billion in the same industrial sector. |

R&D centres are not entitled to a reduced corporate rate where the controlling shareholders or beneficiaries are Israeli residents. Check this before granting a preferred rate to a local R&D subsidiary.

## Dividend withholding, by regime

The owner's net depends on extraction, not just on company-level tax.

| Regime | Dividend withholding |
|---|---|
| Preferred Enterprise | 20%, reducible under treaty |
| Special Preferred Enterprise | 20%, reducible under treaty |
| Preferred Technology Enterprise | 4% to a foreign company where at least 90% of shares are foreign-held, otherwise 20% |
| Special Preferred Technology Enterprise | Same as Preferred Technology Enterprise |
| Pre-2017 Approved or Beneficiary Enterprise | 15% where the election year precedes 2014. From 1 January 2014 preferred income distributes at 20% regardless of when it was earned |

## Persistence into terminal value

A preferred status is conditional and time-limited, not permanent. Before carrying a reduced rate into terminal value, ask:

- Do the eligibility conditions hold across the whole forecast?
- Does the status have a stated expiry?
- Is the R&D spend threshold likely to keep being met at forecast revenue levels? A company that grows revenue fast can fail a percentage-of-revenue R&D test precisely because it grew.

If the status may lapse, model a rate step-up and disclose it. Assuming a reduced rate forever is a substantive assumption that belongs in the assumptions table, not buried in a cell.

## IP disposals

Companies selling IP to a related foreign company may qualify for a reduced 12% capital gains rate where the IP was acquired from a foreign company after 1 January 2017 for at least ILS 200 million, subject to Israel Innovation Authority approval. Relevant when the valuation supports an IP migration rather than a share sale.

## What to verify at each update

Rates and thresholds here move with legislation. Re-verify against the Israel Tax Authority and the PwC summary cited in `evidence.json` at every skill update, and specifically re-check:

- The standard corporate rate.
- Whether the closely held company percentages changed.
- Whether the preferred-enterprise rates or eligibility thresholds changed.
- The minimum top-up tax scope, and specifically whether Israel has since added an income inclusion rule or an undertaxed profits rule.
- The shield amounts and the reporting deadline for the section 81ב(ב) escape routes, which the Israel Tax Authority has already moved once.
- Whether the ILS 30 million ceiling in section 62א(א1), the 22-of-36-months window in section 62א(א)(3), or the four-employee exclusion in section 62א(א)(5) has been amended.
