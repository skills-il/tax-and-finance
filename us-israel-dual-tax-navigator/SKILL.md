---
name: us-israel-dual-tax-navigator
description: "Not tax advice and not a filed return. Maps what a US-Israel dual citizen actually has to file in both systems for a tax year: the US 1040, FBAR (FinCEN 114), Form 8938, and how those line up against the Israeli calendar. Compares the Foreign Earned Income Exclusion against the Foreign Tax Credit, flags the revocation trap, and lays out the Streamlined Foreign Offshore route for someone who never filed after making aliyah. Use when a US citizen or green card holder in Israel asks what they owe the IRS, whether they need an FBAR, which years to catch up, or how to brief an accountant. Produces a filing-obligation map and a document checklist, never a completed or signed return. Do NOT use for Israeli-side filing, for classifying Israeli funds as PFICs, for self-employment tax, or for renouncing citizenship."
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
assuming a value, and never state a figure that is not in Reference Links.

### Stage 1: Establish the filing premise

Confirm the user is a US person: a US citizen (including a dual citizen who has never lived
in the US) or a lawful permanent resident. If so, state plainly that US taxation follows
citizenship, not residence, and that the duty to file a 1040 on worldwide income survives
aliyah and survives owing zero US tax.

The 1040 duty is not automatic, though. It turns on gross income against the filing
threshold for the filer's status and age, and for this test gross income INCLUDES income
the foreign earned income exclusion would later remove. For tax year 2025: single under 65
USD 15,750; married filing jointly, both under 65, USD 31,500; married filing SEPARATELY, at
any age, USD 5. The last row matters most here: a married US person who files separately, for
example one married to a non-US spouse, has a return triggered by almost any income. Take other rows from
Publication 501 for the tax year, since the table changes every year. A low-income single
filer can have no 1040 duty while an FBAR duty still exists, because the FBAR is a balance
test.
Never tell a user they are delinquent on a 1040 before this test has been applied.

Do not soften this and do not speculate about enforcement likelihood. Establish it, then
move on.

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
previous employer, and any account the user can only sign on. Also list kupat gemel and keren
hishtalmut balances, and have the preparer confirm how each is treated rather than assuming.

FBAR is filed to FinCEN through the BSA E-Filing System, separately from the tax return.

**Form 8938 (FATCA).** Thresholds depend on where the filer lives and on filing status, and
the abroad thresholds are four times the domestic ones. Use the abroad row for a user living
in Israel:

| Filer | Living outside the US | Living in the US |
|---|---|---|
| Unmarried, or married filing separately | More than USD 200,000 on the last day, or more than USD 300,000 at any time | More than USD 50,000 on the last day, or more than USD 75,000 at any time |
| Married filing jointly | More than USD 400,000 on the last day, or more than USD 600,000 at any time | More than USD 100,000 on the last day, or more than USD 150,000 at any time |

Form 8938 is filed WITH the 1040, while the FBAR goes to FinCEN and is not filed with the
return. The IRS tells filers to check each form's requirements and thresholds and determine
whether they must file one, the other, or both, and each form has its own penalty regime.
Say so in as many words, because the belief that "the FBAR covers it" is widespread.

### Stage 3: Lay out both calendars

For a calendar-year filer living in Israel:

| Date | What is due | Mechanism |
|---|---|---|
| 15 April | 1040 regular due date. Interest on unpaid tax runs from here. | Interest date, whatever extension follows |
| 15 April | FBAR regular due date | Filed to FinCEN |
| 15 June | 1040 and payment, on the automatic 2 month extension for taxpayers abroad | Automatic, but attach a statement to the return saying which situation qualified you |
| 15 October | 1040, if Form 4868 was filed BY 15 June | Must be requested, and requested in time |
| 15 December | 1040, discretionary extension for taxpayers out of the country, on top of the Form 4868 extension | Letter to the IRS explaining why, sent by 15 October; not automatic |
| 15 October | FBAR, on its automatic extension | Automatic, no request needed |

Two traps worth stating every time:

1. An extension to file is not an extension to pay. Interest runs on unpaid tax from
   15 April even when the filing extension is valid. For a filer who qualifies for the
   automatic 2 month extension, late-payment PENALTIES run from 15 June, but interest
   still runs from 15 April.
2. Form 4868 has to be filed by the automatic 2 month extension date, not after it.
   A user who remembers in September has already missed the window for the October date.

