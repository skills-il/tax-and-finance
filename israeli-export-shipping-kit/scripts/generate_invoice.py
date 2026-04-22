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
from decimal import Decimal, ROUND_HALF_UP
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

    # Totals
    subtotal = Decimal("0")
    item_rows_en = []
    item_rows_he = []
    for idx, item in enumerate(order["items"], 1):
        qty = Decimal(str(item["quantity"]))
        unit = Decimal(str(item["unit_price"]))
        line_total = qty * unit
        subtotal += line_total
        item_rows_en.append(
            f"| {idx} | {item['description_en']} | {item.get('hs_code','-')} | {qty} | {money(unit)} | {money(line_total)} |"
        )
        item_rows_he.append(
            f"| {idx} | {item.get('description_he', item['description_en'])} | {item.get('hs_code','-')} | {qty} | {money(unit)} | {money(line_total)} |"
        )

    freight = Decimal(str(order.get("freight", "0")))
    insurance = Decimal(str(order.get("insurance", "0")))
    total = subtotal + freight + insurance
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
    md.append(f"- Freight / הובלה: {money(freight)} {currency}")
    md.append(f"- Insurance / ביטוח: {money(insurance)} {currency}")
    md.append(f"- VAT / מע\"מ (export zero-rated): {money(vat_line)} {currency}")
    md.append(f"- **Total / סה\"כ:** {money(total)} {currency}")
    md.append("")
    md.append("## Country of origin / ארץ מקור")
    md.append("ISRAEL")
    md.append("")
    if code in SEA_ONLY:
        md.append(f"## Transport / הובלה")
        md.append(f"Sea or inland waterway only - {code} is a sea rule. Transport document: Bill of Lading.")
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
    try:
        out = render_invoice(order)
        if args.packing_list:
            out += "\n\n---\n\n" + render_packing_list(order)
    except (KeyError, ValueError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    if args.output:
        args.output.write_text(out, encoding="utf-8")
        print(f"Wrote {args.output}")
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
