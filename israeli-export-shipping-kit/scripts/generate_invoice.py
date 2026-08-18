#!/usr/bin/env python3
"""
generate_invoice.py - Bilingual (Hebrew + English) Israeli commercial invoice
and packing list generator.

Reads a JSON order file and emits a markdown document that can be converted
to PDF. Designed for Israeli exporters under Incoterms 2020.

Key behavior:
  - Israel VAT on exports is zero-rated (still a line item in the invoice).
  - Totals use Decimal to avoid float rounding.
  - Incoterm is validated against the 11 Incoterms 2020 codes.

Input JSON schema (minimum):
{
  "invoice_number": "INV-2026-0042",
  "invoice_date": "2026-04-23",
  "incoterm": "FOB",
  "named_place": "Haifa",
  "currency": "EUR",
  "seller": {"name_en": "...", "name_he": "...", "address": "...", "vat_id": "..."},
  "buyer":  {"name_en": "...", "address": "...", "country": "Germany"},
  "items": [
    {"description_en": "...", "description_he": "...",
     "hs_code": "8413.50.00", "quantity": 10,
     "unit_price": "120.00"}
  ],
  "freight": "350.00",
  "insurance": "50.00"
}

Usage:
  python generate_invoice.py --input order.json --output invoice.md
"""

from __future__ import annotations

import argparse
import json
import sys
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_UP
from pathlib import Path

# Incoterms 2020 - 11 rules (source: ICC, Trade.gov)
INCOTERMS_2020 = {
    # Any mode
    "EXW": "Ex Works",
    "FCA": "Free Carrier",
    "CPT": "Carriage Paid To",
    "CIP": "Carriage and Insurance Paid To",
    "DAP": "Delivered at Place",
    "DPU": "Delivered at Place Unloaded",
    "DDP": "Delivered Duty Paid",
    # Sea and inland waterway
    "FAS": "Free Alongside Ship",
    "FOB": "Free on Board",
    "CFR": "Cost and Freight",
    "CIF": "Cost Insurance and Freight",
}

SEA_ONLY = {"FAS", "FOB", "CFR", "CIF"}


def money(x: Decimal) -> Decimal:
    return x.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def validate_incoterm(code: str) -> None:
    if code.upper() not in INCOTERMS_2020:
        valid = ", ".join(sorted(INCOTERMS_2020.keys()))
        raise ValueError(f"Unknown Incoterm '{code}'. Valid codes: {valid}.")


