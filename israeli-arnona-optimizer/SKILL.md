---
name: israeli-arnona-optimizer
description: Calculate municipal property tax (arnona) for Israeli properties, check discount eligibility, and draft appeal letters to arnona committees. Use when a user needs to estimate arnona payments by municipality, zone, and property usage type, verify eligibility for discounts (olim, soldiers, elderly, disabled, low income, students, single parents), or prepare formal appeals with legal references. Covers all major Israeli municipalities including Tel Aviv, Jerusalem, Haifa, and Beer Sheva. Do NOT use for income tax (mas hachnasa), VAT (maam), or national insurance (bituach leumi) calculations, which fall under separate Israeli tax authorities.
license: MIT
allowed-tools: Bash(python:*) Read Edit Write WebFetch
compatibility: Requires Python 3.10+ for calculator script
---

# Israeli Arnona Optimizer

## Legal notice

This is a free information tool operated by an AI model. It explains the tax rules and helps you organise your own figures. All of its outputs are produced automatically by an AI model, with no involvement, review, or approval by a tax adviser or accountant. The output is not a tax opinion, not a return prepared by a licensed representative, and not professional advice, but a general calculation and explanation only: it does not examine the full extent of your income or your complete documents. An AI model may err, omit data, or present a wrong conclusion.

Any form or text this tool produces is an automatic draft for your personal preparation only, and is not a filed return. Responsibility for reporting and for paying the tax is yours, the binding computation is the Tax Authority's, and representation before the Tax Authority is reserved to those permitted by law. This tool is not a substitute for advice that takes account of the particular circumstances and needs of each person. Consult a tax adviser or accountant before filing or paying. All use of its output is the user's sole responsibility.


## Instructions

### Step 1: Gather Property Details

Before performing any arnona calculation, collect the following information from the user:

1. **Municipality** (iriya): Which city or local council the property is located in (e.g., Tel Aviv-Yafo, Jerusalem, Haifa, Beer Sheva, Netanya, Rishon LeZion).
2. **Property area**: Total area in square meters (sqm). Distinguish between main area and auxiliary areas (storage rooms, balconies, parking) as these are billed at different rates.
3. **Zone classification**: The arnona zone within the municipality. Each city divides into zones (azor) with different rate tiers. Ask the user for their zone or help them determine it from their address.
4. **Usage type**: Residential (megurim), commercial (mishari), office (misrad), industrial (taasia), or other special uses. Rates differ significantly by usage.
5. **Billing period**: Arnona is billed bimonthly (every two months) in most municipalities. The annual rate is divided into 6 payment periods.

### Step 2: Calculate Base Arnona

Use the arnona calculator script to compute the base annual arnona:

```bash
python scripts/arnona-calculator.py --municipality "tel-aviv" --area 80 --zone 2 --usage residential
```

The calculator applies the correct rate per sqm based on the municipality's published rate tables. Key rate structures:

- **Tel Aviv-Yafo**: Rates range from approximately 75 to 130 NIS/sqm/year for residential depending on zone (zones 1-4). Commercial rates are 2-4x higher.
- **Jerusalem**: Rates range from approximately 55 to 95 NIS/sqm/year for residential. Divided into 5 zones using Hebrew letters alef through heh (א through ה).
- **Haifa**: Rates range from approximately 50 to 90 NIS/sqm/year for residential. Lower overall compared to Tel Aviv.
- **Beer Sheva**: Rates range from approximately 35 to 60 NIS/sqm/year for residential. Among the lowest for major cities.

Consult `references/arnona-rates-guide.md` for detailed rate tables and zone classification rules.

### Step 3: Check Discount Eligibility

Israeli arnona discounts come from ONE national instrument, the Arrangements in the State Economy Regulations (Arnona Discount), 5753-1993, plus municipal bylaws on top. Two things decide how you phrase an answer:

