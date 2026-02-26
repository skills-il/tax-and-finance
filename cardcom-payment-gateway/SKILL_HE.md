# שער תשלומים קארדקום

## סקירה

קארדקום היא חברת סליקה ישראלית עם יתרון ייחודי: הפקת חשבוניות וקבלות משולבת בתשלום, בהתאם לחוק המס הישראלי. בעוד שערי תשלום אחרים מטפלים רק בתשלום עצמו, קארדקום יכולה להפיק אוטומטית חשבוניות מס וקבלות כחלק מזרימת התשלום -- דבר שעסקים ישראליים מחויבים לספק על פי חוק.

מדריך זה מנחה אינטגרציה עם REST API V11 של קארדקום לתשלומים, טוקניזציה, חיובים חוזרים, והפקת מסמכים.

## הוראות

### שלב 1: בחירת דפוס אינטגרציה

| דפוס | טיפול בנתוני כרטיס | מתאים ל- |
|---------|-------------------|----------|
| **Low Profile (iframe/redirect)** | קארדקום מטפלת בהזנת הכרטיס | רוב האינטגרציות -- היקף PCI מינימלי |
| **ChargeToken (שרת-לשרת)** | טוקן בלבד, ללא נתוני כרטיס גולמיים | חיובים חוזרים, מנויים |
| **CreateDocument (שרת-לשרת)** | ללא נתוני כרטיס | הפקת חשבונית/קבלה עצמאית |

רוב בתי העסק הישראליים משתמשים ב-**Low Profile** לתשלום ראשוני + יצירת טוקן, ואז ב-**ChargeToken** לחיובים חוזרים. שניהם יכולים להפיק חשבוניות אוטומטית.

### שלב 2: הגדרת אימות

אישורי Cardcom API V11:
- `TerminalNumber` -- מזהה מסוף (השתמשו ב-`1000` לבדיקות)
- `ApiName` -- שם משתמש API (השתמשו ב-`bWlyb24gY2FyZGNvbQ==` לבדיקות)
- `ApiPassword` -- סיסמת API

**סביבת בדיקות:**
מסוף `1000` עם אישורי הבדיקה מאפשר בדיקת API מלאה ללא חיובים אמיתיים. כרטיס בדיקה: `4580000000000000`, כל תפוגה עתידית, CVV `123`.

אחסנו אישורים בצורה מאובטחת -- לעולם לא בקוד מקור או JavaScript בצד הלקוח.

### שלב 3: מימוש זרימת התשלום

#### אינטגרציית Low Profile (מומלץ)

זהו תהליך דו-שלבי:

**שלב 3א: יצירת דף התשלום**

```
POST https://secure.cardcom.solutions/api/v11/LowProfile/Create
Content-Type: application/json

{
  "TerminalNumber": 1000,
  "ApiName": "your-api-name",
  "ApiPassword": "your-api-password",
  "ReturnValue": "unique-order-id",
  "Amount": 100.00,
  "SuccessRedirectUrl": "https://yoursite.com/success",
  "FailedRedirectUrl": "https://yoursite.com/failed",
  "WebHookUrl": "https://yoursite.com/webhook",
  "Document": {
    "DocTypeToCreate": 101,
    "Name": "שם הלקוח",
    "Products": [
      {
        "Description": "שם המוצר",
        "UnitCost": 100.00,
        "Quantity": 1
      }
    ]
  },
  "CoinID": 1,
  "Language": "he"
}
```

התגובה כוללת `Url` -- הפנו את הלקוח לשם או הטמיעו כ-iframe.

**שלב 3ב: קבלת התוצאות**

לאחר השלמת התשלום, קארדקום קוראת ל-`WebHookUrl` שלכם או שאתם שואלים:

```
POST https://secure.cardcom.solutions/api/v11/LowProfile/GetLpResult
{
  "TerminalNumber": 1000,
  "ApiName": "your-api-name",
  "ApiPassword": "your-api-password",
  "LowProfileCode": "code-from-step-3a"
}
```

בדקו `DealResponse` = 0 להצלחה. חלצו `Token` לחיובים עתידיים.

### שלב 4: הפקת מסמכי מס ישראליים

היתרון הייחודי של קארדקום הוא הפקת מסמכים אוטומטית עם תשלומים. זה קריטי לעסקים ישראליים כי חוק המס מחייב הנפקת מסמכים מתאימים לכל עסקה.

**סוגי מסמכים (DocTypeToCreate):**

| קוד | סוג | מתי משתמשים |
|------|--------|-------------|
| 1 | חשבונית מס | מכירות B2B, שירותים |
| 2 | חשבונית זיכוי | החזרים, תיקונים |
| 3 | קבלה | אישור תשלום |
| 101 | חשבונית מס / קבלה | B2C עם תשלום (הנפוץ ביותר) |
| 400 | מסמך Iframe | בהקשר Low Profile |

**הכללת מסמך בזרימת התשלום:**
הוסיפו את אובייקט `Document` לבקשת Low Profile או ChargeToken (כפי שמוצג בשלב 3א). קארדקום מפיקה את המסמך אוטומטית כשהתשלום מצליח.

