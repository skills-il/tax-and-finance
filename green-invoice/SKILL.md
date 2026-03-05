---
name: green-invoice
description: >-
  Integrate Green Invoice (Morning) API for Israeli invoicing, receipts, client
  management, and payment processing. Use when user asks to create invoices via
  Green Invoice, generate hashbonit mas through Morning API, manage clients in
  Green Invoice, set up webhook automation for document creation, query
  documents or expenses, or mentions "Green Invoice", "Morning", "hashbonit
  yeruka", "greeninvoice API", Israeli cloud invoicing, or needs to create tax
  invoice-receipt (cheshbonit mas/kabala). Covers all 13 document types, 8
  payment types, client CRUD, item catalog, and webhook integration. Do NOT use
  for SHAAM allocation numbers or Tax Authority e-invoice compliance (use
  israeli-e-invoice), Cardcom payment processing (use cardcom-payment-gateway),
  or Tranzila integration (use tranzila-payment-gateway).
license: MIT
compatibility: >-
  Requires network access for Green Invoice API calls (api.greeninvoice.co.il).
  API credentials obtained from Green Invoice dashboard (Settings, Developer
  Tools). Works with Claude Code, Claude.ai, Cursor.
metadata:
  author: skills-il
  version: 1.0.0
  category: tax-and-finance
  tags:
    he:
      - חשבונית-ירוקה
      - מורנינג
      - חשבונית
      - מע״מ
      - תשלומים
      - ישראל
    en:
      - green-invoice
      - morning
      - invoice
      - vat
      - payments
      - israel
  display_name:
    he: חשבונית ירוקה (מורנינג)
    en: Green Invoice (Morning)
  display_description:
    he: >-
      אינטגרציה עם API של חשבונית ירוקה (מורנינג) ליצירת חשבוניות, קבלות, ניהול
      לקוחות ועיבוד תשלומים לעסקים בישראל
    en: >-
      Integrate Green Invoice (Morning) API for Israeli invoicing, receipts,
      client management, and payment processing for businesses in Israel
  supported_agents:
    - claude-code
    - cursor
    - github-copilot
    - windsurf
    - opencode
    - codex
    - antigravity
---

# Green Invoice (Morning)

## Instructions

### Step 1: Authentication

Green Invoice uses JWT Bearer token authentication. Obtain API credentials from the Green Invoice dashboard: Settings > Developer Tools > API Keys.

**Base URLs:**

| Environment | Base URL |
|-------------|----------|
| Production | `https://api.greeninvoice.co.il/api/v1` |
| Sandbox | `https://sandbox.d.greeninvoice.co.il/api/v1` |

**Get a token:**

```bash
curl -X POST https://api.greeninvoice.co.il/api/v1/account/token \
  -H "Content-Type: application/json" \
  -d '{"id": "YOUR_API_KEY_ID", "secret": "YOUR_API_KEY_SECRET"}'
```

The response includes a JWT token. Use it in all subsequent requests:

```
Authorization: Bearer <token>
Content-Type: application/json
```

Always start by verifying credentials work:

```bash
curl -s https://api.greeninvoice.co.il/api/v1/users/me \
  -H "Authorization: Bearer <token>" | python3 -m json.tool
```

### Step 2: Understand Document Types

Green Invoice supports 13 document types. Each has a numeric code used in API calls.

| Code | Hebrew | English | Common Use |
|------|--------|---------|------------|
| 10 | הצעת מחיר | Price Quote | Pre-sale proposals |
| 100 | הזמנה | Order | Confirmed orders |
| 200 | תעודת משלוח | Delivery Note | Shipment documentation |
| 210 | תעודת החזרה | Return Note | Product returns |
| 300 | חשבון עסקה | Transaction Invoice | Invoice without payment |
| 305 | חשבונית מס | Tax Invoice | Standalone tax invoice |
| 320 | חשבונית מס / קבלה | Tax Invoice-Receipt | Most common for Israeli clients |
| 330 | חשבונית זיכוי | Credit Note | Refunds and corrections |
| 400 | קבלה | Receipt | Payment confirmation |
| 405 | קבלה על תרומה | Donation Receipt | Non-profit donations |
| 500 | הזמנת רכש | Purchase Order | Procurement |
| 600 | קבלת פיקדון | Deposit Receipt | Security deposits |
| 610 | משיכת פיקדון | Deposit Withdrawal | Deposit returns |

