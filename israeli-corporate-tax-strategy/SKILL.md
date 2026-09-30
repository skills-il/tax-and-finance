---
name: israeli-corporate-tax-strategy
description: "Strategic tax analysis for Israeli company owners (baalei shlita) comparing salary, dividends, shareholder loans, and management fees as profit extraction methods. Use when user asks about paying personal tax from company funds, dividend vs salary comparison, shareholder loan tax implications, Section 3(tet) deemed interest, corporate profit extraction strategy, halokat dividendim, mashichat rvaachim, or baal shlita tax planning. Calculates total tax burden across methods, identifies optimal strategy based on assessment amount and company structure, and verifies compliance with Israeli Tax Authority rules. Prevents costly extraction mistakes by analyzing withholding, Bituach Leumi, surtax, and corporate tax interactions. Do NOT use for VAT reporting (use israeli-vat-reporting), payroll processing (use israeli-payroll-calculator), annual tax return filing (use israeli-tax-returns), or crypto tax (use israeli-crypto-tax-reporter)."
license: MIT
allowed-tools: Bash(python:*) WebFetch
compatibility: Works with Claude Code, OpenClaw, Cursor, Windsurf, Codex, GitHub Copilot, opencode, antigravity.
---

# Israeli Corporate Tax Strategy

## Legal notice

This is a free information tool operated by an AI model. It explains the rules and calculates from the figures you enter, but it does not examine your full circumstances and does not constitute tax advice. All of its outputs are produced automatically, with no involvement, review, or approval by a tax adviser or accountant, and an AI model may err, omit data, or present a wrong conclusion. Responsibility for reporting and paying the tax is yours, the binding computation is the Tax Authority's, and representation before the Tax Authority is reserved to those permitted by law. This tool is not a substitute for advice that takes account of the particular circumstances and needs of each person, and all use of its output is the user's sole responsibility.


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

Section 62A (tightened by Amendment 277 to the Income Tax Ordinance, effective 2025-01-01) attributes a closely-held company's income to its shareholder. Amendment 277 changed the holder test from "material shareholder" to "controlling holder" (בעל שליטה, s.75B(a)(3): an Israeli resident holding 10%+ of any means of control, directly or indirectly). Three routes:

1. **Officer or management services to another company (s.62A(a)(1)).** Exit only if the individual holds 25%+ of the client on some day in the tax year (raised from 10%, so 10-25% stakes that used to be safe are now caught).
2. **Services the individual would otherwise render as an employee**, including where 70%+ of the company's income comes from one client over 22 months within 3 tax years (formerly 30 months within 4). A company employing four or more employees stays excluded from the one-client rule.
3. **Excess profitability (new s.62A(a1)).** Where profitability on personal-exertion activity exceeds 25%, the profit above that 25% margin is taxed to the active shareholder at marginal rates as work income, and Bituach Leumi applies to it. It does not reach a company whose personal-exertion turnover is at least NIS 30 million times the number of controlling holders. It also does not reach a holder whose accumulated profits across all his companies did not exceed NIS 750,000 at the end of the previous year, or a company whose own accumulated profits did not exceed NIS 750,000 where its controlling holders do not control the client.

Where 62A applies, salary-vs-dividend optimization saves little, and planning shifts to documenting genuine business activity, expanding the client base, or restructuring. The company flags 62A on Form 1214 (execution instruction 9/2026).

Common §62A cases: solo consultants, freelance developers, and professionals working through a personal Ltd ("wallet companies", chevrot arnak).

### Step 1b: Benefit-Track Gate (Encouragement of Capital Investments Law)

