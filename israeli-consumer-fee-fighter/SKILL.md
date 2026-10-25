---
name: israeli-consumer-fee-fighter
description: "Use when an Israeli consumer wants to cut recurring bank and credit-card charges: cancel a credit card cleanly (bitul kartis ashrai), switch to a cheaper fixed-price bank fee track (maslul amlot: basic maslul basi or expanded maslul murchav), switch banks in one click (niud / maavar beklik), stop a recurring debit (bitul harshaa lechiyuv / horaat keva), get back charges that continued after cancelling (a subscription still billed to the card), or negotiate lower fees and commissions (amlot including overdraft, FX, and securities fees). Produces a ready-to-send Hebrew cancellation letter, a rights-grounded negotiation script, and a short rights summary, grounded in Bank of Israel fee rules and Israeli consumer-banking law. Do NOT use for maximizing cashback or deals (use israeli-smart-saver), coupon hunting (use israeli-coupon-code-finder), analyzing bank transactions (use israeli-bank-connector), or household budgeting (use israeli-budget-planner)."
license: MIT
---

# Israeli Consumer Fee Fighter

## Problem

Israeli consumers overpay their bank and card companies every month: billed per action instead of on a fixed-price track, paying for a card they barely use, or still charged by a service they cancelled. The law gives clear levers (two supervised fee tracks, a free one-click bank switch, the right to cancel a card or a recurring debit at any time, entitlements for eligible groups) that most people never invoke. This skill turns them into a cancellation letter, a negotiation script, and a short rights summary.

Fees change, so confirm any number against the bank's current tariff (taarifon amlot) and the Bank of Israel fee-tracks calculator before quoting it.

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

Both expanded tracks have been price-supervised since 1.9.2022 under the Banking (Customer Service) Order, 5782-2022: a bank may not raise these tariffs without Bank of Israel approval. Read the price off the bank's tariff rather than assuming a range.

**First, find out what they are actually paying.** Every step below needs two integers the user almost never has to hand, so do not start by asking them to estimate.

- The account-management charge appears on the statement as a single `עמלות עו"ש` line, billed in arrears for the previous period. Most banks bill it monthly at the start of the month; some bill quarterly, so check the period the line covers before dividing by anything.
- Count by the rule's list, not by channel. Direct-channel actions (First Schedule item 1(a)(3)) include every incoming clearing credit (salary, pension, Bituach Leumi), the monthly credit-card debit, every authorization or standing-order debit, transfers, voucher payments, cheques drawn and deposited, and machine cash deposits and ATM withdrawals. Information queries by internet or IVR and immediate-debit card purchases are not charged. Anything done by a clerk, including a staffed phone line, is a teller action (peulat pakid). A pensioner with a pension, a BL allowance and a card bill already has 3 direct actions before doing anything.
- Ask the bank in writing for a concentration of the fees actually charged to the account over the last 12 months. Banks produce this on request and it hands you the totals and the action split in one document, which is far faster than adding up statements.
- The tariff's annexes must be delivered to the customer, and Annex A is specifically the population-group benefits table (`נספח א׳ – הטבות לקבוצות אוכלוסיה`). That is where a bank sets out what it applies to the categories in step 2, so ask for it by name rather than accepting a verbal answer.
- **Cut the count before you re-price it.** Every deposit, transfer or voucher payment moved from a clerk to the app or ATM is billed at the direct-channel price instead of the teller price, which for many users beats any track switch. If the bank offers no reasonable direct channel for depositing cheques or cash, those teller deposits may be charged only at the direct-channel price (item 1(a)(2), note 2): count them as `--direct` in the calculator.
- **No track is not free for a quiet account.** The bank may charge the higher of the actual per-action total or a monthly minimum of up to one teller action's price (item 1(a)(2), note 3). Pass it to the calculator as `--min-fee`.

