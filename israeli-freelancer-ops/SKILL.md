---
name: israeli-freelancer-ops
description: Manage daily operations for Israeli freelancers (osek murshe, osek patur) - invoice aging with collection reminders, utility bill collection via browser automation, tax deadline alerts (VAT, Bituach Leumi, mkdamot, annual report), osek patur threshold monitoring, and organized accountant packages (havila). Use when a freelancer needs help tracking invoices, preparing documents for their accountant, monitoring their osek patur revenue ceiling, or staying on top of Israeli tax filing deadlines. Prevents missed VAT filings (which trigger automatic penalties), forgotten invoice follow-ups, and disorganized handoffs to accountants. Do NOT use for VAT return preparation (use israeli-vat-reporting), e-invoice generation (use israeli-e-invoice), or payroll/employee management.
license: MIT
---

# Israeli Freelancer Operations

## Instructions

### Step 1: Assess Freelancer Profile
Determine the user's business type and tax obligations:

- **Osek Murshe (עוסק מורשה):** Authorized dealer, registered for VAT. Must file VAT returns, issue tax invoices (hashbonit mas), and can deduct input VAT (mas tsumos).
- **Osek Patur (עוסק פטור):** Exempt dealer, under revenue threshold (122,833 NIS for 2026, CPI-indexed; was 120,000 NIS in both 2024 and 2025). Issues receipts (kabala) only, does not charge or report VAT.
- **Esek Za'ir (עסק זעיר):** Micro business track introduced in 2024 (Income Tax Ordinance Section 87ב, added by Amendment 277). Freelancers under the osek patur threshold can register as esek za'ir to receive a 30% normative expense deduction (no receipts needed) and simplified reporting (exempt from the annual income-tax report in most cases). Eligibility caveats to verify with the user: cannot be a former employee of the client receiving the invoice, and no more than 25% of annual revenue may come from a single related party or former employer. The threshold is shared with osek patur and is CPI-indexed from 2026 (122,833 NIS).

