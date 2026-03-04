#!/usr/bin/env python3
"""
Israeli Invoice Categorizer

Parses invoice data (JSON input), categorizes expenses per Israeli Tax Authority
(Rashut HaMisim) official categories, calculates VAT amounts, flags compliance
issues, and generates summary reports.

Usage:
    python categorize_invoices.py --input invoices.json --output categorized.json
    python categorize_invoices.py --input invoices.json --report
    python categorize_invoices.py --input invoices.json --validate
"""

import argparse
import json
import re
import sys
from datetime import datetime, date
from decimal import Decimal, ROUND_HALF_UP
from typing import Any

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

VAT_RATE = Decimal("0.17")
VAT_DIVISOR = Decimal("117")
VAT_MULTIPLIER = Decimal("17")
VAT_TOLERANCE_NIS = Decimal("1")
ROUNDING = ROUND_HALF_UP

# Israeli Tax Authority official expense categories
EXPENSE_CATEGORIES: dict[int, dict[str, str]] = {
    1:  {"he": "חומרי גלם",          "en": "Raw materials"},
    2:  {"he": "קבלני משנה",          "en": "Subcontractors"},
    3:  {"he": "שכר עבודה",           "en": "Wages and salaries"},
    4:  {"he": "ביטוח לאומי מעסיק",    "en": "Employer NII"},
    5:  {"he": "שכירות",              "en": "Rent"},
    6:  {"he": "ביטוח",               "en": "Insurance"},
    7:  {"he": "חשמל ומים",           "en": "Utilities"},
    8:  {"he": "תקשורת",              "en": "Communications"},
    9:  {"he": "הוצאות רכב",          "en": "Vehicle expenses"},
    10: {"he": "פחת",                 "en": "Depreciation"},
    11: {"he": "הוצאות משרד",         "en": "Office expenses"},
    12: {"he": "הוצאות אחרות",        "en": "Other expenses"},
}

# Keyword-based category detection (Hebrew and English)
CATEGORY_KEYWORDS: dict[int, list[str]] = {
    1:  ["חומרי גלם", "חומרים", "raw material", "materials", "production supplies"],
    2:  ["קבלן", "קבלני משנה", "subcontract", "outsourc", "freelanc", "שירותי"],
    3:  ["שכר", "משכורת", "salary", "wage", "payroll"],
    4:  ["ביטוח לאומי", "national insurance", "bituach leumi", "nii"],
    5:  ["שכירות", "rent", "lease", "השכרה"],
    6:  ["ביטוח", "insurance", "פוליסה", "policy"],
    7:  ["חשמל", "מים", "electricity", "water", "חברת חשמל", "מקורות", "utility"],
    8:  ["תקשורת", "טלפון", "אינטרנט", "סלולר", "phone", "internet", "telecom",
         "cellcom", "partner", "pelephone", "bezeq", "בזק", "סלקום", "פרטנר",
         "פלאפון", "הוט"],
    9:  ["דלק", "רכב", "fuel", "gas station", "vehicle", "car", "parking", "חניה",
         "sonol", "paz", "delek", "סונול", "פז", "דור אלון", "ten"],
    10: ["פחת", "depreciation", "ציוד", "equipment", "מחשב", "computer",
         "ריהוט", "furniture"],
    11: ["משרד", "office", "ציוד משרדי", "נייר", "טונר", "paper", "toner",
         "stationery", "הדפסה", "printing"],
}

# Business entity type prefixes
HP_PREFIXES = ("51", "52")
AMUTA_PREFIX = "58"

# Invoice document types
INVOICE_TYPES = {
    "tax_invoice": {
        "he": "חשבונית מס",
        "en": "Tax Invoice",
        "vat_deductible": True,
    },
    "tax_invoice_receipt": {
        "he": "חשבונית מס / קבלה",
        "en": "Tax Invoice Receipt",
        "vat_deductible": True,
    },
    "receipt": {
        "he": "קבלה",
        "en": "Receipt",
        "vat_deductible": False,
    },
    "credit_invoice": {
        "he": "חשבונית זיכוי",
        "en": "Credit Invoice",
        "vat_deductible": True,
    },
    "proforma": {
        "he": "חשבונית פרופורמה",
        "en": "Proforma Invoice",
        "vat_deductible": False,
    },
}


