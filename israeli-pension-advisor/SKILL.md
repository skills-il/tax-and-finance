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

Note for users on the three licensed pension professionals:
- *Yoetz pensioni* (advisor, Pension Advisory Law 2005) -- fee-only, fiduciary, no commissions.
- *Sokhen pensioni* (agent) -- commission-paid by funds, sells products.
- *Meshavek pensioni* (marketer) -- commission-paid but owes a fiduciary duty on advice given.

For unbiased advice ask specifically for a yoetz pensioni.

## Instructions

### Step 1: Identify Savings Type
| Type | Hebrew | Purpose | Tax Benefit |
|------|--------|---------|-------------|
| Keren Pensia | keren pensia | Retirement + disability + survivors | Tax credit + deduction |
| Bituach Menahalim | bituach menahalim | Retirement (insurance-based, declining for new policies since 2013) | Tax credit + deduction |
| Keren Hishtalmut | keren hishtalmut | Medium-term savings (6 years) | Tax-free gains for employees |
| Kupat Gemel le-Tagmulim | kupat gemel le-tagmulim | General savings (historical, mostly closed to new deposits since 2008) | Various |
| Kupat Gemel le-Hashka'a (IRA) | kupat gemel le-hashka'a | Self-directed retirement savings (since 2016 reform) | Tax on withdrawal at marginal rate, or 15% on the nominal gain if drawn as kitzbah at 60+ |
| Kupat Gemel le-Kitzbah (Tikun 190 vehicle) | kupat gemel le-kitzbah | Post-60 tax-shelter (see Step 7) | Full exemption as kitzbah, 15% on the nominal gain as lump sum |
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
  NIS/month from 01.01.2026).** It is the ceiling on income charged BL and
  health contributions, and it governs nothing in this skill. Users routinely
  reach for it when they say "the insurable salary ceiling", which lands them
  almost four times above the real mandatory-pension ceiling of 13,769. When a
  user names a ceiling without qualifying it, ask which of these four they
  mean before computing anything.

**Pension contribution timing for new employees** (Mandatory Pension Expansion Order):
- Employee with existing pension at intake: contributions begin Day 1, paid retroactively after 3 months of work or end of tax year (whichever first).
- Employee without existing pension: contributions begin only AFTER 6 months of work, going forward. The first 6 months are NOT covered retroactively.

**Self-employed mandatory pension** (Mandatory Pension for the Self-Employed Law, 2016):
- 4.45% on net taxable income up to 6,884.50 NIS/month (half average wage)
- 12.55% on income from 6,884.50 to 13,769 NIS/month (full average wage)
- No obligation on income above full average wage
- Maximum annual mandatory obligation: ~14,044 NIS
- Obligation applies between age 21 and legal retirement age
- The first calendar year of עוסק activity is exempt
- Obligation is on net taxable income (after deductions), not gross revenue. עוסק פטור and עוסק מורשה are both covered.

### Step 3: Keren Hishtalmut (Training Fund)
The most popular Israeli savings vehicle:

**For employees:**
- **Employee contribution:** Up to 2.5% of salary
- **Employer contribution:** Up to 7.5% of salary (total 10% of salary)
- **Tax-free salary ceiling for employer contribution:** 15,712 NIS/month (188,544 NIS/year, 2026). At the ceiling the combined contribution is 1,571 NIS/month.
- Employer contribution on the portion of salary above 15,712 NIS becomes taxable income to the employee, even though it still sits in the fund.
- **Withdrawal after 6 years:** Tax-free on gains (unique Israeli benefit)
- **Withdrawal after 3 years:** For accredited training only, with documentation

**For self-employed (two separate ceilings):**
- **Tax deduction from income:** Up to 13,203 NIS/year (4.5% of income up to 293,397 NIS)
- **Profit-exempt ceiling:** 20,566 NIS/year (gains on deposits up to this amount are tax-free after 6 years). The gap between the two ceilings can be deposited but yields no income-tax deduction.

