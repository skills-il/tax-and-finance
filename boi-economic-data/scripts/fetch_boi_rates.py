#!/usr/bin/env python3
"""Fetch Israeli economic data: BOI exchange rates, the BOI policy rate, and the CBS CPI.

Data sources:
  - Bank of Israel SDMX API (Fusion Edge Server) for exchange rates and the policy rate.
  - Central Bureau of Statistics index API for the headline Consumer Price Index.

This script never invents numbers. If a source is unreachable or returns no
observations it exits non-zero. Use --example for clearly-labelled sample output.

Usage:
    python scripts/fetch_boi_rates.py --currency USD
    python scripts/fetch_boi_rates.py --currency EUR --days 30
    python scripts/fetch_boi_rates.py --interest
    python scripts/fetch_boi_rates.py --cpi
    python scripts/fetch_boi_rates.py --list-currencies
    python scripts/fetch_boi_rates.py --example
"""

import sys
import json
import time
import argparse
from datetime import datetime, timedelta
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
import xml.etree.ElementTree as ET


# BOI SDMX 2.1 REST API ("new series database" / Fusion Edge Server).
# Two data paths are live and return the same observations:
#   ws/public/sdmxapi/rest/data/{DATAFLOW}/{series}            (used here)
#   sdmx/v2/data/dataflow/BOI.STATISTICS/{DATAFLOW}/1.0/{series}
# A bare dataflow query with no date filter returns EVERY series in the
# dataflow with full history (.../data/EXR/ is ~20 MB back to 1948), so
# always name the series or bound the request with dates/lastNObservations.
BOI_API_BASE = "https://edge.boi.gov.il/FusionEdgeServer/ws/public/sdmxapi/rest/data"

# Representative exchange rates: EXR dataflow, series RER_<CUR>_ILS.
EXR_ENDPOINT = f"{BOI_API_BASE}/EXR"

# BOI policy rate (ריבית בנק ישראל): BR dataflow, daily series MNT_RIB_BOI_D.
# NOT the BIR dataflow, which is commercial-bank credit rates excluding housing.
BR_SERIES = f"{BOI_API_BASE}/BR/MNT_RIB_BOI_D"

# CBS headline CPI (מדד המחירים לצרכן - כללי), index id 120010.
# This API answers HTTP 200 even for an unknown id (with "month": null), so the
# payload must be validated rather than the status code.
CBS_CPI_URL = ("https://api.cbs.gov.il/index/data/price"
               "?id=120010&format=json&download=false&last={last}")

# Supported currencies for exchange rates.
# מטבעות נתמכים לשערי חליפין
CURRENCIES = {
    "USD": {"name": "US Dollar", "hebrew": "דולר אמריקאי"},
    "EUR": {"name": "Euro", "hebrew": "אירו"},
    "GBP": {"name": "British Pound", "hebrew": "לירה שטרלינג"},
    "JPY": {"name": "Japanese Yen", "hebrew": "ין יפני"},
    "CHF": {"name": "Swiss Franc", "hebrew": "פרנק שוויצרי"},
    "AUD": {"name": "Australian Dollar", "hebrew": "דולר אוסטרלי"},
    "CAD": {"name": "Canadian Dollar", "hebrew": "דולר קנדי"},
    "ZAR": {"name": "South African Rand", "hebrew": "ראנד דרום אפריקאי"},
    "SEK": {"name": "Swedish Krona", "hebrew": "כתר שוודי"},
    "NOK": {"name": "Norwegian Krone", "hebrew": "כתר נורווגי"},
    "DKK": {"name": "Danish Krone", "hebrew": "כתר דני"},
    "JOD": {"name": "Jordanian Dinar", "hebrew": "דינר ירדני"},
    "EGP": {"name": "Egyptian Pound", "hebrew": "לירה מצרית"},
}

USER_AGENT = "Mozilla/5.0 (compatible; boi-economic-data-skill/1.x)"


