---
name: israeli-export-shipping-kit
description: "Generate the full export document set for Israeli exporters: commercial invoice (HE+EN), packing list, bill of lading / AWB / CMR, proforma, and origin documents (EUR.1, invoice origin declaration, US-Israel Origin Invoice Declaration, CIFTA Form B239). Use when user asks about exporting from Israel, Incoterms (FOB, CIF, DDP, EXW), EUR.1 certificate, approved exporter status, US-Israel FTA certificate of origin, commercial invoice template, or packing list. Do NOT use for import calculations (use israeli-customs-duty-calculator) or domestic VAT bookkeeping (use il-invoice-organizer)."
license: MIT
compatibility: "Works with Claude Code, Cursor, GitHub Copilot, Windsurf, OpenCode, Codex, Antigravity, Gemini CLI. Python 3.8+ for helper scripts."
---

# Israeli Export Shipping Kit

## Problem

Shipping a product out of Israel triggers a paperwork chain: commercial invoice, packing list, transport document (B/L, AWB or CMR), and an origin proof matched to the destination's FTA (EUR.1 for EU/UK, US Origin Invoice Declaration for the USA, Form B239 for Canada). Getting any of these wrong delays clearance or denies preferential duty. Exporters also routinely pick the wrong Incoterm and end up absorbing freight or insurance they meant the buyer to pay.

## Instructions

### Step 1: Choose the Incoterm

Incoterms 2020 (ICC) defines 11 three-letter trade terms. Pick once and write it on every document alongside the named place.

| Mode | Code | Name | Seller delivers until... |
|------|------|------|--------------------------|
| Any | EXW | Ex Works | Buyer collects at seller's premises |
| Any | FCA | Free Carrier | Seller hands goods to buyer's carrier |
| Any | CPT | Carriage Paid To | Seller pays freight to named destination |
| Any | CIP | Carriage and Insurance Paid To | Like CPT, seller also buys insurance |
| Any | DAP | Delivered at Place | Seller delivers, buyer unloads |
| Any | DPU | Delivered at Place Unloaded | Seller delivers AND unloads (replaced DAT) |
| Any | DDP | Delivered Duty Paid | Seller pays import duty and clears |
| Sea | FAS | Free Alongside Ship | Alongside the vessel at named port |
| Sea | FOB | Free on Board | On board the vessel |
| Sea | CFR | Cost and Freight | Seller pays sea freight, risk transfers at loading |
| Sea | CIF | Cost Insurance and Freight | CFR plus marine insurance |

Rule of thumb:
- FOB/CFR/CIF are for bulk sea cargo only. Do not use them for containers or air freight; use FCA/CPT/CIP.
- Avoid EXW with international buyers unless the buyer explicitly handles export clearance from Israel.
- DDP is risky for small exporters: you become responsible for Israeli export formalities AND foreign import clearance.

### Step 2: Draft the commercial invoice

Required fields (bilingual HE + EN is recommended for Israeli customs):

- Exporter (shipper): Israeli business name, address, VAT ID, phone, email
- Consignee (buyer): full name, address, country, tax/VAT ID
- Invoice number and date
- Purchase order / buyer reference
- Incoterm + named place (e.g. "FOB Haifa" or "DAP Berlin")
- Country of origin (Israel, for goods wholly or substantially produced in Israel)
- Item lines: description (HE + EN), HS code, quantity, unit price, total
- Currency (USD, EUR, GBP or ILS)
- Totals: subtotal, freight, insurance, total invoice value
- Declaration of origin (when claiming FTA preference, see Step 4)
- Exporter signature, stamp, printed name

Israeli exports are zero-rated for VAT under the 18 percent regime (exports are zero-rated), but the invoice must still show the VAT line as 0 for the Tax Authority.

### Step 3: Build the packing list

- Same header as the invoice (exporter, consignee, invoice number)
- Per-package: package number, dimensions, gross weight, net weight
- Per-item per-package: quantity, description, HS code
- Marks and numbers (visible on the cartons)
- Total number of packages, total gross weight, total net weight

### Step 4: Produce the origin document matched to the destination

