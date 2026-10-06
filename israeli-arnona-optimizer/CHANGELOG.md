# Changelog

## 1.7.0 - 2026-10-07

Replaced every rate in the calculator. The per-zone residential and commercial rates for twelve municipalities had never been read from any tzav arnona, and most of the zone systems were wrong too (Ashdod has one residential zone, not three; Herzliya has seven, not three). The script now carries the full fiscal-2026 residential table of eleven cities, read from each city's own published tzav: Tel Aviv-Yafo, Jerusalem, Haifa, Beer Sheva, Netanya, Rishon LeZion, Petah Tikva, Ashdod, Ramat Gan, Herzliya and Raanana. Every city keys its rate on zone AND a building type or size class, so the script takes `--type` from the bill and, without it, lists every row that fits instead of printing one figure. Haifa's size bands and Ashdod's marginal tiers are modelled. Non-residential use, Modiin and every other authority now take `--rate-per-sqm` from the user's tzav or bill. Tel Aviv's old figures were above the real range for an ordinary flat in every zone.

Added the fiscal-2027 income table (Kovetz HaTakanot 12490, as corrected by 12499), in force 1 January 2027 and testing calendar-2026 income, beside the fiscal-2026 table, which was re-verified cell by cell against Kovetz HaTakanot 12366. The calculator picks the band itself from `--household-income`, `--household-size` and `--fiscal-year`. Added the 3.05% national update for 2027.

Corrected the objection section: the grounds are the four in s.3(a) of the Local Authorities (Arnona Objection) Law 5736-1976, not "Section 3(a) of the Arnona Regulations"; the objection goes to the arnona manager, not a "committee"; silence for 60 days means the objection is deemed accepted; filing does not suspend payment, and an unpaid balance voids the year's discount. A refused discount is not an objection matter.

Added: who the holder is and the written notice that ends liability; household composition for the income test; the per-child computation of the disabled-child discount up to 90% (Arrangements Law s.12(g)); the rows that sit outside Regulation 2 (Prisoner of Zion on an income-based benefit, old-age pension for the disabled, pre-2003 income support and maintenance recipients); the arrears and refund rules of the 1980 Interest Law (CPI linkage on instalments, a one-year arnona instalment limit, linkage plus 0.5% a month on a late refund), which replace a wrong attribution to the Municipalities Ordinance; seller and landlord liability on a sale or lease (s.326); the Senior Citizens Law s.13A 100% row for low-pension seniors; the 7-year limitation; the s.330 destroyed-building exemption; the standing-order ceiling of 2%; and each city's own area-measurement rule in place of an invented "gross area, reduced-rate balconies" default.

Removed: the unsourced reform claims (740,000 to 840,000 households; benefit exclusions presented as new in 2026), a "retroactive for 6 months" rule, the student "under 30" criterion, a soldier "lives alone" declaration, a "30-60 day" processing time and a large-family "four children" criterion, municipal email addresses, an "income-support recipient" row with no pre-2003 condition, municipality phone numbers that had no source, and a catch-all evidence entry that listed numbers without a source behind them.

## 1.6.0 - 2026-09-20

Corrected the Regulation 2(a)(8) First Schedule income table, which was wrong in every cell. All 36 cells (nine household sizes across the 90 / 70 / 50 / 30 percent bands) and all four of the ten-or-more per-person increments were roughly 3 percent too high. Thresholds that are too high tell an eligible low-income household that it falls outside the band it actually qualifies for, so the error ran in the direction that costs users money. The corrected table for fiscal year 2026, tested on income earned in 2025, starts at up to 3,513 NIS for a single person in the 90 percent band and runs to 15,743 / 19,243 / 22,742 / 26,240 for nine persons, with 1,125 / 1,374 / 1,624 / 1,874 added per person from the tenth. The table appears in SKILL.md, SKILL_HE.md and references/arnona-discounts-guide.md, and the three copies are now generated from one list and diffed to prove they match.

Sourced the rate tables. Every municipality block in scripts/arnona-calculator.py now carries the fiscal year of the tzav arnona it represents and a source, and the report prints both.

Surfaced the national annual update. The 1.626 percent coefficient for fiscal year 2026 previously existed only in a reference file; it now appears in Step 2 of both skill files and in the calculator's report.

Made the calculator honest about its own model. It keys the residential rate on zone alone, while a real tzav arnona keys it on zone and building classification code, a roughly two-fold spread inside a single zone. The report now states that limitation at the point of output rather than presenting the figure as the municipality's rate. Tel Aviv's 2026 tzav has five residential zones against the four modelled. Both are listed under a new "Known limitations and deferred work" section in the skill.

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
