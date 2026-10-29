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

- **First check the law even applies to this client.** It governs a state body, a local authority, a budgeted or statutory body (sec. 3(e)(1)), and a business, which the law defines by VAT status (`מוסד כספי, עוסק מורשה או עוסק פטור`), so check the client is VAT-registered rather than assuming. It does NOT supply a due date for a private consumer. Against a consumer the due date is what the contract says; where it is silent, a reasonable time after contracting, on a date the creditor notified a reasonable time in advance (Contracts (General Part) Law sec. 41). So the first written request to a consumer must name a dated deadline, and nothing may call them late before it. The demand letter must not assert a statutory entitlement the creditor does not have. Interest against a consumer is for the court, and by default runs only from the day the claim is filed (sec. 2(b) of the Adjudication of Interest and Linkage Law), so waiting gains the creditor nothing. Everything downstream inherits this answer, so settle it first.
- **Default term when no payment term was agreed**, for a business, state or municipal purchaser: 45 days. The clock runs from when the invoice was **submitted to the customer** (hometza), not from when the supplier issued it. For a private business (sec. 3(z)) the term is 45 days from the end of the month of submission. A local authority (sec. 3(f)(1)) also pays within 45 days from the end of the month of submission. A budgeted or statutory body has its own month-end term (sec. 3(e)(1)), but sec. 10(a) may apply the state-body terms to it, so check the contract. A state body (sec. 3(a)) has two ALTERNATIVE limbs and the contract decides which applies, so do not conjoin them: 45 days from submission, or 30 days from month-end. Construction contracts, a municipality's externally funded share, and other special cases: `references/legal-escalation.md`.
- **Keep proof of submission, because the due date hangs on it.** Sec. 3(i) lists what counts, including registered mail with delivery confirmation and an electronic message with an electronic delivery confirmation; a plain email may not be enough. A purchaser may return an invoice missing a material detail, listing the defects, and it is then treated as never submitted (sec. 3(h)(1)). That resets the clock only for a return within the review period (23 business days for most clients); a later return instead gives the client 10 business days beyond the original due date, not counting the time until the corrected invoice arrives (sec. 3(h)(2)).
- **Use the contract's express payment term, shorter or longer.** Against a private business a later date must be set expressly and is valid only if the special nature of the engagement requires it or it is not exceptionally unfair (sec. 3(z)); the law cannot be contracted out of except in the supplier's favour (sec. 7). Whether a long term fails that test is a lawyer's call, so never chase, or claim interest, ahead of the agreed date.
- Once the statutory (or agreed) due date passes, the debt is legally late, with no need for the creditor to "declare" lateness.
- **What attaches to a late invoice** under this law is **ribit shkalit (shekel interest) from the due date, and dmei pigurim (late-payment fees) only from 30 days after it** (`בתוספת ריבית שקלית, ובחלוף 30 ימים מהמועד האמור - בתוספת דמי פיגורים`). This law attaches no linkage (hatzmada). **Against a private business or a sec. 3(e)(1) body it applies only where the client had the advantage in shaping the contract terms** (sec. 4(b): `רק בהתקשרות שבה היתה לאותו גוף או עסק, לפי העניין, עדיפות בעיצוב תנאי החוזה`). That is bargaining power, not authorship. Who drafted the document is a signal only: the client's own purchase order or standard supplier terms points toward it, while a large client that accepted a freelancer's quote may still have had the advantage. When it is unclear, other remedies stay open (sec. 4(c)) and the letter uses the neutral formula in Step 4. Never quote a self-invented percentage. See references/legal-escalation.md.

Step 2 measures aging against this date, not a generic net-30/60/90.

### Step 2: Import/Track Invoice Aging
Import outstanding invoices (from israeli-e-invoice output, if available, or manual entry) and categorize by aging buckets.

**Age every invoice from its DUE date, not its issue date.** Under the statutory shotef+45 default an invoice issued at the start of a month is not late until roughly 75 days after issue, one issued at month-end at about 46, so a bucket counted from issue fires "you are late" while the client is still within terms. Compute `days_late = today - due_date` using the Step 1 due date, and only then bucket:

| Bucket | Days past the DUE date | Status |
|--------|-----|--------|
| Current | not yet due | Monitor, no action needed |
| 0-day | due date reached, 0-14 days late | Phone call, then friendly WhatsApp |
| 15-day | 15-29 days late | Follow-up WhatsApp |
| 30-day | 30-44 days late | Formal email |
| 45-day | 45-59 days late | Pre-legal warning |
| 60+ day | 60+ days late | Demand letter and escalation evaluation |

