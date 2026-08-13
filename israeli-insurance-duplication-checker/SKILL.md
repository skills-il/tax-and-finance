---
name: israeli-insurance-duplication-checker
description: "Not insurance advice and not insurance marketing. Audits the insurance an Israeli household already pays for, across health, disability, life, motor, home, travel and service riders, and separates real duplication from cover that legitimately stacks. Use when a user asks whether they are paying twice for insurance, wants to cut insurance costs, mentions כפל ביטוחי, holds a שב\"ן plan alongside a private health policy, has surgery cover through an employer or professional group, wonders whether a private אכ\"ע policy is redundant next to the pension fund, or asks which policy to cancel first. Do NOT use for comparing or buying new policies (israeli-insurance-comparator), for co-pays and costs inside the public health system (israeli-hmo-navigator), or for the pension savings product itself (israeli-pension-advisor)."
license: MIT
---

# Israeli Insurance Duplication Checker

## Legal notice

This skill is not insurance advice (ייעוץ ביטוחי) and not insurance marketing (שיווק ביטוחי), and it is not delivered by a licensed agent, advisor or marketer. It maps cover the user already holds and explains the statutory rules that decide whether two policies can pay twice for the same event. It does not recommend buying, replacing or surrendering a named product, does not exercise professional discretion on anyone's behalf, and does not replace a licensed insurance agent or advisor, the insurer, or the kupat cholim. Nothing here is legal advice. Cancelling underwritten cover is irreversible in practice: state the conclusion, then tell the user to confirm it with the insurer or a licensed agent, and never let them cancel a policy before replacement cover is confirmed active.

## Problem

Israelis routinely pay for the same cover in three or four places at once: a שב"ן plan at the kupa plus a private health policy, an employer group policy on top of both, a service subscription that is also a rider on the home policy and also a credit-card benefit. About 37% of the statutorily insured public, roughly 3.4 million people, hold commercial health cover alongside שב"ן (Knesset research centre, 2023, on 2020 data), and the State Comptroller puts the resulting overpayment at a floor of hundreds of millions of shekels a year. The official duplication tool, הר הביטוח, holds no שב"ן data at all, so it structurally cannot see the most common overlap in the country. Meanwhile some of what looks like duplication is not waste at all and cancelling it destroys cover the user can never buy back.

## The three-tier test (apply this before anything else)

Israeli law sorts insurance by PAYMENT MECHANISM, not by subject matter. Getting this wrong is the single biggest failure mode. Do not reason from "these two policies both mention surgery"; reason from how each one pays.

| Tier | Examples | Governing rule | Does it duplicate? |
|---|---|---|---|
| Property and liability | רכב מקיף, צד ג', ביטוח דירה ותכולה | ס' 59 לחוק חוזה הביטוח, applied directly | Yes, and this is real waste |
| Reimbursement (שיפוי) | ניתוחים, תרופות, loss-based אכ"ע | ס' 56(א) via ס' 54(ב) | Yes, but recovery is capped at the actual loss |
| Fixed sum (פיצוי) | ביטוח חיים, מחלות קשות, fixed-sum נכות | פרק ב' via ס' 54(א) | No. It genuinely stacks, and this is NOT waste |

The mechanics behind the table, which the agent should be able to state when challenged:

- ס' 59 is the ביטוח כפל provision, not ס' 56. Its own text is asset-bound: "בוטח נכס בפני סיכון אחד אצל יותר ממבטח אחד לתקופות חופפות". ס' 67 extends it to ביטוח אחריות, so liability cover is caught too, and ס' 64 makes it non-derogable except in the insured's favour.
- Under ס' 59(ג) the insurers are liable "יחד ולחוד לגבי סכום הביטוח החופף". The insured is not left chasing two companies; they simply cannot collect the overlap twice, and the insurers settle the split between themselves.
- ס' 54(ב) imports only ss. 42, 49, 52, 56, 61, 62 and 64 into loss-based accident, illness and disability cover. ס' 59 is absent from that list. What actually caps reimbursement health cover is ס' 56(א), "חובת השיפוי של המבטח תהיה כשיעור הנזק שנגרם".
- ס' 54(א) routes fixed-sum cover to פרק ב', which contains no כפל provision and no indemnity ceiling. So a standalone ריסק, a mortgage life policy and the שאירים cover inside the pension all pay on the same death. Say so plainly. A user who cancels one of them because an agent called it "duplication" has lost cover for nothing.

