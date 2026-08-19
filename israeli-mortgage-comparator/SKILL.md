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
| Prime rate | The bank's own published prime (ribit prime). Read it off the bank, do not compute it from a remembered margin | The margin over the BoI rate is set by the banks, not by regulation, so it is not stated here. Prime itself is uniform across banks; only each bank's discount or premium TO prime varies |
| Purchase tax (mas rechisha) brackets | mas.gov.il, or the `israeli-real-estate` skill, which is the authoritative holder of the bracket table | Do not restate bracket figures from memory |

The regulatory limits in Step 2 are different in kind: they are set by a published Bank of
Israel directive and change only when the directive is amended, so they are stated here with
their section numbers.

## Instructions

### Step 1: Understand the Israeli Mortgage System

The Israeli mortgage system is unique. Unlike most countries where you take a single loan at one rate, Israeli mortgages are composed of multiple parallel tracks (maslulim), each with different interest rate mechanisms. A typical mortgage combines 3-5 tracks to balance risk and cost.

**The 5 main mortgage tracks:**

1. **Prime (ריבית פריים)** - Variable rate linked to the banks' published prime rate, which tracks the Bank of Israel rate with a fixed margin the banks set. Changes whenever the central bank adjusts its rate. Expressed as "Prime minus X%" (e.g., Prime - 0.5%).

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

Section 4 applies the same ceilings to the **aggregate**: a new loan plus the balance of earlier
loans secured on the same apartment may not exceed them. Section 10a lets a bank decline to apply
the section-4 aggregate limit on a non-purchase housing loan up to 70% LTV, provided the excess
above 50% LTV does not exceed 200,000 NIS.

The directive classifies by **property**, not by residency. It contains no separate LTV row for a
foreign resident. Where a buyer's classification is not obvious (a foreign resident, a buyer
between selling and buying), the classification is what to establish first, and the bank's own
policy may be stricter than the directive in any case.

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
  amount.
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

**What the directive does NOT contain.** It sets no minimum number of tracks, and it prescribes no
borrower stress test at any particular rate. Banks do run their own underwriting scenarios, but do
not attribute a specific stress-test rate to Directive 329. Stress-testing your own affordability
against a Prime increase remains sound practice; it is advice, not regulation.

### Step 3: Gather User's Financial Details

Collect the following to enable accurate comparison:

- **Property price** (ILS)
- **Equity available** (the complement of the section-2 LTV ceiling: at least 25% for a single dwelling, 30% for a replacement dwelling, 50% for an investment dwelling)
- **Desired loan term** (typically 15-30 years; Directive 329 section 8 caps the period to final repayment at 30 years)
- **Monthly disposable income** per Appendix A of Directive 329: net income minus fixed expenses (any commitment with over 18 months remaining, alimony included). Both spouses if applicable. This, not gross and not net, is the PTI denominator
- **Purchase type**: first apartment, upgrade (selling existing and buying), or investment
- **Employment type**: salaried (sachir), self-employed (atzmai), or mixed
- **Existing debts**: car loans, credit cards, other obligations, flagging which have over 18 months remaining and which are secured on the same property
- **Age of youngest borrower** (loan term + age cannot exceed 75 in most banks)

### Step 4: Build Track Combinations for Comparison

Design 3-4 different track combinations that comply with Directive 329. The only composition constraint is section 7: the variable-rate portion (Prime plus every other variable track) may not exceed 66.66% of the loan. Everything else below is judgement, not regulation.

**Conservative Mix (low risk, higher initial payment):**
- 34% Fixed Non-Linked (15-20 years)
- 33% Fixed CPI-Linked (20-25 years)
- 33% Prime (variable, 20-25 years)

**Aggressive Mix (lower initial payment, more risk):**
- 34% Prime (20-25 years)
- 33% Variable Non-Linked (every 5 years, 20-25 years)
- 33% Fixed CPI-Linked (25-30 years)

**Balanced Mix:**
- 40% Fixed Non-Linked (20 years)
- 27% Fixed CPI-Linked (25 years)
- 33% Prime (25 years)

