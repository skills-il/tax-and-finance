---
name: israeli-corporate-tax-strategy
description: "Strategic tax analysis for Israeli company owners (baalei shlita) comparing salary, dividends, shareholder loans, and management fees as profit extraction methods. Use when user asks about paying personal tax from company funds, dividend vs salary comparison, shareholder loan tax implications, Section 3(tet) deemed interest, corporate profit extraction strategy, halokat dividendim, mashichat rvaachim, or baal shlita tax planning. Calculates total tax burden across methods, identifies optimal strategy based on assessment amount and company structure, and verifies compliance with Israeli Tax Authority rules. Prevents costly extraction mistakes by analyzing withholding, Bituach Leumi, surtax, and corporate tax interactions. Do NOT use for VAT reporting (use israeli-vat-reporting), payroll processing (use israeli-payroll-calculator), annual tax return filing (use israeli-tax-returns), or crypto tax (use israeli-crypto-tax-reporter)."
license: MIT
allowed-tools: Bash(python:*) WebFetch
compatibility: Works with Claude Code, OpenClaw, Cursor, Windsurf, Codex, GitHub Copilot, opencode, antigravity.
---

# Israeli Corporate Tax Strategy

## Legal notice

This is a free information tool operated by an AI model. It explains the rules and calculates from the figures you enter, but it does not examine your full circumstances and does not constitute tax advice. All of its outputs are produced automatically, with no involvement, review, or approval by a tax adviser or accountant, and an AI model may err, omit data, or present a wrong conclusion. The binding computation is the Tax Authority's and responsibility for reporting is yours. This tool is not a substitute for advice that takes account of the particular circumstances and needs of each person, and all use of its output is the user's sole responsibility.


## Problem

Israeli company owners (baalei shlita) face a critical decision whenever they need to extract profits or pay personal tax obligations: should they take a salary, distribute a dividend, use a shareholder loan, or pay management fees? Each method carries different tax rates, Bituach Leumi implications, and compliance requirements. Getting it wrong can cost tens of thousands of shekels in unnecessary tax, or worse, trigger Tax Authority scrutiny. Most business owners lack the specialized knowledge to model these scenarios accurately, and generic AI responses consistently get Israeli-specific rules wrong (especially Section 3(tet) deemed interest, controlling shareholder NI rates, and the surtax interaction with dividends).

## Instructions

### Step 1: Gather the User's Situation

Before any analysis, collect these details. Each variable significantly affects the optimal strategy:

| Variable | Why It Matters | What to Ask |
|----------|---------------|-------------|
| Company type | Tax rates and NI rules differ | "Is this a Chevra Baam (Ltd/baam)? Single-owner or multiple shareholders?" |
| Ownership percentage | Controlling shareholder (10%+) triggers higher dividend tax (30% vs 25%) and is the holding level at which Section 62A can catch a personal-services company | "What percentage of the company do you hold?" |
| Personal-services share | Section 62A (post-Amendment 277) attributes profits above 25% margin to the shareholder at marginal rates when income is primarily personal services to a single substantial client | "Does most company revenue come from your own services to one main client?" |
| Current salary from company | Determines marginal tax bracket and NI ceiling utilization | "What monthly salary do you currently draw from the company?" |
| Other income sources | Affects marginal rate and surtax threshold | "Do you have income from other sources (employment, rental, investments)?" |
| Amount needed | Strategy differs for 50K vs 500K vs 2M NIS | "How much do you need to extract, and is this a one-time or recurring need?" |
| Purpose | Tax assessment payment has specific timing constraints | "Is this for a tax assessment (shuma), personal expense, or regular income?" |
| Company profit level | Determines available retained earnings and trapped-profits exposure | "What is the company's approximate annual profit before this extraction?" |
| Accumulated retained earnings | Trapped-profits 2% annual tax (Amendment 277, in force 2025+) applies to excess undistributed earnings of closely-held companies | "Roughly how much retained earnings has the company accumulated?" |
| Existing shareholder loans | Section 3(tet) already applies if loans are outstanding | "Does the company currently have any outstanding loans to you (halvaat baalim)?" |

