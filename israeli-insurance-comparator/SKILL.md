---
name: israeli-insurance-comparator
description: Not insurance advice and not insurance marketing. Compare car insurance (mandatory hova, comprehensive makif, third-party), home insurance, and health supplementary insurance across 20+ Israeli insurers using official government calculators and private comparison platforms. Use when a user needs to find the cheapest insurance quote, understand policy differences, or prepare for annual renewal negotiations. Guides through CMA calculator at car.cma.gov.il, Hova.co.il, Shukabit, Wobi, and Bestie. Do NOT use for life insurance, pension fund selection, or travel insurance comparisons.
license: MIT
allowed-tools: Bash(python:*) WebFetch
---

# Israeli Insurance Comparator
## Legal notice

This is a free information tool operated by an AI model. It walks you through the CMA calculators and private comparison platforms and helps you lay side by side the quotes you obtain yourself. All of its output is produced automatically, with no involvement, review, or approval by a licensed insurance agent or pension adviser.

The output is not insurance advice, not insurance marketing, and not a personal recommendation to buy, switch, or cancel a policy. It is raw material for a comparison you carry out yourself, and it does not include underwriting, an assessment of your insurance needs, or a reading of the specific policy terms you will be offered. An AI model can err, omit data, or present a wrong conclusion, and prices and terms change without notice.

Some comparison platforms operate as licensed insurance agencies and earn commission on a sale, so they are not neutral. Do not rely on the output to cancel an existing policy, switch insurer, or drop coverage, and read the policy terms and exclusions in full with the insurer before signing. This tool is not a substitute for advice that takes account of the particular data and needs of each person, and any use of the output is the user's sole responsibility.


## Instructions

### Step 0: Inventory Existing Policies via Har HaBituach

