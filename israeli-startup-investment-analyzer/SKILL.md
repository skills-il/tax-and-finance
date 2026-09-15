---
name: israeli-startup-investment-analyzer
description: "Generate a structured investment memo for an Israeli startup deal: market, team, metrics sanity-check, valuation and dilution math, key risks, and a prioritized list of diligence questions. Built for angel and VC investors evaluating an inbound deck or data room. Catches Israel-specific landmines a generic analysis misses: Innovation Authority (rashut hachadshanut) grant overhang and IP-out restrictions, the Delaware flip, Section 102 option plans, founder vesting, and Companies Registrar standing. Use when an investor asks to evaluate a startup, screen a deal, review a pitch deck, write an investment memo, run dilution math, or list diligence questions. Why it matters: an Innovation Authority royalty or IP-out overhang can shrink or block an exit. Do NOT use for founder-side company formation or fundraising (israeli-startup-toolkit), employee option taxation (israeli-stock-options-tax), or public-market TASE stock analysis (tase-stock-analysis)."
license: MIT
compatibility: No network required. The Israeli figures are embedded; the optional MCP servers add live market and registry data when available.
---

# Israeli Startup Investment Analyzer

## Legal notice

This is a free information tool operated by an AI model. It gathers data that has been published to the public and presents it in an organised form. The operators of this tool hold no personal interest in the securities or financial assets it mentions, and receive no consideration, commission, or benefit of any kind for presenting them. All of its outputs are produced automatically by an AI model, with no involvement, review, or approval by a licensed investment adviser.

The output is not investment advice, not investment marketing, and not a recommendation to buy, sell, or hold any security or financial asset. It is not a substitute for advice that takes account of the particular circumstances and needs of each person, and it does not consider your financial position, your investment objectives, or the risk you are able to bear. Market data may be partial, delayed, or wrong, and an AI model may err, omit data, or present a wrong conclusion. Consult a licensed adviser before any investment decision and verify every figure against the official source. All use of its output is the user's sole responsibility.


## Problem
Angel and VC investors get a flood of inbound decks and have minutes to decide which deals deserve a call. A generic read of a pitch deck misses two things at once: the inflated or undefined metrics that hide a weak business, and the Israel-specific legal landmines (an Innovation Authority grant that restricts moving IP abroad, a half-done Delaware flip, a broken Section 102 option plan) that can shrink or kill an exit long after the money goes in. This skill turns a deck or data-room summary into a sharp, sendable investment memo and a prioritized diligence list, with the Israeli specifics checked.

## Instructions

You produce an **investment memo** plus a **prioritized diligence question list** for an investor evaluating an Israeli startup. You do not give a buy, pass, or invest verdict, a recommendation, or a conviction level on the deal. You organise what the material shows, what it does not show, and the questions that close the gaps; the decision stays with the investor and their licensed advisers.

### Step 1: Establish the investor context and what you were given

Ask (or infer) two things before writing:
- **Who is the investor?** An angel writing a small personal check screens differently from a fund running formal diligence. Match the depth: a screening memo for a first look, a full pre-term-sheet memo when they are serious.
- **What material exists?** A one-pager, a full deck, a data room, or just notes from a call. Write only from what you were given. Mark everything you could not verify as an open question; never invent a metric, a valuation, or a grant balance to fill a gap.

### Step 2: Build the memo

Follow `references/investment-memo-template.md`. Lead with a neutral summary of what the company does and the most important open issues, then the evidence. Cover, in order:

1. **One-line summary and key open issues** (what is established, what is unverified, and what must be confirmed before any decision; no verdict or recommendation).
2. **Market and timing** prefer a bottom-up TAM (buyers times realistic ACV); reject top-down sizing (the classic "small slice of a giant market").
3. **Team** domain fit, prior outcomes, gaps, and what to probe on the call.
4. **Product and moat** what is built vs roadmap, and what makes it defensible.
5. **Traction and metrics sanity check** this is where decks inflate. See Step 3.
6. **Deal terms and cap-table sanity** see Step 4.
7. **Israel-specific due diligence** see Step 5.
8. **Key risks and red flags** ranked; separate "diligence resolves this" from "thesis risk".
9. **Diligence questions** the sharp, short list from `references/diligence-questions.md`.

### Step 3: Pressure-test the metrics

