# Israeli E-Invoice Skill — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a skill that teaches Claude to generate, validate, and manage Israeli e-invoices per Tax Authority (SHAAM) standards, including allocation number requests.

**Architecture:** Domain Intelligence skill with Workflow Automation pattern. Embeds Israeli e-invoicing regulations, SHAAM API structure, and document templates. Uses scripts for validation and references for regulatory details.

**Tech Stack:** SKILL.md, Python validation scripts, SHAAM API OAuth2 reference docs.

---

## Research

### Israeli E-Invoice Mandate
- **Law:** Amendment 157 to the VAT Law (2024)
- **Timeline:** Progressive threshold reduction:
  - May 2024: Transactions over 25,000 NIS
  - January 2025: Over 20,000 NIS
  - July 2025: Over 10,000 NIS
  - January 2026: Over 5,000 NIS
  - **June 2026: ALL invoices** (target date per research, verify current status)
- **Allocation Number:** Every tax invoice above threshold must request a unique allocation number from SHAAM before being issued to the customer

### SHAAM API (Israeli Tax Authority)
- **Base URL:** `https:// tax.gov.il` (production) / sandbox available
- **Auth:** OAuth2 with client credentials
- **Key Endpoints:**
  - `POST /api/tax/e-invoice/allocation` — Request allocation number
  - `POST /api/tax/e-invoice/validate` — Validate invoice structure
  - `GET /api/tax/e-invoice/status/{id}` — Check allocation status
- **Required Fields:** Seller TIN (osek morsheh/patur), buyer TIN, invoice type, amounts, VAT breakdown
- **Invoice Types:**
  - 300: Tax Invoice (Hashbonit Mas)
  - 305: Tax Invoice / Receipt (Hashbonit Mas / Kabala)
  - 310: Credit Invoice (Hashbonit Zikui)
  - 320: Receipt (Kabala)
  - 330: Proforma Invoice
  - 400: Tax Invoice for self-billing

### Existing Resources
- No existing MCP server for SHAAM
- Community `israeli-bank-mcp` handles bank data but not tax
- SHAAM developer portal: Documentation in Hebrew, registration required

### Use Cases
1. **Generate e-invoice** — User provides transaction details, skill creates compliant invoice with correct fields
2. **Request allocation number** — Skill guides through SHAAM API allocation request flow
3. **Validate existing invoice** — Check if an invoice meets current SHAAM requirements
4. **Explain compliance** — Answer questions about e-invoice mandate, thresholds, deadlines
5. **Bulk invoice preparation** — Help prepare multiple invoices for batch submission

---

## Design

### Skill Category
Workflow Automation + Domain-Specific Intelligence (Category 2 + Pattern 5)

### Pattern
Sequential Workflow Orchestration (Pattern 1) for invoice creation flow
Domain-Specific Intelligence (Pattern 5) for compliance checking

### Progressive Disclosure
- **Frontmatter:** Trigger on "e-invoice", "hashbonit", "allocation number", "SHAAM", "Israeli invoice"
- **SKILL.md body:** Step-by-step invoice creation workflow, validation rules, compliance guidance
- **references/:** Full SHAAM API endpoint reference, invoice field specifications, VAT law summary

### File Structure
```
israeli-e-invoice/
  SKILL.md
  scripts/
    validate-invoice.py        # Validate invoice structure locally
  references/
    shaam-api-reference.md     # SHAAM API endpoints and auth
    invoice-types.md           # Israeli invoice type codes and rules
    compliance-timeline.md     # Mandate thresholds and deadlines
```

### Success Criteria
- Triggers on 90%+ of relevant queries (e-invoice, Israeli invoice, allocation number, hashbonit, SHAAM)
- Does NOT trigger on general accounting or non-Israeli invoice queries
- Generates structurally valid invoice JSON in 1 workflow pass
- Correctly identifies which invoice type to use based on transaction details

---

## Build Steps

### Task 1: Create SKILL.md

**Files:**
- Create: `repos/tax-and-finance/israeli-e-invoice/SKILL.md`

**Step 1: Write SKILL.md with frontmatter and full instructions**

