---
name: israeli-property-appraisal
description: >-
  Not a licensed appraisal (shuma) and no substitute for a licensed shamai mekarkein. Builds a
  comparable-transactions analysis for an Israeli property from official government data, and
  handles the appraisal processes around it: a low bank mortgage appraisal under Standard 19, and
  a betterment levy (heitel hashbacha) assessment. Use when someone asks what a property is worth,
  says the bank's appraisal came in low and blocked their mortgage, received a betterment levy
  bill from the local planning committee, or needs the gush and helka for an address. Resolves an
  address to its parcel, pulls real recorded transactions, and assembles the principles and
  arguments for the objection letter. Recorded comparable deals are public but effectively
  unreachable, so people accept a bank number or a municipal bill they could have challenged. Do
  NOT use for purchase tax or betterment tax (mas rechisha, mas shevach), Tabu extracts, rental
  agreements, mortgage track comparison, or land tenders.
license: MIT
---

# Israeli Property Comparable-Sales Analysis

## Legal notice

The Hebrew text below is the authoritative version of this notice.

כלי זה הוא כלי מידע חינמי, הפועל באמצעות מודל בינה מלאכותית. הוא מאתר עסקאות מקרקעין שדווחו לרשות המסים ופורסמו לציבור, מסנן אותן ומציג חציון וטווח מחירים למ"ר, לצד הסבר כללי על הדין החל. כל תוצריו מופקים באופן אוטומטי על ידי מודל בינה מלאכותית, ללא מעורבות, בדיקה או אישור של שמאי מקרקעין. הפלט שיוצר הכלי אינו שומת מקרקעין ואינו חוות דעת מקצועית, אלא אינדיקציה סטטיסטית גולמית בלבד: הוא אינו כולל ביקור בנכס, אינו מבצע את ההתאמות השמאיות הנדרשות בגישת ההשוואה, ונשען על נתונים ציבוריים שאינם אחידים ואינם שלמים. מודל בינה מלאכותית עלול לשגות, להשמיט נתונים או להציג מסקנה שגויה.

אין להציג את הפלט כשומה מוסמכת שנערכה על ידי שמאי, אין להסתמך עליו כראיה, ואין להגישו לבית משפט או לכל גורם אחר המוסמך לגבות ראיה בעניין מקרקעין. לשם כך נדרשת שומה שנערכה בידי שמאי מקרקעין מוסמך. כל נוסח שהכלי מנסח הוא טיוטה אוטומטית לצורכי התארגנות אישית בלבד, ואינו השגה שמאית. הכלי אינו מחליף ייעוץ של שמאי מקרקעין מוסמך או איש מקצוע אחר, וכל שימוש בפלט ובתוצריו הוא באחריותו הבלעדית של המשתמש.

In English, for convenience only: this is a free, AI-operated information tool. It locates property transactions reported to the Tax Authority and published to the public, filters them, and presents a median and a price range per square metre alongside a general explanation of the applicable law. All of its outputs are produced automatically by an AI model, with no involvement, review, or approval by a licensed real estate appraiser (shamai mekarkein). The output is not a property appraisal (shuma) and not a professional opinion, but a raw statistical indication only: it involves no site visit, it does not perform the appraisal adjustments required by the comparison approach, and it relies on public data that is neither uniform nor complete. An AI model may err, omit data, or present a wrong conclusion. The output must not be presented as a certified appraisal, must not be relied on as evidence, and must not be submitted to a court or any other body empowered to take evidence in a property matter. Any text this tool drafts is an automatic draft for the user's personal preparation only, and is not an appraiser's objection. This tool does not replace advice from a licensed appraiser or other professional, and all use of its output is the user's sole responsibility.


## Problem

Israeli property value is settled on recorded comparable transactions. Every deal is reported to the Tax Authority and published, but the data sits behind an interface nobody can practically query, so when the bank's appraiser returns a number ninety thousand shekels below the purchase price, or the local committee sends a betterment levy bill, most people have no way to check the figure and simply accept it. Both numbers are challengeable, and both have hard deadlines that expire quietly.

