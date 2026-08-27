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


# Tranzila response codes, transcribed from the vendor's own
# "Transaction Response Codes" page:
#   https://docs.tranzila.com/docs/payments-and-billing/transaction-response-codes
#
# Only codes that appear on that page are listed. Earlier versions of this
# script carried 033, 036, 039, 091, 125 and 200, none of which exist in the
# vendor table, and gave invented meanings to 014, 057, 061, 065, 075, 107 and
# 111. Expired card is 015, not 033/036. Do not re-add a code from memory.
RESPONSE_CODES = {
    "shva": "Pending SHVA response",
    "000": "Transaction approved",
    "777": "Operation completed (success for operations with no transaction recorded, incl. J2 and J5)",
    "001": "Blocked, confiscate card",
    "002": "Stolen, confiscate card",
    "003": "Contact the credit company to approve the transaction",
    "004": "Refusal, contact the card owner to check the reason with the credit company",
    "005": "Forged, confiscate card",
    "006": "Incorrect identity number or CVV",
    "007": "Invalid cavv/ucaf",
    "008": "Invalid avs",
    "009": "Unsuccessful communication",
    "010": "Partial confirmation",
    "012": "Unauthorized card for this terminal",
    "014": "Card not affiliated with the network",
    "015": "Expired card, check the expiration date again",
    "016": "Unauthorized currency",
    "017": "Unauthorized credit type for this transaction",
    "026": "Wrong ID number",
    "141": "Terminal not authorized to clear this transaction brand",
    "401": "Number of payments above the terminal maximum",
    "402": "Number of payments below the terminal minimum",
    "403": "Transaction sum below the minimum payment amount",
    "404": "Number-of-payments field not supplied",
    "405": "First / fixed payment amount missing",
    "406": "Transaction sum differs from first payment + fixed payment x number of payments",
    "416": "Invalid expiry date",
    "417": "Invalid terminal number",
    "425": "Duplicate record",
    "431": "General failure",
    "447": "Wrong credit card number",
    "500": "Transaction stopped by the user",
    "800": "Transaction cancelled",
    # 3DS codes, transcribed from the "3DS Errors" tab of the same vendor page.
    # These are returned during 3D Secure authentication, before the transaction
    # reaches SHVA for clearing. Note 905 is the 3DS-space expired card; the
    # SHVA-space expired card is 015.
    "900": "Transaction failed at 3D Secure authentication stage",
    "901": "3DS: card authentication failed",
    "902": "3DS: unrecognized device",
    "903": "3DS: unsupported device",
    "904": "3DS: authentication frequency limit exceeded",
    "905": "3DS: expired card",
    "906": "3DS: invalid card number",
    "907": "3DS: invalid transaction",
    "908": "3DS: card registration record not found",
    "909": "3DS: security failure",
    "910": "3DS: stolen card",
    "911": "3DS: suspected fraud",
    "912": "3DS: transaction not authorized for the cardholder",
    "913": "3DS: cardholder not enrolled in the service",
    "914": "3DS: ACS transaction timeout expired",
    "915": "3DS: low trust level",
    "916": "3DS: medium trust level",
    "917": "3DS: high trust level",
    "918": "3DS: very high trust level",
    "919": "3DS: maximum ACS challenge count exceeded",
    "920": "3DS: non-payment transaction not supported",
    "921": "3DS: 3RI transaction not supported",
    "922": "3DS: technical issue at ACS",
    "923": "3DS: decoupled authentication required by ACS but not requested by the 3DS requestor",
    "924": "3DS: maximum decoupled 3DS requestor expiry time exceeded",
    "925": "3DS: decoupled authentication did not have sufficient time to authenticate the cardholder",
    "926": "3DS: authentication was attempted but not completed by the cardholder",
    "927": "3DS: card authentication cancelled by user",
    "928": "3DS: card authentication cancelled by user",
    "930": "3DS: authentication was attempted but not completed by the cardholder",
    "951": "PayPal error",
    "952": "PayPal error",
    "954": "PayPal error",
    "997": "General failure",
    "998": "Transactions-file failure",
}