The 23% corporate rate and the 30% dividend rate are the STANDARD-company defaults. A company
holding a status under the Law for Encouragement of Capital Investments, 5719-1959 pays neither,
and modelling it at 23% roughly doubles the corporate layer. Ask before comparing: "does the
company hold a Preferred, Special Preferred, or Technology Enterprise status?" Software and tech
companies are most often caught.

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
`pfe-a`, `spfe`, `spfe-a`); it defaults to `standard`. Use `--dividend-rate` for the 4% (treated as a body-corporate recipient, no surtax) or the
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
| Salary (top bracket) | 50% above 721,560 (47% between the NI ceiling and 721,560); up to ~62% in the 47% band below the ceiling | 50% income tax above 721,560 with no NI above 51,910/month; below the ceiling add employee 11.96% and employer 7.38% |
| Dividend | 46.1% (up to 49.95% with surtax) | 23% corporate + 30% on remainder (+3% above 721,560 total income, +2% more above 721,560 capital income, Step 3) |
| Shareholder Loan | 6.53% annual deemed interest (taxed as income) | Not a real extraction, must eventually repay or convert |
| Management Fees | Similar to salary (~50% at the top) | Self-employed NI instead of employee + employer NI; VAT neutral when the company reclaims it |

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

The two limbs are measured SEPARATELY against the same 721,560 NIS threshold:
- **3% (s.121B(a))** on TOTAL taxable income above 721,560, salary and dividend together.
- **2% more (s.121B(a1), Amendment 276, from 2025)** on capital-source income (dividends, interest, capital gains, rent) above 721,560, measured on that capital income ALONE. Salary does not use up this threshold: 400,000 salary plus 700,000 of dividends and interest owes the 3% but not the 2% (ITA execution instruction 5/2025, example 3.2).
- A dividend reaches the full 5% only on the slice by which capital income itself exceeds 721,560, where the combined rate is ~49.95%. Because both limbs reset every tax year, pacing a large distribution over several years so capital income stays under 721,560 avoids the 2% (and the 3% too when salary is low).

The 46.1% figure prices CURRENT profit that still has to bear corporate tax. Distributing retained earnings that already bore it costs only the dividend rate plus any surtax.

**Dividend tends to win** when salary already fills the lower brackets and passes the NI ceiling, the amount would push salary into 47%+, and retained earnings (arvei rvaachim) are sufficient. **It tends to lose** when the shareholder draws little or no salary (unused brackets and credit points), the amount is moderate (under ~200,000 NIS), or the company needs the cash (a dividend is irreversible).

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
| Up to 7,703 NIS/month | 1.02% | 3.23% | 4.46% |
| 7,703 - 51,910 NIS/month | 6.79% | 5.17% | 7.38% |
| Above 51,910 NIS/month | 0% (ceiling) | 0% (ceiling) | 0% (ceiling) |

Note: both sides differ from a regular employee. Employer 4.46%/7.38% (regular 4.51%/7.60%); employee NI 1.02%/6.79% (regular 1.04%/7.0%), which with health makes 4.25%/11.96% (BTL rate table, column 2).

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

**Use it** as a documented short-term bridge (e.g. until a dividend is approved); **avoid it** for long-term extraction or without a written agreement and schedule. See `references/section-3tet-rules.md` for reclassification risk and for answering a Tax Authority challenge.

**Deemed interest calculation example:**

```
Loan amount:             500,000 NIS
Annual deemed interest:  500,000 x 6.53% = 32,650 NIS
Tax on deemed interest:  32,650 x marginal rate (e.g., 47%) = 15,346 NIS
Net annual cost:         15,346 NIS (3.07% of loan)
```

The loan defers the dividend tax but does not avoid it, and lending cash still requires profit that has already borne corporate tax.

### Step 6: Management Fees (Dmei Nihul)

The shareholder (as an osek murshe, or through a management company) invoices the company for management services. The company deducts the fee, so there is no corporate tax; the fee is business income plus VAT (18%), and a personal osek murshe pays self-employed NI. Check Step 1a first: a management company billing one client is a classic §62A case. The comparison script models this route for a personal osek murshe (VAT assumed reclaimed, no expenses deducted).

**Self-employed NI rates (2026):**

| Income Range | NI Rate | Health Rate | Total |
|-------------|---------|-------------|-------|
| Up to 7,703 NIS/month | 4.47% | 3.23% | 7.70% |
| 7,703 - 51,910 NIS/month | 12.83% | 5.17% | 18.00% |

Note: 52% of the NI amount is tax-deductible (Section 47A).

**Advantages:** business expenses (office, car, phone, travel) are deductible against the fees, timing of income recognition is more flexible, and family members can be employed in the management entity.

