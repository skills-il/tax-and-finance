# Changelog

All notable changes to this skill are documented here.

## 1.1.0 - 2026-10-01

First full audit since launch. Two law changes the skill did not reflect, plus coverage gaps a
practitioner review found.

- **Olim ten-year exemption is gone for 2026 arrivals.** Amendment 272 to the Ordinance deleted
  section 135(1)(b) for anyone who became a first-time or veteran returning resident from
  1 January 2026. The skill stated the exemption as current law with no date. It now asks when the
  person became resident, keeps the exemption only for earlier residents, and routes the new
  section 135א1 (foreign company controlled from Israel) out.
- **Online filing becomes mandatory for individuals on 1 January 2027.** A Finance Minister's order
  of 3 September 2026 brings section 135(1)(a1) into force, and section 131ג(ו) treats a paper filing
  that should have been online as not filed. The skill said only that online filing is optional.
  It now dates that, flags 2026 demands that fall due in 2027, and describes the 2026 online-reporting
  rules (electronic certificate, taxpayer-signed scan, receipt, infected files not received).
- Foreign currency: general rule 12 governs items paid or received in foreign currency; a foreign
  bank balance, which section 3 asks for as at the declaration date, is not settled by the form and
  is now surfaced rather than asserted either way.
- Gifts: only a non-monetary gifted or inherited asset is 1 shekel; gifted money sits at its balance.
- New: first declaration as the baseline, a stop-and-consult trigger before filing when an asset or
  its income was never reported, a walk-every-section prompt, the three bank-account cases
  (co-owned, controlled, signatory only), and a new `references/hard-cases.md` covering employee
  equity states, crypto cost after swaps, fund withdrawals, the mortgage figure, guarantees and
  household contents.
- Fixed a misattribution: the per-portfolio separate-line rule is part C section 5's wording.
- Statutory evidence re-anchored from a January 2023 Ordinance PDF to a current consolidation.

## 1.0.1 - 2026-09-09

Acted on the MAJOR findings from the launch review panel. No factual corrections; these close gaps
where a term was used without being defined, or where the skill refused without giving a route.

- Section 6 said "the sum of all deposits" without saying WHOSE. A salaried filer's statement carries
  employee, employer and severance streams and the form's instructions distinguish none of them, so
  the readings can differ by about a factor of two. The skill now surfaces the ambiguity and routes
  the treatment to the filer's representative rather than silently picking a reading.
- Added the extension mechanism. Section 188(z) contemplates a later filing date set at the filer's
  own request, which is the first practical move when the pack cannot be assembled in time. The skill
  previously mentioned a later date only as the trigger for the higher monthly fine.
- Gave a route for reconstructing cost on an old asset (the purchase contract held by the lawyer, the
  land-registry extract, the taxpayer's own file at the assessing office) instead of a bare refusal.
  The refusal to estimate is unchanged and deliberate.
- Named the Tax Authority information centre where Troubleshooting previously routed the user to it
  without saying how to reach it.

## 1.0.0 - 2026-09-09

Initial release of Israeli Capital Declaration Preparer.

Every factual claim in this skill is tied to a verbatim snippet from a primary source in
`evidence.json`, and each snippet was verified as present at its cited URL before release.
Figures that research surfaced but could not be quoted from primary text are deliberately NOT
stated; they are recorded as unverified in `references/domain-checklist.md`.
