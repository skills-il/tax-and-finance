#!/usr/bin/env python3
"""
Israeli Invoice Categorizer

Parses invoice data (JSON input), categorizes expenses into 12 working bookkeeping
categories that map onto the income-statement groups an Israeli accountant works with.
The 1-12 numbering is this skill's own convention, NOT an ITA-published code list, so
refer to a category by name rather than by number. Calculates VAT amounts, flags
compliance issues, and generates summary reports.

Usage:
    python categorize_invoices.py --input invoices.json --output categorized.json
    python categorize_invoices.py --input invoices.json --report
    python categorize_invoices.py --input invoices.json --validate
"""

import argparse
import json
import re
import sys
from datetime import datetime, date, timedelta
from decimal import Decimal, ROUND_HALF_UP
from typing import Any

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

VAT_RATE = Decimal("0.18")
VAT_DIVISOR = Decimal("118")
VAT_MULTIPLIER = Decimal("18")
VAT_TOLERANCE_NIS = Decimal("1")

# Allocation-number (מספר הקצאה) thresholds under the Israel Invoice model, on the
# amount BEFORE VAT, keyed to the invoice date. Source: Israel Tax Authority,
# gov.il/he/departments/topics/israel-invoice. 5,000 is the terminal step: nothing
# below it is legislated or announced.
# Substrings identifying a validation issue that BARS the input-VAT deduction,
# as opposed to one that is merely informational. generate_report zeroes the
# deductible VAT of any invoice carrying one of these.
BLOCKING_ISSUE_MARKERS = (
    "מספר הקצאה",
    "six-month input-VAT window",
    "על שם העוסק",
)

# Document types on which no Israeli VAT arises at all, so the gross amount is
# the expense. A חשבונית עסקה is NOT one of these: VAT arises, it is simply not
# deductible until the חשבונית מס is issued.
NO_ISRAELI_VAT_TYPES = ("receipt", "proforma")

# הוצאות אחזקת רכב reach the Regulation 18(b) ladder whatever expense category
# they land in. Keying the ladder on the category alone let "ביטוח רכב" match
# Insurance (6) ahead of Vehicle (9) and take a full deduction.
VEHICLE_RUNNING_COST_KEYWORDS = (
    "רכב", "לרכב", "הרכב", "ברכב", "vehicle", "car", "דלק", "לדלק", "fuel",
    "אופנוע", "motorcycle", "חניה", "parking",
)


def _tokens(text: str) -> set[str]:
    """Whole-word tokens of a description.

    Substring matching is unusable here: רכב is inside רכבת (train) and הרכבת
    (assembly), and car is inside cartridge and cardboard, so a bare `in` test
    dragged train tickets, furniture assembly and toner onto the vehicle ladder.
    """
    return set(re.findall(r"[\w\u0590-\u05FF]+", text.lower()))


def is_vehicle_running_cost(description: str, category: int) -> bool:
    """True when the expense is a vehicle running cost, whatever category it
    landed in. Keying the Regulation 18(b) ladder on the category alone let
    ביטוח רכב match Insurance first and take a full deduction."""
    if category == 9:
        return True
    return bool(_tokens(description) & set(VEHICLE_RUNNING_COST_KEYWORDS))

ALLOCATION_THRESHOLDS = [
    (date(2026, 6, 1), Decimal("5000")),
    (date(2026, 1, 1), Decimal("10000")),
    (date(2025, 1, 1), Decimal("20000")),
    (date(2024, 5, 5), Decimal("25000")),
]

# The standard rate rose from 17% to 18% on 1 January 2025. An invoice dated before
# that carries the legacy rate and must not be checked against 18%.
LEGACY_VAT_CUTOVER = date(2025, 1, 1)
LEGACY_VAT_RATE = Decimal("0.17")


def _parse_invoice_date(invoice):
    """Return the invoice date, or None when absent or malformed."""
    try:
        return datetime.strptime(invoice.get("date", ""), "%d/%m/%Y").date()
    except (ValueError, TypeError):
        return None


