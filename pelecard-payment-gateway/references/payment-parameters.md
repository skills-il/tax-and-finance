# Pelecard Payment Parameters

This reference groups the Pelecard `PaymentRequest` parameters by purpose. The dofinity/pelecard PHP wrapper documents the full set across these groups; the most-used ones are listed below. For the complete parameter list, see `https://github.com/dofinity/pelecard/blob/master/src/Pelecard/PaymentRequest.php` and Pelecard's official sandbox at `https://gateway20.pelecard.biz/sandbox`.

## Authentication

Sent server-side only. Never expose to the browser.

| Field | Type | Notes |
|-------|------|-------|
| `terminal` | string | Pelecard-issued terminal ID. dofinity declares it as `protected $terminal;`. |
| `user` | string | API username. dofinity: `protected $user;`. |
| `password` | string | API password. dofinity: `protected $password;`. |

## ActionType

The Pelecard sandbox lists ActionType options as: "J4 (default) J2 (for registration only) J5 J5h".

| Value | Meaning | Money moves? |
|-------|---------|--------------|
| `J4` | Standard sale. **Default.** | Yes |
| `J2` | Card validation / registration only. | No |
| `J5` | Authorize now, charge later. | No (auth only) |
| `J5h` | Enhanced J5. | No (auth only) |

The dofinity `PaymentRequest` constructor sets the default to `'J4'`. Picking the wrong value is the most common Pelecard integration bug -- `J2` looks identical to `J4` in the merchant UI but does not move money.

## Currency

The dofinity wrapper documents `Currency` with the comment `1 = ILS`. Pelecard's currency-code mapping is not consistently documented across Gateway20, Gateway21, and the Match API; only `1 = ILS` is reliably confirmed across surfaces.

| Code | Currency | Note |
|------|----------|------|
| `1` | ILS (Israeli shekel) | Default. Confirmed via the dofinity wrapper. Required for Bit. |
| Other | USD / EUR / GBP / etc. | Pelecard's currency-code mapping is not consistently documented across Gateway20, Gateway21, and the Match API. **Verify the exact integer for your terminal in the live Postman workspace before sending non-ILS amounts.** |

## Tashlumim (Installments)

Per the dofinity `PaymentRequest`:

| Field | Notes |
|-------|-------|
| `MaxPayments` | Maximum number of installments offered to the customer. |
| `MinPayments` | Minimum installments. |
| `MinPaymentsForCredit` | Threshold above which the transaction is treated as a "credit" tashlumim (separate from regular tashlumim). |
| `FirstPayment` | First installment amount. dofinity comment: "the amount is in agorot/cents". |
| `DisabledPaymentNumbers` | dofinity comment: "comma separated string". Disable specific installment counts. |

Money fields use minor units (agorot) on Gateway21: send `9900` for ₪99.00 in `Total`, and `5000` for ₪50.00 in `FirstPayment`. The dofinity wrapper documents `FirstPayment` as "in agorot/cents"; the same convention applies to `Total`. Mixing the unit silently divides or multiplies every charge by 100; do a 1 ₪ test charge in sandbox before going live.

## Tokenization

Per the dofinity `PaymentRequest`:

| Field | Notes |
|-------|-------|
| `CreateToken` | Set true on the first transaction to save a token. |
| `TokenForTerminal` | Identifies which terminal owns the token (for multi-terminal setups). |
| `IsToken` | Flag a charge as token-based instead of card-entry-based. |
| `TokenCreditCardDigits` | Card last-4 (or similar) tied to the token, used to display "**** 1234" in the merchant UI. |

The Pelecard WordPress plugin lists "Saved payment methods (tokenization)" as a feature and added it in v1.2.0 ("Added Tokenization support") and shipped "WooCommerce Subscriptions support" in v1.4.

## BIN Controls

Per the dofinity `PaymentRequest`:

| Field | Notes |
|-------|-------|
| `AllowedBINs` | Comma-separated list of allowed BINs. |
| `BlockedBINs` | Comma-separated list of blocked BINs. |
| `SupportedCards` | dofinity comment: "Supported credit cards" (Visa/MC/Amex/Diners/IsraCard toggles). |

