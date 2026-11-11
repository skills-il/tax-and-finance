---
name: grow-payment-gateway
description: Integrate Grow by Meshulam payment gateway into Israeli applications -- covers payment pages (iframe/redirect/SDK), tokenization, recurring billing, payment links, refunds, invoices, webhooks, and 3DS authentication via the Grow Light API. Use when user asks to accept payments via Grow or Meshulam, set up "slikat ashrai" with Grow, create payment links (drishat tashlum), handle recurring charges (hora'ot keva) via Grow tokens, process refunds or Bit cancellations, integrate Grow webhooks, or mentions "Grow", "Meshulam", "grow-il", "meshulam.co.il", Grow payment page, or Grow API. Prevents costly integration mistakes by guiding correct FormData request format, server-side-only restrictions, and the mandatory approveTransaction step that many developers miss. Do NOT use for Cardcom integration (use cardcom-payment-gateway), Tranzila integration (use tranzila-payment-gateway), general payment orchestration across multiple gateways (use israeli-payment-orchestrator), or non-payment queries.
license: MIT
---

# Grow Payment Gateway (Meshulam)

## Overview

Grow (formerly Meshulam) is an Israeli payment gateway for credit cards, Bit, Apple Pay, Google Pay, bank transfer and more. Its "Light API" covers payment pages, tokenization, recurring billing, payment links, invoices, and webhooks.

This skill guides integration with the Light API for the full payment lifecycle: accepting payments, saving and charging tokens, payment links, refunds, and server notifications.

**Official docs:** `https://developers.grow.business/`

**Support:** `support@grow.business` is the address Grow's own documentation gives for production review. (Earlier versions of this skill named `apisupport@grow.business`; that address does not appear anywhere in Grow's published docs.)

## Instructions

### Step 1: Understand Grow's Authentication

| Credential | Purpose | Notes |
|------------|---------|-------|
| `userId` | Identifies the business | Unique per business account |
| `pageCode` | Identifies a payment page or payment method | Different page codes for credit card, Bit, recurring, and so on |
| `apiKey` | Identifies a platform that processes payments for MULTIPLE businesses | Only for platform / system-integrator setups. A direct business sends `userId` + `pageCode` |

**Each environment has its own identifiers.** Sandbox and production each get their own `pageCode`, `userId` and (if relevant) `apiKey`.

**Environments (Light API):**

| Environment | Base URL |
|-------------|----------|
| Sandbox (testing) | `https://sandbox.meshulam.co.il/api/light/server/1.0/` |
| Production | `https://secure.meshulam.co.il/api/light/server/1.0` |

Payment-link management is the exception and lives on a separate host, see Step 8.

**Critical: Server-side only.** All API requests must originate from your server.

**Critical: form encoding, not JSON.** Request bodies use `multipart/form-data` (a probe showed `application/x-www-form-urlencoded` is parsed too), NOT JSON. A JSON body is not parsed at all, so you get a misleading validation error about a missing or invalid field rather than a content-type error.

**Critical: every response is HTTP 200.** The Light API signals failure in the body. Success returns `status: 1`; failure returns `status: 0` with an `err` object. Branch on `status` and `err`, never on the HTTP code.

**`err` changes shape, three ways.** On a validation failure `err` is an object `{"id": 707, "message": "..."}`. On an unrecognised endpoint name `err` is the plain string `"unknown method"`. And `err.id` is sometimes itself an OBJECT: `getTokenTransactionsByExternalIdentifiers` returns `err.id = {"id": 1012, "content": "..."}` with the useful text in `err.id.content`. Normalise before comparing.

**`status` is sometimes a JSON string and sometimes a number.** Compare loosely (coerce to string) rather than with a strict `=== 1`.

### Step 2: Choose Your Integration Pattern

| Pattern | How It Works | Best For |
|---------|-------------|----------|
| **Payment Page (iframe/redirect)** | Grow hosts the payment form; you embed via iframe or redirect | E-commerce checkout, one-time payments |
| **SDK Wallet** | Modular JS SDK embedded in your page | Custom UX without iframe/redirect |
| **Payment Link** | Generate a URL to send to customers | Invoicing, remote payments |
| **Token Charge (server-to-server)** | Charge a saved card token directly | Your own subscription logic, repeat customers |

