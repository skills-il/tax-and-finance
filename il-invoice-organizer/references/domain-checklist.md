# Domain Coverage Checklist, il-invoice-organizer

Generated: 2026-07-06 via CPA coverage audit + fact research on gov.il/taxes, kolzchut, nevo VAT regs, greeninvoice, CPA-firm publications.

## Must cover (core)

- [ ] Document-type triage: only a חשבונית מס or חשבונית מס/קבלה grants input VAT; a חשבונית עסקה does not; a קבלה, a חשבונית פרופורמה and a חשבונית זיכוי are each handled distinctly, the credit note as a NEGATIVE, source: §38 VAT Law 5736-1975. [covered]

- [ ] VAT extraction via the 18/118 rule at 18%, using the printed VAT line when present, rounding tolerance 1 NIS, source: VAT Law §2; rate 18% from 1 Jan 2025. [covered]

- [ ] Foreign / import invoices: NO Israeli input VAT from a foreign-supplier invoice; import VAT reclaimed ONLY via the customs import entry (רשימון יבוא); convert foreign currency to ILS at the invoice-date rate, source: VAT Law §7 (import), §30 (zero-rated). [covered v1.3.0]

- [ ] Input-VAT eligibility gates: invoice issued in the claiming business's name (על שם העוסק), actually held by the claimant, and within the 6-month deduction window (later needs VAT-office approval), source: §38(א) VAT Law (NOT תקנה 23א, which is an unrelated extra return). [covered v1.3.0]

- [ ] Blocked / partial input VAT: hospitality/entertainment (אירוח) blocked (תקנה 16, except foreign guest); purchase/import VAT on a private vehicle non-deductible (תקנה 14); running-cost apportionment 2/3 where the main use is business and 1/4 where it is not, subject to the Director's determination (תקנה 18(ב)), source: VAT Regulations 1976. [אירוח + vehicle purchase now enforced in the script v1.3.0; תקנה 18(ב) vehicle ladder implemented in the script v1.5.0; the general תקנה 18(א) taxable/exempt turnover split is still to add]

- [ ] SHAAM allocation number (מספר הקצאה) required above the issue-date threshold (25k from 5-May-2024 / 20k 2025 / 10k Jan-2026 / 5k Jun-2026; 5,000 is the terminal step and nothing below it is legislated). Keyed to the invoice ISSUE date.

- [ ] Business-type recognition (Osek Murshe / Patur, HP, amuta, malkar) + Osek Patur ceiling 122,833 (2026), source: VAT Law §31 + annual index. [covered]

- [ ] Expense categorization into the 12 working categories. The 1-12 numbering is this skill's own convention, NOT an ITA-published code list, and must not be presented to a user as official.

- [ ] Accountant-ready export flagging: missing allocation number, invoices older than 6 months, invoices not in the business name, VAT mismatches, source: Bookkeeping Regulations. [covered v1.3.0]

## Should cover (advanced / edge cases)

- [ ] Withholding tax at source + supplier certificate (אישור ניכוי מס במקור, §164 ITO) check for subcontractors/services, source: Income Tax Ordinance §164. [to add next cycle]

- [ ] Reporting basis note: cash (מזומן) vs accrual (מצטבר) driving VAT-period allocation, source: bookkeeping regs. [to add next cycle]

- [ ] Reverse charge / self-invoicing (חשבונית עצמית) for foreign/unregistered suppliers, source: §20-21 VAT Law. [briefly noted v1.3.0]

- [ ] Filing-deadline surfacing (bi-monthly ≤1,775,000 / monthly VAT, detailed report >500,000, annual return, BL advances). [covered]

- [ ] Osek Zair 30% flat-expense election interaction. [covered]

- [ ] Small-value simplified-document threshold for input deduction (תקנה 23); petty cash. [to add next cycle]

- [ ] 7-year record retention. [covered in expense-categories note 5]

## Out of scope (explicit)

- [ ] Filing the VAT return itself, handled by `israeli-vat-reporting`.
- [ ] Generating / issuing invoices, handled by `israeli-e-invoice`.
- [ ] Income-tax annual-return computation and payroll processing.

## Authoritative sources

- Value Added Tax Law (חוק מס ערך מוסף), תשל"ו-1975, and VAT Regulations (תקנות מע"מ), תשל"ו-1976 (nevo.co.il).
- Israel Tax Authority: https://www.gov.il/he/departments/israel_tax_authority ; digital invoices: (link removed, this gov.il page now returns 404)
- Income Tax Ordinance (פקודת מס הכנסה [נוסח חדש]).
- CPA-firm publications (bshcpa, tax-advisor, greeninvoice) for 2026 thresholds.
