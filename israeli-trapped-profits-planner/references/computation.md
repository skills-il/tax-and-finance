# Computing the section 81B exposure

Every figure below is tied to a verbatim primary-source snippet in `evidence.json`.

## Order of operations

1. Confirm the entity is a chevrat me'atim under section 76 and, for the section 81B charge,
   resident in Israel.
2. Fix the examined tax year.
3. If section 62A also applies, run it first: it fixes attributed income and the company's taxable
   income, and an attribution can reduce the accumulated-profits base for section 81A where the
   attributed amounts were not already removed from retained earnings in the financial statements.
4. Compute accumulated profits, then exempt accumulated profits, to get taxable accumulated
   profits at the end of the year PRECEDING the examined year.
5. Compute all three shields at the end of the EXAMINED year and take the highest.
6. Excess profits = (4) minus (5).
6a. **Apply the transitional provisions BEFORE testing the escapes, because they move the figures
    the escapes are measured against.** If the company is in the section 5(a) route for this year,
    either by distributing the required percentage this year or by having met a section 5(b) band
    inside the Determining Period, then limb (1) reduces this year's excess profits by the profits
    remaining from commencement-day profits, and limb (2) reduces the DENOMINATOR of the 50% test
    by the same class of amount. Skipping this step overstates both the charge and the distribution
    needed to clear the 50% safe harbour.
7. Test the three escapes in section 81B(b), using the figures as adjusted by step 6a.
8. If none applies, the charge is 2% of excess profits after deducting the dividend distributed
   during the tax year.

## The two measurement dates

The formula deliberately reads its two legs at different year ends: taxable accumulated profits at
the end of the preceding year, the shields at the end of the examined year. A calculator that uses
one date for both is wrong for any company whose balance sheet moved during the year. Keep them as
separate inputs and label them.

## The shields

| Shield | Definition | Trap |
|---|---|---|
| Magen kaspi | A flat shekel sum | Not available in full per company within a group under one controlling individual |
| Magen hotzaot | The higher of the tax-year deductible expenses, or the average across the tax year and the two preceding tax years | It is a maximum-of-two, not the current year |
| Magen nechasim | Company asset cost, less special-asset cost, less equity, less related-party loan balance, plus held-body-corporate cost | Two positive terms, three negative; the held-body term is ADDED |

The three are collectively the shields, and the computation subtracts only the highest.

### The anti-splitting rule

Where the controlling shareholder, alone or together with a relative, is an individual who controls
further closely-held companies, the money shield divides equally among the held companies unless
the company notifies a different division. The other held companies must notify the assessing
officer on the section 131 return that they waive their pro-rata share and did not elect it for
that year. Control here means holding half or more of the means of control.

The circular states the purpose expressly: the money shield exists to avoid charging companies with
low accumulated profits, and the splitting rule exists because a fixed shield would otherwise
reward fragmenting one business across many companies. That purpose is what an assessing officer
will reason from on a fact pattern the circular does not list.

## The base and its deductions

Taxable accumulated profits are accumulated profits less exempt accumulated profits.

Deductions attach at four different stages and must not be pooled into one bucket:

1. Inside the tax alternative for accumulated profits: tax the company paid, dividends distributed
   out of that income, and unoffset losses under sections 28, 29 and 92, measured from
   incorporation to the end of the year preceding the examined year.
2. Inside the accounting alternative: profits attributed to a shareholder and charged to tax under
   the attribution provisions, provided they were not already removed from retained earnings in the
   financial statements; neutralisation of equity profits AND equity losses, which is signed in both
   directions; and a declared-but-unpaid dividend, subject to its own timing condition.
3. From exempt accumulated profits: taxes imposed on them, dividends distributed out of them, and
   unoffset losses originating in the listed exempt activity branches.
4. From excess profits at the charging stage: the dividend distributed during the tax year.

Only the fourth is the charging-stage deduction. Confusing it with the others double-counts.

## Character of the charge

The addition is not deductible from the company's taxable income, and although it is treated as
corporate tax it is expressly not part of corporate tax for computing tax under the Ordinance. It
therefore sits on top of the ordinary corporate rate and cannot be credited against it. Advance
payment provisions do not apply to it.
