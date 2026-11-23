# Changelog

## 1.4.0 (2026-11-23)

Grow retry and fulfilment correction. This skill no longer gives its own retry or verification steps for Grow and routes them to `grow-payment-gateway`: Step 5.5 for a payment page, Step 9 Option B for a token charge, and Step 5.6 after a timeout. Grow documents no way to authenticate its server update, so an update is a trigger only and never proof of payment. A Grow charge whose outcome is unknown is never retried automatically. The per-gateway void and refund table moved to `references/gateway-matrix.md`.
