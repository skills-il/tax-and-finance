#!/usr/bin/env python3
"""
Israeli Arnona (Municipal Property Tax) Calculator

Calculates annual and bimonthly arnona payments based on municipality,
property area, zone classification, and usage type. Supports discount
calculations for eligible populations.

Usage:
    python arnona-calculator.py --municipality "tel-aviv" --area 80 --zone A --usage residential
    python arnona-calculator.py --municipality "jerusalem" --area 70 --zone B --usage residential --discount oleh --discount-months 12
    python arnona-calculator.py --list-municipalities
    python arnona-calculator.py --list-discounts

Requirements:
    Python 3.8+
    No external dependencies
"""

import argparse
import json
import sys
from dataclasses import dataclass
from typing import Optional


# ============================================================
# Rate Tables (approximate, based on recent tzav arnona data)
# ============================================================

# Structure: municipality -> zone -> usage_type -> rate_per_sqm_per_year (NIS)
RATE_TABLES = {
    "tel-aviv": {
        "name": "Tel Aviv-Yafo",
        "zone_system": "numbered (1-4)",
        "zones": {
            "1": {
                "residential": 125.0,
                "commercial": 400.0,
                "office": 320.0,
                "industrial": 180.0,
            },
            "2": {
                "residential": 95.0,
                "commercial": 310.0,
                "office": 250.0,
                "industrial": 150.0,
            },
            "3": {
                "residential": 80.0,
                "commercial": 240.0,
                "office": 190.0,
                "industrial": 120.0,
            },
            "4": {
                "residential": 70.0,
                "commercial": 175.0,
                "office": 140.0,
                "industrial": 95.0,
            },
        },
    },
    "jerusalem": {
        "name": "Jerusalem",
        "zone_system": "Hebrew letters (alef-heh / A-E)",
        "zones": {
            "A": {
                "residential": 90.0,
                "commercial": 280.0,
                "office": 220.0,
                "industrial": 130.0,
            },
            "B": {
                "residential": 72.0,
                "commercial": 220.0,
                "office": 175.0,
                "industrial": 105.0,
            },
            "C": {
                "residential": 65.0,
                "commercial": 180.0,
                "office": 140.0,
                "industrial": 90.0,
            },
            "D": {
                "residential": 55.0,
                "commercial": 140.0,
                "office": 110.0,
                "industrial": 75.0,
            },
            "E": {
                "residential": 48.0,
                "commercial": 110.0,
                "office": 85.0,
                "industrial": 60.0,
            },
        },
    },
    "haifa": {
        "name": "Haifa",
        "zone_system": "lettered (A-D)",
        "zones": {
            "A": {
                "residential": 85.0,
                "commercial": 260.0,
                "office": 200.0,
                "industrial": 120.0,
            },
            "B": {
                "residential": 70.0,
                "commercial": 200.0,
                "office": 155.0,
                "industrial": 95.0,
            },
            "C": {
                "residential": 55.0,
                "commercial": 155.0,
                "office": 120.0,
                "industrial": 75.0,
            },
            "D": {
                "residential": 45.0,
                "commercial": 110.0,
                "office": 85.0,
                "industrial": 55.0,
            },
        },
    },
    "beer-sheva": {
        "name": "Beer Sheva",
        "zone_system": "numbered (1-3)",
        "zones": {
            "1": {
                "residential": 55.0,
                "commercial": 170.0,
                "office": 130.0,
                "industrial": 80.0,
            },
            "2": {
                "residential": 45.0,
                "commercial": 130.0,
                "office": 100.0,
                "industrial": 65.0,
            },
            "3": {
                "residential": 37.0,
                "commercial": 100.0,
                "office": 80.0,
                "industrial": 50.0,
            },
        },
    },
    "netanya": {
        "name": "Netanya",
        "zone_system": "numbered (1-3)",
        "zones": {
            "1": {
                "residential": 82.0,
                "commercial": 250.0,
                "office": 195.0,
                "industrial": 110.0,
            },
            "2": {
                "residential": 68.0,
                "commercial": 195.0,
                "office": 150.0,
                "industrial": 90.0,
            },
            "3": {
                "residential": 56.0,
                "commercial": 150.0,
                "office": 115.0,
                "industrial": 70.0,
            },
        },
    },
    "rishon-lezion": {
        "name": "Rishon LeZion",
        "zone_system": "lettered (A-D)",
        "zones": {
            "A": {
                "residential": 88.0,
                "commercial": 270.0,
                "office": 210.0,
                "industrial": 125.0,
            },
            "B": {
                "residential": 74.0,
                "commercial": 215.0,
                "office": 170.0,
                "industrial": 100.0,
            },
            "C": {
                "residential": 65.0,
                "commercial": 175.0,
                "office": 135.0,
                "industrial": 85.0,
            },
            "D": {
                "residential": 58.0,
                "commercial": 140.0,
                "office": 110.0,
                "industrial": 70.0,
            },
        },
    },
    "petah-tikva": {
        "name": "Petah Tikva",
        "zone_system": "numbered (1-3)",
        "zones": {
            "1": {
                "residential": 78.0,
                "commercial": 240.0,
                "office": 185.0,
                "industrial": 105.0,
            },
            "2": {
                "residential": 65.0,
                "commercial": 185.0,
                "office": 145.0,
                "industrial": 85.0,
            },
            "3": {
                "residential": 55.0,
                "commercial": 145.0,
                "office": 110.0,
                "industrial": 70.0,
            },
        },
    },
    "ashdod": {
        "name": "Ashdod",
        "zone_system": "numbered (1-3)",
        "zones": {
            "1": {
                "residential": 68.0,
                "commercial": 210.0,
                "office": 160.0,
                "industrial": 95.0,
            },
            "2": {
                "residential": 55.0,
                "commercial": 165.0,
                "office": 125.0,
                "industrial": 78.0,
            },
            "3": {
                "residential": 46.0,
                "commercial": 130.0,
                "office": 100.0,
                "industrial": 62.0,
            },
        },
    },
    "herzliya": {
        "name": "Herzliya",
        "zone_system": "lettered (A-C)",
        "zones": {
            "A": {
                "residential": 108.0,
                "commercial": 340.0,
                "office": 265.0,
                "industrial": 150.0,
            },
            "B": {
                "residential": 88.0,
                "commercial": 270.0,
                "office": 210.0,
                "industrial": 120.0,
            },
            "C": {
                "residential": 72.0,
                "commercial": 210.0,
                "office": 165.0,
                "industrial": 95.0,
            },
        },
    },
    "raanana": {
        "name": "Ra'anana",
        "zone_system": "lettered (A-C)",
        "zones": {
            "A": {
                "residential": 102.0,
                "commercial": 320.0,
                "office": 250.0,
                "industrial": 140.0,
            },
            "B": {
                "residential": 85.0,
                "commercial": 255.0,
                "office": 200.0,
                "industrial": 115.0,
            },
            "C": {
                "residential": 74.0,
                "commercial": 210.0,
                "office": 160.0,
                "industrial": 95.0,
            },
        },
    },
    "ramat-gan": {
        "name": "Ramat Gan",
        "zone_system": "lettered (A-D)",
        "zones": {
            "A": {
                "residential": 98.0,
                "commercial": 310.0,
                "office": 240.0,
                "industrial": 135.0,
            },
            "B": {
                "residential": 82.0,
                "commercial": 245.0,
                "office": 190.0,
                "industrial": 110.0,
            },
            "C": {
                "residential": 72.0,
                "commercial": 200.0,
                "office": 155.0,
                "industrial": 90.0,
            },
            "D": {
                "residential": 65.0,
                "commercial": 165.0,
                "office": 125.0,
                "industrial": 75.0,
            },
        },
    },
    "modiin": {
        "name": "Modi'in-Maccabim-Re'ut",
        "zone_system": "numbered (1-3)",
        "zones": {
            "1": {
                "residential": 82.0,
                "commercial": 250.0,
                "office": 195.0,
                "industrial": 110.0,
            },
            "2": {
                "residential": 70.0,
                "commercial": 200.0,
                "office": 155.0,
                "industrial": 90.0,
            },
            "3": {
                "residential": 60.0,
                "commercial": 160.0,
                "office": 125.0,
                "industrial": 75.0,
            },
        },
    },
}

