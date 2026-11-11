# Grow Webhook and Callback Payloads

Field names below come from the examples on Grow's Webhooks page (developers.grow.business/docs/overview-7) and its Server-to-Server Callback pages. Values are placeholders.

## Setup

Webhooks are enabled per account by Grow support (`support@grow.business`). A sandbox configuration is not copied to production.

## Webhook options

1. All one-time transactions (all single payments across all pages and sources)
2. All static payment pages (legacy system)
3. Specific static payment pages (legacy system)
4. Specific payment links (new system)
5. WordPress plugin transactions
6. Recurring payments (from the second charge)
7. Failed recurring payments
8. POS devices
9. Invoice creation
10. Grow mobile application transactions

## Flat `webhookKey` family (API one-time, recurring, legacy pages)

```json
{
  "webhookKey": "ABC1234",
  "transactionCode": "ABCD1234",
  "transactionType": "אשראי",
  "paymentSum": 2.00,
  "paymentsNum": 1,
  "allPaymentNum": 2,
  "firstPaymentSum": 1,
  "periodicalPaymentSum": 1,
  "paymentType": "רגיל",
  "paymentDate": "14/10/21",
  "asmachta": "123456789",
  "paymentDesc": "Description",
  "fullName": "Full Name",
  "payerPhone": "0500000000",
  "payerEmail": "test@test.com",
  "cardSuffix": "1234",
  "cardBrand": "Mastercard",
  "cardType": "Local",
  "paymentSource": "מערכת חיצונית"
}
```

Recurring payloads add `directDebitId` (the standing-order id, not a transaction id). Legacy static-page payloads add `purchasePageKey`, `purchasePageTitle`, `amount` and `purchaseCustomField`. This family has no `statusCode`, `transactionId` or `transactionToken`, so it cannot be fed to `getTransactionInfo` or `approveTransaction`.

## Failed recurring payment

```json
{
  "regular_payment_id": "55545",
  "payer_name": "Full Name",
  "phone": "0500000000",
  "email": "test@test.com",
  "transaction_type": "הוראת קבע",
  "card_suffix": "4580",
  "sum": "1",
  "description": "תיאור עסקה",
  "business_title": "שם העסק",
  "error_message": "פג תוקף",
  "charges_attempts": "6",
  "webhook_key": "123456ABCD"
}
```

`regular_payment_id` is the standing-order id, not a transaction id.

## Invoice webhook (VAT invoice/receipt and automatically generated invoices)

```json
{
  "transactionCode": "ABCD1234",
  "invoiceNumber": "20",
  "invoiceUrl": "https://secure.meshulam.co.il"
}
```

## Payment links (new system)

Same envelope as the server-to-server callback:

```json
{
  "err": "",
  "status": "1",
  "data": {
    "statusCode": "2",
    "status": "שולם",
    "sum": "13",
    "transactionId": "1234567",
    "transactionToken": "818bf8333e7a3f0c53ef8e7",
    "paymentLinkProcessId": "1234567",
    "paymentLinkProcessToken": "7ab1c9133444a8507ebf24ff2",
    "asmachta": "12345",
    "invoice_license_number": "123456789",
    "invoice_name": "שם לחשבונית",
    "productData": [
      {"product_id": "0", "name": "...", "catalog_number": "", "vat": "1", "quantity": "1", "price": "1", "price_mark": "0"}
    ],
    "shipping": {"type": "...", "amount": "10"},
    "dynamicFields": [{"key": "", "label": "...", "option_label": "", "option_key": "", "field_value": "..."}]
  }
}
```

## Server-to-server callback (`notifyUrl`)

Sent as a form POST ("NOT as JSON"), shown here as JSON. Fields sit under `data`:

```json
{
  "err": "",
  "status": "1",
  "data": {
    "statusCode": "2",
    "status": "שולם",
    "sum": "269",
    "transactionId": "145111110",
    "transactionToken": "c68d98D4c3f19b30hgy7362e9g5g5g5862",
    "processId": "332002",
    "processToken": "f01644c3f19b30h825eg5g5g5g3b0",
    "asmachta": "0289199",
    "cardSuffix": "1177",
    "cardExp": "0126",
    "customFields": {"cField1": "3ba543214f1"}
  }
}
```

When the payment saved a card (`saveCardToken=1`), `data.cardToken` carries the reusable card token; `transactionToken` is NOT the card token. The save-token-only example arrives with `statusCode` `11` (suspended). Recurring callbacks add `directDebitId` and `recurringDebitId`.
