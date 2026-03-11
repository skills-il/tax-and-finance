---
name: israeli-client-payment-chaser
description: >-
  Chase unpaid invoices and manage debt collection for Israeli freelancers and businesses.
  Use when user asks about "unpaid invoices Israel", "payment reminder", "invoice
  aging", "debt collection freelancer", "michtav hitchayvut", "demand letter Hebrew",
  "tvi'ot ktanot", or "גביית חובות". Covers graduated WhatsApp/email reminder escalation,
  Hebrew demand letter generation, Small Claims Court eligibility assessment, and
  Shabbat/holiday- aware scheduling. Do NOT use for invoice generation (use israeli-e-invoice)
  or general accounting.
license: MIT
allowed-tools: Bash(python:*) WebFetch
compatibility: >-
  Works with Claude Code, OpenClaw, Cursor. OpenClaw recommended for scheduled reminder
  automation and WhatsApp message delivery.
metadata:
  author: skills-il
  version: 1.0.0
  category: tax-and-finance
  tags:
    he:
    - גביית-חובות
    - invoices
    - תשלום
    - משפטי
    - עצמאי
    - ישראל
    en:
    - debt-collection
    - invoices
    - payment
    - legal
    - freelancer
    - israel
  display_name:
    he: גובה חובות לקוחות ישראלי
    en: Israeli Client Payment Chaser
  display_description:
    he: >-
      מעקב גבייה וניהול חובות לקוחות לפרילנסרים ועסקים ישראליים — תזכורות מדורגות,
      מכתבי התחייבות, ותביעות קטנות
    en: >-
      Chase unpaid invoices and manage debt collection for Israeli freelancers and
      businesses. Use when user asks about "unpaid invoices Israel", "payment reminder",
      "invoice aging", "debt collection freelancer", "michtav hitchayvut", "demand
      letter Hebrew", "tvi'ot ktanot", or "גביית חובות". Covers graduated WhatsApp/email
      reminder escalation, Hebrew demand letter generation, Small Claims Court eligibility
      assessment, and Shabbat/holiday- aware scheduling. Do NOT use for invoice generation
      (use israeli-e-invoice) or general accounting.
  openclaw:
    requires:
      bins: []
      env: []
    emoji: 💰
---

# Israeli Client Payment Chaser

## Instructions

### Step 1: Import/Track Invoice Aging
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

### Step 2: Configure Graduated Reminder Schedule
Set up a Shabbat/chagim-aware reminder escalation sequence. **No reminders may be sent on Shabbat (Friday sunset to Saturday sunset) or Jewish holidays.** If a scheduled reminder falls on a blocked day, move it to the next business day (typically Sunday). See references/legal-escalation.md for major holiday dates.

- **Day 30 — Friendly WhatsApp:**
  "היי [שם], רציתי לבדוק לגבי חשבונית מספר [X] מ-[DATE] בסך [AMOUNT] ש"ח. אשמח לעדכון."

- **Day 45 — Follow-up WhatsApp:**
  "שלום [שם], תזכורת נוספת לגבי חשבונית [X]. סה"כ לתשלום: [AMOUNT] ש"ח. פרטי העברה: [BANK DETAILS]."

- **Day 60 — Formal email** with invoice copy attached and a clear payment deadline.

- **Day 75 — Warning of potential legal steps:**
  "שלום [שם], למרות פניותינו הקודמות, חשבונית [X] טרם שולמה. ללא תשלום תוך 14 יום, ניאלץ לשקול צעדים נוספים."

- **Day 90+ — Escalation alert:** Evaluate legal options (see Step 5). Generate formal demand letter (see Step 3).

See references/reminder-templates.md for complete, customizable templates at each stage.

### Step 3: Generate Hebrew Demand Letters (Michtav Hitchayvut)
Generate a formal Hebrew demand letter at the 60 or 90 day mark. The letter must include:

1. **Creditor details:** Full name/business name, address, osek murshe/patur number
2. **Debtor details:** Full name/business name, address, registration number
3. **Invoice details:** Invoice number, date issued, original amount, any partial payments received
4. **Total amount due:** Including interest if applicable (see interest calculation below)
5. **Payment deadline:** Typically 14 days from letter date
6. **Warning of legal action:** Clear statement that failure to pay will result in legal proceedings

**Interest calculation:** As per the Adjudication of Interest and Linkage Law (חוק פסיקת ריבית והצמדה), interest on business debts accrues from the invoice due date. The rate is the Bank of Israel rate plus a margin. Verify the current rate at boi.org.il.

