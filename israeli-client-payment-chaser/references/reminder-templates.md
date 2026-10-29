# Payment Reminder Templates (Hebrew)

Customizable templates for each escalation stage.

**Every stage below is timed from the DUE date established in Step 1 of the skill, never from the invoice date.** Under the statutory shotef+45 default an invoice can sit unpaid for over two months and still be perfectly within terms, so a template sent on invoice age accuses a client who owes nothing yet.

Replace placeholders with actual values:
- `[NAME]`: client name (שם הלקוח)
- `[INVOICE_NUMBER]`: invoice number (מספר חשבונית)
- `[AMOUNT]`: amount in NIS (סכום בש"ח)
- `[DATE]`: invoice date (תאריך חשבונית)
- `[DUE_DATE]`: payment due date (תאריך פירעון)
- `[BANK_DETAILS]`: bank transfer details (פרטי העברה בנקאית)
- `[BUSINESS_NAME]`: creditor business name (שם העסק)
- `[DEADLINE]`: payment deadline in demand letter (מועד אחרון לתשלום). In Stage 5 set it at least 21 days after the letter date, so the debtor has 14 days after a registered letter arrives, and never inside chol hamoed or on a rest day
- `[DAYS_LATE]`: days elapsed since the DUE date (ימי איחור), computed in Step 2. Never assert a number of days without computing it

## Stage 1: Friendly WhatsApp (due date + 0 to 3 days)

Phone first: a short call to the client's bookkeeper or accounts payable, asking whether the invoice arrived and is in the next payment run, settles many of these files before any message is sent. Log the call, then send:

```
היי [NAME],
רציתי לבדוק לגבי חשבונית מספר [INVOICE_NUMBER] מ-[DATE] בסך [AMOUNT] ש"ח.
אשמח לעדכון על מועד התשלום.
תודה רבה!
[BUSINESS_NAME]
```

## Stage 2: Follow-up WhatsApp (due date + 15)

```
שלום [NAME],
תזכורת נוספת לגבי חשבונית [INVOICE_NUMBER] מתאריך [DATE].
סה"כ לתשלום: [AMOUNT] ש"ח.

פרטי העברה בנקאית:
[BANK_DETAILS]

אשמח לעדכון בהקדם.
בברכה,
[BUSINESS_NAME]
```

## Stage 3: Formal Email (due date + 30)

**Subject:** דרישת תשלום, חשבונית מספר [INVOICE_NUMBER]

```
לכבוד [NAME],

הנדון: דרישת תשלום עבור חשבונית מספר [INVOICE_NUMBER]

אני פונה אליך בהמשך לפניות קודמות בנושא חשבונית מספר [INVOICE_NUMBER]
שהונפקה בתאריך [DATE] בסך [AMOUNT] ש"ח.

נכון להיום, החשבונית טרם שולמה, וחלפו [DAYS_LATE] ימים ממועד הפירעון שלה ([DUE_DATE]).

אבקש להסדיר את התשלום בהקדם האפשרי.

פרטי העברה בנקאית:
[BANK_DETAILS]

מצורף עותק החשבונית לנוחותך.

בברכה,
[BUSINESS_NAME]
```

## Stage 4: Warning of Legal Steps (due date + 45)

**Subject:** התראה לפני נקיטת צעדים, חשבונית מספר [INVOICE_NUMBER]

```
לכבוד [NAME],

הנדון: התראה לפני נקיטת צעדים משפטיים

למרות פניותינו החוזרות ונשנות, חשבונית מספר [INVOICE_NUMBER] מתאריך [DATE]
בסך [AMOUNT] ש"ח טרם שולמה.

ללא תשלום מלא תוך 14 יום מתאריך מכתב זה (עד [DEADLINE]),
ניאלץ לשקול נקיטת צעדים נוספים לגביית החוב, לרבות הליכים משפטיים
או פנייה ללשכת ההוצאה לפועל.

אנו מעדיפים להגיע לפתרון מוסכם. אם יש בעיה עם התשלום,
נשמח לשמוע ולמצוא פתרון משותף.

פרטי העברה בנקאית:
[BANK_DETAILS]

בברכה,
[BUSINESS_NAME]
```

## Stage 5: Final Notice / Demand Letter (due date + 60 or more)

This is the formal letter the creditor reviews, adapts, signs and sends in their own name. If the file later goes to court or to the Enforcement Office it is what they will rely on, so it must carry all six contents from Step 4 of the skill. Fill every bracket, and do not delete a block because the information seems obvious.

**Subject:** מכתב דרישה לפני נקיטת הליכים, חשבונית מספר [INVOICE_NUMBER]

```
[CREDITOR_BUSINESS_NAME]
[עוסק מורשה / עוסק פטור / ח.פ.] [CREDITOR_ID_NUMBER]
[CREDITOR_ADDRESS]
[CREDITOR_PHONE] | [CREDITOR_EMAIL]

תאריך: [LETTER_DATE]

לכבוד
[DEBTOR_LEGAL_NAME]        <- השם הרשום המלא, לא השם המסחרי
[ח.פ. / ע.מ.] [DEBTOR_ID_NUMBER]
[DEBTOR_ADDRESS]

בדואר רשום עם אישור מסירה ובדוא"ל [DEBTOR_EMAIL]

הנדון: מכתב דרישה לתשלום חוב בסך [TOTAL_AMOUNT] ש"ח, לפני נקיטת הליכים

1. הריני לפנות אליכם בדרישה לתשלום חוב בגין [DESCRIPTION_OF_GOODS_OR_SERVICES]
   שסופקו לכם על ידי [CREDITOR_BUSINESS_NAME].

2. פירוט החוב:

   | חשבונית | תאריך הוצאה | מועד פירעון | סכום | שולם | יתרה |
   |---------|-------------|-------------|------|------|------|
   | [NUM]   | [DATE]      | [DUE_DATE]  | [X]  | [Y]  | [Z]  |

   סה"כ יתרת קרן לתשלום: [TOTAL_PRINCIPAL] ש"ח.

3. מועד הפירעון של החשבונית חלף ביום [DUE_DATE].
   [OPTIONAL_STATUTORY_INTEREST_SENTENCE]

4. למרות פניותיי אליכם בתאריכים [DATES_OF_PRIOR_REMINDERS], החוב טרם שולם
   ולא התקבלה כל התייחסות עניינית מצדכם.

5. הריני לדרוש כי תשלמו את מלוא החוב, בסך [TOTAL_AMOUNT] ש"ח בתוספת ריבית
   והצמדה כדין ממועד הפירעון, וזאת תוך 14 יום מיום קבלת מכתב זה, ולא יאוחר
   מיום [DEADLINE].

6. ככל שהתשלום לא יתקבל במלואו עד למועד האמור, אפעל לגביית החוב בכל דרך
   חוקית העומדת לרשותי, לרבות הגשת תביעה, וזאת ללא כל הודעה נוספת. במקרה כזה
   תידרשו לשאת גם באגרות, בריבית ובהצמדה ובהוצאות שייפסקו.

7. אין באמור במכתב זה כדי לגרוע מכל זכות, טענה או סעד העומדים לי על פי כל
   דין או הסכם, וכל זכויותיי שמורות.

פרטים לתשלום:
[BANK_DETAILS]

מצורפים:
- העתקי החשבוניות שבנדון
- [אישור מסירה / הזמנת עבודה / הסכם / תכתובת רלוונטית]

בכבוד רב,

_______________________
[SIGNATORY_NAME], [ROLE]
[CREDITOR_BUSINESS_NAME]
```

**Before sending, check all six:** creditor identified with number and address; debtor identified by REGISTERED name and number; invoices itemised with dates and any partial payments; total demanded; a dated deadline; and an explicit statement of what happens if it passes. A letter missing the debtor's registered name or the itemisation is the one that gets argued about later.

**Paragraph 3, the statutory-interest sentence, is conditional.** Fill `[OPTIONAL_STATUTORY_INTEREST_SENTENCE]` only where the Payment Ethics to Suppliers Law applies to this client AND, for a private business or a budgeted body, sec. 4(b) is met (the client had the advantage in shaping the terms, for example through its own purchase order or standard supplier terms; when unclear, leave it out). Then use:

```
   בהתאם לסעיף 4 לחוק מוסר תשלומים לספקים, התשע"ז-2017, על הסכום שלא שולם
   במועד מתווספת ריבית שקלית ממועד הפירעון, ובחלוף 30 ימים נוספים אף דמי פיגורים.
```

Otherwise delete the placeholder. Paragraph 5 already claims `בתוספת ריבית והצמדה כדין ממועד הפירעון`, which demands whatever the law allows without asserting a statute or a figure. **Never write a percentage** unless the current quarter's rate has been confirmed.

**This letter is not the fixed-sum warning.** If the user may later use the Enforcement Office fixed-sum route (skill Step 7), the warning is a separate document built on the prescribed Form 19א wording with the particulars reg. 109a requires, served by registered mail with delivery confirmation, and the route needs evidence signed by the debtor. Use the Enforcement and Collection Authority's form; do not improvise it here.

## Usage Notes

- All templates should be reviewed before sending. Adjust tone and details as needed
- For WhatsApp messages (Stages 1-2), keep the tone professional but friendly
- For email messages (Stages 3-5), use formal business Hebrew
- Always verify the recipient's name and invoice details before sending
- Stage 5 (demand letter) should be sent by registered mail with delivery confirmation (doar rashum im ishur mesira) in addition to email. Keep the postal receipt and the confirmation: they fix when the 14-day deadline starts.
- Verify the debtor's REGISTERED name and number at the Companies Registrar before sending Stage 5. A demand addressed to a trading name rather than the legal entity is the most common defect in these letters.