def die(message: str) -> None:
    """Print an error to stderr and exit non-zero.

    A data skill must fail loudly. Returning plausible-looking placeholder
    numbers on failure is worse than returning nothing.
    """
    print(f"Error: {message}", file=sys.stderr)
    sys.exit(1)


def fetch_url(url: str, accept: str = "application/xml",
              attempts: int = 3) -> str:
    """Fetch URL content as text, retrying transient failures.

    api.cbs.gov.il drops connections intermittently under repeated automated
    requests, returning no HTTP status at all, so a single-shot fetch turns a
    recoverable blip into a hard failure. An HTTP error status is NOT retried:
    a 404 will not become a 200.
    """
    req = Request(url)
    req.add_header("Accept", accept)
    req.add_header("User-Agent", USER_AGENT)

    last_reason = None
    for attempt in range(attempts):
        try:
            with urlopen(req, timeout=30) as response:
                return response.read().decode("utf-8")
        except HTTPError as exc:
            die(f"{url} returned HTTP {exc.code}.")
        except URLError as exc:
            last_reason = exc.reason
            if attempt < attempts - 1:
                time.sleep(1 + 2 * attempt)

    die(f"could not reach {url} after {attempts} attempts ({last_reason}). "
        f"api.cbs.gov.il resets connections intermittently under repeated "
        f"automated requests and usually recovers; this is not evidence that "
        f"the endpoint is gone.")
    return ""  # unreachable; keeps type checkers happy


def parse_sdmx(xml_data: str, url: str) -> tuple:
    """Parse an SDMX-XML response into (series_attributes, observations).

    Observations are <Obs> elements carrying TIME_PERIOD and OBS_VALUE as
    ATTRIBUTES. The server emits them as <Obs ...></Obs> (not self-closing),
    so match on the element name, never on the raw text shape.
    """
    try:
        root = ET.fromstring(xml_data)
    except ET.ParseError:
        die(f"{url} did not return parseable XML (a bot-protection or error "
            f"page is the usual cause).")

    attrs, observations = {}, []
    for element in root.iter():
        tag = element.tag.split("}")[-1]
        if tag == "Series" and not attrs:
            attrs = dict(element.attrib)
        elif tag == "Obs":
            date, value = element.get("TIME_PERIOD"), element.get("OBS_VALUE")
            if date and value:
                try:
                    observations.append({"date": date, "value": float(value)})
                except ValueError:
                    continue

    if not observations:
        die(f"{url} returned no observations. The usual cause is a date "
            f"range that covers only non-publication days; try "
            f"lastNObservations=1 instead.")

    observations.sort(key=lambda o: o["date"], reverse=True)
    return attrs, observations


def _validated(currency: str) -> str:
    """Upper-case a currency code and reject anything not in the allowlist."""
    currency = currency.upper()
    if currency not in CURRENCIES:
        die(f"unsupported currency {currency}. "
            f"Supported: {', '.join(CURRENCIES)}")
    return currency


def fetch_exchange_rate(currency: str, days: int) -> tuple:
    """Fetch representative exchange rates for a currency from the BOI API."""
    currency = _validated(currency)

    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    url = (f"{EXR_ENDPOINT}/RER_{currency}_ILS"
           f"?startPeriod={start_date}&endPeriod={end_date}")

    print(f"Fetching {currency} representative rate from the Bank of Israel...")
    print()
    return parse_sdmx(fetch_url(url), url)


def fetch_latest_exchange_rate(currency: str) -> tuple:
    """Fetch only the most recently published rate, ignoring calendar gaps.

    lastNObservations is the correct primitive here. Do NOT use lastNPeriods:
    the BOI server accepts it, returns HTTP 200, and silently ignores it,
    handing back the entire series back to 1948.
    """
    currency = _validated(currency)
    url = f"{EXR_ENDPOINT}/RER_{currency}_ILS?lastNObservations=1"
    return parse_sdmx(fetch_url(url), url)


