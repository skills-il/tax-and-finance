# Domain Checklist: grow-payment-gateway

Scope: integrate the Grow by Meshulam Light API (payments, tokens, recurring, links, refunds, invoices, webhooks). Category: tax-and-finance (payments/dev skill).

## Must cover (core)
- Correct base URLs (sandbox.meshulam.co.il / secure.meshulam.co.il) + /api/light/server/1.0/ path; multipart/form-data; server-side only.
- Auth credentials (userId, pageCode, apiKey).
- createPaymentProcess required params + integration patterns (iframe/redirect/SDK/link/token).
- The MANDATORY approveTransaction step after the webhook (and when NOT to call it).
- Tokenization + recurring (createTransactionWithToken, recurringDebitId, updateRecurringPayment).
- Refunds (refundTransaction) + Bit cancellation (cancelBitTransaction).
- Payment links, J4J5 delayed payments (settleSuspendedTransaction).
- Webhooks: webhookKey-based payload (no signature header), field set, trigger options.
- transactionTypes is a positional array, SDK-wallet only (NOT numeric codes).
- Gotchas: JSON-vs-FormData, server-side-only, 10-minute URL expiry, approveTransaction.

## Should cover (advanced)
- Payment page types, installments (paymentNum/maxPaymentNum), invoice webhooks, premium recurring (card-expiry update).

## Out of scope (explicit)
- Cardcom (cardcom-payment-gateway), Tranzila (tranzila-payment-gateway), multi-gateway orchestration (israeli-payment-orchestrator).

## Authoritative sources
- grow-il.readme.io (reference/overview, createPaymentProcess, webhooks/overview-7).
- secure.meshulam.co.il (production host).
