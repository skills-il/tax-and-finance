#!/usr/bin/env python3
"""
calculate_duty.py - Israeli landed-cost calculator.

Computes the cascading tax sequence used by Israeli Customs:
  CIF -> customs duty -> purchase tax -> VAT -> landed cost.

Constants:
  - Israel VAT rate: 18% (since January 1, 2025).
  - Personal import threshold: USD 75 (as of April 2026, after Knesset
    reversed the November 2025 Smotrich decree that had raised it to USD 150).

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
) -> dict:
    """Compute full landed cost breakdown. All outputs are in ILS."""
    # Personal-import threshold check (USD basis, excludes shipping and insurance)
    if personal_import and currency.upper() == "USD":
        if product_value < PERSONAL_IMPORT_THRESHOLD_USD:
            return {
                "exempt": True,
                "reason": f"Product value {product_value} USD is below the personal import threshold of {PERSONAL_IMPORT_THRESHOLD_USD} USD.",
                "cif_ils": money((product_value + shipping + insurance) * fx_rate),
                "duty_ils": Decimal("0.00"),
                "purchase_tax_ils": Decimal("0.00"),
                "vat_ils": Decimal("0.00"),
                "broker_fees_ils": money(broker_fees_ils),
                "landed_cost_ils": money((product_value + shipping + insurance) * fx_rate + broker_fees_ils),
            }

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
    p.add_argument("--json", action="store_true", help="Output as JSON.")
    return p.parse_args()


def main() -> int:
    args = parse_args()
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
    )

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
