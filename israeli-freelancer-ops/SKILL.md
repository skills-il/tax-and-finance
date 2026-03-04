---
name: israeli-freelancer-ops
description: >-
  Manage daily operations for Israeli freelancers (osek murshe, osek patur) —
  invoice aging, utility bill collection, tax deadline reminders, and accountant
  packages. Use when user asks about "freelancer operations", "osek murshe
  workflow", "osek patur tracking", "invoice aging", "accountant package",
  "freelancer tax deadlines", "utility bills collection", or "חבילה לרואה
  חשבון". Covers VAT filing deadline alerts, Bituach Leumi payment tracking,
  osek patur threshold monitoring, and organized monthly accounting exports.
  Do NOT use for invoice generation (use israeli-e-invoice), VAT reporting
  (use israeli-vat-reporting), or payroll calculation.
license: MIT
allowed-tools: "Bash(python:*) WebFetch"
compatibility: >-
  Works with Claude Code, OpenClaw, Cursor. OpenClaw recommended for scheduled
  deadline alerts and browser-based utility bill collection.
metadata:
  author: skills-il
  version: 1.0.0
  category: tax-and-finance
  tags:
    he:
      - עצמאי
      - מיסים
      - מע״מ
      - עוסק-מורשה
      - עוסק-פטור
      - חשבונאות
      - ישראל
    en:
      - freelancer
      - tax
      - vat
      - osek-murshe
      - osek-patur
      - accounting
      - israel
  display_name:
    he: ניהול תפעול לפרילנסר ישראלי
    en: Israeli Freelancer Operations
  display_description:
    he: >-
      ניהול תפעול יומיומי לפרילנסרים ועוסקים מורשים בישראל — מעקב חשבוניות,
      גביית חשבונות שירות, תזכורות מועדי דיווח, וחבילה לרואה חשבון
    en: >-
      Manage daily operations for Israeli freelancers (osek murshe, osek patur) —
      invoice aging, utility bill collection, tax deadline reminders, and accountant
      packages.
  openclaw:
    requires:
      bins: []
      env: []
    emoji: "📋"
---

# Israeli Freelancer Operations

## Instructions

### Step 1: Assess Freelancer Profile
Determine the user's business type and tax obligations:

- **Osek Murshe (עוסק מורשה):** Authorized dealer, registered for VAT. Must file VAT returns, issue tax invoices (hashbonit mas), and can deduct input VAT (mas tsumos).
- **Osek Patur (עוסק פטור):** Exempt dealer, under revenue threshold. Issues receipts (kabala) only, does not charge or report VAT.

Key profile details to collect:
- Business type (osek murshe / osek patur)
- VAT filing frequency: bi-monthly (standard) or monthly (large businesses exceeding the monthly-filing threshold)
- Industry: tech consulting, design, trades, content creation, etc.
- Accountant details: name, preferred package format, submission schedule
- Current revenue tracking: year-to-date income, number of active clients

Store the freelancer profile in persistent memory for ongoing tracking across sessions. If persistent memory is unavailable, export the profile as `freelancer-profile.json` in the working directory and reload it at the start of each session.

### Step 2: Set Up Invoice Aging Tracker
Track all issued invoices by payment status using aging buckets:

| Bucket | Age | Action |
|--------|-----|--------|
| Current | 0-29 days | Monitor, no action needed |
| 30-day | 30-59 days | Friendly WhatsApp reminder |
| 60-day | 60-89 days | Formal email follow-up |
| 90+ day | 90+ days | Alert for escalation |

Configure graduated reminder schedule:
- **Day 30:** Friendly WhatsApp message — "היי, רציתי לבדוק לגבי חשבונית מספר [X] מתאריך [DATE]. אשמח לעדכון על מועד התשלום."
- **Day 60:** Formal email follow-up with invoice copy attached, payment details (bank transfer info), and a clear due date.
- **Day 90+:** Alert the freelancer for escalation consideration. Suggest using the israeli-client-payment-chaser skill for structured collection (if available).

Additional tracking:
- Record partial payments and update outstanding balances accordingly
- Link to israeli-e-invoice for generating new invoices or credit notes
- Maintain running totals: total outstanding, total overdue, by client

### Step 3: Configure Utility Bill Collection
Use browser automation (CDP) to collect monthly bills from Israeli utility portals:

| Provider | Portal | Bill Type |
|----------|--------|-----------|
| Israel Electric Corporation (חברת החשמל) | iec.co.il | Electricity |
| Bezeq | bezeq.co.il | Landline/internet |
| Partner Communications | partner.co.il | Mobile/internet |
| HOT Telecom | hot.net.il | Cable/internet |
| Municipal water corporation | Varies by city | Water |
| Arnona (municipal tax) | Municipality-specific portals | Property tax |