def allocation_threshold_for(invoice_date):
    """Threshold in force on the invoice issue date, or None if the model
    did not yet apply. Always keyed to the ISSUE date, never to today."""
    if invoice_date is None:
        return None
    for start, threshold in ALLOCATION_THRESHOLDS:
        if invoice_date >= start:
            return threshold
    return None


def vat_rate_for(invoice_date):
    """The standard rate in force on the invoice date."""
    if invoice_date is not None and invoice_date < LEGACY_VAT_CUTOVER:
        return LEGACY_VAT_RATE
    return VAT_RATE
ROUNDING = ROUND_HALF_UP

# Working expense categories. The 1-12 numbering is this skill's own convention and is
# NOT an ITA-published code list. Refer to a category by name, not by number.
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
    2:  ["קבלן", "קבלני משנה", "subcontract", "outsourc", "freelanc",
         "שירותי פיתוח", "שירותי תכנות", "שירותי ייעוץ"],
    3:  ["שכר", "משכורת", "salary", "wage", "payroll"],
    4:  ["ביטוח לאומי", "national insurance", "bituach leumi", "nii"],
    5:  ["שכירות", "rent", "lease", "השכרה"],
    6:  ["ביטוח", "insurance", "פוליסה", "policy"],
    7:  ["חשמל", "מים", "electricity", "water", "חברת חשמל", "מקורות", "utility"],
    8:  ["תקשורת", "טלפון", "אינטרנט", "סלולר", "phone", "internet", "telecom",
         "cellcom", "partner", "pelephone", "bezeq", "בזק", "סלקום", "פרטנר",
         "פלאפון", "הוט", "שירותי ענן", "ענן", "cloud", "aws", "azure",
         "מנוי תוכנה", "saas", "hosting", "אחסון אתר"],
    9:  ["דלק", "רכב", "fuel", "gas station", "vehicle", "car", "parking", "חניה",
         "sonol", "paz", "delek", "סונול", "פז", "דור אלון", "ten"],
    10: ["פחת", "depreciation", "ציוד", "equipment", "מחשב", "computer",
         "ריהוט", "furniture"],
    11: ["משרד", "office", "ציוד משרדי", "נייר", "טונר", "paper", "toner",
         "stationery", "הדפסה", "printing"],
}

