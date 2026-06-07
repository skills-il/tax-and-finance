# Israeli Payment Gateway Comparison Matrix

## API Integration Details

### Cardcom
- **Base URL:** `https://secure.cardcom.solutions/api/`
- **Auth:** API name + API password (per terminal)
- **Format:** REST JSON
- **Tokenization:** Yes (card token for recurring)
- **3D Secure:** Supported (3DS2)
- **Webhook:** POST callback on transaction completion
- **Sandbox:** Available with test credentials
- **Documentation:** https://kb.cardcom.co.il/

### Tranzila
- **Base URL:** `https://secure5.tranzila.com/`
- **Auth:** Terminal name + password
- **Format:** REST JSON (new) / Form POST (legacy)
- **Tokenization:** Yes (TranzilaTK)
- **3D Secure:** Supported (3DS2)
- **Webhook:** IPN (Instant Payment Notification)
- **Sandbox:** Available with test terminal
- **Documentation:** https://docs.tranzila.com/

### PayMe
- **Base URL:** `https://ng.paymeservice.com/api/`
- **Auth:** Seller API key (bearer token)
- **Format:** REST JSON
- **Tokenization:** Yes (buyer key)
- **3D Secure:** Supported (3DS2)
- **Webhook:** POST callback
- **Sandbox:** Available
- **Documentation:** https://www.payme.io/developers

### Meshulam (Grow)
- **Base URL:** `https://secure.meshulam.co.il/api/light/server/1.0/` (production); `https://sandbox.meshulam.co.il/api/light/server/1.0/` (sandbox)
- **Auth:** userId + page code (apiKey for multi-business)
- **Format:** multipart/form-data (NOT JSON), server-side only
- **Tokenization:** Yes
- **3D Secure:** Supported
- **Webhook:** POST callback
- **Sandbox:** Available
- **Documentation:** https://grow-il.readme.io/reference/overview

### iCredit
- **Base URL:** `https://icredit.rivhit.co.il/api/`
- **Auth:** Group private Token + credentials
- **Format:** REST JSON
- **Tokenization:** Yes
- **3D Secure:** Supported
- **Webhook:** POST callback
- **Sandbox:** Available
- **Documentation:** https://icredit.rivhit.co.il/

### Pelecard
- **Base URL:** `https://gateway20.pelecard.biz/`
- **Auth:** Terminal number + user + password
- **Format:** REST JSON
- **Tokenization:** Yes
- **3D Secure:** Supported (3DS2)
- **Webhook:** POST callback
- **Sandbox:** Available
- **Documentation:** https://www.pelecard.com/support/

## Installment (Tashlumim) Support

| Gateway | Regular | Credit | Club | Max Installments | Min Amount |
|---------|---------|--------|------|-----------------|------------|
| Cardcom | Yes | Yes | Yes | 36 | Per issuer |
| Tranzila | Yes | Yes | No | 24 | Per issuer |
| PayMe | Yes | Yes | No | 36 | Per issuer |
| Meshulam | Yes | No | No | 12 | Per issuer |
| iCredit | Yes | Yes | No | 24 | Per issuer |
| Pelecard | Yes | Yes | Yes | 36 | Per issuer |

## Settlement Timing

| Gateway | Standard Settlement | Express Option | Currency |
|---------|-------------------|----------------|----------|
| Cardcom | T+2 business days | Available (fee) | NIS |
| Tranzila | T+2 business days | Available (fee) | NIS |
| PayMe | T+2 business days | T+1 (fee) | NIS |
| Meshulam | T+3 business days | N/A | NIS |
| iCredit | T+2 business days | Available (fee) | NIS |
| Pelecard | T+2 business days | Available (fee) | NIS |

## Shva CreditType (סוג אשראי) Reference

These are Shva CreditType values, a field distinct from the transaction type (סוג עסקה) and from gateway-level refund operations.

| CreditType | Type | Hebrew | Description |
|------|------|--------|-------------|
| 1 | Regular / immediate | רגיל | Single immediate payment |
| 2 | Isracredit / 30+ | ישראקרדיט / 30+ | Issuer special-credit product |
| 3 | Immediate debit | חיוב מיידי | Debit cleared immediately |
| 4 | Club credit | קרדיט מועדון | Issuer club credit program |
| 5 | Leumi special | מיוחד לאומי | Leumi Card special |
| 6 | Credit installments | קרדיט | Bank-financed installments (interest to bank) |
| 8 | Regular installments | תשלומים | Merchant-financed installments |
| 9 | Club installments | תשלומי מועדון | Issuer club installment program |

Refunds are a gateway-level operation (often signalled separately, e.g. operation codes 51 full / 52 installment refund), not a CreditType value.
