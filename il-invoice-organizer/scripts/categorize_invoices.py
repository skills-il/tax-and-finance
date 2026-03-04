#!/usr/bin/env python3
"""
Israeli Invoice Categorizer

Parses invoice data from JSON input and categorizes expenses per
Tax Authority (Rashut HaMisim) official expense categories.
Calculates VAT amounts, flags compliance issues, and generates
summary reports suitable for accountant review.

Usage:
    python categorize_invoices.py --input invoices.json --output categorized.json
    python categorize_invoices.py --input invoices.json --report
    python categorize_invoices.py --help

Input JSON format:
    [
        {
            "invoice_number": "1001",
            "date": "15/01/2025",
            "vendor_name": "Office Depot Israel",
            "vendor_number": "514567890",
            "description": "Office supplies",
            "total_with_vat": 585.0,
            "stated_vat": 85.0,
            "category_hint": "office"
        },
        ...
    ]
"""

import argparse
import json
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional

# ---------------------------------------------------------------------------
# Israeli VAT constants
# ---------------------------------------------------------------------------
VAT_RATE = 0.17
VAT_DIVISOR = 117  # total * 17 / 117 = VAT amount
VAT_TOLERANCE_NIS = 1.0  # rounding tolerance

# ---------------------------------------------------------------------------
# Tax Authority expense categories (Rashut HaMisim)
# ---------------------------------------------------------------------------
EXPENSE_CATEGORIES = {
    1:  {"he": "חומרי גלם",           "en": "Raw materials"},
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

# Keyword-to-category mapping for auto-categorization
CATEGORY_KEYWORDS = {
    1:  ["raw material", "חומרי גלם", "חומר גלם", "materials", "production"],
    2:  ["subcontract", "קבלן", "קבלני משנה", "freelance", "outsource", "consultant"],
    3:  ["salary", "wages", "שכר", "payroll", "משכורת"],
    4:  ["bituach leumi", "ביטוח לאומי", "national insurance", "nii"],
    5:  ["rent", "שכירות", "lease", "שכ\"ד", "office space"],
    6:  ["insurance", "ביטוח", "polisa", "פוליסה"],
    7:  ["electric", "water", "חשמל", "מים", "arnona", "ארנונה", "utility"],
    8:  ["phone", "internet", "טלפון", "אינטרנט", "cellular", "סלולר", "communication", "תקשורת"],
    9:  ["fuel", "gas", "דלק", "vehicle", "רכב", "car", "parking", "חניה", "toll", "אגרה"],
    10: ["depreciation", "פחת", "amortization"],
    11: ["office", "משרד", "supplies", "stationery", "printing", "הדפסה", "ציוד משרדי"],
    12: [],  # fallback category
}

# Business number prefixes
HP_PREFIXES = ("51", "52")  # Hevra Peratit (private company)
AMUTA_PREFIX = "58"         # Amuta (non-profit / registered association)


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------
@dataclass
class InvoiceRecord:
    """Represents a single parsed and categorized invoice."""
    invoice_number: str
    date: str
    vendor_name: str
    vendor_number: str
    description: str
    total_with_vat: float
    stated_vat: Optional[float]
    calculated_vat: float
    amount_before_vat: float
    category_code: int
    category_name_en: str
    category_name_he: str
    vendor_type: str  # osek_murshe, osek_patur, hp, amuta, unknown
    vat_deductible: bool
    flags: list = field(default_factory=list)


@dataclass
class CategorySummary:
    """Aggregated summary for one expense category."""
    code: int
    name_en: str
    name_he: str
    count: int = 0
    total_before_vat: float = 0.0
    total_vat: float = 0.0
    total_with_vat: float = 0.0


# ---------------------------------------------------------------------------
# Core functions
# ---------------------------------------------------------------------------
def validate_business_number(number: str) -> tuple[bool, str]:
    """
    Validate an Israeli business number (mispar osek / HP / amuta).
    Returns (is_valid, entity_type).

    Israeli business numbers are 9 digits. The check digit is validated
    using a weighted sum algorithm similar to Luhn.
    """
    cleaned = number.strip().replace("-", "")

    if not cleaned.isdigit() or len(cleaned) != 9:
        return False, "unknown"

    # Determine entity type by prefix
    if cleaned.startswith(HP_PREFIXES):
        entity_type = "hp"
    elif cleaned.startswith(AMUTA_PREFIX):
        entity_type = "amuta"
    else:
        entity_type = "osek_murshe"

    # Israeli business number check-digit validation
    # Weights alternate: 1, 2, 1, 2, 1, 2, 1, 2, 1
    weights = [1, 2, 1, 2, 1, 2, 1, 2, 1]
    total = 0
    for digit_char, weight in zip(cleaned, weights):
        product = int(digit_char) * weight
        # Sum the digits of the product (e.g., 14 -> 1 + 4 = 5)
        total += product // 10 + product % 10

    is_valid = total % 10 == 0
    return is_valid, entity_type


def calculate_vat(total_with_vat: float) -> tuple[float, float]:
    """
    Extract VAT from a total amount using the 1/6 rule.
    Israeli VAT: 17%, so VAT = total * 17 / 117.

    Returns (vat_amount, amount_before_vat).
    """
    vat_amount = round(total_with_vat * 17 / VAT_DIVISOR, 2)
    amount_before_vat = round(total_with_vat - vat_amount, 2)
    return vat_amount, amount_before_vat


def categorize_by_description(description: str, category_hint: str = "") -> int:
    """
    Auto-categorize an invoice based on its description and optional hint.
    Returns a category code (1-12).
    """
    search_text = f"{description} {category_hint}".lower()

    for code, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in search_text:
                return code

    return 12  # Default: Other expenses


def process_invoice(raw: dict) -> InvoiceRecord:
    """Process a single raw invoice dict into a categorized InvoiceRecord."""
    total_with_vat = float(raw.get("total_with_vat", 0))
    stated_vat = raw.get("stated_vat")
    if stated_vat is not None:
        stated_vat = float(stated_vat)

    vendor_number = str(raw.get("vendor_number", "")).strip()
    description = raw.get("description", "")
    category_hint = raw.get("category_hint", "")

    # Calculate VAT
    calculated_vat, amount_before_vat = calculate_vat(total_with_vat)

    # Validate business number
    is_valid_bn, vendor_type = validate_business_number(vendor_number)

    # Determine VAT deductibility
    vat_deductible = vendor_type in ("osek_murshe", "hp") and is_valid_bn

    # Categorize
    category_code = categorize_by_description(description, category_hint)
    cat_info = EXPENSE_CATEGORIES.get(category_code, EXPENSE_CATEGORIES[12])

    # Compliance flags
    flags = []

    if not raw.get("invoice_number"):
        flags.append("Missing invoice number")

    if not vendor_number:
        flags.append("Missing vendor business number")
    elif not is_valid_bn:
        flags.append(f"Invalid business number: {vendor_number}")

    if not raw.get("date"):
        flags.append("Missing invoice date")
    else:
        try:
            inv_date = datetime.strptime(raw["date"], "%d/%m/%Y")
            if inv_date > datetime.now():
                flags.append(f"Future-dated invoice: {raw['date']}")
        except ValueError:
            flags.append(f"Invalid date format: {raw['date']} (expected DD/MM/YYYY)")

    if stated_vat is not None and abs(stated_vat - calculated_vat) > VAT_TOLERANCE_NIS:
        flags.append(
            f"VAT mismatch: stated {stated_vat:.2f}, calculated {calculated_vat:.2f}"
        )

    if vendor_type == "osek_patur" and stated_vat and stated_vat > 0:
        flags.append("Osek Patur should not charge VAT")

    # Vehicle expense partial deduction flag
    if category_code == 9:
        flags.append("Vehicle expense: only 2/3 of VAT is deductible for non-commercial vehicles")

    return InvoiceRecord(
        invoice_number=str(raw.get("invoice_number", "")),
        date=str(raw.get("date", "")),
        vendor_name=str(raw.get("vendor_name", "")),
        vendor_number=vendor_number,
        description=description,
        total_with_vat=total_with_vat,
        stated_vat=stated_vat,
        calculated_vat=calculated_vat,
        amount_before_vat=amount_before_vat,
        category_code=category_code,
        category_name_en=cat_info["en"],
        category_name_he=cat_info["he"],
        vendor_type=vendor_type,
        vat_deductible=vat_deductible,
        flags=flags,
    )


def generate_report(records: list[InvoiceRecord]) -> str:
    """Generate a summary report from categorized invoice records."""
    # Build category summaries
    summaries: dict[int, CategorySummary] = {}
    for code, info in EXPENSE_CATEGORIES.items():
        summaries[code] = CategorySummary(
            code=code, name_en=info["en"], name_he=info["he"]
        )

    total_vat = 0.0
    non_deductible_vat = 0.0
    all_flags = []

    for rec in records:
        s = summaries[rec.category_code]
        s.count += 1
        s.total_before_vat += rec.amount_before_vat
        s.total_with_vat += rec.total_with_vat
        s.total_vat += rec.calculated_vat
        total_vat += rec.calculated_vat

        if not rec.vat_deductible:
            non_deductible_vat += rec.calculated_vat
        elif rec.category_code == 9:
            # Vehicle: only 2/3 deductible
            non_deductible_vat += rec.calculated_vat / 3

        for flag_msg in rec.flags:
            all_flags.append(f"  ! Invoice #{rec.invoice_number}: {flag_msg}")

    deductible_vat = total_vat - non_deductible_vat

    lines = []
    lines.append("=" * 60)
    lines.append("  Invoice Summary Report / דוח סיכום חשבוניות")
    lines.append("=" * 60)
    lines.append(f"  Total invoices processed: {len(records)}")
    lines.append("")
    lines.append("--- Expense Breakdown by Category ---")
    lines.append(f"  {'Category':<25} | {'Count':>5} | {'Before VAT':>12} | {'VAT':>10} | {'Total':>12}")
    lines.append(f"  {'-'*25}-+-{'-'*5}-+-{'-'*12}-+-{'-'*10}-+-{'-'*12}")

    for code in sorted(summaries.keys()):
        s = summaries[code]
        if s.count == 0:
            continue
        lines.append(
            f"  {s.name_en:<25} | {s.count:>5} | {s.total_before_vat:>10,.2f}  | {s.total_vat:>8,.2f}  | {s.total_with_vat:>10,.2f}"
        )

    lines.append("")
    lines.append("--- VAT Summary / סיכום מע\"מ ---")
    lines.append(f"  Total input VAT (mas tsumos):    {total_vat:>10,.2f} NIS")
    lines.append(f"  Non-deductible VAT:              {non_deductible_vat:>10,.2f} NIS")
    lines.append(f"  Net deductible VAT:              {deductible_vat:>10,.2f} NIS")

    if all_flags:
        lines.append("")
        lines.append("--- Flagged Items / פריטים מסומנים ---")
        lines.extend(all_flags)

    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Israeli Invoice Categorizer -- Categorize invoices per Tax Authority expense categories",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example input (invoices.json):
[
    {
        "invoice_number": "1001",
        "date": "15/01/2025",
        "vendor_name": "Office Depot Israel",
        "vendor_number": "514567890",
        "description": "Office supplies and printing",
        "total_with_vat": 585.00,
        "stated_vat": 85.00,
        "category_hint": "office"
    }
]
        """,
    )
    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Path to input JSON file containing invoice data",
    )
    parser.add_argument(
        "--output", "-o",
        help="Path to output JSON file for categorized results",
    )
    parser.add_argument(
        "--report", "-r",
        action="store_true",
        help="Print a human-readable summary report to stdout",
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Only validate invoices without categorizing (exit code 1 if issues found)",
    )

    args = parser.parse_args()

    # Load input
    try:
        with open(args.input, "r", encoding="utf-8") as f:
            raw_invoices = json.load(f)
    except FileNotFoundError:
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {args.input}: {e}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(raw_invoices, list):
        print("Error: Input JSON must be an array of invoice objects", file=sys.stderr)
        sys.exit(1)

    # Process invoices
    records = [process_invoice(inv) for inv in raw_invoices]

    # Check for validation issues
    has_issues = any(rec.flags for rec in records)

    if args.validate_only:
        if has_issues:
            for rec in records:
                for flag_msg in rec.flags:
                    print(f"Invoice #{rec.invoice_number}: {flag_msg}", file=sys.stderr)
            sys.exit(1)
        else:
            print("All invoices passed validation.")
            sys.exit(0)

    # Output categorized JSON
    if args.output:
        output_data = [asdict(rec) for rec in records]
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        print(f"Categorized data written to: {args.output}")

    # Print report
    if args.report or not args.output:
        report = generate_report(records)
        print(report)


if __name__ == "__main__":
    main()
