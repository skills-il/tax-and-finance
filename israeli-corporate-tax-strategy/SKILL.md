---
name: israeli-corporate-tax-strategy
description: "Strategic tax analysis for Israeli company owners (baalei shlita) comparing salary, dividends, shareholder loans, and management fees as profit extraction methods. Use when user asks about paying personal tax from company funds, dividend vs salary comparison, shareholder loan tax implications, Section 3(tet) deemed interest, corporate profit extraction strategy, halokat dividendim, mashichat rvaachim, or baal shlita tax planning. Calculates total tax burden across methods, identifies optimal strategy based on assessment amount and company structure, and verifies compliance with Israeli Tax Authority rules. Prevents costly extraction mistakes by analyzing withholding, Bituach Leumi, surtax, and corporate tax interactions. Do NOT use for VAT reporting (use israeli-vat-reporting), payroll processing (use israeli-payroll-calculator), annual tax return filing (use israeli-tax-returns), or crypto tax (use israeli-crypto-tax-reporter)."
license: MIT
allowed-tools: Bash(python:*) WebFetch
compatibility: Works with Claude Code, OpenClaw, Cursor, Windsurf, Codex, GitHub Copilot, opencode, antigravity.
---

# Israeli Corporate Tax Strategy

## Problem

Israeli company owners (baalei shlita) face a critical decision whenever they need to extract profits or pay personal tax obligations: should they take a salary, distribute a dividend, use a shareholder loan, or pay management fees? Each method carries different tax rates, Bituach Leumi implications, and compliance requirements. Getting it wrong can cost tens of thousands of shekels in unnecessary tax, or worse, trigger Tax Authority scrutiny. Most business owners lack the specialized knowledge to model these scenarios accurately, and generic AI responses consistently get Israeli-specific rules wrong (especially Section 3(tet) deemed interest, controlling shareholder NI rates, and the surtax interaction with dividends).

## Instructions

### Step 1: Gather the User's Situation

Before any analysis, collect these details. Each variable significantly affects the optimal strategy:

| Variable | Why It Matters | What to Ask |
|----------|---------------|-------------|
| Company type | Tax rates and NI rules differ | "Is this a Chevra Baam (Ltd/baam)? Single-owner or multiple shareholders?" |
| Ownership percentage | Controlling shareholder (10%+) triggers higher dividend tax (30% vs 25%) | "What percentage of the company do you hold?" |
| Current salary from company | Determines marginal tax bracket and NI ceiling utilization | "What monthly salary do you currently draw from the company?" |
| Other income sources | Affects marginal rate and surtax threshold | "Do you have income from other sources (employment, rental, investments)?" |
| Amount needed | Strategy differs for 50K vs 500K vs 2M NIS | "How much do you need to extract, and is this a one-time or recurring need?" |
| Purpose | Tax assessment payment has specific timing constraints | "Is this for a tax assessment (shuma), personal expense, or regular income?" |
| Company profit level | Determines available retained earnings | "What is the company's approximate annual profit before this extraction?" |
| Existing shareholder loans | Section 3(tet) already applies if loans are outstanding | "Does the company currently have any outstanding loans to you (halvaat baalim)?" |

### Step 2: Understand the Extraction Methods

Israeli tax law provides four main ways for a controlling shareholder to extract value from their company. Each has a fundamentally different tax structure:

| Method | Corporate Tax | Personal Tax | Bituach Leumi | Key Advantage |
|--------|-------------|-------------|---------------|---------------|
| **Salary** | 0% (deductible expense) | Progressive rates (10%-50%) | Employee + Employer NI | Tax credit points, pension deductions, NI ceiling |
| **Dividend** | 23% (on profit first) | 30% (controlling shareholder) | None | No NI, simple, no employer cost beyond profit |
| **Shareholder Loan** | 0% (no immediate tax) | Section 3(tet) deemed interest (6.53% in 2026) | None | Defers real tax, keeps cash flexible |
| **Management Fees** | 0% (deductible) | Income tax as business income + VAT 18% | Self-employed NI rates | Can deduct business expenses against fees |

**Combined effective tax rates (2026, controlling shareholder above surtax threshold):**

| Method | Effective Rate (approximate) | Calculation |
|--------|------------------------------|-------------|
| Salary (top bracket) | ~55-60% | 50% income tax + employer NI 7.38% (on amount above ceiling, lower) |
| Dividend | 46.1% (up to 51.95% with surtax) | 23% corporate + 30% on remainder (+ 5% surtax above 721,560) |
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
| Up to 7,122 NIS/month | 0.4% | 3.1% | 4.46% |
| 7,122 - 47,465 NIS/month | 7.0% | 5.0% | 7.38% |
| Above 47,465 NIS/month | 0% (ceiling) | 0% (ceiling) | 0% (ceiling) |

