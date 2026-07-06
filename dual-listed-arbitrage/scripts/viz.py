#!/usr/bin/env python3
"""Self-contained interactive HTML/SVG diverging-bar chart (no third-party deps).

Renders one horizontal bar per dual-listed pair: the currency-adjusted gap %
between the Tel-Aviv and US legs. This is polarity data, so it uses the DIVERGING
convention -- premium (TASE above US, positive) in blue (--s1), discount (TASE
below US, negative) in red (--bad), both measured from a neutral gray zero
baseline at the midpoint. Not two arbitrary categorical hues.

Ships hover crosshair + tooltip, a table view, and a light/dark toggle. Colours
come from the data-viz reference palette (colour-blind validated). Dynamic tooltip
text is built with DOM textContent -- never innerHTML -- so pair names can never
inject markup.

This is the OPTIONAL visualization layer -- the skill renders it only when a
chart helps or the user asks; the text answer never depends on it.
"""

from __future__ import annotations

import html
import json
from dataclasses import dataclass
from typing import Optional

# Data-viz reference palette (roles only; light + dark are both selected sets).
PAL = {
    "light": {
        "surface": "#fcfcfb",
        "page": "#f9f9f7",
        "primary": "#0b0b0b",
        "secondary": "#52514e",
        "muted": "#898781",
        "grid": "#e1e0d9",
        "axis": "#c3c2b7",
        "s1": "#2a78d6",
        "s2": "#1baf7a",
        "s3": "#eda100",
        "s4": "#4a3aa7",
        "good": "#006300",
        "bad": "#d03b3b",
        "bandfill": "#e1e0d9",
    },
    "dark": {
        "surface": "#1a1a19",
        "page": "#0d0d0d",
        "primary": "#ffffff",
        "secondary": "#c3c2b7",
        "muted": "#898781",
        "grid": "#2c2c2a",
        "axis": "#383835",
        "s1": "#3987e5",
        "s2": "#199e70",
        "s3": "#c98500",
        "s4": "#9085e9",
        "good": "#0ca30c",
        "bad": "#d03b3b",
        "bandfill": "#2c2c2a",
    },
}

W, ML, MR, MT, MB = 880, 108, 64, 60, 46
ROW_H, BAR_H = 34, 16
PX0, PX1 = ML, W - MR
CX = (PX0 + PX1) / 2  # zero baseline (midpoint)


@dataclass(frozen=True)
class PairGap:
    """One charted pair: currency-adjusted gap and the legs it came from.

    us_date / tase_date are each leg's as-of date; synchronous is False when they
    differ, meaning the gap is an overnight move rather than a live dislocation.
    """

    pair: str
    gap_pct: float
    tase_ils: float
    us_in_ils: float
    us_usd: float
    flagged: bool
    us_date: str = ""
    tase_date: str = ""
    synchronous: bool = True


@dataclass(frozen=True)
class Unavailable:
    """A pair skipped because a leg or price was absent from the free source."""

    pair: str
    reason: str


def _fmt(v: Optional[float], nd: int = 2) -> str:
    return "-" if v is None else f"{v:,.{nd}f}"


