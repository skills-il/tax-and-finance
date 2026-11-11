# שער תשלומים Grow (משולם)

## סקירה

חברת Grow (לשעבר משולם) היא שער תשלומים ישראלי לכרטיסי אשראי, Bit, Apple Pay, Google Pay, העברה בנקאית ועוד. ה-"Light API" שלה מכסה דפי תשלום, טוקניזציה, חיובים חוזרים, דרישות תשלום, חשבוניות ו-webhooks.

המדריך מנחה אינטגרציה עם ה-Light API לכל מחזור חיי התשלום: קבלת תשלומים, שמירת טוקנים וחיובם, דרישות תשלום, זיכויים והתראות שרת.

**תיעוד רשמי:** `https://developers.grow.business/`

**תמיכה:** הכתובת `support@grow.business` היא זו שהתיעוד של Grow עצמו נותן לבקשת מעבר לייצור. (גרסאות קודמות של הסקיל ציינו `apisupport@grow.business`; הכתובת הזו לא מופיעה בשום מקום בתיעוד המפורסם של Grow.)

## הוראות

### שלב 1: הבנת אימות Grow

| פרט גישה | תפקיד | הערות |
|------------|---------|-------|
| `userId` | מזהה את העסק | ייחודי לכל חשבון עסקי |
| `pageCode` | מזהה דף תשלום או אמצעי תשלום | קודי דף שונים לאשראי, Bit, הוראת קבע וכו' |
| `apiKey` | מזהה פלטפורמה שסולקת עבור כמה עסקים | רק בהגדרת פלטפורמה או אינטגרטור. עסק ישיר שולח `userId` + `pageCode` |

**לכל סביבה מזהים משלה.** לסביבת הבדיקות ולסביבת הייצור יש `pageCode`, `userId` ו-`apiKey` (אם רלוונטי) נפרדים.

**סביבות (Light API):**

| סביבה | כתובת בסיס |
|-------------|----------|
| בדיקות (Sandbox) | `https://sandbox.meshulam.co.il/api/light/server/1.0/` |
| ייצור | `https://secure.meshulam.co.il/api/light/server/1.0` |

ניהול דרישות תשלום הוא היוצא מן הכלל ונמצא על שרת נפרד, ראו שלב 8.

**קריטי: צד שרת בלבד.** כל קריאות ה-API חייבות לצאת מהשרת שלכם.

**קריטי: קידוד טופס, לא JSON.** גוף הבקשה הוא `multipart/form-data` (בבדיקה נמצא שגם `application/x-www-form-urlencoded` מפוענח), ולא JSON. גוף JSON לא מפוענח בכלל, ולכן מתקבלת שגיאת אימות מטעה על שדה חסר או לא תקין במקום שגיאת content-type.

**קריטי: כל תגובה היא HTTP 200.** ה-Light API מסמן כישלון בגוף התגובה. הצלחה מחזירה `status: 1`; כישלון מחזיר `status: 0` עם אובייקט `err`. הסתעפו לפי `status` ו-`err`, לעולם לא לפי קוד ה-HTTP.

**המבנה של `err` משתנה, בשלוש דרכים.** בכישלון אימות `err` הוא אובייקט `{"id": 707, "message": "..."}`. בשם endpoint לא מוכר `err` הוא המחרוזת `"unknown method"`. ולפעמים `err.id` עצמו הוא אובייקט: `getTokenTransactionsByExternalIdentifiers` מחזיר `err.id = {"id": 1012, "content": "..."}` והטקסט השימושי ב-`err.id.content`. נרמלו לפני השוואה.

**השדה `status` מגיע לפעמים כמחרוזת ולפעמים כמספר.** השוו באופן רופף (המרה למחרוזת) ולא עם `=== 1` קשיח.

### שלב 2: בחירת דפוס אינטגרציה

| דפוס | איך זה עובד | מתאים ל- |
|---------|-------------|----------|
| **דף תשלום (iframe/הפניה)** | Grow מארחת את טופס התשלום; אתם מטמיעים ב-iframe או מפנים | צ'קאאוט במסחר מקוון, תשלום חד-פעמי |
| **ארנק SDK** | SDK מודולרי ב-JS בתוך הדף שלכם | חוויה מותאמת בלי iframe או הפניה |
| **דרישת תשלום** | יצירת קישור שנשלח ללקוח | חשבוניות, תשלום מרחוק |
| **חיוב טוקן (שרת-לשרת)** | חיוב ישיר של טוקן כרטיס שמור | לוגיקת מנויים משלכם, לקוחות חוזרים |

התיעוד של Grow מציג את הבחירה כ-**Billing מול Tokens**: ב-Billing חברת Grow מנהלת את לוח החיובים (סכום, יום חיוב, מספר חיובים, פעם בחודש) ואתם עורכים או מבטלים דרך Update Direct Debit; ב-Tokens המערכת שלכם מחליטה מתי וכמה לחייב.

### שלב 3: מימוש דף תשלום

**נקודת קצה:** `POST /api/light/server/1.0/createPaymentProcess`

**פרמטרים חובה** (כולם מסומנים "Required field" בסכמה הרשמית):

| פרמטר | סוג | תיאור |
|-----------|------|-------------|
| `pageCode` | string | מזהה דף התשלום |
| `userId` | string | מזהה העסק |
| `sum` | number | סכום התשלום (למשל `10.99`) |
| `successUrl` | string | הפניה אחרי הצלחה. HTTPS, כתובת חיצונית, לא localhost |
| `cancelUrl` | string | הפניה אם התשלום בוטל |
| `description` | string | תיאור המוצר או השירות |
| `pageField[fullName]` | string | שם הלקוח, לפחות שני שמות |
| `pageField[phone]` | string | מספר נייד ישראלי תקין |

