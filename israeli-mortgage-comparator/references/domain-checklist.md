# Domain coverage checklist, israeli-mortgage-comparator

Anchor for expert review. Scope: comparing Israeli mortgage tracks across banks, computing
mixed-track payments, and the Bank of Israel limits that constrain the mix.

Source of record for every regulatory row below: Proper Conduct of Banking Business Directive 329,
"Limitations on Housing Loans", version [13] (06/26), https://www.boi.org.il/media/ez4npagt/329.pdf

## Must cover (core)

### Tracks and pricing
- The 5 tracks (Prime, fixed non-linked, fixed CPI-linked, variable CPI-linked, variable non-linked).
- Prime = Bank of Israel rate + 1.5 percentage points. Captured 2026-10-01 from the BoI's own
  Directive 451 Appendix 6 explanation sheet and from a bank's published definition. Only each
  bank's discount or premium TO prime is negotiable.
- Current Bank of Israel rate as a fetch-always value, not a hard-coded one.

### Directive 329, one row per operative limit
Each of these is a separate item. A single row reading "Directive 329 limits" is not sufficient
coverage, and collapsing the PTI rules into one row is how the prohibition and the risk weight got
conflated into a false "no legal cap, 40% flagged as high risk" claim in v1.2.2.

- **Section 2, LTV ceilings by property class**: single dwelling 75%, replacement 70%, investment 50%.
  CORRECTED 2026-10-01: section 1 defines single and replacement dwellings as bought by an
  individual "Israeli citizen" within Land Taxation Law s.16A(a)(1)-(1b) (registered or obliged to
  register in the Population Registry, an individual Israeli resident, or a Law-of-Return-eligible
  resident of the Area); everything else is an investment dwelling. A buyer outside all three is in
  the 50% row even for an only home. (The v1.3.0 "classifies by property, not residency" wording,
  and a first repair reading it as plain citizenship, were both wrong.)
- **Section 4**, the same ceilings applied to the aggregate with earlier loans on the same apartment.
- **Section 10a**, the discretion to disapply section 4 up to 70% LTV where the excess above 50% is
  under 200,000 NIS.
- **Section 4a**, valuation of a discounted-price apartment: value capped at 2.1 million NIS or the
  purchase price whichever is higher, penalties deducted, minimum own funds of 60,000 or 100,000 NIS.
- **Section 5, the PTI PROHIBITION at 50%.** A bank shall not approve or execute above it. Must be
  presented as a ceiling on the bank, never as a borrowing allowance.
- **Section 6, the 100% risk weight above 40% PTI.** A bank capital rule, not a borrower cap and not
  merely a "flag". Must be presented as a cost cliff, and must NOT be described as a legal limit.
- **Section 11**, sections 5 and 6 do not apply to 12.1 and 12.2 loans.
- **Section 7, variable-rate share capped at 66.66%** of the loan, covering Prime and every other
  variable track together. The directive contains NO Prime-specific cap; the word does not appear
  in it. Any "Prime limited to one third" statement is a coverage failure.
- **Section 8**, 30-year maximum to final repayment. **Section 8a**, temporary 10% quarterly cap on
  contractor-subsidised bullet and balloon loans, in force to 31.12.2026.
- **Section 9**, refinancing may not create or widen a breach of any limit.
- **Section 12**, the carve-outs: bridge loans up to 3 years, any-purpose loans up to 120,000 NIS,
  FX or FX-linked loans to a foreign resident.
- **Section 13**, the public-sector and defence-system lane, limits disapplied up to 50,000 NIS.
- **Appendix A aggregation start date**: loans on the same property from any lender count in the
  PTI numerator for loans given from 1.10.2026 (circular 2852 postponed it from 1.7.2026).
- **LTV value**: the lower of the appraisal and the purchase-agreement cost (BoI Q&A on 329,
  quoting reporting directive 876), not the purchase price alone.
- **Appendix A, how PTI is measured**: monthly repayment over monthly DISPOSABLE income; other loans
  on the same property with over 18 months remaining and the full approved facility in the numerator;
  alimony and any commitment over 18 months as fixed expenses; rent deducted for a borrower not
  living in the purchased apartment; half a first-degree relative's disposable income recognised only
  where the relative guarantees the loan and pays 20% or more of the repayment from their own account.