- **Ceiling vs entitlement.** Almost every row in Regulation 2 opens with "a council MAY set a discount not exceeding X percent". That X is a **ceiling the municipality chooses within**, not an amount the resident is owed. Chapter Hey2 (Regulations 14e, 14e1) and Regulations 3c and 3c1 are the opposite: the resident "is entitled", and the municipality has no discretion. Never present a Regulation 2 ceiling as an entitlement.
- **Area caps differ per row.** 100 sqm, 70 sqm (90 sqm if more than four family members live with the holder), or no cap at all. Applying a blanket 100 sqm to every row overstates several discounts and understates others.

**A. Entitlements (mandatory, no municipal discretion)**

| Who | Discount | Area cap | Source |
|-----|----------|----------|--------|
| Conscript soldier, national-service volunteer, civilian-security service; and up to 4 months after discharge | 100% | 70 sqm, 90 sqm if the holder's family living with them exceeds four | Reg. 14e(1), cap in Reg. 14f |
| Parent supported by the soldier before service, with no other livelihood | 100% | same | Reg. 14e(1)(b) |
| Civilian-social service, 30 weekly hours over two years | three quarters | same | Reg. 14e(1a) |
| IDF-disabled, Nazi-war disabled, police and prison-service disabled, bereaved family of a fallen serviceperson, hostile-action casualty | two thirds | same | Reg. 14e(2) |
| Civilian service split track, or civilian-social service 20 weekly hours over three years | 50% | same | Reg. 14e(3) |
| Person determined to be a hostage or missing person (Hostages and Missing Persons Law 5784-2023) | 100% | none | Reg. 14e1 |
| Senior citizen whose total income from every source is within the average wage; where more than one senior lives in the flat, the combined income of all residents must be within 150% of the average wage | 30% | 100 sqm | Senior Citizens Law 5750-1989, s.9(b) and s.9(c)(4) |
| The same senior, receiving an income-support benefit under the Income Support Law 5741-1980 | 100% | 100 sqm | Senior Citizens Law, s.9(b) |
| Holder in Sderot, the Gaza-envelope localities, or within 7 km of the Gaza perimeter fence | 45% residential, 39% other property | none | Reg. 3c, fiscal years 2015 to 2026 |
| Holder in an evacuated locality listed under the Iron Swords deferral law | 100% from 7 October 2023 to the end of the evacuation period | none | Reg. 3c1 |

The senior entitlement runs for one flat only and goes to one senior only, even where several qualify in the same flat. Once granted it renews automatically; a senior on the 30% rate who is under 70 gets automatic renewal for three calendar years or until turning 70, whichever comes first, and must re-apply after that. Regulation 2(a)(1) below is the parallel DISCRETIONARY route, which is why the same person can appear in both tables at different rates. Give the resident the higher one, since only one discount applies.

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
| Single parent; or a single parent of a co-resident child under 21 in conscript or national service | 20% | none stated | 2(10) |
| Parent of a child, including a foster child, entitled to the disabled-child benefit; or over 18 with a disability benefit preceded by the disabled-child benefit | 33% | 100 sqm | 2(11) |
| Released captive entitled to payment under the Payments to Released Captives Law 5765-2005 | 20% | none stated | 2(12) |
| Active reserve soldier holding a valid active-reservist certificate | 5% | none stated | Reg. 3f |
| Active reserve COMMANDER in a command role holding a valid certificate | 25% | 100 sqm | Reg. 3g |
| Needy holder (nazak): exceptional medical expenses, or an event causing a serious unforeseen worsening of their material position | 70%, granted by the discounts committee | none stated | Reg. 7 |
| Senior business owner: sole business up to 75 sqm, aged 65 (60 for a woman), turnover up to 240,000 NIS index-linked, already receiving a Reg. 2(8) discount at home | the same rate given on the home | first 40 sqm of the business | Reg. 14c |

**No national row exists for these.** The regulation has NO student discount and NO large-family discount. A municipality may still grant one under its own bylaw, so check the local table, but there is no national rate to quote and none should be assumed. A large family's national route is the Regulation 2(8) income test, whose thresholds rise with household size.

