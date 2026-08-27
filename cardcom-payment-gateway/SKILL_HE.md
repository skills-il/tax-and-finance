# שער תשלומים קארדקום

## הבהרה משפטית

זהו מדריך אינטגרציה טכני חינמי, הפועל באמצעות מודל בינה מלאכותית. הוא מסביר איך לקרוא ל-API של קארדקום ואיך כללי החשבוניות בישראל משליכים על כך. כל תוצריו מופקים באופן אוטומטי על ידי מודל בינה מלאכותית, ללא מעורבות, בדיקה או אישור של יועץ מס, רואה חשבון או עורך דין. אין כאן חוות דעת מס ואין ייעוץ מקצועי, ומודל בינה מלאכותית עלול לשגות, להשמיט נתונים או להציג מסקנה שגויה.

המסמכים שהאינטגרציה הזאת מפיקה הם מסמכי מס. האחריות להפיק אותם כראוי, לדווח ולשלם את המס היא שלכם, החישוב המחייב הוא של רשות המסים, וייצוג מול רשות המסים שמור למי שרשאי לכך לפי דין. השאלה אם חשבונית מסוימת טעונה מספר הקצאה, והשאלה אם ניתן לקזז מס תשומות, הן קביעות של רואה החשבון שלכם על העובדות שלכם בפועל. תנו ליועץ מס או לרואה חשבון לבדוק את תצורת החשבוניות לפני עלייה לאוויר, וטפלו בנתוני כרטיסי אשראי בהתאם ל-PCI DSS. כל שימוש בפלט של הסקיל הוא באחריותו הבלעדית של המשתמש.

## סקירה

קארדקום היא חברת סליקה ישראלית עם יתרון ייחודי אחד: הפקת חשבוניות וקבלות משולבת בתשלום, לפי חוק המס הישראלי. שערי תשלום אחרים מטפלים רק בתשלום עצמו, אבל קארדקום יכולה להפיק אוטומטית חשבוניות מס וקבלות כחלק מתהליך התשלום, דבר שעסקים ישראליים חייבים לספק לפי חוק.

המדריך הזה עובר אתכם דרך אינטגרציה עם REST API V11 של קארדקום לתשלומים, טוקניזציה, חיובים חוזרים והפקת מסמכים. כל endpoint וכל שם שדה במדריך הזה לקוחים ממפרט ה-OpenAPI הרשמי של קארדקום V11.

תיעוד רשמי נמצא בכתובת `https://secure.cardcom.solutions/Api/v11/Docs`, מרכז התמיכה בכתובת `https://support.cardcom.solutions`. V11 הוא ה-API הנוכחי נכון ל-2026, אין V12 פומבי.

קארדקום בנוף הישראלי: מתחרה בטרנזילה, ישראפיי וביט עסקי. התמחור נסגר מול כל בית עסק. קארדקום מפרסמת עמלה שמתחילה בכ-1.2% ויורדת בהתאם למחזור, אבל זו רצפה ולא הצעת מחיר, אז תתייחסו אליה כנקודת פתיחה בלבד ותפנו את המשתמש לקארדקום לקבלת מספר אמיתי במקום להבטיח לו תעריף. היתרון הייחודי שנשאר לעסקים ישראליים הוא הפקת מסמכי מס מובנית. לאינטגרציה עם טרנזילה, השתמשו ב-`tranzila-payment-gateway` במקום.

## הוראות

### שלב 1: בחירת דפוס אינטגרציה

| דפוס | טיפול בנתוני כרטיס | מתאים ל- |
|---------|-------------------|----------|
| **Low Profile (iframe/redirect)** | קארדקום מטפלת בהזנת הכרטיס | רוב האינטגרציות, היקף PCI מינימלי (SAQ-A) |
| **Transaction (שרת-לשרת)** | נתוני כרטיס גולמיים או טוקן | חיוב טוקנים שמורים, חיובים חוזרים |
| **CreateDocument (שרת-לשרת)** | ללא נתוני כרטיס | הפקת חשבונית/קבלה עצמאית |

רוב בתי העסק הישראליים משתמשים ב-Low Profile לתשלום הראשון ויצירת טוקן, ואז ב-endpoint של Transaction עם הטוקן השמור לחיובים חוזרים. כל זרימות התשלום יכולות להפיק חשבוניות אוטומטית על ידי צירוף אובייקט `Document`.

### שלב 2: הגדרת אימות

