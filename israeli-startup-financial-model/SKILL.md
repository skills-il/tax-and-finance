---
name: israeli-startup-financial-model
description: >-
  Build financial models for Israeli startups with local cost structures,
  grants, and tax incentives. Use when user asks about startup runway,
  financial projections, IIA (Innovation Authority / "Rashut HaHadshnut")
  grants, R&D tax credits ("Hok HaIdud"), Angels Law (Section 20), Israeli
  employment costs (pension, "Keren Hishtalmut", "Bituach Leumi"), or
  shekel/dollar dual-currency modeling. Covers grant reporting, burn rate
  calculation, and investor-ready financial plans. Do NOT use for general
  accounting, established company finance, or non-Israeli startups.
license: MIT
compatibility: >-
  Works with Claude Code, Cursor, GitHub Copilot, Windsurf, OpenCode, Codex.
  Python 3.8+ for helper scripts.
metadata:
  author: skills-il
  version: 1.0.0
  category: tax-and-finance
  tags:
    he:
      - סטארטאפ
      - מודל-פיננסי
      - מענקים
      - רשות-החדשנות
      - מו"פ
      - ישראל
    en:
      - startup
      - financial-model
      - grants
      - iia
      - r-and-d
      - israel
  display_name:
    he: מודל פיננסי לסטארטאפ ישראלי
    en: Israeli Startup Financial Model
  display_description:
    he: >-
      בניית מודלים פיננסיים לסטארטאפים ישראליים עם מבנה עלויות מקומי, מענקי
      רשות החדשנות, הטבות מס מו"פ וחוק האנג'לים.
    en: >-
      Build financial models for Israeli startups with local cost structures,
      grants, and tax incentives. Use when user asks about startup runway,
      financial projections, IIA (Innovation Authority / "Rashut HaHadshnut")
      grants, R&D tax credits ("Hok HaIdud"), Angels Law (Section 20), Israeli
      employment costs (pension, "Keren Hishtalmut", "Bituach Leumi"), or
      shekel/dollar dual-currency modeling. Covers grant reporting, burn rate
      calculation, and investor-ready financial plans. Do NOT use for general
      accounting, established company finance, or non-Israeli startups.
  supported_agents:
    - claude-code
    - cursor
    - github-copilot
    - windsurf
    - opencode
    - codex
---

# Israeli Startup Financial Model

## Instructions

### Step 1: Define Company Stage and Structure
Ask the user about their startup:

| Stage | Hebrew | Typical Characteristics | Key Financial Needs |
|-------|--------|------------------------|---------------------|
| Pre-seed | טרום זרע | Founders only, no revenue | Runway estimation, grant eligibility |
| Seed | זרע | Small team, early product | Full financial model, IIA grant application |
| Series A | סבב A | Product-market fit, scaling | Growth projections, dual-currency model |
| Growth | צמיחה | Revenue generating, expanding | Unit economics, profitability path |

Also determine:
- **Entity type:** Israeli C-Corp (Chevra Baam), LP (Shutafut Mugbelet), or branch
- **R&D center location:** Israel-based development (required for most grants)
- **Headcount:** Current and planned team size
- **Currency exposure:** NIS costs, USD revenue (common pattern)

### Step 2: Model Israeli Employment Costs
Israeli employer costs are significantly higher than base salary. Calculate the full "employer cost" (olut maasik):