**Anti-Inflation Mix (minimizes CPI exposure):**
- 50% Fixed Non-Linked (20 years)
- 17% Variable Non-Linked (every 5 years, 20 years)
- 33% Prime (25 years)

### Step 5: Compare Across Banks

Request quotes from at least 3-4 banks. The major mortgage lenders in Israel:

**Tier 1 Banks (largest market share):**
- **Bank Leumi (בנק לאומי)** - Historically competitive on fixed rates
- **Bank Hapoalim (בנק הפועלים)** - Largest bank, strong in Prime deals
- **Mizrachi-Tefahot (מזרחי-טפחות)** - Largest mortgage lender by volume, often best rates

**Tier 2 Banks:**
- **Bank Discount (בנק דיסקונט)** - Sometimes offers aggressive rates to gain market share
- **FIBI / Bank Benleumi (הבנק הבינלאומי)** - Competitive for specific profiles
- **Bank Mercantile (בנק מרכנתיל)** - Subsidiary of Discount, sometimes has unique offers

**Specialized:**
- **Bank Yahav (בנק יהב)** - Serves government and public sector employees; often has exclusive rates for eligible borrowers

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
- Monthly payment (using standard amortization formula)
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
4. **Early repayment penalty exposure**: Variable tracks are cheaper to exit early; fixed tracks carry penalties

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

**Mortgage advisor (yoetz mashkantaot):**
- Fee: typically 3,000-8,000 ILS (some charge percentage of loan)
- Advantages: negotiates with multiple banks simultaneously, knows current market rates, handles paperwork
- Best for: large mortgages where small rate differences matter significantly
- Find licensed advisors at the Israel Association of Mortgage Advisors

**Direct bank negotiation:**
- Free, but you do the comparison work yourself
- Tip: Get a written offer (ishur ikroni) from one bank and use it to negotiate with others
- Banks are more flexible near end-of-quarter when they need to meet targets

### Step 9: Understand Government Programs

**Discounted housing lottery (Dira BeHanacha / דירה בהנחה umbrella):**
- Government subsidized housing lottery for eligible buyers. The program runs under the "Dira BeHanacha" (דירה בהנחה) umbrella; "Mechir LaMishtaken" (מחיר למשתכן) is the original track and "Mechir Matara" (מחיר מטרה) is the current flagship lottery variant, check gov.il for the active lottery
- Discounted property prices; the size of the discount varies by project and is published per tender, so read it off the specific project rather than assuming a national figure
- Eligibility based on housing history and marital status

**How the bank values a discounted apartment (Directive 329, section 4a).** This changes the
equity arithmetic and is routinely missed:
- The bank may base the property value on an appraisal at loan-approval date, but **where the
  appraisal exceeds 2.1 million NIS, the value must be set at 2.1 million NIS or the purchase
  price, whichever is higher.** A higher appraisal does not buy a bigger loan.
- Programme penalties (clawback of the benefit, agreed penalty) are deducted from the apartment's
  value unless the bank's right ranks ahead of the state's.
- The buyer must pay from their **own resources** at least **60,000 NIS** for an apartment
  carrying a grant under Annex A of the Accountant General's "Mechir LaMishtaken" circular, or
  **100,000 NIS** for any other apartment.

**Purchase tax (mas rechisha).** First-time buyers pay 0% up to a threshold, with graduated rates
above it, and additional-property buyers pay a higher schedule from the first shekel. **The
bracket figures are deliberately not restated in this skill**, they live in `israeli-real-estate`
and on mas.gov.il, and duplicating them here creates a second place for them to go stale. Fetch
them before quoting a number.

**Public-sector and defence-system borrowers (section 13).** Loans a bank grants under agreements
with government representatives to state employees, teaching staff, and defence-system
beneficiaries are exempt from the directive's limits up to 50,000 NIS, and without that cap where
a qualifying Ministry of Defence guarantee is in place. This is the lane Bank Yahav operates in.

### Step 10: Refinancing Analysis (Michzur)

For users with existing mortgages considering refinancing:

