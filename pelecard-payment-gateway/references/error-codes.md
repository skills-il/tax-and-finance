# Pelecard Error Codes

Pelecard returns a numeric `PelecardStatusCode` on every transaction callback. By convention, `000` is success and any other value is an error -- but the exact code-to-meaning mapping is not fully public, varies per acquirer, and changes over time. EMV / Shva result codes ride alongside via `ShvaResultEmv`.

**Consult Pelecard support for exact codes.** The categories below cover the typical failure modes you will encounter; specific numeric codes change per acquirer and per Pelecard release. Do not guess from generic Israeli-payment articles.

## `PelecardStatusCode` Convention

| Value | Meaning | Action |
|-------|---------|--------|
| `"000"` (literal 3-digit string) | Success | Proceed to verify via `PaymentGW/GetTransaction`. |
| `"0"` or `"00"` | Malformed | Treat as a warning and verify the callback was not truncated or coerced upstream. Pelecard returns the canonical `"000"`. |
| any other value | Error | Look up the category below; if uncertain, capture the raw code and contact Pelecard support. |

Note from the Pelecard plugin v1.4.20 changelog: "Convert information errors 041,042 that received in J2 to 000." -- reinforcing that the code semantics differ across `ActionType` values and aren't a flat lookup table.

## Error Categories

### Authentication Failure
The credentials triple is wrong, malformed, or doesn't match the host (sandbox vs prod).

- Symptom: every transaction fails immediately, no iframe URL returned, or `GetTransaction` returns "transaction not found" for every ID.
- Solution: confirm `terminal` + `user` + `password` match the host (`gateway20.pelecard.biz/sandbox` for sandbox creds, `gateway21.pelecard.biz` for prod creds).

### Card Declined
Issuer rejected the charge for risk, balance, velocity, or chargeback-history reasons.

- Symptom: a single transaction fails with a non-`000` `PelecardStatusCode` while other cards succeed.
- Solution: prompt the customer to try another card or contact their issuer. Do not retry automatically -- repeated declines hurt your acquirer trust score.

### Expired / Invalid Card
Card data failed acquirer validation (expiry past, CVV mismatch, PAN check digit wrong).

- Symptom: same card consistently fails. EMV / Shva result codes will indicate the specific check that failed.
- Solution: ask customer to update card details. For tokenized recurring billing, fall back to Pelecard's saved-card replacement flow if the issuer reissued the card.

### Insufficient Funds
Acquirer reported the customer doesn't have available credit/balance.

- Symptom: transaction declines, often with an issuer-level reason code.
- Solution: prompt customer for a different card. For subscription billing, queue a retry per your dunning policy.

### 3DS Challenge Required / Failed
The acquirer required EMV 3DS step-up (challenge) and the customer either didn't complete it or failed.

- Symptom: `ShvaResultEmv` is populated; transaction did not complete.
- Solution: log `ShvaResultEmv`. The Pelecard plugin v1.4.19 changelog: "Added Emv errors in order notes. ShvaResultEmv parameter". Verify your `Initiate` and `AskForChallenge` settings in the sandbox UI match your prod policy.

### Network Timeout / Stale Callback
Pelecard couldn't reach your server, or your IPN handler took too long.

- Symptom: customer reports successful payment but your DB shows no transaction. Pelecard plugin v1.5.1: "Fixed timeout-retry issues: correct transaction display and stale callbacks no longer fail paid orders."
- Solution: poll `PaymentGW/GetTransaction` with the `PelecardTransactionId` you stored from the create-session response or from any prior IPN (`GetTransaction` keys on `TransactionId`, not on `ParamX`). Make IPN handlers idempotent on `PelecardTransactionId` and fast (<30s).

### Tashlumim Mismatch
Customer requested an installment count outside `MinPayments`/`MaxPayments`/`MinPaymentsForCredit` window.

- Symptom: customer-facing error during checkout; transaction never reaches authorization.
- Solution: validate the tashlumim selector client-side against the same min/max you sent to Pelecard, so the iframe never gets a bad value.

### Validation-Only (J2) Confusion
The transaction succeeded as a `J2` (registration only) but the merchant expected a `J4` charge.

- Symptom: `PelecardStatusCode` is `000` but `DebitTotal` from `PaymentGW/GetTransaction` is zero (or missing).
- Solution: confirm the original `ActionType` field. Default to `J4` for sales. Pelecard plugin v1.4.7: "Bypass validation for J2 transactions" reinforces that J2 has its own code path.

### Bit Limit Hit
Customer chose Bit but the cart exceeds the merchant's Bit per-transaction cap (commonly 5,000 ₪, set by the Bit agreement and operator risk tier), a tashlumim count was selected, or the currency is not ILS.

- Symptom: Bit payment fails or never initializes; customer falls back to card.
- Solution: gate the Bit option in your UI to the cap your Bit agreement allows (treat 5,000 ₪ as the design ceiling unless cleared above), hide the tashlumim selector when Bit is selected, and ensure `Currency: 1`.

## EMV / Shva Result Codes

`ShvaResultEmv` carries the result code from Israel's underlying clearing network (Shva, שב"א) for EMV / 3DS transactions. Codes follow Shva conventions and are not Pelecard-specific. For the canonical mapping, consult Shva at `https://www.shva.co.il/`. The Pelecard plugin v1.4.20 specifically converts "information errors 041, 042" received in J2 to `000`, illustrating that a non-zero EMV code does not always mean the transaction failed -- context (ActionType, business logic) matters.

## Recommended Logging

Log every callback with at least:

- `PelecardStatusCode` (raw)
- `ConfirmationKey` (raw)
- `PelecardTransactionId`
- `ShvaResultEmv` (if present)
- `ParamX` (your order correlation)
- The host you posted to (sandbox vs prod)

That set is the minimum to triage a failed transaction with Pelecard support without recreating it.
