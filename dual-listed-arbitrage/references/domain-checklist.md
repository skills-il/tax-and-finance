# Domain Coverage Checklist - Dual-Listed TASE / US Comparison

Scope: given a dual-listed company, fetch the TASE leg (agorot) and the US leg
(USD), convert USD to ILS via the BoI representative rate and the pair's
conversion ratio, compute the currency-adjusted gap %, flag pairs above a
per-pair threshold, and score confidence by trading-hours overlap. Single-market
analysis is out of scope (defers to tase-stock-analysis).

## Must cover (core)

- **Agorot to shekel scaling of the TASE leg.** TASE equities quote in agorot
  (1 shekel = 100 agorot); divide the TASE quote by 100. A missed /100 misprices
  the TASE leg by 100x and manufactures a fake ~100x premium. (Covered: Step 2
  + a magnitude sanity check in chart.py that skips a ~100x pair.)
- **Correct instrument model: dual-listed ordinaries are 1:1, not ADRs.** Under
  Israel's dual-listing arrangement the same ordinary share is fungible across
  TASE and the US exchange, so the ratio is 1:1 by construction (no depositary
  ratio). A true ADR ratio must come from the depositary agreement / SEC Form
  F-6, never assumed. (Covered: Step 4 + registry.)
- **BoI representative-rate conversion (not intraday) with its timestamp
  acknowledged.** The headline USD to ILS uses the daily representative rate
  (published ~15:30 Israel time), which is itself timed near midday and so is
  stale relative to a US close. (Covered: Step 3.)
- **Trading-hours overlap under the post-Jan-2026 Monday-Friday TASE week.**
  TASE trades Mon-Fri since 5 Jan 2026; Friday closes early (~14:00) before the
  US open (no overlap). Even Mon-Thu the live overlap is only the last ~45 min of
  the TASE session. (Covered: Step 6.)
- **Synchronicity of the two legs.** The US session (~16:30-23:00 Israel) runs
  almost entirely after the TASE close (~17:15), so a naive last-close comparison
  can pull the legs from different days. Enforce/surface an as-of match; a
  non-synchronous gap is an overnight move, not a dislocation. (Covered: Step 5 + chart.py synchronous flag
  and non-synchronous caveat.)
- **Settlement / FX caveats, no risk-free-profit framing.** Closing a real gap on
  fungible ordinaries means transferring shares between registers (T+ days, cost);
  the measured gap is mostly quote staleness + FX timing + bid/ask. (Covered:
  intro + Gotchas.)
- **Missing / stale leg handled without fabrication.** An absent leg or rate is
  reported as unavailable/skipped, never estimated; NaN placeholder rows ignored.
  (Covered: provider.py + chart.py.)

## Should cover (advanced)

- Corporate actions / splits / bonus shares / rights issues that change the
  effective ratio or split-adjust on different dates. (Partially: 1:1 default
  reduces the ratio-drift risk; split-date skew logged for a future cycle.)
- Dividend / ex-date timing differing between the registers. (Logged.)
- Halts and suspensions leaving a stale print on one side. (Partially caught by
  the synchronicity/as-of check.)
- Liquidity asymmetry: a thin TASE leg can carry an hours-old last price. (Logged
  for a future cycle - needs a volume/last-trade-age signal.)
- Holiday-calendar asymmetry (US holidays, Israeli chagim) closing one side.
  (Partially caught by the as-of-date mismatch check; explicit calendar logged.)

## Out of scope (explicit)

- Single-market technical / fundamental analysis - deferred to tase-stock-analysis.
- Tax treatment (capital gains, dividend withholding) - person/jurisdiction
  specific, not a price-comparison concern.
- Execution / brokerage / order routing - the skill measures a gap, it does not
  place or cost trades.

## Authoritative sources

- TASE trading & vacation schedule (Mon-Fri session times, Friday early close).
- ISA / Securities Law dual-listing arrangement (same fungible instrument, 1:1).
- Bank of Israel representative (sha'ar yatzig) USD/ILS rate and its calendar.
- US depositary agreement / SEC Form F-6 (only for a genuine ADR's ratio).
