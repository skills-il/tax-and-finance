# Domain Coverage Checklist - israeli-hon-declaration-preparer

Generated: 2026-09-08

Sources: ITA form 1219 PDF (new version, 7 form pages + 8 pages of official filling
instructions, extracted with pdftotext from the gov.il blob), ITA Deputy Director
(Assessment and Audit) circular 2025-000538 of 05/05/2025 launching the digital filing
system, the text of פקודת מס הכנסה [נוסח חדש] as published by gov.il (sections 135, 143,
155, 188, 215, 216, 220, 224), Hebrew Wikipedia entry on הצהרת הון, CPA-firm category
pages of זיו שיפר ושות' and שטיינמץ עמינח.

NOTE on Step A: Kol Zchut has NO dedicated הצהרת הון page (its tax hub covers the annual
return, not the capital declaration), so the aggregator role was filled by Hebrew Wikipedia
plus two CPA firm guides. The complete named taxonomy came from the form's own instruction
pages, which enumerate every section explicitly.

## Must cover (core)

### Trigger, scope, dates

- [ ] Statutory trigger: a declaration is owed ONLY on a written demand under s.135(1)(a) -
  "רשאי פקיד השומה לדרוש ממנו בהודעה בכתב למסור לו כל דו"ח שיצויין בהודעה, ובכלל זה דו"ח על
  הונם ונכסיהם" - why core: a skill that lets a user "prepare a hon declaration" without a
  demand in hand is preparing a document nobody asked for; the demand letter also fixes the
  declaration DATE, which every other row depends on.
- [ ] The declaration DATE (יום ההצהרה) as the single anchor - form header is "דין וחשבון על
  רכוש והתחייבויות ליום ___" and every balance, bank statement and wallet snapshot must be
  as of that date - why core: mixing "today's balance" with the declaration date is the most
  common data-collection error and it silently corrupts the capital comparison.
- [ ] Deadline: 120 days, specifically the LATER of two dates. s.135(1)(a): "לגבי דו"ח על הון
  לא ייקבע מועד שהוא לפני תום 120 יום מהמועד שהצהרת ההון צריכה להתייחס אליו או מיום הדרישה,
  לפי המאוחר" - why core: the statute is a FLOOR on what the assessor may set, not a flat
  clock from the letter; getting the direction wrong produces a wrong internal due date.
- [ ] WHOSE assets: the form says "שלך, של בן/בת זוגך וילדיכם, שבשנת המס עדיין לא מלאו להם 18
  שנה". The STATUTE is worded differently: "של בן זוגו ושל ילדיהם שהם זכאים בעדם לנקודות זיכוי
  או לנקודות קצבה" - why core: the two scopes do not coincide in every family; collect on the
  form's under-18 rule and flag the credit-points wording as the statutory basis rather than
  asserting "under 18" as the law.
- [ ] Spouse opt-out mechanism: s.135(1)(a) allows a filer to EXCLUDE the spouse's capital
  "אם צירף הצהרה חתומה בידי אותו בן זוג כי יגיש דו"ח נפרד על הונו ונכסיו", in which case the
  report is due when the spouse's is due - why core: real, statutory, almost never documented;
  a preparer that always merges the spouse is wrong for separated or separately-assessed couples.
- [ ] Assets held as trustee for another: s.135(1)(a) reaches "נכסים שהוא משמש לגביהם כנאמנו
  של אדם אחר" - why core: an entire declarable class outside the taxpayer's own ownership.
- [ ] Ten-year exemption for עולה חדש / תושב חוזר ותיק: s.135(1)(b) - a person who first became
  an Israeli resident, or a veteran returning resident under s.14(a), is NOT required to file a
  report on capital and assets OUTSIDE Israel for ten years from the date they became resident.
  Two carve-outs: income the individual elected out of under s.14(a), and an asset received
  tax-free under s.97(a)(5), from 11 Tevet 5767 (1 January 2007) - why core: for this population
  "list every foreign asset" is affirmatively WRONG advice, and the two carve-outs decide the
  borderline cases.

### Valuation basis, general rules (form 1219 instructions, "איך לציין את ערך הנכס/ההתחייבות")

- [ ] Basis is COST, never market value: "ציין ליד כל נכס את הסכום שעלה לך הנכס בפועל, אין
  לציין את שווי הנכס" (rule 3) - why core: a market-value declaration destroys the comparison
  against the previous declaration. THE classic error in the domain.
- [ ] Cost includes acquisition-side costs and improvements: add "כל השקעה נוספת בקשר לנכס,
  כגון שכר טרחת עו"ד, תיווך, הוצאות הובלה, מס רכישה" (rule 4), and add improvements and
  betterments to the asset's cost (rule 5) - why core: omitting purchase tax and legal fees
  understates opening cost and manufactures a fake capital increase later.
- [ ] Inherited or gifted assets enter at 1 shekel: "אם קיים נכס בבעלותך שהתקבל בידך בירושה או
  במתנה עליך לציין בשדה סכום/עלות 1 ש"ח" (rule 2). Rule 8 adds that any asset whose acquisition
  cost is under 1 shekel is also entered as 1 shekel - why core: counter-intuitive and unique to
  this form; booking an inherited apartment at value produces a nonsense declaration.
- [ ] Instalment purchases: cost is the total of payments made including linkage and interest
  (rule 6). If the consideration has not been fully paid, the FULL price including interest and
  linkage is entered as the asset and the unpaid balance is entered separately as a liability
  (rule 7) - why core: netting or double-counting here is a direct arithmetic error in net capital.
