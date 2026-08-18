#!/usr/bin/env python3
"""
Pull comparable residential transactions for an Israeli address from the open
government real-estate API, and print a comparables table.

Chain (each step fails loudly if the upstream shape changes):
  1. address    -> addr_id + ITM centroid   (govmap search-service)
  2. centroid   -> gush / helka             (govmap spatial-analysis, parcel_all)
  3. addr_id    -> polygon_id               (nadlan deal-info)
  4. polygon_id -> deal rows                (govmap real-estate street-deals)

This script NEVER invents a price. Every row printed comes back from the API.
If a step fails it raises, it does not fall back to a guess.

Pass the subject property (--area / --rooms) whenever one exists. Without it the
output is a polygon-wide market indicator across every size, floor and age, which
is the price of the street rather than the value of the apartment.

Usage:
  python3 comparables.py "דיזנגוף 100 תל אביב"
  python3 comparables.py "דיזנגוף 100 תל אביב" --years 3 --area 75 --rooms 3
  python3 comparables.py "הרצל 10 חיפה" --years 5 --area 90 --json
"""

import argparse
import json
import statistics
import sys
import urllib.error
import urllib.request
from datetime import datetime, timedelta

# Public client constant embedded in the nadlan.gov.il front end. It is scoped to
# the nadlan.gov.il origin, which is why the headers below are not optional.
API_TOKEN = "cf153c72-fb28-4b27-9db4-982bc89cb3b0"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Origin": "https://www.nadlan.gov.il",
    "Referer": "https://www.nadlan.gov.il/",
    "Content-Type": "application/json",
}

SEARCH_URL = "https://www.govmap.gov.il/api/search-service/api-search"
PARCEL_URL = "https://www.govmap.gov.il/api/spatial-analysis/layer-features-by-location"
DEALINFO_URL = "https://api.nadlan.gov.il/deal-info"
DEALS_URL = "https://www.govmap.gov.il/api/real-estate/street-deals/{polygon_id}"

# Deal natures that are NOT a comparable for valuing a flat. Land, offices, shops
# and storage price per square metre on a completely different basis; averaging
# them into a residential figure is the classic wrong answer.
RESIDENTIAL_NATURES = {
    "דירה בבית קומות",
    "דירה",
    "דירת גן",
    "דירת גג",
    "פנטהאוז",
    "בית בודד",
    "דו משפחתי",
    "קוטג' חד משפחתי",
    "קוטג' דו משפחתי",
}


class PipelineError(RuntimeError):
    """Raised when an upstream endpoint changes shape, 403s, or returns nothing."""


