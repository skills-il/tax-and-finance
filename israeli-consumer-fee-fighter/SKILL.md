---
name: israeli-consumer-fee-fighter
description: "Use when an Israeli consumer wants to cut recurring bank and credit-card charges: cancel a credit card cleanly (bitul kartis ashrai), switch to a cheaper fixed-price bank fee track (maslul amlot: basic maslul basi or expanded maslul murchav), switch banks in one click (niud / maavar beklik), stop a recurring debit (bitul harshaa lechiyuv / horaat keva), or negotiate lower fees and commissions (amlot including overdraft, FX, and securities fees). Produces a ready-to-send Hebrew cancellation letter, a rights-grounded negotiation script, and a short rights summary, grounded in Bank of Israel fee rules and Israeli consumer-banking law. Do NOT use for maximizing cashback or deals (use israeli-smart-saver), coupon hunting (use israeli-coupon-code-finder), analyzing bank transactions (use israeli-bank-connector), or household budgeting (use israeli-budget-planner)."
license: MIT
---

# Israeli Consumer Fee Fighter

## Problem

Israeli consumers quietly overpay their bank and credit-card companies every month. Many are billed per action (peula) instead of on a fixed-price fee track, pay for a credit card they barely use, or keep getting charged by a service they thought they cancelled. The law gives them clear levers: two standardized fee tracks, the right to switch, a free one-click bank-switching reform that moves the whole account to a cheaper bank, the right to cancel a card or a recurring debit at any time, and discounts for eligible populations. Most people do not know these levers exist or how to invoke them. This skill turns those rights into three concrete deliverables: a cancellation letter, a negotiation script, and a short rights summary.

This skill is grounded in the Bank of Israel fee rules and Israeli consumer-banking law. Fee amounts and transaction counts are cited from the sources in `references/`; because fees change, always confirm any number against the current tariff (taarifon amlot) and the Bank of Israel fee-tracks calculator before quoting it to the user.

## Instructions

Work in the tracks below depending on what the user needs. Ask which one applies, or handle several.

### A. Pick the cheaper bank fee track

Israeli banks (except the Postal Bank) must offer two fixed-price tracks under Banking Rules (Customer Service)(Fees), 5768-2008, section 4a (in force since 1.4.14). A customer who picks no track is charged per action, which is often more expensive than a track for anyone with steady monthly activity. Do not quote the user a specific multiple: compare their own per-action total against the track price using the calculator in step 4.

| Method | Direct-channel actions/month | Teller actions/month | Monthly price |
|---|---|---|---|
| No track (per action) | pay per action | pay per action | varies, compute from the user's own statement |
| Basic track (maslul basi) | up to 10 | up to 1 | supervised, max 10 NIS |
| Expanded track (maslul murchav) | up to 50 | up to 10 | supervised since Sept 2022, bank-specific price |
| Expanded-plus (some banks) | expanded + extras | expanded + extras | supervised since Sept 2022, bank-specific |

Both expanded tracks came under price supervision in the Banking Order (Customer Service)(Supervision of teller-action, direct-channel-action, expanded track and expanded-plus track services), 5782-2022, published 1.9.2022: a bank may not raise these tariffs without Bank of Israel approval. Read the current price off the bank's published tariff (taarifon) rather than assuming a range.

**First, find out what they are actually paying.** Every step below needs two integers the user almost never has to hand, so do not start by asking them to estimate.

- The account-management charge appears on the statement as a single `עמלות עו"ש` line, billed in arrears for the previous period. Most banks bill it monthly at the start of the month; some bill quarterly, so check the period the line covers before dividing by anything.
- Map the line items to the calculator's two inputs: internet, app, ATM and standing-order actions are direct-channel; anything done by a clerk, including via a staffed phone line, is a teller action (peulat pakid).
- Ask the bank in writing for a concentration of the fees actually charged to the account over the last 12 months. Banks produce this on request and it hands you the totals and the action split in one document, which is far faster than adding up statements.
- The tariff's annexes must be delivered to the customer, and Annex A is specifically the population-group benefits table (`נספח א׳ – הטבות לקבוצות אוכלוסיה`). That is where a bank sets out what it applies to the categories in step 2, so ask for it by name rather than accepting a verbal answer.

