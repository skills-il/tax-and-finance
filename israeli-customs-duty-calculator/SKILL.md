---
name: israeli-customs-duty-calculator
description: "Not customs advice. Classify products into Israeli 8-digit HS codes and calculate full landed cost for imports to Israel: customs duty, VAT 18%, and purchase tax (mas kniya). Use when user asks about Israel import tax, personal import threshold, customs duty on an online order from Amazon/AliExpress, FTA preferences from US/EU/UK/Canada, Shaar Olami tariff lookup, or the cost of bringing goods into Israel. Do NOT use for domestic VAT bookkeeping (use israeli-vat-reporting) or for export documentation (use israeli-export-shipping-kit)."
license: MIT
compatibility: "Works with Claude Code, Cursor, GitHub Copilot, Windsurf, OpenCode, Codex, Antigravity, Gemini CLI. Python 3.8+ for helper scripts."
---

# Israeli Customs Duty Calculator

## Legal notice

This is a free information tool operated by an AI model. It explains the rules and calculates from the figures you enter, but it does not examine your full circumstances and does not constitute customs or tax advice. All of its outputs are produced automatically, with no involvement, review, or approval by a customs agent or tax adviser, and an AI model may err, omit data, or present a wrong conclusion. The binding classification and charge are determined by the Tax Authority at import. This tool is not a substitute for advice that takes account of the particular circumstances and needs of each person, and all use of its output is the user's sole responsibility.


## Problem

Importing goods into Israel (whether a single Amazon order or a commercial shipment) triggers up to three separate taxes: customs duty, VAT, and purchase tax (mas kniya). Thresholds shift (the personal exemption moved from $75 to $150 in December 2025, was annulled back to $75 by the Knesset on 24 February 2026, and was re-set to $130 by a new Finance Ministry order the next day, and reverted to $75 after that window ran to 1 June 2026), duty depends on an 8-digit HS code that is not the same as the US or EU code, and free-trade preferences only help when you produce the right origin proof. Buyers constantly over- or under-estimate the landed cost.

## Instructions

### Step 1: Identify the import type

| Type | Typical user | Tax treatment |
|------|--------------|---------------|
| Personal import, small parcel | Consumer ordering online | Exemption threshold applies (see Step 2) |
| Personal import, high-value | Consumer buying jewelry, electronics | VAT applies; some goods also owe duty and purchase tax depending on the HS code (see Step 2) |
| Commercial import (B2B) | Osek Murshe importing stock | Full duty + VAT, no threshold exemption. Import VAT is recoverable as input tax, but only against a rashimon that identifies the importer as the taxable person; check with your bookkeeper how the rashimon is made out before assuming recovery. This skill does not verify the input-tax rule |
| Gift | Individual sending to an Israeli | Treated as personal import, no special exemption |
| Aliyah, oleh hadash or toshav chozer belongings | New immigrant or returning resident | A separate personal-effects exemption this skill does not compute. Take it to a customs broker or the customs house; do not use the commercial row |

**This table is not exhaustive.** Israeli customs law carries several further regimes this skill does not cover and cannot compute: temporary import under an ATA carnet or a customs deposit (trade-fair goods, professional equipment, demo units), goods exported for repair or warranty service and re-imported, returning resident (toshav chozer), and diplomatic or international-organisation entry. If the shipment is any of those, **do not route it through the commercial row**: the tax base is different and following this skill will overstate the charge, sometimes by the whole value of the goods. Take those to a customs broker or to the customs house directly. See `references/domain-checklist.md`.

**Courier vs postal clearance:** how the parcel arrives changes who clears it. Courier shipments (DHL, FedEx, UPS) are self-cleared by the courier, which then bills the importer the duty, VAT, and a handling fee. Israel Post parcels go through a separate postal clearance process: low-value items can clear automatically, while items above the threshold get a payment demand the recipient settles before delivery. The tax math is the same either way; the fees and timeline differ.

### Step 2: Check the personal import threshold

As of 27 August 2026, re-verified against the source on that date, the personal import exemption is USD 75 (cost of goods, excluding shipping and insurance). This figure is exceptionally unstable. It was raised from USD 75 to USD 150 by a Finance Ministry order in late December 2025; the Knesset revoked that order on 24 February 2026, reverting to USD 75; the Finance Minister signed a fresh order setting it to USD 130 effective midnight 24-25 February 2026; and the USD 130 window ran until 1 June 2026, after which the threshold returned to USD 75. Four moves in seven months, so treat any value quoted here as provisional and confirm it against the live official calculator before quoting a number.

