# Pulling the comparables, route by route

Read this in full before running Step 2. The text is moved verbatim from SKILL.md; nothing here is
a summary. Which route applies is decided by the table in Step 2.

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
