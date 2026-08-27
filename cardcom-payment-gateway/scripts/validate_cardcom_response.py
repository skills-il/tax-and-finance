#!/usr/bin/env python3
"""Validate a Cardcom V11 API response.

Cardcom V11 responses carry a top-level ``ResponseCode`` (0 = success) and a
``Description`` string. This script checks ``ResponseCode``, surfaces
``Description``, and verifies the fields you would expect on a successful
transaction, token, or document operation.

Usage:
    python scripts/validate_cardcom_response.py --response '{"ResponseCode":0,"TranzactionId":12345}'
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


# ResponseCode values that count as success in Cardcom V11.
# 0 is the only unconditional success. 700/701 mean a J2/J5 VALIDATION-ONLY transaction
# succeeded: the card was checked, NO money moved. Treating them as success on a charge, a
# document creation or a refund is how goods get shipped without a charge, or a refund is
# believed complete when nothing was returned. Pass --validation-only to have them accepted.
_allow_validation_only = False
_expect = None
_expect_amount = None
SUCCESS_CODES = {0}
VALIDATION_ONLY_CODES = {700, 701}


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


def _check_response_code(data: dict, label: str, errors: list, info: list):
    """Check a ResponseCode field on a response object or nested object."""
    code = data.get("ResponseCode")
    description = data.get("Description")
    if code is None:
        errors.append(f"{label}: missing required field 'ResponseCode'")
        return None
    if isinstance(code, bool) or not isinstance(code, int):
        # Do not coerce. A float or a numeric string is a malformed response shape, and
        # int("0")/int(0.9) would silently report a successful operation.
        errors.append(
            f"{label}: ResponseCode must be an integer, got {type(code).__name__}: {code!r}"
        )
        return None
    if code in SUCCESS_CODES:
        info.append(f"{label}: ResponseCode={code} (success)")
    elif code in VALIDATION_ONLY_CODES:
        if _allow_validation_only:
            info.append(
                f"{label}: ResponseCode={code} (validation-only success, NO money moved)"
            )
        else:
            errors.append(
                f"{label}: ResponseCode={code} means a validation-only (J2/J5) check "
                "succeeded and NO money moved. If this was a charge, a document creation "
                "or a refund, it did NOT complete. Re-run with --validation-only if you "
                "genuinely issued a J2/J5 check."
            )
    else:
        desc = description or "(no Description returned)"
        errors.append(f"{label}: ResponseCode={code} -- {desc}")
    return code


def validate_response(data: dict) -> tuple:
    """Validate a Cardcom V11 API response.

    Args:
        data: Parsed response dictionary.

    Returns:
        Tuple of (errors: list[str], warnings: list[str], info: list[str]).
    """
    errors = []
    warnings = []
    info = []

    # --- Top-level ResponseCode / Description ---
    top_code = _check_response_code(data, "Response", errors, info)

    description = data.get("Description")
    if description:
        info.append(f"Description: {description}")
    elif top_code is not None and top_code not in SUCCESS_CODES | VALIDATION_ONLY_CODES:
        warnings.append(
            "Non-zero ResponseCode but no 'Description' string -- "
            "cannot surface the failure reason to the user"
        )

    # --- ReturnValue echo ---
    return_value = data.get("ReturnValue")
    if return_value is not None:
        info.append(f"ReturnValue: {return_value}")

    # --- Transaction fields ---
    transaction_id = data.get("TranzactionId")
    if transaction_id is not None:
        info.append(f"TranzactionId: {transaction_id}")

    token = data.get("Token")
    if token:
        info.append(f"Token: {token}")

    # --- Refund response ---
    new_transaction_id = data.get("NewTranzactionId")
    if new_transaction_id is not None:
        info.append(f"NewTranzactionId (refund): {new_transaction_id}")

    # --- Document fields (top-level, e.g. DocumentInfo or Transaction) ---
    document_number = data.get("DocumentNumber")
    if document_number is not None:
        info.append(f"DocumentNumber: {document_number}")
    document_url = data.get("DocumentUrl")
    if document_url:
        info.append(f"DocumentUrl: {document_url}")

    # --- A refund must not be mistaken for a charge ---
    # TransactionInfo carries IsRefund and DealType. A response with ResponseCode 0
    # and IsRefund true is a successful REFUND, not a successful charge.
    for scope in (data, data.get("TranzactionInfo") or {}):
        if not isinstance(scope, dict):
            continue
        if scope.get("IsRefund") is True or str(scope.get("DealType", "")).lower() == "refund":
            if _expect == "refund":
                info.append("Response is a refund, as expected")
            elif _expect is not None:
                errors.append(
                    f"Response is a REFUND (IsRefund/DealType), but --expect {_expect} "
                    "was requested. Do not record this as a charge."
                )
            else:
                warnings.append(
                    "Response is a REFUND (IsRefund/DealType true). Pass --expect refund "
                    "to assert that, or --expect charge to reject it."
                )

    # --- Amount reconciliation ---
    if _expect_amount is not None:
        actual = data.get("Amount")
        if actual is None:
            nested_tx = data.get("TranzactionInfo")
            if isinstance(nested_tx, dict):
                actual = nested_tx.get("Amount")
        if actual is None:
            errors.append(
                f"--amount {_expect_amount} was given but the response carries no Amount "
                "to reconcile against. Do not fulfil on an unreconciled response."
            )
        elif abs(float(actual) - _expect_amount) > 0.001:
            errors.append(
                f"Amount mismatch: response says {actual}, expected {_expect_amount}. "
                "The customer was not charged the order amount."
            )
        else:
            info.append(f"Amount reconciled: {actual}")

    # --- Nested objects inside a LowProfileResult ---
    # A null nested object is NOT a pass. The top-level ResponseCode on a
    # LowProfileResult means only "not a developer error"; the card result lives in
    # TranzactionInfo, which the spec says is non-null only for ChargeOnly and
    # ChargeAndCreateToken. A null TranzactionInfo means no money moved, and a null
    # DocumentInfo after a charge means the tax invoice was never issued.
    _REQUIRED_FOR = {
        "charge": ("TranzactionInfo",),
        "token": ("TokenInfo",),
        "document": ("DocumentInfo",),
        "refund": ("TranzactionInfo",),
    }
    for key in _REQUIRED_FOR.get(_expect or "", ()):
        if not isinstance(data.get(key), dict) or not data.get(key):
            errors.append(
                f"--expect {_expect} was requested but '{key}' is null or absent. "
                "On a LowProfile result that means the operation did NOT complete "
                "(an abandoned page, or a document that was never created). "
                "Fail closed: do not fulfil."
            )

    for key in ("TranzactionInfo", "TokenInfo", "DocumentInfo", "SuspendedInfo"):
        nested = data.get(key)
        if key in data and nested is None:
            warnings.append(
                f"'{key}' is present but null. On a LowProfile result that means the "
                "corresponding operation did not complete."
            )
        if isinstance(nested, dict) and nested:
            # TokenInfo and SuspendedInfo do not carry ResponseCode;
            # TranzactionInfo and DocumentInfo do.
            if "ResponseCode" in nested:
                _check_response_code(nested, key, errors, info)
            else:
                info.append(f"{key}: present")
            if key == "TokenInfo" and nested.get("Token"):
                info.append(f"  TokenInfo.Token: {nested['Token']}")
            if key == "SuspendedInfo" and nested.get("SuspendedDealId"):
                info.append(
                    f"  SuspendedInfo.SuspendedDealId: "
                    f"{nested['SuspendedDealId']}"
                )

    # --- Warn on the legacy DealResponse field ---
    if "DealResponse" in data:
        warnings.append(
            "Response contains 'DealResponse' -- that field belongs to the "
            "legacy .aspx interface, not V11. V11 uses 'ResponseCode'."
        )

    return errors, warnings, info


def print_results(errors: list, warnings: list, info: list):
    """Print validation results with color coding."""
    for line in info:
        print(f"  {GREEN}[INFO]{RESET}  {line}")
    for line in warnings:
        print(f"  {YELLOW}[WARN]{RESET}  {line}")
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
    """Return an example Cardcom V11 response for demonstration."""
    return {
        "ResponseCode": 0,
        "Description": "Operation completed successfully",
        "TranzactionId": 219282004,
        "Token": "84cc1f4f-c089-410b-9f93-6437ac9abba6",
        "DocumentNumber": 10042,
        "DocumentUrl": "https://secure.cardcom.solutions/doc/10042",
        "ReturnValue": "order-2026-0042",
    }


def main():
    parser = argparse.ArgumentParser(
        description="Validate a Cardcom V11 API response.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
examples:
  # Validate a JSON response string
  %(prog)s --response '{"ResponseCode":0,"TranzactionId":219282004}'

  # Validate from a file
  %(prog)s --file response.json

  # Show an example valid response and validate it
  %(prog)s --example

  # Validate a failed transaction
  %(prog)s --response '{"ResponseCode":3,"Description":"Call credit company"}'
""",
    )
    parser.add_argument("--response", help="JSON response string")
    parser.add_argument(
        "--expect",
        choices=["charge", "token", "document", "refund", "validation"],
        help="What the call was supposed to do. Without it the script cannot fail "
             "closed on a null nested object, because a LowProfile top-level "
             "ResponseCode of 0 only means the request was not a developer error.",
    )
    parser.add_argument(
        "--amount",
        type=float,
        help="Expected charge amount, reconciled against the response Amount.",
    )
    parser.add_argument(
        "--validation-only",
        action="store_true",
        help="Accept ResponseCode 700/701 as success. Use ONLY when the call really was a "
             "J2/J5 validation-only check, where no money moves.",
    )
    parser.add_argument(
        "--file", help="Path to a file containing the JSON response"
    )
    parser.add_argument(
        "--example",
        action="store_true",
        help="Show an example valid response and validate it",
    )

    args = parser.parse_args()

    global _allow_validation_only, _expect, _expect_amount

    _allow_validation_only = args.validation_only or args.expect == "validation"
    _expect = args.expect
    _expect_amount = args.amount

    if args.example:
        example = generate_example()
        print("Example Cardcom V11 response:")
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

    try:
        data = parse_response(raw)
    except ValueError as e:
        print(f"{RED}Error: {e}{RESET}")
        sys.exit(1)

    if not data:
        print(f"{RED}Error: Parsed response is empty.{RESET}")
        sys.exit(1)

    print("Cardcom V11 Response Validation")
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