## The safe-cut rule (the organising principle of every recommendation)

Cancel only the layer the user can BUY BACK.

A kupat cholim must accept anyone into its שב"ן regardless of health, "ללא קשר למצבו הבריאותי או הכלכלי... למעט תקופות אכשרה סבירות" (ס' 10(ג)(1) לחוק ביטוח בריאות ממלכתי). It can make the user wait; it cannot refuse them. A private policy is gated by חיתום, and if the user's health changed since they bought it, they cannot repurchase it at any price.

So the sequence is always: map first, verify with the insurer or a licensed agent second, cancel last. Where two layers overlap and one has to go, the reversible layer goes first unless the user has a specific reason to prefer otherwise.

## Audit workflow

### Step A. Build the inventory

Ask for, or have the user pull:

1. הר הביטוח, the personal insurance file, from the ONLY official domain: `harb.cma.gov.il`, logging in through the government identification system. It shows life, health, disability, motor and home policies, but only to the בעל הפוליסה, so a spouse's policies will not appear in the user's own file.
2. The kupa's personal area, for the שב"ן plan and tier. הר הביטוח will not show this.
3. Payslip and the employer's benefits page, for group health, group אכ"ע, and any employer-bundled service plan.
4. Credit-card benefit pages for every card held.
5. Bank statements and credit-card statements scanned for small recurring charges: towing, home trades, windscreen, gadget cover, roadside subscriptions. This is where the cheapest wins live and no register lists them.

### Step B. Sort every line into one of the three tiers

Use the table above. Label each item שיפוי, פיצוי or נכס/אחריות. Do not proceed until every line has a tier, because the verdict for the same words ("ניתוחים", "נכות") differs by tier.

### Step C. Health

Handle the reform correctly, because most secondary sources do not.

- The שקל ראשון reform took effect in June 2024, "שמטרתה לצמצם את תופעת כפל הביטוחים". February 2016 is only the purchase-date cutoff defining which policies were caught. Never call the reform a 2016 event.
- The reform applied to פוליסות פרט only, and the window to reverse the automatic transfer closed on 1.6.2025. It is no longer a live choice.
- GROUP policies were never auto-converted, and most group surgery cover is still מהשקל הראשון. Everyone whose surgery cover comes through an employer or a professional organisation was left duplicating, untouched by the reform.
- Anyone who bought their individual policy BEFORE February 2016 was never caught by the reform either.

Those last two populations are this skill's core audience. Ask explicitly: is the policy individual or group, and when was it bought? Do not write the health section of the report as though the reform solved the problem.

Overlap by layer, once the track is known:

- ניתוחים בישראל: heavy overlap between a מהשקל הראשון policy and שב"ן. The regulator's own position is that מהשקל הראשון cover "חופפות במידה רבה לשירותים שניתנים בשב"ן", while a משלים שב"ן policy "לא כוללות כפל ביטוחי".
- אמבולטורי (consultations, imaging, second opinions): heavy overlap and badly under-discussed. Check it.
- ניתוחים בחו"ל, השתלות, תרופות מחוץ לסל: the catastrophic tail. Genuinely additional to שב"ן. Do not flag as waste.
- מחלות קשות: fixed sum, so it cannot duplicate anything. Leave it alone.

Note on labels: מהשקל הראשון and משלים שב"ן are market names for the two tracks, not statutory terms. Use them because the user's documents use them, but do not attribute them to a specific regulation by those names.

Group cover has a structural time limit: a group health policy runs for at most five years, so it is temporary by design. On leaving the group there is a right to convert to an individual policy without fresh underwriting or a fresh אכשרה, subject to conditions the regulator sets. State the right; do not state a deadline, and warn that the converted individual premium is typically far above the subsidised group rate.

### Step D. אובדן כושר עבודה (get this right, it is counterintuitive)

"You already have אכ"ע through your pension, so cancel the private policy" is WRONG, and it is the most damaging piece of common advice in this domain.