# ============================================================
# Discount Definitions
# ============================================================

DISCOUNTS = {
    "oleh": {
        "name": "Oleh Chadash (New Immigrant)",
        "name_he": "עולה חדש",
        "percentage": 90,
        "max_sqm": 100,
        "duration_months": 12,
        "description": "90% discount for the first 12 months from aliyah date",
    },
    "soldier": {
        "name": "Active-Duty Soldier",
        "name_he": "חייל בשירות סדיר",
        "percentage": 100,
        "max_sqm": 100,
        "duration_months": None,
        "description": "Up to 100% for lone soldiers in mandatory service",
    },
    "elderly-65": {
        "name": "Elderly (65-69)",
        "name_he": "קשיש (65-69)",
        "percentage": 25,
        "max_sqm": 100,
        "duration_months": None,
        "description": "25% discount, income threshold applies",
    },
    "elderly-70": {
        "name": "Elderly (70+)",
        "name_he": "קשיש (70+)",
        "percentage": 30,
        "max_sqm": 100,
        "duration_months": None,
        "description": "30% discount, income threshold applies",
    },
    "disabled-50": {
        "name": "Disabled (50-74%)",
        "name_he": "נכה (50-74%)",
        "percentage": 40,
        "max_sqm": 100,
        "duration_months": None,
        "description": "40% discount with Bituach Leumi disability certificate",
    },
    "disabled-75": {
        "name": "Disabled (75-100%)",
        "name_he": "נכה (75-100%)",
        "percentage": 80,
        "max_sqm": 100,
        "duration_months": None,
        "description": "80% discount with Bituach Leumi disability certificate",
    },
    "low-income": {
        "name": "Low Income",
        "name_he": "הכנסה נמוכה",
        "percentage": 80,
        "max_sqm": 100,
        "duration_months": None,
        "description": "20-80% depending on income level (showing max)",
    },
    "student": {
        "name": "Student",
        "name_he": "סטודנט",
        "percentage": 50,
        "max_sqm": 100,
        "duration_months": None,
        "description": "Up to 50%, full-time student living alone",
    },
    "single-parent": {
        "name": "Single Parent",
        "name_he": "הורה יחיד",
        "percentage": 20,
        "max_sqm": 100,
        "duration_months": None,
        "description": "20% discount for recognized single parents",
    },
    "large-family": {
        "name": "Large Family (4+ children)",
        "name_he": "משפחה ברוכת ילדים",
        "percentage": 20,
        "max_sqm": 100,
        "duration_months": None,
        "description": "20% discount for families with 4+ dependent children",
    },
    "bereaved": {
        "name": "Bereaved Family",
        "name_he": "משפחה שכולה",
        "percentage": 66,
        "max_sqm": 100,
        "duration_months": None,
        "description": "66% discount for families of fallen soldiers/terror victims",
    },
    "holocaust-survivor": {
        "name": "Holocaust Survivor",
        "name_he": "ניצול שואה",
        "percentage": 66,
        "max_sqm": 100,
        "duration_months": None,
        "description": "66% discount for recognized Holocaust survivors",
    },
}


