---
name: israeli-tax-withholding
description: Israeli tax withholding (nikui mas bemakor) rates, certificates, and calculations. Use when user asks about withholding tax, "nikui mas", withholding certificates, "ishur nikui", tax coordination (tium mas), or needs to calculate withholding amounts. Covers payments to suppliers, freelancers, landlords, and cross-border payments. Do NOT use for employee payroll tax (see israeli-payroll-calculator) or VAT reporting.
license: MIT
---

# Israeli Tax Withholding

## Legal notice

This is a free information tool operated by an AI model. It explains the tax rules and helps you organise your own figures. All of its outputs are produced automatically by an AI model, with no involvement, review, or approval by a tax adviser or accountant. The output is not a tax opinion, not a return prepared by a licensed representative, and not professional advice, but a general calculation and explanation only: it does not examine the full extent of your income or your complete documents. An AI model may err, omit data, or present a wrong conclusion.

Any form or text this tool produces is an automatic draft for your personal preparation only, and is not a filed return. Responsibility for reporting and for paying the tax is yours, the binding computation is the Tax Authority's, and representation before the Tax Authority is reserved to those permitted by law. This tool is not a substitute for advice that takes account of the particular circumstances and needs of each person. Consult a tax adviser or accountant before filing or paying. All use of its output is the user's sole responsibility.


## Instructions

### Step 1: Identify Payment Type and Default Rate
| Payment Type | Hebrew | Default Rate | Section |
|-------------|--------|-------------|---------|
| Services/assets (payee keeps acceptable books, no certificate) | shlumim avur sherutim o nechasim | 20% | reg. 1977 |
| Services/assets (payee without acceptable books, no certificate) | shlumim avur sherutim o nechasim | 30% | reg. 1977 |
| Services (companies, no certificate) | shlumim avur sherutim | 20%, or 30% without acceptable books (reg. 2 draws no individual/company distinction) | reg. 1977 |
| Rent (real estate, where the tenant deducts the rent as a business expense) | schar dira | 35% (uniform, no residential/commercial split) | reg. 1998 |
| Royalties | tamlugim | No separate category in the 1977 regulations: a payment to a resident falls under the 20%/30% services-and-assets rule; a payment to a non-resident is withheld under section 170 | 170 |
| Interest | ribit | 25% to an individual (15% on a non-index-linked asset); the maximum rate to a company (the 23% corporate rate), and the maximum rate when a company pays its substantial shareholder, its employee or its supplier (reg. 6, the top section 121 rate for an individual) | reg. 2005 |
| Dividends | dividendim | To an individual: 25%, 30% to a substantial shareholder. Company to an Israeli-resident company: withheld only where a limited rate applies under any law (reg. 2(א1)) | reg. 2005 |
| Building and haulage work | avodot bniya vehovala | 20%; 17% or 15% with the assessing officer's written approval; 10 points higher without acceptable books | reg. 1973 |
| Agricultural work / agricultural produce | avoda chaklait / tozeret chaklait | 20% / 5%; 10 points higher without acceptable books | reg. 1979 |
| Payments to non-residents | tishlumin letoshvei chutz | **25% to an individual, the 23% corporate rate to a company**, unless the assessing officer sets another rate in writing; see Step 9 | 170 |

For a service/asset payment with no certificate, the statutory default under the 1977 regulations is **20% where the payee keeps acceptable books** (reg. 2(a), the ordinary case) and **30% where the payee does not** (reg. 2(b), the penalty rate for an unverified/no-books payee, not a separate "high" rate; there is no ~47% service-withholding rate). Start from 20% and move to 30% only once you know the payee failed the books-and-returns test. A valid certificate from the assessing officer sets a reduced rate or an exemption for that payee. Rent on real estate that the tenant deducts as a business expense is withheld at a uniform **35%** (there is no separate residential vs. commercial rate); a private residential tenant who cannot deduct the rent is generally not a withholding agent at all.

**Every category has two rates, not one.** The ITA states this as a general rule of the withholding regulations, not a quirk of the services category: "בתקנות לניכוי מס במקור מהכנסות שאינן שכר עבודה נקבעו שיעורים שונים למי שמנהלים ספרים קבילים ומגישים את הדו"ח במועד, ושיעורים גבוהים יותר לסרבנים." So a single quoted rate for any category is incomplete by construction. Always establish the payee's bookkeeping and filing status before quoting a number.