def render_invoice(order: dict) -> str:
    code = order["incoterm"].upper()
    validate_incoterm(code)
    incoterm_name = INCOTERMS_2020[code]
    currency = order.get("currency", "USD")

    # Totals. Quantize each line to 2dp and sum the QUANTIZED lines, so the printed
    # arithmetic reconciles. Summing unrounded Decimals and rounding only at display
    # time produces an invoice whose columns visibly do not add up, which is a
    # standard query/rejection trigger at customs.
    subtotal = Decimal("0")
    item_rows_en = []
    item_rows_he = []
    for idx, item in enumerate(order["items"], 1):
        qty = Decimal(str(item["quantity"]))
        # Round the unit price to the invoice currency FIRST, then multiply. Rounding
        # only the product leaves an invoice whose own columns do not multiply out
        # (33.333 x 3 prints as "33.33 x 3 = 100.00"), which customs reads as an error.
        unit = Decimal(str(item["unit_price"])).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        line_total = (qty * unit).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        subtotal += line_total
        item_rows_en.append(
            f"| {idx} | {item['description_en']} | {item.get('hs_code','-')} | {qty} | {money(unit)} | {money(line_total)} |"
        )
        item_rows_he.append(
            f"| {idx} | {item.get('description_he', item['description_en'])} | {item.get('hs_code','-')} | {qty} | {money(unit)} | {money(line_total)} |"
        )

    freight = Decimal(str(order.get("freight", "0")))
    insurance = Decimal(str(order.get("insurance", "0")))
    # Whether freight and insurance belong IN the invoice total depends on the
    # Incoterm. Under E and F terms the buyer contracts and pays for main carriage,
    # so adding them overstates the transaction value, misstates the customs value
    # the importer declares, and can wrongly push a shipment past the EUR 6,000
    # invoice-declaration threshold. Under C and D terms the seller bears them.
    BUYER_PAYS_CARRIAGE = {"EXW", "FCA", "FAS", "FOB"}
    seller_bears = code not in BUYER_PAYS_CARRIAGE
    total = subtotal + (freight + insurance if seller_bears else Decimal("0"))
    vat_line = Decimal("0.00")  # Israeli export: zero-rated

    md = []
    md.append(f"# Commercial Invoice / חשבונית מסחרית")
    md.append("")
    md.append(f"**Invoice number / מספר חשבונית:** {order['invoice_number']}")
    md.append(f"**Date / תאריך:** {order['invoice_date']}")
    md.append(f"**Incoterm:** {code} {incoterm_name} - {order.get('named_place', '')} (Incoterms 2020)")
    md.append("")
    md.append("## Seller / המייצא")
    md.append(f"- Name (EN): {order['seller']['name_en']}")
    md.append(f"- שם (HE): {order['seller'].get('name_he', order['seller']['name_en'])}")
    md.append(f"- Address: {order['seller']['address']}")
    md.append(f"- VAT ID / מספר עוסק: {order['seller']['vat_id']}")
    md.append("")
    md.append("## Buyer / הקונה")
    md.append(f"- Name: {order['buyer']['name_en']}")
    md.append(f"- Address: {order['buyer']['address']}")
    md.append(f"- Country / ארץ יעד: {order['buyer'].get('country', '')}")
    md.append("")
    md.append("## Items (English)")
    md.append("| # | Description | HS code | Qty | Unit price | Line total |")
    md.append("|---|-------------|---------|-----|------------|------------|")
    md.extend(item_rows_en)
    md.append("")
    md.append("## פריטים (עברית)")
    md.append("| # | תיאור | קוד HS | כמות | מחיר יחידה | סה\"כ שורה |")
    md.append("|---|-------|--------|------|-------------|-----------|")
    md.extend(item_rows_he)
    md.append("")
    md.append("## Totals / סיכום")
    md.append(f"- Subtotal / סיכום ביניים: {money(subtotal)} {currency}")
    carriage_note = "" if seller_bears else "  (buyer's account under " + code + ", not included in the total / על חשבון הקונה, לא נכלל בסה\"כ)"
    md.append(f"- Freight / הובלה: {money(freight)} {currency}{carriage_note}")
    md.append(f"- Insurance / ביטוח: {money(insurance)} {currency}{carriage_note}")
    md.append(f"- VAT / מע\"מ (export zero-rated): {money(vat_line)} {currency}")
    md.append(f"- **Total / סה\"כ:** {money(total)} {currency}")
    md.append("")
    md.append("## Country of origin / ארץ מקור")
    # Never hard-code this. Not every line an Israeli exporter ships is of Israeli
    # origin (re-exports, foreign-made components sold on), and printing ISRAEL on a
    # customs document for goods that are not Israeli-originating is a false origin
    # statement, not a formatting detail.
    md.append(str(order.get("country_of_origin", "ISRAEL")).upper())
    md.append("")
    if order.get("reason_for_export"):
        md.append("## Reason for export / סיבת הייצוא")
        md.append(str(order["reason_for_export"]))
        md.append("")
    if code in SEA_ONLY:
        md.append(f"## Transport / הובלה")
        md.append(f"Sea or inland waterway only - {code} is a sea rule. Transport document: Bill of Lading.")
        md.append("")
    # The preferential-origin claim for the EU/UK route under the invoice-declaration
    # path lives ON the commercial invoice; a separate sheet is not accepted. Emit the
    # exact PEM wording so the exporter cannot paraphrase it (a paraphrased declaration
    # is the single most common reason an invoice declaration is refused at the border).
    dest = str(order.get("origin_declaration", "")).lower()
    if dest in ("eu", "uk"):
        auth = order.get("approved_exporter_number")
        if auth:
            auth_txt = f"(customs authorization No {auth}) "
        elif currency == "EUR" and subtotal > Decimal("6000"):
            print(
                "WARNING: an invoice declaration by a non-approved exporter is only\n"
                "         accepted up to 6,000 EUR. This consignment is above that, so a\n"
                "         EUR.1 movement certificate is required instead, or supply\n"
                "         approved_exporter_number.",
                file=sys.stderr,
            )
            auth_txt = "(customs authorization No ...) "
        elif currency != "EUR":
            # The ceiling is a EUR-equivalent value test, not a test on EUR-denominated
            # invoices only. The script has no exchange rate, so it cannot decide this
            # for a foreign-currency invoice and must not stay silent about it.
            print(
                "WARNING: the 6,000 EUR ceiling for a non-approved exporter's invoice\n"
                f"         declaration applies to the EUR-equivalent value. This invoice is in\n"
                f"         {currency} ({subtotal} {currency}), so convert it and check the\n"
                "         ceiling yourself; above it you need a EUR.1 instead.",
                file=sys.stderr,
            )
            auth_txt = ""
        else:
            auth_txt = ""
        md.append("## Origin declaration / הצהרת מקור")
        md.append("")
        md.append(
            "The exporter of the products covered by this document " + auth_txt
            + "declares that, except where otherwise clearly indicated, these products "
            "are of ISRAEL preferential origin."
        )
        md.append("")
        md.append(
            "Place and date / מקום ותאריך: "
            + str(order.get("origin_place", "______________"))
            + "  " + str(order.get("origin_postcode", ""))
            + "   " + order["invoice_date"]
        )
        md.append("")
        md.append("(Sign manually. The place name AND postal code where the originating")
        md.append("processing took place are required on Israeli origin proofs.)")
        md.append("")
    elif dest == "us":
        md.append("## Origin declaration / הצהרת מקור")
        md.append("")
        md.append(
            "I, the undersigned, hereby declare that unless otherwise indicated, the "
            "goods covered by this document fully comply with the rules of origin and "
            "the other provisions of the Agreement on the Establishment of a Free Trade "
            "Area between the Government of Israel and the Government of the United "
            "States of America."
        )
        md.append("")
        md.append(
            "I hereby undertake to provide such supporting evidence regarding the origin "
            "status of the goods as may be required by the customs authorities of the "
            "importing country."
        )
        md.append("")
        md.append("(Sign manually. Print the signatory name and position in clear.)")
        md.append("")
    md.append("## Signature / חתימה")
    md.append("")
    md.append("Exporter: ______________________   Date: ________________")
    md.append("")
    md.append("Name (print) / שם בדפוס: ______________________________")
    return "\n".join(md)


