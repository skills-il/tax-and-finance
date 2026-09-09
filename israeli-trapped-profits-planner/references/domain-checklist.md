# Domain Coverage Checklist - israeli-trapped-profits-planner

Generated 2026-09-09. This is the COVERAGE CONTRACT the skill is judged against, not the full
research record. Figures live in `evidence.json`, where each is tied to a verbatim snippet from a
primary source. Nothing numeric is asserted here that is not evidenced there.

Primary sources, all read directly:
- Income Tax Circular 7/2025 as amended 08.02.2026 (gov.il)
- Income Tax Circular 2/2026 (gov.il)
- Amendment 277 to the Income Tax Ordinance, Reshumot 31.12.2024 (knesset.gov.il)
- Tax Authority guidance letter 2025-001394 (gov.il)

## Framing that governs everything below

The reform is TWO independent statutes with one commencement date. s.62A attributes company income
to an active shareholder at marginal rates. ss.81A-81F impose an additive tax on undistributed
excess profits. Different bases, different escapes, and the same headline shekel figure doing
opposite jobs in each. Collapsing them is the single most common error in the secondary literature.

## Must cover (core)

- [ ] Entity gate: chevrat me'atim per s.76, three cumulative conditions.
- [ ] Residence gate for the s.81B charge, and that foreign shareholding does not exempt.
- [ ] Commencement, and the examined-tax-year gate that serves both statutes.
- [ ] The charging rule: the rate, and that its base is excess profits net of the year's dividend,
      NOT retained earnings and NOT a shortfall against a required distribution.
- [ ] The excess-profits formula, and that its two legs are read at DIFFERENT year ends.
- [ ] Taxable accumulated profits as accumulated less exempt accumulated.
- [ ] All THREE shields, each defined in full, and the highest-of rule rather than the sum.
- [ ] The expenses shield as a maximum-of-two, not simply the current year.
- [ ] The assets shield's signed terms, with the held-body term ADDED not subtracted.
- [ ] The anti-splitting rule: equal division across held companies under one controlling
      individual, the waiver notice on the annual return, and the control level it turns on.
- [ ] All THREE escapes, each on its own base, with accumulated and excess profits kept distinct.
- [ ] The loss test measured on the NET loss after offsetting other sources.
- [ ] The warning that the dividend reduces the charging base but NOT the 50% denominator.
- [ ] The two-limb definition of a dividend on which tax was paid, and that an ordinary exempt
      inter-company dividend does not qualify absent the election.
- [ ] Non-deductibility, and that the addition is not part of corporate tax and not creditable.
- [ ] That advance payments do not apply to the addition.
- [ ] The transitional annual route, its rate, its base, and the years it spans.
- [ ] The protection bands: earned once inside the Determining Period, extending later years
      without a further distribution, and WHICH years each band reaches.
- [ ] That every band reaches the current year, so a company meeting the lowest band is covered
      without distributing again. This is the load-bearing fact for a 2026 reader.
- [ ] The boundary ambiguity in the bands, drafted as open ranges with no tie-breaking rule.
- [ ] The 2025-only escape, its base, and BOTH its conditions, kept distinct from the standing
      alternative it is routinely conflated with.
- [ ] The Determining Period end date, and that the dividend must be both paid and received inside it.
- [ ] s.62A classification: the officeholder limb's threshold and its any-day-in-the-year test.
- [ ] s.62A single-client window as amended.
- [ ] That the Ordinance calls the person a controlling shareholder in this section, and that the
      older term is repealed drafting.
- [ ] The s.62A(a1) attribution formula, with its TWO distinct income quantities and the
      related-company deduction inside the bracket.
- [ ] That the two conditions of the attribution paragraph do not include the shekel figure.
- [ ] That the shekel figure sits in the EXCLUSION, is gated on a substantial holder, and that one
      escape route AGGREGATES across all companies where that person is a substantial holder.
- [ ] The reporting vehicle: the annual return plus its dedicated annex.
- [ ] That the withholding report is a different document from the declaration.
- [ ] The deemed-last-day rule and the recurring annual withholding date it produces.

## Should cover (advanced / edge cases)

- [ ] Group structures modelled chain-wide rather than company by company.
- [ ] Capital notes and pre-commencement loans, which carry both a statutory and a circular rule.
- [ ] The forced-distribution power, as a discretionary route alongside the automatic charge.
- [ ] That the parent definition must be read first, being the most reused definition in the reform.
- [ ] Accounting-standard consequences for a user who prepares financial statements.
- [ ] The Tax Authority's own attribution simulator as a routing target rather than a rule.
- [ ] That the replacement s.62A circular remains a draft, so the older circular is still the
      standing published interpretation. Carry a re-check instruction.
- [ ] The officially published worked examples, usable as fixtures.
- [ ] Shareholder-level surtax as a reason a distribution sized only to escape the company charge
      can still be the wrong distribution. NOT YET VERIFIED against the Ordinance; do not state a
      rate or threshold until it is.

## Out of scope (explicit, with rationale)

- Filing any return, annex or withholding report on the user's behalf. The skill computes and
  explains; filing is the taxpayer's or a licensed representative's act.
- Advising a user to liquidate to escape the regime. The statutory window closed at the end of tax
  year 2025, and it is a corporate-law decision in any event. Explain as history.
- Company-law solvency and distribution analysis. Whether a distribution is LAWFUL is separate from
  whether it is tax-effective, and belongs to counsel.
- Companies outside the entity gate. One classification answer, then stop.
- Foreign-resident companies. One line, then stop.
- Treaty rate lookup for a specific foreign shareholder.
- The distributable-profits computation for a liquidation, relevant only to the closed route.
- Audit-selection, risk-scoring or data-matching behaviour. Not in any primary source. The circular
  gives classification indicia for special assets, which is a different thing. Do not invent
  detection criteria.
- Any rate or threshold for tax years beyond those the sources fix. Do not extrapolate.

## Known bad figures in circulation

Each of these is wrong, and each appears in published Israeli guidance. The correct position is in
`evidence.json` with its primary citation.

- That the declaration is filed on the withholding report form. It is not.
- That the headline distribution percentage is measured on trapped or excess profits. It is
  measured on gross accumulated profits, before exempt profits and before the shields.
- That the company must choose between a distribution and "paying" that same percentage as a tax.
  It is a distribution, not a tax, and the date usually quoted alongside it is a reporting deadline
  for a different document.
- That the 2025-only relief and the standing alternative are the same rule at two rates, one
  superseding the other. They are distinct provisions, but they share a base: both run on
  accumulated profits at the preceding year end and both require taxed dividends. They differ in
  rate, in window, and in the transitional provision's payment deadline. Do not over-correct this
  into "unrelated with different bases", which is itself false.
- That the charge falls on retained earnings or on the accumulated balance.
- That the two escape percentages run on one base. They do not.
- That the money shield is available per company within a group.
- That the attribution paragraph requires accumulated profits above the shekel figure. The figure
  sits in an exclusion with different drafting and an aggregation limb.

## Verification note

Every figure this skill states is tied to a verbatim primary-source snippet in `evidence.json`,
extracted directly from the source PDFs. Where research surfaced a figure that could not be quoted
from primary text, the figure is NOT stated in the skill and is recorded here as unverified.
