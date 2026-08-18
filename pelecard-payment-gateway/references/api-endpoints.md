# Pelecard API Endpoints

This reference documents the Pelecard endpoints surfaced by the legacy iframe gateway and the third-party PHP wrapper that most Israeli merchants integrate against. Pelecard also publishes a newer "Match API" REST surface (`match-api.pelecard.biz`); the public docs page for it was not retrievable during research, so verify endpoint shape directly with Pelecard before relying on it.

## Hosts

| Environment | Host | Purpose |
|------|------|---------|
| Sandbox | `gateway20.pelecard.biz/sandbox` | Development and testing. |
| Production | `gateway21.pelecard.biz` | Live transactions. The Pelecard WordPress plugin's "Third Party Services" disclosure lists this as the production payment API. |
| Modern REST (verify) | `match-api.pelecard.biz` | Pelecard's "Match" REST sandbox. Doc page exists but rendered empty during research. Confirm endpoint shape with vendor. |

Switch hosts at deploy time via env var. Each host has its own credentials -- prod credentials hitting sandbox (or vice versa) returns "transaction not found".

## Authentication

Every request server-to-server carries the same credentials triple:

| Field | Source |
|-------|--------|
| `terminal` | Issued by Pelecard. |
| `user` | API user. |
| `password` | API password. |

The dofinity/pelecard PHP wrapper declares them as `protected $terminal; protected $user; protected $password;`. The convention: never expose them on the client side. Keep them in server environment variables only.

## Iframe Payment Flow

The iframe flow runs in two phases.

### Phase 1: Create the payment session

