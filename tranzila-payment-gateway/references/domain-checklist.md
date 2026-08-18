# Domain coverage checklist, tranzila-payment-gateway

Anchor for expert review. Scope: integrating Tranzila payments (iframe, hosted fields, API V2, tokens, installments, refunds, 3DS, Bit) into Israeli apps.

## Must cover (core)
- Integration patterns + PCI scope (Iframe SAQ-A, Hosted Fields SAQ-A-EP, API V2 SAQ-D).
- Auth: legacy supplier+TranzilaPW; API V2 = 4-header HMAC-SHA256 (app-key + request-time + nonce + access-token) at api.tranzila.com/v1.
- Endpoints: direct.tranzila.com/{supplier}/iframenew.php; secure5.tranzila.com CGIs (tranzila31/36a/31tk).
- Israeli payment types: installments (cred_type=8, npay/fpay/spay, fpay+npay*spay=sum), credit types, currency codes, tokenization (TranzilaTK, tranmode K/VK/AK), refund (tranmode=C{index}).
- Error handling: HTTP 200 on failure, read Response field; two code spaces (SHVA + 3DS 900-930); verify codes against official docs.
- Bit dedicated API + constraints (NIS, >5 NIS, Visa/Isracard, Max-only not supported).
- Webhook signature verification (don't trust inbound shape).
- ITA allocation number for B2B invoices (20K/10K/5K schedule).

## Out of scope (explicit)
- Cardcom (use cardcom-payment-gateway), general accounting.

## Authoritative sources
- Tranzila docs: https://docs.tranzila.com/
- Tranzila site: https://www.tranzila.com
- tranzilajs: https://github.com/NirTatcher/tranzilajs
