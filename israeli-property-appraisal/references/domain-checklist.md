# Domain Coverage Checklist: israeli-property-appraisal

Generated: 2026-07-30. Verified against Kolzchut (betterment levy, exemptions, objections), the deciding-appraiser fee regulations on Nevo, Bank of Israel Directive 329, and Standard 19 published by the Land Appraisers Council. Every figure referenced below is recorded in `evidence.json` with its source quotation.

This file is the coverage contract. A future `update-skill` run re-reads it and flags any Must-cover item missing from SKILL.md.

## Must cover (core)

- [ ] Who may issue a valuation, only a licensed appraiser registered with the Land Appraisers Council may produce a shuma; the skill's output is an indication of value only. Why core: the largest liability risk in the whole domain
- [ ] The comparison approach and its adjustment dimensions, floor, lift, size, condition, parking, balcony, protected space, storage, building age, orientation, view, noise, unexercised building rights, ownership against Israel Land Authority lease, and deal date. Why core: an unadjusted price per square metre is the classic wrong answer
- [ ] Contaminated rows in the published data, transfers between relatives, partial-share sales, and combination deals publish alongside genuine sales. Why core: they distort any average and must be identified rather than hidden
- [ ] Non-residential filtering, shops, offices, storage and land price on a different basis. Why core: the dataset mixes them into the same polygon
- [ ] Pagination, the transactions endpoint returns a small default page out of hundreds or more. Why core: an unpaginated answer silently describes only the newest deals
- [ ] Coverage is not uniform, some addresses return neither a parcel nor deals. Why core: a coverage gap must be reported as missing data, never as a low value
- [ ] Standard 19 and why a bank appraisal is conservative by design, the conservative-approach requirement, stringent assumptions where data is missing, caution in unusual market conditions, and the refusal to value at all where material data is absent. Why core: prevents the user from disputing a correct appraisal
- [ ] What a Standard 19 appraiser actually checks, legal status, planning status including permits and unpermitted construction, and measured against registered area. Why core: these are the common causes of a low appraisal and are fixable beforehand
- [ ] The loan-to-value caps and the repayment-to-income cap under Directive 329, and that the ratio is measured against the purchased asset alone. Why core: this is what converts an appraisal shortfall into a cash gap
- [ ] Routes when a bank appraisal is low, obtain the document, examine the comparables used, submit corrections and counter-comparables, second appraiser from the bank's list, or move banks; there is no statutory appeal since the appraiser serves the bank. Why core: the primary job to be done
- [ ] The betterment levy rate and that it is charged by the local committee, not the Tax Authority. Why core: the headline number and the most common confusion with betterment tax
- [ ] Who is liable, the owner or long-term lessee holding rights at the time of the betterment. Why core: liability attaches by date of holding, not by who sells
- [ ] The three triggering events, enumerated in full, plan approval, relief, non-conforming use. Why core: users commonly believe only a plan counts
- [ ] Calculated at plan approval, paid at realisation. Why core: explains a levy surfacing decades later, and the indexation that follows
- [ ] The pre-1975 cutoff for plans. Why core: eliminates whole classes of old-plan claims
- [ ] The exemption list, each with its condition, including the residential building or expansion exemption with its total-area limit and its multi-year occupancy condition, the protected-space exemption for the minimum required area, and the reduced rate where the betterment arises from seismic strengthening. Why core: an exemption removes the bill entirely and is checked before arguing amount
- [ ] The two sub-rules of the residential exemption that people get wrong, the limit is total post-expansion area rather than area added, and breaching the occupancy condition revives the debt. Why core: the arithmetic, not the existence, is where money is lost
- [ ] The exemption request deadline to the local committee. Why core: a missed window
- [ ] The two objection routes and the split between them, whether the levy is owed goes to the district appeals committee, the amount goes to a deciding appraiser. Why core: the highest-value single fact; filing in the wrong forum forfeits the deadline
- [ ] Both objection deadlines, including the alternative period running from display of the assessment table. Why core: unrecoverable if missed
- [ ] How a deciding appraiser is appointed and the document deadlines that follow. Why core: the procedural path the user must actually walk
- [ ] The appeal chain after a deciding appraiser's decision, through the appeals committee for compensation and betterment levy and on to the administrative affairs court. Why core: users assume the decision is final or assume court is next, and both are wrong
- [ ] The deciding-appraiser fee, as a full marginal band table with its floor, ceiling and VAT treatment, plus the default equal split and the appraiser's power to vary it. Why core: the go/no-go economics of challenging at all
- [ ] The advisory-appraiser fee range. Why core: the cost of the other forum
- [ ] Correction of a factual error as distinct from an objection. Why core: cheapest fix, and users burn the objection window on typos
- [ ] The output is not a shuma, and a binding position needs a licensed appraiser. Why core: stated at creation and repeated at the drafting step