**Non-residential and agricultural rows.** Three further routes sit outside the residential tables above and are easy to miss when the property is not a flat: a new industrial plant gets a ceiling from up to 10% to up to 75% depending on its year of holding and the local unemployment rate published by the Employment Service (Reg. 14); agricultural land left unworked for shmita observance for at least eight months of the fiscal year, with agricultural use proven in two of the three preceding years, gets 90% to 100% (Reg. 3d); and a holder of non-residential premises who meets the Chapter Hey2 conditions can claim the same rate there if they owed no income-tax advance that year and the assessing officer certified it (Reg. 14z). Details in `references/arnona-discounts-guide.md`.

**Regulation 2(8) income table, fiscal year 2026** (average monthly gross household income, NIS; the columns give the 90% / 70% / 50% / 30% ceilings):

| Persons | up to 90% | up to 70% | up to 50% | up to 30% |
|---------|-----------|-----------|-----------|-----------|
| 1 | up to 3,623 | 3,623 to 4,430 | 4,430 to 5,235 | 5,235 to 6,041 |
| 2 | up to 5,798 | 5,798 to 7,088 | 7,088 to 8,377 | 8,377 to 9,666 |
| 3 | up to 7,683 | 7,683 to 9,392 | 9,392 to 11,100 | 11,100 to 12,807 |
| 4 | up to 9,278 | 9,278 to 11,341 | 11,341 to 13,403 | 13,403 to 15,465 |
| 5 | up to 10,872 | 10,872 to 13,291 | 13,291 to 15,707 | 15,707 to 18,124 |
| 6 | up to 12,323 | 12,323 to 15,063 | 15,063 to 17,801 | 17,801 to 20,539 |
| 7 | up to 13,771 | 13,771 to 16,835 | 16,835 to 19,896 | 19,896 to 22,956 |
| 8 | up to 15,077 | 15,077 to 18,429 | 18,429 to 21,780 | 21,780 to 25,131 |
| 9 | up to 16,237 | 16,237 to 19,847 | 19,847 to 23,456 | 23,456 to 27,064 |

For 10 people or more, take the 9-person figure in the same column and add per additional person: 1,160 in the 90% column, 1,417 in the 70% column, 1,675 in the 50% column, 1,933 in the 30% column. These amounts update every 1 January by the change in the minimum wage known on 20 May of the preceding fiscal year, so re-read the First Schedule each year rather than carrying these figures forward.

Run the calculator with discount flags:

```bash
python scripts/arnona-calculator.py --municipality "tel-aviv" --area 80 --zone 2 --usage residential --discount oleh --discount-months 8
```

Consult `references/arnona-discounts-guide.md` for the full list of discount categories, required documentation, and municipality-specific variations.

**Important rules about discounts:**
- Discounts apply only to a flat used solely for residence. Read the area cap off the row you are using, not off a blanket 100 sqm.
- Area above the discount cap is charged at the full rate.
- Only one discount applies. Where several fit, the resident gets the single highest one, and no discount goes to a second holder of the same property (Reg. 17(a)). A holder of two or more properties gets the discount on one only (Reg. 17(b)), and a part-year holder gets it pro rata by months held (Reg. 17(c)).
- A discount is conditional on clearing the year's arnona balance, whether in one advance payment, by standing order, or under another payment arrangement the municipality accepts (Reg. 20). An unpaid balance at 31 December voids the discount for that year and it is added back to the debt (Reg. 16). Regulations 16, 17(b) and 20 do not apply to the Reg. 3c1 evacuation discount, and Regulations 16, 17(b), 18, 20 and 21 do not apply to the Chapter Hey2 entitlements.
- Discounts must be renewed annually in most municipalities.
- The application deadline is set by each council (Reg. 21), typically January to March.

**Income-test reform for 2026 (effective 1 January 2026):** the income-tested discounts (the low-income table, and the income tests behind other bands) were reformed. Eligibility is now computed on the applicant's **12-month average income only** (the earlier 3-month option was removed), against a **per-capita threshold table indexed to the minimum wage and household size**, and certain Bituach Leumi benefits (child allowances, old-age/survivors pensions) are excluded from the counted income. The reform widened eligibility (roughly 740,000 to 840,000 households) while keeping the top band at 90%. The operative thresholds are the First Schedule table reproduced above, which is the regulation's own text for fiscal year 2026. They are revised every 1 January, so re-read the Schedule at the start of each year rather than carrying the figures forward.