**הפקת מסמך עצמאית:**

```
POST https://secure.cardcom.solutions/api/v11/Documents/CreateDocument
{
  "TerminalNumber": 1000,
  "ApiName": "your-api-name",
  "ApiPassword": "your-api-password",
  "Document": {
    "DocTypeToCreate": 1,
    "Name": "שם הלקוח בע\"מ",
    "VAT_Number": "123456789",
    "Products": [
      {
        "Description": "שירותי פיתוח אתרים",
        "UnitCost": 5000.00,
        "Quantity": 1,
        "IsVatFree": false
      }
    ],
    "SendByEmail": true,
    "Email": "customer@example.com",
    "Language": "he",
    "CoinID": 1
  }
}
```

התגובה כוללת `InvoiceNumber`, `InvoiceType`, ו-`Link` למסמך ה-PDF.

### שלב 5: מימוש תשלומים חוזרים מבוססי טוקן (הוראות קבע)

למנויים וחיובים חוזרים:

1. **יצירת טוקן בתשלום הראשון:**
   - השתמשו ב-Low Profile עם יצירת טוקן מופעלת
   - התגובה כוללת `Token`, `CardValidityMonth`, `CardValidityYear`

2. **אחסון טוקן מאובטח:**
   - שמרו טוקן (פורמט UUID), תפוגת כרטיס, ו-4 ספרות אחרונות
   - הטוקן קשור למסוף שלכם

3. **חיוב הטוקן:**

```
POST https://secure.cardcom.solutions/api/v11/Transactions/Transaction
{
  "TerminalNumber": 1000,
  "ApiName": "your-api-name",
  "ApiPassword": "your-api-password",
  "Token": "token-uuid",
  "CardValidityMonth": "12",
  "CardValidityYear": "2027",
  "Amount": 99.00,
  "Document": {
    "DocTypeToCreate": 101,
    "Name": "שם המנוי",
    "Products": [
      {
        "Description": "מנוי חודשי - פברואר 2026",
        "UnitCost": 99.00,
        "Quantity": 1
      }
    ],
    "SendByEmail": true,
    "Email": "customer@example.com"
  }
}
```

כל חיוב טוקן יכול להפיק ולשלוח חשבונית במייל אוטומטית.

### שלב 6: עיבוד החזרים

החזר עסקה עם הפקת חשבונית זיכוי אופציונלית:

```
POST https://secure.cardcom.solutions/api/v11/Transactions/RefundByTransactionId
{
  "TerminalNumber": 1000,
  "ApiName": "your-api-name",
  "ApiPassword": "your-api-password",
  "TransactionId": "original-transaction-id",
  "Amount": 100.00,
  "Document": {
    "DocTypeToCreate": 2,
    "Name": "שם הלקוח"
  }
}
```

פעולה זו גם מבצעת החזר וגם מפיקה חשבונית זיכוי -- מטפלת בצד הפיננסי ובעמידה בתקנות המס בקריאה אחת.

### שלב 7: טיפול בשגיאות

בדקו קודי תגובה בכל קריאת API. תגובה של `0` פירושה הצלחה.

שגיאות נפוצות:

| קוד | משמעות | פעולה |
|------|---------|--------|
| 0 | הצלחה | המשיכו כרגיל |
| 5033 | מספר מסוף חסר | בדקו TerminalNumber בבקשה |
| 5034 | אימות נכשל | ודאו ApiName ו-ApiPassword |
| 5035 | סכום לא תקין | ודאו שAmount הוא מספר חיובי |
| 5100 | כרטיס סורב | בקשו מהמשתמש לנסות כרטיס אחר |
| 5101 | כרטיס פג תוקף | בקשו מהמשתמש לעדכן פרטי כרטיס |
| 5102 | CVV שגוי | בקשו מהמשתמש להזין CVV מחדש |
| 5200 | טוקן לא נמצא | ודאו UUID של טוקן ותאימות מסוף |
| 5300 | הפקת חשבונית נכשלה | בדקו פרמטרי Document |

למדריך תגובות API מלא, עיינו ב-`references/api-responses.md`.

## דוגמאות

### דוגמה 1: checkout לחנות מקוונת עם חשבונית
המשתמש אומר: "אני צריך לקבל תשלומים באתר המסחר האלקטרוני הישראלי שלי ולהפיק חשבוניות מס אוטומטית"
פעולות:
1. בחירה: אינטגרציית Low Profile עם DocTypeToCreate=101 (חשבונית מס + קבלה)
2. הנחיה: יצירת דף Low Profile עם פרטי מוצרים באובייקט Document
3. מימוש: handler ל-WebHook לאישור תשלום
4. תוצאה: הלקוח משלם, מקבל אוטומטית חשבונית מס/קבלה במייל כ-PDF
תוצאה: זרימת checkout מלאה עם עמידה אוטומטית בתקנות מסמכי מס ישראליים.