### Step 1a: Section 62A Gate (Personal-Services Companies)

Before running any comparison, check whether Section 62A look-through applies. If it does, the salary-vs-dividend choice is largely moot.

Section 62A (tightened by Amendment 277 to the Income Tax Ordinance, effective 2025-01-01) treats a closely-held company as a transparent pass-through when:

1. Revenue comes mainly from the personal services of a material shareholder (10%+ of the means of control; this trigger was NOT changed by Amendment 277).
2. The shareholder works for a single substantial client over a meaningful window (22 months within 3 tax years; Amendment 277 tightened this from the prior 30 months within 4 tax years).
3. Profits exceed a 25% margin on personal-effort revenue (the new excess-profitability limb, Section 62A(a1)).

When these tests are met, profits above the 25% margin are deemed distributed to the shareholder and taxed at marginal rates regardless of the actual extraction method chosen. Salary-vs-dividend optimization saves nothing in this fact pattern, and planning shifts to documenting genuine business activity, expanding the client base, or restructuring.

**Key exemption:** if the shareholder holds 25%+ of the *client* entity receiving the services, the personal-services attribution does not apply (they are treated as a genuine part-owner of the client, not a wallet company). Amendment 277 raised this exit threshold from the prior 10% to 25%, so mid-size stakes (10-25%) in the client that used to be safe now fall inside §62A.

Common §62A triggers: solo consultants, freelance developers, lawyers/doctors operating through a personal Ltd, and "wallet companies" (chevrot arnak).

### Step 1b: Benefit-Track Gate (Encouragement of Capital Investments Law)

The 23% corporate rate and the 30% dividend rate are the STANDARD-company defaults. A company
holding a status under the Law for Encouragement of Capital Investments, 5719-1959 pays neither,
and modelling it at 23% roughly doubles the corporate layer. Ask before comparing: "does the
company hold a Preferred, Special Preferred, or Technology Enterprise status?" Israeli software
and tech companies are the population this most often catches.

| Track | Development Area A | Elsewhere | Dividend from that profit |
|---|---|---|---|
| Preferred Enterprise (מפעל מועדף) | 7.5% | 16% | 20% (s.51יח) |
| Special Preferred Enterprise (מפעל מועדף מיוחד) | 5% | 8% | 20% (s.51יח) |
| Preferred Technology Enterprise (מפעל טכנולוגי מועדף) | 7.5% | 12% | 20%, or 4% to a foreign company (s.51כו) |
| Special Preferred Technology Enterprise (מפעל טכנולוגי מועדף מיוחד) | 6% | 6% | 20%, or 4% to a foreign company (s.51כו) |

Three rules that decide whether the headline rate is the right one:

1. **Qualifying income only.** The reduced rate applies to preferred / qualifying technological
   income. Other income stays at 23%. For the technology tracks it applies only to the
   Israel-developed share of the intangible asset, on a nexus basis, so mixed IP gives a blended rate.
2. **The 4% dividend rate is narrow.** It needs a foreign-resident body corporate recipient AND
   90% or more of the payer's shares held directly by foreign-resident bodies corporate, plus the
   further conditions in s.51כו(2). Otherwise the rate is 20%.
3. **Entitlement is selected by approval or election date, not by tax year.** A company on a
   pre-2011 מפעל מוטב or מפעל מאושר approval, or one computing an earlier year, may still be on a
   superseded table (the Preferred Area A rate was 9% for 2014-2016, and the benefit-track dividend
   rate was 15% until 2017). See `references/tax-rates-2026.md` for the cohort-selection rule under
   Amendment 68 s.39 and the superseded tables. Do NOT answer such a company from the table above.

Pass the track to the comparison script with `--benefit-track` (`pte`, `pte-a`, `spte`, `pfe`,
`pfe-a`, `spfe`, `spfe-a`); it defaults to `standard`. Use `--dividend-rate` for the 4% or the
non-controlling 25% case.

### Step 2: Understand the Extraction Methods

