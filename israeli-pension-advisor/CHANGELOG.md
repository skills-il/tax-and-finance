# Changelog

## 2.6.0 - 2026-10-01

- Tikun 190: removed the claim that a Bituach Leumi old-age pension counts toward
  the minimum pension; it does not. The minimum-pension test (5,306 in 2026) is
  applied when a lump sum is taken, not at deposit, and the monthly route needs
  only age 60+. Added the first-38,412-per-year qualifying-pension tranche and the
  death-before-75 / after-75 rules.
- Kupat gemel lehashkaa: lump sum is taxed 25% on the real gain at any age, and a
  monthly pension from 60 is exempt. The skill previously said "marginal rate".
- Self-employed mandatory pension: the obligation runs to early-retirement age 60,
  not legal retirement age; the new-business exemption is "fewer than 6 months
  since first VAT registration at year end", not "the first calendar year"; added
  the 55-on-01.01.2017 exemption and the correct statute (Economic Efficiency Law
  2016, Chapter B). Script updated to match.
- Employees: removed the false "deposits above 679 earn a deduction" rule; added
  the employer-exclusion ceilings (34,423/month tagmulim salary cap, 45,600/year
  severance) and the self-employed 5% vs 5.5% credit rule.
- Form 161: silence defaults to rezef-kitzbah only when severance in kitzbah funds
  is within the 405,900 default ceiling and there are no non-kupah grants.
- Nayadut: the 10-business-day transfer deadline is now sourced to reg. 5(a) of
  the 2008 Transfer Regulations, resolving a two-cycle carry.
- Keren hishtalmut: early withdrawal by an employee taxes employer deposits AND
  gains; withdrawal is also allowed after 3 years at retirement age.
- Form 161ד renamed to its official title (fixation of rights, kibua zechuyot);
  "gibush kitzbaot" removed.
- New references/approaching-retirement.md: Bituach Leumi old-age pension income
  test and deferral increment, the transition grant for women born 1960-1966,
  commutation (hivun) rules, Form 161ד, and budget-pension routing.
- Example 2 no longer ranks hishtalmut over pension; the ceilings are presented
  neutrally.
- Exempt-pension schedule attributed to Amendment 275 (December 2024).
- Pension-adviser note corrected to the Pension Advice Law s.19(a)(2): an adviser
  may take a distribution fee with the client's written consent; the "meshavek"
  category and the "no commissions" claim were removed.
- Heichum kitzbah window anchored to the eligibility age: the cut-off is about 35
  for men but about 33 for women born 1970 or later (was a flat "under ~35").
- Self-employed credit and deduction tiers now say they apply to a beneficiary
  member (amit mutav, 26,436 NIS in 2026).
- Form 161ג described as the request to revert a rezef election (not a route for
  returning withdrawn severance); the unsourced "return with interest" route was
  removed.
- Added the 90-day deadline for the commutation exemption and the 300-day
  unemployment entitlement for women born 1960+ aged 57+.
- Examples 1, 3 and 4 and Step 8 reworded to explain options and trade-offs
  without recommending a product or a choice for the user.
- Moved the Section 14 sub-cases to references/tax-benefits.md and the Hebrew
  cohort table and troubleshooting to references/, bringing both SKILL.md and
  SKILL_HE.md under the 5,000-word cap with matching section counts.

## 2.5.0 - 2026-08-19

- Tikun 190 lump-sum tax base corrected to the NOMINAL gain (15%) in the three
  English passages that still said "real (CPI-adjusted) gain". The skill now
  states the base once and agrees across SKILL.md, SKILL_HE.md,
  references/tax-benefits.md and references/pension-fund-types.md.
- Mandatory pension contributions are now computed on the tzav-harchava
  insurable ceiling (the average wage, 13,769) instead of twice it. The script
  previously overstated the compulsory employer obligation for every salary
  above the average wage.
- Women's retirement age in scripts/calculate_pension.py is resolved from the
  per-cohort birth-year table via a new --birth-year flag, replacing a flat
  63.25 that shorted a woman born 1968 by 15 months.
- Added the 1959-and-earlier cohort (flat 62) so the retirement-age lookup is
  total, in both the reference table and the Hebrew inline table.
- Named the Bituach Leumi maximum insurable income (51,910/month from
  01.01.2026) as explicitly NOT one of this skill's pension ceilings.
- Retirement projections now model the deposit base actually contributed and
  disclose it, and the annuity factor tracks the resolved retirement age.
- Re-verified the 2026 ceilings (9,700 / 13,750 / 15,712 / 5,306 / 13,769)
  directly against the Tax Authority's 2026 monthly-deductions booklet.
- Hedged the nayadut transfer deadline and the Form 161 Part B window, which
  could not be re-verified because their sources block automated fetches.
- Moved Step 9 (life events) to references/life-events.md, bringing SKILL.md
  back under the 5,000-word validator cap it was already breaching.

## 2.4.1 - 2026-08-11

Retirement age for women is set by DATE OF BIRTH, not by calendar year. Replaced the '65 by 2032' calendar framing with the statutory rule (65 for women born 1970 or later), corrected the cohort range from 1960-1965 to 1960-1970+, corrected the law citation to the Retirement Age Law 5764-2004 as amended in force from January 2022, and added the full per-cohort table. Moved Troubleshooting to references/ because SKILL.md was already over the 5,000-word cap.

All notable changes to this skill are documented here.

## [2.4.0] - 2026-08-09

### Changed

- שם הסקיל עודכן ל"ניווט פנסיה וחיסכון בישראל". השם הקודם כלל את המילה "יועץ", והסקיל אינו מספק ייעוץ פנסיוני אלא הסבר על המערכת.
- התיאור נפתח כעת בהבהרה שהפלט אינו ייעוץ פנסיוני ואינו שיווק פנסיוני.

### Added

- נוסף פרק "הבהרה משפטית" בראש SKILL.md ו-SKILL_HE.md, המבהיר שהתוצרים מופקים אוטומטית ללא מעורבות יועץ פנסיוני בעל רישיון, ושאין להסתמך עליהם לניוד כספים, לשינוי מסלול או למשיכת פיצויים.
