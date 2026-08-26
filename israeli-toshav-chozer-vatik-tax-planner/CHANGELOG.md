# Changelog

## 1.3.0 - 2026-08-27

### Fixed

- Corrected the year-of-acclimation guidance, which said the election defers the start of the 10-year clock. Section 14(b)(2) says the opposite: the acclimation year is counted inside the Section 14(a) exemption period and the Section 97(b)(1) period, so the election buys a year of non-residency, not a year of exemption. It also does not move the Hok Iddud window, because Section 2(e) of that law disapplies Section 14(b)(1) for its own start date, so the previously stated trade-off of sacrificing the 2026 cap was built on a false premise.
- Removed a Hok Iddud offer made to a regular toshav chozer in Example 2. The statute grants those caps only to an oleh or a veteran returning resident.
- Qualified the Misrad HaKlitah certificate note. It still does not establish Section 14 status, but Hok Iddud makes the certificate a precondition to the Israeli-source caps, so a returnee told to skip it can lose that benefit.
- Corrected the Section 35 credit-point taper, which was described as front-loaded when year 1 accrues at the lowest rate; the statutory citation 135(b) to 135(1)(b); and the CFC discussion, which quoted an unsourced 25% test in place of the Section 75B control tests.
- Removed figures no source supported: a "3 years if you left before 1.1.2009" track rule, a 14-day bank deadline for Form 2409, and the framing of 3.1M NIS as tax saved when it is the total of exempt-income caps.

### Added

- Section 97(b)(3): there is no capital-gains cliff at year 10. An asset sold after the window keeps the exemption on the time-apportioned slice of the gain accrued up to the end of the window, so a rushed sale in year 9 or 10 is usually the wrong advice.
- The relief that stops a foreign company being treated as Israeli-resident merely because a veteran returning resident manages it from Israel during the same ten-year window.
- That the Section 14 exemption is waivable, which is the only lever that generates a US foreign tax credit for a US-person returnee.
- An exit-tax pointer on the clawback scenario, noting that deferral under Section 100A(b) is deemed rather than elected and that interest runs only from realization.
- A note that Section 14 is an income-tax exemption and does not cover National Insurance or health-levy contributions.
- The gift and Israeli-linked-asset carve-outs on the capital-gains rows.

### Changed

- `scripts/cashflow-projection.py` now refuses to run on an unrecognised track, an invalid residency date, out-of-range years, or a regular-track stream that does not state whether the asset was acquired abroad. An unrecognised track previously fell through to classifying every stream as taxable, producing a confident wrong projection. Israeli personal-exertion income is now reported as IL-LABOUR with the Hok Iddud caps explained, instead of a flat TAXABLE that contradicted Step 5.

## 1.2.2 - 2026-08-19

### Fixed

- Translated section headings that had been left in English in SKILL_HE.md, where they rendered as-is on the Hebrew page. Hebrew is the site's default locale, and the skill validator never checked the Hebrew file, so these went unnoticed.

## 1.2.1 - 2026-08-13

Corrected the capital-gains section number: the 10-year foreign capital-gains exemption for a toshav chozer vatik is Section 97(b)(1) of the Income Tax Ordinance, not 97(b3) (97(b3) is the non-resident exemption on Israeli securities). Replaced the nevo.co.il/law/84255 short-form links, which resolve to a login wall, with the law_html document of the Ordinance.

All notable changes to this skill are documented here.

## [1.2.0] - 2026-08-09

### Added

- נוסף פרק "הבהרה משפטית" בראש SKILL.md ו-SKILL_HE.md, המפרט מה הכלי עושה, מה הוא אינו, ולאיזה בעל מקצוע מוסמך יש לפנות.

### Changed

- התיאור נפתח כעת בהבהרה קצרה, כך שהיא נראית גם בכרטיס ובתוצאות החיפוש.