Decision steps:
1. Get the typical monthly action count, split into direct-channel and teller, using the list above rather than a guess.
2. Check for a cheaper path first. The senior and disability entitlement is set by the fee rules themselves, so it is identical at every bank and is **not** a percentage discount:
   - **What it is:** a customer who is an azrach vatik, a person with a disability, or who holds no cash-withdrawal card gets **4 teller actions a month charged at the direct-channel price** (Banking Rules (Customer Service)(Fees), 5768-2008, First Schedule, item 1(a)(2) note). There is no published percentage or shekel discount. Do not invent one.
   - **Senior = retirement age.** The fee rules define azrach vatik through the Senior Citizens Law, 5750-1989, which keys it to the Retirement Age Law, 5764-2004 (sex- and birth-date-dependent), so read it off that law rather than quoting a number.
   - **Disability = a customer who has PRESENTED the bank a Ministry of Defense or Bituach Leumi certificate of 40%+ disability.** Presenting it is what creates the entitlement, which starts on the 1st of the month after presentation and is **not retroactive**. Tell the user to hand it in now rather than assume the bank knows.
   - A small business (esek katan) may not be charged more for a tariff service than a larger corporation, card-clearing fees excepted (rule 2(b)), and gets the rule 4a(b2) true-up in step 3.

   The entitlement is **not** an alternative to joining a track, and it does not discount the fixed track price. It reprices teller actions wherever they are billed per action under item 1(a)(2), which means both when the customer is on no track at all and on a track's teller OVERAGE. So it changes the arithmetic of all three options at once rather than adding a fourth. Do not reason about it by hand: pass `--entitled` to the calculator in step 4, which applies it to every method. For a low-volume eligible customer it routinely flips the recommendation.
3. **Check the bank owed them an automatic track enrolment.** Under rule 4a(b1), if a senior or a person with a disability was charged more every single month of a financial year than the basic track would have cost, the bank must compute the differences and **enroll them in the basic track by 1 March of the following year**, notify in writing, and allow an opt-out. Rule 4a(b2) does the same for a small business / osek murshe, enrolling it in the basic or the expanded track, whichever the average differences favour. Banks do not always do this. Have the user ask what the comparison showed for the last completed year, and treat a missing enrolment as a complaint ground under section C. The rule obliges enrolment **going forward** and does not on its text award a refund of the prior year's excess; ask for restitution anyway in the same letter (template 4) as a separate request, so the complaint does not concede the past year.
4. Run `scripts/fee_track_calculator.py` with the user's action counts and their bank's real per-action and track prices to compare all three methods. It adds estimated overage so an over-limit track is not recommended blindly.
5. Use the Bank of Israel fee-tracks calculator to compare banks, but its stored bank prices can be years old (the page dates them); the bank's current tariff controls.
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
- **Stop a recurring debit:** under the Payment Services Law, 5779-2019, s.34(a), the payer may cancel a debit authorization at any time by notice to the bank or to the beneficiary. Use template 2. The bank must notify the beneficiary within two business days. Cancelling an authorization or standing order before at least 6 debits have been presented under it lets the bank charge up to 6 direct-channel action fees (First Schedule item 1(a)(3), note), so the cancellation itself is not always free.
- **Cancel the debit is not the same as cancel the debt:** stopping the harshaa or the card charge only stops the payment instrument. The underlying contract survives, so the business can still invoice you or send the debt to collections. To end the obligation itself, also cancel the underlying transaction (template 3), not just the payment.
- **Cancel an ongoing subscription (iska mitmasheshet):** cancellation follows the contract's terms, and a merchant other than a telecom company may charge an agreed exit fee if it is reasonable, so check the contract first. The contract ends and charging must stop within 3 business days of the notice (6 business days if sent by registered mail), Consumer Protection Law s.13d(c). Use template 3. If the business keeps charging after the cutoff, the later charges are refundable and a court may award exemplary damages without proof of damage of up to 10,000 NIS (s.31a(a)(2b)), or up to 50,000 NIS for a repeat or continuing breach. A suit needs a prior cancellation notice that is not merely oral (s.31a(b)), so a phone-only cancellation is not enough. A sign-up made by phone or online (a distance sale) also carries a separate 14-day cancellation right (s.14c).

Always send by a channel that leaves a record (registered mail, email, or the company website) so the notice date is provable; the stop-charging clock runs from that date.

