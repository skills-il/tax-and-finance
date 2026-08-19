# Domain checklist: Israeli withholding at source (ניכוי מס במקור)

Anchor for the Expert Review. Last refreshed 2026-08-19 (v1.5.0) against the
Income Tax Ordinance, the 1977 services/assets withholding regulations, and the
ITA taxpayer guide "דע זכויותיך וחובותיך 2025".

## Must cover (core)

| Item | Why it is core | Source | Status |
|---|---|---|---|
| Services/assets base rate 20% with acceptable books | reg. 2(a), the ordinary case for every freelancer and supplier | תקנות מס הכנסה (ניכוי מתשלומים בעד שירותים או נכסים), תשל"ז-1977, reg. 2(a) | Covered |
| Services/assets sanction rate 30% without acceptable books | reg. 2(b); must be presented as the exception, not the default | same, reg. 2(b) | Covered |
| Two-tier rate structure as a general rule across categories | The ITA states it for the withholding regulations as a whole, so a one-rate answer is wrong by construction | ITA guide ch. 8 s.9(b) | Covered (v1.5.0) |
| De-minimis keyed to the value of the asset or service | reg. 2(a) incorporates s.2(b) of the Public Bodies Transactions Law, 1976 (5,520 NIS). It is not a cumulative annual test | reg. 2(a) + חוק עסקאות גופים ציבוריים s.2(b) | Covered (v1.5.0) |
| Rent 35% uniform where the tenant deducts it as a business expense | reg. 1998; the residential/commercial split is a common false belief | תקנות 1998 | Covered |
| Interest 25%, dividends 25%, substantial shareholder 30% | 2005 regulations; s.88 defines substantial shareholder at 10% or more | 2005 regs | Covered |
| Periodic return and payment by the 16th, not the 15th | reg. 4, amended from the 15th by תק' תשע"ח-2017. The 15th is the Bituach Leumi date. A one-day error is a late-filing penalty | reg. 4 | Covered (v1.5.0) |
| Form 0852 as the per-payee periodic return | Named in reg. 4; Form 102 alone does not discharge supplier withholding | reg. 4 | Covered (v1.5.0) |
| Annual reconciliation 856 and 126 by 30 April, commonly extended | ITA guide; the extension is announced most years | ITA guide | Covered |
| Who is a mandatory withholder | No turnover threshold exists. s.164 scopes withholders and payments by ministerial order with Knesset Finance Committee approval; the 1977 exit is a written assessing-officer approval | s.164; 1977 regs reg. 1 | Covered (v1.5.0) |
| Schedule A exempt recipients | A payment to the State, a local authority, BTL, a bank or an insurer is outside the regime entirely | 1977 regs, תוספת א | Covered (v1.5.0) |
| The full statutory category list | The skill prices a subset; a user asking about agriculture, diamonds, artists or lecturers must not get a made-up rate | Ordinance s.166(c); ITA guide נספח א s.87 | Covered (v1.5.0), named without rates |
| Per-payee live lookup as the authority over any table | The ITA declines to publish a consolidated rate table | ITA guide ch. 8 s.9(b) | Covered (v1.5.0) |
| Certificates reduce or zero the rate; annual validity | Practical first question on every payment | ITA gmishurim service | Covered |
| Circular 3/2026 deduction disallowance and the cash-use law | A missed withholding now costs the expense deduction, not just a penalty | חוזר מס הכנסה 3/2026; חוק לצמצום השימוש במזומן | Covered |

## Should cover (advanced)

| Item | Status |
|---|---|
| Non-resident withholding under s.170 and treaty documentation | Covered, hedged to "commonly applied at 25%" |
| Reduction/exemption certificates set per taxpayer by the assessing officer, general or per-withholder, refused where collection deficiencies exist | Partially covered; the per-withholder variant is not spelled out |
| Rates for agricultural work/produce, diamonds, insurance commission, prizes | **Not covered by design.** Categories named, rates deliberately not asserted, routed to the per-payee lookup. Reopen when the specific תקנות under s.164 can be cited |
| Penalty for failing to give the payee the required certificates | Not covered; the ITA guide notes "צפוי לקנס" |

## Out of scope (explicit)

| Item | Rationale | Reviewed |
|---|---|---|
| Employee payroll withholding from salary | Belongs to `israeli-payroll-calculator`. An ordinary user WOULD ask, and the description routes them there explicitly, so this survives the re-litigation test | 2026-08-19 |
| VAT computation and reporting | Belongs to `israeli-vat-reporting`. VAT appears here only as a separate line beside the withholding, which is the part users conflate | 2026-08-19 |
| Real-estate purchase-tax withholding mechanics | Named as a certificate type only; the substantive rules belong to a property skill. A user asking would get the certificate name and a pointer, not silence | 2026-08-19 |

## Authoritative sources

- תקנות מס הכנסה (ניכוי מתשלומים בעד שירותים או נכסים), תשל"ז-1977, `https://www.nevo.co.il/law_html/law01/255_374.htm`
- פקודת מס הכנסה (s.164, s.166, s.124ב, s.2א, s.170), `https://www.nevo.co.il/law_html/law01/255_001.htm`
- חוק עסקאות גופים ציבוריים s.2(ב), `https://www.nevo.co.il/law_html/law01/271_046.htm`
- ITA taxpayer guide 2025, `https://www.gov.il/BlobFolder/generalpage/income-tax-guide-knowyourright/he/Guides_IncomeTax_da-2025.pdf`
- Per-payee rate lookup, `https://www.misim.gov.il/gmishurim/frmInputMekabel.aspx`