def fetch_interest_rate(days: int) -> tuple:
    """Fetch the Bank of Israel policy rate (ריבית בנק ישראל) from BR."""
    start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    url = f"{BR_SERIES}?startPeriod={start_date}"
    print("Fetching the Bank of Israel policy rate...")
    print()
    return parse_sdmx(fetch_url(url), url)


def fetch_cpi(last: int) -> list:
    """Fetch the headline CBS Consumer Price Index (מדד המחירים לצרכן - כללי)."""
    url = CBS_CPI_URL.format(last=last)
    print("Fetching the CBS Consumer Price Index...")
    print()
    raw = fetch_url(url, accept="application/json")
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        die(f"{url} did not return JSON. This API answers HTTP 200 with an "
            f"HTML error page for an undefined path.")

    months = payload.get("month")
    if not months or not months[0].get("date"):
        die(f"{url} returned no CPI observations. This API answers HTTP 200 "
            f"with \"month\": null for an unknown index id, so the payload "
            f"must be validated rather than the status code.")

    series = months[0]
    rows = []
    for entry in series["date"]:
        base = entry.get("currBase") or {}
        rows.append({
            "year": entry.get("year"),
            "month": entry.get("month"),
            "index": base.get("value"),
            "base": base.get("baseDesc"),
            "monthly_pct": entry.get("percent"),
            "yearly_pct": entry.get("percentYear"),
        })
    return rows


def unit_label(attrs: dict) -> tuple:
    """Derive the quotation unit from the API's own UNIT_MULT attribute.

    UNIT_MULT is the power of ten the rate is quoted per: 0 means per 1 unit,
    2 means per 100 (the Japanese yen). Reading it beats a hardcoded table,
    which silently diverges if the BOI changes a quotation basis.
    """
    try:
        unit = 10 ** int(attrs.get("UNIT_MULT", 0))
    except (TypeError, ValueError):
        unit = 1
    return unit, (f" per {unit}" if unit > 1 else "")


def print_rates(currency: str, attrs: dict, observations: list) -> None:
    """Print exchange rates in a formatted table."""
    info = CURRENCIES.get(currency, {})
    unit, suffix = unit_label(attrs)

    print(f"  {info.get('name', currency)} ({info.get('hebrew', '')}){suffix}")
    print(f"  {'Date':<12} {'Rate (NIS)':<12}")
    print(f"  {'-' * 12} {'-' * 12}")
    for obs in observations[:10]:
        print(f"  {obs['date']:<12} {obs['value']:<12.4f}")

    latest = observations[0]
    print(f"\n  Latest ({latest['date']}): "
          f"{unit} {currency} = {latest['value']} NIS")
    if unit == 1:
        print(f"  Inverse: {1 / latest['value']:.4f} {currency} per shekel")


def print_interest(observations: list) -> None:
    """Print the current policy rate and the dates it changed."""
    latest = observations[0]
    print(f"  Bank of Israel policy rate (ריבית בנק ישראל)")
    print(f"  Current: {latest['value']}% (as published for {latest['date']})")
    print()
    print("  Recent changes:")
    ordered = list(reversed(observations))
    previous = None
    for obs in ordered:
        if previous is not None and obs["value"] != previous:
            print(f"    {obs['date']}  {previous}% -> {obs['value']}%")
        previous = obs["value"]
    if previous == ordered[0]["value"]:
        print(f"    no change in the fetched window "
              f"(from {ordered[0]['date']})")


def print_cpi(rows: list) -> None:
    """Print recent CPI readings."""
    print(f"  Consumer Price Index (מדד המחירים לצרכן - כללי)")
    print(f"  Base: {rows[0]['base']}")
    print()
    print(f"  {'Month':<10} {'Index':<10} {'Monthly %':<12} {'Yearly %':<10}")
    print(f"  {'-' * 10} {'-' * 10} {'-' * 12} {'-' * 10}")
    for row in rows:
        month = f"{row['year']}-{row['month']:02d}"
        print(f"  {month:<10} {str(row['index']):<10} "
              f"{str(row['monthly_pct']):<12} {str(row['yearly_pct']):<10}")


