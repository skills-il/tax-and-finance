---
name: israeli-pension-advisor
description: "Navigate the Israeli pension and savings system including pension funds (keren pensia), manager's insurance (bituach menahalim), training funds (keren hishtalmut), severance handling at Form 161, Tikun 190 post-60 deposits, and retirement planning. Use when user asks about Israeli pension, \"pensia\", \"keren hishtalmut\", retirement savings, \"bituach menahalim\", pension contributions, tax benefits from savings, severance withdrawal vs continuity, or pension at divorce / relocation. Uninformed pension decisions cost hundreds of thousands of NIS over a lifetime. Covers mandatory pension, voluntary savings, withdrawal rules, and life events (divorce, relocation, death). Do NOT provide specific investment recommendations or fund performance comparisons."
license: MIT
compatibility: No network required.
---

# Israeli Pension and Savings Navigator

## Legal notice

This is a free information tool operated by an AI model. It explains the Israeli pension and long-term savings system and presents rules and data that have been published to the public. All of its outputs are produced automatically by an AI model, with no involvement, review, or approval by a licensed pension adviser. The output is not pension advice, not pension marketing, and not a personal recommendation about the merits of your savings, but a general explanation only: it does not examine your personal circumstances, the full set of pension products you hold, or your particular needs. An AI model may err, omit data, or present a wrong conclusion.

The output must not be relied on to transfer funds, change an investment track, withdraw severance money, or make any other pension decision. This tool is not a substitute for advice that takes account of the particular circumstances and needs of each person. Before any such decision, consult a licensed pension adviser and verify every figure with the managing institution. All use of its output is the user's sole responsibility.


## Critical Note
This skill provides general pension INFORMATION. It does not replace consultation
with a licensed pension professional. Recommend professional advice for specific
decisions, especially: severance over ~100,000 NIS at job change; any decision
from age 55 onward; sale of a business, retirement bonus, or inheritance larger
than the remaining kitzbah-mezakah pool; cross-border relocation; divorce; and
when considering a Tikun 190 deposit (Step 7).

Under the Pension Advice Law 2005 a *yoetz pensioni* (pension adviser) has no affiliation to the product, but may receive a distribution fee from the institutional body if the client agrees in advance and in writing (s.19(a)(2)); a *sokhen pensioni* (pension agent) is affiliated. Tell users to ask any adviser how they are paid.

## Instructions

### Step 1: Identify Savings Type
| Type | Hebrew | Purpose | Tax Benefit |
|------|--------|---------|-------------|
| Keren Pensia | keren pensia | Retirement + disability + survivors | Tax credit + deduction |
| Bituach Menahalim | bituach menahalim | Retirement (insurance-based, declining for new policies since 2013) | Tax credit + deduction |
| Keren Hishtalmut | keren hishtalmut | Medium-term savings (6 years) | Tax-free gains for employees |
| Kupat Gemel le-Tagmulim | kupat gemel le-tagmulim | General savings (historical, mostly closed to new deposits since 2008) | Various |
| Kupat Gemel le-Hashka'a | kupat gemel le-hashka'a | Liquid long-term savings (since 2016 reform); deposits capped at 83,641 NIS/year (2026) | Lump sum at any age: 25% on the real gain; from 60, taken as a monthly pension: exempt |
| Kupat Gemel le-Kitzbah (Tikun 190 vehicle) | kupat gemel le-kitzbah | Post-60 tax-shelter (see Step 7) | Full exemption as kitzbah from 60, 15% on the nominal gain as lump sum |
| Kranot Neemanot | kranot neemanot | Mutual funds (not pension) | Capital gains tax |

### Step 2: Mandatory Pension Contributions
Since 2008, all employees must have pension insurance. Statutory average wage (sakhar memutza) as published for 2026 by the Tax Authority and used by National Insurance: 13,769 NIS/month. This is the base figure for nearly every pension ceiling. (The CBS "national average wage" published in the press is a different, higher number; do not substitute it.)

