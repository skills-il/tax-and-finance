# Example: Do I need both VTI and VOO?

## User request
"I hold both VTI and VOO. Am I doubling up? Which one is cheaper?"

## Steps the skill takes
1. Resolve both tickers: VTI (total US market) and VOO (S&P 500) — both plain
   index ETFs, so a weight-based overlap comparison is meaningful.
2. Pull both profiles and compute overlap:
   `python scripts/etf_holdings.py --ticker VTI --compare VOO`
   Overlap is `sum(min(weight_A, weight_B))` over shared holdings — two
   S&P-heavy funds can be ~85%+ overlapping by weight. The output also reports
   each fund's expense ratio (with `expense_ratio_source`) and the delta.
3. Interpret: high overlap → holding both adds little diversification; the tie-
   breaker is usually cost (expense-ratio delta) and small-cap coverage (VTI adds
   mid/small caps VOO lacks).
4. Optional visual — a side-by-side comparison reads better as a chart:
   `python scripts/chart.py --ticker VTI --compare VOO --out vti-voo.html`

## Expected output shape
- A single overlap percentage by shared-holding weight, with the as-of date.
- The shared mega-cap names driving the overlap (AAPL, MSFT, NVDA…).
- Expense ratios for both funds and the delta in percentage points (cheaper wins).
- A one-line redundancy call: "largely redundant — keep the cheaper/broader one."
- One self-contained interactive `vti-voo.html`: grouped bars per shared holding
  (VTI vs VOO in two palette colours, with a legend), an overlap % and cost-delta
  readout, hover tooltip, table view, and a light/dark toggle.

## Notes
- Overlap by weight ≠ overlap by count; report the weight-based figure, it is what
  affects real diversification.
- Out of scope: Israeli mutual funds (kranot ne'emanut) and single stocks — route
  a single-stock question to global-stock-analysis.
