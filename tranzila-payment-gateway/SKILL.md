---
name: tranzila-payment-gateway
description: >-
  Integrate Tranzila payment processing into Israeli applications -- covers
  iframe payments, tokenization, installments (tashlumim), refunds, 3D Secure,
  and Bit wallet. Use when user asks to accept payments via Tranzila, integrate
  Israeli credit card processing, set up "slikat ashrai", handle tashlumim
  (installment payments), create payment tokens, process refunds through
  Tranzila, or mentions "Tranzila", "tranzila API", "secure5", or Israeli
  online payments. Supports both legacy CGI endpoints and modern API V2.
  Do NOT use for Cardcom integration (use cardcom-payment-gateway), general
  accounting, or non-payment financial queries.
license: MIT
compatibility: >-
  Requires network access for Tranzila API calls. Works with Claude Code,
  Claude.ai, Cursor.
metadata:
  author: skills-il
  version: 1.0.0
  category: tax-and-finance
  tags:
    - payments
    - credit-card
    - tranzila
    - slikat-ashrai
    - israel
  display_name:
    he: שער תשלומים טרנזילה
    en: Tranzila Payment Gateway
  display_description:
    he: אינטגרציה עם טרנזילה לסליקת אשראי, תשלומים בתשלומים, טוקניזציה והחזרים
    en: >-
      Integrate Tranzila payment processing into Israeli applications -- covers
      iframe payments, tokenization, installments (tashlumim), refunds, 3D Secure,
      and Bit wallet. Use when user asks to accept payments via Tranzila, integrate
      Israeli credit card processing, set up "slikat ashrai", handle tashlumim
      (installment payments), create payment tokens, process refunds through
      Tranzila, or mentions "Tranzila", "tranzila API", "secure5", or Israeli
      online payments. Supports both legacy CGI endpoints and modern API V2.
      Do NOT use for Cardcom integration (use cardcom-payment-gateway), general
      accounting, or non-payment financial queries.
  supported_agents:
    - claude-code
    - cursor
    - github-copilot
    - windsurf
    - opencode
    - codex
    - openclaw
---

# Tranzila Payment Gateway

## Overview

Tranzila is one of Israel's leading payment processors (solek), operating since 1999. It connects to the Shva network (reshet shva) -- Israel's central card processing infrastructure -- and supports all Israeli card issuers: Isracard, Visa Cal, Leumi Card/Max.

This skill guides integration with Tranzila for accepting credit card payments (slikat kartis ashrai) in Israeli applications.

## Instructions

### Step 1: Choose Integration Pattern

Help the user select the right approach based on their needs:

| Pattern | Hebrew | PCI Scope | Best For |
|---------|--------|-----------|----------|
| **Iframe** | daf tashlum mutman | Minimal (SAQ-A) | Quick integration, minimal compliance |
| **Hosted Fields** | sdot mitarachim | Low (SAQ-A-EP) | Custom checkout UX with low PCI burden |
| **API V2 (server-to-server)** | sharat le-sharat | Full (SAQ-D) | Token charging, recurring, refunds |

Most Israeli merchants start with **Iframe** for collecting payments, then use **API V2** for server-side operations like token charging and refunds.

### Step 2: Set Up Authentication

Tranzila uses different credentials depending on the integration:

**For Iframe / Legacy CGI:**
- `supplier` -- Terminal name (provided by Tranzila)
- `TranzilaPW` -- Transaction password

**For API V2:**
- `X-tranzila-api-app-key` HTTP header -- Application key from Tranzila dashboard

Remind the user to store credentials securely (environment variables, secrets manager) and never commit them to source control.

### Step 3: Implement the Payment Flow

#### Option A: Iframe Integration (Recommended Start)

1. Embed the Tranzila iframe in your checkout page:
   - URL: `https://direct.tranzila.com/{supplier}/iframenew.php`
   - Add query parameters: `sum`, `currency`, `cred_type`
   - Default mode creates a token (J5); use J4 for one-time charge

2. Handle the response via your `notify_url`:
   - Tranzila POSTs results to your server
   - Check `Response` field: `000` = approved
   - Store `TranzilaTK` (token) for future charges

3. Confirm transaction server-side (recommended):
   - Use the three-sided handshake to verify the transaction is genuine

#### Option B: Server-to-Server via API V2

For token charging, refunds, and operations that don't involve card entry:

**Charge a token:**
```
POST https://secure5.tranzila.com/cgi-bin/tranzila31tk.cgi
Content-Type: application/x-www-form-urlencoded

supplier={terminal}&TranzilaPW={password}&TranzilaTK={token}&expdate={MMYY}&sum={amount}&currency=1&cred_type=1
```

**Process a refund:**
Use `tranmode=C{index}` with the original `ConfirmationCode` and `index` from the original transaction.

Consult `references/api-parameters.md` for the complete parameter reference.

### Step 4: Handle Israeli-Specific Payment Types

Israeli payments have unique features that differ from international processing:

**Installments (Tashlumim):**
- Set `cred_type=8` for regular installments
- Parameters: `npay` (number of payments minus 1), `fpay` (first payment), `spay` (subsequent payments)
- The sum of `fpay + (npay * spay)` must equal the total `sum`
- Not all terminals are authorized for installments (error code 111 if not)

**Credit Types (cred_type):**

