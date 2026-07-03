# Example: What does QQQ hold, and what does it cost?

## User request
"What does QQQ actually hold, and is it expensive?"

## Steps the skill takes
1. Resolve the ticker: QQQ is a plain (non-leveraged) index ETF tracking the
   Nasdaq-100 — safe to treat as buy-and-hold, unlike leveraged/inverse products.
2. Pull the data:
   `python scripts/etf_holdings.py --ticker QQQ`
   The provider resolves the expense ratio across candidate keys
   (`netExpenseRatio` → `annualReportExpenseRatio` → `feesExpensesInvestment`) and,
   if those are empty, yfinance `funds_data`. The JSON carries an
   `expense_ratio_source` so the number is never a silent null or a guess.
3. Read exposure: top-10 concentration as a single-name-risk proxy (mega-cap tech
   dominates QQQ), noting the holdings as-of date.
4. Optional visual — only because the user asked "what does it hold":
   `python scripts/chart.py --ticker QQQ --out QQQ.html`

## Expected output shape
- Top holdings with weights (e.g. AAPL, MSFT, NVDA…), largest first.
- Expense ratio as a percentage, with its `expense_ratio_source`.
- AUM and top-10 concentration, with the disclosure as-of date.
- One self-contained interactive `QQQ.html` (inline SVG): horizontal holdings bars
  on a sequential blue ramp, an expense-ratio + AUM readout, hover tooltip, table
  view, and a light/dark toggle. The written answer stands on its own without it.

## Notes
- The expense ratio is not the total cost — bid/ask spread and tracking error
  also matter; call that out for cost-sensitive users.
- If holdings come back empty, the issuer discloses on a delay — report the
  latest available as-of date rather than fabricating constituents.
