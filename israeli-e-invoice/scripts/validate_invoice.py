#!/usr/bin/env python3
"""Validate Israeli e-invoice structure and fields.

Checks invoice JSON against SHAAM (Israeli Tax Authority) requirements:
- Required fields presence
- TIN (mispar osek) format and check digit
- Invoice type validity
- VAT calculation accuracy
- Allocation number requirement based on amount threshold

Usage:
    python scripts/validate_invoice.py <invoice.json>
    python scripts/validate_invoice.py --example
"""

import sys
import json
import re
from datetime import datetime, date
from typing import Optional


# Valid Israeli invoice type codes
VALID_INVOICE_TYPES = {
    300: "Tax Invoice (Hashbonit Mas)",
    305: "Tax Invoice / Receipt (Hashbonit Mas / Kabala)",
    310: "Credit Invoice (Hashbonit Zikui)",
    320: "Receipt (Kabala)",
    330: "Proforma Invoice",
    400: "Self-billing Tax Invoice",
}

# Allocation number thresholds (NIS) by date range
ALLOCATION_THRESHOLDS = [
    ("2024-05-01", "2024-12-31", 25000),
    ("2025-01-01", "2025-06-30", 10000),
    ("2025-07-01", "2025-12-31", 5000),
    ("2026-01-01", None, 5000),  # Verify - mandate expanding
]

# Invoice types that require allocation numbers
ALLOCATION_REQUIRED_TYPES = {300, 305, 310}

VAT_RATE = 0.17  # 17% as of 2025


def validate_tin(tin: str) -> bool:
    """Validate Israeli TIN (mispar osek) - 9 digits with Luhn-like check digit.

    Args:
        tin: String of 9 digits representing the Israeli business TIN.

    Returns:
        True if the TIN has valid format and check digit.
    """
    if not re.match(r"^\d{9}$", tin):
        return False
    digits = [int(d) for d in tin]
    weights = [1, 2, 1, 2, 1, 2, 1, 2, 1]
    total = 0
    for d, w in zip(digits, weights):
        product = d * w
        total += product // 10 + product % 10
    return total % 10 == 0


def get_allocation_threshold(invoice_date: str) -> Optional[int]:
    """Get the allocation number threshold for a given date.

    Args:
        invoice_date: Date string in YYYY-MM-DD format.

    Returns:
        Threshold amount in NIS, or None if no threshold applies.
    """
    for start, end, threshold in ALLOCATION_THRESHOLDS:
        if invoice_date >= start:
            if end is None or invoice_date <= end:
                return threshold
    return None


def validate_invoice(invoice: dict) -> list:
    """Validate invoice structure against SHAAM requirements.

    Args:
        invoice: Dictionary with invoice fields.

    Returns:
        List of error strings. Empty list means valid.
    """
    errors = []

    # Check required fields
    required_fields = ["seller_tin", "invoice_type", "date", "total_amount"]
    for field in required_fields:
        if field not in invoice:
            errors.append(f"Missing required field: {field}")

    # Validate seller TIN
    if "seller_tin" in invoice:
        if not validate_tin(str(invoice["seller_tin"])):
            errors.append(
                f"Invalid seller TIN format: {invoice['seller_tin']}. "
                "Must be 9 digits with valid check digit."
            )

    # Validate buyer TIN (optional but must be valid if present)
    if "buyer_tin" in invoice and invoice["buyer_tin"]:
        if not validate_tin(str(invoice["buyer_tin"])):
            errors.append(
                f"Invalid buyer TIN format: {invoice['buyer_tin']}. "
                "Must be 9 digits with valid check digit."
            )

    # Validate invoice type
    if "invoice_type" in invoice:
        if invoice["invoice_type"] not in VALID_INVOICE_TYPES:
            errors.append(
                f"Invalid invoice type: {invoice['invoice_type']}. "
                f"Valid types: {list(VALID_INVOICE_TYPES.keys())}"
            )

    # Validate date
    if "date" in invoice:
        try:
            inv_date = datetime.strptime(invoice["date"], "%Y-%m-%d").date()
            if inv_date > date.today():
                errors.append("Invoice date cannot be in the future")
        except ValueError:
            errors.append(
                f"Invalid date format: {invoice['date']}. Use YYYY-MM-DD."
            )

    # Validate VAT calculation
    if "net_amount" in invoice and "vat_amount" in invoice:
        expected_vat = round(invoice["net_amount"] * VAT_RATE, 2)
        actual_vat = invoice["vat_amount"]
        if abs(expected_vat - actual_vat) > 0.01:
            errors.append(
                f"VAT mismatch: expected {expected_vat} NIS "
                f"(17% of {invoice['net_amount']}), got {actual_vat} NIS"
            )

    # Check allocation number requirement
    if (
        "invoice_type" in invoice
        and "date" in invoice
        and "total_amount" in invoice
    ):
        inv_type = invoice["invoice_type"]
        if inv_type in ALLOCATION_REQUIRED_TYPES:
            try:
                threshold = get_allocation_threshold(invoice["date"])
                if threshold and invoice["total_amount"] >= threshold:
                    if not invoice.get("allocation_number"):
                        errors.append(
                            f"Allocation number required: invoice amount "
                            f"{invoice['total_amount']} NIS >= threshold "
                            f"{threshold} NIS for date {invoice['date']}"
                        )
            except (ValueError, TypeError):
                pass  # Date validation already handled above

    return errors


def generate_example_invoice() -> dict:
    """Generate an example valid invoice for testing."""
    return {
        "seller_tin": "123456782",
        "seller_name": "Example Business Ltd",
        "buyer_tin": "987654328",
        "buyer_name": "Client Company Ltd",
        "invoice_type": 300,
        "invoice_number": "INV-2026-0001",
        "date": "2026-01-15",
        "net_amount": 15000,
        "vat_amount": 2550,
        "total_amount": 17550,
        "currency": "ILS",
        "allocation_number": "SHAAM-2026-123456",
        "items": [
            {
                "description": "Web development services",
                "quantity": 1,
                "unit_price": 15000,
                "amount": 15000,
            }
        ],
    }


def main():
    """Main entry point for invoice validation."""
    if len(sys.argv) < 2:
        print("Usage: python validate_invoice.py <invoice.json>")
        print("       python validate_invoice.py --example")
        print()
        print("Validates Israeli e-invoice JSON against SHAAM requirements.")
        sys.exit(1)

    if sys.argv[1] == "--example":
        example = generate_example_invoice()
        print("Example invoice:")
        print(json.dumps(example, indent=2))
        print()
        errors = validate_invoice(example)
        if errors:
            print("VALIDATION FAILED:")
            for e in errors:
                print(f"  - {e}")
        else:
            print("VALIDATION PASSED")
        sys.exit(0)

    try:
        with open(sys.argv[1]) as f:
            invoice = json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found: {sys.argv[1]}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON: {e}")
        sys.exit(1)

    errors = validate_invoice(invoice)
    if errors:
        print("VALIDATION FAILED:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print("VALIDATION PASSED")
        sys.exit(0)


if __name__ == "__main__":
    main()
