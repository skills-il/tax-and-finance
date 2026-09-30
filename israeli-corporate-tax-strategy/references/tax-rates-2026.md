# Israeli Tax Rates 2026

All figures verified against official Israeli Tax Authority publications and Kolzchut.

## Corporate Tax

- Standard rate: **23%** (Section 126(a) of the Income Tax Ordinance)

### Benefit tracks under the Law for Encouragement of Capital Investments, 5719-1959

Five distinct rate sets, each with its own eligibility gate. A company that holds one of these
statuses is NOT taxed at 23% on its qualifying income, and treating it as if it were roughly
doubles the modelled corporate-tax layer. The technology tracks (PTE / SPTE) are the ones that
cover ordinary Israeli software and tech companies.

| Track (Hebrew) | Development Area A | Elsewhere | Statute |
|---|---|---|---|
| Preferred Enterprise, מפעל מועדף (PFE) | 7.5% | 16% | s.51טז |
| Special Preferred Enterprise, מפעל מועדף מיוחד (SPFE) | 5% | 8% | s.51כא(a) |
| Preferred Technology Enterprise, מפעל טכנולוגי מועדף (PTE) | 7.5% | 12% | s.51כה(1)-(2) |
| Special Preferred Technology Enterprise, מפעל טכנולוגי מועדף מיוחד (SPTE) | 6% | 6% | s.51כה(3) |

The reduced rate applies only to the track's *qualifying* income (preferred income / qualifying
technological income), and for the technology tracks only to the share of the intangible asset
developed in Israel, on a nexus basis. A company with mixed IP origin or mixed activity carries a
blended rate, not the headline rate. Non-qualifying income stays at 23%.

The SPTE rate is a single 6% with no area split. The SPFE rate applies for ten years, after which
the PFE rates apply unless a new investment programme requalifies the company.
- 2% additional tax on excess retained corporate profits of a closely-held company not distributed as dividends (Amendment 277; see the Trapped Profits section below for the protective cushion and the 6% distribution safe harbor that avoids it)

## Income Tax Brackets (Earned Income, 2026)

The 20% and 31% band ceilings were widened for 2026 by Amendment 288 to the Income Tax Ordinance (enacted 31 March 2026, retroactive to January 1, 2026). The credit-point value and the surtax threshold (721,560) were NOT indexed, they stay frozen 2025-2027 under the Economic Efficiency Law, which is why only the middle rungs move while the top of the ladder holds.

| Annual Income (NIS) | Monthly Income (NIS) | Tax Rate |
|---------------------|---------------------|----------|
| 0 - 84,120 | 0 - 7,010 | 10% |
| 84,121 - 120,720 | 7,011 - 10,060 | 14% |
| 120,721 - 228,000 | 10,061 - 19,000 | 20% |
| 228,001 - 301,200 | 19,001 - 25,100 | 31% |
| 301,201 - 560,280 | 25,101 - 46,690 | 35% |
| 560,281 - 721,560 | 46,691 - 60,130 | 47% |
| Above 721,560 | Above 60,130 | 50% |

Note: The 50% top rate includes the base 47% rate plus 3% surtax (Section 121B).

## Income Tax Brackets (Non-Labor Income, Under Age 60)

| Annual Income (NIS) | Tax Rate |
|---------------------|----------|
| 0 - 301,200 | 31% |
| 301,201 - 560,280 | 35% |
| 560,281 - 721,560 | 47% |
| Above 721,560 | 52% |

The 52% rate includes: 47% base + 3% surtax + 2% additional surtax on capital-source income (effective 2025). The 3% applies once TOTAL income passes 721,560; the extra 2% applies only on the part of CAPITAL income alone above 721,560, so the full 52% bites only when capital income by itself exceeds the threshold.

## Surtax (Mas Yesafim, Section 121B)

- Threshold: **721,560 NIS** a year, frozen for 2025-2027
- **3%** (s.121B(a)) on TOTAL taxable income above the threshold, all sources combined
- **2% more** (s.121B(a1), added by Amendment 276, from tax year 2025, permanent) on capital-source income (dividends, interest, capital gains, rent) above the threshold, measured on that capital income ALONE. Salary does not use up the threshold for this limb. ITA execution instruction 5/2025, example 3.2: salary 400,000 plus dividends and interest of 700,000 owes the 3% but not the 2%, because capital income (700,000) is below 721,560.
- Total surtax on capital income: **5%**, but only on the slice by which capital income itself exceeds 721,560

## Dividend Tax

### Ordinary (non-benefit-track) company profits, Section 125B of the Ordinance

| Shareholder Type | Tax Rate |
|-----------------|----------|
| Non-controlling (under 10% holding) | 25% |
| Controlling shareholder (10%+ holding, baal shlita) | 30% |
| With surtax | +3% once total income passes 721,560; +2% more once capital income alone passes 721,560 |

### Profits of a company holding a benefit track

These rates displace Section 125B, so the 25% / 30% split by holding percentage does not apply to
this income. They are the source of the single largest modelling error in this domain: a tech
company distributing PTE profits pays 20%, not 30%.