- Up to and including USD 75: no customs, no VAT, no purchase tax (full exemption). The source rule is "up to 75 dollars", so a parcel of exactly USD 75.00 is exempt. `scripts/calculate_duty.py` implements it inclusively
- USD 75 to USD 500: customs duty is waived under the personal-import regime, but VAT of 18 percent applies, and purchase tax still applies to goods that carry it (televisions and vehicle spare parts are the common examples). Note the two different bases: the THRESHOLD is tested on the goods value alone, excluding shipping and insurance, but the TAX is computed on the CIF value (goods plus insurance plus freight) plus any duty and purchase tax
- Above USD 500: VAT applies, and SOME goods also owe customs duty and purchase tax. It is not automatic that all three apply: the rate depends on the HS classification, so look the code up rather than assuming the full stack.
- Above USD 1,000: the shipment is treated as commercial for tax purposes. In practice carriers will usually require a customs broker and a full import declaration (rashimon) at this point, though that is a commercial practice rather than a stated legal threshold, so confirm with the carrier.

**Important carve-out**: the exemption does NOT apply to tobacco products or alcoholic beverages. Those are taxed in full from the first shekel, regardless of value. (The exemption text quoted by the rights guides names tobacco and alcoholic beverages only. E-cigarettes are commonly assumed to be treated the same way, but that is not what the quoted text says, so check the current rule before telling a user their vape shipment is or is not excluded.)

**Anti-splitting rule**: two or more parcels sent from the same supplier to the same customer within 72 hours of each other are treated as one split shipment, and import taxes are computed on their combined value. Ordering below the threshold repeatedly in the same window does not work.

Confirm the current threshold via the official Personal Import Tax calculator at `https://shaarolami-query.customs.mof.gov.il/CustomspilotWeb/PersonalImportTax` or the gov.il service page at `https://www.gov.il/en/service/customs-tax-calculation-import-by-israelis` before quoting a number to the user. The personal-import threshold has changed four times in seven months.

### Step 3: Classify the product into an 8-digit HS code

Israel uses the international Harmonized System at the 6-digit level plus 2 Israel-specific digits (positions 7 and 8) that refine the classification for local duty and purchase tax rules.

1. Describe the product: material, function, packaging form, use, brand, model.
2. Start from the 2- or 4-digit HS chapter (e.g. chapter 85 for electronics, chapter 61 for apparel).
3. Look up the full 8-digit code in Shaar Olami: `https://shaarolami-query.customs.mof.gov.il/CustomspilotWeb/en/CustomsBook/Import/Doubt`.
4. Do not guess the last 2 digits. If unsure, ask Israeli Customs for an advance classification decision. Confirm its cost and the extent to which it binds directly with the customs house; this skill does not verify either.

### Step 4: Look up the duty rate, VAT rate, and purchase tax

From the Shaar Olami entry for the HS code, read:
- **Ad-valorem only.** This skill and its script price rates expressed as a percentage of value. The Israeli tariff also uses specific rates (NIS per kg, per litre, per unit) and compound rates of the form "X percent but not less than Y NIS per kg". Those are common on food, beverages, alcohol, tobacco, and some textiles and footwear. Read the rate cell in Shaar Olami literally: if it is not a bare percentage, this calculator cannot price it and the figure has to be worked out by hand.
- Customs duty rate. Read it off Shaar Olami for the specific 8-digit code. Do not quote a typical range: a great many Israeli tariff lines carry a zero applied rate and others do not, and the only rate that matters is the one on the code
- VAT rate: 18 percent standard since 1 January 2025
- Purchase tax: only on specific items (alcohol, tobacco, perfumes, some electronics, passenger cars)

### Step 4.5: Check the order confirmation before computing anything

Some sellers and some courier services collect Israeli import tax at checkout or ship on a delivered-duty-paid basis. Read the order confirmation and the shipping terms for a tax or duties line that has already been charged BEFORE running the cascade below, because the skill computes the charge from scratch and will otherwise hand the user a second bill for money already paid. If tax was collected at checkout and a courier still demands payment at the door, that is a dispute to raise with the seller and the carrier with the checkout receipt in hand, not a second liability to settle.