| Component | Rate | Cap (Monthly) | Notes |
|-----------|------|----------------|-------|
| Base salary (sachar basis) | 100% | -- | Gross salary |
| Pension (pensia) | 6.5% employer | Up to salary ceiling | Mandatory from day 1 |
| Severance fund (pitzuyim) | 8.33% | Up to salary ceiling | Section 14 approval common |
| Keren Hishtalmut | 7.5% employer | Up to tax-exempt ceiling | Common perk in tech |
| Bituach Leumi (employer) | ~3.5% | Up to max bracket | National Insurance |
| Health tax component | Included in BL | -- | Part of Bituach Leumi |
| Recreation pay (dmei havra'a) | ~380 NIS/month | Per year of employment | After 1 year |
| Total employer overhead | ~26-30% | -- | On top of gross salary |

Formula:
```python
employer_cost = gross_salary * (1 + 0.065 + 0.0833 + 0.075 + 0.035)
# Approximately: employer_cost = gross_salary * 1.26 to 1.30
```

### Step 3: Map IIA Grant Structures
If the startup is eligible for Innovation Authority (Rashut HaHadshnut) grants:

| Program | Grant Rate | Reporting | Key Requirements |
|---------|-----------|-----------|------------------|
| Early-stage incubator | Up to 85% | Quarterly | In approved incubator (chashamanit) |
| R&D Fund (Keren Mechkar) | 20-50% | Semi-annual | Approved R&D plan, Israeli IP |
| Binational (BIRD, BSF) | 50% | Per agreement | US-Israel collaboration |
| Multinational collaboration | 30-50% | Per agreement | With approved foreign entity |

Key rules:
- Grants create a **royalty obligation** (tamlugim): typically 3-5% of revenue until repaid
- **IP must remain in Israel** unless approved by IIA committee
- Approved budget (taktziv me'ushar) defines eligible expenses
- Must file reports on time or risk grant clawback

### Step 4: Apply Tax Incentives
Layer in available tax benefits:

**R&D Tax Credits (Hok HaIdud / Encouragement of R&D Law):**
- Up to 40% tax credit on qualifying R&D expenditures
- Must have "Preferred Enterprise" (Mifal Muadaf) or "Preferred Technology Enterprise" status
- Application through IIA for technology enterprise classification

**Angels Law (Section 20 / Hok HaAngels):**
- Individual investors in qualifying R&D companies get tax deductions
- Investment deductible over 3 years against any income (not just capital gains)
- Company must be Israeli, under 5 years old, revenue under 50M NIS
- Maximum investment for deduction: varies by year (check current limits)
- Investor cannot hold more than 49% of the company

**Preferred Enterprise Tax Rates:**

| Benefit Track | Corporate Tax | Dividend Withholding | Requirements |
|---------------|---------------|---------------------|--------------|
| Preferred Enterprise | 7.5% (Zone A) / 16% (other) | 20% | Export revenue over 25% |
| Preferred Technology Enterprise | 7.5% (Zone A) / 12% (other) | 4-20% | IP income, R&D criteria |
| Special Preferred Technology | 6% | 4% | Revenue over 10B NIS |

### Step 5: Build Dual-Currency Model
Most Israeli startups operate in both NIS and USD:

| Item | Typical Currency | Notes |
|------|-----------------|-------|
| Employee salaries | NIS | Including all employer costs |
| Office rent | NIS | Often linked to CPI (madad) |
| Cloud infrastructure | USD | AWS, GCP, Azure |
| Revenue (SaaS) | USD | International customers |
| IIA grant disbursements | NIS | Received in NIS |
| Investor funding rounds | USD | SAFEs, equity rounds |

Model approach:
```python
# Monthly burn rate in dual currency
nis_costs = salaries_nis + rent_nis + local_expenses_nis
usd_costs = cloud_usd + tools_usd + travel_usd
total_burn_usd = (nis_costs / exchange_rate) + usd_costs
runway_months = cash_balance_usd / total_burn_usd
```

Use `scripts/model_runway.py` for automated runway calculations.

### Step 6: Generate Financial Projections
Create a 24-36 month projection including:
1. **Revenue forecast:** MRR/ARR growth with assumptions clearly stated
2. **Cost structure:** Headcount plan with Israeli employer costs
3. **Cash flow:** Monthly cash in/out including grant disbursements
4. **Runway:** Months until cash reaches zero or next funding needed
5. **Key metrics:** Burn rate, burn multiple, LTV/CAC (if applicable)
6. **Scenario analysis:** Base case, upside, downside with different exchange rate assumptions

### Step 7: Prepare Grant Reporting
If the startup has an active IIA grant, generate reporting data:
- **Eligible expenses:** Only expenses approved in the grant budget
- **Co-funding match:** Ensure company matches its share of the budget
- **Milestone tracking:** R&D milestones as defined in the approved plan
- **Royalty projection:** Estimate future royalty payments based on revenue forecast

## Examples

### Example 1: Pre-Seed Runway Calculation
User says: "I have 2 founders and 500K USD. How long can we last with 3 developers in Israel?"
Actions:
1. Calculate: 3 developers at average 30,000 NIS/month gross
2. Add employer overhead: 30,000 * 1.28 = 38,400 NIS per developer
3. Add founders (minimal salary): 15,000 NIS each with overhead = 38,400 NIS total
4. Monthly NIS burn: (38,400 * 3) + 38,400 = 153,600 NIS
5. Add cloud/tools: ~2,000 USD/month
6. Convert at ~3.6 NIS/USD: total ~44,700 USD/month
7. Runway: 500,000 / 44,700 = ~11 months
Result: Detailed runway breakdown with headcount and currency split

### Example 2: IIA Grant Application Model
User says: "We're applying for an IIA R&D fund grant. Help me build the budget"
Actions:
1. Determine approved budget categories (salaries, subcontractors, materials, overhead)
2. Model R&D team costs with Israeli employer overhead
3. Apply grant percentage (typically 20-50%)
4. Calculate company co-funding requirement
5. Project royalty obligation based on revenue estimates
6. Generate budget table in IIA-required format
Result: Grant budget model with eligible expenses and co-funding plan

### Example 3: Angels Law Tax Benefit
User says: "An angel wants to invest 1M NIS. What tax benefit does he get under Section 20?"
Actions:
1. Verify company eligibility (Israeli R&D, under 5 years, revenue under 50M NIS)
2. Check investor eligibility (individual, will hold under 49%)
3. Calculate deduction: 1,000,000 NIS deductible over 3 years
4. At top marginal rate (50%): potential tax saving up to 500,000 NIS over 3 years
5. Note: Subject to approval and holding period requirements
Result: Tax benefit analysis for the angel investor with eligibility checklist

### Example 4: Series A Financial Model
User says: "Build a 24-month model. We have 10 employees, raising 5M USD Series A"
Actions:
1. Map current team with Israeli employment costs
2. Build hiring plan with ramp-up timeline
3. Model revenue growth from current MRR
4. Include IIA grant cash flows if applicable
5. Dual-currency projection with NIS salaries and USD revenue
6. Run `python scripts/model_runway.py --employees 10 --funding 5000000`
7. Generate scenario analysis (base, optimistic, pessimistic)
Result: Complete 24-month P&L and cash flow with runway analysis

## Bundled Resources

### Scripts
- `scripts/model_runway.py` -- Calculates startup runway with Israeli cost structure. Includes employer overhead, dual-currency modeling, and grant impact. Run: `python scripts/model_runway.py --help`

### References
- `references/iia-grants.md` -- Innovation Authority grant programs: eligibility criteria, application process, reporting requirements, royalty obligations, and IP restrictions. Consult when helping with grant applications or compliance.
- `references/tax-incentives.md` -- Israeli startup tax incentives: R&D credits (Hok HaIdud), Angels Law (Section 20), Preferred Enterprise tracks, and employee stock option taxation (Section 102). Consult when modeling tax impact on startup financials.

## Troubleshooting

### Error: "Employer cost calculation seems too low"
Cause: Missing one or more mandatory components (pension, severance, Bituach Leumi)
Solution: Use the full employer overhead formula in Step 2. Minimum overhead is ~22% even without Keren Hishtalmut. Most tech companies offer Keren Hishtalmut, pushing it to ~28%.

### Error: "IIA budget rejected"
Cause: Including non-eligible expenses or exceeding approved categories
Solution: Only include expenses from IIA-approved categories. Common mistake: including marketing costs in R&D budget. General overhead is typically limited to 20-25% of direct costs.

### Error: "Currency mismatch in projections"
Cause: Mixing NIS and USD without consistent conversion
Solution: Pick a presentation currency (usually USD for investors) and convert all NIS items using a stated exchange rate assumption. Include sensitivity analysis for +/-10% rate changes.

### Error: "Angels Law eligibility unclear"
Cause: Company may not meet all Section 20 requirements
Solution: Verify: Israeli company, R&D focused, under 5 years from founding, revenue under 50M NIS, investor will hold under 49%. Consult a tax advisor (yo'etz mas) for formal ruling.
