#!/usr/bin/env python3
"""Calculate Israeli VAT liability for periodic reporting.

Computes net VAT from sales (output) and purchase (input) records,
applies Israeli deduction rules, and maps results to the periodic VAT return fields.

Usage:
    python scripts/calculate_vat.py --sales 100000 --purchases 60000
    python scripts/calculate_vat.py --json transactions.json
    python scripts/calculate_vat.py --example
"""

import sys
import json
import argparse
from dataclasses import dataclass, field, asdict
from typing import Optional


VAT_RATE = 0.18  # 18% standard Israeli VAT rate (effective January 2025)

# Non-deductible expense categories
# private_car_purchase: VAT Regulations reg. 14 (buying/importing a private car)
# entertainment: reg. 16 (except entertaining a person from abroad)
NON_DEDUCTIBLE = {"entertainment", "private_car_purchase"}

# Partially deductible categories (reg. 18(b), mixed use, no Director ratio)
PARTIAL_DEDUCTIBLE = {
    "vehicle_running_mainly_business": 2 / 3,  # running costs only (fuel, upkeep)
    "vehicle_running_mainly_private": 1 / 4,   # running costs only
    "mixed_use_mainly_business": 2 / 3,        # other mixed-use inputs
    "mixed_use_mainly_private": 1 / 4,
}
VEHICLE_CATEGORIES = {"private_car_purchase", *PARTIAL_DEDUCTIBLE}

# Fully deductible categories (anything else is rejected, not silently deducted).
FULL_DEDUCTIBLE = {"general", "equipment", "rent", "services", "inventory"}
# Only when the Director has set a ratio for this dealer; needs "director_ratio" (0..1).
DIRECTOR_RATIO = "director_set_ratio"  # when the Director set a ratio for the dealer, that ratio applies instead of 2/3 or 1/4

SALE_TYPES = {"standard", "zero_rated", "export", "exempt"}


@dataclass
class VATReport:
    """Israeli periodic VAT return structure."""
    period: str = ""
    taxable_sales_base: float = 0.0         # taxable sales, net base EXCLUDING VAT
    zero_rated_sales: float = 0.0           # zero-rated sales
    exempt_sales: float = 0.0               # exempt sales
    output_vat: float = 0.0                 # output VAT
    equipment_inputs_base: float = 0.0      # working figure
    other_inputs_base: float = 0.0          # working figure
    equipment_input_vat: float = 0.0        # input VAT on equipment / fixed assets
    other_input_vat: float = 0.0            # input VAT on other inputs
    input_vat_claimed: float = 0.0          # total input VAT
    net_vat: float = 0.0                    # net VAT
    adjustments: float = 0.0               # adjustments
    amount_due: float = 0.0                # amount to pay


def calculate_output_vat(
    sales: list[dict],
) -> tuple[float, float, float, float]:
    """Calculate output VAT from sales records.

    Args:
        sales: List of sale records with 'amount', 'type' fields.

    Returns:
        Tuple of (taxable_sales_base_excl_vat, zero_rated, exempt, output_vat).
    """
    taxable_base = 0.0
    zero_rated = 0.0
    exempt = 0.0
    output_vat = 0.0

    for sale in sales:
        amount = sale.get("amount", 0)
        sale_type = sale.get("type", "standard")
        if sale_type not in SALE_TYPES:
            raise ValueError(f"Unknown sale type: {sale_type!r} (use one of {sorted(SALE_TYPES)})")

        if sale_type in ("zero_rated", "export"):
            zero_rated += amount  # zero-rated box, not in the taxable base
        elif sale_type == "exempt":
            exempt += amount  # exempt box, not in the taxable base
        else:
            vat = round(amount * VAT_RATE, 2)
            output_vat += vat
            taxable_base += amount  # net base; its VAT is output VAT

    return taxable_base, zero_rated, exempt, output_vat


