---
name: israeli-budget-planner
description: >-
  Plan household and personal budgets with Israeli-specific costs, rates, and
  financial products. Use when user asks about budgeting in Israel, mortgage
  (mashkanta) calculations, arnona rates, cost of living, "takciv", or monthly
  expense planning. Covers Bank of Israel prime rate, mashkanta tracks,
  arnona by city, Sal Briut costs, and Israeli household benchmarks. Do NOT
  use for business accounting, tax filing, or investment portfolio management.
license: MIT
compatibility: No network required. Works offline with reference data.
metadata:
  author: skills-il
  version: 1.0.0
  category: tax-and-finance
  tags:
    he:
      - תקציב
      - משכנתא
      - ארנונה
      - יוקר-המחיה
      - חיסכון
      - ישראל
    en:
      - budget
      - mortgage
      - arnona
      - cost-of-living
      - savings
      - israel
  display_name:
    he: מתכנן תקציב ישראלי
    en: Israeli Budget Planner
  display_description:
    he: תכנון תקציב משק בית עם עלויות, שיעורים ומוצרים פיננסיים ישראליים
    en: >-
      Plan household and personal budgets with Israeli-specific costs, rates,
      and financial products. Use when user asks about budgeting in Israel,
      mortgage (mashkanta) calculations, arnona rates, cost of living,
      "takciv", or monthly expense planning. Covers Bank of Israel prime rate,
      mashkanta tracks, arnona by city, Sal Briut costs, and household
      benchmarks.
  supported_agents:
    - claude-code
    - cursor
    - github-copilot
    - windsurf
    - opencode
    - codex
---

# Israeli Budget Planner

## Instructions

### Step 1: Understand Key Israeli Financial Rates
Reference rates that affect household budgets:

| Rate/Index | Hebrew | Value (Reference) | Updated |
|-----------|--------|-------------------|---------|
| BOI Interest Rate | ריבית בנק ישראל | 4.50% | Check boi.org.il for current |
| Prime Rate (Ribit HaPrime) | ריבית פריים | BOI rate + 1.50% = ~6.00% | Follows BOI decisions |
| CPI (Madad) | מדד המחירים לצרכן | Published monthly by CBS | cbs.gov.il |
| Average Wage | שכר ממוצע | ~12,500 NIS/month | CBS data |
| Minimum Wage | שכר מינימום | 5,880.02 NIS/month (as of 2024) | Updated by law |
| VAT (Ma'am) | מע"מ | 17% | Standard rate |
| National Insurance (Bituach Leumi) | ביטוח לאומי | 3.5%/12% of income | Two-tier rates |
| Health Tax (Mas Briut) | מס בריאות | 3.1%/5% of income | Two-tier rates |

**Note:** Always verify current BOI rate at boi.org.il as it changes with monetary policy decisions (announced ~6 times per year).

### Step 2: Calculate Mashkanta (Mortgage) Payments
Israeli mortgages (mashkantaot) are structured with multiple tracks (maslulim):

| Track | Hebrew | Rate Type | Typical Rate Range |
|-------|--------|-----------|-------------------|
| Prime-linked (Tzmuda LaPrime) | צמודת פריים | Variable: Prime +/- spread | Prime - 0.5% to Prime + 0.5% |
| Fixed unlinked (Kvua Lo Tzmuda) | קבועה לא צמודה | Fixed for full term | 4.5% - 6.5% |
| CPI-linked fixed (Kvua Tzmudat Madad) | קבועה צמודת מדד | Fixed + CPI adjustments | 3.0% - 5.0% + CPI |
| CPI-linked variable (Mishtana Tzmudat Madad) | משתנה צמודת מדד | Resets every 5 years + CPI | 2.5% - 4.5% + CPI |
| Fixed unlinked short (Kvua Lo Tzmuda Ktzara) | קבועה לא צמודה קצרה | Fixed for 5-10 years | 4.0% - 5.5% |

**BOI mashkanta regulations:**
- Maximum LTV (Loan-to-Value): 75% for first home, 50% for investment property, 70% for home upgrade
- Maximum variable-rate portion: 33.33% of total mortgage
- Maximum CPI-linked portion: 33.33% of total mortgage
- Mandatory life insurance and property insurance

**Monthly payment formula (PMT):**
```
Monthly Payment = P * [r(1+r)^n] / [(1+r)^n - 1]
Where:
  P = Principal (loan amount)
  r = Monthly interest rate (annual rate / 12)
  n = Total number of payments (years * 12)
```

### Step 3: Estimate Arnona (Municipal Property Tax)
Arnona rates vary significantly by city and property type:

| City | Residential (NIS/sqm/month, approx.) | Notes |
|------|--------------------------------------|-------|
| Tel Aviv | 85-130 | Highest in Israel, varies by neighborhood |
| Jerusalem | 55-80 | Lower than TA, exemptions for new olim |
| Haifa | 45-65 | Relatively affordable |
| Beer Sheva | 35-50 | Lowest among major cities |
| Raanana | 70-95 | High, affluent suburb |
| Herzliya | 75-100 | Coastal premium |
| Netanya | 50-70 | Mid-range |
| Rishon LeZion | 55-75 | Growing city |
| Petah Tikva | 50-70 | Central district |

**Arnona calculation:**
```
Monthly arnona = Rate per sqm * Apartment size in sqm
Annual arnona = Monthly * 12
```

**Discounts available (hanacha):**
- New immigrants (olim chadashim): Up to 90% discount for first year
- Soldiers (chayalim): Various discounts
- Elderly/disabled: Up to 30-70% discount
- Low income: Means-tested discounts
- Single parents: Additional discounts
- Pay full year upfront: ~2% discount

### Step 4: Build Monthly Budget Template
Standard Israeli household expense categories:

| Category | Hebrew | Typical Range (couple + 1 child) | % of Income |
|----------|--------|----------------------------------|-------------|
| Housing (rent/mortgage) | דיור | 4,000-8,000 NIS | 25-35% |
| Arnona | ארנונה | 400-800 NIS | 3-5% |
| Va'ad Bayit (building maintenance) | ועד בית | 150-500 NIS | 1-3% |
| Electricity (Cheshbon Chashmal) | חשמל | 300-600 NIS | 2-4% |
| Water (Mei Mekorot) | מים | 100-200 NIS | 1% |
| Gas (Gaz) | גז | 80-150 NIS | 0.5-1% |
| Groceries (Makolet/Super) | מזון | 2,500-4,500 NIS | 15-25% |
| Transportation | תחבורה | 500-1,500 NIS | 3-8% |
| Health (Kupat Cholim) | בריאות | 200-500 NIS | 1-3% |
| Education/Childcare (Gan/Maon) | חינוך | 1,500-3,500 NIS | 8-15% |
| Internet + Phone (Selulari) | אינטרנט + סלולרי | 200-400 NIS | 1-2% |
| Insurance (Bituach) | ביטוח | 300-800 NIS | 2-4% |
| Savings/Pension (Pensia) | חיסכון/פנסיה | Mandatory employer contribution | 6-7% employee |

### Step 5: Israeli-Specific Budget Considerations

**Mandatory deductions from salary:**
- National Insurance (Bituach Leumi): 3.5% on income up to 7,122 NIS, 12% above (2024 brackets)
- Health Tax (Mas Briut): 3.1% up to 7,122 NIS, 5% above
- Income Tax (Mas Hachnasa): Progressive brackets 10%-50%
- Pension: 6% employee + 6.5% employer (mandatory since 2008)

**Seasonal expenses to budget for:**
- High Holidays (September/October): Gifts, food, travel
- Passover (March/April): Special food costs, vacation
- Back-to-school (August/September): Supplies, uniforms
- Annual car expenses: Test (techni), insurance, licensing (rishayon rechev)
- Annual Bituach Leumi adjustments (January)

**Sal Briut (Health Basket):**
- Monthly health tax covers basic kupat cholim membership
- Supplemental insurance (mashlim): ~50-150 NIS/month per person
- Dental, vision typically not covered in basic basket

### Step 6: Savings and Investment Vehicles
| Vehicle | Hebrew | Tax Benefit | Liquidity |
|---------|--------|-------------|-----------|
| Pension Fund (Keren Pensia) | קרן פנסיה | Tax-deductible contributions | Locked until retirement |
| Provident Fund (Kupat Gemel) | קופת גמל | Capital gains tax exempt | 6-year lock for tax benefit |
| Study Fund (Keren Hishtalmut) | קרן השתלמות | Tax-free after 6 years | 6-year minimum |
| Savings Account (Tochni Chisachon) | תוכנית חיסכון | Interest taxed at 15-25% | Varies |
| ETFs/Mutual Funds | קרנות נאמנות | Capital gains 25% | Liquid |

## Examples

### Example 1: First-Time Homebuyer Budget
**Input:** "I earn 15,000 NIS/month, how much mashkanta can I afford?"
**Output:** Calculate maximum monthly payment (~30% of net income), show mortgage amounts for different terms (20/25/30 years), explain track mixing strategy per BOI rules, estimate total monthly housing costs including arnona and va'ad bayit.

### Example 2: Monthly Budget Review
**Input:** "Create a monthly budget for a family in Tel Aviv earning 25,000 NIS combined"
**Output:** Build detailed budget template with Tel Aviv-specific costs (high arnona, rental market), show mandatory deductions, categorize expenses, identify savings potential, suggest keren hishtalmut optimization.

### Example 3: City Comparison
**Input:** "Compare cost of living between Tel Aviv and Beer Sheva"
**Output:** Side-by-side comparison of arnona, rent/housing costs, grocery prices, transportation costs. Quantify monthly savings from relocation. Note salary differential between cities.

### Example 4: Mashkanta Calculation
**Input:** "Calculate mortgage payments for 1.5 million NIS over 25 years"
**Output:** Show payment breakdown by track (prime-linked, fixed, CPI-linked), demonstrate mixed portfolio per BOI guidelines, calculate total interest paid, compare early repayment scenarios.

## Troubleshooting

### Error: "Interest rates seem wrong"
Cause: BOI rate changes affect prime-linked products immediately
Solution: Always check current BOI rate at boi.org.il/en/monetary-policy. The prime rate is always BOI rate + 1.5%. Last major change cycles happened 2022-2024.

### Error: "Arnona rate doesn't match my bill"
Cause: Arnona has surcharges for heating zones, building age, floor level
Solution: Check your specific municipality website for detailed rate tables. Rates shown here are averages. Apply for eligible discounts (hanacha) through your local iriya.

### Error: "Budget doesn't balance with take-home pay"
Cause: Forgetting mandatory deductions (Bituach Leumi, Mas Briut, pension)
Solution: Calculate net salary first by subtracting all mandatory deductions. Use net (not gross) as the starting point for budgeting. Typical take-home is 55-70% of gross for most brackets.
