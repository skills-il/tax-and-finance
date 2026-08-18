# Tranzila Response Codes

`000` = approved. Any other value is a decline or error.

## How Tranzila returns codes (read this first)

- **HTTP 200 does NOT mean the transaction succeeded.** On API V2 the HTTP status is 200 even for a declined or failed transaction; the real result is the `Response` / response-code field in the body.
- **There are two separate code spaces:**
  - **SHVA / issuer codes** (the large numeric table, hundreds of codes): card-issuer refusals cluster in the 300s, installment-related errors in the 400s, PinPad errors in the 700s, PayPal-specific errors in the 950s.
  - **3D Secure codes** (a separate set, **900-930**): e.g. 900 = 3DS authentication failed.
- **Do NOT reuse codes from Stripe, Cardcom, or other gateways.** Tranzila's codes are gateway-specific.
- The authoritative, complete list is the official **"Transaction Response Codes"** page in the Tranzila docs (260+ SHVA rows + the 3DS tab). Always verify a specific code there before acting on it; do not hardcode codes from memory.

## Confirmed common codes

| Code | Space | Meaning | Action |
|------|-------|---------|--------|
| `000` | SHVA | Approved | Transaction completed |
| `004` | SHVA | Refusal / declined (contact card owner) | Ask the customer to try another card |
| `036` | SHVA | Card expired | Ask the customer to update card details |
| `037` | SHVA | Installment error: transaction sum must equal first payment + (fixed payments x count) | Recompute the installment amounts |
| `900` | 3DS | 3D Secure authentication failed | Re-authenticate, or retry without 3DS if permitted |

(Every specific code above should still be re-confirmed against the official Transaction Response Codes page; the SHVA code space has hundreds of entries and is easy to mis-cite.)

## Categories to expect (verify the exact code in the official table)

- **Card-issuer refusals** (insufficient funds, restricted card, stolen, etc.): generally in the 300s.
- **Installment / credit-type errors**: generally in the 400s (401-406).
- **3D Secure**: 900-930.
- **PinPad / terminal hardware**: 700s.
- **PayPal-specific**: 950s.

When you hit a non-000 code, look it up by exact number in the official Transaction Response Codes page rather than inferring its meaning. Build error handling to fall back to a generic "payment could not be completed, please try another card or contact your bank" message for any code you have not explicitly mapped.