פרטי הגישה ל-Cardcom API V11:
- `TerminalNumber` (מספר שלם), מזהה המסוף שלכם (תשתמשו ב-`1000` לבדיקות)
- `ApiName` (מחרוזת), שם משתמש API
- `ApiPassword` (מחרוזת), סיסמת API. נדרשת בכ-26 מסכמות הבקשה של V11 בגרסת המפרט הנוכחית. המספר משתנה בין גרסאות, אז תקראו את הסכמה של נקודת הקצה במקום להסתמך עליו. כלל האצבע: **פעולות שקוראות או פועלות על נתונים ברמת החברה דורשות אותה, ופעולות שמחייבות כרטיס בודד לא.** היא נדרשת בכל כתיבה ב-`Documents/*`, בכל דוח ב-`Financial/*`, בכל קריאה ב-`TapTransactions/*`, וגם ב-`Transactions/ListTransactions`, ב-`RefundByTransactionId` וב-`SpecialTransactions`. היא בכלל לא שדה קיים ב-`LowProfile/Create` או ב-`Transactions/Transaction`, אז אל תשלחו אותה שם. במקרה של ספק, תבדקו את מערך ה-`required` של סכמת הבקשה ב-[מפרט ה-OpenAPI של V11](https://secure.cardcom.solutions/swagger/v11/swagger.json).

סביבת בדיקות: מסוף `1000` עם ה-`ApiName` של ה-demo מצוטט הרבה בספריות קהילתיות כסביבת הבדיקות, עם כרטיס בדיקה `4580000000000000`, כל תפוגה עתידית ו-CVV `123`. לא הצלחנו לאמת את הפרטים האלה מול עמוד רשמי של קארדקום, אז תתייחסו אליהם כפולקלור קהילתי: תאמתו את פרטי סביבת הבדיקות מול התמיכה של קארדקום לפני שאתם מסתמכים עליהם, ואל תניחו שקריאה מול מסוף 1000 לא יכולה להזיז כסף.

תשמרו פרטי גישה בצורה מאובטחת, אף פעם לא בקוד מקור או ב-JavaScript בצד הלקוח.

### שלב 3: מימוש זרימת התשלום

#### אינטגרציית Low Profile (מומלץ)

זה תהליך בשני שלבים.

**שלב 3א: יצירת דף התשלום**

```
POST https://secure.cardcom.solutions/api/v11/LowProfile/Create
Content-Type: application/json

{
  "TerminalNumber": 1000,
  "ApiName": "your-api-name",
  "Operation": "ChargeAndCreateToken",
  "ReturnValue": "unique-order-id",
  "Amount": 100.00,
  "SuccessRedirectUrl": "https://example.com/success",
  "FailedRedirectUrl": "https://example.com/failed",
  "WebHookUrl": "https://example.com/webhook",
  "ISOCoinId": 1,
  "Language": "he",
  "Document": {
    "DocumentTypeToCreate": "TaxInvoiceAndReceipt",
    "Name": "שם הלקוח",
    "Email": "customer@example.com",
    "Products": [
      { "Description": "שם המוצר", "UnitCost": 100.00, "Quantity": 1 }
    ]
  }
}
```

התגובה היא `CreateLowProfileResponse`: תבדקו `ResponseCode == 0` (הצלחה), תקראו את `Description` בכשלון. בהצלחה היא מחזירה `LowProfileId` (תשמרו אותו) ו-`Url` (תפנו לשם את הלקוח או תטמיעו כ-iframe). `UrlToBit` ו-`UrlToPayPal` מוחזרים גם הם כשהאמצעים האלה מופעלים במסוף שלכם.

השדה `Operation` שולט בהתנהגות: `ChargeOnly` (ברירת מחדל), `ChargeAndCreateToken`, `CreateTokenOnly`, `SuspendedDeal`, `Do3DSAndSubmit`.

**שלב 3ב: קבלת התוצאות**

אחרי שהתשלום מסתיים, קארדקום קוראת ל-`WebHookUrl` שלכם, או שאתם עושים שאילתה:

```
POST https://secure.cardcom.solutions/api/v11/LowProfile/GetLpResult
{
  "TerminalNumber": 1000,
  "ApiName": "your-api-name",
  "LowProfileId": "id-from-step-3a"
}
```

התגובה היא `LowProfileResult`, וה-`ResponseCode` ברמה העליונה שלה אינו תוצאת התשלום. המפרט מתאר אותו כשגיאת מפתח: הוא אומר שהבקשה נבנתה נכון, וזה הכול. תוצאת הכרטיס נמצאת ב-`TranzactionInfo` המקונן, שלפי המפרט אינו null רק בפעולות ChargeOnly ו-ChargeAndCreateToken, כלומר הוא כן null כשהלקוח נטש את הדף.

**לפני שמספקים משהו, כל חמשת התנאים האלה חייבים להתקיים:**

1. סטטוס HTTP הוא 200. תשובת 404 מחזירה `{"Message": "No HTTP resource was found..."}` בלי `ResponseCode` בכלל, אז בדיקה של `ResponseCode == 0` לבדה קוראת שגיאת ניתוב כ-`None`.
2. `ResponseCode` ברמה העליונה שווה 0.
3. `TranzactionInfo` אינו null.
4. `TranzactionInfo.ResponseCode` שווה 0 (700 ו-701 הם הצלחה רק ל-J2 ו-J5).
5. `TranzactionInfo.Amount` שווה לסכום שציפיתם לו, ו-`ReturnValue` תואם למזהה ההזמנה שלכם.

תבדקו גם את `TranzactionInfo.IsRefund` ואת `DealType`: החזר הוא עסקה מוצלחת ויעבור בדיקה נאיבית של `ResponseCode == 0`. אם ביקשתם מסמך, גם `DocumentInfo` חייב להיות לא-null, כי חיוב שהצליח עם `DocumentInfo: null` פירושו שלקחתם את הכסף ולא הפקתם חשבונית מס. הסקריפט `scripts/validate_cardcom_response.py --expect charge --amount <n>` מחיל את כל זה ונכשל בברירת מחדל בטוחה.

אף פעם אל תספקו על סמך נחיתת הדפדפן ב-`SuccessRedirectUrl`, שנמצא בשליטת הלקוח, או על סמך גוף ה-webhook, שהוא POST ציבורי לא מאומת. תתייחסו ל-webhook רק כאות לקרוא ל-`GetLpResult` ולבדוק מחדש. `TokenInfo` נושא את ה-`Token` השמור עם `CardMonth`/`CardYear`, ו-`SuspendedInfo` מכסה עסקאות ממתינות.

#### אמצעי תשלום חלופיים

תגובת ה-Low Profile כוללת כתובות לאמצעי תשלום חלופיים כשהם מופעלים במסוף שלכם:

| אמצעי | שדה בתגובה | הערות |
|--------|---------------|-------|
| **Bit** | `UrlToBit` | אפליקציית התשלום הנייד הפופולרית ביותר בישראל, מנותבת דרך קארדקום |
| **PayPal** | `UrlToPayPal` | תשלומים בינלאומיים |
| **Apple Pay** | נרנדר בתוך דף ה-Low Profile עצמו | מופיע באתר `cardcom.solutions` כארנק נתמך בדף התשלום |
| **Google Pay** | נרנדר בתוך דף ה-Low Profile עצמו | זהה ל-Apple Pay, מוצג ככפתור ארנק בדף ה-Low Profile |

`UrlToBit` ו-`UrlToPayPal` הם שדות URL מפורשים שאפשר להציג ליד טופס הכרטיס. Apple Pay ו-Google Pay עולים ככפתורי ארנק בתוך דף ה-Low Profile עצמו אחרי שמפעילים אותם במסוף, אז אין שדה URL נפרד בתגובה. הפעילו כל אמצעי במסוף שלכם בלוח הבקרה של קארדקום לפני שאתם סומכים עליו בפרודקשן.

### שלב 4: הפקת מסמכי מס ישראליים

היתרון הייחודי של קארדקום הוא הפקת מסמכים אוטומטית עם התשלומים. זה קריטי לעסקים ישראליים כי חוק המס מחייב להנפיק מסמכים מתאימים לכל עסקה.

סוג המסמך נקבע באמצעות השדה **`DocumentTypeToCreate`**, שהוא enum מסוג מחרוזת (לא מספר שלם). ערכים נפוצים:

| ערך | סוג | מתי משתמשים |
|-------|--------|-------------|
| `Auto` | אוטומטי | ברירת מחדל, משתמש בהגדרות לוח הבקרה שלכם |
| `TaxInvoiceAndReceipt` | חשבונית מס / קבלה | B2C עם תשלום (הנפוץ ביותר) |
| `TaxInvoice` | חשבונית מס | B2B, כשהקבלה מונפקת בנפרד |
| `Receipt` | קבלה | אישור תשלום בלבד |
| `TaxInvoiceAndReceiptRefund` | זיכוי חשבונית מס / קבלה | ביטול של `TaxInvoiceAndReceipt` |
| `TaxInvoiceRefund` | זיכוי חשבונית מס | ביטול של `TaxInvoice` |
| `ReceiptRefund` | זיכוי קבלה | ביטול של `Receipt` |
| `ProformaInvoice` | חשבונית עסקה / פרופורמה | מסמך הצעת מחיר טרום מכירה |
| `DonationReceipt` | קבלת תרומות | עמותות רשומות |

ל-enum המלא של `DocumentToCreate` יש 25 ערכים, וכולל גם `Quote`, `Order`, `OrderConfirmation`, `DeliveryNote`, `DemandForPayment`, `ProformaDealInvoice`, `ReceiptForTaxInvoice` ו-`CouponDocumentAndReceipt`. לרובם קיימות גרסאות החזר אבל לא לכולם: אין `QuoteRefund` ואין `OrderRefund`. אלה 11 שכן קיימות: `TaxInvoiceAndReceiptRefund`, `ReceiptRefund`, `OrderConfirmationRefund`, `DeliveryNoteRefund`, `DemandForPaymentRefund`, `ProformaDealInvoiceRefund`, `ProformaInvoiceRefund`, `TaxInvoiceRefund`, `DonationReceiptRefund`, `CouponDocumentAndReceiptRefund` ו-`ReceiptForTaxInvoiceRefund`. תאמתו את הערך המדויק שאתם צריכים מול התיעוד הרשמי בכתובת `https://secure.cardcom.solutions/Api/v11/Docs`.

איך לכלול מסמך בתהליך תשלום: תוסיפו את אובייקט `Document` לבקשת `LowProfile/Create` או `Transaction`. קארדקום מפיקה את המסמך אוטומטית כשהתשלום מצליח.

הפקת מסמך עצמאית:

```
POST https://secure.cardcom.solutions/api/v11/Documents/CreateDocument
{
  "ApiName": "your-api-name",
  "ApiPassword": "your-api-password",
  "Document": {
    "DocumentTypeToCreate": "TaxInvoice",
    "Name": "שם הלקוח בעמ",
    "TaxId": "123456789",
    "Email": "customer@example.com",
    "IsSendByEmail": true,
    "Languge": "he",
    "ISOCoinID": 1,
    "Products": [
      { "Description": "שירותי פיתוח אתרים", "UnitCost": 5000.00, "Quantity": 1 }
    ]
  }
}
```

התגובה היא `DocumentInfo`: תבדקו `ResponseCode == 0`, ואז תקראו את `DocumentType`, `DocumentNumber`, `AccountId` ו-`DocumentUrl` (קישור ל-PDF).

שימו לב לאיות האמיתי של השדות ב-V11 בתוך אובייקט `Document`: `DocumentTypeToCreate` (enum מחרוזת), `Name` (ה"document To", נדרש, עד 50 תווים), `TaxId` (מספר עוסק או מספר זהות, מחליף את `VAT_Number` הישן), `IsSendByEmail` (מחליף את `SendByEmail`), `Languge` (האיות בסכמה הזו, חסרה ה-`a` השנייה; שימו לב שאובייקט המסמך של Low Profile, `DocumentLP`, משתמש דווקא באיות התקין `Language`), `ISOCoinID` (מחליף את `CoinID`), `IsVatFree`, ו-`Products[]` עם `Description`, `UnitCost`, `Quantity`, `IsVatFree`. ראו את `references/document-types.md` לרשימת השדות המלאה.

### שלב 4.5: מספר הקצאה בחשבוניות מס

**אל תחפשו שדה של מספר הקצאה ב-API. אין כזה, וזו לא השמטה.** קארדקום פיתחה ממשק ישיר מול
רשות המסים, ולכן כשמפיקים חשבונית מס מעל התקרה בקשת מספר ההקצאה נשלחת אוטומטית בעת הפקת
המסמך, בצד השרת. בגוף הבקשה של `CreateDocument` אין שדה `AllocationNumber`, ומפתח שיחפש
אותו במפרט ה-OpenAPI יסיק בטעות שקארדקום לא תומכת בדרישה.

**זה לא פעיל כברירת מחדל. נדרשת הגדרה חד-פעמית, ובלעדיה הלקוח שלכם לא יוכל לקזז מע"מ
תשומות.** קיום מספר הקצאה על חשבונית מס הוא תנאי לניכוי מס תשומות אצל המקבל, בכל חשבונית
שסכומה לפני מע"מ עולה על התקרה שנקבעה בחוק. ההגדרה, שמבצע בעל העסק או הדירקטור פעם אחת
באתר רשות המסים, היא:

1. הזדהות באזור האישי באתר רשות המסים, ורישום אם עוד אין חשבון.
2. בחברה בע"מ או באיחוד עוסקים צריך גם לבצע רישום פרטי תאגיד.
3. במערכת הרשאה לפעולות דיגיטליות של רשות המסים (יש אליה קישור מעמוד השירות של מספר
   הקצאה) נותנים את ההרשאה ובוחרים את שני הנושאים של חשבוניות ישראל, לא אחד מהם. נושא
   אחד הוא אימות מספר ההקצאה שעל חשבונית של ספק, והשני הוא בקשת מספר הקצאה לחשבונית
   שאתם מוציאים ללקוח. לבחור רק את הראשון זו הטעות הנפוצה, והיא משאירה את החשבוניות
   שלכם בלי מספר. הניסוח המדויק של שני הנושאים מופיע רק בתוך המערכת, שדורשת הזדהות, אז
   תזהו אותם לפי המשמעות ולא לפי מחרוזת שמצוטטת כאן.
4. בוחרים לכמה זמן ניתנת ההרשאה, ומקבל ההרשאה מאשר אותה.

**מתווה התקרות (הסכומים לפני מע"מ):**

החובה למספר הקצאה נכנסה לתוקף במאי 2024.

| נכון מ | תקרה |
|---------|------|
| מאי 2024 | 25,000 ש"ח |
| ינואר 2025 | 20,000 ש"ח |
| 1.1.2026 | 10,000 ש"ח |
| 1.6.2026 | **5,000 ש"ח (בתוקף עכשיו)** |

חשבוניות שתאריכן לפני מאי 2024 קדמו למודל ומעולם לא נדרש להן מספר. הסף נקבע לפי תאריך
המסמך עצמו, אז אם אתם מפיקים מחדש, מעבירים או מבקרים מסמכים ישנים, תבדקו כל אחד מול הסף
שהיה בתוקף בתאריך שלו ולא מול 5,000 של היום. החוק כותב "עולה על", כך שמסמך בדיוק בגובה
הסף אינו בתחולה.

עוסק פטור לא מושפע, כי הוא לא מוציא חשבוניות מס ולא מקזז מע"מ תשומות. גם חשבוניות בשיעור
אפס וחשבוניות פטורות בלבד מחוץ לתחולה (סעיף 47(א2)(1)), אז חשבונית ייצוא אינה טעונה מספר
יהיה סכומה אשר יהיה. אם האינטגרציה נכתבה מוקדם יותר ב-2026 מול הסף של 10,000, הטווח שבין
5,000 ל-10,000 הוא מה שצריך לבדוק מחדש.

### שלב 4.6: מניעת כפילות, ואישור מול גבייה

**תשלחו `ExternalUniqTranId` בכל קריאה ל-`Transactions/Transaction`.** זה מזהה ייחודי משלכם
לחיוב, והמפרט מפורש: אם יישלח אותו `ExternalUniqTranId` פעם נוספת, תקבלו שגיאה 608. בלי זה,
קרון שהקריאה שלו נכשלה בטיימאאוט אחרי שקארדקום כבר חייבה את הכרטיס ינסה שוב ויחייב את הלקוח
פעמיים.

**608 אומר "כבר חויב", לא "התשלום נכשל".** זה קוד השגיאה היחיד שחייבים לטפל בו בנפרד:
תתייחסו אליו ככפילות שנחסמה כראוי, ולא ככישלון שצריך לנסות שוב או לחייב ידנית. אחרי כל
טיימאאוט או תוצאה לא ברורה, תקראו ל-`POST /api/v11/Transactions/GetTransactionByExternalUniqTran`
כדי לברר אם החיוב המקורי עבר, לפני שאתם עושים משהו אחר.

**J2 ו-J5 אינם אותו דבר, ו-700/701 לא אומרים שהלקוח לא נגוע.** השדה
`Advanced.JValidateType` בוחר בין J2 (אימות כרטיס פשוט, שום דבר לא נתפס) לבין J5 (אישור,
שתופס את הכסף במסגרת של בעל הכרטיס). J5 חייב גבייה לאחר מכן באמצעות
`Advanced.ApprovalNumber`, שמתועד במפרט כגבייה של בקשת J5. אישור שלא נגבה משאיר את כספי
הלקוח תפוסים עד שהוא פג, אז אם אתם משתמשים ב-J5 חייב להיות לכם שלב גבייה ומסלול שחרור.

### שלב 5: תשלומים חוזרים מבוססי טוקן

למנויים וחיובים חוזרים (הוראות קבע), קארדקום תומכת בשתי גישות:

- **הוראת קבע על כרטיס אשראי**, חיוב של `Token` שמור על מחזור קבוע. מטופל בשלב הזה.
- **הוראת קבע בנקאית דרך מס"ב**, חיוב ישיר מחשבון הבנק הישראלי של הלקוח. מנוהל דרך ה-endpoints של `RecuringPayments` (`RecuringPayments/GetRecurringPayment`, `GetRecurringPaymentHistory`, `IsBankNumberValid`). תשתמשו בזה כשהלקוח מעדיף חיוב בנקאי על פני חיוב כרטיס או כשאין כרטיס זמין. ההוראה עצמה מוקמת מלוח הבקרה של קארדקום.

לתשלום חוזר מבוסס כרטיס:

1. **יצירת טוקן בתשלום הראשון.** תשתמשו ב-Low Profile עם `Operation: "ChargeAndCreateToken"` (או `"CreateTokenOnly"`). ה-`LowProfileResult` מחזיר `TokenInfo` עם `Token`, `CardMonth`, `CardYear` ו-`TokenExDate` (התאריך שבו הטוקן נמחק ממערכת קארדקום).

2. **אחסון הטוקן בצורה מאובטחת.** תשמרו את מחרוזת ה-`Token`, תפוגת הכרטיס ו-4 הספרות האחרונות. הטוקן קשור למסוף שלכם.

3. **חיוב הטוקן** דרך endpoint של Transaction:

```
POST https://secure.cardcom.solutions/api/v11/Transactions/Transaction
{
  "TerminalNumber": 1000,
  "ApiName": "your-api-name",
  "Token": "token-uuid",
  "CardExpirationMMYY": "1227",
  "Amount": 99.00,
  "ISOCoinId": 1,
  "Document": {
    "DocumentTypeToCreate": "TaxInvoiceAndReceipt",
    "Name": "שם המנוי",
    "Email": "customer@example.com",
    "IsSendByEmail": true,
    "Products": [
      { "Description": "מנוי חודשי", "UnitCost": 99.00, "Quantity": 1 }
    ]
  }
}
```

התגובה היא `TransactionInfo`: תבדקו `ResponseCode == 0` (שימו לב ש-`700` ו-`701` נחשבים גם הם הצלחה לעסקאות אימות בלבד מסוג J2/J5), ואז תקראו את `TranzactionId`, `Token`, `DocumentNumber` ו-`DocumentUrl`. כל חיוב טוקן יכול להפיק ולשלוח חשבונית במייל אוטומטית כשמצורף אובייקט `Document`.

### שלב 6: ביצוע החזרים

החזר עסקה לפי מזהה העסקה של קארדקום:

```
POST https://secure.cardcom.solutions/api/v11/Transactions/RefundByTransactionId
{
  "ApiName": "your-api-name",
  "ApiPassword": "your-api-password",
  "TransactionId": 219282004,
  "PartialSum": 100.00,
  "CancelOnly": false,
  "AllowMultipleRefunds": false
}
```

`ApiPassword` נדרשת להחזרים. `PartialSum` מחזיר חלק מהעסקה (תשמיטו אותו כדי להחזיר את הסכום המלא). `CancelOnly: true` מבטל עסקה לפני שהיא הופקדה. התגובה היא `RefundByTransactionIdResp`: תבדקו `ResponseCode == 0`, ואז תקראו את `NewTranzactionId` (מזהה עסקת ההחזר).

כדי להנפיק את מסמך הזיכוי התואם, תקראו ל-`Documents/CreateDocument` עם `DocumentTypeToCreate` של זיכוי כמו `TaxInvoiceAndReceiptRefund` או `TaxInvoiceRefund`.

### שלב 6.5: שליפת עסקאות לדוחות

כדי למשוך טווח תאריכים של עסקאות (התאמות, דוחות חודשיים, דשבורדים):

```
POST https://secure.cardcom.solutions/api/v11/Transactions/ListTransactions
{
  "ApiName": "your-api-name",
  "ApiPassword": "your-api-password",
  "FromDate": "01062026",
  "ToDate": "30062026",
  "TranStatus": "Success",
  "Page": 1,
  "Page_size": 100
}
```

ארבעה דברים בנקודת הקצה הזו מפילים כמעט כל אינטגרציה:

1. שדה `ApiPassword` נדרש. זו קריאה ברמת החברה, לא חיוב בודד.
2. אין שדה `TerminalNumber`. הסכמה מגדירה `additionalProperties: false`, ולכן שליחת `TerminalNumber` נדחית על הסף. כדי לצמצם את התוצאות למסוף אחד, תשתמשו ב-`LimitForTerminal` האופציונלי.
3. התאריכים הם מחרוזות בפורמט `DDMMYYYY`, לא ISO. הערך `01062026` הוא 1 ביוני 2026.
4. השדות `Page` ו-`Page_size` שניהם נדרשים, ו-`Page_size` חייב להיות בין 10 ל-2000. הדפדוף מתחיל מ-1, לא מ-0.

התגובה היא `GetTranzactionsResp`: תבדקו `ResponseCode == 0`, ואז תקראו את `Tranzactions` (מערך של `TransactionInfo`), יחד עם `Page` ו-`Page_size` שמוחזרים בחזרה. תמשיכו לבקש את העמוד הבא עד שעמוד מחזיר פחות שורות מ-`Page_size`.

נקודת הקצה `Transactions/SpecialTransactions` היא אחות שלה לקריאה בלבד (היא מחזירה עסקאות אחרות כשקארדקום היא הסולק שלכם) ומקבלת בדיוק את אותם ארבעה שדות נדרשים: `ApiName`, `ApiPassword`, `FromDate`, `ToDate`. למרות השם, היא לא יוצרת שום דבר.

### שלב 7: עסקאות מושהות

עסקה מושהית מאשרת כוונת תשלום בלי חיוב מיידי:

1. תיצרו סשן Low Profile עם `Operation: "SuspendedDeal"`.
2. ה-`LowProfileResult` מחזיר `SuspendedInfo` עם `SuspendedDealId`.
3. תחייבו את העסקה המושהית מאוחר יותר דרך לוח הבקרה של קארדקום או דרך נקודת הקצה `SuspendedDeals/Charge` (קבוצת `SuspendedDeals` כוללת גם `Cancel` ו-`GetSuspendedDealInfo`).

שימושי להרשאות מראש ולשירותים שמחויבים אחרי אספקה. ודאו את שדות הבקשה המדויקים של `SuspendedDeals/Charge` מול התיעוד הרשמי לפני חיבור קריאת החיוב המאוחר.

### שלב 8: טיפול בשגיאות

כל endpoint ב-V11 מחזיר מספר שלם `ResponseCode` ומחרוזת `Description`. `ResponseCode == 0` משמעו הצלחה, כל ערך שאינו אפס הוא שגיאת מפתח/עסקה ו-`Description` נושא את הסיבה הקריאה לאדם.

```python
import requests

resp = requests.post(
    "https://secure.cardcom.solutions/api/v11/Transactions/Transaction",
    json=payload,
).json()

if resp.get("ResponseCode") == 0:
    deal_id = resp["TranzactionId"]
else:
    log_error(f"Cardcom error {resp.get('ResponseCode')}: {resp.get('Description')}")
```

תמיד תבדקו גם את סטטוס ה-HTTP (200 משמעו שהבקשה התקבלה) וגם את `ResponseCode` (0 משמעו שהפעולה הצליחה). התיעוד הרשמי בכתובת `https://secure.cardcom.solutions/Api/v11/Docs` נושא את מדריך השגיאות המספרי המלא, אל תקודדו מיפוי קבוע של קוד שגיאה להודעה, תקראו את `Description` במקום. ראו את `references/api-responses.md` לדפוס הטיפול.

## דוגמאות

### דוגמה 1: checkout לחנות מקוונת עם חשבונית
המשתמש אומר: "אני צריך לקבל תשלומים באתר המסחר האלקטרוני הישראלי שלי ולהפיק חשבוניות מס אוטומטית"
פעולות:
1. תבחרו Low Profile עם `DocumentTypeToCreate: "TaxInvoiceAndReceipt"`.
2. תיצרו את דף ה-Low Profile דרך `LowProfile/Create` עם פרטי המוצרים באובייקט `Document`.
3. תממשו handler ל-`WebHookUrl` שקורא ל-`LowProfile/GetLpResult`.
תוצאה: הלקוח משלם ומקבל אוטומטית חשבונית מס/קבלה במייל כ-PDF.

### דוגמה 2: מנוי SaaS חודשי
המשתמש אומר: "אני מפעיל מוצר SaaS, אני צריך לחייב משתמשים 149 שח בחודש ולשלוח להם חשבוניות"
פעולות:
1. תשלום ראשון: `LowProfile/Create` עם `Operation: "ChargeAndCreateToken"`.
2. תשמרו את ה-`Token`, `CardMonth`, `CardYear` מתוך `TokenInfo`.
3. cron חודשי: `Transactions/Transaction` עם הטוקן, `ExternalUniqTranId` חדש לכל מחזור חיוב, ואובייקט `Document`.
תוצאה: חיוב חוזר אוטומטי עם הפקת חשבונית חודשית.

### דוגמה 3: חשבונית עצמאית בלי תשלום
המשתמש אומר: "אני צריך להפיק חשבונית מס על העברה בנקאית שכבר קיבלתי"
פעולות:
1. תשתמשו ב-`Documents/CreateDocument` (בלי עיבוד תשלום).
2. תגדירו `DocumentTypeToCreate: "TaxInvoice"`.
3. תכללו `Name`, `TaxId`, `Products[]`, תגדירו `IsSendByEmail: true` עם מייל הלקוח.
תוצאה: חשבונית מס מופקת ונשלחת במייל בלי לעבד כרטיס אשראי.

### דוגמה 4: ביצוע החזר עם מסמך זיכוי
המשתמש אומר: "לקוח רוצה החזר על הזמנה מספר 5678, צריך גם להנפיק חשבונית זיכוי"
פעולות:
1. תקראו ל-`Transactions/RefundByTransactionId` עם `TransactionId` ו-`ApiPassword`.
2. תבדקו `ResponseCode == 0` ותקראו את `NewTranzactionId`.
3. תקראו ל-`Documents/CreateDocument` עם `DocumentTypeToCreate: "TaxInvoiceAndReceiptRefund"`.
תוצאה: ההחזר מעובד ומסמך הזיכוי התואם מופק.

### דוגמה 5: קבלת תשלום Bit, Apple Pay ו-Google Pay
המשתמש אומר: "אני רוצה לאפשר ללקוחות לשלם גם עם Bit, Apple Pay ו-Google Pay בנוסף לכרטיס אשראי"
פעולות:
1. תפעילו כל אמצעי (Bit, Apple Pay, Google Pay) במסוף קארדקום דרך לוח הבקרה.
2. תיצרו סשן Low Profile כרגיל דרך `LowProfile/Create`.
3. תציגו את `UrlToBit` מהתגובה לצד טופס הכרטיס. Apple Pay ו-Google Pay יופיעו ככפתורי ארנק בתוך דף ה-Low Profile עצמו, בלי URL נפרד.
תוצאה: לקוחות יכולים לבחור בין כרטיס אשראי, Bit, Apple Pay ו-Google Pay, אותו תהליך webhook.

## ספריות קהילתיות

- **@tsdiapi/cardcom** (TypeScript/Node.js), לקוח API V11 עם תשלומים, החזרים, טוקניזציה, שאילתות עסקאות. התקנה: `npm install @tsdiapi/cardcom`
- **CardCom/OpenFields-FrontEnd-React** (React), דוגמת OpenFields רשמית. ראו `https://github.com/CardCom/OpenFields-FrontEnd-React`
- **CardCom/OpenFields-Backend-Node** (Node.js), דוגמת backend רשמית. ראו `https://github.com/CardCom/OpenFields-Backend-Node`

## קישורים לחומרי עזר

| משאב | כתובת |
|----------|-----|
| תיעוד API V11 (מדריך OpenAPI) | `https://secure.cardcom.solutions/Api/v11/Docs` |
| מרכז התמיכה של קארדקום | `https://support.cardcom.solutions` |
| דוגמת OpenFields ב-React | `https://github.com/CardCom/OpenFields-FrontEnd-React` |
| דוגמת OpenFields ב-Node.js | `https://github.com/CardCom/OpenFields-Backend-Node` |

## משאבים מצורפים

### חומרי עזר
- `references/api-endpoints.md`, מדריך endpoints של Cardcom REST API V11: נתיבי LowProfile, Transactions, Documents, RecuringPayments, Financial ו-CompanyOperations עם שדות הבקשה/תגובה המרכזיים שלהם. תסתכלו עליו כשאתם בונים אינטגרציות API.
- `references/api-responses.md`, דפוס התגובה `ResponseCode` + `Description` של V11, אובייקטי התגובה לכל פעולה, וזרימת הטיפול המומלצת בשגיאות. תסתכלו עליו כשאתם מדבגים קריאות API שנכשלו.
- `references/document-types.md`, ה-enum המחרוזתי `DocumentTypeToCreate`, רשימת השדות של אובייקט `Document`, וטיפול במעמ לפי חוק המס הישראלי. תסתכלו עליו כשאתם מחליטים איזה סוג מסמך להפיק.

### סקריפטים
- `scripts/validate_cardcom_response.py`, מאמת תגובת API של קארדקום V11: בודק `ResponseCode`, מציג את `Description`, ומוודא שדות צפויים לפעולות עסקה, טוקן ומסמך. רק `ResponseCode` 0 נחשב הצלחה; הקודים 700/701 נדחים אלא אם מוסיפים `--validation-only`, כי הם אומרים שבדיקת כרטיס מסוג J2/J5 עברה ושום כסף לא זז. להרצה: `python scripts/validate_cardcom_response.py --help`

## מלכודות נפוצות
- בדיקת ההצלחה ב-V11 היא `ResponseCode == 0`, לא `DealResponse == 0`. `DealResponse` לא קיים ב-V11, סוכנים שאומנו על דוגמאות קארדקום ישנות ממציאים אותו. כל endpoint ב-V11 מחזיר `ResponseCode` יחד עם מחרוזת `Description`.
- `DocumentTypeToCreate` הוא enum מסוג מחרוזת (`"TaxInvoiceAndReceipt"`, `"TaxInvoice"`, `"Receipt"`, ...), לא קוד מספרי. קודי מסמך מספריים כמו `101` או `400` שייכים לממשקי `.aspx` ישנים, לא ל-V11.
- ה-`TerminalNumber` חייב להישלח כמספר שלם, לא כמחרוזת. סוכנים נוטים לעטוף אותו במירכאות.
- `ApiPassword` נדרשת בהרבה יותר מהחזרים ומסמכים: 26 סכמות בקשה מציינות אותה כ-required במפרט הנוכחי. אל תכלילו את זה למשפחת נתיבים שלמה, כי יש חריגים אמיתיים: ל-`Documents/ExternalShopCreateDocument` אין בכלל שדה `ApiPassword`, ו-`Documents/CrossDocument` ו-`TapTransactions/NotifyExternalTapTransaction` לא מגדירות מערך `required`. תבדקו את הסכמה של נקודת הקצה המסוימת. מקרה אחד פועל בכיוון ההפוך: `ApiPassword` אינו שדה ברמה העליונה של `LowProfile/Create` או `Transactions/Transaction`, אבל הוא כן נדרש בתוך האובייקט המקונן `Advanced` / `AdvancedDefinition` כשמסמנים `IsRefund` (ב-Transaction) או `IsRefundDeal` (ב-LowProfile). זה מסלול ההחזר השני, שמשמש כשיש לכם טוקן או כרטיס אבל אין מזהה עסקה מקורי. קריאות וכתיבות ברמת החברה דורשות אותה (`ListTransactions`, `SpecialTransactions`, `RefundByTransactionId`, כל הכתיבות ב-`Documents/*`, כל הדוחות ב-`Financial/*`, כל `TapTransactions/*`), וחיובי כרטיס בודד לא. היא אפילו לא שדה קיים ב-`LowProfile/Create` או ב-`Transaction`, אז גם שליחה שלה שם היא טעות. סוכנים נוטים להשמיט אותה ב-`ListTransactions` כי הנחיות ישנות תיארו אותה כנדרשת "רק להחזרים ומסמכים".
- נקודות הקצה לדוחות `ListTransactions` ו-`SpecialTransactions` לא מקבלות `TerminalNumber`, ושתיהן מגדירות `additionalProperties: false`, ולכן הכללה שלו מפילה את הקריאה. תצמצמו למסוף מסוים עם `LimitForTerminal` ב-`ListTransactions`. התאריכים שלהן הם מחרוזות `DDMMYYYY`, ו-`ListTransactions` דורשת בנוסף `Page` ו-`Page_size` בטווח 10 עד 2000.
- שימו לב לאיות האמיתי של השדות ב-V11: `ISOCoinID` / `ISOCoinId`, `IsSendByEmail` (לא `SendByEmail`), `TaxId` (לא `VAT_Number`). **שדה השפה מאויית אחרת לפי אובייקט המסמך שבו אתם נמצאים, וכל הסכמות האלה דוחות שדות לא מוכרים, ולכן טעות כאן מפילה את הקריאה:** `Document` (בקריאת `CreateDocument` העצמאית) ו-`DocumentTran` (ב-`Transaction`) משתמשים באיות השגוי `Languge`, בעוד `DocumentLP`, המסמך שמצרפים ל-`LowProfile/Create`, משתמש באיות התקין `Language`. שימוש ב-`Languge` בכל מקום שובר את זרימת ה-Low Profile, שהיא הזרימה שהסקיל ממליץ עליה קודם.
- שיעור המע"מ הנוכחי בישראל הוא 18% (מינואר 2025; לפני כן הוא היה 17%, אז מסמך שמופק מחדש לתקופה קודמת צריך את השיעור שהיה בתוקף בתאריך שלו). קארדקום מחשבת מעמ בצד השרת, אז סכומי המסמך מטופלים לפי דגל `IsVatFree`.
- **היקף PCI**: Low Profile מארח שומר אתכם ב-SAQ-A. שרת-לשרת `Transaction` עם `CardNumber`/`CVV2` גולמיים נופל ל-SAQ-D. התקן הנוכחי הוא PCI DSS v4.0.1 (עדכון מצומצם שפורסם ביוני 2024), ו-51 הדרישות הדחויות נכנסו לתוקף ב-31 במרץ 2025, כך שכולן בתוקף היום. עדיף להישאר עם Low Profile או טוקנים אלא אם יש סיבה אמיתית לגעת בנתוני כרטיס גולמיים.
- **לוח הסליקה הכספית** נקבע ברמת המסוף, לא בכל בקשה, ולא נקבע דרך ה-API. קארדקום מפרסמת שלושה מסלולי זיכוי: חודשי (עסקאות מה-1 לחודש ועד יום לפני סוף החודש מזוכות ב-6 לחודש העוקב), שבועי (מיום ראשון עד יום שישי, זיכוי ביום רביעי בשבוע שאחרי), ודו-חודשי (עסקאות מה-1 עד ה-15 מזוכות ב-2 לחודש העוקב, ועסקאות מה-16 ועד יום לפני סוף החודש מזוכות ב-8). עדיין כדאי לוודא איזה מסלול מוגדר בפועל במסוף של בית העסק לפני שמבטיחים לו יום מסוים.
- **ל-Apple Pay ו-Google Pay אין שדות URL נפרדים** כמו `UrlToBit` / `UrlToPayPal`. הם מופיעים ככפתורי ארנק בתוך דף ה-Low Profile עצמו אחרי שמפעילים אותם במסוף בלוח הבקרה.

## פתרון בעיות

### שגיאה: `ResponseCode` שאינו אפס ב-`LowProfile/Create`
סיבה: בעיית אימות או ולידציה בבקשה.
פתרון: תקראו את מחרוזת ה-`Description` בתגובה, היא מציינת את הבעיה המדויקת. תוודאו ש-`TerminalNumber` הוא מספר שלם ו-`ApiName` נכון. מדריך השגיאות המספרי המלא נמצא בכתובת `https://secure.cardcom.solutions/Api/v11/Docs`.

### שגיאה: "דף Low Profile נטען אבל התשלום נכשל"
סיבה: בדרך כלל בעיה ב-`WebHookUrl` או בכתובות ה-redirect.
פתרון: תוודאו ש-`SuccessRedirectUrl`, `FailedRedirectUrl` ו-`WebHookUrl` הן כתובות HTTPS נגישות מהאינטרנט. כתובות localhost לא עובדות, תשתמשו ב-ngrok לפיתוח.

### שגיאה: "החזר מחזיר `ResponseCode` שאינו אפס"
סיבה: `ApiPassword` חסרה, או שהעסקה כבר הופקדה ושלחתם `CancelOnly: true`.
פתרון: תכללו `ApiPassword` בכל בקשת החזר. תשתמשו ב-`CancelOnly: true` רק לפני הפקדה, אחרי הפקדה תשלחו החזר אמיתי (תשמיטו את `CancelOnly` או תגדירו אותו `false`).

### שגיאה: "חשבונית נוצרה אבל לא נשלחה במייל"
סיבה: `IsSendByEmail` לא מוגדר או שחסר אימייל.
פתרון: תגדירו `IsSendByEmail: true` ותכללו `Email` תקין באובייקט `Document`. תבדקו בתיקיית ספאם, קארדקום שולחת מהדומיין שלה.

### שגיאה: "חיוב טוקן מצליח אבל אין חשבונית"
סיבה: אובייקט `Document` חסר מבקשת ה-`Transaction`.
פתרון: תכללו את אובייקט `Document` המלא עם `DocumentTypeToCreate`, `Name` ו-`Products` בכל חיוב טוקן. הפקת מסמכים היא opt-in לכל עסקה.
