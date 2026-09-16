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

### Two rules that remove or shrink a shield

- **Second exempt-profits alternative.** Under section 81C(c), as the circular states at 2.13, a
  company that chose the second alternative for computing exempt accumulated profits cannot use the
  magen nechasim when computing excess profits. Only the magen kaspi and the magen hotzaot remain.
  Check which alternative was chosen before computing the asset shield at all.
- **Magen hotzaot is tax-deductible expenses only** (circular 4.3). Excluded: expenses invested in
  balance-sheet assets and not yet released to profit and loss; expenses for acquiring special
  assets or tied to acquiring them, such as depreciation on a special asset or financing costs on a
  loan that funded one.

### The magen hotzaot for a young company

The average runs over the tax year and the two preceding tax years. The circular does not say how to
compute it for a company with fewer than two preceding tax years. Use the current-year deductible
expenses as the floor (the first limb of the maximum is always defined) and flag the average as
undefined rather than averaging over fewer years.

### Special assets: the carve-outs (circular 2.16)

The magen nechasim deducts the cost of special assets, so every exclusion below RAISES the shield.

| Class | Excluded from special assets |
|---|---|
| Rights in land (2.16.4) | Land for self-use, that is a fixed asset under GAAP, even where it is in use by another entity in the group as defined in section 51XXIV of the Encouragement of Capital Investments Law (2.16.4.1). The circular's examples: the company's own office building, a hotel held and operated by the company. A building or commercial asset leased to a third party, for example a mall, is NOT self-use. Where one group company owns and another operates, the asset is attributed to the owner, and a hotel owned by A and operated by group company B is not a special asset of A. |
| Rights in land (2.16.4) | A rental building under section 53(a3), or an institutional-rental building under section 53A, of the Encouragement of Capital Investments Law (2.16.4.2). |
| Loans, deposits, cash (2.16.5) | Cash or cash equivalents pledged or deposited under the obligation in a financial-accompaniment agreement under the Sale (Apartments) (Assurance of Investments of Purchasers of Apartments) Law, as approved by the company's accountant (2.16.5.1). The circular lists further exclusions in 2.16.5.2 to 2.16.5.4; read them from the circular before relying on a loan or cash balance. |

### Tax cost, not book value

The circular states that the asset shield is computed by business-inventory cost, the original-price
balance under section 88 of the Ordinance, or the acquisition-value balance under section 47 of the
Real Estate Taxation Law, as the case may be, and not as presented in the financial statements. In
its worked example 3, investment property shown at fair value of 1,200 is restated to its
acquisition-value balance of 400 before the shield is computed.

### What worked example 3 shows about land inventory

Note (3) of the example describes the land inventory (2,700) as rights in land whose income falls
under section 8A(c). The example's list of deducted items does not include it, and the arithmetic
reaches a total asset shield of 3,000 with that inventory left inside the shield (10,700 adjusted
assets, less 7,700 of deducted items). The circular does not state a general rule for 8A(c) land
inventory in its carve-out list; state only that this is how the example treats it.

### The 50% base and its dating

Circular 3.6.2 measures the 50% alternative against excess profits "to the end of the preceding tax
year", while the charging computation reads the shields at the end of the examined year. The circular
does not resolve which year end the shields inside the 50% base are read at. Compute both and flag it.

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

## Pricing an escape against the charge

For a company whose profits will be distributed eventually, a distribution made to escape the 2%
does not add the shareholder's dividend tax; it mostly brings that tax forward. The 2% is different:
it is a permanent cost, and it repeats in every year the charge applies. The comparison is therefore:

- **Cost of escaping:** the time value of paying the shareholder tax earlier; any difference in the
  shareholder's rate or surtax between distributing now and distributing later; and the lost use of
  the distributed cash inside the company.
- **Cost of not escaping:** the sum of the 2% charges across every year the charge would apply, on
  a base that changes as profits accumulate or are distributed.

Neither side is presumed cheaper. Where the owners genuinely intend never to distribute, state that
as an explicit assumption, because it is the only case in which the full dividend tax is an added
cost. This skill quotes no shareholder rate or surtax; they come from the user's representative.

## Which dividends count toward which escape

The definition of "dividends on which tax was paid" (circular 3.6.3.1 and 3.6.3.2) sits in the 6%
paragraph. It covers an ordinary dividend and a section 126(b) dividend for which the distributing
company elected tax at the highest rate. The 50% paragraph (3.6.2) is worded to cover dividends that
are not dividends to which section 126(b) applies. On the face of the circular, then, an elected
126(b) dividend counts toward the 6% alternative, and whether it also counts toward the 50%
alternative is unresolved. Flag it; do not rely on it to clear the 50% test.