De-minimis: reg. 2(a) excludes a payment for an asset or service **whose value does not exceed the amount fixed in section 2(b) of the Public Bodies Transactions Law, 1976**, which stands at **5,520 NIS**. The test in the regulation is the value of that asset or service, not a running annual total, and neither text says whether the figure is VAT-inclusive, so do not assert that either way. The amount is updated by ministerial notice, so verify the current-year figure.

### Step 2: Check for Withholding Certificate
A valid withholding certificate (ishur nikui mas bemakor) may reduce or eliminate
the withholding:
- Certificate shows: business name, TIN, approved rate, validity period
- **Verify online, shortly before each payment.** Certificates are electronic
  only and are not printed or mailed, and instruction 02/2026 puts the duty to
  check them close to payment on the payer. Confirm today's date falls inside the
  validity shown. Do not assume a calendar year: under that instruction the
  certificates issued for 2026 run from 1.1.2026 (or their issue date, if later)
  to 31.3.2027, with a 1.1.2026 to 31.3.2026 overlap in which the 2025
  certificates stayed valid. A certificate cannot be back-dated
- **Verify:** certificate is genuine, issued by the ITA
- **Online lookup:** verify the payee's certificate status through the ITA's
  gmishurim service (see Reference Links)

### Step 3: Calculate Withholding
```
Payment amount (before VAT): X NIS
Withholding rate: Y% (from certificate, or default)
Withholding amount: X * Y%
Net payment to payee: X - withholding
VAT (if applicable): calculated separately on the full pre-withholding amount
```

### Step 4: Periodic Reporting and Payment (Form 102)
- Supplier withholding is a monthly cycle: reg. 4 of the 1977 regulations
  requires the return and the payment by the 16th of each month for the previous
  month. Withhold at the time you pay, not when the invoice arrives.
- **Form 102** is the periodic deductions report and payment. It summarises the
  wages/payments and the income tax (and, on the National Insurance side, the
  parallel 102) withheld in the period.
- **Deadline: the 16th of each month, not the 15th.** This is in the regulation
  itself: reg. 4 of the 1977 regulations reads "משלם יגיש לפקיד השומה עד היום
  ה-16 לכל חודש דין וחשבון ... וישלם לו באותו מועד את סך כל המס שנוכה". The
  amendment history is explicit that this replaced the 15th, by תק' תשע"ח-2017.
  The 15th is the Bituach Leumi date, and BTL has its own separate form also
  called 102, which is why the two get conflated. Late reporting and late payment
  carry penalties and indexation.
- Reg. 4 names **form 0852** as the per-payee return the payer files on that date
  for service and asset payments. Do not assume Form 102 alone discharges the
  obligation for supplier withholding.

### Step 5: Annual Reconciliation (Form 856)
- **Form 856** is the ANNUAL withholding reconciliation for payments to
  suppliers and service providers. It is a detailed file listing every payee,
  the total paid, and the total withheld during the year, reconciled against the
  Form 102 deposits made through the year.
- **Deadline: 30 April, online.** Section 166(ב) of the Ordinance sets it by
  statute for form 0856 (and 0126 for salaries): "באופן מקוון, עד יום 30 באפריל
  שלאחר שנת המס". Reg. 5(a) of the 1977 regulations still carries an older
  31 March date and names the per-payee 0851 cards. Check for an ITA extension
  notice for the current year before telling a user they are late.
- Workflow: deposit withheld amounts monthly via form 0852 / Form 102 -> at year
  end, compile the per-payee detail file -> submit Form 856.
- Form 856 is separate from the payee's own annual return; it is the payer's
  obligation as the withholding agent.
- **Interest and dividends:** the payer gives the recipient, on request and by
  20 March, a certificate on form 0867 (2005 regulations).
- **Form 0857, the payee's annual certificate.** Reg. 6 of the 1977 regulations
  requires the payer to give every payee a certificate on form 0857 of the
  payments made and the tax withheld in the previous tax year, by 20 March.
  Payees need it to credit the withholding on their own return.
- **Form 126** is the salary-side counterpart: the annual report of employee
  salaries and the tax withheld from them, filed alongside Form 856 on the same
  30 April online date under section 166(ב). A payer with both suppliers and
  employees files both: 856 for suppliers/service providers, 126 for salaries.

