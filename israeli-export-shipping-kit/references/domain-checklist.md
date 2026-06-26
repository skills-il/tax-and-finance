# Domain Coverage Checklist: Israeli Goods-Export Workflow

Canonical coverage contract for `israeli-export-shipping-kit`. A senior Israeli
customs broker / international-trade expert expects every "Must" item to be
present and correct before this skill is trusted to drive a real export shipment.
"Should" items are strong best-practice. "Out of scope" items are deliberately
excluded and should be redirected, not answered.

---

## Must (core export workflow; an error here delays clearance or denies duty preference)

1. **VAT zero-rating + proof-of-export condition.** Exports of goods are
   zero-rated under Section 30(a)(1) of the VAT Law; the 0% rate is CONDITIONAL
   on documentary proof that the goods physically left Israel (the customs
   export entry / רשימון יצוא + transport documents). Missing proof lets the
   Tax Authority deny 0% and assess at the standard rate (18% as of 2025).
   Source: VAT Law s.30(a)(1); PwC Israel "Other taxes"
   (https://taxsummaries.pwc.com/israel/corporate/other-taxes).

2. **Customs export declaration via Sha'ar Olami (שער עולמי).** The export
   entry (רשימון יצוא) is filed electronically to Israeli Customs through the
   Sha'ar Olami / Global Gateway system, normally by the customs broker /
   freight forwarder on the exporter's behalf, drawing on the invoice, packing
   list and origin proof. Source: Israel Tax Authority customs portal
   (https://shaarolami-query.customs.mof.gov.il/).

3. **Commercial invoice — required fields.** Exporter (name, address, VAT/עוסק
   ID), consignee, invoice number + date, Incoterm + named place, country of
   origin, per-line description + HS code + qty + unit price + total, currency,
   freight/insurance/total, origin declaration when claiming preference,
   signature + stamp. Bilingual HE+EN recommended.

4. **Packing list.** Per-package number/dimensions/gross+net weight, per-item
   per-package qty + description + HS code, marks & numbers, totals.

5. **Origin document matched to destination FTA.** The correct preferential
   proof per destination — wrong document = no preferential duty:
   - EU-27 + UK + EFTA + Mercosur + Turkey + Ukraine: **EUR.1** movement
     certificate (stamped by Israeli Customs), OR an **invoice declaration**
     (any exporter ≤ EUR 6,000; approved exporter at any value).
   - USA: **US-Israel Origin Invoice Declaration** signed on the commercial
     invoice (the "Green Form" / Form A was retired 10 Jan 2018).
   - Canada: **CIFTA Form B239** certificate of origin (modernized CIFTA in
     force 1 Sep 2019; valid 4 years).
   - UAE (CEPA, 1 Apr 2023), South Korea (KIFTA, 1 Jan 2023), Vietnam (VIFTA,
     17 Nov 2024), Guatemala (1 Mar 2024), Panama, Colombia, Mexico, Jordan:
     origin proof per the specific bilateral protocol.
   Sources: Trade.gov US-Israel FTA; CBSA D11-5-6; Wikipedia "Free trade
   agreements of Israel".

6. **EU-Israel Technical Arrangement: place-of-production + postal code + Y864.**
   EUR.1 Box 7 and every EU invoice declaration MUST state the city/village/
   industrial-zone name AND postal code where origin-conferring processing
   occurred. Goods from Israeli settlements in territories under Israeli
   administration since June 1967 are NOT entitled to EU preference. Since
   16 May 2023 the EU enforces this via import code Y864. Missing place+postcode
   = rejected at the EU border. Source: Access2Markets Y864 news
   (https://trade.ec.europa.eu/access-to-markets/en/news/new-code-y864-...).

7. **FTA matrix correctness.** Each in-force Israeli FTA mapped to the correct
   origin-document type and entry-into-force date. Israel has in-force FTAs with
   EU, USA, EFTA, Canada, Mercosur, UK, Turkey, Ukraine, Jordan, Mexico, Panama,
   Colombia, Guatemala, South Korea, UAE, Vietnam.

8. **HS classification step.** Every invoice/packing-list line needs an HS code;
   look it up in the Israeli customs tariff book (תעריף המכס, Israel Tax
   Authority). The HS code drives both the rules-of-origin check and the
   destination duty rate.

9. **Incoterms 2020 (ICC), all 11 terms + mode constraints.** EXW/FCA/CPT/CIP/
   DAP/DPU/DDP (any mode) and FAS/FOB/CFR/CIF (sea/inland-waterway only). DPU
   replaced DAT. Correct cost-vs-risk transfer point and export/import clearance
   responsibility per term. Source: ICC Incoterms 2020.

10. **Transport document matched to mode + Incoterm.** Sea = B/L, Air = AWB,
    Road = CMR, Courier = waybill. The document must be consistent with the
    chosen Incoterm (who contracts carriage / who is shipper).

11. **US-Israel 35% value-content rule.** For US preference, materials produced
    in Israel + direct processing costs in Israel ≥ 35% of appraised value
    (up to 15 percentage points may come from US materials). Source: Trade.gov.

12. **EUR.1 validity window + wet-ink signature.** EUR.1 must reach destination
    customs within its validity period (4 months under the 2012 PEM rules that
    Israel still applies). Israeli Customs rejects electronic signatures —
    original stamped form must travel with / follow the shipment.

13. **Revised PEM status for Israel.** Israel has NOT ratified the revised PEM
    Convention; Israeli exporters continue under the 2012 rules and the same
    EUR.1 form. EUR-MED certificates are retired and must not be requested.

## Should (strong best-practice; absence is a gap, not a blocker)

1. **Customs-broker power of attorney (ייפוי כוח לסוכן מכס).** The exporter
   appoints the customs broker via a PoA so the broker can file the export
   entry in Sha'ar Olami. (Israel moved toward signature-less / digital customs
   PoA arrangements; verify current form.)

2. **Approved-exporter status (מייצא מאושר).** Process to obtain it from Israeli
   Customs so invoice declarations replace EUR.1 at any value for repeat EU/EFTA
   shipments.

3. **Proforma invoice** for advance payment / destination import licence.

4. **Optional/conditional certificates:** certificate of inspection (SGS/Bureau
   Veritas), health/phytosanitary certificate (food, plants, cosmetics),
   ISPM-15 fumigation certificate (wood pallets), insurance certificate
   (CIF/CIP).

5. **6,000-euro threshold mechanics.** Applies to total invoice value (not per
   line); below it any exporter may use an invoice declaration.

6. **Record retention.** Keep origin calculations, supplier declarations and
   declaration copies (≥ 3 years EU PEM; 5 years US-Israel FTA).

7. **Exporter identity numbers.** Israeli exporter VAT/עוסק number on documents;
   note the destination-side **EORI** number requirement for EU/UK consignees
   and the US importer's IRS/EIN where relevant.

8. **Currency / valuation.** Invoice in a hard currency (USD/EUR/GBP) at the
   Bank of Israel daily rate for ILS conversion.

9. **Rules-of-origin substance vs. document.** Distinguish "wholly obtained"
   vs. "sufficiently worked/processed" and supplier declarations feeding the
   origin claim, not just the certificate mechanics.

## Out of scope (redirect, do not answer)

1. **Import duty / purchase tax calculation** → `israeli-customs-duty-calculator`.
2. **Domestic VAT bookkeeping / invoicing** → `il-invoice-organizer`.
3. **Export licensing of controlled goods** — defense/military items (Defense
   Export Control Agency, אגף הפיקוח על היצוא הביטחוני, Ministry of Defense) and
   civilian dual-use items (Export Control Agency, Ministry of Economy). The
   skill must flag this regime exists and refer the exporter to the relevant
   agency, but not attempt the licensing determination.
4. **Service exports / IP / SaaS** zero-rating nuances (different s.30 sub-rules).
5. **Destination-country import VAT/duty liability and customs valuation in the
   buyer's country.**

## Authoritative sources

- ICC Incoterms 2020: https://iccwbo.org/business-solutions/incoterms-rules/incoterms-2020/
- US-Israel FTA (Trade.gov): https://www.trade.gov/us-israel-free-trade-agreement
- US CBP Israel COO requirements: https://www.cbp.gov/trade/free-trade-agreements/israel/certificate-origin-requirements
- CIFTA rules of origin (CBSA D11-5-6): https://www.cbsa-asfc.gc.ca/publications/dm-md/d11/d11-5-6-eng.html
- EU-Israel trade page: https://policy.trade.ec.europa.eu/eu-trade-relationships-country-and-region/countries-and-regions/israel_en
- EU code Y864 (Access2Markets): https://trade.ec.europa.eu/access-to-markets/en/news/new-code-y864-goods-imported-eu-preferential-origin-israel-16-may-2023
- Revised PEM Convention (Access2Markets): https://trade.ec.europa.eu/access-to-markets/en/content/rules-origin-revised-pan-euro-mediterranean-convention
- UK-Israel TPA: https://www.gov.uk/guidance/summary-of-the-uk-israel-trade-and-partnership-agreement
- Israel Tax Authority (VAT zero-rating, customs tariff): https://www.gov.il/en/departments/israel_tax_authority
- Sha'ar Olami customs portal: https://shaarolami-query.customs.mof.gov.il/
- Israel FTAs in force (overview): https://en.wikipedia.org/wiki/Free_trade_agreements_of_Israel
- Bank of Israel exchange rates: https://www.boi.org.il/en/economic-roles/financial-markets/exchange-rates/
