---
name: israeli-price-quote-generator
description: "Generate compliant Hebrew price quotes (hatzaat mechir / הצעת מחיר) for Israeli freelancers and small businesses. Use when user asks to create a price quote, quote a client, build a pre-sale proposal with VAT, send a hatzaat mechir, or draft a הצעת מחיר. Covers 18% VAT math (or VAT-exempt for oseik patur), validity period (תוקף ההצעה), payment terms aligned with Chok Moser Tashlumim leSapakim 5777-2017 (the Late Payment Law: shotef+30, max shotef+45 for SMB suppliers), oseik murshe vs oseik patur header rules, escalation and cancellation clauses, Bit/PayBox/bank transfer payment details, and bilingual HE/EN layout. Outputs ready-to-send Hebrew markdown or printable HTML. Do NOT use for government tender proposals (use israeli-tender-proposal-builder), for generating actual tax invoices after the quote is accepted (use green-invoice), or for chasing unpaid invoices (use israeli-client-payment-chaser)."
license: MIT
---

# Israeli Price Quote Generator

## Legal notice

This is a free information tool operated by an AI model. It explains the tax rules and helps you organise your own figures. All of its outputs are produced automatically by an AI model, with no involvement, review, or approval by a tax adviser or accountant. The output is not a tax opinion, not a return prepared by a licensed representative, and not professional advice, but a general calculation and explanation only: it does not examine the full extent of your income or your complete documents. An AI model may err, omit data, or present a wrong conclusion.

Any form or text this tool produces is an automatic draft for your personal preparation only, and is not a filed return. Responsibility for reporting and for paying the tax is yours, the binding computation is the Tax Authority's, and representation before the Tax Authority is reserved to those permitted by law. This tool is not a substitute for advice that takes account of the particular circumstances and needs of each person. Consult a tax adviser or accountant before filing or paying. All use of its output is the user's sole responsibility.


## Problem

Israeli freelancers and small businesses send price quotes (הצעת מחיר) every week, but most copy an old quote and edit it: the validity date stays stale, the VAT rate stays at 17% three years after the increase, and the payment terms clause silently waives the protections of חוק מוסר תשלומים. A quote that looks fine on the surface costs the freelancer real money when the client pays in 90 days or argues over the VAT line two months later. This skill builds the quote from current data, the right VAT, the right oseik patur header, the legally-correct payment-terms clause, and an explicit validity date, so the freelancer's hand is strong before the work starts.

## Instructions

### Step 1: Identify the issuer's oseik status

Ask the user (or read from prior session memory) whether they are:

- **Oseik morshe (עוסק מורשה):** registered for VAT. Charges 18% VAT on every quote and invoice. Clients can deduct it as input tax.
- **Oseik patur (עוסק פטור):** under the annual turnover ceiling (122,833 ₪ for 2026, CPI-indexed). Does NOT charge VAT. Cannot issue a tax invoice (חשבונית מס), uses חשבונית עסקה for the payment request, then קבלה for the receipt.
- **Esek za'ir (עסק זעיר) is NOT a fourth VAT status.** "Esek za'ir" is the 2024 מסלול מקוצר, an *income-tax* election (30% normative expense deduction, simplified reporting). It is orthogonal to VAT classification: a freelancer in מסלול מקוצר can be either oseik patur or oseik morshe. From the quote's perspective, use whichever VAT status the freelancer actually holds; the מסלול מקוצר election affects income-tax filing, not the quote header.
- **Chevra ba'am (חברה בע"מ):** incorporated. Charges 18% VAT, has both מספר עוסק and מספר חברה.

The oseik status drives whether the quote shows a VAT line, what the issuer header says, and what the issuer can label the future invoice.

### Step 2: Collect the line items

For each line item, get:

- Description (Hebrew preferred for Israeli clients; bilingual if the client is international)
- Quantity and unit (hours, days, units, "fixed")
- Unit price in ₪ (or specify another currency, see Step 6 on FX clauses)
- Optional discount (% or flat ₪)

Compute:

