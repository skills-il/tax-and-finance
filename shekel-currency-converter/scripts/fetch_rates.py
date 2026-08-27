#!/usr/bin/env python3
"""Fetch and convert currencies using Bank of Israel exchange rates.

Current rates come from the live Bank of Israel JSON endpoint. Historical
(tax-date) rates come from the Bank of Israel SDMX EXR series, because the
JSON endpoint's ?date= parameter is ignored and always returns the most
recently published rate. Note that "most recently published" is not the same as
"today": the endpoint keeps serving the previous publication until the next one
lands, so before the daily publication it returns the PREVIOUS business day's
rate. The date reported for a conversion is therefore always taken from the
endpoint's own lastUpdate field, never from the system clock.

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


def fetch_current_rates() -> tuple[dict, str]:
    """Fetch current representative rates from the Bank of Israel JSON endpoint.

    Returns:
        Tuple of (rates, rate_date). rates maps currency code to
        (rate, unit, change_pct); change_pct is the percentage daily move, not
        an absolute NIS delta. rate_date is the date the returned rates were
        actually published, taken from the endpoint's own lastUpdate field.

        Do NOT substitute today's date for rate_date. The endpoint keeps serving
        the previous publication until the next one lands (Mon-Thu soon after
        15:15, Fri soon after 12:15, Israel time), so before today's publication
        it returns YESTERDAY's rate. The shaar yatzig is date-attributed for tax,
        so labelling it with today's date misstates which day's rate was used.

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
    rate_date = None
    for entry in data.get("exchangeRates", []):
        code = entry.get("key")
        rate = entry.get("currentExchangeRate")
        unit = entry.get("unit", 1)
        change = entry.get("currentChange", 0.0)
        if code and rate:
            rates[code] = (float(rate), int(unit), float(change))
            stamp = entry.get("lastUpdate")
            if stamp and (rate_date is None or stamp[:10] > rate_date):
                rate_date = stamp[:10]
    if not rates:
        raise RateFetchError(
            "Bank of Israel endpoint returned no usable rates."
        )
    if rate_date is None:
        raise RateFetchError(
            "Bank of Israel endpoint returned rates with no lastUpdate stamp, "
            "so the publication date cannot be established. Refusing to emit a "
            "tax-stamped rate with an unknown date."
        )
    return rates, rate_date


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
        "USD": (2.972, 1, -0.47),
        "EUR": (3.4685, 1, -0.4),
        "GBP": (4.0511, 1, -0.48),
        "JPY": (1.8684, 100, -0.33),
        "CHF": (3.697, 1, -0.59),
        "CAD": (2.1441, 1, -0.48),
        "AUD": (2.1357, 1, -0.01),
    }


def _sig_figs(value: float) -> int:
    """Count the significant figures the BOI actually published for a rate."""
    text = f"{abs(value):.10f}".rstrip("0").lstrip("0.")
    return len(text.lstrip("0")) or 1


def _fmt_rate(value: float) -> str:
    """Format a per-unit rate without collapsing a small rate to zero.

    A fixed 4-decimal format prints the Lebanese pound as "0.0000", which reads
    as a zero rate on a line a user may copy into a filing. Widen the decimal
    places until the value is non-zero. This is a DISPLAY fix only: it cannot
    add precision the Bank of Israel did not publish, which is what
    _precision_warning exists to say out loud.
    """
    for places in (4, 6, 8, 10):
        text = f"{value:.{places}f}"
        if float(text) != 0.0:
            return text
    return f"{value:.10g}"


