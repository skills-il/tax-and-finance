# Israeli Invoice Type Codes

## Standard Types

| Code | Hebrew | English | VAT | Allocation |
|------|--------|---------|-----|------------|
| 300 | hashbonit mas | Tax Invoice | Yes (17%) | Required above threshold |
| 305 | hashbonit mas / kabala | Tax Invoice + Receipt | Yes (17%) | Required above threshold |
| 310 | hashbonit zikui | Credit Invoice | Yes (reversal) | Required above threshold |
| 320 | kabala | Receipt | No | Not required |
| 330 | hashbonit proforma | Proforma Invoice | No | Not required |
| 400 | hashbonit mas atzmi | Self-billing Tax Invoice | Yes (17%) | Required above threshold |

## Required Fields by Type

### Type 300/305 (Tax Invoice / Tax Invoice + Receipt)
- Seller: Name, TIN, address
- Buyer: Name, TIN (if business), address
- Invoice number (sequential)
- Date
- Item descriptions, quantities, unit prices
- VAT amount (separate line)
- Total amount
- Allocation number (if above threshold)
- Payment method (for 305 only)

### Type 310 (Credit Invoice)
- All fields from original invoice
- Reference to original invoice number
- Reason for credit
- Credit amount with VAT reversal

### Type 320 (Receipt)
- Seller: Name, TIN
- Buyer: Name
- Date and amount
- Payment method

### Type 330 (Proforma)
- Not a legal tax document
- No allocation number needed
- Used for quotes and pre-billing
