---
name: tranzila-payment-gateway
description: Integrate Tranzila payment processing into Israeli applications -- covers iframe payments, tokenization, installments (tashlumim), refunds, 3D Secure, and Bit wallet. Use when user asks to accept payments via Tranzila, integrate Israeli credit card processing, set up "slikat ashrai", handle tashlumim (installment payments), create payment tokens, process refunds through Tranzila, or mentions "Tranzila", "tranzila API", "secure5", or Israeli online payments. Supports both legacy CGI endpoints and modern API V2. Do NOT use for Cardcom integration (use cardcom-payment-gateway), general accounting, or non-payment financial queries.
license: MIT
compatibility: Requires network access for Tranzila API calls. Works with Claude Code, Claude.ai, Cursor.
---

# Tranzila Payment Gateway

## Overview

Tranzila is one of Israel's leading payment processors (solek), operating since 1999. It connects to the Shva network (reshet shva) -- Israel's central card processing infrastructure -- and supports all Israeli card issuers: Isracard, Visa Cal, and Max (formerly Leumi Card).

This skill guides integration with Tranzila for accepting credit card payments (slikat kartis ashrai) in Israeli applications.

**Official docs:** `https://docs.tranzila.com/`

**Test credentials:** ask Tranzila support for the sandbox card numbers for your terminal, and configure the terminal for sandbox mode via the Tranzila dashboard. Test-card values circulating in blog posts and older versions of this skill are not published by the vendor and should not be treated as valid.

## Instructions

### Step 1: Choose Integration Pattern

Help the user select the right approach based on their needs:

| Pattern | Hebrew | PCI Scope | Best For |
|---------|--------|-----------|----------|
| **Iframe** | daf tashlum mutman | Smallest (typically SAQ A) | Quick integration, minimal compliance |
| **Hosted Fields** | sdot mitarachim | Small (typically SAQ A-EP) | Custom checkout UX with low PCI burden |
| **API V2 (server-to-server)** | sharat le-sharat | Largest (typically SAQ D) | Token charging, recurring, refunds |

The SAQ mapping is the PCI Security Standards Council's, not Tranzila's, and eligibility depends on the merchant's whole environment and on what the acquirer requires, so confirm it rather than assuming it follows from the integration choice. Note also that PCI DSS v4 tightened the payment-page script requirements (6.4.3 and 11.6.1) and that the SAQ forms were reissued for v4.x, so check the current SAQ A against the PCI SSC document library rather than assuming "iframe means nothing to do" still holds.

Most Israeli merchants start with **Iframe** for collecting payments, then use **API V2** for server-side operations like token charging and refunds.

### Step 2: Set Up Authentication

Tranzila uses different credentials depending on the integration:

**For Iframe / Legacy CGI:**
- `supplier` -- Terminal name (provided by Tranzila)
- `TranzilaPW` -- Transaction password

**For API V2 (api.tranzila.com/v1):** authentication is a 4-header HMAC-SHA256 handshake, NOT a single key header. Every request must send all four:
- `X-tranzila-api-app-key` -- your public application key
- `X-tranzila-api-request-time` -- current Unix time in SECONDS
- `X-tranzila-api-nonce` -- a random nonce (about 40 bytes)
- `X-tranzila-api-access-token` -- `hmac_sha256(secret + request_time + nonce, app_key)` (HMAC-SHA256 of the app key, keyed with secret concatenated with the request-time and nonce)

You get both a public app key and a secret key when you enrol in API V2. A request with only `X-tranzila-api-app-key` is rejected. (Base URL is `https://api.tranzila.com`; core payment endpoints are under `/v1` and "API V2" refers to the auth generation, though some newer endpoints, such as standing-order create, use a `/v2` path.) Confirm the exact concatenation order in the Authentication page at docs.tranzila.com before shipping.

Remind the user to store credentials securely (environment variables, secrets manager) and never commit them to source control.

### Step 3: Implement the Payment Flow

#### Option A: Hosted Fields (Recommended for Custom UX)

Hosted Fields let you design your own checkout form while Tranzila securely handles card inputs:

1. Include the Tranzila Hosted Fields JS on your page
2. Create container `<div>` elements for card number, expiry, and CVV
3. Initialize fields with your terminal name and styling options
4. On submit, the JS generates a `TranzilaTK` token without card data touching your server
5. Send the token to your backend for charging via API V2

