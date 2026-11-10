---
name: israeli-insurance-duplication-checker
description: "Not insurance or pension advice and not insurance or pension marketing. Audits the insurance an Israeli household already pays for, across health, long-term care, dental, disability, life, personal accident, motor, home, mortgage, travel and service riders, and separates real duplication from cover that legitimately stacks. Use when a user asks whether they are paying twice for insurance, wants to cut insurance costs, mentions כפל ביטוחי, holds a שב\"ן plan alongside a private health policy, has surgery cover through an employer or professional group, pays for a private ביטוח סיעודי next to the kupa group policy, wonders whether a private אכ\"ע policy is redundant next to the pension fund, or asks which policy to cancel first. Do NOT use for comparing or buying new policies (israeli-insurance-comparator), for co-pays and costs inside the public health system (israeli-hmo-navigator), or for the pension savings product itself (israeli-pension-advisor)."
license: MIT
---

# Israeli Insurance Duplication Checker

## Legal notice

This skill is a free information tool operated by an AI model. It is not insurance advice (ייעוץ ביטוחי), insurance marketing (שיווק ביטוחי), pension advice (ייעוץ פנסיוני) or pension marketing (שיווק פנסיוני), and no licensed agent, advisor or marketer is involved. It maps cover the user already holds, explains the statutory rules that decide whether two policies pay twice, and helps the user spot overlaps; whether to keep, cut or cancel anything is the user's own decision. It does not recommend buying a product, and what it says about cover inside a pension fund or ביטוח מנהלים is not a personal recommendation about any pension product. An AI model may err, omit data or reach a wrong conclusion. It "אינו מהווה תחליף לייעוץ המתחשב בנתונים ובצרכים המיוחדים של כל אדם", and relying on it is the user's sole responsibility. Nothing here is legal advice. Cancelling underwritten cover is irreversible in practice: confirm with the insurer, the fund or a licensed agent or advisor, and never cancel before replacement cover is active.

## Problem

Israelis routinely pay for the same cover in three or four places: a שב"ן plan plus a private health policy, an employer group policy over both, a service subscription that is also a home-policy rider and a card benefit. About 37% of the statutorily insured public, roughly 3.4 million people, hold commercial health cover alongside שב"ן, and the State Comptroller puts the overpayment at a floor of hundreds of millions of shekels a year. The main הר הביטוח register lists no שב"ן plan; since 2023 its health area shows the kupa's cover beside the policies and flags overlaps, an inventory aid, never the verdict. And some of what looks like duplication is not waste: cancelling it destroys cover the user can never buy back.

## The three-tier test (apply this before anything else)

Israeli law sorts insurance by PAYMENT MECHANISM, not subject matter, and getting it wrong is the biggest failure mode. Do not reason from "these two policies both mention surgery"; reason from how each pays.

**Tier the BENEFIT, not the policy.** A tier belongs to a CLAIM, not to an inventory line, and one policy can sit in two tiers. The kupot group סיעוד policy is the clearest case, paying "פיצוי כספי של 5,000 ש\"ח לחודש למשך 60 חודשים אם הוא שוהה בביתו, ושיפוי כספי בסך 10,000 ש\"ח לחודש למשך 60 חודשים אם שוהה במוסד סיעודי". Fixed sum at home, reimbursement in an institution, one contract. A private health policy that carries a fixed-sum מחלות קשות rider alongside reimbursement ניתוחים cover has the same shape.

A line with more than one benefit head splits into one row per benefit, each tiered separately; where the tier depends on a future state (home versus institution) say so rather than picking one, since a single verdict would be wrong in one of the two worlds.

| Tier | Examples | Governing rule | Does it duplicate? |
|---|---|---|---|
| Property and liability | רכב מקיף, צד ג', ביטוח דירה ותכולה | ס' 59 לחוק חוזה הביטוח, applied directly | Yes, and this is real waste |
| Reimbursement (שיפוי) | ניתוחים, תרופות, loss-based אכ"ע | ס' 56(א) via ס' 54(ב) | Yes, but recovery is capped at the actual loss |
| Fixed sum (פיצוי) | ביטוח חיים, מחלות קשות, fixed-sum נכות | פרק ב' via ס' 54(א) | No. It genuinely stacks, and this is NOT waste |