Note: Controlling shareholder NI rates (4.46%/7.38% employer) differ slightly from regular employees (4.51%/7.60%).

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

**Optimal salary level:**
The sweet spot is often drawing enough salary to utilize the lower tax brackets (up to ~228,000 NIS/year at 20% marginal rate) and pension/keren hishtalmut deductions, then extracting additional amounts as dividends. Run the comparison script (see Bundled Resources) with specific numbers.

### Step 5: Shareholder Loan Analysis (Section 3(tet))

A shareholder loan (halvaat baalim) defers taxation but does not eliminate it. The Israeli Tax Authority watches these closely.

**Section 3(tet) rules (2026):**

When a company lends money to a shareholder (or related party) at below-market interest:
- Deemed interest rate: **6.53%** per year (set annually by regulation)
- The difference between actual interest charged and 6.53% is treated as taxable income to the borrower
- For controlling shareholders: deemed interest is classified as **salary income** and taxed at marginal rates
- The company must report the deemed interest on Form 126

**Section 3(yod) rate:** 4.9% (applies to CPI-linked loans between related parties)

**Critical rules:**

| Rule | Detail |
|------|--------|
| Interest-free loan | Full 6.53% deemed as income to borrower |
| Loan not repaid within reasonable time | Tax Authority may reclassify as dividend (30% tax + potential penalties) |
| Loan used for personal expenses | Strengthens reclassification risk |
| Loan has no repayment schedule | Red flag for Tax Authority |
| Company has retained earnings | Increases risk of deemed dividend reclassification |

**When shareholder loan makes sense:**
- Short-term cash need (under 12 months) with clear repayment plan
- Bridge financing until dividend declaration is approved
- The 6.53% deemed interest cost is lower than the tax on alternative extraction
- Company has a formal loan agreement with interest and repayment terms

**When to avoid shareholder loans:**
- Long-term extraction need (will accumulate deemed interest annually)
- Company has distributable retained earnings (Tax Authority will challenge the loan structure)
- No documented loan agreement or repayment schedule
- Existing shareholder loan balance is already significant

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
| Up to 7,122 NIS/month | 2.87% | 3.1% | 5.97% |
| 7,122 - 47,465 NIS/month | 12.83% | 5.0% | 17.83% |

Note: 52% of the NI amount is tax-deductible.

**Advantages:**
- Can deduct business expenses (office, car, phone, travel) against the fees
- More flexibility in timing of income recognition
- Can employ family members in the management entity

**Disadvantages:**
- VAT (18%) applies on the gross fee (though offset if company is also osek murshe)
- Self-employed NI rates are higher than employee rates
- Tax Authority may challenge "excessive" management fees as disguised dividends
- Requires maintaining a separate business entity with bookkeeping
- Transfer pricing rules apply (Section 85A) -- fees must reflect market rates

**When management fees work:**
- Shareholder has legitimate business expenses to offset
- Amount is reasonable relative to services provided
- Properly documented with service agreements

### Step 7: Compare Strategies Side by Side

Use this framework to compare extraction methods for the user's specific situation:

**Decision matrix:**

| Factor | Salary | Dividend | Loan | Management Fees |
|--------|--------|----------|------|-----------------|
| Total effective tax rate | Variable (10%-60%) | 46.1%-51.95% | 6.53% deemed/year | Variable + 18% VAT |
| Bituach Leumi | Yes (capped) | No | No | Yes (higher rates) |
| Corporate tax deductible | Yes | No | N/A | Yes |
| Pension benefits | Yes | No | No | Self-funded |
| Reversible | No | No | Yes (repay loan) | No |
| Tax Authority scrutiny | Low | Low | High | Medium |
| Timing flexibility | Monthly | Board resolution | Immediate | Per invoice |
| Minimum salary requirement | ~6,500 NIS/month for controlling shareholders | None | None | None |

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
| Board resolution for dividends | Required before distribution, must be documented |
| Loan agreement for shareholder loans | Written agreement with interest rate, repayment schedule, and signatures |
| Minimum salary for controlling shareholder | Tax Authority expects reasonable salary (~6,500+ NIS/month) before dividends |
| Withholding tax on dividends | Company must withhold 30% and deposit with Tax Authority by the 15th of the following month |
| Form 856 reporting | Payments to shareholders must be reported |
| Section 3(tet) reporting | Deemed interest must be reported on Form 126 |
| Transfer pricing for management fees | Fees must reflect arm's length market rates |
| VAT invoice for management fees | Must issue tax invoice (heshbonit mas) |
| Surtax reporting | Include all income sources when calculating surtax threshold |

**Always recommend:**
- Consult with a licensed Israeli CPA (roeh heshbon) or tax advisor (yoetz mas) before executing any strategy
- The analysis provides a framework for informed discussion with professionals, not a substitute for professional advice