### Step 5: Calculate the CIF value

Israel Customs values goods at CIF: cost + insurance + freight.

**The conversion rate is not the plain Bank of Israel rate.** For goods priced in foreign currency, customs converts at the Bank of Israel representative rate **plus 0.5 percent**. Apply the uplift once, here, and nowhere else in the calculation:

```
customs_rate = BOI_representative_rate * 1.005
CIF_ILS      = (product_price + shipping + insurance) * customs_rate
```

The `boi-exchange` MCP returns the representative rate; the 0.5 percent uplift is yours to add. `scripts/calculate_duty.py` takes the representative rate in `--fx` and applies the uplift internally, so do not pre-multiply before passing it in. Ignoring the uplift understates every landed cost by about half a percent of CIF.

### Step 6: Compute the full landed cost

The three taxes are calculated on a cascading base. Use `scripts/calculate_duty.py` to avoid arithmetic mistakes.

```
duty       = CIF * duty_rate
base_after_duty = CIF + duty
purchase_tax = base_after_duty * purchase_tax_rate
base_for_vat = base_after_duty + purchase_tax
vat        = base_for_vat * 0.18
landed_cost = CIF + duty + purchase_tax + vat + broker_fees + handling
```

**Known limit on the purchase-tax line.** Purchase tax under the Purchase Tax (Goods and Services) Law is a percentage of the WHOLESALE price, not of CIF plus duty. On an import that wholesale price is reconstructed rather than observed, by an uplift on top of CIF plus duty that varies by tariff item and is commonly called TAMA. **The uplift's rates, and the exact mechanism, are not verified in this skill.** The formula above omits it entirely, so on any item that actually carries purchase tax the figure it produces is a FLOOR, not the charge. Do not present a purchase-tax number as final: read the combined rate for the specific item off the Tax Authority personal-import calculator instead, which already has the uplift built in.

### Step 7: Check for FTA preference

A valid origin proof can eliminate the duty (but not VAT or purchase tax).

| Origin | Agreement | Origin proof |
|--------|-----------|--------------|
| United States | US-Israel FTA (1985) | US Origin Invoice Declaration on the commercial invoice |
| European Union | EU-Israel Association Agreement. The revised PEM Convention (established 2011) is the ONLY set of origin rules applying from 1 January 2026; the transitional two-set regime ended 31 December 2025. Israel signed the Regional Convention on 10 October 2013 and has ratified it | EUR.1 movement certificate, or an invoice declaration. The value ceiling for a non-approved exporter's invoice declaration is not verified here; confirm it with the exporter's customs authority |
| United Kingdom | UK-Israel Trade and Partnership Agreement (2019) | EUR.1 movement certificate, or an invoice declaration under a value ceiling not verified here |
| Canada | CIFTA, in its modernized form | CBSA form B239 certificate of origin (blanket-period field, no fixed validity) |
| EFTA (CH, NO, IS, LI) | EFTA-Israel Free Trade Agreement | EUR.1 movement certificate. Not verified in this skill; confirm with the exporter before relying on it |
| Mercosur (BR, AR, UY, PY) | Mercosur-Israel FTA | Mercosur-Israel certificate of origin. Not verified in this skill; confirm with the exporter before relying on it |

See `references/fta-preferences.md` for details and pitfalls.

### Step 8: Check whether the item needs an import approval before it needs a tax figure

Tax is not the only thing that stops a parcel, and for several product classes it is not the first thing. Any person may import personally provided the goods are not on the prohibited-import list and, where a competent authority sets criteria for that class, its approval or import licence has been obtained. Check this BEFORE quoting a landed cost, because a parcel that cannot be released does not have one.

| Product class | Competent authority | Note |
|---|---|---|
| Communications products, baby monitors, remote controls, smartphones when the shipment is 4 devices or more | Ministry of Communications | The 4-device count is what moves a phone shipment from personal to approval-requiring |
| Vehicle spare parts | Ministry of Transport and Road Safety | Also a common purchase-tax class |
| Food and food supplements | Ministry of Health, National Food Service | |
| Plants and seeds | Ministry of Agriculture, plant-protection services | |
| Helmets, gas-fired barbecues | Standards Institute of Israel | A helmet needs no approval if it already carries European or American certification |

