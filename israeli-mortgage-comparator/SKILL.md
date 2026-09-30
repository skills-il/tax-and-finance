---
name: israeli-mortgage-comparator
description: Compare mortgage tracks (maslulei mashkanta) across Israeli banks, calculate monthly payments for mixed-track portfolios, and understand Bank of Israel Directive 329 limits including LTV ceilings, the payment-to-income prohibition, and the cap on the variable-rate share. Use when a user needs to evaluate mortgage offers from different banks, calculate refinancing savings, or understand how Prime rate changes affect their payments. Covers Leumi, Hapoalim, Discount, Mizrachi-Tefahot, FIBI, Mercantile, and Yahav. Do NOT use for commercial real estate loans, business credit lines, or non-Israeli mortgage products.
license: MIT
allowed-tools: Bash(python:*) WebFetch
---

# Israeli Mortgage Comparator

## Snapshot (fetch before quoting)

This skill hard-codes **no** interest rate and **no** tax bracket. Both drift, and a stale
number here is worse than no number. Fetch them at use time:

| Variable | Where to get it | Note |
|---|---|---|
| Bank of Israel rate | `https://boi.org.il/PublicApi/GetInterest` returns the current rate and the next decision date as JSON. Human-readable equivalent at boi.org.il | The single most drift-prone input to every calculation below. Decisions land roughly every 6 weeks |
| Prime rate | BoI rate + 1.5 percentage points. The Bank of Israel's own explanation sheet for the approval in principle (Directive 451, Appendix 6) defines Prime as "Bank of Israel rate + 1.5%". Confirm against the bank's published prime before quoting | Prime is uniform across banks; only each bank's discount or premium TO prime varies |
| Purchase tax (mas rechisha) brackets | mas.gov.il, or the `israeli-real-estate` skill, which is the authoritative holder of the bracket table | Do not restate bracket figures from memory |

The regulatory limits in Step 2 are different in kind: they are set by a published Bank of
Israel directive and change only when the directive is amended, so they are stated here with
their section numbers.

## Instructions

### Step 1: Understand the Israeli Mortgage System

Israeli mortgages are usually composed of several parallel tracks (maslulim), each with its own rate mechanism, combined to balance risk and cost.

**The 5 main mortgage tracks:**

1. **Prime (ריבית פריים)** - Variable rate linked to the prime rate, which is the Bank of Israel rate plus 1.5 percentage points. Changes whenever the central bank adjusts its rate. Expressed as "Prime minus X%" (e.g., Prime - 0.5%).

2. **Fixed Non-Linked (קבועה לא צמודה)** - Fixed interest rate, not linked to CPI. The safest track: your payment never changes for the entire loan period. Typically the highest starting interest rate.

3. **Fixed CPI-Linked (קבועה צמודה למדד)** - Fixed interest rate but the principal is linked to the Consumer Price Index (madad). Lower starting rate than fixed non-linked, but your outstanding balance grows with inflation.

4. **Variable CPI-Linked (משתנה צמודה למדד)** - Variable interest rate (resets every 5 years) and principal linked to CPI. Double exposure: both rate changes and inflation adjustments.

5. **Variable Non-Linked (משתנה לא צמודה)** - Variable interest rate (resets every 5 years), not linked to CPI. Rate adjusts periodically but no inflation linkage.

### Step 2: Know the Bank of Israel Regulations

The binding rules live in **Bank of Israel Proper Conduct of Banking Business Directive 329,
"Limitations on Housing Loans"**. The version in force is `[13] (06/26)`, published 30/06/2026
under circular 2852. Every limit below is a prohibition on the BANK, phrased as
"a banking corporation shall not approve and shall not execute". Section numbers are given so
the user can check them.

**Loan-to-Value (LTV), section 2.** "A banking corporation shall not approve and shall not
execute a housing loan at a financing rate exceeding the following rates":

