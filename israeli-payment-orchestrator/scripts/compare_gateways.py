#!/usr/bin/env python3
"""Compare Israeli payment gateways based on features, fees, and volume.

Generates a comparison matrix to help choose the right payment gateway(s)
for Israeli merchants. Supports filtering by features and volume-based
cost estimation.

Usage:
    python scripts/compare_gateways.py --features installments,recurring
    python scripts/compare_gateways.py --volume 500 --avg-amount 200
    python scripts/compare_gateways.py --all
    python scripts/compare_gateways.py --example
"""

import sys
import json
import argparse
from dataclasses import dataclass, asdict, field
from typing import List, Optional


@dataclass
class GatewayInfo:
    """Israeli payment gateway information."""
    name: str
    hebrew_name: str
    api_style: str
    installment_types: List[str]
    recurring: bool
    hosted_page: str
    bit_support: bool
    apple_pay: bool
    fee_range_pct: tuple  # (min, max) percentage
    settlement_days: int  # typical settlement time
    api_docs_url: str
    notes: str


# שערי תשלום ישראליים - Israeli payment gateways database
GATEWAYS = {
    "cardcom": GatewayInfo(
        name="Cardcom",
        hebrew_name="קארדקום",
        api_style="REST JSON",
        installment_types=["regular", "credit", "club"],
        recurring=True,
        hosted_page="iframe",
        bit_support=False,
        apple_pay=False,
        fee_range_pct=(0.6, 0.8),
        settlement_days=2,
        api_docs_url="https://kb.cardcom.co.il/",
        notes="Full installment support including club. Good documentation.",
    ),
    "tranzila": GatewayInfo(
        name="Tranzila",
        hebrew_name="טרנזילה",
        api_style="REST / Form POST",
        installment_types=["regular", "credit"],
        recurring=True,
        hosted_page="redirect",
        bit_support=False,
        apple_pay=False,
        fee_range_pct=(0.5, 0.7),
        settlement_days=2,
        api_docs_url="https://docs.tranzila.com/",
        notes="Veteran provider. Lower fees. Form POST legacy API still common.",
    ),
    "payme": GatewayInfo(
        name="PayMe",
        hebrew_name="פיימי",
        api_style="REST JSON",
        installment_types=["regular", "credit"],
        recurring=True,
        hosted_page="iframe",
        bit_support=True,
        apple_pay=True,
        fee_range_pct=(0.7, 1.0),
        settlement_days=2,
        api_docs_url="https://www.payme.io/developers",
        notes="Modern API. Bit and Apple Pay support. Higher fees.",
    ),
    "meshulam": GatewayInfo(
        name="Meshulam",
        hebrew_name="משולם",
        api_style="REST JSON",
        installment_types=["regular"],
        recurring=True,
        hosted_page="iframe + redirect",
        bit_support=True,
        apple_pay=False,
        fee_range_pct=(0.6, 0.9),
        settlement_days=3,
        api_docs_url="https://www.meshulam.co.il/developers",
        notes="Popular with SMBs. Bit support. Limited installment types.",
    ),
    "icredit": GatewayInfo(
        name="iCredit",
        hebrew_name="אייקרדיט",
        api_style="REST JSON",
        installment_types=["regular", "credit"],
        recurring=True,
        hosted_page="redirect",
        bit_support=False,
        apple_pay=False,
        fee_range_pct=(0.5, 0.8),
        settlement_days=2,
        api_docs_url="https://icredit.rivhit.co.il/",
        notes="Part of Rivhit (accounting software). Good for existing Rivhit users.",
    ),
    "pelecard": GatewayInfo(
        name="Pelecard",
        hebrew_name="פלאכארד",
        api_style="REST JSON",
        installment_types=["regular", "credit", "club"],
        recurring=True,
        hosted_page="iframe",
        bit_support=False,
        apple_pay=False,
        fee_range_pct=(0.5, 0.7),
        settlement_days=2,
        api_docs_url="https://www.pelecard.com/support/",
        notes="Full installment support. Competitive pricing for high volume.",
    ),
}


def filter_by_features(gateways: dict, features: List[str]) -> dict:
    """Filter gateways by required features.

    Args:
        gateways: Dictionary of gateway name to GatewayInfo.
        features: List of required features.

    Returns:
        Filtered dictionary of gateways that support all features.
    """
    result = {}
    for name, gw in gateways.items():
        matches = True
        for feature in features:
            feature = feature.strip().lower()
            if feature == "installments" and not gw.installment_types:
                matches = False
            elif feature == "credit" and "credit" not in gw.installment_types:
                matches = False
            elif feature == "club" and "club" not in gw.installment_types:
                matches = False
            elif feature == "recurring" and not gw.recurring:
                matches = False
            elif feature == "bit" and not gw.bit_support:
                matches = False
            elif feature == "apple_pay" and not gw.apple_pay:
                matches = False
        if matches:
            result[name] = gw
    return result


