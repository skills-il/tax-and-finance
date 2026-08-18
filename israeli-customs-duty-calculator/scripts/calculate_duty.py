#!/usr/bin/env python3
"""
calculate_duty.py - Israeli landed-cost calculator.

Computes the cascading tax sequence used by Israeli Customs:
  CIF -> customs duty -> purchase tax -> VAT -> landed cost.

Constants:
  - Israel VAT rate: 18% (since January 1, 2025).
  - Personal import threshold: USD 75 (as of July 2026). The threshold
    moved 75 -> 150 in December 2025, was revoked back to 75 by the
    Knesset on 24 February 2026, was reset to 130 by a new Finance
    Ministry order effective 25 February 2026, and reverted to 75 when
    the USD 130 window ran to 1 June 2026. It has moved four times
    in seven months; confirm via the official calculator before quoting.
  - Two different bases: the exemption THRESHOLD is tested on the goods
    value alone (excluding shipping and insurance), while the TAX is computed
    on the CIF value plus any duty and purchase tax.
  - The USD 75-500 duty waiver is NOT modelled here: pass --duty-rate 0 for a
    personal import in that band.
  - Tobacco products and alcoholic beverages are EXCLUDED
    from the personal-import exemption regardless of value. This script
    does NOT model that exclusion automatically; callers must override
    --personal for those product categories.

Sources for each constant are cited in the skill's evidence.json.

Usage:
  python calculate_duty.py --value 200 --shipping 20 --insurance 5 \\
      --currency USD --fx 3.65 \\
      --duty-rate 0 --purchase-tax-rate 0 \\
      --personal

Exit 0 on success.
"""

from __future__ import annotations

import argparse
import json
import sys
from decimal import Decimal, ROUND_HALF_UP
from typing import Optional

# Constants grounded in evidence.json
PERSONAL_IMPORT_DUTY_WAIVER_CEILING_USD = Decimal("500")
VAT_RATE = Decimal("0.18")
PERSONAL_IMPORT_THRESHOLD_USD = Decimal("75")


