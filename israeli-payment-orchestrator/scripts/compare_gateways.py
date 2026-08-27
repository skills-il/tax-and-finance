#!/usr/bin/env python3
"""Compare Israeli payment gateways on capabilities that are vendor-documented.

Generates a capability matrix to help choose the right payment gateway(s) for
Israeli merchants.

This script deliberately does NOT estimate processing cost. Merchant discount
rates on every Israeli gateway are contractual and quoted per merchant; none of
the six publishes a rate card. A cost ranking built from invented bands names a
"cheapest" gateway on numbers no vendor stands behind, and the ordering flips on
a difference smaller than any real negotiation. Ask each gateway for a quote.

Usage:
    python scripts/compare_gateways.py --features installments,recurring
    python scripts/compare_gateways.py --all
    python scripts/compare_gateways.py --example
    python scripts/compare_gateways.py --json
"""

import sys
import json
import argparse
from dataclasses import dataclass, asdict
from typing import List

# Capability values. "yes" / "no" mean the vendor (or this skill's dedicated
# per-gateway sibling skill) documents the answer. "unverified" means no source
# was found either way -- it is NOT a soft "no", and the script never filters a
# gateway out on it without saying so.
YES, NO, UNVERIFIED = "yes", "no", "unverified"
# "per sibling" means a dedicated skills-il gateway skill documents it, but this
# skill did not re-verify it against the vendor. It is weaker than YES and is
# reported separately rather than being folded into a plain "yes".
PER_SIBLING = "yes (per sibling skill)"

FEATURE_KEYS = ("installments", "credit", "recurring", "bit", "apple_pay")

# "club" is deliberately NOT a feature key. Club and issuer-loyalty programmes are
# a terminal and acquirer configuration, not a capability your code selects and not
# a CreditType value any vendor publishes. Filtering on it used to return an empty
# match, which reads as "no Israeli gateway supports club installments" and is wrong.
NOT_A_GATEWAY_CAPABILITY = {
    "club": "Club and loyalty programmes are configured on the merchant's terminal by "
            "the acquirer. They are not a gateway capability and not a CreditType "
            "value: only 1, 6 and 8 are vendor-published. Ask the acquirer.",
}


@dataclass
class GatewayInfo:
    """Israeli payment gateway information."""
    name: str
    hebrew_name: str
    api_style: str
    base_url: str
    auth: str
    installment_types: List[str]
    recurring: object          # True / False / UNVERIFIED
    hosted_page: str
    bit_support: str          # YES / NO / UNVERIFIED
    apple_pay: str            # YES / NO / UNVERIFIED
    money_unit: str           # what the amount field actually carries
    void_call: str
    refund_call: str
    partial_refund: str
    api_docs_url: str
    notes: str


