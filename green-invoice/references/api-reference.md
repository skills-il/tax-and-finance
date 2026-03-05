# Green Invoice API Reference

Complete reference for all Green Invoice (Morning) API endpoints, request/response schemas, and enum codes.

## Base URLs

| Environment | URL |
|-------------|-----|
| Production | `https://api.greeninvoice.co.il/api/v1` |
| Sandbox | `https://sandbox.d.greeninvoice.co.il/api/v1` |
| WebSocket | `wss://wss.greeninvoice.co.il` |

## Authentication

### POST /v1/account/token

**Request:**
```json
{
  "id": "api_key_id",
  "secret": "api_key_secret"
}
```

**Response:**
Returns JWT token in `X-Authorization-Bearer` header and in response body `token` field.

Use in all subsequent requests: `Authorization: Bearer <token>`

---

## Documents API

### POST /v1/documents (Create Document)

**Full Request Schema:**
```json
{
  "description": "string",
  "remarks": "string",
  "footer": "string",
  "emailContent": "string",
  "type": 320,
  "date": "YYYY-MM-DD",
  "dueDate": "YYYY-MM-DD",
  "lang": "he|en",
  "currency": "ILS",
  "vatType": 0,
  "discount": {
    "amount": 10,
    "type": "sum|percentage"
  },
  "rounding": true,
  "signed": true,
  "attachment": true,
  "maxPayments": 1,
  "client": {
    "id": "string (optional, use for existing client)",
    "name": "string (required for new)",
    "emails": ["string"],
    "taxId": "string",
    "department": "string",
    "address": "string",
    "city": "string",
    "zip": "string",
    "country": "IL",
    "phone": "string",
    "mobile": "string",
    "contactPerson": "string",
    "accountingKey": "string",
    "paymentTerms": -1,
    "labels": ["string"],
    "add": true,
    "self": false
  },
  "income": [
    {
      "catalogNum": "SKU-001",
      "description": "string (required)",
      "quantity": 1,
      "price": 100.00,
      "currency": "ILS",
      "currencyRate": 1.0,
      "vatRate": 0.17,
      "vatType": 0,
      "itemId": "string (optional, reference to catalog)"
    }
  ],
  "payment": [
    {
      "type": 3,
      "subType": 0,
      "date": "YYYY-MM-DD",
      "price": 100.00,
      "currency": "ILS",
      "currencyRate": 1.0,
      "quantity": 1,
      "bankName": "string",
      "bankBranch": "string",
      "bankAccount": "string",
      "chequeNum": "string",
      "cardType": 2,
      "cardNum": "string",
      "dealType": 1,
      "numPayments": 1,
      "firstPayment": 100.00,
      "appType": 0
    }
  ],
  "linkedDocumentIds": ["string"],
  "linkedPaymentId": "string",
  "linkType": "link|cancel",
  "paymentRequestData": {
    "maxPayments": 12,
    "plugins": [
      {
        "id": "plugin-uuid",
        "group": 100,
        "type": 12100
      }
    ]
  }
}
```

### GET /v1/documents/{id}

Returns full document object.

### POST /v1/documents/search

**Request:**
```json
{
  "page": 0,
  "pageSize": 25,
  "number": 12345,
  "type": [320, 305, 300],
  "status": [0, 1],
  "paymentTypes": [3, 4],
  "fromDate": "YYYY-MM-DD",
  "toDate": "YYYY-MM-DD",
  "clientId": "string",
  "clientName": "string",
  "description": "string",
  "download": false,
  "sort": "documentDate|creationDate"
}
```

### POST /v1/documents/{id}/close

Closes an open document.

### GET /v1/documents/{id}/download/links

**Response:**
```json
{
  "he": "https://www.greeninvoice.co.il/api/v1/documents/download?d=...",
  "en": "https://www.greeninvoice.co.il/api/v1/documents/download?d=...",
  "origin": "https://www.greeninvoice.co.il/api/v1/documents/download?d=..."
}
```

---

## Clients API

### POST /v1/clients (Create)

