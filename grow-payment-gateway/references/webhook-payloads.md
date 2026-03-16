# Grow Webhook Payload Reference

## Setup

Contact `apisupport@grow.business` to enable webhooks for your account.

## Trigger Options

1. All one-time transactions across all pages
2. Specific static payment pages
3. Specific payment links
4. WordPress plugin transactions
5. Recurring payments (from 2nd charge onward)
6. Failed recurring payments
7. POS device transactions
8. Invoice creation
9. Mobile app transactions

## Standard Payment Webhook

```json
{
  "webhookKey": "unique-webhook-id",
  "transactionCode": "txn-reference",
  "paymentSum": "149.90",
  "paymentDate": "2026-03-17 14:30:00",
  "fullName": "Israel Israeli",
  "payerPhone": "0501234567",
  "payerEmail": "customer@example.com",
  "cardSuffix": "1234",
  "cardBrand": "Visa",
  "cardType": "Credit",
  "paymentSource": "page",
  "asmachta": "0012345",
  "paymentDesc": "Monthly subscription"
}
```

## Recurring Payment Webhook (2nd charge+)

Additional fields beyond standard:

```json
{
  "directDebitId": "recurring-series-id",
  "paymentsNum": "3",
  "periodicalPaymentSum": "99.00"
}
```

## Failed Recurring Payment Webhook

```json
{
  "error_message": "Card declined",
  "charges_attempts": "2",
  "regular_payment_id": "recurring-payment-id"
}
```

## Invoice Webhook (via invoiceNotifyUrl)

```json
{
  "transactionCode": "txn-reference",
  "invoiceNumber": "INV-2026-001",
  "invoiceUrl": "https://grow.business/invoice/..."
}
```

## Payment Link Webhook (New System)

Extended format with product and shipping data:

```json
{
  "processToken": "process-token",
  "transactionCode": "txn-reference",
  "paymentSum": "299.00",
  "productData": [
    {
      "catalogNumber": "SKU-001",
      "quantity": 2,
      "price": 149.50,
      "itemDescription": "Widget Pro"
    }
  ],
  "shipping": {},
  "dynamicFields": {}
}
```