Israeli tax law provides four main ways for a controlling shareholder to extract value from their company. Each has a fundamentally different tax structure:

| Method | Corporate Tax | Personal Tax | Bituach Leumi | Key Advantage |
|--------|-------------|-------------|---------------|---------------|
| **Salary** | 0% (deductible expense) | Progressive rates (10%-50%) | Employee + Employer NI | Tax credit points, pension deductions, NI ceiling |
| **Dividend** | 23% (on profit first; less on a benefit track, Step 1b) | 30% (controlling shareholder; 20% or 4% on benefit-track profits) | None | No NI, simple, no employer cost beyond profit |
| **Shareholder Loan** | 0% (no immediate tax) | Section 3(tet) deemed interest (6.53% in 2026) | None | Defers real tax, keeps cash flexible |
| **Management Fees** | 0% (deductible) | Income tax as business income + VAT 18% | Self-employed NI rates | Can deduct business expenses against fees |

**Combined effective tax rates (2026, controlling shareholder above surtax threshold):**

| Method | Effective Rate (approximate) | Calculation |
|--------|------------------------------|-------------|
| Salary (top bracket) | ~55-60% | 50% income tax + employer NI 7.38% (on amount above ceiling, lower) |
| Dividend | 46.1% (up to 49.95% with surtax) | 23% corporate + 30% on remainder (+ 5% surtax above 721,560) |
| Shareholder Loan | 6.53% annual deemed interest (taxed as income) | Not a real extraction, must eventually repay or convert |
| Management Fees | ~50-55% + 18% VAT on gross | Similar to salary but with VAT and self-employed NI |

### Step 3: Dividend Distribution Analysis

Dividend distribution (halokat dividendim) is often the default choice. Analyze it carefully:

**Tax calculation for controlling shareholder (baal shlita, 10%+ holding):**

```
Company pre-tax profit:           P
Corporate tax (23%):              P x 0.23
Distributable profit:             P x 0.77
Dividend withholding tax (30%):   P x 0.77 x 0.30 = P x 0.231
Net to shareholder:               P x 0.77 x 0.70 = P x 0.539
Effective total tax rate:         46.1%
```

**Surtax impact (mas yesafim) for 2026:**

If the shareholder's total annual income (including the dividend) exceeds 721,560 NIS:
- Additional 3% surtax on the excess (Section 121B)
- Additional 2% surtax on non-labor income above 721,560 NIS (effective 2025+)
- Total additional: 5% on dividend portion above threshold
- Effective rate climbs to ~49.95% on the portion above threshold

**When dividend is optimal:**
- Shareholder's salary already maximizes lower tax brackets
- Amount is large enough that salary would push into 47%+ bracket anyway
- Company has sufficient retained earnings (arvei rvaachim)
- No Bituach Leumi advantage left (salary already above NI ceiling)

**When dividend is suboptimal:**
- Shareholder draws no or low salary (wasting lower brackets and credit points)
- Amount is moderate (under ~200,000 NIS) and salary brackets aren't fully utilized
- Company needs the cash for operations (dividend is irreversible)

### Step 4: Salary Extraction Analysis

Salary (maskoret) is a deductible expense for the company, avoiding the 23% corporate tax layer. But it triggers progressive income tax and Bituach Leumi.

**2026 Income Tax Brackets (earned income):**

| Annual Income (NIS) | Tax Rate |
|---------------------|----------|
| Up to 84,120 | 10% |
| 84,121 - 120,720 | 14% |
| 120,721 - 228,000 | 20% |
| 228,001 - 301,200 | 31% |
| 301,201 - 560,280 | 35% |
| 560,281 - 721,560 | 47% |
| Above 721,560 | 50% (47% + 3% surtax) |

**Bituach Leumi rates for controlling shareholder employees (2026):**

| Income Range | Employee NI | Employee Health | Employer NI |
|-------------|------------|----------------|-------------|
| Up to 7,703 NIS/month | 1.04% | 3.23% | 4.46% |
| 7,703 - 51,910 NIS/month | 7.0% | 5.17% | 7.38% |
| Above 51,910 NIS/month | 0% (ceiling) | 0% (ceiling) | 0% (ceiling) |