**Employee contributions:**
- **Employee:** 6% of salary
- **Employer pension (tagmulim):** 6.5% of salary (includes disability-insurance component up to 2.5%)
- **Employer severance (pitzuim):** 6% of salary (mandatory minimum); 8.33% under full Section 14 (see Step 6)
- **Total mandatory minimum:** 18.5% of salary
- **Three different ceilings, do not merge them.** All three are multiples of the
  same average wage (13,769 NIS in 2026), which is why they get confused:

| Ceiling | 2026 | Limits |
|---------|------|--------|
| Mandatory-pension insurable salary (tzav harchava) | 13,769 (the average wage itself) | The salary the compulsory 18.5% must be paid on |
| Comprehensive-fund tax-favoured deposit | 5,645/month, being 20.5% of twice the average wage | The favoured monthly deposit; beyond it, route to a keren mashlima or kupat gemel le-tagmulim |
| Comprehensive-fund maximum determining salary | about 41,307 (three times the average wage) | The cap the fund applies to entitlements |

  "Contributions above 2x the average wage route elsewhere" collapses the first
  two and states the mandatory ceiling at double its real value. The mandatory
  ceiling is the average wage, NOT twice it.

- **Not one of these: the Bituach Leumi maximum insurable income (51,910
  NIS/month from 01.01.2026)**, which governs only BL and health contributions.
  When a user names "the insurable salary ceiling" without qualifying it, ask
  which of these four they mean before computing anything.

**Pension contribution timing for new employees** (Mandatory Pension Expansion Order):
- Employee with existing pension at intake: contributions begin Day 1, paid retroactively after 3 months of work or end of tax year (whichever first).
- Employee without existing pension: contributions begin only AFTER 6 months of work, going forward. The first 6 months are NOT covered retroactively.

**Self-employed mandatory pension** (Economic Efficiency Law 5777-2016, Chapter B, in force 01.01.2017):
- 4.45% on net taxable income up to 6,884.50 NIS/month (half average wage)
- 12.55% on income from 6,884.50 to 13,769 NIS/month (full average wage)
- No obligation on income above full average wage
- Maximum annual mandatory obligation: ~14,044 NIS
- Obligation applies from age 21 until early-retirement age 60 (NOT legal retirement age), both tested at the end of the tax year. Anyone aged 55+ on 01.01.2017 is exempt.
- New-business exemption: a tax year in which fewer than 6 months have passed since first VAT registration as an osek, measured at year end. It is NOT "the first calendar year".
- Obligation is on net taxable income (after deductions), not gross revenue. עוסק פטור and עוסק מורשה are both covered.

### Step 3: Keren Hishtalmut (Training Fund)
The most popular Israeli savings vehicle:

**For employees:**
- **Employee contribution:** Up to 2.5% of salary
- **Employer contribution:** Up to 7.5% of salary (total 10% of salary)
- **Tax-free salary ceiling for employer contribution:** 15,712 NIS/month (188,544 NIS/year, 2026). At the ceiling the combined contribution is 1,571 NIS/month.
- Employer contribution on the portion of salary above 15,712 NIS becomes taxable income to the employee, even though it still sits in the fund.
- **Withdrawal after 6 years:** Tax-free on gains (unique Israeli benefit)
- **Withdrawal after 3 years:** for accredited training (with documentation), or once the employee has reached retirement age. Gains on deposits above the tax-favoured ceiling are not exempt even after 6 years

**For self-employed (two separate ceilings):**
- **Tax deduction from income:** Up to 13,203 NIS/year (4.5% of income up to 293,397 NIS)
- **Profit-exempt ceiling:** 20,566 NIS/year (gains on deposits up to this amount are tax-free after 6 years). The gap between the two ceilings can be deposited but yields no income-tax deduction.

**Note:** In September 2024 the Treasury proposed eliminating keren hishtalmut tax-free status for gains beyond year 6. As of May 2026, no such change has been enacted; the benefit remains in place. Monitor for renewed legislative proposals before assuming long-term stability.