@dataclass
class ArnonaResult:
    municipality: str
    municipality_name: str
    zone: str
    usage: str
    area_sqm: float
    rate_per_sqm: float
    annual_base: float
    discount_type: Optional[str]
    discount_percentage: float
    discount_area_sqm: float
    full_rate_area_sqm: float
    annual_discounted: float
    annual_after_discount: float
    bimonthly_payment: float
    monthly_equivalent: float
    discount_months: Optional[int]
    prorated_annual: Optional[float]


def normalize_zone(zone: str) -> str:
    """Normalize zone input to match rate table keys."""
    zone = zone.strip().upper()

    # Map Hebrew letters to English equivalents
    hebrew_map = {
        "ALEF": "A", "BET": "B", "GIMEL": "C", "DALET": "D", "HEH": "E",
        "A": "A", "B": "B", "C": "C", "D": "D", "E": "E",
    }

    if zone in hebrew_map:
        return hebrew_map[zone]

    # Try as number
    try:
        return str(int(zone))
    except ValueError:
        pass

    return zone


def calculate_arnona(
    municipality: str,
    area_sqm: float,
    zone: str,
    usage: str = "residential",
    discount_type: Optional[str] = None,
    discount_months: Optional[int] = None,
) -> ArnonaResult:
    """Calculate arnona for the given parameters."""

    municipality = municipality.lower().strip()
    usage = usage.lower().strip()
    zone = normalize_zone(zone)

    if municipality not in RATE_TABLES:
        available = ", ".join(sorted(RATE_TABLES.keys()))
        print(f"Error: Municipality '{municipality}' not found in rate tables.", file=sys.stderr)
        print(f"Available municipalities: {available}", file=sys.stderr)
        sys.exit(1)

    muni_data = RATE_TABLES[municipality]

    if zone not in muni_data["zones"]:
        available = ", ".join(sorted(muni_data["zones"].keys()))
        print(
            f"Error: Zone '{zone}' not valid for {muni_data['name']}.",
            file=sys.stderr,
        )
        print(f"Available zones ({muni_data['zone_system']}): {available}", file=sys.stderr)
        sys.exit(1)

    zone_rates = muni_data["zones"][zone]

    if usage not in zone_rates:
        available = ", ".join(sorted(zone_rates.keys()))
        print(f"Error: Usage type '{usage}' not found.", file=sys.stderr)
        print(f"Available types: {available}", file=sys.stderr)
        sys.exit(1)

    rate = zone_rates[usage]
    annual_base = area_sqm * rate

    # Calculate discount
    discount_percentage = 0.0
    discount_area = 0.0
    full_rate_area = area_sqm
    annual_discounted = 0.0

    if discount_type:
        discount_type = discount_type.lower().strip()
        if discount_type not in DISCOUNTS:
            available = ", ".join(sorted(DISCOUNTS.keys()))
            print(f"Error: Discount category '{discount_type}' not recognized.", file=sys.stderr)
            print(f"Available discounts: {available}", file=sys.stderr)
            sys.exit(1)

        disc = DISCOUNTS[discount_type]
        discount_percentage = disc["percentage"]
        max_sqm = disc["max_sqm"]

        # Split area into discounted and full-rate portions
        discount_area = min(area_sqm, max_sqm)
        full_rate_area = max(0, area_sqm - max_sqm)

        discounted_portion = discount_area * rate * (discount_percentage / 100)
        annual_discounted = discounted_portion

    annual_after_discount = annual_base - annual_discounted

    # Prorate if discount is time-limited
    prorated_annual = None
    if discount_months and discount_months < 12:
        months_with_discount = discount_months
        months_without = 12 - months_with_discount
        prorated_annual = (
            (annual_after_discount * months_with_discount / 12)
            + (annual_base * months_without / 12)
        )

    effective_annual = prorated_annual if prorated_annual is not None else annual_after_discount
    bimonthly = effective_annual / 6
    monthly = effective_annual / 12

    return ArnonaResult(
        municipality=municipality,
        municipality_name=muni_data["name"],
        zone=zone,
        usage=usage,
        area_sqm=area_sqm,
        rate_per_sqm=rate,
        annual_base=annual_base,
        discount_type=discount_type,
        discount_percentage=discount_percentage,
        discount_area_sqm=discount_area,
        full_rate_area_sqm=full_rate_area,
        annual_discounted=annual_discounted,
        annual_after_discount=annual_after_discount,
        bimonthly_payment=bimonthly,
        monthly_equivalent=monthly,
        discount_months=discount_months,
        prorated_annual=prorated_annual,
    )


