# Changelog

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
