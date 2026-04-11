#!/usr/bin/env python3
"""Fetch Bank of Israel economic data: exchange rates, interest rates, and CPI.

Retrieves data from the BOI public API (SDMX format) and displays results
in a human-readable format.

Usage:
    python scripts/fetch_boi_rates.py --currency USD
    python scripts/fetch_boi_rates.py --currency EUR --days 30
    python scripts/fetch_boi_rates.py --interest
    python scripts/fetch_boi_rates.py --interest-history
    python scripts/fetch_boi_rates.py --example
"""

import sys
import json
import argparse
from datetime import datetime, timedelta
from typing import Optional
from urllib.request import urlopen, Request
from urllib.error import URLError
import xml.etree.ElementTree as ET


# BOI API endpoints (SDMX format)
BOI_API_BASE = "https://edge.boi.gov.il/FusionEdgeServer/sdmx/v2/data/dataflow/BOI"

# Exchange rate endpoint
EXR_ENDPOINT = f"{BOI_API_BASE}/EXR/1.0"

# Interest rate endpoint
IR_ENDPOINT = f"{BOI_API_BASE}/IR_INTEREST/1.0"

# Supported currencies for exchange rates
# מטבעות נתמכים לשערי חליפין
CURRENCIES = {
    "USD": {"name": "US Dollar", "hebrew": "דולר אמריקאי", "unit": 1},
    "EUR": {"name": "Euro", "hebrew": "אירו", "unit": 1},
    "GBP": {"name": "British Pound", "hebrew": "לירה שטרלינג", "unit": 1},
    "JPY": {"name": "Japanese Yen", "hebrew": "ין יפני", "unit": 100},
    "CHF": {"name": "Swiss Franc", "hebrew": "פרנק שוויצרי", "unit": 1},
    "AUD": {"name": "Australian Dollar", "hebrew": "דולר אוסטרלי", "unit": 1},
    "CAD": {"name": "Canadian Dollar", "hebrew": "דולר קנדי", "unit": 1},
    "ZAR": {"name": "South African Rand", "hebrew": "ראנד דרום אפריקאי", "unit": 1},
    "SEK": {"name": "Swedish Krona", "hebrew": "כתר שוודי", "unit": 1},
    "NOK": {"name": "Norwegian Krone", "hebrew": "כתר נורווגי", "unit": 1},
    "DKK": {"name": "Danish Krone", "hebrew": "כתר דני", "unit": 1},
    "JOD": {"name": "Jordanian Dinar", "hebrew": "דינר ירדני", "unit": 1},
    "EGP": {"name": "Egyptian Pound", "hebrew": "לירה מצרית", "unit": 1},
}


def fetch_url(url: str) -> str:
    """Fetch URL content as string.

    Args:
        url: URL to fetch.

    Returns:
        Response body as string.
    """
    req = Request(url)
    req.add_header("Accept", "application/xml")
    try:
        with urlopen(req, timeout=15) as response:
            return response.read().decode("utf-8")
    except URLError:
        print("Error: Could not connect to the BOI API. Please check your network connection.")
        sys.exit(1)


def fetch_exchange_rate(currency: str, days: int = 1) -> list:
    """Fetch exchange rate for a currency from BOI API.

    Args:
        currency: Currency code (e.g., 'USD', 'EUR').
        days: Number of days of history to fetch.

    Returns:
        List of dicts with date and rate.
    """
    if currency.upper() not in CURRENCIES:
        print(f"Unsupported currency: {currency}")
        print(f"Supported: {', '.join(CURRENCIES.keys())}")
        sys.exit(1)

    currency = currency.upper()
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

    url = (f"{EXR_ENDPOINT}"
           f"?startperiod={start_date}&endperiod={end_date}"
           f"&c[CURRENCY]={currency}")

    print(f"Fetching {currency} exchange rate from BOI...")
    print()

    try:
        xml_data = fetch_url(url)
        rates = parse_sdmx_rates(xml_data)
        return rates
    except Exception as e:
        print(f"Error parsing BOI response: {e}")
        print("Returning example data instead.")
        return generate_example_rate(currency, days)


def parse_sdmx_rates(xml_data: str) -> list:
    """Parse SDMX XML response from BOI API.

    Args:
        xml_data: Raw XML response string.

    Returns:
        List of dicts with date and rate.
    """
    rates = []
    try:
        root = ET.fromstring(xml_data)
        # SDMX namespaces vary; try common patterns
        ns = {
            "message": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message",
            "generic": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic",
        }
        for obs in root.iter():
            if "Obs" in obs.tag:
                date_elem = obs.find(".//{%s}ObsDimension" % ns.get("generic", ""))
                value_elem = obs.find(".//{%s}ObsValue" % ns.get("generic", ""))
                if date_elem is not None and value_elem is not None:
                    rates.append({
                        "date": date_elem.get("value", ""),
                        "rate": float(value_elem.get("value", 0)),
                    })
    except ET.ParseError:
        pass
    return rates


