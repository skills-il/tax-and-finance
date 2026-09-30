# Israeli Tax Withholding Rates Reference

## Default Rates by Payment Type

These are the no-certificate defaults. A valid certificate from the assessing
officer sets a reduced rate or an exemption for that payee; this file does not
guess what that rate typically is.

### Section 164, Income Payments
| Payment Type | Rate | Notes |
|-------------|------|-------|
| Services/assets (individual, acceptable books, no certificate) | 20% | Base rate under the 1977 regulations |
| Services/assets (individual, no acceptable books, no certificate) | 30% | Penalty rate for an unverified / no-books payee |
| Services (company, no certificate) | 20% base / 30% without acceptable books | reg. 2 draws no individual/company distinction. The 20-30% range often quoted reflects the assessing officer's classification on the certificate, not a different statutory default |
| Interest to an individual | 25% | 15% where the asset is not index-linked (regs. 4 and 5 of the 2005 regulations) |
| Interest to a company | Maximum rate (23%) | Reg. 7 of the 2005 regulations; "maximum rate" for a company is the s.126(a) corporate rate |
| Interest to a company's substantial shareholder, employee or supplier | Maximum rate | Reg. 6 of the 2005 regulations: the top s.121 rate for an individual. Shareholder-loan interest is the common case |
| Dividends | 25% | To an individual, resident or non-resident. A company paying an Israeli-resident company withholds only where a limited rate applies under any law (reg. 2(א1)) |
| Dividends (major shareholder) | 30% | Substantial shareholder: holding 10% or more, at any time in the 12 months before payment |
| Building and haulage work | 20% | Regs. 1973, reg. 2(a). 17% (one to four sub-payees) or 15% (five or more) with the assessing officer's written approval, reg. 2(b). Without acceptable books reg. 2(c) sets "שיעור הגדול ב-10% מהשיעורים", i.e. 30% on the 20% base |
| Agricultural work / agricultural produce | 20% / 5% | Regs. 1979. 10 points higher without acceptable books |
| Gambling, lotteries and prizes | Not encoded | Withheld under s.164 by reference to s.2A. The substantive rate under s.124B is 35% with no exemption, relief, deduction, credit or offset, except an exemption under s.9(28) or a deduction under s.17(11). The operative withholding rate sits in its own regulations; look it up per payee. The 25% figure previously shown here was unsourced and has been removed |

For a no-certificate service/asset payment, the statutory default is 20% where
the payee keeps acceptable books (reg. 2(a), the ordinary case) and 30% where
they do not (reg. 2(b), the sanction rate). There is no ~47% service-withholding
rate; that figure does not appear in the regulations.

**Two rates per category is the general rule, not a services-only quirk.** The
ITA states it directly: "בתקנות לניכוי מס במקור מהכנסות שאינן שכר עבודה נקבעו
שיעורים שונים למי שמנהלים ספרים קבילים ומגישים את הדו"ח במועד, ושיעורים גבוהים
יותר לסרבנים." Treat any single-rate row below as the compliant-payee rate and
establish the payee's status before applying it.

### Rent (s.164), royalties, non-residents (s.170) and unpriced categories
| Payment Type | Rate | Notes |
|-------------|------|-------|
| Rent (real estate the tenant deducts as a business expense), s.164, 1998 regulations | 35% | Uniform, no residential/commercial split; a private residential tenant who cannot deduct the rent is generally not a withholding agent |
| Royalties | See note | The 1977 regulations create no separate royalties rate. To a resident, use the 20%/30% services-and-assets default; to a non-resident, section 170 applies. The figure often quoted for royalties is simply the corporate tax rate applied to a non-resident company, not a distinct withholding category |
| Payments to non-residents | 25% individual / 23% company | s.170(a), statutory, unless the assessing officer sets another rate in writing. Paid within 7 days of withholding (s.171). Covers income not withheld under s.161/164, so dividends and interest follow the 2005 regulations. Relief: Form 2513/2 bank declaration for its closed list of capital payment types only; everything else (services, licences, royalties) through the assessing officer under execution instruction 34/93 |
| Insurance commissions | Not encoded | A statutory category (Ordinance s.166(c)(1), under s.164). The 20% figure in circulation is not verified against a primary source here, so it is not asserted. Look it up per payee |

## Thresholds

- **De-minimis floor:** reg. 2(a) of the 1977 regulations excludes a payment for
  an asset or service whose value does not exceed the amount fixed in section
  2(b) of the Public Bodies Transactions Law, 1976, currently **5,520 NIS**. The
  test is the value of that asset or service, not a running annual total, and
  neither text states whether the amount is VAT-inclusive, so do not assert that
  either way. The figure is updated by ministerial notice; verify the current
  year.
