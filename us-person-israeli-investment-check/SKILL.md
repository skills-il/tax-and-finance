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
| Annual and lifetime contribution amounts, and whether they are set as a percentage of salary | 5.03 accepts a percentage-of-earned-income limit OR a dollar limit; 5.04 uses dollar limits only |
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

**The USD 25,000 exception, which is widely missed and widely misstated.** A shareholder is
not required to complete Part I of Form 8621 for a specific section 1291 fund if all three
conditions hold for the year:

| Condition | What it means in practice |
|---|---|
| Value test on the last day of the tax year | The threshold counts ALL the user's PFIC stock together, direct or indirect (QEFs, section 1291 funds and mark-to-market stock), not each fund separately. USD 25,000, or a combined USD 50,000 on a joint return |
| No excess distribution received from that fund | A distribution large enough to be an excess distribution removes the exception |
| No gain recognized on selling or disposing of that fund's stock | A sale at a gain in the year removes the exception, whatever the year-end value |

The aggregate excludes PFIC stock held through another US person or through another PFIC. The
exception is also unavailable for a fund the user has made a QEF election for. A separate
USD 5,000 exception covers a section 1291 fund owned indirectly THROUGH ANOTHER PFIC, measured
per fund on the last day of the tax year with the same no-excess-distribution, no-gain and
no-QEF conditions, and it can apply even when total PFIC stock exceeds USD 25,000. It does NOT
reach fund stock owned through a pension, gemel or hishtalmut wrapper treated as a grantor
trust, which counts toward the USD 25,000 aggregate instead, see the look-through note in
Stage 5.

Check this before telling anyone they have a Part I obligation. A modest, untouched TASE ETF
position often falls under it; one that was partly sold at a gain does not.

Two cautions on the exception. It relieves the annual Part I reporting only, and it does not
change how a distribution or a gain is taxed. It also does not affect any other duty, so a
holding under the threshold can still be reportable elsewhere.

**Why the default regime is the problem.** A shareholder of a section 1291 fund is subject to
special rules on an excess distribution, and the ENTIRE gain on disposing of a section 1291
fund is treated as an excess distribution. That default allocates the amount back across the
holding period with an interest charge, which is what removes the benefit of deferral. There
are elections that avoid it, a qualified electing fund election and a mark-to-market election,
but a QEF election depends on the fund providing a PFIC Annual Information Statement every
year, so ask whether the fund issues one before it is even considered. Explain the shape of this and route the election to a preparer. Do not
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
reported to the local tax authority, and funded only from earned income. Criterion 5.03(4) is
met in ANY of three ways: contributions limited by a percentage of the participant's earned
income, OR an annual limit of USD 50,000 or less, OR a lifetime limit of USD 1,000,000 or less.
A plan whose contributions are capped as a percentage of salary can meet 5.03(4) even when a
high earner's shekel contributions exceed USD 50,000. For an employer-maintained plan,
criterion 5.03(6) adds a nondiscrimination requirement. Criterion 5.03(5) is the one
that decides most Israeli cases: withdrawals must be conditioned on reaching a specified
retirement age, disability, or death, or penalties must apply to earlier withdrawals. The
carve-out is narrow and covers only in-service loans, hardship, education, or a primary
residence.

**Section 5.04, tax-favored foreign non-retirement savings trust.** The trust must operate
exclusively or almost exclusively to provide MEDICAL, DISABILITY, or EDUCATIONAL benefits, and
contributions must be limited to USD 10,000 or less annually or USD 200,000 or less lifetime.
There is no percentage-of-income limb in 5.04.

**Which exchange rate.** Both 5.03(4) and 5.04(3) are measured using the US Treasury Bureau of
the Fiscal Service foreign currency conversion rate on the last day of the tax year, not a
Bank of Israel rate and not an average. Record the rate and the date used.

Apply these literally. A general-purpose savings vehicle is not within 5.04 merely because it
is not a pension, because 5.04 has its own purpose test.

### Stage 5: Where each Israeli product usually lands, and why

Present this as the analysis and its reasoning, never as a ruling. The "why" column is the
part that matters, because it is what a preparer will actually test against the plan terms.

| Product | PFIC question | Trust question | Where the analysis usually lands |
|---|---|---|---|
| Kranot neemanut, Israeli mutual funds | Pooled passive holdings meet both PFIC tests | Not a trust question | Treated as a PFIC. Check the de minimis exception first |
| TASE-listed ETFs, kranot sal | Same as above | Not a trust question | Same as above |
| Keren pensia, pension fund | Not only a trust question. If the owner is treated as owning the arrangement, they are treated as owning the fund stock it holds, see the look-through note below | Purpose is retirement, withdrawals are retirement conditioned | Often within 5.03, provided 5.03(4) is met. Check the plan terms for whether contributions are capped as a percentage of salary before testing the dollar limbs |
| Kupat gemel used for retirement | Same as above | Same as above | Often within 5.03, subject to the same limits |
| Keren hishtalmut | Depends on the underlying investment track | Purpose is not retirement, and after the maturity period (6 years from the start of deposits, or 3 for training or after retirement age) withdrawal is not conditioned on retirement age, disability or death. 5.03(5) also accepts plans where penalties apply to earlier withdrawals, so whether Israeli tax on an early withdrawal counts as such a penalty is the live preparer question | Commonly fails 5.03(5), and its purpose is not medical, disability or educational so 5.04 does not fit either. This is the product most likely to need advice |
| Bituach menahalim | Depends on structure and track | Depends heavily on the individual policy terms | Genuinely indeterminate without the policy. Always escalate |
| Chisachon le'chol yeled | Small balances, often under any de minimis | General-purpose child savings, not a 5.04 purpose | Usually low stakes, still worth naming to a preparer |