def calculate_input_vat(purchases: list[dict]) -> tuple[float, float, float, float]:
    """Calculate deductible input VAT from purchase records.

    Applies Israeli deduction rules: private car purchase and entertainment
    not deductible (regs. 14, 16); mixed-use costs 2/3 or 1/4 (reg. 18(b));
    director_set_ratio uses the ratio the Director set.

    Args:
        purchases: List of purchase records with 'amount' (net, before VAT),
            'category', and optional boolean 'equipment' (fixed asset) fields.

    Returns:
        Tuple of (equipment_inputs_base, other_inputs_base,
        equipment_input_vat, other_input_vat). Bases are net amounts
        EXCLUDING VAT; the return states input VAT on equipment and
        fixed assets separately from input VAT on other inputs.
    """
    equipment_base = 0.0
    other_base = 0.0
    equipment_vat = 0.0
    other_vat = 0.0

    for purchase in purchases:
        amount = purchase.get("amount", 0)
        category = purchase.get("category", "general")
        vat = round(amount * VAT_RATE, 2)
        is_equipment = bool(purchase.get("equipment")) or category == "equipment"
        if is_equipment and category.startswith("vehicle_running"):
            raise ValueError(
                "A vehicle bought as equipment is a car purchase: use category "
                "'private_car_purchase' (not deductible, reg. 14) unless a reg. 14 "
                "exception applies, in which case consult an accountant"
            )

        if category in NON_DEDUCTIBLE:
            continue  # No VAT deduction, and not reported as a claimed input
        elif category in PARTIAL_DEDUCTIBLE:
            deductible = round(vat * PARTIAL_DEDUCTIBLE[category], 2)
        elif category == DIRECTOR_RATIO:
            ratio = purchase.get("director_ratio")
            if isinstance(ratio, bool) or not isinstance(ratio, (int, float)) or not 0 <= ratio <= 1:
                raise ValueError("director_set_ratio purchase needs a numeric director_ratio between 0 and 1")
            deductible = round(vat * ratio, 2)
        elif category in FULL_DEDUCTIBLE:
            deductible = vat
        else:
            raise ValueError(f"Unknown purchase category: {category!r}")

        if is_equipment:
            equipment_base += amount
        else:
            other_base += amount
        if is_equipment:
            equipment_vat += deductible
        else:
            other_vat += deductible

    return equipment_base, other_base, equipment_vat, other_vat


def prepare_vat_report(
    period: str,
    sales: Optional[list[dict]] = None,
    purchases: Optional[list[dict]] = None,
    adjustments: float = 0.0,
) -> VATReport:
    """Prepare a complete periodic VAT return.

    Args:
        period: Reporting period string (e.g., "2026-01" or "2026-01-02").
        sales: List of sale records.
        purchases: List of purchase records.
        adjustments: Manual adjustments amount.

    Returns:
        VATReport with all periodic-return fields populated.
    """
    sales = sales or []
    purchases = purchases or []

    total_sales, zero_rated, exempt, output_vat = calculate_output_vat(sales)
    equipment_base, other_base, equipment_vat, other_vat = calculate_input_vat(purchases)
    input_vat = equipment_vat + other_vat

    net_vat = round(output_vat - input_vat, 2)  # net VAT = output VAT - input VAT

    return VATReport(
        period=period,
        taxable_sales_base=round(total_sales, 2),
        zero_rated_sales=round(zero_rated, 2),
        exempt_sales=round(exempt, 2),
        output_vat=round(output_vat, 2),
        equipment_inputs_base=round(equipment_base, 2),
        other_inputs_base=round(other_base, 2),
        equipment_input_vat=round(equipment_vat, 2),
        other_input_vat=round(other_vat, 2),
        input_vat_claimed=round(input_vat, 2),
        net_vat=net_vat,
        adjustments=adjustments,
        amount_due=round(net_vat + adjustments, 2),  # amount to pay = net VAT + adjustments
    )


