# Changelog

## 1.8.0 - 2026-10-29

### Fixed

- Statutory interest under the Payment Ethics to Suppliers Law was asserted on every business invoice. Sec. 4(b) limits it, against a private business or a budgeted body, to engagements where the client had the advantage in shaping the terms. Step 1, Step 3, Step 4, the Gotchas and the demand-letter template now condition it, and the letter falls back to the neutral formula. The claim that linkage attaches automatically is removed: sec. 4 attaches none.
- "The law caps how far an agreed term can be pushed out" was wrong for a private business. There is no fixed cap; a later date must be express and pass the special-nature or not-exceptionally-unfair test (sec. 3(z)). An express longer term is now honoured rather than chased.
- references/legal-escalation.md still contradicted the skill after 1.7.1: venue fixed to the debtor's city, an absolute 30-day enforcement wait, "simple interest" (the Interest Law capitalises annually, sec. 4a(b)), an appeal described as limited to points of law (it is by leave, sec. 64, within 30 days for proceedings opened from 11.4.2025), the local-authority clock keyed to issue rather than submission, and a sunset Shabbat start. All corrected. No repealed venue limb is presented as live.
- The Gotchas still said an enforcement file cannot be opened until 30 days after judgment; the date set in the judgment governs (sec. 6(b)).
- חייב מוגבל באמצעים was described as constraining the creditor. It is a separate debtor status with its own restrictions (sec. 69d).
- SKILL_HE.md had drifted a full cycle behind SKILL.md (examples, reports, Shabbat rule, interest). It is now a faithful mirror.
- The display description called the letter a "michtav hitchayvut" (a letter of undertaking); it is a michtav drisha.

### Added

- The court-free fixed-sum route (Execution Law sec. 81a1): up to 75,000 NIS, evidence signed by the debtor (reg. 109d1), a warning in the prescribed Form 19א wording (reg. 109a) served by registered mail with delivery confirmation, filing only 30 days after service, a 30-day objection window, and no early action (sec. 81a1(e)(2)). Open to a company claimant.
- Proof and return of submission (sec. 3(i), 3(h)(1)-(3)), budgeted and statutory bodies (sec. 3(e)(1)), the VAT-status definition of a business, external funding (3(f)(2)) and the sec. 12 exclusions.
- Consumer branch: no date is due until the creditor names one a reasonable time ahead (Contracts Law sec. 41); court interest runs from filing by default.
- A phone call to accounts payable before the first written reminder; a payment and withholding check before every reminder.
- Enforcement mechanics: third-party attachment (sec. 44), fees charged to the debtor with interest (sec. 9), file consolidation (sec. 74b-74c), the evader route to restrictions (sec. 66b(a)(3)), late filing (sec. 6(b2)), the debtor-details requirement (sec. 6(d)(2)), and the lawyer-fee rule for suing on a claim that could have gone to the Enforcement Office (sec. 81a2).
- Enforcement fees: 1% for a judgment or fixed-sum file, 1.25% for a notes file, plus a protocol fee; credited against the court fee if an objection is accepted (Court Fees reg. 4).
- The insolvency freeze (sec. 29) and the temporary stay without an opening order (sec. 319ג, 319יז).
- Limitation: the Swords of Iron freeze (sec. 15a) and the restart on acknowledgment or part payment (sec. 9).
- references/domain-checklist.md.

### Changed

- The demand letter goes out at due date + 60 in every file (it was "30 to 60" in one place), with a dated deadline at least 21 days after the letter date. It is no longer described as the fixed-sum warning.
- The small-claims fee is now cited to reg. 6(a) (1%, at least 50 NIS, rounded up to a multiple of 5).

## 1.7.1 - 2026-09-02

### Fixed

- Small-claims venue cited limbs that are repealed. Reg. 2(a) marks paragraphs (2), (3) and (4) as (נמחקה); the live options are the defendant's residence or place of business, and the place of the act or omission sued on. Added that reg. 2(a) applies notwithstanding any agreement between the parties, so a contractual venue clause does not bind in Small Claims, and that reg. 2(b) narrows online-publication and online-trade claims.
- Step 5.5 said an individual debtor "changes which forum applies". It does not, and it contradicted the venue text. Replaced with what actually changes: no Companies Registrar record, protected-minimum garnishment limits, and a different insolvency track.

