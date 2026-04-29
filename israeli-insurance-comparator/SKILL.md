---
name: israeli-insurance-comparator
description: Compare car insurance (mandatory hova, comprehensive makif, third-party), home insurance, and health supplementary insurance across 20+ Israeli insurers using official government calculators and private comparison platforms. Use when a user needs to find the cheapest insurance quote, understand policy differences, or prepare for annual renewal negotiations. Guides through CMA calculator at car.cma.gov.il, Hova.co.il, Shukabit, Wobi, and Bestie. Do NOT use for life insurance, pension fund selection, or travel insurance comparisons.
license: MIT
allowed-tools: Bash(python:*) WebFetch
---

# Israeli Insurance Comparator

## Instructions

### Step 0: Inventory Existing Policies via Har HaBituach

Before comparing offers, the user should pull their existing policy inventory from **Har HaBituach** (`https://harb.cma.gov.il/`), the CMA-operated personal-policy aggregator. Har HaBituach lists every policy the user holds across all Israeli insurers (life, health, pension, disability, mortgage life, supplementary HMO, manager's insurance, etc.). Many users discover overlapping or expired coverage they had forgotten. Skipping this step is the most common reason a comparison ends up over-insuring or duplicating coverage.

Authentication is via Israeli ID + a one-time SMS or email code. The interface is Hebrew-only.

### Step 1: Identify the Insurance Type Needed

Determine which insurance product the user is comparing. Israeli insurance falls into these main categories:

**Car Insurance (3 types):**
- **Bituach Hova (ביטוח חובה)** - Mandatory by law under the Victims of Road Accidents Law (חוק הפיצויים). Covers bodily injury only. Every vehicle on the road must have this.
- **Bituach Makif (ביטוח מקיף)** - Comprehensive insurance covering theft, fire, damage to your car, and third-party property damage. Optional but very common.
- **Bituach Tzad Gimel (ביטוח צד ג׳)** - Third-party only. Covers damage you cause to others' property but not your own vehicle. Cheaper alternative to makif.

**Home Insurance (2 components):**
- **Mivne (מבנה)** - Building structure coverage. Often required by mortgage lender.
- **Tochen (תוכן)** - Contents coverage. Protects furniture, electronics, personal items.

**Health Supplementary Insurance:**
- **Bituach Mashlim (ביטוח משלים)** - Supplementary insurance from kupot cholim (health funds) beyond the basic basket of services.

### Step 2: Gather Required Details for Comparison

Before comparing, collect these details from the user:

**For car insurance:**
- Full name and Israeli ID number (teudat zehut)
- Date of birth and driving license issue date
- Vehicle details: manufacturer, model, year, engine size, license plate number
- City of residence (affects premium significantly)
- Claims history in the past 3 years
- Current insurer and policy expiration date
- Number of years with no claims (shin-nun years - shanim lelo tvi'ot)

**For home insurance:**
- Property address and floor number
- Apartment size in square meters
- Year of construction
- Type (apartment, house, penthouse)
- Estimated rebuild value (for structure) and contents value
- Whether there's a mortgage (lender may require specific coverage)
- Security features (alarm, safe, bars)

**For health supplementary insurance:**
- Age of all family members to be covered
- Current kupat cholim (Clalit, Maccabi, Meuhedet, Leumit)
- Current supplementary tier (if any)
- Specific medical needs (surgeries, specialists, medications)

### Step 3: Use Government Comparison Tools

Start with official government calculators for unbiased baseline pricing:

**For mandatory car insurance (bituach hova):**
1. Navigate to **car.cma.gov.il** - the Capital Market Authority (CMA / רשות שוק ההון) official insurance calculator
2. Enter vehicle and driver details
3. The system queries all licensed insurers in real time and returns sorted quotes
4. Results show: insurer name, annual premium, monthly payment option, and coverage details
5. Note: This is the most reliable source as insurers are required by law to provide accurate quotes

**For comprehensive car insurance comparison:**
1. Navigate to **govcarins.mof.gov.il** - Ministry of Finance simulator
2. This tool helps estimate comprehensive insurance costs and understand coverage components
3. Compare deductible amounts (hashtatfut atzmit) across insurers

### Step 4: Use Private Comparison Platforms

After getting the government baseline, check private platforms for potentially better deals:

**Hova.co.il (hova.co.il):**
- Specializes in mandatory car insurance (bituach hova)
- Quick quote process: enter license plate + ID number
- Shows real-time quotes from multiple insurers
- Can purchase directly through the platform

**Shukabit (shukabit.co.il):**
- Comprehensive insurance comparison platform
- Covers car (all types), home, health, and travel insurance
- Provides side-by-side policy comparison tables
- Shows coverage differences, not just price

**Wobi (wobi.co.il):**
- Large Israeli insurance comparison site (acquired by The Phoenix Holdings in Oct 2025)
- Covers car, home, health, life, and business insurance
- Offers phone consultation with licensed agents
- Can handle the entire purchase process
- Note: Since the Phoenix acquisition, Wobi is no longer fully independent. Cross-check quotes with other platforms

**Bestie (bestie.co.il):**
- Independent comparison platform (not an insurer or broker)
- Provides personalized recommendations based on a short questionnaire
- Covers car, home, health, and mortgage insurance
- Good for understanding which coverage level you actually need

**InsuranceFind (insurancefind.co.il):**
- Aggregates quotes from multiple insurers
- Good for niche insurance products

### Step 5: Compare Car Insurance Quotes

When comparing car insurance, build a comparison table with these columns:

| Factor | Insurer A | Insurer B | Insurer C |
|--------|-----------|-----------|-----------|
| Annual premium | | | |
| Monthly payment (if available) | | | |
| Deductible (hashtatfut atzmit) | | | |
| Towing included | | | |
| Replacement car (rechev chalufi) | | | |
| Glass coverage (without deductible) | | | |
| New-for-old car policy (age limit) | | | |
| Roadside assistance | | | |
| Approved garages vs. free choice | | | |

Key considerations:
- **Shin-nun discount**: More years without claims means lower premiums. Verify your shin-nun status is correctly reported.
- **Deductible tradeoff**: Lower deductible means higher premium. For good drivers, a higher deductible often saves money overall.
- **Approved garages**: Some policies require using the insurer's approved garage network. Free-choice (bchirat musach chofshit) costs more but gives you flexibility.
- **Replacement car**: Check how many days of replacement car are included and what size vehicle.

### Step 6: Compare Home Insurance Quotes

For home insurance, compare:

| Factor | Insurer A | Insurer B | Insurer C |
|--------|-----------|-----------|-----------|
| Structure coverage amount | | | |
| Contents coverage amount | | | |
| Annual premium | | | |
| Earthquake coverage included | | | |
| Water damage (pipe burst) | | | |
| Theft deductible | | | |
| Third-party liability | | | |
| Loss of rent coverage | | | |

Important notes:
- **Earthquake coverage**: Since 2013, standard policies include earthquake coverage per the Israeli Earthquake Insurance Pool. Verify this is included.
- **Mortgage requirement**: If you have a mortgage, the bank typically requires structure insurance assigned (meshuabed) to the bank. Ask the insurer about bank assignment.
- **Underinsurance penalty**: If your coverage amount is less than the actual value, the insurer can apply a proportional reduction (klal yachasi) to any claim.

### Step 7: Compare Health Supplementary Insurance

Israeli health supplementary insurance operates in tiers from each kupat cholim:

**Clalit (Clalit Mushlam / Clalit Platinum):**
- Mushlam: Basic supplementary tier
- Platinum: Premium tier with shorter wait times and broader specialist access

**Maccabi (Maccabi Sheli / Maccabi Zahav):**
- Maccabi Sheli: Basic supplementary
- Maccabi Zahav: Premium tier

**Meuhedet (Meuhedet Adif / Meuhedet Si):**
- Adif: Basic supplementary
- Si: Premium tier

**Leumit (Leumit Kesef / Leumit Zahav):**
- Kesef: Basic supplementary
- Zahav: Premium tier

Compare these factors:
- Monthly premium per family member (varies by age)
- Surgery in private hospitals: coverage percentage and ceiling
- Specialist consultations: co-pay amount and availability
- Advanced medications not in the health basket
- Dental coverage
- Fertility treatments coverage
- Second opinion from abroad
- Rehabilitation services

### Step 8: Negotiate and Optimize

After gathering comparison data:

1. **Contact your current insurer** with competitor quotes. Retention departments often match or beat competitor pricing.
2. **Bundle policies**: Ask about discounts for holding multiple policies (car + home) with the same insurer.
3. **Timing**: Renew or switch 30-60 days before policy expiration. Last-minute renewals reduce negotiating power.
4. **Annual payment**: Paying annually instead of monthly often saves 5-8%.
5. **Increase deductible**: If you can afford a higher out-of-pocket expense, raising the deductible can significantly reduce premiums.
6. **Review coverage annually**: Life changes (new car, moved to a safer area, kids left home) can affect premiums.

### Step 9: Read and Understand the Policy

Before finalizing any insurance purchase:

1. **Polisa (פוליסה)**: Read the full policy document, not just the summary
2. **Exclusions (חריגים)**: Identify what is NOT covered
3. **Waiting periods (תקופת אכשרה)**: Some coverages activate only after a waiting period
4. **Cancellation terms**: Understand penalties for early cancellation
5. **Claims process**: Know how to file a claim (tvi'a) and required documentation
6. **Complaint channel**: The CMA (Rasha) handles consumer complaints at pe.cma.gov.il

## Examples

### Example 1: First-Time Car Insurance Buyer

User says: "I just bought a 2024 Hyundai i20 and I need car insurance. I live in Tel Aviv, I'm 28 years old, and got my license at 18."

Actions:
1. Clarify the user needs both bituach hova (mandatory) and likely bituach makif (comprehensive) for a new car
2. Guide them to car.cma.gov.il to get mandatory insurance quotes from all licensed insurers
3. Collect vehicle details: 2024 Hyundai i20, approximate engine size 1.2L
4. Note premium-affecting factors: Tel Aviv (higher premiums due to traffic density), age 28 (past the under-24 surcharge), 10 years of license history
5. Run comparisons on Hova.co.il for mandatory, then Wobi and Shukabit for comprehensive
6. Build a comparison table showing top 5 quotes for each type
7. Recommend considering: new-for-old replacement policy (important for a new car), free garage choice, and glass coverage without deductible

Result: User receives a side-by-side comparison of the cheapest 5 mandatory insurance quotes and 5 comprehensive insurance quotes, with a clear recommendation based on coverage-to-price ratio.

### Example 2: Home Insurance for Mortgage Approval

User says: "The bank says I need home insurance for my mortgage approval. My apartment is 85 sqm in Haifa, built in 2010."

Actions:
1. Explain the two components: mivne (structure) for the bank, tochen (contents) for personal protection
2. Calculate approximate rebuild value based on size and construction type (typically 6,000-8,000 ILS per sqm for standard construction)
3. Note that the bank needs the policy assigned (meshuabed) to them as beneficiary
4. Compare quotes from Harel, Migdal, Clal, Phoenix, and Menora via Shukabit
5. Check if the mortgage bank has a preferred insurer (sometimes offers discounted rates)
6. Verify earthquake coverage is included (mandatory since 2013)
7. Recommend contents insurance amount based on typical household inventory

Result: User receives 4-5 home insurance quotes showing structure + contents premiums, with guidance on the minimum coverage the bank will accept and recommended additional coverage.

### Example 3: Comparing Health Supplementary Insurance for a Family

User says: "We're a family of 4 in Maccabi and thinking about upgrading to Maccabi Zahav. Is it worth it? My wife needs knee surgery."

Actions:
1. Identify current tier (likely Maccabi Sheli or no supplementary)
2. Look up Maccabi Zahav benefits: private hospital surgery coverage, specialist access, shorter wait times
3. Calculate monthly premium for the family (2 adults + 2 children, need ages for accurate pricing)
4. Compare the surgery coverage: Maccabi Sheli vs. Maccabi Zahav for orthopedic surgery
5. Check waiting period (tku'fat achshara) for surgery benefits - typically 6-12 months
6. Compare with private health insurance from commercial insurers (Harel, Migdal, Clal) as an alternative
7. Factor in the urgency: if surgery is needed soon, the waiting period may make the upgrade ineffective in the short term

Result: User receives a cost-benefit analysis comparing Maccabi Sheli vs. Zahav premiums against the expected surgery costs, plus alternative private insurance options if the waiting period is a problem.

## Bituach Siudi (Long-Term Care) Crisis 2025-2026

A major structural change broke the Israeli long-term-care market in 2025-2026 and any 2026 comparison must surface it:

- **Ministry of Health ordered the four kupot cholim to STOP selling new bituach siudi (long-term care) policies from July 1, 2025**, and to cease all bituach siudi operations by January 1, 2026. The kupot-channel policies that millions of Israelis held are no longer the recommended model.
- **The CMA tightened the patient-eligibility definition to 4-of-6 ADLs (activities of daily living)** effective January 1, 2025 (was 3-of-6). Patients who would have qualified under the old definition may not qualify now.
- **Remaining options for new long-term-care coverage:** private bituach siudi from major insurers (Phoenix, Migdal, Harel, Clal, Menorah), and Bituach Leumi's siudi track. Pricing and underwriting differ significantly across these. Verify current availability per insurer; the market is still adjusting.

When a user asks about "bituach siudi" in 2026, surface this disruption explicitly — quoting the pre-2025 kupot-channel framing as if still active is misleading.

## War / Iron Swords Coverage Considerations

- **Reservist (miluim) policies:** call-up under Order 8 may trigger automatic coverage adjustments on disability and life policies (some carriers waive premiums; others apply standard exclusions). Bituach Leumi's reservist track operates separately and pays for service-related disability or death.
- **Travel-insurance war exclusions:** since Iron Swords (Oct 2023), most travel insurers exclude active-war-zone destinations and may exclude flights routed through them. Verify the geographic exclusion clause before purchase.
- **Disability and life-insurance terror clauses:** check the policy's "war risk" and "terror" definitions; some payouts are reduced or excluded for organized hostilities, while pure terror events are usually still covered (verify per policy).

## Gotchas
- Israeli car insurance has three distinct mandatory/optional layers: Hova (mandatory third-party), Makif (comprehensive), and Tzad Gimel (third-party property). Agents may conflate these or use US/UK insurance terminology that does not map to Israeli categories.
- Insurance premiums in Israel are quoted per year, not per month. Agents may present monthly prices when the API returns annual figures, causing 12x confusion.
- The Bituach Hova (mandatory car insurance) pool is regulated by the government and prices are set by committee. Agents may suggest "shopping around" for this type, which has limited price variation.
- Israeli health insurance has a public layer (kupat cholim) and supplementary private layers (shaban, mashlim). Agents may compare only private plans without noting the universal public coverage.

## Troubleshooting

### Error: "The CMA calculator at car.cma.gov.il returns no results"

Cause: The CMA calculator requires exact vehicle registration details. Common issues include incorrect license plate format, vehicle not yet registered in the Ministry of Transport database (for very new cars), or the calculator being temporarily down during maintenance hours (usually late night).

Solution: Verify the license plate format (7 or 8 digits, no dashes). For newly purchased vehicles, wait 24-48 hours after registration before trying the calculator. If the site is down, try during business hours (Sunday-Thursday 8:00-17:00). As a fallback, use Hova.co.il which maintains its own insurer API connections.

### Error: "Insurance quotes vary wildly between platforms for the same details"

Cause: Different platforms may use slightly different underwriting models, have exclusive deals with certain insurers, or apply promotional discounts not available elsewhere. Some platforms also show base price before taxes/fees while others show the final price.

Solution: Always compare the final annual premium including all fees and taxes (VAT is included in insurance premiums in Israel). Check if the quote includes "rishuyon shimush" (usage fee) which some platforms list separately. Use the CMA government calculator as the baseline since it shows standardized pricing, then check if private platforms offer better deals. When in doubt, call the insurer directly to verify the quoted price.

### Error: "My shin-nun (no-claims) years don't match what the insurer shows"

Cause: The shin-nun record is maintained by the Pool (the Israeli insurance pool). Insurers query this database, but sometimes there are delays in updating, especially if you switched insurers recently or had a claim that was later withdrawn or settled as not-at-fault.

Solution: Request your official shin-nun record from your current or previous insurer. You can also contact the Pool directly. If there's an error, file a correction request through your insurer. Keep copies of all no-claim certificates from previous policies. The difference between shin-nun levels can be 10-20% on premiums, so it's worth correcting any errors.

### Error: "The comparison platform asks for my ID number but I'm uncomfortable sharing it"

Cause: Israeli insurance quotes require the policyholder's teudat zehut (ID number) for regulatory compliance and to query the shin-nun database and vehicle registry.

Solution: Government platforms (car.cma.gov.il) are secure and regulated. For private platforms, verify they are licensed insurance agents or brokers listed on the CMA website. You can start with platforms that provide preliminary estimates without ID (like Wobi's general calculator) and only enter your ID on the platform you choose to purchase from. Never share your ID number on unsecured websites or via email.
