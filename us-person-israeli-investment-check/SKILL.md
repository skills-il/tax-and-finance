---
name: us-person-israeli-investment-check
description: "Not tax advice and not a filed return. Screens the Israeli savings and investment products a US person holds, keren hishtalmut, kupat gemel, pension, kranot neemanut, TASE ETFs, bituach menahalim, for two separate US exposures: whether the holding is a PFIC needing Form 8621, and whether it is a foreign trust needing Forms 3520 and 3520-A. Walks the actual statutory tests and the Revenue Procedure 2020-17 exemption criteria rather than guessing, and outputs a per-product table saying which test each product passes or fails and what to ask a preparer. Use when a US citizen or green card holder in Israel asks whether their keren hishtalmut, pension, kupat gemel or Israeli fund creates a US reporting problem, or is deciding what to buy. Do NOT use for annual filing mechanics or FBAR, for Israeli-side tax, for self-employment tax, or to obtain a final classification of any specific product."
license: MIT
---

# US-Person Israeli Investment Check

## Legal notice

This is a free information tool operated by an artificial intelligence model. It applies
published statutory tests and the criteria in a published Revenue Procedure to product
features you describe, and produces a screening table. It does all of this without the
involvement, review, or approval of a licensed tax adviser, accountant, or attorney.

It is not tax advice, it is not a filed return, and it is not a professional opinion. It does
not, and cannot, give you a final classification of any product. The IRS has never issued
guidance naming Israeli savings products, whether a particular arrangement is a foreign trust
or a PFIC for US purposes turns on that specific plan's terms and on that specific fund's
holdings, and practitioners genuinely differ. What this tool produces is a preliminary
screening worksheet: which test a product appears to pass or fail, and the question to put to
a preparer. It does not read your plan documents, does not examine any fund's actual holdings,
does not make or evaluate any election, and does not prepare any form.

An AI model can err, omit data, or present a wrong conclusion. Any text it produces is an
automatic draft for personal organisation only and must never be submitted to any authority
as it stands.

Responsibility for reporting and for paying tax is yours, the binding assessment is made by
the tax authority concerned, whether the Israeli Tax Authority or the IRS, and representation
before a tax authority is reserved to those permitted to do so by law. This tool is not a
substitute for advice that takes into account the particular data and needs of each person.
Criteria and thresholds change, so verify each one against the primary sources under
Reference Links before relying on it.

## Problem

An Israeli employee is enrolled by default into exactly the products the US tax code treats
worst. A keren hishtalmut is tax free in Israel and may be a reportable foreign trust in the
US. A kranot neemanut or a TASE ETF is an ordinary savings choice in Israel and is very likely
a PFIC, taxed under a punitive default regime designed to remove the benefit of deferral.
Most people discover this years later, holding a decade of unreported positions, because
nothing in the Israeli sales process mentions it and most online guidance either overstates
the problem or waves it away.

## Instructions

The output of this skill is a screening table plus a list of questions for a preparer. It is
never a final classification. Say so at the start and at the end.

### Stage 1: Inventory what the user actually holds

Ask for each holding by name and record five things. Do not proceed on assumptions, because
the classification turns on precisely these details:

| Field | Why it decides the answer |
|---|---|
| Product name and provider | Distinguishes a pension from a gemel from a hishtalmut |
| Roughly what it holds | Pooled securities points at PFIC, a pure deposit usually does not |
| Who contributes and from what | Section 5.03 accepts only earned-income contributions |
| Annual and lifetime contribution amounts, in USD | The exemption criteria are hard dollar limits |
| Withdrawal conditions | The single criterion most Israeli products fail |

### Stage 2: Treat the two questions as separate

This is the structural point users and guides both get wrong. There are two independent
regimes and a product can fall in one, both, or neither:

- **Is it a PFIC?** A question about a foreign CORPORATION whose stock the user owns. Leads to
  Form 8621.
- **Is it a foreign trust?** A question about an ARRANGEMENT the user is treated as owning or
  transacting with. Leads to Forms 3520 and 3520-A.

Never answer one and present it as the answer to the other. Run both.

### Stage 3: The PFIC screen

A foreign corporation is a PFIC if it meets either test:

| Test | Threshold | Authority |
|---|---|---|
| Income test | 75 percent or more of gross income is passive | section 1297(b) |
| Asset test | At least 50 percent of average assets produce, or are held to produce, passive income | section 1297(e) |

A pooled investment fund holding securities meets both comfortably. That is why an Israeli
kranot neemanut, a TASE-listed ETF, and most Israeli pooled funds are treated as PFICs by
practitioners as a matter of course. Note that this is an inference from the tests applied to
what such funds hold, not an IRS determination about any named Israeli fund.

