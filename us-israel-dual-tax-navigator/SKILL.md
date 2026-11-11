---
name: us-israel-dual-tax-navigator
description: "Not tax advice and not a filed return. Maps what a US-Israel dual citizen actually has to file in both systems for a tax year: the US 1040, FBAR (FinCEN 114), Form 8938, and how those line up against the Israeli calendar. Compares the Foreign Earned Income Exclusion against the Foreign Tax Credit, flags the revocation trap, and lays out the Streamlined Foreign Offshore route for someone who never filed after making aliyah. Use when a US citizen or green card holder in Israel asks what they owe the IRS, when their US return and FBAR are due, whether they need an FBAR, which years to catch up, or how to brief an accountant. Produces a filing-obligation map and a document checklist, never a completed or signed return. Do NOT use for Israeli-side filing, for classifying Israeli funds as PFICs, for self-employment tax, or for renouncing citizenship."
license: MIT
---

# US-Israel Dual Filing Navigator

## Legal notice

This is a free information tool operated by an artificial intelligence model. It applies
published filing thresholds and deadlines to figures you supply, and produces a map of which
forms appear to be triggered plus a checklist of documents to gather. It does all of this
without the involvement, review, or approval of a licensed tax adviser, accountant, or
attorney.

It is not tax advice, it is not a filed return, and it is not a professional opinion. What it
produces is a preliminary worksheet for your own organisation, nothing more. It does not
examine your documents, does not verify your residency or domicile status, does not consider
your full financial picture, does not decide any election between reliefs, and does not judge
whether any past failure to file was willful. Each of those is a professional step that this
tool does not perform.

An AI model can err, omit data, or present a wrong conclusion. Any text it produces is an
automatic draft for personal organisation only and must never be submitted to any authority
as it stands.

Responsibility for reporting and for paying tax is yours, the binding assessment is made by
the tax authority concerned, whether the Israeli Tax Authority or the IRS, and representation
before a tax authority is reserved to those permitted to do so by law. This tool is not a
substitute for advice that takes into account the particular data and needs of each person.
Figures and thresholds change, so verify every one against the primary sources under
Reference Links before relying on it.

## Problem

A US citizen who moves to Israel keeps their US filing obligation for life, and almost
nobody is told this on the way in. The result is a population of olim who file perfectly
correct Israeli returns while a separate US obligation quietly accumulates, along with an
FBAR duty that attaches at a level most households cross without noticing. The two systems
have different deadlines, different currencies, and a choice between two forms of relief
that cannot both be used on the same income, where picking the wrong one can be locked in
for five years.

## Instructions

Work through the stages in order. Stop and ask the user for a missing input rather than
assuming a value, and never state a figure that is not in Reference Links or `references/filing-matrix.md`.

### Stage 1: Establish the filing premise

Confirm the user is a US person: a US citizen (including a dual citizen who has never lived
in the US) or a lawful permanent resident. If so, state plainly that US taxation follows
citizenship, not residence, and that the duty to file a 1040 on worldwide income survives
aliyah and survives owing zero US tax.

The 1040 duty is not automatic, though. It turns on gross income against the filing
threshold for the filer's status and age, and for this test gross income INCLUDES income
the foreign earned income exclusion would later remove. Under-65 rows from Publication 501:

| Tax year | Single | Head of household | Married filing jointly | Married filing separately (any age) |
|---|---|---|---|---|
| 2023 | USD 13,850 | USD 20,800 | USD 27,700 | USD 5 |
| 2024 | USD 14,600 | USD 21,900 | USD 29,200 | USD 5 |
| 2025 | USD 15,750 | USD 23,625 | USD 31,500 | USD 5 |

The MFS row matters most here: a married US person who files separately, for example one
married to a non-US spouse, has a return triggered by almost any income. For other ages and
years take the row from that year's Publication 501 (prior years are archived on irs.gov);
the 2026 edition is not out yet, so do not invent a TY2026 row. Gross income is not the only
trigger: Publication 501 also requires a return from anyone with net earnings from
self-employment of at least USD 400, so an osek patur or osek murshe under the threshold
still files (the SE tax itself belongs to `american-freelancer-israel-tax`). A low-income
employee can have no 1040 duty while an FBAR duty still exists, because the FBAR is a balance
test. Never tell a user they are delinquent on a 1040 before these tests have been applied.

