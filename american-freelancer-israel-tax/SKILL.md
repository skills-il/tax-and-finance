---
name: american-freelancer-israel-tax
description: "Not tax advice and not a filed return. Works out the US self-employment tax an American osek patur or osek murshe in Israel owes on top of Bituach Leumi, because there is no US-Israel totalization agreement and the foreign earned income exclusion does not reduce SE tax. Projects the yearly bill from net earnings, explains the quarterly estimated payment cycle, and lays out the structural options and their trade-offs without recommending one. Use when a US citizen or green card holder freelancing in Israel asks why they owe US tax despite paying Israeli tax, what SE tax is, whether the exclusion covers it, or how much to set aside. Produces a projection worksheet, never a filed return. Do NOT use for annual filing mechanics or FBAR, for classifying Israeli funds as PFICs, for Israeli-side bookkeeping or VAT, or for advice on whether to incorporate."
license: MIT
---

# American Freelancer in Israel

## Legal notice

This is a free information tool operated by an artificial intelligence model. It applies
published rates and thresholds to figures you supply and produces a projection. It does all of
this without the involvement, review, or approval of a licensed tax adviser, accountant, or
attorney.

It is not tax advice, it is not a filed return, and it is not a professional opinion. What it
produces is a preliminary worksheet for your own planning. It does not examine your books,
does not verify your residency or business classification, does not model your Israeli tax
position, does not decide whether any structure suits you, and does not recommend
incorporating or not incorporating.

An AI model can err, omit data, or present a wrong conclusion. Any text it produces is an
automatic draft for personal organisation only and must never be submitted to any authority
as it stands.

Responsibility for reporting and for paying tax is yours, the binding assessment is made by
the tax authority concerned, whether the Israeli Tax Authority or the IRS, and representation
before a tax authority is reserved to those permitted to do so by law. This tool is not a
substitute for advice that takes into account the particular data and needs of each person.
Rates and thresholds change every year, so verify each one against the primary sources under
Reference Links before relying on it.

## Problem

An American freelancing in Israel pays Bituach Leumi like everyone else, and then discovers a
second social tax bill from a country they may not have lived in for years. The United States
has social security agreements with thirty countries that stop exactly this double charge, and
Israel is not one of them. Worse, the relief most Americans abroad rely on, the foreign earned
income exclusion, does not touch self-employment tax at all. So a freelancer can owe zero US
income tax and still owe thousands of dollars of US self-employment tax, usually finding out
when a penalty notice arrives.

## Instructions

### Stage 1: Confirm the trap actually applies

Three conditions have to hold together. Check each rather than assuming:

1. The user is a US person, a citizen or lawful permanent resident.
2. The income is self-employment income, not salary. An osek patur or osek murshe invoicing
   clients is self-employed. A sachir on a tlush is not, and the analysis is different.
3. Net earnings from self-employment are USD 400 or more, which is the threshold at which the
   tax applies.

Then state the two facts that make this different from every other country's expats:

**There is no US-Israel totalization agreement.** The United States has social security
agreements with Australia, Austria, Belgium, Brazil, Canada, Chile, the Czech Republic,
Denmark, Finland, France, Germany, Greece, Hungary, Iceland, Ireland, Italy, Japan,
Luxembourg, the Netherlands, Norway, Poland, Portugal, the Slovak Republic, Slovenia, South
Korea, Spain, Sweden, Switzerland, the United Kingdom, and Uruguay. Israel is absent from that
list. Under such an agreement a person generally pays social taxes to only the country where
they live. Without one, both systems charge.

**The exclusion does not help.** Foreign earnings from self-employment cannot be reduced by
the foreign earned income exclusion when computing SE tax, and a self-employed US citizen
living outside the United States must in most cases pay SE tax. This is the point users find
hardest to believe, so state it plainly and cite it.

The result: Bituach Leumi and Israeli income tax on one side, US self-employment tax on the
other, with the exclusion or the credit reaching only the US INCOME tax and never the SE tax.

### Stage 2: Project the SE tax

The computation, in the order Schedule SE performs it:

| Step | Operation | Authority |
|---|---|---|
| 1 | Start from net earnings from self-employment (business income less business expenses) | Schedule C feeds Schedule SE |
| 2 | Multiply by 92.35 percent (0.9235) | Schedule SE line 4a |
| 3 | Apply 12.4 percent for social security, up to the year's wage base | Rate is 12.4 percent of the 15.3 percent total |
| 4 | Apply 2.9 percent for Medicare, with no cap | Remainder of the 15.3 percent |
| 5 | Add Additional Medicare Tax above the threshold for the filing status | See the threshold table below |

The combined rate is 15.3 percent, being 12.4 percent for social security and 2.9 percent for
Medicare. Note that the 15.3 percent applies to the reduced base from step 2, not to the full
net earnings, which is why a rough estimate using 15.3 percent of net earnings slightly
overstates the bill.

**The social security wage base is annual and it changes.** For 2025 the maximum amount of
self-employment income subject to social security tax is USD 176,100. Look up the figure for
the year you are computing rather than reusing this one. The Medicare portion has no cap, so
income above the base is still charged at 2.9 percent.

**Additional Medicare Tax thresholds:**

| Filing status | Threshold |
|---|---|
| Married filing jointly | USD 250,000 |
| Married filing separately | USD 125,000 |
| Single, head of household, or qualifying surviving spouse | USD 200,000 |

Where the user has both wages and self-employment income, the threshold applying to the
self-employment income is reduced by the wages. Flag this rather than computing it.

**One relief that does exist.** The employer-equivalent portion of SE tax is deductible in
figuring adjusted gross income. Be precise about what that does: it reduces INCOME tax only.
It does not reduce net earnings from self-employment and it does not reduce the SE tax itself.
Users routinely hear "it is deductible" and assume the bill shrinks. It does not.

### Stage 3: Set up the payment cycle

US tax on self-employment income is not withheld by anyone, so it is paid in quarterly
estimated instalments during the year rather than in one lump at filing. Explain that the
filing deadline and the payment deadline are different things, and that the automatic
extension available to filers abroad extends filing, not payment.

Practical framing that helps more than a lecture: convert the projected annual SE tax into a
percentage of each invoice the user should set aside as they get paid, in shekels, so the
money exists when the instalment is due. Show the arithmetic rather than asserting a
percentage.

### Stage 4: Lay out the structural options without recommending one

Users invariably ask "how do I make this stop". There are recognised structural responses and
each has real costs. Present them as a comparison for a professional conversation, and state
clearly that choosing among them is not something this skill does.

| Option | The idea | What it costs or risks |
|---|---|---|
| Stay an osek and pay both | No restructuring | The full double charge every year |
| Operate through an Israeli company | Income may be characterised as corporate profit and salary rather than self-employment earnings | Israeli corporate compliance, payroll, accounting cost, and a set of US anti-deferral rules for owning a foreign corporation that are their own significant problem |
| Operate through a US entity | Changes the US characterisation | US filing obligations, possible Israeli tax residence of the entity, and cost |

The middle option is the one most often suggested casually in forums and it is the one with
the largest hidden US complexity, because a US person owning a foreign corporation can walk
into anti-deferral reporting that is worse than the tax they were avoiding. Say so, name it as
outside this skill's scope, and refer it to a cross-border professional. Never present
incorporation as a clean fix.

### Stage 5: Produce the worksheet

Output: the projected SE tax for the year with each step shown, the Additional Medicare Tax
position, the amount to set aside per invoice, the quarterly instalment schedule, and a short
list of questions for a preparer. State which year's wage base you used and where it came
from.

## Do NOT use this skill for

- Deciding whether to incorporate, in Israel or the United States. That is exactly the
  decision that needs a licensed cross-border adviser.
- Anti-deferral rules for a US person owning a foreign corporation. Out of scope, and named
  here so it is not treated as covered.
- Annual filing mechanics, deadlines, FBAR, Form 8938, or the exclusion versus credit choice
  on income tax. Use `us-israel-dual-tax-navigator`.