def render_packing_list(order: dict) -> str:
    md = []
    md.append("# Packing List / רשימת אריזה")
    md.append("")
    md.append(f"**Invoice number:** {order['invoice_number']}")
    md.append("")
    md.append("| # | Description | HS code | Qty | Gross weight | Net weight |")
    md.append("|---|-------------|---------|-----|--------------|------------|")
    for idx, item in enumerate(order["items"], 1):
        md.append(
            f"| {idx} | {item['description_en']} | {item.get('hs_code','-')} | {item['quantity']} | {item.get('gross_kg','-')} | {item.get('net_kg','-')} |"
        )
    return "\n".join(md)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate a bilingual Israeli commercial invoice and packing list.")
    p.add_argument("--input", type=Path, required=True, help="Order JSON file.")
    p.add_argument("--output", type=Path, help="Output markdown file (default: stdout).")
    p.add_argument("--packing-list", action="store_true", help="Also append a packing list.")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    try:
        order = json.loads(args.input.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"ERROR: invalid JSON in {args.input}: {e}", file=sys.stderr)
        return 2
    REQUIRED = ["invoice_number", "invoice_date", "incoterm", "seller", "buyer", "items"]
    missing = [k for k in REQUIRED if k not in order]
    if not missing:
        if "vat_id" not in order.get("seller", {}):
            missing.append("seller.vat_id")
        if not order.get("items"):
            missing.append("items (must contain at least one line)")
    if missing:
        print(
            "ERROR: missing required field(s): " + ", ".join(missing) + "\n"
            "  Required top level: " + ", ".join(REQUIRED) + "\n"
            "  seller needs name_en and address; buyer needs name_en, address, country.\n"
            "  Each item needs description_en, quantity and unit_price.\n"
            "  See scripts/sample_order.json for a complete working example.",
            file=sys.stderr,
        )
        return 1
    try:
        out = render_invoice(order)
        if args.packing_list:
            out += "\n\n---\n\n" + render_packing_list(order)
    except (KeyError, ValueError) as e:
        print(
            f"ERROR: {e}\n  A required field is missing or malformed. "
            "Required: invoice_number, invoice_date, incoterm, seller (name_en, address, vat_id), buyer (name_en, address, country), items (description_en, quantity, unit_price). Compare your input against scripts/sample_order.json.",
            file=sys.stderr,
        )
        return 1
    if args.output:
        args.output.write_text(out, encoding="utf-8")
        print(f"Wrote {args.output}")
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
