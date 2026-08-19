# Domain coverage checklist, israeli-mortgage-comparator

Anchor for expert review. Scope: comparing Israeli mortgage tracks across banks, computing
mixed-track payments, and the Bank of Israel limits that constrain the mix.

Source of record for every regulatory row below: Proper Conduct of Banking Business Directive 329,
"Limitations on Housing Loans", version [13] (06/26), https://www.boi.org.il/media/ez4npagt/329.pdf

## Must cover (core)

### Tracks and pricing
- The 5 tracks (Prime, fixed non-linked, fixed CPI-linked, variable CPI-linked, variable non-linked).
- Prime is the banks' published rate tracking the Bank of Israel rate. The margin is set by the
  banks, not by regulation, so the skill must route to the bank's published prime rather than
  assert a margin. Only each bank's discount or premium TO prime is negotiable.
- Current Bank of Israel rate as a fetch-always value, not a hard-coded one.

### Directive 329, one row per operative limit
Each of these is a separate item. A single row reading "Directive 329 limits" is not sufficient
coverage, and collapsing the PTI rules into one row is how the prohibition and the risk weight got
conflated into a false "no legal cap, 40% flagged as high risk" claim in v1.2.2.

- **Section 2, LTV ceilings by property class**: single dwelling 75%, replacement 70%, investment 50%.
  The directive classifies by PROPERTY, not residency; there is no foreign-resident LTV row in it.
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
- **Appendix A, how PTI is measured**: monthly repayment over monthly DISPOSABLE income; other loans
  on the same property with over 18 months remaining and the full approved facility in the numerator;
  alimony and any commitment over 18 months as fixed expenses; rent deducted for a borrower not
  living in the purchased apartment; half a first-degree relative's disposable income recognised only
  where the relative guarantees the loan and pays 20% or more of the repayment from their own account.

### Computation and cost
- Amortization math, CPI linkage applied to PRINCIPAL, early-repayment penalty by track type,
  refinancing break-even.
- Required life and property insurance assigned to the bank; closing costs.

### Other
- Reservist (Order 8) statutory protections; verify temporary BoI relief frameworks before quoting.

## Should cover (advanced)
- Mortgage advisor vs direct; end-of-quarter negotiation leverage.
- Dira BeHanacha / Mechir Matara discounted-housing lottery.

## Out of scope (explicit)
- Commercial real-estate loans, business credit lines, non-Israeli mortgages (per description).
- **Purchase-tax bracket figures.** Re-litigated 2026-08-19. A user comparing mortgages plainly does
  ask what purchase tax they will pay, so this is not silence: the skill states the SHAPE of the rule
  (0% band then graduated for a single dwelling, a higher schedule from the first shekel for an
  additional dwelling) and routes to mas.gov.il and to `israeli-real-estate`, which is the
  authoritative holder of the table. The figures are deliberately not duplicated here because two
  copies of a CPI-updated bracket table is two places for it to go stale, and the duplicate in
  v1.2.2 was already a second drift surface for the same fact.
- **A Prime margin over the BoI rate.** Re-litigated 2026-08-19. Users do ask, and the rule is
  "never route a number you could capture", so this needs a reason: on 2026-08-19 the figure could
  not be captured from any reachable authoritative source. boi.org.il HTML is Radware-protected
  against non-browser clients, kolzchut is bot-blocked, the four major banks' rate pages return
  either 404 or a JS shell with no prime in the text layer, and the shared browser was returning
  other agents' pages. The BoI rate itself IS capturable and is wired in as a fetch-always API call.
  The margin is a bank-published figure rather than a regulated constant, so routing the user to the
  bank's own published prime is also the correct answer on the merits. Revisit next cycle.

## Authoritative sources
- Directive 329 full text (PDF): https://www.boi.org.il/media/ez4npagt/329.pdf
- Directive 329 landing / version history: https://www.boi.org.il/roles/supervisionregulation/nbt/nbt329/
- BoI current rate as JSON: https://boi.org.il/PublicApi/GetInterest
- BoI banking supervision index: https://www.boi.org.il/en/economic-roles/supervision-and-regulation/supervision-of-the-banking-system/
- Purchase tax: mas.gov.il, and the `israeli-real-estate` skill
- Mortgage calculator: https://www.gov.il/he/pages/mashkanta-calculator
