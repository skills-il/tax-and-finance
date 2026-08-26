---
name: israeli-price-quote-generator
description: "Generate compliant Hebrew price quotes (hatzaat mechir / הצעת מחיר) for Israeli freelancers and small businesses. Use when user asks to create a price quote, quote a client, build a pre-sale proposal with VAT, send a hatzaat mechir, or draft a הצעת מחיר. Covers 18% VAT math (or VAT-exempt for oseik patur), validity period (תוקף ההצעה), payment terms aligned with Chok Moser Tashlumim leSapakim 5777-2017 (the Late Payment Law: shotef+30, statutory default shotef+45 for B2B), oseik murshe vs oseik patur header rules, escalation and cancellation clauses, Bit/PayBox/bank transfer payment details, and bilingual HE/EN layout. Outputs ready-to-send Hebrew markdown or printable HTML. Do NOT use for government tender proposals (use israeli-tender-proposal-builder), for generating actual tax invoices after the quote is accepted (use green-invoice), or for chasing unpaid invoices (use israeli-client-payment-chaser)."
license: MIT
---

# Israeli Price Quote Generator

## Legal notice

This is a free information tool operated by an AI model. It explains the tax rules and helps you organise your own figures. All of its outputs are produced automatically by an AI model, with no involvement, review, or approval by a tax adviser or accountant. The output is not a tax opinion, not a return prepared by a licensed representative, and not professional advice, but a general calculation and explanation only: it does not examine the full extent of your income or your complete documents. An AI model may err, omit data, or present a wrong conclusion.

Any form or text this tool produces is an automatic draft for your personal preparation only, and is not a filed return. Any wording this tool drafts is an automatic draft for your personal preparation only. It is not a document drawn up by a lawyer and may not be relied on as evidence. Explanations here about how a clause would be treated, including a payment term, a validity date or a cancellation charge, are general information and not a legal opinion. This tool is not a substitute for advice that takes account of the particular circumstances and needs of each person, and before taking a proceeding, signing a document, or filing with an authority or a court, consult a lawyer. Responsibility for reporting and for paying the tax is yours, the binding computation is the Tax Authority's, and representation before the Tax Authority is reserved to those permitted by law. This tool is not a substitute for advice that takes account of the particular circumstances and needs of each person. Consult a tax adviser or accountant before filing or paying. All use of its output is the user's sole responsibility.


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

Note the other side of that coin. Under section 3(b) of the Contracts Law, an offeror who fixed a time for acceptance may not revoke the offer once it has been delivered to the offeree. Printing a validity date therefore makes the quote **irrevocable until that date**, which binds the issuer, not only the client. Keep the window short whenever the price depends on a cost that can move (materials, a subcontractor, an exchange rate), or write an explicit adjustment clause into the price.

### Step 4: Set the payment terms clause

The legal anchor is **חוק מוסר תשלומים לספקים, התשע"ז-2017** (Late Payment to Suppliers Law, 5777-2017). It caps how long a payer can delay paying a supplier:

| Payer (as defined in section 2) | Statutory cap | Section |
|---|---|---|
| State authority (President's office, Knesset, State Comptroller, Bank of Israel, ISA, Bituach Leumi), government ministry, Mifal HaPayis, sports-betting council | 45 days from invoice submission, or 30 days from month-end where the contract counts from month-end | 3(a) |
| The same bodies, for construction-engineering works | 85 days from invoice, or 70 days from month-end | 3(b) |
| Budgeted body, budgeted higher-education institution, any other body established by law | 45 days from month-end, unless the parties expressly agreed another date with the payer's CEO approval | 3(e) |
| Local authority (including its corporations and water corporations) | 45 days from month-end; 80 days from month-end for construction works; an externally-financed portion may be deferred but must be paid within 150 days of invoice | 3(f) |
| Business ("esek": financial institution, oseik morshe, oseik patur) | 45 days from month-end, unless the parties expressly agreed another date in the contract | 3(g) |

The definition of "esek" in section 2 **excludes** a corporation at least half-owned by a local authority, a water corporation, Mifal HaPayis and the sports-betting council, so a quote to one of those is not on the 3(g) track. Check which row the client actually falls into before writing the clause; a university, a government company and a municipality each sit on a different row.

**Critical terminology:** "shotef + N" means *end of the invoice's calendar month + N days*, NOT N days from the invoice date. An invoice dated 5 March under shotef + 30 is due by 30 April, about 56 days post-invoice in the worst case. This is the #1 thing Israeli freelancers get wrong when copying the American "Net 30" wording.

**Default the quote to "shotef + 30" as a freelancer-friendly term** (better cash flow than the default statutory date of shotef + 45).

**Do not tell the client a longer term is automatically void.** Section 3(g) sets shotef + 45 as the default, "אלא אם כן קבעו הצדדים באופן מפורש בחוזה מועד אחר לתשלום", and a longer date is permitted where it is required by the special character of the engagement or is not "בלתי הוגן באופן חריג" (exceptionally unfair). Section 3(e) works the same way for budgeted bodies and universities, with the extra requirement of CEO approval, tender disclosure and a report to the Small and Medium Business Agency. So a shotef + 60 term agreed in writing is not void on its face; it is challengeable as exceptionally unfair. What the freelancer actually gains from the law is the fallback: if the contract is silent, the statutory date governs.

Section 4 adds interest in **two stages**: ריבית שקלית from the payment date under section 3, and after a further 30 days, דמי פיגורים as well (both per `חוק פסיקת ריבית והצמדה, התשכ"א-1961`). Section 4(b) narrows this for a 3(e) body or a 3(g) business: the interest applies only where that payer "היתה לו עדיפות בעיצוב תנאי החוזה" (had superiority in shaping the contract terms), which is the ordinary case for a freelancer quoting a larger client, but is not automatic.

**Section 3(h): an incomplete invoice restarts the clock.** If the invoice omits a material particular required by the contract, or the contractual conditions for payment were not met, the payer returns it with a list of the defects and the invoice is treated as never having been delivered. The examination period is 23 business days (60 days for construction works). This is the single most common way a payer legitimately stretches payment, so the quote should state exactly what the invoice must carry (PO number, contract reference, deliverable sign-off).

Suggested clause text (Hebrew):
> תנאי תשלום: שוטף + 30 ימים מהנפקת החשבונית, כמוסכם בין הצדדים. בהיעדר הסכמה אחרת, חוק מוסר תשלומים לספקים, התשע"ז-2017 קובע מועד של שוטף + 45 בעסקה בין עסקים. איחור מעבר למועד שבחוק נושא ריבית שקלית, ובחלוף 30 ימים נוספים גם דמי פיגורים, לפי חוק פסיקת ריבית והצמדה, התשכ"א-1961.

**Important nuance on the late-interest clause:** section 4 triggers statutory interest from the payment date fixed by section 3, not from the day the **contractual** term in your quote is missed. Where the contract is silent that date is shotef + 45 for B2B, so a contractual shotef + 30 is a payment expectation and the statutory interest clock still starts at shotef + 45. Don't draft a clause promising statutory interest "from day 31"; if you want interest earlier than the statutory date, it has to be an agreed contractual interest clause, priced as such.

If the user is asked to accept something longer than the statutory date for their tier (e.g., shotef + 60 in a B2B contract), tell them what is actually true: an expressly agreed longer date is not automatically void, it is challengeable as exceptionally unfair, so the time to push back is before signing, not after the invoice is late.

### Step 5: Build the header

| Issuer type | Header label | Fields to include |
|---|---|---|
| Oseik morshe | "הצעת מחיר" + "עוסק מורשה" + 9-digit מספר עוסק | name, address, phone, email, oseik number |
| Oseik patur | "הצעת מחיר" + "עוסק פטור" + 9-digit מספר עוסק (usually the freelancer's תעודת זהות) | name, address, phone, email, oseik number |
| Chevra | "הצעת מחיר" + "חברה בע"מ" + 9-digit מספר חברה | name, address, phone, email, company number, optionally CEO name |

A price quote is not an accounting document (it is not reported to the tax authorities), so unlike a חשבונית מס it has **no statutory list of mandatory particulars**. The fields above are commercial convention, and they matter because the quote is the document the client will treat as the offer under Contracts Law.

**Oseik patur clarifier (optional but useful):** adding "פטור ממע"מ" or the older phrasing "אינו רשום כעוסק מורשה" alongside the "עוסק פטור" label tells the client up front that they will not receive a tax invoice. The Tax Authority required label is just "עוסק פטור" + number; the clarifier is admin practice, not a regulatory mandate.

### Step 6: Optional clauses (use sparingly)

- **Scope-change clause:** "כל שינוי בהיקף העבודה מעבר למפורט בהצעה זו יחויב בנפרד לפי תעריף שעתי של {rate} ₪ + מע"מ." Useful for project work.
- **FX clause** (only for foreign-currency quotes): "המחירים נקובים ב-USD. הסכום הסופי לחיוב יחושב לפי שער יציג של בנק ישראל ביום הוצאת החשבונית." Israeli convention is to use Bank of Israel's daily reference rate (שער יציג).
- **Cancellation clause:** "ביטול הזמנה לאחר אישור הצעה זו יחויב ב-{percent}% מהסכום הכולל." There is no statutory scale for this. Commercial practice is a rising scale by project stage (lowest before work starts, highest after delivery), and the number should be set against the loss that was foreseeable at signing, which is the test a court applies (see Gotchas).
- **Materials clause:** "המחיר אינו כולל חומרים / רישוי תוכנה / נסיעות מעבר לאזור גוש דן" (or whatever applies).

Don't dump all four onto every quote. Pick what's load-bearing for the specific deal.

### Step 6.5: Zero-rated export quotes (check the exception before writing 0%)

Section 30(a)(5) of the VAT Law zero-rates "מתן שירות לתושב חוץ" (a service to a foreign resident), but the same paragraph carries an exception that catches a very common Israeli freelancer fact pattern:

> לא יראו שירות כניתן לתושב חוץ כאשר נושא ההסכם הוא מתן השירות בפועל, נוסף על תושב החוץ, גם לתושב ישראל בישראל, לשותפות שרוב הזכויות בה הן של שותפים תושבי ישראל או לחברה שלענין פקודת מס הכנסה רואים אותה כתושבת ישראל

In plain terms: if the subject of the agreement is that the service is actually rendered, in addition to the foreign customer, **also to an Israeli resident in Israel, to a partnership mostly owned by Israeli residents, or to a company treated as an Israeli resident**, the transaction is NOT zero-rated even though the invoice goes abroad and payment arrives in dollars. Consulting for a foreign parent where the work is actually delivered to its Israeli subsidiary is the textbook case. The paragraph also carves out "שירות ששר האוצר קבע לענין זה", so a service on the Finance Minister's list is outside the zero rate regardless.

The exposure is asymmetric: the freelancer who quoted 0% and is later assessed at 18% cannot re-bill a foreign client after the fact and pays it out of margin. Before writing 0% on a quote, ask who actually receives the service, not who pays the invoice. Where the answer is not clearly "only the foreign resident", quote the price as "plus VAT if applicable" and get a written confirmation of the recipient, or route the user to a CPA. Keep the engagement contract, the proof of foreign residency and the foreign-currency payment record; the zero rate has to be documented, not just asserted.

### Step 7: Payment-method footer

Israeli SMB clients overwhelmingly expect at least one of:

- **Bit:** peer-to-peer payment app from Bank Hapoalim. Two limits published by Bit itself govern a freelancer collecting through it: the P2P service accepts up to **100,000 ₪ per calendar year** in receipts (since 14.11.2024), and a **0.8% fee** applies to receipts above a cumulative **25,000 ₪ per calendar year** ("התקרה החינמית"). Bit's own pages disagree on when that fee started, so quote the rate, not the start date. This is the consumer P2P tier, not a merchant-acquiring contract. Often the default for invoices under ~5,000 ₪.
- **PayBox:** competing P2P app from Discount Bank. Its fee and annual caps have changed more than once since 2025 and its public fee page was not reachable at the time of writing, so confirm the current figures with the bank before promising the client a PayBox route.
- **Pepper Pay:** the P2P feature inside the Pepper banking app. Less common in B2B than Bit, so confirm the client actually uses it before making it the only route.
- **Bank transfer (העברה בנקאית):** include bank name, branch (סניף), account number. Format: `בנק לאומי (10), סניף 800, חשבון 12345/67`.
- **Credit card via a gateway** (Cardcom, Tranzila, Grow). If the user wants to pass processing fees on to the client, add a surcharge clause; the actual percentage depends on the user's processor contract and card scheme, confirm before quoting.

Avoid asking for a wire transfer (SWIFT) from an Israeli client, it's slow and they'll resist.

### Step 8: Emit the document

Default output is markdown (easy to paste into email, convert to PDF in Pages/Word, or render in a markdown-to-PDF tool). When the user wants a printable file, emit HTML with `dir="rtl"` on the body and inline CSS that prints to A4. See `scripts/quote_builder.py` for a working example.

### After acceptance

Once the client accepts the quote (in writing, email reply is enough under contract law), the next step is the actual tax invoice.

**Allocation numbers (מספר הקצאה) now sit under most B2B quotes.** Under the חשבוניות ישראל reform, from **01.06.2026 a tax invoice above 5,000 ₪ needs an allocation number from the Tax Authority** for the invoice to be usable by the buyer (the threshold was above 10,000 ₪ in the first half of 2026, above 20,000 ₪ in 2025 and above 25,000 ₪ in 2024). Two things follow, and both are commonly misstated:

- The allocation number gates the **buyer's input-VAT deduction**, not the invoice's validity. An invoice issued without one is not void; the issuer still reports and remits the output VAT. The loss falls on the customer, who cannot offset the VAT.
- The number can be requested **retroactively up to a year** from issuance (past six months a deferral application is also needed), so a missing number at issue time is recoverable, not fatal.

For a quote above 5,000 ₪ to a business client this is worth one line in the payment section ("החשבונית תופק עם מספר הקצאה מרשות המסים"), because the client's bookkeeper will ask. An oseik patur is unaffected: the regime attaches to חשבונית מס, which they cannot issue. Use the **`green-invoice`** skill to issue a חשבונית מס (oseik morshe) or חשבונית עסקה / קבלה (oseik patur) via the Green Invoice / Morning API. The price quote itself is NOT a tax event, no VAT is reported, no entry in the books, but a written acceptance creates a binding contract under Contracts Law section 1 (offer + acceptance) and section 5 (acceptance by notice to the offeror).

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

**תנאי תשלום:** שוטף + 30 ימים מהנפקת החשבונית, כמוסכם בין הצדדים. בהיעדר הסכמה אחרת חוק מוסר תשלומים לספקים, התשע"ז-2017 קובע שוטף + 45 בעסקה בין עסקים.

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

For an Israeli SaaS selling to a US customer, emit two columns: Hebrew on the right (RTL block), English on the left (LTR block). Currency is USD with the bank-of-Israel FX clause from Step 6. A service to a foreign resident is zero-rated under VAT Law section 30(a)(5), so note "VAT 0% (export of services per VAT Law §30(a)(5))" on the line, but read the exception in Step 6.5 before you write 0% on any quote.

## Bundled Resources

### references/

- `payment-terms-law.md`, full breakdown of חוק מוסר תשלומים לספקים 5777-2017 with every payer tier (3(a), 3(b), 3(e), 3(f), 3(g)), the section 3(h) incomplete-invoice rule and the two-stage section 4 interest.
- `vat-and-oseik-status.md`, 2026 thresholds, when to upgrade from oseik patur, how to handle the calendar year you cross the threshold.
- `quote-templates.md`, four ready-to-copy templates: hourly consulting and fixed-scope project (oseik morshe), an oseik patur variant, and a bilingual HE/EN export quote.
- `domain-checklist.md`, the skill's domain coverage contract.

### scripts/

- `quote_builder.py`, CLI that takes a JSON spec (issuer, client, line items, terms) and emits markdown or HTML. Validates the payment-terms tier and warns if VAT was set wrong for the oseik status.

## Recommended MCP Servers

No MCP server is required to draft a quote. After acceptance, the natural next step is to issue the actual invoice via the **`green-invoice`** skill (Green Invoice / Morning API). Optionally, the **`boi-economic-data`** MCP can supply the daily שער יציג for the FX clause in Step 6.

## Reference Links

| Source | URL | What to Check |
|---|---|---|
| Late Payment to Suppliers Law text | https://www.nevo.co.il/law_html/law00/144599.htm | Current payer tiers, payment caps, late-interest reference |
| Late Payment Law plain summary (Kol-Zchut) | https://www.kolzchut.org.il/he/המועד_האחרון_לתשלום_תמורה_לספקים_עבור_סחורה_או_שירות | Plain-language summary of the payer tiers |
| Israeli VAT rate (PwC tax summary) | https://taxsummaries.pwc.com/israel/corporate/other-taxes | Current VAT rate (18% since 2025-01-01) |
| Oseik patur threshold (Kol-Zchut) | https://www.kolzchut.org.il/he/עוסק_פטור | Annual ceiling and reporting rules |
| Contracts Law (General Part) 5733-1973 | https://www.nevo.co.il/law_html/law00/71888.htm | Section 1 (offer/acceptance), section 3(b) (irrevocability), section 5 (acceptance by notice), section 8 (reasonable time) |
| Contracts Law (Remedies for Breach) 5731-1970 | https://www.nevo.co.il/law_html/law00/71887.htm | Section 15 (agreed damages, and the narrow reduction test) |
| Input VAT and allocation numbers (Kol-Zchut) | https://www.kolzchut.org.il/he/%D7%A7%D7%99%D7%96%D7%95%D7%96_%D7%AA%D7%A9%D7%9C%D7%95%D7%9E%D7%99_%D7%9E%D7%A2%22%D7%9E_%D7%A9%D7%9C_%D7%A2%D7%95%D7%A1%D7%A7_%D7%9E%D7%95%D7%A8%D7%A9%D7%94_(%D7%9E%D7%A1_%D7%AA%D7%A9%D7%95%D7%9E%D7%95%D7%AA) | Current allocation-number threshold and what it gates |
| Bit fee and limit page | https://www.bitpay.co.il/he/private-faq | Current receipt fee, its threshold, and the annual P2P receipt cap |
| Price quote document guide (Green Invoice) | https://www.greeninvoice.co.il/magazine/hazat-mechir/ | Distinction between quote, חשבונית עסקה, חשבונית מס |

## Gotchas

- **Don't label an oseik patur quote with the phrase "כולל מע"מ".** Oseik patur cannot charge VAT. Putting "כולל מע"מ" on an oseik patur document looks like fraud and exposes the issuer to a Tax Authority fine. Either show no VAT line at all or write "אינו רשום כעוסק מורשה, לא חייב מע"מ".
- **The VAT rate is 18%, not 17%.** This changed on 2025-01-01. Skills written before then often default to 17%, which is wrong every time. Hardcode 0.18 in calculations.
- **shotef + 30 ≠ 30 days.** It's end-of-month + 30 days. An invoice dated 2 March under shotef + 30 isn't due until 30 April. Don't tell the user "30 days" when explaining the clause, say "up to 60 days post-invoice in the worst case, depending on the invoice date".
- **"VAT 0%" for export is not the same as "no VAT".** An oseik morshe selling services abroad still files a VAT return showing the line as a zero-rated transaction (עסקה חייבת בשיעור אפס). The dealer preserves the right to קיזוז מס תשומות (input-VAT credit) on related expenses, which exempt transactions do NOT. Mark the export line "0%, export of services" and keep the VAT row in the return, don't omit it.
- **Don't promise a binding price after the validity date.** Use the explicit "תוקף ההצעה עד {date}" line, and after that date treat the quote as expired even if the client comes back.
- **Bit's annual receipt ceiling can block a project before the fee does.** The live figures on Bit's own pages are a **100,000 ₪ per calendar year** P2P receipt cap (since 14.11.2024) and a **0.8% fee** on receipts above a cumulative 25,000 ₪ per calendar year. A freelancer who already collected 80,000 ₪ this year cannot take a 30,000 ₪ project on Bit at all, whatever the fee. Check the year-to-date total, not just the single amount, and treat the P2P tier as distinct from a merchant-acquiring contract.
- **Withholding at source (ניכוי במקור) can shrink the cash received.** When the client is a חברה / מוסד / רשות that's a registered tax-deduction agent under פקודת מס הכנסה §164, they withhold income tax from your payment unless you present a valid אישור פטור מניכוי מס במקור (usually valid for one year). For B2B quotes worth more than a few thousand shekels, add a footer line: "התשלום כפוף להצגת אישור פטור מניכוי מס במקור בתוקף; אחרת ינוכה לפי שיעור ברירת המחדל החל על הספק." The withholding doesn't reduce the supplier's invoice amount, only the cash received on the day; the freelancer reconciles via the annual tax return.
- **A cancellation fee is agreed damages, and the reduction test is not "actual damage".** Under סעיף 15(א) לחוק החוזים (תרופות בשל הפרת חוזה), התשל"א-1970, agreed damages are payable "ללא הוכחת נזק" (without proof of damage). A court may reduce them only where they were fixed "ללא כל יחס סביר לנזק שניתן היה לראותו מראש בעת כריתת החוזה" (with no reasonable relation to the damage foreseeable at the time the contract was made), which is a much narrower test than actual loss. So a staged cancellation clause of the kind in Step 6 is enforceable as written unless it is wildly out of proportion, and the freelancer does not have to prove what the cancellation cost them. Set the tiers against foreseeable loss at signing, and say so in the clause if the reasoning is not obvious.

## Troubleshooting

| Issue | Cause | Fix |
|---|---|---|
| VAT calculation off by one agorah | Floating-point rounding | Round subtotal × 0.18 to 2 decimals using banker's rounding (Python's `round()` or `Decimal.quantize(Decimal('0.01'), ROUND_HALF_EVEN)`) |
| Client says "I'll pay in 60 days" | The contract is silent, or the client wants to write a longer term in | Section 3(g) gives shotef + 45 as the default when the contract says nothing, so silence favours the supplier. If the client insists on writing shotef + 60 into the contract, it is not void on its face, it is challengeable as "exceptionally unfair", so negotiate it rather than telling the client it has no effect. |
| Client is a foreign company, wants USD | Currency conversion exposure | Use the FX clause from Step 6, peg to Bank of Israel שער יציג at invoice date, not quote date. Spell out which date in the quote. |
| User crossed the 122,833 ₪ ceiling mid-year | Must upgrade to oseik morshe | The skill should flag this. Quotes after the upgrade date must show VAT; quotes before the upgrade date stay oseik-patur format. Don't backdate. |
| Quote was accepted by email, client now disputes the price | Email acceptance is binding | Under Contracts Law §5, acceptance is by the offeree's notice to the offeror showing intent to contract, and under §6(a) it can also be by conduct performing the contract. (§7 is a different rule, the presumption of acceptance for an offer that only benefits the offeree.) The quote stands. |