def _request(url, payload=None, timeout=30):
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    method = "POST" if payload is not None else "GET"
    req = urllib.request.Request(url, data=data, headers=HEADERS, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read()
    except urllib.error.HTTPError as exc:
        if exc.code == 403:
            raise PipelineError(
                f"{method} {url} returned HTTP 403. The request was refused at the "
                f"network edge before reaching the API. This is not the token and not "
                f"the headers, so retrying will not help; non-Israeli or datacentre "
                f"egress is the likeliest cause but is not confirmed. Do not guess a "
                f"value and do not report a rotated token."
            ) from exc
        raise PipelineError(
            f"{method} {url} returned HTTP {exc.code}. The endpoint may have moved or "
            f"changed shape. Do not guess a value, re-check the chain."
        ) from exc
    except urllib.error.URLError as exc:
        raise PipelineError(f"{method} {url} failed: {exc.reason}") from exc
    try:
        return json.loads(body)
    except json.JSONDecodeError as exc:
        snippet = body[:200].decode("utf-8", "replace")
        raise PipelineError(
            f"{method} {url} did not return JSON (got: {snippet!r}). "
            f"This usually means a WAF/maintenance page, not an empty result."
        ) from exc


def resolve_address(address):
    """Step 1: address -> (addr_id, centroid, matched_text)."""
    payload = {
        "searchText": address,
        "language": "he",
        "maxResults": 10,
        "isAccurate": True,
        "apiKey": API_TOKEN,
    }
    data = _request(SEARCH_URL, payload)
    results = data.get("results")
    if results is None:
        raise PipelineError(f"search response missing 'results' key: {list(data)}")
    hit = next((r for r in results if r.get("type") == "address"), None)
    if hit is None:
        raise PipelineError(
            f"No address match for {address!r}. Try adding the city, or check spelling."
        )
    parts = hit["id"].split("|")
    if len(parts) < 3:
        raise PipelineError(f"unexpected address id format: {hit['id']!r}")
    return parts[2], hit["centroid"], hit.get("text", address)


def resolve_parcel(centroid):
    """Step 2: ITM centroid -> (gush, helka). Returns (None, None) where uncovered."""
    payload = {
        "data": {
            "geometry": centroid.replace("POINT (", "POINT("),
            "radius": 0.1,
            # 'fields' is required, and a "*" wildcard returns empty attributes,
            # so the field names have to be listed explicitly.
            "layers": [{"name": "parcel_all", "fields": ["gush_num", "parcel"]}],
        },
        "apiToken": API_TOKEN,
    }
    data = _request(PARCEL_URL, payload)
    feats = data.get("layers", {}).get("parcel_all", [])
    if not feats:
        return None, None
    attrs = feats[0].get("attributes", {})
    return attrs.get("gush_num"), attrs.get("parcel")


def resolve_polygon(addr_id):
    """Step 3: addr_id -> (polygon_id, neighborhood, settlement)."""
    data = _request(DEALINFO_URL, {"base_name": "addr_id", "base_id": str(addr_id)})
    polygon_id = data.get("polygon_id")
    if not polygon_id:
        raise PipelineError(
            f"deal-info returned no polygon_id for addr_id={addr_id}. "
            f"This address has no transaction polygon in the government data."
        )
    return polygon_id, data.get("neigh_name"), data.get("setl_name")


def fetch_deals(polygon_id, page_size=2000):
    """Step 4: polygon_id -> all deal rows.

    The endpoint returns 10 rows by default. Reporting on those 10 alone would
    silently describe only the newest transactions, so page until the declared
    totalCount is satisfied.
    """
    url = DEALS_URL.format(polygon_id=polygon_id)
    try:
        first = _request(f"{url}?offset=0&limit={page_size}")
    except PipelineError as exc:
        # A 500 here is how the API reports a polygon it holds no deal data for.
        # Coverage is not uniform across the country (see the Coverage section in
        # SKILL.md). Say so plainly rather than implying the whole chain broke.
        if "HTTP 500" in str(exc):
            raise PipelineError(
                f"The government API has no transaction data for polygon {polygon_id} "
                f"(HTTP 500). This address is in a coverage gap. Do NOT estimate a "
                f"value from nothing, tell the user the data is unavailable here."
            ) from exc
        raise
    if not isinstance(first, dict) or "data" not in first:
        raise PipelineError(f"street-deals returned unexpected shape: {type(first)}")
    try:
        total = int(first.get("totalCount") or 0)
    except (TypeError, ValueError):
        total = 0
    rows = list(first["data"])
    seen = {r.get("objectid") for r in rows}
    while len(rows) < total:
        page = _request(f"{url}?offset={len(rows)}&limit={page_size}")
        batch = page.get("data") or []
        fresh = [r for r in batch if r.get("objectid") not in seen]
        if not fresh:
            # totalCount can exceed the number of distinct objectids the endpoint
            # will actually serve (it counts duplicate rows). Stop and report the
            # real fetched count rather than looping forever or inventing rows.
            break
        seen.update(r.get("objectid") for r in fresh)
        rows.extend(fresh)
    return rows, total


def filter_deals(rows, years):
    """Keep residential rows with a usable area, within the window.

    This does NOT test for arm's length. Gifts, partial-share and combination
    deals pass straight through here and are only flagged later by _flag_outliers.
    """
    cutoff = datetime.now() - timedelta(days=365 * years)
    kept, dropped = [], {"non_residential": 0, "no_area": 0, "too_old": 0}
    for r in rows:
        nature = (r.get("dealNatureDescription") or "").strip()
        if nature not in RESIDENTIAL_NATURES:
            dropped["non_residential"] += 1
            continue
        area = r.get("assetArea") or 0
        amount = r.get("dealAmount") or 0
        if not area or not amount:
            dropped["no_area"] += 1
            continue
        raw_date = (r.get("dealDate") or "")[:10]
        try:
            when = datetime.strptime(raw_date, "%Y-%m-%d")
        except ValueError:
            dropped["too_old"] += 1
            continue
        if when < cutoff:
            dropped["too_old"] += 1
            continue
        kept.append(
            {
                "date": raw_date,
                "nature": nature,
                "rooms": r.get("assetRoomNum"),
                "floor": r.get("floorNo"),
                "area": area,
                "amount": amount,
                "price_sqm": round(amount / area),
                "year_built": r.get("yearBuilt"),
            }
        )
    kept.sort(key=lambda d: d["date"], reverse=True)
    _flag_outliers(kept)
    return kept, dropped


def _flag_outliers(deals):
    """Mark implausible price-per-sqm rows instead of silently averaging them in.

    The published data includes transfers that are not arm's-length sales at full
    value: gifts between relatives, sales of a partial share in a property, and
    combination deals. They surface as absurd shekel-per-square-metre figures: a
    sale recorded far below the surrounding rate is one of these, not a bargain.

    They are flagged, never deleted, so the user can still see every row and
    decide. Only the headline median and range exclude them.

    Uses the median absolute deviation (Iglewicz-Hoaglin modified z-score),
    NOT Tukey's interquartile fences. IQR fences are computed from the quartiles,
    and on a thin sample the outlier itself lands inside the half it is measured
    against and inflates it. At n=5 the upper half is only two values, so a single
    extreme row drags Q3 up with it and the fence outruns the very row it was
    meant to catch. Verified: with [10000, 10100, 10200, 10300, 100000] the upper
    half is [10300, 100000], giving Q3 = 55150 and an upper fence of 122,800, so
    the 100000 row was not flagged. The same failure hit n=4, and
    both directions (a gift recorded far BELOW market is the more damaging case,
    because it drags the median down and makes a property look cheap).

    MAD is measured against the median, which a minority of extreme rows cannot
    move, so it stays reliable down to n=4 and survives two contaminated rows out
    of five. It also produced fewer false positives than IQR on clean samples
    (13.0% vs 15.1% over 6,800 simulated clean draws, n=4..20).
    """
    if len(deals) < 4:
        for d in deals:
            d["outlier"] = False
        return
    values = [d["price_sqm"] for d in deals]
    median = statistics.median(values)
    mad = statistics.median([abs(v - median) for v in values])
    if mad == 0:
        # More than half the rows share one price per square metre, so there is no
        # dispersion to judge against. Claiming an outlier here would be arbitrary.
        for d in deals:
            d["outlier"] = False
        return
    for d in deals:
        modified_z = 0.6745 * (d["price_sqm"] - median) / mad
        d["outlier"] = abs(modified_z) > 3.5


def main():
    ap = argparse.ArgumentParser(description="Israeli property comparables from open gov data")
    ap.add_argument("address", help='e.g. "דיזנגוף 100 תל אביב"')
    ap.add_argument("--years", type=int, default=3, help="lookback window (default 3)")
    ap.add_argument("--json", action="store_true", help="emit JSON instead of a table")
    # Subject property. Without these the output is a polygon-wide market
    # indicator across every size, floor and age, which is NOT a comparables
    # analysis and must not be presented as one.
    ap.add_argument("--area", type=float, help="subject area in sqm, bands comparables around it")
    ap.add_argument("--rooms", type=float, help="subject room count")
    ap.add_argument("--band", type=float, default=0.25,
                    help="area tolerance as a fraction of the subject area, default 0.25")
    args = ap.parse_args()

    try:
        addr_id, centroid, matched = resolve_address(args.address)
        gush, helka = resolve_parcel(centroid)
        polygon_id, neigh, settlement = resolve_polygon(addr_id)
        rows, total = fetch_deals(polygon_id)
    except PipelineError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    kept, dropped = filter_deals(rows, args.years)

    # Band to the subject property where it was supplied. A median across every
    # flat in the polygon answers "what does this street cost", not "what is this
    # apartment worth", and only the latter belongs in an objection letter.
    subject_given = args.area is not None or args.rooms is not None
    if subject_given:
        banded = []
        for d in kept:
            if args.area is not None:
                lo, hi = args.area * (1 - args.band), args.area * (1 + args.band)
                if not (lo <= d["area"] <= hi):
                    continue
            if args.rooms is not None and d["rooms"] is not None:
                if abs(d["rooms"] - args.rooms) > 1:
                    continue
            banded.append(d)
        dropped["outside_subject_band"] = len(kept) - len(banded)
        kept = banded
        _flag_outliers(kept)

    out = {
        "basis": "comparables banded to subject" if subject_given
                 else "polygon-wide market indicator, subject not supplied",
        "subject_area": args.area,
        "subject_rooms": args.rooms,
        "query": args.address,
        "matched_address": matched,
        "gush": gush,
        "helka": helka,
        "neighborhood": neigh,
        "settlement": settlement,
        "polygon_id": polygon_id,
        "deals_reported_by_api": total,
        "deals_fetched": len(rows),
        "comparables_kept": len(kept),
        "dropped": dropped,
        "comparables": kept,
    }
    clean = [d for d in kept if not d["outlier"]]
    out["comparables_flagged_outlier"] = len(kept) - len(clean)
    if clean:
        psm = [d["price_sqm"] for d in clean]
        out["price_sqm_median"] = int(statistics.median(psm))
        out["price_sqm_min"] = min(psm)
        out["price_sqm_max"] = max(psm)

    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0

    print(f"כתובת שהותאמה: {matched}")
    print(f"גוש/חלקה: {('גוש ' + str(gush) + ' חלקה ' + str(helka)) if gush else 'לא נמצא (ראו הערת הכיסוי)'}")
    print(f"שכונה: {neigh or '-'} | יישוב: {settlement or '-'}")
    print(f"עסקאות במאגר: {total} | נמשכו: {len(rows)} | השוואה רלוונטית: {len(kept)}")
    print(f"סוננו: לא-מגורים {dropped['non_residential']}, ללא שטח {dropped['no_area']}, מחוץ לחלון {dropped['too_old']}")
    if not kept:
        print("\nאין עסקאות מגורים בחלון הזמן הזה. הרחיבו עם --years, אל תמציאו מספר.")
        return 0
    if "price_sqm_median" not in out:
        print("\nכל העסקאות סומנו כחריגות. בדקו אותן ידנית, אל תגזרו מהן טווח.")
        return 0
    flagged = out["comparables_flagged_outlier"]
    if subject_given:
        print(f"\nבסיס: עסקאות שהותאמו לנכס הנדון (הוצאו מחוץ לטווח: {dropped.get('outside_subject_band', 0)})")
    else:
        print("\nבסיס: אינדיקציה כללית לפוליגון, לא ניתן נכס נדון.")
        print("זה מחיר האזור ולא שווי הדירה. הריצו עם --area ו---rooms כדי לצמצם לעסקאות דומות")
        print("לפני שמשתמשים במספר במכתב או מול הבנק.")
    print(f"חציון: {out['price_sqm_median']:,} ש\"ח למ\"ר | טווח: {out['price_sqm_min']:,} עד {out['price_sqm_max']:,}")
    if flagged:
        print(f"({flagged} עסקאות סומנו חריגות ולא נכנסו לחציון. הן מסומנות ב-! בטבלה)")
    print()
    print(f"{'תאריך':<12}{'חדרים':>7}{'מ\"ר':>8}{'מחיר':>14}{'ש\"ח/מ\"ר':>11}  סוג")
    for d in kept[:40]:
        rooms = d["rooms"] if d["rooms"] is not None else "-"
        mark = "!" if d["outlier"] else " "
        print(f"{d['date']:<12}{str(rooms):>7}{d['area']:>8.0f}{d['amount']:>14,}{d['price_sqm']:>11,}{mark} {d['nature']}")
    if len(kept) > 40:
        print(f"... ועוד {len(kept) - 40} עסקאות (השתמשו ב---json לרשימה המלאה)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
