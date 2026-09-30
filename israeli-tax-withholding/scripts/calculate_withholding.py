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
# certificate from the assessing officer sets a reduced rate or an exemption.
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
    "interest": 0.25,          # 25% - 2005 regs, interest to an individual
                               #       (15% on a non-index-linked asset: pass
                               #       --certificate-rate 15)
    "interest_non_linked": 0.15,  # 2005 regs: interest to an individual on
                                  #       an asset that is not index-linked
    "interest_company": 0.23,  # 2005 regs reg. 7: the maximum rate, which for a
                               #       company is the s.126(a) corporate rate
    "dividends": 0.25,         # 25% - 2005 regs, dividend to an individual
    "dividends_major": 0.30,   # 30% - substantial shareholder (10% or more)
    # Building and haulage, regs. 1973: 20% base; 17% / 15% only with the
    # assessing officer's written approval (pass --certificate-rate); 10 points
    # higher where the payee has no acceptable books (reg. 2(c)).
    "contractor": 0.20,
    "contractor_no_books": 0.30,
    # Agriculture, regs. 1979: work 20%, produce 5%; 10 points higher without
    # acceptable books.
    "agricultural_work": 0.20,
    "agricultural_work_no_books": 0.30,
    "agricultural_produce": 0.05,
    "agricultural_produce_no_books": 0.15,
    # Section 170(a) fixes the non-resident rate in the statute itself: 25% for
    # an individual payee, the s.126 corporate rate for a company. Treaty relief
    # is NOT automatic. Paid to the assessing officer within 7 days (s.171).
    "non_resident_individual": 0.25,
    "non_resident_company": 0.23,
}

# Payment types whose deadline is not the monthly 16th cycle.
SEVEN_DAY_TYPES = {"non_resident_individual", "non_resident_company"}

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
        "Agriculture has two rates under the 1979 regulations: work 20%, produce "
        "5%. Use --type agricultural_work or agricultural_produce (or the "
        "_no_books variants, 10 points higher)."
    ),
    "dividends_company": (
        "A dividend from an Israeli company to an Israeli-resident company is "
        "withheld only where a limited tax rate applies to it under any law "
        "(reg. 2(a1) of the 2005 regulations), at that rate."
    ),
    "interest_related": (
        "Interest a company pays to its substantial shareholder, its employee, or "
        "its supplier is withheld at the maximum rate (reg. 6 of the 2005 "
        "regulations): for an individual, the top rate in section 121."
    ),
    "non_resident": (
        "Section 170(a) sets different statutory rates by payee: 25% for an "
        "individual and the 23% corporate rate for a company. Use --type "
        "non_resident_individual or non_resident_company. A treaty rate is not "
        "self-executing."
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
    "prizes": (
        "Gambling, lottery and prize income is withheld under s.164 by reference "
        "to s.2A. The substantive tax rate under s.124B is 35% with no "
        "exemption, relief, deduction, credit or offset (other than an "
        "exemption under s.9(28) or a deduction under s.17(11)), but the operative "
        "withholding rate is set by its own regulations and is not encoded here."
    ),
}


# reg. 2(a) of the 1977 regulations: no withholding on a payment for an asset or
# service whose value does not exceed the amount in s.2(b) of the Public Bodies
# Transactions Law (5,520 NIS). Applies to the 1977 services/assets types only.
DE_MINIMIS = 5520
DE_MINIMIS_TYPES = {"services", "services_with_books", "services_no_books",
                    "services_company"}

# Payments on which no Israeli VAT line belongs to the payee: interest and
# dividends are not a supply, and a foreign supplier does not charge Israeli VAT.
NO_VAT_TYPES = {"interest", "interest_non_linked", "interest_company",
                "dividends", "dividends_major",
                "non_resident_individual", "non_resident_company"}


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
    note: str = ""


