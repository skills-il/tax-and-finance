# Changelog

All notable changes to this skill are documented here.

## 1.1.0 - 2026-09-16

Content update against Income Tax Circular 7/2025 as amended 08.02.2026.

- Special assets: added the land carve-outs (self-use fixed assets including group use; rental and
  institutional-rental buildings under sections 53(a3) and 53A of the Encouragement of Capital
  Investments Law), the Sale (Apartments) Law financial-accompaniment cash exclusion, and the rule that
  the asset shield runs on tax cost, not book or fair value. The reference file records how the
  circular's worked example treats section 8A(c) land inventory.
- Payment: the 2% addition is due by the section 132 return date or the end of the following tax
  year, whichever is earlier, with linkage and interest under section 159A(a). This is now kept
  distinct from the 16 January date for tax on an elected dividend.
- The 50% alternative: the skill no longer asserts which year end the shields inside its base are read
  at. It quotes the circular and tells the agent to compute both and flag the gap.
- Example 1 is now a numbered worked example with illustrative figures.
- Young companies: the expense-shield average is flagged as undefined with fewer than two preceding
  tax years.
- Escape pricing is framed over several years; added a zero-exposure screen and a Companies Law gotcha.

## 1.0.1 - 2026-09-09

Acted on the MAJOR findings from the launch review panel. No factual corrections; these close gaps
where a term was used without being defined, or where the skill refused without giving a route.

- The Section 62A excess-profitability limb used "profitability rate exceeding 25%" as a gating
  condition without stating its numerator and denominator, so a reader could not tell whether the limb
  bites. The skill now says so explicitly rather than implying the test is complete.
- The four-or-more-employees exclusion was mentioned without its terms, and without resolving whether
  it reaches the new excess-profitability limb or only the pre-existing ones. Both gaps are now stated
  rather than left for the reader to discover.

## 1.0.0 - 2026-09-09

Initial release of Israeli Trapped Profits Planner.

Every factual claim in this skill is tied to a verbatim snippet from a primary source in
`evidence.json`, and each snippet was verified as present at its cited URL before release.
Figures that research surfaced but could not be quoted from primary text are deliberately NOT
stated; they are recorded as unverified in `references/domain-checklist.md`.
