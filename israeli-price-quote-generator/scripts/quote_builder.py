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
        "oseik_status": "morshe",      # morshe | patur | chevra (NOT "zair": esek za'ir is an income-tax election, not a VAT status)
        "oseik_number": "311234567",
        "phone": "050-1234567",
        "email": "yael@example.co.il",
        "address": "Tel Aviv",
        "ytd_turnover": 0,             # optional, patur only: turnover so far this calendar year
        "bank": {"name": "Leumi", "code": "10", "branch": "800", "account": "12345/67",
                 "iban": null, "swift": null}   # iban/swift: optional, printed for foreign clients
    },
    "client": {
        "name": "Rishon Tech Ltd",
        "id_label": "company",          # company | oseik | none
        "id": "514567890",
        "tier": "b2b"                   # state | state-construction | budgeted-body | local-authority | b2b | construction | consumer | foreign
    },
    "lines": [
        {"description": "ייעוץ אסטרטגי", "quantity": 20, "unit": "שעות",
         "unit_price": 450.00, "discount": 0}     # discount: flat amount; or "discount_percent": 10
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
import html
import json
import re
import sys
from datetime import date, timedelta
from decimal import ROUND_HALF_EVEN, Decimal

VAT_RATE = Decimal("0.18")
OSEIK_PATUR_THRESHOLD_2026 = Decimal("122833")

# Statutory payment dates by payer row. Construction splits by WHO ordered the
# work: section 3(b) (state authority) is 85 days from invoice / 70 from
# month-end, section 3(f) (local authority) is 80 days from month-end. Section
# 3(e) covers budgeted bodies, universities and other statutory bodies.
PAYMENT_TIER_CAPS = {
    "state": ("45 days from invoice submission, or 30 days from month-end", 45, "from-invoice"),
    "state-construction": ("85 days from invoice, or 70 days from month-end (section 3(b))", 70, "from-month-end"),
    "budgeted-body": ("shotef + 45 (section 3(e))", 45, "from-month-end"),
    "local-authority": ("45 days from month-end", 45, "from-month-end"),
    "b2b": ("shotef + 45 (45 days from month-end)", 45, "from-month-end"),
    "construction": ("80 days from month-end, local-authority construction (section 3(f))", 80, "from-month-end"),
}

# Payers for whom the quote cites no Late Payment Law date. Section 3 has rows
# only for public bodies and an "esek" (a financial institution, oseik morshe or
# oseik patur under the VAT Law), so a private individual is on no row. Whether
# the law binds a foreign payer is unsettled (territoriality and the contract's
# governing law), so a foreign quote states the agreed term only. The Israeli
# withholding and allocation-number lines are dropped for both tiers as well.
NON_STATUTORY_TIERS = {"consumer", "foreign"}

ALLOCATION_THRESHOLD_ILS = Decimal("5000")  # tax invoices from 01.06.2026, before VAT


def longer_term_note(tier):
    """Only sections 3(e)(1) and 3(g) let the parties expressly agree another date."""
    if tier in {"b2b", "budgeted-body"}:
        return ("A longer date agreed expressly is challengeable as exceptionally unfair, "
                "not automatically void.")
    return ("For this payer the statute offers no express contractual opt-out (that route "
            "exists only in sections 3(e) and 3(g)), so do not rely on a longer agreed term.")


def unit_money(x: Decimal) -> str:
    """Unit prices keep their own precision (e.g. 0.125 ₪ per word), so a row
    never displays a rounded price that does not multiply out to its total."""
    if x == x.quantize(Decimal("0.01")):
        return money(x)
    return f"{x.normalize():,f}"


def cell(text) -> str:
    """Escape a pipe so a description cannot split a markdown table row."""
    return str(text).replace("|", "\\|")


def money(x: Decimal) -> str:
    """Format Decimal as Israeli-style number with two decimals and commas."""
    q = x.quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)
    return f"{q:,.2f}"


def line_discount(line, gross):
    """Flat "discount" or "discount_percent" (of the line's gross amount)."""
    if line.get("discount_percent") is not None:
        return gross * Decimal(str(line["discount_percent"])) / Decimal("100")
    return Decimal(str(line.get("discount", 0)))


