---
name: israeli-customs-duty-calculator
description: "Classify products into Israeli 8-digit HS codes and calculate full landed cost for imports to Israel: customs duty, VAT 18%, and purchase tax (mas kniya). Use when user asks about Israel import tax, personal import threshold, customs duty on an online order from Amazon/AliExpress, FTA preferences from US/EU/UK/Canada, Shaar Olami tariff lookup, or the cost of bringing goods into Israel. Do NOT use for domestic VAT bookkeeping (use il-invoice-organizer) or for export documentation (use israeli-export-shipping-kit)."
license: MIT
compatibility: "Works with Claude Code, Cursor, GitHub Copilot, Windsurf, OpenCode, Codex, Antigravity, Gemini CLI. Python 3.8+ for helper scripts."
---

# Israeli Customs Duty Calculator

## Problem

Importing goods into Israel (whether a single Amazon order or a commercial shipment) triggers up to three separate taxes: customs duty, VAT, and purchase tax (mas kniya). Thresholds shift (the personal exemption flipped from $75 to $150 and back to $75 within a few months in 2026), duty depends on an 8-digit HS code that is not the same as the US or EU code, and free-trade preferences only help when you produce the right origin proof. Buyers constantly over- or under-estimate the landed cost.

## Instructions

### Step 1: Identify the import type

| Type | Typical user | Tax treatment |
|------|--------------|---------------|
| Personal import, small parcel | Consumer ordering online | Exemption threshold applies (see Step 2) |
| Personal import, high-value | Consumer buying jewelry, electronics | Full duty + VAT + purchase tax |
| Commercial import (B2B) | Osek Murshe importing stock | Full duty + VAT, no threshold exemption; VAT is recoverable |
| Gift | Individual sending to an Israeli | Treated as personal import, no special exemption |
| Aliyah / oleh hadash belongings | New immigrant | Separate oleh exemption, consult the Aliyah unit |

### Step 2: Check the personal import threshold

As of April 2026, the personal import VAT exemption is USD 75 (cost of goods, excluding shipping and insurance). The draft order from November 2025 that raised the threshold to 150 dollars was revoked by the Knesset on 24 February 2026.

- Below USD 75: no customs, no VAT, no purchase tax
- USD 75 to USD 500 (approx): VAT + purchase tax typically apply, customs duty is often waived for personal imports
- Above USD 500: full duty + VAT + purchase tax, commercial clearance rules apply

Confirm the current threshold via the official calculator at `https://www.gov.il/en/service/customs-tax-calculation-import-by-israelis` before quoting a number to the user. Legislation has changed twice in six months.

### Step 3: Classify the product into an 8-digit HS code

Israel uses the international Harmonized System at the 6-digit level plus 2 Israel-specific digits (positions 7 and 8) that refine the classification for local duty and purchase tax rules.

1. Describe the product: material, function, packaging form, use, brand, model.
2. Start from the 2- or 4-digit HS chapter (e.g. chapter 85 for electronics, chapter 61 for apparel).
3. Look up the full 8-digit code in Shaar Olami: `https://shaarolami-query.customs.mof.gov.il/CustomspilotWeb/en/CustomsBook/Import/Doubt`.
4. Do not guess the last 2 digits. If unsure, ask Israeli Customs for a free pre-ruling (binding classification).

### Step 4: Look up the duty rate, VAT rate, and purchase tax

From the Shaar Olami entry for the HS code, read:
- Customs duty rate (typically 0 to 12 percent depending on category; many goods are duty-free due to MFN bindings)
- VAT rate: 18 percent standard since 1 January 2025
- Purchase tax: only on specific items (alcohol, tobacco, perfumes, some electronics, passenger cars)

### Step 5: Calculate the CIF value

Israel Customs values goods at CIF: cost + insurance + freight.

```
CIF_ILS = (product_price + shipping + insurance) * USD_to_ILS_rate
```

Use the Bank of Israel daily rate for the clearance date. The `boi-exchange` MCP returns the current rate; see "Recommended MCP Servers" below.

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

### Step 7: Check for FTA preference

A valid origin proof can eliminate the duty (but not VAT or purchase tax).

| Origin | Agreement | Origin proof |
|--------|-----------|--------------|
| United States | US-Israel FTA (1985) | US Origin Invoice Declaration on the commercial invoice |
| European Union | EU-Israel Association Agreement, PEM 2012 rules (Israel has not ratified revised PEM) | EUR.1 movement certificate, or invoice declaration under 6000 euros |
| United Kingdom | UK-Israel Trade and Partnership Agreement (2019) | EUR.1 movement certificate, or invoice declaration under 6000 euros |
| Canada | Modernized CIFTA (September 2019) | Form B239 certificate of origin |
| EFTA (CH, NO, IS, LI) | EFTA-Israel Free Trade Agreement | EUR.1 movement certificate |

See `references/fta-preferences.md` for details and pitfalls.

## Examples

### Example 1: Amazon order under the threshold

User says: "I'm ordering a 60 dollar keyboard from Amazon US. Will I pay tax?"

Actions:
1. Personal import, value below the USD 75 threshold.
2. No customs duty, no VAT, no purchase tax.
3. Warn that shipping charges are NOT counted toward the threshold.
4. Note: the threshold can change, verify via the official calculator.

Result: No import tax. Landed cost equals the US price plus shipping.

### Example 2: 200 dollar camera above the threshold

User says: "How much will I pay in import tax for a 200 dollar camera from Amazon?"

