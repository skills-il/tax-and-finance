---
name: cardcom-payment-gateway
description: >-
  Integrate Cardcom payment processing and Israeli invoice generation into
  applications -- covers Low Profile payments, tokenization, recurring billing,
  and automatic tax invoice/receipt creation per Israeli law. Use when user asks
  to accept payments via Cardcom, generate Israeli invoices with payments,
  set up "slikat ashrai" with hashbonit, handle recurring billing (hora'ot keva),
  or mentions "Cardcom", "CardCom API", "Low Profile", Israeli payment with
  invoicing, or needs combined payment + document generation. Supports REST
  API V11 and legacy endpoints. Do NOT use for Tranzila integration (use
  tranzila-payment-gateway), general accounting, or non-payment queries.
license: MIT
compatibility: >-
  Requires network access for Cardcom API calls. Works with Claude Code,
  Claude.ai, Cursor.
metadata:
  author: skills-il
  version: 1.0.0
  category: tax-and-finance
  tags:
    - payments
    - credit-card
    - cardcom
    - invoice
    - slikat-ashrai
    - israel
  display_name:
    he: שער תשלומים קארדקום
    en: Cardcom Payment Gateway
  display_description:
    he: אינטגרציה עם קארדקום לסליקת אשראי, הפקת חשבוניות מס וקבלות אוטומטית
    en: >-
      Integrate Cardcom payment processing and Israeli invoice generation into
      applications -- covers Low Profile payments, tokenization, recurring billing,
      and automatic tax invoice/receipt creation per Israeli law. Use when user asks
      to accept payments via Cardcom, generate Israeli invoices with payments,
      set up "slikat ashrai" with hashbonit, handle recurring billing (hora'ot keva),
      or mentions "Cardcom", "CardCom API", "Low Profile", Israeli payment with
      invoicing, or needs combined payment + document generation. Supports REST
      API V11 and legacy endpoints. Do NOT use for Tranzila integration (use
      tranzila-payment-gateway), general accounting, or non-payment queries.
---

# Cardcom Payment Gateway

## Overview

Cardcom is an Israeli payment processor with a unique strength: integrated invoice and receipt generation compliant with Israeli tax law. While other Israeli gateways handle only the payment, Cardcom can automatically generate tax invoices (hashbonit mas) and receipts (kabala) as part of the payment flow -- something Israeli businesses are legally required to issue.

This skill guides integration with Cardcom's REST API V11 for payments, tokenization, recurring billing, and document generation.

## Instructions

### Step 1: Choose Integration Pattern

| Pattern | Card Data Handling | Best For |
|---------|-------------------|----------|
| **Low Profile (iframe/redirect)** | Cardcom handles card entry | Most integrations -- minimal PCI scope |
| **ChargeToken (server-to-server)** | Token only, no raw card data | Recurring charges, subscription billing |
| **CreateDocument (server-to-server)** | No card data | Standalone invoice/receipt generation |

Most Israeli merchants use **Low Profile** for initial payment + token creation, then **ChargeToken** for recurring charges. Both can auto-generate invoices.

### Step 2: Set Up Authentication

Cardcom API V11 credentials:
- `TerminalNumber` -- Your terminal ID (use `1000` for testing)
- `ApiName` -- API username (use `bWlyb24gY2FyZGNvbQ==` for testing)
- `ApiPassword` -- API password

**Test environment:**
Terminal `1000` with the test credentials allows full API testing without real charges. Test card: `4580000000000000`, any future expiry, CVV `123`.

Store credentials securely -- never in source code or client-side JavaScript.

### Step 3: Implement the Payment Flow

#### Low Profile Integration (Recommended)

This is a two-step process:

**Step 3a: Create the payment page**

```
POST https://secure.cardcom.solutions/api/v11/LowProfile/Create
Content-Type: application/json

{
  "TerminalNumber": 1000,
  "ApiName": "your-api-name",
  "ApiPassword": "your-api-password",
  "ReturnValue": "unique-order-id",
  "Amount": 100.00,
  "SuccessRedirectUrl": "https://yoursite.com/success",
  "FailedRedirectUrl": "https://yoursite.com/failed",
  "WebHookUrl": "https://yoursite.com/webhook",
  "Document": {
    "DocTypeToCreate": 101,
    "Name": "Customer Name",
    "Products": [
      {
        "Description": "Product name",
        "UnitCost": 100.00,
        "Quantity": 1
      }
    ]
  },
  "CoinID": 1,
  "Language": "he"
}
```

Response includes `Url` -- redirect customer there or embed as iframe.

**Step 3b: Get the results**

After payment completes, Cardcom calls your `WebHookUrl` or you query:

```
POST https://secure.cardcom.solutions/api/v11/LowProfile/GetLpResult
{
  "TerminalNumber": 1000,
  "ApiName": "your-api-name",
  "ApiPassword": "your-api-password",
  "LowProfileCode": "code-from-step-3a"
}
```

Check `DealResponse` = 0 for success. Extract `Token` for future charges.

### Step 4: Generate Israeli Tax Documents

Cardcom's standout feature is automatic document generation with payments. This is critical for Israeli businesses because tax law requires issuing proper documents for every transaction.

**Document types (DocTypeToCreate):**

| Code | Hebrew | English | When to Use |
|------|--------|---------|-------------|
| 1 | hashbonit mas | Tax Invoice | B2B sales, services |
| 2 | hashbonit zikui | Credit Note | Refunds, corrections |
| 3 | kabala | Receipt | Payment confirmation |
| 101 | hashbonit mas / kabala | Tax Invoice + Receipt | B2C with payment (most common) |
| 400 | -- | Iframe document | Low Profile context |

**Include document in payment flow:**
Add the `Document` object to your Low Profile or ChargeToken request (as shown in Step 3a). Cardcom generates the document automatically when payment succeeds.

**Standalone document creation:**

```
POST https://secure.cardcom.solutions/api/v11/Documents/CreateDocument
{
  "TerminalNumber": 1000,
  "ApiName": "your-api-name",
  "ApiPassword": "your-api-password",
  "Document": {
    "DocTypeToCreate": 1,
    "Name": "Customer Ltd",
    "VAT_Number": "123456789",
    "Products": [
      {
        "Description": "Web development services",
        "UnitCost": 5000.00,
        "Quantity": 1,
        "IsVatFree": false
      }
    ],
    "SendByEmail": true,
    "Email": "customer@example.com",
    "Language": "he",
    "CoinID": 1
  }
}
```

Response includes `InvoiceNumber`, `InvoiceType`, and `Link` to the PDF document.

### Step 5: Implement Token-Based Recurring Payments

For subscriptions and recurring billing (hora'ot keva):

1. **Create token during first payment:**
   - Use Low Profile with token creation enabled
   - Response includes `Token`, `CardValidityMonth`, `CardValidityYear`

2. **Store token securely:**
   - Save token (UUID format), card expiry, and last 4 digits
   - Token is bound to your terminal

3. **Charge the token:**

```
POST https://secure.cardcom.solutions/api/v11/Transactions/Transaction
{
  "TerminalNumber": 1000,
  "ApiName": "your-api-name",
  "ApiPassword": "your-api-password",
  "Token": "token-uuid",
  "CardValidityMonth": "12",
  "CardValidityYear": "2027",
  "Amount": 99.00,
  "Document": {
    "DocTypeToCreate": 101,
    "Name": "Subscriber Name",
    "Products": [
      {
        "Description": "Monthly subscription - February 2026",
        "UnitCost": 99.00,
        "Quantity": 1
      }
    ],
    "SendByEmail": true,
    "Email": "customer@example.com"
  }
}
```

Each token charge can automatically generate and email an invoice.

### Step 6: Process Refunds

Refund a transaction and optionally generate a credit note:

```
POST https://secure.cardcom.solutions/api/v11/Transactions/RefundByTransactionId
{
  "TerminalNumber": 1000,
  "ApiName": "your-api-name",
  "ApiPassword": "your-api-password",
  "TransactionId": "original-transaction-id",
  "Amount": 100.00,
  "Document": {
    "DocTypeToCreate": 2,
    "Name": "Customer Name"
  }
}
```

This both refunds the payment AND generates a credit note (hashbonit zikui) -- handling both the financial and tax compliance sides in one call.

### Step 7: Handle Errors

Check response codes in every API call. A response of `0` means success.

Common errors:

| Code | Meaning | Action |
|------|---------|--------|
| 0 | Success | Proceed normally |
| 5033 | Terminal number missing | Check TerminalNumber in request |
| 5034 | Authentication failed | Verify ApiName and ApiPassword |
| 5035 | Invalid amount | Ensure Amount is positive number |
| 5100 | Card declined | Ask user to try another card |
| 5101 | Expired card | Ask user to update card details |
| 5102 | CVV incorrect | Ask user to re-enter CVV |
| 5200 | Token not found | Verify token UUID and terminal match |
| 5300 | Invoice creation failed | Check Document parameters |

For the full API response reference, consult `references/api-responses.md`.

## Examples

### Example 1: E-commerce Checkout with Invoice
User says: "I need to accept payments on my Israeli e-commerce site and generate tax invoices automatically"
Actions:
1. Choose: Low Profile integration with DocTypeToCreate=101 (tax invoice + receipt)
2. Guide: Create Low Profile page with product details in Document object
3. Implement: WebHook handler for payment confirmation
4. Result: Customer pays, gets automatic hashbonit mas/kabala emailed as PDF
Result: Full checkout flow with automatic Israeli tax document compliance.

### Example 2: Monthly SaaS Subscription
User says: "I run a SaaS product, I need to charge users 149 NIS monthly and send them invoices"
Actions:
1. First payment: Low Profile with token creation
2. Store: Token, card expiry from response
3. Monthly cron: ChargeToken with Document for each billing cycle
4. Handle: Failed charges, expired cards, email invoices
Result: Automated recurring billing with monthly invoice generation.

### Example 3: Standalone Invoice Without Payment
User says: "I need to generate a tax invoice for a bank transfer payment I already received"
Actions:
1. Use: CreateDocument endpoint (no payment processing)
2. Set: DocTypeToCreate=1 (tax invoice)
3. Include: Customer details, line items, amounts
4. Send: Set SendByEmail=true with customer email
Result: Tax invoice generated and emailed without credit card processing.

### Example 4: Process a Refund with Credit Note
User says: "Customer wants a refund for order #5678, need to issue a credit note too"
Actions:
1. Use: RefundByTransactionId endpoint
2. Include: Document with DocTypeToCreate=2 (credit note)
3. Process: Refund + credit note generated in single API call
4. Verify: DealResponse=0 for success
Result: Refund processed and hashbonit zikui (credit note) generated automatically.

## Bundled Resources

### References
- `references/api-endpoints.md` -- Complete Cardcom REST API V11 endpoint reference including Low Profile, Transactions, Documents, RecurringPayments, Financial, and CompanyOperations. Lists request/response fields for each endpoint. Consult when building API integrations or exploring available operations.
- `references/api-responses.md` -- Full listing of Cardcom response codes with meanings and recommended handling for transaction, token, and invoice operations. Consult when debugging failed API calls.
- `references/document-types.md` -- Israeli tax document type codes (1, 2, 3, 101, 400) with required fields, VAT handling, and usage guidelines per Israeli tax law. Consult when determining which document type to generate for a transaction.

### Scripts
- `scripts/validate_cardcom_response.py` -- Validates a Cardcom API response: checks response codes for transaction, token, and invoice operations, verifies required fields, and flags common integration issues. Run: `python scripts/validate_cardcom_response.py --help`

## Troubleshooting

### Error: "5033 -- Terminal Number is Missing"
Cause: TerminalNumber not included or sent as wrong type
Solution: Ensure TerminalNumber is sent as an integer (not string) in the JSON body. For testing, use 1000.

### Error: "5034 -- Authentication failed"
Cause: Invalid ApiName or ApiPassword
Solution: Verify credentials in your Cardcom dashboard. For testing, use terminal 1000 with the test API credentials. Credentials are separate from your login password.

### Error: "Low Profile page loads but payment fails"
Cause: Often a WebHookUrl or redirect URL issue
Solution: Ensure SuccessRedirectUrl, FailedRedirectUrl, and WebHookUrl are publicly accessible HTTPS URLs. Localhost URLs do not work -- use a tunnel (ngrok) for development.

### Error: "Invoice created but not emailed"
Cause: SendByEmail not set or email address missing
Solution: Set `SendByEmail: true` and include a valid `Email` in the Document object. Check spam folders -- Cardcom sends from their domain.

### Error: "Token charge succeeds but no invoice"
Cause: Document object missing from ChargeToken request
Solution: Include the full Document object with DocTypeToCreate, Name, and Products in every token charge request. Document generation is opt-in per transaction, not automatic.