# ---------------------------------------------------------------------------
# Business number validation
# ---------------------------------------------------------------------------

def validate_business_number(number: str) -> dict[str, Any]:
    """
    Validate an Israeli business number (9 digits).
    Returns entity type and validity info.

    Israeli business numbers use a Luhn-like check-digit algorithm:
    - Multiply alternating digits by 1 and 2
    - If product > 9, subtract 9
    - Sum all results; valid if total % 10 == 0
    """
    cleaned = re.sub(r"[\s\-]", "", number)
    result: dict[str, Any] = {
        "number": cleaned,
        "valid_format": False,
        "entity_type": None,
        "entity_type_he": None,
        "check_digit_valid": False,
    }

    if not re.match(r"^\d{9}$", cleaned):
        result["error"] = (
            f"Business number must be exactly 9 digits, "
            f"got {len(cleaned)} characters"
        )
        return result

    result["valid_format"] = True

    # Determine entity type from prefix
    if cleaned.startswith(HP_PREFIXES):
        result["entity_type"] = "hevra_peratit"
        result["entity_type_he"] = 'חברה פרטית (ח"פ)'
    elif cleaned.startswith(AMUTA_PREFIX):
        result["entity_type"] = "amuta"
        result["entity_type_he"] = "עמותה"
    else:
        result["entity_type"] = "osek"
        result["entity_type_he"] = "עוסק (מורשה/פטור)"

    # Luhn-like check-digit validation
    total = 0
    for i, ch in enumerate(cleaned):
        digit = int(ch)
        if i % 2 == 0:
            val = digit
        else:
            val = digit * 2
            if val > 9:
                val -= 9
        total += val

    result["check_digit_valid"] = (total % 10 == 0)
    return result


# ---------------------------------------------------------------------------
# VAT calculations
# ---------------------------------------------------------------------------

def extract_vat_from_total(total_with_vat: Decimal) -> dict[str, Decimal]:
    """Extract VAT from a total that includes VAT using the 1/6 rule."""
    vat = (total_with_vat * VAT_MULTIPLIER / VAT_DIVISOR).quantize(
        Decimal("0.01"), rounding=ROUNDING
    )
    before_vat = total_with_vat - vat
    return {"before_vat": before_vat, "vat": vat, "total": total_with_vat}


def calculate_vat_from_net(amount_before_vat: Decimal) -> dict[str, Decimal]:
    """Calculate VAT from a net amount (before VAT)."""
    vat = (amount_before_vat * VAT_RATE).quantize(
        Decimal("0.01"), rounding=ROUNDING
    )
    total = amount_before_vat + vat
    return {"before_vat": amount_before_vat, "vat": vat, "total": total}


def verify_vat(
    stated_before_vat: Decimal | None,
    stated_vat: Decimal | None,
    stated_total: Decimal | None,
) -> dict[str, Any]:
    """
    Verify VAT consistency across stated amounts.
    Returns calculated values and any mismatches.
    """
    issues: list[str] = []
    calculated: dict[str, Decimal] = {}

    if stated_total is not None:
        calc = extract_vat_from_total(stated_total)
        calculated = calc
        if stated_vat is not None:
            diff = abs(stated_vat - calc["vat"])
            if diff > VAT_TOLERANCE_NIS:
                issues.append(
                    f"VAT mismatch: stated {stated_vat}, "
                    f"calculated {calc['vat']} (difference: {diff} NIS)"
                )
        if stated_before_vat is not None:
            diff = abs(stated_before_vat - calc["before_vat"])
            if diff > VAT_TOLERANCE_NIS:
                issues.append(
                    f"Before-VAT mismatch: stated {stated_before_vat}, "
                    f"calculated {calc['before_vat']} (difference: {diff} NIS)"
                )
    elif stated_before_vat is not None:
        calc = calculate_vat_from_net(stated_before_vat)
        calculated = calc
        if stated_vat is not None:
            diff = abs(stated_vat - calc["vat"])
            if diff > VAT_TOLERANCE_NIS:
                issues.append(
                    f"VAT mismatch: stated {stated_vat}, "
                    f"calculated {calc['vat']} (difference: {diff} NIS)"
                )
    else:
        issues.append(
            "Insufficient amount data: need at least "
            "total_with_vat or amount_before_vat"
        )

    return {"calculated": calculated, "issues": issues}


