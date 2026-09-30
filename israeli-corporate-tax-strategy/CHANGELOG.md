# Changelog

## 1.4.0 - 2026-10-01

### Fixed

- Surtax: the extra 2% on capital income (s.121B(a1), Amendment 276) is measured on capital income ALONE against 721,560, not on the part of total income above it. Salary no longer "uses up" that threshold. Fixed in the body, the reference file, and `calc_surtax()` in the calculator, which had been overcharging the 2% whenever salary pushed total income past the threshold (ITA execution instruction 5/2025, example 3.2).
- Controlling-shareholder EMPLOYEE Bituach Leumi is 1.02% / 6.79% (4.25% / 11.96% with health, BTL column 2), not the regular-employee 1.04% / 7.0%. Fixed in the body, reference file, calculator, and the worked examples, which were recomputed.
- Family Company (s.64A): the election is only available within three months of incorporation. The November 30 date the skill gave is the withdrawal deadline, and a company that withdraws cannot re-elect.

### Changed

- Trapped profits: cites ss.81A-81F, adds the two missing exits (over 50% of excess profits, current losses over 10% of accumulated profits), states that an s.126(b)-exempt intercompany dividend counts only with a top-rate withholding election, marks the 5% rate as expired 2025-only, and adds the Form 1214 / appendix 1281 reporting from execution instruction 9/2026.
- Section 62A: rewritten around its three routes after Amendment 277, the controlling-holder (בעל שליטה) test, the 25% client exit scoped to s.62A(a)(1), the 70% one-client rule with the four-employee exclusion, and the s.62A(a1) 30M and 750k exclusions.

### Added

- `analyze_management_fees()` in the calculator (self-employed NI, the s.47A 52% deduction), closing a gap carried since v1.1.1.
- The optimal-mix search now tests the all-dividend and all-salary endpoints.
- `--company-recipient` (implied by `--dividend-rate 0.04`): a body-corporate shareholder pays no s.121B surtax and has no salary or fee route.
- Step 3 notes that already-taxed retained earnings cost only the dividend rate plus surtax, and that pacing a large distribution across years avoids the capital-income surtax.
- The legal notice now states that paying the tax is the user's responsibility and that representation before the Tax Authority is reserved by law.

### Removed

- The duplicate Gotcha on grandfathered benefit-track companies (Step 1b rule 3 carries it), and the "Tax Authority questioned my loan" troubleshooting entry, moved to `references/section-3tet-rules.md`.

## 1.2.1 - 2026-08-11

Removed the unsourced "(typically 10-15%)" treaty-rate range. Replaced nevo.co.il/law/70264, a JS shell that resolves to no document, with the real Income Tax Ordinance text.

All notable changes to this skill are documented here.

## [1.2.0] - 2026-08-09

### Added

- נוסף פרק "הבהרה משפטית" בראש SKILL.md ו-SKILL_HE.md, המפרט מה הכלי עושה, מה הוא אינו, ולאיזה בעל מקצוע מוסמך יש לפנות.

### Changed

- התיאור נפתח כעת בהבהרה קצרה, כך שהיא נראית גם בכרטיס ובתוצאות החיפוש.
