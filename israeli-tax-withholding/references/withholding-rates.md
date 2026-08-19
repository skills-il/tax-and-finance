# Israeli Tax Withholding Rates Reference

## Default Rates by Payment Type

These are the no-certificate ITA defaults. A valid withholding certificate
typically brings the rate down to 0-5%.

### Section 164, Income Payments
| Payment Type | Rate | Notes |
|-------------|------|-------|
| Services/assets (individual, acceptable books, no certificate) | 20% | Base rate under the 1977 regulations |
| Services/assets (individual, no acceptable books, no certificate) | 30% | Penalty rate for an unverified / no-books payee |
| Services (company, no certificate) | 20% base / 30% without acceptable books | reg. 2 draws no individual/company distinction. The 20-30% range often quoted reflects the assessing officer's classification on the certificate, not a different statutory default |
| Interest | 25% | Bank and non-bank interest |
| Dividends | 25% | Standard shareholders |
| Dividends (major shareholder) | 30% | Substantial shareholder: holding 10% or more |
| Gambling, lotteries and prizes | Not encoded | Withheld under s.164 by reference to s.2A. The substantive rate under s.124B is 35% with no exemption, relief, deduction, credit or offset. The operative withholding rate sits in its own regulations; look it up per payee. The 25% figure previously shown here was unsourced and has been removed |

For a no-certificate service/asset payment, the statutory default is 20% where
the payee keeps acceptable books (reg. 2(a), the ordinary case) and 30% where
they do not (reg. 2(b), the sanction rate). There is no ~47% service-withholding
rate; that figure does not appear in the regulations.

**Two rates per category is the general rule, not a services-only quirk.** The
ITA states it directly: "בתקנות לניכוי מס במקור מהכנסות שאינן שכר עבודה נקבעו
שיעורים שונים למי שמנהלים ספרים קבילים ומגישים את הדו"ח במועד, ושיעורים גבוהים
יותר לסרבנים." Treat any single-rate row below as the compliant-payee rate and
establish the payee's status before applying it.

### Section 170, Special Payments
| Payment Type | Rate | Notes |
|-------------|------|-------|
| Rent (real estate the tenant deducts as a business expense) | 35% | Uniform, no residential/commercial split; a private residential tenant who cannot deduct the rent is generally not a withholding agent |
| Royalties | See note | The 1977 regulations create no separate royalties rate. To a resident, use the 20%/30% services-and-assets default; to a non-resident, section 170 applies. The figure often quoted for royalties is simply the corporate tax rate applied to a non-resident company, not a distinct withholding category |
| Payments to non-residents | Section 170 rate, commonly 25% | Treaty relief is NOT self-executing: a reduced rate or exemption needs prior approval from the assessing officer |
| Insurance commissions | Not encoded | A statutory category (Ordinance s.166(c)(1), under s.164). The 20% figure in circulation is not verified against a primary source here, so it is not asserted. Look it up per payee |
| Building and haulage work | Not encoded | Its own statutory category (Ordinance s.166(c)(5), under s.164) with its own regulations. The 30% figure previously shown here was unsourced and has been removed. For a plain service or asset payment to a contractor, use the 20%/30% services default |

## Thresholds

- **De-minimis floor:** reg. 2(a) of the 1977 regulations excludes a payment for
  an asset or service whose value does not exceed the amount fixed in section
  2(b) of the Public Bodies Transactions Law, 1976, currently **5,520 NIS**. The
  test is the value of that asset or service, not a running annual total, and
  neither text states whether the amount is VAT-inclusive, so do not assert that
  either way. The figure is updated by ministerial notice; verify the current
  year.
- **The 1977 regulations contain no turnover threshold for becoming a withholding agent.** Do not
  tell a payer they are below one. Under s.164 the classes of withholders and of
  payments are fixed by an order of the Finance Minister with Knesset Finance
  Committee approval, so the family is open and order-by-order. In the 1977
  regulations "משלם" is any person making service/asset payments, except an
  individual or partnership of individuals whom the assessing officer has
  approved **in writing** as not a payer for a given year after a material
  contraction of their business.
- **Schedule A recipients are outside the regime**: the State, Bank of Israel, a
  local authority, the State Comptroller, an association of towns, the National
  Insurance Institute, a religious council, the Jewish Agency, the World Zionist
  Organization, the Airports Authority, KKL, the Employment Service, Keren
  Hayesod, the Administrator General, a banking institution, an insurer, and a
  house-committee representation for common-property maintenance charges.

## Tax Treaty Reduced Rates (Common)
| Country | Dividends | Interest | Royalties |
|---------|-----------|----------|-----------|
| USA | 12.5-25% | 17.5% | 15% |
| UK | 5% (holding 10%+) / 15% | 5% bank / 10% | **0%** |
| Germany | 5% / 10% | 0% / 5% | 0% |
| France | 10-15% | 10% | 10% |
| Canada | 5% (holding 25%+) / 15% | 10% | 10% |

NOTE: Treaty rates require proper documentation and forms. Always verify the
specific treaty provision before relying on a row. The gov.il treaty index URL
this table used to cite, the taxation agreements guide page, returns
404 as of 2026-08-19 and no replacement index was located this cycle, so these
rows are carried forward from the v1.4.0 verification and are **not
re-verified**. Treat them as a prompt to read the treaty, not as an authority.

## Withholding Certificate Rates
Businesses can apply for reduced rates:
- 0%, clean tax record, established business
- 2%, most common reduced rate
- 5%, standard reduced rate
- 10%, moderate reduction
- Custom rate based on tax assessment

## Reporting Forms
- **Deadline: the 16th, not the 15th.** Reg. 4 of the 1977 regulations: "משלם
  יגיש לפקיד השומה עד היום ה-16 לכל חודש דין וחשבון ... וישלם לו באותו מועד את
  סך כל המס שנוכה". This replaced the 15th by תק' תשע"ח-2017. The 15th is the
  Bituach Leumi date, and BTL has its own separate form also called 102.
- **Form 0852:** the per-payee periodic return reg. 4 names for service and asset
  payments, filed and paid on that same 16th.
- **Form 102:** the periodic deductions report and payment (monthly or
  bi-monthly), on the same 16th for income-tax deductions.
- **Form 856:** annual per-payee withholding reconciliation for supplier and
  service-provider payments, due April 30 of the following year (commonly
  extended by ITA notice, e.g. to end-May/June).
- **Form 126:** the salary-side annual withholding report (employees), filed
  alongside Form 856 with the same April 30 baseline deadline. 856 covers
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
