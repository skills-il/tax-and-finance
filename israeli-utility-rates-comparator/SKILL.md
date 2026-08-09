---
name: israeli-utility-rates-comparator
description: Compare electricity providers, water tariffs, cooking-gas (LPG) rates, cellular plans, fiber internet packages, and arnona (municipal property tax) across Israeli municipalities and utility companies. Use when a user needs to understand IEC tariff structures, calculate solar panel ROI, compare tiered water pricing, pick a cheap cellular plan, switch to fiber internet, or evaluate arnona differences between cities. Covers electricity market deregulation, independent power producers, Mekorot water pricing, cellular operators and MVNOs, fiber-optic infrastructure, and municipal rate variations. Do NOT use for commercial/industrial utility contracts at scale, or utility infrastructure investment analysis.
license: MIT
allowed-tools: Bash(python:*) WebFetch
---

# Israeli Utility & Telecom Rates Comparator

## Instructions

### Step 1: Identify Which Utility to Compare

Determine which utility cost the user wants to analyze. Israeli household utilities and recurring service costs include:

**Electricity (חשמל):**
- Israel Electric Corporation (IEC / חברת החשמל) owns transmission, distribution, and meter reading
- The household supply market is open: as of 2026 roughly 360,000 customers have moved to private suppliers and the count keeps climbing
- Tariffs are set by the Electricity Authority (רשות החשמל)
- Time-of-use (TOU) pricing available for smart-meter customers (about 1M meters / ~30% of households as of 2026)

**Water (מים):**
- Mekorot (מקורות) is the national water company supplying bulk water
- Municipal water corporations (taagidei mayim) handle local distribution
- Tiered pricing: ascending block tariff system where price per cubic meter increases with consumption