- [ ] No offsetting debtors against creditors: "אין לקזז חייבים כנגד זכאים, גם אם הנך חייב
  וזכאי בעת ובעונה אחת כלפי אותו אדם/מוסד" (rule 13) - why core: netting hides a declarable
  asset and a declarable liability at once.
- [ ] Foreign currency: enter the foreign-currency amount in its own column and convert to
  shekels "לפי השער היציג ליום התשלום או הקבלה" - the representative rate on the PAYMENT OR
  RECEIPT date, NOT the declaration date (rule 12) - why core: converting at the declaration-date
  rate is a plausible-looking mistake that shifts every foreign asset.
- [ ] Formatting constraints the worksheet must satisfy: whole shekels, no agorot, rounded
  (rule 11); one asset or liability per line (rule 9); a section with nothing in it gets "0"
  (rule 1); jointly-owned PRIVATE assets entered at the filer's share (rule 10).
- [ ] Annex mechanics, general: where the form's space is insufficient or further detail is
  needed, attach additional sheets, certify them with your signature, write "מצורף נספח" on the
  matching line and mark on the annex which line of the declaration it belongs to (rule 14).
  One annex per additional non-balance-sheet business, aggregated at field 760 (rule 15).
- [ ] Supporting documents are part of the filing: "צרף מסמכים והוכחות לאימות הפרטים המוצהרים.
  הנך רשאי לצרף צילום או העתק של המסמכים ולהציג את המקור על פי דרישת פקיד השומה" - and the
  closing warning box ties the late-filing fine to filing "בצירוף כל המסמכים הנדרשים" - why
  core: a pack filed without annexes can be treated as NOT filed on time.

### PART A - private ASSET classes, one row each

- [ ] S1 נדל"ן בארץ: structure, improvements including construction in progress, דמי מפתח,
  land, agricultural areas. Fields: asset type, purchase/improvement date, גוש, חלקה, תת חלקה,
  address, cost. Valuation: cost + ancillary (lawyer, brokerage, purchase tax) + improvements
  and renovations; property under construction at all construction costs paid to date.
  Annex: contracts, tabu extract, improvement receipts. Total -> field 10.
- [ ] S2 נדל"ן בחו"ל: same asset scope. Fields add country, currency type, cost in foreign
  currency alongside shekel cost. Valuation: same cost basis, converted per general rule 12.
  Total -> field 20. NEW dedicated section in the 2025 form, not a sub-case of S1.
- [ ] S3 חשבונות בבנקים ובמוסדות כספיים בארץ ובחו"ל, including digital banks and digital
  accounts, overdraft as a NEGATIVE. Fields: country, institution, account holder, account
  number, bank number, branch number, currency, foreign amount, shekel amount. Valuation:
  balance per the bank statement as of the declaration date. Two limbs easy to miss: report
  accounts you own OR CONTROL even if not registered in your name, and internet accounts such
  as PayPal. Annex: bank statements as of the declaration date. Total -> field 30.
- [ ] S4 נכסים דיגיטליים (examples on the form: ביטקוין, אתריום, לייטקוין, NFT). Fields: asset
  type, quantity, purchase date, wallet address, cost. Valuation: cost. Annex, expressly: if
  held through a service provider such as an exchange, attach the account number and files
  containing balances of ALL digital assets held as of the declaration date. Total -> field 40.
  NEW dedicated section in the 2025 form; crypto cannot be folded into "other assets".
- [ ] S5 מזומנים not held at a bank or other financial institution. Fields: currency type,
  foreign amount, shekel amount. Total -> field 50.
- [ ] S6 ביטוח חיים, קופות גמל, קרן פנסיה, קרן השתלמות ותכניות חיסכון בארץ ובחו"ל. Fields:
  account type, country, institution, account holder, currency, amounts. Valuation, class-
  specific and MOST often got wrong: "הסכום בש"ח הוא סכום כל ההפקדות בתכניות מבלי להתחשב
  בסכומי ריבית, הצמדה או רווחים אחרים" - the sum of DEPOSITS, ignoring interest, linkage and
  other gains, NOT the fund's current balance. Total -> field 60.
- [ ] S7 השקעה בניירות ערך וקרנות נאמנות בארץ ובחו"ל. Fields: security type, country,
  institution, account holder, account number, bank number, branch number, currency, amounts.
  Valuation: the amount actually INVESTED; "נתוני העלות יוזנו בהתאם לתדפיסי המוסד בו מתנהל תיק
  ני"ע". Separate line per portfolio per institution. Annex: institution statements.
  Total -> field 70. Cost-only reporting for securities was an explicit change in the new form.
- [ ] S8 חייבים - הלוואות שנתתי לאחרים (loans the taxpayer GAVE). Fields: debtor name,
  relationship (family member / friend / other), ID or ח.פ, year the debt arose, currency,
  amounts. Valuation: "יש לרשום את החוב במונחי קרן בלבד", principal only. Total -> field 80.
  An outbound loan is an ASSET; omitting it understates closing capital and manufactures an
  unexplained gap.
- [ ] S9 כלי תחבורה לרבות כלי רכב, שייט וטייס: private car, motorcycle, commercial vehicle,
  watercraft, aircraft. Fields: type, purchase date, licence/registration number, cost.
  Total -> field 90. The new form no longer asks for make and model.
- [ ] S10 תכשיטים, זהב, יהלומים, פרטי אספנות ואומנות, expressly including private collections,
  coins, stamps, antiques, artworks and "כל אוסף אחר". Fields: item type, purchase date, cost.
  Total -> field 100.
