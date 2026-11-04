#!/usr/bin/env python3
"""Fetch TASE (Tel Aviv Stock Exchange) index data from the TASE Data Hub API.

What it does:
  --list-indices   GET /api/v2/basic-indices/indices-list (all index IDs and names)
  --index KEY      GET /api/v2/basic-indices/index-components-basic for one index
                   (constituents and weights on a trade date)
  --stock NUMBER   prints the official market.tase.co.il page for a security number,
                   so the company name can be read back before the number is used
  --example        offline demonstration data (no key, no network)

What it does NOT do: it does not read Maya filings (use https://maya.tase.co.il) and it
does not fetch live stock quotes.

The live calls need a TASE Data Hub API key registered for the "Indices - Basic"
product (sign in at https://datahubapi.tase.co.il). The key is sent in the `apikey`
HTTP header, the same way the skills-il tase-mcp server sends it. The response JSON
is printed as returned; field names are TASE's, not this script's.

Usage:
    python scripts/fetch_tase_data.py --list-indices
    python scripts/fetch_tase_data.py --index TA35 [--date 2026-11-03] [--lang en-US]
    python scripts/fetch_tase_data.py --stock 662577
    python scripts/fetch_tase_data.py --example
"""

import os
import sys
import json
import argparse
from datetime import date, datetime
from typing import Optional
from urllib.parse import urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError


# Data Hub gateway. Override with TASE_API_BASE if TASE moves it.
TASE_API_BASE = os.environ.get("TASE_API_BASE", "https://datawise.tase.co.il").rstrip("/")
INDICES_LIST_PATH = "/api/v2/basic-indices/indices-list"
INDEX_COMPONENTS_PATH = "/api/v2/basic-indices/index-components-basic"
SECURITY_PAGE = "https://market.tase.co.il/en/market_data/security/{}"

# Index identifiers (TASE index codes). New indices appear over time (for example
# TA-Technology 35 and TA-Israel Energy, launched February 2026): use --list-indices
# for any index not listed here, and pass its numeric ID with --index-id.
INDICES = {
    "TA35": {"id": 142, "name": "TA-35", "hebrew": 'ת"א-35'},
    "TA125": {"id": 137, "name": "TA-125", "hebrew": 'ת"א-125'},
    "TA90": {"id": 143, "name": "TA-90", "hebrew": 'ת"א-90'},
    "TABANK": {"id": 194, "name": "TA-Bank", "hebrew": 'ת"א-בנקים'},
    "TAREAL": {"id": 149, "name": "TA-RealEstate", "hebrew": 'ת"א-נדל"ן'},
    "TATECH": {"id": 169, "name": "TA-Technology", "hebrew": 'ת"א-טכנולוגיה'},
}

# Well-known dual-listed Israeli companies (TASE + NASDAQ/NYSE), keyed by US ticker.
# TASE security numbers are deliberately NOT hardcoded: the dual-listed set changes
# through mergers and take-privates (Sapiens stopped trading on both exchanges in
# December 2025 after being taken private, so it is not listed here). Check Point is
# not listed either: it trades only in the US. Palo Alto Networks trades on TASE under
# the symbol CYBR, not under its Nasdaq ticker PANW.
DUAL_LISTED_US_TICKERS = {
    "NICE": "NICE Ltd",
    "TEVA": "Teva Pharmaceutical",
    "ICL": "ICL Group",
    "PANW": "Palo Alto Networks (TASE symbol CYBR)",
}


def fetch_json(path: str, params: Optional[dict], lang: str) -> object:
    """GET a Data Hub endpoint and return the parsed JSON body."""
    api_key = os.environ.get("TASE_API_KEY")
    if not api_key:
        print("Error: TASE_API_KEY environment variable is required for live data.")
        print("Get a key at https://datahubapi.tase.co.il (register it for the product you call).")
        print("For a demonstration, use the --example flag.")
        sys.exit(1)
    url = TASE_API_BASE + path
    if params:
        url += "?" + urlencode(params)
    req = Request(url, headers={
        "accept": "application/json",
        "accept-language": lang,
        "apikey": api_key,
    })
    try:
        with urlopen(req, timeout=20) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as err:
        hint = {
            401: "the key was rejected (check TASE_API_KEY)",
            403: "the key is not registered for this product, or the path was rejected",
            429: "rate limit exceeded (10 requests per 2 seconds); wait and retry",
        }.get(err.code, "see the product page in the Developers' Portal")
        print(f"Error: HTTP {err.code} from {path}: {hint}.")
        sys.exit(1)
    except (URLError, TimeoutError) as err:
        print(f"Error: could not reach {TASE_API_BASE} ({err}).")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: {path} did not return JSON.")
        sys.exit(1)


def generate_example() -> dict:
    """Offline example. Security numbers are real; weights are deliberately omitted
    because they change at every index update. Fetch them with --index TA35."""
    return {
        "index": "TA-35",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "components": [
            {"name": "Bank Hapoalim", "symbol": "POLI", "securities_no": "662577", "weight_pct": None},
            {"name": "Bank Leumi", "symbol": "LUMI", "securities_no": "604611", "weight_pct": None},
            {"name": "Bank Discount", "symbol": "DSCT", "securities_no": "691212", "weight_pct": None},
        ],
        "note": ("Example data for demonstration only. Use --index TA35 with an API key "
                 "for the real constituents and weights."),
    }


def main():
    parser = argparse.ArgumentParser(description="Fetch TASE index data from the TASE Data Hub API")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--list-indices", action="store_true", help="List all TASE indices with their IDs")
    group.add_argument("--index", choices=list(INDICES.keys()), help="Index constituents and weights")
    group.add_argument("--index-id", type=int, help="Same as --index, by numeric TASE index ID")
    group.add_argument("--stock", help="Show the official page for a TASE security number")
    group.add_argument("--example", action="store_true", help="Show offline example TA-35 data")
    parser.add_argument("--date", help="Trade date YYYY-MM-DD for --index (default: today; "
                        "use the last trading day, TASE trades Monday-Friday)")
    parser.add_argument("--lang", choices=["he-IL", "en-US"], default="he-IL", help="Response language")
    args = parser.parse_args()

    if args.example:
        print(json.dumps(generate_example(), indent=2, ensure_ascii=False))
        return

    if args.stock:
        if not args.stock.isdigit():
            print("Error: --stock takes a numeric TASE security number, e.g. 662577.")
            sys.exit(1)
        print(json.dumps({
            "securities_number": args.stock,
            "official_page": SECURITY_PAGE.format(args.stock),
            "note": "Open the page and read back the company name before using the number.",
        }, indent=2, ensure_ascii=False))
        return

    if args.list_indices:
        print(json.dumps(fetch_json(INDICES_LIST_PATH, None, args.lang), indent=2, ensure_ascii=False))
        return

    trade_date = args.date or date.today().isoformat()
    try:
        datetime.strptime(trade_date, "%Y-%m-%d")
    except ValueError:
        print("Error: --date must be YYYY-MM-DD.")
        sys.exit(1)
    index_id = args.index_id if args.index_id is not None else INDICES[args.index]["id"]
    data = fetch_json(INDEX_COMPONENTS_PATH, {"IndexId": index_id, "TradeDate": trade_date}, args.lang)
    print(json.dumps({"index_id": index_id, "trade_date": trade_date, "response": data},
                     indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