Note: Controlling shareholder employer NI rates (4.46%/7.38%) differ slightly from regular employees (4.51%/7.60%). The employee NI rate at the lower band is 1.04% (raised through 2024 budget measures) and health is 3.23%/5.17% (updated by the 2025 amendment).

**Tax credit points (nekudot zikui):**
Each point reduces tax by 242 NIS/month (2,904 NIS/year, frozen 2025-2027). Base: 2.25 points for residents (additional points for women, children, new immigrants, etc.).

**Salary advantages:**
- Pension contributions (hafrashat pensia) are tax-deductible up to ceiling
- Keren Hishtalmut contributions (up to ceiling) are employer-deductible, tax-free to employee
- Tax credit points reduce effective rate on first brackets
- NI contributions build social security entitlements

**Salary disadvantages:**
- Employer NI cost (~7.38%) adds to the total extraction cost
- Top marginal rate (50%) exceeds the effective dividend rate (46.1%) for high amounts
- Creates ongoing employment obligations
- **Controlling shareholders are excluded from unemployment insurance** (demei avtala) under the Bituach Leumi Law since the 2003 amendment, so the employer NI premium does NOT buy unemployment coverage; maternity and disability entitlements are also restricted compared to regular employees. The "NI builds social security" advantage is partial for baalei shlita.

**Optimal salary level:**
The sweet spot is often drawing enough salary to utilize the lower tax brackets (up to ~228,000 NIS/year at 20% marginal rate) and pension/keren hishtalmut deductions, then extracting additional amounts as dividends. Run the comparison script (see Bundled Resources) with specific numbers.

### Step 5: Shareholder Loan Analysis (Section 3(tet) and 3(tet1))

A shareholder loan (halvaat baalim) defers taxation but does not eliminate it. The Israeli Tax Authority watches these closely, and Section 3(tet1) sets a hard automatic-reclassification deadline.

**Section 3(tet) rules (2026):**

When a company lends money to a shareholder (or related party) at below-market interest:
- Deemed interest rate: **6.53%** per year (set annually by regulation)
- The difference between actual interest charged and 6.53% is treated as taxable income to the borrower
- For controlling shareholders: deemed interest is classified as **salary income** and taxed at marginal rates
- The company must report the deemed interest on Form 126

**Section 3(yod) rate:** 4.9% (deemed interest income for the lender where special relations exist between the parties)

**Section 3(tet1) automatic-reclassification deadline (Amendment 235, in force 2017):**

A loan or withdrawal from a closely-held company to a controlling shareholder is **automatically deemed withdrawn** if not repaid by **the end of the tax year FOLLOWING the year of withdrawal**. Circular 7/2017 reclassifies the deemed withdrawal in this order: (1) dividend to the extent of distributable profits, (2) salary/work income if an employer-employee relationship exists, (3) otherwise business or professional income under Section 2(1).

Concretely: a loan drawn on 2026-01-15 must be repaid by **2027-12-31** to avoid automatic reclassification. The skill's earlier "90 days" guidance was incorrect.

De minimis exemption: cumulative withdrawals stay outside §3(tet1) if balance is below **NIS 100,000** on every day of year N and every day of year N-1.

**Critical rules:**

| Rule | Detail |
|------|--------|
| Interest-free loan | Full 6.53% deemed as income to borrower |
| Loan still outstanding at end of year N+1 | Automatic §3(tet1) reclassification (typically as dividend, 30% + any surtax) |
| Loan used for personal expenses | Locks reclassification as withdrawal under §3(tet1) cascade |
| Loan has no repayment schedule | Red flag for Tax Authority |
| Company has retained earnings | Increases risk of deemed dividend reclassification |

**When it makes sense:** a short-term need with a documented loan agreement and a repayment plan, or bridge financing until a dividend is approved, where the 6.53% deemed-interest cost beats the tax on the alternative.

