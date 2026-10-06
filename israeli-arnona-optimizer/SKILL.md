---
name: israeli-arnona-optimizer
description: Calculate municipal property tax (arnona) for Israeli properties, check discount eligibility, and draft appeal letters to arnona committees. Use when a user needs to estimate arnona payments by municipality, zone, and property usage type, verify eligibility for discounts (olim, soldiers, elderly, disabled, low income, students, single parents), or prepare formal appeals with legal references. Covers all major Israeli municipalities including Tel Aviv, Jerusalem, Haifa, and Beer Sheva. Do NOT use for income tax (mas hachnasa), VAT (maam), or national insurance (bituach leumi) calculations, which fall under separate Israeli tax authorities.
license: MIT
allowed-tools: Bash(python:*) Read Edit Write WebFetch
compatibility: Requires Python 3.8+ for calculator script
---

# Israeli Arnona Optimizer

## Legal notice

This is a free information tool operated by an AI model. It explains the tax rules and helps you organise your own figures. All of its outputs are produced automatically by an AI model, with no involvement, review, or approval by a tax adviser or accountant. The output is not a tax opinion, not a return prepared by a licensed representative, and not professional advice, but a general calculation and explanation only: it does not examine the full extent of your income or your complete documents. An AI model may err, omit data, or present a wrong conclusion.

Any form or text this tool produces is an automatic draft for your personal preparation only, and is not a filed return. Responsibility for reporting and for paying the tax is yours, the binding computation is the Tax Authority's, and representation before the Tax Authority is reserved to those permitted by law. This tool is not a substitute for advice that takes account of the particular circumstances and needs of each person. Consult a tax adviser or accountant before filing or paying. All use of its output is the user's sole responsibility.

## Instructions

### Step 1: Gather Property and Household Details

Before calculating anything, collect:

1. **Municipality** (iriya) or local council.
2. **The bill's own codes**: zone (azor), building type or size class, and charged area. Every city keys its residential rate on zone AND a building type or size class, so ask for the bill rather than guessing from the address.
3. **Usage type**: residential (megurim), or offices, commerce, industry and so on. The calculator carries residential tables only.
4. **Who the holder (machzik) is.** The holder is whoever actually holds the property as owner, tenant or otherwise (Municipalities Ordinance s.1). A holder who leaves stays liable until they give the municipality written notice (s.325). On a sale, or a lease of a year or more, the seller or landlord must notify the municipality and name the buyer or tenant, or stays liable for whatever they do not pay; on a lease shorter than a year the landlord is liable (s.326). Every discount and every objection belongs to the holder, not automatically to the owner.
5. **Who lives in the flat.** The Reg. 2(a)(8) income test counts the holder AND everyone living with them, and picks the row by the number of people living there. For a divorced or separated parent, ask whether the children actually live with them: the household size, the income-test row, and whether a single-parent row can apply at all all turn on it.
6. **Which fiscal year** the question is about. In October to December the user is often deciding about both the current year and the next one.

### Step 2: Calculate Base Arnona

The calculator carries the full fiscal-2026 residential table of eleven cities, read from each city's own tzav arnona: Tel Aviv-Yafo, Jerusalem, Haifa, Beer Sheva, Netanya, Rishon LeZion, Petah Tikva, Ashdod, Ramat Gan, Herzliya and Raanana.

```bash
python scripts/arnona-calculator.py --municipality tel-aviv --area 85 --zone 2 --type ב+ג
python scripts/arnona-calculator.py --list-types haifa
```

- Without `--type` the script lists every row of the tzav that fits the zone and area, with the annual total for each. Do not quote a single figure from that list; ask for the type on the bill.
- For any other authority, or any non-residential property, pass the rate from that authority's tzav or the bill: `--municipality other --rate-per-sqm 150 --usage commercial`.
- Size can change the rate for the whole flat, not just the extra metres. Haifa's regular class pays one rate up to 75 sqm, another for 76 to 100, another above 100. Ashdod is marginal: the first 75 sqm at one rate, every further metre at a higher one.
- Jerusalem zone ד: the ministers approved charging types 1 and 2 at zone ג rates for 2026, but the booklet the municipality published in September 2026 still prints the old cells. The script shows both; the bill decides.