The classes and criteria change; confirm with the authority itself, and with the Ministry of Economy for anything not listed.

### Step 9: If the assessment looks wrong, appeal it, and know which route

Two different objections go to two different places, and conflating them loses the user weeks.

- **Against the carrier's clearance commission**: to that carrier's own customer service. Customs has nothing to do with it.
- **Against the amount of tax assessed**: an online application through the personal area of the National Identification System (maarechet ha-hizdahut ha-leumit), which needs a one-time registration first. Attach proof of the payment transferred to the supplier and evidence of the actual transaction value. The service is free. For help, the claims, deposits and arrears unit (tafag) at the relevant customs house.

Refund claims (Step 10) and, for Eilat residents, a VAT refund claim go through the same personal-area route and the same tafag unit.

### Step 10: If the goods are returned or exchanged, claim the tax back

Someone who paid the import taxes and then returns or exchanges the goods because they are defective or not as described is entitled to a refund. This is a real entitlement and it is routinely left unclaimed. File online through the Tax Authority site; where the parcel came via an international shipping company, file with the claims, deposits and arrears department (tafag) at the Ben Gurion customs house.

Four conditions all have to hold:

- the goods were not imported in bulk
- they were not used, beyond any use that was necessary to discover the defect
- they were returned no later than 6 months after import, provably on time
- the goods exported are shown to be the same goods that were imported

Attach the tax receipt quoting the import-declaration number, the correspondence with the supplier, proof of the credit or the replacement, and a cheque copy or bank-account confirmation. **Above USD 250 of returned or exchanged goods** a customs export-inspection request form is also required, and the shipper or post office must have recorded on the export declaration that a refund claim is intended and have performed a physical check. Getting that recorded at the moment of export is the step people miss; it cannot be added afterwards.

## Examples

### Example 1: Amazon order under the threshold

User says: "I'm ordering a 60 dollar keyboard from Amazon US. Will I pay tax?"

Actions:
1. Personal import, product value below the USD 75 threshold (re-verified 27 August 2026).
2. No customs duty, no VAT, no purchase tax.
3. Warn that shipping charges are NOT counted toward the threshold as long as they are itemized separately on the invoice. If shipping is bundled into the product price, the combined figure is tested.
4. Note: the same keyboard at 120 dollars would NOT be exempt today. It exceeds the USD 75 threshold and would owe about 18 percent VAT (the USD 130 window that once covered it ran only to 1 June 2026). The threshold has changed four times in seven months, so verify via the official calculator before quoting.

Result: No import tax at 60 dollars. Landed cost equals the US price plus shipping.

### Example 2: 200 dollar camera above the threshold

User says: "How much will I pay in import tax for a 200 dollar camera from Amazon?"

Actions:
1. Personal import, product value above USD 75 but under USD 500. VAT applies, customs duty is waived under the personal-import regime.
2. Classify camera: HS chapter 85 (electrical machinery), likely 8525.89.xx range. Look up exact 8-digit code in Shaar Olami.
3. Apply 18 percent VAT on the CIF value (product + shipping + insurance, converted to ILS at the Bank of Israel representative rate plus 0.5 percent). For a personal import the CIF is typically just the product value plus itemized shipping.
4. Customs duty: 0 percent under the personal-import waiver for values up to USD 500. Above USD 500 the waiver stops applying and the rate is whatever the 8-digit entry says, so look it up rather than assuming cameras are duty-free.
5. Purchase tax: generally none for cameras (check Shaar Olami for the specific 8-digit code).
6. Run `python3 scripts/calculate_duty.py --value 200 --shipping 20 --duty-rate 0 --purchase-tax-rate 0 --fx 3.65 --personal`.

Result: Approximate tax of 18 percent of (200 + 20) USD converted to ILS at the representative rate plus 0.5 percent, plus a courier or postal handling and clearance commission charged on top (the amount varies by carrier, and any dispute about it goes to the carrier, not to customs). Confirm via the official calculator.

### Example 3: Commercial EU import with EUR.1

User says: "I'm importing 50 units of Italian leather bags, CIF 12000 euros, HS 4202.21.xx. What paperwork do I need?"

