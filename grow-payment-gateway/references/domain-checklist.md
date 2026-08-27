# Domain Checklist: grow-payment-gateway

Scope: integrate the Grow by Meshulam Light API (payments, tokens, recurring, links, refunds, invoices, webhooks). Category: tax-and-finance (payments/dev skill).

## Must cover (core)
- Correct base URLs (sandbox.meshulam.co.il / secure.meshulam.co.il) + /api/light/server/1.0/ path; multipart/form-data; server-side only.
- Auth credentials (userId, pageCode, apiKey).
- createPaymentProcess required params + integration patterns (iframe/redirect/SDK/link/token).
- The MANDATORY approveTransaction step after the webhook (and when NOT to call it).
- Tokenization + recurring (createTransactionWithToken with cardToken/paymentType=2/paymentNum, recurringDebitId, updateDirectDebit). There is no getTokenOnly and no updateRecurringPayment on the Light API.
- Refunds (refundTransaction) + Bit cancellation (cancelBitTransaction).
- Payment links, J4J5 delayed payments (settleSuspendedTransaction).
- Webhooks: webhookKey-based payload (no signature header), field set, trigger options.
- transactionTypes: the array index selects the slot (0 Credit Card, 1 Bit, 2 Apple Pay, 3 Google Pay, 4 Bank transfer, 5 Pay Box) AND the value is an integer method code (1 / 6 / 13 / 14 / 15, Pay Box defaults to 5). SDK-wallet pages only. The v1.2.1 claim that there are no numeric value-codes was wrong and was reverted in v1.4.0.
- Gotchas: JSON-vs-FormData, server-side-only, 10-minute URL expiry, approveTransaction.

## Should cover (advanced)
- Payment page types, installments (paymentNum/maxPaymentNum), invoice webhooks, premium recurring (card-expiry update).

## Out of scope (explicit)
- Cardcom (cardcom-payment-gateway), Tranzila (tranzila-payment-gateway), multi-gateway orchestration (israeli-payment-orchestrator).

## Authoritative sources
- developers.grow.business (reference/overview, createPaymentProcess, webhooks/overview-7).
- secure.meshulam.co.il (production host).


## Added 2026-08-27 (live-probe findings)

Must cover:
- Every response is HTTP 200; success is `status: 1` and failure is `status: 0` with `err`. `err` is an object for validation failures and the string "unknown method" for an unrecognised endpoint name.
- The full required-parameter set per endpoint, established by probing: approveTransaction and getTransactionInfo need transactionId AND transactionToken; getPaymentProcessInfo needs processId AND processToken; cancelBitTransaction is keyed by processId/processToken, not transactionId; refundTransaction needs transactionId + transactionToken + refundSum (not `sum`); settleSuspendedTransaction is keyed by userId, not pageCode; createTransactionWithToken also needs paymentNum.
- The endpoints that do NOT exist: getTokenOnly, updatePaymentLink, updateRecurringPayment (all return "unknown method" on sandbox AND production).
- The numeric error-code table, including 403 = X-API-KEY not sent, 271 = Bit above 3,600 NIS, 734 = credit minimum 3 payments / 25 NIS, 736 = paymentNum and maxPaymentNum are mutually exclusive.
- The real mechanism behind "server-side only": absent CORS headers, not a 403 to browsers.

Out of scope (explicit):
- createFarPaymentRequest and updateDirectDebit parameter sets. Re-litigated 2026-08-27: both endpoints are confirmed live and are now NAMED so a caller can find them, but their full parameter sets were not established by probing and are not asserted here. A user would plausibly ask, so this is a candidate for the next cycle rather than a permanent exclusion.
- Grow pricing and merchant fees. Re-litigated 2026-08-27: still out of scope. Fees are contractual per merchant and are not published in the API docs, so any figure would be unsourceable. The orchestrator skill carries a hedged cross-gateway range.

## Expert findings 2026-08-27

Addressed this cycle: callback forgery (re-verify server-to-server and match the amount before fulfilling), idempotency and the timeout-retry rule tied to err.id 712, the unverifiable consequences of skipping approveTransaction stated as unverified rather than guessed, 3DS pointed at Grow's own reference page with the MIT/CIT caveat, the three err shapes and the string/number `status`, getPaymentLinkInfo's required paymentLinkProcessToken, token-as-bearer-credential and PCI handling, and ILS-only amounts.

Deferred to the next cycle (recorded so they are not lost):
- Reconciliation and missed-webhook fallback: polling cadence against pending orders, Grow's webhook retry policy, and what the endpoint must return for delivery to count as successful. None of this is published in the pages this cycle could read.
- Sandbox test cards and whether sandbox credentials are distinct from production ones.
- How to refund a token/recurring charge, where the refund endpoint is pageCode-keyed but the charge is userId-keyed.
- How to cancel a Grow-managed recurring series (API vs dashboard).
- The Israeli invoice-allocation regime as it applies to Grow-issued documents.
- Whether createPaymentProcess genuinely requires pageField[fullName] and pageField[phone]; the required-parameter table and the helper script disagree and a probe should settle it.
