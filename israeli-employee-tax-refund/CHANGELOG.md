# Changelog

All notable changes to this skill are documented here.

## [1.7.0] - 2026-10-07

### Fixed

- Section 39B reserve-duty credit points (Amendment 283): restricted to COMBAT reserve service as confirmed by the IDF, and to tax years 2026 onward (for service in 2025). The ITA announcement of 18.12.2025 sets the benefit in force from 1.1.2026 as a two-year temporary order (2026-2027), with the minimum dropping to 20 days from tax year 2028. The skill previously applied the points to any reservist and told a 2024 reservist to claim them on the 2025 refund, which the law does not allow. The estimator now declines to add the points for a claim year before 2026 and says why.
- The supporting document for Section 39B is the IDF confirmation of combat service and days served, not Form 3010.
- Yishuv mutav credit: the estimator computed the credit as a percentage of the TAX on capped income. Section 11 grants the locality rate on earned INCOME up to the locality ceiling (Kol Zchut worked example: 11% of 168,000 NIS is 18,480 NIS), floored so it cannot take tax below zero. This understated the credit for every periphery resident.
- Form 101: entitlements are claimed in part ח of the form, not part ז (SKILL.md, SKILL_HE.md, references).
- Severance routing: every Form 161 event was sent to Form 1301. The ITA lists Form 161 as a routine Form 135 attachment for anyone who left a job, so only taxable severance or a spreading request now routes to israeli-tax-returns.
- Refund interest: linkage plus 4% applies to EVERY refund from the end of the claim year (Section 160(a)), not only to a late one.
- Example 1: the "normal withholding leaves about 800 NIS owed" figure was not derived from the example's facts; with a Form 101 at each job in turn the year comes out at about 105 NIS back.
- מענק עבודה (negative income tax) was described as a Bituach Leumi claim; the Tax Authority pays it and takes the claim online.
- Troubleshooting for a failed online login pointed to a gov.il identity; the refund system uses the Tax Authority's own login (ID number plus a permanent user code, or a smart card). The cause is now marked as unconfirmed.
- Section 44 and the yishuv mutav claim now name the forms the ITA lists (116א, 1312א).

### Changed

- Submission channels rewritten from the current gov.il Form 135 service page: the online system opens a refund-only file at secapp.taxes.gov.il/srbksOpentik, and a paper Form 135 is submitted through the ITA public-inquiries system or a service point. A married couple files one request.
- Married couples (Expert MAJOR carried since 1.3.0): the tax is computed per spouse on salary (Section 66(a)(1) and 66(c)(1)), so the skill and the estimator now say to run one estimate per spouse and never sum both salaries.
- One refund request per tax year; a married claimant attaches the spouse's income documents and a registered-spouse declaration; reserve-duty points are shown as "up to" because credit points only reduce tax to zero; the estimator flags income above the mas yesafim threshold.
- Example 2 now routes a 2025 reservist to Form 101 part ח section 16 before 31.12.2026 for an in-year payslip correction (online tax coordination with two or more employers), with a refund request for tax year 2026 from January 2027 for the rest.

## [1.6.0] - 2026-08-26

### Fixed

- Section 9(5) disability exemption: the skill stated the PRE-15.11.2021 eligibility test (100% medical disability, or 90%+ via a multi-impairment calculation) as if it were current law, and SKILL_HE.md told the reader outright that anything less than that does not qualify. Since 15.11.2021 the general threshold is 90% disability, and where the 90% is reached by a weighted calculation across several impairments one impairment must be at least 40%. In נכות כללית the relevant figure is the MEDICAL disability percentage and not the incapacity degree (דרגת אי כושר). A user with a 90% determination was being told they had no entitlement, on an exemption worth up to 445,200 NIS of exempt income a year and claimable six years back. Both regimes are documented in references/2026-rates.md, together with the pension limb for חוק הנכים and חוק נפגעי פעולות איבה recipients, the grandfathering rules for determinations predating 15.11.2021, the 185-day duration test and the list of qualifying laws.
- Refund payment deadline: the second limb ran "two years from the end of the tax year" where the rule is two years from the end of the year in which the TAX WAS PAID. Also noted that a filer obliged to submit a return is on a different clock (90 days from receipt of the return, or 31 July of the following year) and belongs in israeli-tax-returns.

### Added