| Destination | Document | Who signs | Notes |
|-------------|----------|-----------|-------|
| EU (27) | EUR.1 movement certificate | Israeli Customs stamps the form | Wet-ink signature required; for shipments up to 6000 euros an invoice declaration by any exporter is accepted |
| EU (27), repeat shipper | Invoice declaration (any value) | Approved exporter | Approved-exporter status granted by Israeli Customs |
| United Kingdom | EUR.1 movement certificate (or invoice declaration up to 6000 euros) | Israeli Customs / exporter | UK-Israel Trade and Partnership Agreement 2019 |
| United States | US Origin Invoice Declaration | Exporter or manufacturer | Printed and signed on the commercial invoice; Green Form (Form A) retired January 10, 2018 |
| Canada | Form B239 (CIFTA CO) | Exporter | Modernized CIFTA in force September 1, 2019; certificate valid 4 years |
| EFTA, Mercosur | EUR.1 movement certificate | Israeli Customs | Same EUR.1 form, different tick-box |

See `references/eur1-application-guide.md` for the EUR.1 fields and pitfalls, and `references/origin-declaration-template.md` for invoice declaration wording.

### Step 5: Attach the transport document

| Transport mode | Document |
|----------------|----------|
| Sea | Bill of Lading (B/L) - issued by the carrier or NVOCC |
| Air | Air Waybill (AWB) - issued by the airline or freight forwarder |
| Road (to a neighboring country or via a land border) | CMR consignment note per the CMR Convention |
| Courier (DHL, UPS, FedEx) | Waybill issued by the courier |

The transport document must match the Incoterm: under FOB the buyer chooses the carrier and receives the B/L, under CIF the seller buys the freight and may be on the B/L as shipper.

### Step 6: Optional documents

- Proforma invoice: sent before shipment, used for advance payment or import license in the destination country.
- Certificate of Inspection (SGS / Bureau Veritas): required by some destination buyers for government tenders.
- Health certificate / phytosanitary certificate: for food, plants, cosmetics.
- Fumigation certificate: for wood pallets under ISPM-15.
- Insurance certificate: for CIF / CIP shipments.

### Step 7: Generate the set with the helper script

`scripts/generate_invoice.py` takes a JSON input (seller, buyer, items, Incoterm) and outputs a bilingual commercial invoice and packing list in markdown, ready for review before you lock the final PDF.

```
python scripts/generate_invoice.py --input sample_order.json --output invoice.md
```

## Examples

### Example 1: EU shipment of 12000 euros to Germany

User: "I am shipping 12000 euros of industrial pumps to Germany. What do I need?"

Actions:
1. Incoterm: negotiate CIP Berlin (paid insurance, road/sea via a forwarder).
2. Commercial invoice HE + EN showing origin Israel, HS code per pump, zero VAT.
3. Packing list with per-carton breakdown.
4. EUR.1 movement certificate stamped by Israeli Customs. Wet-ink signature.
5. Bill of Lading or FCR/AWB from the forwarder.
6. Insurance certificate (required by CIP).
7. Reminder: the value exceeds 6000 euros, so an invoice declaration is NOT enough unless the exporter has approved-exporter status.

### Example 2: US shipment of 3000 USD to California

User: "I am sending 3000 USD of cosmetics to a US distributor."

Actions:
1. Incoterm: DAP Los Angeles (door delivery, buyer imports).
2. Commercial invoice HE + EN, zero VAT, full HS codes.
3. Packing list.
4. US Origin Invoice Declaration printed and signed on the invoice. No separate certificate.
5. AWB from the courier.
6. Ensure that Israeli content + direct processing costs meet the 35 percent value-added rule.

### Example 3: Small EU shipment under 6000 euros

User: "I am sending 4500 euros of leather goods to Poland."

Actions:
1. Incoterm: DAP Warsaw.
2. Invoice + packing list.
3. Under the 6000 euros threshold, an invoice origin declaration by any exporter is accepted; no EUR.1 needed.
4. Add the declaration wording (see `references/origin-declaration-template.md`).

## Bundled Resources

### Scripts
- `scripts/generate_invoice.py` -- Renders a bilingual commercial invoice and packing list from JSON input (seller, buyer, items, Incoterm). Run: `python scripts/generate_invoice.py --help`