| Property class | Max LTV | Section |
|---|---|---|
| Single dwelling (dira yechida) | 75% | 2.1 |
| Replacement dwelling (dira chalifit) | 70% | 2.2 |
| Investment dwelling (dira le'hashkaa) | 50% | 2.3 |

The **value** in the ratio is not the purchase price: it may not exceed the lower of the appraisal and the price in the purchase agreement (see `references/offer-comparison-and-fees.md` section 5). An appraisal below the price shrinks the maximum loan.

Section 4 applies the same ceilings to the **aggregate**: a new loan plus the balance of earlier
loans secured on the same apartment may not exceed them. Section 10a lets a bank decline to apply
the section-4 aggregate limit on a non-purchase housing loan up to 70% LTV, provided the excess
above 50% LTV does not exceed 200,000 NIS.

**The buyer's status can decide the row.** Section 1 defines a single dwelling and a replacement
dwelling as one bought by an individual "Israeli citizen", and an investment dwelling as any
dwelling that is neither. "Israeli citizen" here is the Land Taxation Law s.16A(a)(1)-(1b)
definition, which is wider than citizenship: anyone registered, or obliged to register, in the
Population Registry, any individual Israeli resident, or a Law-of-Return-eligible resident of the
Area. A buyer outside all three (typically a foreign national neither registered nor resident)
falls in the **50%** row even for an only home. Otherwise establish the classification first (for
example a buyer between selling and buying); the bank's own policy may be stricter in any case.

**Payment-to-income (PTI), sections 5 and 6. Read these two together, because they are commonly
reported backwards.**

- **Section 5 is a hard prohibition at 50%.** Verbatim: "a banking corporation shall not approve
  and shall not execute a housing loan at a payment-to-income ratio exceeding 50%." This is a
  ceiling, not a target and not an approval promise. Banks set stricter internal policy, and most
  will decline well below 50%.
- **Section 6 is a capital rule, not a borrower cap.** Where PTI exceeds **40%**, the loan must be
  assigned a **100% risk weight** for the bank's capital requirement, regardless of the reduced
  risk weights in Directive 203 section 72. It does not forbid the loan. It makes the loan
  expensive for the bank to hold, which is why pricing and willingness deteriorate sharply above
  40%. Treat 40% as a **cost cliff**, not a legal limit.
- **Section 11:** sections 5 and 6 do not apply to the loans in 12.1 (bridge loans with an
  original repayment term of up to three years) or 12.2 (any-purpose loans up to 120,000 NIS).

**How PTI is measured (Appendix A) is not what most borrowers assume:**

- The denominator is **monthly disposable income** (net income minus fixed expenses), not gross
  and not net.
- The numerator includes repayments on the borrower's **other loans secured on the same property**
  whose remaining term exceeds 18 months, and the full approved facility is counted, not the drawn
  amount. This aggregation, which also catches loans from another bank or a non-bank lender on the
  same property, applies to loans given from **1.10.2026** (circular 2852 postponed it from
  1.7.2026). It bites on equity and renovation top-ups taken against an already-mortgaged home.
- A "fixed expense" is any commitment with more than 18 months remaining. **Alimony (mezonot)
  counts.** Rent paid by a borrower who will not live in the purchased apartment is deducted from
  income even if the lease has under 18 months left.
- Half of a first-degree relative's disposable income may be recognised only if all of 1.3.1 to
  1.3.4 hold, including that the relative guarantees the loan and **pays 20% or more of the
  monthly repayment from their own bank account**. A cohabiting spouse who meets the conditions
  may be recognised in full.

**Variable-rate share, section 7.** "A banking corporation shall approve and execute a housing
loan only on condition that the ratio between the variable-rate portion of the housing loan and
the total loan does not exceed **66.66%**."

- This is a single cap on the **whole variable-rate portion**, Prime and other variable tracks
  together.
- **The directive contains no Prime-specific cap.** The word "prime" does not appear in it at all.
  Any advice built on an older "Prime limited to one third" rule is describing text that is not in
  the directive in force.
- The complement is arithmetic, not a separate rule: if variable may not exceed 66.66%, then at
  least 33.34% of the loan is in fixed-rate tracks.
- Section 12 lets a bank disapply section 7 for bridge loans (12.1), any-purpose loans up to
  120,000 NIS (12.2), and FX or FX-linked loans to a foreign resident (12.3), provided the bank's
  own quarterly variable-rate share stays within 66.66%.

**Repayment term, section 8.** Maximum period to final repayment: **30 years**. Section 8a, a
temporary rule in force to 31.12.2026, caps contractor-subsidised bullet and balloon loans at 10%
of a bank's quarterly housing-loan volume.

**Refinancing, section 9.** A bank may not refinance a housing loan if the refinancing creates a
breach of any of the above limits, or widens a breach that existed before it.

**A limit is not an entitlement.** Every rule above binds the BANK. None of them gives a
borrower a right to a loan, and clearing all of them does not make approval likely, let alone
certain. Anything this skill produces is general information that does not account for the
individual's own data and needs, and is not a substitute for advice that does.

**What the directive does NOT contain.** No minimum number of tracks, and no borrower stress test at
any particular rate. Stress-testing affordability against a Prime increase is sound advice, not
regulation.

### Step 3: Gather User's Financial Details

Collect the following to enable accurate comparison:

- **Property price** (ILS)
- **Equity available** (the complement of the section-2 LTV ceiling: at least 25% for a single dwelling, 30% for a replacement dwelling, 50% for an investment dwelling)
- **Desired loan term** (typically 15-30 years; Directive 329 section 8 caps the period to final repayment at 30 years)
- **Monthly disposable income** per Appendix A of Directive 329: net income minus fixed expenses (any commitment with over 18 months remaining, alimony included). Both spouses if applicable. This, not gross and not net, is the PTI denominator
- **Purchase type**: first apartment, upgrade (selling existing and buying), or investment
- **Employment type**: salaried (sachir), self-employed (atzmai), or mixed
- **Existing debts**: car loans, credit cards, other obligations, flagging which have over 18 months remaining and which are secured on the same property
- **Age of the oldest borrower**: each bank sets its own maximum age at final repayment. Directive 329 has no age cap, only the 30-year term cap in section 8, so ask each bank

### Step 4: Build Track Combinations for Comparison

Design 3-4 different track combinations that comply with Directive 329. The only composition constraint is section 7: the variable-rate portion (Prime plus every other variable track) may not exceed 66.66% of the loan. Everything else below is judgement, not regulation.

**Conservative Mix (low risk, higher initial payment):**
- 34% Fixed Non-Linked (15-20 years)
- 33% Fixed CPI-Linked (20-25 years)
- 33% Prime (variable, 20-25 years)

**Aggressive Mix (lower initial payment, more risk):**
- 33% Prime (20-25 years)
- 33% Variable Non-Linked (every 5 years, 20-25 years)
- 34% Fixed CPI-Linked (25-30 years)

**Balanced Mix:**
- 40% Fixed Non-Linked (20 years)
- 27% Fixed CPI-Linked (25 years)
- 33% Prime (25 years)

**Anti-Inflation Mix (minimizes CPI exposure):**
- 50% Fixed Non-Linked (20 years)
- 17% Variable Non-Linked (every 5 years, 20 years)
- 33% Prime (25 years)

### Step 5: Compare Across Banks

Request an approval in principle (ishur ikroni) from at least 3-4 banks, ideally BEFORE signing the purchase agreement. Directive 451 makes these documents directly comparable: every approval shows three **uniform baskets** priced by that bank, plus the bank's own proposed mix, with the total projected repayment and the highest projected monthly payment already computed. Compare uniform basket against uniform basket first, then the proposed mixes. The terms hold for a period the bank states, at least 24 days. Full rules: `references/offer-comparison-and-fees.md`.

The major mortgage lenders in Israel:

**Tier 1 Banks (largest market share):**
- **Bank Leumi (בנק לאומי)**
- **Bank Hapoalim (בנק הפועלים)**
- **Mizrachi-Tefahot (מזרחי-טפחות)** - Largest mortgage lender by volume. Size is not price; compare the offers

**Tier 2 Banks:**
- **Bank Discount (בנק דיסקונט)**
- **FIBI / Bank Benleumi (הבנק הבינלאומי)**
- **Bank Mercantile (בנק מרכנתיל)** - Subsidiary of Discount

**Specialized:**
- **Bank Yahav (בנק יהב)** - Advertises dedicated benefits for state employees and teachers; ask whether they extend to its mortgages

For each bank, create a comparison table:

| Track | Bank A Rate | Bank B Rate | Bank C Rate | Bank D Rate |
|-------|-------------|-------------|-------------|-------------|
| Prime | P - ___% | P - ___% | P - ___% | P - ___% |
| Fixed Non-Linked | ___% | ___% | ___% | ___% |
| Fixed CPI-Linked | ___% | ___% | ___% | ___% |
| Variable CPI-Linked (5yr) | ___% | ___% | ___% | ___% |
| Variable Non-Linked (5yr) | ___% | ___% | ___% | ___% |

### Step 6: Calculate Monthly Payments

For each track combination at each bank, calculate:

**Per track:**
- Monthly payment (the Spitzer formula below; if an offer uses equal principal (keren shava), the first payment is higher and total interest lower, so compare like with like)
- For CPI-linked tracks: project payments with assumed 2-3% annual inflation
- For variable tracks: calculate current payment AND stress-test with +2% rate increase

**Total mortgage:**
- Sum of all track monthly payments
- Total interest paid over loan lifetime
- Total CPI linkage cost (projected with 2% and 3% inflation scenarios)
- Total cost of mortgage (principal + interest + CPI adjustments)

**Calculation formula for each track:**
Monthly payment = P * [r(1+r)^n] / [(1+r)^n - 1]
Where: P = principal for this track, r = monthly interest rate, n = number of monthly payments

**For CPI-linked tracks**, the outstanding balance increases with CPI monthly. The effective cost is significantly higher than the nominal interest rate suggests when inflation is high.

### Step 7: Evaluate Total Cost, Not Just Monthly Payment

Many borrowers focus only on the monthly payment, but the total cost of the mortgage is what matters:

1. **Total interest paid**: Sum of all interest payments over the loan lifetime for all tracks
2. **CPI linkage cost**: For CPI-linked tracks, calculate the total inflation adjustment over the loan term using 2% and 3% annual inflation scenarios
3. **Total cost = Principal + Total Interest + CPI Adjustments**
4. **Early repayment fee exposure**: Prime and tracks resetting at least annually carry no capitalisation fee; fixed tracks and 5-year variable tracks between resets can (Step 10)

Create a summary comparison:

| Metric | Bank A | Bank B | Bank C |
|--------|--------|--------|--------|
| Monthly payment (year 1) | | | |
| Monthly payment (year 10, projected) | | | |
| Total interest (30 years) | | | |
| Total CPI cost (2% inflation) | | | |
| Total CPI cost (3% inflation) | | | |
| Total cost of mortgage | | | |
| Early exit penalty (after 5yr) | | | |

### Step 8: Consider Mortgage Advisor vs. Direct

**Mortgage advisor (yoetz mashkantaot):** fee typically 3,000-8,000 ILS (some charge a percentage of the loan). Negotiates with several banks at once and handles paperwork; most worthwhile on large loans. Membership of an advisors' association is not a government licence; get the fee in writing and ask whether the advisor receives anything from a bank.

**Direct negotiation:** free, but you do the comparison yourself. Use one bank's written approval in principle as leverage with the others; banks are often more flexible near end-of-quarter.

### Step 9: Understand Government Programs

**Discounted housing lottery (Dira BeHanacha / דירה בהנחה umbrella):**
- Government subsidized housing lottery for eligible buyers. The program runs under the "Dira BeHanacha" (דירה בהנחה) umbrella; "Mechir LaMishtaken" (מחיר למשתכן) is the original track and "Mechir Matara" (מחיר מטרה) is the current flagship lottery variant, check gov.il for the active lottery
- Discounted property prices; the size of the discount varies by project and is published per tender, so read it off the specific project rather than assuming a national figure
- Eligibility based on housing history and marital status
- A first-home buyer should also obtain an eligibility certificate (teudat zakaut) for the government-directed loan and fold that portion into the mix; the gov.il calculator in Reference Links sizes it

**Purchase tax (mas rechisha).** First-time buyers pay 0% up to a threshold, with graduated rates
above it, and additional-property buyers pay a higher schedule from the first shekel. **The
bracket figures are deliberately not restated in this skill**, they live in `israeli-real-estate`
and on mas.gov.il, and duplicating them here creates a second place for them to go stale. Fetch
them before quoting a number.

**Discounted-price apartments and public-sector lanes.** Directive 329 section 4a changes how the
bank values a discounted apartment (a 2.1 million NIS valuation cap and a minimum of own funds), and
section 13 exempts loans under government agreements with state employees, teachers and
defence-system beneficiaries up to 50,000 NIS. Details: `references/directive-329-special-cases.md`.

### Step 10: Refinancing Analysis (Michzur)

For users with existing mortgages considering refinancing:

1. **Calculate current remaining balance** per track
2. **Calculate early repayment fees** per track under the 2002 Banking Order (full table in `references/offer-comparison-and-fees.md` section 4):
   - Directed (eligibility) loan: no early-repayment fee at all
   - Fixed tracks: a capitalisation fee only if the Supervisor's published average rate is now below the loan's rate. Where the average rate at origination was also below the loan's rate, the bank takes the LOWER of the two statutory computations, which is often much smaller. Then discount it by elapsed time from each loan's exact execution date: 20% from 3 years, 30% from 5; a complementary loan (a bank loan given alongside a directed loan) gets 10/20/30/40% from years 1/2/3/4
   - CPI-linked tracks: add the CPI-average fee if repaid between the 1st and the 15th of the month
   - Prime, and tracks resetting at least annually: no capitalisation fee. On a reset date, only the operational fee
   - 5-year variable track between reset dates: a capitalisation fee is possible
   - One tenth of a percent if under ten days' notice was given, except on a reset date, on the part refinanced by the same bank, or on death
3. **Get new rate quotes** from current bank and competitors
4. **Calculate break-even point**: how many months until the new lower rate savings exceed the refinancing costs (penalties + new appraisal + legal fees)
5. **Rule of thumb**: refinancing makes sense when you can save at least 0.3-0.5% on weighted average rate AND have at least 10+ years remaining

### Step 11: Required Insurance and Additional Costs

Directive 451 section 11 lets the bank require (not on loans of up to 30,000 NIS):

- **Life insurance (bituach chaim)** up to the loan amount, with the bank as irrevocable beneficiary
- **Property insurance (bituach mivne)** on the collateral; see the insurance comparator skill

The bank must tell you that you may buy both directly rather than through its own agency, so compare its quote against external policies.

**Additional closing costs:**
- Attorney fees: ~0.5% of property price + VAT
- Appraiser (shamai): 1,500-3,000 ILS
- Mortgage registration (reshum mashkanta): 188 NIS per the Land Registry fee regulations (2026 consolidation, indexed), paid by the mortgagor
- Purchase tax (mas rechisha): varies by buyer type and property value

## Examples

### Example 1: First-Time Buyer Comparing Mortgage Offers

User says: "I'm buying my first apartment for 2,500,000 ILS. I have 700,000 ILS saved for a down payment. My wife and I together earn 25,000 ILS net per month. We got offers from Leumi and Mizrachi-Tefahot."

Actions:
1. Calculate loan amount: 2,500,000 - 700,000 = 1,800,000 ILS (72% LTV, within the 75% first-apartment limit), provided the appraisal comes in at or above the price; an appraisal of 2,300,000 would make it about 78% and force more equity
2. Compute PTI against **disposable** income, not the 25,000 net figure: subtract fixed expenses with over 18 months remaining. Directive 329 section 5 forbids a loan above 50% PTI, and section 6 makes anything above 40% carry a 100% risk weight for the bank, so pricing worsens there. Aim materially below 40% and confirm the bank's own internal threshold, which is usually stricter
3. Request the specific rate offers from both banks for each track
4. Design 3 track combinations respecting Directive 329 section 7 (variable-rate portion, Prime included, at most 66.66%, so at least 33.34% fixed)
5. Calculate monthly payments for each combination at each bank's rates
6. Calculate total cost over 25-year and 30-year terms
7. Stress-test: show what happens if Prime increases by 1% and if inflation averages 3%
8. Recommend getting a third offer from Hapoalim or Discount to strengthen negotiation position

Result: payments, total cost and risk for each bank's offer across several mixes, plus a negotiation plan.

### Example 2: Refinancing Decision

User says: "I took a 1,200,000 ILS mortgage 5 years ago at Hapoalim. My remaining balance is about 1,050,000. My Prime track is at Prime-0.3% and my fixed track is at 4.5%. Mizrachi offered me Prime-0.7% and fixed at 3.8%. Should I refinance?"

Actions:
1. Identify current track composition and remaining terms
2. Calculate current monthly payments across all tracks
3. Calculate early repayment penalties for each track (especially the fixed track at 4.5%)
4. Calculate new monthly payments at Mizrachi's offered rates
5. Factor in refinancing costs: appraisal (~2,000 ILS), attorney (~3,000 ILS), new insurance setup
6. Calculate total savings over remaining loan term minus all costs
7. Determine break-even point (months until savings exceed costs)
8. Consider: negotiate with Hapoalim first using Mizrachi's offer as leverage (retention departments often match)

Result: monthly and lifetime savings, the break-even month, and whether refinancing pays after all fees and costs.

### Example 3: Investment Property Mortgage

User says: "I want to buy a second apartment for investment (hashkaa) for 1,800,000 ILS in Beer Sheva. I already own my primary residence."

Actions:
1. Apply Directive 329 section 2.3 (investment dwelling): maximum LTV 50%, so the user needs at least 900,000 ILS of equity (more if the appraisal comes in below the price). Section 4 applies the same ceiling to the aggregate of any earlier loans secured on the same apartment
2. Maximum loan: 900,000 ILS
3. Note that an additional property is taxed on a higher purchase-tax schedule from the first shekel; fetch the current brackets from mas.gov.il or the `israeli-real-estate` skill rather than quoting a remembered figure
4. Calculate rental yield to determine if the investment makes financial sense after mortgage payments
5. Design track combinations and compare approvals from 3+ banks

Result: the LTV constraint, total acquisition cost including purchase tax, and payments against expected rent.

## Reservist and wartime relief (temporary frameworks)

Do not tell a reservist they hold a standing right to defer mortgage payments: the deferrals seen so
far came from time-limited arrangements, each with its own window:

- **Bank of Israel relief frameworks (mitve).** Activated during conflict periods, with fixed
  eligibility lists and expiry dates. The 2026 "Roaring Lion" measures, for example, were time-boxed: the
  Supervisor's related temporary directive 253 was extended only to 31.05.2026. Before
  quoting any framework, verify at boi.org.il or Kol-Zchut that one is currently active and that the
  user is in a named group. Individual banks sometimes offer their own reservist deferrals; those are
  bank offers, not entitlements.
- **Execution Office protection.** Temporary regulations (Swords of Iron, reserve service) freeze
  listed enforcement steps against a reservist AND their spouse for three months from the start of
  service, extendable by up to three more months if service continues, on notice to the Execution
  Office with the call-up order, subject to the registrar's discretion; alimony-judgment debts are
  excluded. They expire no later than 28.02.2027 and end earlier if the underlying temporary
  provision lapses. They restrict enforcement; they are not a payment deferral.

War-displaced residents (mefunim) may have separate evacuee arrangements; verify with the bank.

## Gotchas
- **The 50% PTI figure is a ceiling on the bank, not an allowance for the borrower.** Directive 329 section 5 forbids a bank from writing a loan above 50% payment-to-income. Agents may restate it as "you can borrow up to 50% of your income", which is both wrong in substance and dangerous. Most banks decline far below it.
- **40% PTI is a capital rule, not a limit.** Section 6 assigns a 100% risk weight above 40%, which makes the loan costly for the bank to hold. Agents may report it as a legal cap (it is not) or as merely a "flag" (it has a concrete pricing consequence). It is a cost cliff.
- **PTI is measured against disposable income, not gross or net.** Agents routinely compute it off gross salary, which understates the ratio badly and produces an affordability answer the bank will not recognise.
- Directive 329 sets **no minimum number of tracks**. Agents may assert that Israeli mortgages must contain at least two tracks; the directive says nothing of the sort. The real constraint is section 7's 66.66% cap on the variable-rate portion, which forces at least 33.34% into fixed tracks but does not otherwise dictate a track count.
- **There is no Prime-specific cap in the directive in force.** The word "prime" does not appear in it. Agents may apply an obsolete one-third Prime rule.
- The Israeli Prime rate is **not** the US Prime rate, and it is **not** the Bank of Israel rate itself. It is the BoI rate plus 1.5 percentage points. Agents routinely substitute the US figure, or quote the bare BoI rate as if it were Prime.
- **Early-repayment fees are not a percentage of the balance.** The capitalisation fee depends on the gap between the loan's rate and the Supervisor's published average rate, and can be zero or large. Agents may invent a flat "penalty of X% of the balance"; compute it from the order's rules instead.
- CPI-linked tracks (tzmudot madad) adjust the outstanding **principal** by the index, not just the interest payment. Agents may adjust only the interest.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Directive 329 (Limitations on Housing Loans), full text | https://www.boi.org.il/media/ez4npagt/329.pdf | LTV, PTI, variable-rate share, term, refinancing. The operative source for every limit in Step 2 |
| Directive 329 landing page (version history) | https://www.boi.org.il/roles/supervisionregulation/nbt/nbt329/ | Which version is in force and which circular amended it |
| Bank of Israel (BOI) | https://www.boi.org.il | Current BOI interest rate, Prime rate decisions, announcements |
| BOI banking supervision | https://www.boi.org.il/en/economic-roles/supervision-and-regulation/supervision-of-the-banking-system/ | Index of supervisory directives and circulars |
| Directive 451 (Procedures for Extending Housing Loans) | https://www.boi.org.il/media/utld2tgp/451.pdf | Approval in principle, uniform baskets, insurance, appraisal, porting |
| Banking Order (Early Repayment of a Housing Loan), 2002 | https://www.boi.org.il/media/qy5cow0l/116.pdf | Every early-repayment fee a bank may charge |
| Bank of Israel credit data system | https://www.creditdata.org.il | How to obtain your free credit data report, and the licensed credit bureaus |
| Dira BeHanacha (umbrella: Mechir Matara, Mechir Mufhat, Mechir LaMishtaken, Dira LeHaskir) | https://www.gov.il/he/Departments/Topics/dira | Reduced-price apartment eligibility and entitlement rules |
| Ministry of Construction housing-loan points calculator | https://www.gov.il/he/pages/mashkanta-calculator | Eligibility points and the size of the GOVERNMENT assistance loan. It is not a multi-track payment calculator, do not send users there to model a mix |

## Troubleshooting

### Error: "Bank rejected the mortgage application despite meeting LTV requirements"

Cause: Banks evaluate more than just LTV. Common rejection reasons include: payment-to-income ratio exceeding the bank's internal threshold, which is typically well below the directive's 50% prohibition and often below the 40% risk-weight cliff, insufficient employment history (banks typically want 12+ months at current employer for salaried, 2+ years of tax returns for self-employed), negative data in the Bank of Israel credit data system, or existing debt obligations that push the total debt ratio too high.

Solution: Ask the bank for its reason. Directive 451 requires a written answer within 5 business days, but not a reason for refusing, so the bank may decline to explain. Order your free credit report through the Bank of Israel credit data system. For an income-ratio problem: a longer term, a guarantor (arev), or a larger down payment. For short employment history: wait and reapply, or try a bank with a more flexible policy for your employment type.

### Error: "CPI-linked track costs are much higher than expected"

Cause: CPI linkage grows the outstanding principal, not just the interest. A 500,000 ILS CPI-linked track at 3% inflation grows to ~672,000 ILS after 10 years before any principal payments, so the "low rate" understates the cost.

Solution: Cost CPI-linked tracks under several inflation scenarios (2%, 3%, 4%) and compare total cost against fixed non-linked. Section 7's 66.66% cap governs the VARIABLE-rate share, not CPI linkage, so there is no regulatory CPI ceiling; how much linkage to hold is judgement. Use a model that applies the index to the principal each period. The gov.il "mashkanta calculator" is an eligibility-points calculator and will not model a mix.

### Error: "Early repayment penalty is unexpectedly high on fixed-rate track"

Cause: On a fixed-rate track the capitalisation fee is the present-value gap between the payments at your rate and at the Supervisor's published average rate. When average rates have fallen below your rate, it can reach tens of thousands of shekels on a large balance.

Solution: Recompute it with the 2002 Order's rules (`references/offer-comparison-and-fees.md` section 4): check the origination-date computation (the bank must take the lower), apply the elapsed-time discount for the loan type, repay a CPI-linked track after the 15th of the month, and give 10 to 45 days' notice. Repay the Prime track and variable tracks on their reset dates first, where no capitalisation fee applies. If average rates have risen above your rate, there is no capitalisation fee at all.

### Error: "Different banks show different Prime rates for the same period"

Cause: Prime itself is uniform across banks (the Bank of Israel rate plus 1.5 percentage points). What differs is each bank's spread to Prime ("Prime - 0.65%"), and some banks quote an effective rate that folds the two together.

Solution: Compare the spread, not the effective rate: P-0.7% beats P-0.5% by 0.2% whatever Prime is. Prime-track payments change with every rate decision, so stress-test affordability with Prime at +1% and +2% (prudent practice, not a Directive 329 requirement).