אמתו שם וטלפון בעצמכם לפני הקריאה: בדיקת המעבר לייצור של Grow בודקת שהאינטגרציה לא יוצרת שגיאות שאפשר היה למנוע בגלל שדות לקוח חסרים או שגויים (`err.id` 717 הוא "לא נשלח שם וטלפון או שאינו תקין").

**פרמטרים אופציונליים:**

| פרמטר | סוג | תיאור |
|-----------|------|-------------|
| `pageField[email]` | string | אימייל הלקוח |
| `pageField[invoiceName]` / `pageField[invoiceLicenseNumber]` | string | שם ומספר עוסק לחשבונית |
| `paymentNum` | integer | מספר תשלומים קבוע (1-12) |
| `maxPaymentNum` | integer | מקסימום תשלומים שהלקוח יכול לבחור (לפחות 2) |
| `chargeType` | integer | `1` = חיוב רגיל, `3` = יצירת טוקן בלבד (ראו שלב 9) |
| `saveCardToken` | integer | `1` = שמירת הכרטיס גם כטוקן (ראו שלב 9) |
| `notifyUrl` | string | כתובת callback שרת-לשרת |
| `invoiceNotifyUrl` | string | כתובת webhook לחשבונית |
| `cField1` - `cField9` | string | שדות מותאמים שחוזרים אליכם |
| `transactionTypes[]` | integer array | הגבלת אמצעי תשלום, בדפי ארנק SDK בלבד, ראו למטה |

**אמצעי תשלום (transactionTypes), בדפי ארנק SDK בלבד.** האינדקס במערך בוחר את המשבצת והערך הוא קוד אמצעי תשלום מספרי: `[0]`=`1` אשראי, `[1]`=`6` Bit, `[2]`=`13` Apple Pay, `[3]`=`14` Google Pay, `[4]`=`15` העברה בנקאית, `[5]`=`5` Pay Box (טבלה ב-`references/api-endpoints.md`).

**שורות חשבונית (אופציונלי):** `productData[0][catalogNumber]`, `productData[0][quantity]`, `productData[0][price]`, `productData[0][itemDescription]`. שורות שלא מסתכמות ב-`sum` נכשלות עם `err.id` 617.

**דוגמת בקשה:**

```bash
curl -X POST https://sandbox.meshulam.co.il/api/light/server/1.0/createPaymentProcess \
  -F "pageCode=YOUR_PAGE_CODE" \
  -F "userId=YOUR_USER_ID" \
  -F "sum=149.90" \
  -F "successUrl=https://example.com/payment/success" \
  -F "cancelUrl=https://example.com/payment/cancel" \
  -F "description=Monthly subscription" \
  -F "pageField[fullName]=Israel Israeli" \
  -F "pageField[phone]=0501234567" \
  -F "notifyUrl=https://example.com/api/grow/webhook" \
  -F "cField1=order-12345"
```

התגובה כוללת `url`: הפנו את הלקוח אליו או הטמיעו אותו ב-iframe. צרו כתובת חדשה לכל סשן צ'קאאוט; קישור שפג תוקפו מחזיר `err.id` 709.

### שלב 4: טיפול בתגובת התשלום

אחרי התשלום קורים שני דברים:

1. **הפניית לקוח:** הלקוח מגיע ל-`successUrl` עם `response=success` וערכי ה-`cField` שלכם. בהפניה הזו לא נשלחים פרטי עסקה.
2. **קריאה חוזרת מהשרת (callback):** חברת Grow שולחת POST ל-`notifyUrl` שלכם עם פרטי העסקה המלאים.

**ספקו הזמנה רק לפי callback השרת**, לעולם לא לפי ההפניה, ואשרו הצלחה לפי `statusCode` (`2` = שולם; תהליך של שמירת טוקן בלבד מדווח `11`, ראו שלב 9). שמרו ברשומת ההזמנה את `processId` ו-`processToken` שהחזירה קריאת `createPaymentProcess` שלכם, והכניסו את מספר ההזמנה ל-`cField1`; הם מה שקושר callback להזמנה.

**ה-callback הוא POST של טופס, לא JSON.** לפי Grow הוא נשלח "the same way as you would send the data to the CreatePaymentProcess method and NOT as JSON". התיעוד מציג אותו כ-JSON לנוחות הקריאה, עם השדות מקוננים תחת `data` (רמה עליונה `{err, status, data}`): קראו את `data.statusCode`, `data.transactionId`, `data.transactionToken`, וכשנשמר טוקן גם את `data.cardToken`. handler שמפענח רק `application/json` יראה גוף ריק. התיעוד לא מפרט את שמות המפתחות בפועל לשדות המקוננים (שטוחים, או בסוגריים כמו `data[statusCode]` בדומה לבקשה), ולכן רשמו ללוג גוף גולמי אחד מהסימולטור שלמטה ומפו את המפתחות לפיו, במקום לנחש.

**החזירו HTTP 200 מנקודת הקצה של ה-callback.** בדיקת המעבר לייצור של Grow בודקת את זה.

**בדקו את ה-handler לפני העלייה לאוויר** עם הסימולטור של Grow: בקשת GET ל-`https://sandbox.meshulam.co.il/api/light/server/1.0/updateMyUrl/?url=<your endpoint>` שולחת callback לדוגמה לכתובת שתתנו.

### שלב 5: אישור העסקה (חובה)

אחרי ה-callback קראו ל-`approveTransaction` כדי לאשר קבלה. לפי התיעוד של Grow הקריאה לא משנה את סטטוס העסקה, וחובה לבצע אותה לכל עסקה מוצלחת. עמוד האישור אומר לשלוח "the pageCode and all data received from the server update", והסכמה של ה-endpoint מסמנת כל שדה של ה-callback כחובה, ולכן החזירו את `pageCode` ועוד כל שדה שה-callback מסר.

