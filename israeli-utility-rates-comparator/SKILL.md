---
name: israeli-utility-rates-comparator
description: Compare electricity providers, water tariffs, cooking-gas (LPG) rates, cellular plans, fiber internet packages, and arnona (municipal property tax) across Israeli municipalities and utility companies. Use when a user needs to understand IEC tariff structures, calculate solar panel ROI, compare tiered water pricing, pick a cheap cellular plan, switch to fiber internet, or evaluate arnona differences between cities. Covers electricity market deregulation, independent power producers, Mekorot water pricing, cellular operators and MVNOs, fiber-optic infrastructure, and municipal rate variations. Do NOT use for commercial/industrial utility contracts at scale, or utility infrastructure investment analysis.
license: MIT
allowed-tools: Bash(python:*) WebFetch
---

# Israeli Utility & Telecom Rates Comparator

## Instructions

### Step 1: Identify Which Utility to Compare

Establish which bill the user wants to move; the levers differ sharply. Electricity, water and
cooking gas are national or near-national and barely change with location, arnona changes with the
municipality, telecom with the provider. Ask for the last three bills, and where a household has
several, start with the largest line rather than the one they mentioned. Market-structure
background, including who owns which telecom brand, is in `references/details-2026.md`.

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

- In force from 1.7.2026, re-verified against the IEC low-voltage TOU page on 27 August 2026: all three seasons and both VAT bases still match.
- **Peak applies on different days per season, and this is where most of the money is.** In SUMMER and in TRANSITION there is NO peak band at all on Fridays, holiday eves, Shabbat or holidays: the whole day is off-peak. In WINTER the peak band applies on every day including Shabbat and holidays. There is no morning peak in any season.
- For TOU purposes these holidays count as Shabbat, and their eves as Friday: Rosh Hashana, Yom Kippur, the first day of Sukkot, Simchat Torah, the first and seventh days of Pesach, Independence Day and Shavuot. The hours are Israel local time and the metering equipment is adjusted when summer time is in force.
- Do not quote transition-season band hours: the IEC page states them in a garbled form ("22:00-17:00"). It rarely matters, the spread there is under 4 agorot.
- Savings are seasonal: shifting load off-peak is worth over 120 agorot/kWh in summer and under 4 in transition. Never quote a flat "15-25% saving"; compute it from the user's own seasonal pattern.
- Tariffs update semi-annually via Electricity Authority decisions and can shift mid-year; verify before quoting.

**Fixed charges, priced (from 1.7.2026, IEC residential tariff page).** These are what makes a
bill more than kWh times rate, and a total cannot be computed without them. Agorot for energy,
shekels for the rest.

| Component | Excl. VAT | Incl. VAT |
|---|---|---|
| Energy, per kWh (agorot) | 53.83 | 63.52 |
| Distribution, bi-monthly customer, single-phase meter (**the ordinary residential case**) | 9.97 | 11.76 |
| Distribution, bi-monthly customer, three-phase meter | 11.56 | 13.64 |
| Distribution, monthly customer | 157.31 | 185.63 |
| Supply, bi-monthly customer, single-phase meter | 15.60 | 18.41 |
| Supply, bi-monthly customer, three-phase meter | 15.53 | 18.33 |
| Supply, monthly customer | 107.70 | 127.09 |
| Capacity, per KVA per year | 6.18 | 7.29 |

Two fixed charges, distribution and supply, not one, and the amount depends on whether the
customer is billed monthly or bi-monthly and on whether the meter is single or three phase.
**Pick the row before quoting a total.** A normal apartment is a bi-monthly, single-phase
customer; the monthly rows are roughly sixteen times larger per period, so choosing the wrong one
moves the fixed component by more than the whole energy charge of a small household, which can flip a supplier-switch or a TOU comparison.
On the TOU tariff the fixed charges differ again: monthly distribution 174.50 incl. VAT and
bi-monthly distribution 37.88, with supply the same as above.

**There is no broadcasting fee on an electricity bill.** Earlier versions of this skill listed
"agrat shidrur" among the charges an IEC customer keeps paying. The official residential
tariff page enumerates exactly three fixed components, distribution, supply and capacity, and
no broadcasting fee is among them.

The residential tariff itself applies to homes used for residence only, places of worship and
buildings used for agriculture.

