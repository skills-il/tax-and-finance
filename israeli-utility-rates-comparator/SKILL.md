---
name: israeli-utility-rates-comparator
description: >-
  Compare electricity providers, water tariffs, natural gas rates, and arnona (municipal
  property tax) across Israeli municipalities and utility companies. Use when a user needs
  to understand IEC tariff structures, calculate solar panel ROI, compare tiered water
  pricing, or evaluate arnona differences between cities. Covers electricity market
  deregulation, independent power producers, Mekorot water pricing, and municipal rate
  variations. Do NOT use for commercial/industrial utility contracts, telecommunications
  comparisons, or utility infrastructure investment analysis.
license: MIT
allowed-tools: "Bash(python:*) WebFetch"
metadata:
  author: skills-il
  version: 1.0.0
  category: tax-and-finance
  tags:
    he:
      - חשמל
      - מים
      - גז
      - ארנונה
      - תעריפים
      - השוואת מחירים
    en:
      - electricity
      - water
      - gas
      - arnona
      - tariffs
      - price-comparison
  display_name:
    he: "השוואת תעריפי חשמל ומים בישראל"
    en: "Israeli Utility Rates Comparator"
  display_description:
    he: "השוואת ספקי חשמל, תעריפי מים וגז וארנונה בין רשויות מקומיות בישראל"
    en: "Compare electricity providers, water tariffs, gas rates, and arnona across Israeli municipalities"
  supported_agents:
    - claude-code
    - cursor
    - github-copilot
    - windsurf
    - opencode
    - codex
---

# Israeli Utility Rates Comparator

## Instructions

### Step 1: Identify Which Utility to Compare

Determine which utility cost the user wants to analyze. Israeli household utilities include:

**Electricity (חשמל):**
- Israel Electric Corporation (IEC / חברת החשמל) is the dominant provider
- The electricity market is undergoing deregulation; independent producers now compete
- Tariffs are set by the Electricity Authority (רשות החשמל)
- Time-of-use (TOU) pricing available for smart meter customers

**Water (מים):**
- Mekorot (מקורות) is the national water company supplying bulk water
- Municipal water corporations (taagidei mayim) handle local distribution
- Tiered pricing: ascending block tariff system where price per cubic meter increases with consumption

**Natural Gas (גז טבעי) and Cooking Gas (גז בישול):**
- Natural gas infrastructure expanding via Energean/Delek pipelines
- Many homes still use cooking gas balloons (balonei gaz)
- Natural gas connection available in newer buildings and select areas

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

**Time-of-use tariff (tariff meshutane, TOU / עונתי):**
- Requires a smart meter (moné chokhéakh)
- Different rates for peak (shpia), shoulder (gerev), and off-peak (shefel) hours
- Peak hours: typically Sunday-Thursday 17:00-22:00 (summer), 7:00-17:00 (winter)
- Off-peak: nights and Shabbat/holidays
- Can save 15-25% for households that shift consumption to off-peak hours

**Monthly fixed charges:**
- Connection fee (agrat chibbur) regardless of consumption
- Distribution fee
- Public broadcasting fee (agrat shidrur)

To compare electricity costs:
1. Obtain the user's recent electricity bills (at least 3 months, preferably 12 for seasonal patterns)
2. Note current monthly consumption in kWh
3. Check if they have a smart meter (required for TOU pricing)
4. If no smart meter, check eligibility and installation process with IEC (iec.co.il)

**Independent electricity producers:**

Since the electricity market reform, independent producers offer alternatives:
- **OPC Energy** - Major independent producer, offers competitive rates to large consumers
- **Dalia Energy** - Solar-based production
- **Enlight Renewable Energy** - Renewable energy focus
- Most independent producer deals are currently for large consumers and businesses, but the market is gradually opening to residential customers

### Step 3: Calculate Solar Panel ROI

