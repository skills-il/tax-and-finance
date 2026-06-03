#!/usr/bin/env python3
"""Fetch and convert currencies using Bank of Israel exchange rates.

Current rates come from the live Bank of Israel JSON endpoint. Historical
(tax-date) rates come from the Bank of Israel SDMX EXR series, because the
JSON endpoint's ?date= parameter is ignored and always returns today's rate.

Usage:
    python scripts/fetch_rates.py --list
    python scripts/fetch_rates.py --from USD --to ILS --amount 1000
    python scripts/fetch_rates.py --from ILS --to EUR --amount 5000
    python scripts/fetch_rates.py --from USD --to ILS --amount 100 --date 2026-01-15
"""

import sys
import argparse
import json
import csv
import io
from urllib.request import urlopen
from urllib.error import URLError
from datetime import date
from typing import Optional


# Live JSON endpoint for current representative rates.
BOI_CURRENT_URL = "https://www.boi.org.il/PublicApi/GetExchangeRates"
# SDMX EXR series for historical rates: insert the currency code and date range.
BOI_SDMX_URL = (
    "https://edge.boi.gov.il/FusionEdgeServer/sdmx/v2/data/dataflow/"
    "BOI.STATISTICS/EXR/1.0/RER_{cur}_ILS"
    "?startPeriod={start}&endPeriod={end}&format=csv"
)

# The 14 currencies the Bank of Israel publishes a representative rate for,
# with their Hebrew transliterations.
COMMON_CURRENCIES = {
    "USD": ("US Dollar", "dolar"),
    "GBP": ("British Pound", "lira sterling"),
    "JPY": ("Japanese Yen", "yen"),
    "EUR": ("Euro", "euro"),
    "AUD": ("Australian Dollar", "dolar australi"),
    "CAD": ("Canadian Dollar", "dolar kanadi"),
    "DKK": ("Danish Krone", "krone dani"),
    "NOK": ("Norwegian Krone", "krone norvegi"),
    "ZAR": ("South African Rand", "rand"),
    "SEK": ("Swedish Krona", "krona shvedit"),
    "CHF": ("Swiss Franc", "frank shveitzi"),
    "JOD": ("Jordanian Dinar", "dinar yardeni"),
    "LBP": ("Lebanese Pound", "lira levanonit"),
    "EGP": ("Egyptian Pound", "lira mitzrit"),
}


class RateFetchError(Exception):
    """Raised when a real rate cannot be fetched. The caller must FAIL LOUD and
    must never substitute sample data for a tax-stamped conversion."""


def fetch_current_rates() -> dict:
    """Fetch current representative rates from the Bank of Israel JSON endpoint.

    Returns:
        Dictionary mapping currency code to (rate, unit, change_pct) tuples.
        change_pct is the percentage daily move, not an absolute NIS delta.

    Raises:
        RateFetchError: if the endpoint cannot be reached or returns no usable
            rates. The caller must abort, NOT fall back to sample data.
    """
    try:
        with urlopen(BOI_CURRENT_URL, timeout=15) as response:
            data = json.loads(response.read().decode("utf-8"))
    except (URLError, ValueError) as e:
        raise RateFetchError(
            f"Could not fetch live rates from Bank of Israel: {e}"
        ) from e

    rates = {}
    for entry in data.get("exchangeRates", []):
        code = entry.get("key")
        rate = entry.get("currentExchangeRate")
        unit = entry.get("unit", 1)
        change = entry.get("currentChange", 0.0)
        if code and rate:
            rates[code] = (float(rate), int(unit), float(change))
    if not rates:
        raise RateFetchError(
            "Bank of Israel endpoint returned no usable rates."
        )
    return rates


