---
name: pelecard-payment-gateway
description: "Integrate Pelecard payment processing into Israeli web and mobile apps -- covers the iframe payment flow on gateway21.pelecard.biz, ActionType selection (J2/J4/J5/J5h), tashlumim (installments), tokenization, ConfirmationKey server-side validation via PaymentGW/GetTransaction, refunds, 3D Secure 2, Bit wallet, and Apple Pay via ClientSecure.js. Use when user asks to accept payments via Pelecard, set up slikat ashrai with Pelecard, validate a Pelecard callback, charge a saved Pelecard token, or mentions Pelecard, gateway21, PelecardStatusCode, or ConfirmationKey. Do NOT use for Cardcom (use cardcom-payment-gateway), Tranzila (use tranzila-payment-gateway), Grow/Meshulam (use grow-payment-gateway), multi-gateway orchestration (use israeli-payment-orchestrator), or invoice generation (use green-invoice)."
license: MIT
compatibility: Requires network access for Pelecard API calls. Works with Claude Code, Cursor, Claude Desktop, OpenAI Codex, and GitHub Copilot.
version: 1.1.0
---

# Pelecard Payment Gateway

## Problem

Pelecard is a Payment Service Provider (PSP) that aggregates Israeli merchants onto the card acquirers over Shva, but its public documentation is scattered across a Postman workspace, a sandbox UI, a WordPress plugin listing and third-party PHP libraries, with no single canonical reference. Agents integrating Pelecard end up treating the hostname as an environment switch (it is not), inventing a refund endpoint that does not exist, picking the wrong `ActionType` (which silently changes whether money moves), or trusting a browser-side `ConfirmationKey` instead of re-verifying server-side. Each mistake leaks revenue or ships an exploitable "free order" path.

## Overview

