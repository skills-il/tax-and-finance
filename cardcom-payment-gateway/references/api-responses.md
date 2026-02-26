# Cardcom Response Codes

## Response Code Location

Every Cardcom API response includes a numeric code. Check the relevant field based on the operation:
- **Payments:** `DealResponse`
- **Tokens:** `TokenResponse`
- **Documents:** `InvoiceResponseCode`

A value of `0` always means success.

## Transaction Response Codes (DealResponse)

| Code | Meaning | Category | Action |
|------|---------|----------|--------|
| 0 | Success | OK | Proceed normally |
| 1 | Card declined by issuer | Card | Ask customer to try another card |
| 2 | Stolen card | Card | Do not retry, contact processor |
| 3 | Call credit company | Card | Customer should call card issuer |
| 4 | Transaction not approved | Card | Retry or use different card |
| 6 | CVV error | Card | Ask customer to re-enter CVV |
| 10 | Partial amount approved | Card | Decide: accept partial or cancel |
| 33 | Card expired | Card | Ask customer to update card |
| 36 | Card restricted | Card | Customer should contact issuer |
| 39 | Invalid card number | Card | Ask customer to re-enter number |
| 61 | Over credit limit | Card | Try smaller amount or different card |
| 65 | Over daily transaction limit | Card | Try again tomorrow or different card |
| 75 | Too many PIN attempts | Card | Customer should contact issuer |

## Token Response Codes (TokenResponse)

| Code | Meaning | Category | Action |
|------|---------|----------|--------|
| 0 | Token created/charged successfully | OK | Store token securely |
| 1 | Token creation failed | Token | Retry the payment flow |
| 2 | Token not found | Token | Verify token UUID and terminal match |
| 3 | Token expired | Token | Re-create token with new payment |
| 4 | Token blocked | Token | Contact Cardcom support |

## Invoice Response Codes (InvoiceResponseCode)

| Code | Meaning | Category | Action |
|------|---------|----------|--------|
| 0 | Document created successfully | OK | Use InvoiceNumber from response |
| 1 | Missing required fields | Doc | Check Name, Products, DocType |
| 2 | Invalid document type | Doc | Use valid DocTypeToCreate (1,2,3,101,400) |
| 3 | VAT number invalid | Doc | Verify VAT_Number format (9 digits) |
| 4 | Products array empty | Doc | Include at least one product line |
| 5 | Document cancelled | Doc | Cannot modify; create a new document |

## API/HTTP Error Codes

| Code | Meaning | Category | Action |
|------|---------|----------|--------|
| 5033 | Terminal number missing | Auth | Add `TerminalNumber` to request body |
| 5034 | Authentication failed | Auth | Verify `ApiName` and `ApiPassword` |
| 5035 | Invalid amount | Validation | Ensure `Amount` is a positive number |
| 5036 | Invalid currency | Validation | Use valid `CoinID` (1=ILS, 2=USD, 3=EUR) |
| 5037 | Missing return URL | Validation | Add `SuccessRedirectUrl` (LowProfile) |
| 5100 | Card declined (general) | Card | Ask user to try another card |
| 5101 | Card expired | Card | Ask user to update card details |
| 5102 | CVV incorrect | Card | Ask user to re-enter CVV |
| 5200 | Token not found | Token | Verify token UUID and terminal ownership |
| 5201 | Token expired or revoked | Token | Re-create token via new payment |
| 5300 | Invoice creation failed | Doc | Check Document object parameters |
| 5301 | Document type not enabled | Doc | Enable document type in Cardcom dashboard |

## Handling Pattern

```python
response = call_cardcom_api(endpoint, payload)

if response.get("DealResponse") == 0:
    # Success -- extract InternalDealNumber, Token, InvoiceNumber
    deal_id = response["InternalDealNumber"]
elif response.get("DealResponse") in [1, 4, 61, 65]:
    # Card issue -- prompt customer to retry
    show_error("Payment declined. Please try a different card.")
elif response.get("DealResponse") in [2, 36]:
    # Blocked card -- do not retry
    show_error("Card cannot be used. Contact your bank.")
else:
    # Unexpected -- log full response for debugging
    log_error(f"Cardcom error: {response}")
```

## Notes

- Always check both HTTP status (200 = request received) AND response code (0 = operation succeeded)
- A 200 HTTP status with a non-zero DealResponse means the API call was valid but the operation failed
- Log the full response body for any non-zero codes to aid debugging