When the spouse is not a US person, raise the filing-status choice instead of defaulting to
married filing separately. Publication 54 lets a US citizen married to a nonresident alien
choose to treat the spouse as a US resident and file jointly. Both are then treated as US
residents for income tax purposes for that year and all future years until the election is
terminated, neither can claim under any tax treaty not to be a US resident, and the spouse
needs an SSN or ITIN. Without that choice, a filer who pays more than half the cost of
maintaining a household for a qualifying dependent, other than the spouse, may be able to use
head of household status. Once the choice is made, both spouses must report worldwide income
for that and all future years unless it is suspended or terminated, so the Israeli spouse's
income comes onto the US return. Which route is better is a preparer's decision; record the facts.

Do not soften this or speculate about enforcement likelihood.

### Stage 2: Build the filing-obligation map

Ask for, and record, only what the downstream tests need:

| Input | Why it is needed |
|---|---|
| Tax year in question | Selects the FEIE amount and the deadline set |
| Gross worldwide income for the year, before any exclusion, and age | 1040 filing-threshold test |
| Filing status, and whether the spouse is a US person | Selects the Form 8938 threshold row |
| Highest combined balance across ALL foreign accounts at any point in the year | FBAR test |
| Total value of specified foreign financial assets, at year end and at peak | Form 8938 test |
| Days physically outside the US during the year | Bears on FEIE qualification and on the streamlined route |
| Whether any US return has been filed since arriving | Selects normal filing vs a catch-up route |

Then apply each test and record a yes or no with the reason.

**FBAR (FinCEN Form 114).** Required when the aggregate value of all foreign financial
accounts exceeds USD 10,000 at any time during the calendar year. Three points that are
routinely got wrong, so state them explicitly:

- The test is on the AGGREGATE across every account, not on any single account.
- It is a balance test, not an income test. An account that earned nothing still counts.
- It is a peak test. An account that touched the threshold for one day counts, even if it
  was empty on 31 December.

The FBAR reaches accounts the user has a financial interest in OR signature or other
authority over, such as bank, brokerage and mutual fund accounts. Ask explicitly about the
accounts Israelis forget: a bank account held jointly with a parent, a dormant account from a
previous employer, and any account the user can only sign on. Include kupat gemel and keren
hishtalmut balances in the aggregate provisionally until the preparer confirms their
treatment; never clear a user under USD 10,000 who left them out.

FBAR is filed to FinCEN through the BSA E-Filing System, separately from the tax return.

**Form 8938 (FATCA).** Thresholds depend on where the filer lives and on filing status, and
the abroad thresholds are four times the domestic ones. Use the abroad row for a user living
in Israel:

| Filer | Living outside the US | Living in the US |
|---|---|---|
| Unmarried, or married filing separately | More than USD 200,000 on the last day, or more than USD 300,000 at any time | More than USD 50,000 on the last day, or more than USD 75,000 at any time |
| Married filing jointly | More than USD 400,000 on the last day, or more than USD 600,000 at any time | More than USD 100,000 on the last day, or more than USD 150,000 at any time |

Form 8938 is filed WITH the 1040, and a taxpayer not required to file an income tax return is
not required to file Form 8938. The FBAR, by contrast, goes to FinCEN and is not filed with the
return. The IRS tells filers to check each form's requirements and thresholds and determine
whether they must file one, the other, or both, and each form has its own penalty regime.
Say so in as many words, because the belief that "the FBAR covers it" is widespread.

### Stage 3: Lay out both calendars

For a calendar-year filer living in Israel:

| Date | What is due | Mechanism |
|---|---|---|
| 15 April | 1040 regular due date. Interest on unpaid tax runs from here. | Interest date, whatever extension follows (Israel relief aside, below) |
| 15 April | FBAR regular due date | Filed to FinCEN |
| 15 June | 1040 and payment, on the automatic 2 month extension for taxpayers abroad | Automatic, but attach a statement to the return saying which situation qualified you |
| 15 October | 1040, if Form 4868 was filed BY 15 June | Must be requested, and requested in time |
| 15 December | 1040, discretionary extension for taxpayers out of the country, on top of the Form 4868 extension | Letter to the IRS explaining why, sent by 15 October; not automatic |
| 15 October | FBAR, on its automatic extension | Automatic, no request needed |
| Varies | 1040, Form 2350 extension for an arrival-year oleh who expects to meet the bona fide residence or physical presence test only after the due date | Must be requested; rules out the 15 December letter extension |

Two traps worth stating every time:

1. An extension to file is not an extension to pay. Interest runs on unpaid tax from
   15 April even when the filing extension is valid. For a filer who qualifies for the
   automatic 2 month extension, late-payment PENALTIES run from 15 June, but interest
   still runs from 15 April. The exception is the Israel relief below: for an act whose due
   date falls inside a postponement period, that period is disregarded in figuring interest
   and penalties. Have the preparer compute interest with any postponement applied.
2. Form 4868 has to be filed by the automatic 2 month extension date, not after it.
   A user who remembers in September has already missed the window for the October date.

**Israel relief: check it before applying the dates above.** Under IRS Notice 2026-63,
affected taxpayers have until 30 September 2027 to file tax returns, make tax payments and
perform certain time-sensitive acts that are due on or after 30 September 2026 and before
30 September 2027. Affected taxpayers include any individual whose principal residence is in
the State of Israel, the West Bank or Gaza, and anyone whose tax return preparer or necessary
records are located there. The IRS applies the relief automatically based on the address on
previously filed returns; an affected taxpayer whose principal residence is outside that area
should call the IRS disaster hotline. So for a resident of Israel, a 1040 for tax year 2026 that would
be due in 2027 falls inside the window. Check irs.gov for a later notice before relying on any
date after 30 September 2027.

For a never-filer this cuts both ways. Notice 2026-63 further postpones acts already postponed
under Notice 2025-53 and the earlier Israel notices, for taxpayers eligible under them, so some
recent 1040 years may not yet be past due. But the IRS identifies affected taxpayers automatically
from previously filed returns, which a never-filer does not have, and the FBAR years are not
covered at all. Which 1040 years are inside the chain, and how that shapes the streamlined
3-year window, is for the preparer to settle.

The FBAR is filed to FinCEN, not the IRS, and the IRS notice does not move it. FinCEN gave
Israel-affected filers their own FBAR extensions only for calendar years 2022 (to 7 October
2024) and 2023 (to 30 September 2025). No FinCEN notice for later years was found on
fincen.gov, so treat the FBAR's own 15 October extended date as the operative one unless the
user finds a newer FinCEN notice.

Align this against the user's Israeli deadline, but do not compute the Israeli return here.
Hand the Israeli side to `israeli-tax-returns`.

One Israeli change matters for the document pack. Israel's 10-year exemption from REPORTING
foreign income was cancelled by Amendment 272 to the Income Tax Ordinance, but only for olim
and long-term returning residents who attain that status from 1 January 2026; the 10-year
exemption from Israeli TAX on foreign-source income continues. So an oleh from 2026 lists
foreign income on the Israeli return as well, while an earlier oleh usually does not.
Separately, olim and long-term returning residents who arrived between 5 November 2025 and
31 December 2026 may be exempt from Israeli tax on Israeli-source personal-effort income for
2026 to 2030. Less Israeli tax paid means less to credit, so flag this cohort when the
exclusion-versus-credit question comes up in Stage 4. None of this changes the US filing duty.

### Stage 4: Compare FEIE against the Foreign Tax Credit

The exclusion amount is set per tax year by Revenue Procedure. Use the amount for the year
being filed, not the current year, and never take it from the IRS FEIE landing page, which
is stale (see Gotchas):

