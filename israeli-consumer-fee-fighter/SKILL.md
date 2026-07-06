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

Israeli banks (except the Postal Bank) must offer two fixed-price tracks under Banking Rules (Customer Service)(Fees), 5768-2008, section 4a (in force since 1.4.14). A customer who picks no track is charged per action and can pay up to 2.5x (basic-level volume) or 5x (expanded-level volume) at some banks.

| Method | Direct-channel actions/month | Teller actions/month | Monthly price |
|---|---|---|---|
| No track (per action) | pay per action | pay per action | varies (can be 2.5x-5x a track) |
| Basic track (maslul basi) | up to 10 | up to 1 | supervised, max 10 NIS |
| Expanded track (maslul murchav) | up to 50 | up to 10 | not supervised, 20-30 NIS |
| Expanded-plus (some banks) | expanded + extras | expanded + extras | bank-specific |

Decision steps:
1. Ask the user for their typical monthly action count, split into direct-channel (internet, app, ATM, standing orders) and teller (peulat pakid). If they do not know, tell them to read it off recent statements or ask the bank.
2. Check for a cheaper path first: seniors (azrachim vatikim) and people with 40%+ determined disability are entitled to fee discounts; a business may qualify as a small business (esek katan) for the reduced tariff. A discount can beat a track.
3. Run `scripts/fee_track_calculator.py` with the user's action counts and their bank's real per-action and track prices to compare all three methods. It adds estimated overage so an over-limit track is not recommended blindly.
4. Confirm the result against the Bank of Israel fee-tracks calculator, which compares against every bank.
5. To switch: notify the bank via site, phone, or branch. The switch takes effect on the 1st of the month after the notice. Use the request template in `references/cancellation-letter-templates.md` (template 4).

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
- **Stop a recurring debit:** under the Payment Services Law, 5779-2019, section 34(a), the payer may cancel a debit authorization at any time by notice to the bank or to the beneficiary. Use template 2. The bank must notify the beneficiary within two business days.
- **Cancel the debit is not the same as cancel the debt:** stopping the harshaa or the card charge only stops the payment instrument. The underlying contract survives, so the business can still invoice you or send the debt to collections. To end the obligation itself, also cancel the underlying transaction (template 3), not just the payment.
- **Cancel an ongoing subscription (iska mitmasheshet):** the business must stop charging within 3 business days of the notice (6 business days if sent by registered mail). Use template 3. If the business keeps charging after the cutoff, the consumer is entitled to compensation without proof of damage of up to 10,000 NIS plus a full refund. A general 14-day cancellation right also applies to recent sign-ups.

Always send by a channel that leaves a record (registered mail, email, or the company website) so the notice date is provable; the stop-charging clock runs from that date.

### C. Negotiate fees down

The Israeli approach is not US-style "call and threaten to leave." It is grounded in concrete rights:
1. State your position with data: "I run X direct actions and Y teller actions a month; the [basic/expanded] track or a discount is cheaper for me than what I pay now."
2. Cite the lever: the two fee tracks, your eligibility for a discount (senior / 40%+ disability / small business), and the Bank of Israel calculator showing a cheaper bank.
3. Ask for a specific outcome: switch to the named track, apply the discount you qualify for, or waive/reduce a specific commission.
4. If the bank will not move, the credible alternative is switching tracks or switching banks via the one-click switch reform (see section D), not an empty threat. Put the request in writing so there is a record.

Do not stop at the account-management fee. The biggest real overpayment is often outside the fee tracks: overdraft interest (when the balance drops below zero or past the credit line, riba al chariga), the interest and setup fees on a credit line, and foreign-currency and securities fees. These are not covered by any track, but they are negotiable, so raise them as separate targets and ask for a lower rate or a waiver on each.

If the bank refuses to switch your track or apply a discount you clearly qualify for, escalate for free to the Public Complaints unit at the Supervisor of Banks (yechidat pniyot hatsibur, Pikuach al HaBankim) at the Bank of Israel. This is the enforcement lever when a bank stonewalls; a written complaint there costs nothing.