### Step 4: Draft Appeal Letters

If the user believes their arnona assessment is incorrect, help them draft an appeal letter (hasaga) to the municipality's arnona committee (vaada le-hashagot). Common grounds for appeal:

1. **Incorrect area measurement**: The municipality's recorded area differs from the actual property size. Request a surveyor re-measurement.
2. **Wrong zone classification**: The property should be classified in a lower-rate zone based on its location.
3. **Incorrect usage classification**: The property is classified as commercial but is actually used for residential purposes (or vice versa).
4. **Structural issues**: Parts of the property are uninhabitable (e.g., under renovation, flood damage, structural defects).
5. **Empty/vacant property**: An empty building nobody uses carries a discount ladder the council may set within, cumulative over the period one person owns the building and counted from the regulation's commencement on 1 March 2005: up to 100% for the first 6 months, up to 66.66% for months 7 to 12, and up to 50% for months 13 to 36 (Reg. 13(a)). Any continuous vacancy shorter than 30 days does not count toward the cumulative period, and the holder must notify the municipality 7 days before the property is used again or the last stretch of discount can be cancelled. Separately, the FIRST owner of a NEW empty building that has never been used since completion may get up to 100% for up to twelve months (Reg. 12). This is a separate route, not an extension of the Reg. 13 ladder.

**Appeal process:**
- File the appeal (hasaga) within 90 days of receiving the arnona bill.
- The arnona manager (menahel ha-arnona) must respond within 60 days.
- If dissatisfied with the manager's decision, appeal to the arnona appeals committee (vaada le-erurim) within 30 days.
- Further appeals go to the Administrative Court (Beit Mishpat le-Inyanim Minhaliyim).

Include these elements in the appeal letter:
- Full property address and account number (mispar heshbon)
- The specific ground for appeal (with legal reference to the Arnona Regulations)
- Supporting evidence (surveyor report, photos, lease agreement)
- The requested remedy (reclassification, area correction, discount application)

### Step 5: Analyze Payment Options

Help the user understand their payment options:

1. **Bimonthly payments**: Standard 6 payments per year. No additional fees.
2. **Annual lump sum**: Some municipalities offer a 1-2% discount for paying the full year upfront (usually by January 31).
3. **Direct debit (horaat keva)**: Automatic bank debit. Some municipalities offer a small discount.
4. **Payment plan for arrears**: If the user has arnona debt, municipalities typically offer payment plans. Interest on late payments is set by the Local Authorities Ordinance.

### Step 6: Provide Municipality Contact Information

Direct the user to the relevant arnona department. Note that municipality contact details should be verified on official websites as phone numbers and contact information may change:

- **Tel Aviv**: tel-aviv.gov.il, arnona@mail.tel-aviv.gov.il
- **Jerusalem**: jerusalem.muni.il, arnona@jerusalem.muni.il
- **Haifa**: haifa.muni.il, arnona@haifa.muni.il
- **Beer Sheva**: beer-sheva.muni.il

Remind the user that all communications with the arnona department should be documented in writing and sent via registered mail (doar rashum) or through the municipality's online portal.

## Examples

### Example 1: Calculate Arnona for a Tel Aviv Apartment

User says: "I have an 85 sqm apartment in Tel Aviv, zone 2. How much arnona should I pay?"

Actions:
1. Run the arnona calculator: `python scripts/arnona-calculator.py --municipality "tel-aviv" --area 85 --zone 2 --usage residential`
2. Review the output showing the per-sqm rate for Tel Aviv zone 2 residential (approximately 95 NIS/sqm/year)
3. Calculate the annual total: 85 sqm x 95 NIS = 8,075 NIS/year
4. Calculate the bimonthly payment: 8,075 / 6 = approximately 1,346 NIS per billing period