For apartments there is also a share of common-area electricity (chashmal klali) for
stairwells, lifts and lobby lighting. That is billed through the va'ad bayit and is not on the
IEC bill at all, which is what surprises new tenants.

To compare electricity costs:
1. Obtain the user's recent electricity bills (at least 3 months, preferably 12 for seasonal patterns)
2. Note current monthly consumption in kWh
3. Check if they have a smart meter (required for TOU pricing)
4. If no smart meter, check eligibility and installation process with IEC (iec.co.il)

**Independent electricity producers (residential market):**

The residential electricity market is open to private suppliers. The residential supply market is open to private suppliers and the number who have switched keeps rising. The evidenced figure is roughly 279,500 customers who moved during 2025 (Calcalist); a '360,000 in 2026, up from ~280,000 at end-2025' pair previously stated here is NOT on any cited source and is withdrawn. Quote the direction, not a headcount. Active residential suppliers in 2026 include:
- **Cellcom Energy**, **Partner**, **Bezeq**, **HOT Energy** (telecom-bundled offers)
- **Pazgas Electricity**, **Amisragas**, **Electra Power** (energy and gas group offers)
- **OPC Energy**, **Dalia Energy**, **Enlight Renewable Energy** (independent generators, historically large-customer focused, also signing residential customers)

**Critical: switching does NOT replace the full bill.** Independent suppliers compete only on the **generation** (ייצור) component, which is roughly 60-70% of the bill. The household continues to pay IEC the fixed distribution (חלוקה) and supply (אספקה) charges and the capacity charge, priced in the table in Step 2. There is no broadcasting fee on the bill. The supplier discount applies only to the energy portion.

**Cooling-off period:** Under the Consumer Protection Law (חוק הגנת הצרכן), residential customers have a 14-day right to cancel after signing with an alternate supplier. Always read the cancellation clauses before signing, and keep a copy of the contract. The Energy Ministry is also working to shorten the supplier-switching window from 14 days to 7 days during 2026.

**Discounts on the electricity bill (separate from supplier choice). TWELVE groups qualify, not
three.** IEC's own entitlement page enumerates them, and earlier versions of this skill named only
seniors, Holocaust survivors and "the disabled", so a large family or a lone soldier reading it
would never learn they are entitled. Ask which of these applies before assuming none does:

1. Income-support benefit under s.2(a)(4) of the Income Support Law
2. Above retirement age receiving an old-age or survivors' pension PLUS income supplement
3. Nazi-persecution and war-disabled compensation recipients, and Holocaust survivors on
   income-tested compensation
4. Old-age pension for the disabled under s.251 of the National Insurance Law
5. Special-services allowance at 112% or more
6. Disabled-child allowance where the child depends on another person's help or needs special
   medical treatment (other disabled-child grounds do NOT qualify)
7. Nursing (סיעוד) allowance at level 5 or 6
8. A lone soldier in regular service, or a soldier entitled to rent assistance because of the
   distance between home and posting
9. A single parent (הורה עצמאי) with three or more children receiving income support, income
   supplement or alimony
10. A family with four or more children receiving income support, income supplement or alimony
11. IDF disabled at 50% or more, or below 50% with a permanent maintenance grant, and likewise
    hostile-action casualties on the same terms
12. Special-services allowance at 50%

The rate is 50% on consumption up to 400 kWh/month (800 kWh on a bi-monthly bill), and three
groups are set to move to 65%; verify status before quoting 65% as fact.

**The entitlement fails silently if the contract is in the wrong name.** The awarding body
(Bituach Leumi, the Holocaust Survivors' Rights Authority, the IDF or the Defence Ministry
depending on group) notifies the person and passes their details to IEC, but the discount only
lands if that person is the registered IEC consumer under their own name and ID number. Anyone in
one of the twelve groups who does not see a reduced payment on the bill should call IEC on 103 to
have the registration corrected. Tell users this: it is the most common reason a real entitlement
produces no money.

**Debt and disconnection protections (raise this with any user whose bill is unaffordable).**
Ask the supplier about a הסדר תשלומים (payment arrangement) for arrears, and about registering a
household dependent on electrically-powered life-support or medical equipment as a צרכן מוגן
(protected consumer). Both routes exist and are worth pursuing.

**Do not state the protections as absolutes.** The exact conditions are set in the Electricity
Authority's אמות מידה and are **not verified in this skill**. Tell the user the route exists and
to confirm the terms with the Authority or the supplier; do not tell them they cannot be
disconnected. Background in `references/details-2026.md`.

