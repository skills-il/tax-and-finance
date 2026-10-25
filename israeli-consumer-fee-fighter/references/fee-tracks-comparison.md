# Bank fee tracks comparison (Israel)

Fee amounts change; always confirm against the bank's current tariff (taarifon amlot), which controls. The Bank of Israel fee-tracks calculator is useful for comparing banks, but its stored bank prices are dated on its page and can be years old.

## The three ways an Israeli account is billed for עמלות

| Billing method | What it means | Direct-channel actions | Teller actions | Monthly price |
|---|---|---|---|---|
| **No track (per action)** | Default. Charged a separate fee for every action. | pay per action | pay per action | varies; compute from the user's own statement |
| **Basic track (maslul basi)** | Fixed monthly price, supervised. | up to 10 / month | up to 1 / month | supervised, max 10 NIS |
| **Expanded track (maslul murchav)** | Fixed monthly price, price-supervised since 1.9.2022. | up to 50 / month | up to 10 / month | supervised; read the bank's current tariff |
| **Expanded-plus (maslul murchav plus)** | Some banks only. Expanded track + bank-specific extras. | expanded + extras | expanded + extras | bank-specific |

Notes:
- A "direct-channel action" (peula be'aruts yashir) is defined by a LIST, not by channel (First Schedule item 1(a)(3)): (1) a credit to the account through the clearing house (salary, pension, Bituach Leumi), (2) a credit-card debit to the account, (3) a cash deposit and (4) an ATM withdrawal by machine, (5) a transfer or deposit to another account, (6) a voucher payment, (7) an information query from the 7th in the month, (8) a cheque drawn, (9) a cheque deposit, (10) a debit under an authorization or standing order. Information queries by internet or IVR and immediate-debit card purchases are not charged and do not count toward a track.
- A "teller action" (peulat pakid) is one of the item 1(a)(2) actions done by a clerk, including via a staffed phone line.
- If the bank offers no reasonable direct channel for cheque or cash deposits, those deposits are capped at the direct-channel price when billed per action (item 1(a)(2) note 2) and count as direct-channel actions inside a track (basic-track note 3). Enter them as `--direct`.
- Legal anchor: Banking Rules (Customer Service)(Fees), 5768-2008, section 4a. Obligation in force since 1.4.14.
- The Postal Bank is not obligated to offer these tracks.

## Decision rule (which method is cheapest)

1. Count your typical monthly actions, split into direct-channel and teller. Read them off recent account statements or ask the bank. Then cut the count before re-pricing it: each action moved from a clerk to the app or ATM is billed at the direct-channel price instead of the teller price.
2. **Establish eligibility for the teller entitlement BEFORE comparing anything**, because it changes all three methods at once rather than adding a fourth option. Three categories qualify: a senior (azrach vatik), a customer who has presented a 40%+ disability certificate, and a customer who holds no cash-withdrawal card. What they get is **4 teller actions a month priced at the direct-channel rate**, under the note to First Schedule item 1(a)(2).
   - It is **not a percentage discount.** There is no published percentage and no published shekel figure. Do not invent one, and treat any percentage a bank quotes as its own voluntary offer rather than the regulated entitlement.
   - It is **not an alternative to joining a track.** It reprices teller actions wherever they are billed per action under item 1(a)(2), which means both when on no track and on a track's teller OVERAGE. It does not discount the fixed track price, and it does nothing for teller actions already inside a track's allowance.
   - Pass `--entitled` to `scripts/fee_track_calculator.py`; it applies the entitlement to all three methods. Do not reason about it by hand.
3. If your monthly volume is small (roughly a handful of direct actions, at most one teller action), the **basic track** or even **no track** is usually cheapest. On no track the bank may charge the higher of the per-action total or a monthly minimum of up to one teller action's price (note 3 to item 1(a)(2)), so pass that minimum to the calculator as `--min-fee`.
4. If you run many actions (dozens of direct actions and/or several teller actions), the **expanded track** usually wins over paying per action.
5. Compare banks in the **Bank of Israel fee-tracks calculator**, but check the date its prices were last updated; the bank's own tariff controls.
6. A business account: a **small business (esek katan)** may not be charged more for a tariff service than a larger corporation, except card-clearing (acquiring) fees (rule 2(b)), and is covered by the rule 4a(b2) true-up.

## Switching

- Notify the bank via its website, phone center, or a branch.
- The switch takes effect on the **1st of the month after** the month in which you gave notice.
- Billing for a track is monthly, at the start of each month, for the previous month. If the customer switches the account out or closes it mid-month, the bank may charge the full monthly track cost for that month (basic-track note 4).

## Switching banks entirely (niud / maavar beklik)

- If the whole bank is expensive, a track switch is not enough. Since 22.9.2021 you can move the entire account to a cheaper bank through a free, fully online switch that completes within 7 business days.
- It transfers shekel and foreign-currency balances, standing orders (horaot keva) and current-account authorizations, checks, transferable securities, and bank + non-bank credit-card activity.
- It does NOT transfer loans and credit including mortgages, deposits and savings plans, non-transferable securities, or safes and products pledged to the old bank. Each needs a separate arrangement with the previous bank.
- The switch completes within 7 business days of submission, extendable to 30 business days on request. The akev acharai (follow-me) forwarding runs for 3 years from the switch, extended to 31.7.2029 for anyone who switched before 21.9.2026 (transitional rule 5א of the bank-switching rules). Bank of Jerusalem customers cannot use the online switch.
- Because niud moves the standing orders for you, you do not re-set-up each authorization by hand; authorizations on a card the old bank issued move too (rule 3(8)), but any merchant that stored a card number needs the new number once that card is replaced.

## What this does NOT change

- Choosing a track only covers the basic current-account actions it lists. Other fees (overdraft interest, foreign currency, securities, special services) stay per the tariff, but are negotiable as separate targets.
- A track does not cancel any standing debit authorizations (harshaa lechiyuv / horaat keva) - those sit on the account and are cancelled separately at the bank.
