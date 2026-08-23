# Filing Matrix: thresholds, deadlines, penalties

Every figure here is backed by an entry in `evidence.json`. Verify against the primary source
before relying on it. Nothing here is tax advice.

## Which form is triggered by what

| Form | Filed to | Filed with | Trigger |
|---|---|---|---|
| 1040 | IRS | Standalone | Being a US person, regardless of residence or of tax owed |
| FinCEN 114 (FBAR) | FinCEN, BSA E-Filing System | Separately from the return | Aggregate of ALL foreign financial accounts exceeds USD 10,000 at ANY point in the year |
| 8938 (FATCA) | IRS | With the 1040 | Specified foreign financial assets over the threshold for the filer's residence and status |
| 1116 | IRS | With the 1040 | Claiming the Foreign Tax Credit |
| 2555 | IRS | With the 1040 | Claiming the Foreign Earned Income Exclusion |

FBAR and 8938 are independent. Filing one does not satisfy the other, and the same account is
commonly reported on both, each with its own penalty.

## Form 8938 thresholds, all four sub-dimensions

| Residence | Status | More than, on the last day | More than, at any time |
|---|---|---|---|
| Outside the US | Unmarried or MFS | USD 200,000 | USD 300,000 |
| Outside the US | Married filing jointly | USD 400,000 | USD 600,000 |
| In the US | Unmarried or MFS | USD 50,000 | USD 75,000 |
| In the US | Married filing jointly | USD 100,000 | USD 150,000 |

A user living in Israel takes an "Outside the US" row. Secondary guides frequently quote the
domestic row to an expat audience, which invents a duty the user does not have.

## Deadlines, calendar-year filer living abroad

| Date | Item | Automatic? |
|---|---|---|
| 15 April | 1040 due; any tax owed is payable | Payment date regardless of extensions |
| 15 April | FBAR due | |
| 15 June | 1040, on the 2 month abroad extension | Yes, no request needed |
| 15 October | 1040, only if Form 4868 filed before 15 June | No, must be requested in time |
| 15 October | FBAR extended date | Yes, no request needed |

Interest runs on unpaid tax from 15 April even under a valid filing extension.

## Foreign earned income exclusion by tax year

| Tax year | Amount | Authority |
|---|---|---|
| 2025 | USD 130,000 | Rev. Proc. 2024-40, item .39, under section 911(b)(2)(D)(i) |
| 2026 | USD 132,900 | Rev. Proc. 2025-32, item .39, under section 911(b)(2)(D)(i) |

Do NOT source this from the IRS FEIE landing page, which lists only 2020 through 2023.

## Exclusion versus credit

| | Exclusion (2555) | Credit (1116) |
|---|---|---|
| Reaches earned income | Yes, up to the cap | Yes |
| Reaches investment income | No | Yes |
| Can carry forward | No | Yes |
| Usable on income the other covers | No, they cannot be combined on the same income | No |
| Revocation risk | Yes, see below | Taking it on excluded income can revoke the exclusion |

Revocation: once an exclusion election is revoked it cannot be chosen again for 5 years
without IRS approval via a ruling request. Claiming the foreign tax credit, the additional
child tax credit, or the earned income credit in a later year is itself treated as revoking a
prior choice.

## FBAR penalties

| Violation | Statutory | Inflation adjusted | Authority |
|---|---|---|---|
| Non-willful, per violation | USD 10,000 | USD 16,536 | 31 USC 5321(a)(5)(B)(i) |
| Willful, per violation | USD 100,000 | USD 165,353 | 31 USC 5321(a)(5)(C)(i)(I) |

For a willful violation the penalty is the GREATER of the adjusted amount or 50 percent of the
account balance at the violation date. On a large account the percentage prong dominates.

Temporal note: these amounts are adjusted for inflation annually, but no annual inflation
adjustment was made for calendar year 2026, so the amounts above remain operative. Re-check
the table rather than assuming a newer figure exists.

## Streamlined Foreign Offshore Procedures

| Element | Requirement |
|---|---|
| Non-residency | In one or more of the most recent 3 years for which the due date has passed: no US abode AND physically outside the US at least 330 full days. Both spouses on a joint return. |
| Non-willfulness | The failure must have been non-willful. This is a state-of-mind judgement for counsel, not for this skill. |
| Returns | Most recent 3 years, delinquent or amended, with all required information returns |
| FBARs | Most recent 6 years |
| Payment | Full tax and interest remitted with the submission |
| Relief | No failure-to-file, failure-to-pay, accuracy-related, information-return, or FBAR penalties |

Where the returns are already correct and only FBARs are missing, the lighter delinquent-FBAR
submission procedure may be the better fit.

## Treaty

The savings clause at Article 6(3) lets each state tax its own citizens as if the Convention
had not come into effect. Article 6(4) carves out benefits under Article 10 (Grants),
Article 21 (Social Security Payments), Article 26 (Relief from Double Taxation),
Article 27 (Nondiscrimination) and Article 28 (Mutual Agreement Procedure).

The practical reading: the treaty does not stop the US taxing a dual citizen. What survives
the savings clause is the double-tax relief machinery, principally Article 26.