| Source of the distributed profit | Withholding rate | Statute |
|---|---|---|
| Preferred income (PFE and SPFE) | 20% | s.51יח |
| Qualifying technological income (PTE and SPTE) | 20% | s.51כו(1) |
| Qualifying technological income distributed to a foreign-resident body corporate, where 90% or more of the payer's shares are held directly by one or more foreign-resident bodies corporate (further conditions in s.51כו(2)(b)) | 4% | s.51כו(2) |

Treaty rates may reduce these further for a non-resident recipient. Where shares are held
indirectly through another company, the 4% rate applies only if that other company on-distributes
the dividend to the foreign-resident body corporate within one year of receiving it.

## Tax Credit Points (Nekudot Zikui)

- Value per point: **242 NIS/month** (2,904 NIS/year)
- Frozen at this level for 2025-2027
- Base entitlement: 2.25 points for Israeli residents
- Additional 0.5 points for women

## Bituach Leumi (National Insurance) Rates

### Controlling Shareholder Employees (Baalei Shlita)

| Income Range | Employee NI | Employee Health | Employer NI |
|-------------|------------|----------------|-------------|
| Up to 7,703 NIS/month | 1.02% | 3.23% | 4.46% |
| 7,703 - 51,910 NIS/month | 6.79% | 5.17% | 7.38% |
| Above 51,910 NIS/month | 0% (ceiling) | 0% (ceiling) | 0% (ceiling) |

Employee total with health: 4.25% / 11.96% (BTL rate table, column 2, "בעל שליטה בחברת מעטים").

### Regular Employees (for comparison)

| Income Range | Employee NI | Employee Health | Employer NI |
|-------------|------------|----------------|-------------|
| Up to 7,703 NIS/month | 1.04% | 3.23% | 4.51% |
| 7,703 - 51,910 NIS/month | 7.0% | 5.17% | 7.60% |

### Self-Employed

| Income Range | NI Rate | Health Rate | Total |
|-------------|---------|-------------|-------|
| Up to 7,703 NIS/month | 4.47% | 3.23% | 7.70% |
| 7,703 - 51,910 NIS/month | 12.83% | 5.17% | 18.00% |

52% of NI amount is tax-deductible (Section 47A).

### Controlling Shareholder With Zero Salary (BL Minimum)

A baal shlita drawing no salary still owes Bituach Leumi directly as a non-employee with no taxable employment income. 2026 minimums:

| Component | Monthly Minimum |
|-----------|-----------------|
| NI | ~143 NIS |
| Health | ~123 NIS |
| Combined floor | ~266 NIS |

Liability sits on the individual, not the company. If the shareholder has non-employment income (dividends, rental, interest, capital gains), percentage-based rates apply on that income above the floor.

## Section 3(tet) and 3(yod) Deemed Interest Rates (2026)

- Section 3(tet): **6.53%** (for non-CPI-linked loans)
- Section 3(yod): **4.9%** (for CPI-linked loans between related parties)

## VAT

- Standard rate: **18%** (increased from 17% on January 1, 2025)

## Trapped Profits / Closely-Held Company Reforms (Amendment 277, in force 2025)

Amendment 277 to the Income Tax Ordinance (enacted 31 December 2024, in force 1 January 2025) restructured taxation of closely-held companies (chevrot meatim, s.76(a)). The ITA explains it in circular 7/2025 and its update 1 (8 February 2026); reporting is in execution instruction 9/2026 (15 September 2026).

### The 2% surcharge on undistributed profits (ss.81A-81F)