The pension fund's disability test is עיסוק סביר: the member must be unable to work "בעבודתו או בכל עבודה אחרת המתאימה לו לפי השכלתו, הכשרתו או ניסיונו". A surgeon who can no longer operate but could work in administration may collect NOTHING from the fund. Filling exactly that gap is what a private policy (מטריה ביטוחית) is for. The gap, not the cap, is the reason it is not redundant.

The two 75% rules are different instruments on different bases, and the skill must say which one it means:

- Inside a pension or provident fund: "סכום קצבת הנכות לא יעלה על 75% מן השכר המבוטח בקופת הגמל".
- In the uniform private policy: 75% of the average salary insured under that plan.

Cross-insurer offset does NOT trigger at 75%. It triggers only when total monthly benefit from all insurers exceeds "100% ממוצע השכר של המבוטח מכל מקור הכנסה", and even then the private policy still pays a floor: "הפיצוי החודשי שישולם למבוטח לא יפחת, בכל מקרה, משיעור של 30% מסכום הפיצוי החודשי לו הוא זכאי על פי תנאי התכנית". So the band above the per-policy cap and up to 100% of income is legitimate cover, not waste. A pension fund counts as a "מבטח אחר" for this purpose.

Excess-premium refund exists in the uniform policy but is capped at seven years AND conditional on a claim: "לא קרה מקרה הביטוח, המבוטח לא יהיה זכאי להחזר פרמיה". Never claim, never get it back. Tell the user this rather than letting them assume the money is banked.

Two related rules worth surfacing: at the point of sale the insurer must check the מסלקה, must refuse to sell against income that is already insured, and must cancel a duplicate (חוזר ביטוח 2018-1-8). And an אכ"ע premium may never be funded out of מרכיב הפיצויים.

### Step E. Motor, home and the service riders

- The real motor duplication is a standalone צד ג' bought on top of a מקיף. מקיף and צד ג' are two chapters of one prescribed policy, so this is textbook ס' 59.
- Car versus home צד ג' is NOT a duplication. The standard home policy excludes liability arising from a רכב as defined in the road-accident compensation law. The two are carved apart by construction. Do not put it on the list.
- תכולה riders are partial overlap, not waste. The standard policy caps jewellery as a fraction of the contents sum and excludes theft outside the home, in a vehicle and abroad. A כל הסיכונים rider lifts exactly those limits. Ask what the rider actually covers before calling it redundant.
- כתבי שירות are the highest-yield manual audit in the whole workflow. Towing, home trades and windscreen typically sit in three or four places at once: a policy rider, a credit-card benefit, a direct subscription, and an employer or utility bundle. The service company's own contract carries a clawback and subrogation covenant and states "אין כפל הטבות". The user gets the tow once; the extra subscriptions deliver only extra monthly charges. הר הביטוח lists none of these.
- There is no retroactive refund for a duplication the user created themselves. The reduction under ס' 59(ב) runs forward only, "מיום הדרישה". Retroactive refunds have been ordered only where the INSURER created the duplicate. Do not promise money back on past premiums.

### Step F. Travel

- No Israeli card issuer requires the trip to be charged to the card. That is the US and UK model and it is the most repeated false belief in Israeli consumer content on this subject. What matters is that the card is valid, and for discount benefits, that the policy premium is paid on that card.
- Most Israeli cards give a DISCOUNT, not embedded cover, typically a few free days and then a percentage off. Verified embedded exceptions are CAL Visa Infinite and Isracard World Elite. MAX's embedded cover for its פלטינה and זהב עסקי tiers ended in 2017.
- Everything that is not embedded requires activation before every single trip. The classic failure is believing the card covers you and never activating.
- The six-month pre-existing-condition exclusion is statutory, not underwriter discretion. It excludes "מחלה שבשלה היה המבוטח בטיפול או בהשגחה בעת צאתו לחוץ לארץ או במשך ששת החדשים שקדמו לצאתו".
- A standalone policy is genuinely needed on top of a card benefit for: pre-existing conditions, pregnancy, extreme and winter sports, trips longer than the age-banded day caps, ביטול נסיעה for non-medical reasons (absent from every card product examined), high-value gear above the כבודה sub-limits, and ages 80 and over.
- Do not invent per-card specifics. Give the user a checklist of what to verify on their own card's benefit page.
- Travel policies do not appear in הר הביטוח.

### Step G. The ותק and אכשרה trap, before anyone cancels anything