Grow's docs frame the recurring choice as **Billing vs Tokens**: with Billing, Grow runs the schedule (sum, charge day, number of charges, processed once a month) and you edit or cancel it via Update Direct Debit; with Tokens, your system decides when and how much to charge.

### Step 3: Implement a Payment Page

**Endpoint:** `POST /api/light/server/1.0/createPaymentProcess`

**Required parameters** (all marked "Required field" on the official schema):

| Parameter | Type | Description |
|-----------|------|-------------|
| `pageCode` | string | Payment page identifier |
| `userId` | string | Business identifier |
| `sum` | number | Payment amount (e.g., `10.99`) |
| `successUrl` | string | Redirect after success. HTTPS, external, not localhost |
| `cancelUrl` | string | Redirect if the payment is cancelled |
| `description` | string | Product/service description |
| `pageField[fullName]` | string | Customer name, at least two names |
| `pageField[phone]` | string | Valid Israeli mobile number |

Validate name and phone yourself before calling: Grow's production review checks that the integration does not cause avoidable errors from missing or invalid customer fields (`err.id` 717 is "name and phone not sent or invalid").

**Optional parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `pageField[email]` | string | Customer email |
| `pageField[invoiceName]` / `pageField[invoiceLicenseNumber]` | string | Name and license number for the invoice |
| `paymentNum` | integer | Fixed number of installments (1-12) |
| `maxPaymentNum` | integer | Max installments the customer can choose (minimum 2) |
| `chargeType` | integer | `1` = regular charge, `3` = create token only (see Step 9) |
| `saveCardToken` | integer | `1` = also save the card as a token (see Step 9) |
| `notifyUrl` | string | Server-to-server callback URL |
| `invoiceNotifyUrl` | string | Invoice webhook URL |
| `cField1` - `cField9` | string | Custom fields, passed back to you |
| `transactionTypes[]` | integer array | Restrict payment methods, SDK-wallet pages only, see below |

**Payment methods (transactionTypes), SDK-wallet pages only.** The ARRAY INDEX selects the slot and the VALUE is an integer method code: `[0]`=`1` credit card, `[1]`=`6` Bit, `[2]`=`13` Apple Pay, `[3]`=`14` Google Pay, `[4]`=`15` bank transfer, `[5]`=`5` Pay Box (table in `references/api-endpoints.md`).

**Invoice line items (optional):** `productData[0][catalogNumber]`, `productData[0][quantity]`, `productData[0][price]`, `productData[0][itemDescription]`. Line items that do not add up to `sum` fail with `err.id` 617.

**Example request:**

```bash
curl -X POST https://sandbox.meshulam.co.il/api/light/server/1.0/createPaymentProcess \
  -F "pageCode=YOUR_PAGE_CODE" \
  -F "userId=YOUR_USER_ID" \
  -F "sum=149.90" \
  -F "successUrl=https://example.com/payment/success" \
  -F "cancelUrl=https://example.com/payment/cancel" \
  -F "description=Monthly subscription" \
  -F "pageField[fullName]=Israel Israeli" \
  -F "pageField[phone]=0501234567" \
  -F "notifyUrl=https://example.com/api/grow/webhook" \
  -F "cField1=order-12345"
```

The response includes a `url`: redirect the customer there or embed it as an iframe. Generate a fresh URL for each checkout session; an expired link returns `err.id` 709.

### Step 4: Handle the Payment Response

After payment, two things happen:

1. **Client redirect:** the customer goes to `successUrl` with `response=success` and your `cField` values appended. No transaction details are sent on this redirect.
2. **Server callback:** Grow POSTs to your `notifyUrl` with the full transaction details.

**Fulfil only from the server callback**, never from the redirect, and confirm success by `statusCode` (`2` = paid; a save-token-only flow reports `11`, see Step 9). Persist the `processId` and `processToken` returned by YOUR `createPaymentProcess` call on the order record, and put your order id in `cField1`; they are what binds a callback to an order.