Actions:
1. Personal import, value above USD 75.
2. Classify camera: HS chapter 85 (electrical machinery), likely 8525.89.xx range. Look up exact 8-digit code in Shaar Olami.
3. Apply 18 percent VAT on the CIF value, which for a personal import is often just the product value when shipping is bundled.
4. Customs duty: typically 0 percent for digital cameras under MFN.
5. Purchase tax: generally none for cameras (check Shaar Olami for the specific 8-digit code).
6. Run `python scripts/calculate_duty.py --value 200 --shipping 20 --duty-rate 0 --purchase-tax-rate 0`.

Result: Approximate tax of 18 percent of 220 USD converted to ILS, plus broker/handling. Confirm via the official calculator.

### Example 3: Commercial EU import with EUR.1

User says: "I'm importing 50 units of Italian leather bags, CIF 12000 euros, HS 4202.21.xx. What paperwork do I need?"

Actions:
1. Commercial import; no personal exemption applies.
2. Classify to the full 8-digit code via Shaar Olami; duty on leather bags is often in the 6 to 12 percent range.
3. Because CIF is above 6000 euros, require a EUR.1 movement certificate stamped by Italian customs.
4. Duty is waived under the EU-Israel agreement provided the EUR.1 is valid.
5. VAT at 18 percent on (CIF + duty) is still due.
6. Israel does NOT accept electronic signatures on EUR.1; the supplier must post the original.

Result: Origin-prefereed landed cost is CIF plus 18 percent VAT plus broker fees. Without a valid EUR.1, full duty applies.

## Bundled Resources

### Scripts
- `scripts/calculate_duty.py` -- Calculates cascading duty + purchase tax + VAT 18 percent on a CIF value. Supports USD/EUR input and prints a full breakdown. Run: `python scripts/calculate_duty.py --help`

### References
- `references/hs-codes-guide.md` -- How 8-digit HS classification works in Israel, how to use Shaar Olami, binding pre-rulings.
- `references/fta-preferences.md` -- All Israeli FTAs, which origin proof each requires, common traps.
- `references/duty-rates-by-category.md` -- Indicative duty and purchase-tax rates by product category with examples. Always verify the exact rate for your 8-digit code in Shaar Olami.

## Recommended MCP Servers

| MCP | Why | URL |
|-----|-----|-----|
| boi-exchange | Converts USD, EUR, GBP invoice values to ILS at the Bank of Israel daily rate used for customs valuation | https://agentskills.co.il/mcp/boi-exchange |

## Gotchas

- The personal-import threshold changed twice in a few months (USD 75 to USD 150 via a Smotrich decree in November 2025, then back to USD 75 by Knesset vote in February 2026). Always verify the current rate via the official calculator before quoting a number.
- Shipping and insurance are part of CIF for commercial imports but are excluded from the personal-import threshold test. Do not mix the two rules.
- The last two digits of an Israeli 8-digit HS code are Israel-specific. A US HTS code or an EU CN code does not translate directly; confirm the Israeli code in Shaar Olami.
- FTA preference removes the customs duty only. VAT 18 percent and purchase tax (where applicable) still apply regardless of origin.
- EUR.1 must carry a wet-ink (original) signature. Israel does not accept electronically signed EUR.1 certificates. Plan courier time for the original to arrive.
- Purchase tax is NOT a small rounding item. Alcohol and tobacco can carry rates in the hundreds of percent. Do not assume only VAT applies.

## Reference Links

| Source | URL | What to check |
|--------|-----|---------------|
| Israel Tax Authority | https://www.gov.il/en/departments/israel_tax_authority | Current VAT rate, customs policy updates |
| Personal import calculator | https://www.gov.il/en/service/customs-tax-calculation-import-by-israelis | Live calculation with current thresholds |
| Shaar Olami tariff query | https://shaarolami-query.customs.mof.gov.il/CustomspilotWeb/en/CustomsBook/Import/Doubt | 8-digit HS code, duty rate, purchase tax rate |
| EU-Israel trade relationship | https://policy.trade.ec.europa.eu/eu-trade-relationships-country-and-region/countries-and-regions/israel_en | EUR.1, association agreement, PEM status |
| US-Israel FTA | https://www.trade.gov/us-israel-free-trade-agreement | Origin invoice declaration, 35 percent value-added rule |
| CIFTA rules of origin | https://www.cbsa-asfc.gc.ca/publications/dm-md/d11/d11-5-6-eng.html | Form B239, modernized rules 2019 |
| Bank of Israel exchange rates | https://www.boi.org.il/en/economic-roles/financial-markets/exchange-rates/ | Daily USD/EUR/GBP to ILS rate for customs valuation |

## Troubleshooting

### Error: "My landed cost estimate is way off"

Cause: Forgetting that VAT is calculated on CIF + duty + purchase tax, not on the product price alone.

Solution: Recompute using the cascading formula in Step 6, or run `scripts/calculate_duty.py`. Add broker and handling fees separately (NIS 100 to 400 is typical for a parcel).

### Error: "Customs rejected my EUR.1"

Cause: Electronic signature, missing supplier declaration, or shipment above 6000 euros without an EUR.1 when only an invoice declaration was issued by a non-approved exporter.

Solution: Request an original wet-ink EUR.1 from the EU exporter's customs authority. For repeat shipments, the exporter should apply for approved-exporter status so invoice declarations cover any value.

### Error: "HS code I used gives a different duty in the US"

Cause: US HTS and Israeli customs tariff share the first 6 digits but diverge in positions 7 to 8.

Solution: Re-look the product up in Shaar Olami. If you need certainty, request a free pre-ruling from Israeli Customs with a product description and catalog.
