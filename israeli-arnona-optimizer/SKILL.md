---
name: israeli-arnona-optimizer
description: Calculate municipal property tax (arnona) for Israeli properties, check discount eligibility, and draft appeal letters to arnona committees. Use when a user needs to estimate arnona payments by municipality, zone, and property usage type, verify eligibility for discounts (olim, soldiers, elderly, disabled, low income, students, single parents), or prepare formal appeals with legal references. Covers all major Israeli municipalities including Tel Aviv, Jerusalem, Haifa, and Beer Sheva. Do NOT use for income tax (mas hachnasa), VAT (maam), or national insurance (bituach leumi) calculations, which fall under separate Israeli tax authorities.
license: MIT
allowed-tools: Bash(python:*) Read Edit Write WebFetch
compatibility: Requires Python 3.10+ for calculator script
version: 1.2.1
---

# Israeli Arnona Optimizer

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

After calculating the base arnona, check if the user qualifies for any discounts. Israeli law (the Arnona Regulations and individual municipal bylaws) provides discounts for specific populations:

| Category | Discount | Key Requirements |
|----------|----------|-----------------|
| Oleh Chadash (new immigrant) | Up to 90% on up to 100 sqm | 12 discounted months chosen within the first 24 months from the teudat-oleh / registration date; primary residence |
| Active-duty soldier (chayal sadir) | Up to 100% | IDF service confirmation; lone/qualifying soldier |
| Senior (vatik), pension recipient | Up to 25% (discretionary) | Receives old-age / survivors / work-injury pension; no income test |
| Senior (vatik), income-tested | 30% (mandatory) | Household income up to the average wage |
| Senior (vatik) with income supplement | Up to 100% | Also receives hashlamat hachnasa within the income limit |
| Disabled, medical disability 90%+ | Up to 40% | Bituach Leumi medical-disability certificate (90%+) |
| Disabled, earning incapacity 75%+ | Up to 80% | 75%+ loss of earning capacity (ai-kosher) with a full monthly benefit |
| Low income (individual) | 20-80% | Income below municipality threshold (varies by city) |
| Student | Up to ~50% (municipality-dependent) | Discretionary per municipal bylaw; no uniform national rate |
| Single parent | Up to 20% | Recognized single parent status |
| Large family (4+ children) | Income-tested, up to ~30% | Four or more dependent children; income bands |
| Bereaved family | Up to 66% | Ministry of Defense bereaved family recognition |
| Holocaust survivor | Up to 66% | Recognized Holocaust survivor status |

Run the calculator with discount flags:

```bash
python scripts/arnona-calculator.py --municipality "tel-aviv" --area 80 --zone 2 --usage residential --discount oleh --discount-months 8
```

Consult `references/arnona-discounts-guide.md` for the full list of discount categories, required documentation, and municipality-specific variations.

**Important rules about discounts:**
- Discounts apply only to the primary residence (dira ikarit), up to 100 sqm in most municipalities.
- Area above the discount cap is charged at the full rate.
- Only one discount can be applied at a time (the highest applicable discount).
- Discounts must be renewed annually in most municipalities.
- The application deadline varies by municipality (typically January-March).

### Step 4: Draft Appeal Letters

If the user believes their arnona assessment is incorrect, help them draft an appeal letter (hasaga) to the municipality's arnona committee (vaada le-hashagot). Common grounds for appeal:

1. **Incorrect area measurement**: The municipality's recorded area differs from the actual property size. Request a surveyor re-measurement.
2. **Wrong zone classification**: The property should be classified in a lower-rate zone based on its location.
3. **Incorrect usage classification**: The property is classified as commercial but is actually used for residential purposes (or vice versa).
4. **Structural issues**: Parts of the property are uninhabitable (e.g., under renovation, flood damage, structural defects).
5. **Empty/vacant property**: The property has been vacant for an extended period (some municipalities offer partial exemptions for vacant properties, typically up to 6 months).

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
| gov.il: Property Tax (Arnona) | https://www.gov.il/he/departments/topics/property_tax_arnona | Official ministry topic page covering legislation and discount eligibility |
| Bituach Leumi: Disability Benefits | https://www.btl.gov.il/benefits/Disability/Pages/default.aspx | Source documents for the disability percentages used in arnona discount eligibility |
| Tel Aviv Municipality | https://www.tel-aviv.gov.il/ | Tel Aviv tzav arnona, current rates, online payment, appeals |
| Jerusalem Municipality | https://www.jerusalem.muni.il/ | Jerusalem alef-heh zone rates, payment, discount applications |

## Gotchas
- Arnona rates vary dramatically between municipalities. Agents may use Tel Aviv rates for Haifa properties or vice versa. Always verify rates against the specific municipality (iriya or mo'atza).
- Arnona discounts (hanacha) have strict eligibility windows and require annual renewal. Agents may suggest discounts the user no longer qualifies for or that have expired.
- Property classification (residential vs. commercial) significantly affects arnona rates. Agents may misclassify home offices, which in Israel are usually still taxed at residential rates unless formally rezoned.
- Arnona appeal deadlines are typically 90 days from the annual bill date. Agents may draft appeals after the deadline has passed, making them void.

## Troubleshooting

### Error: "Municipality not found in rate tables"
Cause: The arnona calculator does not have rate data for the specified municipality. Smaller local councils (moatzot mekomiyot) and regional councils (moatzot azeriyot) have their own rate tables that may not be included.
Solution: Check the municipality name spelling. Use the `--list-municipalities` flag to see all supported municipalities. For unsupported municipalities, consult the municipality's website directly for their published arnona rate ordinance (tzav arnona). You can also try searching for "[municipality name] tzav arnona [year]" to find the official rate publication.

### Error: "Discount category not recognized"
Cause: The discount type specified does not match one of the supported discount categories in the calculator.
Solution: Run `python scripts/arnona-calculator.py --list-discounts` to see all supported discount categories. Common mistakes include using "immigrant" instead of "oleh". The supported categories are: oleh, soldier, senior-pension, senior-income, senior-supplement, disabled-medical, disabled-incapacity, low-income, student, single-parent, large-family, bereaved, holocaust-survivor.

### Error: "Zone not valid for this municipality"
Cause: Each municipality uses its own zone classification system. Tel Aviv uses numbered zones (1-4), Jerusalem uses Hebrew-letter zones alef through heh (א-ה), and other cities have their own systems.
Solution: Check the zone classification for your specific municipality. If unsure of your zone, look at a previous arnona bill (it shows the zone), or contact the municipality's arnona department. The `references/arnona-rates-guide.md` file lists the zone systems for each supported municipality.

### Error: "Cannot determine appeal deadline"
Cause: The appeal filing deadline depends on when the arnona bill was received, and the system cannot verify the receipt date.
Solution: The general rule is 90 days from the date of the arnona bill for filing an appeal (hasaga) to the arnona manager. After receiving the manager's decision, the user has 30 days to appeal to the appeals committee (vaada le-erurim). Always recommend filing as early as possible and keeping proof of the filing date (registered mail receipt or online submission confirmation).