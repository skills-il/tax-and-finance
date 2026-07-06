---
name: cardcom-payment-gateway
description: Integrate Cardcom payment processing and Israeli invoice generation into applications, covering Low Profile payments, tokenization, recurring billing, and automatic tax invoice/receipt creation per Israeli law. Use when user asks to accept payments via Cardcom, generate Israeli invoices with payments, set up "slikat ashrai" with hashbonit, handle recurring billing (hora'ot keva), or mentions "Cardcom", "CardCom API", "Low Profile", Israeli payment with invoicing, or needs combined payment plus document generation. Targets the REST API V11. Do NOT use for Tranzila integration (use tranzila-payment-gateway), general accounting, or non-payment queries.
license: MIT
---

# Cardcom Payment Gateway

## Overview

Cardcom is an Israeli payment processor with a unique strength: integrated invoice and receipt generation compliant with Israeli tax law. While other Israeli gateways handle only the payment, Cardcom can automatically generate tax invoices (hashbonit mas) and receipts (kabala) as part of the payment flow, something Israeli businesses are legally required to issue.

This skill guides integration with Cardcom's REST API V11 for payments, tokenization, recurring billing, and document generation. Every endpoint and field name in this skill is taken from the official Cardcom V11 OpenAPI specification.

**Official docs:** `https://secure.cardcom.solutions/Api/v11/Docs` (interactive API reference with the full OpenAPI schema). V11 is the current API as of 2026; there is no public V12.

**Support center:** `https://support.cardcom.solutions`

**Cardcom in the Israeli landscape:** competes with Tranzila, Israpay, and Bit Business. Cardcom's pricing in 2026 is roughly 1.2-1.4% per transaction with optional monthly plans starting around 59 NIS/month for the invoicing add-on; exact numbers are quoted per merchant. The distinguishing feature for Israeli businesses remains the built-in tax document generation. For Tranzila integration use the `tranzila-payment-gateway` skill instead.

## Instructions

### Step 1: Choose Integration Pattern

| Pattern | Card Data Handling | Best For |
|---------|-------------------|----------|
| **Low Profile (iframe/redirect)** | Cardcom handles card entry | Most integrations, minimal PCI scope (SAQ-A) |
| **Transaction (server-to-server)** | Raw card data or token | Charging stored tokens, recurring billing |
| **CreateDocument (server-to-server)** | No card data | Standalone invoice/receipt generation |

Most Israeli merchants use **Low Profile** for the initial payment plus token creation, then the **Transaction** endpoint with the stored token for recurring charges. All payment flows can auto-generate invoices by attaching a `Document` object.

### Step 2: Set Up Authentication

Cardcom API V11 credentials:
- `TerminalNumber` (integer) -- your terminal ID (use `1000` for testing)
- `ApiName` (string) -- API username
- `ApiPassword` (string) -- API password (required only for refunds and document creation; not sent on a normal charge)

**Test environment:**
Terminal `1000` with the demo `ApiName` allows API testing without real charges. Test card: `4580000000000000`, any future expiry, CVV `123`.

Store credentials securely, never in source code or client-side JavaScript.

### Step 3: Implement the Payment Flow

#### Low Profile Integration (Recommended)

This is a two-step process.

**Step 3a: Create the payment page**

```
POST https://secure.cardcom.solutions/api/v11/LowProfile/Create
Content-Type: application/json

{
  "TerminalNumber": 1000,
  "ApiName": "your-api-name",
  "Operation": "ChargeAndCreateToken",
  "ReturnValue": "unique-order-id",
  "Amount": 100.00,
  "SuccessRedirectUrl": "https://example.com/success",
  "FailedRedirectUrl": "https://example.com/failed",
  "WebHookUrl": "https://example.com/webhook",
  "ISOCoinId": 1,
  "Language": "he",
  "Document": {
    "DocumentTypeToCreate": "TaxInvoiceAndReceipt",
    "Name": "Customer Name",
    "Email": "customer@example.com",
    "Products": [
      { "Description": "Product name", "UnitCost": 100.00, "Quantity": 1 }
    ]
  }
}
```

The response is a `CreateLowProfileResponse`: check `ResponseCode == 0` (success), read `Description` on failure. On success it returns `LowProfileId` (save it) and `Url` (redirect the customer there or embed as an iframe). `UrlToBit` and `UrlToPayPal` are also returned when those methods are enabled on your terminal.

The `Operation` field controls behaviour: `ChargeOnly` (default), `ChargeAndCreateToken`, `CreateTokenOnly`, `SuspendedDeal`, `Do3DSAndSubmit`.

**Step 3b: Get the results**

After payment completes, Cardcom calls your `WebHookUrl`, or you query:

```
POST https://secure.cardcom.solutions/api/v11/LowProfile/GetLpResult
{
  "TerminalNumber": 1000,
  "ApiName": "your-api-name",
  "LowProfileId": "id-from-step-3a"
}
```

The response is a `LowProfileResult`: check `ResponseCode == 0`. On success it carries `TranzactionInfo` (transaction details), `TokenInfo` (the stored `Token` plus `CardMonth`/`CardYear`), `DocumentInfo` (the generated document), and `SuspendedInfo` (for suspended deals). Each nested object is `null` when not applicable.

#### Alternative Payment Methods

The Low Profile response includes URLs for alternative payment methods when enabled on your terminal:

| Method | Response Field | Notes |
|--------|---------------|-------|
| **Bit** | `UrlToBit` | Israel's most popular mobile payment app, routed through Cardcom |
| **PayPal** | `UrlToPayPal` | International payments |
| **Apple Pay** | rendered inside the hosted Low Profile page | Listed on `cardcom.solutions` as a supported wallet on the hosted payment page |
| **Google Pay** | rendered inside the hosted Low Profile page | Same as Apple Pay, surfaced as a wallet button on the Low Profile page |

`UrlToBit` and `UrlToPayPal` are explicit URL fields you can show alongside the card form. Apple Pay and Google Pay surface as wallet buttons inside the hosted Low Profile page itself once enabled on the terminal, so no separate URL field is exposed. Enable each method on your terminal in the Cardcom admin panel before relying on it in production.

### Step 4: Generate Israeli Tax Documents

Cardcom's standout feature is automatic document generation with payments. This is critical for Israeli businesses because tax law requires issuing proper documents for every transaction.

The document type is set with the **`DocumentTypeToCreate`** field, a STRING enum (not an integer). Common values:

| Value | Hebrew | English | When to Use |
|-------|--------|---------|-------------|
| `Auto` | --- | Auto | Default; uses your admin-panel configuration |
| `TaxInvoiceAndReceipt` | hashbonit mas / kabala | Tax Invoice + Receipt | B2C with payment (most common) |
| `TaxInvoice` | hashbonit mas | Tax Invoice | B2B, when receipt is issued separately |
| `Receipt` | kabala | Receipt | Payment confirmation only |
| `TaxInvoiceAndReceiptRefund` | --- | Tax Invoice + Receipt Refund | Reversing a `TaxInvoiceAndReceipt` |
| `TaxInvoiceRefund` | --- | Tax Invoice Refund | Reversing a `TaxInvoice` |
| `ReceiptRefund` | --- | Receipt Refund | Reversing a `Receipt` |
| `ProformaInvoice` | hashbonit iska / proforma | Proforma Invoice | Pre-sale quote document |
| `DonationReceipt` | kabalat trumot | Donation Receipt | Registered non-profits |

The full enum (`DocumentToCreate` in the OpenAPI schema) also includes `Quote`, `Order`, `OrderConfirmation`, `DeliveryNote`, `DemandForPayment`, `ProformaDealInvoice`, `ReceiptForTaxInvoice`, `CouponDocumentAndReceipt`, and their `*Refund` variants. Verify the exact value you need against the official docs at `https://secure.cardcom.solutions/Api/v11/Docs`.

**Include a document in a payment flow:**
Add the `Document` object to your Low Profile `Create` or `Transaction` request. Cardcom generates the document automatically when the payment succeeds.

**Standalone document creation:**

```
POST https://secure.cardcom.solutions/api/v11/Documents/CreateDocument
{
  "ApiName": "your-api-name",
  "ApiPassword": "your-api-password",
  "Document": {
    "DocumentTypeToCreate": "TaxInvoice",
    "Name": "Customer Ltd",
    "TaxId": "123456789",
    "Email": "customer@example.com",
    "IsSendByEmail": true,
    "Languge": "he",
    "ISOCoinID": 1,
    "Products": [
      { "Description": "Web development services", "UnitCost": 5000.00, "Quantity": 1 }
    ]
  }
}
```

The response is a `DocumentInfo`: check `ResponseCode == 0`, then read `DocumentType`, `DocumentNumber`, `AccountId`, and `DocumentUrl` (link to the PDF).

Note the real V11 field spellings inside the `Document` object: `DocumentTypeToCreate` (string enum), `Name` (the "document To", required, max 50 chars), `TaxId` (business registration or ID number, replaces the older `VAT_Number`), `IsSendByEmail` (replaces `SendByEmail`), `Languge` (the official V11 field spelling, missing the second `a`), `ISOCoinID` (replaces `CoinID`), `IsVatFree`, and `Products[]` with `Description`, `UnitCost`, `Quantity`, `IsVatFree`. See `references/document-types.md` for the complete field list.

### Step 5: Implement Token-Based Recurring Payments

For subscriptions and recurring billing (hora'ot keva), Cardcom supports two flavours:

- **Card-based recurring**, charging a stored credit-card `Token` on a schedule. Covered in this step.
- **MASAV bank standing orders**, debiting the customer's Israeli bank account directly. Managed through the `RecuringPayments` endpoints (`RecuringPayments/GetRecurringPayment`, `GetRecurringPaymentHistory`, `IsBankNumberValid`). Use this when the customer prefers a bank debit over a card charge or when the card is unavailable. The Cardcom dashboard provisions the underlying instruction.

For card-based recurring:

1. **Create a token during the first payment.** Use Low Profile with `Operation: "ChargeAndCreateToken"` (or `"CreateTokenOnly"`). The `LowProfileResult` returns `TokenInfo` with `Token`, `CardMonth`, `CardYear`, and `TokenExDate` (the date the token is purged from Cardcom).

2. **Store the token securely.** Save the `Token` string, card expiry, and last 4 digits. The token is bound to your terminal.

3. **Charge the token** via the Transaction endpoint:

```
POST https://secure.cardcom.solutions/api/v11/Transactions/Transaction
{
  "TerminalNumber": 1000,
  "ApiName": "your-api-name",
  "Token": "token-uuid",
  "CardExpirationMMYY": "1227",
  "Amount": 99.00,
  "ISOCoinId": 1,
  "Document": {
    "DocumentTypeToCreate": "TaxInvoiceAndReceipt",
    "Name": "Subscriber Name",
    "Email": "customer@example.com",
    "IsSendByEmail": true,
    "Products": [
      { "Description": "Monthly subscription", "UnitCost": 99.00, "Quantity": 1 }
    ]
  }
}
```

The response is a `TransactionInfo`: check `ResponseCode == 0` (note `700` and `701` also count as success for J2/J5 validation-only transactions), then read `TranzactionId`, `Token`, `DocumentNumber`, and `DocumentUrl`. Each token charge can automatically generate and email an invoice when a `Document` object is attached.

### Step 6: Process Refunds

Refund a transaction by its Cardcom transaction id:

```
POST https://secure.cardcom.solutions/api/v11/Transactions/RefundByTransactionId
{
  "ApiName": "your-api-name",
  "ApiPassword": "your-api-password",
  "TransactionId": 219282004,
  "PartialSum": 100.00,
  "CancelOnly": false,
  "AllowMultipleRefunds": false
}
```

`ApiPassword` is required for refunds. `PartialSum` refunds part of the transaction (omit it to refund the full amount). `CancelOnly: true` voids a transaction before it is deposited. The response is a `RefundByTransactionIdResp`: check `ResponseCode == 0`, then read `NewTranzactionId` (the id of the refund transaction).

To issue the matching credit document, call `Documents/CreateDocument` with a refund `DocumentTypeToCreate` such as `TaxInvoiceAndReceiptRefund` or `TaxInvoiceRefund`.

### Step 7: Suspended Deals (Deferred Charges)

A suspended deal authorizes a payment intent without an immediate charge:

1. Create a Low Profile session with `Operation: "SuspendedDeal"`.
2. The `LowProfileResult` returns `SuspendedInfo` with a `SuspendedDealId`.
3. Charge the suspended deal later through the Cardcom admin panel or the `SuspendedDeals/Charge` endpoint (the `SuspendedDeals` group also exposes `Cancel` and `GetSuspendedDealInfo`).

Useful for pre-authorizations and services billed after delivery. Verify the exact `SuspendedDeals/Charge` request fields against the official docs before wiring the charge-later call.

### Step 8: Handle Errors

Every V11 endpoint returns a `ResponseCode` integer and a `Description` string. `ResponseCode == 0` means success; any non-zero value is a developer/transaction error and `Description` carries the human-readable reason.

```python
import requests

resp = requests.post(
    "https://secure.cardcom.solutions/api/v11/Transactions/Transaction",
    json=payload,
).json()

if resp.get("ResponseCode") == 0:
    deal_id = resp["TranzactionId"]
else:
    log_error(f"Cardcom error {resp.get('ResponseCode')}: {resp.get('Description')}")
```

Always check both the HTTP status (200 means the request was received) AND `ResponseCode` (0 means the operation succeeded). The official docs at `https://secure.cardcom.solutions/Api/v11/Docs` carry the full numeric error reference; do not hardcode error-code-to-message mappings, read `Description` instead. See `references/api-responses.md` for the handling pattern.

## Examples

### Example 1: E-commerce Checkout with Invoice
User says: "I need to accept payments on my Israeli e-commerce site and generate tax invoices automatically"
Actions:
1. Choose Low Profile with `DocumentTypeToCreate: "TaxInvoiceAndReceipt"`.
2. Create the Low Profile page via `LowProfile/Create` with product details in the `Document` object.
3. Implement a `WebHookUrl` handler that calls `LowProfile/GetLpResult`.
Result: Customer pays and receives an automatic hashbonit mas/kabala emailed as a PDF.

### Example 2: Monthly SaaS Subscription
User says: "I run a SaaS product, I need to charge users 149 NIS monthly and send them invoices"
Actions:
1. First payment: `LowProfile/Create` with `Operation: "ChargeAndCreateToken"`.
2. Store the `Token`, `CardMonth`, `CardYear` from `TokenInfo`.
3. Monthly cron: `Transactions/Transaction` with the token and a `Document` object for each billing cycle.
Result: Automated recurring billing with monthly invoice generation.

### Example 3: Standalone Invoice Without Payment
User says: "I need to generate a tax invoice for a bank transfer payment I already received"
Actions:
1. Use `Documents/CreateDocument` (no payment processing).
2. Set `DocumentTypeToCreate: "TaxInvoice"`.
3. Include `Name`, `TaxId`, `Products[]`, set `IsSendByEmail: true` with the customer email.
Result: Tax invoice generated and emailed without credit card processing.

### Example 4: Process a Refund with Credit Note
User says: "Customer wants a refund for order #5678, need to issue a credit note too"
Actions:
1. Call `Transactions/RefundByTransactionId` with `TransactionId` and `ApiPassword`.
2. Check `ResponseCode == 0` and read `NewTranzactionId`.
3. Call `Documents/CreateDocument` with `DocumentTypeToCreate: "TaxInvoiceAndReceiptRefund"`.
Result: Refund processed and the matching credit document generated.

### Example 5: Accept Bit, Apple Pay, and Google Pay
User says: "I want to let customers pay with Bit, Apple Pay, and Google Pay in addition to credit cards"
Actions:
1. Enable each method (Bit, Apple Pay, Google Pay) on your Cardcom terminal via the dashboard.
2. Create a Low Profile session as usual via `LowProfile/Create`.
3. Display `UrlToBit` from the response alongside the card form. Apple Pay and Google Pay surface as wallet buttons inside the Low Profile page itself, no extra URL needed.
Result: Customers can choose between credit card, Bit, Apple Pay, and Google Pay, same webhook flow.

## Community Libraries

- **@tsdiapi/cardcom** (TypeScript/Node.js) -- V11 API client with payments, refunds, tokenization, transaction queries. Install: `npm install @tsdiapi/cardcom`
- **CardCom/OpenFields-FrontEnd-React** (React) -- official OpenFields example. See `https://github.com/CardCom/OpenFields-FrontEnd-React`
- **CardCom/OpenFields-Backend-Node** (Node.js) -- official Node.js backend example. See `https://github.com/CardCom/OpenFields-Backend-Node`

## Reference Links

| Resource | URL |
|----------|-----|
| V11 API documentation (OpenAPI reference) | `https://secure.cardcom.solutions/Api/v11/Docs` |
| Cardcom support center | `https://support.cardcom.solutions` |
| OpenFields React example | `https://github.com/CardCom/OpenFields-FrontEnd-React` |
| OpenFields Node.js example | `https://github.com/CardCom/OpenFields-Backend-Node` |

## Bundled Resources

### References
- `references/api-endpoints.md` -- Cardcom REST API V11 endpoint reference: LowProfile, Transactions, Documents, RecuringPayments, Financial, and CompanyOperations paths with their key request/response fields. Consult when building API integrations.
- `references/api-responses.md` -- the V11 `ResponseCode` + `Description` response pattern, the per-operation response objects, and the recommended error-handling flow. Consult when debugging failed API calls.
- `references/document-types.md` -- the `DocumentTypeToCreate` string enum, the `Document` object field list, and VAT handling per Israeli tax law. Consult when determining which document type to generate.

### Scripts
- `scripts/validate_cardcom_response.py` -- Validates a Cardcom V11 API response: checks `ResponseCode`, surfaces `Description`, and verifies expected fields for transaction, token, and document operations. Run: `python scripts/validate_cardcom_response.py --help`

## Gotchas
- The V11 success check is `ResponseCode == 0`, NOT `DealResponse == 0`. `DealResponse` does not exist in V11; agents trained on older Cardcom examples invent it. Every V11 endpoint returns `ResponseCode` plus a `Description` string.
- `DocumentTypeToCreate` is a STRING enum (`"TaxInvoiceAndReceipt"`, `"TaxInvoice"`, `"Receipt"`, ...), not an integer code. Integer document codes like `101` or `400` belong to legacy `.aspx` interfaces, not V11.
- The `TerminalNumber` must be sent as an integer, not a string. Agents commonly wrap it in quotes.
- `ApiPassword` is required for `RefundByTransactionId` and `CreateDocument`, but is NOT sent on a normal `LowProfile/Create` or `Transaction` charge.
- Watch the real V11 field spellings: `Languge` (missing the second `a`) inside the `Document` object, `ISOCoinID` / `ISOCoinId`, `IsSendByEmail` (not `SendByEmail`), `TaxId` (not `VAT_Number`).
- The current Israeli VAT rate is 18% (effective January 2025; the January 2026 budget proposal to raise it to 19% was rejected). Cardcom calculates VAT server-side, so document amounts are treated per the `IsVatFree` flag.
- **PCI scope**: hosted Low Profile keeps you in SAQ-A. Server-to-server `Transaction` with raw `CardNumber`/`CVV2` lands in SAQ-D. PCI DSS v4.0 became mandatory March 2025, so prefer Low Profile or tokens unless you have a real reason to touch raw card data.
- **Settlement timing** is configured on the terminal, not per request. Weekly settlement deposits on the Wednesday following the transaction; monthly settlement deposits on the 6th of the following month. Don't try to set this in the API.
- **Apple Pay and Google Pay don't have separate URL fields** like `UrlToBit` / `UrlToPayPal`. They surface as wallet buttons inside the hosted Low Profile page once enabled on the terminal in the admin panel.

## Troubleshooting

### Error: a non-zero `ResponseCode` on `LowProfile/Create`
Cause: a validation or authentication problem with the request.
Solution: Read the `Description` string in the response, it names the exact issue. Verify `TerminalNumber` is an integer and `ApiName` is correct. The full numeric error reference is at `https://secure.cardcom.solutions/Api/v11/Docs`.

### Error: "Low Profile page loads but payment fails"
Cause: often a `WebHookUrl` or redirect URL issue.
Solution: Ensure `SuccessRedirectUrl`, `FailedRedirectUrl`, and `WebHookUrl` are publicly accessible HTTPS URLs. Localhost URLs do not work, use a tunnel (ngrok) for development.

### Error: "Refund returns a non-zero `ResponseCode`"
Cause: `ApiPassword` missing, or the transaction is already deposited and you sent `CancelOnly: true`.
Solution: Include `ApiPassword` on every refund request. Use `CancelOnly: true` only before deposit; after deposit, send a real refund (omit `CancelOnly` or set it `false`).

### Error: "Invoice created but not emailed"
Cause: `IsSendByEmail` not set or email address missing.
Solution: Set `IsSendByEmail: true` and include a valid `Email` in the `Document` object. Check spam folders, Cardcom sends from its own domain.

### Error: "Token charge succeeds but no invoice"
Cause: `Document` object missing from the `Transaction` request.
Solution: Include the full `Document` object with `DocumentTypeToCreate`, `Name`, and `Products` in every token charge. Document generation is opt-in per transaction.