**Key rule:** For Israeli clients who pay immediately, use type `320` (Tax Invoice-Receipt). For invoices where payment comes later, use type `300` (Transaction Invoice). For international clients, use type `400` (Receipt).

### Step 3: Create Documents

**POST** `/v1/documents`

Required fields: `type`, `client` (with `name` and `emails`), `income` (line items array).

```json
{
  "type": 320,
  "date": "2026-03-05",
  "lang": "he",
  "currency": "ILS",
  "vatType": 0,
  "rounding": true,
  "signed": true,
  "attachment": true,
  "client": {
    "name": "Moshe Cohen",
    "emails": ["moshe@example.com"],
    "taxId": "123456789",
    "add": true
  },
  "income": [
    {
      "description": "Web Development Services",
      "quantity": 1,
      "price": 5000,
      "currency": "ILS",
      "vatType": 0
    }
  ],
  "payment": [
    {
      "type": 4,
      "date": "2026-03-05",
      "price": 5000,
      "currency": "ILS"
    }
  ]
}
```

**VAT types (document level):**

| Code | Meaning |
|------|---------|
| 0 | Default (VAT added based on business type) |
| 1 | Exempt (no VAT) |
| 2 | Mixed (some items exempt, some not) |

**VAT types (income row level):**

| Code | Meaning |
|------|---------|
| 0 | Default (follows document VAT setting) |
| 1 | VAT included in price |
| 2 | Exempt for this line item |

### Step 4: Payment Types

When adding payment records to a document, use these type codes:

| Code | Hebrew | English |
|------|--------|---------|
| -1 | לא שולם | Unpaid |
| 0 | ניכוי במקור | Withholding Tax |
| 1 | מזומן | Cash |
| 2 | המחאה | Check |
| 3 | כרטיס אשראי | Credit Card |
| 4 | העברה בנקאית | Bank Transfer |
| 5 | פייפאל | PayPal |
| 10 | אפליקציית תשלום | Payment App (Bit, Pepper Pay, PayBox) |
| 11 | אחר | Other |

**Credit card types** (when payment type is 3):

| Code | Card |
|------|------|
| 1 | Isracard |
| 2 | Visa |
| 3 | Mastercard |
| 4 | American Express |
| 5 | Diners |

**Credit card deal types:**

| Code | Type |
|------|------|
| 1 | Regular (ragil) |
| 2 | Installments (tashlumim) |
| 3 | Credit |
| 4 | Deferred (chiyuv nidche) |

### Step 5: Manage Clients

**Create client:** `POST /v1/clients`

```json
{
  "name": "Startup Ltd.",
  "emails": ["billing@startup.co.il"],
  "taxId": "515123456",
  "country": "IL",
  "city": "Tel Aviv",
  "address": "Rothschild 45",
  "paymentTerms": 30,
  "labels": ["tech", "monthly"]
}
```

**Payment terms:**

| Code | Meaning |
|------|---------|
| -1 | Immediate (shotef) |
| 0 | End of month (shotef sof chodesh) |
| 30 | End of month + 30 (shotef plus 30) |
| 60 | End of month + 60 |
| 90 | End of month + 90 |

**Other client endpoints:**

| Method | Path | Description |
|--------|------|-------------|
| GET | `/v1/clients/{id}` | Get client by ID |
| PUT | `/v1/clients/{id}` | Update client |
| DELETE | `/v1/clients/{id}` | Delete client |
| POST | `/v1/clients/search` | Search clients |

**Search clients:**

```json
{
  "name": "Startup",
  "active": true,
  "page": 0,
  "pageSize": 25
}
```

### Step 6: Search and Query Documents

**POST** `/v1/documents/search`