**Getting back money already taken.** Stopping future charges is only half the job, and users routinely assume a wrong debit is gone for good. First establish whether the charge ran under an authorization on the ACCOUNT or on a CARD (is it in the bank's list of active authorizations, or only on the card statement?).

- **Account authorization (harshaa lechiyuv), four routes against the bank:** s.35(a) reverses any one debit if the user notifies within 3 business days of it (refund within 1 business day); s.37 refunds a charge that broke the authorization's terms (expired, above the permitted amount, wrong date) with no user deadline, within 1 business day; s.38(a) refunds an unreasonably large debit within 7 business days, but s.38(c) switches it off entirely where the bank offered a ceiling and expiry at setup, which most now do; s.34(c) voids an authorization unused for 24 months. Have the user set a ceiling (tikra) on every new authorization, which turns a later overrun into a s.37 case.
- **Card charge, run three tracks in parallel, not in sequence.** (1) Cancel with the merchant under the ongoing-transaction rules above; that is where the damages lie. (2) Notify the card ISSUER (Cal / Max / Isracard, or the bank if it issued the card): the statute defines a harshaa lechiyuv as an authorization to charge the account *or the payer's payment instrument* (s.1), so ss.34-35 can reach a recurring card charge, though an issuer may argue a merchant that merely stored the card number holds no authorization. Send it within 3 business days of a charge anyway. Separately, s.29 lets a payer who tells the issuer within 30 days that they did not execute a card-not-present charge claim it back within 8 business days; whether a charge after a valid cancellation counts as one the payer did not execute is arguable, so present it as a claim, not a guarantee. (3) For a purchase paid in card instalments where the goods or service were not supplied, or the merchant stopped supplying for good, and the user has notified the merchant of cancellation, s.17 obliges the issuer to stop the remaining payments from the notice date; it does not refund what was already paid. A charge increased beyond what the user agreed is refunded within 8 business days (s.28).

Verbatim text and clocks for every route are in `references/payment-services-remedies.md`.

**Closing the account is not free, but it is capped.** Total closure fees may not exceed 40 NIS (track fees excluded), and that cap explicitly covers cancelling debit authorizations and standing orders, so a bank may not bill those separately on closure. The customer may end the account contract at any time under Payment Services Law s.6(a), but the bank may require the steps set out in the contract first, and the five-business-day clock only starts once those are done. That is the lever a stalling bank uses, so frame it as "complete their checklist, then the clock runs," not "they cannot refuse."

### C. Negotiate fees down

The Israeli approach is not US-style "call and threaten to leave." It is grounded in concrete rights:
1. State your position with data: "I run X direct actions and Y teller actions a month; the [basic/expanded] track, or the entitlement I qualify for, is cheaper for me than what I pay now."
2. Cite the lever: the two fee tracks, your entitlement (senior / 40%+ disability / no cash-withdrawal card: 4 teller actions a month at the direct price; small business: rule 2(b), which excludes card clearing, and the 4a(b2) true-up), and the Bank of Israel calculator showing a cheaper bank.
3. Ask for a specific outcome: switch to the named track, apply the entitlement you qualify for, or waive/reduce a specific commission.
4. If the bank will not move, the credible alternative is switching tracks or switching banks via the one-click switch reform (see section D), not an empty threat. Put the request in writing so there is a record.

Do not stop at the account-management fee. The biggest real overpayment is often outside the fee tracks: overdraft interest (when the balance drops below zero or past the credit line, riba al chariga), the interest on a credit line (an individual may not be charged for setting a line up), and foreign-currency and securities fees. No track covers them; raise each as a separate target. An unused credit line is not free either: an individual can be charged a quarterly credit-allocation fee (hakatzat ashrai) in any quarter the line goes unused (with partial use, the higher of that quarter's interest or the fee), so shrink or cancel an unused line. Two hard caps are worth checking on the statement: the basic track (10 NIS) and, since 1 October 2026, the immediate-debit (debit) card fee, which a bank may not set above 7 NIS a month (section E). A charge above either is a complaint ground, not a negotiation.

If the bank refuses to switch your track or apply an entitlement you clearly qualify for, escalate. The route has two steps and users routinely skip the first, which gets the complaint bounced back:

1. **The bank's own ombudsman (natziv tlunot hatsibur) first.** The Bank of Israel requires this step to be exhausted before it will take the complaint. Submit in writing and keep the reference number; a written answer is due within 45 days, extendable to 60 with written notice (Directive 308A).
2. **Then the Supervisor of Banks Public Inquiries unit**, via the online complaint form linked from <https://www.boi.org.il/information/public-enquiries-unit/ihaveaq/>. Filing requires identity verification and is free. Attach the ombudsman's reply.

Match the regulator to the counterparty. The Supervisor of Banks covers banks and credit-card companies only. A gym, streaming service, or other merchant that keeps charging after a cancellation is a Consumer Protection and Fair Trade Authority matter; sending it to the Bank of Israel loses months.

Produce the letter (from `references/cancellation-letter-templates.md`), the negotiation script (steps 1-4 above, filled with the user's numbers), and a short rights summary (the specific track limits, cancellation rights, and entitlements that apply to them).

### D. Switch banks in one click (niud / maavar beklik)

Since 22 September 2021 every Israeli can move their current account to a cheaper bank through a free, fully online switch. The customer only opens an account at the new bank and asks it to run the switch; the process completes within 7 business days from submission, and the customer may request an extension of up to 30 business days. It transfers the shekel and foreign-currency balances, the standing orders (horaot keva) and current-account authorizations, checks, and both bank and non-bank credit-card activity. After the move, an "akev acharai" ("follow me") service forwards charges and credits that still land in the old account to the new one for 3 years.

The window is 3 years from the switch, except that **anyone who switched before 21.9.2026 keeps forwarding until 31.7.2029** (transitional rule 5a of the bank-switching rules). So the first cohort did NOT lose forwarding in September 2026; do not tell them it ended. During forwarding the bank sends a half-yearly report listing the parties not yet updated. Use it to move the employer, Bituach Leumi and every standing beneficiary to the new account before forwarding ends, or incoming payments and outgoing charges start failing silently.

An overdrawn account switches only if the new bank's available balance, including its approved credit line, covers the debit balance (rule 2(5)(b)), and an existing loan needs an agreed repayment arrangement and adequate collateral (rule 2(6)), so arrange a credit line at the new bank first. Securities take up to 12 business days (Israeli) or 15 (foreign). Tell the user plainly what does NOT come across: loans (including mortgages), deposits and savings plans, non-transferable securities, and safe-deposit boxes or products pledged to the old bank all stay behind and need a separate arrangement with the previous bank. Bank of Jerusalem customers cannot use the online switch at all.

This is the single biggest fee-cut lever for many people: instead of negotiating one commission at a time, they land at the bank the Bank of Israel calculator shows as cheapest for their profile. It also solves the standing-order problem in section B automatically. Because niud moves the horaot keva for you, a user who is switching banks does NOT need to re-set-up each authorization by hand. Authorizations on a card the old bank issued move as well (rule 3(8)), but any merchant that stored a card number needs the new number once that card is replaced, so check each one. When a user's real problem is a bank that is simply expensive across the board, route them to niud, not to a track switch.

### E. The fee reform (circular 06-2851): partly in force since 1.10.2026

Supervisor of Banks circular 06-2851 of 21 June 2026 replaces the track system in section A, in two stages:

- **In force since 1 October 2026:** a bank may charge at most 7 NIS a month for an immediate-debit card, including cards issued before the change. The existing waiver (no debit-card fee for 36 months for a customer who also holds a valid credit card from the same bank) runs alongside until 1 July 2027. Three charges were abolished the same day: debiting a cheque writer for a cheque returned for a technical reason, account location, and estate handling.
- **From 1 July 2027:** the tracks become one supervised service, "nihul cheshbon tashlum", capped at 10 NIS for 3 to 100 operations a month (5 NIS for 0 to 2, 1 NIS per operation beyond 100), with automatic enrolment and no teller-versus-direct split. The senior and disability definitions are deleted with the 4a(b1) true-up; the section A entitlement becomes moot because teller and direct actions are no longer priced apart. A bank may adopt these rules earlier only if it adopts them in full.

Until a bank adopts the 2027 rules, section A remains the operative advice for its customers; check the effective date on its tariff or ask in writing. `references/2027-fee-reform.md` has the circular's wording.

## Examples

**Cancel a barely-used credit card.** User pays a fee on a second card they rarely use. Settle open installments or credit first, send template 1 to the issuer asking for written confirmation and the list of recurring charges on the card, and move each card-billed charge to another payment method before the card dies. Any harshaa lechiyuv on the account keeps running and is handled at the bank.

**Switch a heavy-transaction account to a fixed track.** User does about 40 direct-channel and 3 teller actions a month and pays per action. Run the calculator with their tariff numbers (all six flags are required): `scripts/fee_track_calculator.py --direct 40 --teller 3 --direct-fee 1.30 --teller-fee 6.50 --basic-price 10 --expanded-price 26`. At that volume the expanded track beats paying per action. Give them template 4 to join it from the 1st of next month.

**Negotiate down a specific commission.** User is charged a monthly account-management fee higher than the basic track cap. Script: cite that the basic track is supervised at max 10 NIS, ask to be moved to it, and check senior/disability eligibility. Provide the written request and tell them to confirm against the Bank of Israel calculator.

## Recommended MCP Servers

| MCP | What It Adds |
|-----|-------------|
| [Kolzchut (All-Rights)](https://agentskills.co.il/he/mcp/kolzchut) | Reads the current text of the rights this skill cites |
| [Asher MCP](https://agentskills.co.il/he/mcp/asher) | Local aggregator for Israeli banks and card issuers; pulls real fee charges and action counts |
| [Israeli Bank MCP](https://agentskills.co.il/he/mcp/israeli-bank) | Fetches transactions to spot forgotten recurring charges and standing orders |

Use these for the user's real numbers; confirm fees against the bank's tariff.

## Gotchas

- **A harshaa lechiyuv is not on the card.** It sits at the bank, on the account, and pulls straight from it. Cancelling or replacing a card does NOT stop it. A card-billed subscription is the mirror image: it dies with the card, so update the payment method with each merchant BEFORE the old card stops. Getting these two backwards is the single most common error in this domain.
- **Stopping the debit does not cancel the debt.** Killing the payment instrument leaves the contract alive, so the business can still invoice or send you to collections. Cancel the underlying iska mitmasheshet too.
- **Card charges need their own routes, run in parallel.** ss.34-38 reach a card only where the charge runs under an authorization, and an issuer may say a stored card number is not one. Do not bet the 3-business-day s.35 window on the issuer alone: cancel with the merchant at the same time, and use s.17 for unsupplied instalment purchases.
- **The niud forwarding did not end in September 2026.** Switches before 21.9.2026 keep forwarding until 31.7.2029.
- **Do not promise the s.38 refund.** s.38(c) switches it off entirely where the bank offered a debit ceiling and expiry at setup, which most now do. Lead with s.37 (exceeded authorization, no deadline) or s.35 (any debit, 3 business days), and have the user set a ceiling on every new authorization.
- **The senior/disability entitlement is not a percentage.** It is 4 teller actions a month at the direct-channel price, set uniformly by the fee rules, and it reprices per-action teller billing rather than discounting a track's fixed price. A bank quoting a percentage is describing its own voluntary offer. Never invent a percentage or a flat senior age.
- **No soldier, student, youth or new-immigrant discount exists in the rules.** The only categories are senior, 40%+ disability, no-cash-withdrawal-card, and small business. Anything else a bank offers those groups is a revocable commercial benefit, never a legal right.
- **The Postal Bank is exempt** from offering the tracks, so this analysis may not apply there.
- **A track covers only the basic current-account actions it lists.** Overdraft interest, foreign-currency and securities fees stay per the tariff, are not solved by a track, and are often the biggest overpayment. Negotiate them separately (section C).

## Reference Links

| Topic | Source | URL |
|---|---|---|
| Bank fees + the two tracks + small-business tariff | Bank of Israel | https://boi.org.il/information/fees/ |
| Fee-tracks calculator (compare banks) | Bank of Israel | https://www.boi.org.il/information/מחשבונים-וכלים/עמלות/ |
| One-click bank switching (niud): 7-day online move, akev acharai (to 31.7.2029 for pre-21.9.2026 switches) | Kol Zchut | https://www.kolzchut.org.il/he/מעבר_בין_בנקים_באופן_מקוון_%28ניוד%29 |
| Overdraft (chariga mimisgeret): higher interest on a current account | Kol Zchut | https://www.kolzchut.org.il/he/חריגה_ממסגרת_אשראי_בחשבון_עובר_ושב |
| Fixed monthly fee tracks (limits, entitlements, switching) | Kol Zchut | https://www.kolzchut.org.il/he/מסלולי_עמלות_במחיר_חודשי_קבוע_בחשבון_עובר_ושב_בבנק |
| Cancelling an ongoing transaction (3/6-day stop, compensation) | Kol Zchut | https://www.kolzchut.org.il/he/ביטול_עסקה_מתמשכת |
| Payment Services Law 5779-2019, sections 34-38 (cancel authorization, reverse a debit, exceeded authorization) | Wikisource (full text) | https://he.wikisource.org/wiki/חוק_שירותי_תשלום |
| Banking Rules (Customer Service)(Fees) 5768-2008: tracks, the 4-teller-action entitlement, rule 4a(b1) true-up | Wikisource (consolidated) | https://he.wikisource.org/wiki/כללי_הבנקאות_(שירות_ללקוח)_(עמלות) |
| Banking (Customer Service) Law 5741-1981 | Nevo | https://www.nevo.co.il/law_html/law01/047_016.htm |

Nevo blocks automated fetching; quote sections from the two Wikisource entries instead.

## Bundled Resources

- `references/domain-checklist.md` - full coverage contract (core / advanced / out of scope) with sources.
- `references/fee-tracks-comparison.md` - the three billing methods, decision rule, and switching mechanics.
- `references/cancellation-letter-templates.md` - four ready-to-fill letters, Hebrew and English (cancel card, stop debit, cancel subscription, request a track or an entitlement).
- `references/payment-services-remedies.md` - the four account-authorization refund routes, the card-charge routes (ss.17, 28, 29), and the merchant damages rule, with verbatim statutory text and clocks.
- `references/2027-fee-reform.md` - the circular 06-2851 stages (1.10.2026 and 1.7.2027), price caps, and what the reform does to the section A entitlements.
- `scripts/fee_track_calculator.py` - compares no-track vs basic vs expanded using the user's own action counts and bank tariff numbers, with optional `--entitled` and `--min-fee` (`--example` for a worked run).

### Ready-to-send templates (copy and fill the brackets)

The four letters live in `references/cancellation-letter-templates.md`. Send them in Hebrew even when the conversation is in English, since that is what the bank's service desk processes.

## Troubleshooting

- **User does not know their monthly action count:** use the statement mapping and the 12-month fee concentration in section A.
- **The bank refuses to switch the track or apply an entitlement:** put the request in writing (template 4), reference the regulation and their eligibility, and note that the one-click switch (niud) lets them move to a cheaper bank if needed. If the bank still stonewalls, file a free complaint with the Public Complaints unit at the Supervisor of Banks (yechidat pniyot hatsibur, Pikuach al HaBankim) at the Bank of Israel.
- **A charge continues after cancellation:** confirm the notice date and a written channel; if past the 3/6 business-day cutoff, the later charges are refundable and a court may award up to 10,000 NIS exemplary damages. If it was a card charge, check the payment method is actually removed at the merchant, not just the card. Escalate a bank or card company to the Public Complaints unit, a merchant to the consumer protection authority.
- **The user wants money already debited back:** first establish whether it ran under an account authorization or on a card (section B). For an account authorization pick the route by cause: s.35 within 3 business days for any debit, s.37 with no deadline if the authorization's terms were broken, s.38 only after checking the bank did not offer a ceiling at setup. See `references/payment-services-remedies.md`.
- **The bank says it cannot cancel the authorization from a letter:** the right under s.34(a) is exercised by notice to the bank, and the bank's own form is a convenience, not a precondition. Send the notice anyway, then use the bank's online channel too if it has one. Supply the beneficiary institution code (kod mosad) and the asmachta, the same fields the banks require to identify an authorization when it is created (Leumi and Mizrahi-Tefahot both publish exactly these), rather than the business's trading name alone.
- **A calculator result looks off:** the per-action and track prices are user inputs from a specific bank's tariff; recheck them against the bank's current tariff, which controls; the Bank of Israel calculator's stored prices may be out of date.