### דוגמה 2: מנוי SaaS חודשי
המשתמש אומר: "אני מפעיל מוצר SaaS, אני צריך לחייב משתמשים 149 ש"ח בחודש ולשלוח להם חשבוניות"
פעולות:
1. תשלום ראשון: Low Profile עם יצירת טוקן
2. שמירה: טוקן, תפוגת כרטיס מהתגובה
3. cron חודשי: ChargeToken עם Document לכל מחזור חיוב
4. טיפול: חיובים שנכשלו, כרטיסים שפג תוקפם, שליחת חשבוניות במייל
תוצאה: חיוב חוזר אוטומטי עם הפקת חשבונית חודשית.

### דוגמה 3: חשבונית עצמאית ללא תשלום
המשתמש אומר: "אני צריך להפיק חשבונית מס על העברה בנקאית שכבר קיבלתי"
פעולות:
1. שימוש: נקודת קצה CreateDocument (ללא עיבוד תשלום)
2. הגדרה: DocTypeToCreate=1 (חשבונית מס)
3. כלול: פרטי לקוח, פריטים, סכומים
4. שליחה: הגדירו SendByEmail=true עם מייל הלקוח
תוצאה: חשבונית מס מופקת ונשלחת במייל ללא עיבוד כרטיס אשראי.

### דוגמה 4: ביצוע החזר עם חשבונית זיכוי
המשתמש אומר: "לקוח רוצה החזר על הזמנה מספר 5678, צריך גם להנפיק חשבונית זיכוי"
פעולות:
1. שימוש: נקודת קצה RefundByTransactionId
2. כלול: Document עם DocTypeToCreate=2 (חשבונית זיכוי)
3. עיבוד: החזר + חשבונית זיכוי מופקים בקריאת API אחת
4. אימות: DealResponse=0 להצלחה
תוצאה: החזר מעובד וחשבונית זיכוי מופקת אוטומטית.

## משאבים מצורפים

### חומרי עזר
- `references/api-endpoints.md` -- מדריך מלא של נקודות קצה Cardcom REST API V11 כולל Low Profile, Transactions, Documents, RecurringPayments, Financial, ו-CompanyOperations. מפרט שדות בקשה/תגובה לכל נקודת קצה. עיינו בקובץ זה בעת בניית אינטגרציות API או חקירת פעולות זמינות.
- `references/api-responses.md` -- רשימה מלאה של קודי תגובה של קארדקום עם משמעויות וטיפול מומלץ לפעולות עסקה, טוקן, וחשבונית. עיינו בקובץ זה בעת דיבוג קריאות API שנכשלו.
- `references/document-types.md` -- קודי סוגי מסמכי מס ישראליים (1, 2, 3, 101, 400) עם שדות נדרשים, טיפול במע"מ, והנחיות שימוש בהתאם לחוק המס הישראלי. עיינו בקובץ זה בעת קביעת סוג מסמך להפקה לעסקה.

### סקריפטים
- `scripts/validate_cardcom_response.py` -- מאמת תגובת API של קארדקום: בודק קודי תגובה לפעולות עסקה, טוקן, וחשבונית, מוודא שדות נדרשים, ומסמן בעיות אינטגרציה נפוצות. הרצה: `python scripts/validate_cardcom_response.py --help`

## פתרון בעיות

### שגיאה: "5033 -- Terminal Number is Missing"
סיבה: TerminalNumber לא כלול או נשלח כסוג שגוי
פתרון: ודאו ש-TerminalNumber נשלח כמספר שלם (לא מחרוזת) בגוף ה-JSON. לבדיקות, השתמשו ב-1000.

### שגיאה: "5034 -- Authentication failed"
סיבה: ApiName או ApiPassword לא תקינים
פתרון: ודאו אישורים בלוח הבקרה של קארדקום. לבדיקות, השתמשו במסוף 1000 עם אישורי הבדיקה. האישורים נפרדים מסיסמת ההתחברות.

### שגיאה: "דף Low Profile נטען אבל התשלום נכשל"
סיבה: לרוב בעיה ב-WebHookUrl או כתובות redirect
פתרון: ודאו ש-SuccessRedirectUrl, FailedRedirectUrl, ו-WebHookUrl הן כתובות HTTPS נגישות ציבורית. כתובות localhost לא עובדות -- השתמשו בתעלה (ngrok) לפיתוח.

### שגיאה: "חשבונית נוצרה אבל לא נשלחה במייל"
סיבה: SendByEmail לא מוגדר או כתובת מייל חסרה
פתרון: הגדירו `SendByEmail: true` וכללו `Email` תקין באובייקט Document. בדקו תיקיית ספאם -- קארדקום שולחת מהדומיין שלהם.

### שגיאה: "חיוב טוקן מצליח אבל אין חשבונית"
סיבה: אובייקט Document חסר מבקשת ChargeToken
פתרון: כללו את אובייקט Document המלא עם DocTypeToCreate, Name, ו-Products בכל בקשת חיוב טוקן. הפקת מסמכים היא opt-in לכל עסקה, לא אוטומטית.
