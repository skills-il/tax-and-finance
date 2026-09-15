# Example: Is NICE cheaper in Tel Aviv or New York?

## User request
"NICE is dual-listed - is it trading at a premium or a discount on TASE
versus NASDAQ right now?"

## Steps the skill takes
1. Look up NICE in `references/dual-listed-pairs.md` (or `scripts/registry.py`):
   TASE symbol NICE, US ticker NICE, ratio 1, 2.0% alert threshold.
2. Fetch both legs with `scripts/provider.py`:
   - US leg: last close of `NICE` in USD.
   - Tel-Aviv leg: last close of `NICE.TA`; because the line is quoted in agorot
     (currency `ILA`), divide by 100 to get shekels.
   - USD/ILS: use the Bank of Israel representative rate if the user supplied one
     (`--boi-rate`), otherwise fetch `USDILS=X` and mark it indicative.
3. Convert and compute the gap:
   `us_in_ils = us_usd * rate * ratio`;
   `gap_pct = (tase_ils - us_in_ils) / us_in_ils * 100`.
4. Check both as-of dates, score confidence from trading-hours overlap (Mon-Thu
   only the end of the TASE session overlaps the US open; Friday none), and
   compare `|gap|` to the pair threshold.

## Expected output shape
- TASE price in ILS and the NASDAQ price converted to ILS.
- Gap %, labelled premium (TASE above US) or discount (TASE below US).
- Whether it clears the 2.0% threshold, plus the overlap-confidence note and the
  settlement / FX-cost caveat that the gap is not risk-free profit.
- No chart for a single pair - the text answer stands alone. A chart is offered
  only if the user then asks to compare several pairs.

## If the user names a company that is not dual-listed
"Compare Check Point in Tel Aviv and New York" gets a plain answer that Check
Point trades on Nasdaq only, so there is no Tel-Aviv leg and no gap to compute.