1. **Calculate current remaining balance** per track
2. **Calculate early repayment penalties** per track:
   - Fixed non-linked: penalty if current market rate is lower than your rate
   - Fixed CPI-linked: penalty based on rate differential plus CPI adjustment
   - Prime: no penalty (can be repaid anytime)
   - Variable (at reset date): no penalty
   - Variable (between reset dates): small penalty possible
3. **Get new rate quotes** from current bank and competitors
4. **Calculate break-even point**: how many months until the new lower rate savings exceed the refinancing costs (penalties + new appraisal + legal fees)
5. **Rule of thumb**: refinancing makes sense when you can save at least 0.3-0.5% on weighted average rate AND have at least 10+ years remaining

### Step 11: Required Insurance and Additional Costs

Every Israeli mortgage requires:

**Life insurance (bituach chaim):**
- Required for the full mortgage amount
- Decreases as mortgage balance decreases
- Compare bank-offered vs. external policies (external is often 30-50% cheaper)
- Must be assigned (meshubad) to the mortgage bank

**Property insurance (bituach mivne):**
- Required for the structure/building value
- Must be assigned to the mortgage bank
- See the insurance comparator skill for details

**Additional closing costs:**
- Attorney fees: ~0.5% of property price + VAT
- Appraiser (shamai): 1,500-3,000 ILS
- Mortgage registration (reshum mashkanta): ~200 ILS
- Purchase tax (mas rechisha): varies by buyer type and property value

## Examples

### Example 1: First-Time Buyer Comparing Mortgage Offers

User says: "I'm buying my first apartment for 2,500,000 ILS. I have 700,000 ILS saved for a down payment. My wife and I together earn 25,000 ILS net per month. We got offers from Leumi and Mizrachi-Tefahot."

Actions:
1. Calculate loan amount: 2,500,000 - 700,000 = 1,800,000 ILS (72% LTV, within the 75% first-apartment limit)
2. Compute PTI against **disposable** income, not the 25,000 net figure: subtract fixed expenses with over 18 months remaining. Directive 329 section 5 forbids a loan above 50% PTI, and section 6 makes anything above 40% carry a 100% risk weight for the bank, so pricing worsens there. Aim materially below 40% and confirm the bank's own internal threshold, which is usually stricter
3. Request the specific rate offers from both banks for each track
4. Design 3 track combinations respecting Directive 329 section 7 (variable-rate portion, Prime included, at most 66.66%, so at least 33.34% fixed)
5. Calculate monthly payments for each combination at each bank's rates
6. Calculate total cost over 25-year and 30-year terms
7. Stress-test: show what happens if Prime increases by 1% and if inflation averages 3%
8. Recommend getting a third offer from Hapoalim or Discount to strengthen negotiation position

Result: User receives a comprehensive comparison showing monthly payments, total costs, and risk profiles for each bank's offer across multiple track combinations, plus a recommended strategy for negotiation.

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

Result: User receives a detailed savings analysis showing monthly savings, total lifetime savings, break-even month, and whether refinancing is worthwhile after accounting for all penalties and costs.

### Example 3: Investment Property Mortgage

User says: "I want to buy a second apartment for investment (hashkaa) for 1,800,000 ILS in Beer Sheva. I already own my primary residence."

Actions:
1. Apply Directive 329 section 2.3 (investment dwelling): maximum LTV 50%, so the user needs at least 900,000 ILS of equity. Section 4 applies the same ceiling to the aggregate of any earlier loans secured on the same apartment
2. Maximum loan: 900,000 ILS
3. Note that an additional property is taxed on a higher purchase-tax schedule from the first shekel; fetch the current brackets from mas.gov.il or the `israeli-real-estate` skill rather than quoting a remembered figure
4. Investment property mortgages often get slightly worse rates from banks
5. Calculate rental yield to determine if the investment makes financial sense after mortgage payments
6. Design track combinations optimized for investment (shorter terms often better for investment properties)
7. Compare rates from 3+ banks, noting some banks are more friendly to investment property mortgages

Result: User receives the LTV constraint analysis, total acquisition cost (including higher purchase tax), mortgage payment projections vs. expected rental income, and a comparison of bank offers for investment property mortgages.