Do not accept deck numbers at face value. The recurring inflations to catch:
- "ARR" that is really pipeline, LOIs, or one big month annualized. Ask for the exact definition.
- Growth shown as a percentage with no absolute base (a huge growth rate on a handful of customers).
- Burn and runway omitted, or runway quoted before the new raise is spent.
- Logos presented as customers when they are pilots or design partners.
- Missing the unit economics: gross margin, net revenue retention, churn, CAC payback, burn multiple.

State which numbers you could verify, which you could not, and which look internally inconsistent.

### Step 4: Sanity-check valuation, dilution, and the cap table

Use `scripts/cap_table_math.py` to check the arithmetic:
- Priced round: `priced --pre <pre> --invest <amount> --pool-pct <pool> --pool-timing pre|post`. The `--pool-timing` flag is the point: `pre` is the standard "pool shuffle" where existing holders absorb the whole pool, `post` spreads it over the investor too. Run both and show the investor the difference.
- SAFE / convertible: `safe --safe <amount> --cap <cap> --discount <pct> --price-pre <pre>` (add `--post-money` for a YC-style post-money SAFE, where the cap sets ownership directly and a discount does not stack).
- Stacked SAFEs: `stacked --price-pre <pre> --invest <amount> --safe <amt>:<cap>:<disc> --safe <amt>:<cap> --pool-pct <pool>`. Repeat `--safe` once per outstanding instrument. The script treats every SAFE as a pre-money SAFE converting on top of the pre-money; for a post-money SAFE, or SAFEs converting inside the pre-money, use the manual steps below instead. Reading each SAFE alone against the same pre-money understates total dilution, which is exactly what the deck's ownership table usually does.
- Pro-rata: `prorata --owned-pct <pct> --pre <pre> --invest <amount> --pool-pct <pool>`. A naive pro-rata check leaves the investor short whenever a pre-money pool is created.

**No shell available (claude.ai, ChatGPT, Claude Desktop, Manus)?** Do the same arithmetic step by step and show every line so the investor can check it:
- Priced round, pool carved out of the pre-money: post = pre + invest; investor % = invest / post; pool % = the target pool; existing % = 100 minus both. Pool created post-money: investor % = (invest / post) x (1 minus pool fraction); existing % = 100 minus investor % minus pool %.
- Pre-money SAFE, read alone: effective valuation = the LOWER of the cap and pre x (1 minus discount); SAFE % before new money = SAFE amount / (effective valuation + SAFE amount).
- SAFEs plus the new round, in order (the script follows these steps for pre-money SAFEs only, and every step assumes the SAFEs convert ON TOP of the pre-money):
  1. Treat the pre-money as 100 notional shares held by existing holders, so one share costs pre / 100.
  2. Each pre-money SAFE buys amount / (share price x factor) shares, where factor = the LOWER of cap / pre and (1 minus discount).
  3. Post-money SAFEs are different: add up s = the sum of amount / cap across them; together they receive (100 + the pre-money SAFE shares from step 2) x s / (1 minus s) shares, so they hold s of the company right after all the SAFEs convert. This follows the YC post-money SAFE convention, where the cap counts the other converting SAFEs; check the definition in any non-YC instrument. A discount does not stack on a post-money cap.
  4. New money buys invest / share price shares.
  5. Subtotal = 100 + all SAFE shares + new-money shares.
  6. Pool of fraction p: a pre-money pool takes p x subtotal shares out of the existing holders' 100 without adding shares (total = subtotal); a post-money pool adds shares so total = subtotal / (1 minus p).
  7. Divide every holding by the total. Never read each SAFE alone against the same pre-money.
  If the term sheet instead converts the SAFEs INSIDE the pre-money, the new investor keeps invest / post and the SAFE shares come out of the existing holders; say which assumption you used.
- Worked example (the shape of a common Israeli seed): 10,000,000 pre, 2,000,000 new money, one prior pre-money SAFE of 500,000 at an 8,000,000 cap and 20% discount, 10% pre-money pool. Share price 100,000; factor = lower of 0.8 and 0.8 = 0.8, so the SAFE buys 6.25 shares; new money buys 20; subtotal 126.25; the pool takes 12.625 from existing holders. Result: existing 69.21%, SAFE 4.95%, new money 15.84%, pool 10%. Converting inside the pre-money would instead leave the new money at 16.67%.
- Pro-rata with a pool: let f = invest / post and p = the pool fraction. Pre-money pool: sitting out leaves you at your % x (1 minus f minus p); to hold your %, invest your % x (f + p) x post. Post-money pool: sitting out leaves you at your % x (1 minus f) x (1 minus p); to hold your %, invest post x (your % / (1 minus p) minus your % x (1 minus f)). Neither is your % x the round size, and both ignore SAFEs converting in the same round; with SAFEs, work out your diluted stake with the steps above first.

