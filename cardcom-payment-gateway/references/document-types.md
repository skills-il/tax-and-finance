# Cardcom V11 Israeli Tax Document Types

All field names and enum values below are taken from the official Cardcom V11
OpenAPI specification at `https://secure.cardcom.solutions/Api/v11/Docs`
(the `Document`, `DocumentBase`, `DocumentToCreate`, and `Products` schemas).

## DocumentTypeToCreate (string enum)

The document type is set with the `DocumentTypeToCreate` string field on the
`Document` object. It is a STRING enum, NOT an integer code. The full
`DocumentToCreate` enum from the V11 schema:

| Value | Hebrew | English | Typical Use |
|-------|--------|---------|-------------|
| `Auto` | --- | Auto | Default; uses your admin-panel configuration |
| `TaxInvoiceAndReceipt` | hashbonit mas / kabala | Tax Invoice + Receipt | B2C with payment (most common) |
| `TaxInvoiceAndReceiptRefund` | --- | Tax Invoice + Receipt Refund | Reversing a `TaxInvoiceAndReceipt` |
| `Receipt` | kabala | Receipt | Payment confirmation only |
| `ReceiptRefund` | --- | Receipt Refund | Reversing a `Receipt` |
| `Quote` | hatzaat mehir | Quote | Price quote, no financial effect |
| `Order` | hazmana | Order | Customer order document |
| `OrderConfirmation` | ishur hazmana | Order Confirmation | Confirms an order |
| `OrderConfirmationRefund` | --- | Order Confirmation Refund | Reverses an order confirmation |
| `DeliveryNote` | teudat mishloach | Delivery Note | Goods delivery |
| `DeliveryNoteRefund` | --- | Delivery Note Refund | Reverses a delivery note |
| `ProformaInvoice` | hashbonit iska / proforma | Proforma Invoice | Pre-sale document |
| `ProformaInvoiceRefund` | --- | Proforma Invoice Refund | Reverses a proforma invoice |
| `DemandForPayment` | drishat tashlum | Demand for Payment | Payment demand |
| `DemandForPaymentRefund` | --- | Demand for Payment Refund | Reverses a demand for payment |
| `ProformaDealInvoice` | --- | Proforma Deal Invoice | Proforma tied to a deal |
| `ProformaDealInvoiceRefund` | --- | Proforma Deal Invoice Refund | Reverses a proforma deal invoice |
| `TaxInvoice` | hashbonit mas | Tax Invoice | B2B, when the receipt is issued separately |
| `TaxInvoiceRefund` | --- | Tax Invoice Refund | Reverses a `TaxInvoice` |
| `ReceiptForTaxInvoice` | kabala al heshbon hashbonit mas | Receipt for Tax Invoice | Receipt against a prior tax invoice |
| `ReceiptForTaxInvoiceRefund` | --- | Receipt for Tax Invoice Refund | Reverses a receipt-for-tax-invoice |
| `DonationReceipt` | kabalat trumot | Donation Receipt | Registered non-profits |
| `DonationReceiptRefund` | --- | Donation Receipt Refund | Reverses a donation receipt |
| `CouponDocumentAndReceipt` | --- | Coupon Document and Receipt | Coupon sale plus receipt |
| `CouponDocumentAndReceiptRefund` | --- | Coupon Document and Receipt Refund | Reverses a coupon document and receipt |

If you need a value not listed, verify it against the official docs rather than
guessing.

## When to Use Each Type (Israeli Tax Law)

- **`TaxInvoice`:** Required when supplying goods/services to a business. The
  buyer needs it to claim an input-VAT deduction. Issue at the time of supply or
  payment, whichever is earlier.
- **`Receipt`:** Confirms payment was received. Does NOT replace a tax invoice.
- **`TaxInvoiceAndReceipt`:** Combined document for when payment and supply
  happen simultaneously. Standard for most B2C retail and e-commerce.
- **`*Refund` types:** Required when reversing a previous document (refunds,
  price reductions, returned goods).
- **Osek Patur** (exempt dealer): issues a `Receipt` only, not tax invoices.

## Document Object Fields (DocumentBase + Document)

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `DocumentTypeToCreate` | string enum | Yes | One of the values above; default `Auto` |
| `Name` | string | Yes | The "document To" / customer name, 1-50 chars |
| `TaxId` | string | For B2B | Business registration number or ID number (replaces the older `VAT_Number`) |
| `Email` | string | No | Email to send the document to, max 50 chars |
| `IsSendByEmail` | bool | No | `true` to auto-email the PDF (default `true`) |
| `AddressLine1` / `AddressLine2` | string | No | Customer address |
| `City` | string | No | Customer city |
| `Mobile` / `Phone` | string | No | Customer phone numbers |
| `Comments` | string | No | Free text printed on the document, max 250 chars |
| `IsVatFree` | bool | No | `true` if every line in the document is VAT-free |
| `ISOCoinID` | int | No | `1` = ILS (default), `2` = USD, the rest per ISO |
| `ISOCoinName` | string | No | Alternative to `ISOCoinID` |
| `Languge` | string | No | Document language, `he` (default) or `en`. Lives on the `Document` and `DocumentTran` schemas (the standalone `CreateDocument` and `Transaction` flows), NOT on `DocumentBase` itself. Note the V11 misspelling: `Languge`, missing the second `a` |
| `DepartmentId` | int | No | Department id from the admin panel, for reports |
| `ExternalId` | string | No | Your custom id stored on the document |
| `Products` | array | Yes (for financial docs) | See the Products fields below |

In the `LowProfile/Create` flow the document object is a `DocumentLP`; in the
`Transaction` flow it is a `DocumentTran` (which uses `DocumentDateDDMMYYYY` and
`Languge`). Both extend the same `DocumentBase` shown above. One quirk: the
`DocumentLP` sub-schema uses the correctly-spelled `Language`, while `DocumentTran`
uses the misspelled `Languge`; for the LowProfile page as a whole, set the
top-level `Language` field on the `LowProfile/Create` request (see
api-endpoints.md).

## Products Array Fields

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `Description` | string | Yes | Line item description, 1-250 chars |
| `UnitCost` | decimal | Yes | Cost of one unit |
| `Quantity` | decimal | No | Quantity, default `1` |
| `TotalLineCost` | decimal | No | Send when `Quantity` has decimals, to prevent rounding errors |
| `IsVatFree` | bool | No | `true` for a VAT-free line, for mixed-VAT documents |
| `ProductID` | string | No | Your internal SKU / product id |
| `IsGiftCard` | bool | No | `true` creates a non-financial gift-card document type |

## VAT Handling

- The current Israeli VAT rate is 18% (effective January 2025).
- Set `IsVatFree: true` on a single product line for a VAT-exempt line item.
- Set `IsVatFree: true` on the `Document` object for a fully VAT-free document.
- Mixed documents: set `IsVatFree` per line item.
- **Osek Patur** (exempt dealer): should issue `Receipt` documents only.

## Example: Tax Invoice + Receipt

```json
{
  "ApiName": "your-api-name",
  "ApiPassword": "your-api-password",
  "Document": {
    "DocumentTypeToCreate": "TaxInvoiceAndReceipt",
    "Name": "Israel Israeli",
    "Email": "customer@example.com",
    "IsSendByEmail": true,
    "Languge": "he",
    "ISOCoinID": 1,
    "Products": [
      { "Description": "Annual software license", "UnitCost": 1180.00, "Quantity": 1 },
      { "Description": "Setup fee", "UnitCost": 236.00, "Quantity": 1 }
    ]
  }
}
```

Cardcom computes the VAT server-side from the line totals.
