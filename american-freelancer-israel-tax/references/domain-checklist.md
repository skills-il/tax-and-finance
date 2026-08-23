# Domain Coverage Checklist -- american-freelancer-israel-tax

Generated: 2026-08-23 via research on: irs.gov primary sources (the self-employment tax page,
the Instructions for Schedule SE, and the Schedule SE form itself).

Aggregator sweep (Step A): Israeli expat-tax practitioner guides were used ONLY to enumerate
the candidate topic list and to identify the commonly quoted worked example. Every rate,
threshold and list below is cited to a primary source.

## Must cover (core)

- [ ] The absence of a US-Israel totalization agreement, evidenced by the FULL country list
      rather than asserted. Thirty countries are named in the Schedule SE instructions and
      Israel is not among them.
      source: Instructions for Schedule SE
      why core: this is the premise of the whole skill, and it is the kind of negative claim
      that must be shown from an enumerated list, not from a secondary source saying so.

- [ ] That the foreign earned income exclusion does NOT reduce self-employment tax, and that a
      self-employed US citizen abroad must in most cases pay it.
      source: Instructions for Schedule SE
      why core: the single most damaging misconception in the domain.

- [ ] The rate decomposed, not just the headline: 15.3 percent total, being 12.4 percent
      social security and 2.9 percent Medicare, because only the first is capped.
      source: IRS self-employment tax page

- [ ] The USD 400 net-earnings threshold at which SE tax applies.
      source: IRS self-employment tax page

- [ ] The 92.35 percent factor and its place in the ORDER of operations (applied before the
      rates, per Schedule SE line 4a).
      source: Schedule SE, line 4a
      why core: omitting it overstates every projection by roughly 8 percent.

- [ ] The social security wage base as a TEMPORAL row (Step C.1a): it is set annually, the
      2025 figure is USD 176,100, and a prior year's figure must never be carried forward. The
      Medicare portion is uncapped, so the two components behave differently above the base.
      source: Instructions for Schedule SE
      why core: capping both components, or neither, is the main high-earner error.

- [ ] Additional Medicare Tax thresholds enumerated by filing status (Step C.1): MFJ USD
      250,000, MFS USD 125,000, single/HoH/QSS USD 200,000, plus the rule that wages reduce
      the threshold applied to self-employment income.
      source: Instructions for Schedule SE

- [ ] The SE tax deduction stated precisely: the employer-equivalent portion is deductible in
      figuring adjusted gross income, it affects income tax ONLY, and it reduces neither net
      earnings from self-employment nor the SE tax itself.
      source: IRS self-employment tax page
      why core: the imprecise version leads users to under-reserve.

- [ ] The quarterly estimated payment cycle, and that a filing extension is not a payment
      extension.

- [ ] The structural options presented as a comparison with costs, never as a recommendation,
      with the US anti-deferral exposure for owners of foreign corporations named as the
      hidden cost of the "just open an Israeli company" answer.
      why core: it is the most common forum advice and the most under-examined.

## Should cover (advanced / edge cases)

- [ ] Distinguishing an osek from a sachir on a tlush at the outset, since the analysis differs.
- [ ] Converting shekel invoice income to USD net earnings, and the set-aside percentage back
      to shekels.
- [ ] Interaction with the income-tax side (exclusion versus credit), owned by
      `us-israel-dual-tax-navigator` and cross-referenced only.

## Out of scope (explicit, with rationale)

- Whether to incorporate. This is the decision that most needs a licensed cross-border
  adviser, and giving it is exactly what this skill must not do.
- Anti-deferral rules for a US person owning a foreign corporation. Named in the body so it is
  visibly excluded rather than silently missing.
- Annual filing mechanics, FBAR, Form 8938, the exclusion-versus-credit choice. Related skill:
  `us-israel-dual-tax-navigator`.
- PFIC and foreign-trust classification. Related skill: `us-person-israeli-investment-check`.
- Israeli bookkeeping, VAT, invoicing, osek thresholds. Related skills:
  `israeli-freelancer-ops`, `israeli-vat-reporting`.
- Bituach Leumi rates and entitlements on the Israeli side.

## Known bad framings (do not regress to these)

- "The exclusion means you owe nothing." False for SE tax specifically.
- Applying 15.3 percent to full net earnings without the 92.35 percent step.
- Presenting an Israeli company as a clean fix for the double social charge.
- Assuming a totalization agreement exists because most OECD countries have one.

## Authoritative sources

- https://www.irs.gov/pub/irs-pdf/i1040sse.pdf -- country list, exclusion rule, wage base, Additional Medicare thresholds
- https://www.irs.gov/pub/irs-pdf/f1040sse.pdf -- line 4a and the 92.35 percent factor
- https://www.irs.gov/businesses/small-businesses-self-employed/self-employment-tax-social-security-and-medicare-taxes -- rate, split, USD 400 threshold, the deduction