Actions:
1. Commercial import; no personal exemption applies.
2. Classify to the full 8-digit code via Shaar Olami and read the duty rate off that entry. Do not assume a range; this skill does not carry rates.
3. At this value, ask the Italian exporter for a EUR.1 movement certificate stamped by Italian customs rather than a plain invoice declaration. A non-approved exporter's invoice declaration is capped by value under the PEM rules; **the exact ceiling is not verified in this skill** (a figure of 6,000 euros is widely quoted but is not sourced here), so confirm it with the exporter's customs authority or your broker before choosing the cheaper proof.
4. Duty is waived under the EU-Israel agreement provided the EUR.1 is valid.
5. VAT at 18 percent on (CIF + duty) is still due.
6. Israel does NOT accept electronic signatures on EUR.1; the supplier must post the original.

Result: Origin-preferred landed cost is CIF plus 18 percent VAT plus broker fees. Without a valid EUR.1, full duty applies.

## Bundled Resources

### Scripts
- `scripts/calculate_duty.py` -- Calculates cascading duty + purchase tax + VAT 18 percent on a CIF value. Supports USD/EUR input and prints a full breakdown. Run: `python3 scripts/calculate_duty.py --help`

### References
- `references/hs-codes-guide.md` -- How 8-digit HS classification works in Israel, how to use Shaar Olami, binding pre-rulings.
- `references/fta-preferences.md` -- All Israeli FTAs, which origin proof each requires, common traps.
- `references/duty-rates-by-category.md` -- Indicative duty and purchase-tax rates by product category with examples. Always verify the exact rate for your 8-digit code in Shaar Olami.

## Recommended MCP Servers

| MCP | Why | URL |
|-----|-----|-----|
| boi-exchange | Returns the Bank of Israel daily representative rate for USD, EUR, GBP. Customs valuation adds 0.5 percent on top of that rate, which the MCP does not do for you | https://agentskills.co.il/mcp/boi-exchange |

## Gotchas

- The personal-import threshold is exceptionally volatile: USD 75 to USD 150 by a Finance Ministry order in late December 2025, back to USD 75 when the Knesset revoked that order on 24 February 2026, USD 130 by a fresh order signed less than 24 hours later (effective midnight 24-25 February 2026), and back to USD 75 after that window ran to 1 June 2026. Four moves in seven months. The current value is USD 75. Always verify it against the official calculator before quoting a number.
- The exemption does NOT cover tobacco products or alcoholic beverages. Those pay VAT and purchase tax from the first shekel regardless of value. E-cigarettes are not named in the exemption text the rights guides quote, so verify rather than asserting.
- Shipping and insurance are part of CIF for commercial imports but are excluded from the personal-import threshold test as long as they are itemized separately on the invoice. If shipping is bundled into the price, the combined figure is tested.
- The last two digits of an Israeli 8-digit HS code are Israel-specific. A US HTS code or an EU CN code does not translate directly; confirm the Israeli code in Shaar Olami.
- FTA preference removes the customs duty only. VAT 18 percent and purchase tax (where applicable) still apply regardless of origin.
- EUR.1 must carry a wet-ink (original) signature. Israel does not accept electronically signed EUR.1 certificates. Plan courier time for the original to arrive.
- Purchase tax is NOT a small rounding item. On alcohol and tobacco it is the dominant charge, and on those the tariff is specific or compound (NIS per litre of pure alcohol, NIS per unit), not a percentage, so this skill and its script cannot price them at all. Do not assume only VAT applies. Its base is also not CIF plus duty but a reconstructed wholesale price, so the script's purchase-tax line is a floor rather than the charge; take the combined rate off the official calculator instead.
- Packages above USD 1,000 are treated as commercial for tax purposes. Carriers will usually require a customs broker and a full import declaration (rashimon) at that point, but that is commercial practice rather than a stated legal threshold, so confirm with the carrier.
- The conversion rate is the Bank of Israel representative rate plus 0.5 percent, not the representative rate itself. Every landed cost computed on the bare rate is low by roughly half a percent of CIF.
- Israel Post and the courier companies charge their own commission for the clearance service, on top of the shipping cost. On a small parcel that commission routinely exceeds the tax. Objections and appeals about the commission go to the carrier's customer service, not to customs, which is a different route from an appeal against the tax itself.
- Customs may inspect the declared value and reject it, substituting a value of its own under part 2.5 of the personal-import valuation procedure. A supplier invoice is a starting point, not a ceiling.
- A false declaration or label lets customs seize the parcel or impose a fine as a condition of release, **and that applies even when the buyer did not know the declaration was wrong**. Confirm with an online seller that the declared contents and price on the package match what was actually bought.
- A parcel holding items with different tax treatments (clothing plus alcohol, say) is assessed item by item, not on one blended rate for the box.
- Several product classes need a competent authority's approval before release regardless of value: communications products and smartphones from 4 devices up, vehicle spare parts, food and supplements, plants and seeds, helmets and gas barbecues. See Step 8.
- Import taxes paid on goods later returned or exchanged are refundable, but only within 6 months and only if the export was recorded and physically checked at the time. See Step 10.