Key profile details to collect:
- Business type (osek murshe / osek patur / esek za'ir)
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
- **Day 30:** Friendly WhatsApp message: "היי, רציתי לבדוק לגבי חשבונית מספר [X] מתאריך [DATE]. אשמח לעדכון על מועד התשלום."
- **Day 60:** Formal email follow-up with invoice copy attached, payment details (bank transfer info), and a clear due date.
- **Day 90+:** Alert the freelancer for escalation consideration. Suggest using the israeli-client-payment-chaser skill for structured collection (if available).

**Israel Invoice allocation numbers (from 2026):** For osek murshe, tax invoices (hashbonit mas) exceeding 10,000 NIS (before VAT) must include an allocation number (mispar haktza'a) obtained from the Tax Authority system. From June 2026 this threshold drops to 5,000 NIS. Without an allocation number, the recipient cannot deduct input VAT. When tracking invoices, flag any issued invoice above the threshold that is missing an allocation number.

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
| Bituach Leumi (self-employed) | Monthly | 15th of each month | National Insurance advance payments |
| Annual tax report (doch shnati) | Yearly | Paper: May 31. Online: June 30 | Tax year 2025 filed in 2026. Online filing is mandatory for most filers. Accountant extensions push to July 31 or later. Do not confuse with the osek patur annual turnover declaration (Jan 31). |
| Advance tax payments (mkdamot) | Monthly or bi-monthly | 15th of the month after the period (19th if paid online via the Tax Authority website, by 18:30) | Frequency set by Tax Authority assessment letter; bi-monthly requires prior approval |
| Osek patur annual declaration | Yearly | January 31 | Report previous year's turnover to VAT office |
| Self-employed pension deposit (Section 45א + 47) | Yearly | **December 31** | Last day to deposit into a pension fund, kupat gemel, or polisat bituach for that tax year's benefits. Section 45א gives a **35 percent tax credit** on contributions up to a combined 5.5 percent of business income (5 percent + an additional 0.5 percent slice; 2026 cap ≈ 11,640 NIS + 1,164 NIS). Section 47 gives an **income deduction** of up to 11 percent of qualifying income (2026 qualifying-income ceiling 232,800 NIS, max deposit ≈ 25,608 NIS for a preferred member). Missing Dec 31 forfeits both benefits for the year. |
| Mandatory self-employed pension contribution | Yearly | December 31 | Separate from 45א/47 credits. 2026 rates: 4.45 percent on income up to half the average wage and 12.55 percent above it (average wage 13,769 NIS/month). Annual employer-equivalent caps for 2026: 3,676 NIS on the lower bracket, 14,044 NIS on the upper. The mandatory deposit is a legal obligation, not just a tax benefit. |

**Detailed VAT reporting (from 2026):** Osek murshe businesses with annual turnover exceeding 500,000 NIS must now file detailed VAT reports (doch meforat, report 874) listing each invoice individually. This also forces a switch from bi-monthly to monthly filing, and the filing deadline changes from the 15th to the **23rd** of the following month. Ask the user about their annual turnover to determine if this applies.

Reminder schedule for each deadline:
- **7 days before:** First alert via WhatsApp/Telegram with what to prepare
- **3 days before:** Second alert with checklist of required documents
- **Deadline day:** Final reminder with filing links and instructions

If a deadline falls on Shabbat (Saturday), it moves to Sunday. If it falls on a Jewish holiday (chag), check references/deadline-calendar.md for adjusted dates.

Include per-deadline preparation notes:
- VAT filing: have all sales and purchase invoices ready, calculate net VAT (output minus input)
- Bituach Leumi: verify monthly advance amount from latest assessment. Direct-debit payers (הוראת קבע) get an automatic extension to the 22nd. 2026 brackets for self-employed (BTL circular 1502): minimum monthly advance 265 NIS, maximum 8,550 NIS, minimum income floor 3,442 NIS per month.
- Annual report: coordinate with accountant, ensure all monthly packages delivered. For tax year 2025 filed in 2026: paper deadline May 31, online deadline June 30. Online filing is mandatory for most filers. Accountant extensions can push later.
- Mkdamot: check assessment letter for payment coupon amounts. Payments are due by the 15th of the month after the period; paying online via the Tax Authority website extends the deadline to the 19th (until 18:30). Bi-monthly payment requires prior approval in the mkdamot book.
- Pension deposit (Dec 31): alert by **December 15** with the year's business income to date and current 45א/47 ceilings. Confirm both the **tax-benefit** deposit (5.5 percent combined for the 45א credit; up to 11 percent for the Section 47 deduction) and the **mandatory** deposit (4.45 percent below half-average-wage, 12.55 percent above). Missing Dec 31 forfeits the tax benefits for the whole year; insufficient mandatory deposit is a separate legal exposure.

### Step 5: Monitor Osek Patur Threshold
Track cumulative annual revenue against the osek patur threshold:

- **Current threshold (2026):** 122,833 NIS annually (verify at misim.gov.il as this is adjusted periodically for inflation; was 120,000 NIS in 2024-2025)
- **Alert levels:**
  - **70% (~86,000 NIS):** Informational. "You've reached 70% of the annual threshold. Consider planning for potential transition."
  - **85% (~104,400 NIS):** Warning. "Approaching threshold. Review implications of converting to osek murshe."
  - **95% (~116,700 NIS):** Urgent. "Very close to threshold. Conversion may be required soon."

When the threshold is reached or projected to be exceeded, explain the implications:
- Must register as osek murshe with the Tax Authority
- Must start charging VAT (18%) on all invoices
- Must issue hashbonit mas (tax invoice) instead of kabala (receipt)
- Can now deduct input VAT (mas tsumos) on business expenses
- Must file bi-monthly VAT returns
- Bituach Leumi payments may increase

**Esek za'ir alternative:** If the user is approaching the threshold but expects income to stay near it, mention the esek za'ir (micro business) track. Esek za'ir offers a 30% normative expense deduction and simplified reporting, but shares the same revenue ceiling as osek patur (122,833 NIS for 2026). It does not defer the obligation to convert to osek murshe if the threshold is exceeded.

Generate a transition checklist:
1. Register as osek murshe at the local Tax Authority office (misrad mas hachnasa)
2. Update invoicing system to issue tax invoices with VAT
3. Register for the Israel Invoice allocation number system (required for invoices over 10,000 NIS)
4. Notify clients of new invoicing format
5. Set up VAT filing schedule (see Step 4)
6. Begin tracking input VAT on business expenses for deductions
7. Consult accountant on transition timing and implications

### Step 6: Generate Accountant Package (Havila L'Roe Cheshbon)
Compile an organized monthly or quarterly package for the accountant:

**Package contents:**
1. **Issued invoices:** All invoices/receipts issued during the period, sorted by date
2. **Received invoices/receipts:** All expense documents (business purchases, subscriptions, equipment)
3. **Bank statement summary:** Transaction list matched to invoices where possible
4. **Utility bills:** Bills collected in Step 3, organized by provider
5. **Revenue summary:** Running annual total with monthly breakdown
6. **Cover sheet:** Summary page with key numbers

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
3. Compare against current threshold (122,833 NIS for 2026)
4. Result: at 85% of threshold (104,400 NIS earned) with 3 months remaining
5. Average monthly income of ~11,600 NIS projects annual total of ~139,200 NIS, exceeding threshold by ~16,400 NIS
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
- `references/deadline-calendar.md`: Complete Israeli tax deadline calendar for freelancers: VAT filing dates, Bituach Leumi monthly payments, annual report deadlines, and advance tax payment (mkdamot) schedule. Includes both osek murshe and osek patur timelines, plus holiday adjustments. Consult when setting up deadline alerts in Step 4.
- `references/utility-portals.md`: Login URLs, bill download paths, and automation notes for Israeli utility providers (IEC, Bezeq, HOT, Partner, water corporations, Arnona portals). Includes 2FA/OTP handling guidance per portal. Consult when configuring browser-based bill collection in Step 3.

## Gotchas
- Agents may confuse Osek Murshe (licensed dealer, charges VAT) with Osek Patur (exempt dealer, no VAT). The threshold for Osek Patur is 122,833 NIS for 2026 (was 120,000 NIS in 2024-2025, adjusted for inflation). Exceeding it mid-year requires immediate registration upgrade.
- Israeli freelancers must file bi-monthly VAT reports (doch du-chodshi) even in zero-revenue periods. Agents may skip months with no income, but a missing report triggers penalties.
- Bituach Leumi advance payments (mikdamot) for self-employed are based on projected annual income, not actual monthly revenue. Agents may calculate contributions based on current month earnings.
- Invoice numbering in Israel must be sequential with no gaps. Agents may suggest starting from an arbitrary number or allowing gaps, which violates Tax Authority requirements.
- From 2026, osek murshe must obtain an allocation number (mispar haktza'a) for tax invoices exceeding 10,000 NIS (dropping to 5,000 NIS from June 2026). Agents may generate invoices without this number, causing the recipient to lose their input VAT deduction.
- Agents may not distinguish between esek za'ir (micro business) and standard osek patur. Esek za'ir gets a 30% normative expense deduction and simplified reporting, but shares the same revenue ceiling. Recommending esek za'ir benefits to a standard osek patur (or vice versa) causes confusion.
- Agents may quote the wrong annual-report deadline. **April 30 is NOT the annual income-tax report deadline** -- that date is for the osek patur annual turnover declaration. The income-tax annual report (Form 1301) is due May 31 (paper) or June 30 (online) for tax year 2025 filed in 2026.
- Agents may treat the 35 percent Section 45א credit and the mandatory self-employed pension contribution as the same obligation. They are separate: 45א/47 are voluntary deposits that earn tax benefits; the mandatory contribution is a legal floor under the Self-Employed Pension Law.

## Reference Links

Use these official sources to verify time-sensitive figures before quoting them to the user. Israeli tax and Bituach Leumi tables update at least annually; allocation-number thresholds change mid-year.

| Source | URL | What to Check |
|--------|-----|---------------|
| Tax Authority - Form 1301 / annual income-tax report | https://www.gov.il/he/service/reporting-and-payment-2025-annual-tax-report-for-individuals | Current-year deadlines for paper and online filing |
| Tax Authority - PCN 874 / detailed VAT reporting | https://www.gov.il/he/pages/pa280825-1 | 500,000 NIS turnover threshold, 23rd-of-month deadline |
| Tax Authority - Allocation numbers (mispar haktza'a) | https://www.gov.il/he/service/request-assignment-number-for-tax-invoice | Current invoice threshold (10,000 NIS, dropping to 5,000 NIS on June 1, 2026) |
| Kol Zchut - Osek Patur | https://www.kolzchut.org.il/he/עוסק_פטור | Current threshold, conversion rules |
| Kol Zchut - Esek Za'ir | https://www.kolzchut.org.il/he/עסק_זעיר | 30 percent normative deduction, eligibility caveats |
| Kol Zchut - Pension contribution tax credit (Section 45א) | https://www.kolzchut.org.il/he/זיכוי_ממס_הכנסה_בגין_הפרשות_לביטוח_פנסיוני | Current-year ceilings and 5%+0.5% structure |
| Bituach Leumi - Self-employed rates | https://www.btl.gov.il/Insurance/National%20Insurance/type_list/Self_Employed/Pages/rates.aspx | Current advance bracket min/max and floor |

## Troubleshooting

### Error: "Utility portal login failed"
Cause: Israeli utility portals frequently update their login flows or require 2FA (SMS verification).
Solution: Check if the portal requires SMS OTP. If so, configure browser automation to pause for user input during 2FA. Verify credentials are current and the portal URL hasn't changed. See references/utility-portals.md for portal-specific notes.

### Error: "VAT filing deadline incorrect"
Cause: Using wrong filing frequency (bi-monthly vs monthly) for the business type.
Solution: Verify filing frequency in the freelancer profile (Step 1). Osek murshe with annual revenue under the monthly-filing threshold files bi-monthly on the 15th of odd months. Businesses above the threshold file monthly. See references/deadline-calendar.md for the complete schedule.

### Error: "Osek patur threshold outdated"
Cause: The threshold amount changes periodically (adjusted for inflation by the Tax Authority).
Solution: Verify the current threshold at the Tax Authority website (misim.gov.il) or the Kol Zchut osek patur page (see Reference Links). For 2026, the threshold is 122,833 NIS (CPI-indexed). Update the threshold in the freelancer profile when a new amount is published.

### Error: "Annual report due April 30"
Cause: Confusing the income-tax annual report (Form 1301) with the osek patur annual turnover declaration to the VAT office.
Solution: The osek patur turnover declaration is due January 31. The income-tax annual report (Form 1301) for tax year 2025 filed in 2026 is due May 31 on paper or June 30 online. Online filing is mandatory for most filers; accountant extensions can extend further. Verify the current year's exact dates on the Tax Authority Form 1301 service page (see Reference Links).

### Error: "Accountant package missing documents"
Cause: Not all expense receipts were tracked during the period, or utility bills were not collected.
Solution: Run utility bill collection (Step 3) to catch any missed bills. Cross-reference the bank statement against tracked expenses to identify gaps. Check for recurring expenses (subscriptions, rent, insurance) that may not have corresponding receipts.