**נקודת קצה:** `POST /api/light/server/1.0/approveTransaction`

בפועל הנתב בודק קודם את שני המזהים: שליחת `transactionId` בלבד נכשלת עם `err.id` 54 (`חסרים נתונים:transactionToken`), וכך גם להפך. הקריאה עם שלושת השדות שלמטה היא המינימום שעובר אימות, לא החוזה המתועד.

| פרמטר | חובה | מקור |
|-----------|------|------|
| `pageCode` | כן | קוד הדף שלכם |
| `transactionId` | כן | `data.transactionId` מה-callback |
| `transactionToken` | כן | `data.transactionToken` מה-callback |

```bash
curl -X POST https://sandbox.meshulam.co.il/api/light/server/1.0/approveTransaction \
  -F "pageCode=YOUR_PAGE_CODE" \
  -F "transactionId=TRANSACTION_ID_FROM_CALLBACK" \
  -F "transactionToken=TRANSACTION_TOKEN_FROM_CALLBACK"
  # ...plus every other field from the callback (sum, asmachta, paymentDate, processId, ...)
```

**אל תקראו ל-approveTransaction עבור:** שמירת טוקן בלבד, עסקאות נדחות (J4J5), או חיובי `createTransactionWithToken`.

**מה קורה אם מדלגים (מתועד):** התשלום עובר בכל מקרה. חברת Grow כותבת שהעסקה מעובדת גם אם approveTransaction לא בוצע או נכשל. מה שמשתנה הוא ההתראה: כש-Grow לא מקבלת אישורים היא שולחת שוב את עדכון השרת עד 5 פעמים נוספות ועשויה לפנות לעסק, ובדיקת המעבר לייצור בודקת שהאישורים נשלחים. לכן אישור חסר לא משאיר תשלום "תלוי" או לא נגבה, ושחזור אישורים אחרי תקלה לא "מציל" חיוב. צפו לשליחות החוזרות, ולכן הדה-דופליקציה בשלב 5.5 היא חובה.

### שלב 5.5: אל תסמכו על גוף ה-callback לבדו

ה-callback הוא POST ציבורי. עמודי ה-callback וה-webhook של Grow לא מתארים כותרת חתימה או סוד משותף, ו-`webhookKey` מזהה webhook ולא מאמת אותו. מי שמגלה את ה-`notifyUrl` שלכם יכול לזייף `statusCode: 2`.

לפני אספקה של כל הזמנה:

1. בצעו שאילתה חוזרת שרת-לשרת עם `getTransactionInfo` (`transactionId` + `transactionToken`) או `getPaymentProcessInfo` (`processId` + `processToken`). התשובה של ה-API היא האמת.
2. ודאו שהסכום שחזר זהה לסכום ברשומת ההזמנה שלכם, ושה-`processId` שחזר (או `cField1`) הוא זה ששמרתם להזמנה הזו. בדיקת סכום בלבד מאפשרת לשחזר תשלום אמיתי מול הזמנה שנייה באותו מחיר.
3. השתמשו בנתיב `notifyUrl` שלא ניתן לניחוש. חברת Grow גם מפרסמת כתובות IP שיש לאפשר בחומת האש שלכם (עמוד IP Addresses); הגבלת הנתיב אליהן היא שכבה נוספת, אבל העמוד לא מגדיר אותן כמקור הבלעדי של ה-callback, ולכן אל תסתמכו עליה במקום הבדיקה הראשונה.
4. בצעו דה-דופליקציה לפי `transactionId` עם אילוץ ייחודיות על כל ההזמנות, ובצעו את הבדיקה והסימון בטרנזקציית מסד נתונים אחת: חברת Grow שולחת שוב עדכונים שלדעתה לא אושרו, והשליחות החוזרות יכולות להגיע במקביל.
5. השלימו callbacks שהוחמצו. אם נקודת הקצה הייתה למטה אחרי כל השליחות החוזרות, הזמנות נשארות ממתינות לנצח; משימה תקופתית צריכה לקרוא ל-`getPaymentProcessInfo` עם ה-`processId`/`processToken` השמורים להזמנות שממתינות זמן רב, ולסגור אותן לפי התשובה.

### שלב 5.6: אידמפוטנטיות וניסיונות חוזרים בחיובי טוקן

ל-`createTransactionWithToken` יש שני שדות מניעת כפילות עם כללים שונים, לפי הסכמה הרשמית:

| שדה | כלל |
|-------|------|
| `transactionUniqueIdentifier` (חובה, מספר שלם) | אם Grow כבר ראתה את הערך עבור העסק, הבקשה נדחית מיד, **בלי קשר לסטטוס של הבקשה הראשונה** |
| `transactionGroupIdentifier` (אופציונלי, מספר שלם) | נדחה רק אם כבר קיים תשלום מוצלח עם הערך הזה |

שניהם חייבים להיות מספר שלם חיובי בלי אפסים מובילים, קטן מ-4,294,967,295 (ערך של 32 ביט); כל דבר אחר, כולל מילישניות epoch או מחרוזת, נכשל עם `err.id` 1013.

ההשלכות:

- דחייה על `transactionUniqueIdentifier` שחזר על עצמו לא אומרת דבר על השאלה אם הניסיון הראשון חויב. לעולם אל תפרשו אותה כ"כבר שולם".
- כדי להבטיח לכל היותר חיוב מוצלח אחד לכל חיוב לוגי, שלחו `transactionGroupIdentifier` יציב לחיוב הלוגי ו-`transactionUniqueIdentifier` חדש לכל ניסיון.
- חברת Grow לא אומרת אם בדיקת הקבוצה מוגבלת לטוקן הכרטיס או לכל העסק. הניחו שלכל העסק: קבעו ערך קבוצה ייחודי לכל (לקוח, תקופת חיוב), למשל המפתח הראשי המספרי של שורת "חיוב" שאתם מכניסים לפני הקריאה, ולעולם אל תגזרו אותו מתאריך בלבד, אחרת הלקוח הראשון שחויב בתקופה חוסם את החיוב של כל השאר באותה תקופה.
- אחרי timeout, בצעו קודם התאמה עם `getTokenTransactionsByExternalIdentifiers` (`userId`, `cardToken`, ואחד משני המזהים בכל קריאה; שליחת שניהם מחזירה 1012), ונסו שוב רק אם אין חיוב מוצלח.
- שמרו את שני הערכים לפני הקריאה, כדי שמפתח החיפוש יהיה קיים גם אם התשובה לא הגיעה.

### שלב 6: שליפת פרטי עסקה

הקריאה `POST /api/light/server/1.0/getTransactionInfo` מקבלת `pageCode`, `transactionId`, `transactionToken` (כולם חובה; בלי הטוקן מתקבל `err.id` 54).

הקריאה `POST /api/light/server/1.0/getPaymentProcessInfo` מקבלת `pageCode`, `processId`, `processToken` (כולם חובה; בלי `processToken` מתקבל `err.id` 54).

### שלב 7: עיבוד החזרים

**זיכוי עסקת אשראי:** `POST /api/light/server/1.0/refundTransaction`

| פרמטר | חובה | תיאור |
|-----------|----------|-------------|
| `userId` או `pageCode` | אחד מהם | הסכמה מסמנת `userId` כחובה ו-`pageCode` כאופציונלי; בפועל הקריאה מקבלת כל אחד מהם ומחזירה `err.id` 724 ("נדרש שדה userId או pageCode") כששניהם חסרים. בחיובי טוקן, שאין להם קוד דף, השתמשו ב-`userId` |
| `transactionId` | כן | העסקה לזיכוי |
| `transactionToken` | כן | טוקן העסקה |
| `refundSum` | כן | סכום הזיכוי (חלקי או מלא). שם הפרמטר הוא `refundSum`; `sum` לא מתקבל |
| `stopDirectDebit` | לא | הערך `1` בעסקת הוראת קבע עוצר את החיובים הבאים בסדרה |

כישלונות זיכוי שכדאי לטפל בהם: 105 / 190 / 218 (זיכוי גדול מהמקור), 130 ו-207 (זיכוי חלקי על עסקה שבוצעה היום או שעדיין לא שודרה), 210 (כבר זוכתה), 110 (הכסף כבר בחשבון הבנק; הבקשה עוברת לאישור ידני).

**ביטול עסקת Bit:** הקריאה `cancelBitTransaction` ממופתחת לפי התהליך (`pageCode`, `processId`, `processToken`), לא לפי העסקה. התיעוד מציין את הנתיב `/api/light/andriod/1.0/cancelBitTransaction/` (בכתיב של Grow); גם `/api/light/server/1.0/cancelBitTransaction` עונה עם אותו אימות.

### שלב 8: יצירת דרישות תשלום

דרישות תשלום הן קישורי תשלום לשיתוף. חברת Grow יכולה לשלוח אותם בעצמה ב-SMS או באימייל (`sendingMode` 1 / 2), או שאתם משתפים את הכתובת בדרך שלכם.

**ה-API המתועד נמצא על שרת וגרסה שונים משאר ה-Light API:**

| פעולה | Endpoint מתועד (sandbox) | הערות |
|-----------|-------------------------------|-------|
| יצירה | `POST https://sandboxapi.grow.link/api/light/server/1.1/CreatePaymentLink` | רגיש לאותיות: `createPaymentLink` באות קטנה לא מנותב בשרת הזה |
| עדכון או השבתה | `POST https://sandboxapi.grow.link/api/light/server/1.0/UpdatePaymentLink` | דורש `pageCode`, `isActive` (1/0), `paymentLinkProcessId`, `paymentLinkProcessToken` |

שתי הקריאות נושאות כותרת `X-API-KEY`. חברת Grow מפרסמת את ערך הייצור של CreatePaymentLink בעמוד Transition to Production; קחו אותו משם ולא מקטע קוד של צד שלישי. העמודים של Grow נותנים רק את שרת ה-sandbox לשתי הקריאות האלה, ולכן אמתו את שרת הייצור מול Grow כשהיא מנפיקה מזהי ייצור, ואל תנחשו.

החוזה של CreatePaymentLink שונה מ-`createPaymentProcess`: אין `sum`; הסכום נלקח מ-`products[data][N][price]`. השדות החובה כוללים `userId`, `pageCode`, `paymentLinkType`, `isActive`, `title`, `paymentTypes[0][type]` עם `paymentTypes[0][payments][paymentsPaymentNum]` או `...[paymentsMaxPaymentNum]`, `pageFieldSettings[fullName][value]`, `pageFieldSettings[phone][value]`, ולכל מוצר `name`, `price` ו-`vatType`. העתיקו את רשימת הפרמטרים המלאה מעמוד התיעוד.

**אל תערבבו חוזים.** גם שרתי `meshulam.co.il` עונים למתודה `createPaymentLink`, אבל עם חוזה אחר ולא מתועד (היא מבקשת קודם `sum`). בנו על החוזה המתועד.

שליפת קישור קיים נעשית עם `getPaymentLinkInfo`, שהסכמה מתעדת עבורה את `pageCode`, `paymentLinkProcessId` ו-`paymentLinkProcessToken` כשדות חובה.

### שלב 9: טוקניזציה וחיובים חוזרים

