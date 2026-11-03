# Domain checklist: israeli-vat-reporting (periodic VAT return, doch maam)

Scope: prepare, validate and guide submission of an Israeli SME's periodic VAT return. Decide monthly vs bi-monthly and whether the detailed report (PCN874) applies, compute output and input VAT from the user's sales and purchase invoices (with the input-VAT limits), map to the periodic return, and state the filing deadline.

Category: tax-and-finance. Prepared 2026-11-03 (bootstrap, update-skill v1.6.0). Coverage in SKILL.md v1.6.0: A1-A5c, B1-B4, C1-C3, C6, D1-D9, D11, E1-E3 (including E1b and E2c), E4, E5, F1, F4, G1-G6, H1-H2. Reference-only this cycle (logged in optimization-log.json): A4d, A4e, A6-A6b, C4, C5, D10, E6, F2, F3, F5, F6, G8, H3, H4 and the Should-cover table.

Primary texts read locally (verbatim):
- VAT Law 1975 (חוק מס ערך מוסף, התשל"ו-1975), Nevo 271_001, "נוסח עדכני נכון ליום 13-07-2026" (`src/271_001.txt`).
- VAT Regulations 1976 (תקנות מס ערך מוסף, התשל"ו-1976), Nevo 271_005 (`src/271_005.txt`).
- ITA directive (הוראת ביצוע מע"מ) 01/2025, 7.12.2025, allocation numbers (`src/vat_inst-071225-1.txt`).
- ITA directive 01/2024, 15.8.2024 (`src/vat_inst-180824-1.txt`), SUPERSEDED schedule, kept only as a negative control.
- ITA "מודל חשבוניות ישראל, תיאור ה-API's", edition 2.0, 7.2024 (`src/vat_software-houses-180724.txt`).
- Research notes `research-2026-11-03.md` (secondary-source items are marked as such below).

Notation: "s." = section of the VAT Law; "reg." = VAT Regulations 1976. Every amount below is in NIS, before VAT unless stated.

---

## Must cover (core)

### A. Who files and how often

| # | Item | What the skill must state or do | Authority |
|---|------|---------------------------------|-----------|
| A1 | Osek patur is out of this flow | An osek patur (turnover up to 122,833 for 2026) does not file a periodic VAT return with output/input computation; route to the annual declaration. 2027 figure is NOT PUBLISHED as of 2026-11-03 (indexed 1 January by CPI of 15 December, s.126(א)). | s.1 definition "עוסק פטור"; s.126(א); reg. 22 |
| A2 | VAT rate | 18% from 1.1.2025. No enacted change for 2027 (proposals only). Output VAT = 18% of the price; VAT included in a gross amount = gross x 18/118. | s.2; צו מע"מ (שיעור המס) (תיקון) התשפ"ד-2024 (secondary: capitax) |
| A3 | Frequency BY detailed-report status | An osek obliged to file the detailed report (A5) files MONTHLY, regardless of turnover. | s.67א(א) |
| A4 | Frequency BY turnover (not detailed-report filers) | Bi-monthly if turnover in the "determining year" does not exceed the threshold; otherwise monthly. Bi-monthly periods start 1 Jan, Mar, May, Jul, Sep, Nov. | s.67(א2)(1); reg. 20(ב), 20(ג)(1) |
| A4a | Threshold row: year 2026 | 1,775,000 (statutory figure in Nevo text current to 13-07-2026). Note: reg. 20(ג)(1) still prints 910,000; the statutory s.67(א2) figure governs. | s.67(א2)(1) |
| A4b | Threshold row: year 2027 | 1,805,000 from 1.1.2027 (Kol Zchut and a CPA firm relaying the ITA notice; the gov.il amounts page was blocked this cycle). | s.126(ד) mechanism; Kol Zchut |
| A4c | Determining year / indexation date | Determining year = 12 consecutive months ending 31 August of the past year (so frequency for 2027 is set by turnover 1.9.2025 to 31.8.2026). Threshold indexed every 1 September, rounded to the nearest 5,000. Do NOT say "indexed 1 January". | reg. 20(א) "השנה הקובעת"; s.126(ד) |
| A4d | New osek / part-year | Turnover for a partial year is annualised per reg. 14 of the Registration Regulations; first period runs from the start date to the end of that month or two-month period. | reg. 20(ג)(3), 20(ד); s.67א(ג) |
| A4e | Voluntary monthly | Director may permit a bi-monthly osek to file monthly. | s.67(א2)(1); reg. 20(ג)(5) |
| A5 | Detailed report (PCN874) trigger | Applies if turnover exceeds 500,000, OR the osek must keep double-entry books under the Income Tax bookkeeping instructions, OR the Director allowed it on request. | s.69א(ז)(1), (3) |
| A5a | Detailed report row: companies / corporations | Obligation in force (no deferral). | s.69א(ז); ITA notice (secondary, britcpa circular 59.2025) |
| A5b | Detailed report row: individual, turnover > 500,000 | Starts with period 1/2026 (deferred from 1.9.2025). | ITA notice (secondary, britcpa) |
| A5c | Detailed report row: individual with deferral to 1.1.2027 | Allowed on application + affidavit if at least 90% of total input-invoice AMOUNT for 2025 was on invoices of up to 5,000 each (by amount, not count). Deferral does not apply to companies or to an individual who already started detailed filing. First detailed period 1/2027. | ITA notice (secondary, britcpa) |
| A6 | Detailed report content | Itemise each tax invoice (issued and claimed): serial number, date, amount, VAT, seller and buyer registration numbers, allocation number where the invoice has one; import/export declarations by number. | s.69א(א), 69א(ב) |
| A6a | Itemisation exemption <= 5,000 | Invoices of up to 5,000 each (before VAT) need not be itemised, provided their total is reported. For individuals the ITA fixed code 77777772 is used for the aggregate (secondary). | s.69א(ג), 69א(ד); ITA notice (secondary) |
| A6b | PCN874 record fields | Per invoice record: counterparty VAT file N(9), date YYYYMMDD, reference group A(4), reference number (9 rightmost positions), VAT amount rounded to shekel, +/- sign (credit always minus), invoice total, SHORT allocation number N(9) (mandatory where allocated), on both sales and input side. Storno rule for an input rejected over allocation mismatch: omit both the input and the storno record. | ITA API spec v2.0 s.6 |

### B. Output VAT (עסקאות)

| # | Item | What the skill must state or do | Authority |
|---|------|---------------------------------|-----------|
| B1 | What goes in the period | All transactions whose invoice date fell in the period (even if exempt from issuing), plus every tax invoice actually issued even if early; nothing already reported. | s.69(א); s.69א(א)(1)-(2) |
| B2 | Tax point by type | Goods: on delivery (s.22(א)). Services: on receipt of consideration and on the amount received (s.24). Self-use: s.25. Invoice must issue within 14 days of the tax point (s.46(א)). | s.22, s.24, s.25, s.46(א) |
| B3 | Taxable vs zero-rated vs exempt shown separately | Report separately the total of each class and the tax on each. | s.69(ב); s.69א(ה); s.30 (zero rate), s.31 (exemptions) |
| B4 | Credit notes / cancelled transactions | VAT per invoice stays payable until the invoice is cancelled or corrected as prescribed; a buyer who received a credit notice adjusts input VAT in the period the notice was received. | s.49; reg. 24(ב) |

### C. Input VAT (תשומות): base rule and documents

| # | Item | What the skill must state or do | Authority |
|---|------|---------------------------------|-----------|
| C1 | Valid document | Deduct only from a tax invoice lawfully issued to the osek, an import declaration, or another Director-approved document bearing the osek's name. Receipts and transaction invoices (חשבונית עסקה) are not enough. | s.38(א) |
| C2 | Six-month window | Deduction must be made within 6 months of the document date. Director may extend up to 5 years. A late-requested allocation number does not extend the window. | s.38(א); s.116(א); s.47(א2)(4) |
| C3 | Inputs only for taxable transactions | No deduction on inputs for exempt transactions. | s.41 |
| C4 | Pre-registration inputs | Not deductible, except business-setup inputs proven to the Director (and allocation number if above the s.38(א1) amount). | s.40, s.40א |
| C5 | Cash-law breach | No deduction where the payment was a violation of the Cash Reduction Law and a monetary sanction was imposed. | s.38(א2) |
| C6 | Report fields | Report separately total purchases (incl. imports), total services received, and deductible input VAT on documents issued before period end. Split "fixed assets/equipment" vs "other inputs" as the return form requires. | s.69(ג); s.69א(ו); reg. 23(א) (form set by Director) |

### D. Allocation-number condition (מספר הקצאה), by invoice date

| # | Invoice date (row) | Rule | Authority |
|---|-------------------|------|-----------|
| D1 | Before 5.5.2024 | No allocation-number condition. | Directive 01/2025 intro ("החל מיום 01.01.2024, לאחר מתן אורכה הוחל מיום 05.05.2024") |
| D2 | 5.5.2024 to 31.12.2024 | Required above 25,000 before VAT. | ITA API spec v2.0 ("בשנת 2024 ... גבוה מ-25,000 (בשלב הפיילוט)") |
| D3 | 1.1.2025 to 31.12.2025 | Required above 20,000. | Directive 01/2025 s.1(א) |
| D4 | 1.1.2026 to 31.5.2026 | Required above 10,000. | Directive 01/2025 |
| D5 | From 1.6.2026 | Required above 5,000. No further step-down scheduled. | s.38(א1) (5,000 in statute); Directive 01/2025 |
| D6 | Superseded schedule warning | Directive 01/2024 and API spec v2.0 still print 15,000 (2026) / 10,000 (2027) / 5,000 (2028). The skill must NOT use that table. | Directive 01/2024 lines 20-23 (negative control) |
| D7 | Conditions for the number | Invoice includes VAT, buyer is an osek murshe, buyer requested it. Zero-rated or exempt-only invoices get no number. Any amount may be voluntarily allocated. | Directive 01/2025 s.1; s.47(א2)(1) |
| D8 | Who obtains and prints it | The ISSUER requests it (obliged on the buyer's demand above the threshold) and prints it, including by hand. Printing the 9 rightmost digits under "הקצאה מספר:" is permitted and recommended; full numbers in ITA examples are 26 digits (field A30). | s.47(א2)(1)-(2); API spec v2.0 s.2.2.1, table 3.1 |
| D9 | Missing number = no deduction | Above the threshold, an invoice without a Director-allocated number is not deductible, whoever is at fault. No "buyer requested it" exception. Only outs: s.40ב (ITA system outage, Director's order) and the reverse-charge self-invoice path. | s.38(א1); s.40ב; s.47(א2)(3)(ג) |
| D10 | Denied allocation: the issuer's 4 options | Cancel; issue without a number (buyer cannot deduct); shift liability to buyer (special number, zero-rated invoice, buyer self-invoices); appeal to control room / hearing within 2 business days. | Directive 01/2025 s.ד |
| D11 | "אישור הקצאה" on proforma | A 9-digit approval on a proforma/transaction bill is NOT an allocation number and cannot support deduction. | Directive 01/2025 s.2 |

### E. Input-VAT limits (one row per category)

| # | Category | Rule | Authority |
|---|----------|------|-----------|
| E1 | Private car: purchase or import | Input VAT on buying or importing a private car is not deductible. | reg. 14(א) |
| E1a | Private car exceptions | Deductible where the osek's main business is selling cars (car held only for sale), or the car is used exclusively for driving school, car rental business, passenger transport business, or tours/field trips business. | reg. 14(ב)(2)(א)-(ב) |
| E1b | "Private car" definition | By reference to the Traffic Regulations and the fourth schedule list (e.g. certain SUVs/pickups). Ask vehicle type before applying. | reg. 1; fourth schedule |
| E2 | Mixed use: Director set a ratio | Use the Director's ratio (e.g. vehicle running costs) as an assessment. | reg. 18(ב)(1) |
| E2a | Mixed use: no ratio, mainly business | Deduct 2/3 of the input VAT. | reg. 18(ב)(2) |
| E2b | Mixed use: no ratio, mainly non-business | Deduct 1/4 of the input VAT. | reg. 18(ב)(3) |
| E2c | Mixed use: identifiable split | Deduct the proportional business share. | reg. 18(א) |
| E2d | Private-car running costs | Fuel, repairs, insurance-related services etc.: not barred by reg. 14 (purchase only); fall under reg. 18 (2/3 or 1/4 unless a ratio was set). | reg. 14(א) scope; reg. 18(ב) |
| E3 | Entertainment / hosting (אירוח) | Not deductible, except hosting a person from abroad. | reg. 16 |
| E4 | Employee benefits (meals, housing, gifts, recreation for employees, owners, managers) | Not deductible unless the benefit is sold or supplied to the employee and reported as a taxable transaction. | reg. 15א |
| E5 | Residential apartment used as business place | No deduction on buying or building one's own residence (or services for it) even if also used for business. | reg. 15 |
| E6 | Imports via personal-import agent | Input on goods imported for individuals via a personal-import agent's entry is not deductible. | reg. 16א |
| E7 | Allocation number | See section D (condition applies on top of any category above). | s.38(א1) |

### F. Computing and mapping the return

| # | Item | What the skill must state or do | Authority |
|---|------|---------------------------------|-----------|
| F1 | Net computation | VAT payable = output VAT minus deductible input VAT for the period. Show the working per category. | s.38(א); s.69 |
| F2 | Refund (excess input) | Excess input refunded within 30 days of receipt of the return (90 if books audited, 180 if investigation). Director may withhold if books not kept or earlier returns missing. | s.39(א)-(ב) |
| F3 | Large-refund return channel | A paper return with excess input of 21,718 or more is filed at the VAT office (representatives connected to Sha'am may file any amount online). | reg. 23(ג) (amount per הודעה (מס' 2) התשפ"ו-2026) |
| F4 | Nil return still due | A return is due even if there was no activity, unless business ceased and the Director was notified. | s.67(ב); s.67א(ד)(1) |
| F5 | Provisional and supplementary returns | Provisional (estimated) return allowed max twice a year, full return within 30 days; omitted data via supplementary report with Director's permission. | s.68; s.71 |
| F6 | Signature / form | Filed on the Director's form, signed personally or by an authorised representative. | reg. 23(א) |

### G. Filing deadline (one row per channel x report type x rest-day shift)

| # | Row | Deadline | Authority |
|---|-----|----------|-----------|
| G1 | Regular periodic return, statutory | 15th of the month after the period. | s.67(ב) |
| G2 | Regular return filed and paid ONLINE, non-detailed filers | Up to the 19th, by 18:30 on the Tax Authority site. | Kol Zchut periodic-returns page (evidence `online-19-non-detailed`, `online-1830`) |
| G3 | Detailed report (PCN874) | 23rd of the month after the period (online only in practice). | s.67א(ד)(1) |
| G4 | Statutory rest-day shift | If at least 3 rest days (Shabbat, statutory holidays, chol hamoed) fall in the 5 days before the deadline, it moves to the 4th working day after the run of rest days. | s.67(ב1); s.67א(ה) |
| G5 | Weekend administrative shift | If the 15/16/23 falls on Fri, Sat or Sun, the deadline moves to the next business day (Monday in Sha'am). | ITA 2026 calendar s.4 (secondary: Haifa Chamber reproduction) |
| G6 | Use the ITA annual calendar | The ITA fixes each period's dates (e.g. Oct 2026 period: 16.11 regular / 23.11 detailed; Nov: 15.12 / 23.12; Dec: 18.1.2027 / 26.1.2027). 2027 calendar NOT seen as of 2026-11-03: tell the user to confirm. | ITA 2026 calendar (secondary) |
| G7 | 18:30 cutoff | Stated for VAT periodic returns by Kol Zchut; the gov.il service page could not be read this cycle. | Kol Zchut |
| G8 | Online filing as sole channel | Where a filer is required to file online, a non-online filing is treated as not filed. | s.67ב(ו) |

### H. Consequences the user must be warned about

| # | Item | Rule | Authority |
|---|------|------|-----------|
| H1 | Late filing penalty | A fixed fine per two-week period of delay, indexed; verify the current amount. | s.94 |
| H2 | Late payment | A weekly late-payment surcharge plus linkage and interest; verify current rates. | s.96; s.97 |
| H3 | Unrecorded input documents | A fine applies to input documents the osek did not record. | s.95(א1) |
| H4 | Burden of proof | The person claiming that tax was paid, a return filed, or input deducted bears the proof: keep invoices. | s.132 |

---

## Should cover (advanced)

| # | Item | Why advanced | Authority |
|---|------|-------------|-----------|
| S1 | Turnover rising mid-year | If current-year turnover is found to exceed the prior year's, the higher figure is the turnover from that day; may flip osek patur status or detailed-report status mid-year. | s.1 "מחזור עסקאות של עוסק" |
| S2 | Reverse-charge alternative after denied allocation (buyer side) | Buyer issues a self-invoice with the special number, reports output, deducts input as allowed. | s.47(א2)(3)(ג)(1), (א3); Directive 01/2025 s.ד(3) |
| S3 | Car rental short-term | The historic reg. 14(ב)(1) exception for short rentals was repealed: do not apply it. | reg. 14(ב)(1) "(בוטלה)" |
| S4 | Director's delegated vehicle ratios | Director's powers under reg. 18 delegated to the ממונה (י"פ 7301, 7547). Mention that ITA-set ratios for vehicles override 2/3. | reg. 18 footnote [2] |
| S5 | Palestinian Authority / Area suppliers | Input on invoices from Area/Gaza-Jericho registered dealers deductible within 6 months on prescribed form plus s.72 report. | s.38(ג); reg. 23א |
| S6 | Correcting a filed return | Supplementary report (s.71) vs folding into next period; 5-year assessment window. | s.71; s.77(ב); s.79(א) |
| S7 | Joint registration (union of dealers) | Annual summary report within 90 days of year end. | s.71א |
| S8 | Allocation-number short form in bookkeeping | Short number (9 rightmost digits) is what goes into PCN874; reconcile with supplier's full number. | API spec v2.0 s.2.2.1, s.6 |
| S9 | Transition years for period start | Bi-monthly filer who becomes detailed-report-obliged switches to monthly from the first month the obligation applies. | s.67א(א); s.69א(ז) |
| S10 | Refund-return interest and audit triggers | Large refunds trigger audit (90 days) and possible withholding; prepare substantiation. | s.39(א)(1), 39(ב) |

---

## Out of scope (explicit)

| Item | Rationale |
|------|-----------|
| Reverse charge on services and intangibles bought from foreign suppliers (s.21 and the buyer-liability regulations) | Separate self-invoicing regime with its own conditions; route to accountant. |
| Reg. 6A (buyer pays the tax on listed services from a person whose main income is salary, pension or annuity) and other buyer-liability rules | Sector-specific buyer-liability rules; route to accountant. |
| Eilat (חוק אזור סחר חפשי באילת) | Separate exemption and annual-report regime (reg. 21א); proposals to repeal pending; route to accountant. |
| Amutot / malkar, financial institutions (s.70, wage/profit tax) | Different tax base and reports; not an SME doch maam. |
| Mixed taxable and exempt activity apportionment (s.41 with reg. 18(א) beyond simple cases) | Requires turnover-based or usage-based allocation and annual adjustment; route to accountant. |
| Precious-stones dealers (s.33, reg. 21א annual period) | Special annual regime. |
| Real estate transactions (s.28, s.31(1)), new-apartment zero rate | Specialised tax point and exemptions; route to accountant or lawyer. |
| Second-hand goods margin scheme (s.5) | Margin-based tax; specialist. |
| Imports and customs valuation (s.11, s.26) | Customs-entry driven; route to customs broker. |
| Exports and zero-rated services to foreign residents (s.30(א)) | Classification is fact-heavy; skill may flag but not decide. |
| Osek patur annual declaration | Different filing; separate skill. |
| Income-tax advances (מקדמות) and withholding | Different tax; route to income-tax skills. |
| Assessments, objections, appeals, criminal exposure, tax opinions reporting (s.67ג, s.67ד) | Litigation and advisory; route to accountant or lawyer. |
| Actually submitting on the ITA portal for the user, or holding credentials | Out of agent capability and a security risk; skill guides, the user submits. |

---

## Authoritative sources

Primary (read verbatim locally):
1. חוק מס ערך מוסף, התשל"ו-1975, Nevo 271_001, current to 13-07-2026. Sections used: 1, 2, 22, 24, 25, 38, 39, 40, 40א, 40ב, 41, 46, 47(א2)-(א4), 49, 67, 67א, 67ב, 68, 69, 69א, 71, 71א, 94, 95(א1), 96, 97, 116, 126, 132. https://www.nevo.co.il/law_html/law01/271_001.htm
2. תקנות מס ערך מוסף, התשל"ו-1976, Nevo 271_005. Regs used: 14, 15, 15א, 16, 16א, 18, 20, 21א, 22, 23, 24. https://www.nevo.co.il/law_html/law01/271_005.htm
3. הוראת ביצוע מע"מ 01/2025 (7.12.2025), מודל חשבוניות ישראל, הקצאת מספרי חשבוניות. https://www.gov.il/BlobFolder/policy/inst-071225-1/he/vat_inst-071225-1.pdf
4. מודל חשבוניות ישראל, תיאור ה-API's, מהדורה 2.0, 7.2024 (incl. s.6 PCN874 changes). https://www.gov.il/BlobFolder/generalpage/hor-software-other/he/vat_software-houses-180724.pdf
5. Negative control only: הוראת ביצוע מע"מ 01/2024 (15.8.2024), superseded 15k/10k/5k schedule.

Secondary (ITA text relayed; gov.il HTML was 403 from this machine, re-verify with a browser):
6. Bi-monthly threshold 1,805,000 from 1.1.2027: Kol Zchut periodic-returns page and Stark CPA notice 24.8.2026 (evidence `monthly-threshold-2027`).
7. Detailed-report deferral for individuals (1.1.2026, optional 1.1.2027, 90% by amount, code 77777772): britcpa circular 59.2025.
8. ITA 2026 reporting calendar and weekend rule: Haifa Chamber of Commerce reproduction (15.10.2025).
9. Online filing until the 19th: gov.il service page "reporting-or-payment-of-vat-reports" (search snippet).
10. 18% rate order: capitax summary. with a working browser before publishing: gov.il "סכומים ושיעורים במע"מ" (1,805,000 and 2027 osek patur), "הגשת דיווח מפורט למע"מ" (deferral status), ITA 2027 reporting calendar. Note: the current reg. 18(ג) reads "(בוטלה)"; an older Nevo version block shows a "full deduction then self-use charge" route. Do NOT teach that route.