```
line_total = quantity × unit_price − discount
subtotal = sum(line_totals)
vat = subtotal × 0.18    # ONLY if issuer is oseik morshe or chevra
total = subtotal + vat
```

Round VAT and total to two decimals (agorot). Israeli convention is two-decimal display, not whole shekel.

### Step 3: Set the validity period

Default to **14 days** from issue date for project work, **30 days** for product sales or longer-cycle B2B. Never leave the validity field blank, an open-ended quote that's accepted months later may still bind the issuer to outdated pricing: under section 8 of חוק החוזים (חלק כללי), התשל"ג-1973 (Contracts Law (General Part), 5733-1973), an offer with no stated validity must be accepted "within a reasonable time", and what counts as reasonable is decided after the fact by a court.

The quote must show: "תוקף ההצעה עד {date}" / "Quote valid until {date}".

### Step 4: Set the payment terms clause

The legal anchor is **חוק מוסר תשלומים לספקים, התשע"ז-2017** (Late Payment to Suppliers Law, 5777-2017). It caps how long a payer can delay paying a supplier:

| Payer | Statutory cap (per the law) | What it means in days |
|---|---|---|
| State authority (section 3(a)) | 45 days from invoice submission | up to ~45 days |
| Local authority (section 3(f)) | 45 days from month-end (80 for construction) | up to ~75 days |
| Business-to-business (section 3(g)) | 45 days from month-end ("shotef + 45") | up to ~75 days |

**Critical terminology:** "shotef + N" means *end of the invoice's calendar month + N days*, NOT N days from the invoice date. An invoice dated 5 March under shotef + 30 is due by 30 April, about 56 days post-invoice in the worst case. This is the #1 thing Israeli freelancers get wrong when copying the American "Net 30" wording.

**Default the quote to "shotef + 30" as a freelancer-friendly term** (better cash flow than the legal max of shotef + 45). Sections 4 and 4(a) of the law add statutory interest (per `חוק פסיקת ריבית והצמדה, התשכ"א-1961`) on amounts paid past the cap. Any contract clause that imposes longer than the statutory cap on a small-business supplier is void by force of the law, but you still want the clause IN the quote so the client doesn't propose worse later.

Suggested clause text (Hebrew):
> תנאי תשלום: שוטף + 30 ימים מהנפקת החשבונית. חוק מוסר תשלומים לספקים, התשע"ז-2017 קובע תקרה חוקית של שוטף + 45 לעסקה בין עסקים. עיכוב מעבר לתקרה החוקית נושא ריבית פיגורים לפי חוק פסיקת ריבית והצמדה, התשכ"א-1961.

**Important nuance on the late-interest clause:** Sections 4 and 4(a) of the Late Payment Law trigger statutory interest from the day the **statutory cap** is breached (shotef + 45 for B2B), not from the day the **contractual term** in your quote is breached (shotef + 30). The contractual shotef + 30 is a payment expectation; the legal late-interest clock starts at shotef + 45. Don't draft a clause that promises interest "from day 31" because a court will not enforce that.

If the user picks something longer than the legal cap for their tier (e.g., shotef + 60 for an SMB-to-SMB quote), warn them: their client cannot legally enforce that term, but more importantly, accepting longer-than-cap terms can signal weakness.

### Step 5: Build the header

