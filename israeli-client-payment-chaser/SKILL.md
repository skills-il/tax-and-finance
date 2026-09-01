---
name: israeli-client-payment-chaser
description: Chase unpaid invoices and manage debt collection for Israeli freelancers and businesses. Use when user asks about "unpaid invoices Israel", "payment reminder", "invoice aging", "debt collection freelancer", "Michtav Drisha (pre-suit demand letter)", "demand letter Hebrew", "tvi'ot ktanot", or "גביית חובות". Covers graduated WhatsApp/email reminder escalation, Hebrew demand letter generation, Small Claims Court eligibility assessment, and Shabbat/holiday-aware scheduling. Do NOT use for invoice generation (use israeli-e-invoice) or general accounting.
license: MIT
allowed-tools: Bash(python:*) WebFetch
compatibility: Works with Claude Code, OpenClaw, Cursor. OpenClaw recommended for scheduled reminder automation and WhatsApp message delivery.
---

# Israeli Client Payment Chaser

## Legal notice

This is a free information tool operated by an AI model. It explains the law and the procedure and helps you organise your own documents. All of its outputs are produced automatically by an AI model, with no involvement, review, or approval by an advocate. The output is not legal advice and not a legal opinion, but a general explanation and a template only: it does not read the full file of your matter, does not check current case law, and does not examine your specific circumstances. An AI model may err, omit data, or present a wrong conclusion.

Any text this tool drafts is an automatic draft for your personal preparation only. It is not a document prepared by an advocate and must not be relied on as evidence. This tool is not a substitute for advice that takes account of the particular circumstances and needs of each person. Before starting proceedings, signing a document, or filing with an authority or a court, consult an advocate. All use of its output is the user's sole responsibility.


## Instructions