Decision steps:
1. Ask the user for their typical monthly action count, split into direct-channel (internet, app, ATM, standing orders) and teller (peulat pakid), using the statement mapping above rather than a guess.
2. Check for a cheaper path first. The senior and disability entitlement is set by the fee rules themselves, so it is identical at every bank and is **not** a percentage discount:
   - **What it is:** a customer who is an azrach vatik, a person with a disability, or who holds no cash-withdrawal card gets **4 teller actions a month charged at the direct-channel price** (Banking Rules (Customer Service)(Fees), 5768-2008, First Schedule, item 1(a)(2) note). There is no published percentage or shekel discount. Do not invent one.
   - **Senior = retirement age.** The fee rules give no age; they define azrach vatik by reference to the Senior Citizens Law, 5750-1989, which keys it to the Retirement Age Law, 5764-2004. That age differs by sex and birth date and has been re-staged more than once, so read it off that law rather than quoting a number.
   - **Disability = a customer who has PRESENTED the bank a Ministry of Defense or Bituach Leumi certificate of 40%+ disability.** Presenting it is what creates the entitlement, which starts on the 1st of the month after presentation and is **not retroactive**. Tell the user to hand it in now rather than assume the bank knows.
   - A business may separately qualify as a small business (esek katan) or osek murshe for the reduced tariff.

   The entitlement is **not** an alternative to joining a track, and it does not discount the fixed track price. It reprices teller actions wherever they are billed per action under item 1(a)(2), which means both when the customer is on no track at all and on a track's teller OVERAGE. So it changes the arithmetic of all three options at once rather than adding a fourth. Do not reason about it by hand: pass `--entitled` to the calculator in step 4, which applies it to every method. For a low-volume eligible customer it routinely flips the recommendation.
3. **Check the bank owed them an automatic track enrolment.** Under rule 4a(b1) (and 4a(b2) for a small business / osek murshe), if a senior, a person with a disability, or a small business was charged more every single month of a financial year than the basic track would have cost, the bank must compute the differences and **enroll them in the basic track by 1 March of the following year**, in writing, with the option to opt out. Banks do not always do this. Have the user ask what the comparison showed for the last completed year, and treat a missing enrolment as a complaint ground under section C. Note what the rule does and does not give: it obliges the bank to enroll the customer **going forward**, and does not on its own text award a refund of the prior year's excess. Ask for the refund anyway in the same letter, as a separate restitution request rather than as something the rule guarantees, so the complaint does not silently concede the past year.
4. Run `scripts/fee_track_calculator.py` with the user's action counts and their bank's real per-action and track prices to compare all three methods. It adds estimated overage so an over-limit track is not recommended blindly.
5. Confirm the result against the Bank of Israel fee-tracks calculator, which compares against every bank.
6. To switch: notify the bank via site, phone, or branch. The switch takes effect on the 1st of the month after the notice. Use the request template in `references/cancellation-letter-templates.md` (template 4).

### B. Cancel a credit card or stop a recurring charge

First separate the two mechanisms, because they behave in opposite ways:

- **Standing debit authorization (harshaa lechiyuv / horaat keva):** set up at the BANK, on the ACCOUNT. It pulls money straight from the bank account, so it is NOT tied to any card. Cancelling a card does not touch it, and replacing a card does not stop it. You cancel or stop it at the bank (see below).
- **Card-billed recurring charge:** a subscription billed to the card NUMBER (streaming, gym, insurance, cloud storage). These are tied to the card, so cancelling or replacing the card makes them FAIL. The fix is to update the payment method with each merchant BEFORE the old card dies, so nothing bounces.