## Reservist statutory mortgage protections

A reservist (משרת מילואים) called up under Order 8 during an active conflict period is generally entitled to defer mortgage and loan payments (commonly up to about 3 months) without interest or fees. The exact terms and eligibility are set largely by the active-period relief framework and reservist-protection legislation:

- Right to defer monthly payments without late fees during active reserve duty
- Foreclosure freeze for the duration of active duty
- The bank cannot demand penalty interest or accelerate the loan due to the deferral
- Spouse / co-borrower may invoke the same protections when the reservist is the primary earner

Beyond the statutory reservist protections, the Bank of Israel periodically activates a temporary bank-relief framework (broader payment deferrals, fee waivers for war-zone evacuees and affected borrowers) during active conflict periods. These frameworks have specific eligibility windows and expiry dates that change as the security situation changes, so agents must **verify the current framework status and dates at boi.org.il before quoting** rather than assuming any particular framework is either active or lapsed. Reservist payment-deferral terms and eligibility are set largely by the active-period relief framework and periodic reservist legislation, so verify the current terms at boi.org.il or Kol-Zchut before quoting.

War-displaced residents (מפונים) from Tkuma authority programs may have separate evacuee-specific arrangements; verify with the bank's social work / evacuee desk.

## Gotchas
- **The 50% PTI figure is a ceiling on the bank, not an allowance for the borrower.** Directive 329 section 5 forbids a bank from writing a loan above 50% payment-to-income. Agents may restate it as "you can borrow up to 50% of your income", which is both wrong in substance and dangerous. Most banks decline far below it.
- **40% PTI is a capital rule, not a limit.** Section 6 assigns a 100% risk weight above 40%, which makes the loan costly for the bank to hold. Agents may report it as a legal cap (it is not) or as merely a "flag" (it has a concrete pricing consequence). It is a cost cliff.
- **PTI is measured against disposable income, not gross or net.** Agents routinely compute it off gross salary, which understates the ratio badly and produces an affordability answer the bank will not recognise.
- Directive 329 sets **no minimum number of tracks**. Agents may assert that Israeli mortgages must contain at least two tracks; the directive says nothing of the sort. The real constraint is section 7's 66.66% cap on the variable-rate portion, which forces at least 33.34% into fixed tracks but does not otherwise dictate a track count.
- **There is no Prime-specific cap in the directive in force.** The word "prime" does not appear in it. Agents may apply an obsolete one-third Prime rule.
- The Israeli Prime rate is **not** the US Prime rate, and it is **not** the Bank of Israel rate itself. It is the BoI rate plus a fixed margin the banks publish. Agents routinely substitute the US figure, or quote the bare BoI rate as if it were Prime. Read the current Israeli prime off the bank.
- CPI-linked tracks (tzmudot madad) adjust the outstanding **principal** by the index, not just the interest payment. Agents may adjust only the interest.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Directive 329 (Limitations on Housing Loans), full text | https://www.boi.org.il/media/ez4npagt/329.pdf | LTV, PTI, variable-rate share, term, refinancing. The operative source for every limit in Step 2 |
| Directive 329 landing page (version history) | https://www.boi.org.il/roles/supervisionregulation/nbt/nbt329/ | Which version is in force and which circular amended it |
| Bank of Israel (BOI) | https://www.boi.org.il | Current BOI interest rate, Prime rate decisions, announcements |
| BOI banking supervision | https://www.boi.org.il/en/economic-roles/supervision-and-regulation/supervision-of-the-banking-system/ | LTV limits, multi-track requirement, supervisory caps |
| Bank of Israel credit data | https://www.creditdata.org.il | Free annual credit report lookup at the BOI credit bureau (BDI) |
| Dira BeHanacha (umbrella: Mechir Matara, Mechir Mufhat, Mechir LaMishtaken, Dira LeHaskir) | https://www.gov.il/he/Departments/Topics/dira | Reduced-price apartment eligibility and entitlement rules |
| Ministry of Construction housing-loan points calculator | https://www.gov.il/he/pages/mashkanta-calculator | Eligibility points and the size of the GOVERNMENT assistance loan. It is not a multi-track payment calculator, do not send users there to model a mix |