For each provider:
1. Navigate to the provider's bill/invoice section using stored credentials
2. Download the latest PDF bill
3. Extract key details: billing period, amount due, due date, payment status
4. Organize downloaded files by month and category into the accountant package folder

Handle 2FA/OTP: If a portal requires SMS verification, pause browser automation and prompt the user for the OTP code. See references/utility-portals.md for portal-specific notes.

### Step 4: Set Deadline Calendar
Configure proactive alerts for Israeli tax deadlines:

| Deadline | Frequency | Date | Details |
|----------|-----------|------|---------|
| VAT filing (osek murshe) | Bi-monthly | 15th of the month after the period | Deadlines: Mar 15, May 15, Jul 15, Sep 15, Nov 15, Jan 15 |
| VAT filing (monthly filers) | Monthly | 15th of each month | For businesses exceeding the monthly threshold |
| Bituach Leumi (self-employed) | Quarterly | 15th of Jan, Apr, Jul, Oct | National Insurance advance payments |
| Annual tax report (doch shnati) | Yearly | By March 31 | Extensions possible via accountant |
| Advance tax payments (mkdamot) | Bi-monthly | 15th of the month after the period | If applicable per Tax Authority assessment |

Reminder schedule for each deadline:
- **7 days before:** First alert via WhatsApp/Telegram with what to prepare
- **3 days before:** Second alert with checklist of required documents
- **Deadline day:** Final reminder with filing links and instructions

If a deadline falls on Shabbat (Saturday), it moves to Sunday. If it falls on a Jewish holiday (chag), check references/deadline-calendar.md for adjusted dates.

Include per-deadline preparation notes:
- VAT filing: have all sales and purchase invoices ready, calculate net VAT (output minus input)
- Bituach Leumi: verify quarterly advance amount from latest assessment
- Annual report: coordinate with accountant, ensure all monthly packages delivered
- Mkdamot: check assessment letter for payment coupon amounts

### Step 5: Monitor Osek Patur Threshold
Track cumulative annual revenue against the osek patur threshold:

- **Current threshold:** approximately 120,000 NIS annually (verify at misim.gov.il as this is adjusted periodically for inflation)
- **Alert levels:**
  - **70% (~84,000 NIS):** Informational — "You've reached 70% of the annual threshold. Consider planning for potential transition."
  - **85% (~102,000 NIS):** Warning — "Approaching threshold. Review implications of converting to osek murshe."
  - **95% (~114,000 NIS):** Urgent — "Very close to threshold. Conversion may be required soon."

When the threshold is reached or projected to be exceeded, explain the implications:
- Must register as osek murshe with the Tax Authority
- Must start charging VAT (18%) on all invoices
- Must issue hashbonit mas (tax invoice) instead of kabala (receipt)
- Can now deduct input VAT (mas tsumos) on business expenses
- Must file bi-monthly VAT returns
- Bituach Leumi payments may increase

Generate a transition checklist:
1. Register as osek murshe at the local Tax Authority office (misrad mas hachnasa)
2. Update invoicing system to issue tax invoices with VAT
3. Notify clients of new invoicing format
4. Set up VAT filing schedule (see Step 4)
5. Begin tracking input VAT on business expenses for deductions
6. Consult accountant on transition timing and implications

### Step 6: Generate Accountant Package (Havila L'Roe Cheshbon)
Compile an organized monthly or quarterly package for the accountant:

**Package contents:**
1. **Issued invoices** — All invoices/receipts issued during the period, sorted by date
2. **Received invoices/receipts** — All expense documents (business purchases, subscriptions, equipment)
3. **Bank statement summary** — Transaction list matched to invoices where possible
4. **Utility bills** — Bills collected in Step 3, organized by provider
5. **Revenue summary** — Running annual total with monthly breakdown
6. **Cover sheet** — Summary page with key numbers

**Cover sheet fields:**
- Period covered (month/quarter/year)
- Total revenue (bruto)
- Total expenses
- Net income (neto)
- VAT collected (for osek murshe)
- VAT paid on expenses (mas tsumos, for osek murshe)
- Net VAT payable/refundable
- Running annual revenue total
- Number of invoices issued / received

**Export format:**
- Organized folder structure: `YYYY-MM/invoices-issued/`, `YYYY-MM/invoices-received/`, `YYYY-MM/utility-bills/`, `YYYY-MM/bank-statements/`
- Or as a single ZIP file with the same structure
- Cover sheet as PDF or CSV at the root of the package

