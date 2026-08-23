# Domain Coverage Checklist -- us-israel-dual-tax-navigator

Generated: 2026-08-23 via research on: irs.gov (primary pages, Publication 54, Rev. Proc.
2024-40 and 2025-32 PDFs, IRM 4.26.16, the US-Israel treaty text), govinfo.gov (31 CFR
1010.821), fincen.gov, OMB Memorandum M-26-11.

Aggregator taxonomy sweep (Step A): the IRS "International taxpayers" hub plus the
Taxes-for-Expats and CWS Israel country guides were used ONLY to enumerate the candidate
topic list. Every value below is cited to a primary source, per the primary-source rule.

## Must cover (core)

- [ ] Citizenship-based taxation premise -- a US citizen files a 1040 on worldwide income
      regardless of residence, and a zero-tax year does not remove the filing duty.
      source: https://www.irs.gov/individuals/international-taxpayers/us-citizens-and-resident-aliens-abroad
      why core: the entire skill is meaningless if the user believes aliyah ended the duty.

- [ ] Filing deadline chain for a taxpayer abroad, all four dates, as its own row set:
      regular due date 15 April; AUTOMATIC 2-month extension to 15 June with no request;
      further extension to 15 October by filing Form 4868 BEFORE the 15 June date;
      interest still accrues from 15 April regardless of extension.
      source: https://www.irs.gov/individuals/international-taxpayers/us-citizens-and-resident-aliens-abroad
      why core: the "extension to file is not an extension to pay" trap is the single most
      common costly misunderstanding, and the 4868 must be filed before June 15, not after.

- [ ] FBAR (FinCEN 114) threshold: aggregate value of ALL foreign financial accounts
      exceeds USD 10,000 at ANY time during the calendar year. Aggregate, not per account.
      source: https://www.irs.gov/newsroom/details-on-reporting-foreign-bank-and-financial-accounts
      why core: nearly every US person in Israel crosses this, and most assume it is a
      per-account test or an income test.

- [ ] FBAR deadline: due 15 April, automatically extended to 15 October with no request.
      source: https://www.irs.gov/newsroom/details-on-reporting-foreign-bank-and-financial-accounts
      why core: differs in mechanism from the 1040 extension and is filed to FinCEN, not IRS.

- [ ] FBAR penalty structure, BOTH prongs and BOTH the statutory and adjusted figures:
      non-willful statutory USD 10,000 adjusted to USD 16,536 (31 USC 5321(a)(5)(B)(i));
      willful statutory USD 100,000 adjusted to USD 165,353 (31 USC 5321(a)(5)(C)(i)(I)),
      but the willful penalty is the GREATER of that adjusted amount or 50% of the account
      balance at the violation date.
      source: govinfo CFR-2025-title31-vol3-sec1010-821 ; https://www.irs.gov/irm/part4/irm_04-026-016
      why core: quoting only the fixed dollar figure understates willful exposure by orders
      of magnitude on a large account. Both prongs are required.

- [ ] Penalty TEMPORAL rule (Step C.1a): the 31 CFR 1010.821 figures are inflation-adjusted
      annually, BUT OMB Memorandum M-26-11 (17 April 2026) directed no annual inflation
      adjustment for calendar year 2026, so the 2025 levels remain in force for 2026.
      source: OMB M-26-11 as reported in the 2026 Federal Register penalty-adjustment notices
      why core: a skill that says "adjusted annually, check the current table" without the
      2026 freeze sends the user hunting for a revision that does not exist.

- [ ] Form 8938 thresholds, enumerated by ALL FOUR sub-dimensions (Step C.1): filer living
      abroad vs in the US, unmarried/MFS vs married filing jointly, and last-day-of-year vs
      any-time-during-year. Living abroad: unmarried more than USD 200,000 last day or
      300,000 any time; MFJ more than USD 400,000 last day or 600,000 any time. Living in
      the US: unmarried 50,000 / 75,000; MFJ 100,000 / 150,000.
      source: https://www.irs.gov/businesses/comparison-of-form-8938-and-fbar-requirements
      why core: the abroad thresholds are 4x the domestic ones and guides routinely quote
      the domestic row to an expat audience.

- [ ] 8938 and FBAR are INDEPENDENT duties with separate penalties. Filing one never
      satisfies the other, and the same account is commonly reported on both.
      source: https://www.irs.gov/businesses/comparison-of-form-8938-and-fbar-requirements
      why core: users routinely believe FBAR "covers it".

- [ ] FEIE amount by tax year, with the statutory cite: TY2025 USD 130,000, TY2026
      USD 132,900, both under section 911(b)(2)(D)(i).
      source: Rev. Proc. 2024-40 section 3.39 ; Rev. Proc. 2025-32 section 3.39
      why core: the IRS FEIE landing page is STALE and stops at 2023 (see Known bad sources).

- [ ] FEIE vs Foreign Tax Credit, the interaction rules, not merely the two definitions:
      a credit may NOT be claimed for taxes on income excluded under FEIE; and taking the
      credit on excluded income may be treated as REVOKING the election.
      source: https://www.irs.gov/individuals/international-taxpayers/foreign-tax-credit
      why core: this is the decision the skill exists to support.

