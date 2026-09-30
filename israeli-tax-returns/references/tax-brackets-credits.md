# Israeli Income Tax Brackets and Tax Credits Reference

## Income Tax Brackets (Tax Year 2025)

Use these for a 2025 return, which is what is being filed during 2026. Values frozen at their 2024 levels (ITA 2025 annual deductions booklet).

| Bracket | Annual Income Range (NIS) | Marginal Rate |
|---------|--------------------------|---------------|
| 1 | 0 - 84,120 | 10% |
| 2 | 84,121 - 120,720 | 14% |
| 3 | 120,721 - 193,800 | 20% |
| 4 | 193,801 - 269,280 | 31% |
| 5 | 269,281 - 560,280 | 35% |
| 6 | 560,281 and above | 47% |
| Surtax | Above 721,560 | 47% + surtax |

For earlier tax years (a Form 135 refund claim can reach back six years), take the table from that year's ITA annual booklet.

## Income Tax Brackets (2026)

These brackets apply to active income (employment, self-employment, business income) for Israeli tax residents. Brackets 3-5 were expanded by the Economic Efficiency Law 2026 (Amendment 288 to the Income Tax Ordinance, approved March 31, 2026, retroactive to January 1, 2026). Brackets 1-2 and 6 remain frozen at 2025 values.

| Bracket | Annual Income Range (NIS) | Monthly Equivalent (NIS) | Marginal Rate |
|---------|--------------------------|--------------------------|---------------|
| 1 | 0 - 84,120 | 0 - 7,010 | 10% |
| 2 | 84,121 - 120,720 | 7,011 - 10,060 | 14% |
| 3 | 120,721 - 228,000 | 10,061 - 19,000 | 20% |
| 4 | 228,001 - 301,200 | 19,001 - 25,100 | 31% |
| 5 | 301,201 - 560,280 | 25,101 - 46,690 | 35% |
| 6 | 560,281 and above | 46,691 and above | 47% |
| Surtax | Above 721,560 | Above 60,130 | 47% + surtax, see Surtax section |

The 47% band does NOT stop at 721,560. It applies to every shekel above 560,280, and the
surtax is charged ON TOP of it, which is why the effective top marginal rate is 50% rather
than the surtax rate on its own. Reading the last two rows as consecutive bands
under-reports tax on high earners by 47 points on every shekel above the threshold.

**Note:** Brackets 1-2 and 6 are frozen (not inflation-adjusted). This effectively increases the real tax burden as wages rise with inflation.

## Corporate Tax Rate