```json
{
  "name": "string (required)",
  "emails": ["string (required)"],
  "active": true,
  "department": "string",
  "taxId": "string",
  "accountingKey": "string",
  "paymentTerms": 30,
  "bankName": "string",
  "bankBranch": "string",
  "bankAccount": "string",
  "address": "string",
  "city": "string",
  "zip": "string",
  "country": "IL",
  "category": 0,
  "subCategory": 0,
  "phone": "string",
  "fax": "string",
  "mobile": "string",
  "remarks": "string",
  "contactPerson": "string",
  "labels": ["string"]
}
```

### GET /v1/clients/{id}

### PUT /v1/clients/{id}

### DELETE /v1/clients/{id}

### POST /v1/clients/search

```json
{
  "name": "string",
  "active": true,
  "email": "string",
  "contactPerson": "string",
  "labels": ["string"],
  "taxId": "string",
  "page": 0,
  "pageSize": 25
}
```

### POST /v1/clients/{id}/assoc

Associates documents to a client.

---

## Items API

### POST /v1/items (Create)
### GET /v1/items/{id}
### PUT /v1/items/{id}
### POST /v1/items/search

---

## Businesses API

### GET /v1/businesses
### POST /v1/businesses/search

---

## Users API

### GET /v1/users/me

Returns the authenticated user profile.

---

## Enum Reference

### Document Types

| Code | Name (he) | Name (en) |
|------|-----------|-----------|
| 10 | הצעת מחיר | Price Quote |
| 100 | הזמנה | Order |
| 200 | תעודת משלוח | Delivery Note |
| 210 | תעודת החזרה | Return Note |
| 300 | חשבון עסקה | Transaction Invoice |
| 305 | חשבונית מס | Tax Invoice |
| 320 | חשבונית מס / קבלה | Tax Invoice-Receipt |
| 330 | חשבונית זיכוי | Credit Note |
| 400 | קבלה | Receipt |
| 405 | קבלה על תרומה | Donation Receipt |
| 500 | הזמנת רכש | Purchase Order |
| 600 | קבלת פיקדון | Deposit Receipt |
| 610 | משיכת פיקדון | Deposit Withdrawal |

### Document Statuses

| Code | Meaning |
|------|---------|
| 0 | Open |
| 1 | Closed |
| 2 | Manually Closed |
| 3 | Canceling Other Document |
| 4 | Canceled |

### Payment Types

| Code | Name (he) | Name (en) |
|------|-----------|-----------|
| -1 | לא שולם | Unpaid |
| 0 | ניכוי במקור | Withholding Tax |
| 1 | מזומן | Cash |
| 2 | המחאה | Check |
| 3 | כרטיס אשראי | Credit Card |
| 4 | העברה בנקאית | Bank Transfer |
| 5 | פייפאל | PayPal |
| 10 | אפליקציית תשלום | Payment App |
| 11 | אחר | Other |

### Payment Sub-Types

| Code | Name |
|------|------|
| 1 | Bitcoin |
| 2 | Money Equivalent |
| 3 | V-Check |

### Payment App Types

| Code | Name |
|------|------|
| 1 | Bit |
| 2 | Pepper Pay |
| 3 | PayBox |

### Credit Card Types

| Code | Name |
|------|------|
| 0 | Unknown |
| 1 | Isracard |
| 2 | Visa |
| 3 | Mastercard |
| 4 | American Express |
| 5 | Diners |

### Credit Card Deal Types

| Code | Name (he) | Name (en) |
|------|-----------|-----------|
| 1 | רגיל | Regular |
| 2 | תשלומים | Installments |
| 3 | קרדיט | Credit |
| 4 | חיוב נדחה | Deferred |
| 5 | אחר | Other |

### Payment Plugin Types

| Code | Name |
|------|------|
| 12010 | PayPal |
| 12050 | Payoneer |
| 12100 | Cardcom |
| 12120 | Max (Leumi Card) |
| 12130 | Meshulam |

### VAT Types (Document Level)

| Code | Meaning |
|------|---------|
| 0 | Default (based on business type) |
| 1 | Exempt |
| 2 | Mixed |

### VAT Types (Income Row)

