# Israeli Tax Regimes for Valuation

The effective tax rate is the input generic valuation models get wrong most often. This file is the decision tree. Every rate here is sourced in `evidence.json`.

## Why this matters to the valuation

The tax rate enters in two places that must agree:

1. The tax on EBIT inside free cash flow to firm.
2. The tax shield on debt inside the WACC.

Using the standard rate in one and a preferred rate in the other is a silent inconsistency. Using the standard rate for a company that actually pays a preferred rate overstates the tax drag by more than half and understates the company.

## Decision tree

Ask in this order.

**1. Is the company part of a multinational group large enough to fall under the minimum top-up tax?**
If yes, its Israeli effective rate cannot sit below 15% for tax years beginning after 31 December 2025. A model projecting a lower effective rate for such a group is projecting a rate that no longer survives.

**2. Does the company hold a status under the Encouragement of Capital Investments Law?**
Ask for the approval, do not infer it from the sector. Then place it:

| Status | Development area A | Rest of country |
|---|---|---|
| Preferred Enterprise | 7.5% | 16% |
| Special Preferred Enterprise | 5% | 8%, for ten years |
| Preferred Technology Enterprise | 7.5% | 12% |
| Special Preferred Technology Enterprise | 6% | 6% |

Technology-enterprise rates apply only to the portion of intellectual property developed in Israel, on a nexus basis. A company with mixed IP origin has a blended rate, not the headline rate.

After ten years, Special Preferred Enterprise rates revert to Preferred Enterprise rates unless a new investment program requalifies the company.

**3. If no preferred status, is it a closely held company?**
Then check two rules that change retained cash:

- An annual 2% charge on accumulated undistributed profits.
- Income above 25% profitability may be taxed at the shareholder's marginal rate.
- A service-company rule where 70% or more of income comes from officer or management services to a single entity.

These do not change the corporate rate on ordinary trading income, but they change how much cash the company can retain, which is a cash flow input and affects the treatment of surplus cash on the balance sheet.

**4. Otherwise:** the standard corporate rate of 23%.

## Eligibility gates worth verifying before accepting a reduced rate

| Status | Gates |
|---|---|
| Preferred Technology Enterprise | Group revenue under ILS 10 billion. Average R&D over the prior three years at or above 7% of revenue, or above ILS 75 million a year. Plus one of several secondary tests on R&D headcount, venture funding, revenue growth, or headcount growth, or an Israel Innovation Authority approval. |
| Special Preferred Technology Enterprise | Meets the technology conditions, and group revenue of at least ILS 10 billion. |
| Special Preferred Enterprise | Revenue of at least ILS 1 billion, in a group generating at least ILS 10 billion in the same industrial sector. |

R&D centres are not entitled to a reduced corporate rate where the controlling shareholders or beneficiaries are Israeli residents. Check this before granting a preferred rate to a local R&D subsidiary.

## Dividend withholding, by regime

The owner's net depends on extraction, not just on company-level tax.

| Regime | Dividend withholding |
|---|---|
| Preferred Enterprise | 20%, reducible under treaty |
| Special Preferred Enterprise | 20%, reducible under treaty |
| Preferred Technology Enterprise | 4% to a foreign company where at least 90% of shares are foreign-held, otherwise 20% |
| Special Preferred Technology Enterprise | Same as Preferred Technology Enterprise |

## Persistence into terminal value

A preferred status is conditional and time-limited, not permanent. Before carrying a reduced rate into terminal value, ask:

- Do the eligibility conditions hold across the whole forecast?
- Does the status have a stated expiry?
- Is the R&D spend threshold likely to keep being met at forecast revenue levels? A company that grows revenue fast can fail a percentage-of-revenue R&D test precisely because it grew.

If the status may lapse, model a rate step-up and disclose it. Assuming a reduced rate forever is a substantive assumption that belongs in the assumptions table, not buried in a cell.

## IP disposals

Companies selling IP to a related foreign company may qualify for a reduced 12% capital gains rate where the IP was acquired from a foreign company after 1 January 2017 for at least ILS 200 million, subject to Israel Innovation Authority approval. Relevant when the valuation supports an IP migration rather than a share sale.

## What to verify at each update

Rates and thresholds here move with legislation. Re-verify against the Israel Tax Authority and the PwC summary cited in `evidence.json` at every skill update, and specifically re-check:

- The standard corporate rate.
- Whether the closely held company percentages changed.
- Whether the preferred-enterprise rates or eligibility thresholds changed.
- The minimum top-up tax scope.
