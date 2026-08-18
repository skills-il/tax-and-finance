# Payment Terms under Chok Moser Tashlumim leSapakim 5777-2017

**Full law text:** https://www.nevo.co.il/law_html/law00/144599.htm
**Plain-language summary (Kol-Zchut):** https://www.kolzchut.org.il/he/המועד_האחרון_לתשלום_תמורה_לספקים_עבור_סחורה_או_שירות

This is the Late Payment to Suppliers Law (often called by its Hebrew shorthand "חוק מוסר תשלומים"). It sets binding caps on how long a payer can delay paying a supplier. Contractual clauses that try to exceed these caps are void by statute.

## The three payer tiers

### Tier 1: State authority (section 3(a))

| Limit | Reference |
|---|---|
| 45 days from invoice submission | Section 3(a) |

The cap is calendar days from when the supplier delivered the invoice (חשבון) to the procuring entity. There is no month-end bend.

### Tier 2: Local authority (section 3(f))

| Service type | Limit |
|---|---|
| Standard goods/services | 45 days from month-end of invoice submission |
| Construction work (בנייה) | 80 days from month-end |

Note local authorities use a month-end-anchored ("shotef") count, not invoice-date.

### Tier 3: Business to business (section 3(g))

| Limit | Common shorthand |
|---|---|
| 45 days from month-end of invoice submission | "shotef + 45" |

This is the cap that applies to most freelancer-to-client contracts. An invoice dated 5 March, under shotef + 45, is due by 14 May (45 days after 31 March). About 70 days post-invoice in the worst case.

## What "shotef + N" actually means

Shotef literally means "current" or "running". The convention:

```
due_date = end_of_month(invoice_date) + N_days
```

| Invoice date | Term | Due date | Days post-invoice |
|---|---|---|---|
| 1 March | shotef + 30 | 30 April | 60 |
| 5 March | shotef + 30 | 30 April | 56 |
| 30 March | shotef + 30 | 30 April | 31 |
| 5 March | shotef + 45 | 15 May | 71 |
| 5 March | shotef + 60 | 30 May | 86 |

**This is NOT the same as American "Net 30"**, which means 30 days from invoice date. Many Israeli freelancers fluent in English copy "Net 30" wording from foreign templates and inadvertently agree to faster-than-shotef payment terms (which is fine for them) or assume their client's shotef+30 means 30 days from invoice (which costs them ~15-30 days of float).

## Late payment interest (section 4)

If the payer delays beyond the statutory cap, statutory interest accrues per `Chok Psikat Ribit veHatzmada 5721-1961` (חוק פסיקת ריבית והצמדה, התשכ"א-1961). This is enforceable in court and runs from the day after the cap.

## Drafting the payment-terms clause

Suggested clause (Hebrew, drop into the quote):

> **תנאי תשלום:** שוטף + 30 ימים מהנפקת החשבונית, בהתאם לחוק מוסר תשלומים לספקים, התשע"ז-2017. עיכוב מעבר ל-30 יום נושא ריבית פיגורים לפי חוק פסיקת ריבית והצמדה, התשכ"א-1961.

English equivalent (for bilingual quotes):

> **Payment terms:** Net end-of-month + 30 days from invoice issuance ("shotef + 30"), per the Late Payment to Suppliers Law 5777-2017. Delays beyond the statutory cap accrue interest per the Interest and Linkage Law 5721-1961.

## Defaults this skill uses

- **Default term:** shotef + 30 (better than legal max, helps cash flow)
- **Statutory max for B2B:** shotef + 45 (warn if user picks longer)
- **Statutory max for state authority client:** 45 days from invoice (different anchor)
- **Statutory max for local authority client:** 45 days from month-end (or 80 for construction)
