# Domain coverage checklist, israeli-insurance-comparator

Anchor for expert review. Scope: helping Israelis compare car (hova/makif/tzad gimel), home (mivne/tochen), and health-supplementary (SHABAN) insurance via government calculators and private platforms.

## Must cover (core)
- Har HaBituach (harb.cma.gov.il) policy-inventory step before comparing, including its duplicate-cover alert and its free presentation and secure forwarding of the motor-property insurance history (avar bituchi).
- Car insurance three layers (hova mandatory / makif / tzad gimel), and that hova is sold at a regulated tariff by risk band (low variance) while makif is market-priced.
- Vehicle types beyond the private car: the CMA calculator prices ofanoa (motorcycle/scooter), bus/tour vehicle, taxi, commercial and special vehicles as first-class categories.
- HaPool (המאגר לביטוח שיורי), the statutory residual market for drivers no insurer will write directly. It heads the CMA calculator's list of carriers on the identical regulated tariff. Distinct from the regulated tariff itself, which is also loosely called "the pool" in English.
- Government tools, each described for what it actually is:
  - car.cma.gov.il, the hova regulated-tariff calculator. It is a risk-parameter form with NO licence-plate field and no vehicle-registry lookup.
  - govcarins.mof.gov.il, a makif simulator FOR STATE EMPLOYEES priced off the annual state tender. Not a general public comparison tool.
  - pe.cma.gov.il, CMA public enquiries and complaints, with a quick-enquiry route that needs no registration.
- CMA Service Index (מדד השירות), the regulator's annual insurer service-and-claims ranking, as a comparison input alongside price and coverage. Always state which year's index is being quoted.
- Correct HMO supplementary tier ladder per kupa: Clalit Mushlam Zahav (basic) / Mushlam Platinum (premium); Maccabi Kesef (entry) / Zahav (middle) / Sheli (top), THREE tiers; Meuhedet Adif (basic) / Shia (premium); Leumit Kesef (basic) / Zahav (premium). Note Leumit's ordering is inverted relative to Maccabi and Clalit.
- SHABAN has no medical underwriting and no pre-existing-condition exclusion at any tier; a health declaration in the joining form is optional and the only condition on a service is its waiting period. Private commercial health policies do underwrite.
- Earthquake coverage included by default by law on opt-out basis, direct from insurer (no central pool).
- Insurance premiums are NOT VAT-rated (an insurer is a mosad kaspi under the VAT law and pays mas sachar ve'revach instead).
- Underinsurance proportional-reduction (klal yachasi), the shin-nun no-claims record and where it actually comes from (Har HaBituach, the insurer's own no-claims certificate, or INFOCAR for a specific vehicle's claims history, NOT HaPool), bank assignment (shibud) for mortgage home insurance.

## Should cover (advanced)
- Bituach Siudi 2025-2027 transition (kupot-channel wind-down on a slipped timeline; 4-of-6 ADL eligibility from 1.1.2025) WITHOUT stating the unenforced 2025 dates as fact, and the August 2026 Clalit-Ayalon agreement effective January 2027.
- Iron Swords war/terror exclusions on travel/life/disability; reservist (miluim) policy adjustments.
- Bundling, annual-vs-monthly payment, deductible tradeoffs, renewal timing.

## Out of scope (explicit)
- Life insurance, pension fund selection, travel insurance. Excluded in the skill description. Re-litigated 2026-08-27: a comparison user does plausibly ask about these, but each is a distinct product with its own comparison mechanics, and the boundary is stated in the description rather than left silent. The skill does surface travel-insurance WAR EXCLUSIONS in the Iron Swords section, which is a cross-reference for a live risk rather than scope creep. Retained as out of scope.
- Commercial and business insurance, professional liability, marine and cargo. Re-litigated 2026-08-27: out of audience for a consumer comparison skill. Retained.

## Carried, not yet covered (revisit next cycle)
- Statutory right to cancel a policy mid-term and the pro-rata refund mechanics for elementary lines. The general right under the Insurance Contract Law is real, but the elementary pro-rata detail was not verified against a primary source this cycle, and Step 9 still frames cancellation only as a penalty risk.
- Agent and platform commission / conflict-of-interest disclosure. The skill routes users to four platforms, at least one of which trades as a licensed agency, and flags a conflict for only one of them.
- The 2026 CMA circular on occasional-driver (nehagim mizdamnim) motor policies, including its disclosure duty about possible absence of hova coverage. Reported but not verified against the circular this cycle.

## Authoritative sources
- CMA / Har HaBituach: https://harb.cma.gov.il/
- CMA car calculator: https://car.cma.gov.il/Parameters/Get?next_page=2&curr_page=2
- CMA Service Index: https://www.gov.il/he/pages/service_index_all
- CMA public enquiries: https://pe.cma.gov.il/Login/Login
- MoF state-employee makif simulator: https://govcarins.mof.gov.il/
- INFOCAR vehicle claims history: https://infocar.co.il/
- Kol Zchut SHABAN and earthquake pages; calcalist.co.il and globes.co.il for siudi market coverage
