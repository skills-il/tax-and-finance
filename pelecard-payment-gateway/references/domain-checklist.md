# Domain Checklist: pelecard-payment-gateway

Scope: integrate the Pelecard (unofficial/community-documented) payment gateway. Category: tax-and-finance (payments/dev).

## Must cover (core)
- Hosts: gateway21.pelecard.biz (current generation) and gateway20.pelecard.biz (older generation) serve the SAME API; the hostname is not an environment switch. Environment is decided by the terminal + credentials. Credentials triple server-side only.
- The two parameter surfaces: /PaymentGW/* (terminal, Total, Currency, ParamX, TransactionId) vs /services/* (terminalNumber, total, currency, paramX). Mixing them is the most common silent failure.
- Void vs refund (ביטול vs זיכוי): DeleteTran / DeleteIshur / EmvReversal before the Shva broadcast; a credit transaction after it. There is NO refund endpoint under /PaymentGW.
- The Shva broadcast (שידור) cycle: /services/Broadcast, GetBroadcast, GetTransDataBeforeBc. An approval number is not settled money.
- J5 capture via authorizationNumber on the debit; J9 pending via Pending*Type + ClearPendingBy*.
- Token lifecycle beyond creation: ConvertToToken, RetrieveToken, UpdateToken, CheckCreditCardForToken.
- 3DS2 as an ordered sequence: Initiate3DSAuthenticationProcess -> eci/xid/cavv carried into the debit.
- Status codes are fully public via the credential-free /services/GetErrorMessageEn and GetErrorMessageHe.
- Outbound idempotency (unique paramX/userKey per attempt; look up before re-charging), not only inbound IPN dedupe.
- PCI scope: token vs PAN on /services; ClientSecure.js on the merchant page. Never log ConfirmationKey or CardHolderID.
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