# Ranges the vendor table uses. Reported when an exact code is unknown, so the
# script narrows the fault instead of guessing a meaning.
CODE_RANGES = (
    (1, 17, "issuer refusal or card-status problem"),
    (51, 89, "terminal configuration: a required vector or parameter FILE is missing"),
    (101, 152, "terminal configuration: a required ENTRY in a vector or parameter file is missing"),
    (182, 193, "terminal configuration: invalid values in a vector or parameter file"),
    (300, 354, "acquirer or issuer has not authorised this terminal for that transaction type, currency or credit type"),
    (401, 406, "installment / credit-plan error"),
    (407, 498, "request data or card-handling error"),
    (500, 599, "cancellation or message-level error"),
    (700, 799, "PinPad / terminal hardware"),
    (900, 930, "3D Secure authentication error"),
    (951, 954, "PayPal"),
)


def describe_code(code):
    """Return a meaning for a response code, or a range hint, never a guess."""
    if code in RESPONSE_CODES:
        return RESPONSE_CODES[code]
    try:
        numeric = int(code)
    except (TypeError, ValueError):
        return None
    for low, high, meaning in CODE_RANGES:
        if low <= numeric <= high:
            return (
                f"not in this script's table; the {low:03d}-{high:03d} range is "
                f"{meaning}. Look the exact code up in the vendor's Transaction "
                f"Response Codes page before telling anyone what it means"
            )
    return None

# Fields commonly returned by Tranzila in a successful legacy CGI transaction.
# Note "ccno" is a REQUEST parameter, not a response field: the CGI returns
# masked card data as DBFcard / cardtype, and API V2 returns card_mask / last_4.
COMMON_FIELDS = [
    "Response",
    "ConfirmationCode",
    "index",
    "sum",
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

    # --- Normalise an API V2 JSON body to the legacy field names ---
    # API V2 returns {"error_code":0,"transaction_result":{"processor_response_code":"000",...}}
    # while the legacy CGI returns Response=000&... Handle both.
    if "Response" not in data and isinstance(data.get("transaction_result"), dict):
        txn = data["transaction_result"]
        data = dict(data)
        data["Response"] = txn.get("processor_response_code")
        for src, dst in (
            ("transaction_id", "index"),
            ("auth_number", "ConfirmationCode"),
            ("token", "TranzilaTK"),
        ):
            if txn.get(src) is not None and dst not in data:
                data[dst] = txn[src]
        app_error = data.get("error_code")
        if app_error not in (None, 0, "0"):
            info.append(
                f"API V2 application error_code {app_error} "
                f"({describe_code(str(app_error)) or 'see the vendor response-code page'})"
            )

    # --- Check Response code ---
    response_code = data.get("Response")
    if response_code is not None:
        # A JSON producer may emit the code as an integer; pad it back.
        response_code = str(response_code).strip()
        if response_code.isdigit() and len(response_code) < 3:
            response_code = response_code.zfill(3)
            data = dict(data)
            data["Response"] = response_code
    if response_code is None:
        errors.append("Missing 'Response' field -- cannot determine transaction result")
    else:
        response_code = str(response_code).strip()
        if response_code in ("000", "777"):
            info.append(
                f"Response code: {response_code} ({RESPONSE_CODES[response_code]})"
            )
        else:
            meaning = describe_code(response_code)
            if meaning is None:
                meaning = (
                    "not in the vendor table this script was built from. Do NOT "
                    "guess a meaning: look it up on the Transaction Response "
                    "Codes page in the Tranzila docs "
                    "(docs.tranzila.com, Payments and Billing section)"
                )
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
        else:
            # The vendor publishes no fixed token length or format, and API V2
            # tokens are alphanumeric and differ in shape from legacy CGI ones,
            # so never reject a token on length. Store it as an opaque string.
            info.append(f"TranzilaTK present ({len(token_str)} chars, treated as opaque)")

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
        # Field names taken from the response shape documented in the
        # tranzilajs types (Tempref included).
        "Response=000&ConfirmationCode=0283456&index=3&"
        "expdate=1227&sum=150.00&Tempref=12345678&"
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
