# Grow API Endpoints Reference

## Base URLs

| Environment | URL |
|-------------|-----|
| Sandbox | `https://sandbox.meshulam.co.il` |
| Production | `https://secure.meshulam.co.il` |

## Authentication

All requests require:
- `userId` -- Merchant identifier
- `pageCode` -- Payment page configuration identifier
- `apiKey` -- API key (for multi-business accounts)

## Request Format

- **Method:** POST (all endpoints)
- **Content-Type:** multipart/form-data
- **Server-side only.** Not because a browser request is rejected (the API answers one carrying `Origin` and `Referer` normally) but because the API sends no CORS headers, so the browser blocks reading the response.

## Response Format

Every response is **HTTP 200**, including every failure. Success is `status: 1`; failure is `status: 0` with an `err`. `err` is an object `{"id": N, "message": "..."}` for validation failures and the plain string `"unknown method"` when the endpoint name is unrecognised. Branch on the body, never on the HTTP status, and type-check `err` before reading `err.id`. The full numeric code table is at https://developers.grow.business/reference/errors .

## Endpoints

### Payment Processing

| Endpoint | Path | Description |
|----------|------|-------------|
| Create Payment Process | `/api/light/server/1.0/createPaymentProcess` | Create hosted payment page, returns URL |
| Approve Transaction | `/api/light/server/1.0/approveTransaction` | Confirm receipt of server callback (mandatory). Requires `pageCode` + `transactionId` + `transactionToken` |
| Get Transaction Info | `/api/light/server/1.0/getTransactionInfo` | Query transaction details. Requires `pageCode` + `transactionId` + `transactionToken` |
| Get Payment Process Info | `/api/light/server/1.0/getPaymentProcessInfo` | Query payment process details. Requires `pageCode` + `processId` + `processToken` |
| Create Far Payment Request | `/api/light/server/1.0/createFarPaymentRequest` | Exists on both hosts; not covered by this skill, read its reference page |

### Payment Links

| Endpoint | Path | Description |
|----------|------|-------------|
| Create Payment Link | `/api/light/server/1.0/createPaymentLink` | Generate shareable payment URL |
| Get Payment Link Info | `/api/light/server/1.0/getPaymentLinkInfo` | Query payment link details |

### Tokenization & Recurring

| Endpoint | Path | Description |
|----------|------|-------------|
| Create Transaction With Token | `/api/light/server/1.0/createTransactionWithToken` | Charge a saved token. Uses `userId` (not `pageCode`) and also requires `paymentNum` |
| Update Direct Debit | `/api/light/server/1.0/updateDirectDebit` | Modify a direct-debit series (the live replacement for the non-existent `updateRecurringPayment`) |
| Get Token Transactions | `/api/light/server/1.0/getTokenTransactionsByExternalIdentifiers` | Lookup token transactions |

### Refunds

| Endpoint | Path | Description |
|----------|------|-------------|
| Refund Transaction | `/api/light/server/1.0/refundTransaction` | Refund a card transaction. Requires `pageCode` + `transactionId` + `transactionToken` + `refundSum` (the amount parameter is `refundSum`; `sum` is not accepted) |
| Cancel Bit Transaction | `/api/light/server/1.0/cancelBitTransaction` | Cancel a Bit payment. Keyed by PROCESS: requires `pageCode` + `processId` + `processToken` |

### Delayed Payments (J4J5)

| Endpoint | Path | Description |
|----------|------|-------------|
| Settle Suspended Transaction | `/api/light/server/1.0/settleSuspendedTransaction` | Settle a delayed J4J5 payment. Keyed by `userId` (NOT `pageCode`), plus `transactionId` + `transactionToken` + `sum` |

## Payment Methods (transactionTypes) -- SDK-wallet pages only

The array INDEX selects the slot and the VALUE is an integer method code. Earlier versions of this reference asserted there were no numeric value-codes; the `createPaymentProcess` schema on the official reference page contradicts that, declaring each entry `"type": "integer"` with a documented example value.

| Parameter | Method | Documented value |
|-----------|--------|------------------|
| `transactionTypes[0]` | Credit Card | `1` |
| `transactionTypes[1]` | Bit | `6` |
| `transactionTypes[2]` | Apple Pay | `13` |
| `transactionTypes[3]` | Google Pay | `14` |
| `transactionTypes[4]` | Bank transfer | `15` |
| `transactionTypes[5]` | Pay Box | defaults to `5` |

## Page Code Types

| Type | Description |
|------|-------------|
| SDK Wallet | Modular JS widget (no iframe) |
| Generic | Credit card + Bit, customizable |
| Credit Card | Card payments only |
| Google Pay | Google Pay only (Chrome/Android) |
| Apple Pay | Apple Pay only (requires domain verification) |
| Bit | Bit mobile payment |
| Bit QR | QR code for Bit payments |


## Endpoints that do NOT exist on the Light API

Probed 2026-08-27 against both `sandbox.meshulam.co.il` and `secure.meshulam.co.il`. Each returns `{"err":"unknown method","status":"0","data":{"message":"מתודה לא קיימת"}}`, which is the router's response for an unrecognised method name, and is distinct from the permission errors (300, 714, 715) a real-but-unauthorised endpoint returns.

| Name | Use instead |
|------|-------------|
| `getTokenOnly` | Run a payment through a tokenization-configured page code and take the token from the callback |
| `updatePaymentLink` | Create a replacement payment link |
| `updateRecurringPayment` | `updateDirectDebit` |
