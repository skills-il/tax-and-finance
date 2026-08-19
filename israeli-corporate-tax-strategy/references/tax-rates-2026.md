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

The 52% rate includes: 47% base + 3% surtax + 2% additional surtax on non-labor income (effective 2025).

## Surtax (Mas Yesafim, Section 121B)

- Threshold: **721,560 NIS** annual income (all sources combined)
- Rate: **3%** on all income above threshold
- Additional **2%** on non-labor income (dividends, interest, capital gains, rental) above threshold
- Total surtax on non-labor income above threshold: **5%**

## Dividend Tax

### Ordinary (non-benefit-track) company profits, Section 125B of the Ordinance

| Shareholder Type | Tax Rate |
|-----------------|----------|
| Non-controlling (under 10% holding) | 25% |
| Controlling shareholder (10%+ holding, baal shlita) | 30% |
| With surtax (above 721,560 threshold) | +3% + 2% = +5% |

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
| Up to 7,703 NIS/month | 1.04% | 3.23% | 4.46% |
| 7,703 - 51,910 NIS/month | 7.0% | 5.17% | 7.38% |
| Above 51,910 NIS/month | 0% (ceiling) | 0% (ceiling) | 0% (ceiling) |

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

Amendment 277 to the Income Tax Ordinance restructured taxation of closely-held companies (chevrot meatim):

- **2% additional corporate-tax surcharge** on excess undistributed retained earnings of a closely-held company. A protective cushion applies: the higher of a ~750,000 NIS fixed exemption, a deductible-expense shield, or an asset shield. **Safe harbor:** a company that distributes at least 6% of its accumulated profits during the year (reduced to 5% for 2025 only) avoids the surcharge entirely. This distribution lever, not the raw 2%, is the actual planning decision in retain-vs-distribute.
- **Section 62A tightened.** The material-shareholder trigger stays at 10%+ holding of the closely-held company. What changed: the carve-out for a service provider who also holds a stake in the *client* (recipient) entity was raised from 10% to 25% (you must now hold 25%+ of the recipient to escape attribution, so mid-size 10-25% stakes that used to be safe are now caught); the single-client test was compressed to 22 months within 3 tax years (was 30 months within 4 tax years); and a new limb (Section 62A(a1)) attributes profits above a 25% margin on personal-effort revenue to the shareholder at marginal rates regardless of distribution.
- **+2% surtax on non-labor income** above the 721,560 threshold (in addition to the standard 3% Section 121B surtax). Note: this 2% was enacted by the Economic Efficiency Law (Freezing of Tax Updates and Surtax) 5785-2024, a separate statute from Amendment 277, effective for tax year 2025 onward.

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