- [ ] S11 תכולת בית: durable household goods, furniture, electrical and electronic goods,
  musical instruments, rugs and the like. Fields: item type, purchase date, cost.
  Total -> field 110. A MANDATORY line, not optional.
- [ ] S12 רכוש אחר שלא פורט לעיל: anything not caught by S1-S11. Fields: item type, purchase
  date, cost. Total -> field 120.

### PART A - private LIABILITY classes, one row each

- [ ] S13 התחייבויות לבנקים ולמוסדות כספיים אחרים (הלוואות למיניהן). The instruction names
  mortgages HERE: "לדוגמא הלוואות ומשכנתאות". Fields: country, institution, account holder,
  account number, bank number, branch number, currency, amounts. Valuation: "יש לרשום את החוב
  במונחי עלות בלבד". Total -> field 130. There is NO separate mortgage section; a preparer
  looking for one will wrongly conclude the mortgage is out of scope.
- [ ] S14 הלוואות שלקחתי מאחרים - private loans NOT through financial institutions. Fields:
  lender name, relationship (family member / friend / other), lender ID or ח.פ, year the debt
  arose, currency, amounts. Valuation: cost terms only. Total -> field 140. This is the row
  that carries the "loan from family" explanation for a capital increase, so the lender's
  identity and supporting documents must be gathered at the same time.
- [ ] Part A arithmetic exactly as the form states it: field 200 = 10+20+30+40+50+60+70+80+
  90+100+110+120; field 210 = 130+140; field 220 = 200-210 - why core: the reconciliation
  output must reproduce the form's own field numbering or it cannot be transcribed into the
  online system.

### PART B - השקעה בעסק בו נערך מאזן (three separate vehicles, not one row)

