---
name: grow-payment-gateway
description: >-
  Integrate Grow by Meshulam payment gateway into Israeli applications -- covers
  payment pages (iframe/redirect/SDK), tokenization, recurring billing, payment links,
  refunds, invoices, webhooks, and 3DS authentication via the Grow Light API. Use when
  user asks to accept payments via Grow or Meshulam, set up "slikat ashrai" with Grow,
  create payment links (drishat tashlum), handle recurring charges (hora'ot keva) via
  Grow tokens, process refunds or Bit cancellations, integrate Grow webhooks, or mentions
  "Grow", "Meshulam", "grow-il", "meshulam.co.il", Grow payment page, or Grow API. Prevents
  costly integration mistakes by guiding correct FormData request format, server-side-only
  restrictions, and the mandatory approveTransaction step that many developers miss. Do NOT
  use for Cardcom integration (use cardcom-payment-gateway), Tranzila integration (use
  tranzila-payment-gateway), general payment orchestration across multiple gateways (use
  israeli-payment-orchestrator), or non-payment queries.
license: MIT
compatibility: >-
  Requires network access for Grow API calls (sandbox.meshulam.co.il / api.meshulam.co.il).
  Works with Claude Code, Cursor, GitHub Copilot, Windsurf, OpenCode, Codex.
metadata:
  author: skills-il
  version: 1.0.0
  category: tax-and-finance
  tags:
    he:
    - תשלומים
    - סליקת-אשראי
    - גרו
    - משולם
    - דרישת-תשלום
    - ביט
    - טוקניזציה
    - חיוב-חוזר
    - ישראל
    en:
    - payments
    - credit-card
    - grow
    - meshulam
    - payment-link
    - bit
    - tokenization
    - recurring-billing
    - israel
  display_name:
    he: שער תשלומים Grow (משולם)
    en: Grow Payment Gateway (Meshulam)
  display_description:
    he: >-
      אינטגרציה עם Grow (משולם) לסליקת אשראי, דפי תשלום, טוקניזציה, חיובים חוזרים,
      דרישות תשלום, החזרים וחשבוניות -- מכסה את כל ה-API של Grow כולל Bit, Apple Pay,
      Google Pay ו-NFC
    en: >-
      Integrate Grow by Meshulam payment gateway into Israeli applications -- covers
      payment pages (iframe/redirect/SDK), tokenization, recurring billing, payment links,
      refunds, invoices, webhooks, and 3DS authentication via the Grow Light API. Use when
      user asks to accept payments via Grow or Meshulam, set up "slikat ashrai" with Grow,
      create payment links (drishat tashlum), handle recurring charges (hora'ot keva) via
      Grow tokens, process refunds or Bit cancellations, integrate Grow webhooks, or mentions
      "Grow", "Meshulam", "grow-il", "meshulam.co.il", Grow payment page, or Grow API.
      Prevents costly integration mistakes by guiding correct FormData request format,
      server-side-only restrictions, and the mandatory approveTransaction step that many
      developers miss. Do NOT use for Cardcom integration (use cardcom-payment-gateway),
      Tranzila integration (use tranzila-payment-gateway), general payment orchestration
      across multiple gateways (use israeli-payment-orchestrator), or non-payment queries.
  supported_agents:
  - claude-code
  - cursor
  - github-copilot
  - windsurf
  - opencode
  - codex
---

# Grow Payment Gateway (Meshulam)

## Overview

Grow (formerly Meshulam) is one of Israel's leading payment gateways, powering thousands of businesses with credit card processing, Bit payments, Apple Pay, Google Pay, and more. Unlike other Israeli gateways, Grow offers a unified API (the "Light API") that covers payment pages, tokenization, recurring billing, payment links, invoices, and webhooks in a single integration.

This skill guides integration with Grow's Light API for the full payment lifecycle: accepting payments, saving tokens for recurring charges, creating payment links for invoices, processing refunds, and handling real-time webhook notifications.

**Official docs:** `https://grow-il.readme.io/`

**Developer support:** `apisupport@grow.business`

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
| Production | `https://api.meshulam.co.il` |

**Critical: Server-side only.** All API requests must originate from your server. Client-side (browser) requests are blocked by Grow.

**Critical: FormData format.** All request bodies use `multipart/form-data`, NOT JSON. This is a common mistake -- if you send `application/json`, the API will reject the request.

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
| `transactionTypes[0]` | integer | Payment method filter (see table below) |

**Payment method codes (transactionTypes):**

| Code | Payment Method |
|------|---------------|
| 1 | Credit Card |
| 5 | Pay Box |
| 6 | Bit |
| 13 | Apple Pay |
| 14 | Google Pay |
| 15 | Bank Transfer |

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
  -F "successUrl=https://yoursite.com/payment/success" \
  -F "cancelUrl=https://yoursite.com/payment/cancel" \
  -F "description=Monthly subscription" \
  -F "pageField[fullName]=Israel Israeli" \
  -F "pageField[phone]=0501234567" \
  -F "pageField[email]=customer@example.com" \
  -F "paymentNum=1" \
  -F "notifyUrl=https://yoursite.com/api/grow/webhook" \
  -F "cField1=order-12345"
```

The response includes a `url` field -- redirect the customer there or embed as an iframe.

**Important:** The payment page URL is valid for 10 minutes. Generate a fresh URL for each checkout session.

### Step 4: Handle the Payment Response

After the customer completes payment, two things happen:

1. **Client redirect:** Customer is redirected to `successUrl` with `response=success` appended
2. **Server callback:** Grow sends a POST to your `notifyUrl` with full transaction details

**Always verify via server callback**, not the client redirect (which can be spoofed).

### Step 5: Approve the Transaction (MANDATORY)

After receiving the server callback, you MUST call `approveTransaction` to confirm receipt. This does not alter the payment -- it closes the transaction loop with Grow.

**Endpoint:** `POST /api/light/server/1.0/approveTransaction`

```bash
curl -X POST https://sandbox.meshulam.co.il/api/light/server/1.0/approveTransaction \
  -F "pageCode=YOUR_PAGE_CODE" \
  -F "transactionId=TRANSACTION_ID_FROM_CALLBACK"
```

**Do NOT call approveTransaction for:** token-only saves, delayed (J4J5) transactions, or `createTransactionWithToken` charges.

### Step 6: Query Transaction Details

**Get transaction info:**

`POST /api/light/server/1.0/getTransactionInfo`

| Parameter | Type | Description |
|-----------|------|-------------|
| `pageCode` | string | Page identifier |
| `transactionId` | string | Transaction ID to query |

**Get payment process info:**

`POST /api/light/server/1.0/getPaymentProcessInfo`

| Parameter | Type | Description |
|-----------|------|-------------|
| `pageCode` | string | Page identifier |
| `processId` | string | Process ID from createPaymentProcess |

### Step 7: Process Refunds

**Refund a credit card transaction:**

`POST /api/light/server/1.0/refundTransaction`

| Parameter | Type | Description |
|-----------|------|-------------|
| `pageCode` | string | Page identifier |
| `transactionId` | string | Transaction to refund |
| `refundSum` | number | Amount to refund (partial or full) |

**Cancel a Bit transaction:**

`POST /api/light/server/1.0/cancelBitTransaction`

| Parameter | Type | Description |
|-----------|------|-------------|
| `pageCode` | string | Page identifier |
| `transactionId` | string | Bit transaction to cancel |

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

The response includes a shareable payment URL. You can also update (`updatePaymentLink`) or query (`getPaymentLinkInfo`) existing links.

### Step 9: Tokenization and Recurring Billing

Grow supports three recurring payment models:

#### Option A: Grow-Managed via Page Code

Use a dedicated recurring page code configured in the Grow dashboard:

1. Create payment with `createPaymentProcess` using the recurring page code
2. Set `sum` to the monthly charge amount and `paymentNum` to total iterations
3. Grow handles all subsequent charges automatically

#### Option B: Grow-Managed via Token

Use `createTransactionWithToken` with automatic scheduling:

```bash
curl -X POST https://sandbox.meshulam.co.il/api/light/server/1.0/createTransactionWithToken \
  -F "pageCode=YOUR_PAGE_CODE" \
  -F "userId=YOUR_USER_ID" \
  -F "sum=99.00" \
  -F "token=SAVED_TOKEN" \
  -F "paymentType=1" \
  -F "paymentNum=12"
```

Setting `paymentType=1` with `paymentNum` tells Grow to manage 12 monthly charges.

#### Option C: Merchant-Managed via Token (Full Control)

You control when each charge fires:

**First payment (save token):**

```bash
curl -X POST https://sandbox.meshulam.co.il/api/light/server/1.0/createTransactionWithToken \
  -F "pageCode=YOUR_PAGE_CODE" \
  -F "userId=YOUR_USER_ID" \
  -F "sum=99.00" \
  -F "token=SAVED_TOKEN" \
  -F "isRecurringDebitId=1"
```

The response includes `recurringDebitId` -- save this to link future charges.

**Subsequent charges:**

```bash
curl -X POST https://sandbox.meshulam.co.il/api/light/server/1.0/createTransactionWithToken \
  -F "pageCode=YOUR_PAGE_CODE" \
  -F "userId=YOUR_USER_ID" \
  -F "sum=99.00" \
  -F "token=SAVED_TOKEN" \
  -F "recurringDebitId=RECURRING_DEBIT_ID"
```

**Update recurring payment:**

`POST /api/light/server/1.0/updateRecurringPayment` -- change amount, pause, or cancel.

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

| Parameter | Type | Description |
|-----------|------|-------------|
| `pageCode` | string | Page identifier |
| `transactionId` | string | Suspended transaction to settle |

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

### Step 12: Payment Page Types

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

**URL length limit:** 2000 characters. Use `cField` values instead of long query strings.

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|---------|
| API returns 403 or empty response | Client-side request | Move API calls to your server; Grow blocks browser requests |
| Request returns parsing error | Using JSON content type | Switch to `multipart/form-data` (FormData), not `application/json` |
| Payment page URL expired | URL older than 10 minutes | Call `createPaymentProcess` again for a fresh URL |
| Webhook not received | Webhooks not enabled | Contact `apisupport@grow.business` to enable |
| Transaction not found | Wrong environment | Ensure sandbox transactions are queried against sandbox URL |
| Recurring charge failed | Expired card | Enable premium recurring for automatic card expiry updates |
| localhost in successUrl | Not allowed | Use a tunnel (ngrok) or deployed URL for testing |
| iframe blank on HTTP | HTTPS required | Serve your page over HTTPS |
| Apple Pay iframe fails | Domain not verified | Complete Apple domain verification via Grow dashboard |

## References

- [Grow API Documentation](https://grow-il.readme.io/)
- [Grow Product Overview](https://grow-il.readme.io/docs/about-grow-products)
- [API Reference](https://grow-il.readme.io/reference/overview-6)
- [Webhook Documentation](https://grow-il.readme.io/docs/overview-7)
- [Wix Integration Guide](https://support.wix.com/en/article/connecting-grow-by-meshulam-as-a-payment-provider)