**The callback is a form POST, not JSON.** Grow sends it "the same way as you would send the data to the CreatePaymentProcess method and NOT as JSON". The docs display it as JSON for readability, with the fields nested under `data` (top level `{err, status, data}`): read `data.statusCode`, `data.transactionId`, `data.transactionToken`, and, when a token was saved, `data.cardToken`. A handler that only parses `application/json` sees an empty body. The docs do not spell out the wire key names for the nested fields (flat, or bracketed like `data[statusCode]` in the request convention), so log one raw body from the simulator below and map the keys from it rather than guessing.

**Return HTTP 200 from your callback endpoint.** Grow's production review checks this.

**Test the handler before going live** with Grow's simulator: a GET to `https://sandbox.meshulam.co.il/api/light/server/1.0/updateMyUrl/?url=<your endpoint>` sends a sample callback to the URL you give it.

### Step 5: Approve the Transaction (MANDATORY)

After the callback, call `approveTransaction` to acknowledge it. Per Grow's docs it does not alter the transaction status, and it must be performed for every successful transaction. The Approve page says to send "the pageCode and all data received from the server update", and the endpoint's schema marks every callback field as required, so echo back `pageCode` plus every field the callback delivered.

**Endpoint:** `POST /api/light/server/1.0/approveTransaction`

Live, the router checks the two identifiers first: sending only `transactionId` fails with `err.id` 54 (`חסרים נתונים:transactionToken`), and vice versa. The three-field call below is the minimum that passes validation, not the documented contract.

| Parameter | Required | Source |
|-----------|----------|--------|
| `pageCode` | Yes | Your page code |
| `transactionId` | Yes | `data.transactionId` from the callback |
| `transactionToken` | Yes | `data.transactionToken` from the callback |

```bash
curl -X POST https://sandbox.meshulam.co.il/api/light/server/1.0/approveTransaction \
  -F "pageCode=YOUR_PAGE_CODE" \
  -F "transactionId=TRANSACTION_ID_FROM_CALLBACK" \
  -F "transactionToken=TRANSACTION_TOKEN_FROM_CALLBACK"
  # ...plus every other field from the callback (sum, asmachta, paymentDate, processId, ...)
```

**Do NOT call approveTransaction for:** save-token-only flows, delayed (J4J5) transactions, or `createTransactionWithToken` charges.

**What skipping it does (documented):** the payment goes through anyway. Grow states the transaction is processed even if approveTransaction is not executed or fails. What changes is the notification: when Grow does not receive acknowledgments it resends the server update up to 5 additional times and may contact the business, and its production review checks that approvals are sent. So a missing approval does NOT leave a payment uncaptured or pending, and replaying approvals after an outage cannot "rescue" a charge. Expect the resends, which makes the deduplication in Step 5.5 mandatory.

### Step 5.5: Do not trust the callback body on its own

The callback is a public POST. Grow's callback and webhook pages describe no signature header or shared secret, and `webhookKey` identifies a webhook rather than authenticating it. Anyone who learns your `notifyUrl` can forge `statusCode: 2`.

Before fulfilling any order:

1. Re-query Grow server-to-server with `getTransactionInfo` (`transactionId` + `transactionToken`) or `getPaymentProcessInfo` (`processId` + `processToken`). Treat the API answer as the truth.
2. Assert the returned amount equals the amount on YOUR order record, and that the returned `processId` (or `cField1`) is the one you stored for THIS order. Checking only the amount lets a genuine payment be replayed against a second order of the same price.
3. Use an unguessable `notifyUrl` path. Grow also publishes IP addresses that must be allowed at your firewall (IP Addresses page); restricting the route to them is an extra layer, but the page does not call them the exclusive callback sources, so never rely on it instead of step 1.
4. Deduplicate on `transactionId` with a unique constraint across ALL orders, and do the check-and-mark in one database transaction: Grow resends updates it believes were not acknowledged, and resends can arrive concurrently.
5. Reconcile missed callbacks. If your endpoint was down past Grow's resends, orders stay pending forever; a periodic job should call `getPaymentProcessInfo` with the stored `processId`/`processToken` for orders pending too long and settle them from the answer.

### Step 5.6: Idempotency and retries on token charges

`createTransactionWithToken` has two dedupe fields with different rules, per its official schema:

| Field | Rule |
|-------|------|
| `transactionUniqueIdentifier` (required, integer) | If Grow has already seen the value for the business, the request is rejected outright, **regardless of the status of the first request** |
| `transactionGroupIdentifier` (optional, integer) | Rejected only if a SUCCESSFUL payment already exists with this value |

Both must be a positive integer with no leading zeros, below 4,294,967,295 (a 32-bit value); anything else, including epoch milliseconds or a string, fails with `err.id` 1013.

Consequences:

- A rejection for a reused `transactionUniqueIdentifier` tells you nothing about whether the first attempt charged. Never read it as "already paid".
- For "at most one successful charge per logical charge", send a `transactionGroupIdentifier` that is stable per logical charge and a fresh `transactionUniqueIdentifier` per attempt.
- Grow does not say whether the group check is scoped to the card token or to the whole business. Assume business-wide: make the group value unique per (customer, billing period), for example the integer primary key of a "charge" row you insert before calling, and never derive it from a date alone, or the first customer charged in a period blocks everyone else's charge for that period.
- After a timeout, reconcile first with `getTokenTransactionsByExternalIdentifiers` (`userId`, `cardToken`, and ONE of the two identifiers per call; sending both returns 1012), then retry only if no successful charge exists.
- Persist both values BEFORE the call, so the lookup key exists even if the response never arrives.

### Step 6: Query Transaction Details

`POST /api/light/server/1.0/getTransactionInfo`: `pageCode`, `transactionId`, `transactionToken` (all required; omitting the token returns `err.id` 54).

`POST /api/light/server/1.0/getPaymentProcessInfo`: `pageCode`, `processId`, `processToken` (all required; omitting `processToken` returns `err.id` 54).

### Step 7: Process Refunds

**Refund a credit card transaction:** `POST /api/light/server/1.0/refundTransaction`

| Parameter | Required | Description |
|-----------|----------|-------------|
| `userId` or `pageCode` | One of them | The schema lists `userId` as required and `pageCode` as optional; live, the call accepts either and returns `err.id` 724 ("userId or pageCode required") when both are missing. Use `userId` for token charges, which have no page code |
| `transactionId` | Yes | Transaction to refund |
| `transactionToken` | Yes | Transaction token |
| `refundSum` | Yes | Amount to refund (partial or full). The parameter is `refundSum`; `sum` is not accepted |
| `stopDirectDebit` | No | `1` on a direct-debit transaction stops that series' upcoming payments |

Refund failures worth handling: 105 / 190 / 218 (refund larger than the original), 130 and 207 (partial refund on a transaction made today or not yet transmitted), 210 (already refunded), 110 (funds already at the bank; the request goes to manual approval).