### Added

- The proof-of-claim deadline is now stated: six months from publication of the opening order (sec. 210(a) of the Insolvency Law), 45 days for a post-order debt or the end of that period whichever is later (210(b)), with trustee extension for good cause (210(c)).
- A disputed-debt section in Step 5.5: get the objection in writing early, and the cheque/promissory-note route is NOT a shortcut on a contested debt because an objection sends it to court anyway and the opening fee is spent.
- Personal guarantee (ערבות אישית) from a controlling shareholder, plus the authorised-signatory check on a company cheque or note.

### Changed

- The Shabbat and chag boundary rule moved to references/legal-escalation.md as one deterministic spec (candle-lighting and nightfall offsets, the recipient's city, chol hamoed, erev chag, non-Jewish recipients, and a conservative fallback when no calendar source is available), replacing three partial prose repetitions.
- Steps 6 and 7 condensed; the detail they restated already lives in references/legal-escalation.md.

## 1.7.0 - 2026-09-02

### Fixed

- Corrected the limitation citations: an ordinary debt is 7 years under sec. 5(1) of the Limitation Law, and a judgment is 25 years under sec. 21. The supporting evidence entry previously cited a dead URL with a paraphrased quote.
- Corrected the enforcement restrictions in Step 7. The Execution Law sec. 66a list is closed and does not include a driving-licence restriction or a power to stop the debtor opening bank accounts. The Hebrew no longer conflates לקוח מוגבל מיוחד with חייב מוגבל באמצעים.
- Removed the "Bank of Israel base rate + statutory margin" formula from references/legal-escalation.md, which was wrong after Amendment 9 and contradicted the skill's own rule against quoting the BoI rate.
- Re-anchored every aging bucket, reminder stage and template to the payment DUE date rather than the invoice date. Under the statutory shotef+45 default the old anchoring sent late notices to clients still within terms, and the Stage 3 email asserted "more than 60 days have passed" at a point where 30 had.
- Reconciled the two dmei pigurim start dates, and corrected "75 days" to a start-of-month maximum (about 46 days for a month-end invoice).
- Replaced a 404 Kol Zchut link for the supplier payment deadline.

### Added

- A scope gate in Step 1: the Payment Ethics to Suppliers Law governs a purchaser buying in the course of business and supplies no statutory due date for a private consumer client.
- Step 5.5, the cheap rungs before court: converting the debt into a directly enforceable instrument, giving a settlement the force of a judgment, verifying the debtor at the Companies Registrar, and עיכבון.
- Step 6.5, insolvency: a stay halts individual collection, and a proof of claim must be filed with the trustee within a limited window or the debt is not counted.
- Interim attachment (עיקול זמני) guidance for a debtor who is dissipating assets.
- The Accountant General quarterly rate source, plus an always-safe letter formulation that claims the full statutory entitlement without asserting a figure.
- VAT Law sec. 7: late-payment interest sits inside the VAT base.
- A rewritten Stage 5 demand letter carrying all six mandatory contents.

### Changed

- Venue for a small claim is now stated as a plaintiff's choice rather than fixed by the debtor's address.
- Step 4, Step 6, Step 8, Gotchas and the Examples were condensed to stay within the 5,000-word cap; the detailed interest exposition now lives in references/legal-escalation.md.

## 1.6.1 - 2026-08-11

Replaced two dead gov.il enforcement service URLs with the live Enforcement and Collection Authority portal.

All notable changes to this skill are documented here.

## [1.6.0] - 2026-08-09

### Added

- נוסף פרק "הבהרה משפטית" בראש SKILL.md ו-SKILL_HE.md, המפרט מה הכלי עושה, מה הוא אינו, ולאיזה בעל מקצוע מוסמך יש לפנות.

### Changed

- התיאור נפתח כעת בהבהרה קצרה, כך שהיא נראית גם בכרטיס ובתוצאות החיפוש.
