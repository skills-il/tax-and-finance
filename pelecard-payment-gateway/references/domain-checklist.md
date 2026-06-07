# Domain Checklist: pelecard-payment-gateway

Scope: integrate the Pelecard (unofficial/community-documented) payment gateway. Category: tax-and-finance (payments/dev).

## Must cover (core)
- Hosts: production gateway21.pelecard.biz, legacy/sandbox gateway20.pelecard.biz/sandbox; credentials triple (terminal/user/password) server-side only.
- Iframe create-session (PaymentGW/init) returning URL + ConfirmationKey; money in agorot; Currency 1 = ILS.
- ActionType J4 (sale) / J2 (validation only, no charge) / J5 (auth-later) / J5h - and the "wrong ActionType silently changes whether money moves" warning.
- Server-side callback validation: match the callback ConfirmationKey to the stored Phase-1 value AND re-verify via PaymentGW/GetTransaction (confirm DebitTotal + PelecardTransactionId). No HMAC on IPNs - the server-to-server lookup is the only authoritative source. Dedupe on PelecardTransactionId.
- Tokenization / recurring (CreateToken, IsToken, MIT/3DS exemption), refunds, 3DS2, Apple Pay (ClientSecure.js), Bit (single payment, ILS, ~5,000 NIS operator-set cap).
- Israeli Consumer Protection Law distance-selling refunds (14-day cancel, 14-day refund, fee cap 5% or 100 NIS).

## Should cover (advanced)
- Reconciliation safety net (poll GetTransaction for sessions with no IPN); DebitApproveNumber join to the Shva clearing report; the modern Match API (verify with vendor); pairing with green-invoice for the tax document.

## Out of scope (explicit)
- Cardcom / Tranzila / Grow-Meshulam single gateways; multi-gateway orchestration; invoice generation.

## Authoritative sources
- github.com/dofinity/pelecard (PHP wrapper: PaymentGW/init, ValidateByUniqueKey, agorot, Currency 1); wordpress.org/plugins/woo-pelecard-gateway (gateway21, refunds, tokenization, Apple Pay); postman.com/peleteam/pelecard-public (Gateway21 collection); allpay.co.il (Bit); Consumer Protection Law 14C-14E.
