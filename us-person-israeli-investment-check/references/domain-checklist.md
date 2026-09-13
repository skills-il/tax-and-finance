# Domain Coverage Checklist -- us-person-israeli-investment-check

Generated: 2026-08-23 via research on: irs.gov primary sources (Instructions for Form 8621,
Revenue Procedure 2020-17, the Form 3520 and 3520-A pages).

Aggregator sweep (Step A): expat-tax practitioner guides were used ONLY to enumerate which
Israeli products belong in the candidate list. Every criterion below is cited to a primary
source, and no secondary source was used for a value.

## Must cover (core)

- [ ] The two regimes are SEPARATE. PFIC is about stock in a foreign corporation and leads to
      Form 8621; foreign trust is about an arrangement and leads to Forms 3520 and 3520-A. A
      product can be in one, both, or neither.
      why core: conflating them is the single most common error, in guides and in agents.

- [ ] PFIC tests, both, with their statutory cites: income test 75 percent of gross income
      passive under section 1297(b); asset test at least 50 percent of average assets passive
      under section 1297(e). Either one is sufficient.
      source: Instructions for Form 8621
      why core: the actual legal test, as opposed to "Israeli funds are PFICs" folklore.

- [ ] The Form 8621 Part I USD 25,000 exception, per section 1291 fund: aggregate value of ALL
      PFIC stock on the last day of the tax year is USD 25,000 or less (combined USD 50,000 on a
      joint return), AND no excess distribution from that fund, AND no gain recognized on
      disposing of its stock. Plus the limits on it: it relieves Part I only and does not change
      taxation or other duties. (Corrected 2026-09-13: v1.0.0 had borrowed an "any disposal
      day" condition from the unrelated section 1297(f)(2) deemed-election passage.)
      source: Instructions for Form 8621, Exceptions to Filing Part I
      why core: routinely omitted, and its omission manufactures a filing duty that does not
      exist for smaller holders.

- [ ] The section 1291 default regime: excess distribution rules, and the entire gain on
      disposition treated as an excess distribution. Elections exist (QEF, mark-to-market) and
      are a preparer's call; a QEF election depends on a PFIC Annual Information Statement from the fund.
      source: Instructions for Form 8621
      why core: explains WHY PFIC status matters rather than merely asserting that it does.

- [ ] The USD 5,000 Part I exception, limited to a fund owned THROUGH ANOTHER PFIC (per fund,
      same no-excess-distribution, no-gain and no-QEF conditions; it does not reach stock held
      through a grantor-trust wrapper), and the aggregate carve-outs and no-QEF condition of the
      USD 25,000 exception. (Scope corrected 2026-09-13 after Expert iteration 2.)
      source: Instructions for Form 8621; Treas. Reg. 1.1298-1(c)(2)

- [ ] LOOK-THROUGH for wrapper products: an owner of a grantor trust is treated as owning the
      stock it holds, so a pension, gemel or hishtalmut can carry indirect PFIC stock; Rev.
      Proc. 2020-17 does not affect other reporting; Reg. 1.1298-1(c)(4) foreign pension fund
      exception depends on the treaty and is routed to a preparer. (Added 2026-09-13 after
      Expert review found the wrapper rows implied no Form 8621 exposure.)
      source: Treas. Reg. 1.1291-1(b)(8)(iii)(D) and 1.1298-1(c)(4); Rev. Proc. 2020-17

- [ ] The 5.03(5) and 5.04(4) PENALTY limb: a plan passes if penalties apply to earlier
      withdrawals, so whether Israeli tax on early keren hishtalmut withdrawal is a penalty is
      the live question.
      source: Rev. Proc. 2020-17 sections 5.03(5) and 5.04(4)

- [ ] Revenue Procedure 2020-17 SCOPE: an exemption from section 6048 information reporting
      ONLY, not from taxation.
      source: Rev. Proc. 2020-17 section 1
      why core: the most misreported point in this domain. Exempt from reporting is not exempt
      from tax.

- [ ] Revenue Procedure 2020-17 ELIGIBILITY GATE: only eligible individuals, generally those
      already compliant with the related income tax obligations, may rely on it.
      source: Rev. Proc. 2020-17 section 1, referring to section 5.02
      why core: a never-filed user cannot lead with the exemption, which sets the ordering
      against the catch-up skill.

- [ ] Section 5.03 criteria in FULL, enumerated as their own rows (Step C.1), not summarised:
      the exclusive-purpose test, (1) local tax favour, (2) local reporting, (3) earned-income
      contributions only, (4) a percentage-of-earned-income cap OR the USD 50,000 annual OR
      USD 1,000,000 lifetime limit (disjunctive), (5) the
      withdrawal condition and its narrow carve-out, (6) employer nondiscrimination.
      source: Rev. Proc. 2020-17 section 5.03
      why core: criterion (5) decides most Israeli cases and a summarised checklist hides it.

- [ ] Section 5.04 criteria in FULL, including its OWN purpose test limited to medical,
      disability or educational benefits, and the USD 10,000 annual or USD 200,000 lifetime
      limits.
      source: Rev. Proc. 2020-17 section 5.04
      why core: the frequent error is treating 5.04 as a catch-all for anything that failed
      5.03.

- [ ] Form 3520 and Form 3520-A triggers, and that they are different filings by different
      filers.
      source: the IRS pages for each form

- [ ] The USD conversion duty for the 5.03(4) dollar limbs and 5.04(3), at the rate the
      Revenue Procedure fixes: US Treasury Bureau of the Fiscal Service rate on the last day of
      the tax year. The answer can flip year to year on the rate alone.
      source: Rev. Proc. 2020-17 sections 5.03(4) and 5.04(3)

- [ ] The epistemic frame: the IRS has never issued guidance naming Israeli products, so the
      output is a screen and never a classification.
      why core: this is simultaneously the honest position and the legally safe one.

## Should cover (advanced / edge cases)

- [ ] Bituach menahalim, which is genuinely indeterminate without the policy terms.
- [ ] The interaction with Form 8938, which reports many of these as specified foreign
      financial assets. Owned by `us-israel-dual-tax-navigator`, cross-referenced only.
- [ ] That a fund's PFIC status depends on its actual holdings, so a track change inside the
      same product can change the answer.

## Out of scope (explicit, with rationale)

- Annual filing mechanics, deadlines, FBAR and the exclusion-versus-credit choice. Related
  skill: `us-israel-dual-tax-navigator`.
- Israeli-side taxation of these products. Related skills: `israeli-pension-advisor`,
  `israeli-tax-returns`.
- Self-employment tax. Related skill: `american-freelancer-israel-tax`.
- Making or choosing between QEF and mark-to-market elections. Reserved to a preparer.
- Any buy, sell, hold or switch recommendation. That is investment advice, separately
  regulated, and out of scope on purpose.

## Known bad sources and framings (do not regress to these)

- Guides that state flatly "keren hishtalmut is a foreign trust". No IRS guidance says so.
  The defensible output is the criteria it appears to fail.
- Guides that describe Rev. Proc. 2020-17 as making Israeli pensions "tax exempt" in the US.
  It is a reporting exemption under section 6048 only.
- Guides that assert a Form 8621 duty for every PFIC holder without the de minimis exception.

## Authoritative sources

- https://www.irs.gov/pub/irs-pdf/i8621.pdf -- PFIC tests, de minimis exception, 1291 regime
- https://www.irs.gov/pub/irs-drop/rp-20-17.pdf -- sections 5.02, 5.03, 5.04 and the scope limit
- https://www.irs.gov/forms-pubs/about-form-3520 -- Form 3520 triggers
- https://www.irs.gov/forms-pubs/about-form-3520-a -- Form 3520-A duty
- https://www.irs.gov/forms-pubs/about-form-8621 -- Form 8621 identity and current revision