## Should cover (advanced / edge cases)

- [ ] The advisory appraiser as distinct from the deciding appraiser, advisory to the committee rather than binding
- [ ] Deferral of payment against a guarantee so a sale or permit can proceed while a dispute runs
- [ ] The local committee's certificate confirming the levy is settled or secured, without which a sale cannot be registered
- [ ] Partial realisation of rights producing a proportional levy
- [ ] Development levies and permit fees that are not the betterment levy, which users often blame on it
- [ ] That private appraiser fees are commercially negotiated with no regulated tariff, unlike the deciding and advisory appraiser fees
- [ ] Valuation for court as a distinct product with its own expert-opinion guidelines
- [ ] Verifying an appraiser's licence and locating the deciding-appraiser register
- [ ] Reporting lag in the published transaction data, since deals appear on a reporting basis rather than at registration

## Out of scope (explicit, with rationale)

- Purchase tax and betterment tax (mas rechisha, mas shevach), a separate tax administered by the Tax Authority with its own rates, exemptions and forums, not by the local planning committee
- Municipal tax (arnona) and its area measurement, a recurring municipal charge with its own objection track, unrelated to valuation
- Conveyancing, sale contracts, and registration, legal work, not valuation, handled in the legal-tech category
- Mortgage track selection, rates and mix, the financing product rather than the collateral valuation; `israeli-mortgage-comparator` handles it
- Building permit procedure itself, covered only as a levy realisation trigger
- Urban renewal deal advice, including developer negotiation and tenant consent, a full domain of its own; only the levy treatment is in scope
- Income-capitalisation valuation of commercial and income-producing property, institutional commercial valuation; this skill targets residential comparable-transactions work
- Expropriation and compensation for expropriated land, its own statutory scheme and forums
- Compensation where a plan reduces property value, the mirror mechanism to the levy, with a different claim route; deliberately excluded to keep the skill's scope on the levy and the bank appraisal
- Percentage figures for urban-renewal levy variants beyond the seismic-strengthening rate recorded in evidence.json, the secondary sources reviewed during research disagreed with each other and none was confirmed against the statute, so no figure is stated rather than a plausible guess

## Authoritative sources

- https://www.kolzchut.org.il/he/היטל_השבחה, rate, triggering events, payment timing, cutoff date, who is liable
- https://www.kolzchut.org.il/he/פטור_מהיטל_השבחה, the exemption list, area limits, occupancy condition, seismic-strengthening rate, request deadline
- https://www.kolzchut.org.il/he/השגה_על_היטל_השבחה, forum split, deadlines, procedure, appeal chain
- https://www.nevo.co.il/law_html/law01/500_077.htm, deciding and advisory appraiser fee regulations: band table, floor, ceiling, VAT, cost split
- https://www.boi.org.il/media/brep4lzt/329_12.pdf, Directive 329: loan-to-value caps, repayment-to-income cap, measurement basis
- https://www.gov.il/BlobFolder/dynamiccollectorresultitem/assessor-standardization-db_19/he/land_assessor_shameim_19.pdf, Standard 19: conservative valuation for credit collateral. Read with pdftotext, the text layer does not survive a plain fetch
- https://www.gov.il/he/departments/topics/land_assessor/govil-landing-page, Land Appraisers Council: licensing, registers, complaints. Blocks automated fetching, open in a browser
- חוק התכנון והבנייה, התוספת השלישית, the primary statute behind the levy. Read directly before changing any levy figure in this skill
