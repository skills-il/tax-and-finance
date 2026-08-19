#!/usr/bin/env python3
"""Calculate Israeli tax withholding (nikui mas bemakor) amounts.

Determines the correct withholding rate for a payment type and calculates the
withholding amount, net payment, and VAT.

Usage:
    python scripts/calculate_withholding.py --type services --amount 10000
    python scripts/calculate_withholding.py --type rent --amount 5000 --certificate-rate 10
    python scripts/calculate_withholding.py --example
"""

import sys
import argparse
from dataclasses import dataclass


VAT_RATE = 0.18  # Standard Israeli VAT rate (raised from 17% on Jan 1, 2025)

# Default withholding rates by payment type, used when the payee has no
# withholding certificate. These are the no-certificate ITA defaults; a valid
# certificate typically brings the rate down to 0-5%.
DEFAULT_RATES = {
    # reg. 2(a) of the 1977 regulations: the BASE rate, and the ordinary case.
    # This is the correct starting point for a compliant payee. Only move to
    # services_no_books once you know the payee failed the books/returns test.
    "services": 0.20,
    "services_with_books": 0.20,  # explicit alias for "services"
    "services_no_books": 0.30,    # reg. 2(b) sanction rate for a payee who did
                                  # not prove acceptable books + timely returns
    # reg. 2 draws no individual/company distinction: a company payee sits on the
    # same 20% base and 30% sanction. The "20-30%" range often quoted for
    # companies reflects the assessing officer's classification on the payee's
    # certificate, not a different statutory default, so start at the base.
    "services_company": 0.20,
    "rent": 0.35,              # 35% - uniform rate for real estate the tenant
                               #       deducts as a business expense
    "rent_residential": 0.35,  # 35% - no separate residential rate exists;
                               #       alias kept for backward compatibility
    "interest": 0.25,          # 25% - Section 164
    "dividends": 0.25,         # 25% - Section 164
    "dividends_major": 0.30,   # 30% - substantial shareholder (10% or more)
    "non_resident": 0.25,      # Section 170; commonly 25%, but treaty relief is
                               # NOT automatic and needs prior ITA approval
}

# Statutory withholding categories that this skill deliberately does NOT price,
# because no rate for them was verified against a primary source. Emitting a
# guess here would be worse than emitting nothing: the caller cannot tell an
# invented number from a sourced one. A previous version of this file carried
# a hardcoded royalties rate that was really the corporate tax rate wearing a
# withholding label. Route these to the ITA's per-payee lookup instead.
LOOKUP_URL = "https://www.misim.gov.il/gmishurim/frmInputMekabel.aspx"

UNPRICED_TYPES = {
    "royalties": (
        "The 1977 regulations create no separate royalties withholding category. "
        "To an Israeli resident, use --type services (20%) or services_no_books "
        "(30%). To a non-resident, withholding is set under Section 170 and "
        "normally needs the assessing officer's involvement; a treaty rate is "
        "not self-executing."
    ),
    "agricultural": (
        "Payment for agricultural work or agricultural produce is a statutory "
        "withholding category (Income Tax Ordinance s.166(c)(4), under s.164), "
        "but its rate lives in its own regulations and is not encoded here."
    ),
    "diamonds": (
        "Payment for diamond processing or diamond trading is a statutory "
        "withholding category (Income Tax Ordinance s.166(c)(7), under s.164), "
        "but its rate lives in its own regulations and is not encoded here."
    ),
    "insurance_commission": (
        "Insurance commission is a statutory withholding category (Income Tax "
        "Ordinance s.166(c)(1), under s.164). The 20% figure in circulation is "
        "not verified against a primary source in this skill, so it is not "
        "encoded."
    ),
    "contractor": (
        "Building and haulage work is its own statutory withholding category "
        "(Income Tax Ordinance s.166(c)(5), under s.164) with its own "
        "regulations. The 30% figure previously hardcoded here was not verified "
        "against a primary source, so it is not encoded. For a plain service or "
        "asset payment to a contractor, use --type services or services_no_books."
    ),
    "prizes": (
        "Gambling, lottery and prize income is withheld under s.164 by reference "
        "to s.2A. The substantive tax rate under s.124B is 35% with no "
        "exemption, relief, deduction, credit or offset, but the operative "
        "withholding rate is set by its own regulations and is not encoded here."
    ),
}


@dataclass
class WithholdingResult:
    """Withholding calculation result."""
    payment_type: str
    gross_amount: float
    withholding_rate: float
    withholding_amount: float
    net_payment: float
    vat_amount: float
    total_invoice: float
    certificate_rate: bool


def calculate_withholding(
    payment_type: str,
    amount: float,
    certificate_rate: float = None,
    include_vat: bool = True,
) -> WithholdingResult:
    """Calculate withholding amount for a payment.

    Args:
        payment_type: Type of payment (services, rent, royalties, etc.).
        amount: Payment amount before VAT in NIS.
        certificate_rate: Reduced rate from withholding certificate, as a percentage.
            None means use default rate.
        include_vat: Whether to calculate VAT on the payment.

    Returns:
        WithholdingResult with all calculated amounts.
    """
    if payment_type in UNPRICED_TYPES:
        raise ValueError(
            f"No withholding rate is encoded for '{payment_type}'.\n"
            f"{UNPRICED_TYPES[payment_type]}\n"
            f"Look the payee's operative rate up at {LOOKUP_URL}, or pass an "
            f"explicit --certificate-rate."
        )
    if payment_type not in DEFAULT_RATES:
        raise ValueError(
            f"Unknown payment type: {payment_type}. "
            f"Valid types: {list(DEFAULT_RATES.keys())}. "
            f"Categories with no encoded rate: {list(UNPRICED_TYPES.keys())}"
        )

    has_certificate = certificate_rate is not None
    rate = certificate_rate / 100 if has_certificate else DEFAULT_RATES[payment_type]

    withholding = round(amount * rate, 2)
    net_payment = round(amount - withholding, 2)
    vat = round(amount * VAT_RATE, 2) if include_vat else 0.0
    total_invoice = round(amount + vat, 2)

    return WithholdingResult(
        payment_type=payment_type,
        gross_amount=amount,
        withholding_rate=rate,
        withholding_amount=withholding,
        net_payment=net_payment,
        vat_amount=vat,
        total_invoice=total_invoice,
        certificate_rate=has_certificate,
    )