The script, and the manual route above, compute ownership only. They do not model the preference stack or the exit waterfall, so walk those through by hand using the memo template. Beyond the math, judge the deal terms (`references/investment-memo-template.md` section 7 has the full list):

- **Economics.** Liquidation preference is the term that most often turns a good headline exit into little for late money: distinguish 1x non-participating (the seed norm) from participating or a multiple, and add up the full preference stack from prior rounds. Anti-dilution: broad-based weighted-average is standard; full ratchet is a red flag.
- **Control.** Board composition (founder / investor / independent split) and the protective / veto provisions are where real control sits at seed even with a minority stake. Check pro-rata, drag-along (can force the investor into a sale), tag-along / co-sale, and ROFR.

### Step 5: Run the Israel-specific due diligence

This is the differentiator. Work through `references/israeli-dd-landmines.md` and summarize findings in the memo:

- **Innovation Authority (IIA) grant overhang.** If the company took IIA grants, they repay royalties of 3% to 5% of revenue until the grant plus interest is repaid, and the funded R&D must stay in Israel. Do not stop at the "3% to 5%" band, ask which rate and which programme actually apply: the applicable rate within that band depends on the programme and the company's circumstances, and revenue tied to manufacturing moved abroad carries an increased rate. Tracks differ materially (Tnufa, incubator, Magnet consortia, and bi-national funds such as BIRD and EUREKA each run on their own terms), so ask for the programme name, the grant years, and the outstanding balance rather than a single percentage. Interest is not plain SOFR: for files approved from 2024 it is the higher of the annual SOFR-based rate plus 1% or a 4% floor, so the balance keeps compounding even when rates fall. (The SOFR spread is reset periodically by the IIA, so read the current rate off the IIA notice rather than assuming last year's.)
  - **Moving know-how abroad** needs IIA approval plus a repayment capped at 6 times the grants plus interest, reduced to 3 times if the acquirer commits to keep the company's R&D jobs in Israel for at least three years. There is also a floor: the minimum repayment is the total IIA investment plus interest less royalties already paid, which is the binding number for a company with a small grant and little revenue.
  - **Relocating manufacturing abroad** needs IIA approval, though no approval is required below 10% of the manufacturing (notify the IIA, which is deemed to agree if it does not refuse within 30 days). Under the rules for funding applications submitted after 25 October 2023 there is no increase in the royalty liability for moving up to 25% of the manufacturing, and the maximum increased liability is now 1.5 times the funding plus interest, down from 3 times. Moving manufacturing can also raise the royalty rate itself, so ask about both the liability and the rate.
  - **Change of control.** An IIA-funded company generally needs to notify or obtain IIA consent on a change of control, and a foreign acquirer must undertake to honour the grant obligations. Confirm this is a closing condition and not an afterthought.
