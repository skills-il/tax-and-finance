---
name: israeli-insurance-duplication-checker
description: "Not insurance advice and not insurance marketing. Audits the insurance an Israeli household already pays for, across health, long-term care, dental, disability, life, personal accident, motor, home, mortgage, travel and service riders, and separates real duplication from cover that legitimately stacks. Use when a user asks whether they are paying twice for insurance, wants to cut insurance costs, mentions כפל ביטוחי, holds a שב\"ן plan alongside a private health policy, has surgery cover through an employer or professional group, pays for a private ביטוח סיעודי next to the kupa group policy, wonders whether a private אכ\"ע policy is redundant next to the pension fund, or asks which policy to cancel first. Do NOT use for comparing or buying new policies (israeli-insurance-comparator), for co-pays and costs inside the public health system (israeli-hmo-navigator), or for the pension savings product itself (israeli-pension-advisor)."
license: MIT
---

# Israeli Insurance Duplication Checker

## Legal notice

This skill is not insurance advice (ייעוץ ביטוחי) and not insurance marketing (שיווק ביטוחי), and it is not delivered by a licensed agent, advisor or marketer. It maps cover the user already holds and explains the statutory rules that decide whether two policies can pay twice for the same event. It does not recommend buying, replacing or surrendering a named product, does not exercise professional discretion on anyone's behalf, and does not replace a licensed insurance agent or advisor, the insurer, or the kupat cholim. Nothing here is legal advice. Cancelling underwritten cover is irreversible in practice: state the conclusion, then tell the user to confirm it with the insurer or a licensed agent, and never let them cancel before replacement cover is confirmed active.

## Problem

Israelis routinely pay for the same cover in three or four places at once: a שב"ן plan plus a private health policy, an employer group policy over both, a service subscription that is also a home-policy rider and a card benefit. About 37% of the statutorily insured public, roughly 3.4 million people, hold commercial health cover alongside שב"ן, and the State Comptroller puts the overpayment at a floor of hundreds of millions of shekels a year. הר הביטוח holds no שב"ן data at all, so the official tool structurally cannot see the most common overlap in the country. And some of what looks like duplication is not waste: cancelling it destroys cover the user can never buy back.

## The three-tier test (apply this before anything else)

Israeli law sorts insurance by PAYMENT MECHANISM, not by subject matter. Getting this wrong is the single biggest failure mode. Do not reason from "these two policies both mention surgery"; reason from how each one pays.

**Tier the BENEFIT, not the policy.** A tier is a property of a CLAIM, not of an inventory line, and one policy can sit in two tiers at once. The kupot group סיעוד policy is the clearest case: it pays "פיצוי כספי של 5,000 ש\"ח לחודש למשך 60 חודשים אם הוא שוהה בביתו, ושיפוי כספי בסך 10,000 ש\"ח לחודש למשך 60 חודשים אם שוהה במוסד סיעודי". Fixed sum at home, reimbursement in an institution, one contract. A private health policy that carries a fixed-sum מחלות קשות rider alongside reimbursement ניתוחים cover has the same shape.

So a line with more than one benefit head splits into one row per benefit, each tiered separately. Where the tier depends on a future state, such as at home versus in an institution, say so in the map rather than picking one. A single verdict on a two-tier policy is wrong in one of the two worlds the user might end up in.

| Tier | Examples | Governing rule | Does it duplicate? |
|---|---|---|---|
| Property and liability | רכב מקיף, צד ג', ביטוח דירה ותכולה | ס' 59 לחוק חוזה הביטוח, applied directly | Yes, and this is real waste |
| Reimbursement (שיפוי) | ניתוחים, תרופות, loss-based אכ"ע | ס' 56(א) via ס' 54(ב) | Yes, but recovery is capped at the actual loss |
| Fixed sum (פיצוי) | ביטוח חיים, מחלות קשות, fixed-sum נכות | פרק ב' via ס' 54(א) | No. It genuinely stacks, and this is NOT waste |

