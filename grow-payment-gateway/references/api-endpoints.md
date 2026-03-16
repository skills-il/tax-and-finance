# Grow API Endpoints Reference

## Base URLs

| Environment | URL |
|-------------|-----|
| Sandbox | `https://sandbox.meshulam.co.il` |
| Production | `https://api.meshulam.co.il` |

## Authentication

All requests require:
- `userId` -- Merchant identifier
- `pageCode` -- Payment page configuration identifier
- `apiKey` -- API key (for multi-business accounts)

## Request Format

- **Method:** POST (all endpoints)
- **Content-Type:** multipart/form-data
- **Server-side only** (client-side requests are blocked)

## Endpoints

### Payment Processing

| Endpoint | Path | Description |
|----------|------|-------------|
| Create Payment Process | `/api/light/server/1.0/createPaymentProcess` | Create hosted payment page, returns URL |
| Approve Transaction | `/api/light/server/1.0/approveTransaction` | Confirm receipt of server callback (mandatory) |
| Get Transaction Info | `/api/light/server/1.0/getTransactionInfo` | Query transaction details |
| Get Payment Process Info | `/api/light/server/1.0/getPaymentProcessInfo` | Query payment process details |

### Payment Links

| Endpoint | Path | Description |
|----------|------|-------------|
| Create Payment Link | `/api/light/server/1.0/createPaymentLink` | Generate shareable payment URL |
| Update Payment Link | `/api/light/server/1.0/updatePaymentLink` | Modify existing payment link |
| Get Payment Link Info | `/api/light/server/1.0/getPaymentLinkInfo` | Query payment link details |

### Tokenization & Recurring

| Endpoint | Path | Description |
|----------|------|-------------|
| Get Token Only | `/api/light/server/1.0/getTokenOnly` | Save card as token without charging |
| Create Transaction With Token | `/api/light/server/1.0/createTransactionWithToken` | Charge a saved token |
| Update Recurring Payment | `/api/light/server/1.0/updateRecurringPayment` | Modify recurring series |
| Get Token Transactions | `/api/light/server/1.0/getTokenTransactionsByExternalIdentifiers` | Lookup token transactions |

### Refunds

| Endpoint | Path | Description |
|----------|------|-------------|
| Refund Transaction | `/api/light/server/1.0/refundTransaction` | Refund credit card transaction |
| Cancel Bit Transaction | `/api/light/server/1.0/cancelBitTransaction` | Cancel Bit payment |

### Delayed Payments (J4J5)

| Endpoint | Path | Description |
|----------|------|-------------|
| Settle Suspended Transaction | `/api/light/server/1.0/settleSuspendedTransaction` | Settle a delayed J4J5 payment |

## Payment Method Codes (transactionTypes)

| Code | Method |
|------|--------|
| 1 | Credit Card |
| 5 | Pay Box |
| 6 | Bit |
| 13 | Apple Pay |
| 14 | Google Pay |
| 15 | Bank Transfer |

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
