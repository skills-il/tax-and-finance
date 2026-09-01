# Domain checklist: Israeli Consumer Fee Fighter

Coverage contract for cutting recurring bank and credit-card charges in Israel: choosing a cheaper fee track, cancelling a card or service cleanly, and negotiating fees down. Every row is verified in `evidence.json`.

## Must cover (core)

- **The two fixed-price fee tracks** required by Banking Rules (Customer Service)(Fees), 5768-2008, section 4a, in force since 1.4.14:
  - **Basic track (maslul basi):** up to 10 direct-channel transactions + up to 1 teller transaction/month. Supervised price, cannot exceed 10 NIS/month.
  - **Expanded track (maslul murchav):** up to 50 direct-channel transactions + up to 10 teller transactions/month. Price-supervised since 1.9.2022 under the Banking Order 5782-2022; the bank may not raise the tariff without Bank of Israel approval. Read the current price from the bank's tariff.
- **No-track default:** a customer who does not pick a track is charged per action, which is usually more expensive for steady activity. Compare the user's own per-action total against the track price rather than quoting a multiple.
- **How to pick the cheaper option:** count monthly direct-channel vs teller actions, compare against track prices, use the Bank of Israel fee-tracks calculator.
- **Switching tracks:** notify the bank (site / phone / branch); switch takes effect on the 1st of the month after the notice.
- **One-click bank switching (niud / maavar beklik):** free, fully online move of the CURRENT ACCOUNT to a cheaper bank; completes within 7 business days of submission, extendable to 30 business days on request; transfers shekel + FX balances, standing orders, current-account authorizations, checks, TRANSFERABLE securities, and bank + non-bank card activity. It does NOT transfer loans and credit including mortgages, deposits and savings plans, non-transferable securities, or safes and products pledged to the old bank, each of which needs a separate arrangement with the previous bank. The "akev acharai" auto-forward of old-account charges/credits runs for 3 years. Bank of Jerusalem customers cannot use the online switch. Effective 22.9.2021. Biggest fee-cut lever for many, and it auto-migrates the horaot keva.
- **Right to cancel a recurring debit authorization (harshaa lechiyuv):** Payment Services Law 5779-2019, section 34(a) - the payer may cancel at any time by notice to the bank or the beneficiary. The harshaa is set up at the BANK, on the ACCOUNT, so it is not affected by cancelling a card.
- **Card-billed recurring charge vs harshaa lechiyuv:** a subscription billed to the card number FAILS when the card is cancelled/replaced (fix: update the payment method with each merchant); a harshaa lechiyuv on the account does NOT fail and is stopped separately at the bank. Two distinct mechanisms.
- **Cancel-debit is not cancel-debt:** stopping the harshaa / card charge stops only the payment instrument; the underlying contract survives (business can still invoice or send to collections), so also cancel the underlying iska mitmasheshet.
- **Right to cancel an ongoing transaction (iska mitmasheshet):** business must stop charging within 3 business days (6 by registered mail).
- **Cancelling a credit card:** the process (notify the issuer in writing), distinguishing a bank-issued card (notify the bank) from an externally-issued card (Cal / Max / Isracard: card company holds the card-billed charge list, bank holds the account harshaot), and settling open installments (tashlumim) / kredit balance first so cancellation is not accelerated or blocked.
- **Overdraft + credit-line + FX + securities fees:** separate negotiation targets outside any track; overdraft interest (chariga mimisgeret) is often the biggest real overpayment and is negotiable.
- **Senior / disability / no-cash-card entitlement, quantified:** NOT a percentage. Banking Rules (Customer Service)(Fees) 5768-2008, First Schedule, item 1(a)(2) note: 4 teller actions a month at the direct-channel price. Uniform across banks. Senior = retirement age: the fee rules give no age, defining azrach vatik by reference to the Senior Citizens Law 5750-1989, which keys it to the Retirement Age Law 5764-2004. Sex- and birth-date-dependent and re-staged by amendment more than once, so read it off that law; never a flat number here. Disability = a customer who HAS PRESENTED a MoD/BL certificate of 40%+; entitlement starts the 1st of the following month and is not retroactive. Falls on 1.7.2027 because the two definitions it is written in terms of are deleted, NOT because it sits in rule 4a (it does not) and NOT because rule 4a is repealed in its entirety (only its track-related limbs are; 4a(d)-(e) survive in adapted form).
- **Automatic basic-track enrolment true-up:** rule 4a(b1) (seniors / people with disability) and 4a(b2) (small business / osek murshe). If charged above the basic-track cost in EVERY month of a financial year, the bank must compute the differences and enroll the customer in the basic track by 1 March of the following year, notify in writing, and allow opt-out. An unclaimed entitlement and a complaint ground when skipped.
- **NEGATIVE: no soldier / student / youth / new-immigrant fee discount exists in the fee rules.** The only population categories are senior, 40%+ disability, no-cash-withdrawal-card, and small business / osek murshe. Any bank offer to soldiers or students is a voluntary commercial benefit in its own tariff, revocable, and must never be presented as a legal right. Stating this negative explicitly is required: it is the most common false claim in this domain.
- **Recovering money already debited (Payment Services Law 5779-2019), four distinct routes, all against the BANK:** s.35(a) reverse any one debit, user deadline 3 business days, refund within 1 business day; s.37 charge exceeding the authorization (expired authorization / above permitted amount / wrong date), no user deadline, refund of the difference within 1 business day; s.38(a) unreasonably large debit, refund within 7 business days, BUT disapplied entirely by s.38(c) where the bank offered a debit ceiling and expiry at setup; s.34(c) an authorization unused for 24 months is void. Advise setting a ceiling (tikra) at setup, which converts later overruns into s.37 cases.
- **Account closure economics:** total closure fees capped at 40 NIS, a cap that explicitly includes cancelling debit authorizations and standing orders (so they may not be billed on top); 10 NIS sub-caps for securities and FX transfer on closure. Right to end the contract at any time under Payment Services Law s.6(a), but the five-business-day clock starts only once the customer completes the closure steps the contract prescribes. Closure is NOT free; niud is.
- **Identifying an authorization in practice:** banks match on the beneficiary's kod mosad plus the asmachta, not the trading name; a letter naming only the business can be refused. Fallback: beneficiary name plus last debit date and amount. s.34(a) is exercised by notice and is not conditional on the bank's own form.
- **akev acharai expiry:** the 3-year auto-forwarding window after a niud ends; the first cohort (switched 22.9.2021 to 21.9.2023) loses it from 21.9.2026 and must update employer, Bituach Leumi, and standing beneficiaries before then.
- **Ombudsman route:** Public Complaints unit at the Supervisor of Banks (yechidat pniyot hatsibur, Pikuach al HaBankim) at the Bank of Israel - free enforcement lever if a bank refuses a track switch or discount.
- **Fee-negotiation approach:** grounded in the tracks + the right to leave (niud), not US-style bluffing.
- **Deliverables:** ready-to-send Hebrew cancellation letter/request, negotiation script, short rights summary.