## Troubleshooting

### Error: "Bank rejected the mortgage application despite meeting LTV requirements"

Cause: Banks evaluate more than just LTV. Common rejection reasons include: payment-to-income ratio exceeding the bank's internal threshold, which is typically well below the directive's 50% prohibition and often below the 40% risk-weight cliff, insufficient employment history (banks typically want 12+ months at current employer for salaried, 2+ years of tax returns for self-employed), negative credit history at the Bank of Israel credit bureau (BDI), or existing debt obligations that push the total debt ratio too high.

Solution: Request a detailed rejection reason from the bank (they are required to provide one). Check your credit report at the Bank of Israel credit data system (available free once a year). If the issue is income ratio, consider a longer loan term to reduce monthly payments, adding a guarantor (arev), or increasing the down payment. If employment history is short, wait and reapply, or try a bank that has more flexible policies for your employment type. Some banks are more lenient with high-tech salaried employees even with shorter tenure.

### Error: "CPI-linked track costs are much higher than expected"

Cause: Many borrowers underestimate the impact of CPI linkage on their mortgage. When inflation runs at 3-4% annually, the outstanding balance on CPI-linked tracks grows significantly. For example, a 500,000 ILS CPI-linked track at 3% inflation grows to ~672,000 ILS after 10 years before any principal payments. The "low interest rate" on CPI-linked tracks is misleading because it doesn't include the inflation cost.

Solution: Always calculate the total cost of CPI-linked tracks under multiple inflation scenarios (2%, 3%, 4%). Compare the total cost (interest + CPI adjustments) against fixed non-linked tracks. In high-inflation environments (Israel averaged 3-4% in recent years), fixed non-linked tracks often end up cheaper despite their higher nominal interest rate. Consider reducing CPI exposure by allocating more to fixed non-linked and Prime tracks, keeping CPI exposure modest as a matter of judgement (note that section 7's 66.66% cap governs the VARIABLE-rate share, not CPI linkage, so there is no regulatory CPI ceiling to hide behind). Model this in a spreadsheet or a calculator that applies the index to the outstanding principal each period. Note that the gov.il "mashkanta calculator" is an eligibility-points calculator for the government assistance loan and will not model a track mix.

### Error: "Early repayment penalty is unexpectedly high on fixed-rate track"

Cause: In Israel, early repayment of fixed-rate mortgage tracks incurs a penalty if the current market rate for the same remaining term is lower than your locked rate. The penalty compensates the bank for the interest income they lose. The calculation is based on the differential between your rate and the current market rate, multiplied by the remaining balance and remaining term, discounted to present value. This can amount to tens of thousands of shekels on large fixed-rate tracks.

Solution: Check if your fixed-rate track is approaching a rate-reset date (for variable tracks) or if market rates have risen above your locked rate (in which case there's no penalty). Consider partial repayment strategies: pay off the Prime track first (no penalty ever), then variable tracks at their reset dates (no penalty on reset date). For fixed tracks, wait for a period when market rates rise above your locked rate, then refinance. Some newer mortgage agreements have capped penalties; check your original mortgage agreement (hskem halvaah) for the penalty clause.

### Error: "Different banks show different Prime rates for the same period"

Cause: The Prime rate itself is uniform across all banks (it tracks the Bank of Israel rate with a common published margin). However, the spread (the discount or premium to Prime) differs between banks and between borrowers. When a bank offers "Prime - 0.65%," the 0.65% discount is what varies. Some confusion arises because banks may quote an "effective rate" that combines the Prime rate with their spread, and the Prime rate itself changes periodically.

Solution: Always compare the spread to Prime, not the effective rate. If Bank A offers P-0.5% and Bank B offers P-0.7%, Bank B is cheaper by 0.2% regardless of what the current Prime rate is. Track Bank of Israel rate decisions (announced roughly every 6 weeks) at boi.org.il. Remember that Prime track payments change with every rate decision, so stress-test your own affordability with Prime at +1% and +2%. This is prudent practice, not a Directive 329 requirement.