### Step 4: Tax Benefits Summary

**For employees:**
- **Pension tax credit:** 35% credit on employee contributions up to 679 NIS/month (7% of qualifying salary 9,700 NIS, 2026). Maximum credit ~2,852 NIS/year.
- A salaried employee gets NO Section 47 deduction for deposits from insured salary. An extra credit or deduction arises only on NON-insured pay components; separately, loss-of-work-capacity premiums are deductible up to 3.5% of salary.
- **Employer exclusion:** Employer tagmulim is not taxed as employee income up to 7.5% of salary, with salary capped at 34,423 NIS/month (2.5x the average wage). Employer severance deposits are exempt up to the lower of one month's salary or 45,600 NIS per year (2026).

**For self-employed:**
- Tax credit (35%) on contributions up to 12,804 NIS/year (5.5% bracket). The top 0.5% of that credit is lost if loss-of-work-capacity premiums were deducted under Section 32(14)(b); the credit is then 5% instead of 5.5%
- Tax deduction on contributions up to additional 25,608 NIS/year (11% bracket)
- Combined maximum deductible: 38,412 NIS/year (16.5% of qualifying income up to 232,800 NIS/year, ~19,400 NIS/month)
- These tiers apply to a beneficiary member (amit mutav): kitzbah deposits in the year of at least 16% of the annual average wage, 26,436 NIS in 2026. Below that, lower limits apply; see `references/tax-benefits.md`

**Pension payout (at retirement):**
- Monthly pension partially tax-exempt under Tikun 190 (Amendment 190 to the Income Tax Ordinance, 2012), with the schedule re-split by Amendment 275 (December 2024)
- 2026 exemption rate: 57.5%; rising to 62.5% in 2027 and 67% from 2028
- Tax-free pension amount: up to 5,422 NIS/month (2026)
- Qualifying pension threshold (kitzbah mezakah): 9,430 NIS/month
- Lifetime tax-exempt capital pool (kibua zechuyot / yitrat hahon haptura) = 180 times the monthly tax-exempt pension = 180 × 57.5% × 9,430 = 976,005 NIS (the figure the Tax Authority publishes; do not round the monthly 5,422 first, which gives 975,960) for a worker retiring in 2026 (it grows as the exemption rate climbs toward 67% by 2028). Eaten by severance withdrawn under heichum kitzbah at 1.35x per shekel (see Step 6).

### Step 5: Withdrawal Rules
- **Pension:** Men age 67; women in 2026 age 63 years 3 months, rising 3-4 months per cohort to 65 for women born 1970 or later, under the Retirement Age Law 5764-2004 as amended (in force from January 2022, phased over 11 years). The age is set by DATE OF BIRTH, not by calendar year; check the per-cohort table below, never a flat number.

The per-cohort table is in `references/retirement-age-by-cohort.md`.

