# Changelog

All notable changes to this skill are documented here.

## [1.2.0] - 2026-08-26

First review since publication.

### Fixed

- Refreshed the Israel country-risk inputs from the January 2026 vintage to the July 2026 one: adjusted default spread 1.36% to 1.27%, country risk premium 2.07% to 1.98%, total equity risk premium 6.30% to 6.18%. The Moody's rating is unchanged at Baa1, so the move is CDS repricing, not a downgrade. Figures read directly from the published dataset file.
- Vintage checks now point at the data-current index. The country-premium landing page kept advertising the January file after the July one was published, so a check made there confirms a stale vintage and looks like verification. Corrected in both languages, in the prose AND in both Reference Links tables.
- Corrected the Pillar Two passage. Israel enacted a domestic minimum top-up tax only, with no income inclusion rule and no undertaxed profits rule, so it tops up Israeli low-taxed profit rather than a group's foreign profit. The 15% is a floor, not a cap, and the earlier wording called it a ceiling.
- Corrected the closely held company rules to the statute: sections 81א-81ו for the 2% charge (base is accumulated profits less the highest of three shields, and Encouragement-Law-sourced profits are outside it), section 62א(א1) for excess profitability (25% is BOTH the entry trigger and the deducted normal return, subject to an ILS 30 million per-controlling-shareholder ceiling), and section 62א(א) for attribution. The 25% escape belongs to the officer and management-services limb, not to the 70% limb, and the 70% limb has its own four-employee exclusion in section 62א(א)(5) and a 22-of-36-months duration test.
- Corrected the newly added real estate association passage. A sale of shares in an איגוד מקרקעין changes the charging statute, adds purchase tax on the buyer, and removes ordinary capital-gains apportionment, but section 48א(ב) charges the individual at the SAME 25% and 30% ladder. An earlier draft of this update wrongly said those rates do not govern.
- Three bugs in scripts/valuation_model.py. Staleness suppression keyed off a parameter that does not drive the number, so passing a fresh country premium alone silenced the warning while the stale total premium still set the cost of equity. The vintage line kept asserting the built-in vintage after an override. Guard-rail ValueErrors printed a traceback instead of their own message.

### Added

- Preferred Technology Enterprise eligibility now carries the competitiveness test and the secondary tests (R&D headcount, venture funding, revenue growth, headcount growth, or Innovation Authority certification). A company clearing revenue and R&D alone does not qualify, and the earlier text implied it did.
- The pre-2017 Approved and Beneficiary Enterprise regimes, which still govern older companies at different rates and a 15% dividend withholding.
- A primary-versus-secondary distinction with pre-money and post-money arithmetic. Selling a stake to an investor usually means issuing new shares, in which case the money goes to the company and there is no capital gains event for the owner at all.
- Section 3(ט1) shareholder debit balances in the equity bridge, including the ILS 100,000 de minimis.
- The additional 2% surtax on capital-source income, taking a substantial shareholder's top slice to 35%.
- A Section 104 section in references/transaction-and-sale-he.md, which the Hebrew reference file was missing entirely while its English twin carried it.

### Changed

- The size premium is now presented as contested rather than as an omission that would be an error.
- Moved the discount-rate components, the levels-of-value ladder, the Section 104 detail and the share-sale mechanics into references/ to stay under the validator's word cap.

## 1.1.1 - 2026-08-13

Moved the Troubleshooting section to references/ to bring SKILL.md under the 5,000-word validator cap, which it had been exceeding. No content was removed.

## [1.1.0] - 2026-08-09

### Added

- נוסף פרק "הבהרה משפטית" בראש SKILL.md ו-SKILL_HE.md, המפרט מה הכלי עושה, מה הוא אינו, ולאיזה בעל מקצוע מוסמך יש לפנות.

### Changed

- התיאור נפתח כעת בהבהרה קצרה, כך שהיא נראית גם בכרטיס ובתוצאות החיפוש.