- [ ] Sub-block 1 השקעה בעסק. Header: business name, מס' עוסק, business type, country, your
  share %. Lines: 300 capital-account balance, 310 current-account (חו"ז) balance, 320 loans
  you gave the business, 330 loans you took from the business. Net 340 = 300+310+320-330.
  Rule: a חו"ז balance where you OWE the business is entered as a NEGATIVE number.
- [ ] Sub-block 2 השקעה בשותפות. Header: partnership name, partnership number, country, share %.
  Lines 350, 360, 370, 380 mirroring the above. Net 390 = 350+360+370-380.
- [ ] Sub-block 3 השקעה בחברה, אגודה שיתופית ותאגיד אחר. Header: company/entity name, ח.פ or
  foreign registration number, business type, country, share %. Lines 400 capital account,
  410 חו"ז, 420 loans you gave the company AND amounts paid on account of shares not yet
  allotted, 430 loans you took from the company. Net 440 = 400+410+420-430. Class-specific
  valuation rule: "רשום את השקעתך ואת המניות שלך בערך הנקוב" - shares at PAR value.
- [ ] Annex rule for part B: one separate annex PER additional business, partnership or company,
  with net investments from all annexes summed into field 450. Field 460 = 340+390+440+450.

### PART C - רכוש והתחייבויות בעסק בו לא נערך מאזן (a full second balance sheet, fields 500-770)

- [ ] Header and share rule: business name, מספר עוסק/שותפות/רישום for a foreign business,
  business type (עצמאי, שותפות, אחר), country, share %. If a PARTNERSHIP, enter figures for the
  partnership AS A WHOLE and take your share only at field 750. If a balance sheet WAS prepared
  for the partnership, fill part B instead and attach a signed balance sheet. One annex per
  additional such business.
- [ ] Current assets S1: 500 מזומנים והמחאות בקופה at the declaration date; 510 שטרות והמחאות
  לקבל, notes and cheques received bearing a date LATER than the declaration date, recorded in
  full with NO offsetting of liabilities, list attached; 520 כרטיסי אשראי, vouchers at the
  declaration date not yet credited to the business bank account, list attached; 530 לקוחות,
  with a list of customer and debtor names and amounts attached, accrual-basis businesses to
  include interest accrued to the declaration date, and NO netting of credit balances (credit
  balances go separately under liabilities). Total 540 = 500+510+520+530.
- [ ] S2 מלאי: 550, at cost, including finished goods, raw materials and work in progress.
- [ ] S3 רכוש שוטף אחר: 560, at cost, expressly including VAT refunds claimed and not yet
  received (including the VAT transaction report for the month in which the declaration was
  demanded) and import deposits.
- [ ] S4 חשבונות בבנקים ובמוסדות כספיים בארץ ובחו"ל including digital: 570. Same field set and
  same two limbs as part A S3 (accounts you own or control though not in your name; PayPal-type
  accounts); overdraft as a negative; balances per the bank statement at the declaration date.
- [ ] S5 ניירות ערך וקרנות נאמנות: 580, at the amount actually invested, per the institution's
  statements, separate line per portfolio per institution.
- [ ] S6 הלוואות שהעסק נתן לאחרים וחייבים אחרים בעסק: 590, debtors who are NOT customers.
  Fields: debtor, relationship, ID, year the loan was given, currency, amounts.
- [ ] S7 נכסים דיגיטליים of the business: 600, same fields as part A S4 and the same annex
  requirement - if held via a service provider such as an exchange, attach chronologically
  continuous files from that provider showing balances in all digital assets held as of the
  declaration date.
- [ ] Fixed assets S8 נדל"ן בארץ recorded in the business's books: 610. Fields: asset type
  (דירה, בית פרטי, מחסן, קרקע, חנות, משרד), purchase date, גוש, חלקה, תת חלקה, address, amount
  paid. Cost includes ancillary costs (lawyer, brokerage, purchase tax) and improvements,
  betterments and renovations; property under construction at all construction costs paid.
- [ ] S9 נדל"ן בחו"ל recorded in the business's books: 620, same rules plus country and foreign
  currency.
- [ ] S10 כלי תחבורה לרבות כלי רכב, שייט, טייס וציוד כבד, in Israel and abroad, registered in
  your name or the business's: 630. Fields: item name, purchase date, licence/registration
  number, cost. NOTE this class adds HEAVY EQUIPMENT, which part A S9 does not.
- [ ] S11 מכונות, ציוד, מכשירים וריהוט: 640, cost and purchase date.
- [ ] S12 רכוש קבוע אחר: 650, expressly naming זכות ראויה או מוחזקת, מוניטין, פטנטים, זיכיונות,
  סימני מסחר, שיפורים במושכר.
- [ ] S13 תשלומים על חשבון רכוש קבוע: 660, payments made on account of acquiring a fixed asset
  including an asset not yet transferred into the business's ownership.
- [ ] Total assets: 670 = 540+550+560+570+580+590+600+610+620+630+640+650+660.
- [ ] Business liabilities S14 התחייבויות שוטפות: 680 חובות לספקים in Israel and abroad, with a
  list of supplier names attached; 690 שטרות והמחאות לפירעון לרבות חברות אשראי, notes and
  cheques payable bearing a date later than the declaration date, detail attached.
  Total 700 = 680+690.
- [ ] S15 הלוואות מבנקים ומוסדות כספיים אחרים: 710. Full bank/branch/account field set.
  Valuation: "במונחי עלות (קרן) בלבד, ללא ריביות שטרם שולמו" - principal only, excluding unpaid
  interest.
- [ ] S16 הלוואות מאחרים, זכאים והתחייבויות אחרות: 720, expressly including other liabilities
  that are not loans. Fields: name of the party the business owes, relationship, ID or ח.פ,
  year the debt arose, currency, amounts. Principal only, excluding unpaid interest.
- [ ] Total liabilities 730 = 700+710+720. Net capital in the business 740 = 670-730. Your
  share 750 = 740 x your percentage. 760 = your share in further non-balance-sheet businesses
  and partnerships via annexes. 770 = 750+760.

### PART D - פרטים נוספים (four declaration points, each its own row)

- [ ] S1 כספות: whether you hold or control a safe, directly or indirectly; its location
  (בבית / בבנק with bank name, branch and safe number / אחר); whether it contains assets that
  are NOT yours, with a detailed list, owner name, owner ID or ח.פ and amount. Assets in the
  safe that ARE yours go into the ordinary section for their class. An explicit yes/no on a
  signed form, so a wrong answer is a false statement rather than an omission.
- [ ] S2 ייפוי כוח: whether you, INCLUDING your spouse, act as מיופה כוח, אפוטרופוס, נאמן,
  נציג or authorised signatory on bank accounts, in respect of property or liabilities that are
  not yours, in Israel or abroad. Fields: description, owner name, owner ID or ח.פ, amount.
  Annex required.
- [ ] S3 רכוש שאינו בבעלותי ולא דווח בסעיפים הקודמים: assets you hold that are not yours and
  were not reported above. Fields: item description, location, owner name, owner ID or ח.פ,
  cost. A SEPARATE question from both the safe question and the power-of-attorney question.
- [ ] S4 הון נטו (עסקי ופרטי) שהוצהר בהצהרת הון קודמת ליום ____: carry in the previous
  declaration's net figure; leave blank ONLY if this is the first declaration. This field is
  what turns the form itself into the capital comparison, and it is NEW in the 2025 form.
- [ ] Grand total: field 800 = 220 + 460 + 770, "סה"כ רכוש נטו (עסקי ופרטי)". This is the
  number the assessor actually compares.

### Closing obligations

- [ ] The signature declaration: the filer declares the details reported are complete and
  correct as at the declaration date, and that apart from the property and liabilities listed,
  neither they, their spouse, nor their children who had not yet reached 18 on that date had
  any other liability or property. ONE of the spouses must sign. The form also carries a
  checkbox "אני ובן/בת זוגי נשואים ומנהלים משק בית משותף".
- [ ] Paid-preparer block: to be completed by a person who assisted for payment (רו"ח, עו"ד,
  יועץ מס), citing s.143 on the form itself and noting the preparer's responsibility under
  s.224. Verified: s.143 requires anyone assisting another for payment to declare on the
  document that they assisted; s.224 treats a knowing assistant as if they had committed the
  offences under ss.215-217 and 220 themselves.
- [ ] The reconciliation the skill exists to perform: closing net capital (field 800) minus the
  previous declaration's net capital (part D S4), less declared income and other legitimate
  sources (gifts, inheritances, loans received, non-taxable receipts), plus living expenses
  over the period, equals the gap. Source for the method and for the ITA's use of average
  living-expense tables matched to the taxpayer's profile: Hebrew Wikipedia הצהרת הון.
- [ ] Burden of proof on appeal sits on the TAXPAYER: s.155 - "חובת הראיה כי השומה היא מופרזת
  תהיה על המערער; אולם אם המערער ניהל פנקסים קבילים ... חייבים פקיד השומה או המנהל, לפי הענין,
  להצדיק את החלטתם" - why core: this is WHY explanations must be assembled BEFORE filing, which
  is the skill's whole value proposition, and the acceptable-books exception is the one lever
  that shifts it back.
- [ ] Late filing fine: s.188(ז) imposes a fine per full month of delay on a report under
  s.135(1), and a HIGHER rate from the extended date where the filer obtained a later date at
  their own request and then still filed late. The ordinance names 200 shekels and 400 shekels,
  s.188(ה) defines "חודש" as a full month, and s.188(ח) RE-INDEXES every amount in s.188 on
  1 January each year to the previous year's CPI - so NEITHER nominal figure is a current
  amount and both must be resolved at runtime.
- [ ] Criminal exposure: the form's own warning box cites s.188(ז) for the fine and s.215 for
  the offence, and cites ss.216 and 220 for "רישום פרטים כוזבים בהצהרה, השמטת נכסים בבעלותך
  וכן אי הגשת הצהרת הון במועד". Verified: s.215 is the residual offence (one year or a
  s.61(a)(2) fine); s.216(1) covers failing to comply with a requirement contained in a notice
  given under the ordinance; s.220 is the wilful evasion offence carrying seven years or a
  s.61(a)(4) fine plus twice the concealed income.