Who to notify depends on who issued the card:

- **Bank-issued card:** the same bank holds the account (and its harshaot lechiyuv) and issued the card. Notify the bank for everything.
- **Externally-issued credit-card-company card (Cal / Max / Isracard):** the credit-card company holds the card and the list of card-billed recurring charges; the BANK still holds the harshaot lechiyuv on the account. Cancel the card and get the recurring-charge list from the card company; handle the account authorizations at the bank.

Steps:

- **Before cancelling a card:** settle any open installments (tashlumim) and any credit (kredit) revolving balance first. Cancellation can accelerate the remaining installments into a single immediate charge, or the issuer can block the cancellation until the balance is cleared.
- **Cancel a credit card:** send a written cancellation request to the issuer (template 1 in `references/cancellation-letter-templates.md`). Ask for written confirmation and a list of the recurring charges billed to the card, so you can move each one to another payment method before the card dies.
- **Stop a recurring debit:** under the Payment Services Law, 5779-2019, s.34(a), the payer may cancel a debit authorization at any time by notice to the bank or to the beneficiary. Use template 2. The bank must notify the beneficiary within two business days.
- **Cancel the debit is not the same as cancel the debt:** stopping the harshaa or the card charge only stops the payment instrument. The underlying contract survives, so the business can still invoice you or send the debt to collections. To end the obligation itself, also cancel the underlying transaction (template 3), not just the payment.
- **Cancel an ongoing subscription (iska mitmasheshet):** the business must stop charging within 3 business days of the notice (6 business days if sent by registered mail). Use template 3. If the business keeps charging after the cutoff, the consumer is entitled to compensation without proof of damage of up to 10,000 NIS plus a full refund. A general 14-day cancellation right also applies to recent sign-ups.

Always send by a channel that leaves a record (registered mail, email, or the company website) so the notice date is provable; the stop-charging clock runs from that date.

**Getting back money already taken.** Stopping future charges is only half the job, and users routinely assume a wrong debit is gone for good. The Payment Services Law gives four separate remedies, all of them against the BANK rather than the business, each with its own clock. Full text and the exact wording to quote are in `references/payment-services-remedies.md`.

**Check which mechanism took the money before picking a route, because these four cover only ONE of them.** Sections 34 to 38 are written about a harshaa lechiyuv, the authorization sitting on the bank account. They do **not** apply to a charge billed to a card number, which is the more common case for a gym, a streaming service, or an insurance policy. Sending the bank a s.35(a) demand about a card-billed subscription gets it refused, and the 3-business-day window is gone by the time the user finds out. For a card-billed charge the route is instead: dispute it with the card ISSUER (Cal / Max / Isracard, or the bank if it issued the card), and pursue the merchant under the ongoing-transaction rules above, where continuing to charge after a valid cancellation carries compensation without proof of damage of up to 10,000 NIS plus a full refund. Ask the user which one it is, and if they do not know, have them check whether the charge appears in the bank's list of active authorizations or only on the card statement.

| Situation | Remedy | Deadline on the user |
|---|---|---|
| One specific debit the user simply wants reversed | s.35(a): notify the bank, which refunds at the debit-date value **within 1 business day** | **3 business days from the debit.** Tight, so act immediately |
| Charge exceeded the authorization: expired authorization, more than the permitted amount, or on the wrong date | s.37: the bank refunds the difference **within 1 business day** of discovering it or being told | **None.** The bank must also refund it if it finds the overrun itself |
| Debit far larger than the user could reasonably expect given prior debits | s.38(a): refund **within 7 business days** of notice | Notify promptly |
| Authorization unused for 24 months | s.34(c): it is **no longer valid** and the bank must notify both sides | None |

s.38 has a trap worth flagging before relying on it: under s.38(c) the remedy **does not apply at all** if the bank offered the user the ability to set a debit ceiling and an expiry date when the authorization was approved. Most banks now offer exactly that, so s.38 is the weakest of the four. Tell users to set the ceiling (tikra) when creating any authorization, which both caps the exposure and turns a later overrun into a s.37 case, where there is no deadline.

