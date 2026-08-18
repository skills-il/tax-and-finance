#!/usr/bin/env python3
"""Build an Israeli price quote (הצעת מחיר) from a JSON spec.

Reads spec on stdin or from --input. Emits markdown (default) or HTML
to stdout. Validates oseik status against VAT setting and payment-term
tier against the Late Payment Law.

Usage:
    cat quote.json | python3 quote_builder.py
    python3 quote_builder.py --input quote.json --format html
    python3 quote_builder.py --example > example-quote.md

Spec schema (JSON):
{
    "quote_number": "2026-042",
    "issue_date": "2026-05-19",       # ISO date
    "validity_days": 14,               # 14-30 typical, 40 max for enterprise
    "issuer": {
        "name": "Yael Cohen",
        "oseik_status": "morshe",      # morshe | patur | zair | chevra
        "oseik_number": "311234567",
        "phone": "050-1234567",
        "email": "yael@example.co.il",
        "address": "Tel Aviv",
        "bank": {"name": "Leumi", "code": "10", "branch": "800", "account": "12345/67"}
    },
    "client": {
        "name": "Rishon Tech Ltd",
        "id_label": "company",          # company | oseik | none
        "id": "514567890",
        "tier": "b2b"                   # state | local-authority | b2b | construction
    },
    "lines": [
        {"description": "ייעוץ אסטרטגי", "quantity": 20, "unit": "שעות",
         "unit_price": 450.00, "discount": 0}
    ],
    "payment_term": "shotef+30",        # shotef+30 (default) | shotef+45 | net-30 | custom
    "currency": "ILS",                  # ILS | USD | EUR
    "export_zero_vat": false,            # true = zero-rated under §30(a)(5)
    "clauses": {
        "scope_change_rate": 450,
        "cancellation_percent": 25,
        "fx_clause": false,
        "materials_excluded": null
    }
}
"""

import argparse
import json
import sys
from datetime import date, timedelta
from decimal import ROUND_HALF_EVEN, Decimal

VAT_RATE = Decimal("0.18")
OSEIK_PATUR_THRESHOLD_2026 = Decimal("122833")

PAYMENT_TIER_CAPS = {
    "state": ("45 days from invoice submission", 45, "from-invoice"),
    "local-authority": ("45 days from month-end", 45, "from-month-end"),
    "b2b": ("shotef + 45 (45 days from month-end)", 45, "from-month-end"),
    "construction": ("80 days from month-end", 80, "from-month-end"),
}


def money(x: Decimal) -> str:
    """Format Decimal as Israeli-style number with two decimals and commas."""
    q = x.quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)
    return f"{q:,.2f}"


def compute_totals(lines, charges_vat):
    # Accumulate UN-ROUNDED line totals; round once at the end. Double-rounding
    # (rounding each line then summing) drifts on PCN874 cross-totals.
    raw_subtotal = Decimal("0")
    line_outputs = []
    for line in lines:
        qty = Decimal(str(line.get("quantity", 1)))
        price = Decimal(str(line["unit_price"]))
        discount = Decimal(str(line.get("discount", 0)))
        raw_line = qty * price - discount
        raw_subtotal += raw_line
        # Display value is rounded; the accumulator keeps the precise value.
        display_line = raw_line.quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)
        line_outputs.append({**line, "line_total": display_line})
    subtotal = raw_subtotal.quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)
    vat = (
        (raw_subtotal * VAT_RATE).quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)
        if charges_vat
        else Decimal("0.00")
    )
    total = (subtotal + vat).quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)
    return line_outputs, subtotal, vat, total


def validate(spec):
    warnings = []
    issuer = spec["issuer"]
    status = issuer.get("oseik_status")
    if status not in {"morshe", "patur", "chevra"}:
        raise ValueError(
            f"oseik_status must be morshe / patur / chevra (got {status!r}). "
            f"Note: esek za'ir (מסלול מקוצר) is an income-tax election, "
            f"not a VAT status; use the freelancer's actual VAT status."
        )
    charges_vat = status in {"morshe", "chevra"} and not spec.get(
        "export_zero_vat", False
    )

    if status == "patur":
        annual_revenue_estimate = sum(
            Decimal(str(l.get("quantity", 1))) * Decimal(str(l["unit_price"]))
            for l in spec["lines"]
        )
        if annual_revenue_estimate > OSEIK_PATUR_THRESHOLD_2026 * Decimal("0.5"):
            warnings.append(
                "This single quote is more than 50% of the 2026 oseik patur ceiling "
                f"(122,833 ₪). Confirm year-to-date revenue stays under the cap; "
                f"otherwise plan a status conversion to oseik morshe."
            )

    client_tier = spec.get("client", {}).get("tier", "b2b")
    payment_term = spec.get("payment_term", "shotef+30")

    if client_tier in PAYMENT_TIER_CAPS and payment_term.startswith("shotef+"):
        try:
            user_days = int(payment_term.split("+", 1)[1])
            cap_days = PAYMENT_TIER_CAPS[client_tier][1]
            if user_days > cap_days:
                cap_desc = PAYMENT_TIER_CAPS[client_tier][0]
                warnings.append(
                    f"Payment term {payment_term} exceeds statutory cap "
                    f"({cap_desc}) for tier {client_tier!r}. "
                    f"Late Payment Law 5777-2017 voids longer terms in B2B/public-sector contracts."
                )
        except ValueError:
            pass

    return charges_vat, warnings