| Code | Meaning |
|------|---------|
| 0 | Default |
| 1 | VAT Included |
| 2 | Exempt |

### Business Types

| Code | Name (he) | Name (en) |
|------|-----------|-----------|
| 1 | עוסק מורשה | Licensed Dealer |
| 2 | חברה בע"מ | Ltd. Company |
| 3 | עוסק פטור | Exempt Dealer |
| 4 | עמותה | Non-Profit |
| 5 | חברה לתועלת הציבור | Public Benefit Company |
| 6 | שותפות | Partnership |

### Payment Terms

| Code | Meaning |
|------|---------|
| -1 | Immediate |
| 0 | End of Month |
| 10 | End of Month + 10 |
| 15 | End of Month + 15 |
| 30 | End of Month + 30 |
| 45 | End of Month + 45 |
| 60 | End of Month + 60 |
| 75 | End of Month + 75 |
| 90 | End of Month + 90 |
| 120 | End of Month + 120 |

### Supported Currencies

ILS, USD, EUR, GBP, JPY, CHF, CNY, AUD, CAD, RUB, BRL, HKD, SGD, THB, MXN, TRY, NZD, SEK, NOK, DKK, KRW, INR, IDR, PLN, RON, ZAR, HRK

### Business Categories

| Code | Category |
|------|----------|
| 0 | Other |
| 1 | Internet and Computers |
| 2 | Accounting |
| 3 | Engineering |
| 4 | Marketing |
| 5 | Leisure and Sports |
| 6 | Health and Mind |
| 7 | Agriculture |
| 8 | Art |
| 9 | Education |
| 10 | Communication and Journalism |
| 11 | Religion |
| 12 | Law |
| 13 | Architecture and Design |
| 14 | Finance |
| 15 | Television and Stage |
| 16 | Coaching and Consulting |
| 17 | Hosting and Catering |
| 18 | Delivery |
| 19 | Real Estate |
| 21 | Administration and Logistics |

---

## Webhook Payload

Full webhook payload structure on document creation:

```json
{
  "id": "uuid",
  "type": 300,
  "number": 98765,
  "businessId": "uuid",
  "businessType": 1,
  "currency": "ILS",
  "country": "IL",
  "date": "2026-03-05",
  "createdAt": 1748284806000,
  "subtotal": 1000,
  "taxableTotal": 0,
  "vatTaxableTotal": 0,
  "revenueTaxableTotal": 1000,
  "exemptTotal": 0,
  "rounding": false,
  "bill": {
    "url": "https://pages.greeninvoice.co.il/en/payments/bills/..."
  },
  "tax": [],
  "total": 1170,
  "description": "",
  "remarks": "",
  "reverseCharge": false,
  "recipient": {
    "id": "uuid",
    "name": "Client Name",
    "department": "",
    "address": "",
    "city": "",
    "zip": "",
    "country": "IL",
    "phone": "",
    "mobile": "",
    "emails": ["client@example.com"]
  },
  "items": [
    {
      "description": "Service",
      "sku": "SKU-001",
      "quantity": 1,
      "price": 1000,
      "currency": "ILS",
      "taxIncludedInPrice": false
    }
  ],
  "transactions": [],
  "files": {
    "signed": true,
    "downloadLinks": {
      "he": "https://www.greeninvoice.co.il/api/v1/documents/download?d=...",
      "en": "https://www.greeninvoice.co.il/api/v1/documents/download?d=...",
      "origin": "https://www.greeninvoice.co.il/api/v1/documents/download?d=..."
    }
  }
}
```

## SDKs and Libraries

| Language | Package | Install |
|----------|---------|---------|
| Python | green-invoice | `pip install green-invoice` |
| PHP | mordisacks/greeninvoice | `composer require mordisacks/greeninvoice` |
| PHP | bariew/greeninvoice | `composer require bariew/greeninvoice` |

## Official Documentation

- API Docs (Hebrew): https://www.greeninvoice.co.il/api-docs/
- Apiary Reference: https://greeninvoice.docs.apiary.io/
- In-app API: https://app.greeninvoice.co.il/api