Solar panels (panelim sola'riyyim) are increasingly popular in Israel due to high solar irradiance.

**Net metering program:**
- Install solar panels on your roof or property
- Excess electricity is fed back to the IEC grid
- Your electricity meter runs backward when producing
- You pay only for net consumption (consumption minus production)
- System size limited to your annual consumption level

**ROI calculation factors:**
1. **System cost**: typically 15,000-40,000 ILS for residential (3-10 kW)
2. **Annual production**: Israel averages 1,500-1,800 kWh per installed kW (Negev gets more, north gets less)
3. **Current electricity cost**: multiply production by current IEC tariff rate
4. **Annual savings**: production in kWh multiplied by tariff rate
5. **Payback period**: system cost divided by annual savings (typically 5-8 years in Israel)
6. **System lifetime**: 25+ years with gradual degradation (0.5% per year)
7. **Maintenance**: minimal, panel cleaning 1-2 times per year
8. **Feed-in tariff**: for systems approved under previous programs, a guaranteed purchase rate applies

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
- Approximately 50-60% more expensive than Tier 1
- Applies to all consumption beyond the basic allocation

**Important factors:**
- **Nefashot registration**: register all household members at your water corporation to maximize Tier 1 allocation. Unregistered members mean a lower threshold before Tier 2 kicks in.
- **Garden/pool allocation**: additional allocation available for documented garden irrigation or swimming pool
- **Sewage surcharge (biuv)**: charged as a percentage of water consumption, varies by municipality

**Municipal water corporations (examples):**
- **Mei Avivim** (Tel Aviv)
- **Hagihon** (Jerusalem)
- **Mei Haifa** (Haifa)
- **Mei Raanana** (Raanana)
- **Mekorot** directly (some smaller localities)

Each corporation may add slightly different surcharges for infrastructure and maintenance. Compare by checking:
1. Base water rate per m3 (Tier 1 and Tier 2)
2. Sewage rate
3. Fixed monthly/bi-monthly charge
4. Infrastructure development levy (where applicable)

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
- Compare local suppliers: Supergas, Pazgas, Amerigas
- Typical household uses 1 balloon every 1-3 months

**Natural gas (gaz tiv'i) home connection:**
- Available in newer residential buildings connected to the national gas grid
- Significantly cheaper per unit of energy than cooking gas balloons
- Monthly fixed connection fee plus usage-based charges
- Main infrastructure operators: Energean Israel (formerly Delek Drilling) for supply, local distribution companies for last-mile delivery

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

### Step 6: Arnona Comparison Between Cities

Arnona (municipal property tax) is the largest recurring utility-like cost for Israeli households. Rates vary dramatically between municipalities.

**How arnona is calculated:**
- Rate per square meter per month (shekel l'meter ravu'a l'hodesh)
- Different rates for different zones within the same municipality
- Different rates for residential vs. commercial properties
- Discounts available for eligible populations (olim chadashim, elderly, low income, disabled)

**Arnona rates in major cities (residential, approximate):**

| City | Rate per sqm/month (ILS) | 80 sqm monthly | 100 sqm monthly |
|------|--------------------------|-----------------|------------------|
| Tel Aviv | High range | ~550-700 | ~700-880 |
| Jerusalem | Medium-high | ~450-600 | ~570-750 |
| Haifa | Medium | ~380-500 | ~480-630 |
| Beer Sheva | Lower | ~280-380 | ~350-480 |
| Raanana | High | ~500-650 | ~630-810 |
| Netanya | Medium | ~350-480 | ~440-600 |
| Rishon LeZion | Medium-high | ~400-550 | ~500-690 |
| Petah Tikva | Medium | ~380-500 | ~480-630 |

Note: Rates vary by zone within each city and change annually. Always verify current rates at the municipality website.

**How to check your arnona rate:**
1. Visit your municipality's website (iriya / moatza mekomit)
2. Look for "arnona" section or "tashlumim" (payments)
3. Find the tariff table (tav tariffim) for your zone
4. Calculate based on your property size and classification

**Arnona discounts (hanashot):**
- New immigrants (olim): up to 90% discount for first year, 10% for years 2-5
- Senior citizens (over 62/67): discounts available based on income
- Low income (hakhnasoat nemukhoht): significant discounts, apply through municipal welfare department
- Disabled (nekhim): discounts based on disability percentage
- National service / IDF veterans: various discounts
- Students: some municipalities offer student discounts
- Single-person household: some municipalities offer discounts

### Step 7: Tips for Reducing Utility Bills

**Electricity:**
1. Switch to TOU tariff if you have or can get a smart meter
2. Run washing machine, dryer, and dishwasher during off-peak hours (nights, Shabbat)
3. Install LED lighting throughout the home
4. Set AC to 24-25 degrees Celsius (not lower)
5. Use ceiling fans alongside AC to distribute cool air
6. Consider solar water heater (dud shemesh) maintenance for optimal hot water heating
7. Unplug devices on standby (saves 5-10% on electricity)

**Water:**
1. Register all household members for nefashot allocation
2. Fix leaking faucets and toilets promptly (a leaking toilet can waste 200+ liters per day)
3. Install low-flow showerheads and faucet aerators
4. Use dual-flush toilet mechanisms
5. Water garden during evening hours to reduce evaporation

**Arnona:**
1. Verify your property size in municipal records matches actual measured size
2. Apply for all eligible discounts
3. Pay annual lump sum for a discount (some municipalities offer 1-2% for annual payment)
4. Report any changes in household composition that may qualify for discounts
5. If you run a business from home, verify you're not being overcharged with commercial rates for your entire property

### Step 8: Smart Meter Adoption and Monitoring

**Smart meters (monéi chokhéakh):**
- IEC is gradually rolling out smart meters across Israel
- Allow real-time consumption monitoring
- Enable TOU pricing
- Check eligibility at iec.co.il or call *2730

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
1. Calculate approximate monthly consumption: 800 ILS / ~0.60 ILS per kWh (approximate residential tariff) = ~1,333 kWh per month
2. Determine system size needed: 1,333 * 12 / 1,600 (kWh per kW in central Israel) = ~10 kW system
3. Estimate system cost: 10 kW * ~3,500 ILS per kW = ~35,000 ILS
4. Calculate annual savings: 800 * 12 = 9,600 ILS per year
5. Payback period: 35,000 / 9,600 = ~3.6 years
6. 25-year total savings: (9,600 * 25) - 35,000 = ~205,000 ILS (not accounting for degradation and tariff changes)
7. Check roof suitability: Modi'in gets good solar irradiance, verify south-facing roof availability
8. Recommend getting 3 installer quotes and checking with the local municipality for permit requirements

Result: User receives a detailed ROI analysis showing that solar panels would pay for themselves in approximately 3-4 years with total savings exceeding 200,000 ILS over the system lifetime, making it a strong investment.

### Example 2: Comparing Utility Costs Between Cities for Relocation

User says: "I'm deciding between moving to Beer Sheva or Haifa. What's the difference in utility costs for a 100 sqm apartment, family of 4?"

Actions:
1. Compare arnona rates:
   - Beer Sheva: approximately 350-480 ILS/month for 100 sqm residential
   - Haifa: approximately 480-630 ILS/month for 100 sqm residential
   - Difference: approximately 130-150 ILS/month in favor of Beer Sheva
2. Compare water costs:
   - Both cities use tiered pricing, rates similar at the national level
   - Check specific water corporation surcharges (Mei Haifa vs. Beer Sheva water corp)
   - Family of 4: approximately 14 m3/month Tier 1 allocation
3. Compare electricity:
   - IEC rates are national (same everywhere)
   - Beer Sheva: higher AC costs in summer (desert climate), but better solar potential
   - Haifa: more moderate climate, lower summer cooling costs
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
   - Run washing machine and dryer after 23:00 or on Shabbat (off-peak)
   - Use dishwasher timer for off-peak operation
   - Pre-cool home before peak hours in summer
   - Switch electric water heater timer to heat during off-peak (if applicable)
4. Calculate potential savings:
   - If 40% of consumption shifts from peak to off-peak: savings of approximately 15-20%
   - 600 * 0.17 = ~100 ILS/month potential savings
5. Recommend IEC app for monitoring real-time consumption
6. Suggest additional measures: LED bulbs, AC at 24-25 degrees, unplug standby devices

Result: User receives a practical action plan for shifting consumption to off-peak hours, with estimated monthly savings of 80-120 ILS, plus an ongoing monitoring strategy using the IEC app.

## Troubleshooting

### Error: "My electricity bill seems much higher than expected for my consumption level"

Cause: Several factors can cause unexpectedly high bills: billing estimate rather than actual meter reading (hashavon based on ha'aracha instead of kri'a), a faulty meter, electric water heater (dud hashmal) running inefficiently, or an AC unit consuming more than expected due to poor insulation or maintenance. Some households also don't realize they're being billed for common area electricity in apartment buildings (hashmal klalit).

Solution: Check if the bill shows an actual reading (kri'at moné) or an estimate (ha'aracha). If estimated, request an actual reading from IEC. Compare the meter reading on your bill with the physical meter. If consumption seems genuinely high, check for: electric water heater on during peak hours (dud hashmal timer), AC filters that need cleaning (dirty filters increase consumption by 15-20%), old refrigerator (replacing a 15+ year old unit saves ~30%), and phantom loads from devices on standby. Install the IEC app to monitor real-time consumption and identify spikes.

### Error: "Water bill shows consumption much higher than our actual usage"

Cause: The most common cause is an internal leak, often in a toilet that runs continuously (difficult to notice) or an underground pipe leak. Other causes include: meter reading error, unregistered nefashot (household members) putting more consumption into the expensive Tier 2, or building-wide meter issues in shared buildings.

Solution: Check for toilet leaks by adding food coloring to the tank and waiting 15 minutes without flushing; if color appears in the bowl, there's a leak. Check your most recent bill for nefashot count and verify all family members are registered with your water corporation. Read your water meter before bed and again in the morning without using any water; if the reading changed, you have a leak. Contact your water corporation to request a meter accuracy test (they are required to provide this). If a hidden leak is confirmed, you may be eligible for a bill adjustment (ha'aracha mechudeshét) for the leaked water.

### Error: "I can't find the TOU (time-of-use) tariff option for my account"

Cause: TOU pricing requires a smart meter (moné chokhéakh), which not all households have yet. IEC is rolling out smart meters gradually, and some areas haven't been covered yet. Additionally, some older electrical panel configurations may need upgrades to support smart meter installation.

Solution: Call IEC customer service at *2730 or check iec.co.il to verify if your area is eligible for smart meter installation. If eligible, request installation (free of charge from IEC). Installation typically takes 2-4 weeks from request. Once installed, contact IEC to switch your tariff plan from standard to TOU. Note that TOU is only beneficial if you can shift significant consumption to off-peak hours; if your consumption is already mostly during off-peak times (work from home at night, Shabbat observer), the savings will be greater. If you can't shift consumption, the standard tariff may actually be cheaper since TOU peak rates are higher than the standard flat rate.

### Error: "Arnona rate on my bill doesn't match the published municipal tariff"

Cause: Arnona calculations can be confusing because the published rate per sqm may not include additions like special area surcharges (tosefet ezor), stairwell charges (misparim klalit), shared area allocations, or adjustments for semi-enclosed spaces (mirpesot, mamadim) that are measured at partial rates. Some municipalities also have different rates for different floors or building ages.

Solution: Request a detailed arnona calculation breakdown (pirutt chishuv arnona) from your municipality's arnona department. Verify the property size they have on file matches your actual measured area (sometimes construction records have errors). Check if enclosed balconies (mirpeset sugéret) are being charged at full rate or partial rate (typically 60-75% of full rate for semi-enclosed spaces). The mamad (safe room) is usually charged at full rate if it's a standard room but verify this. If you believe there's an error, file a formal objection (hassaga) within 90 days of receiving the bill. You can also request a municipal surveyor to re-measure your property.
