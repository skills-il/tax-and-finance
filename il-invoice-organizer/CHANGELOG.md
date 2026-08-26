# Changelog

## [1.5.0] - 2026-08-26

### Fixed

- **Removed a fabricated allocation-number step.** Seven places said a further reduction was "planned for 2027". The Israel Tax Authority page that enumerates the ladder contains no mention of 2027 or 2028, verified by rendering it and grepping the text. NIS 5,000 from 1 June 2026 is the terminal step. The original statutory ladder did run to 2028, but the rollout was accelerated and ended early, which is the likeliest origin of the stale row.
- Added the missing first rung of the ladder: NIS 25,000 from 5 May 2024.
- Corrected the six-month input-VAT window from תקנה 23א (an unrelated extra return for Gaza and Jericho transactions) to section 38(א) of the VAT Law. The rule was right, the citation was not.
- Corrected the invoice-issuance trigger. Section 46(א) runs fourteen days from מועד החיוב במס, the charge event under sections 22 to 29, which for a SERVICE is receipt of payment. The previous "supply or payment, whichever comes first" would have told an unpaid cash-basis freelancer they were late.
- Corrected the retention rule from a flat seven years to seven years from the end of the tax year OR six years from the filing date, whichever is later, plus the separate three-year class.
- Corrected the Osek Zair exclusions. Both cited limbs were wrong ("related party" is קרוב under section 88 or a former employer within three years; "10%+ shareholder" is a controlling shareholder under section 32(9)), and four further exclusions plus the two-year lock-out were missing.
- Added the double-entry limb to the detailed-report threshold: double-entry bookkeepers are in regardless of turnover.
- Replaced three dead gov.il links and two "(link removed)" placeholders with live, verified URLs.
- Stopped calling the 12 expense categories "official Tax Authority categories". The 1-12 numbering is this skill's own convention and no ITA source publishes it, so an accountant will not recognise "code 4".

### Fixed (scripts/categorize_invoices.py)

Every edge case the prose warns about was unimplemented. Seven realistic inputs produced seven wrong answers before this release.

- Foreign-supplier invoices had Israeli VAT extracted and reported as input VAT. Now zeroed, with routing to the רשימון יבוא or a חשבונית עצמית.
- Credit invoices ADDED to the reclaim instead of subtracting. Now carried as negatives.
- The Regulation 18 quarter limb was absent, so a mainly-private vehicle was deducted at 2/3 instead of 1/4. The Director's determination is now honoured too.
- The allocation-number threshold was not implemented at all. Now derived from the invoice ISSUE date against the full ladder.
- Pre-2025 invoices were checked against 18% and flagged as errors. The rate is now selected by invoice date.
- A legitimate 0.00 invoice was reported as "missing amount fields" (a falsy-zero bug).
- Supplying both total and VAT left the net at zero, silently breaking every category total.
- Osek Patur receipts contributed a fabricated figure to the accountant-facing input-VAT total.
- `--format text` was declared and never read, so it silently emitted JSON.
- The bare substring "שירותי" in the Subcontractors keywords swallowed "שירותי ענן", contradicting the skill's own worked example.

### Fixed (second review round)

An independent review found that several of the fixes above had reached the prose and not the code, which is the exact failure this skill's own optimization log records against v1.3.0.

- **חשבונית עסקה existed only in the documentation.** The script's taxonomy did not know it, and an unrecognised `invoice_type` fell through to the tax-invoice default, so the most permissive treatment was applied to anything the taxonomy did not recognise. Added the type, and the unknown-type path now fails CLOSED.
- The report's "net deductible VAT" counted the VAT of invoices it flagged on the same page as blocked for want of an allocation number. The two halves of the printout now agree, and the blocked amount is disclosed on its own line.
- A foreign supplier's VAT was only zeroed when the document showed no VAT line. An invoice carrying EU VAT or US sales tax, which is the normal case, still put a fabricated Israeli input-VAT figure into the total.
- When the net was supplied together with a stated VAT, the script overwrote the supplier's figure instead of flagging the discrepancy, so a wrong VAT line was silently corrected out of existence. The mismatch is now reported against net times the rate.
- The Regulation 18 vehicle default was the taxpayer-favourable 2/3 limb, so an ordinary fuel receipt with no explicit flag was over-deducted. It now applies the conservative 1/4 limb and says the main use was not stated. Both worked examples taught the same over-deduction and now ask which use predominates before computing.
- Added the six-month section 38(א) window flag and the על שם העוסק name-mismatch flag. Both are Must-cover items the checklist marked covered and neither existed in the code.
- Proformas were aggregated into the expense totals at face value. They are now excluded and listed separately.
- `validate_invoice` still read amounts by truthiness, and the net-only branch of `verify_vat` never received the date-selected rate.
- Renamed the gross VAT line, which was labelled מס תשומות (a term of art for DEDUCTIBLE input tax) while including blocked and foreign VAT.
- The תקנה 23א misattribution and the superseded "supply or payment, whichever comes first" rule both survived in `references/`, and the Hebrew half of one note stated the corrected rule in English and the wrong one in Hebrew on the same line.
- The Hebrew file still called the 12 categories "official Tax Authority categories" in four places after the English stopped, and dropped the quarter limb from its vehicle gotcha.
- **Removed the depreciation rate table.** Its only citation was a page containing no depreciation content, and it contradicted itself. Rates now route to תקנות מס הכנסה (פחת). Same for the unsourced minimum recognised share on a mixed-use mobile.
- Repointed or removed 13 evidence entries whose snippets merely restated their own claim text, including two that still asserted the errors this release fixes.

