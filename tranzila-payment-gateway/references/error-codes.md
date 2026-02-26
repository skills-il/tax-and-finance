# Tranzila Response Codes

A `Response` value of `000` means the transaction was approved. Any other value indicates an error or decline.

## Common Response Codes

| Code | Meaning | Category | Action |
|------|---------|----------|--------|
| `000` | Approved | Success | Transaction completed successfully |
| `001` | Confiscate card | Decline | Do not retry. Ask customer to contact their bank. |
| `002` | Confiscate card (special) | Decline | Do not retry. Ask customer to contact their bank. |
| `004` | Card declined (kartis surav) | Decline | Ask customer to try another card or contact bank. |
| `006` | Forged card / CVV error | Fraud | Do not retry. Verify card details or use a different card. |
| `033` | Card expired (kartis pagum tokef) | Decline | Ask customer to update their card details. |
| `036` | Restricted card | Decline | Card is blocked. Customer must contact their issuer. |
| `039` | No such account | Decline | Invalid card number. Verify and re-enter. |
| `051` | Insufficient funds (ein yitra) | Decline | Ask customer to use a different card or add funds. |
| `055` | Wrong PIN | Decline | Ask customer to re-enter PIN. Limit retries to prevent lockout. |
| `058` | Transaction not permitted | Decline | Card not authorized for this transaction type. Try a different card. |

## Amount and Authorization Errors

| Code | Meaning | Category | Action |
|------|---------|----------|--------|
| `107` | Amount exceeds limit (chriga memichsa) | Limit | Reduce the amount or ask customer to contact their bank. |
| `111` | Not authorized for installments | Config | Contact Tranzila (073-222-4444) to enable installments on your terminal. |
| `125` | Not authorized for Amex | Config | Contact Tranzila to enable American Express processing. |
| `126` | Invalid club code | Config | Verify `cred_type` and club parameters. Contact Tranzila if persistent. |

## Application and System Errors

| Code | Meaning | Category | Action |
|------|---------|----------|--------|
| `200` | Application error (shegihat mimshal) | System | Check all required parameters are present and correctly named. Retry once. |

## Masav (Direct Debit) Errors

| Code | Meaning | Category | Action |
|------|---------|----------|--------|
| `700` | Masav transaction failed | Masav | Verify bank account details and Masav authorization. |
| `701` | Masav file rejected | Masav | Check file format. Contact Tranzila support for Masav configuration. |

## 3D Secure and Fraud Errors

| Code | Meaning | Category | Action |
|------|---------|----------|--------|
| `900` | 3DS authentication failed (imut 3DS nichal) | 3DS | Retry without 3DS or prompt the customer to complete authentication. |
| `903` | Suspected fraud | Fraud | Do not retry. Flag for manual review. |

## Protocol and Payment Errors

| Code | Meaning | Category | Action |
|------|---------|----------|--------|
| `951` | Protocol error | System | Verify request format and endpoint. Check Tranzila status page. |
| `952` | Payment network timeout | Network | Retry after a short delay (5-10 seconds). |
| `953` | Payment network unavailable | Network | Retry later. If persistent, check Shva network status. |
| `954` | Communication error | Network | Verify network connectivity. Retry after a short delay. |

## Handling Guidelines

1. **Always check `Response`** before processing. Never assume success.
2. **Log the full response** including `Response`, `ConfirmationCode`, and `index` for troubleshooting.
3. **Do not retry** fraud-related declines (`001`, `002`, `006`, `903`).
4. **Safe to retry** network errors (`952`, `953`, `954`) after a brief delay.
5. **Config errors** (`111`, `125`, `126`) require terminal changes -- contact Tranzila support.
6. **Display user-friendly messages** -- never show raw error codes to end users.

## Quick Lookup by Category

| Category | Codes |
|----------|-------|
| Success | `000` |
| Card decline | `001`, `002`, `004`, `033`, `036`, `039`, `051`, `055`, `058` |
| Fraud | `006`, `903` |
| Limits / Authorization | `107`, `111`, `125`, `126` |
| System / Application | `200`, `951` |
| Network | `952`, `953`, `954` |
| Masav | `700`, `701` |
| 3D Secure | `900` |