```json
{
  "page": 0,
  "pageSize": 25,
  "type": [320, 305],
  "status": [0, 1],
  "fromDate": "2026-01-01",
  "toDate": "2026-03-31",
  "sort": "documentDate"
}
```

**Document statuses:**

| Code | Meaning |
|------|---------|
| 0 | Open |
| 1 | Closed |
| 2 | Manually closed |
| 3 | Canceling another document |
| 4 | Canceled |

**Get document:** `GET /v1/documents/{id}`

**Close document:** `POST /v1/documents/{id}/close`

**Download document PDF:** `GET /v1/documents/{id}/download/links` returns URLs in Hebrew, English, and original language.

### Step 7: Link Documents

Documents can be linked to create workflows. Use `linkedDocumentIds` when creating a new document.

Common linking patterns:

| Scenario | Steps |
|----------|-------|
| Invoice then receipt | Create type 300 (invoice), later create type 400 (receipt) with `linkedDocumentIds: ["invoice-id"]` |
| Credit note for invoice | Create type 330 (credit note) with `linkedDocumentIds: ["original-id"]` and `linkType: "cancel"` |
| Quote to order to invoice | Create type 10 (quote), then type 100 (order), then type 300 (invoice), linking each |

When a receipt is linked to an invoice with full payment, the invoice automatically closes.

### Step 8: Item Catalog

Manage reusable product/service items:

| Method | Path | Description |
|--------|------|-------------|
| POST | `/v1/items` | Create item |
| GET | `/v1/items/{id}` | Get item |
| PUT | `/v1/items/{id}` | Update item |
| POST | `/v1/items/search` | Search items |

Use `itemId` in income line items to reference catalog items instead of manually specifying description and price each time.

### Step 9: Business Types and VAT Rules

Green Invoice handles VAT automatically based on business type:

| Code | Hebrew | English | VAT Behavior |
|------|--------|---------|-------------|
| 1 | עוסק מורשה | Licensed Dealer (Osek Murshe) | VAT added (17% as of 2025) |
| 2 | חברה בע"מ | Ltd. Company | VAT added |
| 3 | עוסק פטור | Exempt Dealer (Osek Patur) | No VAT |
| 4 | עמותה | Non-Profit (Amuta) | No VAT |
| 5 | חברה לתועלת הציבור | Public Benefit Company | No VAT |
| 6 | שותפות | Partnership | VAT added |

Set `vatType: 0` on documents and the system applies the correct VAT based on your business type. Override with `vatType: 1` for exempt transactions or `vatType: 2` for mixed documents.

### Step 10: Webhooks

Configure webhooks in: Settings > Developer Tools > Create Webhook.

Webhooks fire on document creation. The payload includes the full document object:

```json
{
  "id": "document-uuid",
  "type": 320,
  "number": 12345,
  "currency": "ILS",
  "date": "2026-03-05",
  "total": 5850,
  "recipient": {
    "name": "Client Name",
    "emails": ["client@example.com"]
  },
  "items": [
    {
      "description": "Service",
      "quantity": 1,
      "price": 5000
    }
  ],
  "files": {
    "signed": true,
    "downloadLinks": {
      "he": "https://www.greeninvoice.co.il/api/v1/documents/download?d=...",
      "en": "https://www.greeninvoice.co.il/api/v1/documents/download?d=..."
    }
  }
}
```

Common webhook automations:
- Save PDF to Google Drive or Dropbox on invoice creation
- Update CRM when a receipt is issued
- Send Slack notification for new documents
- Sync invoices to external accounting systems

Consult `references/api-reference.md` for the complete webhook payload schema.

### Step 11: Currencies and Exchange Rates

Green Invoice supports 28 currencies. If `currencyRate` is not specified, the system uses Bank of Israel (BOI) exchange rates for the document date.

Common currencies: ILS, USD, EUR, GBP, JPY, CHF, CAD, AUD.

For multi-currency invoices, each income line item can specify its own `currency` and `currencyRate`. The totals are always calculated in the document's base currency.