## Instructions

### Step 1: Establish what the user actually needs

Three different jobs arrive worded almost identically. Separate them before doing anything, because the deadlines and the forums differ:

| The user says | What they need | Where to go |
|---|---|---|
| "What is this apartment worth?" | Comparables analysis | Step 2 |
| "The bank's appraisal came in low" | Standard 19 explanation plus counter-comparables | Step 2, then Step 4 |
| "I got a betterment levy bill" | Exemption check, then objection routing | Step 5 |
| "What is the gush and helka here?" | Parcel lookup only | Step 2, first output line |

### Step 2: Pull the comparables

**First check which route is available to you.** The government feed is reachable two ways, and picking the wrong one is the most common failure of this skill:

| Your environment | Route |
|---|---|
| You can run shell commands (Claude Code, Cursor, Codex, Windsurf, CLI agents) | Step 2a, the bundled script |
| You cannot run shell commands, but a local MCP can run (Claude Desktop) | Step 2b, route 1, the `nadlan` MCP |
| You cannot run shell commands and nothing runs locally (claude.ai, ChatGPT, Manus) | Step 2b, route 2, the nadlan.gov.il site |

The script talks to the Govmap and Nadlan endpoints directly. Called from a hosted assistant those endpoints have been observed to refuse the request at the network edge, before it reaches the application, and reshaping the request does not help. The refusal has been reproduced only as a symptom, not traced to a published rule, so treat non-Israeli or datacentre egress as the likeliest explanation rather than an established one. Either way the practical consequence is the same: do not try to substitute a plain web fetch for the script.

Then follow the route the table gave you. **Both routes are set out in full in
`references/comparables-routes.md`, and you must read that file before pulling any deal.** It carries
the bundled script's invocation and its output contract, the `nadlan` MCP route including the
residential-row filtering its own statistics block does not do for you, the nadlan.gov.il route for
clients with nothing running locally, and the filtering and arithmetic rules that make a median
defensible. Applying any of it from memory is how a workshop sale ends up inside a residential median.

### Step 3: Turn deals into a defensible range

Raw shekels per square metre is not a valuation. The comparison approach adjusts each comparable toward the subject property before averaging. Walk the user through the adjustments that matter, and be explicit that the script does not apply them:

- Floor, and whether there is a lift
- Size, since small units almost always carry a higher price per square metre than large ones in the same building
- Condition and whether the unit has been renovated
- Parking, and whether it is covered
- Balcony, protected space (ממ"ד), storage
- Building age and the year built
- Orientation, view, and noise exposure
- Unexercised building rights
- The nature of the right, meaning full ownership against a lease from the Israel Land Authority
- The date of the deal, since a transaction from two years ago reflects a different market

The script flags statistical outliers with `!` and leaves them out of the median. Those rows are usually not bargains. Transfers between relatives, sales of a partial share in a property, and combination deals are all published alongside genuine arm's-length sales and look like absurd prices per square metre. Point them out rather than hiding them.

### Step 4: A bank appraisal that came in low

The single most useful thing to explain is that a bank appraisal is deliberately not a market valuation. Standard 19 governs valuations offered as credit collateral and requires a conservative approach both to the factual data and through the analysis stages, producing a cautious result, and where data is missing the appraiser is required to adopt stringent assumptions. It also directs caution in unusual market conditions, precisely because a collateral asset is usually realised in a slump. A bank number below the purchase price is therefore often correct rather than mistaken.

Where a material fact is missing the appraiser will not produce a collateral valuation at all, which is why unpermitted construction, a missing building permit, or a gap between registered and actual area stall a file. Those are fixable before ordering the appraisal, and checking them first is worth more than arguing afterwards.

Quantify the consequence, because the shortfall is what actually hurts. Bank of Israel Directive 329 caps the loan at 75% of value for a single apartment, 70% for a replacement apartment, and 50% for an investment property, and the ratio is measured against the value of the purchased asset alone even where other properties are pledged. Repayment may not exceed 50% of income.

One caveat to state out loud, because the arithmetic depends on it: banks in practice size the loan against the **lower** of the appraised value and the contract price. That convention is what makes a low appraisal bite, and its corollary is that an appraisal above the price buys the borrower nothing. Directive 329 itself defines the ratio against the value of the purchased asset and does not spell out a lower-of rule in those words, so present this as standard bank practice rather than as the directive's text, and tell the borrower to confirm it with their own bank.

Diagnose before arguing. Ask three questions in order. First, what area did the appraiser use, and does it match the contract, the building permit and the registry extract, since an area gap is the most common cause of a shortfall. Second, does the valuation actually disclose the comparables it relied on and the adjustments applied, so the reasoning can be tested at all. Third, is the contract price simply above market, in which case the remedy is renegotiating with the seller rather than fighting the appraiser.

There is no appeal against the bank's credit decision, and the appraiser was engaged by the bank. The commercial routes are: obtain the valuation document itself, examine which comparables were used, submit corrected facts and counter-comparables, request a second appraisal from another appraiser on the bank's approved list, or move the file to another bank.

That is not the same as saying the appraiser is unaccountable. The profession is regulated under the Land Appraisers Law, the Land Appraisers Council licenses appraisers and runs a disciplinary committee, and it publishes a register of active and suspended appraisers. Where a valuation is negligent rather than merely conservative, a complaint to the council is a real route. Say 'no appeal against the bank's decision', never 'no recourse at all'.

### Step 5: A betterment levy assessment

The levy is charged by the local committee, not the Tax Authority, on an owner or a long-term lessee, and is normally half of the betterment value. It arises from one of exactly three planning events: approval of a new plan, a relief, or permission for non-conforming use. It does not apply to plans that took effect before 01.07.1975. It is calculated as at the date the plan was approved but paid on realisation, usually on sale, which is why a levy can surface decades after the plan that caused it.

**Check the exemptions before arguing about the amount**, because an exemption removes the bill entirely. Building or expanding a residential unit up to a **total** of 140 square metres is exempt, conditional on the owner or a relative living there for four years after construction ends, and any area beyond 140 square metres is charged proportionally. Note the two traps: the 140 is the total post-expansion area rather than the area added, and breaching the residence condition revives the debt. A protected space is exempt for the minimum required area only, 9 square metres net plus walls. Where the betterment arises from TAMA 38 seismic strengthening, Kolzchut states there is a partial exemption and the levy is 5% of the betterment rather than 50%. Urban renewal is the least stable corner of this area and secondary sources disagree with each other, so for a specific case confirm the rate against the Third Addendum and the plan that actually applies before relying on it. An exemption request goes to the local committee within 45 days of receiving the assessment, absent special circumstances. Some exemptions are applied automatically and others must be requested, so check with the committee which applies rather than assuming an unclaimed exemption is already lost.

The three above are the most-used exemptions, not the whole list. `references/betterment-levy.md` carries the full table, including public institutions, rehabilitation areas, accessibility works, and long-holding cases. Read it before concluding a user does not qualify.

### Step 6: Route the objection correctly

This is the highest-value fact in the domain, and filing in the wrong forum burns the deadline:

| The dispute | Forum | Deadline |
|---|---|---|
| Whether the levy is owed at all | District appeals committee (ועדת ערר) | 45 days from receiving the assessment |
| The amount of the levy | Deciding appraiser (שמאי מכריע) | 45 days from receiving the assessment, or one year from display of the assessment table where the betterment estimate was not deferred |

A request for a deciding appraiser goes to the chair of the Land Appraisers Council, who names one from a closed list within 15 days. Within 21 days of the appointment the applicant must supply the registry extract, the local committee's assessment with its annexes, and a valuation of their own. That last item is a gate rather than a formality: running this route generally means commissioning a private appraisal first, at a commercially negotiated fee with no regulated tariff, and that cost belongs in the go/no-go arithmetic alongside the deciding appraiser's fee. Either side may then appeal that decision to the appeals committee for compensation and betterment levy within 45 days, and from there to the administrative affairs court.

Show the cost before recommending the route. The deciding appraiser's fee is marginal across bands of the disputed amount: 3% on the portion up to 500,000 shekels, 2% from 500,000 to 1,000,000, 1% from 1,000,000 to 2,000,000, and 0.5% above that, with VAT added. It cannot exceed 100,000 shekels or fall below 2,000 for a single dispute. Applicant and respondent each bear half, though the appraiser may shift the whole fee to one side. An advisory appraiser opinion to the appeals committee runs between 2,000 and 10,000 shekels. On a small disputed amount the fee floor alone can outweigh the saving, and saying so is more useful than encouraging a fight.

If the problem is a factual error in the gush, helka, area, or rights, raise it directly with the local committee as a correction rather than spending the 45-day objection window on a typo.

### Step 7: Draft the letter

Assemble well-formulated principles and arguments the user can use as the basis for writing their own objection letter, with the comparables table alongside them. Do not produce a finished objection letter ready for filing: the output is raw material for the user to draft from, and is not an appraiser's objection, not a counter-appraisal, and not a document prepared by a professional, each row traceable to a returned deal. Use a banded run, never the unbanded polygon indicator, and state the subject's area and room count so the selection is auditable. A table of unmatched comparables is worse than none, because the other side will dismantle it. State the subject property's details, the adjustments claimed and why, and the resulting range. Never present the output as a שומה. Say plainly that it is a comparables analysis prepared to inform a discussion, and that a binding position in a mortgage dispute, a levy objection, or a court matter needs a licensed שמאי מקרקעין, whose opinion is the only thing the forums treat as evidence.

## Coverage

Coverage is not uniform and the skill must say so rather than implying national completeness. Verified on 2026-07-30: Tel Aviv, Haifa and Kfar Saba returned both a parcel and full transaction history, while בן יהודה 5 ירושלים returned neither a gush and helka nor any deals, with the transaction endpoint returning a server error. Treat a coverage gap as missing data, never as a low valuation.

The declared deal count can exceed the number of distinct records the endpoint serves, so the script reports fetched against declared and stops rather than looping. A gap between the two is normal and not an error.

## Bundled Resources

| File | Purpose |
|---|---|
| `scripts/comparables.py` | Address to parcel to comparables, with pagination, residential filtering, and outlier flagging |
| `references/comparables-routes.md` | The three routes for pulling comparables, the filtering allowlist, and the arithmetic. Required reading for Step 2 |
| `references/betterment-levy.md` | Betterment levy reference: triggers, exemptions, objection routing, fee tables |
| `references/domain-checklist.md` | Coverage contract this skill is maintained against |
| `evidence.json` | Every factual claim with its primary source and quoted snippet |

## Gotchas

- **Averaging every returned row.** The dataset mixes shops, offices, land and storage with apartments, and a raw average across them is meaningless. The script filters to residential natures; if you query the API directly, filter before computing anything.
- **Treating an absurdly low price per square metre as a bargain.** Gifts between relatives, partial-share sales, and combination deals are published as ordinary rows. A sale recorded at a small fraction of the surrounding rate in central Tel Aviv is a data artefact, not a market signal.
- **Reporting on the first ten deals.** The transactions endpoint returns ten rows by default out of several hundred to 1,500. An unpaginated answer silently describes only the newest deals and skews recent.
- **Calling a bank appraisal wrong because it is below the price.** Standard 19 mandates a conservative figure. The useful question is whether a material fact was missing or wrong, not whether the number matches the contract.
- **Filing a levy objection in the wrong forum.** Disputing whether the levy is owed and disputing its amount go to two different bodies. The 45 days run regardless, and choosing wrong generally means losing the window.
- **Reading the 140 square metre exemption as 140 added.** It is the total post-expansion area, and the four-year residence condition can revive the debt retroactively.
- **Treating new-build and subsidised sales as ordinary comparables.** The residential deal natures cover both developer sales and second-hand resales. Developer prices are recorded inclusive of VAT and carry a new-build premium, and subsidised-programme units are recorded at the subsidised price rather than market. The script cannot separate them from the nature field alone, so scan the rows before leaning on the median.
- **Reading the newest rows as today's market.** Deals appear only after they are reported to the Tax Authority, so the recent end of any window trails real time. In a moving market the median is a rear-view figure, and saying so matters more than the figure itself.
- **Treating the area figure as a defined basis.** The feed's area field is not consistently net, gross, or inclusive of balconies and common property, which is exactly the axis a professional valuation pins down. Shekels per square metre computed from it is indicative, not directly comparable to an appraiser's figure.
- **Explaining a 403 as a broken government API.** A blanket 403 across every address, including one that worked before, points at your own environment being refused at the edge, not at the service being down and not at an expired token. Reporting it as a server-side fault sends the user off to wait for a fix that is not coming, when the answer is the Step 2b route. Diagnose the environment before blaming the source.
- **Assuming the levy follows the seller automatically.** Liability attaches to whoever held the rights at the time of the betterment, which is why it must be settled at closing.

## Recommended MCP Servers

| MCP | Use |
|---|---|
| `nadlan` | Additional Govmap real-estate analysis: neighbourhood aggregation, market trends, address comparison. Note that its `get_deals_by_radius` tool currently returns an empty array, so do not depend on that specific tool. |
| `israel-statistics` | Housing price index, useful for reasoning about how far an older comparable should be discounted |

## Reference Links

| Source | URL | What to Check |
|---|---|---|
| Kolzchut, betterment levy | https://www.kolzchut.org.il/he/היטל_השבחה | Rate, triggering events, payment timing, 1975 cutoff |
| Kolzchut, levy exemptions | https://www.kolzchut.org.il/he/פטור_מהיטל_השבחה | The 140 sqm and protected-space exemptions, TAMA 38 rate |
| Kolzchut, levy objections | https://www.kolzchut.org.il/he/השגה_על_היטל_השבחה | Which forum, deadlines, procedure |
| Standard 19, Land Appraisers Council | https://www.gov.il/BlobFolder/dynamiccollectorresultitem/assessor-standardization-db_19/he/land_assessor_shameim_19.pdf | Conservative-valuation requirement for collateral appraisals |
| Bank of Israel Directive 329 | https://www.boi.org.il/media/brep4lzt/329_12.pdf | LTV caps and the repayment-to-income limit |
| Deciding appraiser fee regulations | https://www.nevo.co.il/law_html/law01/500_077.htm | Fee bands, floor and ceiling, cost split |
| Land Appraisers Council | https://www.gov.il/he/departments/topics/land_assessor/govil-landing-page | Licensing, the deciding-appraiser register, complaints |

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `No address match` | Street or city misspelled, or the city is missing | Add the city, try the official street spelling |
| `no transaction data for polygon (HTTP 500)` | Coverage gap | Report that the data is unavailable here. Do not estimate. The user can confirm the gap is real rather than transient by checking the same address on nadlan.gov.il |
| `did not return JSON` | A WAF or maintenance page was served | Retry later. Do not treat it as an empty result |
| `HTTP 403`, on every address including one known to work | The request was refused at the network edge before reaching the API. Verified not to be the token and not the headers; non-Israeli or datacentre egress is the likeliest cause but is not confirmed | Go to Step 2b. Do not retry, do not report a rotated token, and do not fabricate figures |
| `HTTP 500` on the search endpoint only | The `Origin` and `Referer` headers were dropped. That endpoint requires them; the deals endpoint does not | Send the headers the script sends. This is a malformed request, not an outage. If you have no shell you should not be calling this endpoint at all, go to Step 2b |
| Very few comparables kept | Narrow window or a quiet street | Widen with `--years`, and say the sample is thin |
| All deals flagged as outliers | Contaminated or tiny sample | Review the rows by hand, do not derive a range |