Useful for B2B-only flows or fraud rules.

## UI Customization

Per the dofinity `PaymentRequest`:

| Field | Notes |
|-------|-------|
| `CssURL` | Custom CSS for the iframe. |
| `LogoURL` | Merchant logo. |
| `TopText` | Header copy. |
| `BottomText` | Footer copy. |
| `AccessibilityMode` | IS 5568 / Israeli accessibility regulation 35 compliance. |
| `HiddenPelecardLogo` | White-label control. |

## Server-Side Feedback URLs

Per the dofinity `PaymentRequest`:

| Field | Notes |
|-------|-------|
| `GoodURL` | Browser redirect on success. |
| `ErrorURL` | Browser redirect on error. |
| `CancelURL` | Browser redirect on customer cancel. |
| `ServerSideGoodFeedbackURL` | Server-to-server IPN on success. |
| `ServerSideErrorFeedbackURL` | Server-to-server IPN on error. |

The server-side URLs fire only when the transaction reaches a terminal state (success or merchant-rejected error). If the customer closes the browser before submitting the card form, no IPN fires. The complete safety net is to persist the `PelecardTransactionId` from the create-session response, then run a periodic reconciliation job that polls `PaymentGW/GetTransaction` for any session that has not produced an IPN within your timeout window.

Pelecard does NOT sign IPN deliveries with HMAC, so authenticity is established by re-fetching the transaction via `PaymentGW/GetTransaction` (with optional outbound IP allowlisting and TLS 1.2+ on your endpoints).

## Custom Passthrough

Per the dofinity `PaymentRequest`:

| Field | Notes |
|-------|-------|
| `ParamX` | Free-form pass-through, echoed on lookup. Use as the merchant's order correlation ID. NOT an idempotency / dedupe key (Pelecard may deliver the same IPN twice on retry, both with the same `ParamX`); dedupe IPNs on `PelecardTransactionId` instead. |
| `ShopNo` | Shop / branch identifier. |
| `UserKey` | User identifier. |
| `UserData` (and `UserData1`-`UserData15` per Postman) | Up to 15 free-form fields. |

Use these to correlate Pelecard transactions back to your internal order ID without storing card data.

## 3D Secure (EMV 3DS)

The Pelecard sandbox UI exposes:

| Toggle | Values | Notes |
|--------|--------|-------|
| `Initiate` | `None` (default) / `False` / `True` | Whether 3DS is initiated. |
| `AskForChallenge` | `None` (default) / `False` / `True` | Whether to request a step-up challenge. |
| `ShvaResultEmv` | (callback field) | EMV result code surfaced on the response. The Pelecard plugin v1.4.19: "Added Emv errors in order notes. ShvaResultEmv parameter". |

Configure 3DS as mandatory for new merchants in line with Bank of Israel SCA expectations.

## Bit Wallet

The Pelecard sandbox exposes a Bit toggle ("Enable bit: True False") plus UI text parameters. Bit's wallet-side limits (per allpay.co.il/en/help/bit):

| Constraint | Value |
|------------|-------|
| Per-transaction cap | "Payment via Bit cannot exceed 5,000 shekels." |
| Installments | "No installments. You can only pay with Bit in one payment." |
| Per-merchant monthly cap | "The sum of all payments per month from all customers cannot exceed 20,000 shekels." |
| Currency | "Bit only supports payments in shekels." |
| Customer time limit | "From the moment you press the Bit button, the customer has 10 minutes to make a payment." |
| Saved cards | "Bit does not allow you to save your customer card for future charges." |
| Card brand exclusion | "Diners and Discover brand cards are not supported by Bit." |

## Apple Pay

The Pelecard plugin lists Apple Pay support via Pelecard-hosted SDK: "Apple Pay Support (optional, disabled by default) -- When enabled, loads ClientSecure.js from Pelecard servers to enable Apple Pay on supported devices."

## Google Pay

The Pelecard sandbox exposes a `GooglePay` section. Verify rollout state with vendor before relying.