- Switching kupa preserves שב"ן ותק only if the user joins the new kupa's שב"ן within 90 days, and only between parallel tiers. Moving up a tier means serving the receiving kupa's אכשרה for the upgrade.
- Cancelling a שב"ן and re-joining the SAME kupa later restarts the waiting periods from scratch.
- Current tier names, because users and marketing material both garble them: מכבי has כסף, זהב and שלי (three cumulative tiers); כללית has מושלם זהב and מושלם פלטינום; מאוחדת has עדיף and שיא (there is no "זהב" at מאוחדת); לאומית has כסף and זהב.

### Step H. Cancellation mechanics

- The 14-day distance-selling withdrawal right does NOT apply to insurance. חוק הגנת הצרכן excludes insurers entirely. This is widely believed and false, and a user who relies on it will be caught out.
- The real instrument is חוזר ביטוח 2017-1-3, in force since 1.7.2017: every insurer must run a front-page area titled "ביטול פוליסה קיימת", plus email, personal-account, phone and fax routes, an automatic acknowledgement, and three business days to report deficiencies.
- Cancellation by the INSURED takes effect three days after the notice reaches the insurer: "מתבטל החוזה כעבור שלושה ימים מהיום שבו נמסרה הודעת הביטול למבטח". The fifteen days often quoted is the insurer's side. Do not swap them.
- Life insurance may be cancelled at any time by written notice.
- שב"ן cancellation notice is set by each kupa's תקנון, not by statute. Check the specific kupa.
- An insurer may not sell a duplicate פיצוי policy unless the insured confirms in writing after being told they will be charged for both (חוזר צירוף 2016-1-7). And a הר הביטוח lookup is required before every sale, with no opt-out at all in שיווק יזום.

## Deliverables

Produce all three, in this order:

1. **A layer-by-layer duplication map.** One row per cover the user holds, with its tier, what overlaps it, and a verdict of one of: REAL WASTE (pays once, charged twice), CAPPED (recovery limited to actual loss, so the second policy buys little), PARTIAL (the rider lifts a specific limit, keep or cut on price), or LEGITIMATE STACKING (pays cumulatively, cancelling loses cover).
2. **The questions to put to the agent or insurer**, phrased so they can be read out. For each flagged overlap: "האם הפוליסה הזו משלמת שיפוי או פיצוי?", "אם יש לי גם שב\"ן, על מה בדיוק הפוליסה הזו מוסיפה?", "מה תקופות האכשרה אם אחזור לרכוש את הכיסוי הזה בעוד שנה?", "מה הפרמיה החודשית של הכיסוי הזה בנפרד?".
3. **A Hebrew cancellation letter**, only for lines the user has decided to cut after verifying. Use `references/cancellation-letter-he.md`.

Never emit deliverable 3 for a line the user has not confirmed with their insurer or agent, and never for a line whose replacement cover is not already active.

## Recommended MCP Servers

| MCP | Why it helps here |
|---|---|
| `kolzchut` | Israel's rights database. Good for the surrounding rights picture: what the public basket already covers, what a קופת חולים owes a member, and eligibility routes a user might be insuring against unnecessarily. Install page: https://agentskills.co.il/he/mcp/kolzchut |

No MCP exposes a user's personal insurance file. הר הביטוח is behind government identification and must be pulled by the user.

## Reference Links

