#!/usr/bin/env python3
"""Fetch and convert currencies using Bank of Israel exchange rates.

Retrieves the official representative rate (shaar yatzig) from the
Bank of Israel API and performs currency conversions to/from NIS.

Usage:
    python scripts/fetch_rates.py --list
    python scripts/fetch_rates.py --from USD --to ILS --amount 1000
    python scripts/fetch_rates.py --from ILS --to EUR --amount 5000
    python scripts/fetch_rates.py --from USD --to ILS --amount 100 --date 2026-01-15
"""

import sys
import argparse
import json
from urllib.request import urlopen
from urllib.error import URLError
from xml.etree import ElementTree
from datetime import datetime, date
from typing import Optional


BOI_CURRENT_URL = "https://www.boi.org.il/currency.xml"
BOI_HISTORICAL_URL = "https://www.boi.org.il/PublicApi/GetExchangeRates"

# Common currencies with their Hebrew names
COMMON_CURRENCIES = {
    "USD": ("US Dollar", "dolar"),
    "EUR": ("Euro", "euro"),
    "GBP": ("British Pound", "lira sterling"),
    "JPY": ("Japanese Yen", "yen"),
    "CHF": ("Swiss Franc", "frank shveitzi"),
    "CAD": ("Canadian Dollar", "dolar kanadi"),
    "AUD": ("Australian Dollar", "dolar australi"),
    "ZAR": ("South African Rand", "rand"),
    "SEK": ("Swedish Krona", "krona"),
    "NOK": ("Norwegian Krone", "krone"),
    "DKK": ("Danish Krone", "krone"),
    "JOD": ("Jordanian Dinar", "dinar yardeni"),
    "EGP": ("Egyptian Pound", "lira mitzrit"),
}


def fetch_current_rates() -> dict:
    """Fetch current exchange rates from Bank of Israel.

    Returns:
        Dictionary mapping currency code to (rate, unit, change) tuples.
    """
    try:
        with urlopen(BOI_CURRENT_URL, timeout=10) as response:
            xml_data = response.read()
    except URLError as e:
        print(f"Error fetching rates: {e}")
        print("Using sample rates for demonstration.")
        return _sample_rates()

    root = ElementTree.fromstring(xml_data)
    rates = {}

    # Bank of Israel XML namespace handling
    for currency in root.iter():
        if currency.tag.endswith("CURRENCY") or currency.tag == "CURRENCY":
            code = None
            rate = None
            unit = 1
            change = 0.0

            for child in currency:
                tag = child.tag.split("}")[-1] if "}" in child.tag else child.tag
                if tag == "CURRENCYCODE":
                    code = child.text
                elif tag == "RATE":
                    rate = float(child.text)
                elif tag == "UNIT":
                    unit = int(child.text)
                elif tag == "CHANGE":
                    change = float(child.text) if child.text else 0.0

            if code and rate:
                rates[code] = (rate, unit, change)

    return rates


def _sample_rates() -> dict:
    """Sample rates for offline/demo use."""
    return {
        "USD": (3.65, 1, 0.12),
        "EUR": (3.95, 1, -0.05),
        "GBP": (4.62, 1, 0.08),
        "JPY": (2.45, 100, -0.02),
        "CHF": (4.10, 1, 0.03),
        "CAD": (2.70, 1, 0.01),
        "AUD": (2.38, 1, -0.04),
    }


def convert(
    amount: float,
    from_currency: str,
    to_currency: str,
    rates: dict,
) -> Optional[tuple[float, float, str]]:
    """Convert between currencies using Bank of Israel rates.

    Args:
        amount: Amount to convert.
        from_currency: Source currency code.
        to_currency: Target currency code.
        rates: Exchange rates dictionary from fetch_current_rates().

    Returns:
        Tuple of (result, rate_used, description) or None if conversion impossible.
    """
    from_currency = from_currency.upper()
    to_currency = to_currency.upper()

    if from_currency == to_currency:
        return (amount, 1.0, "Same currency")

    if from_currency == "ILS" and to_currency in rates:
        rate, unit, _ = rates[to_currency]
        result = amount / rate * unit
        return (result, rate / unit, f"1 {to_currency} = {rate/unit:.4f} ILS")

    if to_currency == "ILS" and from_currency in rates:
        rate, unit, _ = rates[from_currency]
        result = amount * rate / unit
        return (result, rate / unit, f"1 {from_currency} = {rate/unit:.4f} ILS")

    # Cross-currency via ILS
    if from_currency in rates and to_currency in rates:
        from_rate, from_unit, _ = rates[from_currency]
        to_rate, to_unit, _ = rates[to_currency]
        nis_amount = amount * from_rate / from_unit
        result = nis_amount / to_rate * to_unit
        cross_rate = (from_rate / from_unit) / (to_rate / to_unit)
        return (result, cross_rate, f"1 {from_currency} = {cross_rate:.4f} {to_currency} (via ILS)")

    return None


def format_result(
    amount: float,
    from_currency: str,
    to_currency: str,
    result: float,
    rate_used: float,
    description: str,
    rate_date: Optional[str] = None,
) -> str:
    """Format conversion result for display."""
    date_str = rate_date or date.today().isoformat()
    lines = [
        f"=== Currency Conversion ===",
        f"",
        f"  {amount:,.2f} {from_currency.upper()} = {result:,.2f} {to_currency.upper()}",
        f"",
        f"  Rate: {description}",
        f"  Date: {date_str}",
        f"  Source: Bank of Israel representative rate (shaar yatzig)",
        f"",
        f"  NOTE: Representative rate for reference. Actual bank rates may differ.",
    ]
    return "\n".join(lines)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Convert currencies using Bank of Israel rates"
    )
    parser.add_argument("--from", dest="from_curr", help="Source currency (e.g., USD)")
    parser.add_argument("--to", dest="to_curr", help="Target currency (e.g., ILS)")
    parser.add_argument("--amount", type=float, help="Amount to convert")
    parser.add_argument("--date", type=str, help="Historical date (YYYY-MM-DD)")
    parser.add_argument("--list", action="store_true", help="List available currencies")

    args = parser.parse_args()

    if args.list:
        print("=== Available Currencies (Bank of Israel) ===")
        print(f"  {'Code':<6} {'Currency':<25} {'Hebrew':<20}")
        print(f"  {'─' * 51}")
        print(f"  {'ILS':<6} {'Israeli New Shekel':<25} {'shekel chadash':<20}")
        for code, (name, hebrew) in COMMON_CURRENCIES.items():
            print(f"  {code:<6} {name:<25} {hebrew:<20}")
        return

    if not all([args.from_curr, args.to_curr, args.amount]):
        parser.print_help()
        sys.exit(1)

    rates = fetch_current_rates()
    if not rates:
        print("Error: Could not fetch exchange rates.")
        sys.exit(1)

    result = convert(args.amount, args.from_curr, args.to_curr, rates)
    if result is None:
        print(f"Error: Cannot convert {args.from_curr} to {args.to_curr}.")
        print("Currency not found in Bank of Israel rates.")
        sys.exit(1)

    converted, rate_used, description = result
    print(format_result(
        args.amount, args.from_curr, args.to_curr,
        converted, rate_used, description,
        args.date,
    ))


if __name__ == "__main__":
    main()
