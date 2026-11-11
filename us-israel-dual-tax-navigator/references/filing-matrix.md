# Filing Matrix: thresholds, deadlines, penalties

Every figure here is backed by an entry in `evidence.json`. Verify against the primary source
before relying on it. Nothing here is tax advice.

## Which form is triggered by what

| Form | Filed to | Filed with | Trigger |
|---|---|---|---|
| 1040 | IRS | Standalone | A US person whose gross income (INCLUDING income the exclusion would remove) meets the filing threshold for status and age (table below), OR who had net earnings from self-employment of at least USD 400 (Pub 501). Owing zero tax does not remove the duty. |
| FinCEN 114 (FBAR) | FinCEN, BSA E-Filing System | Separately from the return | Aggregate of ALL foreign financial accounts exceeds USD 10,000 at ANY point in the year |
| 8938 (FATCA) | IRS | With the 1040 | Specified foreign financial assets over the threshold for the filer's residence and status, AND a 1040 is required (no 1040 duty, no 8938 duty) |
| 1116 | IRS | With the 1040 | Claiming the Foreign Tax Credit |
| 2555 | IRS | With the 1040 | Claiming the Foreign Earned Income Exclusion |

FBAR and 8938 are separate forms: check each form's requirements and file one, the other, or both. Each form has its own penalty regime.

## 1040 gross-income thresholds, under 65 (Publication 501, Table 1)

| Tax year | Single | Head of household | MFJ (both under 65) | MFS (any age) | Source |
|---|---|---|---|---|---|
| 2023 | USD 13,850 | USD 20,800 | USD 27,700 | USD 5 | irs.gov/pub/irs-prior/p501--2023.pdf |
| 2024 | USD 14,600 | USD 21,900 | USD 29,200 | USD 5 | irs.gov/pub/irs-prior/p501--2024.pdf |
| 2025 | USD 15,750 | USD 23,625 | USD 31,500 | USD 5 | irs.gov/publications/p501 |

TY2026: Publication 501 for 2026 was not yet published on 2026-11-11. Do not derive a row.

## Other sources behind the skill body

| Rule | Source |
|---|---|
| No 1040 duty, no Form 8938 duty | https://www.irs.gov/businesses/corporations/basic-questions-and-answers-on-form-8938 |
| Child tax credit SSN precondition | https://www.irs.gov/credits-deductions/individuals/child-tax-credit |
| Israeli 2026 to 2030 exemption for arrivals 5.11.2025 to 31.12.2026 | https://www.kolzchut.org.il/he/%D7%94%D7%98%D7%91%D7%95%D7%AA_%D7%9E%D7%A1_%D7%9C%D7%A2%D7%95%D7%9C%D7%99%D7%9D |
| TY2023 exclusion, Rev. Proc. 2022-38 | https://www.irs.gov/pub/irs-drop/rp-22-38.pdf |
| TY2024 exclusion, Rev. Proc. 2023-34 | https://www.irs.gov/pub/irs-drop/rp-23-34.pdf |
| TY2025 exclusion, Rev. Proc. 2024-40 | https://www.irs.gov/pub/irs-drop/rp-24-40.pdf |

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
| 15 April | 1040 due; interest on unpaid tax runs from here | Interest date regardless of extensions |
| 15 April | FBAR due | |
| 15 June | 1040 and payment, on the 2 month abroad extension; late-payment penalties run from here | Yes, attach a statement to the return |
| 15 October | 1040, only if Form 4868 filed by 15 June | No, must be requested in time |
| 15 December | 1040, discretionary extension on top of the Form 4868 extension | No, letter sent by 15 October |
| 15 October | FBAR extended date | Yes, no request needed |
| Varies | 1040, Form 2350 extension to meet the bona fide residence or physical presence test (arrival-year oleh) | No; an approved Form 2350 rules out the 15 December letter extension |

Interest runs on unpaid tax from 15 April even under a valid filing extension, except that a
section 7508A postponement period (the Israel relief below) is disregarded in figuring interest
and penalties for an act falling due inside it (Treas. Reg. 301.7508A-1(b)).

Israel relief (IRS Notice 2026-63): affected taxpayers, including any individual whose
principal residence is in Israel, the West Bank or Gaza, have until 30 September 2027 for
returns, payments and certain time-sensitive acts due on or after 30 September 2026 and before
30 September 2027; acts already postponed under Notice 2025-53 are further postponed to the same
date for those eligible under both. Applied automatically by filing address; others call the
IRS disaster hotline. The FBAR is FinCEN's: FinCEN's own Israel FBAR extensions covered only
calendar years 2022 and 2023, and none was found for later years.

