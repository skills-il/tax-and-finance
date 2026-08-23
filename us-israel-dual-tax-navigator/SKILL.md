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

Do not soften this and do not speculate about enforcement likelihood. Establish it, then
move on.

### Stage 2: Build the filing-obligation map

Ask for, and record, only what the downstream tests need:

| Input | Why it is needed |
|---|---|
| Tax year in question | Selects the FEIE amount and the deadline set |
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

Israeli accounts that commonly count and get forgotten: a bank account held jointly with a
parent, a dormant account from a previous employer, kupat gemel and keren hishtalmut
balances, and any account the user only has signature authority over.

FBAR is filed to FinCEN through the BSA E-Filing System, separately from the tax return.

**Form 8938 (FATCA).** Thresholds depend on where the filer lives and on filing status, and
the abroad thresholds are four times the domestic ones. Use the abroad row for a user living
in Israel:

| Filer | Living outside the US | Living in the US |
|---|---|---|
| Unmarried, or married filing separately | More than USD 200,000 on the last day, or more than USD 300,000 at any time | More than USD 50,000 on the last day, or more than USD 75,000 at any time |
| Married filing jointly | More than USD 400,000 on the last day, or more than USD 600,000 at any time | More than USD 100,000 on the last day, or more than USD 150,000 at any time |

Form 8938 is filed WITH the 1040. It does not replace the FBAR and the FBAR does not replace
it. The same account is frequently reported on both, each carries its own penalty, and
satisfying one duty does nothing for the other. Say so in as many words, because the belief
that "the FBAR covers it" is widespread.

### Stage 3: Lay out both calendars

For a calendar-year filer living in Israel:

| Date | What is due | Mechanism |
|---|---|---|
| 15 April | 1040 regular due date. Any tax owed is due now. | Payment date, whatever extension follows |
| 15 April | FBAR regular due date | Filed to FinCEN |
| 15 June | 1040, on the automatic 2 month extension for taxpayers abroad | Automatic, no request needed |
| 15 October | 1040, if Form 4868 was filed BEFORE 15 June | Must be requested, and requested in time |
| 15 October | FBAR, on its automatic extension | Automatic, no request needed |

Two traps worth stating every time:

1. An extension to file is not an extension to pay. Interest runs on unpaid tax from
   15 April even when the filing extension is valid.
2. Form 4868 has to be filed before the automatic 2 month extension date, not after it.
   A user who remembers in September has already missed the window for the October date.

Align this against the user's Israeli deadline, but do not compute the Israeli return here.
Hand the Israeli side to `israeli-tax-returns`.

### Stage 4: Compare FEIE against the Foreign Tax Credit

The exclusion amount is set per tax year by Revenue Procedure. Use the amount for the year
being filed, not the current year, and never take it from the IRS FEIE landing page, which
is stale (see Gotchas):

| Tax year | Foreign earned income exclusion |
|---|---|
| 2025 | USD 130,000 |
| 2026 | USD 132,900 |

Frame the comparison as a decision with a lock-in, not as arithmetic:

- **The exclusion** removes qualifying foreign EARNED income from US gross income up to the
  cap. It does nothing for investment income, and income above the cap remains taxable.
- **The Foreign Tax Credit** (Form 1116) offsets US tax with Israeli tax already paid.
  Because Israeli effective rates on salary are frequently at or above US rates, the credit
  often wipes out the US liability on the same income the exclusion would have removed, and
  unlike the exclusion it can generate carryforward and it reaches investment income.
- **They cannot be combined on the same income.** A credit may not be claimed for taxes on
  income excluded under the exclusion.

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
  user's state of mind and it is not yours to make. Describe the requirement and send it to
  counsel.

What the route requires, noting that the two lookback periods differ:

| Component | Lookback |
|---|---|
| Delinquent or amended tax returns, with all required information returns | Most recent 3 years |
| Delinquent FBARs | Most recent 6 years |

Full tax and interest must be paid with the submission. In exchange, an eligible filer who
follows the instructions is not subject to failure-to-file, failure-to-pay, accuracy-related,
information-return, or FBAR penalties.

Where the returns are correct and only FBARs are missing, the lighter delinquent-FBAR
submission procedure may fit instead. Mention it rather than defaulting everyone to
streamlined.

### Stage 6: State the exposure honestly, then the document pack

Give the penalty picture with both prongs, because quoting only the fixed figure understates
willful exposure badly on a large account:

| Violation | Statutory maximum | Inflation adjusted |
|---|---|---|
| Non-willful, per violation | USD 10,000 | USD 16,536 |
| Willful, per violation | USD 100,000 | USD 165,353 |

For a willful violation the penalty is the GREATER of the adjusted amount or 50 percent of
the balance in the account at the time of the violation. On a large account the percentage
prong dominates and the dollar figure is close to irrelevant.

These amounts are adjusted for inflation annually, but no annual inflation adjustment was
made for calendar year 2026, so the amounts above remain the operative ones. Re-check the
table rather than assuming a new figure exists.

Close by producing the deliverable: a document checklist split by who needs what.

| For the Israeli accountant | For the US preparer | Exists only on one side |
|---|---|---|
| The annual employer summary | Same, translated and converted to USD | The Israeli annual employer summary has no US equivalent |
| The annual bank statement of interest and investment income | Same, with per-account detail for FBAR and 8938 | Peak balances are needed for US only |
| Israeli return once filed | Israeli tax paid, by date, for the credit | Payment dates drive the credit year |

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
- Self-employment tax for an osek patur or osek murshe who is a US person, including the
  consequences of there being no US-Israel totalization agreement. Use
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
4. **Quoting the willful FBAR penalty as a flat 165,353.** The statute gives the greater of
   that or 50 percent of the balance. On a large account the flat figure is a serious
   understatement.
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
| IRS, foreign tax credit | https://www.irs.gov/individuals/international-taxpayers/foreign-tax-credit | That no credit is available on excluded income |
| IRS Publication 54 | https://www.irs.gov/publications/p54 | Revocation of the exclusion and the 5 year bar |
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