`references/arnona-rates-guide.md` explains how each city keys its rates, with each city's lowest and highest residential rate.

**The annual national update.** Rates rise every 1 January by a national coefficient: half the change in the CPI plus half the change in the public-sector wage. **It is 1.626% for 2026 and 3.05% for 2027.** A council needs an exceptional approval from the Interior and Finance ministers to go above it. The script prints a 2027 projection at 3.05%, and with `--fiscal-year 2027` computes on it; that is wrong for any city that obtained an above-formula increase or reclassified zones.

### Step 3: Check Discount Eligibility

Israeli arnona discounts come from ONE national instrument, the Arrangements in the State Economy Regulations (Arnona Discount), 5753-1993, plus municipal bylaws on top. Two things decide how you phrase an answer:

- **Ceiling vs entitlement.** Almost every row in Regulation 2 opens with "a council MAY set a discount not exceeding X percent". That X is a **ceiling the municipality chooses within**, not an amount the resident is owed. Chapter Hey2 (Regulations 14e, 14e1) and Regulations 3c and 3c1 are the opposite: the resident "is entitled", and the municipality has no discretion. Never present a Regulation 2 ceiling as an entitlement.
- **Area caps differ per row.** 100 sqm, 70 sqm (90 sqm if more than four family members live with the holder, which Kol Zchut and Jerusalem's 2026 tzav read as five or more people in the flat), or no cap at all. Applying a blanket 100 sqm to every row overstates several discounts and understates others.

**A. Entitlements (mandatory, no municipal discretion)**

| Who | Discount | Area cap | Source |
|-----|----------|----------|--------|
| Conscript soldier (and up to 4 months after discharge), national-service volunteer, civilian-security service | 100% | 70 sqm, 90 sqm if the holder's family living with them exceeds four | Reg. 14e(1), cap in Reg. 14f |
| Parent supported by the soldier before service, with no other livelihood | 100% | same | Reg. 14e(1)(b) |
| Civilian-social service, 30 weekly hours over two years | three quarters | same | Reg. 14e(1a) |
| IDF-disabled, Nazi-war disabled, police and prison-service disabled, bereaved family of a fallen serviceperson, hostile-action casualty | two thirds | same | Reg. 14e(2) |
| Civilian service split track, or civilian-social service 20 weekly hours over three years | 50% | same | Reg. 14e(3) |
| Person determined to be a hostage or missing person (Hostages and Missing Persons Law 5784-2023) | 100% | none | Reg. 14e1 |
| Senior citizen whose total income from every source is within the average wage; where more than one senior lives in the flat, the combined income of all residents must be within 150% of the average wage | 30% | 100 sqm | Senior Citizens Law 5750-1989, s.9(b) and s.9(c)(4) |
| The same senior, receiving an income-support benefit under the Income Support Law 5741-1980 | 100% | 100 sqm | Senior Citizens Law, s.9(b) |
| Senior whose pension income is at most 24.3% of the average wage (38.3% with a spouse) and who would get income support but for that pension; only seniors first insured from the comprehensive-pension extension order onward | 100%, as for income support | 100 sqm | Senior Citizens Law, s.13A |
| Holder in Sderot, the Gaza-envelope localities, or within 7 km of the Gaza perimeter fence | 45% residential, 39% other property | none | Reg. 3c, fiscal years 2015 to 2026 |
| Holder in an evacuated locality listed under the Iron Swords deferral law | 100% from 7 October 2023 to the end of the evacuation period | none | Reg. 3c1 |

The senior entitlement runs for one flat only and goes to one senior only, even where several qualify in the same flat, and it applies even when only one of the spouses is a senior. Once granted it renews automatically; a senior on the 30% rate who is under 70 gets automatic renewal for three calendar years or until turning 70, whichever comes first, and must re-apply after that. Regulation 2(a)(1) below is the parallel DISCRETIONARY route, which is why the same person can appear in both tables at different rates. Give the resident the higher one, since only one discount applies.

Reg. 3c runs to fiscal 2026. No 2027 extension had been published by October 2026; earlier extensions were published late and applied retroactively.

**B. Ceilings the council may set within (Regulation 2 and Regulations 3f, 3g, 7, 14c)**

| Who | Ceiling | Area cap | Reg. 2 paragraph |
|-----|---------|----------|------------------|
| Senior citizen receiving old-age, survivors, dependants, or work-injury pension | 25% | 100 sqm | 2(1)(a) |
| The same senior who also receives an income-support benefit | 100% | 100 sqm | 2(1)(b) |
| Full monthly benefit with earning-incapacity 75% or more, including a pre-old-age-pension determination | 80% | none stated | 2(2) |
| Proven medical disability of 90% or more | 40% | none stated | 2(3) |
| Prisoner of Zion or family of a Hanged of the Kingdom; Nazi-persecution disability pension; German BEG, Dutch WUV, Austrian OFG, or Belgian 1954 pension | 66% | 70 sqm, 90 sqm if more than four family members live with them | 2(4) |
| Holder of a blind person's certificate under the Welfare Services Law 5718-1958 | 90% | none stated | 2(5) |
| Oleh, or holder of an oleh-citizen certificate | 90% | 100 sqm, for 12 months chosen within the first 24 | 2(6) |
| Oleh dependent on the help of others, receiving a special or nursing benefit for olim | 80% | none stated | 2(6a) |
| SLA (South Lebanon Army) member recognised as rehabilitation-eligible, and their spouse | 90% | 100 sqm, 12 months within 36 from arrival after May 2000 | 2(6b) |
| Recipient of a long-term nursing benefit (gimlat siud) under Chapter Vav of the National Insurance Law | 70% | none stated | 2(7)(c) |
| Average monthly income within the First Schedule table, by household size | 90% / 70% / 50% / 30% by income column | none stated | 2(8) |
| Righteous Among the Nations recognised by Yad Vashem, and their spouse | 66% | none stated | 2(9) |
| Single parent as defined in the Single-Parent Families Law 5752-1992; or a single parent of a co-resident child under 21 in conscript or national service | 20% | none stated | 2(10) |
| Parent of a child, including a foster child, for whom a disability benefit is paid | 33% PER entitled child, combined ceiling 90% (Arrangements Law s.12(g)) | 100 sqm | 2(11) |
| Released captive entitled to payment under the Payments to Released Captives Law 5765-2005 | 20% | none stated | 2(12) |
| Active reserve soldier holding a valid active-reservist certificate | 5% | none stated | Reg. 3f |
| Active reserve COMMANDER in a command role holding a valid certificate | 25% | 100 sqm | Reg. 3g |
| Needy holder (nazak): exceptional medical expenses, or an event causing a serious unforeseen worsening of their material position | 70%, granted by the discounts committee | none stated | Reg. 7 |
| Senior business owner: sole business up to 75 sqm, aged 65 (60 for a woman), turnover up to 240,000 NIS index-linked (327,191.24 NIS for 2025), already receiving a Reg. 2(8) discount at home | the same rate given on the home | first 40 sqm of the business | Reg. 14c |

Single parent: Reg. 2(a)(10) imports the Single-Parent Families Law definition, so marital status alone does not decide it. A divorced parent whose children live with the other parent should be checked against that definition before the row is offered.

**No national row exists for these.** The regulation has NO student discount and NO large-family discount. A municipality may still grant one under its own bylaw, so check the local table, but there is no national rate to quote and none should be assumed. A large family's national route is the Regulation 2(8) income test, whose thresholds rise with household size.

**Rows outside Regulation 2.** Several rows live in other laws or in transitional provisions, so a reader of the consolidated regulation will not find them: Prisoner of Zion on an income-based benefit who received income support for 6 months before claiming (100%, mandatory, 100 sqm); old-age-for-disabled pension recipient within the average-wage income test (100%, 100 sqm); and income-support or BL maintenance (mezonot) recipients who started before 2003 with no 6-month break (up to 70%). Non-residential and agricultural rows (new industry, Reg. 14; shmita land, Reg. 3d; Chapter Hey2 holders' business premises, Reg. 14z) are in `references/arnona-discounts-guide.md`.

**Regulation 2(8) income table** (average monthly GROSS income of everyone living in the flat, NIS). Each cell is the UPPER bound of its band, shown as fiscal 2026 / fiscal 2027:

| Persons | 90% band | 70% band | 50% band | 30% band |
|---------|----------|----------|----------|----------|
| 1 | 3,513 / 3,623 | 4,295 / 4,430 | 5,076 / 5,235 | 5,857 / 6,041 |
| 2 | 5,621 / 5,798 | 6,872 / 7,088 | 8,122 / 8,377 | 9,372 / 9,666 |
| 3 | 7,449 / 7,683 | 9,106 / 9,392 | 10,762 / 11,100 | 12,417 / 12,807 |
| 4 | 8,996 / 9,278 | 10,996 / 11,341 | 12,995 / 13,403 | 14,994 / 15,465 |
| 5 | 10,541 / 10,872 | 12,886 / 13,291 | 15,229 / 15,707 | 17,572 / 18,124 |
| 6 | 11,948 / 12,323 | 14,604 / 15,063 | 17,259 / 17,801 | 19,914 / 20,539 |
| 7 | 13,352 / 13,771 | 16,322 / 16,835 | 19,290 / 19,896 | 22,257 / 22,956 |
| 8 | 14,618 / 15,077 | 17,868 / 18,429 | 21,117 / 21,780 | 24,366 / 25,131 |
| 9 | 15,743 / 16,237 | 19,243 / 19,847 | 22,742 / 23,456 | 26,240 / 27,064 |

A household falls in the first band whose upper bound its income does not exceed. For 10 people or more, add per additional person to the 9-person figure: 1,125 / 1,374 / 1,624 / 1,874 for fiscal 2026, and 1,160 / 1,417 / 1,675 / 1,933 for fiscal 2027.

- **Which income.** Fiscal 2026 tests calendar-2025 income; fiscal 2027 (published 28.7.2026, in force 1 January 2027) tests calendar-2026 income. For an employee it is the 12-month average; the 2025 temporary option of a 3-month average was not extended. Maintenance received counts as income; child allowances and some other BL benefits do not (full list in the discounts guide). The thresholds are per household by headcount, not per person.
- **The table updates every 1 January** by the change in the minimum wage known on 20 May of the preceding year, published in Reshumot. Re-read it each year.
- **Timing.** Each council sets its own application deadline (Reg. 21), usually early in the year; Haifa's for 2026 was 31 March, or 90 days from the charge or from being recognised as eligible, and later only for special reasons. A holder who missed it should still apply now with reasons, and apply for 2027 in January against the 2027 table. A part-year holder gets the discount pro rata by months (Reg. 17(c)).

Run the calculator with the discount and, for the income test, the household data:

```bash
python scripts/arnona-calculator.py --municipality haifa --area 90 --zone ב --type 2 --discount low-income --household-income 9000 --household-size 3 --fiscal-year 2027
```

**Important rules about discounts:**
- Discounts apply only to a flat used solely for residence. Read the area cap off the row you are using, not off a blanket 100 sqm.
- Area above the discount cap is charged at the full rate.
- Only one discount applies. Where several fit, the resident gets the single highest one, and no discount goes to a second holder of the same property (Reg. 17(a)). A holder of two or more properties gets the discount on one only (Reg. 17(b)).
- A discount is conditional on clearing the year's arnona balance, whether in one advance payment, by standing order, or under another payment arrangement the municipality accepts (Reg. 20). An unpaid balance at 31 December voids the discount for that year and it is added back to the debt (Reg. 16). Regulations 16, 17(b) and 20 do not apply to the Reg. 3c1 evacuation discount, and Regulations 16, 17(b), 18, 20 and 21 do not apply to the Chapter Hey2 entitlements.
- Rows 2(1), 2(2) and 2(7) need no application form (Reg. 4(a)); a holder who was missed, or given the wrong rate, may still apply (Reg. 4(b)). The senior entitlement renews automatically. Most other discounts must be re-applied for each year.

### Step 4: Draft an Objection (hasaga)

An objection is limited to four grounds, set by section 3(a) of the Local Authorities (Arnona Objection) Law 5736-1976: (1) the property is not in the zone stated in the payment notice; (2) the notice has an error in the property's type, size or use; (3) the objector is not the holder; (4) a controlling-shareholder ground for a company's business premises. Typical cases: a wrong measured area, a wrong zone or building type, a residential flat billed as commercial, or a bill that still names a tenant who left.

**The process:**
- File in writing with the **arnona manager** (menahel ha-arnona) within **90 days of receiving the payment notice** (s.3(a)).
- The manager must answer within **60 days**. **No answer in time means the objection is deemed accepted**, unless the appeals committee extended the period by up to 30 days (s.4).
- Against the manager's answer: an appeal (erer) to the appeals committee (vaadat erer) within **30 days** (s.6(a)), then to the Administrative Court (s.6(b)).
- **Filing does not suspend payment.** Pay the bill while the objection is pending and claim the refund in writing; an overpayment not refunded within 30 days of a written demand carries linkage plus 0.5% a month (Interest Law s.6(a)). An unpaid balance at 31 December voids that year's discount (Reg. 16), and arrears carry linkage and interest.
- Last year's area cannot be attacked by an objection once the 90 days passed. Going forward, an area figure carries over unless an error is found that is not just a different calculation method (2007 regs, reg. 3(b)).
- **A refused discount is not an objection matter.** The four grounds above are a closed list. Ask the body that refused (the treasurer or the discounts committee) for its written reasons, and take advice on the administrative route if it stands.

Include in the letter: the address and account number (mispar heshbon), the date the payment notice was received, the specific s.3(a) ground, the evidence (surveyor report, photos, lease, the city's own measurement rules), and the remedy (reclassification, area correction, refund).

**Empty property.** A different route, not an objection: an empty building nobody uses carries a discount ladder the council may set within, cumulative over the period one person owns the building and counted from 1 March 2005: up to 100% for the first 6 months, up to 66.66% for months 7 to 12, and up to 50% for months 13 to 36 (Reg. 13(a)). Any continuous vacancy shorter than 30 days does not count, and the holder must notify the municipality 7 days before the property is used again. Separately, the FIRST owner of a NEW empty building never used since completion may get up to 100% for up to twelve months (Reg. 12). A building destroyed or damaged so it cannot be lived in, and empty, is exempt for three years from written notice to the municipality and then charged the minimum rate for five more years (Municipalities Ordinance s.330).

### Step 5: Payment Options and Arrears

1. **Bimonthly or monthly**: payment dates are set by each council (Haifa 2026: the 1st of every odd month, or 12 monthly standing-order payments). Arnona paid under a payment arrangement is CPI-linked from the November index, which paying the year up front avoids (Interest Law s.1, s.4(a)).
2. **Early payment or standing order**: a council may give up to 2% for paying by standing order (Reg. 3) and may set an early-payment discount; Haifa 2026 gave 2% for paying the year in full by 31.12.2025 and 1% by 31.1.2026.
3. **Arrears**: governed by the Local Authorities (Interest and Linkage on Compulsory Payments) Law 5740-1980. A payment more than 30 days late carries arrears charges, linked interest defined in that Law at 0.5% a month unless the ministers set another rate (s.1, s.2). Payments go to the oldest debt first (s.3). A council may set an arnona instalment plan of up to one year from the charge, each instalment CPI-linked; two missed instalments cancel it (s.4(a), s.4(e)). The two-year plans in s.4(b) cover only the levies listed in the Law's Schedule, not arnona.
4. **Old debts**: by case law a municipality may not collect arnona debt more than 7 years old where it took no collection step in that time, unless it did not know about the ground for collecting.

### Step 6: Provide Municipality Contact Information

Direct the user to the arnona department through the municipality's own website (for example tel-aviv.gov.il, jerusalem.muni.il, haifa.muni.il, beer-sheva.muni.il), where the current contact channels and online forms are listed. Do not quote an email address or phone number from memory.

Communications with the arnona department should be in writing, by registered mail (doar rashum) or the municipality's online portal, so the filing date can be proved.

## Examples

### Example 1: Calculate Arnona for a Tel Aviv Apartment

User says: "I have an 85 sqm apartment in Tel Aviv, zone 2. How much arnona should I pay?"

Actions:
1. Ask for the building type on the bill. Zone 2 alone spans six building types.
2. The user reads type ב+ג. Run: `python scripts/arnona-calculator.py --municipality tel-aviv --area 85 --zone 2 --type ב+ג`
3. Fiscal-2026 rate for a zone-2 flat of up to 140 sqm, type ב+ג: 72.89 NIS/sqm/year. 85 x 72.89 = 6,195.65 NIS/year, about 1,032.61 NIS per two-month bill.

Result: about 6,196 NIS for 2026. At the 3.05% national update, about 6,385 NIS for 2027, unless Tel Aviv obtains an above-formula increase. The bill is authoritative.

### Example 2: Check Oleh Chadash Discount Eligibility

User says: "I made aliyah 6 months ago and I'm renting a 70 sqm apartment in Jerusalem, zone bet. What discounts can I get?"

Actions:
1. Identify the user as an oleh chadash within the 24-month window (6 months after aliyah), and confirm they are the holder on the bill.
2. Ask the building type on the bill; for an ordinary stone or concrete building it is type 2.
3. Run: `python scripts/arnona-calculator.py --municipality jerusalem --area 70 --zone ב --type 2 --discount oleh`
4. Base: 70 sqm x 86.34 = 6,043.80 NIS/year. Up to 90% on up to 100 sqm leaves 604.38 NIS for a full discounted year.

Result: the user may receive up to 90% on up to 100 sqm for 12 months chosen within the first 24 after aliyah (the 12 months need not be consecutive). The 90% is a ceiling Jerusalem chooses within. If they lived in another municipality first, they should bring confirmation that they did not receive the oleh discount there. Apply with the oleh certificate and lease at the arnona department or online.

### Example 3: Draft an Objection for Incorrect Area Measurement

User says: "My arnona bill says my apartment is 95 sqm but I measured it and it's only 82 sqm. I'm in Haifa, zone bet, a regular building. How do I appeal?"

Actions:
1. Ground: an error in the property's size, section 3(a)(2) of the Local Authorities (Arnona Objection) Law 5736-1976.
2. Check the measurement method first. Haifa measures wall to wall INCLUDING balconies, even unroofed ones, internal stairs and galleries 1.80 m high or more; a standard shelter is excluded. A tape measure of the rooms alone will under-count.
3. Impact: both 95 and 82 sqm fall in Haifa's 76 to 100 sqm band for the regular class (78.79 NIS/sqm in zone ב'), so the overcharge is 13 x 78.79 = about 1,024 NIS/year. Had the true area been 75 sqm or less, the whole flat would drop to the lower band, so check band edges.
4. Confirm the payment notice arrived within the last 90 days.

Result: the agent drafts a Hebrew objection to the Haifa arnona manager stating the recorded and measured areas under Haifa's own measurement rules, citing s.3(a)(2), attaching a surveyor's report, and asking for correction and refund. The user keeps paying the bill meanwhile, sends by registered mail, and notes that no answer within 60 days means the objection is deemed accepted.

## Bundled Resources

### Scripts
- `scripts/arnona-calculator.py` -- residential arnona from the fiscal-2026 tzav of eleven cities, keyed on zone and building type, any other rate via `--rate-per-sqm`, every national discount row, and the income-test band for fiscal 2026 or 2027. Run: `python scripts/arnona-calculator.py --help`

### References
- `references/arnona-rates-guide.md` -- how each city keys its residential rates, each city's range, the national update, and area-measurement rules. Consult before quoting any rate.
- `references/arnona-discounts-guide.md` -- every discount category, eligibility details, documents, and the income-test rules. Consult when checking a discount.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Kolzchut: Arnona | https://www.kolzchut.org.il/he/ארנונה | Plain-language guide to arnona obligations, discounts, and appeal rights |
| Arrangements in the State Economy Regulations (Arnona Discount), 5753-1993, consolidated | https://he.wikisource.org/wiki/תקנות_הסדרים_במשק_המדינה_(הנחה_מארנונה) | Every discount paragraph and the empty-building ladder. Its First Schedule shows the CURRENT published table, which since August 2026 is the fiscal-2027 one |
| Senior Citizens Law 5750-1989, consolidated | https://he.wikisource.org/wiki/חוק_האזרחים_הותיקים | The s.9 senior arnona entitlement, its income test, and the automatic-renewal rules |
| Local Authorities (Arnona Objection) Law 5736-1976, consolidated | https://he.wikisource.org/wiki/חוק_הרשויות_המקומיות_(ערר_על_קביעת_ארנונה_כללית) | The four objection grounds, the 90 / 60 / 30 day clock, deemed acceptance |
| Interior Ministry arnona page | https://www.gov.il/he/pages/tax | The annual national update coefficient |
| Tel Aviv Municipality | https://www.tel-aviv.gov.il/ | Tel Aviv tzav arnona, payment, discount applications |

## Gotchas
- Every city keys its residential rate on zone AND a building type or size class. Agents quote a single "zone 2 rate" that does not exist. Ask for the type on the bill, or show the range.
- Arnona discounts (hanacha) have strict eligibility windows and most require annual renewal. Agents may suggest discounts the user no longer qualifies for or that have expired.
- Property classification (residential vs. commercial) significantly affects arnona rates. Agents may misclassify home offices, which are usually still taxed at residential rates unless formally reclassified.
- Objection deadlines run 90 days from receipt of the payment notice, and filing does not suspend payment. Agents may draft an objection after the deadline, or tell the user to withhold payment, which voids that year's discount.
- Most rows in the discount regulation are CEILINGS a council chooses within, not amounts owed. Say "up to", and name whether the row is discretionary or an entitlement.
- There is NO national student discount and NO national large-family discount. Agents fill that gap with plausible round numbers, typically 50% and 30%. Neither has a paragraph behind it.
- Wikisource's consolidated First Schedule now shows the fiscal-2027 table under a header naming the 2026 income year. Agents read it as the 2026 table. Fiscal 2026 still uses the 3,513 row.

## Known limitations

- Residential rates are carried for eleven cities, fiscal 2026 only. Modiin, the other authorities, Haifa's Kiryat Haim and all non-residential tariffs need `--rate-per-sqm` from the tzav or bill.
- Where a city's type depends on facts the script cannot see (year of completion, elevator, building quality), it lists the candidate rows instead of choosing.
- The skill states national ceilings, not where each council sits within them. Each city's tzav carries its own discount chapter.

## Troubleshooting

### Error: "has no built-in table; pass --rate-per-sqm"
Cause: the authority, or the non-residential use, is not tabulated.
Solution: take the rate per sqm from that authority's tzav arnona for the year, or divide the annual charge on the bill by the charged area, and pass it with `--rate-per-sqm`. Search "[authority name] צו ארנונה [year]" for the tzav.

### Error: "Discount category not recognized"
Cause: the discount key does not match one of the calculator's keys.
Solution: run `python scripts/arnona-calculator.py --list-discounts`, which groups every key into entitlements and ceilings with the regulation behind each. `student` and `large-family` do not exist because no national rate exists behind them; for a large household use `low-income`.

### Error: "Zone not valid" or "Type has no rate"
Cause: each city names its zones and types differently (numbers, Hebrew letters, size classes).
Solution: run `--list-types <city>` and copy the zone and type exactly as printed on the bill. Hebrew letters can also be passed as A, B, G, D.

### Error: "Cannot determine objection deadline"
Cause: the 90 days run from receipt of the payment notice, and the receipt date is unknown.
Solution: ask when the bill arrived. If the 90 days passed, the area or classification for that year can no longer be objected to; correct it going forward and keep proof of every filing date.
