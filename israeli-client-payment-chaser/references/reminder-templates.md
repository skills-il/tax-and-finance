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
- `[DEADLINE]`: payment deadline in demand letter (מועד אחרון לתשלום)
- `[DAYS_LATE]`: days elapsed since the DUE date (ימי איחור), computed in Step 2. Never assert a number of days without computing it

## Stage 1: Friendly WhatsApp (due date + 0 to 3 days)

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
ניאלץ לשקול נקיטת צעדים נוספים לגביית החוב, לרבות פנייה לבית משפט
לתביעות קטנות.

אנו מעדיפים להגיע לפתרון מוסכם. אם יש בעיה עם התשלום,
נשמח לשמוע ולמצוא פתרון משותף.

פרטי העברה בנקאית:
[BANK_DETAILS]

בברכה,
[BUSINESS_NAME]
```

## Stage 5: Final Notice / Demand Letter (due date + 60 or more)

This is the document that has to stand up if the file later goes to court or to the Enforcement Office, so it must carry all six mandatory contents from Step 4 of the skill. The earlier stages are messages; this one is a legal document. Fill every bracket, and do not delete a block because the information seems obvious.

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

בדואר רשום ובדוא"ל [DEBTOR_EMAIL]

הנדון: מכתב דרישה לתשלום חוב בסך [TOTAL_AMOUNT] ש"ח, לפני נקיטת הליכים

1. הריני לפנות אליכם בדרישה לתשלום חוב בגין [DESCRIPTION_OF_GOODS_OR_SERVICES]
   שסופקו לכם על ידי [CREDITOR_BUSINESS_NAME].

2. פירוט החוב:

   | חשבונית | תאריך הוצאה | מועד פירעון | סכום | שולם | יתרה |
   |---------|-------------|-------------|------|------|------|
   | [NUM]   | [DATE]      | [DUE_DATE]  | [X]  | [Y]  | [Z]  |

   סה"כ יתרת קרן לתשלום: [TOTAL_PRINCIPAL] ש"ח.

3. מועד הפירעון של החשבונית חלף ביום [DUE_DATE]. בהתאם לחוק מוסר תשלומים
   לספקים, התשע"ז-2017, על הסכום שלא שולם במועד מתווספת ריבית שקלית ממועד
   הפירעון, ובחלוף 30 ימים נוספים אף דמי פיגורים.

4. למרות פניותיי אליכם בתאריכים [DATES_OF_PRIOR_REMINDERS], החוב טרם שולם
   ולא התקבלה כל התייחסות עניינית מצדכם.

5. הריני לדרוש כי תשלמו את מלוא החוב, בסך [TOTAL_AMOUNT] ש"ח בתוספת ריבית
   והצמדה כדין ממועד הפירעון, וזאת תוך 14 יום מיום קבלת מכתב זה, ולא יאוחר
   מיום [DEADLINE].

6. ככל שהתשלום לא יתקבל במלואו עד למועד האמור, אפעל לגביית החוב בכל דרך
   חוקית העומדת לרשותי, לרבות הגשת תביעה, וזאת ללא כל הודעה נוספת. במקרה כזה
   תידרשו לשאת גם באגרת בית המשפט, בריבית ובהצמדה ובהוצאות שייפסקו.

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

**Do not write a percentage into paragraph 3 or 5** unless the current quarter's statutory rate has been confirmed. `בתוספת ריבית והצמדה כדין ממועד הפירעון` claims the full statutory entitlement without asserting a figure, and is the safe default.

## Usage Notes

- All templates should be reviewed before sending. Adjust tone and details as needed
- For WhatsApp messages (Stages 1-2), keep the tone professional but friendly
- For email messages (Stages 3-5), use formal business Hebrew
- Always verify the recipient's name and invoice details before sending
- Stage 5 (demand letter) should be sent via registered mail (doar rashum) in addition to email. Keep the postal receipt: it evidences dispatch, which is what fixes the date the 14-day deadline runs from.
- Verify the debtor's REGISTERED name and number at the Companies Registrar before sending Stage 5. A demand addressed to a trading name rather than the legal entity is the most common defect in these letters.