The statutory mechanics, to be stated when challenged, are in `references/line-by-line-detail.md`: ס' 59 is asset-bound and is the ביטוח כפל provision (not ס' 56), extended to liability by ס' 67 and made non-derogable by ס' 64; ס' 54(ב) does NOT import ס' 59 into loss-based health cover, so what caps it is ס' 56(א); and ס' 54(א) routes fixed-sum cover to פרק ב', which has no כפל provision and no indemnity ceiling.

## The safe-cut rule (the organising principle of every verdict)

Cancel only the layer the user can BUY BACK.

A kupat cholim must accept anyone into its שב"ן regardless of health, "ללא קשר למצבו הבריאותי או הכלכלי... למעט תקופות אכשרה סבירות" (ס' 10(ג)(1) לחוק ביטוח בריאות ממלכתי). It can make the user wait; it cannot refuse. A private policy is gated by חיתום: once its 60-day regret window (Step H) closes, a user whose health changed cannot buy it back.

Sequence is always: map, verify with the insurer or a licensed agent, cancel last. Where two layers overlap and one must go, the reversible layer goes first absent a specific reason otherwise.

## Audit workflow

### Step A. Build the inventory

**Run this per ADULT, not once.** Files are per-policyholder, and the commonest two-earner findings are invisible from one file: children enrolled on BOTH parents' employer health or dental plans, and a "duplication" that is really the spouse's policy seen twice. Every map row gets a covered-person column.

Have the user pull:

1. הר הביטוח, the personal insurance file, from the official domain `harb.cma.gov.il`, through the government identification system. It shows life, health, disability, motor and home policies and the insurer-issued כתבי שירות: "כל פוליסות הביטוח וכתבי השירות... כולל הפרמיה המשולמת". It is per-policyholder, so a spouse's policies will not appear.
   **It also opens "תיק ביטוחים על שם קטין" (where the children's riders from item 7 sit), "תיק ביטוחים על שם קרוב שנפטר" (the ריסק and mortgage-life lines), "תיק ביטוחים על שם אדם שתחת אפוטרופסות", and an authorised-agent view.** Ask which applies before calling a household line uninsured; a spouse still pulls their own.
   **Then open אזור ביטוחי הבריאות (`hit.cma.gov.il`, same login).** The regulator's health area lists the user's health covers with the monthly price and says when it finds "כפל ביטוח". Its FAQ defines the payment types it works with, "החזר (שיפוי)", "הסדר" and "מענק (פיצוי)", and separates "חפיפה בכיסוי ביטוחי" (שב"ן plus an insurer) from "כפל ביטוח" (two or more policies). Kupa data refreshes daily, insurer data monthly; it currently shows the logged-in adult only, no children or spouse; a privacy opt-out signed at purchase may hide that policy. Seed the map from it; tiers and exclusions still come from the policy wording.
2. המסלקה הפנסיונית, for what sits INSIDE the pension products: which bodies hold accounts, and the אכ"ע and שאירים cover attached to each. הר הביטוח does not open the pension savings products, so Step D cannot be answered without this. The official operator is `swiftness.co.il`, "האתר הרשמי של המסלקה הפנסיונית". An account is free and each request carries a small statutory fee; do not quote it (the operator's own FAQ gives two figures for the same request), say a few shekels and read the tariff at the point of request. The operator warns of "נסיונות להתחזות לגורמים מטעם המסלקה הפנסיונית": treat other "free report" sites like the fake הר הביטוח domains.
3. The kupa's personal area, for the שב"ן plan and tier. The group ביטוח סיעודי is different: the insurer reports it to הר הביטוח layer by layer (reported since 1.1.2018, by layer since 1.6.2021), so check the file first.
4. Payslip and the employer's benefits page, for group health, group אכ"ע, group dental, and any employer-bundled service plan.
5. Benefit pages of every card held.
6. Bank and card statements, scanned for small recurring charges: towing, home trades, windscreen, gadget cover, roadside subscriptions. The cheapest wins live here; no register lists the standalone ones.
7. With children: the school תשלומי הורים account (compulsory ביטוח תאונות אישיות לתלמידים) and any private child accident or dental rider on top.
8. With a mortgage: the loan file, for the ביטוח חיים and ביטוח מבנה tied to it, plus any separate ביטוח דירה.

### Step B. Sort every line into one of the three tiers

Use the table above, labelling each benefit שיפוי, פיצוי or נכס/אחריות. Do not proceed until every benefit has one: the same words ("ניתוחים", "נכות") get different verdicts by tier.

### Step C. Health

Most secondary sources get the reform wrong; it has two dates. Since **1.10.2023** new individual policies are modular: a "פוליסת בריאות בסיסית" first, Israeli surgery sold separately as שקל ראשון or משלים שב"ן, the two layers may sit with different insurers, and the marketer must show the candidate's existing שב"ן surgery cover "כפי שמופיע באתר הר הביטוח". The automatic transfer to משלים שב"ן took effect in **June 2024**; February 2016 is only the purchase-date cutoff, so never call it a 2016 event. It caught פוליסות פרט bought from February 2016 to 30.9.2023 by שב"ן members; the reversal window ran to 31 May 2025, some insurers extended theirs, and press reporting says about 42% of those moved went back, so check rather than assume. **The GROUP market was affected far less and later**, because group policies update only every few years, so much group surgery cover is still מהשקל הראשון. Do NOT say group policies were never converted; have the user check. Pre-2016 individual buyers were not caught either. Those three populations are the core audience, so ask whether the policy is individual or group and when it was bought. Detail in `references/line-by-line-detail.md`.

Overlap by layer, once the track is known:

- ניתוחים בישראל: heavy overlap between a מהשקל הראשון policy and שב"ן. The regulator's position is that such cover is "חופפות במידה רבה לשירותים שניתנים בשב"ן", while a משלים שב"ן policy "לא כוללות כפל ביטוחי".
- אמבולטורי (consultations, imaging, second opinions): heavy overlap, rarely discussed. Check it.
- ניתוחים בחו"ל, השתלות, תרופות מחוץ לסל: the catastrophic tail, genuinely additional to שב"ן. Not waste.
- מחלות קשות: fixed sum, so it cannot duplicate anything, and no one should cancel it because an agent called it overlap. But "leave it alone" is not an audit: households commonly hold it in four places (standalone, a private-policy rider, an employer group benefit, a ביטוח מנהלים rider) with materially different condition lists. The output is "stacks, so compare lists and sums, and cut on price only where two are near-identical": PARTIAL, the one place it applies to fixed-sum cover.
- שיניים: check it, because much of it may already be free. The basket covers children "שטרם מלאו להם 18 שנים" and "טיפולי שיניים למבוטחים שמלאו להם 72 שנים", with no co-payment on the periodic check-up, bitewing pair and scaling, so a policy for a nine-year-old or someone over 72 buys much of what the basket provides. Dental is normally שיפוי, so the overlap is CAPPED. The non-basket exception is אורתודנטיה, expressly carved out of the children's trauma item: PARTIAL, not REAL WASTE.

מהשקל הראשון and משלים שב"ן are market names, not statutory terms.

Group cover is temporary by design: at most five years, with a right on leaving to convert to an individual policy without fresh underwriting or אכשרה, on the regulator's conditions. State the right, not a deadline, and warn that the converted premium is typically far above the group rate.

### Step D. אובדן כושר עבודה (get this right, it is counterintuitive)

"You already have אכ"ע through your pension, so cancel the private policy" is WRONG, the most damaging common advice in this domain.

The fund applies a BROAD-occupation test: the takanon defines a נכה as a member at least 25% of whose working capacity is impaired and who therefore cannot work "בעבודתו או בכל עבודה אחרת המתאימה לו לפי השכלתו, הכשרתו או ניסיונו" for over 90 consecutive days. ("עיסוק סביר" is shorthand, not the takanon's term: quote the definition, not the label.) A surgeon who can no longer operate but could work in administration may collect NOTHING. Filling that gap is what a private policy is for: the gap, not the cap, is why it is not redundant.

The two 75% rules are different instruments; say which one you mean: inside a pension or provident fund the disability pension is capped at 75% of the insured salary in the fund; in the uniform private policy it is 75% of the average salary insured under that plan.

Cross-insurer offset does NOT trigger at 75%. It triggers only above "100% ממוצע השכר של המבוטח מכל מקור הכנסה", and even then the private policy pays a floor that "לא יפחת, בכל מקרה, משיעור של 30% מסכום הפיצוי החודשי". The band between the per-policy cap and 100% of income is legitimate cover, not waste. A pension fund counts as a "מבטח אחר" here. The excess-premium refund is capped at seven years AND conditional on a claim: "לא קרה מקרה הביטוח, המבוטח לא יהיה זכאי להחזר פרמיה". At the point of sale the insurer must check the מסלקה and cancel a duplicate (חוזר ביטוח 2018-1-8), and an אכ"ע premium may never be funded out of מרכיב הפיצויים. Arithmetic: `references/worked-examples.md`; wording: `references/line-by-line-detail.md`.

**The one pension line that CAN be pure waste: שאירים cover with no שאירים.** A member with no survivors other than a parent may waive the death-risk cover, renewable "כל עוד אין לו שאירים"; during the waiver "לא ייגבו מהעמית דמי ביטוח בשל כיסוי ביטוחי למקרה מוות". A יתום here is a child "שטרם מלאו לו 21 שנים", or a child with a disability.

**But it is not a free saving, so raise it carefully rather than enthusiastically.** The fund may run חיתום רפואי when the member later asks to re-include the cover, and may then reject the request or exclude any pre-existing condition. The only escape is having kept paying the default ביטוח המשך continuation cover throughout, which the member may also opt out of. State the underwriting risk in the same breath as the saving, and send the user to confirm the continuation-cover position with the fund. Detail in `references/line-by-line-detail.md`.

Separately, a member holding BOTH a קרן פנסיה and a ביטוח מנהלים may be paying for the same אכ"ע twice. That is a genuine overlap and belongs in the map.

### Step D2. סיעוד (the biggest line in the country, and the hardest to undo)

Almost every household has this; ask even if unprompted.

Three things users conflate: **גמלת סיעוד from ביטוח לאומי** (statutory, under חוק הביטוח הלאומי פרק י', income-tested at household level, not a policy); **the kupa group policy** (the two-tier benefit above, under the 2015 group-LTC regulations and חוזר ביטוח 2016-1-3, bought "נוסף על גמלת הסיעוד של בט\"ל"); and **a legacy private policy**, held by about a million Israelis, "אשר נרכשו בעבר ואינם נמכרים יותר בשוק".

**An individual סיעוד policy cannot be repurchased at any price, because the product is no longer sold at all.** Never put a legacy private סיעוד policy at the top of a cut list. **The kupot group policy is not a free layer either.** Joining is "בכפוף לבדיקת מצבך הרפואי", and the benefit is fixed by age at FIRST joining: at home 5,000 / 4,100 / 3,200 and in an institution 10,000 / 6,500 / 4,500 a month, for a first join up to 49 / 50-59 / 60+. A member who leaves may be refused, or return on a lower tier. Since December 2023 the insurer carries no insurance risk: claims come only from the members' fund, which can run down. Where group and private overlap, neither layer is freely reversible: keep both unless the insurer confirms re-entry terms in writing.

The overlap is also narrower than it looks: the 1.1.2025 tightening to four of six ADL applies to the kupot group policies only, so a legacy private policy usually keeps a broader trigger. The regulator itself says several סיעוד policies may be held in parallel to raise the benefit or its duration: two private policies are LEGITIMATE STACKING, and kupa plus insurer means two separate claims. Before any private סיעוד cancellation ask whether the policy carries ערכי סילוק (a reduced paid-up benefit); the health area's "תמונת מצב" page states whether it does. Clalit's policy moves from הראל to איילון on 1.1.2027 (events up to 31.12.2026 are claimed from הראל), per Clalit's announcement automatically and on unchanged terms; a new insurer name is not a new or duplicate policy, and on a kupa switch the group policy follows the member only if the data transfer is approved at registration (else the insurer's certificate within 180 days).

Two things NOT to say: that the group policy is being wound up on a stated date (the January 2025 draft dates were withdrawn; the regulator's October 2026 split-by-age model is a proposal needing legislation), and that גמלת סיעוד does or does not offset a policy payout, which the sources do not settle. Treat the arrangement as operating and send the user to confirm its status and their tier with their kupa. Detail in `references/line-by-line-detail.md`.

### Step E. Motor, home, mortgage and the service riders

- The real motor duplication is a standalone צד ג' on top of a מקיף. מקיף and צד ג' are two chapters of one prescribed policy: textbook ס' 59.
- Car versus home צד ג' is NOT a duplication: the home policy excludes vehicle liability by construction.
- תכולה riders are PARTIAL, not waste: a כל הסיכונים rider lifts exactly the limits the standard policy imposes. Ask what it covers before calling it redundant.
- כתבי שירות are the highest-yield line here. Towing, home trades and windscreen typically sit in three or four places; the user gets the tow once. **Start from הר הביטוח: the file lists the insurer-issued כתבי שירות with the premium paid for each.** Outside it is the non-insurance layer: standalone service-company subscriptions, card benefits, employer and utility bundles, all from the statements in Step A. Detail in `references/line-by-line-detail.md`.
- **Mortgage cover: Directive 451 gives the borrower three levers.** The bank may require property and life cover up to the loan amount only as irrevocable beneficiary; must tell the borrower prominently he may buy both directly rather than through its agency; the customer may cancel at any time without fee against an alternative policy naming the bank; and structure cover may not be required above the unpaid revalued balance. No duty to insure loans up to 30,000.
- **Mortgage ביטוח מבנה against a separate ביטוח דירה is a ס' 59 question.** Confirm both really cover the structure before calling it REAL WASTE, and never cancel before the bank consents to release the charge, or the loan may be treated as in breach.
- **ביטוח תאונות אישיות לתלמידים is already paid for**, compulsory through the local education authority, covering the child anywhere in Israel at any hour, not only school hours. A private child rider is fixed-sum and stacks, but tell the parent what the compulsory policy already buys.
- No retroactive refund for a duplication the user created: the ס' 59(ב) reduction runs forward only, "מיום הדרישה". Retroactive refunds are associated with duplicates the INSURER created, and this skill has no sourced authority for a wider rule, so do not promise money back on past premiums.

### Step F. Travel

Most Israeli card benefits are a discount that must be activated before EVERY trip, not embedded cover, and paying for the trip with the card is generally not a condition. Never invent card specifics; send the user to the card's benefit page. A standalone policy is still needed for pre-existing conditions (a regulatory six-month exclusion), pregnancy, extreme sports, long trips, non-medical ביטול נסיעה, high-value gear and age 80+. Detail in `references/line-by-line-detail.md`.

### Step G. The ותק and אכשרה trap, before anyone cancels anything

- Switching kupa preserves שב"ן ותק only on joining the new kupa's שב"ן within 90 days, and only between parallel tiers. Cancelling and re-joining the SAME kupa restarts the waiting periods.
- Tier names, which users and marketing material both garble: מכבי sells two tiers to a new joiner, זהב and שלי; מכבי כסף is a closed legacy tier, "נסגרה למצטרפים חדשים במאי 2012", with a published upgrade path out and no route back in, so treat cancelling it as irreversible and confirm that with מכבי. כללית has מושלם זהב and מושלם פלטינום; מאוחדת has עדיף and שיא (no "זהב" there); לאומית has כסף and זהב. Marketing names change: confirm the current list on the kupa's site.
- **Check residency before applying the safe-cut rule at all.** The rule assumes the kupa must re-accept the user. That fails for a new oleh, a תושב חוזר, someone on relocation, a dual citizen with foreign cover, or a non-resident spouse, for whom the private policy may be the ONLY cover rather than the redundant layer. This skill does not carry their waiting-period rules: establish status, then have the user confirm entitlement before anything is cancelled.

### Step H. Cancellation mechanics

- The 14-day distance-selling withdrawal right does NOT apply to insurance: חוק הגנת הצרכן excludes insurers.
- **Cancellation by the INSURED takes effect three days after the notice reaches the insurer.** The fifteen days often quoted is the insurer's deadline to execute a request; stopping payment without a request leaves the premium owed. A private health policy cancelled and regretted within 60 days may be re-joined on the same terms (regulator's FAQ): the one reversible cut here; date the notice.
- Every insurer must run an area titled "ביטול פוליסה קיימת" on the MAIN PAGE OF ITS WEBSITE and in the online personal account, plus other channels, an automatic written acknowledgement and at most three business days to report deficiencies (חוזר ביטוח 2017-1-3). Keep the acknowledgement: it proves delivery.
- שב"ן notice is set by each kupa's תקנון, not statute. Life insurance may be cancelled at any time in writing.
- An individual health policy bought from 1.2.2016 renews every two years on 60 to 120 days' notice; renewed without explicit consent, it may be cancelled within 60 days with that period's premium refunded, absent a claim (חוזר ביטוח 2015-1-19). The renewal notice is the moment to audit.
- An insurer may not enrol a user in a duplicate פיצוי policy unless they confirm in writing after being told it duplicates an existing one and that both will be charged (חוזר צירוף 2016-1-7, as amended through 2023-1-5). A duplicate sold without it is a ready-made ground for a complaint.

### Step I. When the insurer says no, and the clock the user cannot see

A duplication audit routinely turns up a benefit the user never claimed, which starts a clock nothing makes visible to them.

- **Limitation is three years from the insured event**, five for ביטוח חיים, ביטוח מפני מחלות ואשפוז and ביטוח סיעודי, on contracts made or renewed from 25.11.2020.
- **Lodging the claim does NOT stop the clock.** The insurer must say so itself: "אינו נעצר בעקבות מסירת התביעה למבטח".
- **Escalation** is to the supervisor, who investigates conduct complaints but not a matter already before a court or arbitrator. Within a year of the deadline the next step is legal advice on timing, not another letter. Wording and route: `references/claims-and-escalation.md`.

## Deliverables

Produce all four, in order:

1. **A layer-by-layer duplication map.** One row per BENEFIT, not per policy: split a policy with two benefit heads, per the three-tier test.

   Columns (schema in the detail reference): covered person, cover/benefit, tier, monthly premium, overlaps with, reversible?, verdict.

   Verdicts: **REAL WASTE** (pays once, charged twice), **CAPPED** (recovery limited to actual loss), **PARTIAL** (a rider lifts a limit, or two fixed-sum policies have near-identical condition lists, so cut on price), **LEGITIMATE STACKING** (pays cumulatively), **UNRESOLVED** (tier or terms unestablished, to the insurer first), **NOT A DUPLICATION**. Sort REAL WASTE by REVERSIBILITY first, premium only as a tiebreak: never let premium size move an unrepurchasable line up the cut list.
2. **Questions to put to the agent or insurer**, phrased to be read out. Per flagged overlap: "האם הפוליסה הזו משלמת שיפוי או פיצוי?", "אם יש לי גם שב\"ן, על מה בדיוק הפוליסה הזו מוסיפה?", "מה תקופות האכשרה אם אחזור לרכוש את הכיסוי הזה בעוד שנה?", "מה הפרמיה החודשית של הכיסוי הזה בנפרד?".
3. **A short "gaps found" list.** An audit that only removes lines will leave a household with no אכ"ע and call it a success. Note any layer absent rather than duplicated: no disability cover on a sole earner, no סיעוד, a mortgage with no life cover. Naming an absence is not marketing: state the gap, name no product, route to a licensed agent (`israeli-insurance-comparator` compares and buys).
4. **A Hebrew cancellation letter**, only for lines the user decided to cut after verifying. Use `references/cancellation-letter-he.md`.

Never emit deliverable 4 for a line not confirmed with the insurer or agent, or whose replacement cover is not yet active.

## Examples

Three worked audits in `references/worked-examples.md`: the three-layer health question, the אכ"ע case where nothing is cancelled, and a two-adult household with a genuine REAL WASTE row. Read them before a first map.

## Bundled Resources

| File | When to use it |
|---|---|
| `references/intake-questionnaire-he.md` | Hebrew intake form, one per adult, with the individual-or-group fallback. Send before Step A. |
| `references/domain-checklist.md` | Coverage contract and do-not-assert list. Read before adding any figure. |
| `references/worked-examples.md` | Three filled-in audits. Read before a first map. |
| `scripts/validate_map.py` | Deterministic QA of a finished map (CSV): tiers, verdicts, cut order, safe-cut traps. Run before deliverable 1. |
| `references/line-by-line-detail.md` | Detail behind Steps A to H and the map schema. |
| `references/claims-and-escalation.md` | ס' 31 wording and the complaints route (Step I). |
| `references/reference-links.md` | Full source table. |
| `references/cancellation-letter-he.md` | Deliverable 4 only, never for an unverified line. |

## Recommended MCP Servers

| MCP | Why it helps here |
|---|---|
| `kolzchut` | Israel's rights database: what the public basket already covers and what a קופת חולים owes a member. Install page: https://agentskills.co.il/he/mcp/kolzchut |

No MCP exposes a personal insurance file; הר הביטוח sits behind government identification and the user pulls it.

## Reference Links

Load-bearing: [חוק חוזה הביטוח](https://www.nevo.co.il/law_html/law00/71902.htm) for the tier split and ס' 31; [מבקר המדינה, הביטוח הסיעודי](https://library.mevaker.gov.il/sites/DigitalLibrary/Documents/2026/Population-Aging/2026-Population-Aging-102.pdf) for סיעוד; [הוראה 451](https://www.boi.org.il/media/utld2tgp/451.pdf) for mortgage cover. Full table: `references/reference-links.md`; verbatim quotes: `evidence.json`.

## Gotchas

These are agent failure modes, not user mistakes.

1. **Treating every overlap as waste.** The most expensive error runs toward cancelling. Fixed-sum cover stacks by law, so a standalone ריסק plus a mortgage life policy plus שאירים in the pension all pay on the same death. Run the three-tier test before writing a single verdict.
2. **Sending the user to the wrong הר הביטוח.** The only official domains are `harb.cma.gov.il` and `hit.cma.gov.il`. Lookalikes exist (`harhabituach.org`, `harhabituach.co.il`, `har-bituach.org.il`); none is governmental, and `.org.il` is not a mark of a public body. The register is a last-month snapshot and its duplicate alert is not dispositive: a missing alert is no evidence either way.
3. **Assuming הר הביטוח is complete, or emptier than it is.** Missing from the main register: the שב"ן plan as a product line (its cover appears only in the health area, hit.cma.gov.il), trip policies of three months or less, standalone service-company subscriptions, card benefits, and policies held by anyone but the בעל הפוליסה. Present, and routinely written off by mistake: the kupot group סיעוד and the insurer-issued כתבי שירות with the premium paid. Excluded, among others: fully employer-funded health cover written למבוטח לא מסוים or inside a business package, and certain approved or pre-2006 unrenewed group life policies. Before asserting any further absence, read the tool's own copy or the reporting circular's scope section.
4. **Cancelling before the replacement is active, or cutting the underwritten layer first.** שב"ן must re-accept the user; a private policy will not after its regret window, and a legacy private סיעוד policy cannot be re-bought at all. If unsure which layer is reversible, stop and ask.
5. **Treating every fixed-sum line as sacred.** The mirror of Gotcha 1. "It stacks, leave it alone" answers an agent trying to cancel a ריסק; it is not an audit. Two מחלות קשות policies with near-identical condition lists are a price comparison, not untouchable assets, and שאירים cover for a member with no שאירים buys a benefit that can never be paid. Run the argument both ways before writing LEGITIMATE STACKING.
6. **Assigning a tier to a policy instead of a benefit.** A line with two benefit heads gets two rows; the group סיעוד policy is the standing example.
7. **Advising a household from one person's file.** Files are per-policyholder. A "duplication" that disappears once the spouse's file is pulled is a common false positive, and so is one that appears only when both are on the table.

## Troubleshooting

**הר הביטוח shows nothing.** Data is a previous-month snapshot, so a recent policy may not appear. Fall back to the insurer's personal area and twelve months of bank and card statements.

**The health area reports "כפל ביטוח".** A prompt, not a verdict. Its own FAQ says what this skill says: שיפוי pays "לכל היותר 100% מגובה ההוצאה הרפואית", פיצוי pays from each policy, שב"ן beside an insurer is "חפיפה בכיסוי ביטוחי", and before cancelling one "חשוב לקרוא את תנאי הביטוחים האחרים". List every source behind the flag and run the three-tier test.

**Cannot tell whether a benefit is שיפוי or פיצוי.** A fixed monthly or lump sum regardless of expense is פיצוי; reimbursement against an invoice, or payment direct to a listed provider (the health area's "הסדר"), is שיפוי. If ambiguous, hand it to the insurer and mark the line UNRESOLVED.

**An agent said the private אכ"ע is redundant.** Ask which disability test each instrument uses. The fund's is the broad one above; a עיסוק ספציפי policy is not the same product. Put it in writing to the insurer.

**The user asks whether to cancel a private ביטוח סיעודי.** Establish first whether it is the kupa group policy or a legacy individual one; neither is freely reversible (Step D2), and the group row splits: פיצוי at home, שיפוי in an institution.

**The insurer refuses, or the two sides have corresponded for months.** Step I: the supervisor's portal for conduct, and the warning that lodging the claim does not stop the limitation clock.

**Two insurers each say the other should pay.** For property and liability cover they are liable "יחד ולחוד לגבי סכום הביטוח החופף" and settle apportionment between themselves. The user claims from either and should say so.