## Should cover (advanced)

- **Small-business reduced tariff (esek katan / taarifon muzal):** Bank of Israel is widening the small-business group the reduced tariff applies to and changing the default enrollment.
- **Expanded-plus track (maslul murchav plus):** offered by some banks, adds bank-specific services.
- **Compensation lever:** up to 10,000 NIS compensation without proof of damage if a business keeps charging after the legal cutoff.
- **General 14-day cancellation right** as a fallback for recent sign-ups.
- **Postal Bank exemption:** not obligated to offer the tracks.
- **Standardized tariff (taarifon amlot):** where to read the current per-action fee list before quoting any number.
- **2027 reform detail:** enrolment becomes automatic and opt-out; Proper Conduct of Banking Business Directive 423 is cancelled; a mid-month closure may still be billed the full month's cost; the track-related limbs of rule 4a are repealed, including the 4a(b1)/(b2) true-up. Rule 4a is amended rather than repealed in its entirety (4a(d) and (e) survive in adapted form), and the 4-teller-action entitlement does not sit in rule 4a at all: it is the note to First Schedule item 1(a)(2) and falls only because the two definitions it is written in terms of are deleted.

## Out of scope (explicit)

- Maximizing cashback, deals, or subscription perks in general - use `israeli-smart-saver`.
- Coupon and promo-code hunting - use `israeli-coupon-code-finder`.
- Analyzing or categorizing bank transactions - use `israeli-bank-connector`.
- Household budgeting and cash-flow planning - use `israeli-budget-planner`.
- Investment fees, pension/gemel management fees, mortgage rates - different domain.
- Disputing a specific fraudulent charge or chargeback dispute logic. **Re-litigated 2026-09-01 and PARTIALLY REOPENED.** An ordinary user of this skill does ask "the charge was wrong, how do I get it back", and the answer is now capturable: the Payment Services Law refund routes (s.35/37/38/34(c)) are covered above and in `references/payment-services-remedies.md`. What remains out of scope is *card* fraud and chargeback strategy proper (unauthorized card use under s.24/27, disputed merchant quality claims), which is a different domain from recurring-fee reduction. Rationale refreshed 2026-09-01.
- Investment fees, pension/gemel management fees, mortgage rates. **Re-litigated 2026-09-01, stays out of scope:** a different regulator (Rashut shuk hahon) and a different fee structure entirely; no overlap with the banking fee rules this skill is built on.
- Maximizing cashback / coupons / transaction analysis / budgeting. **Re-litigated 2026-09-01, stays out of scope:** each is an existing separate skill named in the description, and merging them would blur the trigger boundary the Phase 5.7 holdout protects.

## Authoritative sources

- Bank of Israel - fees (`boi.org.il/information/fees/`): the two tracks, transaction counts, expanded-plus, calculator, small-business reduced tariff.
- Bank of Israel - fee-tracks calculator (`boi.org.il/information/מחשבונים-וכלים/עמלות/`).
- Kol Zchut - fixed monthly fee tracks: transaction counts, price caps/ranges, senior/disability discounts, switch timing, Postal Bank exemption.
- Kol Zchut - one-click bank switching / niud (`מעבר_בין_בנקים_באופן_מקוון_(ניוד)`): 7-business-day online move, what transfers, akev acharai, free, effective 22.9.2021.
- Kol Zchut - overdraft / chariga mimisgeret (`חריגה_ממסגרת_אשראי_בחשבון_עובר_ושב`): higher interest on a current-account overdraft.
- Kol Zchut - cancelling an ongoing transaction (`ביטול_עסקה_מתמשכת`): 3/6 business-day stop rule, 10,000 NIS compensation, 14-day general right.
- Payment Services Law, 5779-2019, section 34 (Nevo `502_043.htm`): cancel debit authorization at any time.
- Banking (Customer Service) Law, 5741-1981 (Nevo `047_016.htm`): parent consumer-banking law.
- Debit Cards Law, 5746-1986 (Wikisource): governs credit/debit cards.
