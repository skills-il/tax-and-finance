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

A capital declaration is demanded in writing, and the clock runs while the taxpayer is still working out which assets count. The form asks for cost rather than value, books an inherited apartment at one shekel, wants pension plans at total deposits, and converts foreign-currency purchases at the rate on the day of payment. Get any of those wrong and the declaration will not reconcile against the previous one, and section 155 puts the burden of proving an assessment excessive on the taxpayer.

## Instructions

Statutory position as checked on 1 October 2026.

### Step 1: Confirm there is a demand, and fix the declaration date

A capital declaration is owed only on a written demand. Section 135(1)(a) lets the assessing officer require "any report specified in the notice, and among them a report on the capital and assets" of the person, their spouse, and their children. Without a demand in hand there is nothing to prepare.

Ask the user for:

- The demand letter, and its date.
- **The declaration date (yom ha'hatzhara)**, printed in the form's header as "a report on property and liabilities as at ___". Every balance, statement and wallet snapshot in the pack must be as at that date.
- Whether this is a first declaration or a later one, and if later, the previous declaration's date and its net-capital figure.

**An extension can be requested, and asking is routine.** Section 188(z) contemplates a later date
set "at that person's request", the statutory footing for a request to defer and usually the first
move when the pack cannot be ready in time. If the user then files after the later date, the monthly
fine runs at the higher rate from it. If the later date falls in 2027, plan to file online
(Step 7).

**The deadline is a later-of, and it is a floor on what the assessor may set, not a clock from the letter.** Section 135(1)(a) provides that for a capital report no date may be set earlier than the end of 120 days from the date the declaration must relate to, or from the date of the demand, whichever is later. Read the actual date on the demand; do not compute 120 days from receipt and treat that as the deadline.

**If the date is close, ask for the extension before it passes, not after.** If it has already passed, file as soon as the pack is complete: section 188(z) charges the fine per month of delay, and section 188(e) counts only full months.

### Step 2: Fix whose assets are in scope

The form states it covers your assets, your spouse's, and your children who had not yet reached 18 in the tax year. Collect on that basis.

The statute is worded differently: section 135(1)(a) covers children "for whom they are entitled to credit points or allowance points", and the two sets do not always coincide. Build on the form's under-18 rule, but do not state it as the law; on the boundary, route the question to the representative.

Two scope items that are easy to miss, both in section 135(1)(a):

- **Spouse opt-out.** The spouse's capital may be excluded if a declaration signed by that spouse is attached, stating that they will file a separate report on their own capital and assets. Ask about this for separated or separately-assessed couples rather than merging by default.
- **Trustee assets.** The demand power reaches assets in respect of which the person acts as trustee for another. That is a reportable class, and it is distinct from the part D disclosures about property held but not owned.

**Olim and veteran returning residents: ask WHEN they became resident.** Section 135(1)(b) gave a person who first became an Israeli resident, or a veteran returning resident under section 14(a), a ten-year exemption from reporting capital and assets outside Israel. Amendment 272 to the Ordinance (2024) deleted it, and its application section, 12(a), applies the deletion to anyone who became such a resident **from 1 January 2026 onward**. The current consolidated text prints (b) simply as deleted; it is section 12(a) that preserves it for earlier residents.

- Became such a resident on or before 31 December 2025: the exemption still runs for the rest of its ten years, with its two carve-outs, tied to income the individual elected out of under section 14(a) and to an asset received under section 97(a)(5) from 1 January 2007. For this group, "list every foreign asset" is wrong advice.
- Became such a resident from 1 January 2026: there is no exemption, and foreign assets are declared like any other.

Establishing the status itself is out of scope; route it out. So is section 135א1, added by the same amendment, which reaches a foreign company controlled from Israel by such a resident: a corporate report, not Form 1219.

### Step 3: Apply the valuation rules before collecting a single figure

These are the form's own general instructions and they override intuition. Getting them wrong is the classic failure in this domain. Full text in `references/valuation-rules.md`.

| Rule | What the form requires |
|---|---|
| Cost, never value | State the amount the asset actually cost you. Do not state the asset's value. |
| Inherited or gifted | Enter **1 shekel** in the amount/cost field. Any asset whose acquisition cost is under 1 shekel is also entered as 1 shekel. Inherited or gifted **money** in an account is not an exception to section 3: it sits at its balance. |
| Ancillary costs | Add every further investment connected with the asset, such as legal fees, brokerage, transport, and purchase tax. |
| Improvements | Improvements and betterments are added to the asset's cost. |
| Instalments | Cost is the total of payments made including linkage and interest. If the consideration is not fully paid, enter the full price as the asset and the unpaid balance separately as a liability. |
| No offsetting | Do not offset debtors against creditors, even where you are debtor and creditor to the same person or institution at once. |
| Foreign currency | Enter the foreign-currency amount in its own column. General rule 12 converts assets and liabilities **paid or received** in foreign currency at the representative rate on the **day of payment or receipt**, not the declaration date. For balances, see the caveat below the table. |
| Formatting | Whole shekels, no agorot, rounded. One asset or liability per line. A section with nothing in it gets 0. Private assets with co-owners go in at your share, and "you" includes your spouse (unless they opted out) and minor children: the form says it is worded in the singular but covers them. Only third parties' shares are left out. |

**Foreign balances are the one case rule 12 does not settle.** Section 3 asks for an account's balance "as it appears in the bank statement as at the declaration date", and a foreign account built up over years has no single day of receipt. The form does not say which rate converts such a balance. Do not present either reading as settled: show the foreign-currency balance, the rate you used and its date, and have the user confirm the treatment with their representative. Items bought in foreign currency (foreign real estate, securities, digital assets) follow rule 12 without that ambiguity.

Two class-specific rules that contradict what users expect:

- **Pension, gemel, hishtalmut, life insurance and savings plans (section 6):** the shekel amount is
  the sum of all deposits, without taking into account interest, linkage or other gains. Not the
  fund's current balance. Ask for deposit history, not a balance screenshot.
  The form does not say **whose** deposits (employee, employer, severance; the readings can differ by
  about a factor of two), nor how to treat **withdrawals and transfers**, which can count the same
  money twice. Present the streams separately, do not silently pick one, and route the treatment
  (see `references/hard-cases.md`).
- **Securities and mutual funds (section 7):** recorded at the amount actually invested, per the statements of the institution holding the portfolio. General rule 9 puts every asset on its own line.

### Step 4: Walk the form section by section and build the worksheet

Reproduce the form's own field numbering, or the worksheet cannot be transcribed into the system. The complete section and field enumeration is in `references/form-1219-sections.md`. Structure:

- **Part A, private:** twelve asset sections totalling to field 200, two liability sections totalling to field 210, and field 220 = 200 - 210.
- **Part B, business where a balance sheet was prepared:** three separate vehicles, a business, a partnership, and a company or other corporation, netting to field 460. A business and a partnership go in at the balance of your capital and current accounts; only the company vehicle asks for your investment and shares **at par value**. A current account where you owe the entity is entered as a **negative** number.
- **Part C, business where no balance sheet was prepared:** a full second balance sheet, fields 500 to 770. For a partnership, enter the partnership's figures **as a whole** and take your share only at field 750. Each asset appears once: an account, vehicle or cash used for both business and household goes in part A or part C, not both.
- **Part D, further particulars:** safes, powers of attorney and trusteeships, property held but not owned, and the previous declaration's net capital.
- **Field 800** = 220 + 460 + 770, the total net property, business and private.

**Walk every section, not only the assets the user mentioned.** Users list what comes to mind. The sections they forget are cash at home (5), savings plans in a child's name (6), loans they gave (8), vehicles (9), jewellery, gold and collectibles (10), household contents (11), safes (part D 1) and signing rights over someone else's account (part D 2). Go through all fourteen part A sections (twelve asset, two liability) and the four part D questions, and enter 0 only where the answer really is nothing.

Collection prompts worth making explicit, because these are the sections users under-report:

- **Bank accounts (section 3):** include accounts in your ownership **or under your control** even if not registered in your name, internet accounts such as PayPal, and digital-bank accounts. Overdraft goes in as a negative. Tell apart three cases the form treats differently: an account you co-own goes in at the share held by everyone in scope (general rule 10); an account in someone else's name that you control is yours in section 3; signing rights over someone else's money is a part D section 2 disclosure, not an asset.
- **Digital assets (section 4):** asset type, quantity, purchase date, wallet address, cost. If held through a service provider such as an exchange, the annex must carry the account number and files showing balances of all digital assets held as at the declaration date. A balance file shows quantities, not cost, so collect the full trade history; swaps, staking and airdrops are open questions (see `references/hard-cases.md`).
- **Employee equity held through a trustee.** This is the class most often got wrong. Shares or units held **by a trustee for you** are **your** asset: they go in part A section 7 at what they actually cost you, not in part D. Part D is for property you hold that belongs to **someone else**. Where the shares cost nothing and the vesting was not taxed as salary, general rule 8 gives 1 shekel; where an exercise price was paid, that payment is the cost. Never enter the market value of vested shares. The trustee's annual statement is the annex and usually the only place the cost figure exists.
  Unvested grants, sold shares whose proceeds sit with a foreign broker, plans with no Israeli trustee, and vesting taxed as salary each need a different answer that the form does not settle; see `references/hard-cases.md` and route the choice.
- **Loans (sections 13 and 14):** there is no separate mortgage section. Mortgages belong in section 13, which names loans and mortgages as its example. Private loans from people rather than institutions go in section 14, which wants the lender's name, your relationship, their ID or company number, and the year the debt arose. Which mortgage figure to use, and where a guarantee you gave goes, are in `references/hard-cases.md`.

### Step 5: Reconcile against the previous declaration

The form makes itself the comparison. Part D section 4 asks for the total net property declared in the previous capital declaration and its date, and is left blank only for a first declaration. Field 800 is the current figure. So:

```
field 800 (this declaration)
  minus  part D section 4 (previous declaration)
  =      the change in net capital over the period
```

**A first declaration is the baseline the next one is measured against.** Part D section 4 stays blank, but anything left out now cannot later explain growth. Cash at home, jewellery, loans the user gave, and gifts already received all belong in it, with documents, because the next declaration will be compared against it line by line.

Field 800 is net and at cost, so only an event that moves it can explain a change in it: income **net of tax** but before fund contributions (including income taxed only at source), money gifted or inherited, proceeds of selling an inherited or gifted asset, exempt realised gains; less living costs, gifts given and assets sold or discarded below cost; plus or minus changes in who is in scope (marriage, a spouse opting in or out, a child turning 18, an oleh whose exemption ended). What the user cannot document is the exposure.

Two things look like explanations and are not. **A loan received** raises an asset and section 14 by the same amount, so it moves field 800 by zero; it answers "where did this cash come from" in the line-by-line pass, never the net gap. **A rise in an asset's value** never reaches field 800, because cost is frozen. The full table, with the double-count traps, is in `references/reconciliation.md`.

**Living costs are the weakest line, so do not let the user treat their own estimate as settled.** A low self-reported figure produces a comfortable reconciliation that collapses under examination. Collect **documented** household expenditure over the period, not a remembered average; where the user can only estimate, say the residual it produces is soft. Do not supply a table of amounts: the form has none, and this skill quotes no current figure.

**Run the comparison line by line, in BOTH directions.** A net change of zero is consistent with an apartment leaving the balance sheet and untraced cash appearing in its place, which is the case the assessor raises:

- For every asset in the **previous** declaration that is absent now: what happened to it, and where did the proceeds land? Sold, and into which account. Gifted, to whom and on what document. Consumed. Transferred to a spouse who filed separately under the section 135(1)(a) opt-out.
- For every asset appearing **now** that was not there before: what is its source, and is that source documented?

**Why before filing.** Section 155 puts the burden of proving an assessment excessive on the appellant, lifted only where acceptable books were kept, so documents gathered now are worth far more than an explanation assembled later.

**Gifts have no form line of their own.** A gifted or inherited non-monetary asset appears at 1 shekel (general rule 2), gifted or inherited money sits at its full balance in section 3, and gifted money already spent sits inside the cost of whatever it bought. The documentary burden falls on the annexes, so collect the paperwork with the figure.

**Stop before filing if an asset or its income was never reported.** This declaration discloses a foreign account (section 3 asks for its country) and a crypto wallet (section 4 asks for its address). If the income behind either never reached a return, do not help assemble the filing until the user has seen a representative. Section 220 attaches criminal exposure to wilful evasion, and whether any voluntary-disclosure route is still open to someone already holding a demand is a question this skill does not answer.

Do not assert a shekel threshold above which a gift or a loan must be documented. No such threshold appears in the form, in the Tax Authority's filing circular, or in section 135.

### Step 6: Assemble the annexes and document checklist

Verifying documents are part of the filing: the form requires them (a photocopy is allowed, with the original on demand), and the warning box ties the late-filing fine to filing "together with all the required documents".

Annex mechanics (general rules 14 and 15: signed extra sheets, "annex attached" on the matching line, one annex per business without a balance sheet) are in `references/valuation-rules.md`.

Produce a per-section checklist of the documents behind each completed section, grouped the way the online system's documents screen groups them.

### Step 7: Explain the filing route, and stop there

Filing is the taxpayer's act or their representative's. Explain, do not transmit.

- **Until 31 December 2026** the online system is optional. The Tax Authority's May 2025 circular says that at this stage using it is **permissive and not mandatory**, and paper filing at the assessment offices remains available.
- **From 1 January 2027 an individual's capital declaration must be filed online.** A Finance Minister's order of 3 September 2026 brings section 135(1)(a1) of the Ordinance into force for individuals on that date. Section 131ג(ו) then treats a report that had to be filed online and was not as **not filed at all**, which is the route into the late-filing fine. The order has no transitional rule for a demand issued in 2026 that falls due in 2027, and the 120-day floor means many demands received from September 2026 onward do. The safe reading, though nothing states it in terms, is that the date the user actually files decides: treat any filing made on or after 1 January 2027, including a late one or one under an extension, as one that must be online, and never tell the user a paper filing made then is safe.
- The online mechanics are set by the Income Tax Rules on online reporting of a capital declaration (2026): a representative identifies with an approved electronic certificate and attaches a taxpayer-signed scan of the output, filing is complete only once the system shows a receipt, and an infected file is treated as never transmitted.
- Accepted attachment types in the system are Pdf, Jpg, Excel and Word. Shape the output pack accordingly.
- Filing on the **previous wording** of form 1219 was permitted only until 30 June 2025. No rule in the circular or in section 135 selects a form version by the date of the demand or by the declaration date. The reading that follows, though nothing states it in terms, is that a demand issued earlier is still filed on the current form. A pre-2025 previous declaration will therefore not map field for field onto the current one, which matters when carrying its net-capital figure into part D.

## Examples

### Example 1: First declaration, self-employed, demand just received

The user is a sole trader who received a demand naming a declaration date of 31 December 2025. Walk Step 1 to fix the date and read the deadline off the letter. Scope: the user, spouse, and one child aged 15. Build part A: apartment at purchase price plus purchase tax, lawyer and brokerage; car at cost; two bank accounts and a PayPal balance as at 31 December 2025; a gemel fund at total deposits, not the balance shown on the annual statement; household contents. Part C for the business, since no balance sheet is prepared. Part D section 4 stays blank. Output the worksheet keyed to the form's field numbers plus a document checklist per section.

### Example 2: Second declaration with an apparent increase

Previous declaration at 31 December 2020 showed net capital of 1.2 million shekels; field 800 now computes to 2.05 million. The change is 850,000. Income net of tax over the five years, less documented living costs, accounts for 400,000. The user also received an inherited apartment, still held at 1 shekel, and a 300,000 loan from a parent. The loan goes in section 14 with the lender's details, the loan agreement and the bank transfer; it shows where the cash came from but moves field 800 by zero. The inheritance explains 1 shekel. About 450,000 is therefore unexplained. Check the scope bridge first (a marriage in the period, for instance), then take the residual and the line-by-line pass to the representative before filing.

### Example 3: Oleh with assets abroad

The user became an Israeli resident for the first time in 2022 and holds an apartment and a brokerage account abroad. Ask the date first: because it falls before 1 January 2026, Amendment 272 does not remove the ten-year exemption from reporting capital and assets outside Israel; whether it applies still turns on the status the representative confirms. Do not list the foreign assets by default, note the two carve-outs, and route the status determination to their representative. Build the Israeli sections normally. Had the user arrived in 2026, Amendment 272 removes the exemption and the foreign assets go in like any other.

## Bundled Resources

### References

- `references/form-1219-sections.md`: every part, section, field number and per-class field list.
- `references/valuation-rules.md`: the form's fifteen general instructions in full.
- `references/penalties-and-offences.md`: sections 188, 189, 215, 216, 220, 224 and what each covers.
- `references/reconciliation.md`: what explains a change in field 800 and what only looks like it.
- `references/hard-cases.md`: employee equity states, crypto cost, fund withdrawals, the mortgage figure, guarantees, household contents.
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
3. **Using one conversion date for everything.** General rule 12 converts a foreign apartment, security or coin at the rate on the day it was paid for; the declaration-date rate shifts its cost arbitrarily. A foreign bank balance is different (section 3 wants the statement balance at the declaration date and names no rate): surface it, do not settle it.
4. **Treating 120 days as a clock from the demand letter.** It is the later of 120 days from the demand and 120 days from the date the declaration relates to, and it is a floor on what the assessor may set. Read the date off the letter.
5. **Netting balances.** General rule 13 forbids offsetting debtors against creditors even against the same institution, and general rule 7 requires an unpaid balance to appear as a liability while the asset appears at full price. Both instincts point the wrong way.
6. **Quoting a current shekel figure for the late-filing fine.** Section 188(h) re-indexes the amounts in section 188 every 1 January to the previous year's index, so the nominal figures in the Ordinance are not current amounts. State the mechanism and route the user to the Tax Authority information and online services centre, on 02-5656400 or *4954, for the figure in force.
7. **Calling the online channel optional without checking the filing date.** It is optional only until 31 December 2026. From 1 January 2027 an individual's declaration must be filed online, section 131ג(ו) treats a paper filing that should have been online as not filed, and the safe course is to treat any filing made from that date as online-only (Step 7).
8. **Applying the olim ten-year exemption without asking when the person became resident.** Amendment 272 deleted it for anyone who became a first-time or veteran returning resident from 1 January 2026.

## Reference Links

| Source | URL | What to check |
|---|---|---|
| Form 1219 and its official filling instructions | https://www.gov.il/BlobFolder/service/itc1219/he/Service_Pages_Income_tax_itc1219.pdf | Section titles, field numbers 10 to 800, per-class valuation rules, the fifteen general rules, the part D questions |
| Online capital-declaration system | http://secapp.taxes.gov.il/sh-haz-hon | The live filing channel named in the form instructions and the circular. Reference only, do not automate against it |
| Income Tax Ordinance, current consolidation | https://www.nevo.co.il/law_html/law01/255_001.htm | Sections 131ג, 135, 135א1, 143, 155, 188, 189, 215, 216, 220, 224 |
| Amendment 272 to the Ordinance (2024) | https://fs.knesset.gov.il/25/law/25_lsr_4303082.pdf | Deletion of section 135(1)(b) and its application from 1 January 2026 |
| Order bringing section 135(1)(a1) into force | https://olaw.org.il/takanot/takanot-12523.pdf | Mandatory online filing for individuals from 1 January 2027 |
| Tax Authority circular 2025-000538 | https://www.gov.il/BlobFolder/dynamiccollectorresultitem/represent-info-050525-1/he/IncomeTax_represent-info-050525-1.pdf | Digital system optional, list of what changed in the form, the 30 June 2025 old-version cut-off, attachment file types |

## Troubleshooting

### "The user does not have their previous declaration"

Part D section 4 must come from the user's own copy or their assessment file. If the previous one was filed through the online system, the system lets the filer view digital declarations already submitted, so check there first. Do not reconstruct or estimate it. Ask them to request it from their representative or the assessing officer, and note that the reconciliation cannot be completed without it.

### "The reconciliation shows a large gap"

Work through the explanation lines in `references/reconciliation.md` first: money gifted or inherited, proceeds of selling an inherited asset, exempt realised gains, income taxed only at source, and changes in who is in scope. A loan received and a rise in an asset's value are not explanations. If a genuine unexplained amount remains, stop. Pricing the tax on a gap is an assessment, and advising on how to present it is where a licensed professional is required.

### "The user only knows what an asset is worth, not what it cost"

Ask for the acquisition documents, the purchase contract, the deposit records. Do not estimate a cost
and do not substitute a value. Where the asset was inherited or received as a gift, the answer is
1 shekel regardless.

Household contents and jewellery bite hardest here: a 0 for a furnished home is also wrong. See `references/hard-cases.md`.

For an asset bought decades ago the documents are rarely in a drawer, and a refusal without a route
is where users invent a number. Send them to look for the file rather than to guess: the purchase
contract held by the lawyer who handled the transaction, the land-registry extract for a property,
and their own tax file at the assessing office. If the cost genuinely cannot be reconstructed, that
is a question for their representative to take to the assessor, not a gap for the skill to fill with
an estimate.

### "An old-wording form was already filed after June 2025"

The circular permitted the previous wording only until 30 June 2025 and does not say what happens to a later submission on it. Do not guess the consequence. Route the user to the Tax Authority information and online services centre, on 02-5656400 or *4954.