- [ ] FEIE revocation and the 5-year bar: a revoked election cannot be re-made for the next
      5 tax years without IRS approval (a ruling request). Claiming the foreign tax credit,
      the additional child tax credit, or the earned income credit in a later year is itself
      treated as revoking the prior choice.
      source: IRS Publication 54, "Effect of Choosing the Exclusions and Deduction"
      why core: an accidental, unnoticed revocation is a real and expensive failure mode,
      and it is the hinge between this skill and the child-credit question.

- [ ] Streamlined Foreign Offshore Procedures, all four elements: the non-residency test
      (in one or more of the most recent 3 years for which the due date has passed, no US
      abode AND physically outside the US at least 330 full days); 3 years of delinquent or
      amended returns; 6 years of delinquent FBARs; and the penalty relief, being no
      failure-to-file, failure-to-pay, accuracy-related, information-return or FBAR penalties.
      Full tax and interest must still be remitted.
      source: https://www.irs.gov/individuals/international-taxpayers/u-s-taxpayers-residing-outside-the-united-states
      why core: this is the actual route for the never-filed oleh, and the 3-vs-6 year
      asymmetry is the detail that gets it wrong in practice.

- [ ] Treaty savings clause: each state may tax its citizens as if the Convention had not
      come into effect, SUBJECT TO the paragraph 4 carve-outs which preserve Article 26
      (Relief from Double Taxation), Article 21 (Social Security Payments) and others.
      source: https://www.irs.gov/pub/irs-trty/israel.pdf Article 6(3) and 6(4)
      why core: users read "there is a treaty" as "I am protected". The carve-out list is
      what actually preserves double-tax relief, and naming it is the honest answer.

- [ ] NIS to USD conversion duty: US returns are stated in USD, so Israeli-source figures
      must be translated. Pair with the boi-exchange MCP for Bank of Israel representative
      rates.
      why core: every number the user has is in shekels.

## Should cover (advanced / edge cases)

- [ ] Which Israeli filing the user is aligning against and that the Israeli tax
      year is the calendar year, so the two systems share a year boundary but not deadlines.
      Defer the Israeli mechanics to `israeli-tax-returns`.
- [ ] Delinquent FBAR submission procedure where returns are correct and only FBARs are
      missing, which is a lighter route than streamlined.
- [ ] The document pack: what to hand an Israeli accountant vs a US preparer, and what only
      exists on one side (tofes 106, tofes 867, US 1099/W-2 equivalents).
- [ ] Married-to-a-non-US-spouse filing status choices and why MFS is common in Israel.
- [ ] State filing residue for those who never formally severed a US state domicile.

## Out of scope (explicit, with rationale)

- Per-product PFIC and foreign-trust classification of Israeli savings vehicles -- this is a
  distinct job with a distinct trigger. Related skill: `us-person-israeli-investment-check`.
- Self-employment tax, SECA, and the absent totalization agreement -- distinct audience and
  distinct math. Related skill: `american-freelancer-israel-tax`.
- Israeli-side return preparation and submission to Reshut HaMisim. Related skill:
  `israeli-tax-returns`.
- Renunciation and the section 877A exit tax -- small audience, and it is an irreversible
  personal-status decision that belongs with counsel, not a worksheet.
- Completing, signing or submitting any return, and any representation before the IRS or
  Reshut HaMisim. Reserved to licensed practitioners. See the Legal notice.

## Known bad sources and figures (do not regress to these)

- The IRS FEIE landing page
  (https://www.irs.gov/individuals/international-taxpayers/foreign-earned-income-exclusion)
  lists only 2020 through 2023 amounts (107,600 / 108,700 / 112,000 / 120,000). It is STALE.
  Take the current amount from the Revenue Procedure for the tax year, never from this page.
- Secondary expat-tax guides frequently quote the DOMESTIC 8938 thresholds (50,000 / 75,000)
  to an expat audience. The abroad thresholds are 200,000 / 300,000 / 400,000 / 600,000.
- Guides quote the willful FBAR penalty as a flat 165,353 and omit the 50%-of-balance prong.

## Authoritative sources

- https://www.irs.gov/individuals/international-taxpayers/us-citizens-and-resident-aliens-abroad -- deadlines, extension chain
- https://www.irs.gov/newsroom/details-on-reporting-foreign-bank-and-financial-accounts -- FBAR threshold and deadline
- https://www.irs.gov/businesses/comparison-of-form-8938-and-fbar-requirements -- 8938 thresholds, independence of the two duties
- https://www.irs.gov/pub/irs-drop/rp-25-32.pdf -- TY2026 FEIE amount
- https://www.irs.gov/pub/irs-drop/rp-24-40.pdf -- TY2025 FEIE amount
- https://www.irs.gov/individuals/international-taxpayers/foreign-tax-credit -- FTC vs exclusion interaction
- https://www.irs.gov/publications/p54 -- revocation and the 5-year bar
- https://www.irs.gov/individuals/international-taxpayers/u-s-taxpayers-residing-outside-the-united-states -- streamlined procedures
- https://www.govinfo.gov/content/pkg/CFR-2025-title31-vol3/xml/CFR-2025-title31-vol3-sec1010-821.xml -- FBAR penalty table
- https://www.irs.gov/irm/part4/irm_04-026-016 -- willful penalty 50% prong
- https://www.irs.gov/pub/irs-trty/israel.pdf -- treaty savings clause and carve-outs