# Business entity type prefixes. NOTE: these are a working heuristic, not a
# sourced registry rule. The prefix narrows the likely entity type; it does not
# establish it, and other company ranges exist. Treat the emitted entity_type as
# a hint, and verify against the Registrar of Companies where it matters.
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
    "transaction_invoice": {
        "he": "חשבונית עסקה",
        "en": "Transaction Invoice",
        "vat_deductible": False,
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
        result["entity_type"] = "hevra_peratit_likely"
        result["entity_type_he"] = 'חברה פרטית (ח"פ), לפי הקידומת'
    elif cleaned.startswith(AMUTA_PREFIX):
        result["entity_type"] = "amuta"
        result["entity_type_he"] = "עמותה, לפי הקידומת"
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

def extract_vat_from_total(total_with_vat: Decimal,
                           rate: Decimal = VAT_RATE) -> dict[str, Decimal]:
    """Extract VAT from a VAT-inclusive total: total * rate / (1 + rate)."""
    vat = (total_with_vat * rate / (Decimal(1) + rate)).quantize(
        Decimal("0.01"), rounding=ROUNDING
    )
    before_vat = total_with_vat - vat
    return {"before_vat": before_vat, "vat": vat, "total": total_with_vat}


def calculate_vat_from_net(amount_before_vat: Decimal,
                           rate: Decimal = VAT_RATE) -> dict[str, Decimal]:
    """Calculate VAT from a net amount (before VAT)."""
    vat = (amount_before_vat * rate).quantize(
        Decimal("0.01"), rounding=ROUNDING
    )
    total = amount_before_vat + vat
    return {"before_vat": amount_before_vat, "vat": vat, "total": total}


def verify_vat(
    stated_before_vat: Decimal | None,
    stated_vat: Decimal | None,
    stated_total: Decimal | None,
    rate: Decimal = VAT_RATE,
) -> dict[str, Any]:
    """
    Verify VAT consistency across stated amounts, at the rate in force on the
    invoice date. Checking a pre-2025 invoice against 18% produces a phantom
    mismatch on an invoice that is perfectly correct at 17%.
    """
    issues: list[str] = []
    calculated: dict[str, Decimal] = {}

    if stated_before_vat is not None and stated_vat is not None:
        expected = (stated_before_vat * rate).quantize(
            Decimal("0.01"), rounding=ROUNDING
        )
        diff = abs(stated_vat - expected)
        if diff > VAT_TOLERANCE_NIS:
            issues.append(
                f"VAT mismatch: net {stated_before_vat} at {rate:.0%} gives "
                f"{expected}, but the invoice states {stated_vat} "
                f"(difference: {diff} NIS)"
            )
        calculated = {"before_vat": stated_before_vat, "vat": stated_vat,
                      "total": stated_before_vat + stated_vat}
        return {"calculated": calculated, "issues": issues}

    if stated_total is not None:
        calc = extract_vat_from_total(stated_total, rate)
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
        calc = calculate_vat_from_net(stated_before_vat, rate)
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
    toks = _tokens(text)

    # Match on whole tokens, and only fall back to a substring for multi-word
    # keywords. A bare substring test put "רכבת" (train) and "cartridge" into
    # the vehicle category, which then dragged them onto the Regulation 18(b)
    # ladder and produced a wrong deduction, not merely a wrong label.
    for cat_code, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            kw = keyword.lower()
            if " " in kw:
                if kw in text:
                    return cat_code
            elif kw in toks:
                return cat_code

    return 12  # Default: Other expenses


def determine_vat_deductibility(invoice: dict[str, Any]) -> dict[str, Any]:
    """
    Determine how much VAT is deductible based on invoice type and category.
    Applies special rules: hospitality/אירוח blocked (Reg 16); the running-cost
    ladder under Reg 18(b), being the Director's determination if any, else two
    thirds where the main use is business and a quarter where it is not; the
    purchase or import of a private vehicle blocked under Reg 14(a); no Israeli
    VAT at all on a foreign supplier or a non-VAT document; otherwise full.
    """
    vat_amount = Decimal(str(invoice.get("vat_amount", 0)))
    category = invoice.get("category_code", 12)
    invoice_type = invoice.get("invoice_type", "tax_invoice")
    type_info = INVOICE_TYPES.get(invoice_type)

    result: dict[str, Any] = {
        "total_vat": vat_amount,
        "deductible_vat": Decimal("0"),
        "non_deductible_vat": vat_amount,
        "deduction_rate": Decimal("0"),
        "rule_applied": None,
    }

    if type_info is None:
        # Fail CLOSED. Defaulting an unrecognised document to "tax invoice"
        # granted a full deduction to anything the taxonomy did not know about,
        # including a חשבונית עסקה spelled any other way.
        result["rule_applied"] = (
            "Unrecognised invoice_type %r: VAT not deducted. Classify it "
            "explicitly before claiming anything" % invoice_type
        )
        return result

    if invoice.get("foreign_supplier", False):
        # A foreign supplier charges no Israeli VAT, so there is nothing to
        # deduct and nothing to report as input VAT. Import VAT is claimed off
        # the רשימון יבוא, and a reverse-charge case needs a חשבונית עצמית.
        result["total_vat"] = Decimal("0")
        result["non_deductible_vat"] = Decimal("0")
        result["rule_applied"] = (
            "Foreign supplier: no Israeli VAT. Claim import VAT off the "
            "רשימון יבוא, or raise a חשבונית עצמית where reverse charge applies"
        )
        return result

    if not type_info["vat_deductible"]:
        result["rule_applied"] = "Invoice type not eligible for VAT deduction"
        return result

    # Check business number presence
    business_number = invoice.get("business_number", "")
    if not business_number:
        result["rule_applied"] = "Missing business number - VAT not deductible"
        return result

    description = invoice.get("description", "").lower()

    # Hospitality / entertainment (אירוח): input VAT NOT deductible per Reg 16
    hospitality_keywords = [
        "אירוח", "מסעדה", "restaurant", "entertainment", "catering",
        "בית קפה", "cafe", "בית מלון", "hotel",
    ]
    business_travel = any(
        kw in description for kw in
        ("נסיעת עבודה", "נסיעת עסקים", "לינה בתפקיד", "business trip",
         "לינת עובד")
    )
    if any(kw in description for kw in hospitality_keywords) and not business_travel:
        result["deductible_vat"] = Decimal("0")
        result["non_deductible_vat"] = vat_amount
        result["deduction_rate"] = Decimal("0")
        result["rule_applied"] = (
            "Hospitality/entertainment (אירוח): input VAT not deductible (Reg 16)"
        )
        return result

    # Vehicle expenses: 2/3 deductible on RUNNING costs of a non-commercial vehicle.
    # VAT on buying/importing a private vehicle is fully non-deductible (Reg 14).
    if (is_vehicle_running_cost(description, category)
            and not invoice.get("commercial_vehicle", False)):
        purchase_keywords = [
            "רכישת רכב", "קניית רכב", "vehicle purchase", "car purchase",
            "רכישה", "יבוא רכב",
        ]
        if invoice.get("vehicle_purchase", False) or any(
            kw in description for kw in purchase_keywords
        ):
            result["deductible_vat"] = Decimal("0")
            result["non_deductible_vat"] = vat_amount
            result["deduction_rate"] = Decimal("0")
            result["rule_applied"] = (
                "Private-vehicle purchase/import: input VAT not deductible (Reg 14)"
            )
            return result
        # Regulation 18(b). The Director's determination governs if there is
        # one. Otherwise two thirds where the MAIN use is business, and only a
        # quarter where it is not. Applying 2/3 to a mainly-private vehicle
        # over-deducts, which is the defect this branch exists to prevent.
        director_share = invoice.get("director_determined_business_share")
        if director_share is not None:
            fraction = Decimal(str(director_share))
            rule = ("Vehicle running cost: Director's determination governs "
                    "(Reg 18(b)(1))")
        elif invoice.get("mainly_business_use") is None:
            # The statute turns on which use PREDOMINATES, and nothing in a
            # receipt reveals that. Deducting two thirds by default over-claims
            # on every mainly-private vehicle, so take the conservative limb
            # and say plainly that an answer is needed.
            fraction = Decimal(1) / Decimal(4)
            rule = ("Vehicle running cost: main use NOT stated, so the "
                    "conservative 1/4 limb was applied (Reg 18(b)(3)). Set "
                    "mainly_business_use to true or false to resolve this")
        elif invoice.get("mainly_business_use"):
            fraction = Decimal(2) / Decimal(3)
            rule = ("Vehicle running cost: 2/3 VAT deductible, main use is "
                    "business (Reg 18(b)(2))")
        else:
            fraction = Decimal(1) / Decimal(4)
            rule = ("Vehicle running cost: 1/4 VAT deductible, main use is NOT "
                    "business (Reg 18(b)(3))")
        deductible = (vat_amount * fraction).quantize(
            Decimal("0.01"), rounding=ROUNDING
        )
        result["deductible_vat"] = deductible
        result["non_deductible_vat"] = vat_amount - deductible
        result["deduction_rate"] = fraction.quantize(Decimal("0.0001"))
        result["rule_applied"] = rule
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

    # Light in-house refreshments (כיבוד קל) are 80% deductible for income tax.
    kibud_keywords = ["כיבוד", "refreshment"]
    for kw in kibud_keywords:
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
                    "Light refreshments (כיבוד קל): 80% deductible for income tax"
                ),
            }

    # Client hospitality/entertainment (אירוח) is generally NOT income-tax deductible.
    hospitality_keywords = [
        "אירוח", "ארוחה", "מסעדה", "entertainment", "meal",
        "restaurant", "catering",
    ]
    for kw in hospitality_keywords:
        if kw in description:
            return {
                "total": total,
                "deductible_amount": Decimal("0"),
                "non_deductible_amount": total,
                "deduction_rate": Decimal("0"),
                "rule_applied": (
                    "Hospitality/entertainment (אירוח): generally not income-tax "
                    "deductible - flag for accountant"
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
        invoice.get(f) is not None
        for f in ["total_with_vat", "amount_before_vat"]
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
        if invoice.get("amount_before_vat") is not None else None
    )
    stated_vat = (
        Decimal(str(invoice["vat_amount"]))
        if invoice.get("vat_amount") is not None else None
    )
    stated_total = (
        Decimal(str(invoice["total_with_vat"]))
        if invoice.get("total_with_vat") is not None else None
    )

    # Skip the VAT cross-check where the document carries no Israeli VAT at all:
    # comparing a foreign or non-VAT document against an 18% extraction produces
    # a mismatch on a document that is perfectly correct.
    carries_no_vat = (
        invoice.get("foreign_supplier", False)
        or invoice.get("invoice_type", "tax_invoice") in NO_ISRAELI_VAT_TYPES
    )
    if (stated_total is not None or stated_before is not None) and not carries_no_vat:
        vat_result = verify_vat(stated_before, stated_vat, stated_total,
                                vat_rate_for(_parse_invoice_date(invoice)))
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

    # 4b. Six-month deduction window, section 38(א) of the VAT Law. The
    #     checklist marks this a Must-cover export flag and it was never coded,
    #     so a batch could quietly include VAT that is no longer freely
    #     reclaimable.
    inv_date = _parse_invoice_date(invoice)
    if inv_date is not None:
        # Six CALENDAR months, not 183 days. A day count leaves a short window
        # each month in which an invoice is already out of time under §38(א)
        # and is not flagged.
        y, m = inv_date.year, inv_date.month + 6
        y, m = y + (m - 1) // 12, (m - 1) % 12 + 1
        try:
            deadline = inv_date.replace(year=y, month=m)
        except ValueError:  # e.g. 31 August + 6 months
            deadline = (inv_date.replace(year=y, month=m, day=1)
                        + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        if date.today() > deadline:
            issues.append(
                f"Invoice #{inv_num}: the six-month input-VAT window in "
                f"section 38(א) closed on {deadline.strftime('%d/%m/%Y')}. "
                "The VAT is no longer freely deductible and needs VAT-office "
                "approval. Note this is measured against today, so re-running "
                "an archived batch will flag invoices that were deducted in time"
            )

    # 4c. The invoice must be issued to the claiming business (על שם העוסק).
    #     SKILL.md calls this the most common reason an accountant disallows an
    #     invoice, and it had no check at all.
    claimant = str(invoice.get("claiming_business_number", "") or "").replace("-", "").strip()
    addressed = str(invoice.get("customer_business_number", "") or "").replace("-", "").strip()
    if claimant and addressed and claimant != addressed:
        issues.append(
            f"Invoice #{inv_num}: addressed to {addressed}, but the claiming "
            f"business is {claimant}. An invoice not issued על שם העוסק does "
            "not support an input-VAT deduction under section 38(א)"
        )

    # 5. Allocation number (מספר הקצאה), Israel Invoice model.
    #    The threshold is the one in force on the ISSUE date, not today's.
    #    Missing it does not make the invoice invalid; it blocks the BUYER's
    #    input-VAT deduction (כתנאי לניכוי מס התשומות).
    if not invoice.get("allocation_number"):
        inv_date = _parse_invoice_date(invoice)
        threshold = allocation_threshold_for(inv_date)
        net = invoice.get("amount_before_vat")
        if net is None and invoice.get("total_with_vat"):
            rate = vat_rate_for(inv_date)
            net = Decimal(str(invoice["total_with_vat"])) / (Decimal(1) + rate)
        if (threshold is not None and net is not None
                and Decimal(str(net)) > threshold
                and invoice.get("invoice_type", "tax_invoice") in (
                    "tax_invoice", "tax_invoice_receipt")
                and not invoice.get("foreign_supplier", False)):
            issues.append(
                f"Invoice #{inv_num}: missing allocation number "
                f"(מספר הקצאה). Net {Decimal(str(net)).quantize(Decimal('0.01'))} "
                f"NIS is above the {threshold} NIS threshold in force on "
                f"{invoice.get('date')}. The invoice is still a valid document, "
                "but the input VAT is not deductible until the supplier "
                "supplies an allocation number"
            )
        elif (threshold is not None and net is None
              and invoice.get("invoice_type", "tax_invoice") in (
                  "tax_invoice", "tax_invoice_receipt")
              and not invoice.get("foreign_supplier", False)):
            issues.append(
                f"Invoice #{inv_num}: no amount available, so the allocation "
                f"number could not be tested against the {threshold} NIS "
                "threshold in force. Supply amount_before_vat or "
                "total_with_vat before relying on this batch"
            )
        elif invoice.get("e_invoice_required", False):
            issues.append(
                f"Invoice #{inv_num}: allocation number (מספר הקצאה) missing "
                "on an invoice flagged as requiring one"
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

    # Calculate/verify VAT.
    # Test against None, not truthiness: a legitimate 0.00 invoice is falsy and
    # was previously reported as "missing amount fields".
    def _dec(key):
        v = result.get(key)
        return Decimal(str(v)) if v is not None else None

    stated_total = _dec("total_with_vat")
    stated_before = _dec("amount_before_vat")
    stated_vat = _dec("vat_amount")

    inv_date = _parse_invoice_date(result)
    rate = vat_rate_for(inv_date)
    result["vat_rate_applied"] = float(rate)

    # No Israeli VAT to extract at all: a foreign supplier charges none, and a
    # plain receipt (the Osek Patur case) is not a VAT document. Extracting it
    # anyway put a fabricated figure into the accountant-facing input-VAT total
    # even though it was correctly excluded from the DEDUCTIBLE total.
    # "No Israeli VAT arises at all" (foreign supplier, plain receipt) is a
    # DIFFERENT case from "VAT arises but is not deductible on this document"
    # (a חשבונית עסקה awaiting its חשבונית מס). Only the first folds VAT into
    # the expense; the second must still split the amount.
    inv_type = result.get("invoice_type", "tax_invoice")
    carries_no_vat = (
        result.get("foreign_supplier", False)
        or inv_type in NO_ISRAELI_VAT_TYPES
    )
    if carries_no_vat:
        # Zero it whether or not the document shows a VAT line. A foreign
        # supplier's invoice routinely carries EU VAT or US sales tax, and
        # carrying that number through booked it as Israeli input VAT.
        if stated_vat is not None and stated_vat != 0:
            result["foreign_or_non_vat_amount_ignored"] = float(stated_vat)
        result["vat_amount"] = 0.0
        if stated_before is None and stated_total is not None:
            result["amount_before_vat"] = float(stated_total)
    elif stated_total is not None and stated_vat is None:
        calc = extract_vat_from_total(stated_total, rate)
        result["vat_amount"] = float(calc["vat"])
        result["amount_before_vat"] = float(calc["before_vat"])
    elif stated_before is not None and stated_total is None and stated_vat is None:
        calc = calculate_vat_from_net(stated_before, rate)
        result["vat_amount"] = float(calc["vat"])
        result["total_with_vat"] = float(calc["total"])
    elif stated_before is not None and stated_total is None and stated_vat is not None:
        # Do NOT overwrite the supplier's stated VAT. Deriving the total from
        # what the document actually says leaves the discrepancy visible to
        # validate_invoice instead of erasing it.
        result["total_with_vat"] = float(stated_before + stated_vat)
    elif stated_total is not None and stated_vat is not None and stated_before is None:
        # Both total and VAT given. Derive the net rather than leaving it at
        # zero, which silently broke every category total.
        result["amount_before_vat"] = float(stated_total - stated_vat)

    # A credit invoice (חשבונית זיכוי) reverses the original. Carry it as a
    # negative so it SUBTRACTS from the reclaim instead of adding to it.
    if result.get("invoice_type") == "credit_invoice":
        for key in ("total_with_vat", "amount_before_vat", "vat_amount"):
            if result.get(key) is not None and result[key] > 0:
                result[key] = -abs(result[key])

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

    blocked_by_flags = Decimal("0")
    excluded_docs: list[str] = []

    for inv in invoices:
        # A proforma is a quotation, not a document. Including it inflated the
        # expense total handed to the accountant by its full face value.
        if inv.get("invoice_type") == "proforma":
            excluded_docs.append(
                "%s (%s): proforma, excluded from the totals"
                % (inv.get("invoice_number", "?"),
                   INVOICE_TYPES["proforma"]["he"])
            )
            continue

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
        deductible = Decimal(str(inv.get("deductible_vat", 0)))
        non_deductible = Decimal(str(inv.get("non_deductible_vat", 0)))

        # The allocation-number gate blocks the deduction. Reporting that VAT
        # inside "net deductible" while flagging it as blocked on the same page
        # overstated the reclaim, and the two halves of the printout disagreed.
        # Any flag that bars the deduction must move the number, not just
        # print. Keying this off one marker string is what let the six-month
        # and name-mismatch checks be cosmetic.
        blockers = [i for i in inv.get("validation_issues", [])
                    if any(m in i for m in BLOCKING_ISSUE_MARKERS)]
        # Never block a NEGATIVE deductible. A credit note reduces input tax
        # already claimed, and that reduction is owed whatever the document's
        # age or paperwork. Zeroing it deleted the reversal and INCREASED the
        # reclaim, which is the opposite of what blocking is for.
        if blockers and deductible > 0:
            blocked_by_flags += deductible
            non_deductible += deductible
            deductible = Decimal("0")

        total_deductible_vat += deductible
        total_non_deductible_vat += non_deductible

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
        f'Total VAT on documents (ברוטו):       '
        f"{total_vat:>12,.2f} NIS"
    )
    lines.append(
        f"Non-deductible VAT (לא ניתן לניכוי):   "
        f"{total_non_deductible_vat:>12,.2f} NIS"
    )
    if blocked_by_flags:
        lines.append(
            f"  of which blocked by a flag below:     "
            f"{blocked_by_flags:>12,.2f} NIS"
        )
    net_deductible = total_deductible_vat
    lines.append(
        f'Net deductible VAT (מס תשומות לניכוי): '
        f"{net_deductible:>12,.2f} NIS"
    )
    lines.append("")
    if excluded_docs:
        lines.append("--- Excluded from the totals / לא נכללו בסיכום ---")
        for d in excluded_docs:
            lines.append(f"- {d}")
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
            "working bookkeeping categories, calculate VAT, and generate reports."
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
        if args.format == "text":
            for inv in processed:
                print(
                    "%-12s %-10s %-28s net=%10s vat=%9s deductible=%9s  %s" % (
                        inv.get("invoice_number", "?"),
                        inv.get("date", "?"),
                        (inv.get("category_name_en") or "")[:28],
                        inv.get("amount_before_vat"),
                        inv.get("vat_amount"),
                        inv.get("deductible_vat"),
                        inv.get("vat_deduction_rule") or "",
                    )
                )
        else:
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