| Tax year | Foreign earned income exclusion |
|---|---|
| 2023 | USD 120,000 |
| 2024 | USD 126,500 |
| 2025 | USD 130,000 |
| 2026 | USD 132,900 |
| 2027 | USD 137,300 |

Check qualification before offering the exclusion at all. It requires a tax home in a
foreign country, income from personal services performed there, and either the bona fide
residence test or the physical presence test (present in a foreign country for 330 full
days during a period of 12 consecutive months). An oleh in the arrival year may not yet
qualify. The same abroad status also governs which Form 8938 row applies.

Frame the comparison as a decision with a lock-in, not as arithmetic:

- **The exclusion** removes qualifying foreign EARNED income from US gross income up to the
  cap. Income above the cap remains taxable. It never reaches pension and annuity income
  (including social security benefits), interest, ordinary dividends or capital gains, so a
  household living on investment or pension income gets nothing from it.
- **The Foreign Tax Credit** (Form 1116) offsets US tax with Israeli tax already paid.
  How far it reduces the US liability depends on the Form 1116 limitation, which is for the
  preparer to compute, but it involves no exclusion election and so none of the lock-in below.
- **They cannot be combined on the same income.** A credit may not be claimed for taxes on
  income excluded under the exclusion. They can be used in the same year on different
  income: exclude up to the cap, then take the credit on the portion that was not excluded.
- **The exclusion blocks the refundable child credit in the same year.** A filer who elects
  the exclusion cannot take the additional child tax credit for that year. For an oleh
  family with children this is often the deciding point, so raise it whenever children are
  in the household, including on every catch-up year. First check the precondition: the
  filer (or a spouse on a joint return) and each child need an SSN valid for employment,
  issued before the return's due date including extensions. Israeli-born children often
  have none, and without it the credit is not available whichever route is chosen.

Then the part that matters most, and that a bare comparison misses:

- Taking the credit on excluded income may be treated as REVOKING the exclusion election.
- Once revoked, the same exclusion cannot be chosen again for 5 years without IRS approval,
  obtained through a ruling request.
- Claiming the foreign tax credit, the additional child tax credit, or the earned income
  credit in a later year is itself treated as revoking a prior exclusion choice.

So a user who switches casually between the two, or who claims a child credit without
realising what it does to a standing election, can find the exclusion unavailable for years.
Flag the revocation consequence whenever the user proposes a switch, and route the decision
to a licensed preparer rather than making it.

Convert Israeli figures to USD before any of this. Use Bank of Israel representative rates
via the boi-exchange MCP where available, and record which date's rate was used.

### Stage 5: Catch-up routes if nothing was ever filed

For a user who has not filed since making aliyah, the Streamlined Foreign Offshore
Procedures are usually the relevant route. Check eligibility before describing it:

- **Non-residency test.** In one or more of the most recent 3 years for which the return due
  date has passed, the individual had no US abode AND was physically outside the United
  States for at least 330 full days. For a joint return, both spouses must meet it.
- **Non-willfulness.** The failure must have been non-willful. This is a judgement about the
  user's state of mind and it is not yours to make. Describe the requirement and refer it to
  counsel.
- **No open examination or investigation.** A taxpayer whose returns the IRS has put under
  civil examination for any year, or who is under IRS Criminal Investigation, cannot use the
  streamlined procedures.

What the route requires, noting that the two lookback periods differ:

| Component | Lookback |
|---|---|
| Delinquent or amended tax returns, with all required information returns | Most recent 3 years |
| Delinquent FBARs | Most recent 6 years |

"Most recent 3 years" means the 3 most recent years whose return due date (or properly
extended due date) has passed at the time of submission, and the FBAR window counts the
6 most recent years whose FBAR due date has passed. Work the concrete years out from the
submission date rather than quoting a range.

"All required information returns" is literal. The IRS names Forms 3520, 5471 and 8938 as
examples. A package without the Israeli fund, trust or company forms is incomplete, so hand
those to `us-person-israeli-investment-check` before the package is assembled.