def calculate_withholding(
    payment_type: str,
    amount: float,
    certificate_rate: float = None,
    include_vat: bool = None,
    payer_bears_tax: bool = False,
) -> WithholdingResult:
    """Calculate withholding amount for a payment.

    Args:
        payment_type: Type of payment (services, rent, interest, etc.).
        amount: Payment amount before VAT in NIS. With payer_bears_tax, this is
            the NET amount the payee must receive.
        certificate_rate: Reduced rate from a withholding certificate, as a
            percentage. None means use the default rate.
        include_vat: Whether to add a VAT line. None means the default for the
            type (no VAT line for interest, dividends and non-resident types).
        payer_bears_tax: Gross the payment up so the payee receives `amount`
            net, with tax = net x rate / (1 - rate).

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
    if amount is None or amount <= 0:
        raise ValueError("Amount must be a positive number of NIS.")
    if certificate_rate is not None and not 0 <= certificate_rate < 100:
        raise ValueError("--certificate-rate must be at least 0 and below 100.")
    if include_vat is None:
        include_vat = payment_type not in NO_VAT_TYPES

    note = ""
    has_certificate = certificate_rate is not None
    rate = certificate_rate / 100 if has_certificate else DEFAULT_RATES[payment_type]
    # The de-minimis removes the duty itself, so it applies with or without a
    # certificate. Under gross-up it is tested on the net: if no duty applies,
    # nothing is grossed and the base equals the net.
    if payment_type in DE_MINIMIS_TYPES and amount <= DE_MINIMIS:
        rate = 0.0
        note = (f"De-minimis: a service or asset worth no more than {DE_MINIMIS:,} "
                f"NIS is outside reg. 2(a). The test is the value of that service "
                f"or asset, not one invoice of a larger engagement, and the "
                f"regulation does not say whether the figure includes VAT.")
        if payer_bears_tax and amount / (1 - DEFAULT_RATES[payment_type]) > DE_MINIMIS:
            note += (" Under gross-up the grossed value would exceed the "
                     "threshold; treat this band as uncertain.")

    if payer_bears_tax:
        gross = round(amount / (1 - rate), 2)
        withholding = round(gross - amount, 2)
        net_payment = round(amount, 2)
        if rate > 0:
            note = (f"Grossed up: the payer bears the tax, so the base is "
                    f"{gross:,.2f} and the payee receives {amount:,.2f} net.")
    else:
        gross = round(amount, 2)
        withholding = round(amount * rate, 2)
        net_payment = round(amount - withholding, 2)
    vat = round(gross * VAT_RATE, 2) if include_vat else 0.0
    total_invoice = round(gross + vat, 2)

    return WithholdingResult(
        payment_type=payment_type,
        gross_amount=gross,
        withholding_rate=rate,
        withholding_amount=withholding,
        net_payment=net_payment,
        vat_amount=vat,
        total_invoice=total_invoice,
        certificate_rate=has_certificate,
        note=note,
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
    ]
    if result.note:
        lines += [f"  NOTE: {result.note}"]
    lines += [
        f"  Withholding is on the pre-VAT amount. The VAT line assumes a payee",
        f"  that charges VAT (an osek murshe); pass --no-vat otherwise.",
    ]
    if result.payment_type in SEVEN_DAY_TYPES:
        lines += [
            f"  Section 170 withholding is paid to the assessing officer within",
            f"  7 days of withholding, with a report (section 171).",
        ]
    else:
        lines += [
            f"  Report and pay by the 16th of the following month (reg. 4 of the",
            f"  1977 regulations, form 0852; Form 102 is the periodic deductions",
            f"  report). The 15th is the Bituach Leumi date, not this one. The",
            f"  annual per-payee reconciliation is Form 856, online by 30 April",
            f"  (Ordinance section 166(b)).",
        ]
    lines += [
        f"  With no certificate the services default is 20% where the payee keeps",
        f"  acceptable books and 30% where they do not; a valid certificate sets",
        f"  a reduced rate or an exemption. Confirm the payee's operative rate at",
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
        "--payer-bears-tax", action="store_true",
        help="Treat --amount as the net the payee must receive and gross it up"
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
        print(f"  {'Type':<30} {'Rate':>6}  Section")
        print(f"  {'─' * 42}")
        sections = {
            "services": "164 / reg. 1977",
            "services_with_books": "164 / reg. 1977",
            "services_no_books": "164 / reg. 1977",
            "services_company": "164 / reg. 1977",
            "rent": "164 / reg. 1998",
            "rent_residential": "164 / reg. 1998",
            "interest": "164 / reg. 2005",
            "interest_non_linked": "164 / reg. 2005",
            "interest_company": "164 / reg. 2005",
            "dividends": "164 / reg. 2005",
            "dividends_major": "164 / reg. 2005",
            "contractor": "164 / reg. 1973",
            "contractor_no_books": "164 / reg. 1973",
            "agricultural_work": "164 / reg. 1979",
            "agricultural_work_no_books": "164 / reg. 1979",
            "agricultural_produce": "164 / reg. 1979",
            "agricultural_produce_no_books": "164 / reg. 1979",
            "non_resident_individual": "170(a)",
            "non_resident_company": "170(a) + 126",
        }
        for ptype, rate in DEFAULT_RATES.items():
            print(f"  {ptype:<30} {rate*100:>5.0f}%  {sections.get(ptype, '164')}")
        print()
        print("  Types with no single encoded rate (pick a listed variant, or look up per payee):")
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
            False if args.no_vat else None,
            args.payer_bears_tax,
        )
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(2)
    print(format_result(result))


if __name__ == "__main__":
    main()