Before comparing offers, the user should pull their existing policy inventory from **Har HaBituach** (`https://harb.cma.gov.il/`), the CMA-operated personal-policy aggregator. Har HaBituach lists every policy the user holds across all Israeli insurers (life, health, pension, disability, mortgage life, supplementary HMO, manager's insurance, etc.). Many users discover overlapping or expired coverage they had forgotten. Skipping this step is the most common reason a comparison ends up over-insuring or duplicating coverage.

Authentication is via the Israeli government national-identity system (Hizdahut Memshaltit), using your ID. The interface is Hebrew-only.

### Step 1: Identify the Insurance Type Needed

Determine which insurance product the user is comparing. Israeli insurance falls into these main categories:

**Car Insurance (3 types):**
- **Bituach Hova (ביטוח חובה)** - Mandatory by law under the Victims of Road Accidents Law (חוק הפיצויים). Covers bodily injury only. Every vehicle on the road must have this.
- **Bituach Makif (ביטוח מקיף)** - Comprehensive insurance covering theft, fire, damage to your car, and third-party property damage. Optional but very common.
- **Bituach Tzad Gimel (ביטוח צד ג׳)** - Third-party only. Covers damage you cause to others' property but not your own vehicle. Cheaper alternative to makif.

**Two-wheelers and other vehicle types:** hova is not private-car-only. The CMA calculator prices ofanoa (motorcycle/scooter), bus/tour vehicle, taxi, commercial and special vehicles as first-class categories. If the user rides a two-wheeler, select that vehicle type rather than running a private-car flow, and expect a materially higher tariff.

**HaPool (הפול - המאגר לביטוח שיורי), the residual market:** if no insurer will write the user's hova directly (heavy claims or violation record, licence suspensions, some two-wheeler and young-driver profiles), they are not uninsurable. HaPool is the statutory residual-market mechanism and appears first on the CMA calculator's list of carriers charging the identical regulated tariff. It exists precisely to cover drivers the market declines. This is the answer to "nobody will insure me", which the rest of a price comparison cannot address.

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

- **Every person who will actually drive the car**, with their age and licence seniority. This is not a pricing detail, it decides who is covered. An Israeli hova certificate is issued for a defined class of permitted drivers (for example any driver, or only drivers above a stated age or licence seniority, or named drivers), and makif policies carry their own additional-driver terms. Someone driving outside that class is not covered, which is both an offence and a personal exposure for the damage. Establish the real list of drivers here, and confirm against the certificate in Step 9 before anyone else takes the keys.

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
3. The tool returns the standardized hova price for your risk profile. Hova premiums are set by a regulated tariff (the price is committee-priced by driver/vehicle risk band), so this is NOT a competitive quote marketplace, the variation between insurers is only the small loading or discount each is permitted to apply on top of the tariff
4. Results show: insurer name, annual premium, monthly payment option, and coverage details
5. Note: this is the reliable baseline because the hova price is standardized by regulation, not because insurers compete on it. Two things the CMA states here that users miss: hova and makif need NOT come from the same agent or insurer, so shop them separately; and the tariffs shown are the currently approved ones, so an insurer quoting MORE than the site shows is reportable to CMA public enquiries. Fleets and large collectives may be offered different tariffs

**For comprehensive car insurance (makif):**
1. **govcarins.mof.gov.il is NOT a general public comparison tool.** Its own heading reads "simulator for comprehensive car insurance for state employees" (סימולטור ביטוח רכב מקיף לעובדי מדינה). It prices makif off the annual state procurement tender (mikhraz), with a tender-year selector, and its quoted price assumes 2 or more claims unless the user submits a claims-history form (tofes avar bituchi). It also explains how to derive the tender's hova rate.
2. So route by who the user is:
   - **A state employee (עובד מדינה)**: send them here first. The tender channel is often their cheapest makif route, and no private comparison platform will surface it.
   - **Everyone else**: skip it. The numbers shown are not purchasable by them. Makif is fully market-priced (wide variance driven by underwriting), so real makif numbers come only from the private platforms or a direct insurer quote.
3. Compare deductible amounts (hashtatfut atzmit) across insurers

### Step 4: Use Private Comparison Platforms

After getting the government baseline, check private platforms for potentially better deals. Tell the user how each platform is paid before they weigh its recommendation: some of these trade as licensed insurance agencies and earn commission on a sale, which is legitimate but is not neutrality. Where a platform's own site states its status, quote that; where it does not, say the arrangement is undisclosed rather than implying independence.

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
- Large Israeli insurance comparison site. Its ownership has been the subject of an acquisition process involving a major Israeli insurance group, so do not assume it is independent. Check its current ownership and licensing status before relying on it as a neutral comparison, and note that a comparison site owned by an insurer has an obvious conflict
- Covers car, home, health, life, and business insurance
- Offers phone consultation with licensed agents
- Can handle the entire purchase process

**Bestie (bestie.co.il):**
- Describes itself as the only Israeli comparison platform that is not an insurance company or agency. That is its own claim, useful context but not an audited fact
- Provides personalized recommendations based on a short questionnaire
- Covers car, home, travel, and mortgage insurance (not health supplementary)
- Good for understanding which coverage level you actually need

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
| Permitted drivers on the hova certificate, and additional-driver terms on the makif | | | |
| CMA Service Index rank (state year) | | | |

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
| CMA Service Index rank (state year) | | | |

Important notes:
- **Earthquake coverage**: a structure policy normally includes cover for earthquake damage unless the owner asked to waive it, provided directly by each insurer (there is no central "earthquake pool" for home insurance). Because it is waivable to lower the premium, verify it has not been waived. Three things to check on the deductible, which is where this coverage surprises people: it is a SEPARATE earthquake deductible, it is normally set as a percentage of the SUM INSURED rather than of the damage, and it can be substantially higher than an ordinary deductible. Ask whether a lower earthquake deductible can be bought for a higher premium, and note that earthquakes occurring within 72 hours of each other may be treated as a single insured event for deductible purposes.
- **Check the building's policy first**: many Israeli apartment owners already have structure cover through the vaad bayit / bait meshutaf policy. That policy is not personal, so it will NOT show up in Har HaBituach, and buying a full individual mivne policy on top of it is a common duplicate. Ask the vaad what the building policy covers and to what limit before pricing an individual structure policy.
- **Mortgage requirement**: If you have a mortgage, the bank typically requires structure insurance assigned (meshuabed) to the bank. Ask the insurer about bank assignment.
- **Underinsurance penalty**: If your coverage amount is less than the actual value, the insurer can apply a proportional reduction (klal yachasi) to any claim.

### Step 7: Compare Health Supplementary Insurance

Israeli health supplementary insurance (SHABAN) operates in tiers from each kupat cholim. Two facts shape the whole comparison:

- **SHABAN price is regulated and uniform, not shoppable.** SHABAN pricing is uniform for everyone in the same age band and the same plan within a kupa, so you cannot negotiate it. And you can only buy the SHABAN of YOUR kupat cholim, you cannot mix-and-match. So the real decision is (a) which kupa to belong to, (b) basic vs premium tier within it, and (c) whether to add a private commercial health policy on top. Switching SHABAN means first switching kupa (done free via Bituach Leumi; check the current permitted switching windows, they are set by regulation and change).
- **SHABAN has guaranteed acceptance, private insurance does not.** SHABAN has no medical underwriting and no pre-existing-condition exclusions at any tier, anyone can join regardless of health. A kupa may put a health declaration in the joining form, but signing it is optional (reshut bilvad), and the only condition on receiving a SHABAN service is its waiting period (tkufat achshara). Private commercial health policies (Harel, Migdal, Clal) DO underwrite and can decline, load, or exclude a known condition. This is decisive when someone already has a diagnosis (see Example 3): a private policy bought now would likely exclude that condition, while no SHABAN tier can.

Each kupa sells several SHABAN tiers (rvadim) that differ in scope of services and therefore in price. Always establish which tier the user is actually on before comparing, and check whether a cheaper tier meets their needs.

**Clalit (Clalit Mushlam Zahav / Mushlam Platinum):**
- Mushlam Zahav: Basic supplementary tier (SHABAN)
- Mushlam Platinum: Premium tier with shorter wait times and broader specialist access

**Maccabi (Maccabi Kesef / Maccabi Zahav / Maccabi Sheli) - THREE tiers, not two:**
- Maccabi Kesef (מכבי כסף): the entry SHABAN tier, and the cheapest Maccabi supplementary option
- Maccabi Zahav (מכבי זהב): the middle tier
- Maccabi Sheli (מכבי שלי): the top tier, with the broadest entitlements
- Maccabi lists them top-down as Sheli / Zahav / Kesef / the basic basket. Do not present Zahav as the entry tier, that hides Kesef. Two things are NOT settled here and must be checked with Maccabi for the specific user, because sources disagree: whether Sheli is priced as a standalone tier or as a layer whose price already includes Zahav, and whether Kesef is still open to new joiners or is a legacy tier closed to new members. Get both answers before quoting a price or recommending a downgrade.

**Meuhedet (Meuhedet Adif / Meuhedet Shia):**
- Adif: Basic supplementary
- Shia (שיא): Premium tier

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

### Step 8: Weigh Service Quality, Then Negotiate

Price and coverage are only two of the three axes. The CMA publishes an annual **Service Index (מדד השירות)** ranking insurers and managing companies, describing it as "an important tool in customers' hands when choosing the institutional body from which they will buy an insurance, pension or savings product", with the stated aim of increasing transparency and competition on service. Since the thing a user actually buys is the promise that a claim gets handled, check the index before committing to the cheapest quote, especially where two quotes are close. It is published per year at gov.il (most recent published edition at the time of writing covers 2024), so state which year's index you are quoting rather than presenting it as undated.

After gathering comparison data:

1. **Contact your current insurer** with competitor quotes. Retention departments often match or beat competitor pricing.
2. **Bundle policies**: Ask about discounts for holding multiple policies (car + home) with the same insurer.
3. **Timing**: Renew or switch 30-60 days before policy expiration. Last-minute renewals reduce negotiating power.
4. **Annual payment**: Paying annually instead of monthly is commonly cheaper than the monthly instalment total. Ask each insurer for both figures rather than assuming a fixed discount.
5. **Increase deductible**: If you can afford a higher out-of-pocket expense, raising the deductible can significantly reduce premiums.
6. **Review coverage annually**: Life changes (new car, moved to a safer area, kids left home) can affect premiums.

### Step 9: Read and Understand the Policy

Before finalizing any insurance purchase:

1. **Polisa (פוליסה)**: Read the full policy document, not just the summary
2. **Exclusions (חריגים)**: Identify what is NOT covered
3. **Waiting periods (תקופת אכשרה)**: Some coverages activate only after a waiting period
4. **Cancellation and refunds**: do not assume you are locked in. Ask about cancelling mid-term and what unearned premium comes back. This matters most when a car is sold or written off, where a refund on the remaining makif and hova is routinely left unclaimed
5. **Claims process**: Know how to file a claim (tvi'a) and required documentation. Establish the limitation period that applies to an insurance claim rather than assuming you have the general civil-claim period, it is shorter, and a late claim is refused however valid it was
6. **Complaint channel**: The CMA handles consumer complaints at pe.cma.gov.il, which also offers a quick-enquiry route that needs no registration, so the government-identity login is not a barrier here

## Examples

### Example 1: First-Time Car Insurance Buyer

User says: "I just bought a 2024 Hyundai i20 and I need car insurance. I live in Tel Aviv, I'm 28 years old, and got my license at 18."

Actions:
1. Clarify the user needs both bituach hova (mandatory) and likely bituach makif (comprehensive) for a new car
2. Guide them to car.cma.gov.il to get mandatory insurance quotes from all licensed insurers
3. Collect vehicle details: 2024 Hyundai i20, approximate engine size 1.2L
4. Note premium-affecting factors: Tel Aviv, driver age 28, and 10 years of licence history. Do not assert where the young-driver loading cuts off, the CMA calculator takes age and licence years as inputs and prices them, so read the loading off the quote rather than assuming a threshold
5. Run comparisons on Hova.co.il for mandatory, then Wobi and Shukabit for comprehensive
6. Build a comparison table showing top 5 quotes for each type
7. Flag the options worth pricing for a new car: new-for-old replacement, free garage choice, and glass coverage without a deductible

Result: the user gets a side-by-side comparison of the cheapest 5 mandatory and 5 comprehensive quotes, ranked on coverage-to-price ratio, to decide from themselves.

### Example 2: Home Insurance for Mortgage Approval

User says: "The bank says I need home insurance for my mortgage approval. My apartment is 85 sqm in Haifa, built in 2010."

Actions:
1. Explain the two components: mivne (structure) for the bank, tochen (contents) for personal protection
2. Establish the rebuild value (erech kinun). This is a valuation, not a rule of thumb: ask the insurer for its current rebuild-cost-per-sqm assumption, or commission a shamai. Do not settle on a per-sqm figure from memory, understating it triggers exactly the proportional reduction (klal yachasi) flagged below
3. Note that the bank needs the policy assigned (meshuabed) to them as beneficiary
4. Compare quotes from Harel, Migdal, Clal, Phoenix, and Menora via Shukabit
5. Check if the mortgage bank has a preferred insurer (sometimes offers discounted rates)
6. Verify earthquake coverage has not been waived (normally included in a structure policy unless the owner opted out, provided by the insurer, not a central pool), and ask what the separate earthquake deductible is as a percentage of the sum insured
7. Prompt the user to value their own contents, rather than assuming a typical household inventory

Result: the user gets 4-5 home quotes showing structure and contents premiums, plus the minimum cover the bank will accept and which optional cover to price.

### Example 3: Comparing Health Supplementary Insurance for a Family

User says: "We're a family of 4 in Maccabi and thinking about adding Maccabi Sheli on top of our Maccabi Zahav. Is it worth it? My wife needs knee surgery."

Actions:
1. Place them on the ladder: Maccabi runs three SHABAN tiers, Kesef (entry), Zahav (middle) and Sheli (top). The family is on Zahav, so Sheli is the tier above. Confirm with Maccabi whether the Sheli price quoted is standalone or already includes the Zahav base, the cost-benefit is wrong by the price of Zahav if you assume the wrong one
2. Look up Maccabi Sheli benefits: higher private-hospital surgery ceilings, free choice of surgeon, broader specialist access beyond what Zahav already covers
3. Calculate the monthly premium for the family at each tier (2 adults + 2 children, ages needed for accurate pricing). Also ask about Kesef, in case the family is paying for Zahav entitlements they do not use, and check whether Kesef still accepts new joiners
4. Compare the surgery coverage: Maccabi Zahav alone vs. Zahav + Sheli for orthopedic surgery
5. Check the waiting period (tkufat achshara) for the specific surgery benefit. Each kupa sets its own waiting period and it differs per service, so ask Maccabi for the number that applies to this benefit rather than assuming a general figure
6. Compare with private health insurance from commercial insurers (Harel, Migdal, Clal) as an alternative, and flag the underwriting asymmetry: moving up a SHABAN tier cannot be refused over the existing knee diagnosis, while a private policy bought now could exclude it
7. Factor in the urgency: if surgery is needed soon, the waiting period may make the upgrade ineffective in the short term

Result: User receives a cost-benefit analysis comparing Zahav-alone vs. Zahav + Sheli premiums against the expected surgery costs, plus alternative private insurance options if the waiting period is a problem.

## Bituach Siudi (Long-Term Care) Crisis 2025-2026

The kupot-channel long-term-care market is mid-transition and any 2026 comparison must surface it. Be careful with the dates: the July-2025 "stop selling" deadline was a Ministry of Health DRAFT that was never enforced, and the wind-down moved to a 2026-2027 timeline. Clalit's policy found an operator in August 2026 (Ayalon, from January 2027, for eight years). The CMA also tightened the eligibility definition in December 2024. Never state the July-2025 / January-2026 dates as accomplished facts. Full detail, including the eligibility test and the coverage options, is in `references/bituach-siudi.md`.

## War / Iron Swords Coverage Considerations

- **Reservist (miluim) policies:** call-up under Order 8 may trigger coverage adjustments on disability and life policies (some carriers waive premiums, others apply standard exclusions). Bituach Leumi's reservist track operates separately for service-related disability or death.
- **Travel-insurance war exclusions:** since Iron Swords (Oct 2023), most travel insurers exclude active-war-zone destinations and may exclude flights routed through them. Verify the geographic exclusion clause before purchase.
- **Disability and life terror clauses:** check the policy's "war risk" and "terror" definitions. Some payouts are reduced or excluded for organized hostilities (verify per policy).

## Gotchas
- Israeli car insurance has three distinct mandatory/optional layers: Hova (mandatory third-party), Makif (comprehensive), and Tzad Gimel (third-party property). Agents may conflate these or use US/UK insurance terminology that does not map to Israeli categories.
- Insurance premiums in Israel are quoted per year, not per month. Agents may present monthly prices when the API returns annual figures, causing 12x confusion.
- Bituach Hova (mandatory car insurance) is sold at a regulated tariff set by risk band, so it has very limited price variation. Agents may suggest "shopping around" for it as though it were market-priced. Do not confuse this regulated tariff with HaPool (המאגר לביטוח שיורי), which is a specific residual-market carrier for drivers the market declines, they are different things that both get called "the pool" in English.
- Israeli health insurance has a public layer (kupat cholim) and supplementary private layers (shaban, mashlim). Agents may compare only private plans without noting the universal public coverage.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| CMA hova tariff calculator | https://car.cma.gov.il/ | The regulated hova tariff, the vehicle types priced (incl. motorcycle), and the carrier list that HaPool heads |
| Har HaBituach (CMA) | https://harb.cma.gov.il/ | Existing policies and premiums, duplicate-cover alerts, and your motor-property insurance history |
| CMA Service Index | https://www.gov.il/he/pages/service_index_all | Which year's index is the latest published, and insurer service rankings |
| CMA public enquiries | https://pe.cma.gov.il/ | How to file a complaint against an insurer |
| MoF state-employee makif simulator | https://govcarins.mof.gov.il/ | Tender-year makif pricing, state employees only |
| INFOCAR (insurers' clearing centre) | https://infocar.co.il/ | A specific vehicle's claims history, and the current fee |
| Kol Zchut, supplementary health (SHABAN) | https://www.kolzchut.org.il/he/%D7%A9%D7%99%D7%A8%D7%95%D7%AA%D7%99_%D7%91%D7%A8%D7%99%D7%90%D7%95%D7%AA_%D7%A0%D7%95%D7%A1%D7%A4%D7%99%D7%9D_(%D7%91%D7%99%D7%98%D7%95%D7%97_%D7%9E%D7%A9%D7%9C%D7%99%D7%9D) | Current tier names per kupa, waiting periods, and switching rules |

## Troubleshooting

### Error: "The CMA calculator at car.cma.gov.il returns no results"

Cause: The calculator is a risk-parameter form, NOT a registration lookup. It has no licence-plate field and does not query the vehicle registry. It returns a tariff only once every parameter on the page is filled in, and the usual cause of an empty result is a blank or out-of-range field, most often among the vehicle-characteristics group (fuel type, engine capacity in cc, horsepower, ABS, ESP, airbag count, FCW, LDW) that users skim past.

Solution: Fill in every field, including all the safety-system fields, then resubmit. Each field has a "?" icon with the CMA's own explanation. Vehicle-characteristic values can be looked up via the Ministry of Transport link on the page. For a commercial vehicle up to 3.5t select vehicle type "private car", because the tariff is identical; that is a documented quirk, not an error. Do not tell the user to check a plate format or wait for registration to propagate, neither applies here.

### Error: "Insurance quotes vary wildly between platforms for the same details"

Cause: Platforms use different underwriting models, hold exclusive deals with certain insurers, or apply promotional discounts. Some show a base price before fees while others show the final price.

Solution: Always compare the final annual premium including all fees. Note that insurance premiums in Israel are NOT subject to VAT: under the VAT law an insurer is a financial institution (mosad kaspi), and financial institutions pay payroll-and-profit tax (mas sachar ve'revach) on wages and profit instead of charging VAT on their services. So the quoted premium is the final price and any differences between platforms come from fees and discounts, not tax. Do not confuse the insurance premium with the separate annual vehicle-licensing fee (agrat rishuy rechev / "rishayon"), which is a government charge paid separately to the licensing authority and is NOT part of any insurance quote. Use the CMA calculator as the baseline, then check whether private platforms beat it. When in doubt, call the insurer to verify the quote.

### Error: "My shin-nun (no-claims) years don't match what the insurer shows"

Cause: There is no single "shin-nun registry", and HaPool is NOT it (it is the residual-market insurer, not a claims database). The record is reconstructed from your insurance history, so mismatches usually follow a recent insurer switch, or a claim that was withdrawn or settled as not-at-fault still sitting in the history.

Solution: Three routes, cheapest first.
1. **Har HaBituach (harb.cma.gov.il), free.** The CMA site explicitly presents your motor-property insurance history (avar bituchi) and will send the avar bituchi form directly and securely to a prospective insurer, which also speeds up joining. This is the route to try first, and the skill's Step 0 already has the user logged in.
2. **Your current or previous insurer**, which issues an official no-claims certificate (tofes he'eder tvi'ot).
3. **INFOCAR (infocar.co.il)**, run by the insurers' clearing centre (Merkaz HaSlika), for a small fee stated on the site. Note the scope difference: INFOCAR reports the claims history of a specific VEHICLE, including whether it was insured at all and by whom, which is why it is also used when buying or selling a car. It is not a per-driver no-claims record.

If there is an error, file a correction request through your insurer and keep copies of prior no-claim certificates. The difference between shin-nun levels is material enough to be worth correcting, so ask the insurer to requote once the record is fixed.

### Error: "The comparison platform asks for my ID number but I'm uncomfortable sharing it"

Cause: Israeli insurance quotes require the policyholder's teudat zehut (ID number) for regulatory compliance and to query the shin-nun database and vehicle registry.

Solution: Government platforms are secure and regulated. For private platforms, verify they are licensed agents or brokers listed on the CMA website. Start with platforms giving preliminary estimates without an ID, and enter it only on the one you choose to buy from. Never share an ID number on an unsecured site or by email.