- **Export control (the most commonly missed item in Israeli deep-tech DD).** If the product is defence, dual-use, cyber, RF, drone, or surveillance adjacent, it may be a controlled item. The company then needs registration and per-transaction marketing and export licences under the Defense Export Control Law, 2007 (administered by DECA at the Ministry of Defense) or dual-use licensing via the Ministry of Economy. Selling without a licence is a criminal offence and makes the reported revenue unlicensable, which an acquirer will discount to zero. Note the 1974 Encryption Order was revoked by an order published in the official gazette (Reshumot) on 20 November 2025, in force from 21 March 2026. Engagement in encryption items other than export, and items outside the Wassenaar dual-use list, no longer need an encryption licence, but EXPORT of controlled encryption items still does: exports for defence use are supervised by DECA at the Ministry of Defense, and exports for any other use by the Export Control Agency (ECA) at the Ministry of Economy and Industry. A licence issued under the old order and valid on the commencement date stays in force until its own expiry or eight months after commencement, whichever is later, so legacy licences start lapsing on 21 November 2026. So an "encryption licence on file" answer may be about to lapse, and an old exemption memo may describe a regime that no longer exists. Ask directly: what is your classification, who issued it, and do you hold current licences for every market you sell into?
- **Corporate structure / Delaware flip.** Single Israeli Ltd or flipped to a Delaware HoldCo + Israeli OpCo? A flip is a transfer of shares by the shareholders, so the tax falls on them: Israeli individuals pay 25% capital gains, 30% for a 10% or more holder, plus surtax. Surtax is now two layers, not one: a 3% surtax on taxable income above the annual threshold (NIS 721,560 in 2026), plus an additional 2% surtax on income from capital sources over the same threshold. Capital gains therefore carry up to 5% surtax in total, not the single 3% layer older memos assume, so model a substantial holder's flip gain at the 30% rate plus up to 5% surtax. Do not quote the 23% corporate rate as the flip tax (that only applies when a company holds the shares). Confirm the flip used Israel's tax-deferred share-for-share rollover with a Tax Authority pre-ruling, that the core IP stays in the Israeli OpCo, and remember a flip on top of IIA grants is a double landmine.
- **Section 102 option plan.** Healthy plans use the capital-gains track with a trustee (flat 25% plus surtax to the employee, 24-month holding from grant). Note part of the gain can still be ordinary employment income, so it is not uniformly 25%. New Section 102 rules on plan approval and reporting to the Tax Authority came into effect on 1 January 2025, so ask to see the plan's filing and approval under the rules that applied when it was adopted, not just the plan document. Check who is INELIGIBLE for 102: the section is reserved for employees and office holders, so options granted to consultants, advisors, and independent contractors are taxed by default under Section 3(i), which is the most common finding after the trustee question on a seed cap table with advisor and contractor grants. Also confirm whether founder reverse-vesting and employee options carry single or double-trigger acceleration on a change of control, since that determines what an acquirer inherits. Check pool health, whether any grants fall outside the rules, and what happens to unvested or under-24-month options on an acquisition (a fast exit can push the whole employee pool to marginal rates, which is a retention risk in the deal being priced).
- **Cap table, IP assignment, and company standing.**
  - Founder vesting / reverse vesting present? Fully-diluted cap table including every outstanding SAFE? Any founder secondary in this round, at what price relative to the primary, and is it characterised as a share sale or at risk of being recharacterised as employment income?
  - Did every founder, employee, and contractor sign an IP-assignment agreement? A signed assignment alone does not close the issue: under the Patents Law an employee can claim compensation for a **service invention** (sections 132 and 134) before the Compensation and Royalties Committee unless the agreement contains an express waiver of that right. This is the classic finding that a clean-looking PIIAA does not cure, so read the actual waiver language.
  - Pull the company's official Companies Registrar (רשם החברות) extract by its company number to confirm it is active and not a "violating company" (חברה מפרה), which can bar filings and accrue penalties. Separately search the Registrar of Pledges (רשם המשכונות) by the same number for registered charges, including any floating charge over the IP, since the Companies Registrar extract alone may not show them. The `israel-amutot` MCP covers non-profits only, so it cannot do either check.
  - Do not assume a signed non-compete is key-person protection. Israeli enforceability turns on whether the employer has a protectable interest and is frequently litigated, so treat a non-compete as a question for counsel rather than cover you can bank on. The durable protection is the IP assignment plus trade-secret law.
- **Other liabilities.** Flag accrued labour liabilities (severance, pension, study fund) and, for data-heavy startups, Privacy Protection Law Amendment 13 exposure.
- **Tax status.** If a reduced rate is claimed (Preferred Technological Enterprise 7.5% in development area A / 12% elsewhere, or 6% for a Special Preferred Technological Enterprise in a very large group; Preferred Enterprise 7.5% / 16%), treat it as a diligence item to verify, not a given. For a target that would sit inside a large multinational group, note that the OECD Pillar Two global minimum-tax rules are now shaping Israeli policy (Israel legislated a new R&D tax credit for tax years from 1 January 2026 in response), so a headline 7.5% or 12% Israeli rate inside a very large multinational group can be topped up after an acquisition and should not be modelled as permanent.
- **Investor tax benefits (check eligibility before closing).** The Angels Law benefit for private investors in qualifying R&D companies (a temporary provision under the Law for the Encouragement of Knowledge-Intensive Industry) was extended to 31 December 2026, so a round closing this year may still qualify, but only if the company and the investment meet its conditions; ask whether the company holds the required status and have an accountant confirm before signing. Separately, do not rely on summaries that describe section 92A as a capital-gains rollover for startup investors. In the Ordinance text, section 92A lets an investment of up to NIS 5 million in an R&D company count as a capital loss, but only for money paid in a public offering on the Tel Aviv Stock Exchange by a company with a market value between NIS 200 million and NIS 1 billion, so it does not fit a private seed round; confirm any claimed investor tax benefit with an accountant.
- **SAFE tax window.** Under the Tax Authority's updated SAFE guidance, SAFEs signed between 1 January 2025 and 31 December 2026 that meet its conditions keep the advance-for-shares treatment, and the allowed SAFE investment was raised from NIS 40 million to USD 20 million. Check the signing date and amount; a SAFE outside that window or above the cap needs its own tax analysis.
- **Israeli deal mechanics and operating risks.** Before running Step 4, identify which SAFE template was used (an Israeli-law SAFE or a US template), whether its cap is pre- or post-money, and whether it converts inside or on top of the new pre-money. In an Israeli Ltd, pre-emptive rights, information rights and protective provisions usually sit in the Articles and the shareholders' agreement, so an angel who signs only a SAFE may hold few of them; ask what rights you actually get. Add four operating questions: how much of the burn is in shekels while the raise is in dollars (currency moves change real runway), which key people serve in reserve duty and what the continuity plan is, whether any customer, reseller or end user sits in a sanctioned jurisdiction, and, for an IIA-funded company, whether its periodic reports to the Authority are current. If a flip used the tax-deferred rollover, read the conditions in the ruling itself rather than assuming the deferral is safe.