Card transactions clear on the Israeli Shva network (https://www.shva.co.il/, שב"א); Pelecard handles merchant onboarding, the iframe surface, tokenization and reconciliation on top. Your acquirer, not Pelecard, answers the PCI-tier and broadcast-policy questions below.

Pelecard's dominant integration is an iframe payment page: your server posts a credentials triple (`terminal` + `user` + `password`) plus the transaction parameters, gets back a `URL` and a `ConfirmationKey`, and redirects or embeds it. After the customer pays, Pelecard calls your server-side feedback URL. Store the Phase-1 `ConfirmationKey` keyed by your order; on the callback you MUST (a) match it byte-for-byte and (b) re-call `PaymentGW/GetTransaction` before treating the order as paid.

Pelecard has **two** server-to-server surfaces with different parameter-naming conventions.
`/PaymentGW/*` is the iframe surface and has exactly three endpoints. `/services/*` is where every
other operation lives: charges on a saved token, authorizations, voids, tokens, lookups, settlement,
3DS, invoices. Pelecard publishes a live request builder for them at
https://gateway21.pelecard.biz/services with a preset body for each; that page is the authoritative
endpoint reference, ahead of any third-party wrapper.

The newer "Match API" at `match-api.pelecard.biz` exists, but its docs page still returns an empty
client-side shell (HTTP 200, ~37 characters of text as of 2026-08-27). Verify with Pelecard first.

## Instructions

### Step 1: Choose Integration Pattern

| Pattern | Card Data Handling | Best For |
|---------|-------------------|----------|
| **Iframe / hosted page** | Pelecard hosts the card-entry page | Most integrations; smallest PCI scope |
| **Charge stored token** (`/services`) | Token only, no raw card data | Recurring billing, hora'ot keva, one-click |
| **Apple Pay via ClientSecure.js** | Apple Pay handles card data | iOS/Safari customers |
| **Bit wallet** | A2A push, no card data | Single-payment, ILS only, 5,000 ₪ design ceiling |
| **Server-to-server** (`/services/*`) | Token, or a PAN you handle | Authorizations, voids, reconciliation. A PAN raises your PCI scope. |
| **Match API** | Modern REST surface | Verify with vendor; doc page still renders empty |

### Step 2: Set Up Authentication

Every Pelecard call needs a credentials triple, sent server-side only:

- `terminal` -- your terminal ID issued by Pelecard
- `user` -- API username
- `password` -- API password

These three values open your terminal to charges. They MUST live in server-side environment variables. Never embed them in browser JavaScript, mobile app bundles, or git history.

**The hostname is not an environment switch.** `gateway20.pelecard.biz` and
`gateway21.pelecard.biz` serve the same API: both answer `PaymentGW/init`,
`PaymentGW/GetTransaction` and `PaymentGW/ValidateByUniqueKey` identically, and a 404 on gateway21
redirects to an error page on gateway20. `gateway21` is the current gateway generation and
`gateway20` the older one; `gateway20.pelecard.biz/sandbox` is a sandbox **UI page**, not a
separate API host.

What decides whether a call is a test or a real charge is **the terminal number and credentials you
send**, not the host. Ask Pelecard which host your test terminal was issued on, keep host + terminal +
credentials in one config object you swap as a unit, and never write code that infers "this is safe"
from a hostname: a build pointed at `gateway20` with live credentials is a live charge. Post to
`gateway21.pelecard.biz` unless Pelecard tells you otherwise.

### Step 3: Create the Iframe Payment Page

Build the request body from your credentials, `Total`, `Currency`, `ActionType` and the feedback URLs.

**Money fields use minor units (agorot).** Send `Total: 9900` for ₪99.00. Two independent confirmations: the dofinity wrapper documents `FirstPayment` as "the amount is in agorot/cents", and Pelecard's own builder sends the same 1 shekel as `total: "100"` on `/services/DebitRegularType` and as `TotalX100: "100"` on `ValidateByUniqueKey`. Still do a 1 ₪ test charge before going live.

The create-session path is `PaymentGW/init`, verified live on both gateway hosts.

```
POST https://gateway21.pelecard.biz/PaymentGW/init
Content-Type: application/json

{
  "terminal": "<your-terminal>",
  "user": "<api-user>",
  "password": "<api-password>",
  "ActionType": "J4",
  "Currency": 1,
  "Total": 9900,
  "MaxPayments": 12,
  "MinPayments": 1,
  "GoodURL": "https://example.com/pay/success",
  "ErrorURL": "https://example.com/pay/error",
  "CancelURL": "https://example.com/pay/cancel",
  "ServerSideGoodFeedbackURL": "https://example.com/api/pelecard/ipn-success",
  "ServerSideErrorFeedbackURL": "https://example.com/api/pelecard/ipn-error",
  "ParamX": "order-2026-0042",
  "ShopNo": "main-shop",
  "CreateToken": true
}
```

On success Pelecard responds with a `URL` and a `ConfirmationKey`. **Persist the
`ConfirmationKey` server-side keyed by your order** (you will compare it on the callback in Step 4).
Then redirect the customer to that URL or embed it as an iframe.

**A failed `init` still returns HTTP 200**, as the same two fields blank plus an `Error` object:

```json
{"URL":"","ConfirmationKey":"","Error":{"ErrCode":501,"ErrMsg":"Login for user x failed"}}
```

Check `Error.ErrCode` before using `URL`; treating HTTP 200 as success renders a blank iframe with no
diagnostic. Resolve the code via `/services/GetErrorMessageEn` (Step 8).

**`init` does not return a transaction id.** There is no transaction until the customer transacts, so
correlate on the `ParamX` you sent, not on an id you do not have.

**ActionType reference (full table in `references/payment-parameters.md`):**

| Value | Meaning |
|-------|---------|
| `J4` | Standard sale (default). Money moves now. |
| `J2` | Card validation / registration only. No charge. |
| `J5` | Authorize now, charge later. |
| `J5h` | Enhanced J5. |

### Step 4: Validate the Callback Server-Side

When the customer finishes paying, Pelecard hits your `ServerSideGoodFeedbackURL` with a `PelecardStatusCode`, `ConfirmationKey`, and `PelecardTransactionId`. Before you treat the order as paid, you MUST do all of the following server-side:

1. Compare your stored Phase-1 `ConfirmationKey` byte-for-byte to the callback value. No match, refuse the payment.
2. Re-call `PaymentGW/GetTransaction` with `terminal/user/password/TransactionId` (the callback's `PelecardTransactionId`).
3. Confirm the debited amount matches the order's expected price and the transaction id matches the callback. `GetTransaction` does not return the `ConfirmationKey`, so this amount/id match is what authenticates the lookup.

**Pelecard does NOT sign IPN deliveries with HMAC.** A browser-side `ConfirmationKey` can be forged, so the only authoritative source is the server-to-server `GetTransaction` lookup.

The lookup call is the credentials triple plus the `TransactionId`:

```
POST https://gateway21.pelecard.biz/PaymentGW/GetTransaction
{
  "terminal": "<terminal>",
  "user": "<user>",
  "password": "<password>",
  "TransactionId": "<PelecardTransactionId from callback>"
}
```

The response is **not flat**. It is `{"StatusCode":"...","ErrorMessage":"...","ResultData":{...}}`.
Read `StatusCode` first (`"000"` = success), then take the transaction fields from inside
`ResultData`: the authoritative debited amount, the Shva approval number, the installment count,
masked card last 4, expiry, and your `ParamX` echoed back. Compare the debited amount against the
order's expected price; a mismatch means tampering, so do NOT mark the order paid.

**Inbound dedupe.** Pelecard may legitimately deliver the same IPN twice (timeout retry; plugin v1.5.1: "Fixed timeout-retry issues"). Dedupe on **`PelecardTransactionId`**, unique per attempt, not on `ParamX`, which is your order id and repeats across deliveries.

**Reconciliation safety net.** The server-side feedback URL fires only when the transaction reaches
a terminal state. If the customer closes the browser mid-flow, no IPN fires. Three status codes
describe a broken merchant leg, and they do **not** mean the same thing:

| Code | Pelecard's own wording | What it tells you about the money |
|---|---|---|
| `302` | "Debit was successful but merchant is not responding" | The debit **succeeded**. Look it up, then mark paid. |
| `301` | "Session to Pelecard Timed Out" | **Outcome unknown**, and most likely no debit at all. |
| `303` | "Merchant is not responding" | **Outcome unknown.** Says nothing about the debit. |

Only `302` asserts that money moved. Treat `301` and `303` as unresolved until a lookup settles them.

In all three cases you have no `PelecardTransactionId`, and `init` never gave you one. Reconcile on a
key you own:

- `POST /services/CheckGoodParamX` with your `paramX` and `shvaSuccessOnly` answers "was this order
  actually paid?" directly. `/services/CheckGoodParamXList` does it in a batch.
- `POST /services/TrxLookUp` with `paramX` returns the transaction.

`PaymentGW/ValidateByUniqueKey` also validates without credentials, but it keys on a `UniqueKey` and
this skill has **not** established which `init` parameter sets one (the documented passthrough fields
are `ParamX`, `ShopNo`, `UserKey`, `UserData1`-`15`). Don't build a safety net on it unless Pelecard
confirms how your terminal accepts a merchant-supplied `UniqueKey`. `paramX` is the key this skill can
actually show you how to send.

Run a lookup on a schedule for every session with no IPN inside your timeout window. **Never re-charge
to resolve an unknown outcome; look it up first.**

**Outbound idempotency (the double-charge you will otherwise ship).** All of the above is *inbound*
dedupe. When a token charge times out at the socket you do not know whether it landed, so `paramX` has
to do double duty: make it `<order-id>-<attempt-n>` and reconcile with a prefix match on `<order-id>`,
so `CheckGoodParamX` can still answer "was this order paid". (`userKey` is **not** available on the
debit endpoints; in Pelecard's builder it appears only on the `Pending*Type` family and
`ClearPendingByUserKey`.) Look the attempt up before retrying. Pelecard rejects some repeats with `308`
"Duplicated transaction." or `425` "Double entry" -- proof your retry fired twice, not a transient
error to retry again.

Run the bundled `scripts/validate_pelecard_response.py` against your callback while developing. It is a shape check, not a security gate: it cannot know your expected order amount and never verifies the transaction, so a passing result still requires both checks above. With the opt-in `--resolve-codes` flag it POSTs only the numeric status code to Pelecard's public code lookup; no callback content leaves your machine.

### Step 5: Charge a Stored Token (Recurring Billing)

The first transaction sets `CreateToken: true` on the iframe request and Pelecard stores the token
against `TokenForTerminal`. Save the token, the card last-4 and the expiry.

**Renewals are a `/services` call, not an iframe parameter.** Post to
`/services/DebitRegularType` with the saved `token` **instead of** `creditCard`:

```
POST https://gateway21.pelecard.biz/services/DebitRegularType
{
  "terminalNumber": "<terminal>", "user": "<user>", "password": "<password>",
  "shopNumber": "001", "token": "<saved-token>", "creditCardDateMmYy": "1230",
  "total": "9900", "currency": "1", "paramX": "sub-2026-08-0042"
}
```

Note the casing: `terminalNumber` / `total` / `currency` / `paramX` on `/services`, versus
`terminal` / `Total` / `Currency` / `ParamX` on `/PaymentGW`. Sending the `/PaymentGW` names to a
`/services` endpoint is the most common silent failure here. Use `/services/DebitPaymentsType`
(adds `paymentsNumber`, `firstPayment`) when the renewal is in installments.

**Maintain the token, don't just create it.** Cards get reissued and expiries roll, so
`/services/UpdateToken` (plus `ConvertToToken`, `RetrieveToken`, `CheckCreditCardForToken`, all in
`references/api-endpoints.md`) is what keeps a subscriber. Status `506` "Token number abnormal."
means the stored token is no longer chargeable: re-tokenize or `UpdateToken`, never retry it. The Pelecard WordPress plugin has shipped "Saved payment
methods (tokenization)" since v1.2.0 and "WooCommerce Subscriptions support" since v1.4.

**Recurring charges + 3DS (MIT exemption).** Under EMV 3DS 2.x, repeat charges on a stored token can qualify for the MIT (Merchant Initiated Transaction) exemption, meaning Shva will not step the customer up for a 3DS challenge on each renewal. Pelecard's plugin changelog references this pattern (v1.4.8: "Add 3D-Secure params to J4 after J5 requests"). Confirm the exact MIT-flag parameter for your terminal with Pelecard support before relying on the exemption; without it, recurring charges may intermittently fail with 3DS rejection errors.

### Step 6: Process Refunds

**There is no single "refund" endpoint, and there is no refund endpoint under `/PaymentGW` at all.**
Which primitive applies depends on whether the transaction has already been broadcast to Shva
(see Step 6b). This is the ביטול / זיכוי distinction, and getting it wrong is the most expensive
routine mistake in Israeli card integration.

| Situation | Operation | Endpoint | What the customer sees |
|---|---|---|---|
| Not yet broadcast (still in the open batch) | **Void / ביטול** -- delete the transaction | `/services/DeleteTran` (by `debitTrxId`, `uid`, or `voucherId` + `creditCard` + `total`) | The transaction never settles. A pending line may already have appeared in their card app at authorization time and can take days to drop off, so do not promise them they will see nothing. |
| An authorization you will not capture | **Release the hold** | `/services/DeleteIshur` (by `debitTrxId`) | Their credit line is freed |
| Already broadcast | **Credit / זיכוי** -- a new, opposite transaction | **not documented here, see the warning below** | A second line on their statement, settling on the issuer's own cycle |

Prefer the void whenever it is still available. A void never settles, so you pay no clearing fee; a
זיכוי is itself a cleared transaction, so you pay a fee on the credit leg and generally do not get the
original charge's fee back, meaning a sloppy charge-then-refund is paid for twice. The void is normally
only available while the batch is open, on most terminals the same business day, so timing is the whole
game. `/services/GetTransDataBeforeBc` shows what is still voidable.

**The post-broadcast credit path is NOT documented in this skill, and you must not guess it.** No
`/services` endpoint in Pelecard's public builder is a card-not-present credit operation
(`DebitCreditType` is a *tashlumim kredit* sale; `EmvReversal` is card-present hardware), and no
preset exposes a negative `total` or a credit flag. Get the credit path for your terminal from
Pelecard **before you accept your first payment**, because the Consumer Protection Law clock below
starts without waiting for you. Never try a negative `total` on a debit endpoint: if the terminal
accepts it at all, the likely result is a second charge.

**Israeli consumer protection law (חוק הגנת הצרכן, סעיפים 14ג-14ה)** governs distance-selling refunds: consumers may cancel within 14 days, the merchant must refund within 14 days of the cancellation notice, and cancellation fees are capped at 5% of the order value or 100 ₪, whichever is lower. **Do not hard-code 14 days as the whole rule:** customers who are people with disabilities, aged 65 or over, or new immigrants may cancel within **4 months** where a conversation took place during the sale, and some service categories have their own shorter windows. Treat the above as a summary, not the full statute. A זיכוי settles on the issuer's cycle, so the money can reach the customer well after you issue it; the 14-day duty is on your issuing it. (Source: kolzchut, Consumer Protection Law remote-sales chapter.)

### Step 6b: Broadcast (שידור) -- an approval is not money

An approved transaction holding an approval number is an authorization sitting in your terminal's
open batch. It becomes a claim on the issuer only when the terminal **broadcasts** to Shva. Until
then it is not settled and still voidable.

`/services/Broadcast` (credentials only) triggers it, `/services/GetBroadcast` and
`GetBroadcastsByDate` report status, `/services/GetTransDataBeforeBc` lists what has not gone yet.

Terminals differ on whether broadcast is automatic or merchant-triggered. **Find out which yours is.**
A terminal that quietly stops broadcasting accumulates approved-but-unsettled transactions while your
database says "paid", surfacing only when you reconcile against bank deposits. Alert on anything in
`GetTransDataBeforeBc` older than one broadcast cycle.

### Step 7: Configure 3D Secure 2 and Bit

**3D Secure 2 (EMV 3DS).** On the iframe surface the sandbox UI exposes `Initiate` and
`AskForChallenge` toggles (each: `None` default, `False`, `True`), and Pelecard runs the
authentication for you.

On the server-to-server surface 3DS2 is an **ordered sequence**, not a flag:

1. `POST /Services/Initiate3DSAuthenticationProcess` with the amount, currency, card or `Token`,
   cardholder details, your `RedirectUrl`, and the browser fingerprint fields listed in
   `references/api-endpoints.md`.
2. The customer is either authenticated without interaction (frictionless) or challenged at your
   `RedirectUrl`.
3. Submit the debit **carrying the authentication result**: `/services/DebitRegularType` takes
   `eci`, `xid` and `cavv` for exactly this purpose.

Skipping step 3 wastes the authentication and forfeits the liability shift. Status `650` is
"3DS process failed". The Pelecard plugin v1.4.19 changelog notes "Added Emv errors in order notes.
ShvaResultEmv parameter" -- log `ShvaResultEmv` whenever it appears.

**Bit wallet.** Bit is a Bank-of-Israel-approved A2A wallet. Constraints to bake into the UX:

- **Single payment only.** From allpay.co.il: "No installments. You can only pay with Bit in one payment." Hide the tashlumim selector when Bit is the chosen method.
- **ILS only.** Bit only accepts shekels. Send `Currency: 1` for any Bit transaction; non-ILS Bit transactions fail with no helpful error.
- **Per-transaction cap is operator-set.** The commonly-cited limit is 5,000 ₪ (allpay.co.il: "Payment via Bit cannot exceed 5,000 shekels"), but higher-tier merchants are cleared above it. Treat 5,000 ₪ as the design ceiling unless you have written approval otherwise.
- **Bit is A2A, so the void/credit machinery in Step 6 does not apply the same way.** Confirm the Bit refund and reconciliation path with Pelecard before enabling it.
- Bit also imposes a 20,000 ₪ per-merchant monthly cap and a 10-minute customer window (allpay.co.il).

**Apple Pay.** Pelecard hosts the SDK at `ClientSecure.js`, loaded into your own checkout page (see Step 9 on PCI scope). The plugin lists it as "optional, disabled by default".

### Step 8: Handle Errors

Pelecard returns a numeric status code everywhere: `PelecardStatusCode` on the callback,
`StatusCode` on a `GetTransaction` response, `Error.ErrCode` on a failed `init`. `000` is success.

**Do not hard-code a hand-written mapping, and do not tell users to email support.** Pelecard
publishes the official message for every code through two endpoints that need **no credentials**:

```
POST https://gateway21.pelecard.biz/services/GetErrorMessageEn
POST https://gateway21.pelecard.biz/services/GetErrorMessageHe
{"ErrorCode": "033"}      ->  invalid credit card.  /  כרטיס לא תקין.
```

Because `GetErrorMessageHe` is credential-free, wire it directly into your failure path to show the
customer a real Hebrew decline message instead of a number. Cache the responses; the table is
stable.

`references/error-codes.md` carries the full enumerated table (254 assigned codes, both languages,
swept 2026-08-27) plus a retry policy, including the merchant-unreachable codes `301` / `302` / `303`
and which of them actually means money moved. EMV / 3DS results ride alongside in
`ShvaResultEmv`, a separate code space.

### Step 9: Keep your PCI scope where you think it is

The iframe pattern keeps card data off your servers, which is why it is the default recommendation
here. Two things in this skill quietly move that line, so decide deliberately:

- **Any `/services` call sending `creditCard` puts a PAN through your systems** (typically SAQ D). A
  saved `token` does not. Prefer the token.
- **Apple Pay via `ClientSecure.js` loads a Pelecard script into your own checkout page.** A pure
  redirect/iframe merchant is normally SAQ A; a merchant page hosting a payment script is normally
  SAQ A-EP. Your acquirer decides; those names are the shape of the question to ask them.

Two logging rules follow from the rest of this skill. **Do not log `ConfirmationKey`** -- Step 4's
entire verification scheme rests on an attacker not knowing it, and a log aggregator is not a secret
store; log a hash if you need to correlate. **Do not log `CardHolderID`** (te'udat zehut) in
plaintext; it is personal data under the Privacy Protection Law (Amendment 13) and carries retention
duties your log pipeline probably does not meet.

## Examples

### Example 1: First-Time Iframe Checkout
User says: "I want to accept credit-card payments on my Israeli site via Pelecard, with up to 12 tashlumim."
Actions:
1. Server: POST credentials + `ActionType: J4` + `Total: 9900` (₪99.00 in agorot) + `Currency: 1` + `MaxPayments: 12` to `PaymentGW/init`. Check `Error.ErrCode` before using the returned `URL`.
2. Persist the `ConfirmationKey` keyed by your order. Render the `URL` in an iframe (or redirect).
3. Listen on `ServerSideGoodFeedbackURL`, and run a `CheckGoodParamX` sweep for sessions that never call back.
4. Compare the callback `ConfirmationKey` to your stored value, then re-verify via `PaymentGW/GetTransaction` and confirm the debited amount before marking the order paid.
Result: Customer pays in 1-12 tashlumim, against a verified transaction.

### Example 2: Save a Card and Charge It Monthly
User says: "I run a SaaS, I need to charge users 99 ₪ every month with their saved card."
Actions:
1. First payment: iframe POST with `CreateToken: true` and `Total: 9900` (agorot). Save the token, last-4 and expiry.
2. Monthly cron: POST `/services/DebitRegularType` with `token`, `total`, `currency` and a `paramX` of `<order>-<attempt>`.
3. Verify each charge, dedupe inbound IPNs on `PelecardTransactionId`, and on any timeout look the attempt up before retrying.
4. Handle declines via the code table, and refresh reissued cards with `/services/UpdateToken`. Ask Pelecard about MIT-flag parameters so Shva does not challenge each cycle.
Result: Recurring billing without storing a single PAN on your servers.

### Example 3: Add Bit as a Checkout Option
User says: "Most of my Israeli customers want Bit, can I add it?"
Actions:
1. Enable Bit on the Pelecard terminal (vendor-side configuration).
2. Send `Currency: 1` and gate Bit to `Total <= 5,000 ₪` unless your Bit agreement clears you higher.
3. Hide the tashlumim selector when Bit is chosen; Bit is single-payment only.
4. Same callback flow. Settle the Bit refund path with Pelecard before launch, not after.
Result: Bit added cleanly, no failed charges from wallet-side constraints.

### Example 4: Validate a Callback Payload Locally
User says: "My Pelecard callback came in, how do I sanity-check it before hitting GetTransaction?"
Actions:
1. Run `python scripts/validate_pelecard_response.py --resolve-codes --response '{"PelecardStatusCode":"000","ConfirmationKey":"...","PelecardTransactionId":"...","Total":9900,"Currency":1}'`.
2. It flags a missing `ConfirmationKey` or `PelecardTransactionId`, requires the canonical `"000"`, and resolves any failing code to Pelecard's own bilingual message. `--explain 033` looks a code up on its own.
3. If it passes, do the two real checks: stored-vs-callback `ConfirmationKey`, then `PaymentGW/GetTransaction` for the debited amount.
Result: Quick local check before hitting the Pelecard API.

### Example 5: Authorize Now, Charge on Shipment (J5)
User says: "I want to authorize the customer's card at order time but only charge when I ship -- like Amazon."
Actions:
1. **Before writing any of this, get the capture contract from Pelecard.** This skill verified that
   `authorizationNumber` is a parameter on every `/services` debit type, but did **not** verify that
   posting a debit with it captures the prior hold rather than starting a fresh authorization and
   charge. If your terminal is not provisioned for the pairing, the customer is charged twice.
2. First call: `ActionType: J5` **with `CreateToken: true`**. `/services/DebitRegularType` requires a
   `creditCard` or a `token`, and an iframe J5 without `CreateToken` leaves you with neither, so the
   hold becomes uncapturable. Persist the token, and the authorization number from the IPN /
   `GetTransaction` `ResultData` (it is not in the `init` response).
3. On shipment, post `/services/DebitRegularType` with the saved `token`, the amount, and the
   `authorizationNumber`, per the contract you confirmed in step 1.
4. If you decide NOT to ship, release the hold with `/services/DeleteIshur` so the customer's credit
   line is freed. An abandoned hold is a support ticket.
5. Verify the captured transaction via `PaymentGW/GetTransaction`, and confirm it broadcasts.
Result: Auth-then-capture pattern compatible with Israeli e-commerce flows.

### Example 6: Refund a Failed Order
User says: "Customer disputed order #5678, I need to refund."
Actions:
1. Pull the original `PelecardTransactionId` from your order record (you stored it from Phase 1 / IPN).
2. Check whether it has been broadcast (`/services/GetTransDataBeforeBc`). If it is still in the
   open batch, **void** it with `/services/DeleteTran`: it never settles, so no clearing fee. A
   pending line may still be visible in the customer's card app for a while, so don't promise
   otherwise. If it has already been broadcast you need a **credit**, and the credit path is not
   documented here (Step 6) -- get it from Pelecard rather than guessing.
3. Persist the identifier of the void or credit leg against the original order.
4. Honor the Israeli Consumer Protection Law deadlines: 14 days to refund from the cancellation notice, fee capped at 5% or 100 ₪ (whichever is lower).
5. Issue the credit note (חשבונית זיכוי) via your invoice provider, or via Pelecard's own `/services/CreateInvoice` family.
Result: Refund processed within the legal window.

## Bundled Resources

### References
- `references/api-endpoints.md` -- The verified endpoint catalogue: host model, the three `/PaymentGW` endpoints with their real response envelopes, and the `/services` surface (charge, authorize, void, tokens, lookup, broadcast, 3DS, invoices) with parameter names.
- `references/payment-parameters.md` -- The iframe (`PaymentGW/init`) parameter reference: ActionType, Currency, tashlumim, tokenization, BIN controls, UI customization, feedback URLs, passthrough fields.
- `references/error-codes.md` -- The full status-code table (254 assigned codes, English + Hebrew, swept from Pelecard's credential-free lookup), plus a retry policy and the EMV/Shva note.

### Scripts
- `scripts/validate_pelecard_response.py` -- Shape-checks a Pelecard callback JSON and, with `--resolve-codes`, resolves a failing status code to Pelecard's own bilingual message. `--explain <code>` looks one up directly. Run `--help`.

## Recommended MCP Servers

No Pelecard MCP exists yet. Pair with the `green-invoice` skill for the Israeli tax document (חשבונית מס), or use Pelecard's own `/services/CreateInvoice` family.

## Reference Links

| Source | Purpose |
|--------|---------|
| https://gateway21.pelecard.biz/services | **Primary reference.** Pelecard's live public request builder: 54 `/services` endpoints plus the `/PaymentGW` lookups, each with a preset request body. Use this instead of guessing parameter names. |
| https://www.postman.com/peleteam/pelecard-public/overview | Pelecard's official Postman workspace ("Gateway21" collection). |
| https://gateway20.pelecard.biz/sandbox | Official Pelecard sandbox + parameter reference. ActionType, currency, 3DS, Bit/Apple Pay/Google Pay toggles. |
| https://wordpress.org/plugins/woo-pelecard-gateway/ | Pelecard-authored WooCommerce plugin. Confirms `gateway21.pelecard.biz` host, refunds, subscriptions, tokenization, Apple Pay via ClientSecure.js. |
| https://github.com/dofinity/pelecard | Third-party PHP wrapper. Documents the full `PaymentRequest` parameter set, the `ConfirmationKey` validation flow, and `PaymentGW/GetTransaction`. |
| https://gateway21.pelecard.biz/services/GetErrorMessageEn | Credential-free official status-code lookup (`{"ErrorCode":"033"}`). `GetErrorMessageHe` for Hebrew. |
| https://match-api.pelecard.biz/docs/index | Pelecard "Match" REST sandbox. Docs page still renders empty; verify with vendor. |
| https://www.allpay.co.il/en/help/bit | Bit wallet constraints: 5,000 ILS per-transaction cap, no installments, single-payment only, 10-minute customer window. |

## Gotchas

- **The hostname is not an environment switch.** `gateway20` and `gateway21` serve the same API; both answer `PaymentGW/init`, `GetTransaction` and `ValidateByUniqueKey` identically, and `gateway20.pelecard.biz/sandbox` is a UI page, not a separate API host. Test-versus-live is decided by the terminal and credentials. Keep host + terminal + credentials in one config object and swap them as a unit; never let code infer safety from a hostname.
- **There is no refund endpoint under `/PaymentGW`, and no credit endpoint anywhere in the public builder.** Voids before broadcast are `/services/DeleteTran`; the post-broadcast credit path must come from Pelecard. Do not improvise one with a negative `total`.
- **An approval number is not money.** A transaction settles only after the terminal broadcasts to Shva. Alert on anything sitting in `/services/GetTransDataBeforeBc` longer than one broadcast cycle.
- **`302` means the debit succeeded; `301` and `303` mean the outcome is unknown.** Only `302` says money moved. Resolve the other two by lookup before touching the order.
- **The two surfaces use different parameter casing.** `/PaymentGW` takes `terminal` / `Total` / `Currency` / `ParamX`; `/services` takes `terminalNumber` / `total` / `currency` / `paramX`, and a couple of token endpoints use PascalCase credentials. Copy the preset from https://gateway21.pelecard.biz/services rather than guessing.
- **A failed `init` returns HTTP 200 with a blank `URL`.** Check `Error.ErrCode`, not the HTTP status.
- **Wrong `ActionType` silently changes whether money moves.** `J2` is registration-only and does not charge, but the merchant UI looks identical to `J4`. Default to `J4`. Plugin v1.4.7: "Bypass validation for J2 transactions."
- **A J5 taken without `CreateToken` may be uncapturable.** The `/services` debit types need a `creditCard` or a `token`, and an iframe J5 gives you neither by default.
- **Pelecard does NOT sign IPN deliveries with HMAC.** Protections: re-verify every callback via `PaymentGW/GetTransaction`, restrict your feedback URLs to Pelecard's outbound IP allowlist, enforce TLS 1.2+. Never trust a payload just because its `ConfirmationKey` looks familiar.
- **`PelecardTransactionId` is your inbound dedupe key, not `ParamX`.** Pelecard may deliver one IPN twice (timeout retry). `ParamX` is your order id and repeats; `PelecardTransactionId` is unique per attempt.
- **Bit's no-installments rule is absolute, the 5,000 ₪ cap is operator-tier-set.** From allpay.co.il: "No installments. You can only pay with Bit in one payment." Hide the tashlumim selector, gate to your agreed cap, and send `Currency: 1`.
- **The credentials triple is server-side only,** and money fields are agorot (`Total: 9900` = ₪99.00). Do a 1 ₪ test charge before going live.

## Troubleshooting

### Error: Callback received but `PaymentGW/GetTransaction` returns "transaction not found"
Cause: The terminal you are querying with is not the terminal the transaction was made on (a test terminal looking up a live transaction, or vice versa). Verified NOT to be a host problem: gateway20 and gateway21 serve the same API, so switching hosts will not fix this.
Solution: Confirm the terminal number and credentials match the transaction. `POST /services/GetTerminalName` with the credentials triple is the cheapest check that your credentials resolve to the terminal you expect. Then re-run the lookup.

### Error: `ConfirmationKey` missing from callback
Cause: The customer abandoned mid-flow, or the request was tampered with.
Solution: Treat the order as unpaid. Do NOT mark it paid even if `PelecardStatusCode` looks like success; resolve it with a `paramX` lookup instead.

### Error: Bit payment fails for amounts above 5,000 ₪
Cause: Bit's per-transaction cap is set by the merchant's Bit agreement and operator risk tier; 5,000 ₪ is the commonly-cited default.
Solution: Gate the Bit option to the cap your agreement allows, surface a "Bit limited to <your cap>" message, offer card as the alternative, and confirm `Currency: 1`.

### Error: 3DS challenge appears in sandbox but transaction is rejected
Cause: A challenge on a test terminal needs specific test cards and challenge responses configured per terminal. Status `650` is "3DS process failed"; resolve any code with `/services/GetErrorMessageEn`.
Solution: Ask Pelecard which test cards and challenge codes work against your terminal. The `Initiate` / `AskForChallenge` toggles control whether 3DS is invoked at all.

### Error: Token charge succeeds but customer claims no payment
Cause: J5 (authorize) was used instead of J4 (sale), and capture was never triggered.
Solution: Verify the `ActionType` on the original transaction via `PaymentGW/GetTransaction`. If it was `J5` or `J5h`, capture it by posting a debit carrying the `authorizationNumber` from the authorization, or release it with `/services/DeleteIshur`. Default to `J4` for one-shot sales. If the ActionType was `J4` and it still has not settled, check `/services/GetTransDataBeforeBc` -- an un-broadcast J4 is approved but not yet money.