def estimate_monthly_cost(
    gateway: GatewayInfo,
    daily_volume: int,
    avg_amount: float,
) -> dict:
    """Estimate monthly processing cost for a gateway.

    Args:
        gateway: Gateway information.
        daily_volume: Average daily transaction count.
        avg_amount: Average transaction amount in NIS.

    Returns:
        Dictionary with cost estimates.
    """
    monthly_transactions = daily_volume * 30
    monthly_volume_nis = monthly_transactions * avg_amount
    min_fee = monthly_volume_nis * (gateway.fee_range_pct[0] / 100)
    max_fee = monthly_volume_nis * (gateway.fee_range_pct[1] / 100)
    avg_fee = (min_fee + max_fee) / 2

    return {
        "gateway": gateway.name,
        "monthly_transactions": monthly_transactions,
        "monthly_volume_nis": monthly_volume_nis,
        "fee_range_pct": f"{gateway.fee_range_pct[0]}-{gateway.fee_range_pct[1]}%",
        "monthly_fee_min_nis": round(min_fee, 0),
        "monthly_fee_max_nis": round(max_fee, 0),
        "monthly_fee_avg_nis": round(avg_fee, 0),
    }


def print_comparison_table(gateways: dict) -> None:
    """Print gateway comparison as formatted table."""
    print(f"\n{'Gateway':<12} {'API':<18} {'Installments':<25} {'Recurring':<10} "
          f"{'Hosted':<18} {'Bit':<5} {'Fee':<10}")
    print("-" * 100)
    for name, gw in gateways.items():
        inst = ", ".join(gw.installment_types) if gw.installment_types else "None"
        fee = f"{gw.fee_range_pct[0]}-{gw.fee_range_pct[1]}%"
        print(f"{gw.name:<12} {gw.api_style:<18} {inst:<25} "
              f"{'Yes' if gw.recurring else 'No':<10} "
              f"{gw.hosted_page:<18} {'Yes' if gw.bit_support else 'No':<5} {fee:<10}")


def print_cost_comparison(gateways: dict, daily_volume: int, avg_amount: float) -> None:
    """Print cost comparison for given volume."""
    print(f"\nCost estimate for {daily_volume} daily transactions, "
          f"avg {avg_amount:.0f} NIS:")
    print(f"{'Gateway':<12} {'Monthly Volume':<18} {'Fee Range':<12} "
          f"{'Min Cost':<12} {'Max Cost':<12} {'Avg Cost':<12}")
    print("-" * 80)

    costs = []
    for name, gw in gateways.items():
        cost = estimate_monthly_cost(gw, daily_volume, avg_amount)
        costs.append(cost)
        print(f"{cost['gateway']:<12} {cost['monthly_volume_nis']:>14,.0f} NIS "
              f"{cost['fee_range_pct']:<12} "
              f"{cost['monthly_fee_min_nis']:>8,.0f} NIS "
              f"{cost['monthly_fee_max_nis']:>8,.0f} NIS "
              f"{cost['monthly_fee_avg_nis']:>8,.0f} NIS")

    # מציאת השער הזול ביותר
    cheapest = min(costs, key=lambda c: c["monthly_fee_avg_nis"])
    print(f"\nLowest average cost: {cheapest['gateway']} "
          f"({cheapest['monthly_fee_avg_nis']:,.0f} NIS/month)")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Compare Israeli payment gateways "
                    "(השוואת שערי תשלום ישראליים)"
    )
    parser.add_argument(
        "--features",
        help="Required features, comma-separated: "
             "installments, credit, club, recurring, bit, apple_pay"
    )
    parser.add_argument(
        "--volume", type=int,
        help="Average daily transaction count (מספר עסקאות יומי)"
    )
    parser.add_argument(
        "--avg-amount", type=float, default=200,
        help="Average transaction amount in NIS (סכום עסקה ממוצע, default: 200)"
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

    if not any([args.features, args.volume, args.all, args.example]):
        parser.print_help()
        sys.exit(1)

    gateways = GATEWAYS.copy()

    if args.example:
        print("=== All Gateways Comparison ===")
        print_comparison_table(gateways)
        print("\n=== Cost Estimate: 500 daily transactions, avg 200 NIS ===")
        print_cost_comparison(gateways, 500, 200)
        print("\n=== Gateways with Bit Support ===")
        bit_gateways = filter_by_features(gateways, ["bit"])
        print_comparison_table(bit_gateways)
        return

    # Filter by features if specified
    if args.features:
        features = args.features.split(",")
        gateways = filter_by_features(gateways, features)
        if not gateways:
            print(f"No gateways match features: {args.features}")
            sys.exit(1)

    if args.json:
        data = {name: asdict(gw) for name, gw in gateways.items()}
        if args.volume:
            for name, gw in gateways.items():
                data[name]["cost_estimate"] = estimate_monthly_cost(
                    gw, args.volume, args.avg_amount
                )
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print_comparison_table(gateways)
        if args.volume:
            print_cost_comparison(gateways, args.volume, args.avg_amount)


if __name__ == "__main__":
    main()
