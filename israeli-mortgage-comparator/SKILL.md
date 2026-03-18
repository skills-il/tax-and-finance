---
name: israeli-mortgage-comparator
description: >-
  Compare mortgage tracks (maslulei mashkanta) across Israeli banks, calculate monthly
  payments for mixed-track portfolios, and understand Bank of Israel regulations including
  LTV limits and CPI-linked caps. Use when a user needs to evaluate mortgage offers
  from different banks, calculate refinancing savings, or understand how Prime rate
  changes affect their payments. Covers Leumi, Hapoalim, Discount, Mizrachi-Tefahot,
  FIBI, Mercantile, and Yahav. Do NOT use for commercial real estate loans, business
  credit lines, or non-Israeli mortgage products.
license: MIT
allowed-tools: Bash(python:*) WebFetch
metadata:
  author: skills-il
  version: 1.0.1
  category: tax-and-finance
  tags:
    he:
    - משכנתא
    - בנקים
    - ריבית
    - השוואת מחירים
    - נדל"ן
    - פריים
    en:
    - mortgage
    - banks
    - interest-rate
    - price-comparison
    - real-estate
    - prime-rate
  display_name:
    he: השוואת משכנתאות בישראל
    en: Israeli Mortgage Comparator
  display_description:
    he: >-
      השוואת מסלולי משכנתא בין בנקים ישראליים, חישוב תשלומים חודשיים והבנת תקנות בנק
      ישראל
    en: >-
      Compare mortgage tracks (maslulei mashkanta) across Israeli banks, calculate
      monthly payments for mixed-track portfolios, and understand Bank of Israel regulations
      including LTV limits and CPI-linked caps. Use when a user needs to evaluate
      mortgage offers from different banks, calculate refinancing savings, or understand
      how Prime rate changes affect their payments. Covers Leumi, Hapoalim, Discount,
      Mizrachi-Tefahot, FIBI, Mercantile, and Yahav. Do NOT use for commercial real
      estate loans, business credit lines, or non-Israeli mortgage products.
  supported_agents:
  - claude-code
  - cursor
  - github-copilot
  - windsurf
  - opencode
  - codex
---

# Israeli Mortgage Comparator

## Instructions

### Step 1: Understand the Israeli Mortgage System

The Israeli mortgage system is unique. Unlike most countries where you take a single loan at one rate, Israeli mortgages are composed of multiple parallel tracks (maslulim), each with different interest rate mechanisms. A typical mortgage combines 3-5 tracks to balance risk and cost.

**The 5 main mortgage tracks:**

1. **Prime (ריבית פריים)** - Variable rate linked to the Bank of Israel prime rate. Currently prime = Bank of Israel rate + 1.5%. Changes whenever the central bank adjusts its rate. Expressed as "Prime minus X%" (e.g., Prime - 0.5%).

2. **Fixed Non-Linked (קבועה לא צמודה)** - Fixed interest rate, not linked to CPI. The safest track: your payment never changes for the entire loan period. Typically the highest starting interest rate.

3. **Fixed CPI-Linked (קבועה צמודה למדד)** - Fixed interest rate but the principal is linked to the Consumer Price Index (madad). Lower starting rate than fixed non-linked, but your outstanding balance grows with inflation.

4. **Variable CPI-Linked (משתנה צמודה למדד)** - Variable interest rate (resets every 5 years) and principal linked to CPI. Double exposure: both rate changes and inflation adjustments.

5. **Variable Non-Linked (משתנה לא צמודה)** - Variable interest rate (resets every 5 years), not linked to CPI. Rate adjusts periodically but no inflation linkage.

### Step 2: Know the Bank of Israel Regulations

Bank of Israel imposes strict regulations on mortgage composition. These are critical for comparison:

**Loan-to-Value (LTV) limits:**
- First apartment (dira rishona): up to 75% of property value
- Apartment upgrade (dira l'shipur diur): up to 70%
- Investment property (dira l'hashkaa): up to 50%
- These are maximum limits; banks can offer less

**Track composition limits:**
- CPI-linked tracks: maximum 66.67% (two-thirds) of total mortgage
- Variable rate tracks (any type): maximum 33.33% (one-third) of total mortgage
- Prime track: counted as variable, so limited to one-third
- These limits prevent over-concentration of risk in any single type

**Payment-to-income ratio:**
- Maximum monthly payment should not exceed approximately 40% of net household income
- Banks calculate this based on a stress test assuming interest rate increases

### Step 3: Gather User's Financial Details

Collect the following to enable accurate comparison:

- **Property price** (ILS)
- **Down payment amount** (at least 25% for first apartment, 30% for upgrade, 50% for investment)
- **Desired loan term** (typically 15-30 years; maximum 30 years in Israel)
- **Net monthly household income** (both spouses if applicable)
- **Purchase type**: first apartment, upgrade (selling existing and buying), or investment
- **Employment type**: salaried (sachir), self-employed (atzmai), or mixed
- **Existing debts**: car loans, credit cards, other obligations
- **Age of youngest borrower** (loan term + age cannot exceed 75 in most banks)

### Step 4: Build Track Combinations for Comparison

Design 3-4 different track combinations that comply with Bank of Israel regulations. Here are common strategies:

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

**Mechir LaMishtaken (מחיר למשתכן):**
- Government subsidized housing lottery for eligible buyers
- Discounted property prices (typically 20-30% below market)
- Eligibility based on housing history and marital status
- Special mortgage terms may apply for these properties

**First-time buyer benefits:**
- Reduced purchase tax (mas rechisha): 0% on first ~1.9M ILS, graduated rates above
- Higher LTV availability (75% vs. 70% for upgrade)

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
2. Verify payment-to-income ratio: monthly payments should stay below ~10,000 ILS (40% of 25,000)
3. Request the specific rate offers from both banks for each track
4. Design 3 track combinations respecting BoI regulations (max 66.67% CPI-linked, max 33.33% variable)
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
1. Apply investment property rules: maximum LTV is 50%, so user needs at least 900,000 ILS down payment
2. Maximum loan: 900,000 ILS
3. Note higher purchase tax rates for second property (8% on first ~6M ILS as of current rates)
4. Investment property mortgages often get slightly worse rates from banks
5. Calculate rental yield to determine if the investment makes financial sense after mortgage payments
6. Design track combinations optimized for investment (shorter terms often better for investment properties)
7. Compare rates from 3+ banks, noting some banks are more friendly to investment property mortgages

Result: User receives the LTV constraint analysis, total acquisition cost (including higher purchase tax), mortgage payment projections vs. expected rental income, and a comparison of bank offers for investment property mortgages.

## Gotchas
- Israeli mortgages (mashkantaot) must contain at least two tracks (maslulim) by Bank of Israel regulation. Agents may suggest a single-track mortgage, which is not allowed.
- The Prime rate in Israel (ribit prime) is the BOI rate + 1.5%. Agents may use the US Prime rate (which has a different spread) or forget to add the 1.5% margin.
- CPI-linked mortgage tracks (tzmudot madad) adjust the outstanding principal by the CPI index, not just the interest rate. Agents may only adjust the interest payment without also adjusting the principal.
- Israeli banks charge a "ptor me-onesh" (early repayment penalty) that varies by track type. Agents may suggest refinancing without accounting for this penalty, which can be 0.5-2% of the remaining balance.

## Troubleshooting

### Error: "Bank rejected the mortgage application despite meeting LTV requirements"

Cause: Banks evaluate more than just LTV. Common rejection reasons include: payment-to-income ratio exceeding the bank's internal threshold (varies 35-40%), insufficient employment history (banks typically want 12+ months at current employer for salaried, 2+ years of tax returns for self-employed), negative credit history at the Bank of Israel credit bureau (BDI), or existing debt obligations that push the total debt ratio too high.

Solution: Request a detailed rejection reason from the bank (they are required to provide one). Check your credit report at the Bank of Israel credit data system (available free once a year). If the issue is income ratio, consider a longer loan term to reduce monthly payments, adding a guarantor (arev), or increasing the down payment. If employment history is short, wait and reapply, or try a bank that has more flexible policies for your employment type. Some banks are more lenient with high-tech salaried employees even with shorter tenure.

### Error: "CPI-linked track costs are much higher than expected"

Cause: Many borrowers underestimate the impact of CPI linkage on their mortgage. When inflation runs at 3-4% annually, the outstanding balance on CPI-linked tracks grows significantly. For example, a 500,000 ILS CPI-linked track at 3% inflation grows to ~672,000 ILS after 10 years before any principal payments. The "low interest rate" on CPI-linked tracks is misleading because it doesn't include the inflation cost.

Solution: Always calculate the total cost of CPI-linked tracks under multiple inflation scenarios (2%, 3%, 4%). Compare the total cost (interest + CPI adjustments) against fixed non-linked tracks. In high-inflation environments (Israel averaged 3-4% in recent years), fixed non-linked tracks often end up cheaper despite their higher nominal interest rate. Consider reducing CPI exposure by allocating more to fixed non-linked and Prime tracks, staying well below the 66.67% CPI maximum. Use spreadsheet calculations or online mortgage calculators (like the one at mashkanta.co.il) that properly account for CPI linkage.

### Error: "Early repayment penalty is unexpectedly high on fixed-rate track"

Cause: In Israel, early repayment of fixed-rate mortgage tracks incurs a penalty if the current market rate for the same remaining term is lower than your locked rate. The penalty compensates the bank for the interest income they lose. The calculation is based on the differential between your rate and the current market rate, multiplied by the remaining balance and remaining term, discounted to present value. This can amount to tens of thousands of shekels on large fixed-rate tracks.

Solution: Check if your fixed-rate track is approaching a rate-reset date (for variable tracks) or if market rates have risen above your locked rate (in which case there's no penalty). Consider partial repayment strategies: pay off the Prime track first (no penalty ever), then variable tracks at their reset dates (no penalty on reset date). For fixed tracks, wait for a period when market rates rise above your locked rate, then refinance. Some newer mortgage agreements have capped penalties; check your original mortgage agreement (hskem halvaah) for the penalty clause.

### Error: "Different banks show different Prime rates for the same period"

Cause: The Prime rate itself is uniform across all banks (Bank of Israel rate + 1.5%). However, the spread (the discount or premium to Prime) differs between banks and between borrowers. When a bank offers "Prime - 0.65%," the 0.65% discount is what varies. Some confusion arises because banks may quote an "effective rate" that combines the Prime rate with their spread, and the Prime rate itself changes periodically.

Solution: Always compare the spread to Prime, not the effective rate. If Bank A offers P-0.5% and Bank B offers P-0.7%, Bank B is cheaper by 0.2% regardless of what the current Prime rate is. Track Bank of Israel rate decisions (announced roughly every 6 weeks) at boi.org.il. Remember that Prime track payments will change with every rate decision, so stress-test your affordability with Prime at +1% and +2% above current levels.
