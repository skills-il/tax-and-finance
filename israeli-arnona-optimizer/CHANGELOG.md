# Changelog

## 1.5.0 - 2026-08-19

Rebuilt the whole discount surface directly from the consolidated text of the Arrangements in the State Economy Regulations (Arnona Discount) 5753-1993 and the Senior Citizens Law 5750-1989, rather than from secondary restatements. The skill previously covered eleven of the regulation's rows.

Added, all previously absent: blind person's certificate up to 90% (Reg. 2(a)(5)); the six-item persecution and Prisoner-of-Zion pension list including German BEG, Dutch WUV, Austrian OFG and Belgian 1954 pensions (2(a)(4)); oleh dependent on the help of others up to 80% (2(a)(6a)); SLA member up to 90% (2(a)(6b)); nursing benefit up to 70% (2(a)(7)(c)); Righteous Among the Nations up to 66% (2(a)(9)); parent of a child entitled to the disabled-child benefit, foster children included, up to 33% (2(a)(11)); released captive up to 20% (2(a)(12)); active reserve COMMANDER up to 25% on 100 sqm (Reg. 3g); hostage and missing-person 100% (Reg. 14e1); Gaza-envelope 45% residential and 39% other with the 7 km rule (Reg. 3c); evacuated-locality 100% from 07.10.2023 (Reg. 3c1); the full Chapter Hey2 entitlement set (Reg. 14e) with its 70/90 sqm cap (Reg. 14f); shmita agricultural land (Reg. 3d); new industry (Reg. 14); senior business owner (Reg. 14c); and the Senior Citizens Law s.9 senior entitlement with its average-wage and 150%-of-average-wage tests and automatic-renewal rules.

Corrected: single parent is a national ceiling of up to 20% under Reg. 2(a)(10), not the "municipality-dependent, could not verify a uniform national rate" the skill previously asserted. The empty-property rule is the Reg. 13(a) cumulative ladder of 100 / 66.66 / 50 percent across 6 / 12 / 36 months from 01.03.2005, plus the separate Reg. 12 new-building route of up to 100% for twelve months, not "typically up to 6 months". The Reg. 2(a)(8) income test now carries the operative First Schedule table for fiscal year 2026 in full, replacing an unsourced two-column table.

Removed from scripts/arnona-calculator.py: hardcoded student 50% and large-family 30% rates. The regulation contains no paragraph for either, so no national figure exists to state and the skill now says so explicitly. The low-income key was a flat 80% with no band structure and is now the top band with a percentage override; the soldier key capped at 100 sqm against a statutory 70 sqm. Every remaining constant carries the paragraph it comes from, and each is tagged as a council-set ceiling or a statutory entitlement.

## 1.4.1 - 2026-08-13

Rebuilt the discount table against live Kol-Zchut pages after the single page all three evidence entries cited went dead. Corrections: conscript exemption is 100% on 70 sqm (90 sqm for 5+ residents) for every conscript, not 'up to 100%' for lone soldiers; bereaved-family is a mandatory 66.66%, not 'up to 66%'; income-support 70% applies only to recipients who started before 2003; reserve-duty relief is up to 5% and discretionary, not municipality-defined without a rate; the income-test discount runs in bands of up to 30/50/70/90%, not '20-80%'. Removed the unverifiable single-parent 20% and student 50% rates, the Regulation 7 and Section 330 citations, and the fixed balcony/storage rate fractions.

All notable changes to this skill are documented here.

## [1.4.0] - 2026-08-09

### Added

- נוסף פרק "הבהרה משפטית" בראש SKILL.md ו-SKILL_HE.md, המפרט מה הכלי עושה, מה הוא אינו, ולאיזה בעל מקצוע מוסמך יש לפנות.

### Changed

- התיאור נפתח כעת בהבהרה קצרה, כך שהיא נראית גם בכרטיס ובתוצאות החיפוש.