Cross-reference with related skills:
- Use israeli-e-invoice for generating any missing invoices (if available)
- Use israeli-vat-reporting for VAT return preparation (if available)
- Use israeli-bank-connector for pulling bank transaction data (if available)

## Examples

### Example 1: Freelancer Tracking Invoices Across Aging Buckets
User says: "I have 5 outstanding invoices for my web dev consulting, some are getting old"
Actions:
1. Request invoice list with amounts, issue dates, and client names
2. Categorize each invoice into aging buckets (current, 30-day, 60-day, 90+)
3. Set up WhatsApp reminder schedule for overdue invoices (30+ days)
4. Generate an aging report showing total outstanding by bucket and by client
Result: Organized aging dashboard with 2 invoices current, 1 at 30-day (WhatsApp reminder queued), 1 at 60-day (email follow-up sent), and 1 at 90+ (escalation alert flagged). Automated follow-up reminders configured for all overdue invoices.

### Example 2: Developer Approaching Osek Patur Threshold
User says: "I'm osek patur and I think I'm getting close to the limit this year"
Actions:
1. Request current year's revenue total and number of remaining months
2. Calculate projection based on average monthly income so far
3. Compare against current threshold (~120,000 NIS)
4. Result: at 87% of threshold (104,400 NIS earned) with 3 months remaining
5. Average monthly income of ~11,600 NIS projects annual total of ~139,200 NIS, exceeding threshold by ~19,200 NIS
6. Prepare transition checklist: VAT registration, invoice type changes, expense VAT deductions
Result: Threshold status report showing projection will exceed the limit. Clear breakdown of what changes when converting to osek murshe, with step-by-step transition checklist and recommendation to consult accountant before crossing the threshold.

### Example 3: Preparing Year-End Package for Accountant
User says: "My accountant needs everything organized for the annual report"
Actions:
1. Compile all issued invoices from the year, sorted chronologically
2. Collect expense receipts and match against bank statement entries
3. Run utility bill collection (Step 3) to gather any missed bills
4. Generate revenue/expense summary with monthly breakdown and annual totals
5. Create cover sheet: total revenue, total expenses, net income, VAT collected, VAT paid
6. Package everything into organized folder structure with cover sheet
Result: Complete accountant package (havila l'roe cheshbon) with 12 monthly folders, each containing issued invoices, expense receipts, and utility bills. Cover sheet shows annual revenue of 185,000 NIS, expenses of 42,000 NIS, net of 143,000 NIS, with VAT summary. Ready for handoff as ZIP file.

## Bundled Resources

### References
- `references/deadline-calendar.md` — Complete Israeli tax deadline calendar for freelancers: VAT filing dates, Bituach Leumi quarterly payments, annual report deadlines, and advance tax payment (mkdamot) schedule. Includes both osek murshe and osek patur timelines, plus holiday adjustments. Consult when setting up deadline alerts in Step 4.
- `references/utility-portals.md` — Login URLs, bill download paths, and automation notes for Israeli utility providers (IEC, Bezeq, HOT, Partner, water corporations, Arnona portals). Includes 2FA/OTP handling guidance per portal. Consult when configuring browser-based bill collection in Step 3.

## Troubleshooting

### Error: "Utility portal login failed"
Cause: Israeli utility portals frequently update their login flows or require 2FA (SMS verification).
Solution: Check if the portal requires SMS OTP. If so, configure browser automation to pause for user input during 2FA. Verify credentials are current and the portal URL hasn't changed. See references/utility-portals.md for portal-specific notes.

### Error: "VAT filing deadline incorrect"
Cause: Using wrong filing frequency (bi-monthly vs monthly) for the business type.
Solution: Verify filing frequency in the freelancer profile (Step 1). Osek murshe with annual revenue under the monthly-filing threshold files bi-monthly on the 15th of odd months. Businesses above the threshold file monthly. See references/deadline-calendar.md for the complete schedule.

### Error: "Osek patur threshold outdated"
Cause: The threshold amount changes periodically (adjusted for inflation by the Tax Authority).
Solution: Verify the current threshold at the Tax Authority website (misim.gov.il). The threshold is adjusted periodically for inflation — check for the latest published amount. Update the threshold in the freelancer profile when a new amount is published.

### Error: "Accountant package missing documents"
Cause: Not all expense receipts were tracked during the period, or utility bills were not collected.
Solution: Run utility bill collection (Step 3) to catch any missed bills. Cross-reference the bank statement against tracked expenses to identify gaps. Check for recurring expenses (subscriptions, rent, insurance) that may not have corresponding receipts.
