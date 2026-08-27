---
name: grow-payment-gateway
description: Integrate Grow by Meshulam payment gateway into Israeli applications -- covers payment pages (iframe/redirect/SDK), tokenization, recurring billing, payment links, refunds, invoices, webhooks, and 3DS authentication via the Grow Light API. Use when user asks to accept payments via Grow or Meshulam, set up "slikat ashrai" with Grow, create payment links (drishat tashlum), handle recurring charges (hora'ot keva) via Grow tokens, process refunds or Bit cancellations, integrate Grow webhooks, or mentions "Grow", "Meshulam", "grow-il", "meshulam.co.il", Grow payment page, or Grow API. Prevents costly integration mistakes by guiding correct FormData request format, server-side-only restrictions, and the mandatory approveTransaction step that many developers miss. Do NOT use for Cardcom integration (use cardcom-payment-gateway), Tranzila integration (use tranzila-payment-gateway), general payment orchestration across multiple gateways (use israeli-payment-orchestrator), or non-payment queries.
license: MIT
---

# Grow Payment Gateway (Meshulam)

## Overview

Grow (formerly Meshulam) is one of Israel's leading payment gateways, powering thousands of businesses with credit card processing, Bit payments, Apple Pay, Google Pay, and more. Unlike other Israeli gateways, Grow offers a unified API (the "Light API") that covers payment pages, tokenization, recurring billing, payment links, invoices, and webhooks in a single integration.

This skill guides integration with Grow's Light API for the full payment lifecycle: accepting payments, saving tokens for recurring charges, creating payment links for invoices, processing refunds, and handling real-time webhook notifications.

**Official docs:** `https://developers.grow.business/`

**Developer support:** `apisupport@grow.business` (carried from an earlier cycle; not confirmed against Grow's published documentation this cycle, so confirm it in your merchant portal before relying on it).

## Instructions

### Step 1: Understand Grow's Authentication

Grow uses three credentials provided during merchant onboarding:

| Credential | Purpose | Notes |
|------------|---------|-------|
| `userId` | Merchant identifier | Unique per business account |
| `pageCode` | Payment page configuration | Different page codes for different payment types (credit card, Bit, recurring, etc.) |
| `apiKey` | API authentication | Required when managing multiple businesses or specific configurations |

**Environments:**

| Environment | Base URL |
|-------------|----------|
| Sandbox (testing) | `https://sandbox.meshulam.co.il` |
| Production | `https://secure.meshulam.co.il` |

**Critical: Server-side only.** All API requests must originate from your server. Client-side (browser) requests are blocked by Grow.

**Critical: FormData format.** All request bodies use `multipart/form-data`, NOT JSON. If you send `application/json` the API does not parse your fields at all, so you get a misleading validation error about a missing or invalid field rather than a content-type error.

**Critical: every response is HTTP 200.** The Light API signals failure in the body, never in the status line. A successful call returns `status: 1`; a failure returns `status: 0` with an `err` object. Branch on `status` and `err`, never on the HTTP code. See the Error Codes section.

**`err` changes shape, three ways.** On a validation failure `err` is an object `{"id": 707, "message": "..."}`. On an unrecognised endpoint name `err` is the plain string `"unknown method"`. And `err.id` is itself sometimes an OBJECT: `getTokenTransactionsByExternalIdentifiers` returns `err.id = {"id": 1012, "content": "..."}` with the useful text in `err.id.content` and a generic `err.message`. Code doing `err.id === 54` silently mismatches there, and logging `err.id` prints `[object Object]`. Normalise before comparing.

**`status` is sometimes a JSON string and sometimes a number.** The same endpoint returns `"status":"0"` on one input and `"status":0` on another. Compare loosely (coerce to string) rather than with a strict `=== 1`.

### Step 2: Choose Your Integration Pattern

| Pattern | How It Works | Best For |
|---------|-------------|----------|
| **Payment Page (iframe/redirect)** | Grow hosts the payment form; you embed via iframe or redirect | E-commerce checkout, one-time payments |
| **SDK Wallet** | Modular JS SDK embedded in your page | Custom UX without iframe/redirect overhead |
| **Payment Link** | Generate a URL to send to customers | Invoicing, freelancer billing, remote payments |
| **Token Charge (server-to-server)** | Charge a saved token directly | Recurring billing, subscriptions, repeat customers |

Most Israeli merchants use **Payment Page** for the first payment (which also saves a token), then **Token Charge** for recurring billing.

### Step 3: Implement a Payment Page

This is the most common integration -- create a hosted payment page and redirect or iframe the customer to it.

**Endpoint:** `POST /api/light/server/1.0/createPaymentProcess`

**Required parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `pageCode` | string | Payment page identifier (provided by Grow) |
| `userId` | string | Your merchant ID |
| `sum` | number | Payment amount (e.g., `10.99`) |
| `successUrl` | string | Redirect URL after successful payment (HTTPS required) |
| `cancelUrl` | string | Redirect URL if payment is cancelled |
| `description` | string | Product/service description |
| `pageField[fullName]` | string | Customer name (must contain at least two names) |
| `pageField[phone]` | string | Valid Israeli mobile phone number |

**Optional parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `pageField[email]` | string | Customer email |
| `paymentNum` | integer | Fixed number of installments (1-12) |
| `maxPaymentNum` | integer | Max installments customer can choose (2-N) |
| `chargeType` | integer | `1` = regular charge |
| `notifyUrl` | string | Server-to-server callback URL |
| `invoiceNotifyUrl` | string | Invoice webhook URL |
| `cField1` - `cField9` | string | Custom merchant fields (passed back in callbacks) |
| `transactionTypes[]` | array | Restrict which payment methods appear (SDK-wallet pages only). Each method is a fixed array index, see table below |

**Payment methods (transactionTypes) -- SDK-wallet pages only.** Two things matter and earlier versions of this skill got the second one wrong. The ARRAY INDEX selects the slot, and the VALUE is an integer method code. Both come from the `createPaymentProcess` schema on the official reference page:

| Parameter | Payment Method | Documented value |
|-----------|---------------|------------------|
| `transactionTypes[0]` | Credit Card | `1` |
| `transactionTypes[1]` | Bit | `6` |
| `transactionTypes[2]` | Apple Pay | `13` |
| `transactionTypes[3]` | Google Pay | `14` |
| `transactionTypes[4]` | Bank transfer | `15` |
| `transactionTypes[5]` | Pay Box | defaults to `5` |

**Invoice line items (optional):**

| Parameter | Type | Description |
|-----------|------|-------------|
| `productData[0][catalogNumber]` | integer | Item catalog number |
| `productData[0][quantity]` | integer | Item quantity |
| `productData[0][price]` | number | Item price |
| `productData[0][itemDescription]` | string | Item description |

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
  -F "pageField[email]=customer@example.com" \
  -F "paymentNum=1" \
  -F "notifyUrl=https://example.com/api/grow/webhook" \
  -F "cField1=order-12345"
```

The response includes a `url` field -- redirect the customer there or embed as an iframe.

**Important:** treat the payment page URL as short-lived and generate a fresh one for each checkout session. A 10-minute window is the figure carried by this skill from earlier cycles; it is not stated on any Grow documentation page this cycle could fetch, so do not rely on the exact number.

### Step 4: Handle the Payment Response

After the customer completes payment, two things happen:

1. **Client redirect:** Customer is redirected to `successUrl` with `response=success` appended
2. **Server callback:** Grow sends a POST to your `notifyUrl` with full transaction details

**Always verify via server callback**, not the client redirect (which can be spoofed). In the callback, confirm success by checking `statusCode` (`2` = paid), do not treat the mere arrival of a redirect to `successUrl` as proof of payment.

**Payload nesting (important):** on the server-to-server `notifyUrl` callback the fields are nested under a `data` object (the top level is `{err, status, data}`), so read `data.statusCode`, `data.transactionToken`, and `data.transactionId` (the id you pass to `approveTransaction`), NOT the top level. The separate webhookKey webhook system (Step 11) delivers a flatter payload.

### Step 5: Approve the Transaction (MANDATORY)

After receiving the server callback, you MUST call `approveTransaction` to confirm receipt. This does not alter the payment -- it closes the transaction loop with Grow.

**Endpoint:** `POST /api/light/server/1.0/approveTransaction`

`approveTransaction` requires **both** identifiers from the callback. Sending only `transactionId` fails with `err.id` 54 (`חסרים נתונים:transactionToken`), and sending only `transactionToken` fails with 54 for `transactionId`.

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
```

**Do NOT call approveTransaction for:** token-only saves, delayed (J4J5) transactions, or `createTransactionWithToken` charges.

**What happens if you never call it is NOT documented and this skill does not guess.** Grow's docs mark the step mandatory, and `err.id` 722 (`לא ניתן לבצע אישור לעסקה שלא בוצעה או בוטלה`) shows an approval can be refused. Whether funds are captured without it, whether there is an expiry window, and whether a late approval is still accepted could not be established without a merchant account. If you are recovering approvals after an outage, confirm the answer with Grow before choosing between replaying approvals and refunding, and do not assume either way.

### Step 5.5: Do not trust the callback body on its own

The server callback is the trust anchor for fulfilment, and it is an unauthenticated public POST. Grow sends no signature header; `webhookKey` identifies the webhook, it is not a shared secret you can verify a payload against. Anyone who learns your `notifyUrl` can forge `{statusCode: 2, ...}` and take goods for free.

Before fulfilling any order:

1. Re-query Grow server-to-server with `getTransactionInfo` (`transactionId` + `transactionToken`) or `getPaymentProcessInfo` (`processId` + `processToken`). Treat the API answer as the truth, not the callback body.
2. Assert the returned amount equals the amount on YOUR order record. A forged or replayed callback that names a different sum must not fulfil.
3. Use an unguessable per-merchant `notifyUrl` path, and never log the URL where customers can see it.
4. Deduplicate on `transactionId`: a redelivered or replayed callback must fulfil once, not twice.

### Step 5.6: Idempotency and retries

`transactionUniqueIdentifier` is your idempotency key on `createTransactionWithToken`. Send a value that is stable per logical charge, not per attempt.

- On a network timeout or a 5xx where you do not know whether the card was charged, do NOT blind-retry with a fresh identifier: that is how a customer gets billed twice. Re-send the SAME `transactionUniqueIdentifier`, or reconcile first with `getTokenTransactionsByExternalIdentifiers`.
- `err.id` 712 (`העסקה כבר בוצעה`) is the replay signal, not a bug. Treat it as "already charged, succeed" rather than as a failure to retry.

### Step 6: Query Transaction Details

**Get transaction info:**

`POST /api/light/server/1.0/getTransactionInfo`

| Parameter | Type | Description |
|-----------|------|-------------|
| `pageCode` | string | Page identifier |
| `transactionId` | string | Transaction ID to query |
| `transactionToken` | string | Transaction token from the callback. Required: omitting it returns `err.id` 54 |

**Get payment process info:**

`POST /api/light/server/1.0/getPaymentProcessInfo`

| Parameter | Type | Description |
|-----------|------|-------------|
| `pageCode` | string | Page identifier |
| `processId` | string | Process ID from createPaymentProcess |
| `processToken` | string | Process token from createPaymentProcess. Required: omitting it returns `err.id` 54 |

### Step 7: Process Refunds

**Refund a credit card transaction:**

`POST /api/light/server/1.0/refundTransaction`

| Parameter | Type | Description |
|-----------|------|-------------|
| `pageCode` | string | Page identifier |
| `transactionId` | string | Transaction to refund |
| `transactionToken` | string | Transaction token. Required: without it the call returns `err.id` 54 |
| `refundSum` | number | Amount to refund (partial or full). The parameter is `refundSum`; `sum` is not accepted here and leaves the call failing with `err.id` 707 |

Refund-specific failures worth handling: 105 and 218 (refund larger than the original), 130 and 207 (partial refund on a transaction settled or transmitted today), 210 (already refunded), 110 (funds already transferred to the bank, so the request goes to manual approval).

**Cancel a Bit transaction:**

`POST /api/light/server/1.0/cancelBitTransaction`

This endpoint is keyed by the PROCESS, not the transaction. Sending `transactionId` returns `err.id` 54 for `processId`.

| Parameter | Type | Description |
|-----------|------|-------------|
| `pageCode` | string | Page identifier |
| `processId` | string | Payment process id |
| `processToken` | string | Payment process token |

### Step 8: Create Payment Links

Payment links (drishat tashlum) let you send a payment URL to customers via email, SMS, or WhatsApp. Useful for invoicing and remote payments.

**Endpoint:** `POST /api/light/server/1.0/createPaymentLink`

| Parameter | Type | Description |
|-----------|------|-------------|
| `pageCode` | string | Page identifier |
| `userId` | string | Merchant ID |
| `sum` | number | Payment amount |
| `description` | string | Payment description |
| `pageField[fullName]` | string | Customer name |
| `pageField[phone]` | string | Customer phone |
| `pageField[email]` | string | Customer email |

The response includes a shareable payment URL. Query an existing link with `getPaymentLinkInfo`, which requires `paymentLinkProcessToken` (omitting it returns `err.id` 54 naming that field).

**`updatePaymentLink` is not available on the Light API.** Probed against both `sandbox.meshulam.co.il` and `secure.meshulam.co.il`, it returns `{"err":"unknown method"}`, the same response the router gives for an endpoint name that does not exist, and distinct from the permission errors (300, 714, 715) a real-but-unauthorised endpoint returns. Create a replacement link instead.

### Step 9: Tokenization and Recurring Billing

**Where the token comes from:** the saved card token arrives in the payment webhook's `transactionToken` field after the first payment. Use that value as the `cardToken` in the `createTransactionWithToken` calls below.

**`getTokenOnly` does not resolve on the Light API path.** Grow's reference nav still lists a "Get Token Only" operation, but `POST /api/light/server/1.0/getTokenOnly` returns `{"err":"unknown method"}` on BOTH hosts and across casing variants, which is the router's answer for a name it does not know. Do not code against this path. To save a card without charging it, run a payment through a page code configured for tokenization and take the token from the callback, or confirm the current operation with Grow support.

Grow supports three recurring payment models:

#### Option A: Grow-Managed via Page Code

Use a dedicated recurring page code configured in the Grow dashboard:

1. Create payment with `createPaymentProcess` using the recurring page code
2. Set `sum` to the monthly charge amount and `paymentNum` to total iterations
3. Grow handles all subsequent charges automatically

#### Option B: Charge a Saved Token (server-to-server)

Charge a saved card token directly. The token parameter is `cardToken` (NOT `token`), and `paymentType=2` is a Regular charge:

```bash
curl -X POST https://sandbox.meshulam.co.il/api/light/server/1.0/createTransactionWithToken \
  -F "userId=YOUR_USER_ID" \
  -F "sum=99.00" \
  -F "description=Monthly subscription" \
  -F "cardToken=SAVED_CARD_TOKEN" \
  -F "paymentType=2" \
  -F "pageField[fullName]=Israel Israeli" \
  -F "pageField[phone]=0501234567" \
  -F "transactionUniqueIdentifier=UNIQUE_PER_CHARGE"
```

`cardToken` is the saved card token; it arrives in the payment webhook's `transactionToken` field. Check `statusCode` in the response (`2` = paid) to confirm the charge succeeded. This endpoint uses `userId`, not `pageCode`, and it also requires `paymentNum` (omitting it returns `err.id` 54 for `paymentNum`); send `paymentNum=1` for a single non-instalment charge.

#### Option C: Premium Recurring Series (recurringDebitId)

For a Grow-managed recurring series, each charge carries a `recurringDebitId` that ties it to the series. That id is returned by the FIRST premium-recurring payment's response; pass it on every subsequent `createTransactionWithToken` call, alongside `cardToken`, `paymentType=2`, and the required fields above:

```bash
curl -X POST https://sandbox.meshulam.co.il/api/light/server/1.0/createTransactionWithToken \
  -F "userId=YOUR_USER_ID" \
  -F "sum=99.00" \
  -F "description=Monthly subscription" \
  -F "cardToken=SAVED_CARD_TOKEN" \
  -F "paymentType=2" \
  -F "pageField[fullName]=Israel Israeli" \
  -F "pageField[phone]=0501234567" \
  -F "recurringDebitId=RECURRING_DEBIT_ID" \
  -F "transactionUniqueIdentifier=UNIQUE_PER_CHARGE"
```

Confirm the exact premium-recurring initiation parameters on the `createTransactionWithToken` reference (see Reference Links) rather than assuming a flag name.

**Update recurring payment:**

`updateRecurringPayment` is NOT available on the Light API: probed against both hosts it returns `{"err":"unknown method"}`. The live endpoint for changing a direct-debit series is `POST /api/light/server/1.0/updateDirectDebit`. Confirm its parameter set on the Update Direct Debit reference page before wiring it, and expect `err.id` 180 (`פעולת עידכון לא בוצעה, רשומה לא נמצאה`) when the series id does not match.

**Token transaction lookup:**

`POST /api/light/server/1.0/getTokenTransactionsByExternalIdentifiers` -- find all transactions for a given token using external reference IDs.

**Premium recurring features:**
- Automatic card update on expiration (new expiry date applied to existing token)
- Card transfer support when customer switches cards
- Distinct billing line on customer's credit card statement

### Step 10: Delayed Payments (J4J5 Installments)

J4J5 allows 4 interest-free installments (tashlumim l'lo ribit), a popular payment option in Israel:

**Create delayed payment:**

`POST /api/light/server/1.0/createPaymentProcess` with J4J5 page code

**Settle when ready:**

`POST /api/light/server/1.0/settleSuspendedTransaction`

This endpoint is keyed by `userId`, NOT `pageCode`. Sending `pageCode` returns `err.id` 54 for `userId`.

| Parameter | Type | Description |
|-----------|------|-------------|
| `userId` | string | Merchant ID |
| `transactionId` | string | Suspended transaction to settle |
| `transactionToken` | string | Transaction token |
| `sum` | number | Amount to settle |

Settlement is capped: `err.id` 814 means the charge exceeded the authorised hold by more than 30 percent, and 804 means it exceeded the hold entirely. 803 means the J5 authorisation expired, and 808 means the transaction was already settled.

**Related:** `createFarPaymentRequest` also exists on the Light API (verified live on both hosts). It is not covered by this skill; read its reference page before using it.

### Step 11: Configure Webhooks

Grow sends real-time notifications to your server for various events. Contact `apisupport@grow.business` to enable webhooks for your account.

**Webhook trigger options:**

| Trigger | Description |
|---------|-------------|
| All one-time transactions | Every payment across all pages |
| Specific payment pages | Filter by page code |
| Specific payment links | Filter by payment link |
| Recurring payments | From 2nd charge onward |
| Failed recurring | When a recurring charge fails |
| POS transactions | In-person payments |
| Invoice creation | When invoices are generated |
| Mobile app transactions | Payments via Grow app |

**Common webhook payload fields:**

| Field | Description |
|-------|-------------|
| `webhookKey` | Unique webhook identifier |
| `statusCode` | Payment status code, `2` = paid (success). Branch on this server-side to confirm the payment succeeded before fulfilling; a client redirect alone is not proof |
| `transactionToken` | Saved card token, keep it to charge later via `createTransactionWithToken` for recurring/repeat billing |
| `transactionCode` | Transaction reference |
| `paymentSum` | Amount charged |
| `paymentDate` | Transaction timestamp |
| `fullName` | Payer name |
| `payerPhone` | Payer phone |
| `payerEmail` | Payer email |
| `cardSuffix` | Last 4 digits of card |
| `cardBrand` | Card brand (Visa, Mastercard, etc.) |
| `asmachta` | Reference number (asmakhta) |
| `paymentSource` | Origin (page, link, POS, etc.) |

**Recurring payment webhook (additional fields):**

| Field | Description |
|-------|-------------|
| `directDebitId` | Recurring series identifier |
| `paymentsNum` | Payment number in series |
| `allPaymentNum` | Total number of payments in the series (newer PaymentLinks payloads spell it `allPaymentsNum`) |
| `periodicalPaymentSum` | Recurring charge amount |

**Failed recurring webhook (additional fields):**

| Field | Description |
|-------|-------------|
| `error_message` | Failure reason |
| `charges_attempts` | Number of retry attempts |
| `regular_payment_id` | Failed recurring payment ID |

**Invoice webhook (set via `invoiceNotifyUrl`):**

| Field | Description |
|-------|-------------|
| `transactionCode` | Related transaction |
| `invoiceNumber` | Generated invoice number |
| `invoiceUrl` | URL to download invoice PDF |

### Step 12: 3D Secure

3DS runs on Grow's hosted payment surface, not in your server code: the page or SDK wallet presents any challenge to the cardholder, and your integration sees only the final outcome in the callback. Grow documents it on a dedicated reference page (see Reference Links).

This skill does not restate the mechanics, because which page types run a challenge, whether it is merchant-configurable, and how the liability shift applies to a server-to-server `createTransactionWithToken` charge (a merchant-initiated transaction rather than a cardholder-present one) could not be verified without a merchant account. Read the 3DS reference page before you rely on a liability-shift assumption, and do not assume a token charge inherits the 3DS status of the original payment.

### Step 13: Payment Page Types

Grow offers pre-configured payment page types, each with a different `pageCode`:

| Page Type | Description | Notes |
|-----------|-------------|-------|
| SDK Wallet | Modular JS widget | No iframe/redirect needed |
| Generic | Credit card + Bit | Customizable, up to 2 extra fields |
| Credit Card | Card payments only | Supports regular and recurring |
| Google Pay | Google Pay only | Chrome on Android; requires `allow="payment"` on iframe |
| Apple Pay | Apple Pay only | Requires domain verification for iframe |
| Bit | Bit mobile payment | Best on mobile, full-screen recommended |
| Bit QR | QR code for Bit | For desktop/in-store display |

**iframe integration:**
```html
<iframe src="PAYMENT_URL_FROM_API"
        width="100%" height="600"
        allow="payment"
        style="border: none;">
</iframe>
```

**HTTPS is mandatory** for iframe integrations. HTTP will not work.

**Keep callback URLs short.** Use `cField1`-`cField9` to carry order context instead of long query strings. (Earlier cycles cited a 2000-character limit; that figure is not stated on Grow's published documentation, and 2000 is in any case the common browser rule of thumb rather than a Grow-specific API limit.)

## Error Codes

Grow returns errors in the body with `status: 0` and an `err` object carrying a numeric `id`. The full table is on the Errors reference page (see Reference Links); the codes an integration hits most often are below. Messages are Hebrew, as returned by the API.

| Code | Meaning |
|------|---------|
| 12 | General error |
| 54 | Missing required field; the message names the field |
| 105 / 190 / 218 | Refund amount exceeds the original transaction |
| 110 | Funds already transferred to the bank; refund sent for manual approval |
| 130 / 207 | Partial refund not allowed yet (settled today, or not yet transmitted) |
| 170 | Transaction does not exist |
| 210 | Transaction already refunded |
| 271 | Bit payment above 3,600 NIS |
| 300 | This merchant is not authorised for API access |
| 617 | Transaction total does not match the sum of the products |
| 701 | Invalid identifier: `userId` / `pageCode` |
| 707 | Invalid amount |
| 709 | Link expired |
| 712 | Transaction already performed |
| 714 | Access blocked |
| 716 | Invalid transaction code or token |
| 722 | Cannot approve a transaction that was not performed or was cancelled |
| 723 | `apiKey` is a required field |
| 730 | Invalid process code or token |
| 731 | `pageCode` does not match the one the identification was made with |
| 734 | Credit transaction needs at least 3 instalments and 25 NIS |
| 736 | `paymentNum` and `maxPaymentNum` cannot be sent together |
| 763 | Invalid JSON in `productData` |
| 803 | J5 authorisation expired |
| 814 | Charge exceeds the authorised hold by more than 30 percent |
| 403 | Forbidden: `X-API-KEY` was not sent |

Codes outside this published table exist. `settleSuspendedTransaction` with an unmatched `userId` returns `err.id` 743 (`אין עסק תואם ל userId שנשלח`), and `createTransactionWithToken` with an unknown `userId` returns 104. Treat any unrecognised `err.id` as a failure and surface `err.message` rather than assuming success.

## Gotchas
- The most common integration mistake: Grow's API requires `multipart/form-data` for all requests, NOT `application/json`. Sending JSON does not produce a content-type error. The fields simply never parse, so you get a validation error about the first missing field (typically `err.id` 707, invalid amount), and agents then go hunting for a bug in the amount.
- Every response is HTTP 200, including every failure. An agent that checks `response.ok` or the status code will treat a declined or rejected call as a success. Branch on the body's `status` field (`1` success, `0` failure) and on `err`.
- `err` is an object `{id, message}` for validation failures but the plain string `"unknown method"` when the endpoint name is not recognised. Type-check before reading `err.id`.
- All Grow API requests must originate from a server, but not because the API returns 403 to a browser. It answers a request carrying a browser `Origin` and `Referer` normally; what stops client-side use is that the API sends no CORS headers, so the browser blocks the response. The symptom is a CORS console error, not a 403. A real 403 from Grow means an `X-API-KEY` header was not sent.
- `cardToken` and `transactionToken` are not card data, but they ARE bearer credentials: anyone holding a `cardToken` can charge that card through your merchant account. Never log them, never put them in a URL or in client-side code, and encrypt them at rest. The hosted-page, iframe and payment-link patterns exist so raw card numbers never touch your server; do not accept, log, or proxy a PAN yourself.
- Amounts are Israeli shekels. The Bit ceiling (3,600) and the credit floor (25) in Grow's error table are both NIS. The API exposes no currency parameter in the calls this skill covers, so do not assume a foreign-currency charge can be expressed by changing `sum`.
- `paymentNum` and `maxPaymentNum` are mutually exclusive: sending both returns `err.id` 736. `maxPaymentNum` is also rejected on a standing-order page (739) and on an account configured for regular payments only (740).
- Bit has a per-transaction ceiling: `err.id` 271 is returned for a Bit payment above 3,600 NIS. A credit (kredit) transaction has its own floor, `err.id` 734: minimum 3 instalments and 25 NIS.
- After receiving a payment webhook, you MUST call `approveTransaction` to close the loop. Agents often skip this step, which leaves transactions in a pending state in Grow's system.
- Payment page URLs expire after 10 minutes. Agents may store and reuse a URL across sessions, leading to blank pages or errors.

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|---------|
| HTTP 403 Forbidden | `X-API-KEY` header was not sent. This is the cause Grow's own error table gives for 403 | Send the `X-API-KEY` header on the calls that require it |
| Browser request fails, no 403 seen | The API sends no CORS headers, so the browser blocks reading the response. Verified: a request carrying a browser `Origin` and `Referer` is answered normally | Move the call server-side. Do not go looking for a 403; the symptom is a CORS console error |
| `err.id` 707 "invalid amount" on a request whose amount is fine | Likeliest cause is a JSON body: the fields never parse, so the first validation check fails on the amount. Not confirmed to be the only trigger | Switch to `multipart/form-data` (FormData) and re-send |
| `err.id` 54 on `approveTransaction` | Only one of the two required identifiers was sent | Send BOTH `transactionId` and `transactionToken` from the callback |
| `err.id` 54 on `cancelBitTransaction` | The endpoint is keyed by process, not transaction | Send `processId` and `processToken`, not `transactionId` |
| `{"err":"unknown method"}` | The endpoint name does not exist on the Light API. `getTokenOnly`, `updatePaymentLink` and `updateRecurringPayment` all return this on both hosts | Use a live endpoint; see Step 9 and the Error Codes section |
| Every call "succeeds" but nothing happens | Branching on the HTTP status. Every response is HTTP 200, including failures | Branch on the body's `status` field and on `err` |
| Payment page URL expired (`err.id` 709) | The link has passed its validity window. The commonly-cited window is 10 minutes, but that figure is not confirmed on Grow's published docs | Call `createPaymentProcess` again for a fresh URL |
| Webhook not received | Webhooks not enabled | Contact `apisupport@grow.business` to enable |
| Transaction not found | Wrong environment | Ensure sandbox transactions are queried against sandbox URL |
| Recurring charge failed | Expired card | Enable premium recurring for automatic card expiry updates |
| localhost in successUrl | Not allowed | Use a tunnel (ngrok) or deployed URL for testing |
| iframe blank on HTTP | HTTPS required | Serve your page over HTTPS |
| Apple Pay iframe fails | Domain not verified | Complete Apple domain verification via Grow dashboard |

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Grow 3DS Reference | https://developers.grow.business/reference/3ds-1 | How 3DS behaves and where the liability shift applies |
| Grow Errors Table | https://developers.grow.business/reference/errors | The full numeric error-code table |
| Grow API Reference | https://developers.grow.business/reference/overview | Current endpoints, transactionTypes indices, request/response shapes |
| Grow Documentation | https://developers.grow.business/docs | Tokenization, recurring, J-code installments, webhooks |
| Grow Product Overview | https://developers.grow.business/docs/about-grow-products | Which Grow products exist and how they map to API surface |
| Meshulam (Grow) Production Base | https://secure.meshulam.co.il/ | Confirms production host; do not point production traffic at sandbox.meshulam.co.il |
| Wix Integration Guide | https://support.wix.com/en/article/connecting-grow-by-meshulam-as-a-payment-provider | High-level integration walkthrough for Wix merchants |