**Cancel a Bit transaction:** `cancelBitTransaction`, keyed by the PROCESS (`pageCode`, `processId`, `processToken`), not the transaction. The reference documents the path as `/api/light/andriod/1.0/cancelBitTransaction/` (Grow's spelling); `/api/light/server/1.0/cancelBitTransaction` answers with the same validation.

### Step 8: Create Payment Links

Payment links (drishat tashlum) are shareable payment URLs. Grow can send them itself by SMS or email (`sendingMode` 1 / 2), or you share the URL your own way.

**The documented API is on a different host and version from the rest of the Light API:**

| Operation | Documented endpoint (sandbox) | Notes |
|-----------|-------------------------------|-------|
| Create | `POST https://sandboxapi.grow.link/api/light/server/1.1/CreatePaymentLink` | Case-sensitive: a lowercase `createPaymentLink` is not routed on this host |
| Update / deactivate | `POST https://sandboxapi.grow.link/api/light/server/1.0/UpdatePaymentLink` | Requires `pageCode`, `isActive` (1/0), `paymentLinkProcessId`, `paymentLinkProcessToken` |

Both carry an `X-API-KEY` header. Grow publishes the production value for CreatePaymentLink on its Transition to Production page; read it from there rather than copying one from a third-party snippet. Grow's pages give only the sandbox host for these two endpoints, so confirm the production host with Grow when production identifiers are issued, and do not guess one.

The CreatePaymentLink contract differs from `createPaymentProcess`: there is no `sum`; the amount comes from `products[data][N][price]`. Its required fields include `userId`, `pageCode`, `paymentLinkType`, `isActive`, `title`, `paymentTypes[0][type]` with either `paymentTypes[0][payments][paymentsPaymentNum]` or `...[paymentsMaxPaymentNum]`, `pageFieldSettings[fullName][value]`, `pageFieldSettings[phone][value]`, and per product `name`, `price` and `vatType`. Copy the full parameter list from the reference page.

**Do not mix contracts.** The `meshulam.co.il` hosts also answer a `createPaymentLink` method, but with a different, undocumented contract (it asks for `sum` first). Build on the documented one.

Query an existing link with `getPaymentLinkInfo`, which the schema documents with `pageCode`, `paymentLinkProcessId` and `paymentLinkProcessToken` as required.

### Step 9: Tokenization and Recurring Billing

**Prerequisites (Token page):** working with tokens requires permission from Grow; token saving is not applicable to Bit, Apple Pay or Google Pay, so a subscription checkout must use a credit-card page; a token can be saved for up to 180 payments, so plan to re-tokenise long subscriptions.

**Saving a token.** Two documented flows, both through `createPaymentProcess`:

| Flow | Parameters |
|------|-----------|
| Save token only | `chargeType=3`, `sum=1` (the schema says the amount must be 1), `saveCardToken=1` |
| Regular payment that also saves the token | Normal parameters plus `saveCardToken=1` |

There is no separate `getTokenOnly` endpoint: `POST /api/light/server/1.0/getTokenOnly` returns `{"err":"unknown method"}` on both hosts. Grow's "Get Token Only" reference page documents the `chargeType=3` flow above.

**Where the token comes from:** the callback's `data.cardToken` field. Do NOT use `transactionToken` as the card token: `transactionToken` identifies one transaction (it is what `approveTransaction`, `getTransactionInfo` and `refundTransaction` need), while `cardToken` is the reusable card credential. The save-token-only example callback carries `statusCode` `11` (suspended transaction), not `2`.

**Customer consent is required.** Grow's production checklist requires a checkbox on the payment page in which the customer actively approves saving the card token before it is stored.

#### Option A: Grow-Managed via Page Code

1. Create the payment with `createPaymentProcess` using a recurring page code configured in the Grow dashboard
2. Set `sum` to the per-charge amount and `paymentNum` to the number of charges
3. Grow runs the subsequent charges

#### Option B: Charge a Saved Token (server-to-server)

`POST /api/light/server/1.0/createTransactionWithToken`. Keyed by `userId`, not `pageCode`. The token parameter is `cardToken` (NOT `token`).

| Parameter | Required | Notes |
|-----------|----------|-------|
| `userId`, `cardToken`, `sum`, `description` | Yes | Live, a call with only `sum` reports `userId` missing, then `cardToken` |
| `paymentType` | Yes | `1` recurring managed by Grow, `2` regular, `4` installments. For `1`, Grow's pages disagree on the `paymentNum` range (Work with Token: 1-48; the premium-by-token schema: 2-12); confirm with Grow |
| `paymentNum` | Yes | Live, omitting it returns `err.id` 54. `1` for a single non-installment charge |
| `pageField[fullName]`, `pageField[phone]` | Yes | Same validation as the payment page |
| `transactionUniqueIdentifier` | Yes | 32-bit integer, new per attempt, see Step 5.6 |
| `transactionGroupIdentifier` | No | Integer, stable per logical charge, see Step 5.6 |

```bash
curl -X POST https://sandbox.meshulam.co.il/api/light/server/1.0/createTransactionWithToken \
  -F "userId=YOUR_USER_ID" \
  -F "cardToken=CARD_TOKEN_FROM_CALLBACK" \
  -F "sum=99.00" \
  -F "description=Monthly subscription" \
  -F "paymentType=2" \
  -F "paymentNum=1" \
  -F "pageField[fullName]=Israel Israeli" \
  -F "pageField[phone]=0501234567" \
  -F "transactionGroupIdentifier=48213" \
  -F "transactionUniqueIdentifier=100001"
```

Check `statusCode` in the response (`2` = paid) and persist its `transactionId`, `transactionToken` and `asmachta`: refunds and `updateDirectDebit` need them later. Do not call `approveTransaction` afterwards.

**Declined token charges.** Grow's Token page says a FINAL error (expired, stolen or blocked card) means stop charging the token, delete it, and get a new card from the customer. Its table reuses `err.id` 103 for both kinds, so classify by `err.id` AND `err.message`:

| `err.id` | Message (Hebrew, as returned) | Final? |
|---------|------------------------------|--------|
| 103 | כרטיס פג תוקף / כרטיס גנוב / כרטיס חסום | Final |
| 103 | חברת האשראי לא אשרה את העסקה | Not final |
| 451 / 452 / 453 | Card inactive or expired / blocked by the card company / system block | Final |

On a final error, stop the schedule and send the customer a new `saveCardToken=1` payment page. On a non-final one, retry a bounded number of times with a fresh `transactionUniqueIdentifier` and the same `transactionGroupIdentifier`.

#### Option C: Premium Recurring by Token

Premium recurring needs permission from Grow. It keeps the token valid when the card expires, can move the series to a new card with the customer's approval, and shows the charges as recurring on the card statement. With a saved token:

1. **First payment:** `createTransactionWithToken` with the Option B fields plus `isRecurringDebitPayment=1` (the name in the endpoint schema; one overview page writes `isRecurringDebitId=1` and says the id arrives in the server update rather than the response, so check both). Save the `recurringDebitId`.
2. **Each later payment:** `createTransactionWithToken` with the Option B fields plus `recurringDebitId`.
3. For ordinary non-recurring token charges, send neither parameter.

**Update or cancel a Grow-managed series:** `POST /api/light/server/1.0/updateDirectDebit` (`updateRecurringPayment` does not exist and returns `unknown method`).

| Parameter | Required | Notes |
|-----------|----------|-------|
| `userId`, `transactionId`, `transactionToken`, `asmachta` | Yes | Live, the call names `userId`, then `transactionId`, then `asmachta` as missing |
| `changeStatus` | No | `1` active, `2` canceled |
| `sum`, `paymentNum` (1-48), `chargeDay` (1-31) | No | New amount, count, day of month |
| `fullName`, `phone`, `email` | No | Update payer details |
| `updateCard` | No | `0` no update, `1` update |

`err.id` 180 (`פעולת עידכון לא בוצעה, רשומה לא נמצאה`) means the record was not found.

### Step 10: Delayed Payments (J4J5)

Create the delayed payment with `createPaymentProcess` and a J4J5 page code, then settle it:

`POST /api/light/server/1.0/settleSuspendedTransaction`: keyed by `userId` (NOT `pageCode`; sending `pageCode` returns `err.id` 54 for `userId`), plus `transactionId`, `transactionToken` and `sum`.

Settlement is capped: `err.id` 814 means the charge exceeded the authorised hold by more than 30 percent, 804 that it exceeded the hold, 803 that the J5 authorisation expired, 808 that it was already settled. Do not send `approveTransaction` for J4/J5 flows.

`createFarPaymentRequest` also exists on both hosts; it is not covered here, read its reference page before using it.

### Step 11: Configure Webhooks

Webhooks are separate from the `notifyUrl` callback and are enabled per account by Grow support, per trigger (one-time transactions, payment links, recurring from the 2nd charge, failed recurring, POS, invoices, and more; full list in `references/webhook-payloads.md`).

**Two payload families, read them differently:**

| Family | Shape | Key fields |
|--------|-------|-----------|
| Legacy pages, recurring, API one-time | Flat object with `webhookKey` | `transactionCode`, `paymentSum`, `paymentsNum`, `allPaymentNum`, `paymentType`, `asmachta`, `paymentSource`, `directDebitId` (recurring). No `statusCode`, `transactionId` or `transactionToken` |
| Payment links (new system) | `{err, status, data}` like the callback | `data.statusCode`, `data.transactionId`, `data.transactionToken`, `data.paymentLinkProcessId`, `data.paymentLinkProcessToken`, `productData`, `shipping` |

The failed-recurring payload uses snake_case (`regular_payment_id`, `error_message`, `charges_attempts`, `webhook_key`). The invoice webhook carries `transactionCode`, `invoiceNumber` and `invoiceUrl`. Full examples: `references/webhook-payloads.md`.

For Grow-managed recurring series, charges from the 2nd onward are reported only through these webhooks, and the flat family carries no `transactionId`/`transactionToken`, so the Step 5.5 re-query cannot verify them. Treat them as notifications: reconcile against Grow's reports or your merchant dashboard before extending paid access on their strength.

**Webhooks configured in the sandbox are not copied to production;** they must be configured again.

### Step 12: 3D Secure

Per Grow's 3DS reference page, 3DS is a service the business purchases. Once purchased it is active for every transaction by default, and it sends a code to the cardholder's mobile number registered with the card company. To skip it for a specific transaction, send `cancel3DS=True` in the API call.

The page does not say how a liability shift applies, or whether a server-to-server `createTransactionWithToken` charge runs 3DS. Do not assume a token charge inherits the 3DS status of the original payment; ask Grow.

### Step 13: Payment Page Types

Each page type has its own `pageCode`: SDK Wallet (JS widget), Generic (credit card + Bit), Credit Card, Google Pay (needs `allow="payment"` on the iframe), Apple Pay (needs domain verification, repeated for the production domain), Bit (best full-screen on mobile), Bit QR (desktop or in-store).

```html
<iframe src="PAYMENT_URL_FROM_API" width="100%" height="600"
        allow="payment" style="border: none;"></iframe>
```

HTTPS is mandatory for iframe integrations. Inside an iframe, Grow's PostMessage interface reports browser-side events (credit card success `payment`, Bit success `bit_payment`); treat them as UX signals only and still fulfil from the server callback.

Avoid special characters in parameters.

### Step 14: Sandbox Testing and Going Live

**Sandbox test cards** (Testing Environment page): `4580458045804580` (regular single payments only; use it to test failed multi-payment transactions), `4580000000000000`, `4580111111111121`. Test bank transfer: bank `41`, branch `410`, account `411111111`.

**Bit, Google Pay and Apple Pay have no test environment.** Transactions with them are processed in the live environment and charged as real transactions, even during development. PayBox cannot be completed in the sandbox.

**Growin Wallet SDK:** change `environment` in `configureGrowSdk` from `"DEV"` to `"PRODUCTION"` when going live.

**Production is gated.** Grow issues production identifiers only after reviewing your integration logs: requests sent correctly, callbacks answered with HTTP 200, approveTransaction sent where required, customer fields validated. Platforms also need a signed commercial agreement. E-commerce sites must show a contact phone, a business address, a terms checkbox with a link, and terms covering delivery, liability, age restriction, cancellation and privacy. Request the review at `support@grow.business`.

**Invoices.** Grow can generate invoices (`invoiceNotifyUrl`, `productData`). Its developer docs expose no allocation-number (מספר הקצאה) field or behaviour. If Grow issues your B2B tax invoices, ask Grow how it obtains allocation numbers; the thresholds are covered by `il-invoice-organizer`.

## Error Codes

Grow returns errors in the body with `status: 0` and an `err` object. The common codes are below; the full list, including codes seen live but missing from Grow's table, is in `references/error-codes.md`.

| Code | Meaning |
|------|---------|
| 54 | Missing required field; the message names the field |
| 707 | Invalid amount (also what a JSON body produces) |
| 717 | Name and phone not sent or invalid |
| 722 | Cannot approve a transaction that was not performed or was cancelled |
| 724 | `userId` or `pageCode` required |
| 1013 | Identifier is not a positive 32-bit integer |
| 103 / 451 / 452 / 453 | Token-charge declines; see Step 9 for final vs not final |
| 403 | Forbidden: `X-API-KEY` was not sent |

Treat any unrecognised `err.id` as a failure and surface `err.message`.

## Gotchas
- Grow requires `multipart/form-data`, NOT `application/json`. JSON produces a validation error about the first missing field (typically `err.id` 707, invalid amount), and agents then hunt for a bug in the amount.
- Every response is HTTP 200, including every failure. Branch on the body's `status` and `err`.
- The card token is `data.cardToken`, not `data.transactionToken`. Charging a `transactionToken` as a card token fails, and storing `cardToken` where a transaction token is expected breaks approve, refund and lookup.
- A reused `transactionUniqueIdentifier` is rejected whether or not the first attempt succeeded. Treating that rejection as "already paid" ships goods unpaid; reconcile first.
- Skipping `approveTransaction` does not stop the charge. It causes resent callbacks and a failed production review. Do not tell a user that unapproved payments are pending.
- Bit, Apple Pay and Google Pay have no sandbox: a "test" payment with them is a real charge.
- `cardToken` and `transactionToken` are bearer credentials. Never log them, never show them to the paying customer (Grow says so explicitly; `asmachta` is the value you may show), and encrypt them at rest. Do not accept, log, or proxy a raw card number yourself.
- "Server-side only" is enforced by the absence of CORS headers, so a browser call shows a CORS console error, not a 403.

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|---------|
| HTTP 403 Forbidden | `X-API-KEY` header was not sent, the cause Grow's error table gives. The header is documented for the payment-link endpoints | Send the `X-API-KEY` header on the calls that require it |
| Browser request fails, no 403 seen | The API sends no CORS headers. Verified: a request carrying a browser `Origin` and `Referer` is answered normally | Move the call server-side |
| `err.id` 707 on a request whose amount is fine | Likeliest cause is a JSON body: the fields never parse, so validation fails on the amount first. Not confirmed to be the only trigger | Switch to `multipart/form-data` and re-send |
| `err.id` 54 on `approveTransaction` | Only one of the two identifiers was sent | Send BOTH `transactionId` and `transactionToken` |
| Token charge fails after a successful first payment | `transactionToken` was stored as the card token, or the first payment did not set `saveCardToken=1` | Store `data.cardToken` from a payment created with `saveCardToken=1` |
| Callback handler receives an empty body | It parses JSON only; Grow posts form data | Parse form / multipart bodies on that route |
| Same callback arrives several times | Grow resends updates it believes were not acknowledged | Call `approveTransaction` and dedupe on `transactionId` |
| `{"err":"unknown method"}` | The method name does not exist on that host (for example `getTokenOnly`, `updateRecurringPayment`) | Use the live endpoint named in Step 8 or Step 9 |
| HTTP 403 `{"message":"Missing Authentication Token"}` from `sandboxapi.grow.link` | A path that host does not route, often a lowercase `createPaymentLink` | Use the documented case: `/1.1/CreatePaymentLink`, `/1.0/UpdatePaymentLink` |
| A "test" Bit or Apple Pay payment charged a real card | These methods have no sandbox | Refund it, and test those methods only with amounts you intend to refund |
| Helper script exits with "GROW_API_KEY was renamed to MESHULAM_API_KEY" | Renamed environment variable | Rename it (`export MESHULAM_API_KEY=...`) and unset `GROW_API_KEY`; the value does not change |

## Bundled Resources

- `scripts/grow-payment-helper.sh`: sandbox-first helper for createPaymentProcess, transaction and process lookups, approve, refund, Bit cancel and token charges. It exits non-zero on an API error, sends credentials only to the two pinned `meshulam.co.il` hosts, keeps tokens and keys out of the process list, masks tokens in its output, and refuses production unless `GROW_ALLOW_PRODUCTION=1` is set.
- `references/api-endpoints.md`: endpoint table, hosts, and the methods that do not exist.
- `references/webhook-payloads.md`: webhook and callback payload examples from Grow's docs.
- `references/error-codes.md`: the full error-code table.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Grow API Reference | https://developers.grow.business/reference/introduction | Entry point to the current endpoints and request schemas |
| Grow Errors Table | https://developers.grow.business/reference/errors | The full numeric error-code table |
| Testing Environment | https://developers.grow.business/reference/testing-environment | Sandbox URL, test cards, methods with no sandbox |
| Transition to Production | https://developers.grow.business/reference/live-environment | Production URL, review checklist, payment-link `X-API-KEY` |
| Server-to-Server Callback | https://developers.grow.business/reference/server-to-server-callback | Callback format, approveTransaction behaviour, updateMyUrl |
| IP Addresses | https://developers.grow.business/reference/ip-address | Addresses to allow at your firewall |
| Grow 3DS Reference | https://developers.grow.business/reference/3ds-1 | 3DS service and `cancel3DS` |
| Grow Webhooks | https://developers.grow.business/docs/overview-7 | Webhook options and payloads |
