# Green Invoice Document Workflows

Common Israeli business document workflows using the Green Invoice (Morning) API.

## Workflow 1: Freelancer Monthly Billing

A freelancer (osek murshe or osek patur) billing clients monthly.

**Flow:**
1. Search for client: `POST /v1/clients/search` with client name
2. Create Tax Invoice-Receipt (type 320) with monthly service description
3. Include payment record matching how the client paid

**Osek Murshe (Licensed Dealer):**
- Use type 320 with `vatType: 0` (VAT automatically added at 17%)
- Total = subtotal + VAT
- Example: NIS 10,000 service = NIS 11,700 total

**Osek Patur (Exempt Dealer):**
- Use type 320 with `vatType: 0` (no VAT added automatically)
- Total = subtotal (no VAT)
- Cannot issue standalone Tax Invoice (type 305)
- Annual revenue limit: NIS 120,000 (as of 2025, verify current threshold)

**Best Practice:** Use labels on clients (e.g., "monthly", "retainer") to easily search and batch-process recurring invoices.

---

## Workflow 2: Quote to Invoice to Receipt

A full sales cycle from price quote to final receipt.

**Step 1 - Price Quote:**
```
POST /v1/documents
type: 10 (Price Quote)
```
Send to client for approval. Quote has no tax implications.

**Step 2 - Order Confirmation:**
```
POST /v1/documents
type: 100 (Order)
linkedDocumentIds: ["quote-id"]
```
Links back to the original quote.

**Step 3 - Invoice:**
```
POST /v1/documents
type: 300 (Transaction Invoice)
linkedDocumentIds: ["order-id"]
```
Client has not paid yet. Invoice is open.

**Step 4 - Receipt:**
```
POST /v1/documents
type: 400 (Receipt)
linkedDocumentIds: ["invoice-id"]
payment: [{ type: 4, price: full_amount }]
```
When payment is received. Linking with full payment automatically closes the invoice.

**Shortcut:** For immediate payment, skip steps 1-3 and issue type 320 (Tax Invoice-Receipt) directly.

---

## Workflow 3: Credit Note (Refund)

Issuing a refund or correction for an existing invoice.

**Full Refund:**
```
POST /v1/documents
type: 330 (Credit Note)
linkedDocumentIds: ["original-invoice-id"]
linkType: "cancel"
income: [{ same items as original, same amounts }]
```

**Partial Refund:**
```
POST /v1/documents
type: 330 (Credit Note)
linkedDocumentIds: ["original-invoice-id"]
linkType: "cancel"
income: [{ description: "Partial refund", price: refund_amount }]
```

**Important:** Credit notes must reference the original document. The `linkType: "cancel"` marks the relationship as a cancellation. For partial refunds, only include the refunded amount in the income lines.

---

## Workflow 4: Multi-Currency International Billing

Billing international clients in foreign currencies.

**Create Document:**
```json
{
  "type": 400,
  "currency": "USD",
  "lang": "en",
  "client": {
    "name": "International Corp",
    "country": "US",
    "emails": ["billing@intl.com"]
  },
  "income": [
    {
      "description": "Consulting Services",
      "quantity": 10,
      "price": 150,
      "currency": "USD"
    }
  ],
  "payment": [
    {
      "type": 5,
      "price": 1500,
      "currency": "USD"
    }
  ]
}
```

**Key Points:**
- Use type 400 (Receipt) for international clients (not type 320)
- Set document `lang: "en"` for English
- Set `currency` to the client's currency (USD, EUR, GBP, etc.)
- If `currencyRate` is omitted, Green Invoice uses Bank of Israel exchange rates
- VAT is typically exempt for international transactions (`vatType: 1`)

---

## Workflow 5: E-Commerce Order Processing

Automating invoice generation for online store orders.

**On Order Completion:**
1. Create or find client by email: `POST /v1/clients/search`
2. If new client, create with `add: true` in the document's client object
3. Create Tax Invoice-Receipt (type 320) with order items
4. Payment type depends on payment method used:
   - Credit card: type 3, with cardType and dealType
   - Bit: type 10, appType: 1
   - PayPal: type 5

**Batch Processing:**
For high-volume stores, queue orders and create documents in batches. Green Invoice API has rate limits, so space requests appropriately.

**Webhook Integration:**
Set up a webhook to receive document creation confirmations. Use the `files.downloadLinks` from the webhook payload to archive PDFs.

---

## Workflow 6: Retainer Client with Monthly Advance Invoices

Sending invoices at the start of each month for ongoing services.

**Monthly Flow:**
1. Create Transaction Invoice (type 300) at month start
2. Set `dueDate` based on client's payment terms
3. When payment is received, create Receipt (type 400) linked to the invoice
4. The linked receipt automatically closes the invoice

**With Deposit:**
1. Receive deposit: Create Deposit Receipt (type 600)
2. Monthly invoicing: Create Transaction Invoice (type 300)
3. Apply deposit: Create Deposit Withdrawal (type 610) linked to invoice
4. Collect remaining balance: Create Receipt (type 400) for the difference

---

## Workflow 7: Withholding Tax (Nikui Bamkor)

When clients withhold tax at source before paying.

**Example:** Client owes NIS 10,000 but withholds 20% (NIS 2,000) for tax.

```json
{
  "type": 320,
  "income": [
    { "description": "Service", "quantity": 1, "price": 10000, "currency": "ILS" }
  ],
  "payment": [
    { "type": 4, "price": 8000, "currency": "ILS" },
    { "type": 0, "price": 2000, "currency": "ILS" }
  ]
}
```

Payment type 0 (Withholding Tax) records the amount withheld. The document total remains NIS 10,000 + VAT, but the actual payment received is NIS 8,000 + the NIS 2,000 withheld for tax authorities.

---

## Workflow 8: Donation Receipts for Non-Profits

For amutot (non-profits) issuing donation receipts under Section 46.

**Create Donation Receipt:**
```json
{
  "type": 405,
  "vatType": 1,
  "client": {
    "name": "Donor Name",
    "taxId": "donor-tz",
    "emails": ["donor@example.com"]
  },
  "income": [
    { "description": "Donation", "quantity": 1, "price": 5000, "currency": "ILS" }
  ]
}
```

**Key Points:**
- Type 405 (Donation Receipt) is only available for business type 4 (Amuta)
- Set `vatType: 1` (exempt) as donations are not subject to VAT
- Include donor's `taxId` (Teudat Zehut) for Section 46 tax deduction eligibility
- The receipt allows the donor to claim a tax deduction (35% of donation amount, up to limits)

---

## Common Patterns

### Auto-Save Client on Document Creation
Set `client.add: true` in the document creation payload. This automatically adds a new client to your client list when creating a document, avoiding a separate API call.

### Close Document Without Payment
Use `POST /v1/documents/{id}/close` to manually mark a document as closed without creating a linked receipt. Use for write-offs or adjustments.

### Currency Rate Override
When you have a specific exchange rate (e.g., from the contract), set `currencyRate` explicitly. This overrides the Bank of Israel rate. The rate is always relative to ILS.

### Document Language Per Client
Set `lang` based on client preference. Israeli clients typically get "he", international clients get "en". The download links always provide both language versions regardless.