- [ ] Fine and prosecution do not stack on the same failure: s.189(b) - once a criminal charge
  for non-filing is brought, no s.188 fine is payable for that offence and a fine already paid
  is refunded; on acquittal, linkage and interest run from payment to refund.



## Should cover (advanced / edge cases)

- [ ] Digital filing route and its rules: ITA opened the online capital-declaration system on
  05/05/2025 at http://secapp.taxes.gov.il/sh-haz-hon. Circular 2025-000538 is explicit that at
  that stage use of the system is "בגדר רשות ולא חובה", OPTIONAL not mandatory, though filing
  that way gets faster handling. Attachments can be uploaded per section with a note against
  each; at the end there is a documents screen listing the documents required by the sections
  the filer actually completed, marking whether each was supplied; a consolidated single file,
  per-section files, general files and files explaining a capital increase are all accepted.
  Accepted file types: Pdf, Jpg, Excel, Word. Source: circular 2025-000538 ss.2.1, 2.2.
  Why: the output pack should be shaped to those file types and the per-section attachment
  model, and the documents screen is effectively the ITA's own coverage checklist.
- [ ] The system also offers automatic calculations, draft saving, flexible addition of
  sections, immediate submission confirmation, viewing of previously submitted digital
  declarations, and adding missing documents AFTER the submission date. Why: "you can add a
  missing document later" changes the advice a preparer gives when one annex is not ready by
  day 120.
- [ ] When the filing is actually COMPLETE: only on receipt of the submission notice in the
  system, and where a representative files, only after the signature process is finished. A
  representative must attach the taxpayer-signed form in the designated place or as the first
  page of the document file, and declares the signed form is identical to what was transmitted.
  A signed form printed from the system or third-party software is acceptable. Remote-signature
  rules for the annual return apply to capital declarations too (ITA guidance 23/02/2025). A
  taxpayer filing alone is NOT required to sign the form but must declare the details are
  complete and correct and that all property and liabilities were reported. A representative
  filling the form for clients does not sign it, only completes the end declarations.
  Source: circular 2025-000538 ss.2.3, 2.4. Why: the skill must be able to say when the
  120-day clock actually stops.
- [ ] Spousal visibility in the system: a submitted declaration is viewable by an authorised
  representative, a power-of-attorney holder and the REGISTERED spouse. The non-registered
  spouse may view it only if it was declared at submission that the couple live together and
  maintain a joint household. Source: circular 2025-000538 end of s.2.4. Why: this is what the
  "אני ובן/בת זוגי נשואים ומנהלים משק בית משותף" checkbox actually controls.
- [ ] API route for third-party software: a dedicated capital-declaration API was opened to
  software vendors that adapted to it (ITA letter 22/12/2024). It does NOT carry attachments;
  after transmitting data by API the filer must enter the system to add verifying documents and
  the taxpayer-signed copy. Source: circular 2025-000538 s.3.
- [ ] Support channels named by the ITA: information and online services centre, 02-5656400 or
  the Tax Authority information centre number published on the service page. Source: circular 2025-000538
  s.4. Why: the right escalation to hand a stuck user instead of inventing one.
- [ ] Frequency of demand: NOT fixed by statute. s.135 sets no interval. Practice per secondary
  sources: a first declaration shortly after a status change (opening a tax file, becoming
  self-employed or a company owner), a further declaration roughly every four years, plus an ad
  hoc demand whenever concealment is suspected. Why: users ask "how often"; the honest answer is
  the four-year figure is PRACTICE, not law, and must be labelled as such.
- [ ] Who typically receives a demand: those obliged to file an annual income return (the
  self-employed and company owners), plus employees whose income exceeds the regulation
  threshold. Descriptive only; the operative trigger is always the written demand under
  s.135(1)(a).
- [ ] Living-expense (הוצאות מחיה) tables used in the comparison: drawn from CBS
  household-expenditure data matched to household size and profile, cross-referenced against
  other government data (frequent foreign travel given as an anomaly signal). Updated
  periodically and NOT published inside form 1219. Why: the skill should collect the user's
  ACTUAL living expenses and flag the comparison, and must NOT hard-code a table of amounts it
  cannot source to a current ITA or CBS publication.
- [ ] What counts as an acceptable explanation for a capital increase: gifts, inheritances and
  loans received during the examined period are the standard legitimate sources; recurring
  triggers for scrutiny are omitted assets (foreign and digital especially), undocumented
  transfers, and inconsistencies between successive filings.
