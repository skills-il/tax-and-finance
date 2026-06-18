---
name: israeli-startup-investment-analyzer
description: "Generate a structured investment memo for an Israeli startup deal: market, team, metrics sanity-check, valuation and dilution math, key risks, and a prioritized list of diligence questions. Built for angel and VC investors evaluating an inbound deck or data room. Catches Israel-specific landmines a generic analysis misses: Innovation Authority (rashut hachadshanut) grant overhang and IP-out restrictions, the Delaware flip, Section 102 option plans, founder vesting, and Companies Registrar standing. Use when an investor asks to evaluate a startup, screen a deal, review a pitch deck, write an investment memo, run dilution math, or list diligence questions. Why it matters: an Innovation Authority royalty or IP-out overhang can shrink or block an exit. Do NOT use for founder-side company formation or fundraising (israeli-startup-toolkit), employee option taxation (israeli-stock-options-tax), or public-market TASE stock analysis (tase-stock-analysis)."
license: MIT
compatibility: No network required. The Israeli figures are embedded; the optional MCP servers add live market and registry data when available.
---

# Israeli Startup Investment Analyzer

## Problem
Angel and VC investors get a flood of inbound decks and have minutes to decide which deals deserve a call. A generic read of a pitch deck misses two things at once: the inflated or undefined metrics that hide a weak business, and the Israel-specific legal landmines (an Innovation Authority grant that restricts moving IP abroad, a half-done Delaware flip, a broken Section 102 option plan) that can shrink or kill an exit long after the money goes in. This skill turns a deck or data-room summary into a sharp, sendable investment memo and a prioritized diligence list, with the Israeli specifics checked.

## Instructions

You produce an **investment memo** plus a **prioritized diligence question list** for an investor evaluating an Israeli startup. You do not give a buy/sell verdict the investor must own that, but you give them the structured judgment and the questions that get them there fast.

### Step 1: Establish the investor context and what you were given

Ask (or infer) two things before writing:
- **Who is the investor?** An angel writing a small personal check screens differently from a fund running formal diligence. Match the depth: a screening memo for a first look, a full pre-term-sheet memo when they are serious.
- **What material exists?** A one-pager, a full deck, a data room, or just notes from a call. Write only from what you were given. Mark everything you could not verify as an open question; never invent a metric, a valuation, or a grant balance to fill a gap.

### Step 2: Build the memo

Follow `references/investment-memo-template.md`. Lead with the verdict and the single biggest reason, then the evidence. Cover, in order:

1. **One-line summary and verdict** (PURSUE / PASS / NEEDS MORE).
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
- Priced round: `python3 scripts/cap_table_math.py priced --pre <pre> --invest <amount> --pool-pct <pool>` gives post-money, the investor's stake, and the dilution on existing holders. Watch whether the option-pool top-up is taken pre-money (founders absorb it) or post-money.
- SAFE / convertible: `python3 scripts/cap_table_math.py safe --safe <amount> --cap <cap> --discount <pct> --price-pre <pre>` (add `--post-money` for a YC-style post-money SAFE). Stacked SAFEs converting together can dilute far more than the deck implies.
- Pro-rata: `python3 scripts/cap_table_math.py prorata --owned-pct <pct> --pre <pre> --invest <amount>`.

The script computes ownership arithmetic only. Beyond the math, judge the deal terms (`references/investment-memo-template.md` section 7 has the full list):

- **Economics.** Liquidation preference is the term that most often turns a good headline exit into little for late money: distinguish 1x non-participating (the seed norm) from participating or a multiple, and add up the full preference stack from prior rounds. Anti-dilution: broad-based weighted-average is standard; full ratchet is a red flag.
- **Control.** Board composition (founder / investor / independent split) and the protective / veto provisions are where real control sits at seed even with a minority stake. Check pro-rata, drag-along (can force the investor into a sale), tag-along / co-sale, and ROFR.

### Step 5: Run the Israel-specific due diligence

This is the differentiator. Work through `references/israeli-dd-landmines.md` and summarize findings in the memo:

- **Innovation Authority (IIA) grant overhang.** If the company took IIA grants, they repay royalties of 3% to 5% of revenue until the grant plus SOFR-based interest is repaid, the funded R&D must stay in Israel, and moving the funded know-how abroad needs IIA approval plus a repayment capped at 6 times the grants plus interest (3 times if R&D jobs stay in Israel for three years). Relocating manufacturing abroad also needs approval and raises the liability (up to 1.5 times the funding). This can shrink or block a US acquisition or a flip. Ask for the outstanding balance and model it against the expected exit.
- **Corporate structure / Delaware flip.** Single Israeli Ltd or flipped to a Delaware HoldCo + Israeli OpCo? A flip is a transfer of shares by the shareholders, so the tax falls on them: Israeli individuals pay 25% capital gains (30% for a 10% or more holder), plus surtax. Do not quote the 23% corporate rate as the flip tax (that only applies when a company holds the shares). Confirm the flip used Israel's tax-deferred share-for-share rollover with a Tax Authority pre-ruling, that the core IP stays in the Israeli OpCo, and remember a flip on top of IIA grants is a double landmine.
- **Section 102 option plan.** Healthy plans use the capital-gains track with a trustee (flat 25% plus surtax to the employee, 24-month holding from grant). Note part of the gain can still be ordinary employment income, so it is not uniformly 25%. Check pool health and whether any grants fall outside the rules.
- **Cap table, IP assignment, and company standing.** Founder vesting / reverse vesting present? Fully-diluted cap table including all SAFEs? Did every founder, employee, and contractor sign an IP-assignment agreement (unassigned IP or an open employee service-invention claim undermines the asset)? Pull the company's official Companies Registrar (רשם החברות) extract to confirm it is active, not a "violating company" (חברה מפרה), and check for registered charges / liens (the `israel-amutot` MCP covers non-profits only, so it cannot do this for-profit check).
- **Other liabilities.** Flag accrued labor liabilities (severance, pension, study fund) and, for data-heavy startups, Privacy Protection Law Amendment 13 exposure.
- **Tax status.** If a reduced rate is claimed (Preferred Technological Enterprise 7.5% in area A / 12% elsewhere; Preferred Enterprise 7.5% / 16%), treat it as a diligence item to verify, not a given.

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
- **Confusing founder-side and investor-side framing.** This skill evaluates a deal for an investor. Do not slip into advising the founder how to raise or how to set up their 102 plan. That is `israeli-startup-toolkit`.
- **Doing dilution math in your head.** Pre-money pool shuffles and stacked post-money SAFEs are counterintuitive. Use the script; do not eyeball the ownership table.
- **Over-asking in diligence.** Sending 40 generic questions signals a tourist. The output must be a focused list that resolves the top 5 risks for this specific deal.
- **Stating Israeli tax/legal figures as advice.** Rates and rules (corporate tax, Preferred Enterprise, 102 conditions) change and depend on facts. Present them as screening signals to verify with an Israeli professional, never as binding conclusions.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Israel Innovation Authority, Royalties and IP | https://innovationisrael.org.il/en/royalties-intellectual-property/ | Grant royalty rate (3% to 5%), know-how transfer approval and repayment cap (6x / 3x) |
| Herzog Law, IIA manufacturing-abroad rules | https://herzoglaw.co.il/en/news-and-insights/the-israel-innovation-authority-iia-new-rules-regarding-transfer-of-manufacturing-outside-of-israel-and-the-interest-rate-on-iia-funding/ | Manufacturing-abroad liability (1.5x) and the SOFR-based interest rate |
| RNC, Employee stock options in Israel | https://www.rnc.co.il/employee-stock-options-israel/ | Section 102 capital-gains track: 25% rate, trustee, 24-month holding |
| PwC Tax Summaries, Israel income determination | https://taxsummaries.pwc.com/israel/corporate/income-determination | Corporate tax rate (23%) and capital gains treatment for companies |
| PwC Tax Summaries, Israel incentives | https://taxsummaries.pwc.com/israel/corporate/tax-credits-and-incentives | Preferred / Preferred Technological Enterprise reduced rates |
| Meitar, ITA SAFE guidelines | https://meitar.com/en/media/ita-guidelines-regarding-the-tax-implications-of-safe-investments/ | SAFE treated as advance for shares; conversion not a taxable event |

## Troubleshooting

- **The investor only gave a one-line idea, not a deck.** Produce a thin screening memo from what exists, and make the diligence questions the main deliverable: the questions that would let them decide whether to take a first call.
- **The numbers in the deck contradict each other.** Do not reconcile them silently. Surface the contradiction as a red flag and a diligence question.
- **No IIA / structure information is given.** Do not assume there is no exposure. List the IIA, flip, and 102 checks as open diligence items the investor must confirm before a term sheet.
- **The investor wants a valuation.** This skill sanity-checks a proposed valuation and its dilution math; it does not produce an independent valuation. Frame the output as "is this price reasonable for this stage and traction", not "the company is worth X".
