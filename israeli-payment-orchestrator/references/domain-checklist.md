# Domain Checklist: israeli-payment-orchestrator

Scope: design a multi-gateway payment abstraction for Israeli merchants (routing, fallback, installments, compliance). Category: tax-and-finance (payments/architecture).

## Must cover (core)
- The 6 gateways with CORRECT API styles (Cardcom JSON, Tranzila form-POST, PayMe bearer JSON, Meshulam/Grow multipart/form-data, iCredit, Pelecard) and a hedged fee/feature matrix.
- Unified PaymentRequest/Result abstraction; idempotency keys.
- Gateway routing (feature-match, cost, availability/failover) and the never-retry-a-bank-decline rule.
- Installments with CORRECT Shva CreditType codes: regular installments (תשלומים)=8, credit (קרדיט)=6, club installments (מועדון)=9, club credit=4; CreditType is distinct from transaction type (סוג עסקה). Max ~36 (some gateways 12/24).
- Regulatory compliance: ISA regulates non-bank PSPs (Regulation of Payment Services Law 2023); BOI supervises banks/credit-card cos and oversees Shva; 7-year data retention; PCI DSS tokenization; 3DS2 for CNP.

## Should cover (advanced)
- Settlement timelines, refund (Bit refund uses a different endpoint), circuit-breaker/health checks, volume balancing.

## Out of scope (explicit)
- Single-gateway setup (cardcom-payment-gateway / tranzila-payment-gateway / grow-payment-gateway).

## Authoritative sources
- Shva (שב"א) credit-type enum; gateway docs (Cardcom, Tranzila, PayMe, grow-il.readme.io, iCredit, Pelecard).
- boi.org.il payment-systems-oversight; Regulation of Payment Services and Payment Initiation Law 5783-2023 (ISA).