**Closing the account is not free, but it is capped.** Total closure fees may not exceed 40 NIS, and that cap explicitly covers cancelling debit authorizations and standing orders, so a bank may not bill those separately on closure. The customer may end the account contract at any time under Payment Services Law s.6(a), but the bank may require the steps set out in the contract first, and the five-business-day clock only starts once those are done. That is the lever a stalling bank uses, so frame it as "complete their checklist, then the clock runs," not "they cannot refuse."

### C. Negotiate fees down

The Israeli approach is not US-style "call and threaten to leave." It is grounded in concrete rights:
1. State your position with data: "I run X direct actions and Y teller actions a month; the [basic/expanded] track or a discount is cheaper for me than what I pay now."
2. Cite the lever: the two fee tracks, your eligibility for a discount (senior / 40%+ disability / small business), and the Bank of Israel calculator showing a cheaper bank.
3. Ask for a specific outcome: switch to the named track, apply the discount you qualify for, or waive/reduce a specific commission.
4. If the bank will not move, the credible alternative is switching tracks or switching banks via the one-click switch reform (see section D), not an empty threat. Put the request in writing so there is a record.

Do not stop at the account-management fee. The biggest real overpayment is often outside the fee tracks: overdraft interest (when the balance drops below zero or past the credit line, riba al chariga), the interest and setup fees on a credit line, and foreign-currency and securities fees. These are not covered by any track, but they are negotiable, so raise them as separate targets and ask for a lower rate or a waiver on each.

If the bank refuses to switch your track or apply a discount you clearly qualify for, escalate. The route has two steps and users routinely skip the first, which gets the complaint bounced back:

1. **The bank's own ombudsman (natziv tlunot hatsibur) first.** The Bank of Israel requires this step to be exhausted before it will take the complaint. Submit in writing, keep the reference number, and expect a written answer within 45 days; in certain circumstances the ombudsman may extend to 60 days and must notify the complainant in writing. Handling of public complaints is governed by Proper Conduct of Banking Business Directive 308A.
2. **Then the Supervisor of Banks Public Inquiries unit**, via the online complaint form linked from <https://www.boi.org.il/information/public-enquiries-unit/ihaveaq/>. Filing requires identity verification. Attach the ombudsman's reply and set out the claim. The unit covers current-account management, checks, credit cards, deposits, foreign currency, fees, loans, mortgages, and fraud. It is free. Use the channel published on that page rather than emailing a general address.

Match the regulator to the counterparty. The Supervisor of Banks covers banks and credit-card companies only. A gym, streaming service, or other merchant that keeps charging after a cancellation is a Consumer Protection and Fair Trade Authority matter; sending it to the Bank of Israel loses months.

