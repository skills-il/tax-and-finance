# Changelog

## 1.6.0 (2026-10-01)

- Corrected who must withhold. v1.5.0 said there is no turnover threshold; the regulations have none, but the 1977 order they rely on lists the payers (double-entry duty or turnover above its Schedule A, plus public bodies) and its s.2א excludes small single-entry payers on both limbs.
- Non-resident withholding under s.170(a) is now stated from the statute: 25% for an individual, the 23% s.126 corporate rate for a company. Added s.171 (pay within 7 days), the bank as a payer, gross-up when the payer bears the tax, and s.18(ה) for year-end accruals. The calculator splits `non_resident_individual` / `non_resident_company`.
- Treaty relief: Form 2513/2 covers only its closed list of capital payment types; services, licences and royalties go through the assessing officer under instruction 34/93. Named the 34/93 s.3.9 services-abroad relief ($250,000 per payer since 16.12.2025) in its special-company context. Removed the treaty rate table, unverified for two cycles.
- Certificates: the 2026 certificates run to 31.3.2027 (instruction 02/2026), are electronic only, must be checked shortly before payment, and cannot be back-dated. Removed the "expires 31 December" rule, the unsourced 0-5% and 2% tiers, and a muddled purchase-tax certificate row.
- Rewrote Circular 3/2026 into its three limbs. A withholding failure alone does not deny input VAT; s.32א needs the tax transferred; the cash-law limbs bite only after a sanction; s.32(18) runs from 1.8.2025.
- Added Form 0857 (reg. 6) and Form 0867, the reg. 5(a) 31 March date for 0856, interest by payee type (15% non-linked, maximum rate to a company and to related parties), company-to-company dividends, and the building/haulage (1973) and agriculture (1979) rates.
- Calculator: de-minimis applied, no VAT line on interest/dividends/non-residents, `--payer-bears-tax`, input validation.

## 1.5.0 (2026-08-19)

- Fixed the calculator default: `--type services` was 30%, the sanction rate, while the prose documented 20% for a payee with acceptable books. The common case now defaults to 20% (reg. 2(a)) and the sanction rate moved to the explicit `--type services_no_books`. SKILL.md Example 1 was hard-coded to the 30% answer and now shows both.
- Removed the invented `royalties: 0.23` constant. It was the corporate tax rate wearing a withholding label; the 1977 regulations create no royalties category. Royalties, agricultural work/produce, diamonds, insurance commission and prizes now return a sourced routing message instead of a number.
- Corrected the Form 102 deadline to the 16th in every remaining place (SKILL_HE.md, references/withholding-rates.md, the script footer). Verified verbatim at reg. 4 of the 1977 regulations, which was amended from the 15th to the 16th by תק' תשע"ח-2017.
- Replaced the invented mandatory-withholder turnover threshold. There is none: s.164 scopes withholders and payments by ministerial order, and the 1977 regulations exit is a written assessing-officer approval. Added Schedule A's exempt recipients.
- Added the statutory category list from Ordinance s.166(c), including agricultural work/produce and diamond processing/trading, with no invented rates, plus the ITA per-payee rate lookup as the authoritative source.
- Documented the two-tier (compliant vs non-compliant) rate structure as a general rule of the withholding regulations.
- Re-sourced the de-minimis: reg. 2(a) keys it to the value of the asset or service, not a cumulative annual total.
- Removed two dead gov.il links (form-856 and taxation-agreements, both 404) and replaced them with the live ITA publications index.

## 1.4.1 - 2026-08-11

Sourced the 18% VAT rate to ITA Interpretation Directive 01/2025. Reworded a script docstring whose "(0-100%)" parameter range read as an unsourced factual claim.

All notable changes to this skill are documented here.

## [1.4.0] - 2026-08-09

### Added

- נוסף פרק "הבהרה משפטית" בראש SKILL.md ו-SKILL_HE.md, המפרט מה הכלי עושה, מה הוא אינו, ולאיזה בעל מקצוע מוסמך יש לפנות.

### Changed

- התיאור נפתח כעת בהבהרה קצרה, כך שהיא נראית גם בכרטיס ובתוצאות החיפוש.