## Reference Links

| Source | URL | What to check |
|--------|-----|---------------|
| Israel Tax Authority | https://www.gov.il/en/departments/israel_tax_authority | Current VAT rate, customs policy updates |
| Personal Import Tax calculator (Shaar Olami) | https://shaarolami-query.customs.mof.gov.il/CustomspilotWeb/PersonalImportTax | Live personal-import calculator with the current threshold baked in |
| Personal import calculator (gov.il) | https://www.gov.il/en/service/customs-tax-calculation-import-by-israelis | Alternative live calculator with current thresholds |
| Shaar Olami tariff query | https://shaarolami-query.customs.mof.gov.il/CustomspilotWeb/en/CustomsBook/Import/Doubt | 8-digit HS code, duty rate, purchase tax rate |
| EU-Israel trade relationship | https://policy.trade.ec.europa.eu/eu-trade-relationships-country-and-region/countries-and-regions/israel_en | EUR.1, association agreement, PEM status |
| US-Israel FTA | https://www.trade.gov/us-israel-free-trade-agreement | Origin invoice declaration, 35 percent value-added rule |
| CIFTA certificate form B239 | https://www.cbsa-asfc.gc.ca/publications/forms-formulaires/b239-eng.html | The certificate itself, its fields and its blanket period |
| CIFTA rules of origin (CBSA index page) | https://www.cbsa-asfc.gc.ca/publications/dm-md/d11/d11-5-6-eng.html | Link page only. It points at the CIFTA Rules of Origin Regulations and does NOT state the certificate form number or any validity period, so do not cite it for either |
| Personal import rights guide (Kol Zchut) | https://www.kolzchut.org.il/he/%D7%96%D7%9B%D7%95%D7%AA%D7%95%D7%9F_%D7%91%D7%A0%D7%95%D7%A9%D7%90_%D7%99%D7%91%D7%95%D7%90_%D7%90%D7%99%D7%A9%D7%99_(%D7%97%D7%91%D7%99%D7%9C%D7%95%D7%AA_%D7%9E%D7%97%D7%95%22%D7%9C) | Current threshold, band table, the 0.5 percent FX uplift, approval authorities, refund conditions |
| Bank of Israel exchange rates | https://www.boi.org.il/en/economic-roles/financial-markets/exchange-rates/ | Daily USD/EUR/GBP to ILS rate for customs valuation |

## Troubleshooting

### Error: "My landed cost estimate is way off"

Cause: Forgetting that VAT is calculated on CIF + duty + purchase tax, not on the product price alone.

Solution: Recompute using the cascading formula in Step 6, or run `scripts/calculate_duty.py`. Add courier or broker handling and clearance fees separately; these vary by carrier and are charged on top of duty and VAT.

### Error: "Customs rejected my EUR.1"

Cause: electronic signature, missing supplier declaration, or a shipment above the invoice-declaration value ceiling accompanied only by an invoice declaration from a non-approved exporter. (The exact ceiling is not verified in this skill; confirm it with the exporter's customs authority.)

Solution: Request an original wet-ink EUR.1 from the EU exporter's customs authority. For repeat shipments, the exporter should apply for approved-exporter status so invoice declarations cover any value.

### Error: "HS code I used gives a different duty in the US"

Cause: US HTS and Israeli customs tariff share the first 6 digits but diverge in positions 7 to 8.

Solution: re-look the product up in Shaar Olami. If you need certainty, request an advance classification decision from Israeli Customs with a product description and catalog, and ask them what it costs and how far it binds.