**The de minimis filing exception, which is widely missed.** Form 8621 filing is excepted
where the PFIC stock the user owns is worth USD 25,000 or less, or USD 50,000 or less on a
joint return, on the last day of the tax year and on any day they disposed of stock. Check
this before telling anyone they have a filing obligation. A modest TASE ETF position often
falls under it.

Two cautions on the exception. It is an exception to FILING Form 8621, and it does not change
how a distribution or a gain is taxed. It also does not affect any other duty, so a holding
under the threshold can still be reportable elsewhere.

**Why the default regime is the problem.** A shareholder of a section 1291 fund is subject to
special rules on an excess distribution, and the ENTIRE gain on disposing of a section 1291
fund is treated as an excess distribution. That default allocates the amount back across the
holding period with an interest charge, which is what removes the benefit of deferral. There
are elections that avoid it, a qualified electing fund election and a mark-to-market election,
but a QEF election requires information from the fund that Israeli funds generally do not
produce for US holders. Explain the shape of this and route the election to a preparer. Do not
recommend an election.

### Stage 4: The foreign trust screen and the Revenue Procedure 2020-17 exemption

First state the limit of the exemption, because it is the most misreported point in this
domain: Revenue Procedure 2020-17 provides an exemption ONLY from the section 6048 information
reporting requirements. It does not change how anything is taxed. A product can be exempt from
Forms 3520 and 3520-A and still produce currently taxable income.

Also state the gating condition: only eligible individuals, generally those already compliant
with the income tax obligations relating to the trust, may rely on it. Someone who has never
filed cannot reach for this exemption as a first move, which is why the catch-up question in
`us-israel-dual-tax-navigator` usually comes first.

Then walk the criteria against the product.

**Section 5.03, tax-favored foreign retirement trust.** The trust must operate exclusively or
almost exclusively to provide pension or retirement benefits, and must be locally tax favored,
reported to the local tax authority, funded only from earned income, and limited to USD 50,000
or less annually or USD 1,000,000 or less on a lifetime basis. Criterion 5.03(5) is the one
that decides most Israeli cases: withdrawals must be conditioned on reaching a specified
retirement age, disability, or death, or penalties must apply to earlier withdrawals. The
carve-out is narrow and covers only in-service loans, hardship, education, or a primary
residence.

**Section 5.04, tax-favored foreign non-retirement savings trust.** The trust must operate
exclusively or almost exclusively to provide MEDICAL, DISABILITY, or EDUCATIONAL benefits, and
contributions must be limited to USD 10,000 or less annually or USD 200,000 or less lifetime.

Apply these literally. A general-purpose savings vehicle is not within 5.04 merely because it
is not a pension, because 5.04 has its own purpose test.

### Stage 5: Where each Israeli product usually lands, and why

Present this as the analysis and its reasoning, never as a ruling. The "why" column is the
part that matters, because it is what a preparer will actually test against the plan terms.

| Product | PFIC question | Trust question | Where the analysis usually lands |
|---|---|---|---|
| Kranot neemanut, Israeli mutual funds | Pooled passive holdings meet both PFIC tests | Not a trust question | Treated as a PFIC. Check the de minimis exception first |
| TASE-listed ETFs, kranot sal | Same as above | Not a trust question | Same as above |
| Keren pensia, pension fund | The wrapper is usually analysed as the trust, not as PFIC stock | Purpose is retirement, withdrawals are retirement conditioned | Often within 5.03, provided the contribution limits are met in USD |
| Kupat gemel used for retirement | Same as above | Same as above | Often within 5.03, subject to the same limits |
| Keren hishtalmut | Depends on the underlying investment track | Purpose is not retirement, and after the statutory maturity period withdrawal is not conditioned on retirement age, disability or death | Commonly fails 5.03(5), and its purpose is not medical, disability or educational so 5.04 does not fit either. This is the product most likely to need advice |
| Bituach menahalim | Depends on structure and track | Depends heavily on the individual policy terms | Genuinely indeterminate without the policy. Always escalate |
| Chisachon le'chol yeled | Small balances, often under any de minimis | General-purpose child savings, not a 5.04 purpose | Usually low stakes, still worth naming to a preparer |

The keren hishtalmut row is the reason this skill exists. Give the user the two specific
criteria it appears to fail, not a verdict, so they can put a precise question to a preparer
rather than a vague worry.

### Stage 6: Produce the deliverable

Output one table per holding with four columns: the product, the PFIC screen result with the
test that decided it, the trust screen result with the criterion that decided it, and the
single question to ask a preparer. Then list what you could not determine and what document
would settle it, usually the plan terms or the fund's holdings breakdown.