**Israel relief: check it before applying the dates above.** Under IRS Notice 2025-53,
affected taxpayers have until 30 September 2026 to file tax returns and make tax payments
that fall due on or after 30 September 2025 and before 30 September 2026. Affected taxpayers
include any individual whose principal residence is in the State of Israel, the West Bank or
Gaza, and also, for example, anyone whose tax return preparer or necessary records are
located there. The IRS applies the relief automatically based on the address on previously
filed returns; an affected taxpayer whose principal residence is outside that area must call
the IRS disaster hotline to request it. The notice's list of postponed acts names returns and
payments of income tax and other federal taxes and does not name the FBAR, which is filed to FinCEN, so
confirm FBAR treatment separately. A date on or after 30 September 2026, such as 15 October
2026, is outside this notice. Check irs.gov for any later notice before relying on a date.

Align this against the user's Israeli deadline, but do not compute the Israeli return here.
Hand the Israeli side to `israeli-tax-returns`.

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

Check qualification before offering the exclusion at all. It requires a tax home in a
foreign country, income from personal services performed there, and either the bona fide
residence test or the physical presence test (present in a foreign country for 330 full
days during a period of 12 consecutive months). An oleh in the arrival year may not yet
qualify. The same abroad status also governs which Form 8938 row applies.

Frame the comparison as a decision with a lock-in, not as arithmetic:

- **The exclusion** removes qualifying foreign EARNED income from US gross income up to the
  cap. Income above the cap remains taxable.
- **The Foreign Tax Credit** (Form 1116) offsets US tax with Israeli tax already paid.
  How far it reduces the US liability depends on the Form 1116 limitation, which is for the
  preparer to compute, but it involves no exclusion election and so none of the lock-in below.
- **They cannot be combined on the same income.** A credit may not be claimed for taxes on
  income excluded under the exclusion. They can be used in the same year on different
  income: exclude up to the cap, then take the credit on the portion that was not excluded.
- **The exclusion blocks the refundable child credit in the same year.** A filer who elects
  the exclusion cannot take the additional child tax credit for that year. For an oleh
  family with children this is often the deciding point, so raise it whenever children are
  in the household, including on every catch-up year.

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

### Stage 5: Choose the catch-up route if nothing was ever filed

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

The mechanics the IRS page states, which decide whether the package is processed under the
procedure at all:

- Write "Streamlined Foreign Offshore" in red at the top of the first page of each return
  and each information return.
- Complete and sign Form 14653, the certification of eligibility and non-willfulness.
- Send the returns and payment in paper form to the Austin address given on the IRS page.
  Electronic submissions are not accepted.
- File the delinquent FBARs electronically through the BSA E-Filing System, select "Other"
  as the late-filing reason, and state that they are filed under the Streamlined Filing
  Compliance Procedures.
- A filer not eligible for a Social Security number submits an ITIN application with the
  package.

Full tax and interest must be paid with the submission. In exchange, an eligible filer who
follows the instructions is not subject to failure-to-file, failure-to-pay, accuracy-related,
information-return, or FBAR penalties.

The IRS designed the streamlined procedures for taxpayers whose failures did not result from
willful conduct, so they do not fit a user who carries willfulness risk. Do not default
everyone to them: route the choice of route to a licensed preparer or counsel.

### Stage 6: State the exposure honestly, then the document pack

Give the penalty picture with both prongs, because quoting only the fixed figure understates
willful exposure badly on a large account:

| Violation | Statutory maximum | Inflation adjusted |
|---|---|---|
| Non-willful, per report (not per account) | USD 10,000 | USD 16,536 |
| Willful, per violation | USD 100,000 | USD 165,353 |

For a non-willful violation, the maximum accrues per REPORT, not per account: the US Supreme
Court held in Bittner v. United States (2023) that the non-willful maximum applies to the
failure to file a compliant report. Do not multiply the non-willful figure by the number of
Israeli accounts.

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
   75,000 figures are everywhere in secondary guides, and they are the wrong row. Abroad
   filers get 200,000 and 300,000, or 400,000 and 600,000 when filing jointly. Using the
   domestic row invents a filing duty the user does not have.
3. **Treating FBAR as a per-account or year-end test.** It is aggregate and it is peak. An
   agent that asks only for year-end balances will clear a user who in fact had to file.
4. **Getting either FBAR penalty prong wrong.** The willful penalty is the greater of
   165,353 or 50 percent of the balance, so the flat figure understates a large account.
   The non-willful maximum is per report under Bittner, so multiplying it by the account
   count overstates it several-fold.
5. **Recommending a switch between the exclusion and the credit as if it were free.** It can
   revoke the election and bar it for 5 years, and the additional child tax credit can
   trigger the same revocation without the user ever intending it. Always surface the
   lock-in before discussing which option produces a lower number this year.
6. **Assuming a treaty prevents US taxation of a dual citizen.** The savings clause preserves
   exactly that taxation. What survives it is the relief machinery, notably Article 26. An
   agent that says "the treaty protects you" has it backwards.