**Look-through note, for every wrapper row.** Under Treasury Regulation 1.1291-1(b)(8)(iii)(D),
a person treated under sections 671 through 679 as the owner of a trust that holds stock is
considered to own that stock. So if a pension, gemel or hishtalmut arrangement is treated as a
grantor trust owned by the user, the Israeli funds or ETFs its investment track holds can be
PFIC stock the user owns indirectly, a Form 8621 question in its own right. Revenue Procedure
2020-17 does not help here: it states that it does not affect reporting obligations under any
other provision of US law. Regulation 1.1298-1(c)(4) has a Part I exception for PFIC stock
held through a foreign pension fund, but only where a US income tax treaty treats the fund
that way; whether the US-Israel treaty does is a question for the preparer, not for this
screen. Always list the underlying PFIC question for wrapper products.

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
| `boi-exchange` | Bank of Israel shekel rates for a rough sense of scale only. The 5.03 and 5.04 dollar limits are formally measured at the US Treasury year-end rate, so do not use this for the final test |
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
3. **Misapplying the USD 25,000 exception.** It counts ALL PFIC stock together at year end
   (USD 50,000 combined on a joint return), and it is lost for a fund that paid an excess
   distribution or was sold at a gain that year. Skipping it manufactures work and alarm;
   applying it per fund, or to a fund sold at a gain, hides a real Part I duty.
4. **Applying 5.04 to any non-pension savings product.** Section 5.04 has its own purpose
   test, limited to medical, disability, or educational benefits. A general savings vehicle
   does not qualify just because it failed 5.03.
5. **Stating that keren hishtalmut IS a foreign trust.** No IRS guidance says so. The honest
   output names the criteria it appears to fail and sends the question onward.
6. **Forgetting the eligibility gate.** Only individuals already compliant on the related
   income tax may rely on Revenue Procedure 2020-17, so a never-filed user cannot lead with
   it.
7. **Treating 5.03(4) as a dollar-only test, or converting at the wrong rate.** A pension
   capped as a percentage of salary can pass 5.03(4) whatever the dollar amount. Where a dollar
   limb is used, convert at the US Treasury Bureau of the Fiscal Service rate on the last day
   of the tax year, because a product can sit on either side of the limit depending on it.

## Reference Links

| Source | URL | What to check |
|---|---|---|
| Instructions for Form 8621 | https://www.irs.gov/pub/irs-pdf/i8621.pdf | The income and asset tests, the de minimis exception, and the section 1291 default regime |
| About Form 8621 | https://www.irs.gov/forms-pubs/about-form-8621 | Current revision and who must file |
| Revenue Procedure 2020-17 | https://www.irs.gov/pub/irs-drop/rp-20-17.pdf | Sections 5.02, 5.03 and 5.04, and the scope limited to section 6048 |
| About Form 3520 | https://www.irs.gov/forms-pubs/about-form-3520 | What transactions and ownership trigger it |
| About Form 3520-A | https://www.irs.gov/forms-pubs/about-form-3520-a | The annual duty of a foreign trust with a US owner |
| Treasury Reporting Rates of Exchange | https://fiscaldata.treasury.gov/datasets/treasury-reporting-rates-exchange/treasury-reporting-rates-of-exchange | The year-end shekel rate used for the 5.03(4) and 5.04(3) dollar limits |

## Troubleshooting

| Symptom | Cause | What to do |
|---|---|---|
| The user wants a yes or no on their keren hishtalmut | The question cannot be answered without the plan terms, and no IRS guidance names the product | Give the two criteria it appears to fail, say plainly that this is a screen, and hand them the exact question for a preparer. |
| Two sources disagree on whether Israeli pensions are reportable | One is describing the reporting exemption and the other the income treatment | Separate the two. Revenue Procedure 2020-17 addresses reporting only. |
| A product looks exempt but the user has never filed a US return | The exemption is available only to eligible, already-compliant individuals | Route to `us-israel-dual-tax-navigator` for the catch-up question first. The order matters. |
| The contribution limit test flips between years | The dollar limbs are applied to shekel contributions | First check whether 5.03(4) is met by its percentage-of-earned-income limb. If a dollar limb decides it, convert at the Treasury year-end rate for each year and record the rate used. |
| The user asks whether to sell the fund to avoid the regime | That is investment advice and it is also a taxable event | Decline the recommendation, explain that disposing of a section 1291 fund triggers the excess distribution treatment on the entire gain, and route to a preparer. |