The IRS page's mechanics decide whether the package is processed under the procedure at all:
"Streamlined Foreign Offshore" in red on each return and information return, a signed
Form 14653, paper submission to the Austin address (electronic is not accepted), FBARs
e-filed through BSA E-Filing with "Other" as the late-filing reason, and an ITIN application
for a filer not eligible for an SSN. The full list is in `references/filing-matrix.md`.

Full tax and interest must be paid with the submission. In exchange, an eligible filer who
follows the instructions is not subject to failure-to-file, failure-to-pay, accuracy-related,
information-return, or FBAR penalties.

The IRS designed the streamlined procedures for taxpayers whose failures did not result from
willful conduct, so they do not fit a user who carries willfulness risk. Do not default
everyone to them. The other routes the IRS lists, each for a different fact pattern:

- **IRS Criminal Investigation Voluntary Disclosure Practice.** For someone who WILLFULLY failed
  to comply. It requires a statement acknowledging the willful failure, and it is only timely
  before the IRS has started a civil examination or criminal investigation or received
  third-party information about the noncompliance.
- **Delinquent international information return submission procedures.** For missing
  information returns only, by someone not under civil examination or criminal investigation
  and not already contacted by the IRS about them. Penalties may still be assessed; a
  reasonable cause statement can be attached.
- **Late FBARs alone.** Where the income was reported and the tax paid, the Taxpayer Advocate
  Service says to file them through the normal online system with a statement explaining the
  delay, with no penalty if the IRS has not already contacted the filer about an audit or
  delinquent returns for those years. The old IRS page for this procedure is withdrawn.

Route the choice of route to a licensed preparer or counsel.

### Stage 6: State the exposure honestly, then the document pack

Give the penalty picture with both prongs, because quoting only the fixed figure understates
willful exposure badly on a large account:

| Violation | Statutory maximum | Inflation adjusted |
|---|---|---|
| Non-willful, per report (not per account) | USD 10,000 | USD 16,536 |
| Willful, per violation | USD 100,000 | USD 165,353 |

The non-willful maximum accrues per REPORT, not per account (Bittner v. United States, 2023),
so never multiply it by the number of Israeli accounts.

For a willful violation the penalty is the GREATER of the adjusted amount or 50 percent of
the balance in the account at the time of the violation. On a large account the percentage
prong dominates and the dollar figure is close to irrelevant.

Separately, seriously delinquent tax debt that the IRS certifies to the State Department can
block the issue or renewal of a US passport, or lead to its revocation. That is a reason not
to let a known gap sit.

These amounts are adjusted for inflation annually, but no annual inflation adjustment was
made for calendar year 2026, so the amounts above remain the operative ones. Re-check the
table rather than assuming a new figure exists.

Close by producing the deliverable: a document checklist split by who needs what.

| For the Israeli accountant | For the US preparer | Exists only on one side |
|---|---|---|
| Not needed | SSN, or the status of an SSN application, for the filer, spouse and each child | Decides the child credit and the joint-return route |
| The annual employer summary | Same, translated and converted to USD | The preparer maps it onto the US return |
| The annual bank statement of interest and investment income | Same, with per-account detail for FBAR and 8938 | Peak balances are needed for US only |
| Israeli return once filed | Israeli tax paid, by date, for the credit | The preparer confirms which year each payment is credited in |

### Stage 7: Hand off

State clearly what remains for a licensed professional: the non-willfulness judgement, the
FEIE-versus-credit election, and the preparation and signing of every form. Offer the
worksheet as the thing to bring to that meeting.

## Do NOT use this skill for

- Preparing, completing, signing or submitting any return, on either side.
- Israeli-side return mechanics. Use `israeli-tax-returns`.
- Deciding whether an Israeli fund, keren hishtalmut or kupat gemel is a PFIC or a foreign
  trust, and which of Forms 8621, 3520 or 3520-A it triggers. Use
  `us-person-israeli-investment-check`.
- Self-employment tax for an osek patur or osek murshe who is a US person, including how
  social security contributions interact across the two systems. Use
  `american-freelancer-israel-tax`.
