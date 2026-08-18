---
name: israeli-export-shipping-kit
description: "Generate the full export document set for Israeli exporters: commercial invoice (HE+EN), packing list, bill of lading / AWB / CMR, proforma, and origin documents (EUR.1, invoice origin declaration, US-Israel Origin Invoice Declaration, CIFTA Form B239). Use when user asks about exporting from Israel, Incoterms (FOB, CIF, DDP, EXW), EUR.1 certificate, approved exporter status, US-Israel FTA certificate of origin, commercial invoice template, or packing list. Do NOT use for import calculations (use israeli-customs-duty-calculator) or domestic VAT bookkeeping (use il-invoice-organizer)."
license: MIT
compatibility: "Works with Claude Code, Cursor, GitHub Copilot, Windsurf, OpenCode, Codex, Antigravity, Gemini CLI. Python 3.8+ for helper scripts."
---

# Israeli Export Shipping Kit

## Legal notice

This is a free information tool operated by an AI model. It explains customs and import rules and helps you organise your own figures. All of its outputs are produced automatically by an AI model, with no involvement, review, or approval by a customs agent or tax adviser. The output is not a filed customs declaration and not a professional opinion, but an explanation and a draft only. An AI model may err, omit data, or present a wrong conclusion.

A declaration to the customs authority is a legal document, and a false declaration carries liability. Any text this tool produces is therefore an automatic draft for your personal preparation only, to be checked with a customs agent or with the Tax Authority before filing. This tool is not a substitute for advice that takes account of the particular circumstances and needs of each person, and all use of its output is the user's sole responsibility.


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

Israeli exports are zero-rated for VAT: the standard rate is 18 percent, but exports carry a 0 percent rate. The invoice must still show the VAT line explicitly as 0 for the Tax Authority. The 0 percent rate under Section 30(a)(1) of the VAT Law is CONDITIONAL on proof that the goods actually left Israel: keep the export declaration and the transport documents on file. The statute names the document הצהרת ייצוא (export declaration); everyone in the trade calls it a רשימון יצוא, and your customs broker will use the colloquial name, but that is the thing the section requires. Without that proof the Tax Authority can deny the 0 percent and assess VAT at 18 percent.

Invoice in the currency you actually contracted in, and do not convert the item lines to
shekels on the invoice itself. For the VAT return and the books, the transaction is
translated to shekels at the Bank of Israel representative rate for the date of the tax
point, not at the rate on the day you get paid. For goods the tax point is delivery under section 22(a), so a shipment delivered in
December and paid in February belongs to the December reporting period. Check which basis
applies to you before relying on that: section 22(b) puts a dealer whose turnover does not
exceed 2 million NIS (and certain other categories) on a CASH basis, where the tax point is
receipt of payment instead. Getting this backwards misdates the whole reporting period. Record the rate you used next to the entry, because a later exchange
gain or loss is an income-tax item and does not retroactively change the VAT figure.

### Step 3: Build the packing list

- Same header as the invoice (exporter, consignee, invoice number)
- Per-package: package number, dimensions, gross weight, net weight
- Per-item per-package: quantity, description, HS code
- Marks and numbers (visible on the cartons)
- Total number of packages, total gross weight, total net weight

### Step 4: Produce the origin document matched to the destination