**Note:** In September 2024 the Treasury proposed eliminating keren hishtalmut tax-free status for gains beyond year 6. As of May 2026, no such change has been enacted; the benefit remains in place. Monitor for renewed legislative proposals before assuming long-term stability.

### Step 4: Tax Benefits Summary

**For employees:**
- **Pension tax credit:** 35% credit on employee contributions up to 679 NIS/month (7% of qualifying salary 9,700 NIS, 2026). Maximum credit ~2,852 NIS/year.
- Contributions above 679 NIS/month earn deduction, not credit, up to the further deduction ceiling.
- **Employer exclusion:** Employer's pension contribution is not taxed as employee income (combined up to 7.5% of salary).

**For self-employed:**
- Tax credit (35%) on contributions up to 12,804 NIS/year (5.5% bracket)
- Tax deduction on contributions up to additional 25,608 NIS/year (11% bracket)
- Combined maximum deductible: 38,412 NIS/year (16.5% of qualifying income up to 232,800 NIS/year, ~19,400 NIS/month)

**Pension payout (at retirement):**
- Monthly pension partially tax-exempt under Tikun 190 (Amendment 190 to the Income Tax Ordinance, 2012)
- 2026 exemption rate: 57.5%; rising to 62.5% in 2027 and 67% from 2028 (schedule on track as of 2026)
- Tax-free pension amount: up to 5,422 NIS/month (2026)
- Qualifying pension threshold (kitzbah mezakah): 9,430 NIS/month
- Lifetime tax-exempt capital pool (kibua zechuyot / yitrat hahon haptura) = 180 times the monthly tax-exempt pension = 180 × 57.5% × 9,430 = 976,005 NIS (the figure the Tax Authority publishes; do not round the monthly 5,422 first, which gives 975,960) for a worker retiring in 2026 (it grows as the exemption rate climbs toward 67% by 2028). Eaten by severance withdrawn under heichum kitzbah at 1.35x per shekel (see Step 6).

### Step 5: Withdrawal Rules
- **Pension:** Men age 67; women in 2026 age 63 years 3 months, rising 3-4 months per cohort to 65 for women born 1970 or later, under the Retirement Age Law 5764-2004 as amended (in force from January 2022, phased over 11 years). The age is set by DATE OF BIRTH, not by calendar year; check the per-cohort table below, never a flat number.

The per-cohort table is in `references/retirement-age-by-cohort.md`.

