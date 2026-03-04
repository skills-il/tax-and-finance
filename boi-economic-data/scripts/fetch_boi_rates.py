#!/usr/bin/env python3
"""Fetch Bank of Israel exchange rates and interest rate data.

Uses the BOI SDMX API (edge.boi.gov.il) to retrieve representative
exchange rates, interest rate decisions, and economic indicators.

Usage:
    python scripts/fetch_boi_rates.py --currency USD --latest
    python scripts/fetch_boi_rates.py --currency EUR --start 2026-01-01 --end 2026-01-31
    python scripts/fetch_boi_rates.py --interest-rate
    python scripts/fetch_boi_rates.py --example
"""

import sys
import json
import argparse
from datetime import datetime, timedelta
from urllib.request import urlopen, Request
from urllib.error import URLError


# BOI SDMX API base URL
BOI_API_BASE = "https://edge.boi.gov.il/FusionEdgeServer/sdmx/v2/data/dataflow/BOI.STAT"

# Common currency codes tracked by BOI
CURRENCIES = {
    "USD": "RER_USD_ILS",
    "EUR": "RER_EUR_ILS",
    "GBP": "RER_GBP_ILS",
    "JPY": "RER_JPY_ILS",
    "CHF": "RER_CHF_ILS",
    "AUD": "RER_AUD_ILS",
    "CAD": "RER_CAD_ILS",
    "SEK": "RER_SEK_ILS",
    "NOK": "RER_NOK_ILS",
    "DKK": "RER_DKK_ILS",
    "ZAR": "RER_ZAR_ILS",
    "JOD": "RER_JOD_ILS",
    "EGP": "RER_EGP_ILS",
}

# Data flow paths
DATAFLOWS = {
    "exchange_rate": "EXR/1.0",
    "interest_rate": "DIR/1.0",
}


def fetch_boi_data(url: str) -> dict:
    """Fetch JSON data from BOI API.

    Args:
        url: Full API URL.

    Returns:
        Parsed JSON response.
    """
    req = Request(url, headers={
        "Accept": "application/json",
        "User-Agent": "skills-il-boi-economic-data/1.0",
    })
    try:
        with urlopen(req, timeout=15) as response:
            return json.loads(response.read().decode("utf-8"))
    except URLError as e:
        print(f"Error fetching BOI data: {e}")
        print("Note: BOI API is available Sunday-Thursday during business hours.")
        print("Weekend and holiday queries may return errors.")
        sys.exit(1)


def fetch_exchange_rate(currency: str, start_date: str = None, end_date: str = None) -> dict:
    """Fetch representative exchange rate (sha'ar yatzig) for a currency.

    Args:
        currency: ISO 4217 currency code (e.g., USD, EUR).
        start_date: Start date in YYYY-MM-DD format.
        end_date: End date in YYYY-MM-DD format.

    Returns:
        Dictionary with rate data.
    """
    if currency.upper() not in CURRENCIES:
        print(f"Currency {currency} not found. Available: {list(CURRENCIES.keys())}")
        sys.exit(1)

    series_key = CURRENCIES[currency.upper()]
    url = f"{BOI_API_BASE}/{DATAFLOWS['exchange_rate']}/{series_key}"

    params = []
    if start_date:
        params.append(f"startperiod={start_date}")
    if end_date:
        params.append(f"endperiod={end_date}")
    if params:
        url += "?" + "&".join(params)

    print(f"Fetching {currency}/ILS rate from Bank of Israel...")
    print(f"API URL: {url}")
    print()

    try:
        data = fetch_boi_data(url)
        return {
            "currency": currency.upper(),
            "pair": f"{currency.upper()}/ILS",
            "source": "Bank of Israel (sha'ar yatzig)",
            "api_url": url,
            "data": data,
        }
    except SystemExit:
        return {
            "currency": currency.upper(),
            "pair": f"{currency.upper()}/ILS",
            "api_url": url,
            "note": "Fetch failed. Use this URL directly or check BOI website.",
        }


def fetch_interest_rate() -> dict:
    """Fetch BOI monetary interest rate decisions.

    Returns:
        Dictionary with interest rate data.
    """
    url = f"{BOI_API_BASE}/{DATAFLOWS['interest_rate']}/DIR_BOI"
    print("Fetching BOI interest rate decisions...")
    print(f"API URL: {url}")
    print()

    try:
        data = fetch_boi_data(url)
        return {
            "indicator": "BOI Monetary Interest Rate",
            "hebrew": "ריבית בנק ישראל",
            "source": "Bank of Israel Monetary Committee",
            "api_url": url,
            "data": data,
        }
    except SystemExit:
        return {
            "indicator": "BOI Monetary Interest Rate",
            "api_url": url,
            "note": "Fetch failed. Use this URL directly or check BOI website.",
        }


def generate_example() -> dict:
    """Generate example data for demonstration."""
    return {
        "example_rates": {
            "USD/ILS": {
                "date": "2026-03-03",
                "rate": 3.62,
                "change_pct": -0.15,
                "source": "Bank of Israel representative rate (sha'ar yatzig)",
            },
            "EUR/ILS": {
                "date": "2026-03-03",
                "rate": 3.95,
                "change_pct": 0.22,
                "source": "Bank of Israel representative rate (sha'ar yatzig)",
            },
        },
        "boi_interest_rate": {
            "current_rate": 4.5,
            "last_change_date": "2025-01-06",
            "last_change": -0.25,
            "next_decision": "Check BOI calendar",
        },
        "cpi": {
            "latest_value": 106.8,
            "month": "2026-01",
            "year_over_year_pct": 2.8,
            "source": "CBS (Lishkat HaStatistika)",
        },
        "note": "Example data for demonstration. Use BOI API for live data.",
        "api_base": BOI_API_BASE,
        "available_currencies": list(CURRENCIES.keys()),
    }


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Fetch BOI exchange rates and economic data"
    )
    parser.add_argument("--currency", help="Currency code (e.g., USD, EUR, GBP)")
    parser.add_argument("--latest", action="store_true",
                        help="Fetch latest available rate")
    parser.add_argument("--start", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end", help="End date (YYYY-MM-DD)")
    parser.add_argument("--interest-rate", action="store_true",
                        help="Fetch BOI interest rate decisions")
    parser.add_argument("--list-currencies", action="store_true",
                        help="List available currency codes")
    parser.add_argument("--example", action="store_true",
                        help="Show example data")

    args = parser.parse_args()

    if not any([args.currency, args.interest_rate, args.list_currencies, args.example]):
        parser.print_help()
        sys.exit(1)

    if args.example:
        data = generate_example()
        print("Example BOI economic data:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        return

    if args.list_currencies:
        print("Available currencies for BOI exchange rates:")
        for code, series in CURRENCIES.items():
            print(f"  {code}: {series}")
        return

    if args.interest_rate:
        data = fetch_interest_rate()
        print(json.dumps(data, indent=2, ensure_ascii=False))
        return

    if args.currency:
        start = args.start
        end = args.end
        if args.latest and not start:
            start = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
            end = datetime.now().strftime("%Y-%m-%d")

        data = fetch_exchange_rate(args.currency, start, end)
        print(json.dumps(data, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