def render_markdown(spec, line_outputs, subtotal, vat, total, charges_vat):
    issue = date.fromisoformat(spec["issue_date"])
    validity_days = spec.get("validity_days", 14)
    valid_until = (issue + timedelta(days=validity_days)).isoformat()

    issuer = spec["issuer"]
    status = issuer["oseik_status"]
    # NOTE: esek za'ir is an income-tax election (מסלול מקוצר), not a VAT
    # status. The header always reflects the freelancer's actual VAT status:
    # patur or morshe. There is no "עסק זעיר" header label on Israeli invoices.
    header_label = {
        "morshe": f"עוסק מורשה {issuer['oseik_number']}",
        "patur": f"עוסק פטור {issuer['oseik_number']}",
        "chevra": f"חברה בע\"מ {issuer['oseik_number']}",
    }[status]

    currency = spec.get("currency", "ILS")
    sym = {"ILS": "₪", "USD": "$", "EUR": "€"}.get(currency, currency)

    out = []
    out.append(f"# הצעת מחיר {spec['quote_number']}\n")
    out.append(f"**{issuer['name']}** | {header_label}")
    out.append(f"טלפון {issuer['phone']} | אימייל {issuer['email']}")
    out.append(f"{issuer['address']}\n")

    client = spec["client"]
    cid_label = {
        "company": "מספר חברה",
        "oseik": "מספר עוסק",
        "none": None,
    }.get(client.get("id_label"))
    if cid_label and client.get("id"):
        out.append(f"**לכבוד:** {client['name']} ({cid_label} {client['id']})")
    else:
        out.append(f"**לכבוד:** {client['name']}")
    out.append(f"**תאריך הוצאה:** {spec['issue_date']}")
    out.append(f"**תוקף ההצעה עד:** {valid_until}\n")

    out.append("## פירוט השירות\n")
    out.append("| פריט | כמות | מחיר יחידה | סה\"כ |")
    out.append("|---|---|---|---|")
    for line in line_outputs:
        qty_str = f"{line.get('quantity', 1)} {line.get('unit', '')}".strip()
        out.append(
            f"| {line['description']} | {qty_str} | "
            f"{money(Decimal(str(line['unit_price'])))} {sym} | "
            f"{money(line['line_total'])} {sym} |"
        )

    out.append("")
    out.append(f"**סה\"כ לפני מע\"מ:** {money(subtotal)} {sym}")
    if charges_vat:
        out.append(f"**מע\"מ 18%:** {money(vat)} {sym}")
    elif spec.get("export_zero_vat"):
        out.append("**מע\"מ 0% (יצוא שירותים, סעיף 30(א)(5) לחוק מע\"מ):** 0.00")
    out.append(f"**סה\"כ לתשלום:** {money(total)} {sym}")
    if status == "patur":
        out.append("\n*(אינני רשום כעוסק מורשה, אינני חייב מע\"מ.)*")
    out.append("")

    out.append("## תנאי עבודה\n")
    payment_term = spec.get("payment_term", "shotef+30")
    # Render the term in Hebrew. "shotef+30" → "שוטף + 30 ימים". Bare numbers
    # like "net-30" → "30 ימים".
    if payment_term.startswith("shotef+"):
        days = payment_term.split("+", 1)[1]
        term_he = f"שוטף + {days} ימים מהנפקת החשבונית"
    elif payment_term.startswith("net-"):
        days = payment_term.split("-", 1)[1]
        term_he = f"{days} ימים מהנפקת החשבונית"
    else:
        term_he = payment_term
    out.append(
        f"- **תנאי תשלום:** {term_he}. חוק מוסר תשלומים לספקים, "
        "התשע\"ז-2017 קובע תקרה חוקית של שוטף + 45 לעסקה בין עסקים; "
        "עיכוב מעבר לתקרה החוקית נושא ריבית פיגורים לפי חוק פסיקת ריבית והצמדה, התשכ\"א-1961."
    )
    clauses = spec.get("clauses") or {}
    if clauses.get("scope_change_rate"):
        out.append(
            f"- **שינויים בהיקף:** כל שינוי בהיקף העבודה יחויב בנפרד "
            f"לפי תעריף {money(Decimal(str(clauses['scope_change_rate'])))} ₪ + מע\"מ לשעה."
        )
    if clauses.get("cancellation_percent"):
        out.append(
            f"- **ביטול הזמנה:** ביטול לאחר אישור הצעה זו יחויב "
            f"ב-{clauses['cancellation_percent']}% מהסכום הכולל."
        )
    if clauses.get("fx_clause"):
        out.append(
            "- **שער חליפין:** הסכום הסופי לחיוב יחושב לפי שער יציג של "
            "בנק ישראל ביום הוצאת החשבונית."
        )
    if clauses.get("materials_excluded"):
        out.append(f"- **לא כלול:** {clauses['materials_excluded']}.")

    bank = issuer.get("bank")
    payment_methods = []
    if issuer.get("phone"):
        payment_methods.append(f"Bit {issuer['phone']}")
    if bank:
        payment_methods.append(
            f"העברה בנקאית: {bank['name']} ({bank.get('code', '')}), "
            f"סניף {bank['branch']}, חשבון {bank['account']}"
        )
    if payment_methods:
        out.append(f"- **אמצעי תשלום:** {', או '.join(payment_methods)}.")

    if status == "patur":
        out.append(
            "- **לאחר אישור ההצעה** תופק חשבונית עסקה, "
            "ועם קבלת התשלום תופק קבלה."
        )

    out.append("\n## חתימת קבלת ההצעה\n")
    out.append("________________________  תאריך: __________")
    out.append(f"{client['name']}")
    return "\n".join(out) + "\n"


