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

## Should cover (advanced / edge cases)
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
