# Domain Coverage Checklist

The coverage contract for this skill: the topics a real Israeli VC partner and a
startup lawyer expect an investment memo to address. A future update should diff
the skill against this list and flag any "Must cover" item that has gone missing.
Detailed figures and sources live in evidence.json and references/israeli-dd-landmines.md.

## Must cover (core)

### Generic investment-memo dimensions
- [ ] Memo structure and an explicit recommendation (pursue / pass / needs more) with conviction.
- [ ] Market sizing and timing: bottom-up TAM/SAM, why-now, flag top-down-only sizing.
- [ ] Team and founders: founder-market fit, track record, team completeness, key-person risk.
- [ ] Product and moat: what is built vs roadmap, defensibility (IP, data, network, switching cost).
- [ ] Traction and metrics sanity: ARR/MRR definition, growth with an absolute base, net revenue retention, gross margin, churn.
- [ ] Unit economics: CAC, LTV, LTV-to-CAC, CAC payback, Rule of 40, burn multiple.
- [ ] Burn and runway: months of runway, and whether the round funds to the next milestone.
- [ ] Business model and competition: revenue model, pricing, sales motion, landscape, differentiation.
- [ ] Valuation and dilution math: pre/post-money, round size, ownership reconciled to the cap table.
- [ ] Option pool sizing and the pre-money pool shuffle (who absorbs the dilution).
- [ ] Liquidation preference: non-participating vs participating, multiples, seniority stacking.
- [ ] Anti-dilution: full ratchet (red flag) vs weighted average.
- [ ] Board composition and protective/veto provisions (control).
- [ ] Pro-rata, drag-along, tag-along / co-sale, right of first refusal.
- [ ] Cap-table hygiene and dead equity, including stacked SAFEs.
- [ ] Founder vesting / reverse vesting.
- [ ] Financing history: prior rounds, instruments, prior valuations, carried-forward preferences.
- [ ] Legal DD taxonomy: corporate, capitalization, IP, employment, contracts, regulatory, litigation, tax, privacy.
- [ ] A prioritized, gap-driven diligence question list.

### Israel-specific landmines (the differentiator)
- [ ] Innovation Authority (IIA) grant royalty obligation and outstanding balance.
- [ ] IIA know-how / IP transfer restriction abroad and the redemption fee exposure.
- [ ] IIA manufacturing-in-Israel obligation and the increased liability for moving abroad.
- [ ] IIA change-of-control / exit consent as a closing condition.
- [ ] OpCo / HoldCo Delaware flip: present or planned, and its red flags.
- [ ] Flip tax exposure and whether it was done under a tax-deferral ruling.
- [ ] IP ownership location post-flip (must stay in the Israeli operating company, cleanly assigned).
- [ ] Section 102 employee option plan validity (capital-gains trustee track) and pool health.
- [ ] Companies Registrar standing (active vs "violating company").
- [ ] Employee-invention / IP-assignment compliance from every founder, employee, and contractor.
- [ ] Service-invention waiver: an express waiver referencing Patents Law sections 132 and 134, not just a signed IP assignment. Without it the Compensation and Royalties Committee can award an employee compensation on the core patents. *Cite:* Patents Law 5727-1967 ss.132, 134.
- [ ] IIA royalty rate determinants: which programme/track (R&D Fund, Tnufa, incubator, Magnet, BIRD/EUREKA), which grant years, whether an accelerated rate on manufacturing moved abroad has been triggered. A bare "3% to 5%" is not a coverage answer. *Cite:* IIA royalties page; Herzog IIA rules.
- [ ] Export control: whether the product is a controlled defence or dual-use item, DECA registration, and current marketing/export licences per market, under the Defense Export Control Law, 2007. Includes the post-repeal encryption regime (repeal in force 20 March 2025, export still licensed, legacy licences to 19 November 2026). *Cite:* DECA; Goldfarb Gross Seligman encryption-order repeal.
- [ ] Registrar of Pledges (רשם המשכונות) search by company number for floating charges over the IP, distinct from the Companies Registrar extract.
- [ ] Founder secondary in the round: size, price relative to the primary, and characterisation risk (share sale vs employment income).
- [ ] Non-compete enforceability: Israeli courts largely will not enforce absent a protectable interest, so non-competes are not key-person protection.

## Should cover (advanced / edge cases)
- [ ] Pillar Two global minimum tax interaction with Preferred/Preferred Technological Enterprise rates for a target inside a very large group.
- [ ] Israeli seed documentation conventions (IVCA-style Israeli-law SPA, Shareholders Agreement, and Articles) versus NVCA/Delaware assumptions, including that protective provisions sit in the public Articles.
- [ ] FX exposure: raising and reporting in USD while paying salaries in ILS changes the real runway.
- [ ] VAT leg of a SAFE where the instrument carries debt-like features or attached consideration.
- [ ] Reserve duty (מילואים) and war-related operational risk on delivery and key personnel.
- [ ] Preferred / Preferred Technological Enterprise reduced-tax status and its conditions.
- [ ] Preferred-income dividend withholding to a foreign parent.
- [ ] IP liens registered at the Israel Patent Office.
- [ ] Open-source and generative-AI provenance risk in the codebase.
- [ ] Flip tax-deferral unwind conditions (holding-period breach crystallizes the deferred tax).
- [ ] MNC intra-group know-how license route (license vs transfer).
- [ ] Israeli labor liabilities (severance, pension, study fund, contractor misclassification).
- [ ] Data privacy (Amendment 13) and cyber compliance.

## Out of scope (explicit)
- Founder-side company formation, incorporation, and fundraising prep. Handled by `israeli-startup-toolkit`.
- Employee-side personal taxation of Section 102 options. Handled by `israeli-stock-options-tax`.
- Public-company / TASE listed-equity analysis. Handled by `tase-stock-analysis`.
- Drafting or negotiating the actual term sheet, SPA, or legal instruments.
- Post-investment portfolio management, board reporting, and follow-on tracking.
- Tax filing or applying for a formal tax ruling.
