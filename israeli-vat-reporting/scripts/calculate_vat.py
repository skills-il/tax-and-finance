#!/usr/bin/env python3
"""Calculate Israeli VAT liability for periodic reporting.

Computes net VAT from sales (output) and purchase (input) records,
applies Israeli deduction rules, checks the allocation-number condition on
input invoices, and maps results to the periodic VAT return fields.

Amounts are pre-VAT by default. A record with "vat_included": true (or the
--inclusive flag) is treated as a VAT-inclusive gross amount and split back
into base and VAT (base = gross / 1.18). When the invoice prints its VAT, pass
it as "vat" so the script uses the document's figure (VAT Law s.38(a) deducts
the tax CONTAINED in the invoice). A purchase document that carries no Israeli
VAT (osek patur receipt, foreign supplier, exempt or zero-rated purchase) takes
"vat_type": "none" and is never deducted.

Purchase records may carry "supplier", "invoice" (the supplier's invoice number,
shared by the lines of one invoice: the allocation threshold is tested on the whole
invoice), "date" (YYYY-MM-DD),
"allocation_number", and "extension_approved" (deduction window extended).
Lines are one invoice only when "supplier", "invoice" and "date" all match. A record
that is a total of several documents takes "aggregate": true (the --purchases total
is one): the per-invoice checks then do not run and a warning is printed.

Usage:
    python scripts/calculate_vat.py --sales 100000 --purchases 60000
    python scripts/calculate_vat.py --sales 118000 --purchases 70800 --inclusive
    python scripts/calculate_vat.py --json transactions.json
    python scripts/calculate_vat.py --example
"""

import json
import argparse
from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from typing import Optional


VAT_RATE = Decimal("0.18")  # 18% standard Israeli VAT rate (effective 1 January 2025)
AGORA = Decimal("0.01")
SHEKEL = Decimal("1")

# Non-deductible expense categories
# private_car_purchase: VAT Regulations reg. 14 (buying/importing a private car)
# entertainment: reg. 16 (except entertaining a person from abroad)
# employee_benefit: reg. 15A (meals, gifts, housing for employees/owners) unless sold to them as a reported transaction
NON_DEDUCTIBLE = {"entertainment", "private_car_purchase", "employee_benefit"}

# Actual, determinable business share (reg. 18(a)); needs "business_ratio" (0..1).
ACTUAL_SHARE = "actual_business_share"

# Partially deductible categories (reg. 18(b), mixed use, no Director ratio)
PARTIAL_DEDUCTIBLE = {
    "vehicle_running_mainly_business": Decimal(2) / Decimal(3),  # running costs only (fuel, upkeep)
    "vehicle_running_mainly_private": Decimal(1) / Decimal(4),   # running costs only
    "mixed_use_mainly_business": Decimal(2) / Decimal(3),        # other mixed-use inputs
    "mixed_use_mainly_private": Decimal(1) / Decimal(4),
}

# Fully deductible categories (anything else is rejected, not silently deducted).
FULL_DEDUCTIBLE = {"general", "equipment", "rent", "services", "inventory"}
# Only when the Director has set a ratio for this dealer; needs "director_ratio" (0..1).
DIRECTOR_RATIO = "director_set_ratio"

SALE_TYPES = {"standard", "zero_rated", "export", "exempt"}

# Allocation-number (mispar haktzaa) condition for deducting input VAT, by invoice date.
# The buyer may not deduct input VAT on a tax invoice whose pre-VAT amount is ABOVE the
# threshold unless it carries a number allocated by the Tax Authority (VAT Law s.38(a1)).
# (start date, threshold in NIS before VAT). No further step-down is scheduled after 5,000.
ALLOCATION_SCHEDULE = [
    (date(2024, 5, 5), Decimal("25000")),
    (date(2025, 1, 1), Decimal("20000")),
    (date(2026, 1, 1), Decimal("10000")),
    (date(2026, 6, 1), Decimal("5000")),
]


def q(value: Decimal, unit: Decimal = AGORA) -> Decimal:
    """Round half up (0.005 -> 0.01), never banker's rounding."""
    return value.quantize(unit, rounding=ROUND_HALF_UP)


def dec(value) -> Decimal:
    """Convert a JSON/CLI number to Decimal without binary-float noise."""
    if isinstance(value, bool):
        raise ValueError("amount must be a number")
    return Decimal(str(value))