| Destination | Document | Who signs | Notes |
|-------------|----------|-----------|-------|
| EU (27) | EUR.1 movement certificate | Israeli Customs stamps the form | Wet-ink signature required; for shipments up to 6000 euros an invoice declaration by any exporter is accepted. Box 7 and every invoice declaration MUST state the place + postal code where origin processing happened (see Gotchas) |
| EU (27), repeat shipper | Invoice declaration (any value) | Approved exporter | Approved-exporter status granted by Israeli Customs |
| United Kingdom | EUR.1 movement certificate (or invoice declaration up to 6000 euros) | Israeli Customs / exporter | UK-Israel Trade and Partnership Agreement, in force 1 January 2021 |
| United States | US Origin Invoice Declaration | Exporter or manufacturer | Printed and signed on the commercial invoice; there is no exporter certificate to file. CBP dropped the Form A requirement for imports FROM Israel back on 20 May 1994 and instead may ask the US IMPORTER for a signed affidavit that the goods meet the FTA origin and shipping rules, so your declaration is what your buyer leans on to answer CBP (see `references/origin-declaration-template.md` for the wording) |
| Canada | Form B239 (CIFTA CO) | Exporter | Modernized CIFTA in force September 1, 2019; certificate valid 4 years. No proof of origin is needed at all for commercial goods whose value for duty is CAD 3,300 or less. If the goods were minorly processed outside Israel or Canada on the way, add Form E669 |
| EFTA, Ukraine | EUR.1 movement certificate | Israeli Customs | Same EUR.1 form, different tick-box |
| Turkey | **Do not plan a shipment here without checking first** | n/a | The Israel-Turkey FTA has not been terminated, but Turkey's trade ban on Israel (May 2024) is still in force and was tightened in February 2026, when Turkey stopped issuing EUR-MED certificates for Israel-bound goods even when routed through a third country. Treat Turkey as blocked in practice and confirm with your forwarder before quoting a customer |
| Mercosur (Brazil, Argentina, Uruguay, Paraguay) | Mercosur-Israel certificate of origin | Israeli Customs | NOT the EUR.1 form and NOT an invoice declaration: this agreement has its own certificate. Request it through Israeli Customs before shipping |
| UAE | EUR.1 / origin declaration per the CEPA protocol | Israeli Customs / exporter | UAE-Israel CEPA in force 1 April 2023 |
| South Korea | Origin declaration per the KIFTA protocol | Exporter | Korea-Israel FTA (KIFTA) in force 1 January 2023 |
| Vietnam | Origin proof per the VIFTA protocol | Exporter / Israeli Customs | Vietnam-Israel FTA (VIFTA) in force 17 November 2024 |
| Guatemala, Panama, Colombia, Mexico, Jordan | Origin proof per each bilateral protocol | Per the agreement | Israel also has in-force FTAs with these countries (Guatemala 1 March 2024) |

Israel has free trade agreements in force with the EU, USA, EFTA, Canada (CIFTA), Mercosur, UK, Turkey, Ukraine, Jordan, Mexico, Panama, Colombia, Guatemala, South Korea (KIFTA, in force 1 January 2023), the UAE (CEPA) and Vietnam (VIFTA). Check the exact origin-document type and rules of origin in the specific agreement before shipping; the table above lists the most common ones.

**A note on the EU route, current as of 27 July 2026: preferential access is fully in
force and nothing has been suspended.** The Commission proposed suspending certain trade
provisions of the EU-Israel Association Agreement in September 2025, but the Council never
adopted it; a further attempt at the Foreign Affairs Council in April 2026 did not carry;
and a July 2026 discussion of measures aimed specifically at settlement trade ended without
a decision. So quote EU customers on the preferential basis today. The reason to track it
is that a suspension would move Israeli goods to the EU's third-country MFN duty rates
overnight, which is a real pricing exposure on a long-dated contract. If you are quoting
delivered-duty terms months ahead, say who bears a duty change in the contract rather than
assuming today's rate holds. Note separately that the long-standing exclusion of goods from
Israeli settlements in territories administered since 1967 is unrelated to any of this and
has applied throughout.

**If the destination has no FTA with Israel, you need a different document entirely: a
non-preferential certificate of origin.** The EUR.1 and the invoice declaration are
*preferential* proofs, and they only exist to claim a reduced duty rate under an
agreement. A buyer in the Gulf, India, China, Nigeria, or most of Latin America has no
agreement to claim under, but their customs authority or their bank still demands written
proof of where the goods were made. That document is issued by an Israeli chamber of
commerce (Tel Aviv, Haifa or Jerusalem), stamped by the chamber rather than by Customs,
and it makes no preference claim at all.

Two situations catch exporters out. First, a letter of credit will very often call for a
chamber-stamped certificate of origin even when the destination DOES have an FTA, because
the requirement comes from the bank's document list, not from customs. Read the L/C wording
and produce exactly the document it names: a EUR.1 will be rejected as a discrepancy if the
credit asked for a chamber certificate. Second, some Arab-market destinations additionally
require the chamber certificate to be legalised at their embassy or consulate, which adds
days and a fee. Confirm the requirement with the buyer before the goods ship, not after.

See `references/eur1-application-guide.md` for the EUR.1 fields and pitfalls, and `references/origin-declaration-template.md` for invoice declaration wording.

### Step 5: Attach the transport document

| Transport mode | Document |
|----------------|----------|
| Sea | Bill of Lading (B/L) - issued by the carrier or NVOCC |
| Air | Air Waybill (AWB) - issued by the airline or freight forwarder |
| Road (to a neighboring country or via a land border) | CMR consignment note per the CMR Convention |
| Courier (DHL, UPS, FedEx) | Waybill issued by the courier |

The transport document must match the Incoterm: under FOB the buyer chooses the carrier and receives the B/L, under CIF the seller buys the freight and may be on the B/L as shipper.