### Step 1: Establish the Statutory Payment Deadline
Before chasing anything, fix the date the payment became legally late. This is governed by the **Payment Ethics to Suppliers Law, 5777-2017 (חוק מוסר תשלומים לספקים, תשע"ז-2017)**.

- **First check the law even applies to this client.** The Payment Ethics to Suppliers Law governs a purchaser buying in the course of business: a state body, a local authority, or a business. It does NOT supply a due date for a private consumer client. If the client is a consumer there is no statutory default to fall back on: the due date is whatever the contract says, or a reasonable time where it says nothing, and the demand letter must not assert a statutory entitlement the creditor does not have. Everything downstream in this skill (the aging buckets, the reminder schedule, the interest start date, paragraph 3 of the demand letter) inherits this answer, so settle it before anything else.
- **Default term when no payment term was agreed**, for a business, state or municipal purchaser: 45 days. Note that the clock everywhere runs from when the invoice was **submitted to the customer** (hometza), not from when the supplier issued it. For a private business (sec. 3(z)) the term is 45 days from the end of the month of submission. For a state body (sec. 3(a)) there are two ALTERNATIVE limbs and the contract decides which applies, so do not conjoin them: 45 days from submission where the period is counted from submission, or 30 days from month-end where it is counted from month-end. A local authority (sec. 3(f)(1)) pays within 45 days from the end of the month of submission. Engineering and construction contracts run longer on the same either/or pattern (85 days from submission or 70 from month-end, as applicable).
- An agreed contractual term overrides the default, but the law caps how far it can be pushed out.
- Once the statutory (or agreed) due date passes, the debt is legally late: linkage and interest attach automatically, with no need for the creditor to "declare" lateness.
- **What attaches to a late invoice** under this law is **ribit shkalit (shekel interest) from the payment due date, and dmei pigurim (late-payment fees) only from 30 days after it** (`בתוספת ריבית שקלית, ובחלוף 30 ימים מהמועד האמור - בתוספת דמי פיגורים`). The two components have different start dates, so do not describe dmei pigurim as running from the due date. Do NOT quote a self-invented percentage in a reminder or demand letter. State that statutory late-payment interest applies from the due date and that the exact rate is the statutory rate published for the current quarter, or have the user confirm the rate with their accountant. See references/legal-escalation.md.

This statutory deadline, not a generic net-30/60/90 assumption, is what the aging buckets in Step 2 should be measured against.

### Step 2: Import/Track Invoice Aging
Import outstanding invoices (from israeli-e-invoice output, if available, or manual entry) and categorize by aging buckets:

**Age every invoice from its DUE date, not its issue date.** This is the single most common error here. Under the statutory shotef+45 default an invoice issued at the very start of a month is not late until roughly 75 days after it was issued (30 to month-end plus 45), while one issued at month-end is late at about 46, so a bucket counted from the issue date fires a "you are late" reminder while the client is still well inside their lawful payment term. That damages the relationship and undercuts the demand letter later. Compute `days_late = today - due_date` using the Step 1 due date, and only then bucket:

| Bucket | Days past the DUE date | Status |
|--------|-----|--------|
| Current | not yet due | Monitor, no action needed |
| 0-day | due date reached, 0-14 days late | Friendly WhatsApp reminder |
| 15-day | 15-29 days late | Follow-up WhatsApp |
| 30-day | 30-44 days late | Formal email |
| 45+ day | 45+ days late | Pre-legal warning, then demand letter and escalation evaluation |

If the user's own contract set a shorter term than the statutory default, use theirs; the statutory term is the fallback when nothing was agreed.

Track per-client details:
- Total amount owed across all invoices
- Oldest outstanding invoice date
- Payment history (on-time vs late patterns)
- Contact details (WhatsApp number, email, mailing address)

Store tracking data in persistent memory for ongoing monitoring across sessions. If persistent memory is unavailable, export as `payment-chaser-data.json` in the working directory and reload it at the start of each session.

### Step 3: Configure Graduated Reminder Schedule
Set up a Shabbat/chagim-aware reminder escalation sequence. **Every "Day N" below counts from the DUE date established in Step 1, not from the invoice date.** **No reminders may be sent on Shabbat (Friday sunset to Saturday sunset) or Jewish holidays.** If a scheduled reminder falls on a blocked day, move it to the next business day (typically Sunday). See references/legal-escalation.md for major holiday dates.

- **Due date + 0 to 3 days, friendly WhatsApp:**
  "היי [שם], רציתי לבדוק לגבי חשבונית מספר [X] מ-[DATE] בסך [AMOUNT] ש"ח. אשמח לעדכון."

- **Due date + 15, follow-up WhatsApp:**
  "שלום [שם], תזכורת נוספת לגבי חשבונית [X]. סה"כ לתשלום: [AMOUNT] ש"ח. פרטי העברה: [BANK DETAILS]."

- **Due date + 30, formal email** with invoice copy attached and a clear payment deadline. This is also the point at which dmei pigurim start to run under the suppliers law, which is worth stating in the email.

- **Due date + 45, warning of potential legal steps:**
  "שלום [שם], למרות פניותינו הקודמות, חשבונית [X] טרם שולמה. ללא תשלום תוך 14 יום, ניאלץ לשקול צעדים נוספים."

- **Due date + 60 or more, escalation alert:** Evaluate legal options (see Step 6). Generate formal demand letter (see Step 4).

See references/reminder-templates.md for complete, customizable templates at each stage.

### Step 4: Generate Hebrew Demand Letters (Michtav Drisha (pre-suit demand letter))
Generate a formal Hebrew demand letter once the invoice is roughly 30 to 60 days past its DUE date. The letter must include:

1. **Creditor details:** Full name/business name, address, osek murshe/patur number
2. **Debtor details:** Full name/business name, address, registration number
3. **Invoice details:** Invoice number, date issued, original amount, any partial payments received
4. **Total amount due:** Including interest if applicable (see interest calculation below)
5. **Payment deadline:** Typically 14 days from letter date
6. **Warning of legal action:** Clear statement that failure to pay will result in legal proceedings

**Interest: two distinct statutes, do not conflate them.** A supplier's PRE-SUIT interest comes from the Payment Ethics to Suppliers Law: ribit shkalit from the due date, dmei pigurim only 30 days later (`בתוספת ריבית שקלית, ובחלוף 30 ימים מהמועד האמור - בתוספת דמי פיגורים`). Interest on a JUDGMENT is set by the court under the Adjudication of Interest and Linkage Law; the agent does not compute it. Neither is the Bank of Israel monetary-policy rate, and no rate is hard-coded here because it re-publishes quarterly. If the current quarter's figure is not confirmed, write `בתוספת ריבית והצמדה כדין ממועד הפירעון`, which claims the full entitlement without asserting a number. Rate source and accrual mechanics: `references/legal-escalation.md`.

**Late-payment interest is inside the VAT base.** Sec. 7 of the VAT Law defines the price of a transaction as including `ריבית או כל תשלום אחר בשל פיגור בתשלום ופיצויים בשל הפרת ההסכם כשאין עמה ביטול העסקה`, so interest an osek murshe collects is part of the taxable consideration, not a tax-free extra. The closing words matter: that assumes the breach did not cancel the transaction. Flag it so the user does not treat collected interest as clean cash.

**Delivery options:**
- Registered mail (doar rashum / דואר רשום): provides legal proof of sending. Keep the postal receipt.
- Email with read receipt: supplementary, not a replacement for registered mail for legal purposes.

See references/legal-escalation.md for full demand letter requirements and format.

### Step 5: Track Payment Promises and Negotiate
Record and follow up on payment commitments:

Record every promise with its amount, date and channel, and follow up the day after. Update the balance on each partial payment and confirm it. Timestamp every interaction: this log is the evidence if the file reaches court. If the debtor asks for a payment plan, see Step 5.5 BEFORE agreeing, because that request is the moment the debt can be converted into something enforceable.

### Step 5.5: Take the Cheap Rungs Before Court
Court is the expensive rung, and the ladder has cheaper ones that only work while the debtor still wants something from you. Try these first.

- **Convert the debt into a directly enforceable instrument while you still have leverage.** If the debtor asks for more time or a payment plan, do not simply agree by message. Ask for post-dated cheques covering the instalments, or a signed shtar chov (promissory note). Either one can be filed straight at the Enforcement Office under Step 7 with no court case at all, which removes the slowest and most expensive part of the process. A debtor negotiating for time is usually willing to sign; a debtor who has already stopped answering is not. This is the highest-value five minutes in the whole workflow.
- **Give any settlement the force of a judgment.** If you agree a reduced sum or an instalment plan, ask for it to be recorded as a psak din beheskama (consent judgment) where a case is already filed. A settlement that is only an email is just another contract you would have to sue on if it is broken.
- **Verify who you are actually dealing with before escalating.** Check the debtor at the Companies Registrar (Rasham HaChavarot) via gov.il: confirm the exact registered name and number, and whether the company is active, in liquidation, or struck off. A demand letter addressed to a trading name that is not the legal entity is worthless, and there is no point spending a filing fee on a company already in liquidation. If the counterparty turns out to be an individual or an osek rather than a company, that also changes which forum applies.
- **Retention lien (ikavon).** Where you lawfully hold something of the debtor's connected to the same transaction, a retention right may let you keep it until payment. It is fact-specific and easy to get wrong, so raise it as a question for a lawyer rather than acting unilaterally, especially where withholding work product could cause the client loss.

**If the debtor looks like they are disappearing, jump the ladder.** The sequence takes months and a judgment against an emptied company is worth nothing. If the debtor is winding down, selling up, moving money, changing entity or defaulting to other suppliers, stop escalating politely and get advice on a temporary attachment (ikul zmani), applied for with or just after the claim. It is discretionary, needs a prima facie cause, a real concern the judgment would be frustrated, and an undertaking plus security. Small Claims is a poor forum for it, itself a reason such a case belongs in Magistrate Court.

### Step 6: Evaluate Small Claims Court (Tvi'ot Ktanot) Eligibility
When a debt is well past its due date (roughly 60+ days late) and collection efforts have failed, assess Small Claims Court eligibility:

**Decide first: self-serve or involve a lawyer.** Small Claims is designed for self-representation, but recommend the user consult a lawyer instead of self-filing when any of these apply:
- The debtor genuinely disputes liability (claims the work was defective, never ordered, or already paid).
- The debtor appears insolvent or is in liquidation/insolvency proceedings (a judgment against an empty shell is worthless; a lawyer can advise on priority and timing).
- The debt is near the statute-of-limitations deadline (7 years for an ordinary debt/invoice under sec. 5(1) of the Limitation Law) and a procedural mistake could forfeit the claim entirely.
- The debtor is cross-border (outside Israel), which raises jurisdiction and enforcement questions Small Claims cannot handle.
- The amount exceeds the Small Claims threshold (must go to Magistrate Court, where representation is the norm).
Otherwise, a documented, undisputed invoice under the threshold is a good self-serve candidate.

**Threshold:** Up to 39,900 NIS (as of January 1, 2026; verify current amount at the courts administration website, updated periodically).

**Eligibility checklist:**
- Was proper written notice (demand letter) sent to the debtor? Israeli law does NOT make a pre-action demand letter a condition of filing, so a missing letter is not a bar. It is still worth sending: it fixes the date from which the debtor plainly knew of the demand, and it is evidence of the collection effort.
- Does documentation exist for the debt? (original invoice, signed contract/PO, delivery confirmation)
- **Is the claimant an individual?** Only private individuals can file here, and an osek murshe or osek patur counts as an individual. A company, partnership or amuta is barred outright (`חברה בע"מ, שותפות או עמותה לא יוכלו להגיש תביעה לבית משפט זה`) and must go to Magistrate Court whatever the amount. Ask this before anything else.
- Is the amount within the Small Claims threshold?
- How many small claims has this plaintiff already filed this year? The claim form requires declaring the number filed in the past year, and if more than five were filed in the same court that year the court **may transfer** the case to Magistrate Court. It is not a hard cap, but it changes the track.
- Has the debtor acknowledged the debt in any communication?

**Filing guide:** required documents are the original invoice, delivery or work confirmation, copies of every demand letter, the communication log, and the registered-mail receipts. The fee is 1% of the claim, minimum 50 NIS; confirm it on the courts fee page, as fees are set by regulation and change. Filing to hearing is typically 30-60 days. Venue is a CHOICE, not a rule: the claimant may generally file where the defendant resides or carries on business, and also where the undertaking was made or where it was to be performed. Do not tell a user they must travel to the debtor's city, because for a small claim that misconception is often the difference between filing and giving up. Representation is barred by default and permitted only with the court's leave, so do not say lawyers are flatly forbidden, and do not say one is required.

Above the threshold the claim goes to Magistrate Court (Beit Mishpat Shalom). Representation is NOT legally required there either, but it is strongly advisable, because full civil procedure and evidence rules apply and costs follow the event.

See references/legal-escalation.md for the complete filing process.

### Step 6.5: Check for Insolvency Before Escalating Further
This is the one place in the workflow where doing nothing forfeits the debt, so check it before spending money on a claim or an enforcement file.

If insolvency proceedings have been opened against the debtor under the Insolvency and Economic Rehabilitation Law, 5778-2018, two things change at once:

- **Individual collection stops.** Chasing the debtor directly or pressing an existing enforcement file is no longer permitted once a stay applies. Continuing to send the Step 3 reminders then is not merely futile, it is improper.
- **The creditor must file a proof of claim (tvi'at chov) with the trustee (ne'eman), within a limited window from the opening order.** Miss it and the debt is simply not counted in the distribution. Do not rely on a remembered number of months: read the current deadline off the published notice or the trustee's instructions, and diarise it the day you learn of the proceedings.

Signals worth checking before escalation: the Companies Registrar status from Step 5.5, a liquidation or stay notice, or the debtor saying they cannot pay anyone. When any of these appear, route the user to a lawyer promptly, because the deadline runs whether or not they act.

### Step 7: Open an Enforcement Office (Hotza'a LaPo'al) File to Collect
A Small Claims judgment is not money in the bank. To actually collect, the creditor must open an enforcement file with the Enforcement and Collection Authority (Rashut HaAchifa veHaGviya).

- **After a judgment:** the date for performance set IN the judgment governs. Only where the judgment sets none is the wait 30 days from the date it was given, and where the judgment was given in the debtor's absence and the creditor had to serve it, those 30 days run from service instead. Under sec. 6(b1) the registrar may also permit filing earlier, on an affidavit showing reason to believe that not opening the file would frustrate enforcement. Do not tell a creditor to wait 30 days without first reading the judgment. The creditor opens a "judgment" file (tik psak din), submits the judgment bearing the court stamp plus supporting documents, and pays an opening fee of roughly 1% of the debt plus a protocol fee. The enforcement registrar can then impose liens, garnish bank accounts and wages, and order asset seizure.
- **Bounced-check / promissory-note shortcut (skips court entirely):** A dishonored cheque (with the bank's Notice of Dishonor) or a signed promissory note can be filed directly as a "notes and cheques" file (tik shtarot ve'hamcha'ot) at the Enforcement Office, with no Small Claims judgment needed first. The debtor then has a short window to object; if they do, the matter is referred to court. Use this route when the debt is backed by such an instrument.
- **First, the warning (azhara) has to be served and its period has to run.** Nothing coercive happens before that. Enforcement files routinely stall for months precisely here, because the debtor cannot be served at the address on the file, which is another reason to have verified the debtor's registered details in Step 5.5.
- **What actually moves a debtor who HAS money.** Liens and garnishment only reach assets you can find. Beyond them, sec. 66a of the Execution Law lets the registrar impose restrictions (hagbalot), on the creditor's request or on its own initiative. The list is closed, and it is these five: barring the debtor from obtaining, holding or renewing an Israeli passport or travel document; an exit ban; designating the debtor a lakoach mugbal meyuchad under the Cheques Without Cover Law, 5741-1981 (the cheque restriction); barring use of a payment card (kartis chiyuv); and barring the debtor from founding a corporation or being a beneficial owner (baal inyan) in one.
  There is no power to restrict a driving licence, and none to stop the debtor opening bank accounts, so do not promise either. (A sixth limb once existed and is now marked deleted in the statute, which is why the belief persists.) Do not confuse the sec. 66a(3) cheque restriction with חייב מוגבל באמצעים either: that is a different declaration, which sets the debtor a monthly instalment and in practice CONSTRAINS the creditor rather than pressuring the debtor. These are also not available on demand: sec. 66b gates them, the usual route being that the debtor was brought before the registrar and shown to be able to pay yet evading, with no reasonable explanation, on a judgment debt above 500 NIS. Treat them as the endpoint of a contested file, not an opening move.
- **Ability investigation (chakirat yecholet).** Where the debtor claims they cannot pay, ask the registrar to summon them for an examination of means on oath. It tests the claim, produces the asset information liens and restrictions depend on, and is often what unlocks sec. 66b.
- Required documents: stamped judgment OR the cheque printout / signed promissory note, plus identification of the debtor and proof of the debt.

See references/legal-escalation.md for the enforcement process.

### Step 8: Generate Aging Reports and Cash Flow Forecasts
Produce a per-client aging report (by days-late bucket from Step 2, oldest invoice, total owed, month-on-month trend), a forecast weighted by each client's payment history, and a monthly summary. Score each client Reliable / Slow payer / Problematic and use that to set escalation speed rather than applying one ladder to everyone. Export PDF or CSV.

Two domain-specific points:

- **Bucket by days LATE, never by invoice age.** A report on invoice age overstates the problem and has the user chasing clients still within terms.
- **Do not forget the VAT already paid on an unpaid invoice.** An osek murshe on the ordinary (accrual) basis reports and remits VAT on an invoice in the period it was issued, so on an unpaid invoice they are out of pocket for tax on money never received. Israeli VAT practice provides a bad-debt route (chov avud) to recover it by issuing a credit note once collection has genuinely failed, and the documented collection trail this skill produces is exactly the evidence that route requires. The eligibility window and required documentation are time-bound and are NOT stated here: have the user confirm the current rules with their accountant or the VAT Authority. A separate income-tax deduction exists for a debt established as irrecoverable. Tell the user to preserve every reminder, demand letter and delivery receipt for this purpose, not only for the claim.

## Examples

### Example 1: Five overdue invoices
User says: "I have 5 unpaid invoices from the last 3 months, can you help me collect?"
Establish each invoice's DUE date first (Step 1), including whether the client is a business the suppliers law covers at all. Only then bucket by days late, which typically reveals that one or two are not actually late yet. Configure the reminder ladder from the due dates, draft the formal email for the ones around 30 days late, and prepare a demand letter for the oldest. Report the total outstanding and, separately, the total actually overdue, because those are different numbers and the user needs both.

### Example 2: Client promised to pay and did not
User says: "ABC Ltd promised to pay invoice 1234 two weeks ago but still nothing"
Pull the communication history and note the broken promise with its date. Before escalating, verify ABC Ltd at the Companies Registrar: exact registered name, number, and whether it is active or in liquidation. Then take the cheap rung first (Step 5.5): a client asking for more time is a client who will often sign post-dated cheques or a promissory note, which converts the debt into something enforceable without a court case. If that fails, draft the demand letter under Step 4 with the registered name, send it by registered mail, and assess Small Claims eligibility, checking first that the claimant is an individual or osek rather than a company.

### Example 3: Monthly collection report
User says: "Show me where I stand with all my outstanding invoices this month"
Produce the aging report bucketed by days late, a forecast weighted by each client's payment history, and the month's collection rate. Score each client Reliable / Slow payer / Problematic and use that to set escalation speed. Flag any invoice approaching the 7-year limitation period, and flag the VAT already remitted on invoices now looking irrecoverable so the user can raise the bad-debt route with their accountant.

## Bundled Resources

### References
- `references/legal-escalation.md` - Israeli legal framework for debt collection: demand letter (michtav hitraa / michtav drisha, a pre-suit demand letter) requirements, Small Claims Court (tvi'ot ktanot) thresholds and filing process, interest calculation rules, and registered mail documentation. Consult when preparing legal escalation in Steps 4 and 6.
- `references/reminder-templates.md` - WhatsApp and email reminder templates in Hebrew for each escalation stage (friendly, follow-up, formal, pre-legal). Templates are customizable with placeholder fields. Consult when configuring reminder messages in Step 3.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Accountant General quarterly rates (ribit shkalit / ribit tzmuda / dmei pigurim) | https://data.gov.il/api/3/action/datastore_search?resource_id=d1cdadd7-f6b6-40a2-aab9-73230d5fe294 | THE source for the statutory late-payment rate. Read the row whose `ineffecfrom` covers your period |
| Bank of Israel - interest rates | https://www.boi.org.il/information/interestrates/primerates/ | Monetary-policy rate ONLY. This is NOT the statutory late-payment rate; never quote it as such |
| Courts Administration - Small Claims service page | https://www.gov.il/he/service/filing_a_small_claim | Current threshold, filing process, jurisdiction rules |
| Kol-Zchut - Filing a small claim (Hebrew) | https://www.kolzchut.org.il/he/הגשת_תביעה_קטנה | Plain-language eligibility and procedure guide |
| Nevo - Adjudication of Interest and Linkage Law (text) | https://www.nevo.co.il/law_html/law00/75001.htm | Full statutory text on court-adjudicated interest and linkage |
| Nevo - Payment Ethics to Suppliers Law, 5777-2017 | https://www.nevo.co.il/law_html/law00/144599.htm | Statutory 45-day default payment term and late-payment interest |
| Kol-Zchut - Payment deadline to suppliers | https://www.kolzchut.org.il/he/המועד_האחרון_לתשלום_תמורה_לספקים_עבור_סחורה_או_שירות | Plain-language guide to the 45-day rule by purchaser type |
| Enforcement Authority - judgment enforcement file | https://www.gov.il/he/departments/law_enforcement_and_collection_system_authority | Opening a Hotza'a LaPo'al file, fees, required documents |
| Enforcement Authority - cheques and notes file | https://www.gov.il/he/departments/law_enforcement_and_collection_system_authority | Filing a dishonored cheque or promissory note directly |
| Israel Post - Registered mail service | https://www.israelpost.co.il | Registered mail (doar rashum) service and pricing |
| HebCal - Jewish calendar | https://www.hebcal.com | Shabbat times and holiday dates for reminder scheduling |

## Recommended MCP Servers

| MCP Server | Why |
|------------|-----|
| `hebcal` | Step 3 (graduated reminder scheduling) and the Troubleshooting "Reminder sent on Shabbat/holiday" case both depend on Shabbat and chag-aware scheduling. Use it to resolve Shabbat entry/exit times and holiday dates so reminders never fire on a blocked day. |
| `israel-law` / `kolzchut` | Optional. Look up the current text of the Payment Ethics to Suppliers Law, Small Claims procedure, and enforcement rules instead of relying on cached figures. |

## Gotchas
- **Shotef is not net-N.** "Shotef + 30" means the end of the current month plus 30 days, not 30 days from the invoice date. Agents routinely compute the due date as if it were net-30 and then chase a client who is not yet late.
- **Age from the due date, not the invoice date.** Every bucket, reminder and letter in this skill keys off the Step 1 due date. An agent that reverts to invoice age will send a late notice while the client is still within terms.
- **Do not conflate the two interest statutes, and never quote the BoI rate.** A supplier's pre-suit interest comes from the Payment Ethics to Suppliers Law (ribit shkalit from the due date, dmei pigurim 30 days later); a court sets judgment interest under the Adjudication of Interest and Linkage Law. The Bank of Israel monetary-policy rate is neither. When the current quarter's rate is not confirmed, write `בתוספת ריבית והצמדה כדין ממועד הפירעון` and assert no number.
- **Winning is not collecting.** A judgment does nothing until an enforcement file is opened, which cannot happen until 30 days after judgment, and nothing coercive happens there until the warning is served. Agents stop at "you won".
- **A 7-year limitation period, not 3.** An ordinary debt or unpaid invoice runs 7 years (sec. 5(1) of the Limitation Law, `בשאינו מקרקעין - שבע שנים`); a judgment runs 25 (sec. 21), and a debt in an open enforcement file does not lapse at 7. Telling a user a commercial invoice is time-barred at 3 years abandons a collectable debt.
- **Hebrew is a practical norm here, not an evidentiary rule.** Write to Hebrew-speaking clients in Hebrew because that is what gets processed, but foreign-language documents are admissible; the court may simply require a certified translation. Keep both versions rather than discarding English correspondence.

## Troubleshooting

### Error: "Reminder sent on Shabbat/holiday"
Cause: the Shabbat and chag calendar was not loaded.
Solution: Shabbat runs Friday sunset to Saturday nightfall and varies by season and location. See references/legal-escalation.md for holiday dates, and move any blocked reminder to the next business day (usually Sunday).

### Error: "Small Claims threshold exceeded"
Cause: Invoice amount exceeds the Small Claims Court maximum (currently 39,900 NIS).
Solution: For amounts above the threshold, the claim must go to Magistrate Court (Beit Mishpat Shalom). A lawyer is not legally required there, but is strongly advisable. Recommend the user consult a lawyer. For multiple invoices to the same debtor, consider whether they can be combined or must be filed separately.

### Error: "Demand letter delivery not confirmed"
Cause: registered mail was returned or not collected.
Solution: keep the postal receipt; it evidences dispatch, which is what fixes the deadline's start date. If the address is wrong, re-check the debtor's registered details (Step 5.5) before re-sending.

### Error: "Interest calculation disputed"
Cause: Applied the wrong interest rate or conflated the two statutes.
Solution: separate the two statutes as set out in Step 4, and if the current quarter's rate is not confirmed, fall back to `בתוספת ריבית והצמדה כדין ממועד הפירעון` rather than a figure.