def print_example() -> None:
    """Print clearly-labelled sample output (no network access)."""
    print("=== EXAMPLE OUTPUT -- SAMPLE VALUES, NOT LIVE DATA ===")
    print()
    print("  US Dollar (דולר אמריקאי)")
    print(f"  {'Date':<12} {'Rate (NIS)':<12}")
    print(f"  {'-' * 12} {'-' * 12}")
    for date, rate in (("2026-08-26", 2.9720), ("2026-08-25", 2.9860),
                       ("2026-08-24", 2.9940), ("2026-08-21", 2.9910)):
        print(f"  {date:<12} {rate:<12.4f}")
    print()
    print("  Note the gap over Saturday and Sunday: the representative rate is")
    print("  published Monday to Friday only.")
    print()
    print("Run without --example for live data.")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Fetch Israeli economic data "
                    "(שליפת נתונים כלכליים מבנק ישראל ומהלמ\"ס)"
    )
    parser.add_argument("--currency",
                        help=f"Currency code for the representative exchange "
                             f"rate ({', '.join(list(CURRENCIES)[:6])}...)")
    parser.add_argument("--days", type=int, default=7,
                        help="Days of rate history (default: 7)")
    parser.add_argument("--latest", action="store_true",
                        help="With --currency, fetch only the most recently "
                             "published rate (skips weekend/holiday gaps)")
    parser.add_argument("--interest", action="store_true",
                        help="Fetch the BOI policy rate (ריבית בנק ישראל)")
    parser.add_argument("--interest-days", type=int, default=400,
                        help="Days of policy-rate history to scan for change "
                             "points (default: 400)")
    parser.add_argument("--cpi", action="store_true",
                        help="Fetch the CBS Consumer Price Index (מדד המחירים)")
    parser.add_argument("--cpi-last", type=int, default=6,
                        help="Months of CPI history to fetch (default: 6). "
                             "Raise it to reach the base month a contract "
                             "names; a 2019 lease needs roughly 90")
    parser.add_argument("--list-currencies", action="store_true",
                        help="List all supported currencies")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--example", action="store_true",
                        help="Show clearly-labelled sample output")

    args = parser.parse_args()

    if not any([args.currency, args.interest, args.cpi,
                args.list_currencies, args.example]):
        parser.print_help()
        sys.exit(1)

    if args.list_currencies:
        print("Supported currencies (מטבעות נתמכים):")
        print(f"  {'Code':<6} {'Name':<25} {'Hebrew':<20}")
        print(f"  {'-' * 6} {'-' * 25} {'-' * 20}")
        for code, info in CURRENCIES.items():
            print(f"  {code:<6} {info['name']:<25} {info['hebrew']:<20}")
        return

    if args.example:
        print_example()
        return

    if args.currency:
        if args.latest:
            attrs, observations = fetch_latest_exchange_rate(args.currency)
        else:
            attrs, observations = fetch_exchange_rate(args.currency, args.days)
        if args.json:
            unit, _ = unit_label(attrs)
            print(json.dumps({
                "currency": args.currency.upper(),
                "quoted_per": unit,
                "unit_measure": attrs.get("UNIT_MEASURE"),
                "data_type": attrs.get("DATA_TYPE"),
                "series_code": attrs.get("SERIES_CODE"),
                "observations": observations,
            }, indent=2, ensure_ascii=False))
        else:
            print_rates(args.currency.upper(), attrs, observations)

    if args.interest:
        _, observations = fetch_interest_rate(args.interest_days)
        if args.json:
            print(json.dumps(observations, indent=2, ensure_ascii=False))
        else:
            print_interest(observations)

    if args.cpi:
        rows = fetch_cpi(args.cpi_last)
        if args.json:
            print(json.dumps(rows, indent=2, ensure_ascii=False))
        else:
            print_cpi(rows)


if __name__ == "__main__":
    main()