# ---------------------------------------------------------------------------
# Invoice categorization
# ---------------------------------------------------------------------------

def categorize_by_keywords(description: str, vendor_name: str = "") -> int:
    """
    Categorize an invoice based on description and vendor name keywords.
    Returns the category code (1-12). Defaults to 12 (Other) if no match.
    """
    text = f"{description} {vendor_name}".lower()

    for cat_code, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in text:
                return cat_code

    return 12  # Default: Other expenses


def determine_vat_deductibility(invoice: dict[str, Any]) -> dict[str, Any]:
    """
    Determine how much VAT is deductible based on invoice type and category.
    Applies special rules for vehicles (2/3 deductible) and entertainment.
    """
    vat_amount = Decimal(str(invoice.get("vat_amount", 0)))
    category = invoice.get("category_code", 12)
    invoice_type = invoice.get("invoice_type", "tax_invoice")
    type_info = INVOICE_TYPES.get(invoice_type, INVOICE_TYPES["tax_invoice"])

    result: dict[str, Any] = {
        "total_vat": vat_amount,
        "deductible_vat": Decimal("0"),
        "non_deductible_vat": vat_amount,
        "deduction_rate": Decimal("0"),
        "rule_applied": None,
    }

    if not type_info["vat_deductible"]:
        result["rule_applied"] = "Invoice type not eligible for VAT deduction"
        return result

    # Check business number presence
    business_number = invoice.get("business_number", "")
    if not business_number:
        result["rule_applied"] = "Missing business number - VAT not deductible"
        return result

    # Vehicle expenses: only 2/3 deductible for non-commercial vehicles
    if category == 9 and not invoice.get("commercial_vehicle", False):
        deductible = (vat_amount * 2 / 3).quantize(
            Decimal("0.01"), rounding=ROUNDING
        )
        result["deductible_vat"] = deductible
        result["non_deductible_vat"] = vat_amount - deductible
        result["deduction_rate"] = Decimal("0.6667")
        result["rule_applied"] = (
            "Vehicle expense: 2/3 VAT deductible (non-commercial vehicle)"
        )
        return result

    # Standard: full deduction
    result["deductible_vat"] = vat_amount
    result["non_deductible_vat"] = Decimal("0")
    result["deduction_rate"] = Decimal("1")
    result["rule_applied"] = "Standard full VAT deduction"
    return result


def determine_income_tax_deductibility(invoice: dict[str, Any]) -> dict[str, Any]:
    """
    Determine income tax deductibility percentage.
    Entertainment/meals are only 80% deductible for income tax.
    """
    total = Decimal(str(invoice.get("total_with_vat", 0)))
    description = invoice.get("description", "").lower()

    entertainment_keywords = [
        "אירוח", "ארוחה", "מסעדה", "entertainment", "meal",
        "restaurant", "catering", "כיבוד",
    ]

    for kw in entertainment_keywords:
        if kw in description:
            deductible = (total * Decimal("0.80")).quantize(
                Decimal("0.01"), rounding=ROUNDING
            )
            return {
                "total": total,
                "deductible_amount": deductible,
                "non_deductible_amount": total - deductible,
                "deduction_rate": Decimal("0.80"),
                "rule_applied": (
                    "Entertainment/meals: 80% deductible for income tax"
                ),
            }

    return {
        "total": total,
        "deductible_amount": total,
        "non_deductible_amount": Decimal("0"),
        "deduction_rate": Decimal("1"),
        "rule_applied": "Standard full income tax deduction",
    }


# ---------------------------------------------------------------------------
# Invoice validation
# ---------------------------------------------------------------------------