def render_gap_chart(
    pairs: list[PairGap],
    unavailable: list[Unavailable],
    fx: float,
    fx_label: str,
    threshold: float,
    as_of: str,
) -> str:
    n = len(pairs)
    H = MT + n * ROW_H + MB

    # symmetric diverging scale: domain [-maxabs, +maxabs] so 0 stays centred
    maxabs = max([abs(p.gap_pct) for p in pairs] + [threshold, 1.0]) * 1.18

    def x_of(g: float) -> float:
        return CX + (g / maxabs) * (PX1 - CX)

    # vertical gridlines + x labels (percent), zero baseline emphasised
    grid, xlab = [], []
    for t in range(5):
        val = -maxabs + (2 * maxabs) * t / 4
        x = x_of(val)
        cls = "zero" if abs(val) < 1e-9 else "grid"
        grid.append(
            f'<line x1="{x:.1f}" y1="{MT}" x2="{x:.1f}" y2="{H - MB}" class="{cls}"/>'
        )
        lab = "0" if abs(val) < 1e-9 else f"{val:+.1f}%"
        xlab.append(f'<text x="{x:.1f}" y="{H - MB + 16}" class="xtick">{lab}</text>')

    # recessive threshold markers (the flag boundary) if inside the plot
    tmarks = []
    for tv in (threshold, -threshold):
        if 0 < abs(tv) < maxabs:
            x = x_of(tv)
            tmarks.append(
                f'<line x1="{x:.1f}" y1="{MT}" x2="{x:.1f}" y2="{H - MB}" class="thr"/>'
            )

    # bars + direct pair/value labels
    bars, plabels, vlabels, ycs = [], [], [], []
    for i, p in enumerate(pairs):
        yc = MT + i * ROW_H + ROW_H / 2
        ycs.append(round(yc, 1))
        x_end = x_of(p.gap_pct)
        if p.gap_pct >= 0:
            rx, rw, role = CX, x_end - CX, "s1"
            vx, anchor = x_end + 6, "start"
        else:
            rx, rw, role = x_end, CX - x_end, "bad"
            vx, anchor = x_end - 6, "end"
        op = "1" if p.flagged else "0.82"
        # non-synchronous legs get a dashed outline: the gap is an overnight
        # move, not a live dislocation, so it must not read as a clean signal.
        stroke = (
            ' stroke="var(--muted)" stroke-width="1.4" stroke-dasharray="3 2"'
            if not p.synchronous
            else ""
        )
        bars.append(
            f'<rect class="bar" x="{rx:.1f}" y="{yc - BAR_H / 2:.1f}" '
            f'width="{max(rw, 0.6):.1f}" height="{BAR_H}" rx="2.5" '
            f'fill="var(--{role})" fill-opacity="{op}"{stroke}/>'
        )
        plabels.append(
            f'<text x="{PX0 - 10}" y="{yc + 3:.1f}" class="plab">'
            f"{html.escape(p.pair)}</text>"
        )
        weight = "700" if p.flagged else "500"
        vlabels.append(
            f'<text x="{vx:.1f}" y="{yc + 3:.1f}" class="vlab" '
            f'style="text-anchor:{anchor};font-weight:{weight}">'
            f"{p.gap_pct:+.2f}%</text>"
        )

    # hero: widest gap + how many pairs are flagged
    widest = max(pairs, key=lambda p: abs(p.gap_pct))
    flagged_n = sum(1 for p in pairs if p.flagged)
    hcls = "up" if widest.gap_pct >= 0 else "down"

    # embedded data for the hover layer (strings only -> textContent-safe)
    data = {
        "yc": ycs,
        "px0": PX0,
        "px1": PX1,
        "rows": [
            {
                "pair": p.pair,
                "gap": f"{p.gap_pct:+.2f}%",
                "tase": _fmt(p.tase_ils),
                "us": _fmt(p.us_in_ils),
                "flag": "flagged" if p.flagged else "within threshold",
                "asof": (
                    p.tase_date
                    if p.synchronous
                    else f"TASE {p.tase_date} vs US {p.us_date}"
                ),
                "sync": (
                    "synchronous"
                    if p.synchronous
                    else "NON-SYNCHRONOUS (overnight move, not a live gap)"
                ),
            }
            for p in pairs
        ],
    }

    trows = "".join(
        f"<tr><td>{html.escape(p.pair)}</td><td>{p.gap_pct:+.2f}%</td>"
        f"<td>{_fmt(p.tase_ils)}</td><td>{_fmt(p.us_in_ils)}</td>"
        f"<td>{'yes' if p.flagged else 'no'}</td>"
        f"<td>{html.escape(p.tase_date if p.synchronous else f'{p.tase_date}/{p.us_date}')}</td>"
        f"<td>{'yes' if p.synchronous else 'NON-SYNC'}</td></tr>"
        for p in pairs
    )

    if unavailable:
        items = "".join(
            f"<li>{html.escape(u.pair)} - {html.escape(u.reason)}</li>"
            for u in unavailable
        )
        una_html = (
            '<div class="note"><b>Unavailable from source '
            "(skipped, not estimated):</b>"
            f"<ul>{items}</ul></div>"
        )
    else:
        una_html = ""

    nonsync = [p for p in pairs if not p.synchronous]
    if nonsync:
        nsi = "".join(
            f"<li>{html.escape(p.pair)}: TASE {html.escape(p.tase_date)} vs "
            f"US {html.escape(p.us_date)} - gap is an overnight move, not a live "
            "dislocation</li>"
            for p in nonsync
        )
        nonsync_html = (
            '<div class="note"><b>Non-synchronous legs '
            "(dashed bars, treat the gap as an artifact):</b>"
            f"<ul>{nsi}</ul></div>"
        )
    else:
        nonsync_html = ""

    legend = (
        '<span class="lg"><i style="background:var(--s1)"></i>Premium · TASE &gt; US</span>'
        '<span class="lg"><i style="background:var(--bad)"></i>Discount · TASE &lt; US</span>'
    )

    css_vars = lambda mode: ";".join(f"--{k}:{v}" for k, v in PAL[mode].items())
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Dual-listed gaps - {html.escape(as_of)}</title>
<style>
  :root{{{css_vars("light")};--panel:#fff}}
  html[data-theme="dark"]{{{css_vars("dark")};--panel:#111}}
  @media (prefers-color-scheme:dark){{html:not([data-theme="light"]){{{css_vars("dark")};--panel:#111}}}}
  *{{box-sizing:border-box}} body{{margin:0;background:var(--page);color:var(--primary);
    font-family:system-ui,-apple-system,"Segoe UI",sans-serif}}
  .wrap{{max-width:1000px;margin:0 auto;padding:20px}}
  .head{{display:flex;justify-content:space-between;align-items:flex-end;gap:12px;flex-wrap:wrap}}
  h1{{font-size:20px;margin:0}} .sub{{color:var(--secondary);font-size:13px;margin-top:2px}}
  .hero{{text-align:right}} .hero .px{{font-size:28px;font-weight:700}}
  .hero .dl{{font-size:14px;font-weight:600}} .up{{color:var(--s1)}} .down{{color:var(--bad)}}
  .legend{{display:flex;gap:14px;flex-wrap:wrap;margin:12px 0 4px;font-size:12px;color:var(--secondary)}}
  .lg i{{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:5px;vertical-align:middle}}
  .card{{background:var(--surface);border:1px solid var(--grid);border-radius:12px;padding:10px;position:relative}}
  svg{{display:block;width:100%;height:auto;touch-action:none}}
  .grid{{stroke:var(--grid);stroke-width:1}} .zero{{stroke:var(--secondary);stroke-width:1.4}}
  .thr{{stroke:var(--muted);stroke-width:1;stroke-dasharray:3 3;opacity:.7}}
  .xtick{{fill:var(--muted);font-size:10.5px;text-anchor:middle;font-variant-numeric:tabular-nums}}
  .plab{{fill:var(--secondary);font-size:12px;text-anchor:end;font-weight:600}}
  .vlab{{fill:var(--primary);font-size:11px;font-variant-numeric:tabular-nums}}
  .bar{{transition:fill-opacity .1s}}
  #cross{{stroke:var(--axis);stroke-width:1;opacity:0}}
  .tip{{position:absolute;pointer-events:none;background:var(--panel);border:1px solid var(--grid);
    border-radius:8px;padding:8px 10px;font-size:12px;opacity:0;transform:translate(-50%,-115%);
    white-space:nowrap;box-shadow:0 4px 14px rgba(0,0,0,.18);font-variant-numeric:tabular-nums}}
  .tip b{{display:block;margin-bottom:4px;font-size:11px;color:var(--secondary)}}
  .bar-row{{display:flex;gap:8px;margin:14px 0 4px}}
  button{{background:var(--surface);color:var(--primary);border:1px solid var(--grid);border-radius:8px;
    padding:6px 12px;font-size:12.5px;cursor:pointer}} button:hover{{border-color:var(--s1)}}
  table{{border-collapse:collapse;width:100%;font-size:12px;font-variant-numeric:tabular-nums;margin-top:8px}}
  th,td{{text-align:right;padding:4px 8px;border-bottom:1px solid var(--grid)}} th{{color:var(--secondary)}}
  td:first-child,th:first-child{{text-align:left}} #tableview{{display:none}}
  .note{{margin-top:12px;font-size:12px;color:var(--secondary)}} .note ul{{margin:4px 0 0;padding-left:18px}}
</style></head>
<body><div class="wrap">
  <div class="head">
    <div><h1>Dual-listed premium / discount</h1>
      <div class="sub">TASE vs US, currency-adjusted · USD/ILS {_fmt(fx, 4)} · {html.escape(fx_label)} · as of {html.escape(as_of)}</div></div>
    <div class="hero"><div class="px {hcls}">{widest.gap_pct:+.2f}%</div>
      <div class="dl">widest: {html.escape(widest.pair)} · {flagged_n} of {n} flagged (&gt;{_fmt(threshold, 1)}%)</div></div>
  </div>
  <div class="legend">{legend}</div>
  <div class="card" id="card">
    <svg id="svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid meet"
         role="img" aria-label="Diverging bar chart of dual-listed gap percent per pair">
      {"".join(grid)}{"".join(tmarks)}{"".join(xlab)}
      {"".join(bars)}{"".join(plabels)}{"".join(vlabels)}
      <line id="cross" x1="{PX0}" y1="0" x2="{PX1}" y2="0"/>
    </svg>
    <div class="tip" id="tip"></div>
  </div>
  <div class="bar-row">
    <button id="tbtn">Table view</button>
    <button id="thm">Toggle light/dark</button>
  </div>
  <div id="tableview"><table><thead><tr><th>Pair</th><th>Gap %</th><th>TASE (ILS)</th>
    <th>US to ILS</th><th>Flagged</th><th>As-of</th><th>Synchronous</th></tr></thead>
    <tbody>{trows}</tbody></table></div>
  {nonsync_html}
  {una_html}
</div>
<script>
const D={json.dumps(data)};
const svg=document.getElementById('svg'),card=document.getElementById('card'),tip=document.getElementById('tip'),
  cross=document.getElementById('cross');
const VH={H};
function nearest(py){{let best=0,bd=1e9;for(let i=0;i<D.yc.length;i++){{const d=Math.abs(D.yc[i]-py);if(d<bd){{bd=d;best=i}}}}return best}}
function move(ev){{const r=svg.getBoundingClientRect(),sy=(ev.clientY-r.top)/r.height*VH;
  const i=nearest(sy),y=D.yc[i];cross.setAttribute('y1',y);cross.setAttribute('y2',y);cross.style.opacity=.7;
  const row=D.rows[i];
  tip.textContent='';
  const hd=document.createElement('b');hd.textContent=row.pair;tip.appendChild(hd);
  const lines=[['Gap',row.gap],['TASE (ILS)',row.tase],['US to ILS',row.us],['Status',row.flag],['As-of',row.asof],['Sync',row.sync]];
  for(const pair of lines){{
    tip.appendChild(document.createTextNode(pair[0]+': '+pair[1]));
    tip.appendChild(document.createElement('br'));
  }}
  tip.style.opacity=1;
  const cardR=card.getBoundingClientRect();
  tip.style.left=(ev.clientX-cardR.left)+'px';tip.style.top=(ev.clientY-cardR.top)+'px';
}}
svg.addEventListener('pointermove',move);
svg.addEventListener('pointerleave',()=>{{tip.style.opacity=0;cross.style.opacity=0}});
document.getElementById('tbtn').onclick=()=>{{const t=document.getElementById('tableview');
  t.style.display=t.style.display==='block'?'none':'block'}};
document.getElementById('thm').onclick=()=>{{const h=document.documentElement;
  const cur=h.getAttribute('data-theme')||(matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light');
  h.setAttribute('data-theme',cur==='dark'?'light':'dark')}};
</script></body></html>"""
