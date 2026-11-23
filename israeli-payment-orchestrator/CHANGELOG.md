# Changelog

## 1.3.2 (2026-11-23)

Grow retry correction only. This skill no longer gives its own retry or verification steps for Grow and routes them to `grow-payment-gateway`. A Grow charge whose outcome is unknown is never retried automatically, and the order is not fulfilled until that skill's confirmation step is complete. No other gateway changed.
