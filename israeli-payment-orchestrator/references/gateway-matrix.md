# Israeli Payment Gateway Comparison Matrix

Cross-gateway view only. For field names, error codes and endpoint paths on a single gateway, the dedicated skill for that gateway is the authority: `cardcom-payment-gateway`, `tranzila-payment-gateway`, `grow-payment-gateway`, `pelecard-payment-gateway`. PayMe and iCredit have no dedicated skill, which is why several of their cells below read "unverified".

"Unverified" means no public source establishes the answer either way. It is not a soft "no".

## API Integration Details

### Cardcom
- **Base URL:** `https://secure.cardcom.solutions/api/v11/` (the version segment is part of every path)
- **Auth:** `ApiName` + `ApiPassword` (per terminal)
- **Format:** REST JSON
- **Tokenization:** Yes (card token for recurring)
- **Hosted page:** `LowProfile/Create` returns a `Url` you can redirect to or embed as an iframe
- **Bit:** Yes. `CreateLowProfileResponse.UrlToBit` is an explicit URL field, returned once Bit is enabled on the terminal
- **Apple Pay / Google Pay:** Yes. The v11 `ExtPaymentMethod` enum lists `ApplePay` and `GooglePay`
- **Money unit:** decimal shekels
- **3D Secure:** Supported
- **Webhook:** POST callback on transaction completion
- **Test vs live:** terminal and credentials, confirm the arrangement with Cardcom
- **Schema:** https://secure.cardcom.solutions/swagger/v11/swagger.json

### Tranzila
- **Base URL:** four distinct surfaces, with non-transferable parameter names. `direct.tranzila.com/{supplier}/iframenew.php` (iframe), `secure5.tranzila.com/cgi-bin/*.cgi` (legacy CGI), `api.tranzila.com/v1` (API V2), plus Hosted Fields
- **Auth:** terminal name + password on the legacy surface; a four-header HMAC-SHA256 handshake on API V2 (`X-tranzila-api-app-key`, `X-tranzila-api-request-time`, `X-tranzila-api-nonce`, `X-tranzila-api-access-token`). A request carrying only the app key is rejected
- **Format:** form-encoded key-value on the legacy CGI (the response is a query string, not JSON); REST JSON on API V2
- **Tokenization:** Yes (`TranzilaTK`)
- **Hosted page:** iframe, redirect or Hosted Fields
- **Bit:** Yes, through a dedicated Bit API with its own Init and Refund endpoints; `bit_pay=1` also adds Bit to the iframe
- **Apple Pay / Google Pay:** Yes. The iframe parameter page documents `apple_pay=1` and `google_pay=1`
- **Money unit:** decimal shekels
- **3D Secure:** Supported, with its own endpoint and code space on API V2. Bit does not run through 3DS
- **Webhook:** notify page. Parameter name differs by product: `notify_url_address` on the iframe, `notify_url` on Hosted Fields, the 3DS API and Bit
- **Documentation:** https://docs.tranzila.com/

### PayMe
- **Base URL:** `https://ng.paymeservice.com/api/`
- **Auth:** `payme_client_key`, which the API itself names when the parameter is missing
- **Format:** REST JSON
- **Tokenization:** unverified
- **Hosted page:** unverified
- **Bit:** unverified
- **Money unit:** unverified. Confirm with a 1-shekel test charge before going live
- **3D Secure:** unverified
- **Webhook:** unverified