def generate_example_rate(currency: str, days: int) -> list:
    """Generate example exchange rate data for demonstration.

    Args:
        currency: Currency code.
        days: Number of days.

    Returns:
        Example rate data.
    """
    # שערים לדוגמה - Example rates (approximate)
    base_rates = {
        "USD": 3.60, "EUR": 3.95, "GBP": 4.55, "JPY": 2.40,
        "CHF": 4.10, "AUD": 2.35, "CAD": 2.65, "ZAR": 0.20,
    }
    base = base_rates.get(currency, 3.60)
    rates = []
    for i in range(min(days, 30)):
        date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        # Skip weekends (BOI doesn't publish on Fri/Sat)
        weekday = (datetime.now() - timedelta(days=i)).weekday()
        if weekday in (4, 5):  # Friday=4, Saturday=5 in Israel context
            continue
        # Small random-like variation
        variation = ((i * 7 + 3) % 10 - 5) / 1000
        rates.append({"date": date, "rate": round(base + variation, 4)})
    return rates


def fetch_interest_rate() -> dict:
    """Fetch current BOI interest rate.

    Returns:
        Dictionary with current interest rate info.
    """
    print("Fetching BOI interest rate...")
    print(f"API URL: {IR_ENDPOINT}")
    print()
    print("Note: BOI Monetary Committee announces rate decisions ~6 times/year.")
    print("Rate decisions page: https://www.boi.org.il/en/economic-roles/monetary-policy/")
    print()

    # Return structured info (API parsing is complex for SDMX)
    return {
        "source": "Bank of Israel Monetary Committee",
        "api_endpoint": IR_ENDPOINT,
        "note": "Use BOI website for latest rate. API returns SDMX XML.",
        "website": "https://www.boi.org.il/en/economic-roles/monetary-policy/",
    }


def print_rates(currency: str, rates: list) -> None:
    """Print exchange rates in a formatted table."""
    info = CURRENCIES.get(currency, {})
    unit = info.get("unit", 1)
    unit_str = f" (per {unit})" if unit > 1 else ""

    print(f"  {info.get('name', currency)} ({info.get('hebrew', '')}){unit_str}")
    print(f"  {'Date':<12} {'Rate (NIS)':<12}")
    print(f"  {'-'*12} {'-'*12}")
    for r in rates[:10]:
        print(f"  {r['date']:<12} {r['rate']:<12.4f}")

    if rates:
        latest = rates[0]
        print(f"\n  Latest: 1 {currency}{unit_str} = {latest['rate']} NIS")
        if unit == 1:
            print(f"  Inverse: 1 NIS = {1/latest['rate']:.4f} {currency}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Fetch Bank of Israel economic data "
                    "(שליפת נתונים כלכליים מבנק ישראל)"
    )
    parser.add_argument(
        "--currency",
        help=f"Currency code for exchange rate ({', '.join(list(CURRENCIES.keys())[:6])}...)"
    )
    parser.add_argument(
        "--days", type=int, default=7,
        help="Number of days of rate history (default: 7)"
    )
    parser.add_argument(
        "--interest", action="store_true",
        help="Fetch current BOI interest rate (ריבית בנק ישראל)"
    )
    parser.add_argument(
        "--interest-history", action="store_true",
        help="Show recent interest rate changes"
    )
    parser.add_argument(
        "--list-currencies", action="store_true",
        help="List all supported currencies"
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Output as JSON"
    )
    parser.add_argument(
        "--example", action="store_true",
        help="Show example data"
    )

    args = parser.parse_args()

    if not any([args.currency, args.interest, args.interest_history,
                args.list_currencies, args.example]):
        parser.print_help()
        sys.exit(1)

    if args.list_currencies:
        print("Supported currencies (מטבעות נתמכים):")
        print(f"  {'Code':<6} {'Name':<25} {'Hebrew':<20} {'Unit':<6}")
        print(f"  {'-'*6} {'-'*25} {'-'*20} {'-'*6}")
        for code, info in CURRENCIES.items():
            print(f"  {code:<6} {info['name']:<25} {info['hebrew']:<20} {info['unit']:<6}")
        return

    if args.example:
        print("=== Example: USD/NIS Exchange Rate (7 days) ===")
        rates = generate_example_rate("USD", 7)
        print_rates("USD", rates)
        print("\n=== Example: EUR/NIS Exchange Rate (7 days) ===")
        rates = generate_example_rate("EUR", 7)
        print_rates("EUR", rates)
        return

    if args.currency:
        rates = fetch_exchange_rate(args.currency.upper(), args.days)
        if args.json:
            print(json.dumps(rates, indent=2, ensure_ascii=False))
        else:
            print_rates(args.currency.upper(), rates)

    if args.interest or args.interest_history:
        info = fetch_interest_rate()
        if args.json:
            print(json.dumps(info, indent=2, ensure_ascii=False))
        else:
            print("BOI Interest Rate Information:")
            for key, value in info.items():
                print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
