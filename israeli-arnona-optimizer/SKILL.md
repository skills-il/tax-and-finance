---
name: israeli-arnona-optimizer
description: >-
  Calculate municipal property tax (arnona) for Israeli properties, check discount eligibility,
  and draft appeal letters to arnona committees. Use when a user needs to estimate arnona payments
  by municipality, zone, and property usage type, verify eligibility for discounts (olim, soldiers,
  elderly, disabled, low income, students, single parents), or prepare formal appeals with legal
  references. Covers all major Israeli municipalities including Tel Aviv, Jerusalem, Haifa, and
  Beer Sheva. Do NOT use for income tax (mas hachnasa), VAT (maam), or national insurance (bituach leumi)
  calculations, which fall under separate Israeli tax authorities.
license: MIT
allowed-tools: "Bash(python:*) Read Edit Write WebFetch"
compatibility: "Requires Python 3.8+ for calculator script"
metadata:
  author: skills-il
  version: 1.0.0
  category: tax-and-finance
  tags:
    he:
      - ארנונה
      - מס-רכוש
      - מס-עירוני
      - הנחות
      - ערעור-מס
    en:
      - arnona
      - property-tax
      - municipal-tax
      - discounts
      - tax-appeal
  display_name:
    he: "אופטימיזציית ארנונה ישראלית"
    en: "Israeli Arnona Optimizer"
  display_description:
    he: "חישוב ארנונה עירונית, בדיקת זכאות להנחות, וניסוח מכתבי ערעור לוועדות ארנונה בישראל"
    en: "Calculate municipal arnona, check discount eligibility, and draft appeal letters to arnona committees in Israel"
  supported_agents:
    - claude-code
    - cursor
    - github-copilot
    - windsurf
    - opencode
    - codex
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
python scripts/arnona-calculator.py --municipality "tel-aviv" --area 80 --zone A --usage residential
```

The calculator applies the correct rate per sqm based on the municipality's published rate tables. Key rate structures:

- **Tel Aviv-Yafo**: Rates range from approximately 75 to 130 NIS/sqm/year for residential depending on zone (zones 1-4). Commercial rates are 2-4x higher.
- **Jerusalem**: Rates range from approximately 55 to 95 NIS/sqm/year for residential. Divided into zones alef through heh.
- **Haifa**: Rates range from approximately 50 to 90 NIS/sqm/year for residential. Lower overall compared to Tel Aviv.
- **Beer Sheva**: Rates range from approximately 35 to 60 NIS/sqm/year for residential. Among the lowest for major cities.

Consult `references/arnona-rates-guide.md` for detailed rate tables and zone classification rules.

### Step 3: Check Discount Eligibility

After calculating the base arnona, check if the user qualifies for any discounts. Israeli law (the Arnona Regulations and individual municipal bylaws) provides discounts for specific populations:

| Category | Discount | Key Requirements |
|----------|----------|-----------------|
| Oleh Chadash (new immigrant) | Up to 90% for first 12 months | Valid oleh certificate, property is primary residence |
| Active-duty soldier (chogeret/sadir) | Up to 100% | IDF service confirmation, single soldier living alone |
| Elderly (65-69) | Up to 25% | Income below threshold |
| Elderly (70+) | Up to 30% | Income below threshold |
| Disabled (50-74% disability) | Up to 40% | National Insurance Institute (Bituach Leumi) disability certificate |
| Disabled (75-100% disability) | Up to 80% | National Insurance Institute disability certificate |
| Low income (individual) | 20-80% | Income below municipality threshold (varies by city) |
| Student | Up to 80% | Full-time student, lives alone, income below threshold |
| Single parent | Up to 20% | Recognized single parent status |
| Large family (4+ children) | Up to 20% | Four or more dependent children |
| Bereaved family | Up to 66% | Ministry of Defense bereaved family recognition |
| Holocaust survivor | Up to 66% | Recognized Holocaust survivor status |

Run the calculator with discount flags:

```bash
python scripts/arnona-calculator.py --municipality "tel-aviv" --area 80 --zone A --usage residential --discount oleh --discount-months 8
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

Direct the user to the relevant arnona department:

- **Tel Aviv**: tel-aviv.gov.il, *6195, arnona@mail.tel-aviv.gov.il
- **Jerusalem**: jerusalem.muni.il, *6226, arnona@jerusalem.muni.il
- **Haifa**: haifa.muni.il, *2404, arnona@haifa.muni.il
- **Beer Sheva**: beer-sheva.muni.il, *6230

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
1. Identify the user as an oleh chadash within the first 12 months
2. Consult `references/arnona-discounts-guide.md` for oleh discount rules
3. Run the calculator with the oleh discount: `python scripts/arnona-calculator.py --municipality "jerusalem" --area 70 --zone B --usage residential --discount oleh --discount-months 6`
4. Calculate base arnona: 70 sqm x approximately 72 NIS/sqm = 5,040 NIS/year
5. Apply 90% discount for months 7-12 (remaining 6 months): savings of approximately 2,268 NIS for the remainder of the first year

Result: As an oleh chadash, the user is eligible for a 90% arnona discount for the first 12 months from their aliyah date. For a 70 sqm apartment in Jerusalem zone bet, the base annual arnona is approximately 5,040 NIS. With the 90% discount, the user pays only approximately 504 NIS for the year (about 84 NIS bimonthly). The agent provides instructions for applying: bring the oleh certificate (teudat oleh) and lease agreement to the Jerusalem municipality arnona department or apply online at jerusalem.muni.il.

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

## Troubleshooting

### Error: "Municipality not found in rate tables"
Cause: The arnona calculator does not have rate data for the specified municipality. Smaller local councils (moatzot mekomiyot) and regional councils (moatzot azeriyot) have their own rate tables that may not be included.
Solution: Check the municipality name spelling. Use the `--list-municipalities` flag to see all supported municipalities. For unsupported municipalities, consult the municipality's website directly for their published arnona rate ordinance (tzav arnona). You can also try searching for "[municipality name] tzav arnona [year]" to find the official rate publication.

### Error: "Discount category not recognized"
Cause: The discount type specified does not match one of the supported discount categories in the calculator.
Solution: Run `python scripts/arnona-calculator.py --list-discounts` to see all supported discount categories. Common mistakes include using "immigrant" instead of "oleh", or "senior" instead of "elderly". The supported categories are: oleh, soldier, elderly, disabled, low-income, student, single-parent, large-family, bereaved, holocaust-survivor.

### Error: "Zone not valid for this municipality"
Cause: Each municipality uses its own zone classification system. Tel Aviv uses numbered zones (1-4), Jerusalem uses Hebrew letter zones (alef-heh), and other cities have their own systems.
Solution: Check the zone classification for your specific municipality. If unsure of your zone, look at a previous arnona bill (it shows the zone), or contact the municipality's arnona department. The `references/arnona-rates-guide.md` file lists the zone systems for each supported municipality.

### Error: "Cannot determine appeal deadline"
Cause: The appeal filing deadline depends on when the arnona bill was received, and the system cannot verify the receipt date.
Solution: The general rule is 90 days from the date of the arnona bill for filing an appeal (hasaga) to the arnona manager. After receiving the manager's decision, the user has 30 days to appeal to the appeals committee (vaada le-erurim). Always recommend filing as early as possible and keeping proof of the filing date (registered mail receipt or online submission confirmation).