- [ ] Gifts and loans received: form 1219 has NO "gifts" section. A gift or inheritance surfaces
  as an ASSET entered at 1 shekel under general rule 2; a loan received surfaces in part A S14
  (or part C S16 for the business) with lender identity, relationship, ID and year the debt
  arose. The documentary burden lands on the ANNEXES, not on a form line. IMPORTANT NEGATIVE
  FINDING: NO statutory shekel threshold for documenting a gift or loan was found in form 1219,
  circular 2025-000538, or s.135. DO NOT ASSERT ONE.
- [ ] Two different share mechanics in one form: in part A, jointly-owned private assets go in
  at the filer's share (general rule 10); in parts B and C the FULL entity figures are entered
  and the share is applied at entity level (percentage column in part B, field 750 in part C).
  Why: applying the share twice, or at the wrong level, is a quiet arithmetic error.
- [ ] Business inventory: part C S2 asks for עלות המלאי including finished goods, raw materials
  and work in progress. Why: consistent with the cost basis, but it is the figure most likely to
  be lifted from a management report at SELLING value.
- [ ] Businesses abroad: parts B and C both carry a מדינה column and accept a foreign
  registration number in place of a ח.פ. Why: foreign entity holdings are in scope but the
  identifier field differs and a preparer expecting a ח.פ will stall.
- [ ] Fields the NEW form DROPPED because the ITA already holds the data: vehicle make and
  model, bank address, business establishment date, business address, deductions file number.
  Source: circular 2025-000538 s.1. Why: a data-gathering checklist copied from an older guide
  will make the user chase fields nobody wants.
- [ ] The "1 shekel" convention interacts badly with the comparison: an inherited apartment sits
  in closing capital at 1 shekel while the cash it later generates sits at full value. The skill
  should surface this as an EXPLANATION LINE rather than as a gap. Why: a naive reconciliation
  will flag a phantom increase on exactly the fact pattern the 1 shekel rule exists to handle.
- [ ] Trustee, guardian and power-of-attorney holdings appear in TWO places with different
  meanings: s.135(1)(a) makes assets held as trustee for another demandable as part of the
  report, while part D S2 and S3 collect items held but not owned. The skill must NOT silently
  merge them: one is a reportable asset, the other is a disclosure about someone else's asset.

## Out of scope (explicit, with rationale)

- Computing the tax due on an unexplained capital gap. That is an ASSESSMENT, made by the
  assessor and contested on appeal. The skill reconciles and surfaces the gap; it does not
  price it.
- Filing on the taxpayer's behalf, or transmitting anything to secapp.taxes.gov.il. The system
  requires personal-area authentication, and a representative filing must attach a
  taxpayer-signed form and make a representative declaration under s.143.
- Signing the paid-preparer block. ss.143 and 224 attach PERSONAL liability to a paid human
  assistant; an agent cannot occupy that role.
- Deciding whether a given receipt is taxable income. The substantive income-tax question the
  declaration only frames, and where a licensed professional is required.
- The annual income return and its deadlines. Different form, different statutory
  track (ss.131-133), penalised under s.188(a) not s.188(ז). Relevant here only as the income
  input to the comparison.
- Voluntary-disclosure (גילוי מרצון) procedure. Separate ITA track with its own conditions and
  consequences; advising on it where a gap exists is precisely where a licensed professional is
  required.
- FATCA and CRS reporting under ss.135ב-135ז. Adjacent section numbers, unrelated obligation,
  imposed on financial institutions rather than the declarant. Do not let section-number
  proximity pull this in.
- Structuring advice, or any statement about whether a particular ownership arrangement is
  legitimate.
- Valuing an asset. The form asks for COST, not value, so no appraisal is ever required by the
  form itself; where a user has only a value, ask for the acquisition documents rather than
  estimate.
- Producing the previous declaration where the user does not have it. The prior net-capital
  figure (part D S4) must come from the user's own copy or the assessment file; the skill must
  not reconstruct or guess it.
- Determining residency status, or whether someone qualifies as a תושב חוזר ותיק. The ten-year
  foreign-asset exemption in s.135(1)(b) turns on that status, but establishing it is a separate
  determination the skill should flag and route out.

## Known bad figures (from message 3)

- "500 shekels per month for a late capital declaration, reduced to 400 if an extension was
  granted." BOTH HALVES WRONG. 500 is the s.188(a) figure for the ANNUAL return under s.132.
  For a s.135(1) report the governing provision is s.188(ז): 200 shekels per full month, and
  the 400 rate is an INCREASE not a reduction, applying where the filer obtained a later date at
  their own request and then filed after it, running from the later date. Both nominal figures
  are subject to annual CPI indexation under s.188(ח), so NEITHER is a current amount. This
  error appears in CPA-firm guides.
- "The declaration covers your assets, your spouse's, and your children's under 18" presented as
  the STATUTORY rule. The FORM says under 18. The STATUTE s.135(1)(a) says children for whom
  credit points or allowance points are claimed. Quote the form for the form and the statute for
  the statute; do not merge them.
- Instructions to enter market value, the current fund balance, or a valuer's estimate. General
  rule 3: "אין לציין את שווי הנכס". S6 is more specific: pension/gemel/hishtalmut/life-insurance
  and savings plans are the sum of DEPOSITS ignoring interest, linkage and gains.
- Describing an inherited or gifted asset as declared at its value. General rule 2: 1 shekel.
  Rule 8 extends it to any asset whose acquisition cost is under 1 shekel.