- **Three distinct retirement ages in Israeli law:** gil zakaut le-kitzbah (60+, early access with conditions); gil prishah (67/63+); gil prishah chovah (67 for both genders, the maximum age at which an employer can require retirement). Do not conflate.
- **Early pension withdrawal:** 35% withholding on tagmulim or marginal rate, whichever higher. Early withdrawal of severance beyond the exempt ceiling is taxed at the marginal rate (up to 47%, plus surtax). Exceptions for disability, low household income, or terminal illness can reduce or remove the tax.
- **Keren hishtalmut:** After 6 years (tax-free on gains), or 3 years (accredited training only, with documentation). Early withdrawal taxes the GAINS at the marginal rate, not the full balance.
- **Severance (pitzuim):** On termination, subject to the Section 14 arrangement and the Form 161 process. Tax-exempt up to 13,750 NIS per year of service. See Step 6 in full before any withdrawal decision.
- **Disability:** New comprehensive pension funds under the unified regulations (takanon achid, June 2018) pay up to 75% of insured salary for disability. Bituach Leumi nechut klalit may overlap; offset rules apply per the takanon achid. The disability premium is built into the 6.5% employer tagmulim, up to 2.5% of salary; if the employee opts out of disability coverage that premium is added to the savings component.
- **Survivors (sha'arim)** under takanon achid for an ACTIVE member: spouse 60% of insured salary; orphans combined 40% of insured salary (divided among children under 21, extended to 24 during military / national / regular national service); dependent parent 20%; total cap 100% of insured salary. For an INACTIVE member, the benefit is calculated from the accumulated balance using actuarial coefficients, not fixed percentages. Bituach Leumi shaerim STACKS on top of this; it is not an offset.
- **Nayadut (fund transfer):** No transfer fees. Send the request to the OLD fund only after deposits to the new fund have actually begun, or the transfer can stall. The statutory completion deadline is short but was not re-verifiable this cycle: confirm the current deadline with the receiving fund rather than quoting a number to the user. Vetek (seniority) is preserved for the keren hishtalmut 6-year lock. Transferring from a pre-2013 bituach menahalim to a pensia fund forfeits guaranteed annuity factors (mekadem hamara mubatach) on those balances; check before transferring.

### Step 6: Severance at Termination (Form 161)
The single most consequential decision at job change. Mistakes here cost tens of thousands of NIS in future tax.

**Heichum kitzbah:** the critical interaction users miss.
- Pension payouts at retirement are partially tax-exempt (57.5% of kitzbah mezakah in 2026, rising to 67% by 2028).
- Each shekel of tax-exempt severance withdrawn WITHIN 32 YEARS BEFORE legal retirement age reduces the lifetime kitzbah-mezakah tax-exempt pool by the same amount multiplied by a coefficient of 1.35 (the Tax Authority calls it the מקדם). Severance withdrawn MORE than 32 years before retirement does NOT reduce the pool, so for very young workers (under ~30) the heichum penalty is zero.
- The 1.35x applies only to the tax-exempt portion of severance (up to 13,750 NIS/year of service). Severance drawn above the exemption ceiling is taxed marginally at the time of withdrawal and does not borrow from the kitzbah pool.
- Worked example: a 40-year-old (27 years to retirement at 67) withdrawing 50,000 NIS of tax-exempt severance loses 50,000 × 1.35 = 67,500 NIS of future tax-exempt pension allowance. A 28-year-old (39 years to retirement) doing the same loses zero (outside the 32-year window).

**Section 14 (4 real-world sub-cases, per the אישור כללי of 30 June 1998 and amendments):**
1. Full 8.33% from day 1 on the full salary -- the textbook case; employer fully released from supplemental severance.
2. Section 14 on part of salary only (e.g. base, not bonus); the unfunded portion stays under the general law, calculated at final salary on termination.
3. Section 14 starting after a delay (no pension for the first months); employer owes the gap for the pre-Section-14 period at FINAL salary times years, indexed -- often the largest source of שלמת פיצויים claims.
4. Collective-agreement Section 14 (industry or Histadrut); bonuses, retroactive raises, and certain allowances may sit outside the arrangement and trigger residual severance liability.

The 2.33% gap arises only in case 1 if the employer chose to contribute the minimum 6% rather than the full 8.33% -- the employer owes the difference on termination at final salary.

**Forms involved (Form 161 was redesigned January 2024 as a single unified form):**
- **Form 161 -- Part A (Employer Notice)** -- Filled by the employer at termination, declaring employee details, employment period, salary, Section 14 status, and severance amounts paid out and accumulated in funds.
- **Form 161 -- Part B (Employee Notice)** -- Filled by the employee declaring intent for each component of severance: cash withdrawal (subject to heichum kitzbah), rezef-kitzbah (pension continuity), rezef-pitzuyim (severance continuity), or prisat pituyim (spread tax over up to 6 years). Part B REPLACES the old standalone Form 161א as of January 2024.
- **Form 161 -- Part C** -- Employer's calculation worksheet and instructions to the fund.
- **Default if Part B is not returned: rezef-kitzbah (pension continuity), NOT auto-payout.** The submission window is short (commonly cited as about 10 business days from receipt) but is NOT verified in this skill: read the window off the Part A form the employer hands over, and do not quote a number to the user. The Tax Authority treats a non-responding employee as having elected pension continuity if all severance funds are in annuity-eligible accounts. This is the opposite of the pre-2024 rule.
- **Form 161ג (161C)** -- Filed to REVOKE a prior rezef-pitzuyim election within 2 years of termination (the "bittul pituyim" window). Submitted directly to the Tax Authority.
- **Form 161ד (161D)** -- Filed at retirement to settle the lifetime kitzbah-mezakah exemption calculation against severance the employee took during their career (kibu'a zechuyot).

**Three options at termination (in order of common preference):**
1. **Rezef zechuyot (continuity)** -- Leave severance in the kupah, no tax event, no impact on future kitzbah-mezakah. Default best for younger workers with future retirement income. CAVEAT: only works cleanly if the new employer's severance contributions land in the same continuity arrangement; if the new employer has different terms or no pension yet, the rezef may not actualize and the severance sits frozen.
2. **Bittul pituyim (cancellation)** -- If severance was already drawn within the past 2 years, the employee can return it to the kupah with interest and indexation, with pakid shuma (assessment officer) approval, to restore the kitzbah pool. The original termination tax assessment is re-opened. Filed via Form 161ג.
3. **Prisat pituyim (spreading)** -- Spread severance taxation across up to 6 tax years to lower the marginal rate. Rule of thumb: 1 spread-year per 4 years of seniority, capped at 6. Only the taxable portion (above the petur ceiling) is spread; backward spreading exists but is rare and requires specific approval.

### Step 7: Tikun 190 Deposits (the post-60 tax shelter)
Tikun 190 of the Income Tax Ordinance (2012) lets people aged 60+ who already draw a qualifying pension (kitzbah mezakah) at least the minimum threshold (approximately 5,306 NIS/month in 2026) deposit lump sums into a kupat gemel le-kitzbah with a dramatically improved tax treatment.

**Why it matters:** Tikun 190 deposits are THE standard tax-shelter tool at retirement age for severance, retirement bonuses, sale of a business, inheritance, and surplus liquid savings. A retiree depositing 1M NIS of an inheritance into a kupat gemel le-kitzbah pays 15% tax on the NOMINAL gain on lump-sum withdrawal, against 25% on the REAL (CPI-adjusted) gain in a regular investment account, and pays zero tax if the deposit is drawn down as a monthly kitzbah. Get the tax base right: the 15% applies to the nominal gain, not the real one. That is usually still the better deal, but it is not free money, and in a high-inflation stretch a nominal-basis 15% can exceed a real-basis 25%. Run the comparison rather than assuming the shelter always wins.

**Mechanics:**
- Qualifying pension prerequisite: the depositor must already receive a kitzbah of at least the minimum threshold (BL old-age pension counts; private pension counts; a partial kitzbah from a former employer counts). Without it, the deposit is treated as a normal kupat gemel le-tagmulim and the Tikun 190 benefit does not apply.
- Age 60+ at deposit time.
- No annual deposit cap, no lifetime cap (the benefit is on the tax treatment, not a contribution ceiling).
- Lock-up: funds must remain at least until the depositor is eligible for kitzbah (essentially immediately, given the prerequisite).
- Withdrawal as kitzbah: monthly payments fully exempt from income tax for life.
- Withdrawal as lump sum: 15% tax on the NOMINAL gain only; principal is not taxed. The base is nominal, not real (CPI-adjusted) -- this is the single most misquoted detail of Tikun 190.
- Inheritance: on the depositor's death, the funds pass to designated beneficiaries; their tax treatment depends on the beneficiary's age and choice (kitzbah vs lump sum).

**Common confusion:** "Tikun 190" is used colloquially to refer to BOTH this 60+ deposit benefit AND the parallel reform of severance / kitzbah taxation under the same amendment. The two have nothing operational in common. When a client says "Tikun 190" ask which they mean.

**Triggers to recommend a yoetz pensioni consultation:** any planned Tikun 190 deposit over ~250,000 NIS, any consideration of withdrawing the deposit before 5 years, and any deposit by a depositor with non-Israeli citizenship or US tax exposure (US-Israel cross-border practitioners disagree whether kupot gemel are PFICs under US tax law versus foreign pensions under the treaty; the disagreement is what makes professional advice mandatory here).

### Step 8: Choosing Between Pension Types
**Keren Pensia (Pension Fund):**
- Lower management fees (default funds: 0.22% balance + 1% deposits; non-default: up to 0.5% balance + 6% deposits)
- Includes disability and survivors insurance built-in
- Multiple investment tracks: age-based (default), general, shares-focused, bonds-focused, halacha-compliant (avoids interest-bearing instruments, substitutes alternative instruments; historical returns trend modestly below conventional over long horizons but vary by fund)
- Preferred for most new employees
- Since 2013, most new employees are directed to keren pensia over bituach menahalim by default

**Bituach Menahalim (Manager's Insurance):**
- Separate insurance component (risk premium reduces savings)
- More investment track flexibility
- Higher management fees (up to 1.05% balance + up to 4% contributions)
- Policies sold AFTER 1 January 2013 lost the guaranteed annuity factor (mekadem hamara mubatach); pre-2013 policies retain it, a significant benefit at retirement for those who hold them.
- Worth keeping a pre-2013 policy in most cases; rarely worth opening a new one.

### Step 9: Life Events
Five events change the pension answer materially: divorce (pension splitting under the 2014 Law), relocation abroad (Section 14(a) and the absence of any Israel-US totalization agreement), spousal attribution under Section 47, aggregating pensions at retirement (gibush kitzbaot, Form 161ד), and bridge pensions from age 60. Full rules, citations and the per-event traps are in `references/life-events.md`; read it before advising on any of them.

## Examples

### Example 1: New Employee
User says: "I just started a new job, what pension should I choose?"
Result: Explain mandatory pension (default to keren pensia for new employees; bituach menahalim rarely worth opening since 2013), describe the ID-digit default fund assignment for employers with 50+ workers, recommend comparing management fees, suggest also opening a keren hishtalmut if the employer offers one (10% combined contribution is meaningful). For employees with a prior pension fund, contributions are retroactive to Day 1; without one, they begin only after 6 months.

### Example 2: Self-Employed Savings
User says: "I'm a freelancer, how should I save for retirement?"
Result: Explain that the first year of business is exempt from mandatory pension, then apply 4.45% / 12.55% brackets on net taxable income up to the average wage (max ~14,044 NIS/year). Note the two separate keren hishtalmut ceilings (13,203 NIS deduction vs 20,566 NIS profit-exempt) and the combined max deductible pension contribution of 38,412 NIS/year. Recommend maximizing keren hishtalmut first (best return per shekel of tax benefit).

### Example 3: Job Change with Severance
User says: "I'm switching jobs and have 80,000 NIS of severance accrued under full Section 14. Should I take it or leave it?"
Result: Walk through Form 161 (new 2024 unified form -- the employer files Part A, the employee fills Part B within a short window stated on the form itself; do not quote a day count you have not read off the form). Default if no Part B is filed is rezef-kitzbah (pension continuity), NOT auto-payout. For a worker under ~35 (more than 32 years to retirement) heichum kitzbah penalty is zero, so withdrawal is tax-free up to 13,750 NIS per year of service and the kitzbah pool is unaffected. For a worker over ~35, prefer rezef-pitzuyim UNLESS the new employer's arrangement is not compatible (in which case rezef-kitzbah is the safer default). Mention prisat pituyim as a fallback if the worker needs liquidity but the severance pushes them into a high marginal bracket.

### Example 4: Approaching Retirement (Tikun 190)
User says: "I'm 64, I just sold my business and have 1.5M NIS sitting in the bank. My private pension is 8,000 NIS/month. What should I do with the cash?"
Result: Confirm 8,000 NIS pension exceeds the kitzbah-mezakah minimum (~5,306 NIS) and the user is over 60, both Tikun 190 prerequisites met. Explain deposit into a kupat gemel le-kitzbah: drawn as kitzbah, the monthly payment is fully exempt from income tax for life; drawn as lump sum, the NOMINAL gain is taxed at 15% (against 25% on the real, CPI-adjusted gain in a regular investment account), so check the inflation assumption before presenting it as a saving. Estate-planning effect: funds pass to beneficiaries under fund rules, not probate. Strongly recommend a yoetz pensioni for a deposit at this size, especially if any beneficiary has US tax exposure.

### Example 5: Divorce
User says: "We're divorcing. My ex has a much bigger pension than mine. How is it split?"
Result: Explain the Pension Savings Division between Separated Spouses Law (2014). The divorce decree must specify the split percentage and the marital period. Once a certified copy is registered with each pension fund or insurer, the fund administers the split directly with no repeated enforcement. Register promptly: if the higher-earning spouse retires and starts drawing before registration, the fund may pay out the full amount and the receiving spouse will need to chase the funds personally.

## Bundled Resources

### Scripts
- `scripts/calculate_pension.py` -- Computes mandatory pension contributions (employee, employer, severance), keren hishtalmut benefits with the 15,712 NIS salary cap enforced, and retirement savings projections (with realistic mekadem hamara per gender) for both employees and self-employed. Female retirement age is resolved from the per-cohort birth-year table, never a flat number, so pass `--birth-year` alongside `--female`; without it the script assumes the 1970-and-later age of 65 and says so. Run: `python scripts/calculate_pension.py --help`

### References
- `references/pension-fund-types.md` -- Detailed comparison of Israeli pension vehicles: Keren Pensia, Bituach Menahalim, Kupat Gemel le-Tagmulim, Kupat Gemel le-Hashka'a (IRA), and Kupat Gemel le-Kitzbah (Tikun 190 vehicle), with fee structures, insurance components, default fund system, and major fund providers. Consult when advising on pension fund selection in Step 8.
- `references/tax-benefits.md` -- Israeli pension tax benefits including the 35% tax credit on employee contributions, employer contribution exclusions, keren hishtalmut tax-free gains, self-employed deduction rules, Section 14 details, Tikun 190 deposit mechanics, and pension payout tax exemption rates. Consult when calculating tax savings from pension and savings contributions.
- `references/retirement-age-by-cohort.md` -- Women's retirement age by year of birth, including the 1959-and-earlier cohort. This is the authoritative source for retirement age; never use a flat number.
- `references/life-events.md` -- Life events (Step 9): divorce and pension splitting, relocation abroad, spousal attribution, gibush kitzbaot, and bridge pensions.
- `references/troubleshooting.md` -- Common failure modes and their fixes.

## Recommended MCP Servers

No pension-specific MCP exists today. Pair with general Israeli financial MCPs (e.g., il-bank for transaction data) when the user asks for cash-flow context alongside pension planning.

## Gotchas
- "Tikun 190" means TWO different things. One: the 60+ deposit benefit into kupat gemel le-kitzbah (Step 7). Two: the 2012 amendment that introduced heichum kitzbah and the kitzbah-mezakah exemption schedule (Step 6). Always clarify which when a client uses the term.
- Women's retirement age is 63 years 3 months in 2026, not flat 63. The amendment raises it by 3-4 months per birth cohort (not a constant 4) up to 65 for women born 1970 or later; the exact age is set by date of birth. Use the per-cohort table, not a single number.
- Heichum kitzbah's 1.35x penalty only applies WITHIN 32 years of retirement. Workers under ~35 withdrawing severance pay zero kitzbah-pool penalty. Agents who blanket-discourage severance withdrawal for young workers are leaving liquidity on the table.
- Section 14 is not all-or-nothing. Four sub-cases exist (full, partial-salary, delayed-start, collective-agreement) and three of them leave residual שלמת פיצויים liability at final salary. Don't tell a terminating employee "Section 14 = nothing extra owed" without verifying which sub-case applies.
- Rezef zechuyot needs the new employer's severance contributions to flow into the same continuity arrangement. If the new employer is in a different scheme, or has no pension yet (e.g. the 6-month waiting period applies), rezef may not actualize and the severance sits frozen in the old kupah.
- Survivors pension under takanon achid is 60% spouse + 40% orphans COMBINED (not per orphan) + 20% dependent parent, capped at 100%. Agents who say "30% per orphan" are quoting an outdated or vendor-specific formula.
- Israeli pension has three distinct product types: comprehensive pension fund (keren pensia makifa), provident fund (kupat gemel), and managers' insurance (bituach menahalim). Agents may treat them as interchangeable, but they have different fee structures, insurance components, and withdrawal rules.
- Pension fund management fees in Israel have two components: from deposits (up to 6% for non-default funds) and from accumulated savings (up to 0.5% annually). Agents may quote only one component. Default selected funds cap at 0.22% balance + 1% deposits. The four are Altshuler Shaham, Meitav, Infinity and More, under a tender running to 31.10.2028; re-check the winners after that date. Anyone can join one regardless of employer, often the cheapest available fix for a saver paying full fees.
- Israeli pension funds invest significantly in local government bonds (igrot chov mimshaltiiot), which means returns are partially linked to Israeli economic performance. Agents should not compare Israeli pension returns directly to US 401(k) S&P 500 benchmarks.
- Self-employed keren hishtalmut has TWO separate ceilings: the tax deduction ceiling (13,203 NIS/year) and the profit-exempt ceiling (20,566 NIS/year). Agents often conflate these into a single figure.
- Bituach Leumi old-age pension (kitzvat zikna) STACKS on top of private pension fund payouts; it is not an offset. Self-employed users sometimes assume one replaces the other and underestimate retirement income, or skip private pension thinking BL is enough.
- Form 161 was redesigned January 2024: one unified form, Part B replaces the old 161א, and the submission window is now short rather than the 120 days 161א allowed. See Step 6 for the window and the reversed default. Anything referencing "161א" without the 2024 redesign is stale.
- Hishtalmut tax-free employer contribution stops at salary 15,712 NIS/month. For higher earners, the employer hishtalmut on salary above the ceiling is taxable income to the employee even though it still sits in the fund.

## Reference Links

| Source | URL | What to Check |
|---|---|---|
| Kol Zchut - Average Wage | https://www.kolzchut.org.il/he/השכר_הממוצע | Annual average wage figure from National Insurance (base for pension ceilings) |
| Kol Zchut - Mandatory Pension | https://www.kolzchut.org.il/he/חובת_ביטוח_פנסיוני_לעובדים | Employee/employer pension rates, Section 14, contribution timing |
| Kol Zchut - Default Pension Funds | https://www.kolzchut.org.il/he/קרנות_פנסיה_נבחרות_(קרנות_ברירת_מחדל) | Default fund tender, ID-digit assignment rules, fee caps |
| Kol Zchut - Severance Tax Exemption | https://www.kolzchut.org.il/he/פטור_ממס_הכנסה_על_פיצויי_פיטורים | Tax-exempt severance ceiling, heichum kitzbah, prisat pituyim |
| Kol Zchut - Severance Withdrawal | https://www.kolzchut.org.il/he/משיכת_כספי_פיצויי_פיטורים_מקופת_גמל_או_מהביטוח_הפנסיוני | Bittul pituyim, rezef zechuyot, severance tax mechanics (note: page describes the pre-2024 Form 161א flow; for the current Form 161 unified flow see the gov.il Notice of Retirement link above) |
| Kol Zchut - Retirement Age | https://www.kolzchut.org.il/he/גיל_פרישה_מעבודה | Current male/female retirement ages and the 2032 target schedule |
| Gov.il - Women's Retirement Age | https://www.gov.il/he/pages/women_retirement_age_news | Per-cohort women's retirement age (the by-year-of-birth table) |
| Kol Zchut - Pension Division at Divorce | https://www.kolzchut.org.il/he/חלוקת_פנסיה_בין_בני_זוג_שנפרדו | Mechanics of the 2014 law on registering a divorce decree with a pension fund |
| Gov.il - Form 161 (New) | https://www.gov.il/he/service/notice-of-retirement | Official Tax Authority page for the redesigned Form 161 (Parts A/B/C, January 2024) |
| Pensuni - 2026 Pension Ceilings | https://pensuni.com/?p=827 | Annual aggregator for tax-credit ceilings, hishtalmut ceilings, kitzbah-mezakah figures |
| Pensuni - Tikun 190 Mechanics | https://pensuni.com/?p=1258 | Tikun 190 deposit rules, kitzbah-mezakah exemption schedule, heichum kitzbah formula |

## Troubleshooting

See `references/troubleshooting.md`.
