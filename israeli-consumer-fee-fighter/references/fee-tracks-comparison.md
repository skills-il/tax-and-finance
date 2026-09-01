# Bank fee tracks comparison (Israel)

All figures verified against the Bank of Israel fees page and Kol Zchut. Fee amounts change; always confirm against the current tariff (taarifon amlot) and the Bank of Israel fee-tracks calculator before quoting a number to a user.

## The three ways an Israeli account is billed for עמלות

| Billing method | What it means | Direct-channel actions | Teller actions | Monthly price |
|---|---|---|---|---|
| **No track (per action)** | Default. Charged a separate fee for every action. | pay per action | pay per action | varies; compute from the user's own statement |
| **Basic track (maslul basi)** | Fixed monthly price, supervised. | up to 10 / month | up to 1 / month | supervised, max 10 NIS |
| **Expanded track (maslul murchav)** | Fixed monthly price, price-supervised since 1.9.2022. | up to 50 / month | up to 10 / month | supervised; read the bank's current tariff |
| **Expanded-plus (maslul murchav plus)** | Some banks only. Expanded track + bank-specific extras. | expanded + extras | expanded + extras | bank-specific |

Notes:
- A "direct-channel action" (peula be'aruts yashir) is anything not done by a teller: internet, app, ATM, terminals, standing orders, etc.
- A "teller action" (peulat pakid) is a deposit, withdrawal, transfer, or other action performed by a bank clerk.
- Legal anchor: Banking Rules (Customer Service)(Fees), 5768-2008, section 4a. Obligation in force since 1.4.14.
- The Postal Bank is not obligated to offer these tracks.

## Decision rule (which method is cheapest)

1. Count your typical monthly actions, split into direct-channel and teller. Read them off recent account statements or ask the bank.
2. **Establish eligibility for the teller entitlement BEFORE comparing anything**, because it changes all three methods at once rather than adding a fourth option. Three categories qualify: a senior (azrach vatik), a customer who has presented a 40%+ disability certificate, and a customer who holds no cash-withdrawal card. What they get is **4 teller actions a month priced at the direct-channel rate**, under the note to First Schedule item 1(a)(2).
   - It is **not a percentage discount.** There is no published percentage and no published shekel figure. Do not invent one, and treat any percentage a bank quotes as its own voluntary offer rather than the regulated entitlement.
   - It is **not an alternative to joining a track.** It reprices teller actions wherever they are billed per action under item 1(a)(2), which means both when on no track and on a track's teller OVERAGE. It does not discount the fixed track price, and it does nothing for teller actions already inside a track's allowance.
   - Pass `--entitled` to `scripts/fee_track_calculator.py`; it applies the entitlement to all three methods. Do not reason about it by hand.
3. If your monthly volume is small (roughly a handful of direct actions, at most one teller action), the **basic track** or even **no track** is usually cheapest.
4. If you run many actions (dozens of direct actions and/or several teller actions), the **expanded track** usually wins over paying per action.
5. Run the exact numbers in the **Bank of Israel fee-tracks calculator** - it compares your action count against every bank's prices.
6. A business account: check whether you qualify as a **small business (esek katan)** for the reduced tariff.

## Switching

- Notify the bank via its website, phone center, or a branch.
- The switch takes effect on the **1st of the month after** the month in which you gave notice.
- Billing for a track is monthly, at the start of each month, for the previous month.

## Switching banks entirely (niud / maavar beklik)

- If the whole bank is expensive, a track switch is not enough. Since 22.9.2021 you can move the entire account to a cheaper bank through a free, fully online switch that completes within 7 business days.
- It transfers shekel and foreign-currency balances, standing orders (horaot keva) and current-account authorizations, checks, transferable securities, and bank + non-bank credit-card activity.
- It does NOT transfer loans and credit including mortgages, deposits and savings plans, non-transferable securities, or safes and products pledged to the old bank. Each needs a separate arrangement with the previous bank.
- The switch completes within 7 business days of submission, extendable to 30 business days on request. The akev acharai (follow-me) forwarding runs for 3 years. Bank of Jerusalem customers cannot use the online switch.
- Because niud moves the standing orders for you, you do not re-set-up each authorization by hand; only card-billed subscriptions (which follow the card, not the account) must be updated with each merchant.

## What this does NOT change

- Choosing a track only covers the basic current-account actions it lists. Other fees (overdraft interest, foreign currency, securities, special services) stay per the tariff, but are negotiable as separate targets.
- A track does not cancel any standing debit authorizations (harshaa lechiyuv / horaat keva) - those sit on the account and are cancelled separately at the bank.