def render_html(markdown_body, title):
    """Wrap markdown in a minimal RTL HTML shell for print/PDF export.

    Does NOT convert markdown to HTML, downstream tooling (pandoc, marp, etc.)
    handles that. This wrapper just provides the RTL container and print CSS.
    """
    return f"""<!DOCTYPE html>
<html dir="rtl" lang="he">
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>
  body {{ font-family: 'Arial Hebrew', 'David', sans-serif; max-width: 800px; margin: 2em auto; padding: 1em; }}
  table {{ border-collapse: collapse; width: 100%; }}
  th, td {{ border: 1px solid #ccc; padding: 0.5em; text-align: right; }}
  @media print {{ body {{ margin: 0; padding: 0; }} @page {{ size: A4; margin: 1.5cm; }} }}
</style>
</head>
<body>
<pre>{markdown_body}</pre>
</body>
</html>
"""


EXAMPLE_SPEC = {
    "quote_number": "2026-042",
    "issue_date": "2026-05-19",
    "validity_days": 14,
    "issuer": {
        "name": "יעל כהן",
        "oseik_status": "morshe",
        "oseik_number": "311234567",
        "phone": "050-1234567",
        "email": "yael@example.co.il",
        "address": "תל אביב",
        "bank": {"name": "לאומי", "code": "10", "branch": "800", "account": "12345/67"},
    },
    "client": {
        "name": "Rishon Tech Ltd",
        "id_label": "company",
        "id": "514567890",
        "tier": "b2b",
    },
    "lines": [
        {
            "description": "ייעוץ אסטרטגי",
            "quantity": 20,
            "unit": "שעות",
            "unit_price": 450.00,
        }
    ],
    "payment_term": "shotef+30",
    "currency": "ILS",
    "clauses": {"scope_change_rate": 450, "cancellation_percent": 25},
}


def main():
    parser = argparse.ArgumentParser(description="Build an Israeli price quote.")
    parser.add_argument("--input", help="Path to JSON spec file (default: stdin)")
    parser.add_argument(
        "--format",
        choices=["markdown", "html"],
        default="markdown",
        help="Output format",
    )
    parser.add_argument(
        "--example",
        action="store_true",
        help="Emit an example quote (oseik morshe consulting). Helpful for testing.",
    )
    args = parser.parse_args()

    if args.example:
        spec = EXAMPLE_SPEC
    elif args.input:
        with open(args.input, encoding="utf-8") as f:
            spec = json.load(f)
    else:
        spec = json.load(sys.stdin)

    charges_vat, warnings = validate(spec)
    line_outputs, subtotal, vat, total = compute_totals(spec["lines"], charges_vat)
    markdown = render_markdown(spec, line_outputs, subtotal, vat, total, charges_vat)

    if args.format == "html":
        sys.stdout.write(render_html(markdown, f"Quote {spec['quote_number']}"))
    else:
        sys.stdout.write(markdown)

    for w in warnings:
        sys.stderr.write(f"WARNING: {w}\n")


if __name__ == "__main__":
    main()