Where the contract set an express term, shorter or longer, the due date is that term (Step 1).

Track per client: total owed, oldest open invoice, payment history, and contact details. Persist it across sessions, or export `payment-chaser-data.json` and reload it.

### Step 3: Configure Graduated Reminder Schedule
Set up a Shabbat/chagim-aware escalation sequence. **Every "Day N" counts from the DUE date established in Step 1, not from the invoice date.** Before every reminder, check the bank for a payment, and ask whether the client withheld income tax at source (nikui bemakor): the accountant decides whether that shortfall is really owed. Never send on Shabbat or a chag, and move a blocked reminder to the next business day. The full boundary rule (candle-lighting and nightfall offsets, the recipient's city, chol hamoed, erev chag, non-Jewish recipients, and the conservative Sunday-to-Thursday fallback when no calendar source is available) is in `references/legal-escalation.md`.

- **Due date + 0 to 3 days, phone first.** Before any written reminder, have the user phone the client's bookkeeper or accounts payable and ask one question: did the invoice arrive, and is it in the next payment run? Log the call, then send the friendly WhatsApp:
  "היי [שם], רציתי לבדוק לגבי חשבונית מספר [X] מ-[DATE] בסך [AMOUNT] ש"ח. אשמח לעדכון."

- **Due date + 15, follow-up WhatsApp:**
  "שלום [שם], תזכורת נוספת לגבי חשבונית [X]. סה"כ לתשלום: [AMOUNT] ש"ח. פרטי העברה: [BANK DETAILS]."

- **Due date + 30, formal email** with invoice copy attached and a clear payment deadline. Where the suppliers law's interest applies (Step 1, sec. 4(b)), this is also when dmei pigurim start to run, which is worth stating; where it does not, do not mention them.

- **Due date + 45, warning of potential legal steps:**
  "שלום [שם], למרות פניותינו הקודמות, חשבונית [X] טרם שולמה. ללא תשלום תוך 14 יום, ניאלץ לשקול צעדים נוספים."

- **Due date + 60 or more, demand letter** (Step 4) and evaluation of the routes in Steps 6 and 7.

See references/reminder-templates.md for complete, customizable templates at each stage.

### Step 4: Generate Hebrew Demand Letters (Michtav Drisha (pre-suit demand letter))
Generate the formal Hebrew demand letter at due date + 60, after the Step 3 warning has gone unanswered. It is always issued in the creditor's own name and signature after the user reviews it; never style it as coming from a lawyer, and never send it for them. It must include:

1. **Creditor details:** Full name/business name, address, osek murshe/patur number
2. **Debtor details:** Full REGISTERED name, address, registration number
3. **Invoice details:** Invoice number, date issued, original amount, any partial payments received
4. **Total amount due:** Including interest if applicable (see below)
5. **Payment deadline:** a dated deadline at least 21 days after the letter date, so the debtor gets 14 days after a registered letter arrives
6. **Warning of legal action:** Clear statement that failure to pay will result in legal proceedings

**Interest: two distinct statutes, do not conflate them.** A supplier's PRE-SUIT interest comes from the Payment Ethics to Suppliers Law, and only where sec. 4(b) is met (Step 1). Interest on a JUDGMENT is set by the court under the Adjudication of Interest and Linkage Law; the agent does not compute it. Neither is a Bank of Israel rate, and no rate is hard-coded here because it re-publishes quarterly. Where sec. 4(b) is not clearly met, or the current quarter's figure is not confirmed, write `בתוספת ריבית והצמדה כדין ממועד הפירעון`, which claims whatever the law allows without asserting a number or a statute. Rate source and accrual mechanics: `references/legal-escalation.md`.

**Late-payment interest is inside the VAT base.** Sec. 7 of the VAT Law includes in the price `ריבית או כל תשלום אחר בשל פיגור בתשלום`, so interest an osek murshe collects is taxable consideration.

**Delivery:** send by registered mail with delivery confirmation (doar rashum im ishur mesira / דואר רשום עם אישור מסירה) and keep the receipt and the confirmation. Email is supplementary. The confirmation fixes when the debtor knew of the demand. This letter is NOT the warning the fixed-sum route in Step 7 needs: that warning is a separate document that must carry the prescribed Form 19א wording (reg. 109a of the Execution Regulations).

See references/legal-escalation.md for full demand letter requirements and format.

### Step 5: Track Payment Promises and Negotiate
Record every promise with its amount, date and channel, and follow up the day after. Update the balance on each partial payment and confirm it. Timestamp every interaction: this log is the evidence if the file reaches court. If the debtor asks for a payment plan, see Step 5.5 BEFORE agreeing, because that request is the moment the debt can be converted into something enforceable.

### Step 5.5: Take the Cheap Rungs Before Court
The cheaper rungs only work while the debtor still wants something from you.

- **Convert the debt into a directly enforceable instrument while you still have leverage.** If the debtor asks for more time or a payment plan, do not simply agree by message. Ask for post-dated cheques covering the instalments, or a signed shtar chov (promissory note). Either can be filed straight at the Enforcement Office (Step 7) with no court case. **Against a company with nothing in it, ask for a personal guarantee (ערבות אישית) from the controlling shareholder, or their signature as a co-signer (ערב) on the note**: an instrument signed only by the company is worth what the company is worth. Check that a company cheque or note carries the authorised signatories, and that every cheque names the user as payee and is never endorsed onward, since a cheque the Cash Reduction Law bars from payment cannot go to the notes route without the fixed-sum pre-notice (Execution Law sec. 81a(g)).
- **Give any settlement the force of a judgment.** Where a case is already filed, have a reduced sum or instalment plan recorded as a psak din beheskama (consent judgment).
- **Verify who you are actually dealing with before escalating.** Check the debtor at the Companies Registrar (Rasham HaChavarot) via gov.il: exact registered name and number, and whether the company is active, in liquidation, or struck off. A demand letter addressed to a trading name that is not the legal entity is worthless. If the counterparty is an individual or an osek rather than a company, the forum does not change (Small Claims takes claims against individuals and companies alike; it is the CLAIMANT who must be an individual), but two practical things do: there is no registrar record, so collect their ID number (teudat zehut) from the contract, invoice or a cheque, since no Enforcement Office file is accepted against an individual whose details do not match the Population Registry (Execution Law sec. 6(d)(2)); and personal insolvency follows a different track.
- **Retention lien (ikavon).** Holding something of the debtor's from the same transaction may give a retention right. Fact-specific: a question for a lawyer, not a unilateral step.

**A disputed debt is a different animal.** If the debtor genuinely contests the work or the amount, get the objection in writing NOW: an allegation of defective work first raised in a defence is harder to rebut than one you can show was made late and inconsistently. The court-free routes in Step 7 are NOT a shortcut here, because an objection sends the file to court anyway. The Enforcement Office fee is then credited against the court fee (Court Fees Regulations reg. 4), so the cost is months of delay rather than the fee, and a contested debt should go to court directly. Where liability is genuinely in issue, route the user to a lawyer before escalating.

**If the debtor looks like they are disappearing, jump the ladder.** A judgment against an emptied company is worth nothing. If the debtor is winding down, selling up, moving money, changing entity or defaulting to other suppliers, get advice on a temporary attachment (ikul zmani), applied for with or just after the claim. It is discretionary and the court decides what it needs. The fixed-sum route cannot act early here (sec. 81a1(e)(2)).

### Step 6: Evaluate Small Claims Court (Tvi'ot Ktanot) Eligibility
When a debt is roughly 60+ days late and collection has failed, assess eligibility, alongside the court-free fixed-sum route in Step 7, which is often cheaper for an undisputed invoice. Full filing process in `references/legal-escalation.md`.

**Ask this first: is the CLAIMANT an individual?** Only an individual may file (Courts Law sec. 60(a)), and an osek murshe or osek patur counts as one. A company, partnership or amuta is barred (`חברה בע"מ, שותפות או עמותה לא יוכלו להגיש תביעה לבית משפט זה`) and must go to Magistrate Court, or use Step 7, whatever the amount. Ask before anything else.

**Threshold:** up to 39,900 NIS (2026 indexed figure; verify, it is updated periodically).

**Recommend a lawyer rather than self-filing when:** the debtor genuinely disputes liability (Step 5.5); the debtor is insolvent or in liquidation; the debt is near the limitation deadline; the debtor is outside Israel; or the amount exceeds the threshold.

**Other eligibility points:** documentation must exist (invoice, contract or PO, delivery confirmation). A demand letter is NOT a precondition of filing, though it is worth sending. More than five small claims by the same claimant in the same court that year lets the court **transfer** the case to Magistrate Court; it is not a bar.

**Filing:** fee is 1% of the claim, minimum 50 NIS, rounded up to a multiple of 5 (reg. 6(a) of the Small Claims (Procedure) Regulations). Venue is a CHOICE from a closed list (reg. 2(a)): the defendant's residence or place of business, or the place of the act or omission sued on. The older limbs about where the undertaking was made or was to be performed are repealed, so do not rely on them. It applies `על אף האמור בכל הסכם שבין בעלי הדין`, so a contractual venue clause does NOT bind; online-trade claims: reg. 2(b), in the reference. Never tell a user they must travel to the debtor's city. Representation by a lawyer needs the court's leave for special reasons (Courts Law sec. 63(a)), so do not say lawyers are flatly forbidden, and do not say one is required.

Above the threshold the claim goes to Magistrate Court, where representation is not legally required but is strongly advisable. If the debt is an undisputed note or qualifies for the fixed-sum route, suing in court instead normally means no award of lawyer's fees (Execution Law sec. 81a2).

### Step 6.5: Check for Insolvency Before Escalating Further
This is the one place in the workflow where doing nothing forfeits the debt, so check it before spending money on a claim or an enforcement file.

If insolvency proceedings have been opened against the debtor under the Insolvency and Economic Rehabilitation Law, 5778-2018, two things change at once:

- **Collection freezes.** For a company (sec. 29) or an individual (sec. 121(a)(3)), collection of past debts cannot be opened or continued, and for an individual existing enforcement restrictions lapse. The route is the proof of claim.
- **The creditor must file a proof of claim (tvi'at chov) with the trustee (ne'eman) within six months of PUBLICATION of the opening order** (sec. 210(a)). A debt arising after the order is filed within 45 days of arising or by the end of that six months, whichever is later (210(b)), and the trustee may extend for good cause (210(c)). Miss it and the debt is not counted; diarise it against the published notice.

**A stay can also come without any insolvency order.** A company (sec. 319ג) or an individual (sec. 319יז) with no opening order may ask the court for a temporary stay of proceedings to negotiate a debt arrangement, and while it runs proceedings against the debtor are frozen.

When a registrar status, a liquidation or stay notice, or the debtor's own words point here, route the user to a lawyer promptly.

### Step 7: Open an Enforcement Office (Hotza'a LaPo'al) File to Collect
There are three doors to the Enforcement and Collection Authority, and only one needs a judgment. Fees, forms and the full process are in `references/legal-escalation.md`.

- **A fixed-sum claim, no judgment needed (Execution Law sec. 81a1).** A claim for a fixed sum arising from an express contract or undertaking with written evidence (`תביעה על סכום כסף קצוב הבאה מכוח חוזה או התחייבות מפורשים, שיש עליה ראיה בכתב`), up to 75,000 NIS on the day of filing, can be filed at the Enforcement Office and enforced like a judgment. Three conditions decide whether it works. (1) The evidence must be **signed by the debtor**, by hand or by an approved electronic signature (reg. 109d1): a quote or contract the client signed qualifies, an email or WhatsApp "approved" usually does not, and the office may refuse the request. (2) Before filing, the creditor serves a warning (hatra'a) built on the prescribed Form 19א wording, stating the amount, the main facts and contract details, the date the debt arose and the supporting documents (reg. 109a), by registered mail with delivery confirmation; an uncollected letter is not service. (3) The file may be opened only 30 days after service, and after a year a fresh warning is needed. The debtor then has 30 days from the azhara to object, an objection sends it to court, and nothing is enforced before that period ends (sec. 81a1(e)(2)). Unlike Small Claims it is open to a company claimant. UNDISPUTED debts only (Step 5.5).
- **A cheque or note (sec. 81a).** A dishonoured cheque with the bank's notice of dishonour, or a signed promissory note, is filed directly as a notes file. The debtor's objection period is 30 days from service of the azhara.
- **A judgment.** The date for performance set IN the judgment governs. Only where it sets none is the wait 30 days from the judgment, running from service where it issued in the debtor's absence and you had to serve it. Sec. 6(b1) lets the registrar allow earlier filing on affidavit where waiting would frustrate enforcement. Do not sit on it: a judgment or note filed more than a year after it could have been gets only ribit shkalit for the gap (sec. 6(b2)).
- **Nothing coercive happens until the azhara is served and its period runs** (20 days in a judgment file), unless the registrar finds cause to act earlier (sec. 7(e)), an exception that does not apply to a fixed-sum file.
- **What moves a debtor who HAS money.** Third-party attachment (ikul etzel tzad shlishi, sec. 44) catches what banks or the debtor's own clients hold for them on service and for three months after. Restrictions under sec. 66a (passport and exit ban, the special restricted-customer cheque status, payment cards, founding or holding a corporation) are a closed list, with **no** driving-licence power and **no** power to stop the debtor opening bank accounts, and they are gated by sec. 66b. Where the debtor claims they cannot pay, ask for an ability investigation (chakirat yecholet). Details and conditions: `references/legal-escalation.md`.
- **The fees come back.** The creditor pays fees up front, but they are charged to the debtor as part of the debt and carry interest (sec. 9). If the debtor applies to consolidate files (ichud tikim), proceedings continue until an order is made (sec. 74c).

### Step 8: Generate Aging Reports and Cash Flow Forecasts
Produce a per-client aging report by days-late bucket, a forecast weighted by payment history, and a monthly summary; score each client Reliable / Slow payer / Problematic to set escalation speed. Export PDF or CSV.

Two domain-specific points:

- **Bucket by days LATE, never by invoice age.** A report on invoice age overstates the problem and has the user chasing clients still within terms.
- **Do not forget the VAT already paid on an unpaid invoice.** Where the user issued a tax invoice (chashbonit mas) and reports on the ordinary accrual basis, they remitted VAT on money never received. Many freelancers issue a payment demand (cheshbon iska) first and the tax invoice only on payment, so ask which document went out. The VAT Regulations provide a bad-debt route (chov avud, reg. 24a): a credit note plus a written notice with supporting documents, for which this skill's collection trail is the support. It is open only from 6 months to 3 years after the tax invoice date (reg. 24a(c)); time in a court claim or a liquidation claim is not counted (24a(d)), but informal chasing does not stop the clock, so flag an unpaid tax invoice nearing 3 years.

## Examples

### Example 1: Five overdue invoices
User says: "I have 5 unpaid invoices from the last 3 months, can you help me collect?"
Establish each invoice's DUE date first (Step 1), including whether the suppliers law covers the client and who had the advantage in setting the terms. Only then bucket by days late, which typically reveals that one or two are not actually late yet. Start the ladder with a phone call on the ones just due, draft the formal email for those around 30 days late, and prepare a demand letter for the oldest. Report the total outstanding and, separately, the total actually overdue.

### Example 2: Client promised to pay and did not
User says: "ABC Ltd promised to pay invoice 1234 two weeks ago but still nothing"
Note the broken promise, verify ABC Ltd at the Companies Registrar, and take the cheap rung first (Step 5.5): post-dated cheques or a promissory note. If that fails, send the demand letter by registered mail with delivery confirmation, then weigh the fixed-sum route (Step 7) against Small Claims (Step 6), checking first that the claimant is an individual or osek rather than a company.

### Example 3: Monthly collection report
User says: "Show me where I stand with all my outstanding invoices this month"
Produce the aging report by days late, the forecast and the collection rate. Flag any invoice approaching the limitation period, and flag the VAT on invoices now looking irrecoverable so the user can raise the bad-debt route with their accountant.

## Bundled Resources

### References
- `references/legal-escalation.md` - Israeli legal framework for debt collection: demand letter (michtav hitraa / michtav drisha, a pre-suit demand letter) requirements, Small Claims Court (tvi'ot ktanot) thresholds and filing process, the three Enforcement Office routes and their fees and clocks, interest rules, and the Shabbat scheduling rule. Consult in Steps 3, 4, 6 and 7.
- `references/reminder-templates.md` - WhatsApp and email reminder templates in Hebrew for each escalation stage (friendly, follow-up, formal, pre-legal, demand letter). Consult when configuring reminder messages in Step 3.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Accountant General quarterly rates (ribit shkalit / ribit tzmuda / dmei pigurim) | https://data.gov.il/api/3/action/datastore_search?resource_id=d1cdadd7-f6b6-40a2-aab9-73230d5fe294 | THE source for the statutory late-payment rate. Read the row whose `ineffecfrom` covers your period |
| Courts Administration - Small Claims service page | https://www.gov.il/he/service/filing_a_small_claim | Current threshold, filing process, jurisdiction rules |
| Kol-Zchut - Filing a small claim (Hebrew) | https://www.kolzchut.org.il/he/הגשת_תביעה_קטנה | Plain-language eligibility and procedure guide |
| Payment Ethics to Suppliers Law (consolidated text) | https://he.wikisource.org/wiki/חוק_מוסר_תשלומים_לספקים | Payment terms (sec. 3), interest and its sec. 4(b) condition |
| Execution Law (consolidated text) | https://he.wikisource.org/wiki/חוק_ההוצאה_לפועל | Fixed-sum route (sec. 81a1), notes (81a), filing times (6), restrictions (66a-66b) |
| Enforcement and Collection Authority | https://www.gov.il/he/departments/law_enforcement_and_collection_system_authority | Opening a judgment, notes or fixed-sum file, fees, required documents |
| Israel Post - Registered mail service | https://www.israelpost.co.il | Registered mail with delivery confirmation |
| HebCal - Jewish calendar | https://www.hebcal.com | Shabbat times and holiday dates for reminder scheduling |

## Recommended MCP Servers

| MCP Server | Why |
|------------|-----|
| `hebcal` | Step 3 (graduated reminder scheduling) and the Troubleshooting "Reminder sent on Shabbat/holiday" case both depend on Shabbat and chag-aware scheduling. Use it to resolve Shabbat entry/exit times and holiday dates so reminders never fire on a blocked day. |
| `israel-law` / `kolzchut` | Optional. Look up the current text of the Payment Ethics to Suppliers Law, Small Claims procedure, and enforcement rules instead of relying on cached figures. |

## Gotchas
- **Shotef is not net-N.** "Shotef + 30" means the end of the current month plus 30 days, not 30 days from the invoice date. Agents routinely compute the due date as if it were net-30 and then chase a client who is not yet late.
- **Age from the due date, not the invoice date.** Every bucket, reminder and letter keys off the Step 1 due date.
- **Statutory interest against a business is conditional.** Sec. 4(b) of the suppliers law limits it to engagements where the client had the advantage in shaping the terms. Agents assert it on every invoice, which puts a claim in the letter the creditor may not have. When in doubt, write `בתוספת ריבית והצמדה כדין ממועד הפירעון` and never quote the Bank of Israel rate.
- **Winning is not collecting, and court is not the only door.** A judgment does nothing until an enforcement file is opened. Agents also forget that an undisputed fixed-sum invoice can go to the Enforcement Office with no judgment at all (sec. 81a1).
- **A 7-year limitation period, not 3.** An ordinary debt runs 7 years (sec. 5(1) of the Limitation Law, `בשאינו מקרקעין – שבע שנים`); a judgment runs 25 (sec. 21). For a claim still running on 25.1.2024, the period from 7.10.2023 to 6.4.2024 is not counted (sec. 15a), so do not tell a user an older invoice lapsed on the naive date. A written acknowledgment or a part payment restarts the period (sec. 9), so log both.

## Troubleshooting

### Error: "Reminder sent on Shabbat/holiday"
Cause: the calendar was not loaded, or sunset was used instead of candle-lighting.
Solution: apply the boundary rule in references/legal-escalation.md, resolving times for the RECIPIENT's city. With no calendar source, fall back to Sunday-Thursday 09:00-16:00 rather than sending unchecked.

### Error: "Small Claims threshold exceeded"
Cause: Invoice amount exceeds the Small Claims Court maximum (currently 39,900 NIS).
Solution: check the fixed-sum route first (Step 7, up to 75,000 NIS for an undisputed invoice backed by evidence the client signed). Otherwise the claim goes to Magistrate Court (Beit Mishpat Shalom), where a lawyer is not legally required but is strongly advisable. For several invoices to the same debtor, consider whether they belong in one claim rather than being split to fit under the cap.

### Error: "Demand letter delivery not confirmed"
Cause: registered mail was returned or not collected.
Solution: keep the postal receipt; it evidences dispatch. For a fixed-sum warning there are three cases: delivered, and the 30 days run from the delivery date on the confirmation; refused, and the debtor is treated as served (sec. 81a1(b2)), so keep the postal note of the refusal; uncollected, which is NOT service, so re-send or, if a lawyer acts, use personal service (sec. 81a1(b1)). If the address is wrong, re-check the debtor's registered details (Step 5.5).

### Error: "Interest calculation disputed"
Cause: Applied the wrong interest rate, conflated the two statutes, or assumed sec. 4 applied without checking sec. 4(b).
Solution: separate the two statutes as in Step 4, and fall back to `בתוספת ריבית והצמדה כדין ממועד הפירעון` rather than a figure.
