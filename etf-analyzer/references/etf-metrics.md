# ETF Metrics Methodology

## Expense ratio
Annual net cost as a % of assets. Compare within a category; a 0.03% vs
0.20% gap compounds materially over a decade.

## Holdings overlap (two ETFs)
    overlap% = sum( min(weight_A[i], weight_B[i]) for shared holdings i )
Two S&P-tracking funds can be ~99% overlapping — flag redundancy for
diversification questions.

## Tracking error
Stdev of (ETF return - index return) over a window. Low is good for index
ETFs; a rising value signals sampling/optimization drift.

## Sector / geo exposure
Aggregate holding weights by GICS sector and domicile. Report top-10
concentration as a single-name-risk proxy.

## Not in scope
Israeli mutual funds (kranot ne'emanut) and ETNs.