### Step 3: Calculate Solar Panel ROI

**EXPORT TARIFF WITHDRAWN. Do not quote one from this skill.** The only source it carries is a
March 2025 trade-press article about a tariff then out for CONSULTATION, reporting 0.60 ILS/kWh
for five years falling to 0.3807 (systems up to 30 kW) and 0.39 CPI-linked (up to 15 kW), and
identifying 0.48 over a fixed 25 years as the then-incumbent rate. Earlier versions of this skill
presented 48 agorot plus a "+6 agorot urban premium for cities over 50,000" as an ADOPTED regime
and told the agent to suppress the 0.60 and 0.38 figures, which are the source's own. That premium
and that population threshold appear in no source at all. Read the hesder line in the actual
contract or the current Electricity Authority tariff book, and say so to the user.

The parts that do not depend on the export tariff are still usable:

1. **Roof**: south-facing, unshaded, structurally sound, and confirm the applicant controls it (a
   shared roof needs the building's agreement).
2. **Annual production**: roughly 1,500-1,800 kWh per installed kWp, Negev at the top of that
   range, the north at the bottom, the centre between.
3. **Value of self-consumption**: every kWh used on site avoids the full retail rate, 63.52 agorot
   incl. VAT, which is verified. Export earns less than retail under every variant in the source,
   so **self-consumption is worth more than export**, and that conclusion holds without knowing the
   export tariff.
4. **Payback**: build it from self-consumption at the retail rate and present the export leg as a
   range the user must confirm. **Do not multiply an unverified export tariff across 25 years.**
   The contract duration is itself unresolved (published material differs between 25 and 15 years)
   and it moves a payback materially.

Fuller notes are in `references/details-2026.md`, under the same caveat.

### Step 4: Water Tariff Comparison

Water is priced in two tiers by the Water Authority, nationally, so unlike arnona it barely moves
between cities.

**The Tier-1 allocation has TWO limbs and the second is the one people miss.** The rule is up to
3.5 m3 per registered person per month, **and not less than 7 m3 per housing unit**. The floor
matters most to exactly the households least likely to know it: a one- or two-person home is
entitled to 7 m3 at the low rate regardless of headcount. Saying only "3.5 per person" under-claims
their allocation and prices the difference at the high rate.

- Tier 1 (low rate): 8.51 ILS/m3 incl. VAT, from 1 January 2026
- Tier 2 (everything above the allocation): 15.62 ILS/m3 incl. VAT

**Register every nefesh with the water corporation.** The allocation is per REGISTERED person and
registration is not retroactive beyond its date, so an unregistered household member is the single
most common cause of a bill that looks too high. Note also that since 1.5.2015 the development
levies (היטלי פיתוח) were replaced by כללי דמי הקמה, so do not tell a user to compare an
"infrastructure development levy" under the old name.

Corporation-by-corporation detail, the shared-meter case and leak-credit conditions are in
`references/details-2026.md`.

### Step 5: Natural Gas and Cooking Gas Comparison

**Cooking gas balloons (balonei gaz):**
- Standard 12 kg balloon
- **Not a published national maximum.** The Energy Ministry surface this skill links is a
  comparison calculator (מחשבון השוואת מחירי גז בישול) that asks for the user's LOCALITY and
  connection type and sits beside the ministry's own guides to switching a private or commercial
  gas supplier. Prices differ by supplier and by place, which is why a comparison-and-switching
  tool exists. Earlier versions of this skill told users to wait for a monthly published maximum,
  which pointed them away from the one lever that moves this bill.
- **This skill carries no LPG price anchor.** It has none for the balloon, none per kg, none for
  delivery and none for central gas. Send the user to the ministry calculator for their own
  locality rather than quoting a figure from here.
- Delivery fee varies by supplier
- Israeli LPG suppliers: Supergas, Pazgas, Amisragas, Dorgas
- Typical household uses 1 balloon every 1-3 months

**Natural gas (gaz tiv'i) home connection:**
- Available in newer residential buildings connected to the national gas grid
- Significantly cheaper per unit of energy than cooking gas balloons
- Monthly fixed connection fee plus usage-based charges
- Supply operator: Energean Israel (Karish/Tanin field), a separate company from NewMed Energy (formerly Delek Drilling, Tamar/Leviathan); local distribution companies handle last-mile delivery

**Central gas (גז מרכזי / צובר), a large apartment segment, has a real lever:** households on a shared bulk tank served by one LPG supplier have the RIGHT to switch central-gas supplier and to demand the supplier's published price list (LPG reform under חוק הפיקוח על מצרכים ושירותים). For these households, switching or renegotiating the central-gas supplier is the main way to lower cooking-gas cost, not just accepting the balloon price. See `references/details-2026.md`.

See `references/details-2026.md` for the balloon-versus-natural-gas comparison table and the break-even procedure.

### Step 6: Cellular and Internet Comparison

The Israeli telecom market is one of the cheapest in the developed world after a decade of post-2012 MVNO entry and a fiber-optic rollout that finished covering most of the country between 2022 and 2025. Most households can save 50-200 ILS/month by switching providers, but the comparison has to look at the **total** bill (line + roaming + add-ons) and at lock-in / introductory pricing carefully.

**Provider tables and price ranges** (cellular MNO/MVNO plans, fiber infrastructure operators, speed tiers) are in `references/details-2026.md`. Key points for the body:
- Cheapest cellular clusters ~33-35 NIS/month for 150-400GB with several thousand minutes (genuinely unlimited domestic calls sits at the top of that band); cheaper tiers exist but are data-only or low-data. No setup fee, no commitment ("ללא התחייבות"). Number portability is free and takes ~1 business day, sign with the NEW provider first (never cancel first, that creates a gap). eSIM is widely supported.
- Home internet splits into infrastructure (Bezeq BFiber, HOT, IBC/Unlimited, Cellcom/Partner fiber) and ISP; a single wholesale-market bundle usually beats a legacy split bill by 20-40 NIS/month. Fiber coverage is high and ADSL is being retired; the '>90% of households' figure this skill used to state is **unverified** and should not be quoted.
- Introductory prices commonly jump 50-100% after 12 months, set a reminder and re-shop. Triple-play (cellular+internet+TV) discounts vanish if you cancel one leg.
- **Check who owns the brand before calling it an alternative.** Golan Telecom's own About page states that it formerly held its own mobile licence, that since 24.12.2023 Golan Telecom services are provided on the licence of Cellcom Israel Ltd, and that the activity of Golan International was transferred to Cellcom Fixed-Line Communications. A Cellcom customer moving to Golan has therefore not moved to a different licensee. Brand names in this market outlive the independent companies behind them; verify ownership before presenting two brands as rival options.

**How to comparison-shop:**
1. **Pull last 3 months of bills** for cellular, internet, TV to see actual usage (data per line, peak speed observed, TV channels you watch)
2. **Run an Israeli comparator**: kamaze.co.il, kamazeole.co.il, israeliphoneplans.com, mishtalemli.co.il, or the Ministry of Communications official comparator at gov.il
3. **Get 2-3 quotes** by phone; tell each company you're shopping and ask for "מחיר שמירת לקוח" (retention price), usually 15-30% lower than the published price
4. **Time the switch**: cellular portability is free; internet may have a 1-2 week overlap so schedule installation before cancellation

### Step 7: Arnona Comparison Between Cities

Arnona is the largest recurring utility-like cost for an Israeli household and the only one that
changes materially between municipalities.

**Who pays it: the מחזיק, the occupier.** In a rented flat that is the TENANT, not the landlord.
This is the first thing to establish in any relocation or cost-comparison question and it is the
fact most often assumed the other way round.

**How it is charged:** a rate per square metre per YEAR, per zone within the municipality, and
different for residential and commercial. Divide by 6 for a bi-monthly bill or 12 for a monthly
one; treating the annual rate as monthly overstates the bill twelvefold. To find the rate, the
municipality's own site under arnona or tashlumim carries the tariff table per zone.

**Discounts** exist for olim, seniors, low income, disability, IDF and national service and
bereaved families, students, single-person households, and empty or uninhabitable property, each
with its own eligibility test and time limit. Two rules matter more than the list: **only one
discount applies per property at a time** (תקנות הסדרים במשק המדינה (הנחה מארנונה), תשנ"ג-1993), so
a household qualifying on two grounds gets the larger and not the sum; and a discount is granted
**on application**, so it does not arrive by itself. Never quote a percentage without checking the
municipality, since national regulations set ceilings that municipalities apply differently.

**Objection (השגה):** if the bill is wrong (size, zone, a missing discount, a balcony at full
rate), file a written hassagah with the municipal arnona manager within **90 days** of the bill.
The municipality must answer within **60 days** and silence counts as rejection. If rejected,
**30 days** to appeal to the ועדת ערר לארנונה, and **45 days** from its ruling to the בית משפט
לעניינים מנהליים. **These deadlines have not been independently verified in this skill and a wrong
one forfeits a legal right**: confirm them against the municipality's own notice, which must state
them, before relying on a date.

Indicative city figures, the full discount catalogue and step-by-step objection guidance are in
`references/details-2026.md`. City-average tables there are orders of magnitude, not quotes.

For IEC and water-corporation billing disputes (not arnona), the small-claims court is often a
faster path; its ceiling is carried from a previous cycle and is not re-verified here.

### Step 8: Tips for Reducing Utility Bills

Per-utility bill-reduction tips (electricity, water, arnona, cellular & internet) are in `references/details-2026.md`. Highest-leverage actions: shift electricity to off-peak on a TOU tariff, register all nefashot for the water Tier-1 allocation and fix leaks fast, apply for every arnona discount and verify recorded property size, and compare cellular/internet against MVNOs / wholesale bundles while asking for a "מחיר שמירת לקוח" retention price.

### Step 9: Smart Meter Adoption and Monitoring

A smart meter (מונה חכם) is a prerequisite for the TOU tariff and is what makes any load-shifting
advice actionable, because without interval data there is nothing to shift against. IEC installs
them on request and on a national rollout. The consumption data is what turns the seasonal peak
and off-peak figures in Step 2 into a number for this household rather than a national average.
Adoption details, the rollout position, the data-access routes and prepaid meters are in
`references/details-2026.md`.

## Examples

### Example 1: Family Evaluating Solar Panels

User says: "We pay about 800 ILS a month for electricity. Is solar worth it?"

Convert the bill to kWh at the verified retail rate (63.52 agorot incl. VAT), size the system
from annual consumption divided by the kWh-per-kWp band for their region, and price the saving on
SELF-CONSUMPTION at that retail rate, which is a number this skill can stand behind. Then stop:
present the export leg as something the installer's contract and the current tariff book must
supply, not as a figure from here, and do not multiply an unverified export rate across 25 years
to produce a lifetime saving. Tell the family to get three quotes and to confirm they control the
roof. The worked arithmetic is in `references/details-2026.md`, and it carries the same caveat.

### Example 2: Comparing Utility Costs Between Cities for Relocation

User says: "Should I move from Tel Aviv to Haifa? How much will I save on utilities?"

Electricity, water and cooking gas are national or near-national, so they barely move with the
city. Arnona does, and it is the only line that materially changes. Work it from the user's own
apartment size in square metres, the specific rate zone of each address, and the discounts they
personally qualify for, and treat any city-average table as an order of magnitude rather than a
quote. Give the annual arnona delta and say plainly that the rest of the utility bill is
substantially the same in both cities. Indicative city figures and the objection procedure are
in `references/details-2026.md`.

### Example 3: Optimizing Electricity Bill with Smart Meter

User says: "I have a smart meter. How do I lower my bill?"

Pull the interval data, find how much consumption already sits in the peak band, and price the
shift using the SEASONAL figures from Step 2 rather than a flat percentage: moving a load off
peak is worth over 120 agorot/kWh in summer and under 4 in the transition season, and in summer
and transition there is no peak band at all on Fridays, Shabbat and holidays, so weekend loads
are already off-peak. Then check whether TOU beats the flat tariff for this household at all: a
household that cannot move its evening load is usually better off on the flat rate. Only after
that is the supplier-discount question worth raising, and it touches the generation component
only, not the fixed charges.

## Gotchas
- Israel Electric Corporation rates are updated by the Electricity Authority on a semi-annual cycle, and a mid-year update can move the rate: the 1.7.2026 update moved the residential rate to 53.83 agorot excluding VAT and 63.52 including, down from the January 2026 edition. Agents routinely quote a superseded rate. Always verify the current tariff before quoting per-kWh numbers.
- The TOU (tariff TOZ / תעו"ז) schedule has only two tiers since April 2023: peak (שיא) and off-peak (שפל). The former שלב הגבע (shoulder) tier was eliminated. Agents trained on older docs may still describe a 3-tier structure with a middle band.
- Switching to an alternate electricity supplier (Cellcom Energy, Pazgas, OPC, etc.) only discounts the generation component, which is roughly 60-70% of the bill. The household still pays IEC the fixed distribution and supply charges and the capacity charge (there is no broadcasting fee on the bill; see the priced table in Step 2). Agents may incorrectly imply the entire bill changes.
- Water Tier 1 covers up to 3.5 m³ per registered nefesh per month at the lower rate, with a floor: the recognized quantity per housing unit is never less than 7 m³ per month, so a single-occupant household gets 7 rather than 3.5; consumption above goes to Tier 2 (~84% higher in Jan 2026: 8.51 vs 15.62 ILS/m³ inc. VAT). Sewage is bundled into the regulated per-m³ tariff in most municipalities, NOT a separate percentage surcharge as some older guides describe.
- Israeli utility bills include 18% VAT (raised from 17% on 1 Jan 2025). A rise to 19% was floated at the Finance Ministry but was not enacted: the 2026 state budget contains no such increase, so quote 18%. Be explicit about whether quoted prices include or exclude VAT, especially when comparing alternate-supplier offers, since some advertise the pre-VAT generation rate.
- The Olim Hadashim arnona discount is 90% on up to 100 sqm for 12 months out of the 24 months following aliyah registration, NOT yearly. Agents may incorrectly describe it as multi-year (e.g., "90% first year, 10% years 2-5"). Disabled olim recognized by Bituach Leumi get up to 80% indefinitely under a separate provision.
- The IEC customer-service number is **103**; calls from a Bezeq or HOT landline are free. Do not emit older short codes from memory, they may point at a dead number.
**EXPORT TARIFF WITHDRAWN.** This skill does not state a residential solar export tariff. The only source it carries is a March 2025 trade-press article about a tariff then out for CONSULTATION, which reports 0.60 ILS/kWh for five years falling to 0.3807 (up to 30 kW) and 0.39 CPI-linked (up to 15 kW), and identifies 0.48 over a fixed 25 years as the then-incumbent rate. The '+6 agorot urban premium for cities over 50,000' previously stated here is in no source at all. Read the hesder line in the actual contract or the current Electricity Authority tariff book. Do not multiply an export rate across 25 years from anything in this skill. Self-consumption at the verified 63.52 agorot retail rate is the part that can be relied on.

- Cellular promo-expiry mechanics and the number-portability procedure (always sign with the NEW provider first) are in `references/details-2026.md`.
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
| Arnona property tax rates | (link removed, this gov.il page now returns 404) | Municipal arnona tariffs and discount eligibility |
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

Utility tariffs move on published schedules. Confirm any rate's effective date before quoting it.

## Troubleshooting

### Error: "My electricity bill seems much higher than expected for my consumption level"

Cause: Several factors can cause unexpectedly high bills: billing estimate rather than actual meter reading (hashavon based on ha'aracha instead of kri'a), a faulty meter, electric water heater (dud hashmal) running inefficiently, or an AC unit consuming more than expected due to poor insulation or maintenance. Some households also don't realize they're being billed for common area electricity in apartment buildings (hashmal klalit).

Solution: Check if the bill shows an actual reading (kri'at moné) or an estimate (ha'aracha). If estimated, request an actual reading from IEC. Compare the meter reading on your bill with the physical meter. If consumption seems genuinely high, check for: electric water heater on during peak hours (dud hashmal timer), AC filters that need cleaning (dirty filters increase consumption by 15-20%), old refrigerator (replacing a 15+ year old unit saves ~30%), and phantom loads from devices on standby. Install the IEC app to monitor real-time consumption and identify spikes.

### Error: "Water bill shows consumption much higher than our household uses"

Cause: an unregistered household member (so the Tier-1 allocation is too small), a leak between
the municipal meter and the apartment, or a shared-meter building where one bill is split by
apartment count rather than by actual use.

Solution: first register every nefesh with the water corporation, since Tier 1 is allocated per
registered person and the allocation is retroactive only from the registration date. Then check
for a leak by closing every tap and watching the meter. A leak repaired promptly can qualify for
a partial credit. Full diagnostic sequence, the shared-meter case and the credit conditions are
in `references/details-2026.md`.