| Issuer type | Header label | Required fields |
|---|---|---|
| Oseik morshe | "הצעת מחיר" + "עוסק מורשה" + 9-digit מספר עוסק | name, address, phone, email, oseik number |
| Oseik patur | "הצעת מחיר" + "עוסק פטור" + 9-digit מספר עוסק (usually the freelancer's תעודת זהות) | name, address, phone, email, oseik number |
| Chevra | "הצעת מחיר" + "חברה בע"מ" + 9-digit מספר חברה | name, address, phone, email, company number, optionally CEO name |

**Oseik patur clarifier (optional but useful):** adding "פטור ממע"מ" or the older phrasing "אינו רשום כעוסק מורשה" alongside the "עוסק פטור" label tells the client up front that they will not receive a tax invoice. The Tax Authority required label is just "עוסק פטור" + number; the clarifier is admin practice, not a regulatory mandate.

### Step 6: Optional clauses (use sparingly)

- **Scope-change clause:** "כל שינוי בהיקף העבודה מעבר למפורט בהצעה זו יחויב בנפרד לפי תעריף שעתי של {rate} ₪ + מע"מ." Useful for project work.
- **FX clause** (only for foreign-currency quotes): "המחירים נקובים ב-USD. הסכום הסופי לחיוב יחושב לפי שער יציג של בנק ישראל ביום הוצאת החשבונית." Israeli convention is to use Bank of Israel's daily reference rate (שער יציג).
- **Cancellation clause:** "ביטול הזמנה לאחר אישור הצעה זו יחויב ב-{percent}% מהסכום הכולל." Standard ranges: 25% before work starts, 50% mid-project, 100% after delivery.
- **Materials clause:** "המחיר אינו כולל חומרים / רישוי תוכנה / נסיעות מעבר לאזור גוש דן" (or whatever applies).

Don't dump all four onto every quote. Pick what's load-bearing for the specific deal.

### Step 7: Payment-method footer

Israeli SMB clients overwhelmingly expect at least one of:

- **Bit:** peer-to-peer payment app from Bank Hapoalim. From January 2025, a **0.6% fee** applies to the portion of receipts exceeding 25,000 ₪ per year (raised to **0.8% for Bit from May 2026**). Business inbound settlement is typically T+1. Confirm the current per-transaction and monthly caps with the bank. Often the default for invoices under ~5,000 ₪.
- **PayBox:** competing P2P app from Discount Bank. Same **0.6% fee** on receipts above 25,000 ₪/year as Bit, in force since Jan 2025.
- **Pepper Pay:** P2P feature inside Bank Leumi's Pepper digital banking app.
- **Bank transfer (העברה בנקאית):** include bank name, branch (סניף), account number. Format: `בנק לאומי (10), סניף 800, חשבון 12345/67`.
- **Credit card via a gateway** (Cardcom, Tranzila, Grow). If the user wants to pass processing fees on to the client, add a surcharge clause; the actual percentage depends on the user's processor contract and card scheme, confirm before quoting.

Avoid asking for a wire transfer (SWIFT) from an Israeli client, it's slow and they'll resist.

### Step 8: Emit the document

Default output is markdown (easy to paste into email, convert to PDF in Pages/Word, or render in a markdown-to-PDF tool). When the user wants a printable file, emit HTML with `dir="rtl"` on the body and inline CSS that prints to A4. See `scripts/quote_builder.py` for a working example.

### After acceptance

Once the client accepts the quote (in writing, email reply is enough under contract law), the next step is the actual tax invoice. Use the **`green-invoice`** skill to issue a חשבונית מס (oseik morshe) or חשבונית עסקה / קבלה (oseik patur) via the Green Invoice / Morning API. The price quote itself is NOT a tax event, no VAT is reported, no entry in the books, but a written acceptance creates a binding contract under Contracts Law section 1 (offer + acceptance) and section 5 (acceptance via notice to the offeror).

## Examples

### Example 1: Hourly consulting quote (oseik morshe)

Input:
- Issuer: Yael Cohen, oseik morshe #311234567, Tel Aviv
- Client: Rishon Tech Ltd, מספר חברה 514567890
- Line: "ייעוץ אסטרטגי, 20 שעות @ 450 ₪"
- Validity: 14 days
- Payment: shotef + 30, Bit or transfer

Expected output (markdown excerpt):

```markdown
# הצעת מחיר 2026-042

**יעל כהן** | עוסק מורשה 311234567
טלפון 050-1234567 | אימייל yael@example.co.il
תל אביב

**לכבוד:** Rishon Tech Ltd (מספר חברה 514567890)
**תאריך הוצאה:** 19 במאי 2026
**תוקף ההצעה עד:** 2 ביוני 2026

| פריט | כמות | מחיר יחידה | סה"כ |
|---|---|---|---|
| ייעוץ אסטרטגי | 20 שעות | 450 ₪ | 9,000 ₪ |

**סה"כ לפני מע"מ:** 9,000 ₪
**מע"מ 18%:** 1,620 ₪
**סה"כ לתשלום:** 10,620 ₪

**תנאי תשלום:** שוטף + 30 ימים מהנפקת החשבונית, בהתאם לחוק מוסר תשלומים לספקים, התשע"ז-2017.

**אמצעי תשלום:** Bit 050-1234567 או העברה בנקאית: בנק לאומי (10), סניף 800, חשבון 12345/67.
```

### Example 2: Fixed-scope project quote (oseik patur)

Input:
- Issuer: Daniel Levi, oseik patur #029876543 (under 122,833 ₪ for 2026)
- Client: small bakery in Haifa
- Line: "עיצוב לוגו + מיתוג בסיסי, חבילה קבועה"
- Validity: 30 days
- No VAT, no escalation clause

Expected header difference:
```
**דניאל לוי** | עוסק פטור 029876543, אינו רשום כעוסק מורשה
```

Total stays at 4,500 ₪ (no VAT line). Footer adds: "לאחר אישור ההצעה תופק חשבונית עסקה, ועם קבלת התשלום, קבלה. אינני רשום כעוסק מורשה ואינני חייב מע"מ."

### Example 3: Hebrew + English bilingual (export client)

For an Israeli SaaS selling to a US customer, emit two columns: Hebrew on the right (RTL block), English on the left (LTR block). Currency is USD with the bank-of-Israel FX clause from Step 6. VAT is 0% if the customer is outside Israel (export of services is zero-rated under VAT Law section 30(a)(5)), but the issuer is still oseik morshe, note "VAT 0% (export of services per VAT Law §30(a)(5))" on the line.

## Bundled Resources

### references/

- `payment-terms-law.md`, full breakdown of חוק מוסר תשלומים לספקים 5777-2017 with the three payer tiers and what each tier's cap actually means in calendar days.
- `vat-and-oseik-status.md`, 2026 thresholds, when to upgrade from oseik patur, how to handle the calendar year you cross the threshold.
- `quote-templates.md`, three full ready-to-copy Hebrew templates (hourly consulting, fixed project, monthly retainer) and one bilingual HE/EN template.

### scripts/

- `quote_builder.py`, CLI that takes a JSON spec (issuer, client, line items, terms) and emits markdown or HTML. Validates the payment-terms tier and warns if VAT was set wrong for the oseik status.

## Recommended MCP Servers

No MCP server is required to draft a quote. After acceptance, the natural next step is to issue the actual invoice via the **`green-invoice`** skill (Green Invoice / Morning API). Optionally, the **`boi-economic-data`** MCP can supply the daily שער יציג for the FX clause in Step 6.

## Reference Links

| Source | URL | What to Check |
|---|---|---|
| Late Payment to Suppliers Law text | https://www.nevo.co.il/law_html/law00/144599.htm | Current payer tiers, payment caps, late-interest reference |
| Late Payment Law plain summary (Kol-Zchut) | https://www.kolzchut.org.il/he/המועד_האחרון_לתשלום_תמורה_לספקים_עבור_סחורה_או_שירות | Plain-language summary of the three payer tiers |
| Israeli VAT rate (PwC tax summary) | https://taxsummaries.pwc.com/israel/corporate/other-taxes | Current VAT rate (18% since 2025-01-01) |
| Oseik patur threshold (Kol-Zchut) | https://www.kolzchut.org.il/he/עוסק_פטור | Annual ceiling and reporting rules |
| Contracts Law (General Part) 5733-1973 | https://www.nevo.co.il/law_html/law00/71888.htm | Section 1 (offer/acceptance), section 3(b) (irrevocability), section 8 (reasonable time) |
| Price quote document guide (Green Invoice) | https://www.greeninvoice.co.il/magazine/hazat-mechir/ | Distinction between quote, חשבונית עסקה, חשבונית מס |

## Gotchas

- **Don't label an oseik patur quote with the phrase "כולל מע"מ".** Oseik patur cannot charge VAT. Putting "כולל מע"מ" on an oseik patur document looks like fraud and exposes the issuer to a Tax Authority fine. Either show no VAT line at all or write "אינו רשום כעוסק מורשה, לא חייב מע"מ".
- **The VAT rate is 18%, not 17%.** This changed on 2025-01-01. Skills written before then often default to 17%, which is wrong every time. Hardcode 0.18 in calculations.
- **shotef + 30 ≠ 30 days.** It's end-of-month + 30 days. An invoice dated 2 March under shotef + 30 isn't due until 30 April. Don't tell the user "30 days" when explaining the clause, say "up to 60 days post-invoice in the worst case, depending on the invoice date".
- **"VAT 0%" for export is not the same as "no VAT".** An oseik morshe selling services abroad still files a VAT return showing the line as a zero-rated transaction (עסקה חייבת בשיעור אפס). The dealer preserves the right to קיזוז מס תשומות (input-VAT credit) on related expenses, which exempt transactions do NOT. Mark the export line "0%, export of services" and keep the VAT row in the return, don't omit it.
- **Don't promise a binding price after the validity date.** Use the explicit "תוקף ההצעה עד {date}" line, and after that date treat the quote as expired even if the client comes back.
- **Bit has business-account limits and a receipts fee.** The per-transaction and monthly caps changed in 2024 and again in 2025. A **0.6% fee** (0.8% for Bit from May 2026) applies to the portion of receipts above 25,000 ₪ aggregate per year, not the flat higher rate some older guides still quote. Confirm the user's current limit and fee with their bank before quoting a 30,000 ₪ project as "pay via Bit".
- **Withholding at source (ניכוי במקור) can shrink the cash received.** When the client is a חברה / מוסד / רשות that's a registered tax-deduction agent under פקודת מס הכנסה §164, they withhold income tax from your payment unless you present a valid אישור פטור מניכוי מס במקור (usually valid for one year). For B2B quotes worth more than a few thousand shekels, add a footer line: "התשלום כפוף להצגת אישור פטור מניכוי מס במקור בתוקף; אחרת ינוכה לפי שיעור ברירת המחדל החל על הספק." The withholding doesn't reduce the supplier's invoice amount, only the cash received on the day; the freelancer reconciles via the annual tax return.
- **Cancellation-fee tiers are not automatically enforceable.** The 25 / 50 / 100 percent tiers in Step 6 are common practice, but a court can cap an excess cancellation fee at the supplier's actual damages under סעיף 15 לחוק החוזים (תרופות בשל הפרת חוזה), התשל"א-1970 if the fee is challenged as a contractual penalty. Use the tiers as a negotiating anchor, not as a guaranteed payout.

## Troubleshooting

| Issue | Cause | Fix |
|---|---|---|
| VAT calculation off by one agorah | Floating-point rounding | Round subtotal × 0.18 to 2 decimals using banker's rounding (Python's `round()` or `Decimal.quantize(Decimal('0.01'), ROUND_HALF_EVEN)`) |
| Client says "I'll pay in 60 days" | Client is unaware of the Late Payment Law | Reference the law in the payment clause. For an SMB supplier to large business, shotef+45 is the legal max; longer terms in a contract are void. |
| Client is a foreign company, wants USD | Currency conversion exposure | Use the FX clause from Step 6, peg to Bank of Israel שער יציג at invoice date, not quote date. Spell out which date in the quote. |
| User crossed the 122,833 ₪ ceiling mid-year | Must upgrade to oseik morshe | The skill should flag this. Quotes after the upgrade date must show VAT; quotes before the upgrade date stay oseik-patur format. Don't backdate. |
| Quote was accepted by email, client now disputes the price | Email acceptance is binding | Under Contracts Law §7, written acceptance of a written offer creates a contract. The quote stands. |
