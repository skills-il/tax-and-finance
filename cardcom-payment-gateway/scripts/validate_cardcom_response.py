#!/usr/bin/env python3
"""Validate a Cardcom API response.

Checks DealResponse, TokenResponse, InvoiceRespondCode, and required fields.

Usage:
    python scripts/validate_cardcom_response.py --response '{"DealResponse":0,"InvoiceNumber":12345}'
    python scripts/validate_cardcom_response.py --file response.json
    python scripts/validate_cardcom_response.py --example
"""

import argparse
import json
import sys


# ANSI color codes (disabled when not a terminal)
def _supports_color():
    return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()


if _supports_color():
    GREEN = "\033[32m"
    RED = "\033[31m"
    YELLOW = "\033[33m"
    BOLD = "\033[1m"
    RESET = "\033[0m"
else:
    GREEN = RED = YELLOW = BOLD = RESET = ""


# Known Cardcom deal response codes
DEAL_RESPONSE_CODES = {
    0: "Success",
    5033: "Terminal number missing",
    5034: "Authentication failed",
    5035: "Invalid amount",
    5100: "Card declined",
    5101: "Expired card",
    5102: "CVV incorrect",
    5200: "Token not found",
    5300: "Invoice creation failed",
}

# Known Cardcom invoice response codes
INVOICE_RESPONSE_CODES = {
    0: "Success",
    500: "General invoice error",
    501: "Missing required invoice field",
    502: "Invalid document type",
    503: "VAT calculation error",
}

# Required fields in a well-formed Cardcom response
REQUIRED_DEAL_FIELDS = [
    "DealResponse",
]

# Common fields expected on a successful deal
COMMON_DEAL_FIELDS = [
    "DealResponse",
    "InternalDealNumber",
    "Token",
    "CardValidityMonth",
    "CardValidityYear",
]

# Fields expected when invoice is generated
INVOICE_FIELDS = [
    "InvoiceRespondCode",
    "InvoiceNumber",
    "InvoiceType",
]


def parse_response(raw: str) -> dict:
    """Parse a Cardcom JSON response.

    Args:
        raw: Raw JSON string.

    Returns:
        Dictionary of response fields.
    """
    raw = raw.strip()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}")

    if not isinstance(data, dict):
        raise ValueError(
            "Expected a JSON object (dictionary), "
            f"got {type(data).__name__}"
        )

    return data


def validate_response(data: dict) -> tuple:
    """Validate a Cardcom API response.

    Args:
        data: Parsed response dictionary.

    Returns:
        Tuple of (errors: list[str], warnings: list[str], info: list[str]).
    """
    errors = []
    warnings = []
    info = []

    # --- Check for required deal fields ---
    for field in REQUIRED_DEAL_FIELDS:
        if field not in data:
            errors.append(f"Missing required field: '{field}'")

    # --- Validate DealResponse ---
    deal_response = data.get("DealResponse")
    if deal_response is not None:
        try:
            deal_code = int(deal_response)
        except (ValueError, TypeError):
            errors.append(
                f"DealResponse is not a valid integer: {deal_response}"
            )
            deal_code = None

        if deal_code is not None:
            if deal_code == 0:
                info.append("DealResponse: 0 (Success)")
            else:
                meaning = DEAL_RESPONSE_CODES.get(deal_code, "Unknown error code")
                errors.append(
                    f"Transaction failed: DealResponse={deal_code} ({meaning})"
                )

    # --- Validate TokenResponse if present ---
    token_response = data.get("TokenResponse")
    if token_response is not None:
        try:
            token_code = int(token_response)
        except (ValueError, TypeError):
            errors.append(
                f"TokenResponse is not a valid integer: {token_response}"
            )
            token_code = None

        if token_code is not None:
            if token_code == 0:
                info.append("TokenResponse: 0 (Token created successfully)")
                # Check that Token field exists
                token = data.get("Token")
                if not token:
                    errors.append(
                        "TokenResponse=0 but 'Token' field is missing or empty"
                    )
                else:
                    info.append(f"Token: {token}")
            else:
                errors.append(
                    f"Token creation failed: TokenResponse={token_code}"
                )

    # --- Validate InvoiceRespondCode if present ---
    invoice_response = data.get("InvoiceRespondCode")
    if invoice_response is not None:
        try:
            inv_code = int(invoice_response)
        except (ValueError, TypeError):
            errors.append(
                f"InvoiceRespondCode is not a valid integer: {invoice_response}"
            )
            inv_code = None

        if inv_code is not None:
            if inv_code == 0:
                info.append("InvoiceRespondCode: 0 (Invoice created successfully)")

                # Validate InvoiceNumber is non-zero on success
                invoice_number = data.get("InvoiceNumber")
                if invoice_number is None:
                    errors.append(
                        "InvoiceRespondCode=0 but 'InvoiceNumber' is missing"
                    )
                else:
                    try:
                        inv_num = int(invoice_number)
                        if inv_num == 0:
                            errors.append(
                                "InvoiceRespondCode=0 but InvoiceNumber is 0 -- "
                                "expected a non-zero invoice number"
                            )
                        else:
                            info.append(f"InvoiceNumber: {inv_num}")
                    except (ValueError, TypeError):
                        warnings.append(
                            f"InvoiceNumber is not an integer: {invoice_number}"
                        )

                # Check InvoiceType
                invoice_type = data.get("InvoiceType")
                if invoice_type is not None:
                    info.append(f"InvoiceType: {invoice_type}")
                else:
                    warnings.append(
                        "InvoiceRespondCode=0 but 'InvoiceType' is missing"
                    )
            else:
                meaning = INVOICE_RESPONSE_CODES.get(inv_code, "Unknown invoice error")
                errors.append(
                    f"Invoice creation failed: InvoiceRespondCode={inv_code} ({meaning})"
                )

    # --- Warn on missing common fields for successful deals ---
    deal_code_val = None
    if deal_response is not None:
        try:
            deal_code_val = int(deal_response)
        except (ValueError, TypeError):
            pass

    if deal_code_val == 0:
        for field in COMMON_DEAL_FIELDS:
            if field not in data:
                warnings.append(
                    f"Common field '{field}' missing from successful deal response"
                )

        # Check InternalDealNumber
        internal_deal = data.get("InternalDealNumber")
        if internal_deal is not None:
            try:
                deal_num = int(internal_deal)
                if deal_num == 0:
                    warnings.append(
                        "InternalDealNumber is 0 -- may indicate a test transaction"
                    )
                else:
                    info.append(f"InternalDealNumber: {deal_num}")
            except (ValueError, TypeError):
                info.append(f"InternalDealNumber: {internal_deal}")

    # --- Check for error description fields ---
    deal_response_text = data.get("DealResponseText")
    if deal_response_text:
        info.append(f"DealResponseText: {deal_response_text}")

    operation_response = data.get("OperationResponse")
    if operation_response is not None:
        try:
            op_code = int(operation_response)
            if op_code != 0:
                errors.append(
                    f"OperationResponse={op_code} -- API-level error "
                    f"(separate from deal result)"
                )
            else:
                info.append("OperationResponse: 0 (API call successful)")
        except (ValueError, TypeError):
            warnings.append(
                f"OperationResponse is not an integer: {operation_response}"
            )

    operation_response_text = data.get("OperationResponseText")
    if operation_response_text:
        info.append(f"OperationResponseText: {operation_response_text}")

    # --- Validate ReturnValue if present ---
    return_value = data.get("ReturnValue")
    if return_value is not None:
        info.append(f"ReturnValue: {return_value}")

    return errors, warnings, info