- Fallback when Form 106 cannot be obtained (a deferred finding carried since 1.3.0): all Form 106s from every employer for the last 6 years can be downloaded from the ITA personal area, and the employer's duty to issue one survives bankruptcy. Documented with the caveat that the ITA-side summary does not reliably carry the keren hishtalmut fields 218 and 219.
- Form 119, the form that actually claims the section 40ג academic-degree credit. The skill listed the degree trigger and named seven other forms but never this one, so the entitlement could be identified and then not claimed.

### Changed

- evidence.json repaired and re-verified. Ten entries were failing source verification: eight carried paraphrased summaries rather than verbatim page text and had only ever passed because kolzchut bot-blocks curl, which parked them in the "unreachable" bucket. Two were not claims about the world at all, having been written purely to suppress extractor false positives, and one of those was masking two genuinely unevidenced section 9(5) eligibility thresholds. Source URLs were corrected on entries that cited a hub page containing none of the claimed content. The file now passes --check-sources in full for the first time.
- Removed the bare "Section 14" citation for the returning-resident foreign-income exemption. The 10-year exemption itself is sourced and retained; the section number could not be confirmed against an accessible primary source, so it is not asserted.

## [1.5.0] - 2026-08-19

### Added

- Trigger 18: the aliya income-tax exemption under חוק עידוד עלייה לישראל וחזרה אליה (הוראת שעה), התשפ"ו-2026, in force 31.3.2026. Full exemption on Israeli personal-exertion income for an oleh chadash or תושב חוזר ותיק arriving 5.11.2025 to 31.12.2026, tax years 2026-2030, ceilings 600,000 / 1,000,000 / 1,000,000 / 350,000 / 150,000 NIS, with the lower 140,000 NIS relative-income limb, the 2026 pro-rating rule and the 75-day residency anti-abuse rule. It is given in addition to the section 35 credit points, and a salaried claimant realises it through this skill's own refund route.
- Trigger 19: the section 10 shift-work credit, 15% capped at 12,540 NIS against a 143,040 NIS income ceiling for 2026, regulations extended to 31.12.2026 and confined to productive industrial plants.
- Credit-point entitlement rows that were missing or uncomputable: the single parent's full child schedule (the row previously read "Additional points per scheme" with no number), the extra point for a ילד להורה אחד, the separated-parents rows, the section 40א point for maintenance to a former spouse while remarried, the section 40ב point at ages 16-17, the half point in the year a child turns 18, and the section 40ד vocational-certificate point with its section 40ה election.
- All 15 yishuv mutav rate and ceiling combinations the ITA published for 2026, up from 6, including the entire 18% tier and the previously absent 14% / 219,960 and 14% / 259,920 rows. Added the three 2026 temporary-order regimes (חבל תקומה with אשקלון, mixed urban with נוף הגליל, eastern confrontation line) and the new localities קדם ערבה, יונדב, בתרון and אדוריים.
- Per-year Section 46 minimum donation and ceiling for 2022 to 2026.

### Fixed

- `scripts/estimate_refund.py` applied the 2026 Section 46 minimum of 207 NIS and the 2026 ceiling to every claim year, so a 195 NIS donation in a 2022 claim was silently disqualified. Both are now per-year tables matching the script's existing per-year bracket structure. Years whose ITA booklet is no longer served grant the credit with a warning rather than disqualifying.
- Trigger 9's statutory anchor was sections 64, 65 and 66, which govern income attribution rather than credit points. Corrected to sections 40(ב)(1), 40(ב)(1ב), 40(ב)(2) and 40א.
- The discharged-soldier credit was cited to section 39; it is section 39א.

### Changed

- Reference Links now lead with the ITA 2026 deductions booklet and the consolidated Income Tax Ordinance, the two primary sources behind every amount in this skill.
- Detailed lookup tables moved to `references/2026-rates.md` to keep SKILL.md inside the word cap.

## [1.4.0] - 2026-08-09

### Added

- נוסף פרק "הבהרה משפטית" בראש SKILL.md ו-SKILL_HE.md, המפרט מה הכלי עושה, מה הוא אינו, ולאיזה בעל מקצוע מוסמך יש לפנות.

### Changed

- התיאור נפתח כעת בהבהרה קצרה, כך שהיא נראית גם בכרטיס ובתוצאות החיפוש.