### Step 12: Sandbox Testing

Always test in the sandbox environment before going to production:

1. Register for a sandbox account at the Green Invoice sandbox
2. Use base URL: `https://sandbox.d.greeninvoice.co.il/api/v1`
3. Generate sandbox API credentials
4. Test all document creation, client management, and webhook flows
5. Verify VAT calculations and document linking work correctly
6. Switch to production URL when ready

## Examples

### Example 1: Create Tax Invoice-Receipt for Israeli Client

User says: "Create a hashbonit mas kabala for a client paying by bank transfer"

Actions:
1. Authenticate with Green Invoice API
2. Create client if new (POST `/v1/clients` with name, email, taxId)
3. Create document type 320 (Tax Invoice-Receipt) with payment type 4 (bank transfer)
4. Set `signed: true` for digital signature, `attachment: true` to email PDF

Result: Tax invoice-receipt created, digitally signed, and emailed to client as PDF.

### Example 2: Monthly Recurring Invoices

User says: "I need to send monthly invoices to 3 retainer clients"

Actions:
1. Search existing clients: POST `/v1/clients/search` with client names
2. For each client, create document type 300 (Transaction Invoice) with description "Monthly Retainer - March 2026"
3. Set `dueDate` to payment terms date, `lang` based on client preference
4. Documents are emailed automatically when `attachment: true`

Result: Three invoices created and sent, each with correct payment terms and language.

### Example 3: Issue Credit Note for Partial Refund

User says: "Refund half the amount on invoice #12345"

Actions:
1. Get original document: GET `/v1/documents/{id}`
2. Calculate refund amount (half of original total)
3. Create document type 330 (Credit Note) with `linkedDocumentIds: ["original-id"]` and `linkType: "cancel"`
4. Set income amount to negative refund value

Result: Credit note issued, linked to original invoice, with partial refund amount.

### Example 4: Webhook Automation for Document Filing

User says: "Set up automatic filing when Green Invoice creates a document"

Actions:
1. Configure webhook URL in Green Invoice dashboard
2. Implement webhook endpoint that receives document payload
3. Extract `type` field to route document (invoice vs receipt vs credit note)
4. Use `files.downloadLinks.he` to download the Hebrew PDF
5. File to appropriate folder based on document type and date

Result: All new documents automatically downloaded and organized by type and month.

## Bundled Resources

### Scripts
- `scripts/green-invoice-client.py` -- Python helper for common Green Invoice API operations: authenticate, create documents, search clients, and list recent documents. Run: `python3 scripts/green-invoice-client.py --help`

### References
- `references/api-reference.md` -- Complete Green Invoice API endpoint reference with request/response schemas, all enum codes, and payload examples. Consult when building API integrations or debugging request formats.
- `references/document-workflows.md` -- Common Israeli business document workflows: freelancer billing, retainer invoicing, refund flows, multi-currency billing, and e-commerce integration patterns. Consult when designing invoicing automation or choosing the correct document type sequence.

## Troubleshooting

### Error: "401 Unauthorized" on API calls
Cause: JWT token expired or invalid credentials
Solution: Tokens expire periodically. Re-authenticate by calling POST `/v1/account/token` with your API key ID and secret. Verify credentials in Green Invoice dashboard under Settings > Developer Tools.

### Error: "Document type not supported for your business type"
Cause: Osek Patur (exempt dealer) cannot issue Tax Invoices (type 305)
Solution: Check your business type. Osek Patur should use type 320 (Tax Invoice-Receipt) or type 400 (Receipt). Osek Murshe and Ltd. companies can use all document types.

### Error: "VAT calculation mismatch"
Cause: Mixing vatType settings between document level and income row level
Solution: Set `vatType: 0` at document level to use defaults. Only override at the income row level when you have mixed VAT items. If VAT is included in prices, set income row `vatType: 1`.

### Error: "Client email required"
Cause: Creating a document without providing client email
Solution: The `client.emails` array must contain at least one valid email when `attachment: true`. For documents that should not be emailed, set `attachment: false`.
