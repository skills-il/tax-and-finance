---
name: pelecard-payment-gateway
description: "Integrate Pelecard payment processing into Israeli web and mobile apps -- covers the iframe payment flow on gateway21.pelecard.biz, ActionType selection (J2/J4/J5/J5h), tashlumim (installments), tokenization, ConfirmationKey server-side validation via PaymentGW/GetTransaction, refunds, 3D Secure 2, Bit wallet, and Apple Pay via ClientSecure.js. Use when user asks to accept payments via Pelecard, set up slikat ashrai with Pelecard, validate a Pelecard callback, charge a saved Pelecard token, or mentions Pelecard, gateway21, PelecardStatusCode, or ConfirmationKey. Do NOT use for Cardcom (use cardcom-payment-gateway), Tranzila (use tranzila-payment-gateway), Grow/Meshulam (use grow-payment-gateway), multi-gateway orchestration (use israeli-payment-orchestrator), or invoice generation (use green-invoice)."
license: MIT
compatibility: Requires network access for Pelecard API calls. Works with Claude Code, Cursor, Claude Desktop, OpenAI Codex, and GitHub Copilot.
version: 1.0.2
---

# Pelecard Payment Gateway

## Problem

Pelecard is a Payment Service Provider (PSP) and one of the largest Israeli card-acquiring aggregators, but its public documentation is scattered across a Postman workspace, a sandbox UI, a WordPress plugin listing, and third-party PHP libraries, with no single canonical reference. Agents that try to integrate Pelecard end up confusing the legacy `gateway20` host with the production `gateway21`, picking the wrong `ActionType` (which silently changes whether money actually moves), or trusting a browser-side `ConfirmationKey` instead of re-verifying server-side. Each of those mistakes leaks revenue or, worse, ships an exploitable "free order" path to production.

## Overview

