# Payment Terms under Chok Moser Tashlumim leSapakim 5777-2017

**Full law text:** https://www.nevo.co.il/law_html/law00/144599.htm
**Plain-language summary (Kol-Zchut):** https://www.kolzchut.org.il/he/המועד_האחרון_לתשלום_תמורה_לספקים_עבור_סחורה_או_שירות

This is the Late Payment to Suppliers Law (often called by its Hebrew shorthand "חוק מוסר תשלומים"). It fixes the payment date that governs when the contract is silent, and constrains what the parties may agree instead.

**It does not simply void every longer term.** For a business payer (section 3(g)) and for a budgeted body or university (section 3(e)) the statutory date applies "אלא אם כן קבעו הצדדים באופן מפורש בחוזה מועד אחר לתשלום", and another date is permitted where it is required by the special character of the engagement or is not "בלתי הוגן באופן חריג" (exceptionally unfair). A 3(e) payer additionally needs CEO approval, must disclose the other date in the tender, and must report the engagement to the Small and Medium Business Agency. For state authorities (3(a) and 3(b)) and local authorities (3(f)) the statute does not offer the same express opt-out.

## The payer tiers

Which row applies is decided by the definitions in section 2, not by how large the client feels. "עסק" means a financial institution, an oseik morshe or an oseik patur, and expressly EXCLUDES a corporation at least half-owned by a local authority, a water corporation, Mifal HaPayis and the sports-betting council. "רשות מדינה" is a closed list: the President's office, the Knesset, the State Comptroller, Bank of Israel, the Israel Securities Authority and Bituach Leumi.

### Tier 1: State authority, government ministry, Mifal HaPayis, sports-betting council (section 3(a))

| Limit | Reference |
|---|---|
| 45 days from delivery of the invoice, where the contract counts from delivery | Section 3(a)(1) |
| 30 days from month-end, where the contract counts from month-end | Section 3(a)(2) |

Which of the two applies depends on the counting basis written into the contract, so read the contract before assuming the 45-day figure.

### Tier 1b: The same bodies, construction-engineering works (section 3(b))

| Limit | Reference |
|---|---|
| 85 days from delivery of the invoice, or 70 days from month-end | Section 3(b) |

Section 3(c) preserves shorter dates already set in the Accountant General's תכ"מ rules as they stood on 1 January 2017, and section 3(d) lets the ministers put named categories of contractors back on the 3(a) track.

### Tier 1c: Budgeted bodies, budgeted higher-education institutions, other bodies established by law (section 3(e))

| Limit | Reference |
|---|---|
| 45 days from month-end, unless another date is expressly agreed with the payer's CEO approval | Section 3(e)(1) |

This is the row a freelancer quoting a university, a government company or another statutory body actually sits on. It is neither the state row nor the B2B row.

### Tier 2: Local authority (section 3(f))

| Service type | Limit |
|---|---|
| Standard goods/services | 45 days from month-end of invoice submission |
| Construction work (בנייה) | 80 days from month-end |
| Portion financed by external funding | Deferrable to 10 business days after the funding arrives, but payable no later than 150 days from delivery of the invoice, even if the funding never arrived |

Note local authorities use a month-end-anchored ("shotef") count, not invoice-date. The external-financing deferral only applies if the authority gave the supplier written notice of the financing share and of the deferral option no later than at engagement (or at tender publication).

### Tier 3: Business to business (section 3(g))

| Limit | Common shorthand |
|---|---|
| 45 days from month-end of invoice submission | "shotef + 45" |

This is the date that applies to most freelancer-to-client contracts when the contract is silent. An invoice dated 5 March, under shotef + 45, is due by 15 May (45 days after 31 March). That is 71 days post-invoice.

## An incomplete invoice is treated as never delivered (section 3(h))

If the invoice omits a material particular required by the contract, or the contractual conditions for payment were not met, the payer returns it with the defects listed and it is as if it had never been delivered. The examination period within which the payer must do this is 23 business days from delivery (60 days for construction works under 3(b) or 3(f)). If the payer returns the invoice AFTER the examination period, payment is due within 10 business days of the original due date. The days between return and re-submission of a corrected invoice do not count. Practically: name in the quote exactly what the invoice must carry.

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

Section 4(a) works in two stages: ריבית שקלית from the payment date fixed by section 3, and after a further 30 days דמי פיגורים as well, both per `Chok Psikat Ribit veHatzmada 5721-1961` (חוק פסיקת ריבית והצמדה, התשכ"א-1961).

Section 4(b) narrows this for a 3(e)(1) body and a 3(g) business: the interest provisions apply only where that payer "היתה לו עדיפות בעיצוב תנאי החוזה" (had superiority in shaping the contract terms). That is the ordinary case when a freelancer quotes a larger client, but it is a condition, not an automatic entitlement.

Section 4(c) preserves every other remedy the supplier has for non-payment.

## Drafting the payment-terms clause

Suggested clause (Hebrew, drop into the quote):

> **תנאי תשלום:** שוטף + 30 ימים מהנפקת החשבונית, כמוסכם בין הצדדים. בהיעדר הסכמה אחרת, חוק מוסר תשלומים לספקים, התשע"ז-2017 קובע שוטף + 45 בעסקה בין עסקים. איחור מעבר למועד שבחוק נושא ריבית שקלית, ובחלוף 30 ימים נוספים גם דמי פיגורים, לפי חוק פסיקת ריבית והצמדה, התשכ"א-1961.

English equivalent (for bilingual quotes):

> **Payment terms:** Net end-of-month + 30 days from invoice issuance ("shotef + 30"), as agreed between the parties. Absent another agreed date, the Late Payment to Suppliers Law 5777-2017 sets end-of-month + 45 days for business-to-business transactions. Delay beyond the statutory date accrues shekel interest, and after a further 30 days arrears charges as well, per the Interest and Linkage Law 5721-1961.

## Defaults this skill uses

- **Default term:** shotef + 30 (better than legal max, helps cash flow)
- **Statutory date for a B2B client:** shotef + 45 when the contract is silent (warn if the user agrees to longer, but do not tell them a longer agreed term is void)
- **Statutory date for a budgeted body / university client:** shotef + 45, opt-out possible with CEO approval
- **Statutory date for a state authority client:** 45 days from invoice, or 30 days from month-end, depending on the contract's counting basis (85/70 for construction)
- **Statutory date for a local authority client:** 45 days from month-end (80 for construction; externally-financed portion up to 150 days)