- Renunciation of citizenship and the section 877A exit tax.
- State income tax. If the user kept a home or other ties in a former US state, flag it for the
  preparer; whether that state still expects a return is outside this skill.
- Any judgement about whether a past failure to file was willful.

## Recommended MCP Servers

| MCP | Use in this skill |
|---|---|
| `boi-exchange` | Bank of Israel representative rates for converting Israeli figures to USD. Record the rate date used, because the credit and the exclusion are computed on translated amounts. |
| `kolzchut` | Israeli-side entitlement and procedure background when the user asks how the Israeli half works. |

## Bundled Resources

| Path | Contents |
|---|---|
| `references/domain-checklist.md` | Coverage contract for this skill, with the primary source behind each item and the known bad figures not to regress to |
| `references/filing-matrix.md` | The thresholds, deadlines, and penalty tables in one place for quick lookup |
| `scripts/filing_map.py` | Applies the FBAR and 8938 threshold tests to a set of inputs and prints a filing-obligation map |
| `evidence.json` | Every factual claim in this skill with its source URL and a verbatim snippet |

## Gotchas

Agent failure modes specific to this domain.

1. **Quoting the IRS FEIE landing page for the exclusion amount.** That page lists only 2020
   through 2023 and is stale. An agent that reads it will confidently state USD 120,000 for a
   2026 filing. Take the amount from the Revenue Procedure for the tax year in question.
2. **Using the domestic Form 8938 thresholds for a user living in Israel.** The 50,000 and
   75,000 figures in secondary guides are the wrong row and invent a duty the user lacks.
3. **Treating FBAR as a per-account or year-end test.** It is aggregate and it is peak. An
   agent that asks only for year-end balances will clear a user who in fact had to file.
4. **Getting either FBAR penalty prong wrong.** Willful is the greater of the dollar figure
   or 50 percent of the balance; non-willful is per report, not per account.
5. **Quoting a superseded Israel relief notice.** The IRS rolls the Israel postponement
   forward each autumn (2023-71, 2024-72, 2025-53, 2026-63). Check for the newest notice
   before stating any deadline, and never assume it moves the FBAR.
6. **Recommending a switch between the exclusion and the credit as if it were free.** It can
   revoke the election and bar it for 5 years, and the additional child tax credit can
   trigger the same revocation without the user ever intending it. Always surface the
   lock-in before discussing which option produces a lower number this year.
7. **Assuming a treaty prevents US taxation of a dual citizen.** The savings clause preserves
   exactly that taxation. What survives it is the relief machinery, notably Article 26. An
   agent that says "the treaty protects you" has it backwards.
8. **Answering the non-willfulness question.** Streamlined eligibility turns on the user's
   state of mind. Describe the requirement, never adjudicate it.

## Reference Links

