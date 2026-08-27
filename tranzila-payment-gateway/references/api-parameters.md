# Tranzila API Parameter Reference

## Endpoints

### Legacy CGI Endpoints
| Endpoint | URL | Use Case |
|----------|-----|----------|
| `tranzila31.cgi` | `https://secure5.tranzila.com/cgi-bin/tranzila31.cgi` | Standard charge (ILS, USD) |
| `tranzila36a.cgi` | `https://secure5.tranzila.com/cgi-bin/tranzila36a.cgi` | Multi-currency (EUR, GBP, etc.) |
| `tranzila31tk.cgi` | `https://secure5.tranzila.com/cgi-bin/tranzila31tk.cgi` | Token-based charges |

All legacy endpoints accept `POST` with `Content-Type: application/x-www-form-urlencoded`.

### Iframe Endpoint
```
https://direct.tranzila.com/{supplier}/iframenew.php?sum=100&currency=1&cred_type=1
```
- Mode is selected with `tranmode`: `A` standard charge (the documented standard mode), `V` verification (J5), `N` verification (J2), `J` standing-order initiation, `K` create a token without charging, and the token variants `AK` / `VK` / `NK`.
- There is no `J4` mode, and the iframe does not silently create a token: ask for one with `K`, `AK` or `VK`.

### API V2 Authentication
Base URL is `https://api.tranzila.com`; core payment endpoints are under `/v1` and "API V2" refers to the auth generation, though some newer endpoints (e.g. standing-order create) use a `/v2` path. Authentication is a 4-header HMAC-SHA256 handshake; ALL four headers are required:
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
| `currency` | Yes | Currency code: `1`=ILS, `2`=USD, `978`=EUR, `826`=GBP (EUR and GBP use their ISO 4217 numeric codes) |
| `cred_type` | Yes | Credit type (see table below) |


**These parameter names are the iframe and legacy-CGI ones.** API V2 uses different field names and types for the same concepts: `txn_currency_code` takes ISO alpha codes (ILS, USD, EUR, GBP and others) rather than the numeric `currency`; the installment plan is `payment_plan` plus `installments_number`, `first_installment_amount` and `other_installments_amount` rather than `cred_type` plus `npay` / `fpay` / `spay`; the expiry is `expire_month` and `expire_year` as integers rather than `expdate` as MMYY; and the cardholder ID is `card_holder_id` rather than `myid`. Decide which surface you are integrating against before copying a parameter name across.

### Credit Types (cred_type)
| Value | Type | Notes |
|-------|------|-------|
| `1` | Credit card, regular single charge | The default payment type |
| `6` | Credit (kredit) | The card company's own credit plan |
| `8` | Installments (tashlumim) | Requires `npay`, `fpay`, `spay` |

The vendor's iframe parameter table publishes exactly these three values. `2`, `3`, `5` and `9` were listed in earlier versions of this file and are not documented anywhere; sending one returns code 017 (unauthorized credit type for this transaction).

### Installment Parameters (when cred_type=8)
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
| `A` | Standard | The standard charge, as published in the vendor's iframe parameter table |
| `V` | Verify (J5) | Authorize only, no charge |
| `N` | Verify (J2) | The second verification mode |
| `J` | Standing-order initiation | Starts a standing order |
| `K` | Token only | Create a token without checking the card |
| `AK` / `VK` / `NK` | Mode + token | Add `K` to the mode to also create a token |
| `C{index}` | Cancel/Refund | Refund the transaction at `index`. Documented against `https://secure5.tranzila.com/cgi-bin/tranzila71u.cgi`, and it also needs `CreditPass` and `authnr` |

Earlier versions of this table carried an `F` (Force/Capture) mode and an empty-string default. Neither is published by the vendor: the documented standard mode is `A`.

### Token Parameters
| Parameter | Description |
|-----------|-------------|
| `TranzilaTK` | Token string. Treat it as opaque: the vendor publishes no fixed length or format, and API V2 tokens differ in shape from legacy CGI ones |
| `expdate` | Required even for token charges |

### Callback / Notification
| Parameter | Description |
|-----------|-------------|
| `notify_url_address` | Iframe: the Notify page that receives the transaction data as actually performed. The Bit API uses the bare `notify_url` instead |
| `success_url_address` / `fail_url_address` | Iframe: where the buyer is redirected after success or failure |
| `ConfirmationCode` | Returned on success -- use for refunds and captures |

## Response Fields

| Field | Description |
|-------|-------------|
| `Response` | Status code (`000` = approved, see `error-codes.md`) |
| `ConfirmationCode` | Authorization number from the card network |
| `index` | Transaction index in the current batch |
| `TranzilaTK` | Token (returned when tokenization is requested) |
| `card_mask` / `last_4` (API V2) or `DBFcard` / `cardtype` (legacy CGI) | Masked card data. `ccno` is a REQUEST parameter, not a response field |
| `expdate` | Card expiry as sent |