# שערי תשלום ישראליים - Israeli payment gateways
GATEWAYS = {
    "cardcom": GatewayInfo(
        name="Cardcom",
        hebrew_name="קארדקום",
        api_style="REST JSON",
        base_url="https://secure.cardcom.solutions/api/v11/",
        auth="ApiName + ApiPassword (per terminal)",
        installment_types=["regular", "credit"],
        recurring=True,
        hosted_page="redirect or iframe (Low Profile)",
        bit_support=YES,          # CreateLowProfileResponse.UrlToBit in the v11 swagger
        apple_pay=YES,            # ExtPaymentMethod enum in the v11 swagger lists ApplePay
        money_unit="decimal shekels",
        void_call="Transactions/RefundByTransactionId with CancelOnly=true",
        refund_call="Transactions/RefundByTransactionId",
        partial_refund="yes (PartialSum)",
        api_docs_url="https://secure.cardcom.solutions/swagger/v11/swagger.json",
        notes="Built-in Israeli tax-document generation. CancelOnly is valid "
              "only before the transaction is deposited.",
    ),
    "tranzila": GatewayInfo(
        name="Tranzila",
        hebrew_name="טרנזילה",
        api_style="form-encoded CGI (legacy) + REST JSON (API V2)",
        base_url="https://secure5.tranzila.com/cgi-bin/ (legacy); "
                 "https://api.tranzila.com/v1 (API V2)",
        auth="terminal + password (legacy); 4-header HMAC-SHA256 (API V2)",
        installment_types=["regular", "credit"],
        recurring=True,
        hosted_page="iframe, redirect or Hosted Fields",
        bit_support=YES,          # dedicated Bit API; bit_pay=1 on the iframe
        apple_pay=YES,            # apple_pay=1 on the iframe parameter page
        money_unit="decimal shekels",
        void_call="txn_type=cancel (API V2)",
        refund_call="tranmode=C{index} + CreditPass (legacy); "
                    "txn_type=credit (API V2)",
        partial_refund="yes",
        api_docs_url="https://docs.tranzila.com/",
        notes="Four separate surfaces with non-transferable parameter names. "
              "Decide which one you are integrating against first.",
    ),
    "payme": GatewayInfo(
        name="PayMe",
        hebrew_name="פיימי",
        api_style="REST JSON",
        base_url="https://ng.paymeservice.com/api/",
        auth="payme_client_key (named by the API itself on a missing-parameter error)",
        installment_types=["unverified"],
        recurring=UNVERIFIED,
        hosted_page="unverified",
        bit_support=UNVERIFIED,
        apple_pay=UNVERIFIED,
        money_unit="unverified, confirm before first charge",
        void_call="unverified",
        refund_call="api/refund-sale",
        partial_refund="unverified",
        api_docs_url="https://payme.io/  (no public developer-docs URL; request the reference from PayMe)",
        notes="No dedicated sibling skill and no reachable public developer docs. "
              "Only the API host and the refund-sale route were confirmed by probe; "
              "everything else is unverified in BOTH directions.",
    ),
    "meshulam": GatewayInfo(
        name="Meshulam (Grow)",
        hebrew_name="משולם (גראו)",
        api_style="multipart/form-data",
        base_url="https://secure.meshulam.co.il/api/light/server/1.0/",
        auth="pageCode or userId, depending on the endpoint",
        installment_types=["regular", "credit"],
        recurring=True,
        hosted_page="iframe + redirect",
        bit_support=YES,          # cancelBitTransaction exists (probed); fake methods differ
        apple_pay=UNVERIFIED,
        money_unit="decimal shekels",
        void_call="cancelBitTransaction (Bit only; requires pageCode)",
        refund_call="refundTransaction (refundSum, not sum)",
        partial_refund="yes, blocked once settled or transmitted",
        api_docs_url="https://developers.grow.business/reference/overview",
        notes="Returns HTTP 200 with status=\"0\" on failure. Server-side only.",
    ),
    "icredit": GatewayInfo(
        name="iCredit",
        hebrew_name="אייקרדיט",
        api_style="WCF .svc service",
        base_url="https://icredit.rivhit.co.il/API/",
        auth="unverified",
        installment_types=["unverified"],
        recurring=UNVERIFIED,
        hosted_page="unverified",
        bit_support=UNVERIFIED,
        apple_pay=UNVERIFIED,
        money_unit="unverified, confirm before first charge",
        void_call="unverified",
        refund_call="unverified",
        partial_refund="unverified",
        api_docs_url="https://www.rivhit.co.il/",
        notes="Part of Rivhit accounting software. No dedicated sibling skill; "
              "the refund surface is undocumented publicly.",
    ),
    "pelecard": GatewayInfo(
        name="Pelecard",
        hebrew_name="פלאכארד",
        api_style="REST JSON",
        base_url="https://gateway21.pelecard.biz/",
        auth="terminal + user + password",
        installment_types=["regular", "credit"],
        recurring=True,
        hosted_page="redirect or iframe",
        bit_support=PER_SIBLING,  # documented in pelecard-payment-gateway, not re-verified here
        apple_pay=PER_SIBLING,    # ClientSecure.js, per pelecard-payment-gateway
        money_unit="agorot (minor units)",
        void_call="/services/DeleteTran, while the batch is still open",
        refund_call="undocumented; a credit is a new opposite transaction",
        partial_refund="no (DeleteTran is whole-transaction)",
        api_docs_url="https://gateway21.pelecard.biz/services",
        notes="gateway20 and gateway21 return byte-identical responses; the "
              "hostname is NOT an environment switch. Terminal and credentials "
              "decide whether a call is a test or a real charge.",
    ),
}


class NotAGatewayCapability(ValueError):
    """Raised for a feature that is real but is not a property of the gateway."""


class UnknownFeature(ValueError):
    """Raised when a caller asks to filter on a feature the script does not model."""


def _supports(gw: GatewayInfo, feature: str) -> str:
    """Return YES / NO / UNVERIFIED for one feature on one gateway."""
    if feature == "installments":
        if gw.installment_types == ["unverified"]:
            return UNVERIFIED
        return YES if gw.installment_types else NO
    if feature == "credit":
        if gw.installment_types == ["unverified"]:
            return UNVERIFIED
        return YES if feature in gw.installment_types else NO
    if feature == "recurring":
        if isinstance(gw.recurring, str):
            return gw.recurring
        return YES if gw.recurring else NO
    if feature == "bit":
        return gw.bit_support
    if feature == "apple_pay":
        return gw.apple_pay
    raise UnknownFeature(feature)