Only the API host and the existence of the `refund-sale` route were confirmed here, by probe against a negative control. Every other line above is unverified in BOTH directions, because PayMe publishes no reachable API reference and has no dedicated skill in this catalog.
- **Documentation:** not publicly reachable. `payme.io/developers` redirects to the homepage and `docs.paymeservice.com` answers a Cloudflare 1014, so request the API reference from PayMe directly (https://payme.io/)

### Meshulam (Grow)
- **Base URL:** `https://secure.meshulam.co.il/api/light/server/1.0/`
- **Auth:** endpoint-dependent. `refundTransaction` is keyed by `pageCode`; `createTransactionWithToken` by `userId`; `cancelBitTransaction` by `processId`
- **Format:** multipart/form-data (NOT JSON), server-side only
- **Tokenization:** Yes
- **Hosted page:** iframe + redirect
- **Bit:** Yes. `cancelBitTransaction` exists on the Light API (probed; a fabricated method name on the same base returns `unknown method`), so there is a Bit flow with its own cancellation path
- **Apple Pay:** unverified
- **Money unit:** decimal shekels
- **3D Secure:** Supported
- **Webhook:** POST callback
- **Error convention:** HTTP 200 with `status: "0"` and an `err` object on failure
- **Documentation:** https://developers.grow.business/reference/overview

### iCredit
- **Base URL:** `https://icredit.rivhit.co.il/API/`
- **Auth:** unverified
- **Format:** WCF `.svc` service, not a REST JSON API
- **Tokenization:** unverified
- **Hosted page:** unverified
- **Bit:** unverified
- **Money unit:** unverified. Confirm with a 1-shekel test charge before going live
- **3D Secure:** unverified
- **Webhook:** POST callback
- **Documentation:** https://www.rivhit.co.il/ (iCredit is a Rivhit product; the API surface is not publicly documented in the way the other five are)

### Pelecard
- **Base URL:** `https://gateway21.pelecard.biz/`. `gateway20` is the older generation and returns byte-identical responses, so the hostname is NOT an environment switch. What decides whether a call is a test or a real charge is the terminal number and credentials
- **Auth:** terminal number + user + password
- **Format:** REST JSON
- **Tokenization:** Yes
- **Hosted page:** redirect or iframe
- **Bit:** documented in `pelecard-payment-gateway`, not re-verified here. Pelecard's own service index carries no Bit service, so treat the constraints as terminal configuration to confirm with the acquirer
- **Apple Pay:** documented in `pelecard-payment-gateway` via ClientSecure.js, not re-verified here
- **Money unit:** agorot, minor units. See `pelecard-payment-gateway`
- **3D Secure:** Supported
- **Webhook:** POST callback, validated with `ConfirmationKey`
- **Endpoint index:** https://gateway21.pelecard.biz/services

## Installment (Tashlumim) Support

Installment ceilings are terminal and issuer configuration rather than a gateway constant. Ask the acquirer for the ceiling on the specific terminal instead of hard-coding one.

| Gateway | Regular (CreditType 8) | Issuer credit (CreditType 6) | Notes |
|---------|------------------------|------------------------------|-------|
| Cardcom | Yes | Yes | `NumOfPayments` on the transaction |
| Tranzila | Yes | Yes | `cred_type` plus `npay` / `fpay` / `spay` on the legacy surface; `payment_plan` plus `installments_number` on API V2. Pass either the npay group or `maxpay`, never both |
| PayMe | unverified | unverified | No reachable API reference |
| Meshulam (Grow) | Yes | Yes | `paymentNum` for a fixed count, `maxPaymentNum` to let the customer choose. Credit transactions carry their own minimum instalment count and amount; see `grow-payment-gateway` |
| iCredit | unverified | unverified | API surface not publicly documented |
| Pelecard | Yes | Yes | `MaxPayments` / `MinPaymentsForCredit`; there is no CreditType field |

There is no routable "club installments" value. See the CreditType section below.

## Authorize, Capture and Release

An authorization holds the amount without collecting it. Releasing one is a DIFFERENT call from voiding a sale, and using the sale-reversal call on a hold is a common and expensive mix-up. Each cell below is taken from that gateway's own dedicated skill in this repo; confirm the exact parameter set there before wiring it.

| Gateway | Authorize | Capture | Release the hold |
|---------|-----------|---------|------------------|
| Cardcom | `Operation: SuspendedDeal` on the Low Profile / transaction call | charge the suspended deal | see `cardcom-payment-gateway` |
| Tranzila | `verify_mode=5` (API) or `tranmode=V` (legacy CGI) | `txn_type=force` | `txn_type=reversal`, NOT `cancel` |
| PayMe | unverified | unverified | unverified |
| Meshulam (Grow) | unverified | unverified | unverified |
| iCredit | unverified | unverified | unverified |
| Pelecard | `ActionType: J5` (or `J5h`) | post a debit carrying the `authorizationNumber` | `/services/DeleteIshur` by `debitTrxId`, NOT `DeleteTran` |

An authorization recorded as "approved" and never captured collects nothing, and the hold expires quietly. On Pelecard the wrong `ActionType` silently changes whether money moves at all.

## Transaction lookup, for reconciling a parked unknown outcome

When a charge times out the outcome is unknown, and the gateway's own transaction id does not exist yet, so you must look the transaction up by a key YOU sent. Persist that key before the call.

Two different kinds of key appear below. A **correlator** identifies one attempt and is unique per attempt. An **idempotency key** is what the gateway dedupes on and must stay stable across retries of the same logical charge. Sending a fresh value where the gateway expects a stable one defeats its duplicate detection.

| Gateway | Look up with | Key you must have sent first |
|---------|--------------|------------------------------|
| Cardcom | `Transactions/ListTransactions` over a date range (requires `ApiPassword`) | your own external deal id |
| Tranzila | the transaction-reports API | your own reference |
| PayMe | `api/get-sales` (exists; parameters unverified) | unverified |
| Meshulam (Grow) | `getTokenTransactionsByExternalIdentifiers` | `transactionUniqueIdentifier`: an IDEMPOTENCY KEY, stable per logical charge, re-sent unchanged on a retry |
| iCredit | unverified | unverified |
| Pelecard | `PaymentGW/GetTransaction`; `/services/GetTransDataBeforeBc` for anything not yet broadcast | `ParamX`: a CORRELATOR, unique per attempt as `<order-id>-<attempt-n>`, reconciled by prefix match |

## Void, Refund and Partial Refund

| Gateway | Void, before settlement | Refund / credit, after | Partial refund |
|---------|------------------------|------------------------|----------------|
| Cardcom | `Transactions/RefundByTransactionId` with `CancelOnly: true`, documented as "cancellation only, before deposit of the transaction" | same endpoint without `CancelOnly` | Yes, `PartialSum`. `AllowMultipleRefunds` defaults to false |
| Tranzila | `txn_type=cancel` on API V2 | legacy `tranmode=C{index}` with the separate `CreditPass` credential and `authnr`; `txn_type=credit` on API V2 referencing `reference_txn_id` | Yes |
| PayMe | unverified | `api/refund-sale` exists | unverified |
| Meshulam (Grow) | no card void; Bit only, via `cancelBitTransaction`, which requires `pageCode` | `refundTransaction`, amount field is `refundSum` (`sum` is rejected) | Yes, but blocked on a settled or transmitted transaction, and once funds are at the bank it needs manual approval. See `grow-payment-gateway` for the codes |
| iCredit | unverified | unverified | unverified |
| Pelecard | `/services/DeleteTran`, while the batch is open. `/services/GetTransDataBeforeBc` lists what is still voidable | no refund endpoint exists on `/PaymentGW`; a credit is a new opposite transaction whose path is not publicly documented | No, `DeleteTran` is whole-transaction |

A void never settles, so it carries no clearing fee. A credit clears in its own right, so a charge-then-refund is paid for twice.

## Settlement Timing

Settlement schedules are contractual per merchant and none of the six publishes a general T+N figure. Cardcom publishes calendar cycles rather than T+N (monthly, weekly, bi-monthly), and the others state nothing publicly. Ask the acquirer for the merchant's actual cycle rather than assuming a number.

What matters operationally is not the payout date but the **batch close**, because that is what decides whether a reversal is a void or a credit. On most terminals the batch closes the same business day.

## Pricing

None of the six publishes a rate card. The merchant discount rate is contractual and quoted per merchant. This file deliberately carries no fee table, and `scripts/compare_gateways.py` deliberately does no cost estimation. Earlier versions of this file carried per-gateway bands that no vendor stands behind; they were removed rather than re-hedged.

## CreditType (סוג אשראי) Reference

CreditType is distinct from the transaction type (סוג עסקה) and from gateway-level refund operations.

| CreditType | Type | Hebrew | Description |
|------|------|--------|-------------|
| 1 | Single payment | תשלום אחד | One immediate charge |
| 6 | Issuer credit | קרדיט | The card company finances; the customer repays it with interest |
| 8 | Regular installments | תשלומים | Merchant is paid in full, the issuer collects monthly from the customer |

**These three are the only values published by a vendor.** Cardcom's v11 schema documents `CreditType` as "1 - Single payment / 6 - Credit payments / 8 - Regular payments", and Tranzila's current iframe parameter table publishes the identical three.

Values `2`, `3`, `4`, `5` and `9` circulate in third-party integration libraries and appeared in earlier versions of this file as a "canonical enum". They are in no current vendor parameter table, Cardcom's schema contains none of them, and Tranzila rejects them with an unauthorized-credit-type error. Club and issuer-loyalty programmes are a terminal and acquirer configuration, not a value your code selects.

## Pelecard callback status codes that decide whether money moved

Pelecard publishes the message for any status code through a credential-free lookup at `/services/GetErrorMessageEn` (parameter `errorCode`). The three codes that matter most to an orchestrator, quoted verbatim from that lookup on 2026-08-27, are:

| Code | Pelecard's own message | What it means for the orchestrator |
|------|------------------------|-------------------------------------|
| `301` | Session to Pelecard Timed Out | Outcome unknown |
| `302` | Debit was successful but merchant is not responding | The debit SUCCEEDED |
| `303` | Merchant is not responding | Outcome unknown |

Only `302` asserts that money moved. Mapping all three to "failed, try the next gateway" is the classic duplicate-charge bug. An unassigned code returns Pelecard's own misspelled `UnkownError`, which is how the lookup distinguishes a real code from a fabricated one.