Result: The estimated annual arnona is approximately 8,075 NIS (about 1,346 NIS bimonthly). The agent explains that rates are updated annually by the municipality and may vary slightly from these estimates. The user is advised to verify against their actual arnona bill.

### Example 2: Check Oleh Chadash Discount Eligibility

User says: "I made aliyah 6 months ago and I'm renting a 70 sqm apartment in Jerusalem, zone bet. What discounts can I get?"

Actions:
1. Identify the user as an oleh chadash still within the 24-month eligibility window (6 months after aliyah)
2. Consult `references/arnona-discounts-guide.md` for oleh discount rules
3. Run the calculator with the oleh discount: `python scripts/arnona-calculator.py --municipality "jerusalem" --area 70 --zone B --usage residential --discount oleh --discount-months 12`
4. Calculate base arnona: 70 sqm x approximately 72 NIS/sqm = 5,040 NIS/year
5. Apply 90% on up to 100 sqm: a full 12 discounted months brings the annual charge down to about 504 NIS (saving ~4,536 NIS)

Result: As an oleh chadash, the user is eligible for a 90% arnona discount on up to 100 sqm for 12 months, which they may use any time within the first 24 months after aliyah (the 12 months need not be the first consecutive 12). For a 70 sqm apartment in Jerusalem zone bet, the base annual arnona is approximately 5,040 NIS; with the 90% discount applied across 12 months the user pays only about 504 NIS (roughly 84 NIS bimonthly). To apply: bring the oleh certificate (teudat oleh) and lease agreement to the Jerusalem municipality arnona department or apply online at jerusalem.muni.il.

### Example 3: Draft an Appeal for Incorrect Area Measurement

User says: "My arnona bill says my apartment is 95 sqm but I measured it and it's only 82 sqm. I'm in Haifa. How do I appeal?"

