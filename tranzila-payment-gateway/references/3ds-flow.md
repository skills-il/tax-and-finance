# 3D Secure V2 Implementation for Tranzila

## Overview

3D Secure V2 (3DS2) adds a cardholder authentication step between your server and the card issuer. It shifts fraud liability from the merchant to the issuer for authenticated transactions. Tranzila implements 3DS2 via a **redirect flow** -- the customer is redirected to their bank's authentication page, then returned to your site.

## Flow Diagram

```
1. Customer submits payment on your site
2. Your server sends transaction to Tranzila with 3DS parameters
3. Tranzila returns a redirect URL (if 3DS is required)
4. Customer is redirected to bank authentication page
5. Customer completes authentication (password, OTP, biometric)
6. Bank redirects customer back to your notify_url
7. Tranzila POSTs final result to your server
8. Your server checks Response and 3DS authentication status
```

## Enabling 3DS

Add these parameters to your standard transaction request:

| Parameter | Value | Description |
|-----------|-------|-------------|
| `TranzilaTK` or `ccno` | Card details | Standard card/token parameters |
| `notify_url` | Your callback URL | Where Tranzila sends the final result (must be HTTPS) |

3DS enrollment is typically configured at the terminal level by Tranzila. Contact Tranzila support (073-222-4444) to enable 3DS on your terminal. Once enabled, eligible transactions are automatically routed through the 3DS flow.

For iframe integrations, 3DS is handled within the iframe -- no additional server-side parameters are needed.

## Response Fields for 3DS

After the authentication flow completes, Tranzila includes these additional fields:

| Field | Description |
|-------|-------------|
| `Response` | `000` = approved, `900` = 3DS authentication failed |
| `eci` | Electronic Commerce Indicator -- authentication level |
| `xid` | Transaction identifier from the 3DS flow |
| `cavv` | Cardholder Authentication Verification Value |
| `three_ds_status` | Authentication result (see table below) |

### Authentication Status Values

| Status | Meaning | Liability Shift |
|--------|---------|-----------------|
| `Y` | Fully authenticated | Yes -- issuer bears liability |
| `A` | Authentication attempted | Yes -- issuer bears liability |
| `N` | Authentication failed | No -- merchant bears liability |
| `U` | Authentication unavailable | No -- merchant bears liability |
| `R` | Authentication rejected | No -- do not proceed with transaction |

### ECI Values

| ECI | Card Network | Meaning |
|-----|-------------|---------|
| `01` | Mastercard | 3DS authenticated |
| `02` | Mastercard | 3DS attempted |
| `05` | Visa | 3DS authenticated |
| `06` | Visa | 3DS attempted |
| `07` | Visa / Mastercard | No 3DS / not enrolled |

## Fallback Handling

Not all transactions will go through 3DS. Handle these cases:

**Card/issuer does not support 3DS:**
- Tranzila processes the transaction as a regular (non-3DS) charge
- `eci` will be `07` (Visa) or empty
- Liability remains with the merchant
- No action needed -- the transaction completes normally

**Customer abandons authentication:**
- No callback is received at `notify_url`
- Implement a timeout (recommended: 15 minutes) on your side
- Display a "payment not completed" message and allow retry

**3DS system unavailable:**
- Tranzila falls back to non-3DS processing
- Transaction may still succeed with `Response=000` but without liability shift
- Log the `eci` value to track which transactions were authenticated

**Response code 900:**
- Authentication explicitly failed
- Do not retry automatically with 3DS
- Offer the customer the option to retry or use a different card

## Israeli Issuer Notes

- **Isracard, Visa Cal, Leumi Card/Max** all support 3DS V2 for Visa and Mastercard branded cards
- **American Express** cards issued in Israel have limited 3DS support -- most Amex transactions fall back to non-3DS
- **Diners Club** cards generally do not support 3DS in Israel
- Israeli issuers commonly use SMS OTP for authentication (rather than app-based or biometric)
- Some Israeli business cards (kartis ishi) may be exempt from 3DS requirements based on terminal configuration
- Test 3DS in Tranzila's sandbox environment before going live -- sandbox simulates both successful and failed authentication flows
