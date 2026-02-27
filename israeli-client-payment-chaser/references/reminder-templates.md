# Payment Reminder Templates (Hebrew)

Customizable templates for each escalation stage. Replace placeholders with actual values:
- `[NAME]` — client name (שם הלקוח)
- `[INVOICE_NUMBER]` — invoice number (מספר חשבונית)
- `[AMOUNT]` — amount in NIS (סכום בש"ח)
- `[DATE]` — invoice date (תאריך חשבונית)
- `[DUE_DATE]` — payment due date (תאריך פירעון)
- `[BANK_DETAILS]` — bank transfer details (פרטי העברה בנקאית)
- `[BUSINESS_NAME]` — creditor business name (שם העסק)
- `[DEADLINE]` — payment deadline in demand letter (מועד אחרון לתשלום)

## Stage 1: Friendly WhatsApp (Day 30)

```
היי [NAME],
רציתי לבדוק לגבי חשבונית מספר [INVOICE_NUMBER] מ-[DATE] בסך [AMOUNT] ש"ח.
אשמח לעדכון על מועד התשלום.
תודה רבה!
[BUSINESS_NAME]
```

## Stage 2: Follow-up WhatsApp (Day 45)

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

## Stage 3: Formal Email (Day 60)

**Subject:** דרישת תשלום — חשבונית מספר [INVOICE_NUMBER]

```
לכבוד [NAME],

הנדון: דרישת תשלום עבור חשבונית מספר [INVOICE_NUMBER]

אני פונה אליך בהמשך לפניות קודמות בנושא חשבונית מספר [INVOICE_NUMBER]
שהונפקה בתאריך [DATE] בסך [AMOUNT] ש"ח.

נכון להיום, החשבונית טרם שולמה למרות שחלפו למעלה מ-60 יום ממועד הפירעון.

אבקש להסדיר את התשלום בהקדם האפשרי.

פרטי העברה בנקאית:
[BANK_DETAILS]

מצורף עותק החשבונית לנוחותך.

בברכה,
[BUSINESS_NAME]
```

## Stage 4: Warning of Legal Steps (Day 75)

**Subject:** התראה לפני נקיטת צעדים — חשבונית מספר [INVOICE_NUMBER]

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

## Stage 5: Final Notice / Demand Letter Cover (Day 90+)

**Subject:** מכתב דרישה סופי — חשבונית מספר [INVOICE_NUMBER]

```
לכבוד [NAME],

הנדון: מכתב דרישה לתשלום חוב

מכתב זה מהווה דרישה רשמית ואחרונה לתשלום חשבונית מספר [INVOICE_NUMBER]
שהונפקה בתאריך [DATE] בסך [AMOUNT] ש"ח.

למרות פניות רבות בכתב ובעל פה, החוב טרם שולם.

הריני להודיעך כי ככל שהתשלום המלא לא יתקבל תוך 14 יום מתאריך
מכתב זה (עד [DEADLINE]), אפנה לבית המשפט לתביעות קטנות לגביית
החוב בתוספת ריבית והצמדה כדין, וכן הוצאות משפט.

סכום החוב נכון להיום: [AMOUNT] ש"ח (קרן)
ריבית והצמדה שנצברו: יחושבו בהתאם לחוק פסיקת ריבית והצמדה

פרטי העברה בנקאית:
[BANK_DETAILS]

מכתב זה נשלח בדואר רשום.

בברכה,
[BUSINESS_NAME]
```

## Usage Notes

- All templates should be reviewed before sending — adjust tone and details as needed
- For WhatsApp messages (Stages 1-2), keep the tone professional but friendly
- For email messages (Stages 3-5), use formal business Hebrew
- Always verify the recipient's name and invoice details before sending
- Stage 5 (demand letter) should be sent via registered mail (doar rashum) in addition to email