```markdown
---
name: israeli-e-invoice
description: >-
  Generate, validate, and manage Israeli e-invoices (hashbonit electronit)
  per Tax Authority (SHAAM) standards. Use when user asks to create Israeli
  invoices, request allocation numbers, validate invoice compliance, or asks
  about "hashbonit", "e-invoice", "SHAAM", "allocation number", or Israeli
  invoicing requirements. Supports tax invoice (300), tax invoice/receipt (305),
  credit invoice (310), receipt (320), and proforma (330) types. Do NOT use for
  general accounting, bookkeeping, or non-Israeli invoice formats.
license: MIT
compatibility: "Requires network access for SHAAM API calls. Works with Claude Code, Claude.ai, Cursor."
metadata:
  author: skills-il
  version: 1.0.0
  category: tax-and-finance
  tags: [tax, invoice, e-invoice, vat, shaam, israel]
---

# Israeli E-Invoice

## Instructions

### Step 1: Determine Invoice Type
Ask the user what type of document they need:

| Code | Hebrew | English | When to Use |
|------|--------|---------|-------------|
| 300 | hashbonit mas | Tax Invoice | B2B sales, services over threshold |
| 305 | hashbonit mas / kabala | Tax Invoice / Receipt | B2C with immediate payment |
| 310 | hashbonit zikui | Credit Invoice | Refunds, corrections, returns |
| 320 | kabala | Receipt | Payment confirmation only |
| 330 | hashbonit proforma | Proforma Invoice | Quotes, pre-billing (no allocation needed) |

### Step 2: Collect Required Fields
For all invoice types, gather:
- **Seller details:** Business name, TIN (mispar osek), address, phone
- **Buyer details:** Business name (or individual), TIN (if B2B), address
- **Transaction:** Date, item descriptions, quantities, unit prices
- **Payment:** Method (cash, transfer, check, credit card), terms

### Step 3: Calculate VAT
- Standard Israeli VAT rate: **17%** (as of 2025, verify current rate)
- VAT calculation: `vat_amount = net_amount * 0.17`
- Total: `gross_amount = net_amount + vat_amount`
- For VAT-exempt transactions (osek patur), no VAT line — use receipt (320) instead

### Step 4: Check Allocation Number Requirement
Determine if an allocation number is needed:
- **Required if:** Invoice amount >= current threshold AND invoice type is 300, 305, or 310
- **Current thresholds:**
  - Until June 2025: > 10,000 NIS
  - July 2025 - December 2025: > 5,000 NIS
  - January 2026+: Verify current threshold (mandate expanding)
- **Not required for:** Receipts (320), proforma (330), invoices below threshold

If allocation number IS required:
1. Inform user they must request from SHAAM before issuing
2. Provide the API call structure (see references/shaam-api-reference.md)
3. The allocation number must appear on the printed/sent invoice

### Step 5: Generate Invoice Document
Create the invoice with all fields formatted per Israeli standards:
- Date in both Gregorian (DD/MM/YYYY) and Hebrew calendar
- Amounts in NIS (New Israeli Shekel)
- VAT breakdown as separate line
- Sequential invoice number from seller's series
- Allocation number (if applicable)

### Step 6: Validate
Run validation checks:
1. All required fields present
2. TIN format valid (9 digits with check digit)
3. VAT calculation correct
4. Invoice number sequential
5. Date not in the future
6. Allocation number present if above threshold

If validation fails, report specific errors and how to fix them.

## Examples

### Example 1: Simple B2B Tax Invoice
User says: "Create a tax invoice for a web development project, 15,000 NIS to ABC Ltd"
Actions:
1. Identify: Tax Invoice (type 300), above threshold -> allocation needed
2. Collect: Seller and buyer details
3. Calculate: Net 15,000 + VAT 2,550 = Total 17,550 NIS
4. Guide: Request allocation number from SHAAM
5. Generate: Formatted invoice document
Result: Complete tax invoice with all required fields and allocation number guidance

### Example 2: Small B2C Receipt
User says: "I need a receipt for a 500 NIS cash payment"
Actions:
1. Identify: Receipt (type 320), below threshold -> no allocation needed
2. Collect: Seller and buyer details
3. Generate: Receipt document
Result: Simple receipt, no allocation number required

### Example 3: Credit Invoice for Refund
User says: "I need to issue a credit note for invoice #1234, partial refund of 3,000 NIS"
Actions:
1. Identify: Credit Invoice (type 310)
2. Reference: Original invoice #1234
3. Calculate: Credit amount with VAT reversal
4. Check: Allocation requirement based on amount
Result: Credit invoice referencing original, with correct VAT reversal

## Troubleshooting

### Error: "Invalid TIN format"
Cause: Israeli TIN (mispar osek) must be exactly 9 digits with valid check digit
Solution: Verify the number with the check digit algorithm. Consult references/tin-validation.md.

### Error: "Allocation number required"
Cause: Invoice amount exceeds current threshold for mandatory allocation
Solution: Request allocation number from SHAAM API before issuing invoice. See Step 4.

### Error: "VAT rate mismatch"
Cause: Using incorrect VAT rate (rate changes periodically)
Solution: Verify current rate at the Tax Authority website. Standard rate is 17% as of 2025.

### Error: "Invoice type not suitable"
Cause: Wrong invoice type selected for the transaction
Solution: Review the invoice type table in Step 1. Common mistake: using type 300 when 305 (with receipt) is needed for immediate payment.
```

