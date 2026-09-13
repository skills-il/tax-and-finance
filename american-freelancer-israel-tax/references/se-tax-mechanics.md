# Self-employment tax mechanics

Every figure is backed by `evidence.json`. Nothing here is tax advice.

## The rate

| Component | Rate | Cap |
|---|---|---|
| Social security | 12.4 percent | Yes, the annual wage base |
| Medicare | 2.9 percent | None |
| Combined | 15.3 percent | |

Applies where net earnings from self-employment are USD 400 or more. On the form the test is
line 4c, after the 92.35 percent factor: "If less than $400, stop; you don't owe
self-employment tax".

## Order of computation, per Schedule SE

1. Net earnings from self-employment, from Schedule C.
2. Multiply by 92.35 percent (0.9235). This is Schedule SE line 4a.
3. Social security portion: 12.4 percent on the smaller of the step 2 amount or the wage base
   less social security wages (lines 7 to 10).
4. Medicare portion: 2.9 percent, uncapped (line 11). Line 12 is the SE tax.
5. Separately, on Form 8959: Additional Medicare Tax of 0.9 percent above the filing-status
   threshold. It is not part of line 12, and the line 13 half-deduction does not include it.

Applying 15.3 percent directly to net earnings, skipping step 2, overstates the result.

## Wage base

For 2025 the maximum self-employment income subject to social security tax is USD 176,100.
For 2026 the maximum amount of earned income (wages and net earnings from self-employment)
subject to social security tax is USD 184,500, published in the 2026 Form 1040-ES. The figure
changes annually; take it from the current-year Form 1040-ES or that year's Schedule SE
instructions, never from a prior year.

## Estimated payments, 2026 (Form 1040-ES)

| Payment | Due |
|---|---|
| 1st | April 15, 2026 |
| 2nd | June 15, 2026 |
| 3rd | Sept. 15, 2026 |
| 4th | Jan. 15, 2027 |

Generally required if at least USD 1,000 of tax is expected. The penalty is avoided by paying
the smaller of 90 percent of the 2026 tax or 100 percent of the 2025 tax (110 percent if 2025
AGI exceeded USD 150,000, or USD 75,000 married filing separately). The additional 4 months
of time to file is not an extension of time to pay (Publication 54).

## Additional Medicare Tax thresholds

| Filing status | Threshold |
|---|---|
| Married filing jointly | USD 250,000 |
| Married filing separately | USD 125,000 |
| Single, head of household, qualifying surviving spouse | USD 200,000 |

Where the taxpayer has both wages and self-employment income, the threshold applied to the
self-employment income is reduced (but not below zero) by the total amount of Medicare wages.
On a joint return both spouses' Medicare wages and self-employment income are combined to
determine whether the threshold is exceeded (Instructions for Form 8959).

Form 8959 has two parts that matter here. Part I taxes Medicare wages (box 5) above the
threshold at 0.9 percent. Part II taxes Schedule SE line 6 above the threshold as reduced by
those wages. The total is lines 7, 13 and 17 added. An employer withholds only on wages above
USD 200,000 that it pays, regardless of filing status, so Part I can be owed unwithheld.

## The deduction, stated precisely

The employer-equivalent portion of self-employment tax is deductible in figuring adjusted
gross income. This deduction affects INCOME TAX ONLY. It does not reduce net earnings from
self-employment and it does not reduce the self-employment tax.

## The exclusion does not apply

Foreign earnings from self-employment cannot be reduced by the foreign earned income exclusion
when computing SE tax. A self-employed US citizen living outside the United States must in
most cases pay SE tax. The exclusion and the foreign tax credit reach US INCOME tax only.

## Totalization agreements: the full list

Under a social security agreement a person generally pays social security taxes to only the
country in which they live. The United States has agreements with:

Australia, Austria, Belgium, Brazil, Canada, Chile, the Czech Republic, Denmark, Finland,
France, Germany, Greece, Hungary, Iceland, Ireland, Italy, Japan, Luxembourg, the Netherlands,
Norway, Poland, Portugal, the Slovak Republic, Slovenia, South Korea, Spain, Sweden,
Switzerland, the United Kingdom, and Uruguay.

**Israel is not on this list.** That absence is the whole reason this skill exists. Re-check
the list in the current Schedule SE instructions before relying on it, since agreements can be
added.
