#!/usr/bin/env python3
"""Render an interactive diverging-bar chart of dual-listed gap % per pair.

OPTIONAL visualization step -- run it only when a chart helps the answer or the
user asks to see/visualize the gaps. The text analysis never depends on it.

Pipeline: provider (robust US + ".TA" fetch, USD/ILS rate) -> gap math ->
viz.render_gap_chart (self-contained interactive HTML). A pair whose Tel-Aviv
leg or price is unavailable from the free source is reported as skipped, never
fabricated. A pair whose two legs are from different sessions is charted but
marked NON-SYNCHRONOUS, because such a gap is an overnight move, not a live
dislocation. A ~100x leg ratio is treated as an agorot/shekel scaling error
and skipped. If the FX rate cannot be fetched and no --boi-rate is supplied, no
gap can be computed and the run exits with guidance rather than inventing a rate.

Usage:
    python scripts/chart.py --pairs CHKP,NICE,TEVA --out gaps.html
    python scripts/chart.py --pairs CHKP,NICE --boi-rate 3.65 --out gaps.html
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import provider
import viz

DEFAULT_THRESHOLD = 2.0
# A dual-listed ordinary and its US line should be within a few percent once
# converted; a factor near 100 means the TASE leg is still in agorot (scaling
# bug), so we refuse to chart it rather than show a fake ~100x gap.
SCALE_ERROR_HI = 50.0
SCALE_ERROR_LO = 0.02


def compute_pair(
    symbol: str, fx: float, ratio: float, threshold: float
) -> viz.PairGap:
    """Fetch both legs and derive the currency-adjusted gap.

    Returns a PairGap carrying both legs' as-of dates and a synchronous flag.
    Raises if either leg is missing, or if the magnitude looks like an
    agorot/shekel scaling error, so the caller skips the pair honestly instead
    of charting a fabricated or nonsensical number.
    """
    us_usd, us_date = provider.get_us_leg(symbol)
    tase_ils, tase_date, _currency = provider.get_tase_leg(symbol)
    us_in_ils = us_usd * fx * ratio
    if not us_in_ils:
        raise ValueError(f"{symbol}: US-implied shekel price is zero; cannot compare")
    scale = tase_ils / us_in_ils
    if scale > SCALE_ERROR_HI or scale < SCALE_ERROR_LO:
        raise ValueError(
            f"{symbol}: legs differ by ~{scale:.0f}x - probable agorot/shekel "
            f"scaling error; skipping rather than charting a fake gap"
        )
    gap_pct = (tase_ils - us_in_ils) / us_in_ils * 100.0
    return viz.PairGap(
        pair=symbol,
        gap_pct=round(gap_pct, 2),
        tase_ils=round(tase_ils, 2),
        us_in_ils=round(us_in_ils, 2),
        us_usd=round(us_usd, 2),
        flagged=abs(gap_pct) > threshold,
        us_date=us_date,
        tase_date=tase_date,
        synchronous=(us_date == tase_date),
    )


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Interactive dual-listed gap chart (diverging bars, HTML)."
    )
    ap.add_argument(
        "--pairs",
        required=True,
        help="comma-separated TASE symbols, e.g. CHKP,NICE,TEVA",
    )
    ap.add_argument(
        "--boi-rate",
        type=float,
        default=None,
        help="USD/ILS representative rate; omit to fetch USDILS=X live",
    )
    ap.add_argument(
        "--ratio",
        "--adr",
        dest="ratio",
        type=float,
        default=1.0,
        help="conversion ratio, ordinary shares per US line (1 for dual-listed "
        "ordinaries; only a true ADR differs, per its F-6)",
    )
    ap.add_argument(
        "--threshold",
        type=float,
        default=DEFAULT_THRESHOLD,
        help="abs(gap%%) that flags a pair (default 2.0)",
    )
    ap.add_argument("--out", default="dual-listed-gaps.html")
    a = ap.parse_args()

    symbols = [s.strip().upper() for s in a.pairs.split(",") if s.strip()]
    if not symbols:
        print("no pairs given", file=sys.stderr)
        return 2

    try:
        fx, fx_label = provider.get_fx_usdils(a.boi_rate)
    except Exception as exc:  # FX is shared: without it NO gap can be computed
        print(
            f"USD/ILS rate unavailable ({exc}); pass --boi-rate to proceed",
            file=sys.stderr,
        )
        return 1

    pairs: list[viz.PairGap] = []
    unavailable: list[viz.Unavailable] = []
    dates: list[str] = []
    for sym in symbols:
        try:
            pair = compute_pair(sym, fx, a.ratio, a.threshold)
            pairs.append(pair)
            dates.append(max(pair.us_date, pair.tase_date))
        except Exception as exc:  # per-pair: skip honestly, never fabricate
            unavailable.append(viz.Unavailable(pair=sym, reason=str(exc)[:160]))

    if not pairs:
        print("no pair had both legs available; nothing to chart", file=sys.stderr)
        for u in unavailable:
            print(f"  {u.pair}: {u.reason}", file=sys.stderr)
        return 1

    nonsync = [p for p in pairs if not p.synchronous]
    for p in nonsync:  # surface the caveat on the CLI too, not only in the chart
        print(
            f"  note: {p.pair} legs are non-synchronous "
            f"(TASE {p.tase_date} vs US {p.us_date}); gap is an overnight move, "
            f"not a live dislocation",
            file=sys.stderr,
        )

    as_of = max(dates)
    doc = viz.render_gap_chart(pairs, unavailable, fx, fx_label, a.threshold, as_of)
    Path(a.out).write_text(doc, encoding="utf-8")
    print(
        f"wrote {a.out} ({len(doc)} bytes, {len(pairs)} pairs charted, "
        f"{len(nonsync)} non-synchronous, {len(unavailable)} unavailable, "
        f"as of {as_of})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
