# Grow API Endpoints Reference

Re-verified 2026-11-11 against the official reference (developers.grow.business) and by live probes with invalid input (no merchant account, no charge).

## Hosts

| Host | Use |
|------|-----|
| `https://sandbox.meshulam.co.il/api/light/server/1.0/` | Light API, sandbox (Testing Environment page) |
| `https://secure.meshulam.co.il/api/light/server/1.0` | Light API, production (Transition to Production page) |
| `https://sandboxapi.grow.link` | Payment-link management (CreatePaymentLink, UpdatePaymentLink, SetAccountDetails), sandbox. Grow's pages give no production host for these; obtain it from Grow |

## Authentication

- Direct business: `userId` + `pageCode`.
- Platform / system integrator acting for several businesses: also `apiKey` (error 723 when missing, 812 when invalid).
- Payment-link endpoints on `sandboxapi.grow.link`: `X-API-KEY` header (403 "X-API-KEY not sent" when missing).
- Each environment has its own identifiers.

## Request and response format

- POST, `multipart/form-data`, server-side only (the API sends no CORS headers).
- Every response is HTTP 200 on the `meshulam.co.il` hosts. Success is `status: 1`; failure is `status: 0` with `err`. `err` is an object `{"id": N, "message": "..."}` or the string `"unknown method"`. See `error-codes.md`.

## Light API endpoints (`/api/light/server/1.0/`)

| Endpoint | Required parameters | Notes |
|----------|--------------------|-------|
| `createPaymentProcess` | `pageCode`, `userId`, `sum`, `successUrl`, `cancelUrl`, `description`, `pageField[fullName]`, `pageField[phone]` | `saveCardToken=1` saves the card; `chargeType=3` + `sum=1` + `saveCardToken=1` is the save-token-only flow |
| `approveTransaction` | `pageCode` plus ALL fields from the server update (the schema marks each one required; live, `transactionId` and `transactionToken` are checked first) | Not for token charges, J4J5, or save-token-only. `apiKey` for platforms |
| `getTransactionInfo` | `pageCode`, `transactionId`, `transactionToken` | |
| `getPaymentProcessInfo` | `pageCode`, `processId`, `processToken` | |
| `refundTransaction` | `userId` or `pageCode`, `transactionId`, `transactionToken`, `refundSum` | `stopDirectDebit=1` stops the series. 724 when neither `userId` nor `pageCode` is sent |
| `cancelBitTransaction` | `pageCode`, `processId`, `processToken` | Documented at `/api/light/andriod/1.0/cancelBitTransaction/`; the `/server/1.0/` path answers the same way |
| `createTransactionWithToken` | `userId`, `cardToken`, `sum`, `description`, `paymentType`, `paymentNum` (live: omitting it returns 54), `pageField[fullName]`, `pageField[phone]`, `transactionUniqueIdentifier` | `paymentType` 1 recurring / 2 regular / 4 installments; `transactionGroupIdentifier` optional; premium recurring adds `isRecurringDebitPayment=1` (first) or `recurringDebitId` (later) |
| `updateDirectDebit` | `userId`, `transactionId`, `transactionToken`, `asmachta` | Optional `changeStatus` (1 active, 2 canceled), `sum`, `paymentNum`, `chargeDay`, `fullName`, `phone`, `email`, `updateCard` |
| `getTokenTransactionsByExternalIdentifiers` | `userId`, `cardToken`, and ONE of `transactionUniqueIdentifier` / `transactionGroupIdentifier` | Both identifiers at once returns 1012 |
| `settleSuspendedTransaction` | `userId`, `transactionId`, `transactionToken`, `sum` | J4J5 capture |
| `getPaymentLinkInfo` | `pageCode`, `paymentLinkProcessId`, `paymentLinkProcessToken` (schema) | Its schema lists both the meshulam and grow.link sandbox hosts |
| `createFarPaymentRequest` | not established | Exists on both hosts; not covered |
| `updateMyUrl` (GET, sandbox) | `url` query parameter | Sends a sample server-to-server callback to your URL |

## Payment-link endpoints (`sandboxapi.grow.link`)

| Endpoint | Required parameters (per the reference schema) | Notes |
|----------|-----------------------------------------------|-------|
| `POST /api/light/server/1.1/CreatePaymentLink` | `userId`, `pageCode`, `paymentLinkType`, `isActive`, `title`, `paymentTypes[0][type]`, `paymentTypes[0][payments][paymentsPaymentNum]` or `[paymentsMaxPaymentNum]`, `pageFieldSettings[fullName][value]`, `pageFieldSettings[phone][value]`, per product `products[data][N][name]`, `[price]`, `[vatType]` | No `sum` field. Path is case-sensitive |
| `POST /api/light/server/1.0/UpdatePaymentLink` | `pageCode`, `isActive`, `paymentLinkProcessId`, `paymentLinkProcessToken` | `X-API-KEY` header |

The `meshulam.co.il` hosts also answer a `createPaymentLink` method with a different, undocumented contract (asks for `sum`, then `pageCode`, then `userId`). Do not build on it.

## Payment methods (transactionTypes), SDK-wallet pages only

| Parameter | Method | Documented value |
|-----------|--------|------------------|
| `transactionTypes[0]` | Credit Card | `1` |
| `transactionTypes[1]` | Bit | `6` |
| `transactionTypes[2]` | Apple Pay | `13` |
| `transactionTypes[3]` | Google Pay | `14` |
| `transactionTypes[4]` | Bank transfer | `15` |
| `transactionTypes[5]` | Pay Box | defaults to `5` |

## Methods that do NOT exist

Each returns `{"err":"unknown method","status":"0","data":{"message":"מתודה לא קיימת"}}` on both `meshulam.co.il` hosts (re-probed 2026-11-11).

| Name | Use instead |
|------|-------------|
| `getTokenOnly` | `createPaymentProcess` with `chargeType=3`, `sum=1`, `saveCardToken=1` |
| `updateRecurringPayment` | `updateDirectDebit` |
| `updatePaymentLink` / `UpdatePaymentLink` on `meshulam.co.il` | `UpdatePaymentLink` on `sandboxapi.grow.link` (earlier versions of this skill wrongly said link updates were impossible) |
