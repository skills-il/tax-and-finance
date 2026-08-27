#!/usr/bin/env python3
"""Validate a Pelecard callback response.

Checks PelecardStatusCode, ConfirmationKey presence, PelecardTransactionId
presence, and sanity-checks Total and Currency. Warns when ConfirmationKey
is missing -- the most dangerous case (replay / tampering).

Usage:
    python scripts/validate_pelecard_response.py --response '{"PelecardStatusCode":"000",...}'
    python scripts/validate_pelecard_response.py --file response.json
    python scripts/validate_pelecard_response.py --example
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


# Pelecard convention: '000' is success, anything else is an error.
# Pelecard publishes the official message for every code through two
# credential-free endpoints, so a numeric code never has to stay opaque.
SUCCESS_STATUS = "000"

ERROR_MESSAGE_URL = (
    "https://gateway21.pelecard.biz/services/GetErrorMessage{lang}"
)


def lookup_status_message(code: str, lang: str = "En", timeout: float = 8.0):
    """Resolve a Pelecard status code to its official message.

    Calls Pelecard's own GetErrorMessageEn / GetErrorMessageHe service, which
    takes only {"ErrorCode": "NNN"} and needs NO credentials. Returns None on
    any network problem -- this is an enrichment, never a gate.
    """
    import json as _json
    import urllib.error
    import urllib.request

    code = str(code).strip().strip('"')
    if not code.isdigit():
        return None
    payload = _json.dumps({"ErrorCode": code}).encode("utf-8")
    req = urllib.request.Request(
        ERROR_MESSAGE_URL.format(lang="He" if lang.lower().startswith("he") else "En"),
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            text = resp.read().decode("utf-8", "replace").strip()
    except (urllib.error.URLError, OSError, ValueError):
        return None
    # The service returns a bare JSON string.
    try:
        text = _json.loads(text)
    except ValueError:
        pass
    if not isinstance(text, str):
        return None
    text = text.strip()
    # Pelecard's placeholders for an unassigned code (note its own spelling).
    if not text or text in ("UnkownError", "\u05e9\u05d2\u05d9\u05d0\u05d4 \u05dc\u05d0 \u05d9\u05d3\u05d5\u05e2\u05d4"):
        return None
    return text

# Required fields on every Pelecard callback for safe server-side handling.
REQUIRED_FIELDS = [
    "PelecardStatusCode",
]

# Fields that, if missing, indicate the response cannot be safely trusted
# even when PelecardStatusCode looks like success.
SECURITY_CRITICAL_FIELDS = [
    "ConfirmationKey",
    "PelecardTransactionId",
]

# Currency reference. Only `1 = ILS` is reliably documented across Pelecard
# surfaces. Other integers exist (USD/EUR/GBP) but the mapping is not
# consistently documented across Gateway20, Gateway21, and the Match API --
# verify the exact integer for your terminal in Pelecard's Postman workspace
# before sending non-ILS amounts.
KNOWN_CURRENCY_CODES = {
    1: "ILS (Israeli shekel; default; required for Bit)",
}


def parse_response(raw: str) -> dict:
    """Parse a Pelecard JSON callback payload."""
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


def _normalize_status(value) -> str:
    """Normalize PelecardStatusCode to a string for comparison."""
    if value is None:
        return ""
    s = str(value).strip()
    # Some integrators send 0 instead of '000'; treat numerically-equivalent
    # zero values as success but flag the format mismatch.
    return s


def validate_response(data: dict, resolve_codes: bool = False) -> tuple:
    """Validate a Pelecard callback.

    When resolve_codes is True, a failing status code is resolved to its
    official Pelecard message over the network.

    Returns:
        Tuple of (errors, warnings, info).
    """
    errors = []
    warnings = []
    info = []

    # --- Required fields ---
    for field in REQUIRED_FIELDS:
        if field not in data:
            errors.append(f"Missing required field: '{field}'")

    # --- Security-critical fields ---
    for field in SECURITY_CRITICAL_FIELDS:
        value = data.get(field)
        if value is None or value == "":
            errors.append(
                f"Missing security-critical field: '{field}'. "
                "Do NOT mark the order as paid -- "
                "re-verify via PaymentGW/GetTransaction is impossible "
                "without it, and the callback may be tampered or replayed."
            )

    # --- PelecardStatusCode ---
    # Pelecard returns the literal 3-digit string '000' on success. Accept
    # ONLY '000' as success. Treat '0' / '00' / 0 as malformed (likely
    # truncated or coerced upstream) and warn. Anything else -> error.
    status_raw = data.get("PelecardStatusCode")
    if status_raw is not None:
        status = _normalize_status(status_raw)
        info.append(f"PelecardStatusCode (raw): {status_raw!r}")

        if status == SUCCESS_STATUS:
            info.append("PelecardStatusCode: 000 (Success per Pelecard convention)")
        else:
            try:
                status_int = int(status)
            except (ValueError, TypeError):
                errors.append(
                    f"PelecardStatusCode is not a recognized format: {status!r}"
                )
            else:
                if status_int == 0:
                    # '0' or '00' -- numerically zero but not the canonical
                    # '000'. Do NOT treat as success automatically.
                    warnings.append(
                        f"PelecardStatusCode is not the canonical 3-digit '000' "
                        f"form (got {status!r}) -- verify the callback was not "
                        f"truncated or coerced. Re-fetch via "
                        f"PaymentGW/GetTransaction to confirm the actual status."
                    )
                else:
                    detail = ""
                    if resolve_codes:
                        msg_en = lookup_status_message(status, "En")
                        msg_he = lookup_status_message(status, "He")
                        parts = [m for m in (msg_en, msg_he) if m]
                        if parts:
                            detail = " Pelecard says: " + " / ".join(parts)
                        else:
                            detail = (
                                " Could not reach Pelecard's code lookup; resolve "
                                "manually via POST /services/GetErrorMessageEn "
                                'with {"ErrorCode": "%s"}.' % status
                            )
                    errors.append(
                        f"Transaction failed: PelecardStatusCode={status!r}."
                        + detail
                    )

    # --- Total ---
    total = data.get("Total")
    if total is not None:
        try:
            total_int = int(total)
            if total_int <= 0:
                errors.append(
                    f"Total is non-positive: {total_int}. "
                    "Pelecard charges must be positive."
                )
            else:
                info.append(
                    f"Total: {total_int} "
                    "(minor units / agorot on Gateway21; e.g. 9900 = 99.00 ILS). "
                    "Compare authoritative DebitTotal from PaymentGW/GetTransaction, not this echo."
                )
        except (ValueError, TypeError):
            warnings.append(
                f"Total is not a valid integer: {total!r}"
            )
    else:
        warnings.append(
            "Total field missing from callback. "
            "Re-verify via PaymentGW/GetTransaction to get authoritative DebitTotal."
        )

    # --- Currency ---
    currency = data.get("Currency")
    if currency is not None:
        try:
            cur_int = int(currency)
            label = KNOWN_CURRENCY_CODES.get(cur_int)
            if label:
                info.append(f"Currency: {cur_int} ({label})")
            else:
                # Print the integer back without claiming a name -- Pelecard's
                # currency-code mapping is not consistently documented across
                # API surfaces for codes other than 1.
                warnings.append(
                    f"Currency code {cur_int} is not the confirmed ILS value (1). "
                    "Verify the exact integer for your terminal in Pelecard's "
                    "Postman workspace before relying on it; do not assume "
                    "USD / EUR / GBP from any third-party documentation."
                )
        except (ValueError, TypeError):
            warnings.append(f"Currency is not a valid integer: {currency!r}")

    # --- ShvaResultEmv (informational) ---
    shva_emv = data.get("ShvaResultEmv")
    if shva_emv is not None:
        info.append(
            f"ShvaResultEmv: {shva_emv!r} "
            "(EMV / 3DS result code from Shva network)"
        )

    # --- Passthrough fields (informational) ---
    for field in ("ParamX", "ShopNo", "UserKey"):
        value = data.get(field)
        if value:
            info.append(f"{field}: {value!r}")

    # --- Final security reminder ---
    has_confirmation = bool(data.get("ConfirmationKey"))
    has_txn_id = bool(data.get("PelecardTransactionId"))
    if has_confirmation and has_txn_id and not errors:
        info.append(
            "Local checks passed. REMINDER: (1) compare ConfirmationKey "
            "byte-for-byte against the value you stored from the create-session "
            "response, (2) re-verify server-to-server via "
            "PaymentGW/GetTransaction (Pelecard does NOT sign IPNs with HMAC), "
            "(3) compare DebitTotal (not Total) against your order, "
            "(4) dedupe IPNs on PelecardTransactionId, not ParamX."
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
        print(f"{BOLD}{GREEN}PASS{RESET} -- callback fields present and well-formed")
        if warnings:
            print(f"  ({len(warnings)} warning(s) -- review recommended)")


def generate_example() -> dict:
    """Return an example Pelecard callback for demonstration."""
    return {
        "PelecardStatusCode": "000",
        "ConfirmationKey": "a1b2c3d4e5f60718293a4b5c6d7e8f90",
        "PelecardTransactionId": "12345678",
        "Total": 9900,
        "Currency": 1,
        "ShvaResultEmv": "00",
        "ParamX": "order-2026-0042",
        "ShopNo": "main-shop",
    }


def main():
    parser = argparse.ArgumentParser(
        description="Validate a Pelecard callback response.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
examples:
  # Validate a JSON callback payload
  %(prog)s --response '{"PelecardStatusCode":"000","ConfirmationKey":"abc","PelecardTransactionId":"12345","Total":9900,"Currency":1}'

  # Validate from a file
  %(prog)s --file callback.json

  # Show an example valid callback and validate it
  %(prog)s --example

  # Validate a failed callback and resolve the code to Pelecard's own message
  %(prog)s --resolve-codes --response '{"PelecardStatusCode":"033"}'

  # Just look a status code up
  %(prog)s --explain 033
""",
    )
    parser.add_argument(
        "--response",
        help="JSON callback string",
    )
    parser.add_argument(
        "--file",
        help="Path to a file containing the JSON callback",
    )
    parser.add_argument(
        "--example",
        action="store_true",
        help="Show an example valid callback and validate it",
    )
    parser.add_argument(
        "--resolve-codes",
        action="store_true",
        help=(
            "On a failing status code, look the official Pelecard message up "
            "via /services/GetErrorMessageEn and GetErrorMessageHe "
            "(no credentials required; needs network access)"
        ),
    )
    parser.add_argument(
        "--explain",
        metavar="CODE",
        help="Print the official Pelecard message for a status code and exit",
    )

    args = parser.parse_args()

    if args.explain:
        code = args.explain.strip()
        en = lookup_status_message(code, "En")
        he = lookup_status_message(code, "He")
        if not en and not he:
            print(f"{RED}No official message for code {code!r} "
                  f"(unassigned, or the lookup was unreachable).{RESET}")
            sys.exit(1)
        print(f"{BOLD}Pelecard status code {code}{RESET}")
        if en:
            print(f"  EN: {en}")
        if he:
            print(f"  HE: {he}")
        sys.exit(0)

    if args.example:
        example = generate_example()
        print("Example Pelecard callback:")
        print(json.dumps(example, indent=2))
        print()
        print("Validation results:")
        errors, warnings, info = validate_response(example, args.resolve_codes)
        print_results(errors, warnings, info)
        sys.exit(1 if errors else 0)

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
        print(f"{RED}Error: Parsed callback is empty.{RESET}")
        sys.exit(1)

    print("Pelecard Callback Validation")
    print("=" * 40)
    print()
    print("Parsed fields:")
    for k, v in data.items():
        print(f"  {k} = {v}")
    print()
    print("Validation results:")
    errors, warnings, info = validate_response(data, args.resolve_codes)
    print_results(errors, warnings, info)
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