### Step 6: Certificate Types
| Certificate | Hebrew | Purpose |
|------------|--------|---------|
| Ishur Nikui Mas BeMakor | ishur nikui mas bemakor | Reduced/zero withholding on payments |
| Ishur Tium Mas | ishur tium mas | Tax coordination for multiple payers/employers |

Withholding on the sale of real estate runs under the Land Taxation Law, not this
regime, and is outside this skill.

### Step 7: How to Obtain a Certificate
1. Apply through the ITA online services (the gmishurim system).
2. Provide: TIN, financial statements, tax returns.
3. Validity is shown online. The 2026 certificates run to 31.3.2027, and
   taxpayers with a clean file are renewed automatically without applying
   (execution instruction 02/2026). A company taxed at the section 126(a) rate may
   ask that withholding not exceed that rate.
4. Check the dates each time rather than assuming a January-December year.

### Step 8: Who Is a Mandatory Withholder, and Which Payments Are Covered

**The size test is in the order, not in the regulations.** The 1977 regulations
define the payments they cover by reference to צו מס הכנסה (קביעת תשלומים בעד
שירותים או נכסים כהכנסה), תשל"ז-1977, and that order lists who is a withholding
payer: the State and public bodies, government companies, financial
institutions, hospitals and similar bodies, and any business **required to keep
double-entry books or whose turnover exceeded the amount in Schedule A** to the
order. Section 2א of the order then excludes payments by an individual, a
partnership of individuals, or a company outside a group, where in each of the
three relevant tax years turnover did not exceed the Schedule A amount AND they
were not required to keep double-entry books. The last year shown in the
consolidated Schedule A on Nevo is 2018, at 5,300,000 NIS; the amount is updated
by order, so confirm the current figure. Check both limbs before telling a small
payer they are outside the regime, and never on turnover alone:

- Section 164 of the Ordinance imposes the duty, and the ITA describes the
  scoping mechanism as an order: "קביעת סוגי המנכים וסוגי
  התשלומים נעשית בצו של שר האוצר ובאישור ועדת הכספים של הכנסת", under which
  "נקבעה סדרה של תשלומים ומשלמים שחלה עליהם חובת הניכוי במקור". The withholding
  family is therefore an **open, order-by-order set**, not a closed list.
- The 1977 regulations add one more exit: an individual or a partnership of
  individuals whom **the assessing officer has approved in writing** as not being
  a payer for a given tax year following a material contraction of their
  business.
- Certain **recipients** are outside the regime under Schedule A to the same
  regulations (the State, Bank of Israel, a local authority, the State
  Comptroller, an association of towns, the National Insurance Institute, a
  religious council, the Jewish Agency, the World Zionist Organization, the
  Airports Authority, KKL, the Employment Service, Keren Hayesod, the
  Administrator General, a banking institution, an insurer, and a house-committee
  representation for common-property maintenance charges).

### Step 8a: The Full Set of Withheld Payment Types
The categories above are the ones this skill prices. They are **not** the whole
statutory set. Section 166(c) of the Ordinance defines "הכנסה חבת ניכוי" by
listing the section 164 payment types: insurance commission; fees of artists,
examiners, lecturers, providers of office services, directors and sportspeople;
authors' fees; **payment for agricultural work or agricultural produce**;
building and haulage work; clothing, metal, electrical and electronics work;
**diamond processing or diamond trading**; and payments for services or assets.
The ITA repeats the same list in its taxpayer guide, adding interest, dividends,
work-injury and reserve-duty payments, indirect-damage compensation, and capital
gains including traded securities.

**Do not invent a rate for a category this skill does not price.** Building and
haulage (reg. 1973) and agricultural work/produce (reg. 1979) are now priced in
Step 1 from their own regulations. Diamonds, insurance commission, and the fees of
artists, lecturers, directors and sportspeople are confirmed statutory categories
whose operative rates sit in their own regulations under section 164 and are not
reproduced here.
The ITA declines to publish a consolidated rate table at all and directs users to
the live per-payee figure: "מידע זמין ומעודכן לגבי שיעורי ניכוי מס במקור יכולים
המנכים והמנוכים לקבל ישירות מאתר רשות המסים." Query the payee's own rate by
company/dealer number at the ITA lookup in Reference Links, and treat that result
as authoritative over any table.

