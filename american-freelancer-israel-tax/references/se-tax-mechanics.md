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

| Tax year | Base | Source |
|---|---|---|
| 2023 | USD 160,200 | SSA contribution and benefit base table |
| 2024 | USD 168,600 | SSA contribution and benefit base table |
| 2025 | USD 176,100 | 2025 Schedule SE instructions; SSA table |
| 2026 | USD 184,500 | 2026 Form 1040-ES and 2026 Schedule SE instructions; SSA table |
| 2027 | USD 192,300 | SSA ("For earnings in 2027, this base is $192,300"); 2027 IRS forms not yet published on 2026-11-11 |

The figure changes annually; take it for the year being computed, never from a prior year.

## Estimated payments, 2026 (Form 1040-ES)

| Payment | Due |
|---|---|
| 1st | April 15, 2026 |
| 2nd | June 15, 2026 |
| 3rd | Sept. 15, 2026 |
| 4th | Jan. 15, 2027 |

Generally required if at least USD 1,000 of tax is expected. The penalty is avoided by paying
the smaller of 90 percent of the 2026 tax or 100 percent of the 2025 tax (110 percent if 2025
AGI exceeded USD 150,000, or USD 75,000 married filing separately). The prior-year test needs
a filed 2025 return covering 12 full months; otherwise only the 90 percent test remains (Form
1040-ES worksheet, line 12b). For uneven income the annualized income installment method (Form
2210 with Schedule AI) can lower a required payment. 2027 dates come from the 2027 Form
1040-ES once published. The additional 4 months
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

That is the list printed in the 2026 Schedule SE instructions (30 countries). SSA's own list
adds Romania, in force September 1, 2026, for 31 in all
(https://www.ssa.gov/international/agreements_overview.html, read 2026-11-11).

**Israel is not on either list.** That absence is the whole reason this skill exists. Re-check
SSA's list before relying on it, since the IRS list lags and agreements can be added.

## The Israeli-side exemption for recent US olim (section 350A)

National Insurance Law Amendment No. 262 (temporary provision), passed 25 February 2026, in
force 1 January 2026 to 31 December 2035. A new oleh from a country in Schedule ט"ז1 (only the
United States) who is an Israeli resident is exempt from Bituach Leumi contributions on
business or employment income on which US social security is paid, until five years from the
oleh visa or certificate (or the Ministry of Aliyah and Integration certificate). Health
insurance contributions are still due (section 2 counts the exempt income for health
insurance), Bituach Leumi may still be due on other income without US social security once it
passes minimum monthly amounts (350A(c)), the exempt
period counts toward benefit qualifying periods, and it is claimed at the local Bituach Leumi
branch. Section 3 lets the Minister extend the period by order for two further periods of up
to five years each, and 350A(d) lets the Minister amend the schedule. It does nothing to US SE
tax. The definition does not require aliyah in 2026 or later and the law applies to
contributions due for January 2026 onward (section 5), so an oleh still inside the five years
appears covered for the remaining months; confirm with Bituach Leumi.
