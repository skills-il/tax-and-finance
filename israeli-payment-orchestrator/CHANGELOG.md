# Changelog

## 1.3.2 (2026-11-23)

Grow retry correction only. This skill no longer gives its own retry or verification steps for Grow and routes them to `grow-payment-gateway`. A Grow charge whose outcome is unknown is never retried automatically, and the order is not fulfilled until the server-side checks in that skill's Step 5.5 (and Step 5.6 for token charges) pass. No other gateway changed.