### Step 9: Payments to Non-residents (Section 170)
- **Rate.** Section 170(a) fixes it in the statute: 25% where the payee is an
  individual, and the corporate rate under section 126 (23%) where the payee is a
  company, "או שיעור אחר שיקבע להם פקיד השומה בהודעה בכתב". The assessing officer
  may also allow payment with no withholding.
- **Scope.** Section 170 covers income not already withheld under sections 161 and
  164. Dividends and interest to a non-resident are withheld under the 2005
  regulations instead (dividends 25%, or 30% to a substantial shareholder).
- **The bank is a payer too.** Section 170 treats the financial institution
  that transfers the payment as a payer, unless it holds an assessing-officer
  approval exempting it, so the transferring bank carries the withholding duty
  too.
- **Deadline.** Tax withheld under section 170(a) is paid to the assessing
  officer within 7 days of withholding, with a report (section 171). This is
  not the monthly 16th cycle.
- **Two relief routes, not one.** Form 2513/2 is a bank declaration for exempt
  payment types only: investment in shares, real estate or tangible assets
  abroad, loans, options, investment in a foreign partnership, and (since the
  ITA letter of 15.12.2025) digital assets bought on a KYC exchange, for payees
  resident in a treaty or CRS country. The form itself says every other payment
  type goes through the ordinary route under execution instruction 34/93, i.e.
  the assessing officer. Service fees, licences and royalties are in that second
  group.
- **Services performed wholly abroad.** Instruction 34/93 s.3.9 carries a relief
  for services "שניתנו ובוצעו במלואם בחו"ל" by foreign providers; the ITA's
  16.12.2025 supplement raised its cap to $250,000 per payer. That supplement is
  titled as an update on "special companies" (חברות מיוחדות), an approval status
  under 34/93, and it stresses that such a company stays liable for the tax if it
  withheld less than required. Read the instruction's conditions before relying
  on either.
- **Payer bears the tax (gross-up).** If the contract fixes the net amount the
  vendor receives and you pay the Israeli tax on top, the arithmetic is: tax =
  net x rate / (1 - rate), e.g. 10,000 net at 23% gives 2,987.01 of tax on a
  12,987.01 base. `--payer-bears-tax` computes it. This is arithmetic, not an
  ITA instruction; confirm the base with an advisor or the assessing officer.
- **Year-end accruals.** Under section 18(ה), an expense to a non-resident that is
  subject to withholding under section 164 or 170 is deductible in its year only
  if paid, or the tax withheld, no later than three months after year-end, and
  the tax transferred within 7 days of withholding.

## Examples

### Example 1: Payment to Freelancer
User says: "I need to pay a freelancer 10,000 NIS for consulting"
Result: With no certificate, the default for a freelancer who keeps acceptable
books and files on time is 20% = 2,000 NIS withheld, 8,000 NIS net payment, plus
1,800 NIS VAT (if the payee is an osek murshe). The 30% rate (3,000 NIS withheld,
7,000 NIS net) applies only where the payee cannot show the assessing officer
that they kept acceptable books and filed their returns. Do not open at 30%: for
an ordinary compliant freelancer that over-withholds by half. Recommend asking
the freelancer whether they hold a reduced-rate or exemption certificate, and
check their status on the ITA lookup. A payment for a service worth no more than
5,520 NIS is outside the duty altogether (the de-minimis in Step 1).

### Example 2: Certificate Check
User says: "A vendor gave me a 0% withholding certificate, is it valid?"
Result: Check the payee on the ITA gmishurim lookup shortly before paying, confirm
today falls inside the validity shown there and that the vendor's TIN matches.
Certificates are electronic, so the online record, not a paper copy, decides.

### Example 3: Cross-border Payment
User says: "I need to pay a US company for software licenses"
Result: The payee is a company, so the section 170 default is the 23% corporate
rate, not 25% (25% is the rate for a non-resident individual). The tax is paid to
the assessing officer within 7 days of withholding (section 171). A reduced
treaty rate is NOT automatic: it runs through the assessing officer under
execution instruction 34/93, because software licences are not among the payment
types the bank declaration form 2513/2 accepts. Whether a software payment is a
royalty, a service or a purchase changes the treatment, so have a tax advisor
classify it before relying on a treaty rate.

## Bundled Resources

