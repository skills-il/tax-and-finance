---
name: israeli-client-payment-chaser
description: Chase unpaid invoices and manage debt collection for Israeli freelancers and businesses. Use when user asks about "unpaid invoices Israel", "payment reminder", "invoice aging", "debt collection freelancer", "michtav hitchayvut", "demand letter Hebrew", "tvi'ot ktanot", or "גביית חובות". Covers graduated WhatsApp/email reminder escalation, Hebrew demand letter generation, Small Claims Court eligibility assessment, and Shabbat/holiday-aware scheduling. Do NOT use for invoice generation (use israeli-e-invoice) or general accounting.
license: MIT
allowed-tools: Bash(python:*) WebFetch
compatibility: Works with Claude Code, OpenClaw, Cursor. OpenClaw recommended for scheduled reminder automation and WhatsApp message delivery.
---

# Israeli Client Payment Chaser

## Instructions

### Step 1: Establish the Statutory Payment Deadline
Before chasing anything, fix the date the payment became legally late. This is governed by the **Payment Ethics to Suppliers Law, 5777-2017 (חוק מוסר תשלומים לספקים, תשע"ז-2017)**.

- **Default term when no payment term was agreed:** 45 days. For a private business the clock runs from the end of the month in which the invoice was submitted; for state bodies the term is within 45 days and **not later than shotef+30** (current month plus 30 days); local authorities pay within 45 days from the end of the month the invoice was issued. Engineering and construction contracts have longer caps (up to 85 days from submission, or 70 days from month-end). A 2024 amendment gives small contractors on sub-75,000 NIS public-sector contracts a 30-day term.
- An agreed contractual term overrides the default, but the law caps how far it can be pushed out.
- Once the statutory (or agreed) due date passes, the debt is legally late: linkage and interest attach automatically, with no need for the creditor to "declare" lateness.
- **Late-payment interest (dmei pigurim / ribit pigurim)** under this law accrues from the due date at the Accountant General's rate. Do NOT quote a self-invented percentage in a reminder or demand letter. State that statutory late-payment interest applies from the due date and that the exact rate is the current Accountant General rate, or have the user confirm the rate with their accountant. See references/legal-escalation.md.

This statutory deadline, not a generic net-30/60/90 assumption, is what the aging buckets in Step 2 should be measured against.

### Step 2: Import/Track Invoice Aging
Import outstanding invoices (from israeli-e-invoice output, if available, or manual entry) and categorize by aging buckets:

| Bucket | Age | Status |
|--------|-----|--------|
| Current | 0-29 days | Monitor, no action needed |
| 30-day | 30-59 days | Friendly WhatsApp reminder |
| 60-day | 60-89 days | Formal email with demand letter |
| 90+ day | 90+ days | Legal escalation evaluation |

Track per-client details:
- Total amount owed across all invoices
- Oldest outstanding invoice date
- Payment history (on-time vs late patterns)
- Contact details (WhatsApp number, email, mailing address)

Store tracking data in persistent memory for ongoing monitoring across sessions. If persistent memory is unavailable, export as `payment-chaser-data.json` in the working directory and reload it at the start of each session.

### Step 3: Configure Graduated Reminder Schedule
Set up a Shabbat/chagim-aware reminder escalation sequence. **No reminders may be sent on Shabbat (Friday sunset to Saturday sunset) or Jewish holidays.** If a scheduled reminder falls on a blocked day, move it to the next business day (typically Sunday). See references/legal-escalation.md for major holiday dates.

- **Day 30, Friendly WhatsApp:**
  "היי [שם], רציתי לבדוק לגבי חשבונית מספר [X] מ-[DATE] בסך [AMOUNT] ש"ח. אשמח לעדכון."

- **Day 45, Follow-up WhatsApp:**
  "שלום [שם], תזכורת נוספת לגבי חשבונית [X]. סה"כ לתשלום: [AMOUNT] ש"ח. פרטי העברה: [BANK DETAILS]."

- **Day 60, Formal email** with invoice copy attached and a clear payment deadline.

- **Day 75, Warning of potential legal steps:**
  "שלום [שם], למרות פניותינו הקודמות, חשבונית [X] טרם שולמה. ללא תשלום תוך 14 יום, ניאלץ לשקול צעדים נוספים."

- **Day 90+, Escalation alert:** Evaluate legal options (see Step 6). Generate formal demand letter (see Step 4).

See references/reminder-templates.md for complete, customizable templates at each stage.

### Step 4: Generate Hebrew Demand Letters (Michtav Hitchayvut)
Generate a formal Hebrew demand letter at the 60 or 90 day mark. The letter must include:

1. **Creditor details:** Full name/business name, address, osek murshe/patur number
2. **Debtor details:** Full name/business name, address, registration number
3. **Invoice details:** Invoice number, date issued, original amount, any partial payments received
4. **Total amount due:** Including interest if applicable (see interest calculation below)
5. **Payment deadline:** Typically 14 days from letter date
6. **Warning of legal action:** Clear statement that failure to pay will result in legal proceedings

**Interest calculation, two distinct statutes (do not conflate them):**

1. **Interest a supplier may claim pre-suit** is governed by the Payment Ethics to Suppliers Law, 5777-2017. Late-payment interest (dmei pigurim) runs from the statutory or agreed due date at the **Accountant General's rate**. This is the figure to reference in a demand letter. It is NOT the Bank of Israel monetary-policy rate. Do not write a hard percentage into the letter unless the user's accountant has confirmed the current Accountant General rate; otherwise state that statutory late-payment interest applies from the due date.
2. **Interest a court adjudicates on a judgment** is governed by the Adjudication of Interest and Linkage Law (חוק פסיקת ריבית והצמדה). The court sets interest plus CPI linkage (hatzmada) from the due date as part of the judgment. The agent does not compute this; the court does.

**Do not quote the Bank of Israel base rate (the monetary-policy rate, which changes at each rate decision) as if it were the statutory late-payment rate.** They are different numbers serving different purposes. Do not hard-code the BoI rate in this skill, look it up on boi.org.il when needed.

**Late-payment charge regulations (effective 2025):** Regulations effective January 1, 2025 split late charges into "interest" (ribit) and "late payment fees" (dmei pigurim) and eliminated compound interest on enforcement debts. Late payment fees now accrue quarterly (starting 3 months after the due date) rather than compounding. When estimating amounts for a demand letter, use the simple-interest method per the reformed regime, and verify the published quarterly rate.

**Delivery options:**
- Registered mail (doar rashum / דואר רשום): provides legal proof of sending. Keep the postal receipt.
- Email with read receipt: supplementary, not a replacement for registered mail for legal purposes.

See references/legal-escalation.md for full demand letter requirements and format.

### Step 5: Track Payment Promises and Negotiate
Record and follow up on payment commitments:

- **Log payment promises:** Record the promised amount, committed payment date, and communication channel (WhatsApp, email, phone).
- **Set follow-up alerts:** Configure reminders for 1 day after the promised payment date to verify receipt.
- **Track partial payments:** Update the outstanding balance when partial payments are received. Issue a receipt/confirmation for each partial payment.
- **Maintain communication history:** Timestamp every interaction (message sent, response received, promise made, payment received). This log serves as evidence if legal action becomes necessary.
- **Negotiation support:** If the debtor requests a payment plan, help structure installments. Document the agreement in writing and have both parties confirm.

### Step 6: Evaluate Small Claims Court (Tvi'ot Ktanot) Eligibility
When a debt reaches 90+ days and collection efforts have failed, assess Small Claims Court eligibility:

**Decide first: self-serve or involve a lawyer.** Small Claims is designed for self-representation, but recommend the user consult a lawyer instead of self-filing when any of these apply:
- The debtor genuinely disputes liability (claims the work was defective, never ordered, or already paid).
- The debtor appears insolvent or is in liquidation/insolvency proceedings (a judgment against an empty shell is worthless; a lawyer can advise on priority and timing).
- The debt is near the statute-of-limitations deadline (7 years for an ordinary debt/invoice under sec. 5(a) of the Limitation Law) and a procedural mistake could forfeit the claim entirely.
- The debtor is cross-border (outside Israel), which raises jurisdiction and enforcement questions Small Claims cannot handle.
- The amount exceeds the Small Claims threshold (must go to Magistrate Court, which requires representation).
Otherwise, a documented, undisputed invoice under the threshold is a good self-serve candidate.

**Threshold:** Up to 39,900 NIS (as of January 1, 2026; verify current amount at the courts administration website, updated periodically).

**Eligibility checklist:**
- Was proper written notice (demand letter) sent to the debtor?
- Does documentation exist for the debt? (original invoice, signed contract/PO, delivery confirmation)
- Is the amount within the Small Claims threshold?
- Has the debtor acknowledged the debt in any communication?
- Has the filer already used up the annual quota? A person may file at most **5 small claims per calendar year** (yachid); a freelancer chasing many debtors who hits the limit must wait, get court permission, or route the rest through Magistrate Court.

**Filing guide:**
- **Required documents:** Original invoice, delivery/work confirmation, copies of all demand letters sent, communication history log, postal receipts for registered mail
- **Filing fee:** 1% of the claim amount, minimum 50 NIS (2026)
- **Court location:** Determined by the debtor's address jurisdiction (beit mishpat l'tvi'ot ktanot)
- **Timeline:** Filing to hearing date is typically 30-60 days
- **Representation:** In Small Claims Court, parties represent themselves (no lawyers allowed)

For amounts exceeding the Small Claims threshold, the claim must go to Magistrate Court (Beit Mishpat Shalom), which requires legal representation. Recommend the user consult a lawyer.

See references/legal-escalation.md for the complete filing process.

### Step 7: Open an Enforcement Office (Hotza'a LaPo'al) File to Collect
A Small Claims judgment is not money in the bank. To actually collect, the creditor must open an enforcement file with the Enforcement and Collection Authority (Rashut HaAchifa veHaGviya).

- **After a judgment:** A request to enforce a monetary judgment can be filed only once 30 days have passed from the date the judgment was given. The creditor opens a "judgment" file (tik psak din), submits the judgment bearing the court stamp plus supporting documents, and pays an opening fee of roughly 1% of the debt plus a protocol fee. The enforcement registrar can then impose liens, garnish bank accounts and wages, and order asset seizure.
- **Bounced-check / promissory-note shortcut (skips court entirely):** A dishonored cheque (with the bank's Notice of Dishonor) or a signed promissory note can be filed directly as a "notes and cheques" file (tik shtarot ve'hamcha'ot) at the Enforcement Office, with no Small Claims judgment needed first. The debtor then has a short window to object; if they do, the matter is referred to court. Use this route when the debt is backed by such an instrument.
- Required documents: stamped judgment OR the cheque printout / signed promissory note, plus identification of the debtor and proof of the debt.

See references/legal-escalation.md for the enforcement process.

### Step 8: Generate Aging Reports and Cash Flow Forecasts
Produce comprehensive collection management reports:

**Aging report:**
- Total outstanding by bucket (current, 30-day, 60-day, 90+)
- Per-client breakdown with oldest invoice date and total owed
- Trend comparison: this month vs previous month

**Cash flow forecast:**
- Expected collections based on historical payment patterns
- Probability-weighted forecast using client risk scores
- Gap analysis: projected income vs expected expenses

**Monthly collection summary:**
- Total collected during the period
- Total still outstanding
- Collection rate percentage (collected / total invoiced)
- Number of invoices resolved vs still open

**Client risk scoring:**
- **Reliable:** Pays within terms or within 30 days consistently
- **Slow payer:** Regularly pays 30-60 days late but eventually pays
- **Problematic:** 60+ days late, requires multiple follow-ups, broken promises

**Export formats:** PDF report for review, CSV for spreadsheet analysis.

## Examples

### Example 1: Setting Up Collection Reminders for 5 Overdue Invoices
User says: "I have 5 unpaid invoices from the last 3 months, can you help me collect?"
Actions:
1. Import invoice details (client, amount, date, status)
2. Categorize by aging: 2 at 30 days, 2 at 60 days, 1 at 90+ days
3. Configure WhatsApp reminders for 30-day invoices
4. Generate formal emails for 60-day invoices
5. Prepare demand letter for the 90+ day invoice
6. Set up tracking dashboard with total outstanding: 47,500 NIS
Result: Collection workflow activated. Friendly reminders sent to 2 clients, formal follow-ups to 2 others, and demand letter drafted for review. Dashboard showing 47,500 NIS total outstanding across 5 clients.

### Example 2: Client Promised to Pay but Didn't Follow Through
User says: "ABC Ltd promised to pay invoice 1234 two weeks ago but still nothing"
Actions:
1. Pull communication history for ABC Ltd
2. Note: promise was made on [date], 14 days overdue on promise
3. Draft escalated WhatsApp message referencing the broken promise
4. Prepare formal demand letter (michtav hitchayvut)
5. Assess Small Claims eligibility (invoice: 22,000 NIS, under threshold)
6. Present escalation options to user
Result: Escalated follow-up sent. Demand letter ready for registered mail. Small Claims filing guide prepared with required documents and filing steps.

### Example 3: Generating Monthly Collection Report
User says: "Show me where I stand with all my outstanding invoices this month"
Actions:
1. Pull all tracked invoices and payment status
2. Calculate aging buckets: 3 current (18,000 NIS), 2 at 30-day (12,000 NIS), 1 at 60-day (8,500 NIS), 1 at 90+ (15,000 NIS)
3. Generate cash flow forecast based on payment patterns
4. Score clients by risk level
5. Create monthly summary: 78% collection rate, 53,500 NIS outstanding
Result: Comprehensive aging report with client risk scores. Cash flow forecast shows expected 35,000 NIS collection in next 30 days. Recommended actions: escalate the 90+ day invoice to demand letter stage.

## Bundled Resources

### References
- `references/legal-escalation.md` - Israeli legal framework for debt collection: demand letter (michtav hitchayvut) requirements, Small Claims Court (tvi'ot ktanot) thresholds and filing process, interest calculation rules, and registered mail documentation. Consult when preparing legal escalation in Steps 4 and 6.
- `references/reminder-templates.md` - WhatsApp and email reminder templates in Hebrew for each escalation stage (friendly, follow-up, formal, pre-legal). Templates are customizable with placeholder fields. Consult when configuring reminder messages in Step 3.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Bank of Israel - interest rates | https://www.boi.org.il/information/interestrates/primerates/ | Current BoI base rate used for statutory interest calculation |
| Courts Administration - Small Claims service page | https://www.gov.il/he/service/filing_a_small_claim | Current threshold, filing process, jurisdiction rules |
| Kol-Zchut - Filing a small claim (Hebrew) | https://www.kolzchut.org.il/he/הגשת_תביעה_קטנה | Plain-language eligibility and procedure guide |
| Nevo - Adjudication of Interest and Linkage Law (text) | https://www.nevo.co.il/law_html/law00/75001.htm | Full statutory text on court-adjudicated interest and linkage |
| Nevo - Payment Ethics to Suppliers Law, 5777-2017 | https://www.nevo.co.il/law_html/law00/144599.htm | Statutory 45-day default payment term and late-payment interest |
| Kol-Zchut - Payment deadline to suppliers | https://www.kolzchut.org.il/he/המועד_האחרון_לתשלום_תמורה_לספקים | Plain-language guide to the 45-day rule by purchaser type |
| Enforcement Authority - judgment enforcement file | https://www.gov.il/he/service/claim_for_a_specified_amount_opening_file | Opening a Hotza'a LaPo'al file, fees, required documents |
| Enforcement Authority - cheques and notes file | https://www.gov.il/he/service/opening_promissory_notes_and_checks_file | Filing a dishonored cheque or promissory note directly |
| Israel Post - Registered mail service | https://www.israelpost.co.il | Registered mail (doar rashum) service and pricing |
| HebCal - Jewish calendar | https://www.hebcal.com | Shabbat times and holiday dates for reminder scheduling |

## Recommended MCP Servers

| MCP Server | Why |
|------------|-----|
| `hebcal` | Step 3 (graduated reminder scheduling) and the Troubleshooting "Reminder sent on Shabbat/holiday" case both depend on Shabbat and chag-aware scheduling. Use it to resolve Shabbat entry/exit times and holiday dates so reminders never fire on a blocked day. |
| `israel-law` / `kolzchut` | Optional. Look up the current text of the Payment Ethics to Suppliers Law, Small Claims procedure, and enforcement rules instead of relying on cached figures. |

## Gotchas
- Israeli payment terms (shotef) work differently than net-30/60/90. "Shotef + 30" means end of current month plus 30 days, not 30 days from invoice date. Agents may miscalculate due dates.
- A Small Claims judgment does not collect itself. To enforce it the creditor must open a Hotza'a LaPo'al file (see Step 7), and a judgment-enforcement file can only be opened 30 days after the judgment. Agents may stop at "you won" and forget the collection step.
- Formal enforcement (hotza'a lapo'al) requires a court judgment, a bounced cheque with the bank Notice of Dishonor, a promissory note, or another enforceable instrument. A dishonored cheque or promissory note can be filed at the Enforcement Office directly, skipping court. Agents may suggest filing a claim without the proper prerequisites, or miss the direct-filing shortcut.
- Late-payment interest a supplier claims pre-suit comes from the Payment Ethics to Suppliers Law, 5777-2017 (Accountant General rate), while interest on a judgment comes from the Adjudication of Interest and Linkage Law (set by the court). Do not quote the Bank of Israel monetary-policy rate as the statutory late-payment rate (and do not hard-code its value, it changes per rate decision). Agents may conflate the statutes or invent a percentage.
- Payment reminder communications in Israel must be in Hebrew for Hebrew-speaking clients. Agents may generate English-only reminders that lack legal standing in Israeli small claims court.
- Statute of limitations (hithayyashnut): an ordinary debt or unpaid invoice has a **7-year** limitation period (sec. 5(a) of the Limitation Law, 1958), not 3 years. Do NOT tell a user a commercial invoice is time-barred at 3 years, that is wrong and could make them abandon a still-collectable debt. A money judgment has a 25-year period, and a debt already in an open enforcement (Hotza'a LaPo'al) file does not lapse at 7 years. This is critical for the 90+ day escalation guidance: if a debt is approaching the 7-year deadline, escalation to legal action must be prioritized immediately.

## Troubleshooting

### Error: "Reminder sent on Shabbat/holiday"
Cause: Schedule not properly configured for Jewish holidays or Shabbat times.
Solution: Verify Shabbat/holiday calendar is loaded. Shabbat starts Friday at sunset (varies by season) and ends Saturday after nightfall. Check references/legal-escalation.md for major holiday dates. Reschedule any blocked reminders to the next business day (typically Sunday).

### Error: "Small Claims threshold exceeded"
Cause: Invoice amount exceeds the Small Claims Court maximum (currently 39,900 NIS).
Solution: For amounts above the threshold, the claim must go to Magistrate Court (Beit Mishpat Shalom) which requires legal representation. Recommend the user consult a lawyer. For multiple invoices to the same debtor, consider whether they can be combined or must be filed separately.

### Error: "Demand letter delivery not confirmed"
Cause: Registered mail (doar rashum) was returned or not collected by debtor.
Solution: Registered mail has legal standing even if not collected. Keep the postal receipt as proof of sending. If the debtor's address is wrong, attempt to verify through the Population Authority (Misrad HaPnim). Consider alternative delivery methods recognized by Israeli courts.

### Error: "Interest calculation disputed"
Cause: Applied the wrong interest rate or conflated the two statutes.
Solution: Separate the two. Pre-suit, a supplier's late-payment interest comes from the Payment Ethics to Suppliers Law, 5777-2017, at the Accountant General's rate, accruing from the due date. Interest on a judgment is set by the court under the Adjudication of Interest and Linkage Law. Do not use the Bank of Israel monetary-policy rate as the late-payment rate. If the exact Accountant General rate is unknown, state that statutory late-payment interest applies from the due date and have the user confirm the rate with their accountant.