- **Who must withhold is set by the order, and it does include a size test.**
  The 1977 regulations cover payments as defined in צו מס הכנסה (קביעת תשלומים
  בעד שירותים או נכסים כהכנסה), תשל"ז-1977. That order lists the payers: the State
  and public bodies, government companies, financial institutions, hospitals and
  similar bodies, and any business required to keep double-entry books or whose
  turnover exceeded the Schedule A amount. Section 2א of the order excludes
  payments by an individual, a partnership of individuals or a company outside a
  group where, in each of the three relevant years, turnover did not exceed the
  Schedule A amount and there was no double-entry duty. The last year in the
  consolidated Schedule A on Nevo is 2018, at 5,300,000 NIS; confirm the current
  figure. The 1977 regulations add a further exit for an individual or
  partnership of individuals whom the assessing officer approved **in writing**
  as not a payer for a year after a material contraction of their business.
- **Schedule A recipients are outside the regime**: the State, Bank of Israel, a
  local authority, the State Comptroller, an association of towns, the National
  Insurance Institute, a religious council, the Jewish Agency, the World Zionist
  Organization, the Airports Authority, KKL, the Employment Service, Keren
  Hayesod, the Administrator General, a banking institution, an insurer, and a
  house-committee representation for common-property maintenance charges.

## Tax Treaty Reduced Rates

No treaty rate table is carried here any more. The table previous versions
showed could not be re-verified against the treaty texts for two cycles (its only
cited index page went dead), and some rows had already been found stale. A treaty
rate the skill cannot source is exactly the kind of number an agent will quote
confidently, so it was removed rather than carried a third time.

To find a rate: read the specific treaty (the ITA publishes each one as a PDF on
gov.il, reachable from the ITA publications index), identify the article for the
payment type (dividends, interest, royalties, business profits), and remember that
the reduced rate is not self-executing: for services, licences and royalties it
runs through the assessing officer under execution instruction 34/93.

## Reporting Forms
- **Deadline: the 16th, not the 15th.** Reg. 4 of the 1977 regulations: "משלם
  יגיש לפקיד השומה עד היום ה-16 לכל חודש דין וחשבון ... וישלם לו באותו מועד את
  סך כל המס שנוכה". This replaced the 15th by תק' תשע"ח-2017. The 15th is the
  Bituach Leumi date, and BTL has its own separate form also called 102.
- **Form 0852:** the per-payee periodic return reg. 4 names for service and asset
  payments, filed and paid on that same 16th.
- **Form 102:** the periodic deductions report and payment, on the same 16th
  for income-tax deductions. Reg. 4 sets supplier withholding on a monthly cycle.
- **Form 0857:** the annual certificate the payer gives each payee for the previous tax year, due by 20 March under reg. 6 of the 1977 regulations.
- **Form 0867:** the certificate for interest and dividend recipients, on
  request, by 20 March (2005 regulations).
- **Form 856:** annual per-payee withholding reconciliation for supplier and
  service-provider payments, online by 30 April under Ordinance s.166(ב). Reg.
  5(a) of the 1977 regulations still carries an older 31 March date and names the
  per-payee 0851 cards. Check for a current-year ITA extension notice.
- **Form 126:** the salary-side annual withholding report (employees), filed
  alongside Form 856. 856 covers
  suppliers/service-providers; 126 covers salaries, a payer with both files both.

## The full statutory category list (s.166(c), under s.164)

This skill prices only some of these. The rest are real categories whose rates
live in their own regulations and are NOT reproduced here. Never estimate one.

Insurance commission; fees of artists, examiners, lecturers, providers of office
services, directors and sportspeople; authors' fees; **payment for agricultural
work or agricultural produce**; building and haulage work; clothing, metal,
electrical and electronics work; **diamond processing or diamond trading**;
payments for services or assets. The ITA's taxpayer guide repeats the list and
adds interest, dividends, work-injury and reserve-duty payments, indirect-damage
compensation, and capital gains including traded securities.

The ITA does not publish a consolidated rate table and directs users to the live
per-payee figure: "מידע זמין ומעודכן לגבי שיעורי ניכוי מס במקור יכולים המנכים
והמנוכים לקבל ישירות מאתר רשות המסים." Query by company/dealer number at
`https://www.misim.gov.il/gmishurim/frmInputMekabel.aspx` and treat that result
as authoritative over any table on this page.