def fetch_historical_rate(currency: str, target_date: str) -> Optional[tuple]:
    """Fetch a historical representative rate from the SDMX EXR series.

    The series omits non-publication days (Saturday, Sunday, holidays), so this
    walks back to the most recent published date on or before target_date.

    Args:
        currency: Currency code (e.g., USD). ILS is not fetched (it is the base).
        target_date: Requested date in YYYY-MM-DD format.

    Returns:
        Tuple of (rate, unit, used_date), or None if the series has no published
        observation on or before target_date. The unit is derived from the
        SDMX UNIT_MULT column (unit = 10 ** UNIT_MULT) so the script
        self-corrects if BOI re-bases a series.

    Raises:
        RateFetchError: if the SDMX endpoint cannot be reached. The caller must
            abort, NOT fall back to sample data.
    """
    currency = currency.upper()
    if currency == "ILS":
        return (1.0, 1, target_date)

    # Look back up to 21 days to cross weekends + multi-day holiday clusters.
    from datetime import datetime, timedelta

    end = datetime.strptime(target_date, "%Y-%m-%d").date()
    start = end - timedelta(days=21)
    url = BOI_SDMX_URL.format(
        cur=currency, start=start.isoformat(), end=end.isoformat()
    )
    try:
        with urlopen(url, timeout=20) as response:
            text = response.read().decode("utf-8")
    except URLError as e:
        raise RateFetchError(
            f"Could not fetch historical rate for {currency} from BOI SDMX: {e}"
        ) from e

    reader = csv.DictReader(io.StringIO(text))
    rows = [r for r in reader if r.get("OBS_VALUE")]
    if not rows:
        return None

    # Keep only rows on or before the requested date, pick the latest.
    eligible = [r for r in rows if r["TIME_PERIOD"] <= target_date]
    if not eligible:
        return None
    chosen = max(eligible, key=lambda r: r["TIME_PERIOD"])

    # Unit basis from the SDMX UNIT_MULT exponent (USD=0 -> 1, JPY=2 -> 100,
    # LBP=1 -> 10). Falls back to 1 if the column is missing/unparseable.
    try:
        unit = 10 ** int(chosen.get("UNIT_MULT", "0"))
    except (TypeError, ValueError):
        unit = 1
    return (float(chosen["OBS_VALUE"]), unit, chosen["TIME_PERIOD"])


