# Example: Is Check Point cheaper in Tel Aviv or New York?

## User request
"Check Point is dual-listed — is it trading at a premium or a discount on TASE
versus NASDAQ right now?"

## Steps the skill takes
1. Load `references/dual-listed-pairs.md` and confirm CHKP maps to US `CHKP`
   with an ADR ratio of 1 and a 2.0% alert threshold.
2. Fetch both legs with `scripts/provider.py`:
   - US leg: last close of `CHKP` in USD.
   - Tel-Aviv leg: last close of `CHKP.TA`; because the line is quoted in agorot
     (currency `ILA`), divide by 100 to get shekels.
   - USD/ILS: use the Bank of Israel representative rate if the user supplied one
     (`--boi-rate`), otherwise fetch `USDILS=X` and mark it indicative.
3. Convert and compute the gap:
   `us_in_ils = us_usd * rate * adr`;
   `gap_pct = (tase_ils - us_in_ils) / us_in_ils * 100`.
4. Score confidence from trading-hours overlap (Mon-Thu high; Fri TASE closes
   13:50) and compare `|gap|` to the pair threshold.

## Expected output shape
- TASE price in ILS and the NASDAQ price converted to ILS.
- Gap %, labelled premium (TASE above US) or discount (TASE below US).
- Whether it clears the 2.0% threshold, plus the overlap-confidence note and the
  settlement (T+1) / FX-cost caveat that the gap is not risk-free profit.
- No chart for a single pair — the text answer stands alone. A chart is offered
  only if the user then asks to compare several pairs.
