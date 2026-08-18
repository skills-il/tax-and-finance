# Domain Coverage Checklist, israeli-company-valuation

Generated: 2026-08-03. This file is the coverage contract the skill is judged against, at creation and on every future update. Figures live in `evidence.json`, not here, so this file stays gate-safe.

## Must cover (core)

- [ ] Three approaches and which one governs: income (DCF), market (multiples), asset/NAV. DCF primary for a going concern, NAV for asset-heavy, holding, or loss-making entities, multiples as a cross-check.
- [ ] FCFF build: EBIT, less tax on EBIT at the company's own effective Israeli rate, plus D&A, less capex, less change in working capital.
- [ ] Enterprise value to equity value bridge: less net financial debt, plus non-operating and surplus assets, less contingent liabilities and any severance provision shortfall.
- [ ] Israeli corporate tax rate, FULL category set. Standard rate; the closely-held service-company regime and the excess-profitability rule; Preferred Enterprise; Special Preferred Enterprise; Preferred Technology Enterprise; Special Preferred Technology Enterprise; each split by development area A versus rest of country where the law splits it; and the minimum top-up tax for large multinational groups. Source of every rate: evidence.json.
- [ ] Effective versus statutory rate across the forecast horizon and into terminal value, including the eligibility conditions that could break a preferred status.
- [ ] Dividend withholding by regime, since profit extraction is what the owner actually nets.
- [ ] Risk-free rate: named instrument (nominal shekel government bond, non-index-linked), maturity matched to the horizon, index-linked bond instead if modelling in real terms. Must be fetched live, never carried from memory.
- [ ] Bank of Israel policy rate treated as a DISTINCT input from the bond yield, not a substitute for it.
- [ ] Equity risk premium and Israel country risk premium, with the sovereign rating that drives them and the vintage date of the dataset.
- [ ] The no-double-count rule: a country-inclusive total ERP already contains the country premium, so adding the country premium again on top is a double count.
- [ ] Cost of equity build-up, full component set: risk-free, beta times ERP, country premium subject to the no-double-count rule, size premium, company-specific premium.
- [ ] Beta unlevering and relevering, with the relever step using the subject's Israeli effective rate.
- [ ] Size premium: mechanism, why an Israeli private company sits below the smallest listed decile, and the requirement to cite the empirical dataset used. No Israeli-specific published size study exists; say so.
- [ ] Marketability discount (DLOM): mechanism, the qualitative factors that place a company inside a range, and the hard requirement to name the empirical study relied on. No Israeli regulator publishes a mandated or safe-harbour range; say so rather than asserting a number.
- [ ] Control discount (DLOC) and its mirror the control premium: apply only to a genuinely non-controlling interest, and never stack with DLOM without separate justification for each.
- [ ] Cost of debt and the tax shield, using the SAME effective rate as the FCFF tax line.
- [ ] WACC weights: target versus actual structure, market-value weights and the resulting circularity, and a statement of which basis was used.
- [ ] Terminal value: Gordon growth versus exit multiple, growth strictly below WACC, growth consistent with the inflation basis of the cash flows.
- [ ] Nominal versus real consistency: nominal cash flows need a nominal bond yield, real cash flows need an index-linked bond.
- [ ] Market multiples, enumerated: EV/EBITDA, EV/EBIT, EV/Sales, P/E, P/B, plus sector-specific ones. Must state whether comparables are Israeli or global.
- [ ] Multiple consistency rule: enterprise numerator pairs only with a pre-interest denominator, equity numerator only with a post-interest denominator.
- [ ] Normalization adjustments specific to Israeli owner-managed companies: owner salary versus market, related-party rent, private expenses in the company, war-period effects since October 2023, and grant income.
- [ ] Retained-earnings and trapped-profits regime for a closely held company, and its effect on both the cash flows and the treatment of surplus cash.
- [ ] Section 104 reorganizations: what the valuation is FOR (fixing the share allocation ratio and the carried-over original cost), the existence of post-transfer holding and continuity conditions, and the consequence of breaching them.
- [ ] Who may sign. Israel has no statutory licence for a business valuer; acceptance turns on the signer's professional standing, independence, and documentation quality. Do not imply a credential that does not exist.
- [ ] What a valuation must document to survive review: valuation date, purpose and intended user, standard of value, method and why, every material assumption, the source AND date of each market parameter, sensitivity analysis, and the valuer's identity and independence.
- [ ] The advance tax ruling route as the actual acceptance mechanism for non-trivial reorganizations and related-party transfers.
- [ ] Transfer pricing where the transfer is cross-border or between related parties: arm's length requirement plus documentation.
- [ ] Explicit scope limit in EVERY output: indicative range only, not a signed opinion admissible to the tax authority, a court, or financial statements.
- [ ] Output as a RANGE with a sensitivity grid across WACC, terminal growth, and the marketability discount. Never a single point estimate.