def _precision_warning(published_value: float) -> Optional[str]:
    """Warn when the published rate carries too few significant figures.

    The Bank of Israel publishes some low-value currencies at very coarse
    precision. The Lebanese pound, for example, is published as 0.0003 per 10
    units: a single significant figure, which bounds any converted amount to
    roughly plus or minus 17 percent. That published figure IS the official
    representative rate, so it is not wrong to use it, but a converted total
    printed to the agora should not be presented as if it were precise.
    """
    figures = _sig_figs(published_value)
    if figures >= 3:
        return None
    return (
        f"  WARNING: the Bank of Israel publishes this rate to only {figures} "
        f"significant figure(s) ({published_value:g}),\n"
        "        so the converted total carries a wide margin and must not be\n"
        "        relied on to the agora. It is the official published rate, but\n"
        "        confirm the figure with the Bank of Israel before filing."
    )


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
        return (result, rate / unit, f"1 {to_currency} = {_fmt_rate(rate/unit)} ILS")

    if to_currency == "ILS" and from_currency in rates:
        rate, unit, _ = rates[from_currency]
        result = amount * rate / unit
        return (result, rate / unit, f"1 {from_currency} = {_fmt_rate(rate/unit)} ILS")

    # Cross-currency via ILS
    if from_currency in rates and to_currency in rates:
        from_rate, from_unit, _ = rates[from_currency]
        to_rate, to_unit, _ = rates[to_currency]
        nis_amount = amount * from_rate / from_unit
        result = nis_amount / to_rate * to_unit
        cross_rate = (from_rate / from_unit) / (to_rate / to_unit)
        return (
            result,
            cross_rate,
            f"1 {from_currency} = {_fmt_rate(cross_rate)} {to_currency} "
            "(DERIVED from two Bank of Israel shekel rates; the Bank of Israel "
            "publishes no direct rate for this pair)",
        )

    return None


def build_dated_rates(
    from_currency: str, to_currency: str, target_date: str
) -> tuple[dict, str]:
    """Build a rates dict for a specific historical date using SDMX.

    Returns the rates dict plus the actual publication date used (which may be
    earlier than target_date if the requested day had no publication).
    """
    rates = {"ILS": (1.0, 1, 0.0)}
    resolved = {}
    for cur in sorted({from_currency.upper(), to_currency.upper()}):
        if cur == "ILS":
            continue
        hist = fetch_historical_rate(cur, target_date)
        if hist is None:
            continue
        rate, unit, when = hist
        rates[cur] = (rate, unit, 0.0)
        resolved[cur] = when
    if not resolved:
        return rates, target_date
    # Both legs must resolve to the SAME publication day. Picking whichever leg
    # happened to iterate last would stamp a nondeterministic date on a
    # cross-currency conversion, which is the exact date-misattribution this
    # skill exists to prevent.
    distinct = sorted(set(resolved.values()))
    if len(distinct) > 1:
        detail = ", ".join(f"{c} resolved to {d}" for c, d in sorted(resolved.items()))
        raise RateFetchError(
            "The two currencies resolved to different publication dates "
            f"({detail}). Refusing to stamp one date on a conversion built from "
            "two different days. Request each leg against the shekel separately."
        )
    return rates, distinct[0]


def format_result(
    amount: float,
    from_currency: str,
    to_currency: str,
    result: float,
    description: str,
    rate_date: Optional[str] = None,
    is_sample: bool = False,
    published_value: Optional[float] = None,
) -> str:
    """Format conversion result for display."""
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
    if rate_date is None:
        raise ValueError("rate_date is required: a shaar yatzig must carry the "
                         "date it was actually published, never today's date.")
    date_str = rate_date
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
        "  NOTE: This is the rate PUBLISHED on the date shown. If you need a rate",
        "        for a later date, it may not be published yet: the Bank of Israel",
        "        publishes once per business day and this endpoint keeps serving the",
        "        previous publication until the next one lands.",
        "  NOTE: Import VAT on GOODS uses the weekly customs rate published by the",
        "        Tax Authority, NOT this rate. Read the published customs rate; do",
        "        not derive it. Imported SERVICES (reverse-charge VAT) DO use",
        "        this plain representative rate, with no customs uplift.",
    ]
    if published_value is not None:
        warning = _precision_warning(published_value)
        if warning:
            lines.extend(["", warning])
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
            rates, used_date = fetch_current_rates()
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
        published_value=None if is_sample else _rate_used,
    ))


if __name__ == "__main__":
    main()