### Offer comparison, Directive 451 (added 2026-10-01)
- Approval in principle: written answer within 5 business days (no duty to give reasons),
  terms held for at least 24 days, no costs charged at that stage.
- The three uniform baskets (100% fixed non-linked; 1/3 fixed non-linked + 1/3 Prime + 1/3
  variable CPI-linked every 5 years; 1/2 fixed non-linked + 1/2 Prime), Spitzer, terms 10-30.
- Printed metrics: total projected repayment, highest projected monthly payment.
- Insurance: external insurance right; none required up to 30,000 NIS.
- Appraisal reuse within 90 days; mortgage porting (s.20); partial repayment shortens term.

### Early-repayment fees, Banking Order 2002 (added 2026-10-01)
- Operational fee (up to 60 NIS), one-tenth-of-a-percent short-notice fee (under 10 days; notice max 45 days),
  capitalisation fee against the Supervisor's AVERAGE rate, 20%/30% discounts at 3/5 years,
  CPI-average fee on days 1-15, no capitalisation fee on Prime / annual-or-more-frequent
  variable tracks, operational fee only on a reset date.

### Computation and cost
- Amortization math, CPI linkage applied to PRINCIPAL, early-repayment penalty by track type,
  refinancing break-even.
- Required life and property insurance assigned to the bank; closing costs.

### Other
- Reservist and wartime relief: do not present a standing right to defer mortgage payments; the
  deferrals seen so far came from time-limited arrangements. BoI frameworks are
  time-boxed (directive 253 ran to 31.05.2026); the Execution Office reservist regulations freeze
  enforcement (reservist and spouse, three months, expire by 28.02.2027) but not the duty to pay.

## Should cover (advanced)
- Mortgage advisor vs direct; end-of-quarter negotiation leverage.
- Dira BeHanacha / Mechir Matara discounted-housing lottery.

## Out of scope (explicit)
- Commercial real-estate loans, business credit lines, non-Israeli mortgages (per description).
- **Purchase-tax bracket figures.** Re-litigated 2026-08-19, rationale refreshed 2026-10-01 (unchanged). A user comparing mortgages plainly does
  ask what purchase tax they will pay, so this is not silence: the skill states the SHAPE of the rule
  (0% band then graduated for a single dwelling, a higher schedule from the first shekel for an
  additional dwelling) and routes to mas.gov.il and to `israeli-real-estate`, which is the
  authoritative holder of the table. The figures are deliberately not duplicated here because two
  copies of a CPI-updated bracket table is two places for it to go stale, and the duplicate in
  v1.2.2 was already a second drift surface for the same fact.
- **Bank-specific age limits at final repayment.** Re-litigated 2026-10-01. Users do ask. It is
  bank policy, not regulation (Directive 329 caps only the term), and varies by bank, so the skill
  says so and routes to each bank rather than asserting a number.
- **New-build purchases from a contractor** (staged draws, construction-input index, Sale Law
  guarantees). Re-litigated 2026-10-01: a real and common user need, deferred to next cycle for
  lack of word budget in SKILL.md; candidate for a new references file.

(The former out-of-scope row "A Prime margin over the BoI rate" was REOPENED and resolved on
2026-10-01: the margin is now captured and stated.)

## Authoritative sources
- Directive 329 full text (PDF): https://www.boi.org.il/media/ez4npagt/329.pdf
- Directive 329 landing / version history: https://www.boi.org.il/roles/supervisionregulation/nbt/nbt329/
- BoI current rate as JSON: https://boi.org.il/PublicApi/GetInterest (negative control: /PublicApi/GetInterestXYZ returns 404)
- Directive 451 (procedures, uniform baskets): https://www.boi.org.il/media/utld2tgp/451.pdf
- Early-repayment order: https://www.boi.org.il/media/qy5cow0l/116.pdf
- BoI banking supervision index: https://www.boi.org.il/en/economic-roles/supervision-and-regulation/supervision-of-the-banking-system/
- Purchase tax: mas.gov.il, and the `israeli-real-estate` skill
- Mortgage calculator: https://www.gov.il/he/pages/mashkanta-calculator
