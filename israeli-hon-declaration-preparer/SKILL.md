---
name: israeli-hon-declaration-preparer
description: "Not tax advice and not a filed declaration. Builds a Declaration of Capital (hatzharat hon, Form 1219) preparation pack after Reshut HaMisim demands one under Section 135. Enumerates every asset and liability class the form requires, gives the valuation basis per class (cost rather than market value, inherited or gifted assets at 1 shekel, pension and gemel at total deposits only), assembles the per-section document checklist, and reconciles the growth since your previous declaration against declared income so an unexplained gap is visible before you file. Use when you received a hatzharat hon demand, need to know which assets must be declared, are filling Form 1219, or must explain a capital increase to the assessor. Do NOT use for the annual return (use israeli-tax-returns), profit-extraction planning (use israeli-corporate-tax-strategy), or the trapped-profits regime (use israeli-trapped-profits-planner)."
license: MIT
compatibility: Works with Claude Code, Cursor, Windsurf, Codex, GitHub Copilot, opencode, OpenClaw, antigravity, Gemini CLI, Gemini Spark, Grok, ChatGPT, Claude.ai, Claude Desktop, Manus. No bundled scripts, so every listed host runs the full workflow.
---

# Israeli Capital Declaration Preparer

## Legal notice

This is a free information tool operated by an AI model. It explains what Form 1219 asks for and helps you organise your own figures and documents. All of its outputs are produced automatically by an AI model, with no involvement, review, or approval by a tax adviser or accountant. The output is not a tax opinion, not a declaration prepared by a licensed representative, and not professional advice. It is a general explanation and arithmetic aid only: it does not examine the full extent of your assets or your complete documents. An AI model may err, omit data, or present a wrong conclusion.

Any worksheet or checklist this tool produces is an automatic draft for your personal preparation only. It is not a filed declaration. Responsibility for the declaration and for its accuracy is yours, the binding assessment is the Tax Authority's, and representation before the Tax Authority is reserved to those permitted by law. Signing the paid-preparer block on the form is reserved to a person who assisted for payment and carries personal liability under sections 143 and 224 of the Income Tax Ordinance; this tool cannot occupy that role. Consult a tax adviser or accountant before filing. All use of its output is the user's sole responsibility.

## Problem

A capital declaration is demanded in writing by the assessing officer, and the demand starts a clock while the taxpayer is still working out which of their assets even count. The form asks for cost rather than value, books an inherited apartment at one shekel, wants pension plans at total deposits while ignoring every gain, and converts foreign currency at the rate on the day of payment rather than the declaration date. Get any of those wrong and the declaration will not reconcile against the previous one. Worse, section 155 of the Ordinance puts the burden of proving an assessment excessive on the taxpayer, so an unexplained increase in capital is a problem to solve before filing, not after.

## Instructions

### Step 1: Confirm there is a demand, and fix the declaration date

A capital declaration is owed only on a written demand. Section 135(1)(a) lets the assessing officer require "any report specified in the notice, and among them a report on the capital and assets" of the person, their spouse, and their children. Without a demand in hand there is nothing to prepare.

Ask the user for:

- The demand letter, and its date.
- **The declaration date (yom ha'hatzhara)**, printed in the form's header as "a report on property and liabilities as at ___". Every balance, statement and wallet snapshot in the pack must be as at that date.
- Whether this is a first declaration or a later one, and if later, the previous declaration's date and its net-capital figure.

**The deadline is a later-of, and it is a floor on what the assessor may set, not a clock from the letter.** Section 135(1)(a) provides that for a capital report no date may be set earlier than the end of 120 days from the date the declaration must relate to, or from the date of the demand, whichever is later. Read the actual date on the demand; do not compute 120 days from receipt and treat that as the deadline.

### Step 2: Fix whose assets are in scope

The form states it covers your assets, your spouse's, and your children who had not yet reached 18 in the tax year. Collect on that basis.

Note the statute is worded differently: section 135(1)(a) describes the children in scope as those "for whom they are entitled to credit points or allowance points". The two sets do not coincide for every family. Use the form's under-18 rule to build the pack, and if the user's family sits on that boundary, tell them the statutory wording differs and route the question to their representative. Do not state the under-18 rule as the law.

Two scope items that are easy to miss, both in section 135(1)(a):

- **Spouse opt-out.** The spouse's capital may be excluded if a declaration signed by that spouse is attached, stating that they will file a separate report on their own capital and assets. Ask about this for separated or separately-assessed couples rather than merging by default.
- **Trustee assets.** The demand power reaches assets in respect of which the person acts as trustee for another. That is a reportable class, and it is distinct from the part D disclosures about property held but not owned.

**Olim and veteran returning residents.** Section 135(1)(b) exempts a person who first became an Israeli resident, or a veteran returning resident under section 14(a), from reporting capital and assets outside Israel for ten years. Two carve-outs apply, tied to income the individual elected out of under section 14(a) and to an asset received under section 97(a)(5) from 1 January 2007. For this population, "list every foreign asset" is affirmatively wrong advice. Establishing the status itself is out of scope; flag it and route it out.

### Step 3: Apply the valuation rules before collecting a single figure

These are the form's own general instructions and they override intuition. Getting them wrong is the classic failure in this domain. Full text in `references/valuation-rules.md`.

| Rule | What the form requires |
|---|---|
| Cost, never value | State the amount the asset actually cost you. Do not state the asset's value. |
| Inherited or gifted | Enter **1 shekel** in the amount/cost field. Any asset whose acquisition cost is under 1 shekel is also entered as 1 shekel. |
| Ancillary costs | Add every further investment connected with the asset, such as legal fees, brokerage, transport, and purchase tax. |
| Improvements | Improvements and betterments are added to the asset's cost. |
| Instalments | Cost is the total of payments made including linkage and interest. If the consideration is not fully paid, enter the full price as the asset and the unpaid balance separately as a liability. |
| No offsetting | Do not offset debtors against creditors, even where you are debtor and creditor to the same person or institution at once. |
| Foreign currency | Enter the foreign-currency amount in its own column, and convert at the representative rate on the **day of payment or receipt**, not the declaration date. |
| Formatting | Whole shekels, no agorot, rounded. One asset or liability per line. A section with nothing in it gets 0. Private assets with co-owners go in at your share. |

Two class-specific rules that contradict what users expect:

- **Pension, gemel, hishtalmut, life insurance and savings plans (section 6):** the shekel amount is the sum of all deposits, without taking into account interest, linkage or other gains. Not the fund's current balance. Ask for deposit history, not a balance screenshot.
- **Securities and mutual funds (section 7):** recorded at the amount actually invested, per the statements of the institution holding the portfolio. One line per portfolio per institution.

### Step 4: Walk the form section by section and build the worksheet

Reproduce the form's own field numbering, or the worksheet cannot be transcribed into the system. The complete section and field enumeration is in `references/form-1219-sections.md`. Structure:

- **Part A, private:** twelve asset sections totalling to field 200, two liability sections totalling to field 210, and field 220 = 200 - 210.
- **Part B, business where a balance sheet was prepared:** three separate vehicles, a business, a partnership, and a company or other corporation, netting to field 460. Shares and your investment go in **at par value**. A current account where you owe the business is entered as a **negative** number.
- **Part C, business where no balance sheet was prepared:** a full second balance sheet, fields 500 to 770. For a partnership, enter the partnership's figures **as a whole** and take your share only at field 750.
- **Part D, further particulars:** safes, powers of attorney and trusteeships, property held but not owned, and the previous declaration's net capital.
- **Field 800** = 220 + 460 + 770, the total net property, business and private.

Three collection prompts worth making explicit, because they are the sections users under-report:

- **Bank accounts (section 3):** include accounts in your ownership **or under your control** even if not registered in your name, internet accounts such as PayPal, and digital-bank accounts. Overdraft goes in as a negative.
- **Digital assets (section 4):** asset type, quantity, purchase date, wallet address, cost. If held through a service provider such as an exchange, the annex must carry the account number and files showing balances of all digital assets held as at the declaration date.
- **Employee equity held through a trustee.** This is the class most often got wrong, and the skill's own trustee text can mislead if read alone. Shares or units held **by a trustee for you** are **your** asset: they go in part A section 7 at what they actually cost you, not in part D. Part D is for property you hold that belongs to **someone else**, which is the opposite direction. Where the shares cost the employee nothing, general rule 8's floor applies and the entry is 1 shekel; where an exercise price was actually paid, that payment is the cost. Do not enter the market value of vested shares, which is the error the whole of Step 3 exists to prevent and the one place where the counter-intuitive answer catches even a careful filer. The trustee's annual statement is both the substantiating annex and usually the only place the cost figure exists.
- **Loans (sections 13 and 14):** there is no separate mortgage section. Mortgages belong in section 13, which names loans and mortgages as its example. Private loans from people rather than institutions go in section 14, which wants the lender's name, your relationship, their ID or company number, and the year the debt arose.

### Step 5: Reconcile against the previous declaration

The form makes itself the comparison. Part D section 4 asks for the total net property declared in the previous capital declaration and its date, and is left blank only for a first declaration. Field 800 is the current figure. So:

```
field 800 (this declaration)
  minus  part D section 4 (previous declaration)
  =      the change in net capital over the period
```

Set that change against what the user can document: income reported in the intervening years, gifts and inheritances received, loans received, and other non-taxable receipts, less the household's living costs over the period. What remains unexplained is the exposure.

**Living costs are the weakest line in the reconciliation, so do not let the user treat their own estimate as settled.** A self-reported monthly figure is the number most likely to be challenged, and a low estimate produces a comfortable-looking reconciliation that collapses under examination. Section 155 puts the burden of showing an assessment excessive on the taxpayer, so collect **documented** household expenditure over the period, not a remembered average. Where the user can only estimate, say plainly that the figure is unsupported and that the residual it produces is therefore soft. Do not supply a table of amounts: the form does not contain one, and no current figure is quoted in this skill.

**Run the comparison line by line, in BOTH directions, not just as a net delta.** A net change of zero is entirely consistent with an apartment having left the balance sheet and untraced cash having appeared in its place, and it is the disappearance case the assessor raises. So:

- For every asset in the **previous** declaration that is absent now: what happened to it, and where did the proceeds land? Sold, and into which account. Gifted, to whom and on what document. Consumed. Transferred to a spouse who filed separately under the section 135(1)(a) opt-out.
- For every asset appearing **now** that was not there before: what is its source, and is that source documented?

The net delta tells you the size of the question. Only the line-by-line pass tells you which lines you will be asked about.

**Why this happens before filing and not after.** Section 155 places the burden of proving an assessment excessive on the appellant, and lifts it only where the appellant kept acceptable books. An explanation assembled after a demand for clarification is worth much less than the documents gathered now.

Two structural traps in the reconciliation:

- **The 1 shekel convention manufactures phantom gaps.** An inherited apartment sits in closing capital at 1 shekel while any cash it generated sits at full value. Surface this as an explanation line, not as an unexplained increase.
- **Gifts and loans have no form line of their own.** A gift or inheritance appears as an asset at 1 shekel; a loan received appears in section 14, or in the corresponding loans-from-others section of part C. The documentary burden therefore falls entirely on the annexes. Collect the paperwork at the same time as the figure.

Do not assert a shekel threshold above which a gift or a loan must be documented. No such threshold appears in the form, in the Tax Authority's filing circular, or in section 135.

### Step 6: Assemble the annexes and document checklist

Verifying documents are part of the filing, not an optional extra: the form requires documents and proofs to be attached, and permits a photocopy with the original produced on the assessing officer's demand. The warning box ties the late-filing fine to filing "together with all the required documents".

Annex mechanics, from general rules 14 and 15: where the form's space is insufficient, attach further sheets certified by your signature, write "annex attached" on the matching line, and mark on the annex which line it belongs to. Where there is more than one business for which no balance sheet was prepared, attach a further annex per business.

Produce a per-section checklist naming, for each section the user actually completed, the documents that substantiate it. Group it the way the online system does, since that system presents a documents screen listing what the completed sections require.

### Step 7: Explain the filing route, and stop there

Filing is the taxpayer's act or their representative's. Explain, do not transmit.

- The online system exists and the Tax Authority states that at this stage using it is **permissive and not mandatory**. Filing on paper to the assessment offices remains available.
- The declaration counts as filed only once a submission notice is received in the system.
- Accepted attachment types in the system are Pdf, Jpg, Excel and Word. Shape the output pack accordingly.
- Filing on the **previous wording** of form 1219 was permitted only until 30 June 2025. Note that no rule in the circular or in section 135 selects a form version by the date of the demand or by the declaration date, so a demand issued earlier is still filed on the current form. A pre-2025 previous declaration will therefore not map field for field onto the current one, which matters when carrying its net-capital figure into part D.

## Examples

### Example 1: First declaration, self-employed, demand just received

The user is a sole trader who received a demand naming a declaration date of 31 December 2025. Walk Step 1 to fix the date and read the deadline off the letter. Scope: the user, spouse, and one child aged 15. Build part A: apartment at purchase price plus purchase tax, lawyer and brokerage; car at cost; two bank accounts and a PayPal balance as at 31 December 2025; a gemel fund at total deposits, not the balance shown on the annual statement; household contents. Part C for the business, since no balance sheet is prepared. Part D section 4 stays blank. Output the worksheet keyed to the form's field numbers plus a document checklist per section.

### Example 2: Second declaration with an apparent increase

Previous declaration at 31 December 2020 showed net capital of 1.2 million shekels; field 800 now computes to 2.05 million. The change is 850,000. Reported income over the five years, less living costs, accounts for 400,000. The user also received an inherited apartment, which sits at 1 shekel, and a 300,000 loan from a parent. Show the loan in section 14 with the lender's details and collect the loan agreement and the bank transfer; show the inheritance as an explanation line rather than as growth; and identify the remaining unexplained amount so the user can take it to their representative before filing.

### Example 3: Oleh with assets abroad

The user became an Israeli resident for the first time four years ago and holds an apartment and a brokerage account abroad. Do not list the foreign assets by default. Explain that section 135(1)(b) exempts reporting capital and assets outside Israel for ten years from the date of becoming resident, note the two carve-outs, and route the status determination to their representative. Build the Israeli sections normally.

## Bundled Resources

### References

- `references/form-1219-sections.md`: every part, section, field number and per-class field list.
- `references/valuation-rules.md`: the form's fifteen general instructions in full.
- `references/penalties-and-offences.md`: sections 188, 189, 215, 216, 220, 224 and what each covers.
- `references/domain-checklist.md`: the coverage contract this skill is maintained against.

## Recommended MCP Servers

The form asks for identifiers these servers can resolve. Use them to fill fields, never to value an asset, since the form wants cost rather than value.

| MCP | Use for |
|---|---|
| `nadlan` | Gush, helka and tat-helka for a property, from an address |
| `israel-vehicles` | Confirming a vehicle by registration number |
| `tase-mcp` | Identifying a security held in a portfolio |
| `asher`, `il-bank`, `israeli-bank`, `nudlers` | Pulling account and card balances locally, so financial data stays on the user's machine |
| `boi-exchange` | The representative rate for a given date, for the general rule 12 conversion |

## Gotchas

1. **Reporting market value instead of cost.** The single most common failure. General rule 3 says state what the asset cost you and do not state its value. An agent that helpfully looks up a current apartment price has broken the declaration and the comparison against the previous one.
2. **Reporting the pension fund's balance.** Section 6 wants the sum of deposits with interest, linkage and other gains excluded. The balance on the annual statement is the wrong number, and it is the number every user has to hand.
3. **Converting foreign currency at the declaration date.** General rule 12 uses the representative rate on the day of payment or receipt. Using the declaration-date rate shifts every foreign asset by an arbitrary amount.
4. **Treating 120 days as a clock from the demand letter.** It is the later of 120 days from the demand and 120 days from the date the declaration relates to, and it is a floor on what the assessor may set. Read the date off the letter.
5. **Netting balances.** General rule 13 forbids offsetting debtors against creditors even against the same institution, and general rule 7 requires an unpaid balance to appear as a liability while the asset appears at full price. Both instincts point the wrong way.
6. **Quoting a current shekel figure for the late-filing fine.** Section 188(h) re-indexes the amounts in section 188 every 1 January to the previous year's index, so the nominal figures in the Ordinance are not current amounts. State the mechanism and route the user to the Tax Authority for the figure.
7. **Assuming the online channel is compulsory.** The Tax Authority states that at this stage using the digital system is permissive and not mandatory.

## Reference Links

| Source | URL | What to check |
|---|---|---|
| Form 1219 and its official filling instructions | https://www.gov.il/BlobFolder/service/itc1219/he/Service_Pages_Income_tax_itc1219.pdf | Section titles, field numbers 10 to 800, per-class valuation rules, the fifteen general rules, the part D questions |
| Online capital-declaration system | http://secapp.taxes.gov.il/sh-haz-hon | The live filing channel named in the form instructions and the circular. Reference only, do not automate against it |
| Income Tax Ordinance | https://www.gov.il/BlobFolder/legalinfo/law_pkudat_mas_hachnasa/he/LegalInformation_kesher_%D7%A4%D7%A7%D7%95%D7%93%D7%AA%20%D7%9E%D7%A1%20%D7%94%D7%9B%D7%A0%D7%A1%D7%94%20%5B%D7%A0%D7%95%D7%A1%D7%97%20%D7%97%D7%93%D7%A9%5D%20-%20%D7%9C%D7%90%20%D7%9E%D7%A8%D7%95%D7%91%D7%93.pdf | Sections 135, 143, 155, 188, 189, 215, 216, 220, 224 |
| Tax Authority circular 2025-000538 | https://www.gov.il/BlobFolder/dynamiccollectorresultitem/represent-info-050525-1/he/IncomeTax_represent-info-050525-1.pdf | Digital system optional, list of what changed in the form, the 30 June 2025 old-version cut-off, attachment file types |

## Troubleshooting

### "The user does not have their previous declaration"

Part D section 4 must come from the user's own copy or their assessment file. Do not reconstruct or estimate it. Ask them to request it from their representative or the assessing officer, and note that the reconciliation cannot be completed without it.

### "The reconciliation shows a large gap"

Work through the explanation classes first: gifts and inheritances sitting at 1 shekel, loans received, non-taxable receipts, and any asset entered at cost whose value has since risen. If a genuine unexplained amount remains, stop. Pricing the tax on a gap is an assessment, and advising on how to present it is where a licensed professional is required.

### "The user only knows what an asset is worth, not what it cost"

Ask for the acquisition documents, the purchase contract, the deposit records. Do not estimate a cost and do not substitute a value. Where the asset was inherited or received as a gift, the answer is 1 shekel regardless.

### "An old-wording form was already filed after June 2025"

The circular permitted the previous wording only until 30 June 2025 and does not say what happens to a later submission on it. Do not guess the consequence. Route the user to the Tax Authority information centre.
