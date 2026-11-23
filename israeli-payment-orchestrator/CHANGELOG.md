# Changelog

## 1.4.0 (2026-11-23)

Grow retry and fulfilment correction. This skill no longer gives its own retry or verification steps for Grow and routes them to `grow-payment-gateway`: Step 5.5 for a payment page, Step 9 Option B for a token charge, and Step 5.6 after a timeout. Grow documents no way to authenticate its server update, so an update is a trigger only and never proof of payment. Fulfilment requires a result that shows the transaction itself as paid. A lookup that finds no successful charge leaves the outcome unknown and blocked, it is never retried automatically, and only a person may clear a retry. For every gateway, only a failure before any request byte was sent justifies failover; a TLS or connection error after sending began is an unknown outcome. The per-gateway void and refund table moved to `references/gateway-matrix.md`.
