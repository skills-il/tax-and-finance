# Cardcom Israeli Tax Document Types

## DocTypeToCreate Codes

| Code | Hebrew | English | VAT Included | Typical Use |
|------|--------|---------|-------------|-------------|
| 1 | hashbonit mas | Tax Invoice | Yes (17%) | B2B sales, services rendered |
| 2 | hashbonit zikui | Credit Note | Yes (reversal) | Refunds, corrections, cancellations |
| 3 | kabala | Receipt | No | Payment confirmation only |
| 101 | hashbonit mas / kabala | Tax Invoice + Receipt | Yes (17%) | B2C with payment (most common) |
| 400 | -- | Iframe Document | Varies | Generated within Low Profile iframe |

## When to Use Each Type (Israeli Tax Law)

- **Type 1 (Tax Invoice):** Required when providing goods/services to a business. Buyer needs it to claim input VAT deduction. Issue at time of supply or payment, whichever is earlier.
- **Type 2 (Credit Note):** Required when reversing a previous tax invoice -- refunds, price reductions, returned goods. Must reference the original invoice.
- **Type 3 (Receipt):** Confirms payment was received. Does NOT replace a tax invoice. Use for donations, deposits, or when tax invoice was already issued separately.
- **Type 101 (Tax Invoice + Receipt):** Combined document for when payment and supply happen simultaneously. Standard for most B2C retail and e-commerce transactions.
- **Type 400 (Iframe):** Used internally by Cardcom's Low Profile flow. Not typically set manually.

## InvoiceHead Parameters (Document Object)

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `DocTypeToCreate` | int | Yes | 1, 2, 3, 101, or 400 |
| `Name` | string | Yes | Customer name (appears on document) |
| `VAT_Number` | string | For type 1 | 9-digit Israeli TIN (mispar osek) |
| `Email` | string | No | Customer email for delivery |
| `SendByEmail` | bool | No | `true` to auto-email the PDF |
| `Language` | string | No | `he` (default), `en`, `ar` |
| `CoinID` | int | No | 1=ILS (default), 2=USD, 3=EUR |
| `Comments` | string | No | Free text, printed on document |
| `City` | string | No | Customer city |
| `Address` | string | No | Customer street address |
| `Phone` | string | No | Customer phone |
| `IsVatFree` | bool | No | `true` for VAT-exempt transactions |
| `ManualInvoiceNumber` | int | No | Override auto-numbering (rare) |
| `ReferenceInvoice` | int | For type 2 | Original invoice number being credited |

## InvoiceLines Parameters (Products Array)

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `Description` | string | Yes | Line item description |
| `UnitCost` | decimal | Yes | Price per unit (VAT inclusive by default) |
| `Quantity` | decimal | Yes | Number of units |
| `IsVatFree` | bool | No | `true` for VAT-exempt line items |
| `ProductId` | string | No | Your internal SKU/product ID |
| `IsTaxable` | bool | No | Default `true`, set `false` for non-taxable |

## VAT Handling

- Default: amounts are **VAT inclusive** -- Cardcom extracts the 17% VAT automatically
- For VAT-exempt items: set `IsVatFree: true` on the product line
- For fully VAT-free documents: set `IsVatFree: true` on the InvoiceHead
- Mixed invoices: some lines taxable, some exempt -- set per line item
- **Osek Patur** (exempt dealer): should issue type 3 (receipt) only, not tax invoices

## SendByEmail Options

| Value | Behavior |
|-------|----------|
| `true` | Cardcom emails the PDF document to the `Email` address |
| `false` (default) | Document created but not emailed; retrieve via `Link` in response |

The emailed document includes a PDF attachment and a link to view online.

## Required Fields by Document Type

| Field | Type 1 | Type 2 | Type 3 | Type 101 |
|-------|--------|--------|--------|----------|
| `Name` | Yes | Yes | Yes | Yes |
| `VAT_Number` | Recommended | Recommended | No | No |
| `Products[]` | Yes | Yes | No | Yes |
| `ReferenceInvoice` | No | Yes | No | No |
| `Email` | Optional | Optional | Optional | Optional |

## Example: Tax Invoice + Receipt (Type 101)

```json
{
  "Document": {
    "DocTypeToCreate": 101,
    "Name": "Israel Israeli",
    "Email": "customer@example.com",
    "SendByEmail": true,
    "Language": "he",
    "CoinID": 1,
    "Products": [
      {
        "Description": "Annual software license",
        "UnitCost": 1170.00,
        "Quantity": 1,
        "IsVatFree": false
      },
      {
        "Description": "Setup fee",
        "UnitCost": 234.00,
        "Quantity": 1,
        "IsVatFree": false
      }
    ]
  }
}
```

VAT breakdown: total 1404 NIS inclusive = 1200 NIS net + 204 NIS VAT (17%).