def format_result(result: WithholdingResult) -> str:
    """Format withholding calculation for display."""
    rate_source = "certificate" if result.certificate_rate else "default"
    lines = [
        f"=== Israeli Tax Withholding Calculation ===",
        f"",
        f"  Payment Type:         {result.payment_type}",
        f"  Gross Amount:         {result.gross_amount:>10,.2f} NIS",
        f"  VAT (18%):           +{result.vat_amount:>10,.2f} NIS",
        f"  Total Invoice:        {result.total_invoice:>10,.2f} NIS",
        f"",
        f"  Withholding Rate:     {result.withholding_rate * 100:>9.1f}% ({rate_source})",
        f"  Withholding Amount:  -{result.withholding_amount:>10,.2f} NIS",
        f"  Net Payment to Payee: {result.net_payment:>10,.2f} NIS",
        f"",
        f"  Payment breakdown:",
        f"    To payee:           {result.net_payment:>10,.2f} NIS",
        f"    To Tax Authority:   {result.withholding_amount:>10,.2f} NIS",
        f"    VAT to payee:      +{result.vat_amount:>10,.2f} NIS",
        f"    Total disbursed:    {result.net_payment + result.withholding_amount + result.vat_amount:>10,.2f} NIS",
        f"",
        f"  NOTE: Withholding is on the pre-VAT amount. VAT is paid separately.",
        f"  Report and pay by the 16th of the following month (reg. 4 of the",
        f"  1977 regulations, form 0852; Form 102 is the periodic deductions",
        f"  report). The 15th is the Bituach Leumi date, not this one. The",
        f"  annual per-payee reconciliation is Form 856, due April 30 of the",
        f"  following year.",
        f"  With no certificate the services default is 20% where the payee keeps",
        f"  acceptable books and 30% where they do not; a valid certificate usually",
        f"  reduces it to 0-5%. Confirm the payee's operative rate at",
        f"  {LOOKUP_URL}",
    ]
    return "\n".join(lines)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Calculate Israeli tax withholding (nikui mas bemakor)"
    )
    parser.add_argument(
        "--type", dest="payment_type",
        choices=list(DEFAULT_RATES.keys()) + list(UNPRICED_TYPES.keys()),
        help="Payment type"
    )
    parser.add_argument("--amount", type=float, help="Payment amount (before VAT)")
    parser.add_argument(
        "--certificate-rate", type=float, default=None,
        help="Reduced rate from withholding certificate (percentage, e.g., 10 for 10%%)"
    )
    parser.add_argument(
        "--no-vat", action="store_true", help="Exclude VAT calculation"
    )
    parser.add_argument(
        "--example", action="store_true", help="Show example calculations"
    )
    parser.add_argument(
        "--rates", action="store_true", help="Show default withholding rates"
    )

    args = parser.parse_args()

    if args.rates:
        print("=== Default Israeli Tax Withholding Rates ===")
        print(f"  {'Type':<22} {'Rate':>6}  Section")
        print(f"  {'─' * 42}")
        sections = {
            "services": "164 / reg. 1977",
            "services_with_books": "164 / reg. 1977",
            "services_no_books": "164 / reg. 1977",
            "services_company": "164 / reg. 1977",
            "rent": "164 / reg. 1998",
            "rent_residential": "164 / reg. 1998",
            "interest": "164",
            "dividends": "164",
            "dividends_major": "164",
            "non_resident": "170",
        }
        for ptype, rate in DEFAULT_RATES.items():
            print(f"  {ptype:<22} {rate*100:>5.0f}%  {sections.get(ptype, '164')}")
        print()
        print("  Statutory categories with NO encoded rate (look them up per payee):")
        for ptype, why in UNPRICED_TYPES.items():
            print(f"  {ptype:<22}   {why.split('.')[0]}.")
        print(f"  Per-payee lookup: {LOOKUP_URL}")
        return

    if args.example:
        print("Example 1: Payment to a compliant freelancer (no certificate)")
        result = calculate_withholding("services", 10000)
        print(format_result(result))
        print()
        print("Example 2: Same payment, payee could not prove acceptable books")
        result = calculate_withholding("services_no_books", 10000)
        print(format_result(result))
        print()
        print("Example 3: Payment to vendor with 5% certificate")
        result = calculate_withholding("services", 10000, certificate_rate=5)
        print(format_result(result))
        return

    if not args.payment_type or args.amount is None:
        parser.print_help()
        sys.exit(1)

    try:
        result = calculate_withholding(
            args.payment_type,
            args.amount,
            args.certificate_rate,
            not args.no_vat,
        )
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(2)
    print(format_result(result))


if __name__ == "__main__":
    main()