| Source | What it settles |
|---|---|
| [חוק חוזה הביטוח, תשמ"א-1981, נוסח מאוחד](https://www.nevo.co.il/law_html/law00/71902.htm) | ס' 54(א) and ס' 54(ב), the split between fixed-sum and reimbursement cover; also ס' 59, ס' 56, ס' 10(ב) and ס' 45 |
| [מבקר המדינה, ביטוחי בריאות](https://library.mevaker.gov.il/sites/DigitalLibrary/Documents/2020/71A/2020-71A-201-Health-insurance.pdf) | הר הביטוח holds no שב"ן data; the scale of overpayment |
| [מרכז המחקר והמידע של הכנסת](https://fs.knesset.gov.il/globaldocs/MMM/38209512-c6ce-ed11-815a-005056aa4246/2_38209512-c6ce-ed11-815a-005056aa4246_11_20077.pdf) | 37% of the insured public, about 3.4 million people, duplicating |
| [משרד הבריאות, ביטוח ניתוחים בישראל](https://www.gov.il/BlobFolder/reports/insurances-surgeons-2025/he/files_publications_digital_health_insurances-surgeons-2025.pdf) | The שקל ראשון reform took effect in June 2024 |
| תקנות הפיקוח על שירותים פיננסיים (קופות גמל) (כיסויים ביטוחיים בקופות גמל), תשע"ג-2013 | The 75% ceiling on disability pension inside a fund |
| הפוליסה האחידה לביטוח אובדן כושר עבודה, published by every insurer | The 100% offset trigger, the 30% floor, and the no-claim-no-refund rule |
| חוק ביטוח בריאות ממלכתי, תשנ"ד-1994 | ס' 10(ג)(1), the duty to accept any member into the kupa |

The last three rows carry no link on purpose: their canonical URLs contain Hebrew characters, and a percent-encoded link breaks the skill's fact-grounding gate. The full URLs and the verbatim quotes live in `evidence.json` alongside this file.

## Gotchas

These are agent failure modes, not user mistakes.

1. **Treating every overlap as waste.** The most expensive error in this skill runs in the direction of cancelling. Fixed-sum cover stacks by law, so a standalone ריסק plus a mortgage life policy plus שאירים in the pension all pay on the same death, and cancelling one loses real money for nothing. Run the three-tier test before writing a single verdict.
2. **Sending the user to the wrong הר הביטוח.** The only official domain is `harb.cma.gov.il`. The sites at `harhabituach.org`, `harhabituach.co.il` and `har-bituach.org.il` are commercial lead-generation operations, and the last one uses a `.org.il` suffix to look like a public body. The skill tells people to go pull their full insurance file, so it owes them the real address. Also, הר הביטוח concedes its own duplicate alert is not dispositive ("חשוב לדעת כי ההתראה אינה מחייבת תמיד כי נרכש כיסוי מיותר"), and it is a last-month snapshot, so treat a missing alert as no evidence either way.
3. **Assuming הר הביטוח is complete.** It has no שב"ן data at all, no travel policies, no service subscriptions and no credit-card benefits. It shows policies only to the בעל הפוליסה, so a spouse's cover is invisible. Group cover is excluded only in the narrow case where the employer funds the entire premium AND the policy is written למבוטח לא מסוים, so the blanket claim that employer policies are absent is wrong.
4. **Recommending a cancellation before the replacement is active, or cancelling the underwritten layer first.** שב"ן must re-accept the user; a private policy will not. If the agent is unsure which layer is reversible, it must stop and ask rather than guess.
5. **Advising a household from one person's file.** Motor, home and health files are per-policyholder. A "duplication" that disappears when the spouse's file is pulled is a very common false positive, and so is a duplication that only appears once both files are on the table.

## Troubleshooting

**The user says הר הביטוח shows nothing.** Login is through the government identification system and the data is a snapshot of the previous month. A very recent policy may not appear yet. Fall back to the insurer's personal area and the last twelve months of bank and card statements.

**The user cannot tell whether a policy is שיפוי or פיצוי.** Look at how the benefit is described: a fixed monthly or lump sum regardless of expense is פיצוי; reimbursement of an invoice, or payment direct to a provider, is שיפוי. If the document is ambiguous, this is exactly the question to hand to the insurer, and the audit should mark the line UNRESOLVED rather than guess a tier.

**The user was told by an agent that the private אכ"ע is redundant.** Ask which disability test each instrument uses. The fund's test is עיסוק סביר. If the private policy is עיסוק ספציפי, the two are not the same product and the conclusion does not follow. Put the question in writing to the insurer.

**The user wants past premiums refunded.** There is no retroactive refund duty for cover the user chose themselves, in property or in health. The reduction under ס' 59(ב) is prospective. Set the expectation before the user makes a demand they will lose.

**The user's employer cover is about to end.** Raise the conversion right to an individual policy without fresh underwriting, flag that the individual premium is typically far above the subsidised group rate, and have them ask the insurer for the exact window and terms rather than relying on a number from this skill.

**Two insurers each say the other should pay.** For property and liability cover they are liable "יחד ולחוד לגבי סכום הביטוח החופף" and settle the apportionment between themselves. The user claims from either one and should say so.