**When to avoid:** a long-term extraction need, a company with distributable retained earnings (the Tax Authority will challenge the loan structure), no written agreement or schedule, or an already-significant outstanding balance. See `references/section-3tet-rules.md` for the reclassification-risk detail.

**Deemed interest calculation example:**

```
Loan amount:             500,000 NIS
Annual deemed interest:  500,000 x 6.53% = 32,650 NIS
Tax on deemed interest:  32,650 x marginal rate (e.g., 47%) = 15,346 NIS
Net annual cost:         15,346 NIS (3.07% of loan)
```

Compare with dividend on same 500,000: tax of ~230,500 NIS (46.1%). The loan defers this but accumulates cost annually.

### Step 6: Management Fees (Dmei Nihul)

A shareholder can provide management services to the company through a separate business entity (osek murshe or a management company). This is an alternative extraction method.

**How it works:**
1. Shareholder (or their management company) invoices the company for management services
2. Company deducts the fee as a business expense (no corporate tax)
3. Fee is subject to income tax as business income + VAT (18%)
4. If through a personal osek murshe: subject to self-employed NI rates

**Self-employed NI rates (2026):**

| Income Range | NI Rate | Health Rate | Total |
|-------------|---------|-------------|-------|
| Up to 7,703 NIS/month | 4.47% | 3.23% | 7.70% |
| 7,703 - 51,910 NIS/month | 12.83% | 5.17% | 18.00% |

Note: 52% of the NI amount is tax-deductible (Section 47A).

**Advantages:** business expenses (office, car, phone, travel) are deductible against the fees, timing of income recognition is more flexible, and family members can be employed in the management entity.

**Disadvantages:** VAT (18%) on the gross fee (offset if the company is also an osek murshe), higher self-employed NI rates, the risk that the Tax Authority recharacterises "excessive" fees as disguised dividends, the overhead of a separate bookkept entity, and Section 85A transfer pricing, which requires the fee to reflect market rates.

**When management fees work:**
- Shareholder has legitimate business expenses to offset
- Amount is reasonable relative to services provided
- Properly documented with service agreements

### Step 7: Compare Strategies Side by Side

Use this framework to compare extraction methods for the user's specific situation:

**Decision matrix:**

| Factor | Salary | Dividend | Loan | Management Fees |
|--------|--------|----------|------|-----------------|
| Total effective tax rate | Variable (10%-60%) | 46.1%-49.95% | 6.53% deemed/year | Variable + 18% VAT |
| Bituach Leumi | Yes (capped) | No | No | Yes (higher rates) |
| Corporate tax deductible | Yes | No | N/A | Yes |
| Pension benefits | Yes | No | No | Self-funded |
| Reversible | No | No | Yes (repay loan) | No |
| Tax Authority scrutiny | Low | Low | High | Medium |
| Timing flexibility | Monthly | Board resolution | Immediate | Per invoice |
| Minimum salary requirement | None (no statutory minimum; §32(9) is a reasonableness ceiling, not a floor, see Step 8) | None | None | None |

**Common optimal combinations:**

1. **Small extraction (under 200,000 NIS):** Salary up to the 20% bracket (228,000/year) to maximize credit points and pension benefits
2. **Medium extraction (200,000 - 500,000 NIS):** Salary to optimize brackets + dividend for the remainder
3. **Large extraction (500,000+ NIS):** Salary at optimal level + dividend, potentially with short-term loan bridge
4. **One-time tax assessment:** Short-term shareholder loan with 12-month repayment, funded by planned dividend

### Step 8: Compliance Checklist

Before recommending any strategy, verify these compliance requirements:

| Requirement | Check |
|-------------|-------|
| Company has a CPA (roeh heshbon) | All strategies require professional filing |
| Board resolution for dividends | Required before distribution under Companies Law Sections 301-303 (profit test + solvency test); record date and source of distribution must be documented in the protokol |
| Loan agreement for shareholder loans | Written agreement with interest rate, repayment schedule, and signatures; track §3(tet1) end-of-following-year deadline |
| "Reasonable salary" for controlling shareholder | No fixed statutory minimum. Section 32(9) ITO disallows the company's deduction of UNREASONABLE amounts paid to controlling shareholders (it caps excessive amounts; it is not a minimum-salary rule). The practical "reasonable salary" doctrine comes from case law plus §62A post-Amendment 277, which attributes personal-services profits above a 25% margin to the shareholder at marginal rates regardless of the salary actually drawn. |
| §3(tet1) "use of asset" tracking | A controlling shareholder's personal use of company-owned apartments, vehicles (beyond limited business use), art, yachts, etc., accrues a deemed withdrawal under §3(tet1) at deemed annual usage value, even without any cash loan. Track these alongside cash-loan balances. |
| §126(b) inter-company dividend exemption | Dividends paid between Israeli companies are exempt from corporate tax under §126(b). When a holding-company structure is involved, dividend planning differs from the single-tier model in this skill; consult on the structure. |
| BL minimum for no-salary baal shlita | A controlling shareholder drawing zero salary still owes Bituach Leumi minimum (~NIS 266/month combined NI+health for someone with no other taxable income) paid directly by the individual |
| Withholding tax on dividends | Company withholds at the applicable rate (30% controlling / 25% non-controlling / 20% or 4% on benefit-track profits) and pays the assessing officer by the **16th** of each month for the previous month, filing Form 102 by the same date (regs. 13 and 14(a), Income Tax Regulations (Deduction from Interest, Dividend and Certain Gains), 5766-2005, as replaced with effect from 1 January 2018). The 15th is the superseded pre-2018 date and is also the Bituach Leumi date, which is where the confusion comes from |
| Form 856 reporting | Payments to shareholders must be reported |
| Section 3(tet) reporting | Deemed interest must be reported on Form 126 |
| Trapped-profits 2% surtax + safe harbor | Closely-held companies with excess undistributed earnings owe an additional 2% corporate tax under Amendment 277 (in force from 2025). Distributing at least 6% of accumulated profits during the year (5% for 2025 only) is a safe harbor that avoids the surcharge; weigh this modest distribution against the 2% annual drag |
| Section 77 deemed-distribution risk | Tax Authority may deem unreasonably accumulated retained earnings as distributed (5-year lookback); persistent retention without business purpose triggers this |
| Transfer pricing for management fees | Fees must reflect arm's length market rates (Section 85A) |
| VAT invoice for management fees | Must issue tax invoice (heshbonit mas) |
| Surtax reporting | Include all income sources when calculating surtax threshold; the +2% non-labor surtax (effective 2025) applies separately to dividends, capital gains, interest, and rental |
| Non-resident shareholder | Section 3(i)(1) withholding applies; treaty rates override domestic 25%/30% -- check the relevant tax treaty |
| Encouragement-Law benefit track | Confirm the company's status and the year the approval or election was made before applying any rate. Corporate: 7.5%/16% (PFE), 5%/8% (SPFE), 7.5%/12% (PTE), 6% (SPTE). Dividend out of those profits: 20%, or 4% on technological income to a qualifying foreign company. Do not assume 23%/30%. See Step 1b |

**Always recommend:**
- Consult with a licensed Israeli CPA (roeh heshbon) or tax advisor (yoetz mas) before executing any strategy
- The analysis provides a framework for informed discussion with professionals, not a substitute for professional advice

## Gotchas

1. **Wrong dividend tax rate.** AI agents frequently use 25% dividend tax for all shareholders. For controlling shareholders (baal shlita, 10%+ holding), the rate is **30%**, not 25%. This 5% difference on a 500,000 NIS dividend = 19,250 NIS error.

2. **Ignoring the double taxation on dividends.** Agents often quote 30% as the total dividend tax. The real burden is 23% corporate tax + 30% on the remaining 77% = **46.1% effective rate**. Quoting just 30% understates the cost by over 50%.

3. **Section 3(tet) interest rate confusion.** The deemed interest rate changes annually. For 2026 it is **6.53%** (Section 3(tet)) and **4.9%** (Section 3(yod) for CPI-linked loans). Using old rates or confusing the two sections produces wrong calculations. Always specify the tax year.