def validate_invoice(invoice: dict[str, Any]) -> list[str]:
    """
    Validate a single invoice against Israeli legal requirements.
    Returns a list of issues found.
    """
    issues: list[str] = []
    inv_num = invoice.get("invoice_number", "N/A")

    # 1. Required fields
    required_fields = [
        "business_name", "business_number", "invoice_number", "date",
    ]
    for field in required_fields:
        if not invoice.get(field):
            issues.append(
                f"Invoice #{inv_num}: Missing required field '{field}'"
            )

    # Need at least one amount field
    has_amounts = any(
        invoice.get(f) for f in ["total_with_vat", "amount_before_vat"]
    )
    if not has_amounts:
        issues.append(
            f"Invoice #{inv_num}: Missing amount fields "
            "(need total_with_vat or amount_before_vat)"
        )

    # 2. Business number validation
    biz_num = invoice.get("business_number", "")
    if biz_num:
        biz_result = validate_business_number(str(biz_num))
        if not biz_result["valid_format"]:
            issues.append(
                f"Invoice #{inv_num}: Invalid business number format - "
                f"{biz_result.get('error', '')}"
            )
        elif not biz_result["check_digit_valid"]:
            issues.append(
                f"Invoice #{inv_num}: Business number check digit "
                "validation failed"
            )

    # 3. VAT verification
    stated_before = (
        Decimal(str(invoice["amount_before_vat"]))
        if invoice.get("amount_before_vat") else None
    )
    stated_vat = (
        Decimal(str(invoice["vat_amount"]))
        if invoice.get("vat_amount") else None
    )
    stated_total = (
        Decimal(str(invoice["total_with_vat"]))
        if invoice.get("total_with_vat") else None
    )

    if stated_total or stated_before:
        vat_result = verify_vat(stated_before, stated_vat, stated_total)
        for issue in vat_result["issues"]:
            issues.append(f"Invoice #{inv_num}: {issue}")

    # 4. Date validation
    date_str = invoice.get("date", "")
    if date_str:
        try:
            inv_date = datetime.strptime(date_str, "%d/%m/%Y").date()
            if inv_date > date.today():
                issues.append(
                    f"Invoice #{inv_num}: Future-dated invoice ({date_str})"
                )
        except ValueError:
            issues.append(
                f"Invoice #{inv_num}: Invalid date format '{date_str}' "
                "(expected DD/MM/YYYY)"
            )

    # 5. E-invoice check (from 2024)
    e_invoice_required = invoice.get("e_invoice_required", False)
    if e_invoice_required and not invoice.get("allocation_number"):
        issues.append(
            f"Invoice #{inv_num}: E-invoice allocation number "
            "(mispar hiktzaot) missing - "
            "required for invoices above threshold since 2024"
        )

    return issues


# ---------------------------------------------------------------------------
# Processing pipeline
# ---------------------------------------------------------------------------

def process_invoice(invoice: dict[str, Any]) -> dict[str, Any]:
    """Process a single invoice: categorize, calculate VAT, validate."""
    result = dict(invoice)

    # Auto-categorize if no category provided
    if "category_code" not in result:
        result["category_code"] = categorize_by_keywords(
            result.get("description", ""),
            result.get("business_name", ""),
        )

    cat_code = result["category_code"]
    cat_info = EXPENSE_CATEGORIES.get(cat_code, EXPENSE_CATEGORIES[12])
    result["category_name_he"] = cat_info["he"]
    result["category_name_en"] = cat_info["en"]

    # Calculate/verify VAT
    stated_total = (
        Decimal(str(result["total_with_vat"]))
        if result.get("total_with_vat") else None
    )
    stated_before = (
        Decimal(str(result["amount_before_vat"]))
        if result.get("amount_before_vat") else None
    )
    stated_vat = (
        Decimal(str(result["vat_amount"]))
        if result.get("vat_amount") else None
    )

    if stated_total and not stated_vat:
        calc = extract_vat_from_total(stated_total)
        result["vat_amount"] = float(calc["vat"])
        result["amount_before_vat"] = float(calc["before_vat"])
    elif stated_before and not stated_total:
        calc = calculate_vat_from_net(stated_before)
        result["vat_amount"] = float(calc["vat"])
        result["total_with_vat"] = float(calc["total"])

    # VAT deductibility
    vat_ded = determine_vat_deductibility(result)
    result["deductible_vat"] = float(vat_ded["deductible_vat"])
    result["non_deductible_vat"] = float(vat_ded["non_deductible_vat"])
    result["vat_deduction_rule"] = vat_ded["rule_applied"]

    # Income tax deductibility
    income_ded = determine_income_tax_deductibility(result)
    result["income_tax_deductible_amount"] = float(
        income_ded["deductible_amount"]
    )
    result["income_tax_deduction_rule"] = income_ded["rule_applied"]

    # Validate
    result["validation_issues"] = validate_invoice(result)

    # Business number info
    biz_num = result.get("business_number", "")
    if biz_num:
        biz_info = validate_business_number(str(biz_num))
        result["entity_type"] = biz_info["entity_type"]
        result["entity_type_he"] = biz_info["entity_type_he"]

    return result


