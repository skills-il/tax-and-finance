# Valuation Methods Reference

Method selection, multiple definitions, and the approaches that apply where a standard DCF does not.

## Choosing the governing approach

| Company profile | Primary | Why |
|---|---|---|
| Profitable, stable, forecastable | Income (DCF) | Cash flow is the economic substance |
| Asset-heavy, holding company, real-estate-holding | Asset / NAV | Value sits in the assets, not the earnings stream |
| Loss-making with no credible turnaround forecast | Asset / NAV, as a floor | A DCF on negative cash flow produces a meaningless negative |
| Dense peer set, listed or transacted | Market multiples | The market has already priced the risk |
| Pre-revenue or venture-backed | Round-based methods plus allocation | No forecastable cash flow exists to discount |
| Cyclical at a cycle extreme | DCF on a normalized mid-cycle, never on a peak or trough year | Multiples on a peak year embed the peak |

Always run at least two and reconcile. A single-approach valuation is not reviewable.

## Multiple definitions and the consistency rule

The numerator and denominator must sit on the same side of the capital structure.

| Multiple | Numerator | Denominator | Pairs with |
|---|---|---|---|
| EV / EBITDA | Enterprise value | Pre-interest, pre-tax, pre-D&A | Correct |
| EV / EBIT | Enterprise value | Pre-interest | Correct |
| EV / Sales | Enterprise value | Pre-interest | Correct, weak unless margins are comparable |
| P / E | Equity value | Post-interest, post-tax | Correct |
| P / B | Equity value | Equity book value | Correct |

Wrong pairings, both common and both wrong: enterprise value over net income, and market capitalisation over EBITDA.

Notes on applying multiples in Israel:

- The Israeli listed peer set is thin in most sectors. Global sector data is often the only workable source, and the substitution itself must be disclosed.
- A multiple derived from listed companies embeds liquidity that a private company does not have. That is part of what the marketability discount addresses. Do not silently apply a listed multiple to a private company and then also skip the discount.
- Match the multiple to the same normalized earnings figure you built in the normalization bridge, not to reported earnings.

## Asset / NAV approach

Adjust each balance sheet line from book to market:

- Real estate: needs a licensed appraiser. Flag it, do not estimate it.
- Machinery and equipment: market or depreciated replacement cost.
- Receivables: net of a realistic bad-debt view, not the book provision.
- Inventory: net of obsolescence.
- Intangibles developed in-house: usually absent from the books entirely.
- Liabilities: including contingent ones and any severance provision shortfall.

NAV usually sets a floor for a going concern. If DCF lands below NAV, ask whether the business is worth more broken up than continued, and say so.

## Pre-revenue and venture-backed companies

A standard DCF fails here because there is no forecastable cash flow. Use:

| Method | When |
|---|---|
| Backsolve from the last priced round | A recent arm's length round exists |
| Option pricing model allocation | Multiple share classes with different rights |
| Venture capital method | An exit value and a target return can be reasoned |
| Scorecard or comparable-round benchmarking | Very early, no round yet |

**The allocation waterfall matters more than the headline number.** A company with a preferred round does not have one value per share. Liquidation preferences, participation rights, and conversion mean ordinary shares are worth materially less than preferred shares at the same headline valuation. Valuing ordinary shares as a pro-rata slice of the post-money valuation is simply wrong, and it is the most common error in early-stage Israeli valuations.

Always ask for the cap table with the rights attached, not just the ownership percentages.

## Normalization bridge

Present it as a visible table, from reported to normalized:

| Line | Effect |
|---|---|
| Reported EBITDA | Starting point |
| Owner salary adjustment to market | Usually the largest single item |
| Related-party rent to market | |
| Private expenses run through the company | |
| One-off legal, restructuring, or war-period items | |
| Grant income treatment | |
| Normalized EBITDA | The figure multiples and DCF should use |

## Sensitivity and presentation

The output is a range. Build the grid across:

- WACC, stepped around the central estimate.
- Terminal growth, stepped around the central estimate.
- The marketability discount, stepped across the band you can support.

Present the grid, the range, and the midpoint labelled explicitly as a midpoint rather than as the answer.

## Cross-check discipline

After running the approaches, reconcile:

1. Does the DCF sit inside the multiples range? If not, which assumption drives the gap?
2. Does either sit below NAV? If so, address break-up value.
3. Does the implied exit multiple from the terminal value look sane against current sector multiples? An implied exit multiple far above today's sector median means the terminal assumption is doing the work, and that must be stated.