| Value | Type | Hebrew |
|-------|------|--------|
| 1 | Regular credit | ashrai ragil |
| 2 | Visa Adif / Amex Credit | |
| 3 | Immediate debit | hiyuv miyadi |
| 5 | Leumi Special | |
| 8 | Installments | tashlumim |
| 9 | Club installments | tashlumei moadan |

**Currency codes (matbea):**

| Code | Currency | Hebrew |
|------|----------|--------|
| 1 | ILS (Shekel) | shekel chadash |
| 2 | USD | dolar |
| 3 | GBP | lira sterling |
| 7 | EUR | euro |

**Israeli ID (teudat zehut):**
Some transactions require `myid` parameter -- a 9-digit Israeli ID number (mispar zehut).

### Step 5: Implement Tokenization for Recurring Payments (hora'ot keva)

Tokens (asmachta) let you charge returning customers without handling card data again:

1. **Create token during first payment:**
   - Iframe: Default behavior (J5 mode) returns `TranzilaTK`
   - API: Use `tranmode=K` (token only), `VK` (verify + token), or `AK` (charge + token)

2. **Store the token securely:**
   - Token is a 19-character string (last 4 digits match the card)
   - Store token, expiry date, and card last-4 in your database
   - Token has no value without your terminal credentials

3. **Charge the token later:**
   - Use the `/cgi-bin/tranzila31tk.cgi` endpoint
   - Include `TranzilaTK`, `expdate`, `sum`, and `currency`

### Step 6: Add 3D Secure (if required)

3D Secure V2 adds cardholder authentication. Consult `references/3ds-flow.md` for the full redirect-based flow. Key points:
- 3DS changes the payment flow to include a bank authentication step
- Response includes additional fields for authentication status
- Some Israeli issuers may not support 3DS for all card types

### Step 7: Handle Errors

Check the `Response` field in every transaction result. `000` means approved -- anything else is an error.

Common errors to handle in your code:

| Code | Meaning | Hebrew | User Action |
|------|---------|--------|-------------|
| 004 | Card declined | kartis surav | Ask user to try another card |
| 036 | Card expired | kartis pagum tokef | Ask user to update card details |
| 107 | Amount exceeds limit | chriga memichsa | Reduce amount or contact bank |
| 111 | Not authorized for installments | ein harshaah letashlumim | Contact Tranzila to enable |
| 125 | Not authorized for Amex | ein harshaah le-Amex | Contact Tranzila to enable |
| 200 | Application error | shegihat mimshal | Retry; if persistent, check parameters |
| 900 | 3DS authentication failed | imut 3DS nichal | Retry without 3DS or ask user to authenticate |

For the full error code reference (170+ codes), consult `references/error-codes.md`.

## Examples

### Example 1: Accept a One-Time Payment
User says: "I need to add credit card payments to my Node.js checkout page"
Actions:
1. Choose: Iframe integration (minimal PCI scope)
2. Guide: Embed iframe with supplier name, sum, currency=1 (ILS)
3. Implement: Server-side notify_url handler to capture response
4. Validate: Check Response=000, store ConfirmationCode
Result: Working checkout that accepts Israeli credit cards via embedded form.

### Example 2: Set Up Monthly Subscription
User says: "I want to charge customers 99 NIS every month automatically"
Actions:
1. First payment: Iframe with token creation (J5 mode)
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
1. Use: tranmode=C0 (cancel first transaction in batch)
2. Include: Original ConfirmationCode and index
3. Set: sum to refund amount (partial or full)
4. Verify: Response=000 for successful refund
Result: Refund processed and linked to original transaction.

## Bundled Resources

### References
- `references/api-parameters.md` -- Complete Tranzila API parameter reference for both legacy CGI and API V2 endpoints, including authentication headers, transaction parameters, token operations, and installment fields. Consult when constructing API requests or debugging unexpected parameter behavior.
- `references/error-codes.md` -- Full listing of Tranzila response codes (000-999) with meanings and recommended handling. Consult when a transaction returns a non-000 response code.
- `references/3ds-flow.md` -- Step-by-step 3D Secure V2 implementation guide for Tranzila, including redirect flow, authentication parameters, and fallback handling. Consult when adding 3DS to an existing integration.

### Scripts
- `scripts/validate_tranzila_response.py` -- Validates a Tranzila transaction response: checks response code, verifies required fields are present, and flags common issues (missing confirmation code, mismatched amounts). Run: `python scripts/validate_tranzila_response.py --help`

## Troubleshooting

### Error: "Response code 200 -- Application error"
Cause: Missing or invalid parameters in the API request
Solution: Verify all required parameters are present: supplier, TranzilaPW, sum, ccno (or TranzilaTK), expdate. Check parameter names are exact (case-sensitive).

### Error: "Response code 111 -- Terminal not authorized for installments"
Cause: Your Tranzila terminal does not have installment permissions enabled
Solution: Contact Tranzila support (073-222-4444) to enable installment processing on your terminal.

### Error: "Token charge fails but iframe worked"
Cause: Common when using wrong endpoint or missing expdate
Solution: Token charges use `/cgi-bin/tranzila31tk.cgi` (not tranzila31.cgi). Include both TranzilaTK and expdate parameters.

### Error: "Transaction approved in test but not production"
Cause: Test and production terminals behave differently
Solution: Verify your production terminal name and password. Some operations (like void) behave differently in production. Check with Tranzila support if behavior diverges.

### Error: "Currency mismatch"
Cause: Using wrong endpoint for currency
Solution: ILS and USD use `tranzila31.cgi`. Multi-currency (EUR, GBP, etc.) requires `tranzila36a.cgi`.