def format_result(result: ArnonaResult) -> str:
    """Format the calculation result as a readable report."""
    lines = [
        "=" * 60,
        "ARNONA CALCULATION REPORT",
        "=" * 60,
        "",
        f"Municipality:    {result.municipality_name}",
        f"Zone:            {result.zone}",
        f"Usage type:      {result.usage}",
        f"Property area:   {result.area_sqm:.1f} sqm",
        f"Rate per sqm:    {result.rate_per_sqm:.2f} NIS/year",
        "",
        "-" * 40,
        "BASE CALCULATION",
        "-" * 40,
        f"Annual base arnona: {result.annual_base:,.2f} NIS",
        "",
    ]

    if result.discount_type:
        disc = DISCOUNTS[result.discount_type]
        lines.extend([
            "-" * 40,
            "DISCOUNT APPLIED",
            "-" * 40,
            f"Discount type:      {disc['name']}",
            f"Discount rate:      {result.discount_percentage:.0f}%",
            f"Discount applies to: {result.discount_area_sqm:.1f} sqm (max {disc['max_sqm']} sqm)",
        ])

        if result.full_rate_area_sqm > 0:
            lines.append(
                f"Full-rate area:     {result.full_rate_area_sqm:.1f} sqm"
            )

        lines.extend([
            f"Annual savings:     {result.annual_discounted:,.2f} NIS",
            f"Annual after discount: {result.annual_after_discount:,.2f} NIS",
            "",
        ])

        if result.prorated_annual is not None:
            lines.extend([
                "-" * 40,
                "PRORATED CALCULATION",
                "-" * 40,
                f"Discount months remaining: {result.discount_months}",
                f"Full-rate months:          {12 - result.discount_months}",
                f"Prorated annual total:     {result.prorated_annual:,.2f} NIS",
                "",
            ])

    effective = result.prorated_annual if result.prorated_annual else result.annual_after_discount

    lines.extend([
        "-" * 40,
        "PAYMENT SUMMARY",
        "-" * 40,
        f"Effective annual total:  {effective:,.2f} NIS",
        f"Bimonthly payment:       {result.bimonthly_payment:,.2f} NIS",
        f"Monthly equivalent:      {result.monthly_equivalent:,.2f} NIS",
        "",
        "=" * 60,
        "NOTE: These rates are approximate estimates based on recent",
        "municipal rate ordinances. Actual rates may vary. Always",
        "verify with your municipality's official arnona department.",
        "=" * 60,
    ])

    return "\n".join(lines)


