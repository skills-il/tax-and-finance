#!/usr/bin/env python3
"""Calculate Israeli tax withholding (nikui mas bemakor) amounts.

Determines the correct withholding rate for a payment type and calculates
the withholding amount, net payment, and VAT.

Usage:
    python scripts/calculate_withholding.py --type services --amount 10000
    python scripts/calculate_withholding.py --type rent --amount 5000 --certificate-rate 10
    python scripts/calculate_withholding.py --example
"""

import sys
import argparse
from dataclasses import dataclass


VAT_RATE = 0.17  # Standard Israeli VAT rate

# Default withholding rates by payment type
DEFAULT_RATES = {
    "services": 0.20,          # 20% - Section 164
    "services_company": 0.25,  # 25% - Section 164 (companies)
    "rent": 0.35,              # 35% - Section 170
    "royalties": 0.23,         # 23% - Section 170
    "interest": 0.25,          # 25% - Section 164
    "dividends": 0.25,         # 25% - Section 164
    "dividends_major": 0.30,   # 30% - Major shareholder (>10%)
    "non_resident": 0.25,      # 25% - Section 170
    "contractor": 0.20,        # 20% - Construction services
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
        certificate_rate: Reduced rate from withholding certificate (0-100%).
            None means use default rate.
        include_vat: Whether to calculate VAT on the payment.

    Returns:
        WithholdingResult with all calculated amounts.
    """
    if payment_type not in DEFAULT_RATES:
        raise ValueError(
            f"Unknown payment type: {payment_type}. "
            f"Valid types: {list(DEFAULT_RATES.keys())}"
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
        f"  VAT (17%):           +{result.vat_amount:>10,.2f} NIS",
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
        f"  NOTE: Withholding is on pre-VAT amount. VAT is paid separately.",
        f"  Report on Form 856 by the 15th of the following month.",
    ]
    return "\n".join(lines)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Calculate Israeli tax withholding (nikui mas bemakor)"
    )
    parser.add_argument(
        "--type", dest="payment_type",
        choices=list(DEFAULT_RATES.keys()),
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
        for ptype, rate in DEFAULT_RATES.items():
            section = "164" if ptype in ("services", "services_company", "interest", "dividends", "dividends_major") else "170"
            print(f"  {ptype:<22} {rate*100:>5.0f}%  {section}")
        return

    if args.example:
        print("Example 1: Payment to freelancer (no certificate)")
        result = calculate_withholding("services", 10000)
        print(format_result(result))
        print()
        print("Example 2: Payment to vendor with 5% certificate")
        result = calculate_withholding("services", 10000, certificate_rate=5)
        print(format_result(result))
        return

    if not args.payment_type or args.amount is None:
        parser.print_help()
        sys.exit(1)

    result = calculate_withholding(
        args.payment_type,
        args.amount,
        args.certificate_rate,
        not args.no_vat,
    )
    print(format_result(result))


if __name__ == "__main__":
    main()
