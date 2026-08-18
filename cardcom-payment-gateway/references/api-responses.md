# Cardcom V11 Response Pattern

## ResponseCode + Description

Every Cardcom V11 API response is a JSON object that carries two top-level fields:

- **`ResponseCode`** (integer) -- `0` means success. Any non-zero value is a
  developer or transaction error.
- **`Description`** (string) -- a human-readable explanation of the `ResponseCode`.

There is no `DealResponse`, `TokenResponse`, or `InvoiceResponseCode` field in V11.
Those belong to the legacy `.aspx` interfaces. In V11, always check `ResponseCode`
and read `Description` for the reason.

For `Transactions/Transaction`, J2/J5 validation-only operations return
`ResponseCode` `700` or `701`, which also count as success.

## Per-operation response objects

| Endpoint | Response object | Success fields to read |
|----------|-----------------|------------------------|
| `LowProfile/Create` | `CreateLowProfileResponse` | `LowProfileId`, `Url`, `UrlToBit`, `UrlToPayPal` |
| `LowProfile/GetLpResult` | `LowProfileResult` | `TranzactionId`, `ReturnValue`, `TranzactionInfo`, `TokenInfo`, `DocumentInfo`, `SuspendedInfo` |
| `Transactions/Transaction` | `TransactionInfo` | `TranzactionId`, `Token`, `ApprovalNumber`, `DocumentNumber`, `DocumentUrl` |
| `Transactions/RefundByTransactionId` | `RefundByTransactionIdResp` | `NewTranzactionId` |
| `Documents/CreateDocument` | `DocumentInfo` | `DocumentType`, `DocumentNumber`, `AccountId`, `DocumentUrl` |

In `LowProfileResult`, the nested objects (`TranzactionInfo`, `TokenInfo`,
`DocumentInfo`, `SuspendedInfo`) are `null` when not applicable to the operation
that ran. For example, `TokenInfo` is populated only for `ChargeAndCreateToken`
and `CreateTokenOnly` operations.

## Error codes

Cardcom V11 uses a single numeric `ResponseCode` space. The full numeric
error reference (developer errors, card-decline reasons, document errors) is
maintained in the official Cardcom documentation; do not hardcode a
code-to-message table. Instead, branch on `ResponseCode == 0` for success and
surface the `Description` string for everything else.

See the official Cardcom error reference at
`https://secure.cardcom.solutions/Api/v11/Docs` and the support center at
`https://support.cardcom.solutions`.

## Handling Pattern

```python
import requests

resp = requests.post(
    "https://secure.cardcom.solutions/api/v11/Transactions/Transaction",
    json=payload,
    timeout=30,
).json()

if resp.get("ResponseCode") == 0:
    # Success: extract TranzactionId, Token, DocumentNumber, DocumentUrl
    transaction_id = resp["TranzactionId"]
else:
    # Failure: Description carries the exact reason
    log_error(
        f"Cardcom error {resp.get('ResponseCode')}: {resp.get('Description')}"
    )
    show_error("Payment could not be completed. Please try again.")
```

## Notes

- Always check both the HTTP status (`200` = request received) AND `ResponseCode`
  (`0` = operation succeeded). A `200` with a non-zero `ResponseCode` means the
  request was valid but the operation failed.
- Log the full response body, including `Description`, for any non-zero
  `ResponseCode` to aid debugging.
- For `LowProfileResult`, also inspect the nested object `ResponseCode` values
  (for example `DocumentInfo.ResponseCode`) when a document was requested.
