# שער תשלומים קארדקום

## סקירה

קארדקום היא חברת סליקה ישראלית עם יתרון ייחודי אחד: הפקת חשבוניות וקבלות משולבת בתשלום, לפי חוק המס הישראלי. שערי תשלום אחרים מטפלים רק בתשלום עצמו, אבל קארדקום יכולה להפיק אוטומטית חשבוניות מס וקבלות כחלק מתהליך התשלום, דבר שעסקים ישראליים חייבים לספק לפי חוק.

המדריך הזה עובר אתכם דרך אינטגרציה עם REST API V11 של קארדקום לתשלומים, טוקניזציה, חיובים חוזרים והפקת מסמכים. כל endpoint וכל שם שדה במדריך הזה לקוחים ממפרט ה-OpenAPI הרשמי של קארדקום V11.

תיעוד רשמי נמצא בכתובת `https://secure.cardcom.solutions/Api/v11/Docs`, מרכז התמיכה בכתובת `https://support.cardcom.solutions`. V11 הוא ה-API הנוכחי נכון ל-2026, אין V12 פומבי.

קארדקום בנוף הישראלי: מתחרה בטרנזילה, ישראפיי וביט עסקי. תמחור 2026 הוא בערך 1.2%-1.4% לעסקה עם תוכניות חודשיות שמתחילות בסביבות 59 ש"ח לחודש לתוסף החשבוניות. המספרים המדויקים נסגרים מול כל בית עסק. היתרון הייחודי שנשאר לעסקים ישראליים הוא הפקת מסמכי מס מובנית. לאינטגרציה עם טרנזילה, השתמשו ב-`tranzila-payment-gateway` במקום.

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
- `ApiPassword` (מחרוזת), סיסמת API, נדרשת רק להחזרים ולהפקת מסמכים, לא נשלחת בחיוב רגיל

סביבת בדיקות: מסוף `1000` עם ה-`ApiName` של ה-demo מאפשר בדיקת API בלי חיובים אמיתיים. כרטיס בדיקה: `4580000000000000`, כל תפוגה עתידית, CVV `123`.

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

התגובה היא `LowProfileResult`: תבדקו `ResponseCode == 0`. בהצלחה היא נושאת את `TranzactionInfo` (פרטי העסקה), `TokenInfo` (ה-`Token` השמור יחד עם `CardMonth`/`CardYear`), `DocumentInfo` (המסמך שהופק), ו-`SuspendedInfo` (לעסקאות מושהות). כל אובייקט מקונן הוא `null` כשהוא לא רלוונטי.

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

ה-enum המלא (`DocumentToCreate` במפרט ה-OpenAPI) כולל גם `Quote`, `Order`, `OrderConfirmation`, `DeliveryNote`, `DemandForPayment`, `ProformaDealInvoice`, `ReceiptForTaxInvoice`, `CouponDocumentAndReceipt` והגרסאות `*Refund` שלהם. תאמתו את הערך המדויק שאתם צריכים מול התיעוד הרשמי בכתובת `https://secure.cardcom.solutions/Api/v11/Docs`.

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

שימו לב לאיות האמיתי של השדות ב-V11 בתוך אובייקט `Document`: `DocumentTypeToCreate` (enum מחרוזת), `Name` (ה"document To", נדרש, עד 50 תווים), `TaxId` (מספר עוסק או מספר זהות, מחליף את `VAT_Number` הישן), `IsSendByEmail` (מחליף את `SendByEmail`), `Languge` (האיות הרשמי של V11, חסרה ה-`a` השנייה), `ISOCoinID` (מחליף את `CoinID`), `IsVatFree`, ו-`Products[]` עם `Description`, `UnitCost`, `Quantity`, `IsVatFree`. ראו את `references/document-types.md` לרשימת השדות המלאה.

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
3. cron חודשי: `Transactions/Transaction` עם הטוקן ואובייקט `Document` לכל מחזור חיוב.
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
- `scripts/validate_cardcom_response.py`, מאמת תגובת API של קארדקום V11: בודק `ResponseCode`, מציג את `Description`, ומוודא שדות צפויים לפעולות עסקה, טוקן ומסמך. להרצה: `python scripts/validate_cardcom_response.py --help`

## מלכודות נפוצות
- בדיקת ההצלחה ב-V11 היא `ResponseCode == 0`, לא `DealResponse == 0`. `DealResponse` לא קיים ב-V11, סוכנים שאומנו על דוגמאות קארדקום ישנות ממציאים אותו. כל endpoint ב-V11 מחזיר `ResponseCode` יחד עם מחרוזת `Description`.
- `DocumentTypeToCreate` הוא enum מסוג מחרוזת (`"TaxInvoiceAndReceipt"`, `"TaxInvoice"`, `"Receipt"`, ...), לא קוד מספרי. קודי מסמך מספריים כמו `101` או `400` שייכים לממשקי `.aspx` ישנים, לא ל-V11.
- ה-`TerminalNumber` חייב להישלח כמספר שלם, לא כמחרוזת. סוכנים נוטים לעטוף אותו במירכאות.
- `ApiPassword` נדרשת ל-`RefundByTransactionId` ול-`CreateDocument`, אבל לא נשלחת בחיוב רגיל של `LowProfile/Create` או `Transaction`.
- שימו לב לאיות האמיתי של השדות ב-V11: `Languge` (חסרה ה-`a` השנייה) בתוך אובייקט `Document`, `ISOCoinID` / `ISOCoinId`, `IsSendByEmail` (לא `SendByEmail`), `TaxId` (לא `VAT_Number`).
- שיעור המעמ הנוכחי בישראל הוא 18% (מינואר 2025; ההצעה התקציבית של ינואר 2026 להעלות ל-19% נדחתה). קארדקום מחשבת מעמ בצד השרת, אז סכומי המסמך מטופלים לפי דגל `IsVatFree`.
- **היקף PCI**: Low Profile מארח שומר אתכם ב-SAQ-A. שרת-לשרת `Transaction` עם `CardNumber`/`CVV2` גולמיים נופל ל-SAQ-D. PCI DSS v4.0 הפך לחובה במרץ 2025, אז עדיף להישאר עם Low Profile או טוקנים אלא אם יש סיבה אמיתית לגעת בנתוני כרטיס גולמיים.
- **לוח הסליקה הכספית** נקבע ברמת המסוף, לא בכל בקשה. סליקה שבועית מפקידה ביום רביעי שאחרי העסקה. סליקה חודשית מפקידה ב-6 לחודש שאחרי. אל תנסו להגדיר את זה דרך ה-API.
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