def process_invoices(
    invoices: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Process a list of invoices."""
    return [process_invoice(inv) for inv in invoices]


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def generate_report(
    invoices: list[dict[str, Any]],
    business_name: str = "",
    business_number: str = "",
    period: str = "",
) -> str:
    """Generate a summary report for the accountant."""
    lines: list[str] = []
    lines.append("=" * 60)
    lines.append("Invoice Summary Report / דוח סיכום חשבוניות")
    lines.append("=" * 60)

    if period:
        lines.append(f"Period / תקופה: {period}")
    if business_name:
        lines.append(
            f"Business / עסק: {business_name} | "
            f"Osek Number / מספר עוסק: {business_number}"
        )
    lines.append(f'Total invoices / סה"כ חשבוניות: {len(invoices)}')
    lines.append("")

    # Aggregate by category
    cat_summary: dict[int, dict[str, Any]] = {}
    total_before_vat = Decimal("0")
    total_vat = Decimal("0")
    total_with_vat = Decimal("0")
    total_deductible_vat = Decimal("0")
    total_non_deductible_vat = Decimal("0")
    all_issues: list[str] = []

    for inv in invoices:
        cat = inv.get("category_code", 12)
        if cat not in cat_summary:
            cat_info = EXPENSE_CATEGORIES.get(cat, EXPENSE_CATEGORIES[12])
            cat_summary[cat] = {
                "name_he": cat_info["he"],
                "name_en": cat_info["en"],
                "count": 0,
                "before_vat": Decimal("0"),
                "vat": Decimal("0"),
                "total": Decimal("0"),
            }

        before = Decimal(str(inv.get("amount_before_vat", 0)))
        vat = Decimal(str(inv.get("vat_amount", 0)))
        total = Decimal(str(inv.get("total_with_vat", 0)))

        cat_summary[cat]["count"] += 1
        cat_summary[cat]["before_vat"] += before
        cat_summary[cat]["vat"] += vat
        cat_summary[cat]["total"] += total

        total_before_vat += before
        total_vat += vat
        total_with_vat += total
        total_deductible_vat += Decimal(str(inv.get("deductible_vat", 0)))
        total_non_deductible_vat += Decimal(
            str(inv.get("non_deductible_vat", 0))
        )

        for issue in inv.get("validation_issues", []):
            all_issues.append(issue)

    # Expense breakdown by category
    lines.append(
        "--- Expense Breakdown by Category / פירוט הוצאות לפי קטגוריה ---"
    )
    lines.append(
        f"{'Category':<25} | {'Count':>5} | "
        f"{'Before VAT':>14} | {'VAT':>12} | {'Total':>14}"
    )
    lines.append("-" * 80)

    for cat_code in sorted(cat_summary.keys()):
        s = cat_summary[cat_code]
        lines.append(
            f"{s['name_en']:<25} | {s['count']:>5} | "
            f"{s['before_vat']:>11,.2f} NIS | "
            f"{s['vat']:>9,.2f} NIS | "
            f"{s['total']:>11,.2f} NIS"
        )

    lines.append("-" * 80)
    lines.append(
        f"{'TOTAL':<25} | "
        f"{sum(s['count'] for s in cat_summary.values()):>5} | "
        f"{total_before_vat:>11,.2f} NIS | "
        f"{total_vat:>9,.2f} NIS | "
        f"{total_with_vat:>11,.2f} NIS"
    )
    lines.append("")

    # VAT summary
    lines.append('--- VAT Summary / סיכום מע"מ ---')
    lines.append(
        f'Total input VAT (מע"מ תשומות):        '
        f"{total_vat:>12,.2f} NIS"
    )
    lines.append(
        f"Non-deductible VAT (לא ניתן לניכוי):   "
        f"{total_non_deductible_vat:>12,.2f} NIS"
    )
    net_deductible = total_deductible_vat
    lines.append(
        f'Net deductible VAT (מע"מ נטו לניכוי):  '
        f"{net_deductible:>12,.2f} NIS"
    )
    lines.append("")

    # Flagged items
    if all_issues:
        lines.append("--- Flagged Items / פריטים מסומנים ---")
        for issue in all_issues:
            lines.append(f"! {issue}")
    else:
        lines.append("--- No issues found / לא נמצאו בעיות ---")

    lines.append("")
    lines.append("=" * 60)
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# JSON serialization helper
# ---------------------------------------------------------------------------

class DecimalEncoder(json.JSONEncoder):
    """JSON encoder that handles Decimal objects."""

    def default(self, o: Any) -> Any:
        if isinstance(o, Decimal):
            return float(o)
        return super().default(o)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Israeli Invoice Categorizer - Categorize invoices per "
            "Tax Authority categories, calculate VAT, and generate reports."
        ),
        epilog=(
            "Example: python categorize_invoices.py "
            "--input invoices.json --output categorized.json --report"
        ),
    )
    parser.add_argument(
        "--input", "-i",
        required=True,
        help=(
            "Path to input JSON file containing invoice data. "
            "Expected format: JSON array of invoice objects, or a JSON "
            "object with 'invoices' array and optional 'business_name', "
            "'business_number', 'period' fields."
        ),
    )
    parser.add_argument(
        "--output", "-o",
        help=(
            "Path to output JSON file for categorized results. "
            "If not specified, results are printed to stdout."
        ),
    )
    parser.add_argument(
        "--report", "-r",
        action="store_true",
        help=(
            "Generate a human-readable summary report for the accountant."
        ),
    )
    parser.add_argument(
        "--validate", "-v",
        action="store_true",
        help=(
            "Only validate invoices (no categorization output). "
            "Prints validation issues and exits with code 1 if issues found."
        ),
    )
    parser.add_argument(
        "--format",
        choices=["json", "text"],
        default="json",
        help="Output format for categorized results (default: json).",
    )
    return parser


def load_input(
    path: str,
) -> tuple[list[dict[str, Any]], dict[str, str]]:
    """
    Load invoice data from JSON file.
    Returns (invoices_list, metadata_dict).
    """
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    metadata: dict[str, str] = {}

    if isinstance(data, list):
        return data, metadata
    elif isinstance(data, dict):
        invoices = data.get("invoices", [])
        metadata = {
            "business_name": data.get("business_name", ""),
            "business_number": data.get("business_number", ""),
            "period": data.get("period", ""),
        }
        return invoices, metadata
    else:
        print(f"Error: Unexpected JSON structure in {path}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    # Load input
    invoices, metadata = load_input(args.input)

    if not invoices:
        print("No invoices found in input file.", file=sys.stderr)
        sys.exit(1)

    # Process
    processed = process_invoices(invoices)

    # Validate-only mode
    if args.validate:
        all_issues: list[str] = []
        for inv in processed:
            all_issues.extend(inv.get("validation_issues", []))

        if all_issues:
            print(
                f"Found {len(all_issues)} validation issue(s):\n",
                file=sys.stderr,
            )
            for issue in all_issues:
                print(f"  ! {issue}", file=sys.stderr)
            sys.exit(1)
        else:
            print(f"All {len(processed)} invoices passed validation.")
            sys.exit(0)

    # Output categorized results
    if args.output:
        output_data = {
            "metadata": metadata,
            "invoices": processed,
            "summary": {
                "total_invoices": len(processed),
                "total_issues": sum(
                    len(inv.get("validation_issues", []))
                    for inv in processed
                ),
            },
        }
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(
                output_data, f,
                ensure_ascii=False, indent=2, cls=DecimalEncoder,
            )
        print(f"Categorized {len(processed)} invoices -> {args.output}")
    elif not args.report:
        # Print JSON to stdout
        json.dump(
            processed, sys.stdout,
            ensure_ascii=False, indent=2, cls=DecimalEncoder,
        )
        print()

    # Report
    if args.report:
        report = generate_report(
            processed,
            business_name=metadata.get("business_name", ""),
            business_number=metadata.get("business_number", ""),
            period=metadata.get("period", ""),
        )
        print(report)


if __name__ == "__main__":
    main()