7. **Answering the non-willfulness question.** Streamlined eligibility turns on the user's
   state of mind. Describe the requirement, never adjudicate it.

## Reference Links

| Source | URL | What to check |
|---|---|---|
| IRS, US citizens and resident aliens abroad | https://www.irs.gov/individuals/international-taxpayers/us-citizens-and-resident-aliens-abroad | The 15 June automatic extension and the Form 4868 timing |
| IRS, reporting foreign bank and financial accounts | https://www.irs.gov/newsroom/details-on-reporting-foreign-bank-and-financial-accounts | The USD 10,000 aggregate threshold and FBAR deadlines |
| IRS, comparison of Form 8938 and FBAR | https://www.irs.gov/businesses/comparison-of-form-8938-and-fbar-requirements | The abroad vs domestic threshold rows, and that the duties are independent |
| Rev. Proc. 2025-32 | https://www.irs.gov/pub/irs-drop/rp-25-32.pdf | Item .39 for the TY2026 exclusion amount |
| Rev. Proc. 2024-40 | https://www.irs.gov/pub/irs-drop/rp-24-40.pdf | Item .39 for the TY2025 exclusion amount |
| Rev. Proc. 2023-34 | https://www.irs.gov/pub/irs-drop/rp-23-34.pdf | Item .39 for the TY2024 exclusion amount |
| Rev. Proc. 2022-38 | https://www.irs.gov/pub/irs-drop/rp-22-38.pdf | Item .39 for the TY2023 exclusion amount |
| IRS, streamlined filing compliance procedures | https://www.irs.gov/individuals/international-taxpayers/streamlined-filing-compliance-procedures | The civil examination and criminal investigation bar |
| IRS, foreign tax credit | https://www.irs.gov/individuals/international-taxpayers/foreign-tax-credit | That no credit is available on excluded income |
| IRS Publication 54 | https://www.irs.gov/publications/p54 | Revocation and the 5 year bar, the same-year child credit bar, the qualification tests, the extension chain |
| IRS Notice 2025-53 | https://www.irs.gov/pub/irs-drop/n-25-53.pdf | Israel relief: who is an affected taxpayer, which acts are postponed, the 30 September 2026 end date |
| IRS Publication 501 | https://www.irs.gov/publications/p501 | The 1040 gross-income filing thresholds for the tax year |
| Bittner v. United States | https://www.supremecourt.gov/opinions/22pdf/21-1195_h3ci.pdf | The non-willful FBAR maximum accrues per report |
| IRS, streamlined foreign offshore procedures | https://www.irs.gov/individuals/international-taxpayers/u-s-taxpayers-residing-outside-the-united-states | The 330 day test, the 3 and 6 year lookbacks, and the penalty relief |
| 31 CFR 1010.821 | https://www.govinfo.gov/content/pkg/CFR-2025-title31-vol3/xml/CFR-2025-title31-vol3-sec1010-821.xml | The current adjusted FBAR penalty amounts |
| IRM 4.26.16 | https://www.irs.gov/irm/part4/irm_04-026-016 | The 50 percent of balance prong for willful violations |
| US-Israel income tax treaty | https://www.irs.gov/pub/irs-trty/israel.pdf | Article 6(3) savings clause and the 6(4) carve-outs |

## Troubleshooting

| Symptom | Cause | What to do |
|---|---|---|
| The user insists they owe nothing so there is nothing to file | Conflating tax liability with filing duty | Separate the two. The 1040, the FBAR and the 8938 are each triggered independently of whether tax is owed. |
| Two sources give different exclusion amounts | One of them is keyed to a different tax year, or is the stale IRS landing page | Resolve by tax year against the Revenue Procedure. Do not average or pick the larger. |
| The FBAR total looks lower than expected | Peak balances were not collected, or kupat gemel, keren hishtalmut and signature-authority accounts were omitted | Re-ask for the highest balance each account reached at any point, and enumerate the account types explicitly. |
| A user who took a child credit now cannot use the exclusion | The credit was treated as revoking the prior election, which triggers the 5 year bar | Confirmed behaviour per Publication 54. This needs a licensed preparer, and possibly a ruling request. Do not attempt to undo it in conversation. |
| An IRS page will not load or shows an unexpected 404 | IRS reorganises international-taxpayer URLs regularly | Search irs.gov for the page title rather than assuming the content was withdrawn. Verified working URLs are in Reference Links. |
| The user asks which figure applies to their own facts | This is the reserved judgement the skill does not make | Give the rule and the source, produce the worksheet, and route the determination to a licensed adviser. |
