# Tranzila Response Codes

`000` = approved. Any other value is a decline or error.

## How Tranzila returns codes (read this first)

- **HTTP 200 does NOT mean the transaction succeeded.** On API V2 the HTTP status is 200 even for a declined or failed transaction; the real result is the `Response` / response-code field in the body.
- **There are two separate code spaces:**
  - **SHVA / issuer codes** (the large numeric table, hundreds of codes). The ranges, read off the vendor's own table: **001-017** issuer refusals and card-status problems, **051-089** missing terminal vector or parameter FILE, **101-152** missing ENTRY in a vector or parameter file, **182-193** invalid values in those files, **300-354** acquirer or issuer PERMISSION missing for this transaction type, currency or credit type, **401-406** installment errors, **407-498** data and card-handling errors, **500s** cancellations and message errors, **700s** PinPad, **951-954** PayPal.
  - **3D Secure codes, 900-930**, on the "3DS Errors" tab of the same page: "These error codes are returned during the 3D Secure (3DS) authentication phase, before the transaction is submitted to SHVA for clearing." Examples: 901 card authentication failed, 905 expired card (the 3DS-space one; in the SHVA space expired is 015), 910 stolen card, 913 cardholder not enrolled, 914 ACS timeout, 922 technical issue at ACS, 927 and 928 cancelled by the user, 926 and 930 attempted but not completed.
- **Do NOT reuse codes from Stripe, Cardcom, or other gateways.** Tranzila's codes are gateway-specific.
- The authoritative, complete list is the official **"Transaction Response Codes"** page in the Tranzila docs (https://docs.tranzila.com/docs/payments-and-billing/transaction-response-codes), which carries the SHVA table in English and Hebrew plus a separate 3DS tab. Always verify a specific code there before acting on it; do not hardcode codes from memory.

## Confirmed common codes

| Code | Space | Meaning | Action |
|------|-------|---------|--------|
| `000` | SHVA | Transaction approved | Transaction completed |
| `777` | SHVA | Operation completed, success code for operations where no transaction is recorded, including J2 and J5 | Treat as success for verification-only calls |
| `001` | SHVA | Blocked, confiscate card | Do not retry, ask for another card |
| `002` | SHVA | Stolen, confiscate card | Do not retry |
| `003` | SHVA | Contact the credit company to approve the transaction | Cardholder calls the issuer |
| `004` | SHVA | Refusal, contact the card owner to check the reason with the credit company | Ask the customer to try another card |
| `005` | SHVA | Forged, confiscate card | Do not retry |
| `006` | SHVA | Incorrect identity number or CVV | Re-collect the ID or CVV |
| `010` | SHVA | Partial confirmation | Handle a partial approval explicitly |
| `012` | SHVA | Unauthorized card for this terminal | Terminal or brand permission |
| `015` | SHVA | Expired card, check the expiration date again | Ask the customer to update the card |
| `016` | SHVA | Unauthorized currency | The terminal is not enabled for that currency |
| `017` | SHVA | Unauthorized credit type for this transaction | Wrong `cred_type` for this card or terminal |
| `026` | SHVA | Wrong ID number | Re-collect the ID |
| `141` | SHVA | Terminal not authorized to clear this transaction brand | Configuration, raise with the acquirer |
| `406` | SHVA | Transaction sum differs from first payment + fixed payment times number of payments | Recompute the installment amounts |
| `416` | SHVA | Invalid expiry date | Re-collect the expiry |
| `417` | SHVA | Invalid terminal number | Check the supplier/terminal parameter |
| `425` | SHVA | Duplicate record | Deduplicate; do not blind-retry |
| `431` / `997` | SHVA | General failure | Retry once, then escalate |
| `447` | SHVA | Wrong credit card number | Re-collect the card number |
| `900` | 3DS | Transaction failed at the 3D Secure authentication stage | Re-authenticate, or retry without 3DS if permitted |
| `905` | 3DS | Expired card (3DS space; the SHVA-space expired card is `015`) | Ask the customer to update the card |
| `913` | 3DS | Cardholder not enrolled in the service | Decide whether to proceed without a liability shift |
| `914` | 3DS | ACS transaction timeout expired | The issuer's server timed out, retry |
| `927` / `928` | 3DS | Card authentication cancelled by the user | The customer backed out; this is not a card problem |

### Codes that do NOT exist, and were previously carried here

`033`, `036`, `037`, `039`, `091`, `125` and `200` are absent from the vendor's table entirely. A further set had invented meanings here: `014` is "card not affiliated with the network", not "invalid card number"; `057` / `061` / `065` / `075` are missing vector or parameter FILES; `107` / `111` are missing ENTRIES in vectors 12 and 31. Expired card is `015`; the installment-sum error is `406`.

(Every specific code above should still be re-confirmed against the official Transaction Response Codes page; the SHVA code space has hundreds of entries and is easy to mis-cite.)

## Categories to expect (verify the exact code in the official table)

- **Card-issuer refusals** (blocked, stolen, forged, refusal, expired, wrong CVV): 001-017.
- **Terminal configuration** (missing vector or parameter file or entry): 051-089, 101-152, 182-193.
- **Acquirer or issuer permission missing** for this transaction type, currency or credit type: 300-354. These are configuration problems, not something the cardholder can fix.
- **Installment / credit-type errors**: 401-406.
- **3D Secure**: 900-930, on their own tab of the response-codes page.
- **PinPad / terminal hardware**: 700s.
- **PayPal-specific**: 950s.

When you hit a non-000 code, look it up by exact number in the official Transaction Response Codes page rather than inferring its meaning. Build error handling to fall back to a generic "payment could not be completed, please try another card or contact your bank" message for any code you have not explicitly mapped.