- [ ] Governing documents FIRST when a real transaction is behind the question: shareholders' agreement and articles, pre-agreed valuation formula, right of first refusal, BMBY, tag-along and drag-along, veto and reserved-matter rights, pre-emption.
- [ ] The denominator: issued-and-outstanding versus fully diluted (option pool, warrants, SAFEs, convertibles), and multiple share classes routing to the allocation waterfall before any per-share figure.
- [ ] Levels of value ladder (control, marketable minority, non-marketable minority), what confers control in an Israeli company, and the control-consolidating buyer case where a discount is inappropriate and a premium is arguable.
- [ ] The range is PRE-TAX to the seller: capital gains rate, the higher substantial-shareholder rate, surtax layers, and the original cost basis. Do not compute the tax here, but never let the user treat the range as net.
- [ ] The sale's own duties: reporting with a short clock, an advance payment, withholding at source absent a certificate, and updating the shareholder register with the Registrar of Companies. Name the duty and the clock without inventing form numbers.
- [ ] Domestic related-party status of a sale between existing shareholders, the recharacterisation risk, the Companies Law personal-interest approval track, and the advance ruling route for plain related-party transfers, not only for reorganizations.
- [ ] Share sale versus asset sale as a structuring fork.
- [ ] Price mechanism versus value: locked box versus completion accounts, net-debt and working-capital adjustments, earn-outs discounted to present value, escrow, release of personal guarantees, and the seller's post-deal salary looping back into normalization.
- [ ] Prior transacted evidence in the same shares as the strongest single indicator of value.
- [ ] Terminal value BOTH ways: Gordon growth and exit multiple, compared against each other.
- [ ] Documentation set in the output: valuation date, purpose, INTENDED USER, standard of value, method and why, every material assumption, source and date of each parameter, sensitivity, and who prepared it and on what basis.

## Should cover (advanced / edge cases)

- [ ] Fair value for financial reporting versus market value for a tax filing: different standards of value, different answers.
- [ ] Purchase price allocation and intangible identification after an acquisition, including goodwill, for a buyer who will consolidate.
- [ ] Employee share option valuations and the underlying ordinary share fair value.
- [ ] Pre-revenue and venture-backed methods where DCF fails, plus the preferred versus ordinary allocation waterfall and liquidation preferences.
- [ ] Key-person dependency and customer concentration as a reasoned company-specific premium, not a round alpha.
- [ ] Real estate held inside an operating company, and when that reclassifies the company under a different tax regime entirely.
- [ ] Shareholder dispute, divorce, and estate valuations, where the standard of value and the admissibility of discounts differ.
- [ ] Post-October-2023 macro adjustments, and the danger of carrying a pre-war beta or country premium.
- [ ] Dataset refresh cadence: country risk and industry data refresh on a published schedule, so record which vintage was used.
- [ ] Cross-check discipline: reconcile DCF against multiples and against the NAV floor, and explain a material gap.

## Out of scope (explicit, with rationale)

- Producing a signed, filing-ready valuation opinion. No statutory valuer credential exists for an agent to hold, and the output is indicative only.
- Real estate appraisal. A separate licensed profession; the skill only flags when a property inside the company needs one.
- Listed-share valuation. Different disclosure regime; this skill targets private companies.
- Filing the reorganization notice or the ruling application. The skill prepares the supporting computation and points at the process; submission is the accountant's act.
- A full transfer pricing benchmarking study. Requires paid comparables databases the skill cannot reach.
- COMPUTING the seller's personal capital gains tax. The skill must WARN that the range is pre-tax and name the rates and surtax layers, then route to an accountant. It does not calculate the liability.
- Legal drafting of the share purchase or reorganization documents. The skill flags which provisions matter and sends the user to counsel.
- Pricing employee share options. The skill flags the interaction with a fresh valuation and routes to an accountant.
- Reproducing paywalled proprietary size-premium or discount tables. The skill teaches the sourcing discipline and never invents the table.

## Authoritative sources

See `evidence.json` for the URL, snippet, and fetch date behind every figure. Verify at each update:

- Israel Tax Authority, for the corporate rate, preferred-enterprise regimes, reorganization forms and deadlines, and current retained-earnings percentages.
- Bank of Israel, for the government bond yield curve (the risk-free rate) and the policy rate. Renders via JavaScript behind a bot check, so read it in a browser.
- Tel Aviv Stock Exchange, for government bond data and for Israeli comparable-company multiples.
- Damodaran NYU dataset, for the Israel country risk premium, equity risk premium, sovereign rating, industry betas and sector multiples. Refreshes in January and July; record the vintage.
- Central Bureau of Statistics, for CPI in the nominal versus real check.