## Foreign earned income exclusion by tax year

| Tax year | Amount | Authority |
|---|---|---|
| 2023 | USD 120,000 | Rev. Proc. 2022-38, item .39, under section 911(b)(2)(D)(i) |
| 2024 | USD 126,500 | Rev. Proc. 2023-34, item .39, under section 911(b)(2)(D)(i) |
| 2025 | USD 130,000 | Rev. Proc. 2024-40, item .39, under section 911(b)(2)(D)(i) |
| 2026 | USD 132,900 | Rev. Proc. 2025-32, item .39, under section 911(b)(2)(D)(i) |
| 2027 | USD 137,300 | Rev. Proc. 2026-35, item .41, under section 911(b)(2)(D)(i) |

Do NOT source this from the IRS FEIE landing page, which lists only 2020 through 2023.

## Exclusion versus credit

| | Exclusion (2555) | Credit (1116) |
|---|---|---|
| Qualification | Foreign tax home plus bona fide residence or 330 full days in 12 consecutive months | Israeli tax paid |
| Reaches earned income | Yes, up to the cap | Yes |
| Reaches pensions, social security, interest, dividends, capital gains | No | Preparer to confirm per income category |
| Additional child tax credit in the same year | Blocked | Available |
| Usable on income the other covers | No, they cannot be combined on the same income | No |
| Revocation risk | Yes, see below | Taking it on excluded income can revoke the exclusion |

Revocation: once an exclusion election is revoked it cannot be chosen again for 5 years
without IRS approval via a ruling request. Claiming the foreign tax credit, the additional
child tax credit, or the earned income credit in a later year is itself treated as revoking a
prior choice.

## FBAR penalties

| Violation | Statutory | Inflation adjusted | Authority |
|---|---|---|---|
| Non-willful, per report (Bittner v. United States, 2023), not per account | USD 10,000 | USD 16,536 | 31 USC 5321(a)(5)(B)(i) |
| Willful, per violation | USD 100,000 | USD 165,353 | 31 USC 5321(a)(5)(C)(i)(I) |

For a willful violation the penalty is the GREATER of the adjusted amount or 50 percent of the
account balance at the violation date. On a large account the percentage prong dominates.

Temporal note: these amounts are adjusted for inflation annually, but no annual inflation
adjustment was made for calendar year 2026 (OMB Memorandum M-26-11, 17 April 2026), so the
amounts above remain operative. Re-check
the table rather than assuming a newer figure exists.

## Streamlined Foreign Offshore Procedures

| Element | Requirement |
|---|---|
| Non-residency | In one or more of the most recent 3 years for which the due date has passed: no US abode AND physically outside the US at least 330 full days. Both spouses on a joint return. |
| Non-willfulness | The failure must have been non-willful. This is a state-of-mind judgement for counsel, not for this skill. |
| Returns | Most recent 3 years whose due date has passed, delinquent or amended, with all required information returns (e.g. Forms 3520, 5471, 8938) |
| FBARs | Most recent 6 years whose FBAR due date has passed, e-filed via BSA E-Filing with reason "Other" |
| Mechanics | "Streamlined Foreign Offshore" in red on each return; signed Form 14653; paper submission to the IRS Austin address (electronic not accepted); ITIN application if not SSN-eligible |
| Payment | Full tax and interest remitted with the submission |
| Relief | No failure-to-file, failure-to-pay, accuracy-related, information-return, or FBAR penalties |

Not available to a taxpayer under IRS civil examination for any year or under IRS Criminal
Investigation. Designed for failures that did not result from willful conduct; the route choice belongs to
a licensed preparer or counsel.

## Treaty

The savings clause at Article 6(3) lets each state tax its own citizens as if the Convention
had not come into effect. Article 6(4)(a), as amended by the 1980 and 1993 protocols, carves
out benefits under Article 10 (Grants), Article 15-A (Charitable Contributions), paragraphs (2)
and (3) of Article 20 (Private Pensions and Annuities), Article 21 (Social Security Payments),
Article 26 (Relief from Double Taxation), Article 27 (Nondiscrimination) and Article 28 (Mutual
Agreement Procedure). Article 20(1) on private pensions is not in the list.

The practical reading: the treaty does not stop the US taxing a dual citizen. What survives
the savings clause is the double-tax relief machinery, principally Article 26.