**Delivery options:**
- Registered mail (doar rashum / דואר רשום) — provides legal proof of sending. Keep the postal receipt.
- Email with read receipt — supplementary, not a replacement for registered mail for legal purposes.

See references/legal-escalation.md for full demand letter requirements and format.

### Step 4: Track Payment Promises and Negotiate
Record and follow up on payment commitments:

- **Log payment promises:** Record the promised amount, committed payment date, and communication channel (WhatsApp, email, phone).
- **Set follow-up alerts:** Configure reminders for 1 day after the promised payment date to verify receipt.
- **Track partial payments:** Update the outstanding balance when partial payments are received. Issue a receipt/confirmation for each partial payment.
- **Maintain communication history:** Timestamp every interaction (message sent, response received, promise made, payment received). This log serves as evidence if legal action becomes necessary.
- **Negotiation support:** If the debtor requests a payment plan, help structure installments. Document the agreement in writing and have both parties confirm.

### Step 5: Evaluate Small Claims Court (Tvi'ot Ktanot) Eligibility
When a debt reaches 90+ days and collection efforts have failed, assess Small Claims Court eligibility:

**Threshold:** Up to 38,900 NIS (verify current amount at the courts website — updated periodically).

**Eligibility checklist:**
- Was proper written notice (demand letter) sent to the debtor?
- Does documentation exist for the debt? (original invoice, signed contract/PO, delivery confirmation)
- Is the amount within the Small Claims threshold?
- Has the debtor acknowledged the debt in any communication?

**Filing guide:**
- **Required documents:** Original invoice, delivery/work confirmation, copies of all demand letters sent, communication history log, postal receipts for registered mail
- **Filing fee:** Typically 1% of the claim amount, minimum approximately 80 NIS
- **Court location:** Determined by the debtor's address jurisdiction (beit mishpat l'tvi'ot ktanot)
- **Timeline:** Filing to hearing date is typically 30-60 days
- **Representation:** In Small Claims Court, parties represent themselves (no lawyers allowed)

For amounts exceeding the Small Claims threshold, the claim must go to Magistrate Court (Beit Mishpat Shalom), which requires legal representation. Recommend the user consult a lawyer.

See references/legal-escalation.md for the complete filing process.

### Step 6: Generate Aging Reports and Cash Flow Forecasts
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
5. Assess Small Claims eligibility (invoice: 22,000 NIS — under threshold)
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
- `references/legal-escalation.md` — Israeli legal framework for debt collection: demand letter (michtav hitchayvut) requirements, Small Claims Court (tvi'ot ktanot) thresholds and filing process, interest calculation rules, and registered mail documentation. Consult when preparing legal escalation in Steps 3 and 5.
- `references/reminder-templates.md` — WhatsApp and email reminder templates in Hebrew for each escalation stage (friendly, follow-up, formal, pre-legal). Templates are customizable with placeholder fields. Consult when configuring reminder messages in Step 2.

## Troubleshooting

### Error: "Reminder sent on Shabbat/holiday"
Cause: Schedule not properly configured for Jewish holidays or Shabbat times.
Solution: Verify Shabbat/holiday calendar is loaded. Shabbat starts Friday at sunset (varies by season) and ends Saturday after nightfall. Check references/legal-escalation.md for major holiday dates. Reschedule any blocked reminders to the next business day (typically Sunday).

### Error: "Small Claims threshold exceeded"
Cause: Invoice amount exceeds the Small Claims Court maximum (currently 38,900 NIS).
Solution: For amounts above the threshold, the claim must go to Magistrate Court (Beit Mishpat Shalom) which requires legal representation. Recommend the user consult a lawyer. For multiple invoices to the same debtor, consider whether they can be combined or must be filed separately.

### Error: "Demand letter delivery not confirmed"
Cause: Registered mail (doar rashum) was returned or not collected by debtor.
Solution: Registered mail has legal standing even if not collected — keep the postal receipt as proof of sending. If the debtor's address is wrong, attempt to verify through the Population Authority (Misrad HaPnim). Consider alternative delivery methods recognized by Israeli courts.

### Error: "Interest calculation disputed"
Cause: Applied incorrect interest rate or calculation method.
Solution: Israeli business debt interest follows the Adjudication of Interest and Linkage Law (חוק פסיקת ריבית והצמדה). Standard rate is the Bank of Israel rate + margin. Verify current rate at boi.org.il. For undisputed invoices, interest accrues from the due date.
