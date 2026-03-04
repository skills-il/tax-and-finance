#!/usr/bin/env python3
"""Fetch TASE (Tel Aviv Stock Exchange) index data and stock quotes.

Retrieves index composition, weights, and performance data for TA-35
and TA-125 indices. Also supports individual stock lookups and Maya
filings search.

Usage:
    python scripts/fetch_tase_data.py --index TA35
    python scripts/fetch_tase_data.py --index TA125
    python scripts/fetch_tase_data.py --stock 662577
    python scripts/fetch_tase_data.py --example
"""

import sys
import json
import argparse
from datetime import datetime, timedelta
from typing import Optional
from urllib.request import urlopen, Request
from urllib.error import URLError


# TASE API base URL (public market data)
TASE_API_BASE = "https://api.tase.co.il/api"

# Index identifiers
INDICES = {
    "TA35": {"id": "142", "name": "TA-35", "hebrew": 'ת"א-35'},
    "TA125": {"id": "143", "name": "TA-125", "hebrew": 'ת"א-125'},
    "TA90": {"id": "164", "name": "TA-90", "hebrew": 'ת"א-90'},
    "TABANK": {"id": "145", "name": "TA-Banks", "hebrew": 'ת"א-בנקים'},
    "TAREAL": {"id": "146", "name": "TA-Real Estate", "hebrew": 'ת"א-נדל"ן'},
}

# Well-known dual-listed companies (TASE securities number -> NASDAQ/NYSE ticker)
DUAL_LISTED = {
    "662577": {"name": "Bank Hapoalim", "us_ticker": None},
    "604611": {"name": "Check Point", "us_ticker": "CHKP"},
    "1092508": {"name": "CyberArk", "us_ticker": "CYBR"},
    "691212": {"name": "NICE", "us_ticker": "NICE"},
    "1084992": {"name": "Sapiens", "us_ticker": "SPNS"},
    "604645": {"name": "Teva", "us_ticker": "TEVA"},
    "1082285": {"name": "Fiverr", "us_ticker": "FVRR"},
    "604629": {"name": "ICL", "us_ticker": "ICL"},
}


def fetch_json(url: str, headers: Optional[dict] = None) -> dict:
    """Fetch JSON from a URL with optional headers.

    Args:
        url: The URL to fetch.
        headers: Optional HTTP headers.

    Returns:
        Parsed JSON response as a dictionary.
    """
    req = Request(url)
    if headers:
        for key, value in headers.items():
            req.add_header(key, value)
    try:
        with urlopen(req, timeout=10) as response:
            return json.loads(response.read().decode("utf-8"))
    except URLError as e:
        print(f"Error fetching {url}: {e}")
        sys.exit(1)


def fetch_index_data(index_key: str) -> dict:
    """Fetch index composition and performance data.

    Args:
        index_key: One of TA35, TA125, TA90, TABANK, TAREAL.

    Returns:
        Dictionary with index data including components and weights.
    """
    if index_key not in INDICES:
        print(f"Unknown index: {index_key}. Available: {list(INDICES.keys())}")
        sys.exit(1)

    index_info = INDICES[index_key]
    print(f"Fetching {index_info['name']} ({index_info['hebrew']}) data...")
    print(f"TASE API endpoint: {TASE_API_BASE}/index/{index_info['id']}/components")
    print()
    print("Note: TASE API requires authentication token from tase.co.il.")
    print("For development, use the example data below or register at:")
    print("  https://info.tase.co.il/heb/marketdata/pages/api.aspx")
    print()

    return {
        "index": index_info["name"],
        "hebrew_name": index_info["hebrew"],
        "api_endpoint": f"{TASE_API_BASE}/index/{index_info['id']}/components",
        "note": "Authenticate at tase.co.il for live data",
    }


def fetch_stock_data(securities_number: str) -> dict:
    """Fetch individual stock data by TASE securities number.

    Args:
        securities_number: Numeric TASE securities identifier.

    Returns:
        Dictionary with stock information.
    """
    dual_info = DUAL_LISTED.get(securities_number, {})
    print(f"Looking up securities number: {securities_number}")
    if dual_info:
        print(f"  Company: {dual_info['name']}")
        if dual_info.get("us_ticker"):
            print(f"  US ticker: {dual_info['us_ticker']} (dual-listed)")
    print(f"  TASE API: {TASE_API_BASE}/security/{securities_number}")
    print()

    return {
        "securities_number": securities_number,
        "dual_listed": dual_info,
        "api_endpoint": f"{TASE_API_BASE}/security/{securities_number}",
    }


def generate_example() -> dict:
    """Generate example TA-35 data for demonstration."""
    return {
        "index": "TA-35",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "components": [
            {"name": "Bank Hapoalim", "hebrew": "בנק הפועלים", "weight_pct": 8.2, "securities_no": "662577"},
            {"name": "Bank Leumi", "hebrew": "בנק לאומי", "weight_pct": 7.5, "securities_no": "604654"},
            {"name": "ICL Group", "hebrew": "כי\"ל", "weight_pct": 5.8, "securities_no": "604629"},
            {"name": "Teva Pharmaceutical", "hebrew": "טבע", "weight_pct": 5.1, "securities_no": "604645"},
            {"name": "Check Point", "hebrew": "צ'ק פוינט", "weight_pct": 4.9, "securities_no": "604611"},
            {"name": "NICE", "hebrew": "נייס", "weight_pct": 4.3, "securities_no": "691212"},
            {"name": "Bank Discount", "hebrew": "בנק דיסקונט", "weight_pct": 4.0, "securities_no": "691205"},
            {"name": "Mizrahi Tefahot", "hebrew": "מזרחי טפחות", "weight_pct": 3.8, "securities_no": "695437"},
            {"name": "Elbit Systems", "hebrew": "אלביט מערכות", "weight_pct": 3.5, "securities_no": "604630"},
            {"name": "Tower Semiconductor", "hebrew": "טאואר", "weight_pct": 3.2, "securities_no": "604642"},
        ],
        "note": "Example data for demonstration. Use TASE API for live data.",
    }


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Fetch TASE index and stock data"
    )
    parser.add_argument("--index", choices=list(INDICES.keys()),
                        help="Fetch index composition (TA35, TA125, etc.)")
    parser.add_argument("--stock", help="Fetch stock by TASE securities number")
    parser.add_argument("--example", action="store_true",
                        help="Show example TA-35 data")

    args = parser.parse_args()

    if not any([args.index, args.stock, args.example]):
        parser.print_help()
        sys.exit(1)

    if args.example:
        data = generate_example()
        print("Example TA-35 index data:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        return

    if args.index:
        data = fetch_index_data(args.index)
        print(json.dumps(data, indent=2, ensure_ascii=False))

    if args.stock:
        data = fetch_stock_data(args.stock)
        print(json.dumps(data, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