The export entry itself is filed electronically with Israeli Customs through the "Sha'ar Olami" (שער עולמי) system. In practice the freight forwarder or customs broker submits this declaration on the exporter's behalf, drawing on the commercial invoice, packing list, and origin document the exporter provides.


**Two counterparty details to confirm before the goods move, because both stall a shipment at the far end rather than at yours.**

- **The EU or UK consignee needs an EORI number.** Customs in the destination country will not clear an import without one, and it is the consignee's to obtain, not the Israeli exporter's. Ask for it early and put it on the invoice: chasing it after the container lands is how demurrage starts. An Israeli exporter does not need an EORI of their own unless they are acting as importer of record in the EU.
- **Your customs broker needs a power of attorney (ייפוי כוח לסוכן מכס).** The broker files the export entry in your name, and they cannot do it without that authorisation on file. Sort it once, before the first shipment, rather than per consignment.

### Step 6: Optional documents

- Proforma invoice: sent before shipment, used for advance payment or import license in the destination country.
- Certificate of Inspection (SGS / Bureau Veritas): required by some destination buyers for government tenders.
- Health certificate / phytosanitary certificate: for food, plants, cosmetics.
- Fumigation certificate: for wood pallets under ISPM-15.
- Insurance certificate: for CIF / CIP shipments.

### Step 7: Generate the set with the helper script

`scripts/generate_invoice.py` takes a JSON input (seller, buyer, items, Incoterm) and outputs a bilingual commercial invoice and packing list in markdown, ready for review before you lock the final PDF. A complete working example ships alongside it at `scripts/sample_order.json`; copy that and edit rather than building the JSON from scratch.

Required top-level fields: `invoice_number`, `invoice_date`, `incoterm`, `seller`, `buyer`, `items`. `seller` needs `name_en`, `address` and `vat_id` (add `name_he` for the Hebrew column); `buyer` needs `name_en`, `address` and `country`. Each entry in `items` needs `description_en`, `quantity` and `unit_price`, plus `hs_code`, `description_he`, `gross_kg` and `net_kg` if you want them on the invoice and packing list. Optional: `currency` (defaults to USD), `named_place` for the Incoterm, `freight` and `insurance`. The script validates these up front and names anything missing.

Two behaviours worth knowing before you read the output. **Freight and insurance are only added into the total when the Incoterm puts them on the seller.** Under EXW, FCA, FAS and FOB the buyer contracts the main carriage, so the script prints those amounts as memo lines marked "buyer's account" and leaves them out of the invoice total: adding them there would overstate the transaction value the importer declares to their customs authority. Under the C and D terms the seller bears them and they are included. **Line totals are computed from the rounded unit price**, so the printed columns actually multiply out; give `unit_price` to more decimals than the currency has and the invoice will show the rounded figure consistently rather than a total that does not match its own arithmetic.

To print the preferential origin declaration on the invoice, set `origin_declaration` to `eu`, `uk` or `us`. For the EU and UK route also give `origin_place` and `origin_postcode` (the place and postal code where the originating processing happened, which Israeli origin proofs must state), and `approved_exporter_number` if you hold approved-exporter status. Without that number the script warns when the consignment is over 6,000 EUR, because an invoice declaration by a non-approved exporter is not accepted above that value and a EUR.1 is needed instead. The ceiling is a euro-equivalent test rather than a rule about euro-denominated invoices, so on a foreign-currency invoice the script cannot decide it for you and tells you to convert and check the ceiling yourself.

The packing list is NOT produced by default. Pass `--packing-list` to append it, or you
will ship with an invoice and no packing list, which stalls clearance:

```
python3 scripts/generate_invoice.py --input sample_order.json --packing-list --output invoice.md
```