def print_results(errors: list, warnings: list, info: list):
    """Print validation results with color coding."""
    # Print info
    for line in info:
        print(f"  {GREEN}[INFO]{RESET}  {line}")

    # Print warnings
    for line in warnings:
        print(f"  {YELLOW}[WARN]{RESET}  {line}")

    # Print errors
    for line in errors:
        print(f"  {RED}[FAIL]{RESET}  {line}")

    print()
    if errors:
        print(f"{BOLD}{RED}FAIL{RESET} -- {len(errors)} error(s) found")
    else:
        print(f"{BOLD}{GREEN}PASS{RESET} -- response is valid")
        if warnings:
            print(f"  ({len(warnings)} warning(s) -- review recommended)")


def generate_example() -> dict:
    """Return an example Cardcom response for demonstration."""
    return {
        "OperationResponse": 0,
        "OperationResponseText": "OK",
        "DealResponse": 0,
        "DealResponseText": "Approved",
        "InternalDealNumber": 98765,
        "Token": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
        "TokenResponse": 0,
        "CardValidityMonth": "12",
        "CardValidityYear": "2027",
        "Last4CardDigits": "4444",
        "InvoiceRespondCode": 0,
        "InvoiceNumber": 10042,
        "InvoiceType": 101,
        "ReturnValue": "order-2026-0042",
    }


def main():
    parser = argparse.ArgumentParser(
        description="Validate a Cardcom API response.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
examples:
  # Validate a JSON response string
  %(prog)s --response '{"DealResponse":0,"InvoiceRespondCode":0,"InvoiceNumber":10042}'

  # Validate from a file
  %(prog)s --file response.json

  # Show an example valid response and validate it
  %(prog)s --example

  # Validate a failed transaction
  %(prog)s --response '{"DealResponse":5100,"DealResponseText":"Card declined"}'
""",
    )
    parser.add_argument(
        "--response",
        help="JSON response string",
    )
    parser.add_argument(
        "--file",
        help="Path to a file containing the JSON response",
    )
    parser.add_argument(
        "--example",
        action="store_true",
        help="Show an example valid response and validate it",
    )

    args = parser.parse_args()

    if args.example:
        example = generate_example()
        print("Example Cardcom response:")
        print(json.dumps(example, indent=2))
        print()
        print("Validation results:")
        errors, warnings, info = validate_response(example)
        print_results(errors, warnings, info)
        sys.exit(0)

    if not args.response and not args.file:
        parser.print_help()
        sys.exit(1)

    if args.response and args.file:
        print(f"{RED}Error: Specify --response or --file, not both.{RESET}")
        sys.exit(1)

    # Read input
    if args.file:
        try:
            with open(args.file) as f:
                raw = f.read()
        except FileNotFoundError:
            print(f"{RED}Error: File not found: {args.file}{RESET}")
            sys.exit(1)
        except OSError as e:
            print(f"{RED}Error reading file: {e}{RESET}")
            sys.exit(1)
    else:
        raw = args.response

    # Parse
    try:
        data = parse_response(raw)
    except ValueError as e:
        print(f"{RED}Error: {e}{RESET}")
        sys.exit(1)

    if not data:
        print(f"{RED}Error: Parsed response is empty.{RESET}")
        sys.exit(1)

    # Validate
    print("Cardcom Response Validation")
    print("=" * 40)
    print()
    print("Parsed fields:")
    for k, v in data.items():
        print(f"  {k} = {v}")
    print()
    print("Validation results:")
    errors, warnings, info = validate_response(data)
    print_results(errors, warnings, info)
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