Close by stating that none of this is a classification, and that the exemption criteria are
applied to the user's description of the product rather than to the plan document.

## Do NOT use this skill for

- Obtaining a final or relied-upon classification of any product. This skill screens.
- Annual filing mechanics, deadlines, FBAR, Form 8938 thresholds, or the exclusion versus
  credit choice. Use `us-israel-dual-tax-navigator`.
- Israeli-side taxation of these products, which is a different and generally far simpler
  question. Use `israeli-pension-advisor` or `israeli-tax-returns`.
- Self-employment tax. Use `american-freelancer-israel-tax`.
- Choosing between a QEF election and a mark-to-market election, or making either.
- Advice on whether to buy, sell, or switch any product. That is investment advice and this
  skill does not give it.

## Recommended MCP Servers

| MCP | Use in this skill |
|---|---|
| `boi-exchange` | Bank of Israel rates to convert contribution amounts into USD, which matters because every exemption criterion is a dollar limit |
| `kolzchut` | Israeli-side background on what each product is and how it behaves under Israeli rules |

## Bundled Resources

| Path | Contents |
|---|---|
| `references/domain-checklist.md` | Coverage contract with the primary source behind each item |
| `references/screening-criteria.md` | The PFIC tests and the full 5.03 and 5.04 criteria as checklists |
| `scripts/screen_product.py` | Walks the 5.03 and 5.04 criteria and the PFIC de minimis test for one product |
| `evidence.json` | Every factual claim with its source URL and a verbatim snippet |

## Gotchas

1. **Presenting the Revenue Procedure 2020-17 exemption as a tax exemption.** It exempts from
   section 6048 information reporting only. An agent that tells a user their pension is
   "exempt" without that qualifier has told them something false about their tax.
2. **Treating the PFIC and foreign-trust questions as one question.** They are separate
   regimes with separate forms. A product can be neither, either, or both.
3. **Skipping the de minimis exception.** USD 25,000, or USD 50,000 on a joint return, excepts
   the Form 8621 filing. Asserting a filing duty without checking it manufactures work and
   alarm.
4. **Applying 5.04 to any non-pension savings product.** Section 5.04 has its own purpose
   test, limited to medical, disability, or educational benefits. A general savings vehicle
   does not qualify just because it failed 5.03.
5. **Stating that keren hishtalmut IS a foreign trust.** No IRS guidance says so. The honest
   output names the criteria it appears to fail and sends the question onward.
6. **Forgetting the eligibility gate.** Only individuals already compliant on the related
   income tax may rely on Revenue Procedure 2020-17, so a never-filed user cannot lead with
   it.
7. **Converting contribution limits at the wrong rate or not at all.** Every criterion is in
   dollars while every contribution is in shekels, and a product can sit on either side of the
   limit depending on the year's rate.

## Reference Links

| Source | URL | What to check |
|---|---|---|
| Instructions for Form 8621 | https://www.irs.gov/pub/irs-pdf/i8621.pdf | The income and asset tests, the de minimis exception, and the section 1291 default regime |
| About Form 8621 | https://www.irs.gov/forms-pubs/about-form-8621 | Current revision and who must file |
| Revenue Procedure 2020-17 | https://www.irs.gov/pub/irs-drop/rp-20-17.pdf | Sections 5.02, 5.03 and 5.04, and the scope limited to section 6048 |
| About Form 3520 | https://www.irs.gov/forms-pubs/about-form-3520 | What transactions and ownership trigger it |
| About Form 3520-A | https://www.irs.gov/forms-pubs/about-form-3520-a | The annual duty of a foreign trust with a US owner |

## Troubleshooting

| Symptom | Cause | What to do |
|---|---|---|
| The user wants a yes or no on their keren hishtalmut | The question cannot be answered without the plan terms, and no IRS guidance names the product | Give the two criteria it appears to fail, say plainly that this is a screen, and hand them the exact question for a preparer. |
| Two sources disagree on whether Israeli pensions are reportable | One is describing the reporting exemption and the other the income treatment | Separate the two. Revenue Procedure 2020-17 addresses reporting only. |
| A product looks exempt but the user has never filed a US return | The exemption is available only to eligible, already-compliant individuals | Route to `us-israel-dual-tax-navigator` for the catch-up question first. The order matters. |
| The contribution limit test flips between years | The criteria are dollar limits applied to shekel contributions | Convert per year using that year's rate and record which rate was used. |
| The user asks whether to sell the fund to avoid the regime | That is investment advice and it is also a taxable event | Decline the recommendation, explain that disposing of a section 1291 fund triggers the excess distribution treatment on the entire gain, and route to a preparer. |
