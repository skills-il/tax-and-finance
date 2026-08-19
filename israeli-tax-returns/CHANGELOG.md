# Changelog

## 1.9.0 - 2026-08-19

Corrected the nekudot zikui schedule against the Income Tax Ordinance, Form 101, and the ITA 2026 deductions booklet. Every figure below was verified at the primary source.

- **Child credit points were a superseded schedule.** The skill carried three age bands (born 1.5, ages 1-5 = 2.5, ages 6-17 = 1.0). The statute has six, and both parents differ from age 6: year of birth 2.5, ages 1-2 = 4.5, age 3 = 3.5, ages 4-5 = 2.5, ages 6-17 = 2.0 mother / 1.0 father, year of majority 0.5 mother only (ss.66(c)(4), 66(c)(5), 40(b)). A parent of a one-year-old was being quoted 2.5 points instead of 4.5, understating the credit by 5,808 NIS.
- **Combat reserve points were capped at 1.0 and used the wrong thresholds.** Section 39B, added by Amendment 283 and detailed in ITA circular 2025-001368 of 16.12.2025, caps at 4.0 and has TWO band tables: a hora'at sha'a for 2026-2027 starting at 30 days, and the permanent rule from 2028 starting at 20 days. Points are also counted on the PRECEDING tax year's days and require an IDF certificate. Both tables are now encoded in full.
- **Oleh credit points were the pre-amendment schedule.** Section 35(a) gives 1/3/2/1 points per year across a 54-month window keyed to the aliyah date, 8.5 points in total, not 3/2/1 over 3.5 years.
- **"Returning resident: same as oleh chadash" was wrong.** Section 35(d) defines toshav chozer for this track as someone who resumed Israeli residency between 16.5.2010 and 30.9.2012 only. A person returning today gets no s.35 points on that basis.
- **Added discharged-soldier and national-service credit points**, which were absent entirely: 2.0 points per year for the 36 months after discharge where regular service was 23+ months (22 for a woman), otherwise 1.0 (s.39A, Form 101 box 14).
- **Separated the two filing thresholds that were conflated.** The skill gave 721,560 NIS as the salary mandatory-filing threshold; that is the s.121B surtax figure, which removes the exemption via Regulation 3(a)(8). The Addition A salary ceiling for tax year 2025 is 723,000 NIS. All eight Regulation 134A ceilings, and the separate s.131(b2)(4) online-filing exemption, are now tabulated.
- **Added missing entitlements:** netul yecholet child 2.0 points and its exclusivity with s.44 (s.45(a), (c)); the s.44 institution credit at 35 percent of the excess over 12.5 percent of taxable income; mezonot and split-keep credit points (ss.40A, 40(b)(2)); the s.40B 16-17 point; and s.11 yishuv mutav treatment with the 2026 changes.
- **Added the aliyah and return incentive** (Economic Efficiency Law 2026 chapter D, in force 31.3.2026), which was not reported but is material: a five-year exemption on personal-exertion income for an oleh or toshav chozer vatik arriving between 5.11.2025 and 31.12.2026.
- New `references/credit-points.md` carries the full schedule with a statutory citation per row. `references/tax-brackets-credits.md` had been propagating the same superseded values and now points at it with an explicit old-versus-new table. New `references/domain-checklist.md`.
- Corrected the worked example in Step 3, which used the old bands.

## 1.8.1 - 2026-08-13

Moved the Troubleshooting section to references/ to bring SKILL.md under the 5,000-word validator cap, which it had been exceeding. No content was removed.

All notable changes to this skill are documented here.

## [1.8.0] - 2026-08-09

### Added

- נוסף פרק "הבהרה משפטית" בראש SKILL.md ו-SKILL_HE.md, המפרט מה הכלי עושה, מה הוא אינו, ולאיזה בעל מקצוע מוסמך יש לפנות.

### Changed

- התיאור נפתח כעת בהבהרה קצרה, כך שהיא נראית גם בכרטיס ובתוצאות החיפוש.