Produce the letter (from `references/cancellation-letter-templates.md`), the negotiation script (steps 1-4 above, filled with the user's numbers), and a short rights summary (the specific track limits, cancellation rights, and discount eligibility that apply to them).

### D. Switch banks in one click (niud / maavar beklik)

Since 22 September 2021 every Israeli can move their whole account to a cheaper bank through a free, fully online switch. The customer only opens an account at the new bank and asks it to run the switch; the process completes within 7 business days. It transfers the shekel and foreign-currency balances, the standing orders (horaot keva) and current-account authorizations, checks, securities, and both bank and non-bank credit-card activity. After the move, an "akev acharai" ("follow me") service automatically forwards charges and credits that still land in the old account to the new one, so nothing is lost in transition.

This is the single biggest fee-cut lever for many people: instead of negotiating one commission at a time, they land at the bank the Bank of Israel calculator shows as cheapest for their profile. It also solves the standing-order problem in section B automatically. Because niud moves the horaot keva for you, a user who is switching banks does NOT need to re-set-up each authorization by hand; they only need to update card-billed charges with each merchant (those follow the card, not the account). When a user's real problem is a bank that is simply expensive across the board, route them to niud, not to a track switch.

## Examples

**Cancel a barely-used credit card.** User has a second credit card they rarely use but pay an annual fee on. First tell them to settle any open installments or credit balance so the cancellation is not blocked or accelerated. Produce template 1 addressed to the issuer, request written confirmation, and request the list of recurring charges billed to that card. Warn them to move each card-billed charge (e.g. streaming, gym, insurance) to another payment method before the card dies, or those charges bounce. Note that any harshaa lechiyuv sits on their bank account, not on the card, so it keeps running untouched and is handled separately at the bank.

**Switch a heavy-transaction account to a fixed track.** User does about 40 direct-channel and 3 teller actions a month and pays per action. Run `scripts/fee_track_calculator.py --direct 40 --teller 3` with their tariff numbers; the expanded track (20-30 NIS) beats paying per action. Give them template 4 to join the expanded track from the 1st of next month, and note the switch timing.

**Negotiate down a specific commission.** User is charged a monthly account-management fee higher than the basic track cap. Script: cite that the basic track is supervised at max 10 NIS, ask to be moved to it, and check senior/disability eligibility. Provide the written request and tell them to confirm against the Bank of Israel calculator.

## Gotchas

- **Do not assume US tactics map to Israel.** "Threaten to leave and they will cave" is not the lever here. The real leverage is the regulated fee tracks, the discount eligibilities, and the one-click bank switch (niud). Ground every negotiation in those, not in bluffing.
- **A harshaa lechiyuv is not on the card.** A standing debit authorization is set up at the bank, on the account, and pulls straight from the account. Cancelling or replacing a card does NOT stop it. To stop it, notify the bank (or under section 34(a) stop the debit at any time), or let a niud move it for you. Do not tell the user a card cancellation ends it.
- **Card-billed subscriptions fail when the card dies.** A subscription billed to the card number (streaming, gym, insurance) is the opposite case: it is tied to the card, so cancelling or replacing the card makes it FAIL. The fix is to update the payment method with each merchant before the old card stops, not to cancel anything at the bank.
- **Stopping the debit does not cancel the debt.** Killing the harshaa or the card charge only stops the payment. The contract lives on and the business can still invoice or send you to collections. Always also cancel the underlying transaction (iska mitmasheshet) when the goal is to end the service, not just stop the money.
- **Settle installments before cancelling a card.** Open tashlumim or a kredit balance can be accelerated into one immediate charge, or block the cancellation entirely, if you cancel the card first.
- **Do not quote a stale NIS fee.** Fee amounts change and vary by bank. The basic-track cap (10 NIS) and expanded range (20-30 NIS) are cited from the sources, but per-action fees come from each bank's current tariff. Direct the user to the current tariff and the Bank of Israel calculator before acting on any number.
- **Do not confuse the two tracks.** Basic = up to 10 direct + up to 1 teller, supervised. Expanded = up to 50 direct + up to 10 teller, not supervised. Recommending the wrong one wastes money; check the user's actual action split.
- **The Postal Bank is exempt** from offering the tracks, so this analysis may not apply there.
- **A track only covers the basic current-account actions it lists.** Overdraft interest, foreign-currency, and securities fees stay per the tariff and are not solved by joining a track, but they are often the biggest overpayment and are negotiable on their own (section C).

## Reference Links

| Topic | Source | URL |
|---|---|---|
| Bank fees + the two tracks + small-business tariff | Bank of Israel | https://boi.org.il/information/fees/ |
| Fee-tracks calculator (compare banks) | Bank of Israel | https://www.boi.org.il/information/מחשבונים-וכלים/עמלות/ |
| One-click bank switching (niud): 7-day online move, akev acharai | Kol Zchut | https://www.kolzchut.org.il/he/מעבר_בין_בנקים_באופן_מקוון_(ניוד) |
| Overdraft (chariga mimisgeret): higher interest on a current account | Kol Zchut | https://www.kolzchut.org.il/he/חריגה_ממסגרת_אשראי_בחשבון_עובר_ושב |
| Fixed monthly fee tracks (limits, discounts, switching) | Kol Zchut | https://www.kolzchut.org.il/he/מסלולי_עמלות_במחיר_חודשי_קבוע_בחשבון_עובר_ושב_בבנק |
| Cancelling an ongoing transaction (3/6-day stop, compensation) | Kol Zchut | https://www.kolzchut.org.il/he/ביטול_עסקה_מתמשכת |
| Payment Services Law 5779-2019 (cancel debit authorization) | Nevo | https://www.nevo.co.il/law_html/law01/502_043.htm |
| Banking (Customer Service) Law 5741-1981 | Nevo | https://www.nevo.co.il/law_html/law01/047_016.htm |

## Bundled Resources

- `references/domain-checklist.md` - full coverage contract (core / advanced / out of scope) with sources.
- `references/fee-tracks-comparison.md` - the three billing methods, decision rule, and switching mechanics.
- `references/cancellation-letter-templates.md` - four ready-to-fill Hebrew + English letters (cancel card, stop debit, cancel subscription, request track/discount).
- `scripts/fee_track_calculator.py` - compares no-track vs basic vs expanded using the user's own action counts and bank tariff numbers (`--example` for a worked run).

## Troubleshooting

- **User does not know their monthly action count:** tell them to read recent account statements or ask the bank via site/phone; the calculator needs the direct-channel vs teller split.
- **The bank refuses to switch the track or apply a discount:** put the request in writing (template 4), reference the regulation and their eligibility, and note that the one-click switch (niud) lets them move to a cheaper bank if needed. If the bank still stonewalls, file a free complaint with the Public Complaints unit at the Supervisor of Banks (yechidat pniyot hatsibur, Pikuach al HaBankim) at the Bank of Israel.
- **A charge continues after cancellation:** confirm the notice date and channel; if past the 3/6 business-day cutoff, the up-to-10,000-NIS compensation and full refund apply. If it was a card-billed charge, check the payment method is actually removed at the merchant, not just the card. Escalate to the Bank of Israel banking supervision (Public Complaints unit) or the consumer protection authority.
- **A calculator result looks off:** the per-action and track prices are user inputs from a specific bank's tariff; recheck them against the current tariff and the Bank of Israel fee-tracks calculator, which is authoritative.