**Disadvantages:** VAT (18%) on the gross fee (offset if the company is also an osek murshe), higher self-employed NI rates, the risk that the Tax Authority recharacterises "excessive" fees as disguised dividends, the overhead of a separate bookkept entity, and Section 85A transfer pricing, which requires the fee to reflect market rates.

**When management fees work:** real business expenses to offset, a fee reasonable for the services, and a written service agreement.

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
| §126(b) inter-company dividend exemption | Dividends between Israeli companies are exempt under §126(b), so a holding-company structure needs its own analysis beyond this single-tier model. |
| BL minimum for no-salary baal shlita | A controlling shareholder drawing zero salary still owes Bituach Leumi minimum (~NIS 266/month combined NI+health for someone with no other taxable income) paid directly by the individual |
| Withholding tax on dividends | Company withholds at the applicable rate (30% controlling / 25% non-controlling / 20% or 4% on benefit-track profits) and pays the assessing officer by the **16th** of each month for the previous month, filing Form 102 by the same date (regs. 13 and 14(a), Income Tax Regulations (Deduction from Interest, Dividend and Certain Gains), 5766-2005, as replaced with effect from 1 January 2018). The 15th is the superseded pre-2018 date and is also the Bituach Leumi date, which is where the confusion comes from |
| Form 856 reporting | Payments to shareholders must be reported |
| Section 3(tet) reporting | Deemed interest must be reported on Form 126 |
| Trapped-profits 2% surcharge (ss.81A-81F) | Amendment 277, from tax year 2025: a closely-held company owes 2% a year on excess accumulated profits, after a shield of the highest of NIS 750,000, an expense shield, or an asset shield (cash, securities and loans are "special assets" and do not shield). No surcharge in a year where ANY exit is met: dividends distributed in that year of 6%+ of the prior year-end accumulated profits, OR over 50% of the excess profits, OR current losses above 10% of accumulated profits. An intercompany dividend exempt under s.126(b) counts only if the payer elects to withhold at the top rate (circular 02/2026). The 5% rate was for 2025 only. Reported on Form 1214, appendix 1281 (execution instruction 9/2026) |
| Section 77 deemed-distribution risk | Tax Authority may deem unreasonably accumulated retained earnings as distributed (5-year lookback); persistent retention without business purpose triggers this |
| Transfer pricing for management fees | Fees must reflect arm's length market rates (Section 85A) |
| VAT invoice for management fees | Must issue tax invoice (heshbonit mas) |
| Surtax reporting | Include all income sources for the 3% threshold; the +2% capital-income surtax (effective 2025) is measured on dividends, capital gains, interest, and rent ALONE against the same 721,560 |
| Non-resident shareholder | Section 3(i)(1) withholding applies; treaty rates override domestic 25%/30% -- check the relevant tax treaty |
| Encouragement-Law benefit track | Confirm the company's status and the year the approval or election was made before applying any rate. Corporate: 7.5%/16% (PFE), 5%/8% (SPFE), 7.5%/12% (PTE), 6% (SPTE). Dividend out of those profits: 20%, or 4% on technological income to a qualifying foreign company. Do not assume 23%/30%. See Step 1b |

**Always recommend** a licensed CPA (roeh heshbon) or tax advisor (yoetz mas) before executing any strategy.

## Gotchas

1. **Wrong dividend tax rate.** AI agents frequently use 25% dividend tax for all shareholders. For controlling shareholders (baal shlita, 10%+ holding), the rate is **30%**, not 25%. This 5% difference on a 500,000 NIS dividend = 19,250 NIS error.

2. **Ignoring the double taxation on dividends.** Agents often quote 30% as the total dividend tax. The real burden is 23% corporate tax + 30% on the remaining 77% = **46.1% effective rate**. Quoting just 30% understates the cost by over 50%.

3. **Section 3(tet) interest rate confusion.** The deemed interest rate changes annually. For 2026 it is **6.53%** (Section 3(tet)) and **4.9%** (Section 3(yod) for CPI-linked loans). Using old rates or confusing the two sections produces wrong calculations. Always specify the tax year.