## Gotchas

1. **Wrong dividend tax rate.** AI agents frequently use 25% dividend tax for all shareholders. For controlling shareholders (baal shlita, 10%+ holding), the rate is **30%**, not 25%. This 5% difference on a 500,000 NIS dividend = 19,250 NIS error.

2. **Ignoring the double taxation on dividends.** Agents often quote 30% as the total dividend tax. The real burden is 23% corporate tax + 30% on the remaining 77% = **46.1% effective rate**. Quoting just 30% understates the cost by over 50%.

3. **Section 3(tet) interest rate confusion.** The deemed interest rate changes annually. For 2026 it is **6.53%** (Section 3(tet)) and **4.9%** (Section 3(yod) for CPI-linked loans). Using old rates or confusing the two sections produces wrong calculations. Always specify the tax year.

4. **Forgetting Bituach Leumi on salary.** When comparing salary vs dividend, agents often compare only income tax rates. Salary carries an additional ~12% employee NI+health and ~7.38% employer NI (for controlling shareholders), which significantly changes the breakeven point. The NI ceiling (47,465 NIS/month) is also frequently missed.

5. **Mixing up controlling shareholder NI rates.** Controlling shareholder employees (baalei shlita) have slightly different NI rates (employer: 4.46%/7.38%) than regular employees (4.51%/7.60%). Using regular rates for a baal shlita produces incorrect calculations and may trigger audit questions.

## Bundled Resources

- `references/tax-rates-2026.md` -- Complete 2026 tax rates: income brackets, corporate tax, dividend rates, NI rates, surtax thresholds, credit point value, Section 3(tet) rates
- `references/extraction-methods.md` -- Detailed comparison of salary, dividend, loan, and management fee extraction with worked examples
- `references/section-3tet-rules.md` -- Section 3(tet) and 3(yod) deemed interest rules, reclassification risks, documentation requirements
- `scripts/tax_comparison.py` -- Interactive Python calculator: input company profit and shareholder details, outputs side-by-side comparison of all extraction methods with total tax burden

## Recommended MCP Servers

| MCP Server | What It Adds |
|------------|-------------|
| [kolzchut](https://agentskills.co.il/he/mcps/kolzchut) | Look up tax rights, entitlements, and eligibility criteria from Israel's authoritative rights database |

## Reference Links

Official sources for verifying and updating the tax figures in this skill:

| Source | URL | What to Check |
|--------|-----|---------------|
| Israeli Tax Authority (Reshut HaMisim) | https://www.gov.il/he/departments/israel_tax_authority | Official tax rates, forms, circulars |
| Income Tax Ordinance | https://www.nevo.co.il/law/70264 | Legal text for Section 3(tet), Section 121B (surtax), Section 32(9) |
| Bituach Leumi -- Contribution Rates | https://www.btl.gov.il/Insurance/National%20Insurance/Pages/default.aspx | Current NI and health insurance rates |
| Section 3(tet) Annual Rate | https://www.capitax.co.il | Published annually, usually in December for the following year |
| Kolzchut -- Tax Rights | https://www.kolzchut.org.il/he/%D7%9E%D7%93%D7%A8%D7%92%D7%95%D7%AA_%D7%9E%D7%A1_%D7%94%D7%9B%D7%A0%D7%A1%D7%94 | Income tax brackets, credit points, updated annually |
| CWS Israel -- Tax Guide | https://www.cwsisrael.com/israeli-tax-changes-2026-complete-guide/ | English-language summary of annual tax changes |

## Troubleshooting

### "I need to pay a tax assessment (shuma) urgently"

If the user has received a tax assessment and needs to pay immediately using company funds:
1. **Short-term:** Shareholder loan with formal agreement is the fastest option (no board resolution needed, just a loan agreement)
2. **Within 30 days:** Plan a dividend distribution with board resolution
3. **Document everything:** Written loan agreement even for temporary borrowing
4. **Repayment plan:** Convert the loan to a dividend within the tax year to avoid accumulating Section 3(tet) deemed interest

### "Which method should I use for a one-time large amount?"

For a one-time extraction of 500,000+ NIS:
1. Check current salary level and marginal bracket
2. If salary is already above 228,000/year: dividend is likely optimal
3. If salary is low: increase salary to fill lower brackets, dividend for the rest
4. If timing is urgent: shareholder loan as bridge, convert to dividend within 90 days

### "The Tax Authority questioned my shareholder loan"

If the Tax Authority (pakid shuma) challenges a shareholder loan:
1. Present the formal loan agreement with interest terms
2. Show repayment history or schedule
3. Demonstrate business purpose for the loan
4. If loan was used for personal tax payment: be prepared for reclassification as dividend
5. Consult with tax advisor immediately
