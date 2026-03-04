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

### Meshulam
- **Base URL:** `https://sandbox.meshulam.co.il/api/` (sandbox)
- **Auth:** API key + page code
- **Format:** REST JSON
- **Tokenization:** Yes
- **3D Secure:** Supported
- **Webhook:** POST callback
- **Sandbox:** Available
- **Documentation:** https://www.meshulam.co.il/developers

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

## Shva Network Codes Reference

| Code | Type | Hebrew | Description |
|------|------|--------|-------------|
| 1 | Regular charge | חיוב רגיל | Single payment |
| 2 | Credit installments | קרדיט | Bank-financed installments |
| 3 | Club installments | מועדון | Issuer club program |
| 8 | Regular installments | תשלומים | Merchant-financed installments |
| 51 | Refund | זיכוי | Full or partial refund |
| 52 | Refund installments | זיכוי תשלומים | Refund in installments |