Pelecard is a Payment Service Provider (PSP) and one of the largest Israeli card-acquiring aggregators. Card transactions are cleared on the Israeli Shva network (https://www.shva.co.il/, שב"א, Automated Banking Services); Pelecard handles merchant onboarding, the iframe payment surface, tokenization, and reconciliation on top of that.

Pelecard's dominant integration is an iframe payment page: your server posts a credentials triple (`terminal` + `user` + `password`) plus the transaction parameters to Pelecard, gets back a `URL` and a `ConfirmationKey`, and either redirects the user there or embeds the URL as an iframe. After the customer pays, Pelecard calls your server-side feedback URL with a `PelecardStatusCode` and `ConfirmationKey`. Store the Phase-1 `ConfirmationKey` server-side keyed by your order, then on the callback you MUST (a) match the callback `ConfirmationKey` byte-for-byte to the stored value and (b) re-call `PaymentGW/GetTransaction` to confirm `DebitTotal` and `PelecardTransactionId` before treating the order as paid.

This skill is for developers, product engineers, and Israeli small-business owners integrating Pelecard for the first time. It walks through the iframe flow, server-side validation, tashlumim (installments), tokenization, recurring billing on stored tokens, refunds, 3D Secure 2, and the Bit wallet's quirks (no installments, low per-transaction cap).

The newer "Match API" REST surface at `match-api.pelecard.biz` exists, but its public docs were not retrievable during research -- treat it as the modern path and verify the endpoint shape directly with Pelecard before relying on it.

## Instructions

### Step 1: Choose Integration Pattern

| Pattern | Card Data Handling | Best For |
|---------|-------------------|----------|
| **Iframe / hosted page** (`gateway21.pelecard.biz`) | Pelecard hosts the card-entry page | Most integrations -- minimal PCI scope |
| **Charge stored token** (server-to-server) | Token only, no raw card data | Recurring billing, hora'ot keva, one-click checkout |
| **Apple Pay via ClientSecure.js** | Apple Pay handles card data, Pelecard processes | iOS/Safari customers on supported devices |
| **Bit wallet** | A2A push, no card data at all | Israeli mobile customers, single-payment, ILS only (treat 5,000 ₪ as the design ceiling unless you have written approval otherwise) |
| **Match API** (`match-api.pelecard.biz`) | Modern REST surface | Verify with vendor before using; doc page rendered empty during research |

Most Israeli merchants run an iframe checkout for the first payment (creating a token at the same time), then charge the saved token for subsequent renewals.

### Step 2: Set Up Authentication

Every Pelecard call needs a credentials triple, sent server-side only:

- `terminal` -- your terminal ID issued by Pelecard
- `user` -- API username
- `password` -- API password

These three values open your terminal to charges. They MUST live in server-side environment variables. Never embed them in browser JavaScript, mobile app bundles, or git history. The dofinity/pelecard PHP wrapper declares them as `protected $terminal; protected $user; protected $password;` -- the convention is "credentials never leave the server".

**Sandbox:** `gateway20.pelecard.biz/sandbox` for development.
**Production:** `gateway21.pelecard.biz` for live transactions.

Each environment has its own credential set. Switch hosts at deploy time via env var, not at code level.

### Step 3: Create the Iframe Payment Page

Build a request body with your credentials, the `Total` (in agorot, see "money units" note below), `Currency`, `ActionType`, and feedback URLs.

**Money fields use minor units (agorot) on Gateway21.** Send `Total: 9900` for ₪99.00, `FirstPayment: 5000` for ₪50.00 first payment. The dofinity wrapper documents `FirstPayment` as "the amount is in agorot/cents", and the same convention applies to `Total`. Confirm against your sandbox terminal before going live (do a 1 ₪ test charge) to avoid 100x errors.

The create-session path is `PaymentGW/init` (per the dofinity wrapper's `const PAYMENT_INIT_URI = 'PaymentGW/init'`); Gateway21 also exposes a REST `/services` surface. Confirm the exact path for your terminal in Pelecard's official Postman workspace (https://www.postman.com/peleteam/pelecard-public/overview, "Gateway21" collection) before going live. The request body shape (auth triple + transaction params) is documented below.

```
POST https://gateway21.pelecard.biz/PaymentGW/init
Content-Type: application/json

{
  "terminal": "<your-terminal>",
  "user": "<api-user>",
  "password": "<api-password>",
  "ActionType": "J4",
  "Currency": 1,
  "Total": 9900,
  "MaxPayments": 12,
  "MinPayments": 1,
  "GoodURL": "https://example.com/pay/success",
  "ErrorURL": "https://example.com/pay/error",
  "CancelURL": "https://example.com/pay/cancel",
  "ServerSideGoodFeedbackURL": "https://example.com/api/pelecard/ipn-success",
  "ServerSideErrorFeedbackURL": "https://example.com/api/pelecard/ipn-error",
  "ParamX": "order-2026-0042",
  "ShopNo": "main-shop",
  "CreateToken": true
}
```

Pelecard responds with a `URL` and a `ConfirmationKey`. **Persist the `ConfirmationKey` server-side keyed by your order** (you will compare it on the callback in Step 4). Then redirect the customer to that URL or embed it as an iframe.

**ActionType reference (full table in `references/payment-parameters.md`):**

| Value | Meaning |
|-------|---------|
| `J4` | Standard sale (default). Money moves now. |
| `J2` | Card validation / registration only. No charge. |
| `J5` | Authorize now, charge later. |
| `J5h` | Enhanced J5. |

Picking the wrong `ActionType` is the most common Israeli-gateway integration bug: `J2` looks identical to `J4` in the Pelecard UI but does not move money.

### Step 4: Validate the Callback Server-Side

When the customer finishes paying, Pelecard hits your `ServerSideGoodFeedbackURL` with a `PelecardStatusCode`, `ConfirmationKey`, and `PelecardTransactionId`. Before you treat the order as paid, you MUST do all of the following server-side:

1. Look up your stored Phase-1 `ConfirmationKey` for this order, and compare it byte-for-byte to the value in the callback. If they don't match, refuse the payment.
2. Re-call `PaymentGW/GetTransaction` with `terminal/user/password/TransactionId` (the `TransactionId` is the callback's `PelecardTransactionId`).
3. Confirm `DebitTotal` and `PelecardTransactionId` from the `GetTransaction` response: `DebitTotal` matches the order's expected price (in agorot) and `PelecardTransactionId` matches the callback. (The `ConfirmationKey` is matched in step 1 between your stored Phase-1 value and the callback; `GetTransaction` returns the transaction record, not the ConfirmationKey, so the amount/id match is what authenticates the lookup.)

**Pelecard does NOT sign IPN deliveries with HMAC.** Do not trust a payload that arrives with a `ConfirmationKey` you recognize without re-fetching the transaction server-side. The browser-side `ConfirmationKey` can be forged by a determined attacker; the only authoritative source is the server-to-server `GetTransaction` lookup.

The dofinity/pelecard PHP wrapper wraps these steps (note: that library is pinned to the legacy `gateway20` host and validates via `PaymentGW/ValidateByUniqueKey` posting `ConfirmationKey`/`UniqueKey`/`TotalX100`; on Gateway21 the equivalent re-verification is `PaymentGW/GetTransaction`, shown below):

```php
$PaymentResponse = new \Pelecard\PaymentResponse(
    $PelecardStatusCode, $PelecardTransactionId, '', '', $ConfirmationKey, 100
);
$payment = new \Pelecard\PelecardPayment();
$payment->setPaymentResponse($PaymentResponse);
if ($payment->ValidatePayment()) {
    // Ok. Payment has been verified
}
```

Under the hood, validation calls `PaymentGW/GetTransaction` with the credentials triple plus the `TransactionId`:

```
POST https://gateway21.pelecard.biz/PaymentGW/GetTransaction
{
  "terminal": "<terminal>",
  "user": "<user>",
  "password": "<password>",
  "TransactionId": "<PelecardTransactionId from callback>"
}
```

The response includes the authoritative `DebitTotal` (the actual amount the customer was debited, in agorot), `DebitApproveNumber` (Shva's approval number), `TotalPayments` (tashlumim count), masked card last 4, expiry, and your `ParamX` echoed back. Compare `DebitTotal` against the order's expected price; mismatch means tampering, do NOT mark the order paid.

**Idempotency / dedupe.** `ParamX` is your merchant-side order correlation ID, NOT an idempotency key. Pelecard may legitimately deliver the same IPN twice for one order (e.g., a timeout retry; v1.5.1 plugin changelog: "Fixed timeout-retry issues"). Dedupe on **`PelecardTransactionId`** (Pelecard's per-attempt transaction ID), which is unique per attempt; mark each `PelecardTransactionId` as processed in your DB so the second delivery is a no-op.

**Reconciliation safety net.** The server-side feedback URL fires only when the transaction reaches a terminal state (success or merchant-rejected error). If the customer closes the browser before submitting the card form, no IPN fires. The complete safety net is to persist the `PelecardTransactionId` from the create-session response, then run a periodic reconciliation job that polls `PaymentGW/GetTransaction` for any session that has not produced an IPN within your timeout window.

Run the bundled `scripts/validate_pelecard_response.py` against your callback payload while developing. It warns when `ConfirmationKey` or `PelecardTransactionId` is missing, and flags non-canonical (`0`/`00`) status codes.

### Step 5: Charge a Stored Token (Recurring Billing)

To bill a saved token (subscriptions, hora'ot keva), pass `IsToken=true` plus the saved `Token` and `TokenCreditCardDigits` instead of card-entry params. Subsequent charges run server-to-server with no iframe.

The first transaction sets `CreateToken: true` and Pelecard stores the token against `TokenForTerminal`. Save the token ID and the card last-4 + expiry returned in the validation response. For each renewal, post a J4 transaction with the token reference and the new `Total`. The Pelecard WordPress plugin has shipped "Saved payment methods (tokenization)" since v1.2.0 and "WooCommerce Subscriptions support" since v1.4.

**Recurring charges + 3DS (MIT exemption).** Under EMV 3DS 2.x, repeat charges on a stored token can qualify for the MIT (Merchant Initiated Transaction) exemption, meaning Shva will not step the customer up for a 3DS challenge on each renewal. Pelecard's plugin changelog references this pattern (v1.4.8: "Add 3D-Secure params to J4 after J5 requests"). Confirm the exact MIT-flag parameter for your terminal with Pelecard support before relying on the exemption; without it, recurring charges may intermittently fail with 3DS rejection errors.

### Step 6: Process Refunds

Pelecard's refund flow is exposed via a server-to-server "DebitRegular cancel" / refund endpoint (the exact path lives in the Pelecard Postman workspace, "Gateway21" collection). The merchant calls it with `terminal/user/password/PelecardTransactionId` plus the refund `Total` (full or partial, in agorot). Pelecard returns a new `PelecardTransactionId` for the refund leg; persist it against the original order.

**Israeli consumer protection law (חוק הגנת הצרכן, סעיפים 14ג-14ה)** governs distance-selling refunds: consumers may cancel within 14 days, the merchant must refund within 14 days of receiving the cancellation notice, and cancellation fees are capped at 5% of the order value or 100 ₪, whichever is lower. Build your refund flow around these legal deadlines and ship it before launch, not after. (Source: kolzchut, citing the Consumer Protection Law remote-sales chapter.)

### Step 7: Configure 3D Secure 2 and Bit

**3D Secure 2 (EMV 3DS).** The sandbox UI exposes `Initiate` and `AskForChallenge` toggles (each: `None` default, `False`, `True`). The Pelecard plugin v1.4.19 changelog notes "Added Emv errors in order notes. ShvaResultEmv parameter". Configure 3DS as mandatory for new merchants per Bank of Israel SCA expectations -- when an EMV result code lands in your callback, log it.

**Bit wallet.** Bit is a Bank-of-Israel-approved A2A wallet. Constraints to bake into the UX:

- **Single payment only.** From allpay.co.il: "No installments. You can only pay with Bit in one payment." Hide the tashlumim selector when Bit is the chosen method.
- **ILS only.** Bit only accepts shekels. Send `Currency: 1` for any Bit transaction; non-ILS Bit transactions fail with no helpful error.
- **Per-transaction cap is operator-set.** Bit's per-transaction cap is set by the merchant's Bit agreement and operator risk tier. The commonly-cited limit is 5,000 ₪ per transaction (per allpay.co.il merchant guidance: "Payment via Bit cannot exceed 5,000 shekels"), but higher-tier merchants are cleared above that. Consult your Bit merchant agreement; treat 5,000 ₪ as the design ceiling unless you have written approval otherwise.
- Bit also imposes a per-merchant monthly cap and a 10-minute customer time limit; see allpay.co.il/en/help/bit.

**Apple Pay.** Pelecard hosts the SDK at `ClientSecure.js`. The plugin lists "Apple Pay Support (optional, disabled by default) -- When enabled, loads ClientSecure.js from Pelecard servers to enable Apple Pay on supported devices."

### Step 8: Handle Errors

Pelecard returns a numeric `PelecardStatusCode` on the callback. By convention `000` is success, anything else is an error -- but the exact code-to-meaning table varies per acquirer and changes over time. EMV result codes ride alongside via `ShvaResultEmv`. See `references/error-codes.md` for the categories you'll hit (auth failure, declined, expired card, insufficient funds, 3DS challenge required, network timeout). For specific numeric codes you encounter in production, contact Pelecard support -- do not guess based on code numbers from generic Israeli-payment articles.

## Examples

### Example 1: First-Time Iframe Checkout
User says: "I want to accept credit-card payments on my Israeli site via Pelecard, with up to 12 tashlumim."
Actions:
1. Server: POST credentials + `ActionType: J4` + `Total: 9900` (₪99.00 in agorot) + `Currency: 1` + `MaxPayments: 12` to the Gateway21 create-session path `PaymentGW/init` (confirm in the Pelecard Postman workspace).
2. Receive `URL` and `ConfirmationKey`. Persist the `ConfirmationKey` server-side keyed by your order. Render the URL in an iframe (or redirect).
3. Listen on `ServerSideGoodFeedbackURL` for the callback.
4. Compare the callback `ConfirmationKey` to your stored value, then re-verify via `PaymentGW/GetTransaction` and confirm `DebitTotal` matches the order before marking the order paid.
Result: Customer pays in 1-12 tashlumim, you have a verified transaction ID.

### Example 2: Save a Card and Charge It Monthly
User says: "I run a SaaS, I need to charge users 99 ₪ every month with their saved card."
Actions:
1. First payment: iframe POST with `CreateToken: true` and `Total: 9900` (agorot). Save the returned token + last-4 + expiry.
2. Monthly cron: POST `IsToken: true` with the saved token reference and the new `Total` (in agorot).
3. Verify each charge via `PaymentGW/GetTransaction` and dedupe IPN deliveries on `PelecardTransactionId`.
4. Handle declines, expired cards, and 3DS step-up. For renewals, ask Pelecard support about MIT-flag parameters so Shva does not challenge each cycle.
Result: Recurring billing without storing a single PAN on your servers.

### Example 3: Add Bit as a Checkout Option
User says: "Most of my Israeli customers want Bit, can I add it?"
Actions:
1. Enable Bit on the Pelecard terminal (vendor-side configuration).
2. In your checkout UI, send `Currency: 1` (Bit is ILS only) and gate the Bit option to `Total <= 5,000 ₪` as the design ceiling unless your Bit agreement clears you above that.
3. Hide the tashlumim selector when Bit is chosen, Bit is single-payment only.
4. Same callback flow: compare the Phase-1 `ConfirmationKey`, then re-verify via `PaymentGW/GetTransaction` against `DebitTotal`.
Result: Bit added cleanly, no failed charges from Bit's wallet-side constraints.

### Example 4: Validate a Callback Payload Locally
User says: "My Pelecard callback came in, how do I sanity-check it before hitting GetTransaction?"
Actions:
1. Run `python scripts/validate_pelecard_response.py --response '{"PelecardStatusCode":"000","ConfirmationKey":"...","PelecardTransactionId":"...","Total":9900,"Currency":1}'`.
2. The script flags missing `ConfirmationKey` or `PelecardTransactionId`, requires the canonical `"000"` (warns on `"0"` / `"00"`), and reports parsed fields.
3. If it passes, compare the callback `ConfirmationKey` to your stored Phase-1 value, then call `PaymentGW/GetTransaction` and compare the server-returned `DebitTotal` against your order (in agorot).
Result: Quick local check before hitting the Pelecard API.

### Example 5: Authorize Now, Charge on Shipment (J5)
User says: "I want to authorize the customer's card at order time but only charge when I ship -- like Amazon."
Actions:
1. First call: `ActionType: J5`. Pelecard authorizes the card; no money moves.
2. On shipment, call the capture flow associated with your J5 transaction (verify the exact API with Pelecard support -- the plugin v1.4.8 notes "Add 3D-Secure params to J4 after J5 requests").
3. Verify the captured transaction via `PaymentGW/GetTransaction`.
Result: Auth-then-capture pattern compatible with Israeli e-commerce flows.

### Example 6: Refund a Failed Order
User says: "Customer disputed order #5678, I need to refund."
Actions:
1. Pull the original `PelecardTransactionId` from your order record (you stored it from Phase 1 / IPN).
2. Call Pelecard's refund endpoint (path lives in the Pelecard Postman "Gateway21" collection) with `terminal/user/password/PelecardTransactionId` plus the refund `Total` in agorot (full or partial).
3. Persist the new `PelecardTransactionId` Pelecard returns for the refund leg against the original order.
4. Honor the Israeli Consumer Protection Law deadlines: 14 days to refund from the cancellation notice, fee capped at 5% or 100 ₪ (whichever is lower).
5. If you issue a credit note (חשבונית זיכוי), generate it via your invoice provider, Pelecard handles the money, not the tax document.
Result: Refund processed within the legal window. Pair with `green-invoice` for the credit-note compliance side.

## Bundled Resources

### References
- `references/api-endpoints.md` -- Pelecard hosts (sandbox + prod), the iframe POST + ConfirmationKey flow, the `PaymentGW/GetTransaction` lookup, and a note on the modern Match API. Consult when wiring up a new endpoint.
- `references/payment-parameters.md` -- Full parameter reference: ActionType (J2/J4/J5/J5h), Currency codes, tashlumim, tokenization, BIN controls, UI customization, server-side feedback URLs, custom passthrough fields. Consult when building the iframe request body.
- `references/error-codes.md` -- Categories of Pelecard status codes and EMV/Shva result codes (ShvaResultEmv). Consult when debugging a failed callback.

### Scripts
- `scripts/validate_pelecard_response.py` -- Validates a Pelecard callback JSON: checks `PelecardStatusCode`, confirms `ConfirmationKey` and `PelecardTransactionId` are present, sanity-checks `Total` and `Currency`, and warns when `ConfirmationKey` is missing (the most dangerous case). Run: `python scripts/validate_pelecard_response.py --help`.

## Recommended MCP Servers

No Pelecard MCP exists yet. Pair with the `green-invoice` skill for invoice generation after charge, since Pelecard handles the money but not the Israeli tax document (חשבונית מס).

## Reference Links

| Source | Purpose |
|--------|---------|
| https://www.postman.com/peleteam/pelecard-public/overview | Pelecard's official Postman workspace ("Gateway21" collection). Verify request bodies and example payloads here. |
| https://gateway20.pelecard.biz/sandbox | Official Pelecard sandbox + parameter reference. ActionType, currency, 3DS, Bit/Apple Pay/Google Pay toggles. |
| https://wordpress.org/plugins/woo-pelecard-gateway/ | Pelecard-authored WooCommerce plugin. Confirms `gateway21.pelecard.biz` host, refunds, subscriptions, tokenization, Apple Pay via ClientSecure.js. |
| https://github.com/dofinity/pelecard | Third-party PHP wrapper. Documents the full `PaymentRequest` parameter set, the `ConfirmationKey` validation flow, and `PaymentGW/GetTransaction`. |
| https://match-api.pelecard.biz/docs/index | Pelecard "Match" REST sandbox (modern surface). Verify endpoint shape with vendor before relying. |
| https://www.allpay.co.il/en/help/bit | Bit wallet constraints: 5,000 ILS per-transaction cap, no installments, single-payment only, 10-minute customer window. |

## Gotchas

- **Wrong ActionType silently changes whether money moves.** `J2` is for card registration only and does not charge, but the merchant UI looks identical to `J4`. Default to `J4` unless you specifically want validation-only. Plugin v1.4.7 changelog notes a dedicated bypass: "Bypass validation for J2 transactions."
- **Pelecard does NOT sign IPN deliveries with HMAC.** The only protections against a forged callback are: (a) re-verify every callback via `PaymentGW/GetTransaction` server-to-server, (b) optionally restrict your `ServerSideGoodFeedbackURL` / `ServerSideErrorFeedbackURL` to Pelecard's outbound IP allowlist (request the current list from Pelecard support), (c) enforce TLS 1.2+ on those endpoints. Never trust a payload that arrives with a `ConfirmationKey` you recognize without re-fetching the transaction server-side.
- **Compare `DebitTotal`, not `Total`, on the GetTransaction response.** The authoritative debited amount on the lookup response is `DebitTotal` (per the dofinity `PelecardTransaction` class properties). `Total` is the request-side echo; `DebitTotal` is what actually moved.
- **`PelecardTransactionId` is your IPN dedupe key, not `ParamX`.** Pelecard may legitimately deliver the same IPN twice for one order (timeout retries). `ParamX` is your merchant-side order correlation ID and may match across both deliveries; `PelecardTransactionId` is unique per attempt. Mark each `PelecardTransactionId` as processed in your DB.
- **Bit's no-installments rule is absolute, the 5,000 ₪ cap is operator-tier-set.** From allpay.co.il: "No installments. You can only pay with Bit in one payment." 5,000 ₪ per transaction is the commonly-cited limit ("Payment via Bit cannot exceed 5,000 shekels") and a safe design ceiling, but higher-tier merchants are cleared above it. Hide the tashlumim selector and gate the Bit option to the cap your merchant agreement allows. Bit also rejects non-ILS, send `Currency: 1`.
- **Sandbox vs production host swap.** `gateway20.pelecard.biz/sandbox` is sandbox, `gateway21.pelecard.biz` is production. Each has its own credentials. Set the host via env var, not a code-level constant, otherwise prod deploys hit sandbox or vice versa.
- **Sandbox terminals are issued on request.** Many Israeli merchants end up "testing" against production with a 1 ₪ live charge because they forgot to ask Pelecard support for a sandbox terminal. Email `support@pelecard.co.il` for a sandbox before integrating; never put production credentials in a `.env.local` shared with the dev team.
- **`terminal` + `user` + `password` are server-side only.** Leaking the triple opens your terminal to anyone. The dofinity wrapper declares them as `protected` properties and posts them only from server code. Never embed them in browser JS, native app bundles, or build artifacts.
- **Money fields use minor units (agorot) on Gateway21.** Send `Total: 9900` for ₪99.00, `FirstPayment: 5000` for ₪50.00. The dofinity wrapper documents `FirstPayment` as "in agorot/cents" and the same convention applies to `Total`. Confirm against your sandbox terminal with a 1 ₪ test charge before going live.

## Troubleshooting

### Error: Callback received but `PaymentGW/GetTransaction` returns "transaction not found"
Cause: Querying production endpoint with sandbox credentials, or sandbox endpoint with production credentials. Each env keeps its own ledger.
Solution: Match the host to the credentials. Use `gateway20.pelecard.biz/sandbox` only with sandbox credentials and `gateway21.pelecard.biz` only with production credentials.

### Error: `ConfirmationKey` missing from callback
Cause: Either the customer abandoned mid-flow (browser closed before iframe completed) or the request was tampered with.
Solution: Treat the order as unpaid. Pelecard's `ServerSideGoodFeedbackURL` is the source of truth for completed payments -- if `ConfirmationKey` is missing, do NOT mark the order paid even if `PelecardStatusCode` looks like success.

### Error: Bit payment fails for amounts above 5,000 ₪
Cause: Bit's per-transaction cap is set by the merchant's Bit agreement and operator risk tier; 5,000 ₪ is the commonly-cited default. Higher-tier merchants are cleared above that.
Solution: Treat 5,000 ₪ as the design ceiling unless you have written approval otherwise. Gate the Bit option in your checkout UI based on the cap your Bit agreement allows. Surface a clear "Bit limited to <your cap>" message and offer credit card as the alternative. Also confirm `Currency: 1` (Bit rejects non-ILS).

### Error: 3DS challenge appears in sandbox but transaction is rejected
Cause: Sandbox 3DS challenge requires specific test cards and challenge responses configured per terminal.
Solution: Confirm with Pelecard support which test card numbers and challenge codes work against your sandbox terminal. The `Initiate` and `AskForChallenge` toggles in the sandbox UI control whether 3DS is invoked at all.

### Error: Token charge succeeds but customer claims no payment
Cause: J5 (authorize) was used instead of J4 (sale), and capture was never triggered.
Solution: Verify the `ActionType` field on the original transaction via `PaymentGW/GetTransaction`. If it was `J5` or `J5h`, run the matching capture flow (or void the auth). Default to `J4` for one-shot sales.
