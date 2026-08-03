---
name: israeli-property-appraisal
description: "Build a comparable-transactions analysis for an Israeli property from official government data, and handle the appraisal processes around it: a low bank mortgage appraisal under Standard 19, and a betterment levy (heitel hashbacha) assessment. Use when someone asks what a property is worth, says the bank's appraisal came in low and blocked their mortgage, received a betterment levy bill from the local planning committee, or needs the gush and helka for an address. Resolves an address to its parcel, pulls real recorded transactions, and drafts the objection letter. Israeli property valuation is decided on recorded comparable deals that are public but effectively unreachable, so people accept a bank number or a municipal bill they could have challenged. Do NOT use for purchase tax or betterment tax (mas rechisha, mas shevach), Tabu extracts, rental agreements, mortgage track comparison, or land tenders. This is not a licensed appraisal (shuma) and does not replace a licensed shamai mekarkein."
license: MIT
---

# Israeli Property Appraisal

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

#### Step 2a: The bundled script

Run the bundled script. It resolves the address to a parcel and pulls the recorded transactions for the surrounding polygon:

```bash
# Market indicator for the street, no subject property
python3 scripts/comparables.py "דיזנגוף 100 תל אביב" --years 3

# Actual comparables, banded to the subject property
python3 scripts/comparables.py "דיזנגוף 100 תל אביב" --years 3 --area 75 --rooms 3
python3 scripts/comparables.py "הרצל 10 חיפה" --years 5 --area 90 --json
```

It prints the gush and helka, the neighbourhood, how many deals exist versus how many were used, and a median and range in shekels per square metre, followed by the deals themselves.

**Always pass the subject property when one exists.** Without `--area` and `--rooms` the script returns a median across every flat in the polygon regardless of size, floor or age. That is the price of the street, not the value of the apartment, and the script says so in its output. Only a banded run produces something that belongs in a letter to a bank or a committee.

**Read the filtering line before you read the median.** A typical central-Tel-Aviv polygon holds 1,500 recorded deals of which roughly 70 are residential sales inside a two-year window. The rest are shops, offices, land and older transactions. If the script kept very few deals, say so rather than presenting a median computed from four rows as if it were a market rate.

**Never state a value the script did not return.** If the address is in a coverage gap the script exits with an error, and the correct response is that the government data does not cover this address, not an estimate assembled from general knowledge of the neighbourhood.

#### Step 2b: No shell available

Do not attempt the endpoints directly, and do not present the failure as a temporary outage.

There are two routes here, and which one you have depends on whether anything can run locally on the user's machine.

**Route 1, the `nadlan` MCP, when it is connected.** This is full automation and it is the better answer where it is available. An MCP server runs as a local process on the user's own machine, so it uses their network rather than yours, which is why it succeeds where your own call is refused. That also means it only helps on a client that runs local MCP processes, in practice Claude Desktop. On claude.ai, ChatGPT and Manus there is no local process, so a remote MCP sits on the same ranges that were refused and its failure is that same refusal, not an MCP fault. Use `get_valuation_comparables`, which takes `address`, `years_back`, `min_area` / `max_area`, `min_rooms` / `max_rooms`, `min_floor` / `max_floor`, `radius_meters` and `deal_type`, and returns deal rows carrying `gushNum` and `parcelNum`, so it answers the parcel-lookup job from Step 1 too. Pass `deal_type=2` for resales and `deal_type=1` for new construction rather than mixing them. Note that `get_street_deals` and `get_deals_by_radius` are disabled in current builds, so do not route through them.

**Filter the MCP's output yourself. It does NOT return residential rows only.** Verified on 2026-08-02: a comparables query for הרצל 10 חיפה returned a `מלאכה` workshop of 100 square metres at 708,000 shekels alongside the flats, and that row landed inside the tool's own price-per-square-metre statistics as the minimum and the 25th percentile. Its `market_statistics` block is therefore not safe to quote directly. Take the `deals` array, apply the residential-nature allowlist and every other rule in the filtering list below, and compute the median yourself.

**Route 2, send the user to the source.** Where no MCP is connected, this is the only route that produces comparables. Nadlan publishes the same records at <https://www.nadlan.gov.il>: they enter the address, open the deals list for the surrounding polygon, and paste the rows back. You then apply the whole of Steps 3 to 7 to what they pasted, which is where most of this skill's value sits anyway. The same page shows the gush and helka, which is how the parcel-lookup job in Step 1 gets answered here.

**On route 2, ask what the list said before you use what was pasted.** The site paginates and shows the newest deals first, which is why the script pages through to the declared total. Ask the user how many deals the list declared and how many rows they actually copied. If they pasted only the first page, say so and label the result recency-skewed, because the newest rows already trail the real market.

**Apply the script's filters by hand to whatever you get, from either route.** The safeguards that make a median defensible live in the script, not in the data and not in the MCP, so on this path you have to run them yourself before computing anything:

- **Keep only residential rows.** The feed mixes shops, offices, land and storage into the same list. Keep `דירה בבית קומות`, `דירה`, `דירת גן`, `דירת גג`, `פנטהאוז`, `בית בודד`, `דו משפחתי`, `קוטג' חד משפחתי`, `קוטג' דו משפחתי`, and drop the rest. Averaging across natures is the classic wrong answer.
- **Band to the subject property.** Without a size and room filter you are describing the price of the street, not the value of the flat. Restrict to plus or minus 25 percent of the subject area and to within one room of the subject, which is what the script's own defaults do, before you call anything a comparable. Where a row does not state a room count the script keeps it on area alone, so do the same rather than dropping it and thinning the sample further.
- **Cut the window.** Anything older than the window the user asked for belongs out of the sample, and you should say which window you used.
- **Flag the outliers rather than averaging them in.** Gifts between relatives, partial-share sales and combination deals publish as ordinary rows at a small fraction of the surrounding rate. Pull them out, show them separately, and never let them move the median.
- **Drop new-build and subsidised rows, or mark them.** The nature list above admits developer sales, which are recorded inclusive of VAT and carry a new-build premium, and subsidised-programme units recorded below market. Neither is a comparable for an ordinary second-hand flat. This is a filtering step here, not just a caveat.
- **Keep leasehold and freehold apart.** A unit held on a lease from Rashut Mekarkein Yisrael is not directly comparable to full ownership. If the rows do not say which, say that you could not tell.
- **Count what survived.** Say how many rows the user pasted and how many you actually used. A median over four rows is not a market rate, and a thin sample has to be labelled as one.

Then do the arithmetic the way the script does it, and say that this is what you did:

- **Price per square metre is the deal amount divided by that row's own area field.** Never divide a total by a summed area, and never carry a figure across rows.
- **Report the median, not the mean.** The mean is what non-arm's-length rows distort most.
- **Use a defined outlier rule, not judgement, and measure it against the median.** Take the median of the price-per-square-metre values, then the median of each row's absolute distance from it (the median absolute deviation). Treat a row as an outlier when `0.6745 x (row - median) / MAD` exceeds 3.5 in absolute value. Show those rows, exclude them from the median and range, and never delete them.
- **Do NOT use quartile fences on a thin sample.** The obvious rule (below Q1 minus 1.5 IQR, above Q3 plus 1.5 IQR) breaks exactly where you need it. On five rows the upper half is only two values, so a single extreme row inflates Q3 and the fence outruns the row it was meant to catch: `10000, 10100, 10200, 10300, 100000` produces a fence of 122,800 and flags nothing. The same holds at four rows and in both directions, and a gift recorded far below market is the more damaging miss because it drags the median down. Measuring against the median avoids this, because a minority of extreme rows cannot move it.
- **If more than half the rows share one price per square metre, flag nothing.** There is no dispersion to judge against and any pick would be arbitrary. Say so.
- **Below four rows, do not flag at all.** The script does not, because no dispersion measure is meaningful on three values. Present the rows themselves and say a median would not be reliable.

**State nothing the pasted rows do not support.** This is the Step 2a rule about never inventing a value, and it binds harder here, because the dangerous case on this path is partial data rather than none: a handful of pasted rows topped up from what you remember about the neighbourhood. Do not supplement a thin paste from general knowledge, and do not present a hand-assembled table as if it had the script's coverage.

Every caveat in Step 3 and in Gotchas still applies, in particular that the feed's area field has no consistent basis and that recent rows trail the real market. Step 7 also binds on this path: state the subject's area and room count alongside the selection so the letter is auditable.

Everything in this skill except the data pull works without the feed. The Standard 19 explanation, the betterment-levy exemption check, the objection routing and the letter are all reachable, so say what you cannot do and continue with what you can.

**Say plainly that you have no figures.** With no deals in hand you have no median and no range. Do not fill the gap with remembered neighbourhood prices, and do not describe a number as approximate when it has no source at all.

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

Produce the objection or counter-appraisal letter with the comparables table embedded, each row traceable to a returned deal. Use a banded run, never the unbanded polygon indicator, and state the subject's area and room count so the selection is auditable. A table of unmatched comparables is worse than none, because the other side will dismantle it. State the subject property's details, the adjustments claimed and why, and the resulting range. Never present the output as a שומה. Say plainly that it is a comparables analysis prepared to inform a discussion, and that a binding position in a mortgage dispute, a levy objection, or a court matter needs a licensed שמאי מקרקעין, whose opinion is the only thing the forums treat as evidence.

## Coverage

Coverage is not uniform and the skill must say so rather than implying national completeness. Verified on 2026-07-30: Tel Aviv, Haifa and Kfar Saba returned both a parcel and full transaction history, while בן יהודה 5 ירושלים returned neither a gush and helka nor any deals, with the transaction endpoint returning a server error. Treat a coverage gap as missing data, never as a low valuation.

The declared deal count can exceed the number of distinct records the endpoint serves, so the script reports fetched against declared and stops rather than looping. A gap between the two is normal and not an error.

## Bundled Resources

| File | Purpose |
|---|---|
| `scripts/comparables.py` | Address to parcel to comparables, with pagination, residential filtering, and outlier flagging |
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