The statutory mechanics behind the table, which the agent should be able to state when challenged, are set out in `references/line-by-line-detail.md`: ס' 59 is asset-bound and is the ביטוח כפל provision (not ס' 56), extended to liability by ס' 67 and made non-derogable by ס' 64; ס' 54(ב) does NOT import ס' 59 into loss-based health cover, so what caps it is ס' 56(א); and ס' 54(א) routes fixed-sum cover to פרק ב', which has no כפל provision and no indemnity ceiling.

## The safe-cut rule (the organising principle of every recommendation)

Cancel only the layer the user can BUY BACK.

A kupat cholim must accept anyone into its שב"ן regardless of health, "ללא קשר למצבו הבריאותי או הכלכלי... למעט תקופות אכשרה סבירות" (ס' 10(ג)(1) לחוק ביטוח בריאות ממלכתי). It can make the user wait; it cannot refuse. A private policy is gated by חיתום, and if health changed since purchase it cannot be repurchased at any price.

Sequence is always: map first, verify with the insurer or a licensed agent second, cancel last. Where two layers overlap and one must go, the reversible layer goes first unless the user has a specific reason otherwise.

## Audit workflow

### Step A. Build the inventory

**Run this per ADULT, not once.** Files are per-policyholder, and the commonest two-earner findings are invisible from one file: children enrolled on BOTH parents' employer health or dental plans, and a "duplication" that is really the spouse's policy seen twice. Every map row gets a covered-person column.

Ask for, or have the user pull:

1. הר הביטוח, the personal insurance file, from the ONLY official domain: `harb.cma.gov.il`, logging in through the government identification system. It shows life, health, disability, motor and home policies, but only to the בעל הפוליסה, so a spouse's policies will not appear in the user's own file.
2. המסלקה הפנסיונית, for what sits INSIDE the pension products: which bodies hold accounts, and the אכ"ע and שאירים cover attached to each. הר הביטוח does not open the pension savings products, so Step D cannot be answered without this. The official operator is `swiftness.co.il`, "האתר הרשמי של המסלקה הפנסיונית". An account is free and each request carries a small statutory fee. Do not quote the user a figure: the operator's own FAQ gives two different amounts for the same one-off all-products request, "20 ₪ (כולל מע\"מ)" in one answer and "14 ש\"ח" in another. Tell them it is a few shekels and to read the tariff shown at the point of request. The clearing house warns about "נסיונות להתחזות לגורמים מטעם המסלקה הפנסיונית", so treat any other site offering a free report as you treat the fake הר הביטוח domains.
3. The kupa's personal area, for the שב"ן plan and tier, AND for the group ביטוח סיעודי, which is arranged by the kupa and will not appear in הר הביטוח either.
4. Payslip and the employer's benefits page, for group health, group אכ"ע, group dental, and any employer-bundled service plan.
5. Credit-card benefit pages for every card held.
6. Bank and card statements, scanned for small recurring charges: towing, home trades, windscreen, gadget cover, roadside subscriptions. The cheapest wins live here and no register lists them.
7. With children: the school תשלומי הורים account (compulsory ביטוח תאונות אישיות לתלמידים) and any private child accident or dental rider on top.
8. With a mortgage: the loan file, for the ביטוח חיים and ביטוח מבנה tied to it, plus any separate ביטוח דירה.

### Step B. Sort every line into one of the three tiers

Use the table above, labelling each benefit שיפוי, פיצוי or נכס/אחריות. Do not proceed until every benefit has a tier: the verdict for the same words ("ניתוחים", "נכות") differs by tier.

### Step C. Health

Handle the reform correctly, because most secondary sources do not. It took effect in **June 2024**; February 2016 is only the purchase-date cutoff, so never call it a 2016 event. It applied to פוליסות פרט only, and the reversal window ran to 31 May 2025, though some insurers extended their own, so check rather than assume it is closed. **The GROUP market was affected far less and with delay**, because group policies update only every few years under the policyholder-insurer agreement, so much group surgery cover is still מהשקל הראשון. Do NOT say group policies were never converted; have the user check their own. Anyone who bought individually before February 2016 was not caught either. Those two populations are this skill's core audience, so ask whether the policy is individual or group and when it was bought. Group cover also has a five-year statutory limit and a conversion right on leaving without fresh underwriting or אכשרה, at a much higher individual premium. Detail in `references/line-by-line-detail.md`.

Overlap by layer, once the track is known:

- ניתוחים בישראל: heavy overlap between a מהשקל הראשון policy and שב"ן. The regulator's position is that such cover is "חופפות במידה רבה לשירותים שניתנים בשב"ן", while a משלים שב"ן policy "לא כוללות כפל ביטוחי".
- אמבולטורי (consultations, imaging, second opinions): heavy overlap, badly under-discussed. Check it.
- ניתוחים בחו"ל, השתלות, תרופות מחוץ לסל: the catastrophic tail, genuinely additional to שב"ן. Not waste.
- מחלות קשות: fixed sum, so it cannot duplicate anything, and no one should cancel it because an agent called it overlap. But "leave it alone" is not an audit. Households commonly hold it in four places at once (standalone, a rider on a private health policy, an employer group benefit, a rider inside a ביטוח מנהלים), with covered-condition lists that differ materially. The output is "stacks, so compare the condition lists and the sums, and cut on price only where two are near-identical". That is PARTIAL, and it is the one place PARTIAL applies to fixed-sum cover.
- שיניים: check it, because much of it may already be free. The basket covers dental care for children "שטרם מלאו להם 18 שנים" and "טיפולי שיניים למבוטחים שמלאו להם 72 שנים", where the periodic check-up, bitewing pair and scaling carry no co-payment at all. A policy bought for a nine-year-old or for someone over 72 is buying a lot of what the basket already provides. Dental is normally שיפוי, so the overlap is CAPPED, not stacking. The real non-basket exception is אורתודנטיה, expressly carved out of the children's trauma item, so orthodontic cover is PARTIAL rather than REAL WASTE.

Note on labels: מהשקל הראשון and משלים שב"ן are market names, not statutory terms. Use them because the user's documents do, but do not attribute them to a specific regulation by those names.

Group cover has a structural time limit: a group health policy runs for at most five years, so it is temporary by design. On leaving the group there is a right to convert to an individual policy without fresh underwriting or a fresh אכשרה, subject to conditions the regulator sets. State the right; do not state a deadline, and warn that the converted individual premium is typically far above the subsidised group rate.

### Step D. אובדן כושר עבודה (get this right, it is counterintuitive)

"You already have אכ"ע through your pension, so cancel the private policy" is WRONG, and it is the most damaging common advice in this domain.

The fund applies a BROAD-occupation test: the takanon defines a נכה as a member at least 25% of whose working capacity is impaired, and who therefore cannot work "בעבודתו או בכל עבודה אחרת המתאימה לו לפי השכלתו, הכשרתו או ניסיונו" for over 90 consecutive days. ("עיסוק סביר" is shorthand, not the takanon's term: quote the definition, not the label.) A surgeon who can no longer operate but could work in administration may collect NOTHING from the fund. Filling that gap is what a private policy is for. The gap, not the cap, is why it is not redundant.

The two 75% rules are different instruments on different bases, and the skill must say which one it means: inside a pension or provident fund the disability pension is capped at 75% of the insured salary in the fund; in the uniform private policy it is 75% of the average salary insured under that plan.

Cross-insurer offset does NOT trigger at 75%. It triggers only above "100% ממוצע השכר של המבוטח מכל מקור הכנסה", and even then the private policy still pays a floor that "לא יפחת, בכל מקרה, משיעור של 30% מסכום הפיצוי החודשי". So the band between the per-policy cap and 100% of income is legitimate cover, not waste. A pension fund counts as a "מבטח אחר" for this. The excess-premium refund is capped at seven years AND conditional on a claim: "לא קרה מקרה הביטוח, המבוטח לא יהיה זכאי להחזר פרמיה". At the point of sale the insurer must check the מסלקה and cancel a duplicate (חוזר ביטוח 2018-1-8), and an אכ"ע premium may never be funded out of מרכיב הפיצויים. Worked arithmetic is in `references/worked-examples.md`; full wording in `references/line-by-line-detail.md`.

**The one pension line that CAN be pure waste: שאירים cover with no שאירים.** A member with no survivors other than a parent may waive the death-risk cover, renewable "כל עוד אין לו שאירים", and during the waiver "לא ייגבו מהעמית דמי ביטוח בשל כיסוי ביטוחי למקרה מוות". A יתום here is a child "שטרם מלאו לו 21 שנים", or a child with a disability.

**But it is not a free saving, and this is why you raise it carefully rather than enthusiastically.** The fund may run חיתום רפואי when the member later asks to re-include the cover, and may then reject the request or exclude any pre-existing condition. The only escape is having kept paying for the default ביטוח המשך continuation cover throughout, which the member is also allowed to opt out of. So this is the safe-cut rule one level down: waiving without keeping continuation cover is a one-way door for anyone whose health changes. State the underwriting risk in the same breath as the saving, and send the user to confirm the continuation-cover position with the fund. Detail in `references/line-by-line-detail.md`.

Separately, a member who holds BOTH a קרן פנסיה and a ביטוח מנהלים may be paying for the same אכ"ע twice. That one is a genuine overlap and belongs in the map.

### Step D2. סיעוד (the biggest line in the country, and the hardest to undo)

Almost every household has this and most do not know its shape. Ask even when the user did not raise it.

Three separate things, which users conflate: **גמלת סיעוד from ביטוח לאומי** (statutory, under חוק הביטוח הלאומי פרק י', income-tested at household level, not a policy); **the kupa group policy** (the two-tier benefit above, under the 2015 group-LTC regulations and חוזר ביטוח 2016-1-3, bought "נוסף על גמלת הסיעוד של בט\"ל"); and **a legacy private policy**, held by about a million Israelis, "אשר נרכשו בעבר ואינם נמכרים יותר בשוק".

That last sentence is the whole verdict. **An individual סיעוד policy cannot be repurchased at any price, because the product is no longer sold at all.** This is not merely underwritten cover a sick user might fail to re-buy; a perfectly healthy user could not re-buy it either. Never put a legacy private סיעוד policy at the top of a cancellation list. Where the group and private policies genuinely overlap and one must go, the reversible layer is the group one, because kupa membership is not underwritten.

Two things NOT to say: that the group policy is being wound up on a stated date (a January 2025 draft proposed it, never issued, dropped), and that גמלת סיעוד does or does not offset a policy payout, which the sources do not settle. What to say instead: treat the arrangement as operating, and send the user to confirm its current status and their own tier with their kupa. Scale figures and statutory hooks are in `references/line-by-line-detail.md`.

### Step E. Motor, home, mortgage and the service riders

- The real motor duplication is a standalone צד ג' bought on top of a מקיף. מקיף and צד ג' are two chapters of one prescribed policy, so this is textbook ס' 59.
- Car versus home צד ג' is NOT a duplication: the home policy excludes liability arising from a רכב by construction. Do not put it on the list.
- תכולה riders are PARTIAL, not waste: a כל הסיכונים rider lifts exactly the limits the standard policy imposes. Ask what it covers before calling it redundant.
- כתבי שירות are the highest-yield manual audit here. Towing, home trades and windscreen typically sit in three or four places at once, the user gets the tow once, and הר הביטוח lists none of them. Detail in `references/line-by-line-detail.md`.
- **Mortgage cover: Directive 451 gives the borrower three levers.** The bank may require property and life cover up to the loan amount only as irrevocable beneficiary; it must tell the borrower prominently that he may buy both directly rather than through the bank's agency; the customer may cancel at any time without any fee against an alternative policy naming the bank; and the bank may not require structure cover above the unpaid revalued balance. No duty to insure loans up to 30,000.
- **Mortgage ביטוח מבנה against a separate ביטוח דירה is a ס' 59 question.** Confirm both really cover the structure before calling it REAL WASTE, and never cancel before the bank issues its consent to release the charge, or the loan may be treated as in breach.
- **ביטוח תאונות אישיות לתלמידים is already paid for**, compulsory through the local education authority, covering the child anywhere in Israel at any hour, not only school hours. A private child rider is fixed-sum and does stack, but tell the parent what the compulsory policy already buys.
- There is no retroactive refund for a duplication the user created themselves. The reduction under ס' 59(ב) runs forward only, "מיום הדרישה". Retroactive refunds are associated with cases where the INSURER created the duplicate; this skill has no sourced authority for a wider rule, so do not promise one. Do not promise money back on past premiums.

### Step F. Travel

- **Charging the trip to the card is generally not a condition on Israeli cards**, unlike the US and UK model. Treat that as the default, not a universal, and confirm it on the specific card.
- Most Israeli cards give a DISCOUNT, not embedded cover, and anything not embedded needs activation before EVERY trip. The classic failure is assuming the card covers you and never activating.
- The six-month pre-existing-condition exclusion is regulatory, not underwriter discretion.
- A standalone policy is genuinely needed on top of a card benefit for pre-existing conditions, pregnancy, extreme sports, long trips, ביטול נסיעה for non-medical reasons, high-value gear, and ages 80 and over.
- Do not invent per-card specifics; send the user to their own card's benefit page. Travel policies do not appear in הר הביטוח. Detail in `references/line-by-line-detail.md`.

### Step G. The ותק and אכשרה trap, before anyone cancels anything

- Switching kupa preserves שב"ן ותק only on joining the new kupa's שב"ן within 90 days, and only between parallel tiers. Cancelling and re-joining the SAME kupa restarts the waiting periods from scratch.
- Tier names, which users and marketing material both garble: מכבי has כסף, זהב and שלי; כללית has מושלם זהב and מושלם פלטינום; מאוחדת has עדיף and שיא (there is no "זהב" at מאוחדת); לאומית has כסף and זהב. These are marketing names, they change, and this list has no source of record behind it, so confirm the current one on the kupa's own site before writing it into a report.
- **Check residency before applying the safe-cut rule at all.** The rule assumes the kupa must re-accept the user. That fails for a new oleh, a תושב חוזר, someone on relocation, a dual citizen with foreign cover, or a non-resident spouse, and for them the private policy may be the ONLY cover rather than the redundant layer. This skill does not carry the waiting-period rules for those statuses: establish status, then have the user confirm entitlement before anything is cancelled.

### Step H. Cancellation mechanics

- The 14-day distance-selling withdrawal right does NOT apply to insurance: חוק הגנת הצרכן excludes insurers. Widely believed, and false.
- **Cancellation by the INSURED takes effect three days after the notice reaches the insurer.** The fifteen days often quoted is the insurer's side. Do not swap them.
- Every insurer must run an area titled "ביטול פוליסה קיימת" on the MAIN PAGE OF ITS WEBSITE and in the online personal account, plus other channels, with an automatic written acknowledgement and no more than three business days to report deficiencies (חוזר ביטוח 2017-1-3). Keep that acknowledgement: it proves the delivery date.
- שב"ן notice is set by each kupa's תקנון, not statute. Life insurance may be cancelled at any time in writing.
- An insurer may not enrol a user in a duplicate פיצוי policy unless they confirm after being told it duplicates an existing one and that both will be charged (חוזר צירוף 2016-1-7). A duplicate sold without that confirmation is challengeable and a ready-made ground for a complaint to the supervisor.

### Step I. When the insurer says no, and the clock the user cannot see

A duplication audit routinely turns up a benefit the user was entitled to and never claimed, and that starts a clock nothing makes visible to them.

- **Limitation is three years from the insured event**, and five for ביטוח חיים, ביטוח מפני מחלות ואשפוז and ביטוח סיעודי, on contracts made or renewed from 25.11.2020.
- **Lodging the claim does NOT stop the clock.** The insurer must say so itself: "אינו נעצר בעקבות מסירת התביעה למבטח". Users routinely assume a year of arguing preserves their position. It does not.
- **Escalation** is to the supervisor, who investigates conduct complaints but not a matter already before a court or arbitrator. Within a year of the deadline, the next step is legal advice on timing, not another letter. Wording and the complaints route are in `references/claims-and-escalation.md`.

## Deliverables

Produce all four, in this order:

1. **A layer-by-layer duplication map.** One row per BENEFIT, not per policy: split a policy with two benefit heads, per the three-tier test.

   Columns (schema in the detail reference): covered person, cover/benefit, tier, monthly premium, overlaps with, reversible?, verdict.

   Verdicts: **REAL WASTE** (pays once, charged twice), **CAPPED** (recovery limited to actual loss), **PARTIAL** (a rider lifts a limit, or two fixed-sum policies have near-identical condition lists, so cut on price), **LEGITIMATE STACKING** (pays cumulatively), **UNRESOLVED** (tier or terms unestablished, goes to the insurer first), **NOT A DUPLICATION**. Sort REAL WASTE by REVERSIBILITY first and premium only as a tiebreak, so a reversible layer always outranks an underwritten one. Never let premium size move an unrepurchasable line up the cut list.
2. **Questions to put to the agent or insurer**, phrased to be read out. Per flagged overlap: "האם הפוליסה הזו משלמת שיפוי או פיצוי?", "אם יש לי גם שב\"ן, על מה בדיוק הפוליסה הזו מוסיפה?", "מה תקופות האכשרה אם אחזור לרכוש את הכיסוי הזה בעוד שנה?", "מה הפרמיה החודשית של הכיסוי הזה בנפרד?".
3. **A short "gaps found" list.** An audit that only removes lines will leave a household with no אכ"ע at all and call it a success. Note any layer that is absent rather than duplicated: no disability cover on a sole earner, no סיעוד, a mortgage with no life cover. Naming an absence is not marketing and does not cross the legal line above. State the gap, name no product, route to a licensed agent. Comparing and buying is `israeli-insurance-comparator`.
4. **A Hebrew cancellation letter**, only for lines the user decided to cut after verifying. Use `references/cancellation-letter-he.md`.

Never emit deliverable 4 for a line the user has not confirmed with their insurer or agent, and never for a line whose replacement cover is not already active.

## Examples

Three end-to-end worked audits, with the map filled in and the arithmetic done, are in `references/worked-examples.md`. Read them before producing a first map: the three-layer health question, the אכ"ע case where the answer is to cancel nothing, and a two-adult household with a genuine REAL WASTE row.

## Bundled Resources

| File | When to use it |
|---|---|
| `references/domain-checklist.md` | The coverage contract: tier rule, the audience the reform left behind, non-negotiables, and the do-not-assert list. Read before adding any figure. |
| `references/worked-examples.md` | Three end-to-end audits with the map filled in and the אכ"ע arithmetic done. Read before producing a first map. |
| `references/line-by-line-detail.md` | Long-form detail behind Steps C to H: statutory mechanics, the reform, אכ"ע offset wording, the סיעוד instruments, mortgage, travel, cancellation, map schema. |
| `references/claims-and-escalation.md` | Full ס' 31 wording, the complaints route and the tolling analysis behind Step I. |
| `references/reference-links.md` | The full source table with what each one settles. |
| `references/cancellation-letter-he.md` | Deliverable 4 only. Hebrew cancellation template, pre-send checks, the שב"ן caveat, the mortgage irrevocable-beneficiary warning. Never emit for an unverified line. |

## Recommended MCP Servers

| MCP | Why it helps here |
|---|---|
| `kolzchut` | Israel's rights database. Good for the surrounding rights picture: what the public basket already covers, what a קופת חולים owes a member, and eligibility routes a user might be insuring against unnecessarily. Install page: https://agentskills.co.il/he/mcp/kolzchut |

No MCP exposes a user's personal insurance file. הר הביטוח is behind government identification and must be pulled by the user.

## Reference Links

Full source table in `references/reference-links.md`. Load-bearing: [חוק חוזה הביטוח](https://www.nevo.co.il/law_html/law00/71902.htm) for the tier split and ס' 31; [מבקר המדינה, הביטוח הסיעודי](https://library.mevaker.gov.il/sites/DigitalLibrary/Documents/2026/Population-Aging/2026-Population-Aging-102.pdf) for סיעוד; [הוראה 451](https://www.boi.org.il/media/utld2tgp/451.pdf) for mortgage cover. Verbatim quotes are in `evidence.json`.

## Gotchas

These are agent failure modes, not user mistakes.

1. **Treating every overlap as waste.** The most expensive error runs in the direction of cancelling. Fixed-sum cover stacks by law, so a standalone ריסק plus a mortgage life policy plus שאירים in the pension all pay on the same death. Run the three-tier test before writing a single verdict.
2. **Sending the user to the wrong הר הביטוח.** The only official domain is `harb.cma.gov.il`. Lookalike domains exist (`harhabituach.org`, `harhabituach.co.il`, `har-bituach.org.il`); none is the government service, and the `.org.il` suffix is not a mark of a public body. The register is a last-month snapshot and its duplicate alert is not dispositive, so a missing alert is no evidence either way.
3. **Assuming הר הביטוח is complete.** No שב"ן data, no סיעוד, no travel policies, no service subscriptions, no card benefits, and policies only for the בעל הפוליסה. Group cover is excluded only where the employer funds the entire premium AND the policy is written למבוטח לא מסוים, so the blanket claim that employer policies are absent is wrong.
4. **Cancelling before the replacement is active, or cutting the underwritten layer first.** שב"ן must re-accept the user; a private policy will not, and a legacy private סיעוד policy cannot be re-bought at all. If unsure which layer is reversible, stop and ask.
5. **Treating every fixed-sum line as sacred.** The mirror of Gotcha 1, costing money in the other direction. "It stacks, leave it alone" is the right answer to an agent trying to cancel a ריסק and the wrong answer as an audit. Two מחלות קשות policies with near-identical condition lists are a price comparison, not untouchable assets, and שאירים cover for a member with no שאירים buys a benefit that can never be paid. Run the argument both ways before writing LEGITIMATE STACKING.
6. **Assigning a tier to a policy instead of a benefit.** A line with two benefit heads gets two rows. The group סיעוד policy pays פיצוי at home and שיפוי in an institution, so one verdict on it is wrong in one of the two worlds the user might live in.
7. **Advising a household from one person's file.** Files are per-policyholder. A "duplication" that disappears once the spouse's file is pulled is a very common false positive, and so is one that only appears when both are on the table.

## Troubleshooting

**הר הביטוח shows nothing.** Data is a snapshot of the previous month, so a very recent policy may not appear. Fall back to the insurer's personal area and twelve months of bank and card statements.

**Cannot tell whether a benefit is שיפוי or פיצוי.** A fixed monthly or lump sum regardless of expense is פיצוי; reimbursement against an invoice, or payment direct to a provider, is שיפוי. If ambiguous, hand it to the insurer and mark the line UNRESOLVED rather than guess.

**An agent said the private אכ"ע is redundant.** Ask which disability test each instrument uses. The fund's is עיסוק סביר. If the private policy is עיסוק ספציפי they are not the same product and the conclusion does not follow. Put it in writing to the insurer.

**The user wants past premiums refunded.** No retroactive refund duty for cover the user chose themselves. The ס' 59(ב) reduction is prospective. Set the expectation before they make a demand they will lose.

**Employer cover is about to end.** Raise the conversion right to an individual policy without fresh underwriting, flag that the individual premium is typically far above the subsidised group rate, and have them ask the insurer for the exact window rather than relying on a number from this skill.

**The user asks whether to cancel a private ביטוח סיעודי.** Establish first whether it is the kupa group policy or a legacy individual one. An individual policy cannot be repurchased at all, since the product is no longer sold, so it never goes at the top of a cut list. Also split the row before judging it: the group benefit is פיצוי at home and שיפוי in an institution, so it has two tiers, not one.

**The insurer refuses, or the two sides have corresponded for months.** The supervisor investigates conduct complaints through the authority's portal, but not on a matter already before a court or arbitrator. Separately, warn about the clock: three years, five for חיים, מחלות ואשפוז and סיעוד, and lodging the claim does not stop it running. Close to the deadline, the next step is legal advice on timing, not another letter.

**Two insurers each say the other should pay.** For property and liability cover they are liable "יחד ולחוד לגבי סכום הביטוח החופף" and settle the apportionment between themselves. The user claims from either one and should say so.