def filter_by_features(gateways: dict, features: List[str]) -> tuple:
    """Filter gateways by required features.

    Returns (matching_gateways, uncertain_gateway_names). A gateway whose
    support for a requested feature is UNVERIFIED is excluded from the match
    but reported separately, so an unknown never masquerades as a "no".

    Raises UnknownFeature if a requested feature is not one this script models.
    An unrecognised feature must never silently match everything -- that turns a
    typo into a confident wrong answer.
    """
    requested = []
    for raw in features:
        feature = raw.strip().lower()
        if not feature:
            continue
        if feature in NOT_A_GATEWAY_CAPABILITY:
            raise NotAGatewayCapability(NOT_A_GATEWAY_CAPABILITY[feature])
        if feature not in FEATURE_KEYS:
            raise UnknownFeature(raw.strip())
        requested.append(feature)

    if not requested:
        raise UnknownFeature("(empty feature list)")

    result, uncertain = {}, []
    for name, gw in gateways.items():
        verdicts = [_supports(gw, f) for f in requested]
        if all(v in (YES, PER_SIBLING) for v in verdicts):
            result[name] = gw
        elif UNVERIFIED in verdicts and NO not in verdicts:
            uncertain.append(gw.name)
    return result, uncertain


def _print_grid(headers, rows, footer=None):
    """Print a table whose column widths fit the widest cell, so nothing truncates."""
    widths = [max(len(str(h)), *(len(str(r[i])) for r in rows)) if rows else len(str(h))
              for i, h in enumerate(headers)]
    line = "  ".join(str(h).ljust(w) for h, w in zip(headers, widths))
    print("\n" + line)
    print("-" * len(line))
    for row in rows:
        print("  ".join(str(c).ljust(w) for c, w in zip(row, widths)))
    if footer:
        print("\n" + footer)


def print_comparison_table(gateways: dict) -> None:
    """Print gateway capability comparison as a formatted table."""
    rows = [
        [gw.name,
         gw.api_style,
         ", ".join(gw.installment_types) if gw.installment_types else "None",
         gw.hosted_page,
         gw.bit_support,
         gw.money_unit]
        for gw in gateways.values()
    ]
    _print_grid(
        ["Gateway", "API", "Installments", "Hosted", "Bit", "Money unit"],
        rows,
        "Pricing is quoted per merchant and is not published by any of these "
        "gateways. Ask each one for a quote.",
    )


def print_refund_table(gateways: dict) -> None:
    """Print the void / refund / partial-refund matrix."""
    rows = [[gw.name, gw.void_call, gw.refund_call, gw.partial_refund]
            for gw in gateways.values()]
    _print_grid(
        ["Gateway", "Void (pre-settlement)", "Refund / credit", "Partial"],
        rows,
        "'unverified' means no public source was found, NOT that the "
        "capability is absent. Confirm with the gateway before relying on it.",
    )


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Compare Israeli payment gateways "
                    "(השוואת שערי תשלום ישראליים)"
    )
    parser.add_argument(
        "--features",
        help="Required features, comma-separated: " + ", ".join(FEATURE_KEYS)
    )
    parser.add_argument(
        "--refunds", action="store_true",
        help="Show the void / refund / partial-refund matrix"
    )
    parser.add_argument(
        "--all", action="store_true",
        help="Show all gateways comparison"
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Output as JSON"
    )
    parser.add_argument(
        "--example", action="store_true",
        help="Show example comparison"
    )

    args = parser.parse_args()

    # Explicit None checks: a falsy-but-supplied argument is still an argument.
    if not (args.features is not None or args.refunds or args.all
            or args.example or args.json):
        parser.print_help()
        sys.exit(1)

    gateways = GATEWAYS.copy()

    if args.example:
        print("=== All Gateways: Capabilities ===")
        print_comparison_table(gateways)
        print("\n=== Void / Refund / Partial Refund ===")
        print_refund_table(gateways)
        print("\n=== Gateways with documented Bit support ===")
        bit_gateways, uncertain = filter_by_features(gateways, ["bit"])
        print_comparison_table(bit_gateways)
        if uncertain:
            print(f"Support unverified (not necessarily absent): "
                  f"{', '.join(uncertain)}")
        return

    uncertain = []
    if args.features is not None:
        try:
            gateways, uncertain = filter_by_features(
                gateways, args.features.split(",")
            )
        except NotAGatewayCapability as exc:
            print(exc, file=sys.stderr)
            sys.exit(3)
        except UnknownFeature as exc:
            print(f"Unknown feature: {exc}. Known features: "
                  f"{', '.join(FEATURE_KEYS)}", file=sys.stderr)
            sys.exit(2)
        if not gateways:
            print(f"No gateways match features: {args.features}")
            if uncertain:
                print(f"Support unverified (not necessarily absent): "
                      f"{', '.join(uncertain)}")
            sys.exit(1)

    if args.json:
        print(json.dumps(
            {name: asdict(gw) for name, gw in gateways.items()},
            indent=2, ensure_ascii=False
        ))
        return

    print_comparison_table(gateways)
    if uncertain:
        print(f"Support unverified (not necessarily absent): "
              f"{', '.join(uncertain)}")
    if args.refunds:
        print_refund_table(gateways)


if __name__ == "__main__":
    main()