| Method | Path | Purpose |
|--------|------|---------|
| POST | `PaymentGW/init` | Submit credentials + transaction params, receive `URL` + `ConfirmationKey`. (Path per the dofinity wrapper's `const PAYMENT_INIT_URI = 'PaymentGW/init'`; Gateway21 also exposes a REST `/services` surface. Confirm the exact path for your terminal in the Pelecard Postman "Gateway21" collection.) |

Request fields (subset; see `payment-parameters.md` for the full set):

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `terminal` | string | yes | Server-side credential. |
| `user` | string | yes | Server-side credential. |
| `password` | string | yes | Server-side credential. |
| `ActionType` | string | no | `J2` / `J4` (default) / `J5` / `J5h`. |
| `Currency` | int | no | `1` = ILS (default). Other codes (USD/EUR/GBP) exist but the integer mapping is not consistently documented across Pelecard's API surfaces; verify the exact integer for your terminal in the live Postman workspace before sending non-ILS amounts. |
| `Total` | int | yes | Minor units (agorot) on Gateway21. Send `9900` for ₪99.00. The dofinity wrapper documents `FirstPayment` as "in agorot/cents"; the same convention applies to `Total`. Confirm against your sandbox terminal before going live. |
| `MaxPayments` / `MinPayments` | int | no | Tashlumim controls. |
| `GoodURL` / `ErrorURL` / `CancelURL` | URL | no | Browser redirect destinations. |
| `ServerSideGoodFeedbackURL` / `ServerSideErrorFeedbackURL` | URL | no | Server-to-server IPN destinations. |
| `ParamX` / `ShopNo` / `UserKey` | string | no | Custom passthrough. Echoed back on lookup. |
| `CreateToken` / `TokenForTerminal` | bool / string | no | Tokenization controls. |
| `IsToken` / `TokenCreditCardDigits` | bool / string | no | Charge a saved token. |

Response fields:

| Field | Type | Notes |
|-------|------|-------|
| `URL` | URL | Pelecard-hosted iframe / redirect URL. |
| `ConfirmationKey` | string | Use to verify the callback later. |

### Phase 2: Receive the callback

After the customer pays, Pelecard hits your `ServerSideGoodFeedbackURL` (or `ServerSideErrorFeedbackURL`) with the result.

Callback fields (subset):

| Field | Notes |
|-------|-------|
| `PelecardStatusCode` | The literal string `"000"` indicates success per Pelecard convention; any other value is an error. Treat `"0"` / `"00"` as malformed and verify the callback was not truncated or coerced. |
| `ConfirmationKey` | Compare byte-for-byte against the value you stored from phase 1, then re-verify via `PaymentGW/GetTransaction`. |
| `PelecardTransactionId` | Use as your IPN dedupe key (Pelecard may deliver the same IPN twice on a timeout retry) AND as the lookup key for `PaymentGW/GetTransaction`. |
| `Total` / `Currency` | Echoes from phase 1. Compare the authoritative `DebitTotal` from `PaymentGW/GetTransaction`, not the callback's `Total`. |
| `ParamX` / `ShopNo` / `UserData*` | Passthrough fields you sent in phase 1. `ParamX` is your merchant-side order correlation ID, NOT an idempotency key. |
| `ShvaResultEmv` | EMV / 3DS result code. The Pelecard plugin v1.4.19 changelog: "Added Emv errors in order notes. ShvaResultEmv parameter". |

You MUST re-verify the callback by calling `PaymentGW/GetTransaction` server-to-server before treating the order as paid. Pelecard does NOT sign IPN deliveries with HMAC, so the server-to-server lookup is the only authoritative source.

## Transaction Lookup: `PaymentGW/GetTransaction`

| Method | Path | Purpose |
|--------|------|---------|
| POST | `PaymentGW/GetTransaction` | Look up a Pelecard transaction by ID. |

`PaymentGW/GetTransaction` is a Gateway21 lookup endpoint (confirmed in Pelecard's Postman "Gateway21" collection). Note: the dofinity/pelecard PHP wrapper is pinned to the legacy `gateway20` host (`const GATEWAY_BASE_URI = 'https://gateway20.pelecard.biz';`) and does its own validation via a different endpoint, `const PAYMENT_VALIDATE_URI = 'PaymentGW/ValidateByUniqueKey';` (posting `ConfirmationKey`, `UniqueKey`, and `TotalX100`). Both are valid server-side re-verification paths; on Gateway21 use `PaymentGW/GetTransaction` with the credentials triple plus the transaction id:

```json
{
  "terminal": "<terminal>",
  "user": "<user>",
  "password": "<password>",
  "TransactionId": "<PelecardTransactionId from callback>"
}
```

Request fields:

| Field | Required |
|-------|----------|
| `terminal` | yes |
| `user` | yes |
| `password` | yes |
| `TransactionId` | yes (from the callback `PelecardTransactionId`) |

Response fields (per the dofinity `PelecardTransaction` properties):

| Field | Notes |
|-------|-------|
| `DebitApproveNumber` | Acquirer approval number. |
| `DebitTotal` | Authoritative debited amount. |
| `VoucherId` | Internal voucher ID. |
| `Token` | Saved-card token (when `CreateToken` was true). |
| `TotalPayments` | Tashlumim count. |
| `CreditCardCompanyClearer` | Issuer / clearer. |
| `CreditCardNumber` | Masked PAN / last 4. |
| `CreditCardExpDate` | Card expiry. |
| `CardHolderID` | Cardholder ID (te'udat zehut, when applicable). |
| `FirstPaymentTotal` | First installment amount. |
| `FixedPaymentTotal` | Subsequent installment amount. |
| `UserData` | Echoed passthrough. |

Compare `DebitTotal` (in agorot) against your expected order amount. Mismatch indicates tampering, do not mark the order paid.

`DebitApproveNumber` is Shva's per-transaction approval / authorization number. End-of-day reconciliation: pull the Shva clearing report from your Pelecard merchant portal and join on `DebitApproveNumber` to confirm funds settled. Charged-but-not-settled transactions appear here.

## Refunds

Pelecard supports full and partial refunds via a server-to-server "DebitRegular cancel" / refund endpoint. The merchant calls it with `terminal/user/password/PelecardTransactionId` plus the refund `Total` (in agorot, full or partial). Pelecard returns a new `PelecardTransactionId` for the refund leg. The Pelecard plugin v1.4 changelog: "Added refund capabilities"; the exact endpoint path lives in the Pelecard Postman "Gateway21" collection. Israeli Consumer Protection Law (חוק הגנת הצרכן, סעיפים 14ג-14ה) governs distance-selling refunds: cancellation within 14 days, refund within 14 days of cancellation notice, fee capped at 5% or 100 ₪ (whichever is lower).

## Match API (modern REST -- verify)

`match-api.pelecard.biz/docs/index` is Pelecard's modern REST docs page. The rendered content was not retrievable via WebFetch during research. Treat it as the modern path Pelecard is migrating toward, and confirm endpoints, auth scheme, and request bodies directly with Pelecard before depending on it in production.