**דרישות מוקדמות (עמוד Token):** עבודה עם טוקנים דורשת הרשאה מ-Grow; שמירת טוקן אינה רלוונטית ל-Bit, Apple Pay או Google Pay, ולכן צ'קאאוט של מנוי חייב להשתמש בדף אשראי; טוקן נשמר לעד 180 תשלומים, ולכן תכננו טוקניזציה מחדש למנויים ארוכים.

**שמירת טוקן.** שני תהליכים מתועדים, שניהם דרך `createPaymentProcess`:

| תהליך | פרמטרים |
|------|-----------|
| שמירת טוקן בלבד | `chargeType=3`, `sum=1` (הסכמה קובעת שהסכום חייב להיות 1), `saveCardToken=1` |
| תשלום רגיל שגם שומר טוקן | הפרמטרים הרגילים ועוד `saveCardToken=1` |

אין endpoint נפרד בשם `getTokenOnly`: הקריאה `POST /api/light/server/1.0/getTokenOnly` מחזירה `{"err":"unknown method"}` בשני השרתים. עמוד "Get Token Only" בתיעוד של Grow מתאר את תהליך `chargeType=3` שלמעלה.

**מאיפה מגיע הטוקן:** מהשדה `data.cardToken` ב-callback. אל תשתמשו ב-`transactionToken` כטוקן הכרטיס: `transactionToken` מזהה עסקה אחת (זה מה ש-`approveTransaction`, `getTransactionInfo` ו-`refundTransaction` צריכים), ואילו `cardToken` הוא אמצעי הגישה החוזר לכרטיס. דוגמת ה-callback של שמירת טוקן בלבד מגיעה עם `statusCode` `11` (עסקה מושהית), לא `2`.

**נדרשת הסכמת לקוח.** רשימת הבדיקה של Grow למעבר לייצור דורשת בדף התשלום תיבת סימון שבה הלקוח מאשר באופן פעיל את שמירת טוקן הכרטיס לפני שהוא נשמר.

#### אפשרות א: מנוהל על ידי Grow דרך Page Code

1. צרו את התשלום עם `createPaymentProcess` וקוד דף להוראת קבע שהוגדר בדשבורד של Grow
2. קבעו את `sum` לסכום כל חיוב ואת `paymentNum` למספר החיובים
3. חברת Grow מריצה את החיובים הבאים

#### אפשרות ב: חיוב טוקן שמור (שרת-לשרת)

הקריאה היא `POST /api/light/server/1.0/createTransactionWithToken`. היא ממופתחת לפי `userId`, לא `pageCode`. פרמטר הטוקן הוא `cardToken` (ולא `token`).

| פרמטר | חובה | הערות |
|-----------|----------|-------|
| `userId`, `cardToken`, `sum`, `description` | כן | בפועל, קריאה עם `sum` בלבד מדווחת על `userId` חסר ואחר כך על `cardToken` |
| `paymentType` | כן | `1` הוראת קבע בניהול Grow, `2` רגיל, `4` תשלומים. עבור `1` העמודים של Grow סותרים זה את זה לגבי טווח `paymentNum` (Work with Token: 1-48; הסכמה של פרימיום דרך טוקן: 2-12); אמתו מול Grow |
| `paymentNum` | כן | בפועל, השמטה מחזירה `err.id` 54. `1` לחיוב יחיד בלי תשלומים |
| `pageField[fullName]`, `pageField[phone]` | כן | אותו אימות כמו בדף התשלום |
| `transactionUniqueIdentifier` | כן | מספר שלם של 32 ביט, חדש לכל ניסיון, ראו שלב 5.6 |
| `transactionGroupIdentifier` | לא | מספר שלם, יציב לכל חיוב לוגי, ראו שלב 5.6 |

```bash
curl -X POST https://sandbox.meshulam.co.il/api/light/server/1.0/createTransactionWithToken \
  -F "userId=YOUR_USER_ID" \
  -F "cardToken=CARD_TOKEN_FROM_CALLBACK" \
  -F "sum=99.00" \
  -F "description=Monthly subscription" \
  -F "paymentType=2" \
  -F "paymentNum=1" \
  -F "pageField[fullName]=Israel Israeli" \
  -F "pageField[phone]=0501234567" \
  -F "transactionGroupIdentifier=48213" \
  -F "transactionUniqueIdentifier=100001"
```

בדקו את `statusCode` בתגובה (`2` = שולם) ושמרו את `transactionId`, `transactionToken` ו-`asmachta` שבה: זיכויים ו-`updateDirectDebit` יצטרכו אותם בהמשך. אל תקראו ל-`approveTransaction` אחר כך.

**חיובי טוקן שנדחו.** עמוד ה-Token של Grow קובע ששגיאה סופית (כרטיס פג תוקף, גנוב או חסום) פירושה להפסיק לחייב את הטוקן, למחוק אותו ולקבל מהלקוח כרטיס חדש. הטבלה שלו משתמשת ב-`err.id` 103 לשני הסוגים, ולכן סווגו לפי `err.id` וגם לפי `err.message`:

| `err.id` | הודעה (כפי שחוזרת) | סופי? |
|---------|------------------------------|--------|
| 103 | כרטיס פג תוקף / כרטיס גנוב / כרטיס חסום | סופי |
| 103 | חברת האשראי לא אשרה את העסקה | לא סופי |
| 451 / 452 / 453 | כרטיס לא פעיל או פג תוקף / חברת האשראי חסמה את הכרטיס / חסימת מערכת | סופי |

בשגיאה סופית, עצרו את לוח החיובים ושלחו ללקוח דף תשלום חדש עם `saveCardToken=1`. בשגיאה לא סופית, נסו שוב מספר מוגבל של פעמים עם `transactionUniqueIdentifier` חדש ואותו `transactionGroupIdentifier`.