- PFIC or foreign-trust classification of Israeli savings products. Use
  `us-person-israeli-investment-check`.
- Israeli-side bookkeeping, VAT, invoicing or the osek patur and osek murshe thresholds. Use
  `israeli-freelancer-ops` and `israeli-vat-reporting`.
- Bituach Leumi rates and entitlements on the Israeli side.

## Recommended MCP Servers

| MCP | Use in this skill |
|---|---|
| `boi-exchange` | Bank of Israel rates to convert shekel invoice income into USD net earnings, and to convert the set-aside percentage back into shekels |
| `kolzchut` | Israeli-side background on Bituach Leumi obligations for an osek |

## Bundled Resources

| Path | Contents |
|---|---|
| `references/domain-checklist.md` | Coverage contract with the primary source behind each item |
| `references/se-tax-mechanics.md` | The rates, the wage base, the thresholds, and the full totalization country list |
| `scripts/se_tax_projection.py` | Projects SE tax from net earnings following the Schedule SE order of operations |
| `evidence.json` | Every factual claim with its source URL and a verbatim snippet |

## Gotchas

1. **Saying the foreign earned income exclusion covers it.** It does not touch SE tax. This is
   the central error in the domain and an agent that repeats it causes real financial harm.
2. **Applying 15.3 percent to full net earnings.** Schedule SE multiplies by 92.35 percent
   first. Skipping that step overstates the bill by roughly 8 percent.
3. **Forgetting the social security wage base, or reusing last year's.** The 12.4 percent
   portion stops at the base and the 2.9 percent Medicare portion does not. An agent that caps
   both, or caps neither, gets high earners badly wrong.
4. **Treating the SE tax deduction as reducing the SE tax.** It reduces adjusted gross income
   for income tax purposes only.
5. **Assuming a totalization agreement exists because most developed countries have one.**
   Thirty countries have one and Israel is not among them. Check the list rather than
   generalising.
6. **Recommending an Israeli company as the fix.** It moves the problem into US anti-deferral
   territory for owners of foreign corporations, which is out of scope here and frequently
   worse. Present options, never a recommendation.
7. **Confusing the filing extension with a payment extension.** Estimated payments are due
   during the year and interest runs regardless of any extension to file.

## Reference Links

| Source | URL | What to check |
|---|---|---|
| IRS, self-employment tax | https://www.irs.gov/businesses/small-businesses-self-employed/self-employment-tax-social-security-and-medicare-taxes | The 15.3 percent rate, its split, the USD 400 threshold, and the SE tax deduction |
| Instructions for Schedule SE | https://www.irs.gov/pub/irs-pdf/i1040sse.pdf | The totalization country list, the rule that the exclusion does not reduce SE tax, the wage base, and the Additional Medicare Tax thresholds |
| Schedule SE (form) | https://www.irs.gov/pub/irs-pdf/f1040sse.pdf | Line 4a and the 92.35 percent factor |
| SSA International Programs | Named in the Schedule SE instructions (search "SSA International Programs") | Whether any new social security agreement has been entered into since the instructions were published |

## Troubleshooting

| Symptom | Cause | What to do |
|---|---|---|
| The user insists the exclusion means they owe nothing | The exclusion reaches income tax only | Quote the Schedule SE instruction directly. It is the fastest way to settle it, and it is in Reference Links. |
| The projection looks about 8 percent too high | The 92.35 percent step was skipped | Recompute following the Schedule SE order of operations. |
| A high earner's figure looks too high or too low | The wage base was applied to both portions, or to neither | The 12.4 percent social security portion is capped at the wage base. The 2.9 percent Medicare portion is not capped. |
| The user was told by a forum that an Israeli company solves it | It changes the characterisation but opens US anti-deferral rules for foreign corporations | Present it as one option with that cost named, decline to recommend, and route to a cross-border professional. |
| Two sources give different wage bases | The figure changes annually | Use the base for the tax year being computed and state which year it is. |
| The user asks what percentage of each invoice to save | Reasonable request, but it depends on their own numbers | Compute it from their projected net earnings and show the arithmetic. Do not quote a generic percentage. |