Produce the letter (from `references/cancellation-letter-templates.md`), the negotiation script (steps 1-4 above, filled with the user's numbers), and a short rights summary (the specific track limits, cancellation rights, and discount eligibility that apply to them).

### D. Switch banks in one click (niud / maavar beklik)

Since 22 September 2021 every Israeli can move their current account to a cheaper bank through a free, fully online switch. The customer only opens an account at the new bank and asks it to run the switch; the process completes within 7 business days from submission, and the customer may request an extension of up to 30 business days. It transfers the shekel and foreign-currency balances, the standing orders (horaot keva) and current-account authorizations, checks, and both bank and non-bank credit-card activity. After the move, an "akev acharai" ("follow me") service forwards charges and credits that still land in the old account to the new one for 3 years.

That 3-year window expires, and the first cohort's is expiring now: anyone who switched between 22.9.2021 and 21.9.2023 loses auto-forwarding from **21.9.2026**. If the user switched in that period, tell them to update their employer, Bituach Leumi, and every standing beneficiary with the new account details before that date, or incoming payments and outgoing charges start failing silently.

Tell the user plainly what does NOT come across, because this is where niud surprises people: loans and credit (including mortgages), deposits and savings plans, non-transferable securities, and safe-deposit boxes or products pledged to the old bank all stay behind and need a separate arrangement with the previous bank. Bank of Jerusalem customers cannot use the online switch at all.

This is the single biggest fee-cut lever for many people: instead of negotiating one commission at a time, they land at the bank the Bank of Israel calculator shows as cheapest for their profile. It also solves the standing-order problem in section B automatically. Because niud moves the horaot keva for you, a user who is switching banks does NOT need to re-set-up each authorization by hand; they only need to update card-billed charges with each merchant (those follow the card, not the account). When a user's real problem is a bank that is simply expensive across the board, route them to niud, not to a track switch.

### E. The 2027 fee reform (coming, not yet in force)

Bank of Israel Supervisor of Banks circular 06-2851 of 21 June 2026 replaces the whole track system in section A. Do NOT advise the user as though it already applies: the updated fee rules take effect on 1 July 2027, with a staged entry from 1 October 2026, and banks may adopt earlier if they choose. Until a given bank switches, section A remains the operative advice for that customer.

The headline changes: the three tracks are replaced by one supervised service, "nihul cheshbon tashlum", capped at 10 NIS for the first 100 operations a month (5 NIS for an account with 0 to 2 operations, 1 NIS per operation beyond 100); enrolment becomes automatic instead of opt-in; the teller-versus-direct distinction disappears; a separate 7 NIS cap covers the immediate-debit card fee; and the senior and disability definitions are deleted, taking the section A entitlement and the 4a(b1) true-up with them. `references/2027-fee-reform.md` has the full list with the circular's own wording.

To tell which regime applies to a specific user before 1.7.2027, have them check the effective date on their bank's published tariff, or ask the bank in writing whether it has adopted the payment-account-management service. Do not infer it from the date alone: adoption is per-bank until the deadline.

When the user asks what they pay today, answer from section A. Raise this section when they ask what is changing, or when a bank says their track is being discontinued.

## Examples

**Cancel a barely-used credit card.** User has a second credit card they rarely use but pay an annual fee on. First tell them to settle any open installments or credit balance so the cancellation is not blocked or accelerated. Produce template 1 addressed to the issuer, request written confirmation, and request the list of recurring charges billed to that card. Warn them to move each card-billed charge (e.g. streaming, gym, insurance) to another payment method before the card dies, or those charges bounce. Note that any harshaa lechiyuv sits on their bank account, not on the card, so it keeps running untouched and is handled separately at the bank.

**Switch a heavy-transaction account to a fixed track.** User does about 40 direct-channel and 3 teller actions a month and pays per action. Run the calculator with their tariff numbers; every flag is required, so a bare `--direct 40 --teller 3` exits with an argparse error: `scripts/fee_track_calculator.py --direct 40 --teller 3 --direct-fee 1.30 --teller-fee 6.50 --basic-price 10 --expanded-price 26`. At that volume the expanded track beats paying per action. Give them template 4 to join the expanded track from the 1st of next month, and note the switch timing.

**Negotiate down a specific commission.** User is charged a monthly account-management fee higher than the basic track cap. Script: cite that the basic track is supervised at max 10 NIS, ask to be moved to it, and check senior/disability eligibility. Provide the written request and tell them to confirm against the Bank of Israel calculator.

## Recommended MCP Servers

| MCP | What It Adds |
|-----|-------------|
| [Kolzchut (All-Rights)](https://agentskills.co.il/he/mcp/kolzchut) | Looks up the current text of the fee, discount, and cancellation rights this skill cites, so entitlements are read live instead of from a snapshot |
| [Asher MCP](https://agentskills.co.il/he/mcp/asher) | Local-first aggregator for Israeli banks and credit-card issuers; pulls the user's actual fee charges so step 1 uses real action counts rather than an estimate |
| [Israeli Bank MCP](https://agentskills.co.il/he/mcp/israeli-bank) | Fetches transactions from the major banks and card issuers, useful for spotting recurring charges and standing orders the user forgot about |

Use these to source the user's real numbers. The fee amounts and rights in this skill still need to be confirmed against the bank's published tariff and the Bank of Israel rules.

## Gotchas

- **US tactics do not map here.** "Threaten to leave and they will cave" is not the lever. The leverage is the regulated tracks, the entitlements, and the one-click switch (niud).
- **A harshaa lechiyuv is not on the card.** It sits at the bank, on the account, and pulls straight from it. Cancelling or replacing a card does NOT stop it. A card-billed subscription is the mirror image: it dies with the card, so update the payment method with each merchant BEFORE the old card stops. Getting these two backwards is the single most common error in this domain.
- **Stopping the debit does not cancel the debt.** Killing the payment instrument leaves the contract alive, so the business can still invoice or send you to collections. Cancel the underlying iska mitmasheshet too.
- **The refund routes do not cover card-billed charges.** ss.34-38 are written about a harshaa lechiyuv. A gym or streaming charge on the card number has no s.35 route, and sending the bank one burns the 3-business-day clock. Establish the mechanism, then pick the remedy.
- **Do not promise the s.38 refund.** s.38(c) switches it off entirely where the bank offered a debit ceiling and expiry at setup, which most now do. Lead with s.37 (exceeded authorization, no deadline) or s.35 (any debit, 3 business days), and have the user set a ceiling on every new authorization.
- **The senior/disability entitlement is not a percentage.** It is 4 teller actions a month at the direct-channel price, set uniformly by the fee rules, and it reprices per-action teller billing rather than discounting a track's fixed price. A bank quoting a percentage is describing its own voluntary offer. Never invent a percentage or a flat senior age.
- **No soldier, student, youth or new-immigrant discount exists in the rules.** The only categories are senior, 40%+ disability, no-cash-withdrawal-card, and small business. Anything else a bank offers those groups is a revocable commercial benefit, never a legal right.
- **Settle installments before cancelling a card.** Open tashlumim or a kredit balance can be accelerated into one immediate charge, or block the cancellation outright.
- **Do not quote a stale NIS fee.** The basic-track cap (10 NIS) is set by order, but the expanded-track price and every per-action fee come from each bank's current tariff.
- **Do not confuse the two tracks.** Basic = up to 10 direct + 1 teller. Expanded = up to 50 direct + 10 teller. Both are price-supervised, so the difference is included volume, not whether a cap exists.
- **The Postal Bank is exempt** from offering the tracks, so this analysis may not apply there.
- **A track covers only the basic current-account actions it lists.** Overdraft interest, foreign-currency and securities fees stay per the tariff, are not solved by a track, and are often the biggest overpayment. Negotiate them separately (section C).

## Reference Links

| Topic | Source | URL |
|---|---|---|
| Bank fees + the two tracks + small-business tariff | Bank of Israel | https://boi.org.il/information/fees/ |
| Fee-tracks calculator (compare banks) | Bank of Israel | https://www.boi.org.il/information/מחשבונים-וכלים/עמלות/ |
| One-click bank switching (niud): 7-day online move, akev acharai | Kol Zchut | https://www.kolzchut.org.il/he/מעבר_בין_בנקים_באופן_מקוון_%28ניוד%29 |
| Overdraft (chariga mimisgeret): higher interest on a current account | Kol Zchut | https://www.kolzchut.org.il/he/חריגה_ממסגרת_אשראי_בחשבון_עובר_ושב |
| Fixed monthly fee tracks (limits, discounts, switching) | Kol Zchut | https://www.kolzchut.org.il/he/מסלולי_עמלות_במחיר_חודשי_קבוע_בחשבון_עובר_ושב_בבנק |
| Cancelling an ongoing transaction (3/6-day stop, compensation) | Kol Zchut | https://www.kolzchut.org.il/he/ביטול_עסקה_מתמשכת |
| Payment Services Law 5779-2019, sections 34-38 (cancel authorization, reverse a debit, exceeded authorization) | Wikisource (full text) | https://he.wikisource.org/wiki/חוק_שירותי_תשלום |
| Banking Rules (Customer Service)(Fees) 5768-2008: tracks, the 4-teller-action entitlement, rule 4a(b1) true-up | Wikisource (consolidated) | https://he.wikisource.org/wiki/כללי_הבנקאות_(שירות_ללקוח)_(עמלות) |
| Banking (Customer Service) Law 5741-1981 | Nevo | https://www.nevo.co.il/law_html/law01/047_016.htm |

Nevo blocks automated fetching, so it will look unreachable to an agent while opening normally in a browser. The two Wikisource entries carry the same statutory text and are readable either way, so prefer them when you need to quote a section.

## Bundled Resources

- `references/domain-checklist.md` - full coverage contract (core / advanced / out of scope) with sources.
- `references/fee-tracks-comparison.md` - the three billing methods, decision rule, and switching mechanics.
- `references/cancellation-letter-templates.md` - four ready-to-fill Hebrew + English letters (cancel card, stop debit, cancel subscription, request track/discount).
- `references/payment-services-remedies.md` - the four Payment Services Law refund routes with verbatim statutory text, their clocks, and the s.38(c) exception.
- `references/2027-fee-reform.md` - the circular 06-2851 changes, dates, and price caps, and what the reform does to the section A entitlements.
- `scripts/fee_track_calculator.py` - compares no-track vs basic vs expanded using the user's own action counts and bank tariff numbers (`--example` for a worked run).

### Ready-to-send templates (copy and fill the brackets)

The four letters live in `references/cancellation-letter-templates.md`. Send them in Hebrew even when the conversation is in English, since that is what the bank's service desk processes. The Hebrew companion reproduces all four inline.

## Troubleshooting

- **User does not know their monthly action count:** tell them to read recent account statements or ask the bank via site/phone; the calculator needs the direct-channel vs teller split.
- **The bank refuses to switch the track or apply a discount:** put the request in writing (template 4), reference the regulation and their eligibility, and note that the one-click switch (niud) lets them move to a cheaper bank if needed. If the bank still stonewalls, file a free complaint with the Public Complaints unit at the Supervisor of Banks (yechidat pniyot hatsibur, Pikuach al HaBankim) at the Bank of Israel.
- **A charge continues after cancellation:** confirm the notice date and channel; if past the 3/6 business-day cutoff, the up-to-10,000-NIS compensation and full refund apply. If it was a card-billed charge, check the payment method is actually removed at the merchant, not just the card. Escalate to the Bank of Israel banking supervision (Public Complaints unit) or the consumer protection authority.
- **The user wants money already debited back:** first establish it was a harshaa lechiyuv on the account and not a card-billed charge, because the four statutory routes cover only the former. Then pick the route by cause, not by which is most generous. Within 3 business days of the debit, s.35 reverses any debit at all. If the charge broke the authorization's terms (expired, over the permitted amount, wrong date), s.37 applies with no deadline on the user. Only fall back to s.38 after checking the bank did not offer a ceiling at setup, which disables it. See `references/payment-services-remedies.md`.
- **The bank says it cannot cancel the authorization from a letter:** the right under s.34(a) is exercised by notice to the bank, and the bank's own form is a convenience, not a precondition. Send the notice anyway, then use the bank's online channel too if it has one. Supply the beneficiary institution code (kod mosad) and the asmachta, the same fields the banks require to identify an authorization when it is created (Leumi and Mizrahi-Tefahot both publish exactly these), rather than the business's trading name alone.
- **A calculator result looks off:** the per-action and track prices are user inputs from a specific bank's tariff; recheck them against the current tariff and the Bank of Israel fee-tracks calculator, which is authoritative.
