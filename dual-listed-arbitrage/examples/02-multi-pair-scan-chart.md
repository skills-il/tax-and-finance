# Example: Scan three dual-listed names and chart the gaps

## User request
"Scan Check Point, NICE, and Teva for cross-listing gaps against a
representative rate of 3.65 and show me a chart."

## Steps the skill takes
1. Resolve the three symbols against `references/dual-listed-pairs.md`
   (CHKP, NICE, TEVA; ADR ratio 1; per-pair thresholds).
2. Because the user pinned the rate and asked for a chart, run the optional
   orchestrator:

       python scripts/chart.py --pairs CHKP,NICE,TEVA --boi-rate 3.65 --out gaps.html

   `scripts/chart.py` fetches each US leg and each `.TA` leg via
   `scripts/provider.py`, converts the US price to shekels at 3.65, and computes
   each gap %. A pair whose Tel-Aviv leg is unavailable from the free source is
   collected as skipped, never estimated.
3. `scripts/viz.py` renders a self-contained interactive HTML diverging-bar
   chart — premium in blue, discount in red, from a neutral zero baseline — with
   hover detail, a table view, and a light/dark toggle.

## Expected output shape
- A short per-pair summary: gap % for each name, flagged when it exceeds its
  threshold, with the widest gap called out.
- The optional `gaps.html` file: one horizontal bar per pair on the diverging
  scale, with any skipped pairs listed under "unavailable from source".
- The FX line (3.65, representative rate) and the as-of date shown on the chart.
- The reminder that the gap reflects settlement timing and FX cost, so it is not
  a risk-free arbitrage.
