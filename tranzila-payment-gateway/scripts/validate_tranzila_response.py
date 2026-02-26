#!/usr/bin/env python3
"""Validate a Tranzila transaction response.

Checks response code, required fields, token format, and flags common issues.

Usage:
    python scripts/validate_tranzila_response.py --response 'Response=000&ConfirmationCode=0283456&...'
    python scripts/validate_tranzila_response.py --response '{"Response":"000","ConfirmationCode":"0283456"}'
    python scripts/validate_tranzila_response.py --file response.json
    python scripts/validate_tranzila_response.py --example
"""

import argparse
import json
import sys
from urllib.parse import parse_qs


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


# Known Tranzila response codes (subset of common ones)
RESPONSE_CODES = {
    "000": "Approved",
    "001": "Card restricted",
    "002": "Card stolen",
    "003": "Contact card company",
    "004": "Card declined",
    "005": "Card forged",
    "006": "CVV/ID error",
    "010": "Partial amount approved",
    "014": "Invalid card number",
    "033": "Card expired",
    "036": "Card expired",
    "039": "No credit account",
    "057": "Transaction not permitted",
    "061": "Exceeds withdrawal limit",
    "065": "Daily limit exceeded",
    "075": "PIN tries exceeded",
    "091": "Issuer not available",
    "107": "Amount exceeds limit",
    "111": "Not authorized for installments",
    "125": "Not authorized for Amex",
    "200": "Application error",
    "900": "3DS authentication failed",
}

# Fields commonly returned by Tranzila in a successful transaction
COMMON_FIELDS = [
    "Response",
    "ConfirmationCode",
    "index",
    "sum",
    "ccno",
    "expdate",
]

# Fields that indicate a token was used or created
TOKEN_FIELDS = ["TranzilaTK"]


def parse_response(raw: str) -> dict:
    """Parse a Tranzila response from JSON or URL-encoded format.

    Args:
        raw: Raw response string (JSON or URL-encoded).

    Returns:
        Dictionary of response fields.
    """
    raw = raw.strip()

    # Try JSON first
    if raw.startswith("{"):
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            pass

    # Try URL-encoded
    try:
        parsed = parse_qs(raw, keep_blank_values=True)
        # parse_qs returns lists; flatten single-value fields
        return {k: v[0] if len(v) == 1 else v for k, v in parsed.items()}
    except Exception:
        pass

    raise ValueError(
        "Cannot parse response. Expected JSON object or URL-encoded string."
    )


def validate_response(data: dict) -> tuple:
    """Validate a Tranzila transaction response.

    Args:
        data: Parsed response dictionary.

    Returns:
        Tuple of (errors: list[str], warnings: list[str], info: list[str]).
    """
    errors = []
    warnings = []
    info = []

    # --- Check Response code ---
    response_code = data.get("Response")
    if response_code is None:
        errors.append("Missing 'Response' field -- cannot determine transaction result")
    else:
        response_code = str(response_code).strip()
        if response_code == "000":
            info.append("Response code: 000 (Approved)")
        else:
            meaning = RESPONSE_CODES.get(response_code, "Unknown error code")
            errors.append(
                f"Transaction failed: Response={response_code} ({meaning})"
            )

    # --- On success, check for ConfirmationCode ---
    if response_code == "000":
        confirmation = data.get("ConfirmationCode")
        if not confirmation:
            errors.append(
                "Missing 'ConfirmationCode' on approved transaction -- "
                "store this value for refund and reconciliation"
            )
        else:
            info.append(f"ConfirmationCode: {confirmation}")

    # --- Validate token format if present ---
    token = data.get("TranzilaTK")
    if token is not None:
        token_str = str(token).strip()
        if len(token_str) == 0:
            warnings.append("TranzilaTK is present but empty")
        elif len(token_str) != 19:
            warnings.append(
                f"TranzilaTK length is {len(token_str)} chars "
                f"(expected 19). Value: {token_str}"
            )
        else:
            info.append(f"TranzilaTK: {token_str} (valid 19-char format)")

    # --- Warn on missing common fields ---
    for field in COMMON_FIELDS:
        if field not in data:
            warnings.append(f"Common field '{field}' is missing from response")

    # --- Check for installment fields consistency ---
    cred_type = data.get("cred_type")
    if cred_type and str(cred_type) == "8":
        for inst_field in ["npay", "fpay", "spay"]:
            if inst_field not in data:
                warnings.append(
                    f"Installment transaction (cred_type=8) but '{inst_field}' missing"
                )
        # Validate installment arithmetic if all fields present
        if all(f in data for f in ["npay", "fpay", "spay", "sum"]):
            try:
                npay = int(data["npay"])
                fpay = float(data["fpay"])
                spay = float(data["spay"])
                total = float(data["sum"])
                calculated = fpay + (npay * spay)
                if abs(calculated - total) > 0.01:
                    errors.append(
                        f"Installment mismatch: fpay({fpay}) + npay({npay}) * "
                        f"spay({spay}) = {calculated}, but sum = {total}"
                    )
                else:
                    info.append(
                        f"Installments valid: {npay + 1} payments "
                        f"(first={fpay}, subsequent={spay}, total={total})"
                    )
            except (ValueError, TypeError):
                warnings.append("Could not parse installment fields as numbers")

    # --- Check for index field on success ---
    if response_code == "000" and "index" not in data:
        warnings.append(
            "Missing 'index' field -- needed for refund operations (tranmode=C)"
        )

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


def generate_example() -> str:
    """Return an example Tranzila response for demonstration."""
    return (
        "Response=000&ConfirmationCode=0283456&index=3&"
        "ccno=XXXXXXXXXXXX4444&expdate=1227&sum=150.00&"
        "currency=1&cred_type=1&TranzilaTK=1234567890123454444"
    )


def main():
    parser = argparse.ArgumentParser(
        description="Validate a Tranzila transaction response.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
examples:
  # Validate a URL-encoded response string
  %(prog)s --response 'Response=000&ConfirmationCode=0283456&sum=150.00'

  # Validate a JSON response string
  %(prog)s --response '{"Response":"000","ConfirmationCode":"0283456"}'

  # Validate from a file (JSON or URL-encoded)
  %(prog)s --file response.txt

  # Show an example valid response
  %(prog)s --example
""",
    )
    parser.add_argument(
        "--response",
        help="Response string (JSON or URL-encoded)",
    )
    parser.add_argument(
        "--file",
        help="Path to a file containing the response",
    )
    parser.add_argument(
        "--example",
        action="store_true",
        help="Show an example valid response and validate it",
    )

    args = parser.parse_args()

    if args.example:
        example = generate_example()
        print("Example Tranzila response (URL-encoded):")
        print(f"  {example}")
        print()
        data = parse_response(example)
        print("Parsed fields:")
        for k, v in data.items():
            print(f"  {k} = {v}")
        print()
        print("Validation results:")
        errors, warnings, info = validate_response(data)
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
    print("Tranzila Response Validation")
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