### References
- `references/incoterms-2020.md` -- Full breakdown of all 11 Incoterms 2020 rules with seller / buyer responsibility tables.
- `references/eur1-application-guide.md` -- Field-by-field guide to filling and stamping an EUR.1 in Israel.
- `references/pem-2026-rules.md` -- Current status of the revised PEM Convention and Israel's unratified position.
- `references/origin-declaration-template.md` -- Exact wording for the US-Israel, EU, UK and CIFTA invoice declarations.

## Recommended MCP Servers

| MCP | Why | URL |
|-----|-----|-----|
| boi-exchange | Converts the Israeli exporter's invoice to USD, EUR or GBP at the Bank of Israel daily rate | https://agentskills.co.il/mcp/boi-exchange |

## Gotchas

- Agents confuse Incoterm letters. FOB is sea-only; use FCA for container shipments. CIF is sea-only; use CIP for air or multimodal.
- Israel has NOT ratified the revised PEM Convention (in force from 1 January 2026 between the EU and ratifying PEM parties). Israeli exporters and EU importers must continue using the 2012 rules and the same EUR.1 form they used before.
- EUR-MED certificates are retired under the revised PEM regime and are no longer issued. Never request one.
- An electronic signature on an EUR.1 is rejected by Israeli Customs. Plan time for the original stamped form to travel with the shipment.
- The 6000 euros threshold for an invoice declaration applies to the total invoice value, not per line. A 5999 euros shipment can skip EUR.1; a 6001 euros one cannot (unless the exporter is approved).
- US-Israel FTA requires a SIGNED declaration on the commercial invoice, not a separate certificate. The old hard-copy Green Form (Form A) has not been used since January 10, 2018.

## Reference Links

| Source | URL | What to check |
|--------|-----|---------------|
| ICC Incoterms 2020 | https://iccwbo.org/business-solutions/incoterms-rules/incoterms-2020/ | Authoritative text of the 11 rules |
| US-Israel FTA (Trade.gov) | https://www.trade.gov/us-israel-free-trade-agreement | Origin declaration wording, 35 percent rule |
| US-Israel CBP page | https://www.cbp.gov/trade/free-trade-agreements/israel/certificate-origin-requirements | US importer-side compliance |
| CIFTA rules of origin | https://www.cbsa-asfc.gc.ca/publications/dm-md/d11/d11-5-6-eng.html | Form B239, 4-year validity, modernized 2019 |
| EU-Israel trade page | https://policy.trade.ec.europa.eu/eu-trade-relationships-country-and-region/countries-and-regions/israel_en | EU-Israel Association Agreement, PEM status |
| Revised PEM (Access2Markets) | https://trade.ec.europa.eu/access-to-markets/en/content/rules-origin-revised-pan-euro-mediterranean-convention | Israel-unratified status, EUR-MED retirement |
| UK-Israel TPA | https://www.gov.uk/guidance/summary-of-the-uk-israel-trade-and-partnership-agreement | Post-Brexit UK preference, EUR.1 acceptance |
| Israel Tax Authority | https://www.gov.il/en/departments/israel_tax_authority | Zero-rated export VAT rules |
| Bank of Israel exchange rates | https://www.boi.org.il/en/economic-roles/financial-markets/exchange-rates/ | Daily USD/EUR/GBP to ILS rate for invoicing |

## Troubleshooting

### Error: "EUR.1 rejected at the EU border"

Cause: Electronic signature, missing Israeli Customs stamp, or incorrect box 4 (country / group of countries).

Solution: Request a fresh EUR.1 with a wet-ink signature and a physical Israeli Customs stamp. For repeat shipments, apply for approved-exporter status with Israeli Customs to switch to invoice declarations.

### Error: "US buyer says the origin declaration is invalid"

Cause: Missing signature, missing 35 percent origin calculation, or the declaration placed on a non-commercial document.

Solution: Print the exact US Origin Invoice Declaration wording on the commercial invoice, shipping list or proforma invoice. The exporter or manufacturer must sign manually. Keep the value-added calculation on file in case CBP requests verification.

### Error: "Freight forwarder says my Incoterm is impossible"

Cause: FOB or CIF chosen for air freight, or DDP chosen without clearing authority in the destination country.

Solution: For air or multimodal, switch FOB/CFR/CIF to FCA/CPT/CIP. For DDP, confirm with the buyer that you have a local tax registration or a fiscal representative in the destination, otherwise switch to DAP.
