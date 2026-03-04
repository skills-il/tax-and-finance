#!/usr/bin/env python3
"""Display TASE index composition and sector data.

Provides reference data for Tel Aviv Stock Exchange indices,
sector breakdowns, and dual-listed companies.

Usage:
    python tase_fetcher.py --index ta-35
    python tase_fetcher.py --sectors
    python tase_fetcher.py --dual-listed
    python tase_fetcher.py --help
"""

import argparse

INDICES = {
    "ta-35": {
        "name_he": "ת\"א-35",
        "companies": 35,
        "description": "Largest market-cap stocks, blue-chip benchmark",
    },
    "ta-125": {
        "name_he": "ת\"א-125",
        "companies": 125,
        "description": "Broad market index, includes TA-35",
    },
    "ta-90": {
        "name_he": "ת\"א-90",
        "companies": 90,
        "description": "Mid-cap stocks (TA-125 minus TA-35)",
    },
    "ta-sme60": {
        "name_he": "ת\"א-צמיחה",
        "companies": 60,
        "description": "Small/growth companies",
    },
    "ta-banks5": {
        "name_he": "ת\"א-בנקים5",
        "companies": 5,
        "description": "Bank Hapoalim, Leumi, Discount, Mizrahi-Tefahot, First International",
    },
}

SECTORS = {
    "Banking & Finance": {"weight": "~25%", "key_stocks": ["Hapoalim", "Leumi", "Discount", "Mizrahi-Tefahot"]},
    "Technology": {"weight": "~20%", "key_stocks": ["Check Point", "Nice", "CyberArk", "Tower Semi"]},
    "Real Estate": {"weight": "~12%", "key_stocks": ["Azrieli", "Amot", "Melisron"]},
    "Energy & Chemicals": {"weight": "~10%", "key_stocks": ["ICL", "Delek", "Bazan"]},
    "Insurance": {"weight": "~8%", "key_stocks": ["Harel", "Migdal", "Clal"]},
}

DUAL_LISTED = [
    {"name": "Check Point", "tase": "CHKP", "us": "CHKP (NASDAQ)"},
    {"name": "Nice Systems", "tase": "NICE", "us": "NICE (NASDAQ)"},
    {"name": "Teva Pharmaceutical", "tase": "TEVA", "us": "TEVA (NYSE)"},
    {"name": "ICL Group", "tase": "ICL", "us": "ICL (NYSE)"},
    {"name": "Elbit Systems", "tase": "ESLT", "us": "ESLT (NASDAQ)"},
    {"name": "CyberArk", "tase": "CYBR", "us": "CYBR (NASDAQ)"},
    {"name": "Tower Semiconductor", "tase": "TSEM", "us": "TSEM (NASDAQ)"},
    {"name": "Sapiens International", "tase": "SPNS", "us": "SPNS (NASDAQ)"},
]

def show_index(name):
    idx = INDICES[name]
    print(f"\n{idx['name_he']} ({name.upper()})")
    print("=" * 40)
    print(f"Companies: {idx['companies']}")
    print(f"Description: {idx['description']}")

def show_sectors():
    print("\nTA-35 Sector Breakdown")
    print("=" * 50)
    for sector, data in SECTORS.items():
        print(f"\n{sector} ({data['weight']})")
        for stock in data["key_stocks"]:
            print(f"  - {stock}")

def show_dual_listed():
    print("\nDual-Listed Israeli Companies (TASE + US)")
    print("=" * 55)
    print(f"{'Company':<25} {'TASE':<10} {'US Exchange'}")
    print("-" * 55)
    for co in DUAL_LISTED:
        print(f"{co['name']:<25} {co['tase']:<10} {co['us']}")

def main():
    parser = argparse.ArgumentParser(description="TASE index and sector data")
    parser.add_argument("--index", choices=list(INDICES.keys()), help="Show index info")
    parser.add_argument("--sectors", action="store_true", help="Show sector breakdown")
    parser.add_argument("--dual-listed", action="store_true", help="Show dual-listed companies")
    args = parser.parse_args()

    if args.index:
        show_index(args.index)
    elif args.sectors:
        show_sectors()
    elif args.dual_listed:
        show_dual_listed()
    else:
        for name in INDICES:
            show_index(name)
        show_sectors()

if __name__ == "__main__":
    main()