- **Three distinct retirement ages in Israeli law:** gil zakaut le-kitzbah (60+, early access with conditions); gil prishah (67/63+); gil prishah chovah (67 for both genders, the maximum age at which an employer can require retirement). Do not conflate.
- **Early pension withdrawal:** 35% withholding on tagmulim or marginal rate, whichever higher. Early withdrawal of severance beyond the exempt ceiling is taxed at the marginal rate (up to 47%, plus surtax). Exceptions for disability, low household income, or terminal illness can reduce or remove the tax.
- **Keren hishtalmut:** Tax-free after 6 years; after 3 years for accredited training, or once the employee has reached retirement age. For an EMPLOYEE, early withdrawal taxes the employer's deposits AND the gains at the marginal rate; only the employee's own deposits come back untaxed.
- **Commutation (hivun) of post-2008 pension savings:** a lump sum is possible only if the pension left afterwards (plus other kitzbah-fund and budget pensions, NOT Bituach Leumi) is at least the minimum pension of 5,306 NIS/month (2026); otherwise at most 25% of the pension for up to 5 years. Detail, Bituach Leumi old-age rules and the Form 161ד choice are in `references/approaching-retirement.md`; read it for any user within about 5 years of retirement. Public-sector budget pensions (pensia taktziveet) follow different rules: ask before applying this skill's figures.
- **Severance (pitzuim):** On termination, subject to the Section 14 arrangement and the Form 161 process. Tax-exempt up to 13,750 NIS per year of service. See Step 6 in full before any withdrawal decision.
- **Disability:** New comprehensive pension funds under the unified regulations (takanon achid, June 2018) pay up to 75% of insured salary for disability. Bituach Leumi nechut klalit may overlap; offset rules apply per the takanon achid. The disability premium is built into the 6.5% employer tagmulim, up to 2.5% of salary; if the employee opts out of disability coverage that premium is added to the savings component.
- **Survivors (sha'arim)** under takanon achid for an ACTIVE member: spouse 60% of insured salary; orphans combined 40% of insured salary (divided among children under 21, extended to 24 during military / national / regular national service); dependent parent 20%; total cap 100% of insured salary. For an INACTIVE member, the benefit is calculated from the accumulated balance using actuarial coefficients, not fixed percentages. Bituach Leumi shaerim STACKS on top of this; it is not an offset.
- **Nayadut (fund transfer):** No transfer fees. Send the request to the OLD fund only after deposits to the new fund have actually begun, or the transfer can stall. The transferring fund must move the balance within 10 business days of a complete signed request (Transfer Regulations 2008, reg. 5(a)); the Commissioner may extend this by up to 20 more business days. Vetek (seniority) is preserved for the keren hishtalmut 6-year lock. Transferring from a pre-2013 bituach menahalim to a pensia fund forfeits guaranteed annuity factors (mekadem hamara mubatach) on those balances; check before transferring.

### Step 6: Severance at Termination (Form 161)
The single most consequential decision at job change. Mistakes here cost tens of thousands of NIS in future tax.

**Heichum kitzbah:** the critical interaction users miss.
- Pension payouts at retirement are partially tax-exempt (57.5% of kitzbah mezakah in 2026, rising to 67% by 2028).
- Each shekel of tax-exempt severance withdrawn WITHIN 32 YEARS BEFORE the eligibility age (the later of retirement age and the age the qualifying pension starts) reduces the lifetime kitzbah-mezakah tax-exempt pool by the same amount multiplied by a coefficient of 1.35 (the Tax Authority calls it the מקדם). Earlier withdrawals do NOT reduce the pool: the cut-off is about age 35 for men (67) and about 33 for women born 1970 or later (65); use the user's own cohort age.
- The 1.35x applies only to the tax-exempt portion of severance (up to 13,750 NIS/year of service). Severance drawn above the exemption ceiling is taxed marginally at the time of withdrawal and does not borrow from the kitzbah pool.
- Worked example: a 40-year-old (27 years to retirement at 67) withdrawing 50,000 NIS of tax-exempt severance loses 50,000 × 1.35 = 67,500 NIS of future tax-exempt pension allowance. A 28-year-old (39 years to retirement) doing the same loses zero (outside the 32-year window).

**Section 14 is not all-or-nothing.** Four sub-cases (full 8.33% from day 1, partial salary, delayed start, collective agreement) are detailed in `references/tax-benefits.md`; three of them can leave residual severance owed at FINAL salary. Identify the sub-case before telling a user nothing more is owed.

**Forms involved (Form 161 was redesigned January 2024 as a single unified form):**
- **Form 161 -- Part A (Employer Notice)** -- Filled by the employer at termination, declaring employee details, employment period, salary, Section 14 status, and severance amounts paid out and accumulated in funds.
- **Form 161 -- Part B (Employee Notice)** -- Filled by the employee declaring intent for each component of severance: cash withdrawal (subject to heichum kitzbah), rezef-kitzbah (pension continuity), rezef-pitzuyim (severance continuity), or prisat pituyim (spread tax over up to 6 years). Part B REPLACES the old standalone Form 161א as of January 2024.
- **Form 161 -- Part C** -- Employer's calculation worksheet and instructions to the fund.
- **Default if Part B is not returned is CONDITIONAL.** The employee may skip Part B, and is treated as electing rezef-kitzbah (pension continuity), only when the employer marked in Part A that the severance in kitzbah funds does not exceed the default-rezef ceiling (at least 405,900 NIS in 2026, higher for long service; the employer computes it in Part A) AND there are no grants from payers that are not kupot gemel. In every other case Part B must be filled. Tax-practitioner summaries of Tax Authority clarifications give about 10 days to return the form; read the window off the form itself. The unified form replaced both the old 161 and 161א.
- **Form 161ג (161C)** -- Request to revert from rezef-pitzuyim or rezef-kitzbah (reverting rezef-pitzuyim is limited to 2 years from termination). It is NOT a route for returning severance already withdrawn. Submitted to the Tax Authority.
- **Form 161ד (161D)** -- "Request for fixation of rights under Section 9A" (kibua zechuyot), filed at retirement to allocate the lifetime exemption pool between the monthly pension and capital or severance grants.

**Options at termination (no ranking; which fits is a question for a licensed adviser):** rezef zechuyot (leave severance in the fund; works cleanly only if the new employer's arrangement is compatible), cash withdrawal (subject to heichum kitzbah), prisat pituyim (spread the taxable part over up to 6 tax years), and reverting a rezef election later via Form 161ג. Mechanics are in `references/tax-benefits.md`.

### Step 7: Tikun 190 Deposits (the post-60 tax shelter)
Tikun 190 of the Income Tax Ordinance (2012) lets a saver deposit money, with no employer match and no credit or deduction claimed, into a kupat gemel le-kitzbah and later draw it as a "recognised pension" (kitzbah mukeret). It is used mostly from age 60, because the exemption applies to a recognised pension received from 60.

**Why it matters:** it is THE standard tax-shelter tool at retirement age for severance, retirement bonuses, sale of a business, inheritance and surplus savings: zero tax if drawn as a monthly pension, 15% on the NOMINAL gain as a lump sum, against 25% on the REAL (CPI-adjusted) gain in a regular investment account. In a high-inflation stretch a nominal-basis 15% can exceed a real-basis 25%, so run the comparison rather than assuming the shelter always wins.

**Mechanics:**
- No pension condition at DEPOSIT time. The minimum-pension test (5,306 NIS/month in 2026) is checked when a LUMP SUM is taken (commutation), not when money goes in.
- What counts toward that minimum: pensions from kupot gemel le-kitzbah and budget pensions. Bituach Leumi old-age and survivors' pensions do NOT count. A retiree whose only pension is from Bituach Leumi cannot take the lump sum.
- Drawn as a monthly recognised pension from age 60: fully exempt from income tax, with no minimum-pension test.
- Drawn as a lump sum (age 60+ and the minimum pension required): 15% tax on the NOMINAL gain only; principal is not taxed. The base is nominal, not real (CPI-adjusted) -- this is the single most misquoted detail of Tikun 190.
- The first 38,412 NIS deposited in a tax year (2026) is classed as an ordinary qualifying pension (kitzbah mezakah), because deposits within the Section 45a/47 benefit ceiling are not "exempt payments". Only the excess becomes a recognised pension. There is no cap on the excess.
- Death: before 75, beneficiaries receive the money tax-free if they withdraw within 3 months; gains accruing after that are taxed at 25% of the real gain. After 75 without having started the pension, the depositor is treated as having commuted it (15% on the gain); a beneficiary aged 60+ can instead take it as an exempt pension.

**Common confusion:** "Tikun 190" is used colloquially to refer to BOTH this 60+ deposit benefit AND the parallel reform of severance / kitzbah taxation under the same amendment. The two have nothing operational in common. When a client says "Tikun 190" ask which they mean.

**Triggers to recommend a yoetz pensioni consultation:** any planned Tikun 190 deposit over ~250,000 NIS, any consideration of withdrawing the deposit before 5 years, and any deposit by a depositor with non-Israeli citizenship or US tax exposure (US-Israel cross-border practitioners disagree whether kupot gemel are PFICs under US tax law versus foreign pensions under the treaty; the disagreement is what makes professional advice mandatory here).

### Step 8: Choosing Between Pension Types
- **Keren pensia:** the default product under the mandatory-pension order and the default-fund tender; lower fee caps (default funds 0.22% balance + 1% deposits; others up to 0.5% + 6%), disability and survivors cover built in, age-based default track.
- **Bituach menahalim:** separate risk premium, higher fees (up to 1.05% balance + 4% deposits). Policies sold before 1 January 2013 carry a guaranteed annuity factor (mekadem hamara mubatach) that a transfer forfeits; weigh that before any transfer.
- Tracks, halacha-compliant options and fund operators: `references/pension-fund-types.md`.

### Step 9: Life Events
Five events change the pension answer materially: divorce (pension splitting under the 2014 Law), relocation abroad (Section 14(a) and the absence of any Israel-US totalization agreement), spousal attribution under Section 47, fixation of rights at retirement (kibua zechuyot, Form 161ד), and bridge pensions from age 60. Full rules, citations and the per-event traps are in `references/life-events.md`; read it before explaining any of them.

## Examples

### Example 1: New Employee
User says: "I just started a new job, what pension should I choose?"
Result: Explain mandatory pension, the default-fund mechanism (ID-digit assignment for employers with 50+ workers) and the fee and cover differences between the product types, point out that management fees are worth comparing, mention a keren hishtalmut if the employer offers one (10% combined contribution is meaningful). For employees with a prior pension fund, contributions are retroactive to Day 1; without one, they begin only after 6 months.

### Example 2: Self-Employed Savings
User says: "I'm a freelancer, how should I save for retirement?"
Result: Explain the new-business exemption (fewer than 6 months since first VAT registration at year end), then apply 4.45% / 12.55% brackets on net taxable income up to the average wage (max ~14,044 NIS/year). Present the ceilings neutrally, without ranking the vehicles: pension 38,412 NIS/year (less if loss-of-work-capacity premiums were deducted, see Step 4), of which the first 5.5% (or 5%) earns a 35% credit and the rest a deduction; keren hishtalmut 13,203 NIS deductible and 20,566 NIS profit-exempt. Which to fill first depends on the user's marginal rate and liquidity needs, a question for a licensed pension adviser.

### Example 3: Job Change with Severance
User says: "I'm switching jobs and have 80,000 NIS of severance accrued under full Section 14. Should I take it or leave it?"
Result: Walk through Form 161 (the 2024 unified form: the employer files Part A, the employee fills Part B within a short window stated on the form). Silence counts as rezef-kitzbah only under the Step 6 conditions. Explain what each Part B option does: cash is tax-free up to 13,750 NIS per year of service, but inside the 32-year window each exempt shekel costs 1.35 shekels of the future exemption pool (outside it, nothing); rezef depends on the new employer's arrangement; spreading lowers the rate on the taxable part. List the deciding factors (liquidity, marginal rate, expected pension income, the new employer's scheme) and say that choosing among them for this user is a question for a licensed pension adviser.

### Example 4: Approaching Retirement (Tikun 190)
User says: "I'm 64, I just sold my business and have 1.5M NIS sitting in the bank. My private pension is 8,000 NIS/month. What should I do with the cash?"
Result: Do not tell the user what to do with the money. Explain how a Tikun 190 deposit works as one route people in this position look at. Ask where the 8,000 NIS pension comes from: a pension from a kupat gemel le-kitzbah counts toward the 5,306 NIS minimum needed for a later lump sum, a Bituach Leumi pension does not. The monthly route needs only age 60+. Note that the first 38,412 NIS deposited in the year is ordinary qualifying-pension money. Explain deposit into a kupat gemel le-kitzbah: drawn as kitzbah, the monthly payment is fully exempt from income tax for life; drawn as lump sum, the NOMINAL gain is taxed at 15% (against 25% on the real, CPI-adjusted gain in a regular investment account), so check the inflation assumption before presenting it as a saving. Estate-planning effect: funds pass to beneficiaries under fund rules, not probate. Whether, and how much, to deposit is a pension-advice decision for a licensed pension adviser, especially if any beneficiary has US tax exposure.

### Example 5: Divorce
User says: "We're divorcing. My ex has a much bigger pension than mine. How is it split?"
Result: Explain the Pension Savings Division between Separated Spouses Law (2014): the decree sets the split and the marital period, and once registered with each fund the fund pays the split directly. Stress registering promptly, before the other spouse starts drawing. Detail: `references/life-events.md`.

## Bundled Resources

### Scripts
- `scripts/calculate_pension.py` -- Computes mandatory pension contributions (employee, employer, severance), keren hishtalmut benefits with the 15,712 NIS salary cap enforced, and retirement savings projections (with realistic mekadem hamara per gender) for both employees and self-employed. Female retirement age is resolved from the per-cohort birth-year table, never a flat number, so pass `--birth-year` alongside `--female`; without it the script assumes the 1970-and-later age of 65 and says so. Run: `python scripts/calculate_pension.py --help`

### References
- `references/pension-fund-types.md` -- Detailed comparison of Israeli pension vehicles: Keren Pensia, Bituach Menahalim, Kupat Gemel le-Tagmulim, Kupat Gemel le-Hashka'a, and Kupat Gemel le-Kitzbah (Tikun 190 vehicle), with fee structures, insurance components, default fund system, and major fund providers. Consult when explaining the pension vehicles in Step 8.
- `references/tax-benefits.md` -- Israeli pension tax benefits including the 35% tax credit on employee contributions, employer contribution exclusions, keren hishtalmut tax-free gains, self-employed deduction rules, Section 14 details, Tikun 190 deposit mechanics, and pension payout tax exemption rates. Consult when calculating tax savings from pension and savings contributions.
- `references/retirement-age-by-cohort.md` -- Women's retirement age by year of birth, including the 1959-and-earlier cohort. This is the authoritative source for retirement age; never use a flat number.
- `references/life-events.md` -- Life events (Step 9): divorce and pension splitting, relocation abroad, spousal attribution, fixation of rights (Form 161ד), and bridge pensions.
- `references/approaching-retirement.md` -- The last years before retirement: Bituach Leumi old-age pension (income test, deferral increment), the transition grant for women born 1960-1966, commutation of pension savings, and the Form 161ד choice.
- `references/troubleshooting.md` -- Common failure modes and their fixes.

## Recommended MCP Servers

No pension-specific MCP exists today. Pair with general Israeli financial MCPs (e.g., il-bank for transaction data) when the user asks for cash-flow context alongside pension planning.

## Gotchas
- "Tikun 190" means TWO different things. One: the 60+ deposit benefit into kupat gemel le-kitzbah (Step 7). Two: the 2012 amendment that introduced heichum kitzbah and the kitzbah-mezakah exemption schedule (Step 6). Always clarify which when a client uses the term.
- Women's retirement age is 63 years 3 months in 2026, not flat 63. The amendment raises it by 3-4 months per birth cohort (not a constant 4) up to 65 for women born 1970 or later; the exact age is set by date of birth. Use the per-cohort table, not a single number.
- Heichum kitzbah's 1.35x penalty only applies WITHIN 32 years of the eligibility age. The cut-off is about 35 for men but about 33 for women born 1970 or later; never apply the men's figure to a woman.
- Rezef zechuyot needs the new employer's severance contributions to flow into the same continuity arrangement. If the new employer is in a different scheme, or has no pension yet (e.g. the 6-month waiting period applies), rezef may not actualize and the severance sits frozen in the old kupah.
- Pension fund management fees in Israel have two components: from deposits (up to 6% for non-default funds) and from accumulated savings (up to 0.5% annually). Agents may quote only one component. Default selected funds cap at 0.22% balance + 1% deposits. The four are Altshuler Shaham, Meitav, Infinity and More, under a tender running to 31.10.2028; re-check the winners after that date. Anyone can join one regardless of employer, and the default funds carry the lowest statutory fee caps; whether to move is a question for a licensed pension adviser.
- Self-employed keren hishtalmut has TWO separate ceilings: the tax deduction ceiling (13,203 NIS/year) and the profit-exempt ceiling (20,566 NIS/year). Agents often conflate these into a single figure.
- Bituach Leumi old-age pension (kitzvat zikna) STACKS on top of private pension fund payouts; it is not an offset. Self-employed users sometimes assume one replaces the other and underestimate retirement income, or skip private pension thinking BL is enough.
- Form 161 was redesigned January 2024: one unified form replacing 161 and 161א, with a short return window rather than the 120 days 161א allowed. Silence defaults to rezef-kitzbah ONLY under the conditions in Step 6; do not tell a user whose employer marked the default-rezef ceiling as exceeded, or who has a non-kupah grant, that they may skip Part B.
- Bituach Leumi pensions do not count toward the Tikun 190 minimum pension, and there is no pension test at deposit time. Both mistakes are common. Anything referencing "161א" without the 2024 redesign is stale.

## Reference Links

| Source | URL | What to Check |
|---|---|---|
| Kol Zchut - Average Wage | https://www.kolzchut.org.il/he/השכר_הממוצע | Annual average wage figure from National Insurance (base for pension ceilings) |
| Kol Zchut - Mandatory Pension | https://www.kolzchut.org.il/he/חובת_ביטוח_פנסיוני_לעובדים | Employee/employer pension rates, Section 14, contribution timing |
| Kol Zchut - Default Pension Funds | https://www.kolzchut.org.il/he/קרנות_פנסיה_נבחרות_(קרנות_ברירת_מחדל) | Default fund tender, ID-digit assignment rules, fee caps |
| Kol Zchut - Severance Tax Exemption | https://www.kolzchut.org.il/he/פטור_ממס_הכנסה_על_פיצויי_פיטורים | Tax-exempt severance ceiling, heichum kitzbah, prisat pituyim |
| Kol Zchut - Severance Withdrawal | https://www.kolzchut.org.il/he/משיכת_כספי_פיצויי_פיטורים_מקופת_גמל_או_מהביטוח_הפנסיוני | Bittul pituyim, rezef zechuyot, severance tax mechanics (note: page describes the pre-2024 Form 161א flow; for the current Form 161 unified flow see the gov.il Notice of Retirement link above) |
| Retirement Age Law (Wikisource) | https://he.wikisource.org/wiki/חוק_גיל_פרישה | Statutory retirement-age schedule by month of birth |
| Gov.il - Women's Retirement Age | https://www.gov.il/he/pages/women_retirement_age_news | Per-cohort women's retirement age (the by-year-of-birth table) |
| Kol Zchut - Pension Division at Divorce | https://www.kolzchut.org.il/he/חלוקת_פנסיה_בין_בני_זוג_שנפרדו | Mechanics of the 2014 law on registering a divorce decree with a pension fund |
| Gov.il - Form 161 (New) | https://www.gov.il/he/service/notice-of-retirement | Official Tax Authority page for the redesigned Form 161 (Parts A/B/C, January 2024) |
| Pensuni - 2026 Pension Ceilings | https://pensuni.com/?p=827 | Annual aggregator for tax-credit ceilings, hishtalmut ceilings, kitzbah-mezakah figures |
| Pensuni - Tikun 190 Mechanics | https://pensuni.com/?p=1258 | Tikun 190 deposit rules, kitzbah-mezakah exemption schedule, heichum kitzbah formula |

## Troubleshooting

See `references/troubleshooting.md`.