### Scripts
- `scripts/calculate_withholding.py` -- Calculates Israeli tax withholding (nikui mas bemakor) amounts for services (with and without books), rent, interest, dividends, building and haulage, agriculture, and non-resident payments split into `non_resident_individual` (25%) and `non_resident_company` (23%). Categories with no single sourced rate (royalties, company-to-company dividends, related-party interest, diamonds, insurance commission, prizes) return a routing message instead of a number. Applies the 5,520 NIS de-minimis to service/asset payments, drops the VAT line for interest, dividends, non-residents, residential rent (exempt, VAT Law s.31(1)) and agricultural produce (unprocessed fruit and vegetables of the types the Finance Minister set are zero-rated, s.30(a)(13); other produce may carry VAT, so pass `--with-vat`), grosses up with `--payer-bears-tax`, and supports certificate rates. Run: `python scripts/calculate_withholding.py --help`

### References
- `references/withholding-rates.md` -- Default withholding rates by payment type under Section 164 (including rent) and Section 170 (non-residents), including rates for individuals, companies, major shareholders, and non-residents. Consult when determining the correct default rate for a payment.
- `references/certificate-guide.md` -- Guide to Israeli withholding certificates: types (Ishur Nikui Mas BeMakor, Ishur Tium Mas), application process, validity periods, and verification through the ITA gmishurim service. Consult when a vendor presents a withholding certificate or when guiding users through the certificate application process.

## Recommended MCP Servers
- **israel-law** -- look up the Income Tax Ordinance sections (164, 170) and the cash-use law text when you need the primary legal source behind a withholding rule.

## Gotchas
- Israeli withholding rates are set by the regulations and by the ITA per business, not as one flat rate. With no certificate the service/asset default is **20% where the payee keeps acceptable books and 30% where they do not**; there is no ~47% service-withholding rate (that figure is not in the regulations, do not cite it). An established payee may hold a reduced-rate or exemption certificate. Do not hardcode a single rate.
- **The common case is 20%, not 30%.** The 30% figure is the sanction for a payee who could not prove acceptable books and timely returns. Defaulting to it silently over-withholds an ordinary compliant supplier by half and pushes them into a refund claim. `scripts/calculate_withholding.py --type services` uses 20%; use `--type services_no_books` for the sanction rate.
- The skill prices only some of the section 164 categories. Diamond processing and trading, insurance commission, artists, examiners, lecturers, directors and sportspeople are all statutory withholding categories whose rates are NOT in this skill. If asked about one, say the category exists, name the statute, and send the user to the per-payee lookup. Never estimate the rate.
- Withholding exemption/reduction certificates (ishur nikui mas bemakor) are time-limited but no longer track the calendar year: the 2026 certificates run to 31.3.2027. Read the dates on the certificate; do not tell a user it expired on 31 December.
- When paying a foreign contractor, Israel requires withholding unless a tax treaty provides a reduced rate. Do not apply domestic rates to international payments or skip withholding entirely. And do not quote a flat 25%: that is the individual rate; a foreign company is withheld at the 23% corporate rate.
- A payer who withholds and does not remit, or never withholds, is assessed for the tax itself (sections 167 and 173) and in suitable cases faces criminal sanctions (sections 218 or 219). Losing the expense deduction is on top of that, not instead of it.
- Withholding on rent that the tenant deducts as a business expense is a uniform **35%**, there is NO separate residential vs. commercial rate, and no "30% residential" rate exists. A private residential tenant who cannot deduct the rent is generally not a withholding agent at all. The reduced/zero rate applies only with a valid certificate.
- **2026 black-market legislation (Income Tax Circular 3/2026, 9.2.2026).** Three separate limbs, with different triggers and dates. (1) Section 32A: from payments made on 1.1.2026, an expense subject to withholding is allowed only if the withheld tax was actually transferred to the assessing officer, not just reported, unless the payee paid the tax, the tax was withheld under an assessing-officer approval, or no withholding duty applied; the rule does not apply to a mainly private expense such as a home rented with a business corner. (2) Section 32(16א): a cash-law breach disallows the expense only once a financial sanction has actually been imposed, for payments from 1.1.2026; the parallel VAT limb, section 38(א2), denies input VAT on invoices issued from 1.1.2026 on the same sanctioned-breach condition. **A withholding failure alone does not deny input VAT.** (3) Section 32(18): from expenses paid on 1.8.2025, no deduction without an allocation number where one is required; the threshold fell to 10,000 NIS from 1.1.2026 and to 5,000 NIS from 31.5.2026. The cash-use law caps cash at 6,000 NIS in ANY transaction where a dealer (osek) is a party, on either side (sections 2(א) and 2(ג)), so a dealer taking 10,000 in cash from a private consumer is already in breach. The 15,000 ceiling applies only when NEITHER side is a dealer. **And the ceiling is not the whole rule: permitted cash is the LOWER of the scheduled amount or 10% of the transaction price**, so on a 20,000 NIS deal the real cash limit is 2,000, not 6,000. Treat a missed withholding or a cash-law breach as a deduction risk, not just a reporting issue.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Israel Tax Authority (ITA) | `https://www.gov.il/he/departments/israel_tax_authority` | Default withholding rates per activity, annual updates |
| Withholding certificate lookup (gmishurim) | `https://www.gov.il/he/service/itc-gmishurim` | Verify a vendor's certificate status and validity period |
| Per-payee rate lookup (misim.gov.il) | `https://www.misim.gov.il/gmishurim/frmInputMekabel.aspx` | The authoritative operative rate for a specific payee, queried by company/dealer number. Use this instead of a table whenever the payee is known |
| ITA taxpayer guide, chapter 8 section 9 | `https://www.gov.il/BlobFolder/generalpage/income-tax-guide-knowyourright/he/Guides_IncomeTax_da-2025.pdf` | The two-tier rate rule, the order-based scoping of withholders, and the ITA's own list of withheld income types |
| gmishurim direct lookup tool | `https://taxinfo.taxes.gov.il/gmishurim/firstPage.aspx` | Direct online check of a payee's withholding/bookkeeping status |
| Income Tax Ordinance s.164/170 | `https://www.nevo.co.il/law_html/law01/255_001.htm` | Legal basis for withholding on services, rent, non-residents |
| ITA Circular 3/2026 (black-money amendments) | `https://www.gov.il/BlobFolder/policy/professional-directives-090226-1/he/IncomeTax_professional-directives-090226-1.pdf` | The three disallowance limbs, their triggers and commencement dates |
| ITA execution instruction 02/2026 | `https://www.gov.il/BlobFolder/policy/inst-02-2026/he/IncomeTax_inst-02-2026.pdf` | Certificate validity period and automatic renewal |
| Form 2513/2 (bank declaration, non-resident) | `https://www.bankhapoalim.co.il/sites/default/files/media/PDFS/declaration_of_overseas_transfer_exemption_from_tax2513_2.pdf` | The closed list of payment types the declaration route accepts |
| ITA publications index | `https://www.gov.il/he/collectors/publications?OfficeId=c0d8ba69-e309-4fe5-801f-855971774a90` | Current forms (856, 102, 0852), circulars and treaty publications. The two direct gov.il links this table used to carry, for form 856 and for the taxation agreements guide, both 404 as of 2026-08-19, so search here instead |