def money(x: Decimal) -> Decimal:
    """Round to 2 decimal places, banker's rounding is avoided for clarity."""
    return x.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def calculate_landed_cost(
    product_value: Decimal,
    shipping: Decimal,
    insurance: Decimal,
    fx_rate: Decimal,
    duty_rate: Decimal,
    purchase_tax_rate: Decimal,
    broker_fees_ils: Decimal,
    currency: str,
    personal_import: bool,
    usd_value: Decimal = None,
    excluded_goods: bool = False,
) -> dict:
    """Compute full landed cost breakdown. All outputs are in ILS."""
    # Personal-import threshold check. The threshold is denominated in USD and
    # tested on the goods value alone, excluding shipping and insurance. For a
    # non-USD invoice the caller must supply the USD equivalent, otherwise the
    # exemption cannot be evaluated and the goods would be silently taxed.
    goods_usd = product_value if currency.upper() == "USD" else usd_value
    duty_waived = False
    if personal_import and goods_usd is None:
        raise ValueError(
            f"--personal with a {currency.upper()} invoice requires --usd-value: "
            "the exemption threshold is denominated in USD and cannot be applied "
            "without the USD equivalent of the goods value."
        )
    if personal_import and excluded_goods:
        pass  # tobacco and alcohol never qualify; fall through to the taxed path
    elif personal_import and goods_usd is not None:
        # "up to 75 dollars" is inclusive of 75.
        if goods_usd <= PERSONAL_IMPORT_THRESHOLD_USD:
            return {
                "exempt": True,
                "reason": f"Goods value {goods_usd} USD is at or below the personal import threshold of {PERSONAL_IMPORT_THRESHOLD_USD} USD.",
                "cif_ils": money((product_value + shipping + insurance) * fx_rate),
                "duty_ils": Decimal("0.00"),
                "purchase_tax_ils": Decimal("0.00"),
                "vat_ils": Decimal("0.00"),
                "broker_fees_ils": money(broker_fees_ils),
                "landed_cost_ils": money((product_value + shipping + insurance) * fx_rate + broker_fees_ils),
            }

    # Under the personal-import regime customs duty is waived between the
    # threshold and USD 500; only VAT (and purchase tax where the goods carry
    # it) applies. Enforce it rather than trusting the caller to pass 0.
    if (
        personal_import
        and not excluded_goods
        and goods_usd is not None
        and goods_usd <= PERSONAL_IMPORT_DUTY_WAIVER_CEILING_USD
        and duty_rate > 0
    ):
        duty_rate = Decimal("0")
        duty_waived = True

    # CIF in ILS
    cif_foreign = product_value + shipping + insurance
    cif_ils = cif_foreign * fx_rate

    # Cascading calculation
    duty = cif_ils * duty_rate
    base_after_duty = cif_ils + duty
    purchase_tax = base_after_duty * purchase_tax_rate
    base_for_vat = base_after_duty + purchase_tax
    vat = base_for_vat * VAT_RATE

    landed = cif_ils + duty + purchase_tax + vat + broker_fees_ils

    return {
        "exempt": False,
        "duty_waived_personal_import": duty_waived,
        "cif_ils": money(cif_ils),
        "duty_ils": money(duty),
        "purchase_tax_ils": money(purchase_tax),
        "vat_ils": money(vat),
        "broker_fees_ils": money(broker_fees_ils),
        "landed_cost_ils": money(landed),
        "inputs": {
            "product_value_foreign": str(product_value),
            "shipping_foreign": str(shipping),
            "insurance_foreign": str(insurance),
            "currency": currency.upper(),
            "fx_rate": str(fx_rate),
            "duty_rate": str(duty_rate),
            "purchase_tax_rate": str(purchase_tax_rate),
            "vat_rate": str(VAT_RATE),
        },
    }


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Israeli landed-cost calculator (customs + purchase tax + VAT).",
    )
    p.add_argument("--value", type=Decimal, required=True, help="Product value in the invoice currency.")
    p.add_argument("--shipping", type=Decimal, default=Decimal("0"), help="Freight cost in invoice currency.")
    p.add_argument("--insurance", type=Decimal, default=Decimal("0"), help="Insurance cost in invoice currency.")
    p.add_argument("--currency", type=str, default="USD", help="Invoice currency (USD, EUR, GBP, etc.).")
    p.add_argument("--fx", type=Decimal, required=True, help="Foreign currency to ILS rate (e.g. USD->ILS).")
    p.add_argument("--duty-rate", type=Decimal, default=Decimal("0"), help="Customs duty rate as decimal (0.08 = 8 percent).")
    p.add_argument("--purchase-tax-rate", type=Decimal, default=Decimal("0"), help="Purchase tax rate as decimal.")
    p.add_argument("--broker-fees-ils", type=Decimal, default=Decimal("0"), help="Broker and handling fees in ILS.")
    p.add_argument("--personal", action="store_true", help="Personal import (applies the USD threshold exemption).")
    p.add_argument("--usd-value", type=Decimal, default=None, help="Goods value in USD. Required with --personal when the invoice is not in USD.")
    p.add_argument("--excluded-goods", action="store_true", help="Tobacco, cigarettes or alcoholic beverages: never exempt, taxed from the first shekel.")
    p.add_argument("--json", action="store_true", help="Output as JSON.")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    if args.fx <= 0:
        print("Error: --fx must be greater than 0.", file=sys.stderr)
        return 1
    for name, val in (("--value", args.value), ("--shipping", args.shipping),
                      ("--insurance", args.insurance), ("--broker-fees-ils", args.broker_fees_ils)):
        if val < 0:
            print(f"Error: {name} cannot be negative.", file=sys.stderr)
            return 1
    for name, val in (("--duty-rate", args.duty_rate), ("--purchase-tax-rate", args.purchase_tax_rate)):
        if val > 1:
            print(f"Error: {name} is a decimal fraction (0.12 = 12 percent), got {val}.", file=sys.stderr)
            return 1
    try:
        result = calculate_landed_cost(
            product_value=args.value,
            shipping=args.shipping,
            insurance=args.insurance,
            fx_rate=args.fx,
            duty_rate=args.duty_rate,
            purchase_tax_rate=args.purchase_tax_rate,
            broker_fees_ils=args.broker_fees_ils,
            currency=args.currency,
            personal_import=args.personal,
            usd_value=args.usd_value,
            excluded_goods=args.excluded_goods,
        )
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps({k: str(v) if isinstance(v, Decimal) else v for k, v in result.items()}, indent=2, ensure_ascii=False))
        return 0

    if result.get("exempt"):
        print(f"EXEMPT: {result['reason']}")
        print(f"Estimated delivered cost (no taxes): {result['landed_cost_ils']} ILS")
        return 0

    print("Israeli landed-cost breakdown")
    print(f"  CIF:              {result['cif_ils']} ILS")
    print(f"  Customs duty:     {result['duty_ils']} ILS")
    print(f"  Purchase tax:     {result['purchase_tax_ils']} ILS")
    print(f"  VAT:              {result['vat_ils']} ILS")
    print(f"  Broker fees:      {result['broker_fees_ils']} ILS")
    print(f"  Total landed:     {result['landed_cost_ils']} ILS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