def compute_totals(lines, charges_vat):
    # Round each line to agorot, sum the rounded lines, and compute VAT on the
    # rounded subtotal, so every printed row, the subtotal, the VAT line and the
    # total reconcile exactly, the way the eventual tax invoice will compute them.
    subtotal = Decimal("0")
    line_outputs = []
    for line in lines:
        qty = Decimal(str(line.get("quantity", 1)))
        if "unit_price" not in line:
            raise ValueError(
                f"line item {line.get('description', '(no description)')!r} has no "
                f"'unit_price'; every line needs a unit price in the quote currency"
            )
        price = Decimal(str(line["unit_price"]))
        gross = qty * price
        discount = line_discount(line, gross)
        if discount < 0:
            raise ValueError(
                f"line item {line.get('description', '(no description)')!r} has a negative discount"
            )
        if discount > gross:
            raise ValueError(
                f"line item {line.get('description', '(no description)')!r} has a discount "
                f"({discount}) larger than the line amount ({gross})"
            )
        line_total = (gross - discount).quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)
        subtotal += line_total
        line_outputs.append({**line, "line_total": line_total, "discount_amount": discount})
    vat = (
        (subtotal * VAT_RATE).quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)
        if charges_vat
        else Decimal("0.00")
    )
    total = subtotal + vat
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
        quote_amount = Decimal("0")
        for l in spec["lines"]:
            gross = Decimal(str(l.get("quantity", 1))) * Decimal(str(l["unit_price"]))
            quote_amount += gross - line_discount(l, gross)
        ytd = issuer.get("ytd_turnover")
        if spec.get("currency", "ILS") != "ILS":
            warnings.append(
                "This patur quote is not in shekels, so the 122,833 ₪ ceiling could not be "
                "checked. Convert the quote at the Bank of Israel representative rate and "
                "check year-to-date turnover plus this quote against the ceiling."
            )
        elif ytd is not None:
            if Decimal(str(ytd)) + quote_amount > OSEIK_PATUR_THRESHOLD_2026:
                warnings.append(
                    f"Year-to-date turnover ({ytd}) plus this quote exceeds the 2026 oseik "
                    "patur ceiling (122,833 ₪). Do not promise a VAT-free price for this work: "
                    "quote it as 'plus VAT if the status changes before invoicing', and confirm "
                    "with an accountant from which transaction VAT applies."
                )
        elif quote_amount > OSEIK_PATUR_THRESHOLD_2026 * Decimal("0.5"):
            warnings.append(
                "This single quote is more than half of the 2026 oseik patur ceiling "
                f"(122,833 ₪). Confirm year-to-date revenue stays under the cap; "
                f"otherwise plan a status conversion to oseik morshe."
            )

    if spec.get("export_zero_vat") and status == "patur":
        raise ValueError(
            "export_zero_vat cannot be used with oseik_status='patur'. Zero-rating "
            "under VAT Law section 30(a)(5) is an oseik morshe concept (it is what "
            "preserves the input-VAT credit); an oseik patur document must carry no "
            "VAT wording at all. Drop export_zero_vat for a patur issuer."
        )

    if spec.get("export_zero_vat"):
        warnings.append(
            "export_zero_vat is set, so this quote shows 0% VAT under VAT Law "
            "section 30(a)(5). That paragraph does NOT zero-rate the service where the "
            "subject of the agreement is that the service is actually rendered, in addition "
            "to the foreign resident, also to an Israeli resident in Israel, an "
            "Israeli-majority partnership, or a company treated as an Israeli resident "
            "(the foreign-parent / Israeli-subsidiary case). Confirm WHO RECEIVES the "
            "service, not who pays, and keep the contract, proof of foreign residency and "
            "the foreign-currency payment record. Section 30(c) also requires the foreign "
            "resident to be outside Israel with no business or activity in Israel. If in "
            "doubt, quote 'plus VAT if applicable'."
        )

    client_tier_raw = spec.get("client", {}).get("tier", "b2b")
    if client_tier_raw == "foreign" and status in {"morshe", "chevra"} and not spec.get("export_zero_vat"):
        warnings.append(
            "Client tier is 'foreign' but export_zero_vat is false, so this quote adds 18% "
            "VAT. A service to a foreign resident is usually zero-rated under VAT Law "
            "section 30(a)(5); check the Step 6.5 conditions and set export_zero_vat if they hold."
        )
    if spec.get("export_zero_vat") and client_tier_raw != "foreign":
        warnings.append(
            f"export_zero_vat is set but client tier is {client_tier_raw!r}. A zero-rated "
            "client is a foreign resident, so the quote is rendered as tier 'foreign' (no "
            "Israeli statutory payment, withholding or allocation-number lines). If the "
            "client is in fact Israeli, the zero rate does not apply."
        )

    client_tier = spec.get("client", {}).get("tier", "b2b")
    payment_term = spec.get("payment_term", "shotef+30")

    if client_tier in PAYMENT_TIER_CAPS and payment_term.startswith("shotef+"):
        try:
            user_days = int(payment_term.split("+", 1)[1])
            cap_days = PAYMENT_TIER_CAPS[client_tier][1]
            if client_tier == "state" and payment_term.startswith("shotef+") and user_days > 30:
                warnings.append(
                    "Tier 'state' has two statutory dates (section 3(a)): 45 days from "
                    "delivery of the invoice, or 30 days from month-end. This quote uses a "
                    f"month-end count ({payment_term}), so the applicable figure is 30, not 45. "
                    "Check which counting basis the contract uses."
                )
            if user_days > cap_days:
                cap_desc = PAYMENT_TIER_CAPS[client_tier][0]
                warnings.append(
                    f"Payment term {payment_term} is longer than the statutory date "
                    f"({cap_desc}) for tier {client_tier!r}. "
                    "Late Payment Law 5777-2017 sets that date"
                    + (" when the contract is silent. " if client_tier in {"b2b", "budgeted-body"} else ". ")
                    + 
                    f"{longer_term_note(client_tier)}"
                )
        except ValueError:
            pass
    elif client_tier in PAYMENT_TIER_CAPS and payment_term.startswith("net-"):
        try:
            user_days = int(payment_term.split("-", 1)[1])
            cap_desc, cap_days, basis = PAYMENT_TIER_CAPS[client_tier]
            if client_tier == "state-construction":
                cap_days = 85  # section 3(b): 85 days from the invoice
            # net-N counts from the invoice date. A month-end date (shotef + cap) is
            # at least cap days after the invoice, so net-N above cap can fall after
            # the statutory date for an invoice issued late in the month.
            if user_days > cap_days:
                warnings.append(
                    f"Payment term {payment_term} counts {user_days} days from the invoice, "
                    f"which can fall after the statutory date ({cap_desc}) for tier "
                    f"{client_tier!r}, depending on the invoice day. {longer_term_note(client_tier)}"
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
        "patur": f"עוסק פטור {issuer['oseik_number']}, אינו רשום כעוסק מורשה",
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
        desc = line["description"]
        if line["discount_amount"]:
            pct = line.get("discount_percent")
            disc = f"{pct}%" if pct is not None else f"{money(line['discount_amount'])} {sym}"
            desc = f"{desc} (הנחה {disc})"
        out.append(
            f"| {cell(desc)} | {cell(qty_str)} | "
            f"{unit_money(Decimal(str(line['unit_price'])))} {sym} | "
            f"{money(line['line_total'])} {sym} |"
        )

    out.append("")
    if charges_vat or spec.get("export_zero_vat"):
        # An oseik patur document must not carry VAT-implying wording, so the
        # "before VAT" line is only printed where a VAT line follows it.
        out.append(f"**סה\"כ לפני מע\"מ:** {money(subtotal)} {sym}")
    if charges_vat and currency != "ILS":
        out.append(
            f"**מע\"מ 18%:** {money(vat)} {sym} "
            "(סכום המע\"מ בשקלים ייקבע בחשבונית)"
        )
    elif charges_vat:
        out.append(f"**מע\"מ 18%:** {money(vat)} {sym}")
    elif spec.get("export_zero_vat"):
        out.append(f"**מע\"מ 0% (יצוא שירותים, סעיף 30(א)(5) לחוק מע\"מ):** 0.00 {sym}")
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
        invoice_he = "דרישת התשלום" if status == "patur" else "החשבונית"
        term_he = f"שוטף + {days} ימים מהנפקת {invoice_he}"
    elif payment_term.startswith("net-"):
        days = payment_term.split("-", 1)[1]
        term_he = f"{days} ימים מהנפקת החשבונית"
    elif payment_term.startswith("custom:"):
        term_he = payment_term.split(":", 1)[1].strip()
    else:
        term_he = payment_term
    client_tier = spec.get("client", {}).get("tier", "b2b")
    if spec.get("export_zero_vat"):
        # A zero-rated client is by definition a foreign resident.
        client_tier = "foreign"
    statutory = client_tier not in NON_STATUTORY_TIERS
    tier_he = {
        "state": "רשות מדינה או משרד ממשלתי, 45 ימים מהמצאת החשבון או 30 ימים מתום החודש (סעיף 3(א))",
        "state-construction": "עבודות הנדסה בנאיות לגוף מדינה, 85 ימים מהמצאת החשבון או 70 ימים מתום החודש (סעיף 3(ב))",
        "budgeted-body": "גוף מתוקצב או מוסד להשכלה גבוהה מתוקצב, שוטף + 45 (סעיף 3(ה))",
        "local-authority": "רשות מקומית, שוטף + 45 (סעיף 3(ו))",
        "construction": "עבודות הנדסה בנאיות לרשות מקומית, שוטף + 80 (סעיף 3(ו))",
        "b2b": "עסקה בין עסקים, שוטף + 45 (סעיף 3(ז))",
    }.get(client_tier, "עסקה בין עסקים, שוטף + 45 (סעיף 3(ז))")
    if statutory:
        # Section 4(b): for a 3(e) body or a 3(g) business the interest applies only
        # where the payer had superiority in shaping the contract terms.
        interest_he = (
            "איחור מעבר למועד שבחוק נושא ריבית שקלית, ובחלוף 30 ימים נוספים גם דמי פיגורים, "
            "לפי חוק פסיקת ריבית והצמדה, התשכ\"א-1961"
        )
        if client_tier in {"b2b", "budgeted-body"}:
            interest_he += ", בהתקשרות שבה למזמין הייתה עדיפות בעיצוב תנאי החוזה (סעיף 4(ב) לחוק)"
        # Only 3(e)(1) and 3(g) let the parties expressly agree another date.
        absent_he = "בהיעדר הסכמה אחרת, " if client_tier in {"b2b", "budgeted-body"} else ""
        out.append(
            f"- **תנאי תשלום:** {term_he}, כמוסכם בין הצדדים. {absent_he}"
            f"חוק מוסר תשלומים לספקים, התשע\"ז-2017 קובע לסוג המזמין הזה: {tier_he}. "
            f"{interest_he}."
        )
        out.append(
            "- **פרטי החשבונית:** חשבון שחסר בו פרט מהותי שנדרש בחוזה מוחזר לספק "
            "ונחשב כאילו לא הומצא (סעיף 3(ח) לחוק), ולכן כדאי לסכם מראש מה החשבונית חייבת לכלול."
        )
    else:
        out.append(f"- **תנאי תשלום:** {term_he}, כמוסכם בין הצדדים.")
    # The allocation number serves the buyer's input-VAT deduction, so it is
    # printed for business and budgeted-body clients, not for ministries or
    # local authorities.
    if charges_vat and client_tier in {"b2b", "budgeted-body"}:
        if currency == "ILS" and subtotal > ALLOCATION_THRESHOLD_ILS:
            out.append(
                "- **מספר הקצאה:** החשבונית תופק עם מספר הקצאה מרשות המסים "
                "(נדרש לחשבונית מעל 5,000 ₪ לפני מע\"מ כדי שהלקוח יוכל לקזז את המע\"מ)."
            )
        elif currency != "ILS":
            out.append(
                "- **מספר הקצאה:** אם שווי החשבונית בשקלים יעלה על 5,000 ₪ לפני מע\"מ, "
                "היא תופק עם מספר הקצאה מרשות המסים כדי שהלקוח יוכל לקזז את המע\"מ."
            )
    clauses = spec.get("clauses") or {}
    if statutory:
        out.append(
            "- **ניכוי במקור:** התשלום כפוף להצגת אישור פטור מניכוי מס במקור בתוקף; "
            "אחרת ינוכה לפי השיעור החל על הספק. הניכוי אינו מקטין את סכום החשבונית, "
            "רק את המזומן שמתקבל ביום התשלום."
        )
    if clauses.get("scope_change_rate"):
        # "+ מע"מ" only where this quote actually charges VAT: an oseik patur
        # document must carry no VAT wording, and a zero-rated export quote has none.
        vat_suffix = " + מע\"מ" if charges_vat else ""
        out.append(
            f"- **שינויים בהיקף:** כל שינוי בהיקף העבודה יחויב בנפרד "
            f"לפי תעריף {money(Decimal(str(clauses['scope_change_rate'])))} {sym}{vat_suffix} לשעה."
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
    # Bit is a domestic P2P app; a foreign client pays by international transfer.
    # Public bodies pay through their own payment systems, not Bit.
    if issuer.get("phone") and client_tier in {"b2b", "consumer"}:
        payment_methods.append(f"Bit {issuer['phone']}")
    if bank:
        transfer = (
            f"העברה בנקאית: {bank['name']} ({bank.get('code', '')}), "
            f"סניף {bank['branch']}, חשבון {bank['account']}"
        )
        if client_tier == "foreign" and (bank.get("iban") or bank.get("swift")):
            transfer += f", IBAN {bank.get('iban') or '-'}, SWIFT {bank.get('swift') or '-'}"
        payment_methods.append(transfer)
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


def _inline(text):
    """Escape HTML, then apply **bold** and *italic*."""
    text = html.escape(text, quote=False)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    # Italic only for a whole-line *...* (the patur note); a lone or paired '*'
    # inside ordinary text (2*3, materials * transport) stays literal.
    return re.sub(r"^\*([^*].*[^*])\*$", r"<em>\1</em>", text)


def markdown_to_html(md):
    """Convert the subset of markdown render_markdown emits (headings, pipe
    tables, bullet lists, bold/italic, plain lines) to HTML, so the A4 print CSS
    actually styles a real table."""
    out, table, items = [], [], []

    def flush():
        if table:
            rows = [r for r in table if not re.fullmatch(r"\|[-|\s]+\|", r)]
            cells = [
                [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", r.strip()[1:-1])]
                for r in rows
            ]
            out.append("<table>")
            out.append("<tr>" + "".join(f"<th>{_inline(c)}</th>" for c in cells[0]) + "</tr>")
            for row in cells[1:]:
                out.append("<tr>" + "".join(f"<td>{_inline(c)}</td>" for c in row) + "</tr>")
            out.append("</table>")
            table.clear()
        if items:
            out.append("<ul>" + "".join(f"<li>{_inline(i)}</li>" for i in items) + "</ul>")
            items.clear()

    for line in md.splitlines():
        if line.startswith("|"):
            table.append(line)
            continue
        if line.startswith("- "):
            items.append(line[2:])
            continue
        flush()
        if line.startswith("## "):
            out.append(f"<h2>{_inline(line[3:])}</h2>")
        elif line.startswith("# "):
            out.append(f"<h1>{_inline(line[2:])}</h1>")
        elif line.strip():
            out.append(f"<p>{_inline(line)}</p>")
    flush()
    return "\n".join(out)


def render_html(markdown_body, title):
    """Render the quote as a self-contained RTL HTML page that prints to A4."""
    return f"""<!DOCTYPE html>
<html dir="rtl" lang="he">
<head>
<meta charset="utf-8">
<title>{html.escape(title)}</title>
<style>
  body {{ font-family: 'Arial Hebrew', 'David', sans-serif; max-width: 800px; margin: 2em auto; padding: 1em; }}
  table {{ border-collapse: collapse; width: 17cm; max-width: 100vw; }}
  th, td {{ border: 1px solid #ccc; padding: 0.5em; text-align: right; }}
  p {{ margin: 0.3em 0; }}
  @media print {{ body {{ margin: 0; padding: 0; }} @page {{ size: A4; margin: 1.5cm; }} }}
</style>
</head>
<body>
{markdown_to_html(markdown_body)}
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

    try:
        charges_vat, warnings = validate(spec)
        line_outputs, subtotal, vat, total = compute_totals(spec["lines"], charges_vat)
    except ValueError as e:
        sys.stderr.write(f"ERROR: {e}\n")
        sys.exit(2)
    markdown = render_markdown(spec, line_outputs, subtotal, vat, total, charges_vat)

    if args.format == "html":
        sys.stdout.write(render_html(markdown, f"Quote {spec['quote_number']}"))
    else:
        sys.stdout.write(markdown)

    for w in warnings:
        sys.stderr.write(f"WARNING: {w}\n")


if __name__ == "__main__":
    main()