def format_result_json(result: ArnonaResult) -> str:
    """Format the result as JSON for programmatic use."""
    data = {
        "municipality": result.municipality,
        "municipality_name": result.municipality_name,
        "zone": result.zone,
        "usage": result.usage,
        "area_sqm": result.area_sqm,
        "rate_per_sqm": result.rate_per_sqm,
        "annual_base_nis": round(result.annual_base, 2),
        "discount": None,
        "effective_annual_nis": round(
            result.prorated_annual
            if result.prorated_annual
            else result.annual_after_discount,
            2,
        ),
        "bimonthly_payment_nis": round(result.bimonthly_payment, 2),
        "monthly_equivalent_nis": round(result.monthly_equivalent, 2),
    }

    if result.discount_type:
        data["discount"] = {
            "type": result.discount_type,
            "percentage": result.discount_percentage,
            "discount_area_sqm": result.discount_area_sqm,
            "annual_savings_nis": round(result.annual_discounted, 2),
        }
        if result.discount_months:
            data["discount"]["remaining_months"] = result.discount_months
            data["discount"]["prorated_annual_nis"] = round(result.prorated_annual, 2) if result.prorated_annual else None

    return json.dumps(data, indent=2, ensure_ascii=False)


def list_municipalities():
    """Print all supported municipalities."""
    print("Supported Municipalities:")
    print("-" * 50)
    for key in sorted(RATE_TABLES.keys()):
        muni = RATE_TABLES[key]
        zones = ", ".join(sorted(muni["zones"].keys()))
        print(f"  {key:20s}  {muni['name']:25s}  Zones: {zones}")
    print()
    print(f"Total: {len(RATE_TABLES)} municipalities")


def list_discounts():
    """Print all supported discount categories."""
    print("Supported Discount Categories:")
    print("-" * 60)
    for key in sorted(DISCOUNTS.keys()):
        disc = DISCOUNTS[key]
        duration = f"{disc['duration_months']} months" if disc['duration_months'] else "Ongoing"
        print(f"  {key:20s}  {disc['percentage']:3d}%  Max {disc['max_sqm']:3d} sqm  {duration}")
        print(f"  {'':20s}  {disc['description']}")
        print()


def main():
    parser = argparse.ArgumentParser(
        description="Israeli Arnona (Municipal Property Tax) Calculator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --municipality tel-aviv --area 80 --zone 2 --usage residential
  %(prog)s --municipality jerusalem --area 70 --zone B --usage residential --discount oleh --discount-months 6
  %(prog)s --list-municipalities
  %(prog)s --list-discounts
        """,
    )

    parser.add_argument("--municipality", "-m", help="Municipality name (e.g., tel-aviv, jerusalem)")
    parser.add_argument("--area", "-a", type=float, help="Property area in square meters")
    parser.add_argument("--zone", "-z", help="Zone classification (varies by municipality)")
    parser.add_argument("--usage", "-u", default="residential",
                        choices=["residential", "commercial", "office", "industrial"],
                        help="Property usage type (default: residential)")
    parser.add_argument("--discount", "-d", help="Discount category (e.g., oleh, soldier, elderly-70)")
    parser.add_argument("--discount-months", type=int, help="Remaining months of discount eligibility")
    parser.add_argument("--json", action="store_true", help="Output in JSON format")
    parser.add_argument("--list-municipalities", action="store_true", help="List all supported municipalities")
    parser.add_argument("--list-discounts", action="store_true", help="List all supported discount categories")

    args = parser.parse_args()

    if args.list_municipalities:
        list_municipalities()
        return

    if args.list_discounts:
        list_discounts()
        return

    if not args.municipality or not args.area or not args.zone:
        parser.error("--municipality, --area, and --zone are required for calculation")

    if args.area <= 0:
        parser.error("Property area must be positive")

    result = calculate_arnona(
        municipality=args.municipality,
        area_sqm=args.area,
        zone=args.zone,
        usage=args.usage,
        discount_type=args.discount,
        discount_months=args.discount_months,
    )

    if args.json:
        print(format_result_json(result))
    else:
        print(format_result(result))


if __name__ == "__main__":
    main()
