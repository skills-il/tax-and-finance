# Tranzila API Parameter Reference

## Endpoints

### Legacy CGI Endpoints
| Endpoint | URL | Use Case |
|----------|-----|----------|
| `tranzila31.cgi` | `https://secure5.tranzila.com/cgi-bin/tranzila31.cgi` | Standard charge (ILS, USD) |
| `tranzila36a.cgi` | `https://secure5.tranzila.com/cgi-bin/tranzila36a.cgi` | Multi-currency (EUR, GBP, etc.) |
| `tranzila31tk.cgi` | `https://secure5.tranzila.com/cgi-bin/tranzila31tk.cgi` | Token-based charges |
| `tranzila31pan.cgi` | `https://secure5.tranzila.com/cgi-bin/tranzila31pan.cgi` | PAN-based operations |

All legacy endpoints accept `POST` with `Content-Type: application/x-www-form-urlencoded`.

### Iframe Endpoint
```
https://direct.tranzila.com/{supplier}/iframenew.php?sum=100&currency=1&cred_type=1
```
- **J5 mode** (default): Creates a token -- card is not charged. Use token via `tranzila31tk.cgi` to charge later.
- **J4 mode**: One-time charge -- card is charged immediately, no token returned.

### API V2 Authentication
Base URL is `https://api.tranzila.com/v1` ("API V2" is the auth-generation name, not a `/v2` path). Authentication is a 4-header HMAC-SHA256 handshake; ALL four headers are required:
```
POST https://api.tranzila.com/v1/{resource}
X-tranzila-api-app-key: {public app key}
X-tranzila-api-request-time: {unix time in seconds}
X-tranzila-api-nonce: {~40-byte random nonce}
X-tranzila-api-access-token: {hmac_sha256(secret + request_time + nonce, app_key)}
Content-Type: application/json
```
You enrol in API V2 to get a public app key and a secret key; the access-token is the HMAC-SHA256 of the app key, keyed with the secret concatenated with the request-time and nonce. A request with only `X-tranzila-api-app-key` is rejected. These headers replace `supplier` + `TranzilaPW`. Confirm the exact concatenation order on the Authentication page at docs.tranzila.com before shipping.

## Common Parameters

### Authentication
| Parameter | Required | Description |
|-----------|----------|-------------|
| `supplier` | Yes (CGI) | Terminal name assigned by Tranzila |
| `TranzilaPW` | Yes (CGI) | Transaction password for the terminal |

### Transaction Details
| Parameter | Required | Description |
|-----------|----------|-------------|
| `sum` | Yes | Amount in currency units (e.g., `100` = 100 ILS) |
| `ccno` | Yes* | Full card number (not needed for token charges) |
| `expdate` | Yes | Expiry as `MMYY` (e.g., `0328` for March 2028) |
| `expmonth` | Alt | Expiry month `MM` (alternative to `expdate`) |
| `expyear` | Alt | Expiry year `YY` (use with `expmonth`) |
| `mycvv` | Recommended | 3-4 digit CVV/CVC |
| `myid` | Conditional | 9-digit Israeli ID (teudat zehut), required by some terminals |
| `currency` | Yes | Currency code: `1`=ILS, `2`=USD, `3`=GBP, `7`=EUR |
| `cred_type` | Yes | Credit type (see table below) |

### Credit Types (cred_type)
| Value | Type | Notes |
|-------|------|-------|
| `1` | Regular credit (ashrai ragil) | Default single charge |
| `2` | Visa Adif / Amex Credit | Special credit terms |
| `3` | Immediate debit (hiyuv miyadi) | Deducted same day |
| `5` | Leumi Special | Leumi Card specific |
| `8` | Installments (tashlumim) | Requires `npay`, `fpay`, `spay` |
| `9` | Club installments (tashlumei moadan) | Club-card specific installments |

### Installment Parameters (when cred_type=8 or 9)
| Parameter | Description |
|-----------|-------------|
| `npay` | Number of additional payments after the first (total payments = npay + 1) |
| `fpay` | First payment amount |
| `spay` | Subsequent payment amount |

Rule: `fpay + (npay * spay)` must equal `sum`.

Example -- 3 payments of 100 NIS each (total 300):
```
sum=300&cred_type=8&npay=2&fpay=100&spay=100
```

### Transaction Mode (tranmode)
| Value | Mode | Description |
|-------|------|-------------|
| *(empty)* | Charge | Default -- standard charge |
| `V` | Verify | Authorize only, no charge. Use `ConfirmationCode` to capture later. |
| `F` | Force/Capture | Capture a previously verified (V) transaction |
| `C{index}` | Cancel/Refund | Refund transaction at `index` in batch (e.g., `C0` = first) |
| `K` | Token only | Create token without charging |
| `VK` | Verify + Token | Authorize and create token |
| `AK` | Charge + Token | Charge and create token |

### Token Parameters
| Parameter | Description |
|-----------|-------------|
| `TranzilaTK` | Token string (19 chars, last 4 match card) |
| `expdate` | Required even for token charges |

### Callback / Notification
| Parameter | Description |
|-----------|-------------|
| `notify_url` | URL where Tranzila POSTs the transaction result |
| `ConfirmationCode` | Returned on success -- use for refunds and captures |

## Response Fields

| Field | Description |
|-------|-------------|
| `Response` | Status code (`000` = approved, see `error-codes.md`) |
| `ConfirmationCode` | Authorization number from the card network |
| `index` | Transaction index in the current batch |
| `TranzilaTK` | Token (returned when tokenization is requested) |
| `ccno` | Masked card number (last 4 digits) |
| `expdate` | Card expiry as sent |