4. **Wrong §3(tet1) repayment deadline.** A frequent error is treating shareholder loans as needing repayment within 90 days or within the tax year. The actual deadline under Section 3(tet1) is the **end of the tax year FOLLOWING the year of withdrawal** (Amendment 235, in force 2017; Circular 7/2017). Quoting 90 days creates artificial urgency and bad bridging-loan advice; quoting "anytime" misses the hard automatic-reclassification rule.

5. **Skipping the §62A look-through gate.** For one-client personal-services companies, Amendment 277 (in force 2025-01-01) taxes profits above a 25% margin at marginal rates regardless of salary/dividend choice. Agents that jump straight to the comparison table produce optimization advice that is irrelevant for the slice of users where §62A actually drives the answer.

6. **Forgetting Bituach Leumi on salary.** When comparing salary vs dividend, agents often compare only income tax rates. Salary carries ~12% employee NI+health and ~7.38% employer NI (for controlling shareholders), which significantly changes the breakeven point. The NI ceiling (51,910 NIS/month for 2026) is also frequently missed.

7. **Mixing up controlling shareholder NI rates.** Controlling shareholder employees (baalei shlita) have different NI rates on both sides (employer 4.46%/7.38%, employee 1.02%/6.79%) than regular employees (employer 4.51%/7.60%, employee 1.04%/7.0%). Using regular rates for a baal shlita produces incorrect calculations and may trigger audit questions.

8. **Ignoring the trapped-profits 2% safe harbor in the retain-vs-distribute decision.** Amendment 277 introduced an annual 2% corporate-tax surcharge on closely-held companies that accumulate excess retained earnings without distributing. Crucially, a year with taxed dividends of at least 6% of the prior year-end accumulated profits (or over 50% of the excess profits) owes no surcharge at all, and companies under the NIS 750,000 shield owe nothing. So the real lever is "distribute 6% and the 2% vanishes", not "pay 2% forever". Agents that mention the surcharge but omit the safe harbor push owners to pay a 2% drag they could have escaped with a modest distribution.

9. **Modelling a benefit-track company at 23% and 30%.** A Preferred Technology Enterprise outside Development Area A pays **12%** corporate tax and **20%** on the dividend, an effective 29.6% against the 46.1% the standard model produces. Agents that jump to the standard rates overstate the burden by more than half for exactly the population, Israeli software and tech companies, that asks this question most. Ask about Encouragement-Law status before running any comparison, and remember the reduced rate covers qualifying income only.

10. **Treating §3(tet1) as a cash-loan-only rule.** Amendment 235 explicitly captures shareholder personal use of company-owned assets (apartment, vehicle beyond limited business use, art, yacht) at deemed annual usage value. A baal shlita living in a company-owned apartment without paying market rent accrues a deemed withdrawal even with zero cash loan. This is the single most-missed §3(tet1) trap in real ITA audits.

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
4. **Repayment / conversion timing:** §3(tet) deemed interest (6.53% × loan × marginal rate) accrues from day one, and §3(tet1) reclassifies the loan if still outstanding at the end of the tax year **following** the withdrawal. Most planners convert it to a dividend before the end of year N+1.

### "Which method should I use for a one-time large amount?"

For a one-time extraction of 500,000+ NIS:
1. Check current salary level and marginal bracket
2. If salary is already above 228,000/year: dividend is likely optimal
3. If salary is low: increase salary to fill lower brackets, dividend for the rest
4. If timing is urgent: shareholder loan as bridge, convert before the end of the following tax year (§3(tet1) deadline) -- see Step 5

### "We have a family company election -- does any of this still apply?"

If the company has elected Family Company status (Section 64A), corporate-tax-layer planning collapses: profits are attributed directly to the "representative shareholder" at marginal rates, eliminating the 23% corporate tax. Salary-vs-dividend optimization in that case reduces to "how to characterize income most efficiently for surtax and BL". The election can only be made within 3 months of incorporation, so an existing company cannot adopt it now. Withdrawing requires notice no later than a month before the tax year begins, and a company that withdraws can never re-elect.