| Entity Type | Rate | Notes |
|-------------|------|-------|
| Standard company (Chevra) | 23% | Flat rate on taxable profits |
| Closely held company (Chevra Me'atim) | 23% + 2% on undistributed profits | 2% avoidable by distributing 6% of accumulated profits as dividends |

## Capital Gains Tax Rates

| Asset Type | Rate | Notes |
|------------|------|-------|
| Listed securities (individual) | 25% | Standard rate |
| Listed securities (substantial shareholder 10%+) | 30% | Higher rate for controlling stakes |
| Real estate (Mas Shevach) | 25% | On real gain after inflation adjustment |
| Real estate (qualifying apartment, gain up to 1.1.2014, linear method) | Exempt | s.48A(b2); still in the consolidated statute as of October 2026 |

## Surtax (Mas Yesafim), Two-Tier System from Tax Year 2025

- **Threshold:** Annual taxable income above 721,560 NIS (2025-2027, frozen)
- **All taxable income:** 3% on the excess above the threshold (effective top rate on employment income: 50%)
- **Income from capital sources** (anything other than salary and personal-exertion income): a further 2% on the excess, so 5% in total. Section 121B(a1), added by Amendment 276 (Economic Efficiency Law 2025), in force from tax year 2025
- **Real-estate gain (shevach)** is part of surtax income under the Section 121B definition. For a residential apartment it counts only if the sale value exceeds 5,382,285 NIS (2025) and the sale is not exempt, so an exempt single-residence sale never counts. This predates 2025; the proposal to drop the apartment carve-out was removed from the final 2025 law

## Nekudot Zikui (Tax Credit Points)

### Value Per Point
- **2025-2027:** 2,904 NIS per year (242 NIS per month), frozen (not inflation-adjusted)

### The credit-point schedule lives in `credit-points.md`

**The full schedule was moved out of this file and corrected.** Every category, every child age
band, both combat-reserve regimes, the oleh and returning-resident tracks, discharged soldiers,
netul yecholet, Section 44 and Section 11 are in `references/credit-points.md`, each with its
statutory citation. Read that file; do not reconstruct a table here.

Headline corrections made in v1.9.0, because the superseded values in this file were being
quoted:

| Item | Superseded value that was here | Correct value |
|---|---|---|
| Child born in the tax year | 1.5 | 2.5 |
| Child aged 1-2 | folded into a flat "ages 1-5 = 2.5" | 4.5 |
| Child aged 3 | folded into a flat "ages 1-5 = 2.5" | 3.5 |
| Child aged 6-17 | 1.0 for both parents | 2.0 mother / 1.0 father |
| New immigrant | 3.0 / 2.0 / 1.0 over 3.5 years | 1 / 3 / 2 / 1 over 54 months, 8.5 points total (s.35(a)) |
| Returning resident | same as oleh | s.35(d) covers only those who resumed residency 16.5.2010 to 30.9.2012 |
| Combat reserve | 0.5 / 0.75 / 1.0, max 1.0 | Max 4.0; 2026-2027 bands start at 30 days, permanent bands from 2028 start at 20 days (s.39B, ITA circular 2025-001368) |
| Discharged soldier | absent | 2.0 points per year for 3 years, or 1.0 for shorter service (s.39A) |

## Rental Income Tax Tracks (Residential)

| Track | Tax Rate | Key Rules |
|-------|----------|-----------|
| Exempt | 0% | Monthly rent below ceiling (5,654 NIS/month, 2025-2027, frozen, no longer indexed). No expenses deductible. |
| Flat rate | 10% | On gross rent. No expenses deductible. Pay within 30 days after the end of the tax year (s.122(a1)). |
| Regular | From 31% under age 60 | Rent is not personal-exertion income, so a filer under 60 starts at 31% (s.121(a)); the 10%/14%/20% bands apply only from age 60. Full expense deduction (depreciation, mortgage interest, maintenance). Report with Form 1301. |

## Real Estate Tax Exemptions

### Single Apartment Exemption (Ptur Dira Yechida)
- Sale price below 5,008,000 NIS (2024-2027 ceiling, frozen)
- Seller's only residential property in Israel
- Owned for at least 18 months
- Seller is an Israeli resident
- Partial exemption applies proportionally above the ceiling

### Linear Method (Shita Liniarit)
- For a qualifying residential apartment bought before 1 January 2014 that does not get the full exemption
- The real gain up to 1.1.2014 is exempt; the rest is taxed at the regular rate (s.48A(b2))
- Separately, any property bought before 1.1.2012 has its real gain split by period: up to 7.11.2001 at the top s.121 rate, then to 1.1.2012 at up to 20%, then 25% (s.48A(b1))
- Phase-out proposed by the Ministry of Finance in 2024; the provision is still in the consolidated statute as of October 2026

## Key Filing Deadlines

| Obligation | Deadline | Penalty for Late Filing |
|------------|----------|------------------------|
| Form 1301 (individual) | 2025 return: 30.6.2026 online / end of May 2026 paper (statutory baseline 30 April); CPA-represented: quota schedule, final stage 28.2.2027 | Interest + linkage differences + potential fines |
| Form 1214 (corporate) | Statutory 31 May; 2025 returns extended to 30.7.2026; CPA-represented: final stage 31.3.2027 | Interest + linkage differences + potential fines |
| Form 126 (employer) | April 30 | Administrative fines |
| Form 106 (to employees) | 31 March | Administrative fines |
| Mikdamot | 15th of month after period | Interest on late payment |
| Mas Shevach declaration | 30 days from sale, exemption claims included; tax payable within 60 days | Interest + linkage + fines |
| Rental income (10% track) | Within 30 days after the tax year ends | Interest on late payment |

## Section 46 donation credit (2026)

| Item | Value |
|------|-------|
| Credit rate, individuals | 35% of the eligible donation |
| Credit rate, companies | corporate rate, 23% |
| Minimum floor | 207 NIS of COMBINED donations in the year (200 in 2023; 190 in 2020-2022) |
| Ceiling | lower of 10,354,816 NIS (2026) or 30% of taxable income |
| Excess above ceiling | carried forward up to 3 tax years |

The floor applies to the year's combined total across Section 46 institutions, not to each
donation separately. Checking donations one at a time is the common way a valid claim gets
wrongly disqualified.