## Troubleshooting

### Error: "Certificate expired"
Cause: the validity shown for the certificate has passed. For the 2026
certificates, instruction 02/2026 set validity to 31.3.2027, not to 31 December;
read the dates for the current year's certificates rather than assuming either.
Solution: check the payee's current status on the ITA lookup (clean files are
renewed automatically), and ask the vendor for the new certificate if none shows.

### Error: "Wrong withholding rate applied"
Cause: using the default rate when a certificate exists, or vice versa; or
confusing the with-books (20%) and no-books (30%) service defaults.
Solution: always request the certificate before the first payment, apply the
certificate rate only during its validity period, and for a no-certificate
service payment use 20% if the payee keeps acceptable books, 30% if they do not.

### Error: "Late reporting penalty"
Cause: the periodic deductions report (Form 102) was not filed by the 16th.
Solution: file immediately. Penalties and indexation apply for late reporting and
late payment of withheld amounts. Remember the separate annual Form 856
reconciliation (30 April, online, under section 166(ב)).

### Error: "Deduction disallowed by the tax office"
Cause: under Circular 3/2026, an expense subject to withholding is disallowed
when the withheld tax was not both reported and transferred (section 32A, from
1.1.2026). A cash-use breach (cash over 6,000 NIS, or over 10% of the transaction
price if that is lower, in any transaction where a dealer is a party) disallows
the expense and the input VAT only once a financial sanction has been imposed.
Solution: withhold, report on form 0852 / Form 102 and actually pay the tax by the
16th, keep the per-payee detail for Form 856, and pay above-threshold amounts by
non-cash means.
