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
- **Correct instrument model: dual-listed ordinaries are 1:1.** Under Israel's
  dual-listing arrangement the same ordinary share is fungible across TASE and
  the US exchange, so the ratio is 1:1 by construction. A true ADR ratio must come
  from the depositary agreement / SEC Form F-6, never assumed. (Covered: Step 4 +
  registry.)
- **Registry freshness against the live TASE dual-listed list.** Companies list,
  delist and are acquired; the TASE symbol can differ from the US ticker after an
  acquisition (TASE CYBR is US PANW). Every registry row must be checked against
  the TASE "Dual Listed" securities list, and a named company that is not
  dual-listed (Check Point) must be answered as "no Tel-Aviv leg", never
  estimated. (Covered: Step 1 + registry.py raises on unregistered symbols.
  Rebuilt 2026-09-15.)
- **Unverified ratios among dual listings.** Listings whose US line did not match
  at ratio 1 are excluded from the registry until the ratio is read from the F-6.
  (Covered: registry "NOT registered" list.)
- **BoI representative-rate conversion (not intraday).** The headline USD to ILS
  uses the daily representative rate, which is set during the Israeli business day
  and so is stale relative to a US close. The skill does not assert a setting time.
  (Covered: Step 3 + references/boi-fx.md.)
- **Trading-hours overlap under the Monday-Friday TASE week.** Friday pre-closing
  starts 13:34-13:35 Israel time, before the US open (no overlap). Mon-Thu the live
  overlap runs only from the US open (9:30 New York time) to the TASE pre-close at
  17:14-17:15, and the US open's Israel time shifts for a few weeks a year when the
  two countries change clocks on different dates. (Covered: Step 6 + Gotchas.)
- **Synchronicity of the two legs.** Two daily closes are never simultaneous, even
  on the same date; chart.py marks every close-to-close pair non-synchronous and
  surfaces both as-of dates. (Covered: Step 5 + chart.py.)
- **Settlement / FX / depositary caveats, no risk-free-profit framing.** Closing a
  real gap means moving shares between the lines (days, cost); for an ADS line the
  depositary charges its own fees. (Covered: intro + Gotchas.)
- **Missing / stale leg handled without fabrication.** An absent leg or rate is
  reported as unavailable/skipped, never estimated; NaN placeholder rows ignored.
  (Covered: provider.py + chart.py.)

## Should cover (advanced)

- Corporate actions / splits / bonus shares / rights issues that change the
  effective ratio. (Partially: 1:1 default; last close only.)
- Dividend / ex-date timing differing between the registers. (Covered as a Gotcha;
  not detected automatically.)
- Halts and suspensions leaving a stale print on one side. (Covered as a Gotcha.)
- Liquidity asymmetry: a thin TASE leg can carry an hours-old last price. (Covered
  as a Gotcha + 3.0% registry threshold for thin names; a last-trade-age signal is
  logged for a future cycle.)
- Holiday-calendar asymmetry (US holidays, Israeli chagim, shortened interim-holiday
  sessions). (Covered as a Gotcha + as-of-date check.)

## Out of scope (explicit)

- Single-market technical / fundamental analysis - deferred to tase-stock-analysis.
  Refreshed 2026-09-15: users do ask, and the answer is a routing note, not silence.
- Tax treatment (capital gains, dividend withholding) - person/jurisdiction
  specific, not a price-comparison concern. Refreshed 2026-09-15.
- Execution / brokerage / order routing - the skill measures a gap, it does not
  place or cost trades. Refreshed 2026-09-15; cost categories are named in Gotchas.

## Authoritative sources

- TASE trading & vacation schedule (Mon-Fri session times, pre-closing phases).
- TASE market data, Shares, Dual Listed - Sec. Law (the registry universe).
- NYSE hours & calendars (US core session 9:30-16:00 ET).
- Bank of Israel representative (sha'ar yatzig) USD/ILS rate.
- US depositary agreement / SEC Form F-6 (only for a genuine ADR's ratio).