def as_bool(value, name: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{name} must be true or false (JSON boolean), got {value!r}")
    return value


def split_amount(record: dict, inclusive_default: bool) -> tuple[Decimal, Decimal]:
    """Return (base excluding VAT, VAT) for a standard-rated record.

    If the record states the VAT printed on the document ("vat"), that figure is used.
    Pre-VAT amount: VAT = base x 18%.
    VAT-inclusive amount: base = gross / 1.18 (rounded to the agora), VAT = gross - base,
    so base + VAT always equals the gross the user typed.
    """
    amount = dec(record.get("amount", 0))
    inclusive = as_bool(record.get("vat_included", inclusive_default), "vat_included")
    if record.get("vat") is not None:
        vat = dec(record["vat"])
        return (amount - vat if inclusive else amount), vat
    if inclusive:
        base = q(amount / (1 + VAT_RATE))
        return base, amount - base
    return amount, q(amount * VAT_RATE)


def allocation_threshold(on: date) -> Optional[Decimal]:
    """Threshold in force on an invoice date, or None before the regime started."""
    current = None
    for start, threshold in ALLOCATION_SCHEDULE:
        if on >= start:
            current = threshold
    return current


def parse_date(value) -> Optional[date]:
    if not value:
        return None
    try:
        return date.fromisoformat(str(value))
    except ValueError:
        raise ValueError(f"Invalid date {value!r}, use YYYY-MM-DD")


@dataclass
class VATReport:
    """Israeli periodic VAT return structure."""
    period: str = ""
    taxable_sales_base: Decimal = Decimal(0)    # taxable sales, net base EXCLUDING VAT
    zero_rated_sales: Decimal = Decimal(0)
    exempt_sales: Decimal = Decimal(0)
    output_vat: Decimal = Decimal(0)
    equipment_inputs_base: Decimal = Decimal(0)  # working figure
    other_inputs_base: Decimal = Decimal(0)      # working figure
    equipment_input_vat: Decimal = Decimal(0)
    other_input_vat: Decimal = Decimal(0)
    input_vat_claimed: Decimal = Decimal(0)
    net_vat: Decimal = Decimal(0)
    adjustments: Decimal = Decimal(0)
    amount_due: Decimal = Decimal(0)
    held: list = field(default_factory=list)      # inputs NOT deducted, with reason
    warnings: list = field(default_factory=list)
    notes: list = field(default_factory=list)


def calculate_output_vat(sales: list[dict], inclusive_default: bool = False):
    """Return (taxable_base_excl_vat, zero_rated, exempt, output_vat)."""
    taxable_base = Decimal(0)
    zero_rated = Decimal(0)
    exempt = Decimal(0)
    output_vat = Decimal(0)

    for sale in sales:
        sale_type = sale.get("type", "standard")
        if sale_type not in SALE_TYPES:
            raise ValueError(f"Unknown sale type: {sale_type!r} (use one of {sorted(SALE_TYPES)})")

        if sale_type in ("zero_rated", "export"):
            zero_rated += dec(sale.get("amount", 0))  # no VAT inside a zero-rated amount
        elif sale_type == "exempt":
            exempt += dec(sale.get("amount", 0))
        else:
            base, vat = split_amount(sale, inclusive_default)
            taxable_base += base
            output_vat += vat

    return taxable_base, zero_rated, exempt, output_vat


def period_bounds(period: str) -> Optional[tuple[date, date]]:
    """'2026-10' -> (1.10.2026, 31.10.2026); bi-monthly '2026-09-10' -> (1.9.2026, 31.10.2026)."""
    parts = period.split("-")
    try:
        year, first, last = int(parts[0]), int(parts[1]), int(parts[-1])
        start = date(year, first, 1)
        nxt = date(year + (last // 12), last % 12 + 1, 1)
    except (ValueError, IndexError):
        return None
    return start, date.fromordinal(nxt.toordinal() - 1)


def add_months(d: date, months: int) -> date:
    m = d.month - 1 + months
    y, m = d.year + m // 12, m % 12 + 1
    for day in (d.day, 30, 29, 28):
        try:
            return date(y, m, day)
        except ValueError:
            continue
    raise ValueError(d)


def invoice_key(p: dict):
    """Lines belong to one invoice only when supplier, invoice number and date all match.

    Invoice numbers are sequential PER SUPPLIER, so "1001" from two suppliers is two
    invoices. Without a "supplier" field, lines are merged only when the date matches too.
    """
    inv = p.get("invoice")
    if inv is None:
        return None
    return (str(p.get("supplier", "")).strip().lower(), str(inv), str(p.get("date", "")))


def has_no_vat(p: dict) -> bool:
    if p.get("vat_type", "standard") == "none":
        return True
    return p.get("vat") is not None and dec(p["vat"]) == 0


def invoice_groups(purchases: list[dict]) -> dict:
    """Per invoice key: pre-VAT total of its taxable lines (all categories), whether any
    line carries an allocation number, and whether it also has no-VAT lines."""
    groups: dict = {}
    for p in purchases:
        key = invoice_key(p)
        if key is None:
            continue
        g = groups.setdefault(key, {"total": Decimal(0), "number": None, "mixed": False, "numbers": set(), "lines": 0})
        g["lines"] += 1
        if p.get("allocation_number"):
            g["numbers"].add(str(p["allocation_number"]).strip())
            g["number"] = g["number"] or str(p["allocation_number"]).strip()
        if has_no_vat(p):
            g["mixed"] = True
            continue
        base, _ = split_amount(p, p.get("_inclusive_default", False))
        if base > 0:
            g["total"] += base
    return groups


def label_of(purchase: dict) -> str:
    return str(purchase.get("description") or purchase.get("invoice") or "purchase")


def hold_reason(purchase: dict, base: Decimal, group: Optional[dict],
                report: VATReport, bounds) -> Optional[str]:
    """Return a reason to HOLD (not deduct) this input, or None. Adds warnings as it goes."""
    label = label_of(purchase)
    number = purchase.get("allocation_number") or (group or {}).get("number")
    if purchase.get("allocation_number"):
        digits = str(purchase["allocation_number"]).strip()
        if not digits.isdigit() or not 9 <= len(digits) <= 30:
            report.warnings.append(
                f"{label}: allocation number {digits!r} is not 9 to 30 digits; check it against the invoice")
    invoice_date = parse_date(purchase.get("date"))
    if bounds and invoice_date and invoice_date > bounds[1]:
        kind = "credit note" if base < 0 else "document"
        return (f"{label}: {kind} dated {invoice_date}, after the end of the period; it belongs in the return "
                f"for the period in which it was issued or received (s.69(c), reg. 24(b))")
    if base < 0:
        return None  # a credit note needs no number and is not subject to the six-month window
    if purchase.get("aggregate"):
        report.warnings.append(
            f"{label}: a total of several documents, so the per-invoice checks did not run; confirm every "
            f"invoice in it above NIS 5,000 before VAT (from 1 June 2026) carries an allocation number")
        return None
    measured = group["total"] if group is not None else base
    if invoice_date is None:
        if measured > ALLOCATION_SCHEDULE[-1][1] and not number:
            return (f"{label}: no invoice date and no allocation number on an invoice of "
                    f"{measured:,.2f} NIS before VAT; held under the current NIS 5,000 threshold. "
                    f"Add the date if it is earlier than 1 June 2026, or mark a multi-invoice total as aggregate")
        report.warnings.append(f"{label}: no invoice date, so the six-month window was not checked")
        return None
    threshold = allocation_threshold(invoice_date)
    if threshold is not None and measured > threshold and not number:
        whole = " (whole invoice)" if group is not None else ""
        return (f"{label}: invoice of {measured:,.2f} NIS before VAT{whole} dated {invoice_date} is above "
                f"the {threshold:,.0f} NIS allocation threshold and has no allocation number")
    if bounds and not purchase.get("extension_approved"):
        deadline = add_months(invoice_date, 6)
        if bounds[1] > deadline:
            report.warnings.append(
                f"{label}: dated {invoice_date}; six months from the document date ended {deadline}, before "
                f"this period ended. Input VAT must be deducted within six months (s.38(a)), so confirm with "
                f"your accountant that it is still in time, or set extension_approved if the Director extended it")
    return None


def calculate_input_vat(purchases: list[dict], report: VATReport, inclusive_default: bool = False):
    """Return (equipment_base, other_base, equipment_vat, other_vat).

    Deduction rules: private car purchase, entertainment and employee benefits are not
    deductible (regs. 14, 16, 15A); an actual determinable business share is deducted
    at that share (reg. 18(a)); otherwise mixed-use costs 2/3 or 1/4 (reg. 18(b));
    director_set_ratio uses the ratio the Director set. Documents with no Israeli VAT
    are skipped. Inputs are HELD (not deducted) when an invoice above the allocation
    threshold has no allocation number (s.38(a1)) or when the document is dated after
    the period (s.69(c)). Documents past six months are flagged, not held (s.38(a)).
    """
    equipment_base = Decimal(0)
    other_base = Decimal(0)
    equipment_vat = Decimal(0)
    other_vat = Decimal(0)
    bounds = period_bounds(report.period) if report.period else None
    if report.period and bounds is None:
        report.warnings.append(f"period {report.period!r} not understood (use 2026-10 or 2026-09-10); "
                               f"period and six-month checks were skipped")
    for p in purchases:
        p["_inclusive_default"] = inclusive_default
    groups = invoice_groups(purchases)
    for key, g in groups.items():
        if len(g["numbers"]) > 1:
            report.warnings.append(f"invoice {key[1]!r}: its lines carry different allocation numbers {sorted(g['numbers'])}")
        if g["mixed"] and g["total"] > 0:
            report.warnings.append(
                f"invoice {key[1]!r}: mixes lines with and without VAT; the allocation threshold may be measured "
                f"on the whole invoice including the no-VAT lines, so confirm with your accountant")
    seen: dict = {}
    for p in purchases:
        if p.get("invoice") is None or dec(p.get("amount", 0)) < 0:
            continue  # credit notes naturally carry a later date
        seen.setdefault(str(p["invoice"]), set()).add((str(p.get("supplier", "")).strip().lower(), str(p.get("date", ""))))
    for inv, variants in seen.items():
        if len(variants) > 1:
            report.warnings.append(
                f"invoice {inv!r}: lines differ in supplier or date, so they were treated as separate invoices; "
                f"if they are one invoice, give every line the same supplier and date")
    for key, g in groups.items():
        if key[0] == "" and g["lines"] > 1:
            report.warnings.append(
                f"invoice {key[1]!r}: no supplier given, so lines with this number and date were treated as one "
                f"invoice; add supplier if they come from different suppliers")
    held_keys = set()
    computed = 0

    for purchase in purchases:
        category = purchase.get("category", "general")
        label = label_of(purchase)
        if has_no_vat(purchase):
            report.notes.append(f"{label}: no Israeli VAT on the document, nothing to deduct")
            continue
        base, vat = split_amount(purchase, inclusive_default)
        if purchase.get("vat") is None:
            computed += 1
        elif base != 0 and abs(vat - q(base * VAT_RATE)) > 1:
            report.warnings.append(
                f"{label}: stated VAT {vat:,.2f} is not 18% of the base {base:,.2f} (a document dated before 2025 "
                f"carries 17%); check whether the amount "
                f"includes VAT (set vat_included) or the document is mis-keyed")
        is_equipment = bool(purchase.get("equipment")) or category == "equipment"
        if is_equipment and category.startswith("vehicle_running"):
            raise ValueError(
                "A vehicle bought as equipment is a car purchase: use category "
                "'private_car_purchase' (not deductible, reg. 14) unless a reg. 14 "
                "exception applies, in which case consult an accountant")

        if category in NON_DEDUCTIBLE:
            continue  # no VAT deduction, and not reported as a claimed input
        elif category in PARTIAL_DEDUCTIBLE:
            deductible = q(vat * PARTIAL_DEDUCTIBLE[category])
        elif category in (DIRECTOR_RATIO, ACTUAL_SHARE):
            key = "director_ratio" if category == DIRECTOR_RATIO else "business_ratio"
            ratio = purchase.get(key)
            if isinstance(ratio, bool) or not isinstance(ratio, (int, float)) or not 0 <= ratio <= 1:
                raise ValueError(f"{category} purchase needs a numeric {key} between 0 and 1")
            deductible = q(vat * dec(ratio))
        elif category in FULL_DEDUCTIBLE:
            deductible = vat
        else:
            raise ValueError(f"Unknown purchase category: {category!r}")

        ikey = invoice_key(purchase)
        reason = hold_reason(purchase, base, groups.get(ikey) if ikey is not None else None, report, bounds)
        if reason:
            report.held.append(reason)
            if ikey is not None and base > 0:
                held_keys.add((ikey[0], ikey[1]))
            continue

        if is_equipment:
            equipment_base += base
            equipment_vat += deductible
        else:
            other_base += base
            other_vat += deductible

    for purchase in purchases:
        purchase.pop("_inclusive_default", None)
        ikey = invoice_key(purchase)
        if ikey is not None and (ikey[0], ikey[1]) in held_keys and dec(purchase.get("amount", 0)) < 0:
            report.warnings.append(
                f"{label_of(purchase)}: credit note on invoice {purchase['invoice']!r}, whose input VAT is HELD; "
                f"it still reduces input VAT here (reg. 24(b)). Check with your accountant before filing")
    if computed:
        report.warnings.append(
            f"{computed} purchase record(s) had no 'vat' field, so VAT was computed at 18% of the amount. "
            f"Input VAT is the tax shown on the document (s.38(a)): confirm each figure, and mark documents "
            f"with no Israeli VAT as vat_type none")
    return equipment_base, other_base, equipment_vat, other_vat


def prepare_vat_report(
    period: str,
    sales: Optional[list[dict]] = None,
    purchases: Optional[list[dict]] = None,
    adjustments=0,
    inclusive: bool = False,
) -> VATReport:
    """Prepare a complete periodic VAT return draft."""
    report = VATReport(period=period, adjustments=dec(adjustments))
    taxable, zero_rated, exempt, output_vat = calculate_output_vat(sales or [], inclusive)
    eq_base, other_base, eq_vat, other_vat = calculate_input_vat(purchases or [], report, inclusive)

    if exempt > 0:
        report.warnings.append(
            "exempt sales are present: input VAT on inputs used for exempt transactions is not deductible "
            "(s.41), and mixed taxable and exempt activity needs an apportionment, so route it to an accountant")
    report.taxable_sales_base = q(taxable)
    report.zero_rated_sales = q(zero_rated)
    report.exempt_sales = q(exempt)
    report.output_vat = q(output_vat)
    report.equipment_inputs_base = q(eq_base)
    report.other_inputs_base = q(other_base)
    report.equipment_input_vat = q(eq_vat)
    report.other_input_vat = q(other_vat)
    report.input_vat_claimed = q(eq_vat + other_vat)
    report.net_vat = q(report.output_vat - report.input_vat_claimed)
    report.amount_due = q(report.net_vat + report.adjustments)
    return report


def format_report(report: VATReport) -> str:
    """Format VAT report for display: agorot working plus whole-shekel box values.

    Whole-shekel net and payable are computed FROM the rounded boxes, as the form does,
    and the direction label follows that whole-shekel payable.
    """
    w = {k: q(getattr(report, k), SHEKEL) for k in (
        "output_vat", "equipment_input_vat", "other_input_vat", "adjustments")}
    w_input = w["equipment_input_vat"] + w["other_input_vat"]
    w_net = w["output_vat"] - w_input
    w_due = w_net + w["adjustments"]
    if w_due > 0:
        direction = "TO PAY"
    elif w_due < 0:
        direction = "REFUND DUE"
    else:
        direction = "NOTHING TO PAY"

    def row(label, value, whole=None):
        whole = q(value, SHEKEL) if whole is None else whole
        whole = whole + 0  # turn -0 into 0
        return f"  {label:<36}{value:>14,.2f}{whole:>12,.0f}"

    lines = [
        "=== DRAFT calculation for the periodic VAT return (not a filed return) ===",
        f"Period: {report.period}",
        "",
        f"  {'':<36}{'NIS':>14}{'whole NIS':>12}",
        row("Taxable sales (excl VAT)", report.taxable_sales_base),
        row("Output VAT", report.output_vat),
        row("Zero-rated sales", report.zero_rated_sales),
        row("Exempt sales", report.exempt_sales),
        row("Input VAT - equipment/fixed assets", report.equipment_input_vat),
        row("Input VAT - other inputs", report.other_input_vat),
        row("Total input VAT", report.input_vat_claimed, w_input),
        row("Net VAT (output - input)", report.net_vat, w_net),
        row("Adjustments", report.adjustments),
        row("Amount to pay (net + adjustments)", report.amount_due, w_due) + f"  ({direction})",
        "",
        "  Working figures, not return boxes:",
        row("Equipment purchases base (excl VAT)", report.equipment_inputs_base),
        row("Other purchases base (excl VAT)", report.other_inputs_base),
    ]
    if report.held:
        lines += ["", "  HELD, input VAT NOT deducted:"]
        lines += [f"  - {h}" for h in report.held]
    if report.warnings:
        lines += ["", "  Warnings:"]
        lines += [f"  - {x}" for x in report.warnings]
    if report.notes:
        lines += ["", "  Not deducted (no VAT on the document):"]
        lines += [f"  - {x}" for x in report.notes]
    lines += [
        "",
        "NOTE: The whole-NIS column rounds each box half up; whole-NIS net and payable are computed "
        "from the rounded boxes. Working bases exclude non-deductible and held purchases and show "
        "partially deductible ones in full. Verify with your accountant.",
    ]
    return "\n".join(lines)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Calculate Israeli VAT liability for the periodic return")
    parser.add_argument("--sales", type=str, help="Total standard-rated sales (pre-VAT unless --inclusive)")
    parser.add_argument("--purchases", type=str, help="Total fully deductible purchases (pre-VAT unless --inclusive)")
    parser.add_argument("--exports", type=str, default="0", help="Zero-rated export sales")
    parser.add_argument("--period", type=str, default="2026-01", help="Reporting period, e.g. 2026-10 or 2026-09-10")
    parser.add_argument("--adjustments", type=str, default="0", help="Adjustments (signed)")
    parser.add_argument("--inclusive", action="store_true",
                        help="Treat amounts as VAT-inclusive (base = gross / 1.18) unless a record sets vat_included")
    parser.add_argument("--json", type=str, help="JSON file with detailed transactions")
    parser.add_argument("--example", action="store_true", help="Show example calculation")
    args = parser.parse_args()

    if args.example:
        sales = [
            {"amount": 50000, "type": "standard", "description": "Consulting"},
            {"amount": 35400, "type": "standard", "vat_included": True, "description": "Development (VAT-inclusive)"},
            {"amount": 20000, "type": "zero_rated", "description": "Export services"},
        ]
        purchases = [
            {"amount": 15000, "vat": 2700, "category": "rent", "date": "2026-10-01", "allocation_number": "123456789", "description": "Office rent"},
            {"amount": 8000, "vat": 1440, "category": "general", "date": "2026-10-12", "description": "Software licences, no allocation number"},
            {"amount": 4000, "vat": 720, "category": "general", "date": "2026-10-20", "description": "Supplies"},
            {"amount": 6000, "vat": 1080, "category": "equipment", "date": "2026-10-05", "allocation_number": "987654321", "description": "Laptop (fixed asset)"},
            {"amount": 5000, "vat": 900, "category": "vehicle_running_mainly_business", "date": "2026-10-15", "description": "Car running costs"},
            {"amount": 2000, "vat": 360, "category": "entertainment", "date": "2026-10-18", "description": "Client dinner"},
        ]
        print(format_report(prepare_vat_report("2026-10", sales, purchases)))
        return

    if args.json:
        with open(args.json) as f:
            data = json.load(f)
        report = prepare_vat_report(
            data.get("period", args.period),
            data.get("sales", []),
            data.get("purchases", []),
            data.get("adjustments", 0),
            as_bool(data.get("vat_included", args.inclusive), "vat_included"),
        )
        print(format_report(report))
        return

    if args.sales is not None or args.purchases is not None:
        sales = [{"amount": args.sales or 0, "type": "standard"}]
        if dec(args.exports) != 0:
            sales.append({"amount": args.exports, "type": "zero_rated"})
        purchases = []
        if args.purchases is not None:
            purchases = [{"amount": args.purchases, "category": "general", "aggregate": True,
                          "description": "purchases total"}]
        print(format_report(prepare_vat_report(args.period, sales, purchases, args.adjustments, args.inclusive)))
        return

    parser.print_help()


if __name__ == "__main__":
    main()