def _sample_rates() -> dict:
    """ILLUSTRATIVE sample rates for offline demo ONLY (mid-2026 snapshot).

    These are NOT live and NOT the official representative rate. They are only
    reachable via the explicit --demo flag, and any output built from them is
    labeled as illustrative sample data that must not be used for tax.
    """
    return {
        "USD": (2.872, 1, 1.66),
        "EUR": (3.3365, 1, 1.41),
        "GBP": (3.8629, 1, 1.52),
        "JPY": (1.7968, 100, 1.59),
        "CHF": (3.6409, 1, 1.22),
        "CAD": (2.0732, 1, 1.66),
        "AUD": (2.0584, 1, 1.45),
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
        rates: Exchange rates dictionary mapping code to (rate, unit, change).

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


def build_dated_rates(
    from_currency: str, to_currency: str, target_date: str
) -> tuple[dict, str]:
    """Build a rates dict for a specific historical date using SDMX.

    Returns the rates dict plus the actual publication date used (which may be
    earlier than target_date if the requested day had no publication).
    """
    rates = {"ILS": (1.0, 1, 0.0)}
    used_date = target_date
    for cur in {from_currency.upper(), to_currency.upper()}:
        if cur == "ILS":
            continue
        hist = fetch_historical_rate(cur, target_date)
        if hist is None:
            continue
        rate, unit, when = hist
        rates[cur] = (rate, unit, 0.0)
        used_date = when  # last writer wins; both should resolve to same day
    return rates, used_date


def format_result(
    amount: float,
    from_currency: str,
    to_currency: str,
    result: float,
    description: str,
    rate_date: Optional[str] = None,
    is_sample: bool = False,
) -> str:
    """Format conversion result for display."""
    date_str = rate_date or date.today().isoformat()
    if is_sample:
        lines = [
            "=== Currency Conversion (DEMO) ===",
            "",
            f"  {amount:,.2f} {from_currency.upper()} = {result:,.2f} {to_currency.upper()}",
            "",
            f"  Rate: {description}",
            "  Source: ILLUSTRATIVE SAMPLE DATA, NOT the official rate.",
            "",
            "  WARNING: Sample data only. Do NOT use for tax, VAT, or any filing.",
        ]
        return "\n".join(lines)
    lines = [
        "=== Currency Conversion ===",
        "",
        f"  {amount:,.2f} {from_currency.upper()} = {result:,.2f} {to_currency.upper()}",
        "",
        f"  Rate: {description}",
        f"  Date: {date_str}",
        "  Source: Bank of Israel representative rate (shaar yatzig)",
        "",
        "  NOTE: Representative rate for reference. Actual bank rates may differ.",
        "  NOTE: For import VAT, use the weekly customs rate, not this rate.",
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
    parser.add_argument(
        "--demo", "--offline", dest="demo", action="store_true",
        help="Use illustrative SAMPLE rates offline (NOT official, not for tax)",
    )

    args = parser.parse_args()

    if args.list:
        print("=== Bank of Israel Published Currencies (14) ===")
        print(f"  {'Code':<6} {'Currency':<25} {'Hebrew':<20}")
        print(f"  {'-' * 51}")
        print(f"  {'ILS':<6} {'Israeli New Shekel':<25} {'shekel chadash':<20}")
        for code, (name, hebrew) in COMMON_CURRENCIES.items():
            print(f"  {code:<6} {name:<25} {hebrew:<20}")
        return

    if not all([args.from_curr, args.to_curr, args.amount]):
        parser.print_help()
        sys.exit(1)

    supported = set(COMMON_CURRENCIES) | {"ILS"}
    requested = {args.from_curr.upper(), args.to_curr.upper()}
    unsupported = requested - supported
    if unsupported:
        print(
            f"Error: Currency not published by the Bank of Israel: "
            f"{', '.join(sorted(unsupported))}.",
            file=sys.stderr,
        )
        print(
            "Only these 14 currencies are supported: "
            + ", ".join(COMMON_CURRENCIES) + ".",
            file=sys.stderr,
        )
        sys.exit(2)

    is_sample = False
    try:
        if args.demo:
            # Explicit offline mode: illustrative sample data only.
            rates = _sample_rates()
            rates["ILS"] = (1.0, 1, 0.0)
            is_sample = True
            used_date = None
        elif args.date:
            rates, used_date = build_dated_rates(
                args.from_curr, args.to_curr, args.date
            )
        else:
            rates = fetch_current_rates()
            used_date = None
    except RateFetchError as e:
        # FAIL LOUD: never present sample data as an official tax rate.
        print(f"Error: {e}", file=sys.stderr)
        print(
            "Aborting: no live rate available, and sample rates are never "
            "substituted for a real conversion. Re-run later, or use --demo "
            "for clearly-labeled illustrative output only.",
            file=sys.stderr,
        )
        sys.exit(1)

    result = convert(args.amount, args.from_curr, args.to_curr, rates)
    if result is None:
        # Both currencies are supported (checked above), so this means the
        # SDMX series had no published observation on or before the date.
        print(
            f"Error: No published rate found on or before {args.date} for "
            f"{args.from_curr.upper()}/{args.to_curr.upper()}.",
            file=sys.stderr,
        )
        print(
            "Try an earlier date; the series omits Saturdays, Sundays, and "
            "Israeli holidays.",
            file=sys.stderr,
        )
        sys.exit(1)

    converted, _rate_used, description = result
    print(format_result(
        args.amount, args.from_curr, args.to_curr,
        converted, description, used_date or args.date,
        is_sample=is_sample,
    ))


if __name__ == "__main__":
    main()