Actions:
1. Identify the ground for appeal: incorrect area measurement (13 sqm discrepancy)
2. Calculate the financial impact: 13 sqm x approximately 65 NIS/sqm = approximately 845 NIS/year overcharge
3. Draft an appeal letter referencing Section 3(a) of the Arnona Regulations (Takanot HaSdrei Nisui v'Givia shel Arnona Klalit)
4. Include instructions for obtaining a professional surveyor measurement
5. Provide the Haifa arnona committee address and filing deadline

Result: The agent drafts a formal appeal letter in Hebrew addressed to the Haifa arnona manager (menahel arnona, iriyat Haifa), stating the discrepancy between the recorded area (95 sqm) and actual area (82 sqm), referencing the relevant regulation, requesting a re-measurement by a municipal surveyor, and asking for retroactive correction and refund. The user is advised to attach a private surveyor's measurement report and send via registered mail within 90 days of the bill date.

## Bundled Resources

### Scripts
- `scripts/arnona-calculator.py` -- Calculate arnona payments by municipality, area, zone, and usage type, with optional discount application. Run: `python scripts/arnona-calculator.py --help`

### References
- `references/arnona-rates-guide.md` -- Comprehensive guide to arnona rate structures, zone classifications, usage types, and billing cycles across Israeli municipalities. Consult when determining the correct rate for a specific property.
- `references/arnona-discounts-guide.md` -- Complete reference for all arnona discount categories, eligibility criteria, required documentation, and municipality-specific variations. Consult when checking if a user qualifies for arnona discounts.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Kolzchut: Arnona | https://www.kolzchut.org.il/he/ארנונה | Plain-language guide to arnona obligations, discounts, and appeal rights |
| Arrangements in the State Economy Regulations (Arnona Discount), 5753-1993, consolidated | https://he.wikisource.org/wiki/תקנות_הסדרים_במשק_המדינה_(הנחה_מארנונה) | The authoritative text of every discount paragraph, the First Schedule income table, and the empty-building ladder. Read this before quoting any rate |
| Senior Citizens Law 5750-1989, consolidated | https://he.wikisource.org/wiki/חוק_האזרחים_הותיקים | The s.9 senior arnona entitlement, its income test, and the automatic-renewal rules |
| Bituach Leumi: Disability Benefits | https://www.btl.gov.il/benefits/Disability/Pages/default.aspx | Source documents for the disability percentages used in arnona discount eligibility |
| Tel Aviv Municipality | https://www.tel-aviv.gov.il/ | Tel Aviv tzav arnona, current rates, online payment, appeals |
| Jerusalem Municipality | https://www.jerusalem.muni.il/ | Jerusalem alef-heh zone rates, payment, discount applications |

## Gotchas
- Arnona rates vary dramatically between municipalities. Agents may use Tel Aviv rates for Haifa properties or vice versa. Always verify rates against the specific municipality (iriya or mo'atza).
- Arnona discounts (hanacha) have strict eligibility windows and require annual renewal. Agents may suggest discounts the user no longer qualifies for or that have expired.
- Property classification (residential vs. commercial) significantly affects arnona rates. Agents may misclassify home offices, which in Israel are usually still taxed at residential rates unless formally rezoned.
- Arnona appeal deadlines are typically 90 days from the annual bill date. Agents may draft appeals after the deadline has passed, making them void.
- Most rows in the discount regulation are CEILINGS a council chooses within, not amounts owed. Telling a resident "you get 40%" when the regulation says "up to 40%" sets them up for an argument with a clerk they cannot win. Say "up to", and name whether the row is discretionary or an entitlement.
- There is NO national student discount and NO national large-family discount. Agents fill that gap with plausible round numbers, typically 50% and 30%. Neither has a paragraph behind it. If the user asks, say the national regulation is silent and point them at the municipal bylaw table.

## Troubleshooting

### Error: "Municipality not found in rate tables"
Cause: The arnona calculator does not have rate data for the specified municipality. Smaller local councils (moatzot mekomiyot) and regional councils (moatzot azeriyot) have their own rate tables that may not be included.
Solution: Check the municipality name spelling. Use the `--list-municipalities` flag to see all supported municipalities. For unsupported municipalities, consult the municipality's website directly for their published arnona rate ordinance (tzav arnona). You can also try searching for "[municipality name] tzav arnona [year]" to find the official rate publication.

### Error: "Discount category not recognized"
Cause: The discount type specified does not match one of the supported discount categories in the calculator.
Solution: Run `python scripts/arnona-calculator.py --list-discounts`, which groups every category into entitlements and council-set ceilings and prints the regulation behind each one. Common mistakes include using "immigrant" instead of "oleh". Two keys were REMOVED in v1.5.0 because no national rate exists behind them: `student` and `large-family`. The regulation has no paragraph for either, so the calculator will not produce a number; read the municipality's own bylaw table, and for a large household use `low-income`, whose thresholds already rise with household size. `bereaved` and `holocaust-survivor` were renamed to `disabled-veteran` (Reg. 14e(2), a two-thirds entitlement covering bereaved families, hostile-action casualties, police and prison-service disabled) and `persecution-pension` (Reg. 2(a)(4), a 66% ceiling on 70 sqm).

### Error: "Zone not valid for this municipality"
Cause: Each municipality uses its own zone classification system. Tel Aviv uses numbered zones (1-4), Jerusalem uses Hebrew-letter zones alef through heh (א-ה), and other cities have their own systems.
Solution: Check the zone classification for your specific municipality. If unsure of your zone, look at a previous arnona bill (it shows the zone), or contact the municipality's arnona department. The `references/arnona-rates-guide.md` file lists the zone systems for each supported municipality.

### Error: "Cannot determine appeal deadline"
Cause: The appeal filing deadline depends on when the arnona bill was received, and the system cannot verify the receipt date.
Solution: The general rule is 90 days from the date of the arnona bill for filing an appeal (hasaga) to the arnona manager. After receiving the manager's decision, the user has 30 days to appeal to the appeals committee (vaada le-erurim). Always recommend filing as early as possible and keeping proof of the filing date (registered mail receipt or online submission confirmation).