def format_report(report: VATReport) -> str:
    """Format VAT report for display."""
    direction = "TO PAY" if report.amount_due > 0 else "REFUND DUE"
    lines = [
        f"=== DRAFT calculation for the periodic VAT return (not a filed return) ===",
        f"Period: {report.period}",
        f"",
        f"  Taxable sales (excl VAT):           {report.taxable_sales_base:>12,.2f} NIS",
        f"  Output VAT:                         {report.output_vat:>12,.2f} NIS",
        f"  Zero-rated sales:                   {report.zero_rated_sales:>12,.2f} NIS",
        f"  Exempt sales:                       {report.exempt_sales:>12,.2f} NIS",
        f"  Input VAT - equipment/fixed assets: {report.equipment_input_vat:>12,.2f} NIS",
        f"  Input VAT - other inputs:           {report.other_input_vat:>12,.2f} NIS",
        f"  Total input VAT:                    {report.input_vat_claimed:>12,.2f} NIS",
        f"  Net VAT (output - input):           {report.net_vat:>12,.2f} NIS",
        f"  Adjustments:                        {report.adjustments:>12,.2f} NIS",
        f"  Amount to pay (net + adjustments):  {report.amount_due:>12,.2f} NIS ({direction})",
        f"",
        f"  Working figures, not return boxes:",
        f"  Equipment purchases base (excl VAT): {report.equipment_inputs_base:>11,.2f} NIS",
        f"  Other purchases base (excl VAT):    {report.other_inputs_base:>12,.2f} NIS",
        f"",
        f"NOTE: Calculation estimate in agorot; the return itself may require whole shekels. Working bases exclude non-deductible purchases and show partially deductible ones in full. Verify with your accountant.",
    ]
    return "\n".join(lines)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Calculate Israeli VAT liability for the periodic return"
    )
    parser.add_argument(
        "--sales", type=float, help="Total sales amount (net, before VAT)"
    )
    parser.add_argument(
        "--purchases", type=float, help="Total purchases amount (net, before VAT)"
    )
    parser.add_argument(
        "--exports", type=float, default=0, help="Zero-rated export sales"
    )
    parser.add_argument(
        "--period", type=str, default="2026-01", help="Reporting period"
    )
    parser.add_argument(
        "--adjustments", type=float, default=0, help="Adjustments (signed)"
    )
    parser.add_argument(
        "--json", type=str, help="JSON file with detailed transactions"
    )
    parser.add_argument(
        "--example", action="store_true", help="Show example calculation"
    )

    args = parser.parse_args()

    if args.example:
        sales = [
            {"amount": 50000, "type": "standard", "description": "Consulting"},
            {"amount": 30000, "type": "standard", "description": "Development"},
            {"amount": 20000, "type": "zero_rated", "description": "Export services"},
        ]
        purchases = [
            {"amount": 15000, "category": "general", "description": "Office rent"},
            {"amount": 8000, "category": "general", "description": "Software licenses"},
            {"amount": 6000, "category": "equipment", "description": "Laptop (fixed asset)"},
            {"amount": 5000, "category": "vehicle_running_mainly_business", "description": "Car running costs"},
            {"amount": 1000, "category": "mixed_use_mainly_business", "description": "Home internet"},
            {"amount": 2000, "category": "entertainment", "description": "Client dinner"},
        ]
        report = prepare_vat_report("2026-01", sales, purchases)
        print(format_report(report))
        return

    if args.json:
        with open(args.json) as f:
            data = json.load(f)
        report = prepare_vat_report(
            data.get("period", args.period),
            data.get("sales", []),
            data.get("purchases", []),
            float(data.get("adjustments", 0)),
        )
        print(format_report(report))
        return

    if args.sales is not None or args.purchases is not None:
        sales = [{"amount": args.sales or 0, "type": "standard"}]
        if args.exports != 0:
            sales.append({"amount": args.exports, "type": "zero_rated"})
        purchases = []
        if args.purchases is not None:
            purchases = [{"amount": args.purchases, "category": "general"}]

        report = prepare_vat_report(args.period, sales, purchases, args.adjustments)
        print(format_report(report))
        return

    parser.print_help()


if __name__ == "__main__":
    main()