- **Charge (s.81B(a)).** 2% a year on the company's excess profits (s.81C), after deducting dividends distributed in the year. It is treated like corporate tax but is not creditable against it (s.81F(a)) and is not deductible (s.81D). Israeli-resident companies only.
- **Accumulated profits (s.77(a) as amended).** The LOWER of the tax-basis figure (taxable plus exempt income, less tax paid, dividends and unset losses, since incorporation) and the financial-statement alternative.
- **Excess profits (s.81C).** Accumulated taxable profits minus exempt accumulated profits and minus the HIGHEST of: a monetary shield of **NIS 750,000** (shared among companies under common control), an expense shield (the higher of the tested year's recognised expenses or their average over that year and the two before it), or an asset shield (cost of company assets less "special assets", share capital and related items). Special assets include securities, financial assets including cash, intangibles, real-estate rights and loans, so a cash-rich company or one holding shareholder loans gets little asset shield. A company whose accumulated profits are under 750,000 does not even fill in the reporting appendix.
- **No surcharge in a year where any exit in s.81B(b) is met:**
  1. current losses exceed 10% of the accumulated profits at the end of the previous year;
  2. taxed dividends exceed 50% of the excess profits at the end of the previous year (the "50% alternative");
  3. taxed dividends are 6% or more of the accumulated profits at the end of the previous year (the "6% alternative").
- **Which dividends count.** Any dividend distributed in the tested year counts, except an intercompany dividend exempt under s.126(b), which counts only if the paying company elects to withhold at the top dividend rate (35% in 2025) under the 2025 regulations explained in circular 02/2026. A dividend paid under the s.62A "dividend alternative" does not count toward the s.81B tests (execution instruction 9/2026). For the intercompany route, circular 02/2026 s.4.2 sets payment of the tax on a December distribution by 16 January of the following year.
- **2025 transition (expired).** For 2025 only, taxed dividends of 5% of accumulated profits in the determining period sufficed, provided the tax was paid by 31/12/2025. From 2026 the 6% test applies. Circular 7/2025 s.6 also sets conditional transitional rules for profits accumulated before 2025; they carry distribution conditions of their own, so read them with the company's CPA before relying on them.
- **Reporting.** Form 1214 with appendix 1281; the accumulated-profits figure goes to field 169.

### Section 62A (personal-services companies)

- The holder test moved from "material shareholder" (s.88) to "controlling holder" (בעל שליטה, s.75B(a)(3)): an Israeli resident holding 10%+ of any means of control, directly or indirectly.
- **s.62A(a)(1), officer or management services to another company:** the exit now needs a 25%+ holding in the client on some day in the tax year (was 10%).
- **One-client rule:** 70%+ of the company's income from one client over 22 months within 3 tax years (was 30 months within 4). The exclusion for a company employing four or more employees is unchanged.
- **New s.62A(a1), excess profitability:** where profitability on personal-exertion activity exceeds 25%, taxable income above the 25% margin is attributed to the active shareholder under s.2(1) (Bituach Leumi applies, BL circular 1487). It does not apply where personal-exertion turnover is at least NIS 30 million times the number of controlling holders, or where the holder's accumulated profits across all his companies did not exceed NIS 750,000 at the end of the previous year.
- A closely-held company that is a partner in a partnership: at a 10%+ partnership share the 25% margin rule applies; below 10%, 55% of its share is attributed to the individual.

### Surtax on capital income

The +2% surtax on capital-source income is a separate amendment (Amendment 276, s.121B(a1)); see the Surtax section above for how its threshold is measured.

## Benefit-Track Temporal Cohorts (which version of the table governs)

Entitlement under the Encouragement Law is selected by the **approval / election date of the
programme**, not by the tax year being computed. A company can sit on a superseded rate table
today and be entirely correct to do so. Ask which regime the company is in before applying any
rate above.

### Selection rule (Amendment 68, transitional s.39)

| Cohort | Governing regime | Selection trigger |
|---|---|---|
| Preferred Enterprise regime | Sections 51טז-51כג as in force today | Preferred income produced or accrued from 1 January 2011 onward (s.39(a)) |
| Approved Enterprise, מפעל מאושר (grant track) | Pre-2011 law, through the cooling period, and by election to the end of the benefit period under s.45 | Included in a programme the Investment Center approved before 1 January 2011, and the cooling period from the start of the operating year has not elapsed (s.39(b)). Cooling period is 3 years for a programme approved before 1 April 2005 and 5 years after that date |
| Beneficiary Enterprise, מפעל מוטב | Pre-2011 sections 40יא and 51א to 51יד | Qualifying minimum investment made wholly or partly by 31 December 2010, and the company declared a year of election no later than tax year 2012 (s.39(e)(1)) |
| Either of the above, having opted in | Current Preferred / Special Preferred regime | An irrevocable waiver notice (הודעת ויתור) on the Tax Authority form. For Approved Enterprises the opt-in window closed 30 June 2011 (s.39(c)); a Beneficiary Enterprise files by the annual-return deadline and it applies from the following tax year (s.39(e)(2)) |

### Superseded Preferred Enterprise rate tables

Still relevant for an assessment, objection, or restatement covering an earlier year.

| Tax years | Development Area A | Elsewhere | Dividend from preferred income |
|---|---|---|---|
| 2011-2012 | 10% | 15% | 15% |
| 2013 | 7% | 12.5% | 15% |
| 2014-2016 | 9% | 16% | 15% |
| 2017 onward | 7.5% | 16% | 20% |

The Area A rate moved 9% to 7.5% and the dividend rate 15% to 20%, both by Amendment 73, effective
1 January 2017. The technology tracks (PTE / SPTE) were themselves created by Amendment 73 and have
no pre-2017 cohort.

Out of scope for this skill: the detailed eligibility tests for each track, the pre-2011 Approved
Enterprise alternative-benefits track (מסלול הטבות חלופי) rate schedule, and the s.51כז capital-gains
rates on IP sales. A company in those fact patterns needs its own analysis; this skill covers the
extraction decision once the applicable corporate rate is known.

## Pension and Keren Hishtalmut Ceilings (2026 reference)

| Item | 2026 Value |
|------|-----------|
| Keren Hishtalmut, self-employed deductible ceiling | 13,203 NIS/year |
| Keren Hishtalmut, exempt annual deposit ceiling | 20,566 NIS |
| Keren Hishtalmut, salaried max qualifying monthly salary | 15,751 NIS/month |

## Key Thresholds

| Threshold | 2026 Value |
|-----------|-----------|
| Surtax threshold | 721,560 NIS/year |
| NI maximum insurable income | 51,910 NIS/month |
| Rental income exempt ceiling | 5,654 NIS/month (frozen 2025-2027) |