This gives full design control while maintaining SAQ-A-EP PCI compliance. Refer to the Hosted Fields section under `https://docs.tranzila.com/` (deep slug paths change frequently; navigate from the Payments &amp; Billing index).

> **Webhook signature verification.** When Tranzila POSTs the result to your notify page (`notify_url_address` on the iframe, `notify_url` on the Bit API), do NOT trust it on inbound shape alone. Verify with a mechanism the vendor actually documents: the Hosted Fields **Response Hash** feature (your own secret is used to generate a `response_hash` you can recompute on receipt), or the **Handshake API V2** flow, both under the Payments and Billing section of the docs. Signing your own checksum into the form fields and verifying it on receipt is an acceptable fallback. Do not rely on the `myid` round-tripping, and do not invent a confirmation endpoint. Without this step, anyone who learns that URL can fake transaction-success callbacks.

**Callback and redirect parameter names differ by product.** On the **iframe** they are `success_url_address`, `fail_url_address` and `notify_url_address` (the "Notify" page receives the transaction data as actually performed). The bare `notify_url` is the name used by Hosted Fields, the 3DS API and Bit; on the iframe it is simply not the parameter. Sending `notify_url` to `iframenew.php` means no webhook ever arrives: the customer is charged and the order is never fulfilled.

#### Option B: Iframe Integration (Quick Start)

1. Embed the Tranzila iframe in your checkout page:
   - URL: `https://direct.tranzila.com/{supplier}/iframenew.php`
   - Add query parameters: `sum`, `currency`, `cred_type`
   - `tranmode` selects the mode: `A` standard charge (the default behaviour), `V` verification (J5), `N` verification (J2), `K` create a token without charging, and the token variants `AK`, `VK`, `NK`. There is no `J4` mode, and the iframe does not create a token unless you ask for one

2. Handle the response via your `notify_url_address`:
   - Tranzila POSTs results to your server
   - Check `Response` field: `000` = approved
   - Store `TranzilaTK` (token) for future charges

3. Confirm transaction server-side (recommended):
   - Use the three-sided handshake to verify the transaction is genuine

#### Option C: Server-to-Server via API V2

For token charging, refunds, and operations that don't involve card entry:

**Charge a token:**
```
POST https://secure5.tranzila.com/cgi-bin/tranzila31tk.cgi
Content-Type: application/x-www-form-urlencoded

supplier={terminal}&TranzilaPW={password}&TranzilaTK={token}&expdate={MMYY}&sum={amount}&currency=1&cred_type=1
```

**Process a refund:**
Refunds run on their own endpoint and need credentials the charge request does not use.

- **Legacy CGI:** POST to `https://secure5.tranzila.com/cgi-bin/tranzila71u.cgi` with `tranmode=C{index}` (the index of the original transaction), plus `supplier`, `sum`, `currency`, `TranzilaTK`, `expdate`, `cred_type`, `TranzilaPW`, **`CreditPass`** and **`authnr`**. `CreditPass` is a separate credit password that has to be obtained from Tranzila and enabled on the terminal, so a refund flow that was never tested end to end usually fails on it first.
- **API V2:** `POST https://api.tranzila.com/v1/transaction/credit_card/create` with `txn_type` set to `credit` (return funds), `cancel` (cancel a debit or credit) or `reversal` (release a credit limit taken by a J5), referencing the original with `reference_txn_id`.

Decide which of the two you are on before writing the code: the parameter names do not carry across.

Consult `references/api-parameters.md` for the complete parameter reference.

### Step 4: Handle Israeli-Specific Payment Types

Israeli payments have unique features that differ from international processing:

**Installments (Tashlumim):**
- Set `cred_type=8` for installments (`cred_type=6` is the card company's own credit plan, which is a different product)
- Parameters: `npay` (number of payments minus 1), `fpay` (first payment), `spay` (subsequent payments)
- The sum of `fpay + (npay * spay)` must equal the total `sum`
- Not all terminals are authorized for installments (you get an error if the terminal is not enabled for them; check the exact code in the official table)

**Credit Types (cred_type):**

| Value | Type | Hebrew |
|-------|------|--------|
| 1 | Credit card, a regular single charge | ashrai ragil |
| 6 | Credit (kredit), the card company's own credit plan | kredit |
| 8 | Installments | tashlumim |

These are the only three values the current iframe parameter table publishes ("1 - Credit card, 6 - Credit, 8 - installments"). Earlier versions of this skill listed 2, 3, 5 and 9; those do not appear in the vendor documentation, and sending one gets a code 017 (unauthorized credit type for this transaction).

**Currency codes (matbea):**

| Code | Currency | Hebrew |
|------|----------|--------|
| 1 | ILS (Shekel) | shekel chadash |
| 2 | USD | dolar |
| 978 | EUR | euro |
| 826 | GBP | lira sterling |

Euro and Sterling use their ISO 4217 numeric codes, not small integers. Earlier versions of this skill said `3` = GBP and `7` = EUR; neither value appears in the vendor's parameter table, and sending one produces code 016 (unauthorized currency).


**These parameter names are the iframe and legacy-CGI ones.** API V2 uses different field names and types for the same concepts: `txn_currency_code` takes ISO alpha codes (ILS, USD, EUR, GBP and others) rather than the numeric `currency`; the installment plan is `payment_plan` plus `installments_number`, `first_installment_amount` and `other_installments_amount` rather than `cred_type` plus `npay` / `fpay` / `spay`; the expiry is `expire_month` and `expire_year` as integers rather than `expdate` as MMYY; and the cardholder ID is `card_holder_id` rather than `myid`. Decide which surface you are integrating against before copying a parameter name across.

**Israeli ID (teudat zehut):**
Some transactions require the `myid` parameter, a 9-digit Israeli ID number (mispar zehut). Treat it as regulated personal data, not as a routine field: under the Privacy Protection Law and its Amendment 13, an ID number collected for payment purposes is subject to the same duties as the rest of your customer database, so do not log it in plain application logs, do not retain it beyond the purpose it was collected for, and keep it out of analytics payloads.


**Prevent duplicate charges with `DCdisable`.** Tranzila's own duplicate-transaction guard takes a unique value per transaction in the `DCdisable` parameter and deduplicates against it in Tranzila's database for up to 24 hours, at parent-terminal level. A transaction that failed the first time is not checked against DCdisable, so a retry after a genuine failure still goes through. It has to be enabled as field 20 under "Additional Fields for Transaction" in my.tranzila, on both the parent and the child terminals, and the value is capped at 254 characters. Use it rather than inventing an application-side idempotency scheme the terminal does not honour: a retry of a request whose outcome you never read is the standard way a customer gets charged twice.

**J5 authorizations have to be captured.** `verify_mode=5` (J5) takes a credit limit on the amount without charging it. The charge itself is a separate call with `txn_type=force`, and `txn_type=reversal` releases the limit if you decide not to collect. A subscription that starts with a J5 and never issues the capture never collects its first payment.

**Iframe extras worth knowing.** `bit_pay=1` adds a Bit payment option to the iframe, which is a one-line alternative to a full Bit API integration for iframe merchants. `maxpay` sets a maximum number of installments, and the vendor's rule is explicit: pass either `npay`, `fpay` and `spay`, or `maxpay`, never both together.

### Step 5: Implement Tokenization for Recurring Payments (hora'ot keva)

Tokens (asmachta) let you charge returning customers without handling card data again:

1. **Create token during first payment:**
   - Iframe: pass `tranmode=K` (token only) or `AK` / `VK` (charge or verify, plus token) to get a `TranzilaTK` back
   - API: Use `tranmode=K` (token only), `VK` (verify + token), or `AK` (charge + token)

2. **Store the token securely:**
   - Treat the token as an opaque string. The vendor does not publish a fixed length or format, and tokens seen in the API V2 documentation are alphanumeric and longer than the legacy CGI ones, so never validate it by length or assume the last four digits match the card
   - Store token, expiry date, and card last-4 in your database
   - Token has no value without your terminal credentials
   - **Never store the CVV / CVV2 after authorization, and never store the full card number.** PCI DSS requirement 3.3.1 prohibits retaining sensitive authentication data (CVV, full magnetic-stripe or chip data, PIN) once the transaction is authorized, even encrypted. Storing the token, the expiry and the last four digits is the whole of what you keep. This applies no matter which integration pattern you chose, and it is the single most common way a merchant loses its compliance posture

3. **Charge the token later:**
   - Use the `/cgi-bin/tranzila31tk.cgi` endpoint
   - Include `TranzilaTK`, `expdate`, `sum`, and `currency`

### Step 6: Add 3D Secure (if required)

3D Secure V2 adds cardholder authentication. Consult `references/3ds-flow.md` for the full redirect-based flow. Key points:
- 3DS changes the payment flow to include a bank authentication step
- Response includes additional fields for authentication status
- Some Israeli issuers may not support 3DS for all card types

### Step 7: Accept Bit Payments

Tranzila supports Bit (Israel's popular mobile payment app) through a **dedicated Bit API**, not a flag on the card-charge CGI. It has its own `Bit - Init` and `Bit - Refund` POST endpoints under `https://api.tranzila.com/v1` using the same 4-header HMAC auth as the rest of API V2.

1. Call the Bit Init endpoint via the API -- Tranzila returns a Bit payment URL
2. Redirect the customer to the Bit URL or display a QR code
3. Customer approves payment in the Bit app
4. Tranzila sends the result to your `notify_url` (Bit API naming)
5. Bit refunds use the dedicated Bit Refund endpoint, not the card refund flow

**Bit constraints (from the docs):** NIS only, transaction sum must be above 5 NIS, and the merchant needs a Visa or Isracard identifier, **Max-only merchants are not offered Bit at this time**. Bit does not support Hosted Fields or 3DS. Do not assume a `bit=1` / `bit_url` parameterization on the legacy CGI. On the iframe, Bit is enabled with `bit_pay=1`; for a server-side integration use the dedicated Bit API. For the Bit spec, navigate to the Payments & Billing section from the docs index at `https://docs.tranzila.com/` (deep Bit slug URLs change and may be empty stubs).

### Step 8: Generate Payment Request Links

Payment Requests (TRAPI) let you send payment links via email or SMS without building a checkout page:

1. Create a payment request via API with amount, description, and customer contact
2. Tranzila generates a secure payment link
3. Send the link to the customer (Tranzila can send automatically via email/SMS)
4. Customer clicks the link and pays on a Tranzila-hosted page
5. You receive the result via webhook

This is useful for invoicing, phone orders, or any scenario where you need to collect payment without an embedded form.

### Step 9: Set Up Standing Orders (Recurring Payments)

For automated recurring billing beyond simple token charging, Tranzila offers Standing Orders:

1. Create a standing order with payment schedule (amount, frequency, start/end dates)
2. Tranzila automatically charges the customer on schedule
3. Monitor results via the Reports API or webhook notifications
4. Cancel or modify standing orders via API

Standing orders are a paid feature -- contact Tranzila to enable on your terminal. Refer to Tranzila's documentation for detailed standing order setup instructions.

### Step 10: Generate Invoices

Tranzila has an Invoicing API for generating digitally-signed tax documents approved by the Israeli Income Tax Authority:

1. Create invoices tied to transactions or standalone
2. Invoices are digitally signed for tax compliance
3. Supports tax invoices, receipts, and credit notes
4. Can be auto-generated with PayPal payments

**Israel Tax Authority allocation number (mispar haktza'a), mandatory for B2B invoices over thresholds.** Since May 2024 the ITA requires a B2B tax invoice above a threshold to carry an allocation number obtained from SHAAM. The threshold is keyed to the INVOICE's own date, not today's, so a system that reissues, migrates or audits older documents needs the whole schedule (amounts before VAT): NIS 25,000 from May 2024, NIS 20,000 from January 2025, NIS 10,000 from January 2026, **NIS 5,000 from 1 June 2026 (now in force)**. An invoice dated before May 2024 predates the regime and never needed one. The statute says `עולה על` (EXCEEDS), so an invoice sitting exactly on a band figure is outside the requirement.

Two limits worth wiring into any validation you build on this. Zero-rated and exempt-only invoices are outside the requirement (s.47(a2)(1)), so an export invoice needs no number however large. And the effect of a missing number is precise: s.38(a1) disallows the BUYER's input-VAT deduction. It does not make the invoice void, so do not describe it that way. If you generate invoices through Tranzila's Invoicing API, confirm with Tranzila support that allocation-number requests are wired through SHAAM for invoices above the current threshold; if not, fall back to a separate invoicing provider (Green Invoice, Morning, etc.) that does integrate with SHAAM, or request allocation numbers directly via the ITA portal.

Refer to Tranzila's invoicing documentation for the complete invoicing API reference.

### Step 11: Handle Errors

Check the `Response` field in every transaction result. `000` means approved -- anything else is a decline or error.

**Important: the HTTP status of an API V2 call is 200 even on a declined/failed transaction.** The HTTP 200 does NOT mean success; read the `Response` / response-code field in the body for the actual SHVA result. And there are TWO separate code spaces: the SHVA/issuer codes (hundreds of codes: refusals in 001-017, missing terminal vector or parameter files in 051-089 and 101-152, acquirer and issuer permission errors in 300-354, installment errors in 401-406) and a separate 3D-Secure set, 900-930, on its own tab of the response-codes page. Do not assume codes from Stripe or other gateways.

A few confirmed codes (verify the rest against `references/error-codes.md` and the official "Transaction Response Codes" page at docs.tranzila.com):

| Code | Meaning (verbatim from the vendor table) | User Action |
|------|---------|-------------|
| 000 | Transaction approved | Transaction completed |
| 777 | Operation completed, a success code for operations where no transaction is recorded, including J2 and J5 | Treat as success for a verification-only call |
| 004 | Refusal. Contact the card owner to check the reason with the credit company | Ask the user to try another card |
| 006 | Incorrect identity number or CVV | Re-collect the ID / CVV |
| 012 | Unauthorized card for this terminal | Terminal or brand permissions |
| 015 | Expired card. Check the expiration date again | Ask the user to update card details |
| 016 | Unauthorized currency | Terminal not enabled for that currency |
| 017 | Unauthorized credit type for this transaction | Wrong `cred_type` for the card or terminal |
| 406 | Transaction sum differs from first payment + fixed payment times number of payments | Recompute the installment amounts |
| 416 | Invalid expiry date | Re-collect the expiry |
| 425 | Duplicate record | Idempotency, do not blind-retry |
| 447 | Wrong credit card number | Re-collect the card number |
| 900 | Transaction failed at the 3D Secure authentication stage (the 3DS space is 900-930, on its own tab of the response-codes page) | Re-authenticate, or retry without 3DS if permitted |
| 905 | Expired card **in the 3DS space** (in the SHVA space, expired is 015) | Ask the customer to update the card |
| 927 / 928 | Card authentication cancelled by the user | The customer abandoned the challenge; this is not a card fault |

**Do not carry a code table from memory into your integration.** The 2026 audit of this skill found that seven codes previously listed here and in the bundled script (033, 036, 037, 039, 091, 125, 200) **do not exist in the vendor's table at all**, and that another seven (014, 057, 061, 065, 075, 107, 111) had invented meanings: in the real table the 051-089 range is "missing vector / parameter file", the 101-152 range is "missing entry in vector N", and 300-354 are acquirer and issuer PERMISSION errors, not issuer refusals. Issuer refusals live in 001-017. Look every code up by exact number.

For the full reference (the SHVA table plus the separate 900-930 3DS set), consult `references/error-codes.md` and verify against the official docs, do NOT hardcode codes from memory.

## Examples

### Example 1: Accept a One-Time Payment
User says: "I need to add credit card payments to my Node.js checkout page"
Actions:
1. Choose: Iframe integration (minimal PCI scope)
2. Guide: Embed iframe with supplier name, sum, currency=1 (ILS)
3. Implement: a server-side handler at your `notify_url_address` to capture the response
4. Validate: Check Response=000, store ConfirmationCode
Result: Working checkout that accepts Israeli credit cards via embedded form.

### Example 2: Set Up Monthly Subscription
User says: "I want to charge customers 99 NIS every month automatically"
Actions:
1. First payment: iframe with token creation (`tranmode=AK` to charge and tokenise, or `VK` to verify and tokenise)
2. Store: Save TranzilaTK and expdate from response
3. Monthly: Cron job calls tranzila31tk.cgi with stored token
4. Handle: Check for expired cards, declined tokens
Result: Recurring monthly billing using tokenized cards.

### Example 3: Process Installment Payment
User says: "My customer wants to pay 6,000 NIS in 3 tashlumim"
Actions:
1. Set: cred_type=8 (installments)
2. Calculate: fpay=2000, spay=2000, npay=2 (3 payments total)
3. Verify: Terminal authorized for installments
4. Process: Transaction with installment parameters
Result: Payment split into 3 equal installments of 2,000 NIS.

### Example 4: Refund a Transaction
User says: "I need to refund transaction from last week, confirmation code 0283456"
Actions:
1. Decide the surface first. On the legacy CGI, POST to `https://secure5.tranzila.com/cgi-bin/tranzila71u.cgi`; on API V2, POST to `/v1/transaction/credit_card/create` with `txn_type=credit` and `reference_txn_id`
2. Legacy CGI fields: `tranmode=C{index}` for the original transaction's index, plus `supplier`, `sum`, `currency`, `TranzilaTK`, `expdate`, `cred_type`, `TranzilaPW`, **`CreditPass`** and **`authnr`**. Without `CreditPass` (a separate credit password enabled on the terminal) the refund fails
3. Set: sum to the refund amount (partial or full)
4. Verify: `Response=000` on the CGI, or `transaction_result.processor_response_code` on API V2
Result: Refund processed and linked to original transaction.

### Example 5: Accept Bit Payment
User says: "I want to let customers pay with Bit on my website"
Actions:
1. Call the dedicated Bit Init endpoint (api.tranzila.com/v1, 4-header HMAC auth) -- not a flag on the card CGI
2. Redirect: Send customer to the Bit payment URL from the response (or show a QR)
3. Handle: receive the payment confirmation at your notify page
4. Verify: Check the response code for a successful Bit payment
5. Note constraints: NIS only, sum > 5 NIS, merchant needs a Visa/Isracard identifier (Max-only merchants not supported)
Result: Customers can pay using Israel's Bit mobile wallet alongside credit cards.

### Example 6: Send Payment Link via SMS
User says: "I need to collect payment from a customer over the phone"
Actions:
1. Create: Payment request via TRAPI with amount and customer phone number
2. Send: Tranzila sends SMS with payment link automatically
3. Wait: Customer opens link and pays on Tranzila's hosted page
4. Confirm: Receive webhook notification when payment completes
Result: Payment collected remotely without building a checkout page.

## Community Libraries

- **tranzilajs** (TypeScript/Node.js) -- the one actively maintained community SDK: HMAC auth, Bit payments, credit-card operations, iframe generation. Install: `npm install tranzilajs`. See: `https://github.com/NirTatcher/tranzilajs`
- **futureecom/omnipay-tranzila** (PHP/Omnipay) -- the Omnipay driver lives under the `futureecom` vendor namespace, not `omnipay/tranzila` (that slug 404s on Packagist, which is why older guides mis-cite it). Check its release date before adopting it.
- **active_merchant_tranzila** (Ruby) exists on RubyGems but its only release is **0.0.1 from August 2010**, and Tranzila is not a gateway bundled with ActiveMerchant itself. Treat it as abandoned and read it as documentation at most, not as a dependency.

## Bundled Resources

### References
- `references/api-parameters.md` -- Complete Tranzila API parameter reference for both legacy CGI and API V2 endpoints, including authentication headers, transaction parameters, token operations, and installment fields. Consult when constructing API requests or debugging unexpected parameter behavior.
- `references/error-codes.md` -- Full listing of Tranzila response codes (000-999) with meanings and recommended handling. Consult when a transaction returns a non-000 response code.
- `references/3ds-flow.md` -- Step-by-step 3D Secure V2 implementation guide for Tranzila, including redirect flow, authentication parameters, and fallback handling. Consult when adding 3DS to an existing integration.

### Scripts
- `scripts/validate_tranzila_response.py` -- Validates a Tranzila transaction response: checks response code, verifies required fields are present, and flags common issues (missing confirmation code, mismatched amounts). Run: `python scripts/validate_tranzila_response.py --help`

## Gotchas
- Tranzila API uses form-encoded key-value pairs (not JSON). Agents default to JSON request bodies, which Tranzila will reject or ignore. Send requests as `application/x-www-form-urlencoded`.
- Tranzila's test mode uses the same endpoint as production but with a different `supplier` parameter. Agents may accidentally send test transactions to the production terminal or vice versa.
- The legacy CGI response is a plain-text `key=value` string joined by `&`, in the same shape as a query string (`Response=000&ConfirmationCode=...&index=...&Tempref=...`), not JSON and not newline-separated. Parse it as a query string. API V2, by contrast, does return JSON, with the SHVA result in `transaction_result.processor_response_code` and an application `error_code` beside it.
- Israeli credit card numbers have different BIN ranges than US/European cards. Tranzila validates cards locally, so test cards from Stripe or other international gateways will not work.
- **A code you cannot find in the vendor table is a code you must not explain.** Several plausible-looking codes (033, 036, 037, 039, 091, 125, 200) do not exist in Tranzila's table at all, and an agent that "recognises" one will hand the merchant a confident wrong diagnosis, most often "card expired" when the real fault is a terminal vector or parameter file. Expired card is **015**.
- **The 300s are permission errors, not refusals.** 300-354 mean the acquirer or the issuer has not authorised the terminal for that transaction type, currency or credit type, which is a configuration problem to raise with Tranzila or the acquirer, not something the cardholder can fix by trying again.
- **Guard against duplicate charges explicitly.** Retrying a failed-looking request is the normal reflex, and code 425 (duplicate record) is what a double submission looks like after the fact. Decide up front how you deduplicate, and never blind-retry a request whose outcome you did not read.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Tranzila developer docs | https://docs.tranzila.com/ | API reference, authentication, supported card networks, 3DS flow, error codes |
| Hosted Fields integration | https://docs.tranzila.com/ (Payments &amp; Billing → Hosted Fields) | PCI-friendly embedded card capture, and the Response Hash callback-integrity feature |
| Transaction response codes | https://docs.tranzila.com/docs/payments-and-billing/transaction-response-codes | The authoritative SHVA and 3DS code tables. Look every code up here by exact number |
| Authentication (API V2 headers) | https://docs.tranzila.com/docs/payments-and-billing/authentication | The four HMAC headers and the exact access-token derivation |
| Iframe parameters | https://docs.tranzila.com/docs/payments-and-billing/iframe-integration | The current cred_type, currency and tranmode values |
| Israel Tax Authority allocation numbers | https://www.gov.il/he/service/request-assignment-number-for-tax-invoice | Required above the band for the invoice's own date: nothing before May 2024, then NIS 25,000 (May 2024), 20,000 (Jan 2025), 10,000 (Jan 2026), 5,000 (Jun 2026, in force) |
| Tranzila company site | https://www.tranzila.com | Terminal enablement requests, installment permissions, contact, PCI certification |
| tranzilajs community client | https://github.com/NirTatcher/tranzilajs | Community TypeScript/Node client and usage examples |

## Troubleshooting

### Error: "Transaction rejected with a non-000 response code"
Cause: Missing or invalid parameters, a card-issuer decline, or a config/permission issue. Remember the HTTP status is 200 even on failure, read the `Response` field for the actual code.
Solution: Verify all required parameters are present: supplier, TranzilaPW, sum, ccno (or TranzilaTK), expdate. Check parameter names are exact (case-sensitive). Look up the exact response code in the official Transaction Response Codes page (see references/error-codes.md), do not guess its meaning.

### Error: "Terminal not authorized for installments / Amex"
Cause: Your Tranzila terminal does not have installment (or Amex) permissions enabled.
Solution: Contact Tranzila support (073-222-4444) to enable installment or Amex processing on your terminal.

### Error: "Token charge fails but iframe worked"
Cause: Common when using wrong endpoint or missing expdate
Solution: Token charges use `/cgi-bin/tranzila31tk.cgi` (not tranzila31.cgi). Include both TranzilaTK and expdate parameters.

### Error: "Transaction approved in test but not production"
Cause: Test and production terminals behave differently
Solution: Verify your production terminal name and password. Some operations (like void) behave differently in production. Check with Tranzila support if behavior diverges.

### Error: "Currency mismatch"
Cause: Using wrong endpoint for currency
Solution: ILS and USD use `tranzila31.cgi`. Multi-currency (EUR, GBP, etc.) requires `tranzila36a.cgi`.