- "Online filing has been mandatory since May 2025." Circular 2025-000538 says the opposite in
  terms. What became mandatory is the new VERSION of form 1219, not the online channel.
- "There is no separate mortgage section, so a mortgage is not reported." Mortgages ARE
  reported, in part A S13, which names them expressly.
- TOOLING HAZARD, not a published source: a WebFetch summary of circular 2025-000538 produced
  during this research asserted attachments must be PDF only, that image files are rejected, and
  that every attachment needs a scanned QR code. NONE of that is in the circular. Treat
  model-mediated extraction of ITA PDFs as unreliable and read pdftotext output instead. Same
  applies to the gov.il ordinance PDF, where a WebFetch against a similarly named Nevo URL
  returned sections of the MUNICIPALITIES Ordinance under the same section numbers.
- Secondary guides giving a shekel threshold above which a gift or loan must be documented. No
  such threshold exists in the primary sources. Treat any figure of that shape as unsourced.

## Authoritative sources (partial, message 3 truncated)

- https://www.gov.il/BlobFolder/service/itc1219/he/Service_Pages_Income_tax_itc1219.pdf - the
  form (7 pages) plus 8 pages of official filling instructions. Verify here: every section
  number and title, every field number 10 to 800, per-class field lists, per-class valuation
  rules, general valuation rules, annex rules, the four part-D questions, signature and
  paid-preparer declarations, and the warning box citing ss.188(ז), 215, 216, 220.
  EXTRACT WITH `pdftotext -layout` and strip Unicode bidi format characters; WebFetch cannot
  read this file and will say so.
- Circular 2025-000538 (05/05/2025):
  https://www.gov.il/BlobFolder/dynamiccollectorresultitem/represent-info-050525-1/he/IncomeTax_represent-info-050525-1.pdf
- פקודת מס הכנסה [נוסח חדש] gov.il PDF - ss.135, 143, 155, 188, 189, 215, 216, 220, 224.



- https://www.gov.il/BlobFolder/service/itc1219/he/Service_Pages_Income_tax_itc1219.pdf
  The form (7 pages) plus 8 pages of official filling instructions. Verify: every section number
  and title, every field number 10-800, per-class field lists, per-class valuation rules, general
  valuation rules, annex rules, the four part-D questions, signature and paid-preparer
  declarations, the warning box citing ss.188(ז), 215, 216, 220.
  EXTRACTION: `pdftotext -layout` and strip Unicode bidi format characters. WebFetch CANNOT read
  this file and will say so.