**Cooking Gas (גז בישול / גפ"מ) and Natural Gas (גז טבעי):**
- Most households still use LPG cooking-gas balloons (12kg) or centralized building tanks
- Natural gas infrastructure expanding via Energean (Karish/Athena) pipelines, mostly in newer buildings
- LPG tariffs published by the Energy Ministry per locality

**Cellular and Internet (סלולר ואינטרנט):**
- Cellular market opened to MVNOs in 2012 (Hot Mobile, Golan Telecom, Rami Levy Mobile, 019, Home Cellular and others); unlimited plans dropped to single-digit-to-low-double-digit shekels
- Internet has split into infrastructure (Bezeq, HOT, IBC/Unlimited fiber, partner-built fiber) and content/ISP (Bezeq Beinleumi, Cellcom, Partner, 013, 014/Cellact, Triple-C, Hot-Net), most consumers buy as a single bill ("שוק סיטונאי") today

**Arnona (ארנונה):**
- Municipal property tax charged by local authorities
- Rates vary dramatically between municipalities
- Based on property size (sqm), zone, and usage type (residential/commercial)

### Step 2: Electricity Comparison

**Understanding IEC tariff structure:**

The Electricity Authority publishes official tariffs at pua.gov.il. IEC tariffs for residential customers include:

**Standard tariff (tariff achid):**
- Single rate per kWh for all hours
- Simplest billing structure
- Suitable for low-medium consumption households

**Time-of-use tariff (tariff TOZ / תעריף תעו"ז):**
- Requires a smart meter (moné chokhéakh)
- Two tiers since April 2023: peak (shia) and off-peak (shefel). The shoulder (geva) tier was eliminated; older docs may still show 3 tiers.
- THREE seasons, each with its own peak and off-peak rate. Off-peak is not a single national number.

| Season | Peak band | Peak (agorot/kWh, incl. VAT) | Off-peak |
|---|---|---|---|
| Summer (Jun-Sep) | 17:00-23:00 | 172.23 (145.96 excl. VAT) | 50.42 |
| Winter (Dec-Feb) | 17:00-22:00 | 114.70 | 46.63 |
| Transition (Mar-May, Oct-Nov) | see note | 49.58 | 45.78 |

- In force from 1.7.2026. The winter peak band applies on weekdays, Fri/eves AND Shabbat/holidays; there is no morning peak band.
- Do not quote transition-season band hours: the IEC page states them in a garbled form. It rarely matters, the spread there is under 4 agorot.
- Savings are seasonal: shifting load off-peak is worth over 120 agorot/kWh in summer and under 4 in transition. Never quote a flat "15-25% saving"; compute it from the user's own seasonal pattern.
- Tariffs update semi-annually via Electricity Authority decisions and can shift mid-year; verify before quoting.

**Monthly fixed charges:**
- Connection fee (agrat chibbur) regardless of consumption
- Distribution fee
- Public broadcasting fee (agrat shidrur)
- For apartments: a share of common-area electricity (chashmal klali) for stairwells, elevators, and lobby lighting, billed via the va'ad bayit (building committee) and separate from the IEC bill. New tenants are often surprised by this line item.

To compare electricity costs:
1. Obtain the user's recent electricity bills (at least 3 months, preferably 12 for seasonal patterns)
2. Note current monthly consumption in kWh
3. Check if they have a smart meter (required for TOU pricing)
4. If no smart meter, check eligibility and installation process with IEC (iec.co.il)

**Independent electricity producers (residential market):**

The residential electricity market is open to private suppliers. As of 2026, approximately 360,000 customers had switched to alternate suppliers (up from ~280,000 at end-2025), with typical discounts of 5-21% off the IEC tariff for the generation portion. Active residential suppliers in 2026 include:
- **Cellcom Energy**, **Partner**, **Bezeq**, **HOT Energy** (telecom-bundled offers)
- **Pazgas Electricity**, **Amisragas**, **Electra Power** (energy and gas group offers)
- **OPC Energy**, **Dalia Energy**, **Enlight Renewable Energy** (independent generators, historically large-customer focused, also signing residential customers)

**Critical: switching does NOT replace the full bill.** Independent suppliers compete only on the **generation** (ייצור) component, which is roughly 60-70% of the bill. The household continues to pay IEC for distribution (חלוקה), transmission (הולכה), the public broadcasting fee, and meter charges. The supplier discount applies only to the energy portion.

**Cooling-off period:** Under the Consumer Protection Law (חוק הגנת הצרכן), residential customers have a 14-day right to cancel after signing with an alternate supplier. Always read the cancellation clauses before signing, and keep a copy of the contract. The Energy Ministry is also working to shorten the supplier-switching window from 14 days to 7 days during 2026.

**Discounts on the electricity bill (separate from supplier choice):**
- **Seniors with income supplement (השלמת הכנסה):** 50% discount on consumption up to 400 kWh/month (or 800 kWh per bi-monthly bill). The Energy Minister is advancing a plan to deepen this to 65% for old-age + income-supplement, old-age-disability, and Holocaust survivors, verify status at gov.il before quoting 65% as fact.
- **Holocaust survivors (ניצולי שואה):** 50% discount on up to 400 kWh/month
- **Disabled (נכים) with high disability percentage:** discount tiers per Bituach Leumi recognition
- The discount is applied automatically once Bituach Leumi shares eligibility with IEC; nothing to file each month, but verify the discount line appears on your bill.

**Debt and disconnection protections (say this to any user whose bill is unaffordable):** request a הסדר תשלומים (payment arrangement) for arrears; disconnection for non-payment is regulated (advance notice, a minimum-debt threshold, and no disconnection while a billing dispute is open); a household dependent on electrically-powered life-support / medical equipment can register as a צרכן מוגן (protected consumer) and cannot be disconnected. See `references/details-2026.md`.

### Step 3: Calculate Solar Panel ROI

Solar panels (panelim sola'riyyim) are popular in Israel due to high solar irradiance.

**Gate this FIRST, before any ROI math:** only someone who controls the roof / connection point can install. An apartment resident needs רכוש-משותף consent (building owners' agreement / roof-rights allocation under חוק המקרקעין); a renter generally cannot install at all. For apartments, a shared-roof / roof-lease arrangement is the alternative. Do not hand an apartment renter a payback figure for something they legally cannot do alone.

**Net metering program:**
- Install solar panels on your roof or property
- Excess electricity is fed back to the IEC grid
- Credit accrues via net-metering (מונה נטו) on a bidirectional meter (מונה דו-כיווני), by kWh netting, not a meter spinning backward
- You pay only for net consumption (consumption minus production)
- System size limited to your annual consumption level

**ROI calculation factors:**
1. **System cost**: in 2026, typically 3,500-5,500 ILS per kWp turnkey installed (small systems cost more per kWp). Common residential sizes: 3 kW ~11,000-13,000 ILS; 5 kW ~18,000-22,000 ILS; 10 kW ~38,000-48,000 ILS basic, up to ~75,000 ILS for premium panels or battery-paired systems.
2. **Annual production**: Israel averages 1,500-1,800 kWh per installed kWp (Negev gets ~1,800, north gets ~1,400-1,500, central ~1,600)
3. **Current electricity cost**: multiply production by the current IEC tariff (from 1.7.2026, standard residential ~0.6352 ILS/kWh inc. 18% VAT, 53.83 agorot before VAT)
4. **Annual savings**: production in kWh multiplied by tariff rate (savings on offset consumption) plus the export tariff (~48 agorot/kWh residential, plus a +6 agorot urban premium for cities >50k) for excess fed to the grid. The old energy-vs-energy net-metering is closed to new entrants; self-consumption saves the most. See `references/details-2026.md` for the full two-track regime (≤15 kW residential track).
5. **Payback period**: system cost divided by annual savings (typically 4-7 years in Israel, faster in the south)
6. **System lifetime**: 25+ years with gradual degradation (~0.5% per year)
7. **Maintenance**: minimal, panel cleaning 1-2 times per year
8. **Connection approval**: apply to IEC for the export connection; confirm which track (≤15 kW residential vs larger) the installer is quoting, and that the applicant holds rights to the roof/connection point.

**Steps to evaluate solar:**
1. Check roof orientation (south-facing is optimal in Israel)
2. Assess shading from nearby buildings or structures
3. Contact 3+ solar installers for quotes (comparison sites: Solar Edge, SolarTech Israel)
4. Verify municipal approval requirements (heter bniya for roof modifications)
5. Apply to IEC for net metering connection
6. Calculate ROI using the factors above

### Step 4: Water Tariff Comparison

Israeli residential water uses an ascending block tariff (tiered pricing):

**Tier 1 (consumption up to basic allocation):**
- Lower rate per cubic meter (m3)
- Basic allocation: approximately 3.5 m3 per person per month (varies by household size)
- Calculated based on registered residents at the address (nefashot)

**Tier 2 (consumption above basic allocation):**
- Higher rate per cubic meter
- Approximately 84% more expensive than Tier 1 (Jan 2026: Tier 1 ~8.508 ILS/m³ inc. VAT vs Tier 2 ~15.623 ILS/m³ inc. VAT, both include sewage)
- Applies to all consumption beyond the basic allocation

**Important factors:**
- **Nefashot registration**: register all household members at your water corporation to maximize Tier 1 allocation. Unregistered members mean a lower threshold before Tier 2 kicks in. Registration is forward-looking; back-credit is generally limited to the current billing period.
- **Garden/pool allocation**: additional allocation available for documented garden irrigation or swimming pool
- **Sewage charge (biuv)**: in most municipalities sewage is bundled into the regulated per-m³ water tariff (the 8.508 / 15.623 ILS/m³ figures already include sewer). Where the local authority bills sewer separately, the standalone sewer rate is ~4.39 ILS/m³ on a volume basis (typically 70-90% of metered water).
- **Confirmed-leak credit**: water corporations grant a partial credit (often 50-100%) for documented hidden leaks under תקנות תאגידי מים וביוב. Requires a plumber certificate filed within 60 days of detection.

**Municipal water corporations (examples):**
- **Mei Avivim** (Tel Aviv)
- **Hagihon** (Jerusalem)
- **Mei Haifa** (Haifa)
- **Mei Raanana** (Raanana)
- **Mekorot** directly (some smaller localities)

Each corporation may add slightly different surcharges for infrastructure and maintenance. Compare by checking:
1. Base water rate per m3 (Tier 1 and Tier 2)
2. Sewage rate (bundled into the per-m³ tariff in most municipalities)
3. Infrastructure development levy (where applicable). Note: residential water is purely volumetric, there is no fixed household water service charge to compare.

To compare costs:
1. Obtain recent water bills (hagbanah)
2. Note household size (nefashot registered)
3. Calculate average monthly consumption in cubic meters
4. Check which tier most consumption falls into
5. Compare total cost including all surcharges

### Step 5: Natural Gas and Cooking Gas Comparison

**Cooking gas balloons (balonei gaz):**
- Standard 12 kg balloon
- Prices regulated by the Ministry of Energy (misrad ha'energia)
- Maximum price published monthly at gov.il
- Delivery fee varies by supplier
- Israeli LPG suppliers: Supergas, Pazgas, Amisragas, Dorgas
- Typical household uses 1 balloon every 1-3 months

**Natural gas (gaz tiv'i) home connection:**
- Available in newer residential buildings connected to the national gas grid
- Significantly cheaper per unit of energy than cooking gas balloons
- Monthly fixed connection fee plus usage-based charges
- Supply operator: Energean Israel (Karish/Tanin field), a separate company from NewMed Energy (formerly Delek Drilling, Tamar/Leviathan); local distribution companies handle last-mile delivery

**Central gas (גז מרכזי / צובר), a large apartment segment, has a real lever:** households on a shared bulk tank served by one LPG supplier have the RIGHT to switch central-gas supplier and to demand the supplier's published price list (LPG reform under חוק הפיקוח על מצרכים ושירותים). For these households, switching or renegotiating the central-gas supplier is the main way to lower cooking-gas cost, not just accepting the balloon price. See `references/details-2026.md`.

**Comparison factors:**
| Factor | Gas Balloon | Natural Gas |
|--------|-------------|-------------|
| Cost per cooking hour | Higher | Lower (40-60% savings) |
| Monthly fixed fee | None | Yes (connection charge) |
| Delivery reliability | Depends on supplier | Continuous supply |
| Safety | Requires periodic inspection | Built-in safety systems |
| Environmental impact | Higher emissions | Lower emissions |
| Availability | Everywhere | Limited areas |

To determine if switching to natural gas is worthwhile:
1. Check if your building has natural gas infrastructure (common in buildings built after 2010)
2. Calculate current cooking gas annual cost
3. Get a natural gas connection quote (installation + monthly fees)
4. Calculate break-even point (typically 2-4 years if infrastructure exists)

### Step 6: Cellular and Internet Comparison

The Israeli telecom market is one of the cheapest in the developed world after a decade of post-2012 MVNO entry and a fiber-optic rollout that finished covering most of the country between 2022 and 2025. Most households can save 50-200 ILS/month by switching providers, but the comparison has to look at the **total** bill (line + roaming + add-ons) and at lock-in / introductory pricing carefully.

**Provider tables and price ranges** (cellular MNO/MVNO plans, fiber infrastructure operators, speed tiers) are in `references/details-2026.md`. Key points for the body:
- Cheapest cellular clusters ~30 NIS/month for unlimited domestic calls + 50GB+ data, no setup fee, no commitment ("ללא התחייבות"). Number portability is free and takes ~1 business day, sign with the NEW provider first (never cancel first, that creates a gap). eSIM is widely supported.
- Home internet splits into infrastructure (Bezeq BFiber, HOT, IBC/Unlimited, Cellcom/Partner fiber) and ISP; a single wholesale-market bundle usually beats a legacy split bill by 20-40 NIS/month. Fiber covers >90% of households; ADSL is being retired.
- Introductory prices commonly jump 50-100% after 12 months, set a reminder and re-shop. Triple-play (cellular+internet+TV) discounts vanish if you cancel one leg.

**How to comparison-shop:**
1. **Pull last 3 months of bills** for cellular, internet, TV to see actual usage (data per line, peak speed observed, TV channels you watch)
2. **Run an Israeli comparator**: kamaze.co.il, kamazeole.co.il, israeliphoneplans.com, mishtalemli.co.il, or the Ministry of Communications official comparator at gov.il
3. **Get 2-3 quotes** by phone; tell each company you're shopping and ask for "מחיר שמירת לקוח" (retention price), usually 15-30% lower than the published price
4. **Time the switch**: cellular portability is free; internet may have a 1-2 week overlap so schedule installation before cancellation
5. **For new immigrants or those without Hebrew**: israeliphoneplans.com and No Fryers blog publish English-language guides that explain plan structure and oleh-specific tips

### Step 7: Arnona Comparison Between Cities

Arnona is the largest recurring utility-like cost for Israeli households, and rates vary sharply between municipalities.

**How arnona is calculated:**
- Rate per square meter per YEAR (shekel l'meter ravu'a l'shana). Arnona tariffs are published annually per m2; divide by 6 for a bi-monthly bill or 12 for a monthly one. Treating the annual rate as monthly overstates the bill twelvefold.
- Different rates for different zones within the same municipality
- Different rates for residential vs. commercial properties
- Discounts available for eligible populations (olim chadashim, elderly, low income, disabled)

A city-by-city arnona rate table (80 / 100 sqm monthly estimates for Tel Aviv, Jerusalem, Haifa, Beer Sheva, Raanana, Netanya, Rishon LeZion, Petah Tikva) is in `references/details-2026.md`. Rates vary by zone and change annually, verify at the municipality.

**How to check your arnona rate:**
1. Visit your municipality's website (iriya / moatza mekomit)
2. Look for "arnona" section or "tashlumim" (payments)
3. Find the tariff table (tav tariffim) for your zone
4. Calculate based on your property size and classification

**Arnona discounts (hanashot):** olim, seniors, low income, disability, IDF/national-service and bereaved families, students, single-person households, empty property and uninhabitable property each carry a discount with its own eligibility test and time limit. Full list in `references/details-2026.md`. Never quote a percentage without checking the municipality: national regulations set ceilings that municipalities apply differently.

**Discount stacking rule:** Only one discount tier applies per property at a time, per תקנות הסדרים במשק המדינה (הנחה מארנונה), תשנ"ג-1993. A household qualifying for both senior and low-income discounts receives the larger of the two, not the sum. Apply for whichever gives the highest reduction.

**Filing an arnona objection (hassagah):** if the bill is wrong (property size, zone classification, a missing discount, a balcony charged at full rate), file a written hassagah with the municipal arnona manager within 90 days of the bill. The municipality must answer within 60 days, and silence counts as rejection. If rejected you have 30 days to appeal to the ועדת ערר לארנונה, and 45 days from its ruling to escalate to בית משפט לעניינים מנהליים. Step-by-step guidance and what evidence to attach at each stage are in `references/details-2026.md`.

For IEC and water-corporation billing disputes (not arnona), the small-claims court (בית משפט לתביעות קטנות, 39,900 ILS cap in 2026) is often a faster path.

### Step 8: Tips for Reducing Utility Bills

Per-utility bill-reduction tips (electricity, water, arnona, cellular & internet) are in `references/details-2026.md`. Highest-leverage actions: shift electricity to off-peak on a TOU tariff, register all nefashot for the water Tier-1 allocation and fix leaks fast, apply for every arnona discount and verify recorded property size, and compare cellular/internet against MVNOs / wholesale bundles while asking for a "מחיר שמירת לקוח" retention price.

### Step 9: Smart Meter Adoption and Monitoring

**Smart meters (monéi chokhéakh):**
- IEC has installed approximately 1 million smart meters as of 2026 (~30% of households); the announced target is **3.7 million smart meters by end-2028**, prioritizing high-consumption households and dense urban areas
- Allow real-time consumption monitoring
- Enable TOU pricing and accurate readings for private suppliers (the supplier needs interval data, not a monthly estimate)
- Check eligibility at iec.co.il, call **103** (also reachable as 055-7000103 for SMS / WhatsApp), or use the IEC app
- Self-paid expedited installation (~260 ILS) is available where IEC has not yet deployed in the area, with typical wait of 2-12 weeks

**Monitoring tools:**
- IEC app (available on iOS and Android): view real-time consumption, billing history, and payment options
- Home energy monitors: third-party devices that clip onto your electrical panel
- Solar system monitors: SolarEdge, Enphase apps for solar panel owners

**Benefits of smart meters:**
- See exactly when you consume the most electricity
- Identify energy-wasting appliances
- Optimize consumption patterns for TOU savings
- Receive alerts for unusual consumption (potential leaks or faulty appliances)

## Examples

### Example 1: Family Evaluating Solar Panels

User says: "We live in a house in Modi'in, pay about 800 ILS per month for electricity, and want to know if solar panels are worth it."

Actions:
1. Calculate approximate monthly consumption: 800 ILS / ~0.6352 ILS per kWh (standard residential tariff from 1.7.2026, inc. 18% VAT) = ~1,259 kWh per month
2. Determine system size needed: 1,259 * 12 / 1,600 (kWh per kWp in central Israel) = ~9.4 kWp; round to a 9-10 kWp system
3. Estimate system cost: 9.5 kWp * ~3,800 ILS per kWp = ~36,000 ILS turnkey (mid-range 2026 pricing; basic systems start lower, premium and battery-paired go higher)
4. Estimate annual savings: full net-metering is closed to new entrants. Self-consumption offsets the ~0.6352 ILS/kWh retail rate; export earns ~0.54 ILS/kWh (48 + 6 urban). On a ~15,000 kWh/year system at ~45% self-consumption: ~8,500-9,000 ILS/year
5. Payback period: ~36,000 / ~8,750 = ~4.1 years (within the 4-7 year band)
6. 25-year total savings: roughly (8,750 * 25) - 36,000 = ~183,000 ILS (before ~0.5%/year degradation and tariff changes)
7. Check roof suitability: verify south-facing roof availability and shading.
8. Get 3 installer quotes. The residential export tariff (~48 agorot/kWh, +6 urban) sits well below the ~63.5 agorot retail rate, so self-consumption beats export. Confirm the applicant controls the roof.
9. Check municipal heter bniya requirements for roof modifications.

Result: ~4-5 year payback and lifetime savings over 150,000 ILS, modeling self-consumption and export separately. Strong provided the user controls the roof.

### Example 2: Comparing Utility Costs Between Cities for Relocation

User says: "I'm deciding between moving to Beer Sheva or Haifa. What's the difference in utility costs for a 100 sqm apartment, family of 4?"

Actions:
1. Compare arnona rates: Beer Sheva ~350-480 ILS/month for 100 sqm residential, Haifa ~480-630, a difference of ~130-150 ILS/month favouring Beer Sheva. Read each city's published annual rate per m2 and divide, rather than reusing these bands.
2. Compare water costs:
   - Both use tiered national pricing; check each water corporation's surcharges. Family of 4: ~14 m3/month Tier 1.
3. Compare electricity:
   - IEC rates are national. Beer Sheva has higher summer cooling costs but better solar potential; Haifa is milder.
4. Compare gas: similar pricing nationally, both cities have balloon gas and some natural gas
5. Calculate total annual utility difference:
   - Arnona savings in Beer Sheva: ~1,560-1,800 ILS/year
   - Electricity may be slightly higher in Beer Sheva due to cooling
   - Net annual savings in Beer Sheva: ~1,000-1,500 ILS/year on utilities
6. Note: Beer Sheva has significantly lower housing costs which compounds the savings

Result: User receives a side-by-side comparison showing that Beer Sheva is approximately 1,000-1,500 ILS per year cheaper on utilities (mainly arnona), plus significantly cheaper housing, while Haifa offers more moderate climate with lower cooling costs.

### Example 3: Optimizing Electricity Bill with Smart Meter

User says: "I just got a smart meter installed. My bill is 600 ILS/month. How can I reduce it?"

Actions:
1. Recommend switching from standard tariff to TOU (time-of-use) tariff
2. Analyze typical household consumption patterns:
   - Identify high-consumption appliances: AC, water heater (if electric), dryer, oven
   - Estimate what percentage of consumption can shift to off-peak hours
3. Create an optimization plan:
   - Run washer and dryer after 23:00 in summer, after 22:00 in winter. Shabbat is NOT automatically off-peak: the winter 17:00-22:00 peak band applies on Shabbat and holidays too.
   - Use dishwasher timer for off-peak operation
   - Pre-cool home before peak hours in summer
   - Switch electric water heater timer to heat during off-peak (if applicable)
4. Calculate potential savings:
   - If 40% of consumption shifts from peak to off-peak: savings of approximately 15-20%
   - 600 * 0.17 = ~100 ILS/month potential savings
5. Recommend IEC app for monitoring real-time consumption
6. Suggest additional measures: LED bulbs, AC at 24-25 degrees, unplug standby devices

Result: User receives a practical action plan for shifting consumption to off-peak hours, with estimated monthly savings of 80-120 ILS, plus an ongoing monitoring strategy using the IEC app.

## Gotchas
- Israel Electric Corporation rates are updated by the Electricity Authority on a semi-annual cycle, and a mid-year update can move the rate: the 1.7.2026 update cut the tariff by about 0.57% after the +1.5% January change. Agents routinely quote a superseded rate. Always verify the current tariff before quoting per-kWh numbers.
- The TOU (tariff TOZ / תעו"ז) schedule has only two tiers since April 2023: peak (שיא) and off-peak (שפל). The former שלב הגבע (shoulder) tier was eliminated. Agents trained on older docs may still describe a 3-tier structure with a middle band.
- Switching to an alternate electricity supplier (Cellcom Energy, Pazgas, OPC, etc.) only discounts the generation component, which is roughly 60-70% of the bill. The household still pays IEC for distribution, transmission, the public broadcasting fee, and meter charges. Agents may incorrectly imply the entire bill changes.
- Water Tier 1 covers up to 3.5 m³ per registered nefesh per month at the lower rate; consumption above goes to Tier 2 (~84% higher in Jan 2026: 8.508 vs 15.623 ILS/m³ inc. VAT). Sewage is bundled into the regulated per-m³ tariff in most municipalities, NOT a separate percentage surcharge as some older guides describe.
- Israeli utility bills include 18% VAT (raised from 17% on 1 Jan 2025; the 2026 increase to 19% was rejected by the cabinet in Dec 2025). Be explicit about whether quoted prices include or exclude VAT, especially when comparing alternate-supplier offers, since some advertise the pre-VAT generation rate.
- The Olim Hadashim arnona discount is 90% on up to 100 sqm for 12 months out of the 24 months following aliyah registration, NOT yearly. Agents may incorrectly describe it as multi-year (e.g., "90% first year, 10% years 2-5"). Disabled olim recognized by Bituach Leumi get up to 80% indefinitely under a separate provision.
- The IEC customer-service number is **103**; calls from a Bezeq or HOT landline are free. Do not emit older short codes from memory, they may point at a dead number.
- **Solar export tariff.** Energy-vs-energy net-metering is closed to new entrants. The residential rooftop export tariff is ~48 agorot/kWh plus a +6 agorot urban premium (cities >50k) for 15 years; the small-installation track is <=15 kW. Export pays less than the ~63.5 agorot retail rate, so self-consumption is worth more than export. Quote the contract's actual hesder line, not older ~0.21/~0.60/~0.38 figures.
- **Cellular and internet "promo expiry".** Most plans advertise a low introductory price (often X NIS for 12 months) that doubles or more after the promo period. Agents that quote the intro price as the "real" monthly cost will mislead the user. Always check the תקנון for "מחיר לאחר תום תקופת המבצע".
- **Number portability is free, fast, and no-paperwork.** Suggesting users "cancel first then sign up new" is wrong, they should sign with the new provider, who handles portability in ~1 business day. Cancelling first creates a service gap.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| 2026 tariff book (official PDF) | https://www.gov.il/BlobFolder/generalpage/tarriffbook/he/Files_netunei_hasmal_sefer_tariff_01_2026.pdf | Full tariff tables, all categories. This is the 01/2026 edition; check for a newer one before quoting |
| Israel Electric Corporation | https://www.iec.co.il | Residential tariff plans, smart meter rollout, consumption monitoring |
| IEC TOU low-voltage tariffs | https://www.iec.co.il/content/tariffs/contentpages/taozb-namuch | Per-season peak/off-peak rates and band hours, with the effective date |
| Electricity Authority | https://www.gov.il/he/departments/the_electricity_authority | Regulator decisions and tariff-update announcements (pua.gov.il redirects here) |
| Water Authority | https://www.gov.il/he/departments/water_authority | Tiered water rates, household allocation, municipal corporations |
| Water tariff book (Jan 2026) | https://www.gov.il/he/pages/rates_general1 | Full water + sewage tariff tables and updates |
| Natural Gas Authority | https://www.gov.il/he/departments/natural_gas_authority | Consumer gas pricing, supplier list, connection rules |
| LPG cooking gas comparator (Energy Ministry) | https://migdal-webpages.energy-apps.org/gpmCalculator | Compare LPG cooking-gas tariffs by locality and supplier |
| Ministry of Communications | https://www.gov.il/he/departments/ministry_of_communications | Cellular and internet regulation, complaints, supplier list |
| Kolzchut, senior electricity discount | https://www.kolzchut.org.il/he/הנחה_בחשבון_חשמל_למקבלי_קצבת_זיקנה_עם_השלמת_הכנסה | 50% (proposed 65%) discount up to 400 kWh/month for seniors + income supplement |
| Arnona property tax rates | https://www.gov.il/he/service/arnona-payment | Municipal arnona tariffs and discount eligibility |
| Kolzchut, olim arnona discount | https://www.kolzchut.org.il/he/הנחה_בארנונה_לעולים_חדשים | Exact eligibility window (12 months out of 24), 100 sqm cap, special-needs olim rules |
| Kolzchut, senior arnona discount | https://www.kolzchut.org.il/he/הנחה_בארנונה_לאזרחים_ותיקים | Senior age threshold (men 67; women at the rising retirement age, do NOT assume a flat 62), income tests, discount tiers |

## Bundled Resources

- `references/details-2026.md`: current electricity, water, LPG, cellular, fiber and arnona figures with effective dates and sources.
- `references/domain-checklist.md`: coverage contract with sources.

## Recommended MCP Servers

| MCP | What It Adds |
|-----|-------------|
| [Israeli CBS MCP](https://agentskills.co.il/he/mcps/tax-and-finance/israeli-cbs) | CPI and price-index series, useful for checking whether a tariff change tracks inflation or exceeds it |
| [Kolzchut (All-Rights)](https://agentskills.co.il/he/mcps/government-services/kolzchut) | Live text of the arnona, electricity and water discount entitlements this skill routes to |
| [Israel Statistics](https://agentskills.co.il/he/mcps/tax-and-finance/israel-statistics) | CBS price indices for cross-checking utility cost trends over time |

Utility tariffs move on published schedules. Use these to check whether a figure is current; confirm any rate's effective date before quoting it.

## Troubleshooting

### Error: "My electricity bill seems much higher than expected for my consumption level"

Cause: Several factors can cause unexpectedly high bills: billing estimate rather than actual meter reading (hashavon based on ha'aracha instead of kri'a), a faulty meter, electric water heater (dud hashmal) running inefficiently, or an AC unit consuming more than expected due to poor insulation or maintenance. Some households also don't realize they're being billed for common area electricity in apartment buildings (hashmal klalit).

Solution: Check if the bill shows an actual reading (kri'at moné) or an estimate (ha'aracha). If estimated, request an actual reading from IEC. Compare the meter reading on your bill with the physical meter. If consumption seems genuinely high, check for: electric water heater on during peak hours (dud hashmal timer), AC filters that need cleaning (dirty filters increase consumption by 15-20%), old refrigerator (replacing a 15+ year old unit saves ~30%), and phantom loads from devices on standby. Install the IEC app to monitor real-time consumption and identify spikes.

### Error: "Water bill shows consumption much higher than our actual usage"

Cause: The most common cause is an internal leak, often in a toilet that runs continuously (difficult to notice) or an underground pipe leak. Other causes include: meter reading error, unregistered nefashot (household members) putting more consumption into the expensive Tier 2, or building-wide meter issues in shared buildings.

Solution: Check for toilet leaks by adding food coloring to the tank and waiting 15 minutes without flushing; if color appears in the bowl, there's a leak. Check your most recent bill for nefashot count and verify all family members are registered with your water corporation. Read your water meter before bed and again in the morning without using any water; if the reading changed, you have a leak. Contact your water corporation to request a meter accuracy test (they are required to provide this). If a hidden leak is confirmed, you may be eligible for a bill adjustment (ha'aracha mechudeshét) for the leaked water.

For TOU-not-available, arnona rate mismatch, cellular promo-jump, and consolidating a split Bezeq + ISP bill, see the extended troubleshooting in `references/details-2026.md`.
