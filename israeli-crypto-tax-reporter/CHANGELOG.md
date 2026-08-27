# Changelog

## 1.6.0 - 2026-08-27

Correctness cycle. Several entries below are retractions of statements earlier versions published as settled.

### Corrected
- **Section 100A exit tax**: deferral is a DEEMING rule, not an election. s.100A(b) deems a non-payer to have requested it, the chargeable portion is the real gain measured at REALIZATION and apportioned by elapsed time (s.100A(d)), and **no interest or linkage differentials accrue during the deferral**.
- **The 30% rate**: s.91(b)(2) charges it on a "נייר ערך בחבר-בני-אדם", a security in a body corporate. A fungible token is not one. The skill no longer applies 30% to an ordinary crypto disposal, and the calculator no longer carries it as a selectable rate.
- **VAT**: Circular 05/2018 s.3.2.3.2.3 registers a business-level crypto trader as a **מוסד כספי** under Section 4 of the VAT Law, NOT as an osek charging 18%. Only the miner is an osek (s.3.2.3.2.4). Earlier versions collapsed three regimes into one wrong one.
- **Mining** is business income categorically per s.3.1.4, with no scale test. The worked scenario's "capital treatment" branch was removed.
- **Reporting forms**: 1322 is scoped by the ITA's own title to securities **הנסחרים בבורסה**, 1325 aggregates securities sales **by tax rate**, and neither carries a נספח label (נספח א belongs to 1320). Crypto disposals go on **1399י**, the notice of an ASSET sale. The "Nispach Gimel" routing is withdrawn.
- **Inflationary amount**: re-cited from 91(b)(3) (which is the non-index-linked bond rate) to Sections 88 and 91(c). 91(c) taxes the chargeable inflationary amount at **10%**, not 0%; it comes out nil for crypto only via s.88's 31.12.1993 cut-off.
- **Section 97(a)(5)** is a gift EXEMPTION, not a basis-carryover rule. The carryover runs through s.88.
- **CARF**: Israel is in the OECD Global Forum's "first exchanges by **2028**" group, not 2027. The earlier "2027-2028" hedge resolved against the primary source.
- **Voluntary Disclosure**: the Green Track digital-asset limb is NIS 500,000 for the ENTIRE disclosure period, not per year. The section is now date-aware, with a post-closure branch, because the window ends 31 August 2026. Its citation moved from a two-paragraph clarification page that supported none of the figures to the ITA announcement that does.
- **ITA Instruction 06/2024** was published 03.04.2024 (updated 22.10.2025), not 31.12.2023.

### Removed
- Three fabricated attributions to Circular 05/2018: the enumerated badge-of-trade factor list (s.3.1.4 delegates to the case law), the Bank of Israel representative-rate requirement (the word יציג does not appear in the circular), and the 7-year retention period (s.3.1.3 fixes none).
- The `--manual-rate` flag and the automatic Bank of Israel rate lookup, both of which the troubleshooting section described and neither of which ever existed.
- An unsourced AML shekel threshold.

### Added
- Section 121B structure: the 3% base limb (a), the 2% capital-source limb (a1), the exclusion of the inflationary amount from the base (e), and that s.121B(b) keeps the surtax **out** of the 30-day advance.
- Section 92 loss mechanics: the 3.5:1 offset against the chargeable inflationary amount, and the s.92(b) condition that a return must have been filed for the loss year.
- Sections 91(d)(2a) and 91(d)(2e): the officer may increase the advance, or extend and reduce it.
- The circular's barter rule (same shekel figure both sides) and its stated-price (מחיר נקוב) override.
- How the gain actually reaches the 1301, since the ITA publishes no crypto appendix.

### Calculator
- A disposal with no matching purchase lot is now **UNPRICED**: no invented zero basis, no invented acquisition date, excluded from every total, surfaced in the JSON, exit code 3. Previously it produced a fabricated zero-basis gain that was invisible on the JSON path.
- Totals are **suppressed entirely** when any disposal is unpriced or any row unrecognised, rather than printing a plausible partial that would get filed.
- Unrecognised transaction types (including Hebrew labels from an Israeli exchange export) are reported and set the report incomplete, instead of being silently dropped into a clean zero-tax report.
- Refuses to compute on negative or zero quantities, on dates before the Bitcoin genesis block, and on future dates.
- Enforces the circular's same-value rule across the two legs of a swap.
- The 2% capital-source surtax limb is no longer applied to pre-2025 tax years, which is exactly the Voluntary Disclosure computation.
- `--form-1325` renamed to `--schedule` (the alias is kept) because the output is not an ITA form 1325; `--schedule` and `--advance-payments` now compose instead of one silently shadowing the other.
- `price_nis` is documented in `--help`, in the skill and at the top of the scenarios file as the TOTAL row consideration, never the per-unit price.

## 1.5.1 - 2026-08-11

Corrected the attribution of the FIFO cost-basis rule and the capital-gains rates. ITA Circular 05/2018, read in full, contains no cost-basis method, no 25% or 30% rate and no retention period; the rates come from Section 91(b) of the Income Tax Ordinance. FIFO is now described as the customary default rather than an ITA mandate, since no source prescribes it.

All notable changes to this skill are documented here.

## [1.5.0] - 2026-08-09

### Added

- נוסף פרק "הבהרה משפטית" בראש SKILL.md ו-SKILL_HE.md, המפרט מה הכלי עושה, מה הוא אינו, ולאיזה בעל מקצוע מוסמך יש לפנות.

### Changed

- התיאור נפתח כעת בהבהרה קצרה, כך שהיא נראית גם בכרטיס ובתוצאות החיפוש.