### Fixed (third review round)

The second round's fixes created a fresh instance of the same class of defect, caught by re-running the reviewer.

- The six-month and name-mismatch flags added in round two printed and moved no number, exactly as the allocation flag had before round two. Blocking is now driven by a marker table so any deduction-barring flag zeroes that invoice's deductible VAT.
- A חשבונית מס/קבלה escaped the allocation-number gate entirely, at any amount, because the gate tested only for `tax_invoice`. It is a חשבונית מס and carries the same duty.
- The allocation gate was silent when it could not compute a net. It now says so instead of passing.
- The חשבונית עסקה type was routed through the "no Israeli VAT arises" branch, which sets net equal to gross. That is right for a foreign supplier or a plain receipt and wrong for a חשבונית עסקה, where VAT does arise and is simply not yet deductible, so the income-tax expense base was overstated by the VAT.
- Vehicle running costs escaped the Regulation 18(b) ladder whenever an earlier keyword matched: "ביטוח רכב" landed in Insurance (6) before Vehicle (9) and took a full deduction instead of 2/3 or 1/4. The ladder now triggers on the expense being a vehicle running cost, not on the category code alone.
- `references/expense-categories.md` still stated a flat 2/3 with no quarter limb in two places, and SKILL.md's Gotchas still carried the superseded "supply or payment" trigger 90 lines below the corrected paragraph.
- The "official Tax Authority categories" claim survived in the reference file's title, the Hebrew resources list, a step instruction and the script's own argparse description.
- Removed an unsourced aside about the original ladder running to 2028, and the 300/305/310/320/330 document-type codes, which had no source.
- Softened the entity-type output: the business-number prefix is a heuristic, not a sourced registry rule, so the script no longer asserts an entity type it cannot establish.

### Fixed (fourth review round)

The third round's two fixes each introduced a new wrong number, caught by re-running the reviewer a third time.

- **Substring matching on the vehicle keywords.** רכב is inside רכבת (train) and הרכבת (assembly), and `car` is inside `cartridge` and `cardboard`, so train tickets, furniture assembly, toner and packaging were all pushed onto the Regulation 18(b) ladder and deducted at 1/4 instead of in full. Both the category keywords and the vehicle test now match whole tokens. The same substring defect had been in `categorize_by_keywords` since before this release and was the actual root cause.
- **The blocking-marker table zeroed a credit note's NEGATIVE deductible VAT**, deleting the reversal and increasing the reclaim. A purchase plus its full credit note reported a positive 1,800 NIS reclaim on a cancelled transaction. Blocking now never applies to a negative.
- The six-month window was coded as 183 days rather than six calendar months, leaving a short window each month in which an invoice was already out of time under section 38(א) and was not flagged. The message now states the actual closing date and notes that the test is measured against today.
- Business-travel lodging (לינה בנסיעת עבודה) was blocked as אירוח under Regulation 16. It is not אירוח, and its input VAT is deductible.
- SKILL.md and SKILL_HE.md still asserted the 51/52 and 58 prefixes as fact after the script was softened, and SKILL_HE.md claimed every company is an עוסק מורשה, which is false: a company can be a מלכ"ר, or an עוסק פטור on a low enough turnover.
- Removed the last of the 310/320/330 document codes from the domain checklist.

### Added

- חשבונית עסקה to the document taxonomy, in both languages. It is the single most common document a freelancer mistakes for a tax invoice, and it carries no deductible VAT.
- YAML frontmatter to SKILL_HE.md, which had none at all. Nothing in the pipeline had ever flagged it.
- Aligned the Hebrew step structure with the English (7 numbered steps), clearing a long-standing heading-parity warning.

## 1.4.1 - 2026-08-12

The vehicle 2/3 input-VAT deduction is a Regulation 18 DEFAULT, not a flat rate. Where the Director has set the non-business proportion that governs; otherwise a mainly-business vehicle deducts two thirds and a mainly-private one deducts only a quarter. The quarter limb was missing, so a mainly-private vehicle would have been deducted at 2/3 and over-claimed.

All notable changes to this skill are documented here.

## [1.4.0] - 2026-08-09

### Added

- נוסף פרק "הבהרה משפטית" בראש SKILL.md ו-SKILL_HE.md, המפרט מה הכלי עושה, מה הוא אינו, ולאיזה בעל מקצוע מוסמך יש לפנות.

### Changed

- התיאור נפתח כעת בהבהרה קצרה, כך שהיא נראית גם בכרטיס ובתוצאות החיפוש.