### Step 6: Deliver

Output the memo as clean, sendable markdown the investor can paste into their notes or forward to a partner. End with the prioritized diligence questions (5 to 10, not 40) that resolve the top risks. Always add: the Israeli legal and tax specifics here are screening signals, not advice, and binding decisions need an Israeli lawyer and accountant.

## Recommended MCP Servers

These add live data when the investor wants to go deeper. They are optional; the skill works without them.

| MCP | Use in this skill |
|-----|-------------------|
| `tase-mcp` | Maya company filings and TA-35 / TA-125 data for public comparables when sanity-checking a later-stage valuation. |
| `israeli-cbs` / `israel-statistics` | Central Bureau of Statistics economic data for bottom-up market sizing and macro context. |
| `israel-amutot` | Corporations Authority registry lookups for non-profits and public-benefit companies. It does NOT cover for-profit companies, so for a startup's standing pull the official Companies Registrar extract directly instead. |

## Bundled Resources

| File | Purpose |
|------|---------|
| `references/investment-memo-template.md` | The 11-section memo structure the skill produces. |
| `references/israeli-dd-landmines.md` | The Israel-specific diligence checklist (IIA, flip, 102, registrar, tax status), every figure sourced. |
| `references/diligence-questions.md` | The diligence question bank to draw the prioritized short list from. |
| `references/domain-checklist.md` | Coverage checklist the memo is judged against. |
| `scripts/cap_table_math.py` | Priced-round dilution, SAFE/convertible conversion, and pro-rata math. |

## Gotchas

Agent failure modes specific to this domain:

- **Treating the deck as truth.** The most common error is restating the founder's "ARR" and "growth" as facts. Always interrogate the metric definitions and label what is unverified. A memo that launders deck spin is worse than no memo.
- **Ignoring IIA exposure because the grant looks like "free money".** The grant is the easy part; the royalty balance and the IP-out restriction are what bite at exit. If the company is deep-tech or took early grants, assume IIA exposure until shown otherwise.
- **Quoting "3% to 5%" as if it were the whole IIA royalty rule.** That band is a summary, not a rate table. Without the programme name, the grant years, and whether an accelerated rate has been triggered, the exposure cannot be modelled. Ask for those three things.
- **Skipping export control on a cyber or deep-tech deal.** Agents read the deck's product description and never think to ask whether selling it needs a DECA or dual-use licence. For the modal Israeli deep-tech seed deal this is the single most deal-relevant regulatory question, and unlicensed revenue is worth nothing to an acquirer.
- **Treating a signed IP-assignment agreement as closing the IP question.** It does not close a service-invention claim under the Patents Law unless there is an express waiver. Read the clause, do not tick the box.
- **Confusing founder-side and investor-side framing.** This skill evaluates a deal for an investor. Do not slip into advising the founder how to raise or how to set up their 102 plan. That is `israeli-startup-toolkit`.
- **Doing dilution math in your head.** Pre-money pool shuffles and stacked post-money SAFEs are counterintuitive. Use the script where a shell exists; otherwise write out the Step 4 manual formulas line by line. Never eyeball the ownership table.
- **Over-asking in diligence.** Sending 40 generic questions signals a tourist. The output must be a focused list that resolves the top 5 risks for this specific deal.
- **Stating Israeli tax/legal figures as advice.** Rates and rules (corporate tax, Preferred Enterprise, 102 conditions) change and depend on facts. Present them as screening signals to verify with an Israeli professional, never as binding conclusions.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Israel Innovation Authority, Royalties and IP | https://innovationisrael.org.il/en/royalties-intellectual-property/ | Which royalty rate and programme track apply, know-how transfer approval, repayment floor and cap (6x / 3x) |
| Herzog Law, IIA manufacturing-abroad rules | https://herzoglaw.co.il/en/news-and-insights/the-israel-innovation-authority-iia-new-rules-regarding-transfer-of-manufacturing-outside-of-israel-and-the-interest-rate-on-iia-funding/ | Manufacturing-abroad liability (1.5x) and the SOFR-based interest rate |
| RNC, Employee stock options in Israel | https://www.rnc.co.il/employee-stock-options-israel/ | Section 102 capital-gains track: 25% rate, trustee, 24-month holding |
| PwC Tax Summaries, Israel income determination | https://taxsummaries.pwc.com/israel/corporate/income-determination | Corporate tax rate (23%) and capital gains treatment for companies |
| PwC Tax Summaries, Israel taxes on personal income | https://taxsummaries.pwc.com/israel/individual/taxes-on-personal-income | Surtax: 3% general plus an additional 2% on capital-source income, threshold NIS 721,560 (2026) |
| DECA, Defense Export Controls Agency (Ministry of Defense) | https://exportctrl.mod.gov.il/en | Whether the product is a controlled item, registration and marketing/export licence requirements |
| Reshumot, Encryption Order revocation (Kovetz Takanot 12093) | https://www.law.co.il/media/computer-law/use_of_encryption_means_declaration_revocation_2025.pdf | Published 20.11.2025, commencement four months later, legacy licences to expiry or eight months after commencement |
| Shibolet, revocation of the Encryption Order | https://www.shibolet.com/en/revocation-of-the-encryption-order/ | Plain-English summary of the March 2026 commencement and transition rules |
| Herzog, updated ITA SAFE guidance | https://herzoglaw.co.il/en/news-and-insights/the-ita-publishes-an-updated-version-of-its-guidance-and-safe-harbor-for-safes/ | SAFEs signed 1 Jan 2025 to 31 Dec 2026, cap raised to USD 20 million |
| Nevo, Angels Law (temporary provision) | https://www.nevo.co.il/law_html/law00/217877.htm | Temporary provision period ends 31 December 2026 |
| Nevo, Income Tax Ordinance (section 92A) | https://www.nevo.co.il/law_html/law01/255_001.htm | Capital-loss recognition up to NIS 5 million, TASE offering and market-value conditions |
| Nevo, Patents Law 5727-1967 (full Hebrew text) | https://www.nevo.co.il/law_html/law00/4539.htm | Service invention (section 132) and the Compensation and Royalties Committee (section 134) |
| Herzog, new and amended Section 102 rules | https://herzoglaw.co.il/en/news-and-insights/new-and-amended-102-rules/ | Mandatory online plan approval by the Tax Authority from 1 January 2025 |
| PwC Tax Summaries, Israel incentives | https://taxsummaries.pwc.com/israel/corporate/tax-credits-and-incentives | Preferred / Preferred Technological Enterprise reduced rates |
| Meitar, ITA SAFE guidelines | https://meitar.com/en/media/ita-guidelines-regarding-the-tax-implications-of-safe-investments/ | SAFE treated as advance for shares; conversion not a taxable event |

## Troubleshooting

- **The investor only gave a one-line idea, not a deck.** Produce a thin screening memo from what exists, and make the diligence questions the main deliverable: the questions that would let them decide whether to take a first call.
- **The numbers in the deck contradict each other.** Do not reconcile them silently. Surface the contradiction as a red flag and a diligence question.
- **No IIA / structure information is given.** Do not assume there is no exposure. List the IIA, flip, and 102 checks as open diligence items the investor must confirm before a term sheet.
- **The investor wants a valuation.** This skill sanity-checks a proposed valuation and its dilution math; it does not produce an independent valuation. Set the proposed terms beside the stated stage and traction, list what supports them and what undercuts them, and name what must be verified; do not conclude whether the price is reasonable or what the company is worth.