**Step 2: Validate SKILL.md**

Run: `./repos/tax-and-finance/scripts/validate-skill.sh repos/tax-and-finance/israeli-e-invoice/SKILL.md`
Expected: PASS

**Step 3: Commit**

```bash
git add repos/tax-and-finance/israeli-e-invoice/SKILL.md
git commit -m "feat(tax): add israeli-e-invoice skill with SHAAM compliance workflow"
```

### Task 2: Create Reference Files

**Files:**
- Create: `repos/tax-and-finance/israeli-e-invoice/references/shaam-api-reference.md`
- Create: `repos/tax-and-finance/israeli-e-invoice/references/invoice-types.md`
- Create: `repos/tax-and-finance/israeli-e-invoice/references/compliance-timeline.md`

**Step 1: Create SHAAM API reference**
Document all known SHAAM API endpoints, OAuth2 flow, request/response schemas.

**Step 2: Create invoice types reference**
Full table of all Israeli invoice type codes (300-400 series) with field requirements per type.

**Step 3: Create compliance timeline**
Detailed timeline of e-invoice mandate thresholds with dates and legal references.

**Step 4: Commit**

```bash
git add repos/tax-and-finance/israeli-e-invoice/references/
git commit -m "docs(tax): add SHAAM API and compliance reference docs for e-invoice skill"
```

### Task 3: Create Validation Script

**Files:**
- Create: `repos/tax-and-finance/israeli-e-invoice/scripts/validate-invoice.py`

**Step 1: Write validation script**

```python
#!/usr/bin/env python3
"""Validate Israeli e-invoice structure and fields."""

import sys
import json
import re
from datetime import datetime

def validate_tin(tin: str) -> bool:
    """Validate Israeli TIN (mispar osek) - 9 digits with check digit."""
    if not re.match(r'^\d{9}$', tin):
        return False
    digits = [int(d) for d in tin]
    weights = [1, 2, 1, 2, 1, 2, 1, 2, 1]
    total = 0
    for d, w in zip(digits, weights):
        product = d * w
        total += product // 10 + product % 10
    return total % 10 == 0

def validate_invoice(invoice: dict) -> list:
    """Validate invoice structure. Returns list of errors."""
    errors = []
    required = ['seller_tin', 'invoice_type', 'date', 'total_amount']
    for field in required:
        if field not in invoice:
            errors.append(f"Missing required field: {field}")
    if 'seller_tin' in invoice and not validate_tin(invoice['seller_tin']):
        errors.append("Invalid seller TIN format")
    if 'buyer_tin' in invoice and invoice['buyer_tin'] and not validate_tin(invoice['buyer_tin']):
        errors.append("Invalid buyer TIN format")
    valid_types = [300, 305, 310, 320, 330, 400]
    if 'invoice_type' in invoice and invoice['invoice_type'] not in valid_types:
        errors.append(f"Invalid invoice type: {invoice['invoice_type']}")
    return errors

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: validate-invoice.py <invoice.json>")
        sys.exit(1)
    with open(sys.argv[1]) as f:
        invoice = json.load(f)
    errors = validate_invoice(invoice)
    if errors:
        print("VALIDATION FAILED:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    print("VALIDATION PASSED")
```

**Step 2: Test script**
Run: `echo '{"seller_tin":"123456782","invoice_type":300,"date":"2026-01-15","total_amount":15000}' | python3 repos/tax-and-finance/israeli-e-invoice/scripts/validate-invoice.py /dev/stdin`
Expected: VALIDATION PASSED

**Step 3: Commit**

```bash
git add repos/tax-and-finance/israeli-e-invoice/scripts/
git commit -m "feat(tax): add invoice validation script for e-invoice skill"
```

### Task 4: Test Triggering

**Test queries that SHOULD trigger:**
1. "Help me create an Israeli e-invoice"
2. "I need to generate a hashbonit mas"
3. "How do I get an allocation number from SHAAM?"
4. "Create a tax invoice for 15,000 NIS"
5. "What are the Israeli e-invoice requirements?"
6. "Help me with Israeli invoicing"
7. "Generate an Israeli credit invoice"
8. "What's the current e-invoice threshold?"
9. "I need a hashbonit electronit"
10. "Validate my Israeli invoice"

**Test queries that should NOT trigger:**
1. "Create a US invoice"
2. "Help me with general accounting"
3. "What's my bank balance?"
4. "Calculate my taxes"
5. "Help me with QuickBooks"

### Task 5: Update Category README

**Files:**
- Modify: `repos/tax-and-finance/README.md`

Add the skill to the skills table with accurate description, trust level, and supported agents.