#### אפשרות ג: הוראת קבע פרימיום דרך טוקן

הוראת קבע פרימיום דורשת הרשאה מ-Grow. היא שומרת את הטוקן בתוקף כשהכרטיס פג, יכולה להעביר את הסדרה לכרטיס חדש באישור הלקוח, ומציגה את החיובים כהוראת קבע בפירוט חברת האשראי. עם טוקן שמור:

1. **תשלום ראשון:** קריאה ל-`createTransactionWithToken` עם שדות אפשרות ב ועוד `isRecurringDebitPayment=1` (השם בסכמת ה-endpoint; עמוד סקירה אחד כותב `isRecurringDebitId=1` ואומר שהמזהה מגיע בעדכון השרת ולא בתגובה, אז בדקו את שניהם). שמרו את `recurringDebitId`.
2. **כל תשלום הבא:** קריאה ל-`createTransactionWithToken` עם שדות אפשרות ב ועוד `recurringDebitId`.
3. בחיובי טוקן רגילים, שאינם הוראת קבע, אל תשלחו אף אחד מהשניים.

**עדכון או ביטול סדרה בניהול Grow:** הקריאה `POST /api/light/server/1.0/updateDirectDebit` (המתודה `updateRecurringPayment` לא קיימת ומחזירה `unknown method`).

| פרמטר | חובה | הערות |
|-----------|----------|-------|
| `userId`, `transactionId`, `transactionToken`, `asmachta` | כן | בפועל הקריאה מציינת כחסרים את `userId`, אחר כך `transactionId`, אחר כך `asmachta` |
| `changeStatus` | לא | `1` פעיל, `2` מבוטל |
| `sum`, `paymentNum` (1-48), `chargeDay` (1-31) | לא | סכום חדש, מספר חיובים, יום בחודש |
| `fullName`, `phone`, `email` | לא | עדכון פרטי המשלם |
| `updateCard` | לא | `0` בלי עדכון, `1` עדכון |

השגיאה `err.id` 180 (`פעולת עידכון לא בוצעה, רשומה לא נמצאה`) פירושה שהרשומה לא נמצאה.

### שלב 10: תשלומים נדחים (J4J5)

צרו את התשלום הנדחה עם `createPaymentProcess` וקוד דף של J4J5, ואז שחררו אותו:

הקריאה `POST /api/light/server/1.0/settleSuspendedTransaction` ממופתחת לפי `userId` (לא `pageCode`; שליחת `pageCode` מחזירה `err.id` 54 על `userId`), ועוד `transactionId`, `transactionToken` ו-`sum`.

השחרור מוגבל: `err.id` 814 פירושו שהחיוב חרג מתפיסת המסגרת ביותר מ-30 אחוז, 804 שחרג מתפיסת המסגרת, 803 שתוקף J5 פג, 808 שהעסקה כבר שוחררה. אל תשלחו `approveTransaction` בתהליכי J4/J5.

גם `createFarPaymentRequest` קיימת בשני השרתים; היא לא מכוסה כאן, קראו את עמוד התיעוד שלה לפני שימוש.

### שלב 11: הגדרת Webhooks

ה-Webhooks נפרדים מה-callback של `notifyUrl` ומופעלים לכל חשבון על ידי התמיכה של Grow, לפי טריגר (עסקאות חד-פעמיות, דרישות תשלום, הוראות קבע מהחיוב השני, הוראות קבע שנכשלו, POS, חשבוניות ועוד; רשימה מלאה ב-`references/webhook-payloads.md`).

**שתי משפחות payload, וקוראים אותן אחרת:**

| משפחה | מבנה | שדות מרכזיים |
|--------|-------|-----------|
| דפים ישנים, הוראות קבע, חד-פעמי דרך API | אובייקט שטוח עם `webhookKey` | `transactionCode`, `paymentSum`, `paymentsNum`, `allPaymentNum`, `paymentType`, `asmachta`, `paymentSource`, `directDebitId` (הוראת קבע). בלי `statusCode`, `transactionId` או `transactionToken` |
| דרישות תשלום (מערכת חדשה) | `{err, status, data}` כמו ה-callback | `data.statusCode`, `data.transactionId`, `data.transactionToken`, `data.paymentLinkProcessId`, `data.paymentLinkProcessToken`, `productData`, `shipping` |

ה-payload של הוראת קבע שנכשלה כתוב ב-snake_case (`regular_payment_id`, `error_message`, `charges_attempts`, `webhook_key`). ה-webhook של חשבונית נושא `transactionCode`, `invoiceNumber` ו-`invoiceUrl`. דוגמאות מלאות: `references/webhook-payloads.md`.

בסדרות הוראת קבע בניהול Grow, החיובים מהשני והלאה מדווחים רק דרך ה-webhooks האלה, והמשפחה השטוחה לא נושאת `transactionId`/`transactionToken`, ולכן השאילתה החוזרת של שלב 5.5 לא יכולה לאמת אותם. התייחסו אליהם כהתראות: התאימו מול הדוחות של Grow או ממשק הסוחר לפני שאתם מאריכים גישה בתשלום על סמך אותם.

**הגדרת webhooks ב-sandbox לא מועתקת לייצור;** צריך להגדיר אותם שוב.

### שלב 12: 3D Secure

לפי עמוד ה-3DS של Grow, זה שירות שהעסק רוכש. אחרי הרכישה הוא פעיל כברירת מחדל בכל עסקה, והוא שולח קוד לטלפון הנייד של בעל הכרטיס כפי שרשום בחברת האשראי. כדי לדלג עליו בעסקה מסוימת, שלחו `cancel3DS=True` בקריאת ה-API.

