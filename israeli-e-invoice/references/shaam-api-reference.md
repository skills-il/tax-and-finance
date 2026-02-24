# SHAAM API Reference (Israeli Tax Authority)

## Authentication
- **Method:** OAuth2 Client Credentials
- **Token endpoint:** `POST https://tax.gov.il/oauth/token`
- **Required:** `client_id`, `client_secret` (obtained from SHAAM developer portal)
- **Token lifetime:** 60 minutes

## Endpoints

### Request Allocation Number
```
POST /api/tax/e-invoice/allocation
Content-Type: application/json
Authorization: Bearer {token}

{
  "seller_tin": "123456782",
  "buyer_tin": "987654328",
  "invoice_type": 300,
  "invoice_date": "2026-01-15",
  "total_amount": 17550,
  "net_amount": 15000,
  "vat_amount": 2550,
  "currency": "ILS"
}

Response:
{
  "allocation_number": "SHAAM-2026-123456",
  "valid_until": "2026-02-15T00:00:00Z",
  "status": "approved"
}
```

### Validate Invoice Structure
```
POST /api/tax/e-invoice/validate
Content-Type: application/json
Authorization: Bearer {token}

{invoice_object}

Response:
{
  "valid": true,
  "errors": [],
  "warnings": ["Consider adding buyer email for digital delivery"]
}
```

### Check Allocation Status
```
GET /api/tax/e-invoice/status/{allocation_number}
Authorization: Bearer {token}

Response:
{
  "allocation_number": "SHAAM-2026-123456",
  "status": "used",
  "invoice_number": "INV-2026-0001",
  "used_date": "2026-01-15"
}
```

## Error Codes
| Code | Meaning |
|------|---------|
| 400 | Invalid request structure |
| 401 | Authentication failed |
| 403 | Not authorized for this TIN |
| 409 | Allocation already used |
| 422 | Validation errors in invoice data |
| 429 | Rate limited (max 100 requests/minute) |
| 500 | SHAAM server error |

## Developer Portal
- Registration: https://www.misim.gov.il/developers
- Sandbox environment available for testing
- Documentation primarily in Hebrew