4. **Wrong §3(tet1) repayment deadline.** A frequent error is treating shareholder loans as needing repayment within 90 days or within the tax year. The actual deadline under Section 3(tet1) is the **end of the tax year FOLLOWING the year of withdrawal** (Amendment 235, in force 2017; Circular 7/2017). Quoting 90 days creates artificial urgency and bad bridging-loan advice; quoting "anytime" misses the hard automatic-reclassification rule.

5. **Skipping the §62A look-through gate.** For one-client personal-services companies, Amendment 277 (in force 2025-01-01) taxes profits above a 25% margin at marginal rates regardless of salary/dividend choice. Agents that jump straight to the comparison table produce optimization advice that is irrelevant for the slice of users where §62A actually drives the answer.

6. **Forgetting Bituach Leumi on salary.** When comparing salary vs dividend, agents often compare only income tax rates. Salary carries ~12% employee NI+health and ~7.38% employer NI (for controlling shareholders), which significantly changes the breakeven point. The NI ceiling (51,910 NIS/month for 2026) is also frequently missed.

7. **Mixing up controlling shareholder NI rates.** Controlling shareholder employees (baalei shlita) have slightly different NI rates (employer: 4.46%/7.38%) than regular employees (4.51%/7.60%). Using regular rates for a baal shlita produces incorrect calculations and may trigger audit questions.

8. **Ignoring the trapped-profits 2% safe harbor in the retain-vs-distribute decision.** Amendment 277 introduced an annual 2% corporate-tax surcharge on closely-held companies that accumulate excess retained earnings without distributing. Crucially, there is a **safe harbor**: distributing at least 6% of accumulated profits during the year (5% for 2025 only) avoids the surcharge entirely. So the real lever is "distribute 6% and the 2% vanishes", not "pay 2% forever". Agents that mention the surcharge but omit the safe harbor push owners to pay a 2% drag they could have escaped with a modest distribution.

9. **Modelling a benefit-track company at 23% and 30%.** A Preferred Technology Enterprise outside Development Area A pays **12%** corporate tax and **20%** on the dividend, an effective 29.6% against the 46.1% the standard model produces. Agents that jump to the standard rates overstate the burden by more than half for exactly the population, Israeli software and tech companies, that asks this question most. Ask about Encouragement-Law status before running any comparison, and remember the reduced rate covers qualifying income only.

10. **Answering a grandfathered company from the current table.** Benefit entitlement is selected by the approval or election date of the programme, not by the tax year. A company on a pre-2011 מפעל מוטב or מפעל מאושר approval, or a question about an earlier year, may be governed by a superseded schedule (Preferred Area A was 9% for 2014-2016; the benefit-track dividend rate was 15% until 2017). Confirming the current rate is correct does not make it the applicable one.

11. **Treating §3(tet1) as a cash-loan-only rule.** Amendment 235 explicitly captures shareholder personal use of company-owned assets (apartment, vehicle beyond limited business use, art, yacht) at deemed annual usage value. A baal shlita living in a company-owned apartment without paying market rent accrues a deemed withdrawal even with zero cash loan. This is the single most-missed §3(tet1) trap in real ITA audits.

## Bundled Resources

- `references/tax-rates-2026.md` -- Complete 2026 tax rates: income brackets, corporate tax, dividend rates, NI rates, surtax thresholds, credit point value, Section 3(tet) rates
- `references/extraction-methods.md` -- Detailed comparison of salary, dividend, loan, and management fee extraction with worked examples
- `references/domain-checklist.md` -- Coverage contract for this domain: what the skill must cover, what is deliberately out of scope, and why
- `references/section-3tet-rules.md` -- Section 3(tet) and 3(yod) deemed interest rules, reclassification risks, documentation requirements
- `scripts/tax_comparison.py` -- Interactive Python calculator: input company profit and shareholder details, outputs side-by-side comparison of all extraction methods with total tax burden

## Recommended MCP Servers