העמוד לא מסביר איך חל העברת האחריות (liability shift), וגם לא אם חיוב שרת-לשרת דרך `createTransactionWithToken` עובר 3DS. אל תניחו שחיוב טוקן יורש את סטטוס ה-3DS של התשלום המקורי; בררו מול Grow.

### שלב 13: סוגי דפי תשלום

לכל סוג דף יש `pageCode` משלו: ארנק SDK (ווידג'ט JS), גנרי (אשראי + Bit), כרטיס אשראי, Google Pay (דורש `allow="payment"` ב-iframe), Apple Pay (דורש אימות דומיין, שוב גם לדומיין הייצור), Bit (עדיף במסך מלא בנייד), Bit QR (מחשב או חנות).

```html
<iframe src="PAYMENT_URL_FROM_API" width="100%" height="600"
        allow="payment" style="border: none;"></iframe>
```

חיבור HTTPS הוא חובה באינטגרציית iframe. בתוך iframe, ממשק ה-PostMessage של Grow מדווח על אירועים בצד הדפדפן (הצלחת אשראי `payment`, הצלחת Bit `bit_payment`); התייחסו אליהם כאותות חוויית משתמש בלבד, והמשיכו לספק לפי callback השרת.

הימנעו מתווים מיוחדים בפרמטרים.

### שלב 14: בדיקות ב-Sandbox ומעבר לייצור

**כרטיסי בדיקה ב-sandbox** (עמוד Testing Environment): `4580458045804580` (רק תשלום יחיד רגיל; מתאים לבדיקת כישלון בעסקת תשלומים), `4580000000000000`, `4580111111111121`. פרטי העברה בנקאית לבדיקה: בנק `41`, סניף `410`, חשבון `411111111`.

**ל-Bit, Google Pay ו-Apple Pay אין סביבת בדיקות.** עסקאות בהם מעובדות בסביבה החיה ומחויבות כעסקאות אמיתיות, גם בזמן פיתוח. אי אפשר להשלים תשלום PayBox ב-sandbox.

**ארנק Growin SDK:** בעלייה לאוויר שנו את `environment` ב-`configureGrowSdk` מ-`"DEV"` ל-`"PRODUCTION"`.

**המעבר לייצור מותנה.** חברת Grow מנפיקה מזהי ייצור רק אחרי בדיקת הלוגים של האינטגרציה: בקשות שנשלחו נכון, callbacks שנענו ב-HTTP 200, approveTransaction שנשלח במקומות הנדרשים, שדות לקוח שאומתו. פלטפורמות צריכות גם הסכם מסחרי חתום. אתרי מסחר מקוון חייבים להציג טלפון ליצירת קשר, כתובת העסק, תיבת סימון לתקנון עם קישור, ותקנון שמכסה משלוח, אחריות, הגבלת גיל, ביטול ופרטיות. בקשו את הבדיקה ב-`support@grow.business`.

**חשבוניות.** חברת Grow יכולה להפיק חשבוניות (`invoiceNotifyUrl`, `productData`). התיעוד למפתחים לא חושף שדה או התנהגות של מספר הקצאה. אם Grow מפיקה את חשבוניות המס שלכם לעסקים, שאלו את Grow איך היא משיגה מספרי הקצאה; הספים מכוסים בסקיל `il-invoice-organizer`.

## קודי שגיאה

חברת Grow מחזירה שגיאות בגוף התגובה עם `status: 0` ואובייקט `err`. הקודים הנפוצים בטבלה; הרשימה המלאה, כולל קודים שנצפו בפועל ואינם בטבלה של Grow, נמצאת ב-`references/error-codes.md`.

| קוד | משמעות |
|------|---------|
| 54 | שדה חובה חסר; ההודעה מציינת את השדה |
| 707 | סכום לא תקין (גם מה שגוף JSON מייצר) |
| 717 | לא נשלח שם וטלפון או שאינו תקין |
| 722 | לא ניתן לאשר עסקה שלא בוצעה או בוטלה |
| 724 | נדרש `userId` או `pageCode` |
| 1013 | המזהה אינו מספר שלם חיובי של 32 ביט |
| 103 / 451 / 452 / 453 | דחיות של חיוב טוקן; ראו שלב 9 לגבי סופי ולא סופי |
| 403 | אסור: לא נשלחה כותרת `X-API-KEY` |

התייחסו לכל `err.id` לא מוכר ככישלון והציגו את `err.message`.

## מלכודות נפוצות
- חברת Grow דורשת `multipart/form-data` ולא `application/json`. גוף JSON מייצר שגיאת אימות על השדה החסר הראשון (בדרך כלל `err.id` 707, סכום לא תקין), וסוכנים מחפשים אז באג בסכום.
- כל תגובה היא HTTP 200, כולל כל כישלון. הסתעפו לפי `status` ו-`err` שבגוף.
- טוקן הכרטיס הוא `data.cardToken`, לא `data.transactionToken`. חיוב `transactionToken` כטוקן כרטיס נכשל, ושמירת `cardToken` במקום שמצפה לטוקן עסקה שוברת אישור, זיכוי ושליפה.
- ערך `transactionUniqueIdentifier` שחוזר על עצמו נדחה בין אם הניסיון הראשון הצליח ובין אם לא. מי שמפרש את הדחייה כ"כבר שולם" שולח סחורה בלי תשלום; בצעו התאמה קודם.
- דילוג על `approveTransaction` לא עוצר את החיוב. הוא גורם לשליחות חוזרות של ה-callback ולכישלון בבדיקת המעבר לייצור. אל תגידו למשתמש שתשלומים שלא אושרו "תלויים".
- ל-Bit, Apple Pay ו-Google Pay אין sandbox: תשלום "בדיקה" בהם הוא חיוב אמיתי.
- גם `cardToken` וגם `transactionToken` הם אמצעי גישה. אל תרשמו אותם ללוג, אל תציגו אותם ללקוח המשלם (Grow כותבת זאת במפורש; את `asmachta` מותר להציג), והצפינו אותם במנוחה. אל תקבלו, תרשמו או תעבירו מספר כרטיס גולמי בעצמכם.
- הכלל "צד שרת בלבד" נאכף בהיעדר כותרות CORS, ולכן קריאה מהדפדפן מציגה שגיאת CORS בקונסול, לא 403.

## פתרון בעיות

| בעיה | סיבה | פתרון |
|---------|-------|---------|
| שגיאת HTTP 403 Forbidden | לא נשלחה כותרת `X-API-KEY`, זו הסיבה שטבלת השגיאות של Grow נותנת. הכותרת מתועדת לקריאות של דרישות תשלום | שלחו את כותרת `X-API-KEY` בקריאות שדורשות אותה |
| בקשה מהדפדפן נכשלת בלי 403 | ה-API לא שולח כותרות CORS. נבדק: בקשה עם `Origin` ו-`Referer` של דפדפן נענית כרגיל | העבירו את הקריאה לצד השרת |
| שגיאה `err.id` 707 על בקשה שהסכום בה תקין | הסיבה הסבירה היא גוף JSON: השדות לא מפוענחים, ולכן האימות נכשל קודם על הסכום. לא אומת שזה הטריגר היחיד | עברו ל-`multipart/form-data` ושלחו שוב |
| שגיאה `err.id` 54 ב-`approveTransaction` | נשלח רק אחד משני המזהים | שלחו גם `transactionId` וגם `transactionToken` |
| חיוב טוקן נכשל אחרי תשלום ראשון מוצלח | נשמר `transactionToken` כטוקן הכרטיס, או שהתשלום הראשון לא כלל `saveCardToken=1` | שמרו את `data.cardToken` מתשלום שנוצר עם `saveCardToken=1` |
| ה-handler של ה-callback מקבל גוף ריק | הוא מפענח רק JSON; Grow שולחת נתוני טופס | פענחו גוף טופס או multipart בנתיב הזה |
| אותו callback מגיע כמה פעמים | חברת Grow שולחת שוב עדכונים שלדעתה לא אושרו | קראו ל-`approveTransaction` ובצעו דה-דופליקציה לפי `transactionId` |
| תשובה `{"err":"unknown method"}` | שם המתודה לא קיים בשרת הזה (למשל `getTokenOnly`, `updateRecurringPayment`) | השתמשו ב-endpoint הקיים שמצוין בשלב 8 או 9 |
| תשובת HTTP 403 `{"message":"Missing Authentication Token"}` מ-`sandboxapi.grow.link` | נתיב שהשרת לא מנתב, לרוב `createPaymentLink` באות קטנה | השתמשו בכתיב המתועד: `/1.1/CreatePaymentLink`, `/1.0/UpdatePaymentLink` |
| תשלום "בדיקה" ב-Bit או Apple Pay חייב כרטיס אמיתי | לאמצעים האלה אין sandbox | זכו אותו, ובדקו את האמצעים האלה רק בסכומים שאתם מתכוונים לזכות |
| הסקריפט נעצר עם "GROW_API_KEY was renamed to MESHULAM_API_KEY" | שם משתנה סביבה שהשתנה | שנו את השם (`export MESHULAM_API_KEY=...`) ובטלו את `GROW_API_KEY`; הערך עצמו לא משתנה |

## משאבים מצורפים

- הסקריפט `scripts/grow-payment-helper.sh`: כלי עזר שמתחיל ב-sandbox ל-createPaymentProcess, שליפת עסקה ותהליך, אישור, זיכוי, ביטול Bit וחיובי טוקן. הוא יוצא עם קוד שגיאה על כישלון API, שולח פרטי גישה רק לשני שרתי `meshulam.co.il` הקבועים, מרחיק טוקנים ומפתחות מרשימת התהליכים, ממסך טוקנים בפלט, ומסרב לעבוד מול ייצור בלי `GROW_ALLOW_PRODUCTION=1`.
- הקובץ `references/api-endpoints.md`: טבלת endpoints, שרתים, והמתודות שלא קיימות.
- הקובץ `references/webhook-payloads.md`: דוגמאות payload של webhooks ו-callback מהתיעוד של Grow.
- הקובץ `references/error-codes.md`: טבלת קודי השגיאה המלאה.

## קישורי עזר

| מקור | כתובת | מה לבדוק |
|--------|-----|---------------|
| תיעוד API של Grow | https://developers.grow.business/reference/introduction | נקודת כניסה ל-endpoints ולסכמות בקשה עדכניים |
| טבלת שגיאות | https://developers.grow.business/reference/errors | טבלת קודי השגיאה המלאה |
| סביבת בדיקות | https://developers.grow.business/reference/testing-environment | כתובת sandbox, כרטיסי בדיקה, אמצעים בלי sandbox |
| מעבר לייצור | https://developers.grow.business/reference/live-environment | כתובת ייצור, רשימת בדיקה, `X-API-KEY` לדרישות תשלום |
| callback שרת-לשרת | https://developers.grow.business/reference/server-to-server-callback | מבנה ה-callback, התנהגות approveTransaction, updateMyUrl |
| כתובות IP | https://developers.grow.business/reference/ip-address | כתובות לאפשר בחומת האש |
| 3DS של Grow | https://developers.grow.business/reference/3ds-1 | שירות 3DS ו-`cancel3DS` |
| Webhooks של Grow | https://developers.grow.business/docs/overview-7 | אפשרויות webhook ו-payloads |