- https://www.gov.il/BlobFolder/legalinfo/law_pkudat_mas_hachnasa/he/LegalInformation_kesher_%D7%A4%D7%A7%D7%95%D7%93%D7%AA%20%D7%9E%D7%A1%20%D7%94%D7%9B%D7%A0%D7%A1%D7%94%20%5B%D7%A0%D7%95%D7%A1%D7%97%20%D7%97%D7%93%D7%A9%5D%20-%20%D7%9C%D7%90%20%D7%9E%D7%A8%D7%95%D7%91%D7%93.pdf
  Full Income Tax Ordinance as published by gov.il, about 10.8 MB. Verify: s.135(1)(a) demand
  power and the 120-day floor, spouse opt-out, trustee assets; s.135(1)(b) ten-year foreign-asset
  exemption and its two carve-outs; s.143 preparer declaration; s.155 burden of proof; s.188(ז),
  (ה), (ח) fine, full-month definition, annual indexation; s.189(b) fine versus prosecution;
  ss.215, 216, 220 offences; s.224 assistant liability.
  TWO EXTRACTION TRAPS:
   (1) the ordinance NEVER uses the phrase "הצהרת הון". Search for "דו"ח על הונם ונכסיהם".
   (2) the numbers in the table of contents are PAGE references, not section bodies. Locate a
       section by its marginal heading (e.g. "קנס על אי-הגשת דו"ח") using a REVERSE search,
       not a forward one.

- https://www.gov.il/BlobFolder/dynamiccollectorresultitem/represent-info-050525-1/he/IncomeTax_represent-info-050525-1.pdf
  ITA circular 2025-000538 of 05/05/2025, Deputy Director for Assessment and Audit, addressed to
  representatives and to vendors of capital-declaration software. Verify: the digital system launch
  and that use of it is OPTIONAL; the enumerated list of what changed in the new form; the
  30/06/2025 OLD-VERSION CUT-OFF; accepted attachment file types; signature and representative
  rules; the API limitation; support numbers.
  THE SINGLE BEST TEMPORAL SOURCE IN THE DOMAIN and the only one stating the change list in the
  ITA's own words.

- http://secapp.taxes.gov.il/sh-haz-hon
  The live filing system, named in both the form instructions and the circular. Reference to hand
  the user. DO NOT automate against it.




## STILL OUTSTANDING FROM THIS AGENT

- Step C.1a temporal findings in full (only the 30/06/2025 old-version cut-off has surfaced).
- Whether a current INDEXED value of the s.188(ז) fine is publishable, or whether the skill must
  route the user to the ITA for it.



## 1. Form version cut-off: what 30/06/2025 actually means

The circular grants a TIME-LIMITED PERMISSION; it does NOT describe a rejection rule.
VERBATIM: "על מנת להקל בהטמעת הטופס החדש בקרב הנישומים והמייצגים תתאפשר הגשת הצהרת הון על גבי
טופס 1219 בנוסחו הקודם עד ליום 30/6/2025."

So filing on the PREVIOUS wording was PERMITTED until 30/06/2025, and that permission LAPSED.
What happens to an old-wording form submitted after it (bounced at intake, accepted with a request
to refile, or accepted silently) is **NOT ESTABLISHED**. The circular says nothing about the
consequence and no later ITA notice addresses it.
Source: circular 2025-000538 s.1.

## 2. VERSION SELECTION RULE - the load-bearing answer

**Nothing selects by demand date or by declaration date. Selection is by FILING DATE, and from
01/07/2025 onward the CURRENT form always applies. THE SKILL CARRIES ONE FORM LAYOUT.**

Basis: the circular states the rule as a channel-and-form instruction operating from a date:
"החל מהיום הגשת הצהרת הון תתבצע במערכת המקוונת, או על גבי טופס 1219 ידני בגרסתו החדשה באמצעות
הגשה למשרדי השומה או במערכת הפניות."
The operative verb is הגשה, the act of FILING. Neither that sentence, nor the transitional
sentence above, nor s.135 anywhere, contains a clause keying the form version to when the demand
issued or to the date the declaration relates to. So a demand issued in 2024, and a declaration
dated 31/12/2023, are BOTH filed today on the CURRENT form.

*** CAVEAT TO CARRY INTO THE SKILL ***
This is an ENTAILMENT from the circular's wording plus the ABSENCE of any version-selection
clause. It is NOT an express "the version in force at filing applies" statement. The agent looked
for such a clause in the circular and in s.135; there is none.
HEDGE IT AS: "no rule selects an older version by date" - NOT as "the ITA has stated that filing
date governs."

## 3. What the PREVIOUS version did differently for the three changed classes

**NOT ESTABLISHED for any of the three.** The superseded form was not obtained, so there is no
direct reading of its sections.

What IS established is only the ITA's own characterisation of the change, circular 2025-000538
s.1, VERBATIM: "השינויים כוללים הוספת סעיפי דיווח ייעודיים לנכסים דיגיטליים ונכסי נדל"ן בחו"ל,
דיווח על ניירות ערך במונחי עלות בלבד, פירוט רכוש שלא בבעלות הנישום ומוחזק אצלו והון נטו שהוצהר
בהצהרת הון קודמת."

Strictly what that sentence supports, per class:
- FOREIGN REAL ESTATE: the word is הוספת, ADDITION of a dedicated section. So the old form had NO
  dedicated foreign-real-estate section. Where such an asset went instead (the domestic
  real-estate line, the catch-all רכוש אחר, or nowhere) is NOT ESTABLISHED.
- DIGITAL ASSETS: same wording, same entailment - no dedicated section before. Whether the old
  form required crypto to be reported at all, and under which line, is NOT ESTABLISHED.
- SECURITIES: the change is "דיווח על ניירות ערך במונחי עלות בלבד", cost-only reporting. THAT THE
  BASIS CHANGED is established. WHAT THE OLD BASIS WAS is NOT ESTABLISHED.
  *** DO NOT INFER "market value" from the contrast. The circular does not say it. ***

RECOMMENDATION FOR THE SKILL: state only that these are NEW dedicated sections, that securities
are now cost-only, and that a PRE-2025 PRIOR DECLARATION WILL NOT MAP FIELD-FOR-FIELD.
DO NOT describe the old treatment.

## 4. s.135 amendment history

120-day formulation: **NOT ESTABLISHED** whether it was ever amended. The gov.il ordinance text
places a SINGLE BLOCK of amendment markings above the whole of s.135(1)(a) - תיקון 21 תשל"ה-1975,
תיקון 22 תשל"ה-1975, תיקון 32 תשל"ח-1978, תיקון 37 תש"ם-1980, תיקון 89 תשנ"ב-1992, תיקון 168
תשס"ח... [remainder truncated in delivery]

DESIGN DECISION: since this is NOT ESTABLISHED, the skill will simply state the current
formulation and will NOT make any claim about its amendment history.

## 5. The late-filing fine - DESIGN DECISION (not awaiting further research)

Established: s.188(ז) names 200 shekels per full month, and 400 shekels where the filer obtained a
later date at their own request and then filed after it, running from the later date. s.188(ה)
defines "חודש" as a full month. s.188(ח) RE-INDEXES every amount in s.188 on 1 January each year to
the previous year's CPI.

NOT established: any currently published indexed value.

THE SKILL WILL THEREFORE: state the NOMINAL STATUTORY amounts, state that s.188(ח) re-indexes them
every 1 January, and ROUTE THE USER TO THE ITA for the current figure. It will NOT quote a current
indexed number.

Same treatment for the s.216 administrative fine under תקנות העבירות המינהליות (קנס מינהלי -
חיקוקי מסים), תשמ"ז-1987: the primary was NOT read, secondary sources disagreed irreconcilably
(980 shekels vs a 2,125-8,500 range), and the regulations double the fine on a repeat offence and
triple it on a further repeat. The skill states that an administrative fine exists, that it
escalates on repeat offences, and routes to the regulations. NO NUMBER.

## SUMMARY OF WHAT IS DELIBERATELY OMITTED FROM THE SKILL

Every item below is "not established" from primary sources and will simply not appear:
- the consequence of filing an old-version form after 30/06/2025
- the old form's treatment of foreign real estate, digital assets, and securities
- the amendment history of the 120-day rule
- any current indexed value of the s.188(ז) fine
- any value of the s.216 administrative fine
- what the 11 Tevet 5767 / 1 January 2007 date in s.135(1)(b) selects (never delivered)