Two more optional fields worth setting. `country_of_origin` defaults to ISRAEL but is
honoured if you set it, which matters the moment you re-export goods made somewhere else:
printing ISRAEL on a customs document for non-Israeli goods is a false origin statement,
not a formatting choice. `reason_for_export` (sale, sample, repair, return) is printed when
present and is what a customs officer looks for on a non-sale shipment.

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
- `scripts/generate_invoice.py` -- Renders a bilingual commercial invoice and packing list from JSON input (seller, buyer, items, Incoterm). Run: `python3 scripts/generate_invoice.py --help`

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
- Israel has NOT ratified the revised PEM Convention (in force from 1 January 2025 between the EU and ratifying PEM parties; 2025 a transition year, full application 1 January 2026). Israeli exporters and EU importers must continue using the 2012 rules and the same EUR.1 form they used before. This also means an Israeli EUR.1 is valid for 4 months from issuance (the 2012 rule), NOT the revised-PEM 10-month window.
- An exporter is permanently in a VAT refund position (zero output VAT, real input VAT), so the input side is where the money is, and Israel's allocation-number rule now bites there. A tax invoice from an Israeli supplier needs a מספר הקצאה from the Tax Authority before you can deduct the VAT on it, and the threshold dropped to 10,000 NIS on 1 January 2026 and again to 5,000 NIS on 1 June 2026. Freight forwarding, customs brokerage, packaging and crating invoices land above 5,000 NIS routinely. Check for the allocation number when the invoice arrives, not at the end of the reporting period, because chasing a supplier for it months later is how a refund claim gets cut.
- EUR-MED certificates are retired under the REVISED PEM rules, but Israel is still on the 2012 rules, where the EU's own guidance states that "Movement certificates EUR.1 or EUR-MED are issued by the customs authorities of the exporting country". So do not tell an Israeli exporter the form no longer exists. In practice a plain EUR.1 is what you want for a straight Israel-to-EU shipment; EUR-MED only matters when you are claiming diagonal cumulation with another PEM party, and it is worth asking Israeli Customs whether the specific cumulation you want is available before you plan around it.
- EU-Israel Technical Arrangement: to win EU preference, EUR.1 Box 7 and every invoice declaration MUST state the name of the city, village or industrial zone AND the postal code where the origin-conferring processing took place. Goods produced in Israeli settlements in territories brought under Israeli administration since June 1967 are NOT entitled to preferential treatment. Since 16 May 2023 the EU enforces this with import code Y864. A EUR.1 or invoice declaration missing the place + postal code is rejected at the EU border. See `references/eur1-application-guide.md`.
- An electronic signature on an EUR.1 is rejected by Israeli Customs. Plan time for the original stamped form to travel with the shipment.
- The 6000 euros threshold for an invoice declaration is stated in the PEM rules as "the total value of the products", so it is the value of the originating goods for the whole consignment, not a per-line figure and not the invoice grand total with freight and insurance stacked on top. A 5999 euros consignment of goods can skip the EUR.1; a 6001 euros one cannot, unless the exporter is approved. The helper script applies it to the goods subtotal for that reason.
- US-Israel FTA requires a SIGNED declaration on the commercial invoice, not a separate certificate. Do not mix up the two directions here: the widely-quoted 10 January 2018 retirement of the Green Form (Form A) applies to US exporters shipping INTO Israel. For your direction, Israel to the US, CBP eliminated Form A on 20 May 1994 and replaced it with a signed affidavit that CBP may request from the importer, and CBP states the 2017 amendment "represents no change in the ILFTA requirements for importations into the United States".
- This skill builds shipping paperwork; it does NOT determine whether goods need an export license. Controlled goods are a separate regime: defense and military items fall under the Defense Export Control Agency (אגף הפיקוח על היצוא הביטחוני) at the Ministry of Defense, and civilian dual-use items fall under the Export Control Agency at the Ministry of Economy and Industry. If the product could be military, dual-use, or otherwise controlled, the exporter must check licensing with the relevant agency before shipping. Do not rely on this skill for that determination.

## Reference Links

| Source | URL | What to check |
|--------|-----|---------------|
| ICC Incoterms 2020 | https://iccwbo.org/business-solutions/incoterms-rules/incoterms-2020/ | Authoritative text of the 11 rules |
| US-Israel FTA (Trade.gov) | https://www.trade.gov/us-israel-free-trade-agreement | Origin declaration wording, 35 percent rule |
| US-Israel CBP page | https://www.cbp.gov/trade/free-trade-agreements/israel/certificate-origin-requirements | US importer-side compliance |
| CIFTA rules of origin | https://www.cbsa-asfc.gc.ca/publications/dm-md/d11/d11-4-2-eng.html | Form B239, 4-year validity, modernized 2019 |
| EU-Israel trade page | https://policy.trade.ec.europa.eu/eu-trade-relationships-country-and-region/countries-and-regions/israel_en | EU-Israel Association Agreement, PEM status |
| EU code Y864 (Access2Markets) | https://trade.ec.europa.eu/access-to-markets/en/news/new-code-y864-goods-imported-eu-preferential-origin-israel-16-may-2023 | EU-Israel Technical Arrangement, place + postal code, 1967 territories, code Y864 |
| Israel FTAs in force (overview) | https://en.wikipedia.org/wiki/Free_trade_agreements_of_Israel | Full list of Israel's FTAs and entry-into-force dates |
| PEM 2012 rules (Access2Markets) | https://trade.ec.europa.eu/access-to-markets/en/content/rules-origin-pan-euro-mediterranean-convention | The rules Israel actually applies: EUR.1/EUR-MED, 4-month validity, 6000 euro threshold |
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