| MCP Server | What It Adds |
|------------|-------------|
| [kolzchut](https://agentskills.co.il/he/mcp/kolzchut) | Look up tax rights, entitlements, and eligibility criteria from Israel's authoritative rights database |

## Reference Links

Official sources for verifying and updating the tax figures in this skill:

| Source | URL | What to Check |
|--------|-----|---------------|
| Israeli Tax Authority (Reshut HaMisim) | https://www.gov.il/he/departments/israel_tax_authority | Official tax rates, forms, circulars |
| Income Tax Ordinance | https://www.nevo.co.il/law_html/law00/84255.htm | Legal text for Section 3(tet), Section 121B (surtax), Section 32(9) |
| Bituach Leumi -- Contribution Rates | https://www.btl.gov.il/Insurance/National%20Insurance/Pages/default.aspx | Current NI and health insurance rates |
| Section 3(tet) Annual Rate | https://britcpa.co.il/hozrim/שיעורי-הריבית-לעניין-סעיפים-3ט-ו-3י-לשנת-4/ | Published annually, usually in December for the following year |
| Law for Encouragement of Capital Investments, 5719-1959 | https://www.nevo.co.il/law_html/law01/p181_001.htm | Sections 51טז, 51יח, 51כא, 51כה, 51כו for benefit-track corporate and dividend rates; Amendment 68 s.39 for the grandfathering cohorts |
| Income Tax Regulations (Deduction from Interest, Dividend and Certain Gains), 5766-2005 | https://www.nevo.co.il/law_html/law01/999_549.htm | Regs. 13 and 14 for the monthly withholding deposit date and Form 102 |
| Kolzchut -- Tax Rights | https://www.kolzchut.org.il/he/%D7%9E%D7%93%D7%A8%D7%92%D7%95%D7%AA_%D7%9E%D7%A1_%D7%94%D7%9B%D7%A0%D7%A1%D7%94 | Income tax brackets, credit points, updated annually |
| CWS Israel -- Tax Guide | https://www.cwsisrael.com/israeli-tax-changes-2026-complete-guide/ | English-language summary of annual tax changes |

## Troubleshooting

### "I need to pay a tax assessment (shuma) urgently"

If the user has received a tax assessment and needs to pay immediately using company funds:
1. **Short-term:** Shareholder loan with formal agreement is the fastest option (no board resolution needed, just a loan agreement)
2. **Within 30 days:** Plan a dividend distribution with board resolution
3. **Document everything:** Written loan agreement even for temporary borrowing
4. **Repayment / conversion timing:** §3(tet) deemed-interest accrues from day one (cost = 6.53% × loan amount × marginal rate annually). §3(tet1) automatic reclassification triggers if the loan remains outstanding at the end of the tax year **following** the year of withdrawal. Most planners convert the loan to a dividend before the end of year N+1, accepting one year of 3(tet) interest if the cash-flow benefit justifies it.

### "Which method should I use for a one-time large amount?"

For a one-time extraction of 500,000+ NIS:
1. Check current salary level and marginal bracket
2. If salary is already above 228,000/year: dividend is likely optimal
3. If salary is low: increase salary to fill lower brackets, dividend for the rest
4. If timing is urgent: shareholder loan as bridge, convert before the end of the following tax year (§3(tet1) deadline) -- see Step 5

### "We have a family company election -- does any of this still apply?"

If the company has elected Family Company status (Section 64A), corporate-tax-layer planning collapses: profits are attributed directly to the "representative shareholder" at marginal rates, eliminating the 23% corporate tax. Salary-vs-dividend optimization in that case reduces to "how to characterize income most efficiently for surtax and BL". The election deadline is by November 30 of the tax year (or within 3 months of incorporation), so this is something to set up in advance, not retrofit mid-year.

### "The Tax Authority questioned my shareholder loan"

If the Tax Authority (pakid shuma) challenges a shareholder loan:
1. Present the formal loan agreement with interest terms
2. Show repayment history or schedule
3. Demonstrate business purpose for the loan
4. If loan was used for personal tax payment: be prepared for reclassification as dividend
5. Consult with tax advisor immediately