| Source | URL | What to check |
|---|---|---|
| IRS, US citizens and resident aliens abroad | https://www.irs.gov/individuals/international-taxpayers/us-citizens-and-resident-aliens-abroad | Abroad extensions |
| IRS, reporting foreign bank and financial accounts | https://www.irs.gov/newsroom/details-on-reporting-foreign-bank-and-financial-accounts | FBAR threshold, deadlines |
| IRS, comparison of Form 8938 and FBAR | https://www.irs.gov/businesses/comparison-of-form-8938-and-fbar-requirements | 8938 rows; independent duties |
| Rev. Proc. 2026-35 | https://www.irs.gov/pub/irs-drop/rp-26-35.pdf | TY2027 exclusion (item .41) |
| Rev. Proc. 2025-32 | https://www.irs.gov/pub/irs-drop/rp-25-32.pdf | TY2026 exclusion (item .39) |
| IRS, streamlined filing compliance procedures | https://www.irs.gov/individuals/international-taxpayers/streamlined-filing-compliance-procedures | Examination and investigation bar |
| IRS, foreign tax credit | https://www.irs.gov/individuals/international-taxpayers/foreign-tax-credit | No credit on excluded income |
| IRS Publication 54 | https://www.irs.gov/publications/p54 | Revocation, child credit bar, tests, extensions, spouse election |
| IRS Notice 2026-63 | https://www.irs.gov/pub/irs-drop/n-26-63.pdf | Israel relief to 30 September 2027 |
| FinCEN Israel FBAR relief (CY2023) | https://www.fincen.gov/sites/default/files/shared/FinCEN-FBAR-Israel-Related-Relief-Notice-FINAL508.pdf | Last FinCEN Israel FBAR relief |
| Instructions for Form 2555 | https://www.irs.gov/pub/irs-pdf/i2555.pdf | Income that is never foreign earned income |
| IRS Criminal Investigation Voluntary Disclosure Practice | https://www.irs.gov/compliance/criminal-investigation/irs-criminal-investigation-voluntary-disclosure-practice | Willfulness statement, timeliness |
| Delinquent international information return procedures | https://www.irs.gov/individuals/international-taxpayers/delinquent-international-information-return-submission-procedures | Eligibility, reasonable cause |
| Taxpayer Advocate Service, FBAR | https://www.taxpayeradvocate.irs.gov/get-help/international/foreign-bank-financial-accounts/ | Late FBARs |
| Amendment 272 summary (Shibolet) | https://www.shibolet.com/en/cancellation-of-reporting-exemption-for-new-immigrants-and-long-term-returning-residents-regarding-foreign-income-and-new-reporting-obligation-for-israeli-resident-trustees-regarding-trusts/ | Israeli reporting exemption change |
| IRS Publication 501 | https://www.irs.gov/publications/p501 | Filing thresholds, USD 400 SE trigger; prior years at irs.gov/pub/irs-prior/p501--YEAR.pdf |
| Treas. Reg. 301.7508A-1 | https://www.law.cornell.edu/cfr/text/26/301.7508A-1 | Postponement and interest |
| Bittner v. United States | https://www.supremecourt.gov/opinions/22pdf/21-1195_h3ci.pdf | Non-willful FBAR penalty per report |
| IRS, streamlined foreign offshore procedures | https://www.irs.gov/individuals/international-taxpayers/u-s-taxpayers-residing-outside-the-united-states | 330 days, 3 and 6 year lookbacks, relief |
| 31 CFR 1010.821 | https://www.govinfo.gov/content/pkg/CFR-2025-title31-vol3/xml/CFR-2025-title31-vol3-sec1010-821.xml | Adjusted FBAR penalties |
| IRM 4.26.16 | https://www.irs.gov/irm/part4/irm_04-026-016 | Willful 50 percent prong |
| US-Israel income tax treaty | https://www.irs.gov/pub/irs-trty/israel.pdf | Article 6(3) and 6(4) |

## Troubleshooting

| Symptom | Cause | What to do |
|---|---|---|
| The user insists they owe nothing so there is nothing to file | Conflating tax liability with filing duty | Separate the two. The 1040, the FBAR and the 8938 are each triggered independently of whether tax is owed. |
| Two sources give different exclusion amounts | One of them is keyed to a different tax year, or is the stale IRS landing page | Resolve by tax year against the Revenue Procedure. Do not average or pick the larger. |
| The FBAR total looks lower than expected | Peak balances were not collected, or kupat gemel, keren hishtalmut and signature-authority accounts were omitted | Re-ask for the highest balance each account reached at any point, and enumerate the account types explicitly. |
| A user who took a child credit now cannot use the exclusion | The credit was treated as revoking the prior election, which triggers the 5 year bar | Confirmed behaviour per Publication 54. This needs a licensed preparer, and possibly a ruling request. Do not attempt to undo it in conversation. |
| An IRS page will not load or shows an unexpected 404 | IRS reorganises international-taxpayer URLs regularly | Search irs.gov for the page title before concluding it was withdrawn. |
| The user asks which figure applies to their own facts | This is the reserved judgement the skill does not make | Give the rule and the source, produce the worksheet, and route the determination to a licensed adviser. |
