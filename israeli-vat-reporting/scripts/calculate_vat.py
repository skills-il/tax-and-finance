#!/usr/bin/env python3
"""Calculate Israeli VAT liability for periodic reporting.

Computes net VAT from sales (output) and purchase (input) records,
applies Israeli deduction rules, and maps results to Form 874 fields.

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


VAT_RATE = 0.17  # 17% standard Israeli VAT rate (2025)

# Non-deductible expense categories
NON_DEDUCTIBLE = {"entertainment", "gifts", "fines"}

# Partially deductible categories
PARTIAL_DEDUCTIBLE = {
    "vehicle": 2 / 3,  # 2/3 deductible for vehicles
}


@dataclass
class VATReport:
    """Israeli Form 874 VAT report structure."""
    period: str = ""
    total_sales_incl_vat: float = 0.0       # Field 1
    zero_rated_sales: float = 0.0           # Field 2
    exempt_sales: float = 0.0               # Field 3
    output_vat: float = 0.0                 # Field 4
    total_purchases_incl_vat: float = 0.0   # Field 5
    input_vat_claimed: float = 0.0          # Field 6
    net_vat: float = 0.0                    # Field 7
    adjustments: float = 0.0               # Field 8
    amount_due: float = 0.0                # Field 9


def calculate_output_vat(
    sales: list[dict],
) -> tuple[float, float, float, float]:
    """Calculate output VAT from sales records.

    Args:
        sales: List of sale records with 'amount', 'type' fields.

    Returns:
        Tuple of (total_sales_incl_vat, zero_rated, exempt, output_vat).
    """
    total_incl_vat = 0.0
    zero_rated = 0.0
    exempt = 0.0
    output_vat = 0.0

    for sale in sales:
        amount = sale.get("amount", 0)
        sale_type = sale.get("type", "standard")

        if sale_type == "zero_rated":
            zero_rated += amount
            total_incl_vat += amount  # No VAT added
        elif sale_type == "exempt":
            exempt += amount
            total_incl_vat += amount  # No VAT added
        else:
            vat = round(amount * VAT_RATE, 2)
            output_vat += vat
            total_incl_vat += amount + vat

    return total_incl_vat, zero_rated, exempt, output_vat


def calculate_input_vat(purchases: list[dict]) -> tuple[float, float]:
    """Calculate deductible input VAT from purchase records.

    Applies Israeli deduction rules (entertainment excluded,
    vehicle 2/3 deductible, etc.).

    Args:
        purchases: List of purchase records with 'amount', 'category' fields.

    Returns:
        Tuple of (total_purchases_incl_vat, deductible_input_vat).
    """
    total_incl_vat = 0.0
    deductible_vat = 0.0

    for purchase in purchases:
        amount = purchase.get("amount", 0)
        category = purchase.get("category", "general")
        vat = round(amount * VAT_RATE, 2)
        total_incl_vat += amount + vat

        if category in NON_DEDUCTIBLE:
            continue  # No VAT deduction for these categories
        elif category in PARTIAL_DEDUCTIBLE:
            ratio = PARTIAL_DEDUCTIBLE[category]
            deductible_vat += round(vat * ratio, 2)
        else:
            deductible_vat += vat

    return total_incl_vat, deductible_vat


def prepare_vat_report(
    period: str,
    sales: Optional[list[dict]] = None,
    purchases: Optional[list[dict]] = None,
    adjustments: float = 0.0,
) -> VATReport:
    """Prepare a complete VAT report (Form 874).

    Args:
        period: Reporting period string (e.g., "2026-01" or "2026-01-02").
        sales: List of sale records.
        purchases: List of purchase records.
        adjustments: Manual adjustments amount.

    Returns:
        VATReport with all Form 874 fields populated.
    """
    sales = sales or []
    purchases = purchases or []

    total_sales, zero_rated, exempt, output_vat = calculate_output_vat(sales)
    total_purchases, input_vat = calculate_input_vat(purchases)

    net_vat = round(output_vat - input_vat + adjustments, 2)

    return VATReport(
        period=period,
        total_sales_incl_vat=round(total_sales, 2),
        zero_rated_sales=round(zero_rated, 2),
        exempt_sales=round(exempt, 2),
        output_vat=round(output_vat, 2),
        total_purchases_incl_vat=round(total_purchases, 2),
        input_vat_claimed=round(input_vat, 2),
        net_vat=net_vat,
        adjustments=adjustments,
        amount_due=net_vat,
    )


def format_report(report: VATReport) -> str:
    """Format VAT report for display."""
    direction = "TO PAY" if report.amount_due > 0 else "REFUND DUE"
    lines = [
        f"=== Israeli VAT Report (Form 874) ===",
        f"Period: {report.period}",
        f"",
        f"  Field 1 - Total Sales (incl VAT):  {report.total_sales_incl_vat:>12,.2f} NIS",
        f"  Field 2 - Zero-Rated Sales:         {report.zero_rated_sales:>12,.2f} NIS",
        f"  Field 3 - Exempt Sales:             {report.exempt_sales:>12,.2f} NIS",
        f"  Field 4 - Output VAT:               {report.output_vat:>12,.2f} NIS",
        f"  Field 5 - Total Purchases (incl VAT):{report.total_purchases_incl_vat:>11,.2f} NIS",
        f"  Field 6 - Input VAT Claimed:        {report.input_vat_claimed:>12,.2f} NIS",
        f"  Field 7 - Net VAT:                  {report.net_vat:>12,.2f} NIS",
        f"  Field 8 - Adjustments:              {report.adjustments:>12,.2f} NIS",
        f"  Field 9 - Amount Due:               {report.amount_due:>12,.2f} NIS ({direction})",
        f"",
        f"NOTE: This is a calculation estimate. Verify with your accountant.",
    ]
    return "\n".join(lines)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Calculate Israeli VAT liability for Form 874"
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
            {"amount": 5000, "category": "vehicle", "description": "Car expenses"},
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
        )
        print(format_report(report))
        return

    if args.sales is not None:
        sales = [{"amount": args.sales, "type": "standard"}]
        if args.exports > 0:
            sales.append({"amount": args.exports, "type": "zero_rated"})
        purchases = []
        if args.purchases is not None:
            purchases = [{"amount": args.purchases, "category": "general"}]

        report = prepare_vat_report(args.period, sales, purchases)
        print(format_report(report))
        return

    parser.print_help()


if __name__ == "__main__":
    main()
