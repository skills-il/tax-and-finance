# שער תשלומים Grow (משולם)

## סקירה

Grow (לשעבר משולם) היא אחת מחברות הסליקה המובילות בישראל, המפעילה אלפי עסקים עם סליקת כרטיסי אשראי, תשלומי Bit, Apple Pay, Google Pay ועוד. בניגוד לשערי תשלום ישראליים אחרים, Grow מציעה API אחיד ("Light API") שמכסה דפי תשלום, טוקניזציה, חיובים חוזרים, דרישות תשלום, חשבוניות ו-webhooks באינטגרציה אחת.

מדריך זה מנחה אינטגרציה עם Light API של Grow לכל מחזור חיי התשלום: קבלת תשלומים, שמירת טוקנים לחיובים חוזרים, יצירת דרישות תשלום, עיבוד החזרים וטיפול בהתראות webhook בזמן אמת.

**תיעוד רשמי:** `https://developers.grow.business/`

**תמיכה למפתחים:** `apisupport@grow.business` (נישא ממחזור קודם; לא אומת מול התיעוד המפורסם של Grow במחזור הזה, ולכן אמתו אותו בפורטל בית העסק שלכם לפני הסתמכות).

## הוראות

### שלב 1: הבנת אימות Grow

Grow משתמשת בשלושה פרטי גישה שמסופקים בעת הצטרפות:

| פרט גישה | תפקיד | הערות |
|------------|---------|-------|
| `userId` | מזהה בית עסק | ייחודי לכל חשבון עסקי |
| `pageCode` | הגדרת דף תשלום | page codes שונים לסוגי תשלום שונים (אשראי, Bit, חיוב חוזר וכו') |
| `apiKey` | אימות API | נדרש בניהול מספר עסקים או הגדרות ספציפיות |

**סביבות:**

| סביבה | כתובת בסיס |
|-------------|----------|
| Sandbox (בדיקות) | `https://sandbox.meshulam.co.il` |
| Production | `https://secure.meshulam.co.il` |

**חשוב: צד שרת בלבד.** כל בקשות ה-API חייבות להגיע מהשרת שלכם. בקשות מצד הלקוח (דפדפן) נחסמות על ידי Grow.

**חשוב: פורמט FormData.** כל גוף הבקשות משתמש ב-`multipart/form-data`, לא JSON. אם תשלחו `application/json` ה-API לא מפענח את השדות בכלל, ולכן תקבלו שגיאת ולידציה מטעה על שדה חסר או לא תקין ולא שגיאת content-type.

**חשוב: כל תגובה היא HTTP 200.** ה-Light API מדווח על כישלון בגוף התשובה ולעולם לא בשורת הסטטוס. קריאה מוצלחת מחזירה `status: 1`, וכישלון מחזיר `status: 0` עם אובייקט `err`. תסתעפו לפי `status` ו-`err` ולעולם לא לפי קוד ה-HTTP. ראו את פרק קודי השגיאה.

**`err` משנה צורה בשלוש דרכים.** בכישלון ולידציה `err` הוא אובייקט `{"id": 707, "message": "..."}`. כששם ה-endpoint אינו מוכר `err` הוא המחרוזת `"unknown method"`. ובנוסף `err.id` עצמו הוא לפעמים אובייקט: `getTokenTransactionsByExternalIdentifiers` מחזיר `err.id = {"id": 1012, "content": "..."}` כשהטקסט המועיל נמצא ב-`err.id.content` ו-`err.message` גנרי. קוד שעושה `err.id === 54` לא יתאים שם בשקט, ורישום `err.id` ידפיס `[object Object]`. נרמלו לפני השוואה.

**`status` הוא לפעמים מחרוזת JSON ולפעמים מספר.** אותו endpoint מחזיר `"status":"0"` בקלט אחד ו-`"status":0` באחר. השוו בהמרה למחרוזת ולא ב-`=== 1` קשיח.

### שלב 2: בחירת דפוס אינטגרציה

| דפוס | איך זה עובד | מתאים ל- |
|---------|-------------|----------|
| **דף תשלום (iframe/redirect)** | Grow מארחת את טופס התשלום; הטמיעו באמצעות iframe או הפניה | צ'קאאוט באיקומרס, תשלומים חד-פעמיים |
| **SDK Wallet** | ווידג'ט JS מודולרי מוטמע בדף שלכם | חוויה מותאמת ללא iframe/redirect |
| **דרישת תשלום** | יצירת URL תשלום לשליחה ללקוחות | חשבונות, חיוב פרילנסרים, תשלומים מרחוק |
| **חיוב טוקן (שרת-לשרת)** | חיוב טוקן שמור ישירות | חיובים חוזרים, מנויים, לקוחות חוזרים |

רוב בתי העסק הישראליים משתמשים ב**דף תשלום** לתשלום הראשון (שגם שומר טוקן), ואז **חיוב טוקן** לחיובים חוזרים.

### שלב 3: מימוש דף תשלום

זו האינטגרציה הנפוצה ביותר -- יצירת דף תשלום מתארח והפניית הלקוח אליו.

**Endpoint:** `POST /api/light/server/1.0/createPaymentProcess`

**פרמטרים נדרשים:**

| פרמטר | סוג | תיאור |
|-----------|------|-------------|
| `pageCode` | string | מזהה דף תשלום (מסופק על ידי Grow) |
| `userId` | string | מזהה בית העסק |
| `sum` | number | סכום התשלום (למשל `10.99`) |
| `successUrl` | string | כתובת הפניה לאחר תשלום מוצלח (HTTPS חובה) |
| `cancelUrl` | string | כתובת הפניה אם התשלום בוטל |
| `description` | string | תיאור המוצר/שירות |
| `pageField[fullName]` | string | שם הלקוח (חייב להכיל לפחות שני שמות) |
| `pageField[phone]` | string | מספר טלפון נייד ישראלי תקין |

**פרמטרים אופציונליים:**

| פרמטר | סוג | תיאור |
|-----------|------|-------------|
| `pageField[email]` | string | אימייל הלקוח |
| `paymentNum` | integer | מספר תשלומים קבוע (1-12) |
| `maxPaymentNum` | integer | מקסימום תשלומים שהלקוח יכול לבחור (2-N) |
| `chargeType` | integer | `1` = חיוב רגיל |
| `notifyUrl` | string | כתובת callback שרת-לשרת |
| `invoiceNotifyUrl` | string | כתובת webhook לחשבונית |
| `cField1` - `cField9` | string | שדות מותאמים (מוחזרים ב-callbacks) |
| `transactionTypes[]` | array | הגבלת אמצעי התשלום שיוצגו (בדפי SDK wallet בלבד). לכל אמצעי יש אינדקס קבוע וגם ערך מספרי, ראו טבלה למטה |

**אמצעי תשלום (transactionTypes) -- בדפי SDK wallet בלבד.** שני דברים חשובים כאן, וגרסאות קודמות של הכישור טעו בשני. ה-index במערך בוחר את המשבצת, וה-value הוא קוד אמצעי תשלום מספרי. שניהם מגיעים מהסכמה של `createPaymentProcess` בדף התיעוד הרשמי:

| פרמטר | אמצעי תשלום | ערך מתועד |
|-----------|---------------|------------|
| `transactionTypes[0]` | כרטיס אשראי | `1` |
| `transactionTypes[1]` | Bit | `6` |
| `transactionTypes[2]` | Apple Pay | `13` |
| `transactionTypes[3]` | Google Pay | `14` |
| `transactionTypes[4]` | העברה בנקאית | `15` |
| `transactionTypes[5]` | Pay Box | ברירת מחדל `5` |

**פריטי חשבונית (אופציונלי):**

| פרמטר | סוג | תיאור |
|-----------|------|-------------|
| `productData[0][catalogNumber]` | integer | מספר קטלוגי |
| `productData[0][quantity]` | integer | כמות |
| `productData[0][price]` | number | מחיר |
| `productData[0][itemDescription]` | string | תיאור הפריט |

**בקשה לדוגמה:**

```bash
curl -X POST https://sandbox.meshulam.co.il/api/light/server/1.0/createPaymentProcess \
  -F "pageCode=YOUR_PAGE_CODE" \
  -F "userId=YOUR_USER_ID" \
  -F "sum=149.90" \
  -F "successUrl=https://yoursite.com/payment/success" \
  -F "cancelUrl=https://yoursite.com/payment/cancel" \
  -F "description=מנוי חודשי" \
  -F "pageField[fullName]=ישראל ישראלי" \
  -F "pageField[phone]=0501234567" \
  -F "pageField[email]=customer@example.com" \
  -F "paymentNum=1" \
  -F "notifyUrl=https://yoursite.com/api/grow/webhook" \
  -F "cField1=order-12345"
```

התגובה כוללת שדה `url` -- הפנו את הלקוח לשם או הטמיעו כ-iframe.

**חשוב:** כתובת דף התשלום תקפה ל-10 דקות. צרו כתובת חדשה לכל סשן צ'קאאוט.

### שלב 4: טיפול בתגובת התשלום

לאחר שהלקוח משלים את התשלום, קורים שני דברים:

1. **הפניית לקוח:** הלקוח מופנה ל-`successUrl` עם `response=success`
2. **callback שרת:** Grow שולחת POST ל-`notifyUrl` עם פרטי העסקה המלאים

**תמיד אמתו דרך callback השרת**, לא דרך ההפניה בצד הלקוח (שניתנת לזיוף). ב-callback, אשרו הצלחה על ידי בדיקת `statusCode` (`2` = שולם), אל תתייחסו לעצם ההגעה של ההפניה ל-`successUrl` כהוכחת תשלום.

**קינון ה-payload (חשוב):** ב-callback שרת-לשרת של `notifyUrl` השדות מקוננים תחת אובייקט `data` (הרמה העליונה היא `{err, status, data}`), ולכן קראו את `data.statusCode`, `data.transactionToken` ו-`data.transactionId` (המזהה שמעבירים ל-`approveTransaction`), ולא את הרמה העליונה. מערכת ה-webhook הנפרדת שמבוססת על webhookKey (שלב 11) מספקת payload שטוח יותר.

### שלב 5: אישור העסקה (חובה)

לאחר קבלת callback השרת, חובה לקרוא ל-`approveTransaction` כדי לאשר קבלה. זה לא משנה את התשלום -- זה סוגר את מחזור העסקה מול Grow.

**Endpoint:** `POST /api/light/server/1.0/approveTransaction`

הקריאה דורשת את **שני** המזהים מה-callback. שליחת `transactionId` בלבד נכשלת עם `err.id` 54 (`חסרים נתונים:transactionToken`), ושליחת `transactionToken` בלבד נכשלת עם 54 על `transactionId`.

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
```

**אל תקראו ל-approveTransaction עבור:** שמירת טוקן בלבד, עסקאות נדחות (J4J5), או חיובי `createTransactionWithToken`.

**מה קורה אם לא קוראים לה בכלל אינו מתועד, והכישור הזה לא מנחש.** התיעוד של Grow מסמן את השלב כחובה, ו-`err.id` 722 (`לא ניתן לבצע אישור לעסקה שלא בוצעה או בוטלה`) מראה שאישור יכול להידחות. האם הכסף נתפס בלי הקריאה, האם יש חלון תפוגה, והאם אישור מאוחר עדיין מתקבל, לא ניתן היה לקבוע בלי חשבון סוחר. אם אתם משחזרים אישורים אחרי תקלה, בררו מול Grow לפני שתבחרו בין שחזור אישורים לבין זיכוי, ואל תניחו לשום כיוון.

### שלב 5.5: אל תסמכו על גוף ה-callback לבדו

ה-callback של השרת הוא עוגן האמון לאספקה, והוא POST ציבורי בלי אימות. Grow לא שולחת כותרת חתימה; `webhookKey` מזהה את ה-webhook והוא אינו סוד משותף שאפשר לאמת מולו payload. מי שיגלה את ה-`notifyUrl` שלכם יכול לזייף `{statusCode: 2, ...}` ולקבל סחורה בחינם.

לפני אספקה של כל הזמנה:

1. בצעו שאילתה חוזרת שרת-לשרת מול Grow עם `getTransactionInfo` (`transactionId` + `transactionToken`) או `getPaymentProcessInfo` (`processId` + `processToken`). התשובה של ה-API היא האמת, לא גוף ה-callback.
2. ודאו שהסכום שחזר זהה לסכום ברשומת ההזמנה שלכם. callback מזויף או משוחזר שנוקב בסכום אחר לא יוביל לאספקה.
3. השתמשו בנתיב `notifyUrl` שלא ניתן לניחוש, ואל תרשמו אותו במקום שלקוחות רואים.
4. בצעו דה-דופליקציה לפי `transactionId`: callback שנשלח שוב יוביל לאספקה אחת, לא שתיים.

### שלב 5.6: אידמפוטנטיות וניסיונות חוזרים

`transactionUniqueIdentifier` הוא מפתח האידמפוטנטיות שלכם ב-`createTransactionWithToken`. שלחו ערך יציב לכל חיוב לוגי, ולא לכל ניסיון.

- בתקלת רשת או שגיאת 5xx שבה אינכם יודעים אם הכרטיס חויב, אל תנסו שוב עם מזהה חדש: ככה לקוח מחויב פעמיים. שלחו שוב את אותו `transactionUniqueIdentifier`, או בצעו התאמה קודם עם `getTokenTransactionsByExternalIdentifiers`.
- `err.id` 712 (`העסקה כבר בוצעה`) הוא סימן לשחזור ולא באג. התייחסו אליו כ"כבר חויב, הצלחה" ולא ככישלון שצריך לנסות שוב.

### שלב 6: שליפת פרטי עסקה

**קבלת פרטי עסקה:**

`POST /api/light/server/1.0/getTransactionInfo`

| פרמטר | סוג | תיאור |
|-----------|------|-------------|
| `pageCode` | string | מזהה דף |
| `transactionId` | string | מזהה העסקה לשליפה |
| `transactionToken` | string | טוקן העסקה. חובה: בלעדיו הקריאה מחזירה `err.id` 54 |

**קבלת פרטי תהליך תשלום:**

`POST /api/light/server/1.0/getPaymentProcessInfo`

| פרמטר | סוג | תיאור |
|-----------|------|-------------|
| `pageCode` | string | מזהה דף |
| `processId` | string | מזהה התהליך מ-createPaymentProcess |
| `processToken` | string | טוקן התהליך מ-createPaymentProcess. חובה: בלעדיו הקריאה מחזירה `err.id` 54 |

### שלב 7: עיבוד החזרים

**החזר עסקת כרטיס אשראי:**

`POST /api/light/server/1.0/refundTransaction`

| פרמטר | סוג | תיאור |
|-----------|------|-------------|
| `pageCode` | string | מזהה דף |
| `transactionId` | string | עסקה להחזר |
| `transactionToken` | string | טוקן העסקה. חובה: בלעדיו הקריאה מחזירה `err.id` 54 |
| `refundSum` | number | סכום ההחזר (חלקי או מלא). שם הפרמטר הוא `refundSum`; `sum` אינו מתקבל כאן והקריאה נשארת עם `err.id` 707 |

שגיאות החזר שכדאי לטפל בהן: 105 ו-218 (החזר גדול מהעסקה המקורית), 130 ו-207 (החזר חלקי על עסקה שסולקה או שודרה היום), 210 (כבר בוצע החזר), 110 (הכסף כבר הועבר לבנק ולכן הבקשה עוברת לאישור ידני).

**ביטול עסקת Bit:**

`POST /api/light/server/1.0/cancelBitTransaction`

הקריאה מזוהה לפי התהליך ולא לפי העסקה. שליחת `transactionId` מחזירה `err.id` 54 על `processId`.

| פרמטר | סוג | תיאור |
|-----------|------|-------------|
| `pageCode` | string | מזהה דף |
| `processId` | string | מזהה תהליך התשלום |
| `processToken` | string | טוקן תהליך התשלום |

### שלב 8: יצירת דרישות תשלום

דרישות תשלום מאפשרות לשלוח כתובת תשלום ללקוחות באימייל, SMS או WhatsApp. שימושי לחיובים ותשלומים מרחוק.

**Endpoint:** `POST /api/light/server/1.0/createPaymentLink`

| פרמטר | סוג | תיאור |
|-----------|------|-------------|
| `pageCode` | string | מזהה דף |
| `userId` | string | מזהה בית עסק |
| `sum` | number | סכום התשלום |
| `description` | string | תיאור התשלום |
| `pageField[fullName]` | string | שם הלקוח |
| `pageField[phone]` | string | טלפון הלקוח |
| `pageField[email]` | string | אימייל הלקוח |

התגובה כוללת כתובת תשלום לשיתוף. לשליפת דרישה קיימת השתמשו ב-`getPaymentLinkInfo`, שדורש `paymentLinkProcessToken` (בלעדיו מתקבל `err.id` 54 על השדה הזה).

**`updatePaymentLink` אינו קיים ב-Light API.** בבדיקה מול `sandbox.meshulam.co.il` ומול `secure.meshulam.co.il` הוא מחזיר `{"err":"unknown method"}`, בדיוק כמו שם endpoint שאינו קיים, ובשונה משגיאות ההרשאה (300, 714, 715) שמתקבלות מ-endpoint אמיתי שאין אליו הרשאה. צרו דרישת תשלום חדשה במקום.

### שלב 9: טוקניזציה וחיובים חוזרים

**מאיפה מגיע הטוקן:** טוקן הכרטיס השמור מגיע בשדה `transactionToken` של ה-webhook של התשלום אחרי התשלום הראשון. השתמשו בערך הזה כ-`cardToken` בקריאות `createTransactionWithToken` שלמטה.

**`getTokenOnly` אינו נפתר בנתיב של ה-Light API.** התפריט בתיעוד של Grow עדיין מציג פעולה בשם "Get Token Only", אבל `POST /api/light/server/1.0/getTokenOnly` מחזיר `{"err":"unknown method"}` בשני השרתים וגם בווריאציות אותיות, וזו התשובה של הראוטר לשם שאינו מוכר לו. אל תכתבו קוד מול הנתיב הזה. כדי לשמור כרטיס בלי לחייב, העבירו תשלום דרך page code שמוגדר לטוקניזציה וקחו את הטוקן מה-callback, או אמתו את הפעולה העדכנית מול התמיכה של Grow.

Grow תומכת בשלושה מודלים לחיובים חוזרים:

#### אפשרות א: מנוהל על ידי Grow דרך Page Code

השתמשו ב-page code ייעודי לחיובים חוזרים שמוגדר בלוח הבקרה של Grow:

1. צרו תשלום עם `createPaymentProcess` עם page code לחיובים חוזרים
2. הגדירו `sum` לסכום החיוב החודשי ו-`paymentNum` למספר החיובים הכולל
3. Grow מטפלת בכל החיובים הבאים אוטומטית

#### אפשרות ב: חיוב טוקן שמור (שרת-לשרת)

חייבו טוקן כרטיס שמור ישירות. שם הפרמטר לטוקן הוא `cardToken` (ולא `token`), ו-`paymentType=2` הוא חיוב רגיל:

```bash
curl -X POST https://sandbox.meshulam.co.il/api/light/server/1.0/createTransactionWithToken \
  -F "userId=YOUR_USER_ID" \
  -F "sum=99.00" \
  -F "description=Monthly subscription" \
  -F "cardToken=SAVED_CARD_TOKEN" \
  -F "paymentType=2" \
  -F "pageField[fullName]=Israel Israeli" \
  -F "pageField[phone]=0501234567" \
  -F "transactionUniqueIdentifier=UNIQUE_PER_CHARGE"
```

`cardToken` הוא טוקן הכרטיס השמור, והוא מגיע בשדה `transactionToken` של ה-webhook של התשלום. בדקו את `statusCode` בתגובה (`2` = שולם) כדי לאשר שהחיוב הצליח. נקודת קצה זו משתמשת ב-`userId` ולא ב-`pageCode`, והיא דורשת גם `paymentNum` (בלעדיו מתקבל `err.id` 54 על `paymentNum`); שלחו `paymentNum=1` לחיוב בודד ללא תשלומים.

#### אפשרות ג: סדרת חיובים חוזרים פרימיום (recurringDebitId)

לסדרת חיובים חוזרים בניהול Grow, כל חיוב נושא `recurringDebitId` שמקשר אותו לסדרה. הערך הזה מוחזר בתגובה של התשלום החוזר-פרימיום הראשון; העבירו אותו בכל קריאת `createTransactionWithToken` הבאה, לצד `cardToken`, `paymentType=2`, והשדות הנדרשים למעלה:

```bash
curl -X POST https://sandbox.meshulam.co.il/api/light/server/1.0/createTransactionWithToken \
  -F "userId=YOUR_USER_ID" \
  -F "sum=99.00" \
  -F "description=Monthly subscription" \
  -F "cardToken=SAVED_CARD_TOKEN" \
  -F "paymentType=2" \
  -F "pageField[fullName]=Israel Israeli" \
  -F "pageField[phone]=0501234567" \
  -F "recurringDebitId=RECURRING_DEBIT_ID" \
  -F "transactionUniqueIdentifier=UNIQUE_PER_CHARGE"
```

אמתו את פרמטרי האתחול המדויקים של החיוב-החוזר-פרימיום בעמוד הייחוס של `createTransactionWithToken` (ראו קישורי עזר) במקום להניח שם דגל.

**עדכון חיוב חוזר:**

`updateRecurringPayment` אינו קיים ב-Light API: בבדיקה מול שני השרתים הוא מחזיר `{"err":"unknown method"}`. ה-endpoint החי לשינוי סדרת הוראת קבע הוא `POST /api/light/server/1.0/updateDirectDebit`. אמתו את סט הפרמטרים שלו בדף התיעוד לפני חיווט, וצפו ל-`err.id` 180 (`פעולת עידכון לא בוצעה, רשומה לא נמצאה`) כשמזהה הסדרה לא תואם.

**חיפוש עסקאות טוקן:**

`POST /api/light/server/1.0/getTokenTransactionsByExternalIdentifiers` -- מציאת כל העסקאות לטוקן נתון לפי מזהים חיצוניים.

**יתרונות חיוב חוזר פרימיום:**
- עדכון כרטיס אוטומטי בתפוגה (תאריך תפוגה חדש מוחל על טוקן קיים)
- תמיכה בהעברת כרטיס כשהלקוח מחליף כרטיס
- שורת חיוב ייחודית בדף פירוט כרטיס האשראי של הלקוח

### שלב 10: תשלומים נדחים (תשלומי J4J5)

J4J5 מאפשר 4 תשלומים ללא ריבית, אפשרות תשלום פופולרית בישראל:

**יצירת תשלום נדחה:**

`POST /api/light/server/1.0/createPaymentProcess` עם page code של J4J5

**סילוק כשמוכנים:**

`POST /api/light/server/1.0/settleSuspendedTransaction`

| פרמטר | סוג | תיאור |
|-----------|------|-------------|
| `userId` | string | מזהה בית העסק |
| `transactionId` | string | עסקה מושהית לסילוק |
| `transactionToken` | string | טוקן העסקה |
| `sum` | number | הסכום לסילוק |

הקריאה מזוהה לפי `userId` ולא לפי `pageCode`. שליחת `pageCode` מחזירה `err.id` 54 על `userId`. הסילוק מוגבל: `err.id` 814 פירושו חיוב שחרג מתפיסת המסגרת ביותר מ-30 אחוז, 804 חריגה מהמסגרת, 803 פקיעת תוקף J5, ו-808 עסקה שכבר שוחררה.

**קשור:** גם `createFarPaymentRequest` קיים ב-Light API (אומת חי בשני השרתים). הכישור הזה לא מכסה אותו; קראו את דף התיעוד שלו לפני שימוש.

### שלב 11: הגדרת Webhooks

Grow שולחת התראות בזמן אמת לשרת שלכם לאירועים שונים. פנו ל-`apisupport@grow.business` להפעלת webhooks לחשבון שלכם.

**אפשרויות טריגר ל-webhook:**

| טריגר | תיאור |
|---------|-------------|
| כל העסקאות החד-פעמיות | כל תשלום בכל הדפים |
| דפי תשלום ספציפיים | סינון לפי page code |
| דרישות תשלום ספציפיות | סינון לפי דרישת תשלום |
| חיובים חוזרים | מהחיוב השני והלאה |
| חיובים חוזרים שנכשלו | כשחיוב חוזר נכשל |
| עסקאות POS | תשלומים פיזיים |
| יצירת חשבונית | כשחשבוניות מופקות |
| עסקאות אפליקציה | תשלומים דרך אפליקציית Grow |

**שדות נפוצים ב-webhook:**

| שדה | תיאור |
|-------|-------------|
| `webhookKey` | מזהה webhook ייחודי |
| `statusCode` | קוד סטטוס תשלום, `2` = שולם (הצלחה). בדקו את זה בצד השרת כדי לאשר שהתשלום הצליח לפני אספקה; הפניה בצד הלקוח לבדה אינה הוכחה |
| `transactionToken` | טוקן כרטיס שמור, שמרו אותו כדי לחייב מאוחר יותר דרך `createTransactionWithToken` לחיובים חוזרים |
| `transactionCode` | מזהה עסקה |
| `paymentSum` | סכום שחויב |
| `paymentDate` | חותמת זמן |
| `fullName` | שם המשלם |
| `payerPhone` | טלפון המשלם |
| `payerEmail` | אימייל המשלם |
| `cardSuffix` | 4 ספרות אחרונות של הכרטיס |
| `cardBrand` | מותג כרטיס (Visa, Mastercard וכו') |
| `asmachta` | מספר אסמכתא |
| `paymentSource` | מקור (דף, דרישה, POS וכו') |

**שדות נוספים ב-webhook חיוב חוזר:**

| שדה | תיאור |
|-------|-------------|
| `directDebitId` | מזהה סדרת החיובים |
| `allPaymentNum` | מספר התשלומים הכולל בסדרה (בפורמט PaymentLinks החדש מאויית `allPaymentsNum`) |
| `paymentsNum` | מספר תשלום בסדרה |
| `periodicalPaymentSum` | סכום חיוב חוזר |

**שדות נוספים ב-webhook חיוב חוזר שנכשל:**

| שדה | תיאור |
|-------|-------------|
| `error_message` | סיבת הכישלון |
| `charges_attempts` | מספר ניסיונות חוזרים |
| `regular_payment_id` | מזהה החיוב שנכשל |

**webhook חשבונית (מוגדר דרך `invoiceNotifyUrl`):**

| שדה | תיאור |
|-------|-------------|
| `transactionCode` | עסקה קשורה |
| `invoiceNumber` | מספר חשבונית שהופק |
| `invoiceUrl` | כתובת להורדת PDF החשבונית |

### שלב 12: 3D Secure

3DS רץ על משטח התשלום המתארח של Grow ולא בקוד השרת שלכם: הדף או ה-SDK wallet מציגים את האתגר לבעל הכרטיס, והאינטגרציה שלכם רואה רק את התוצאה הסופית ב-callback. Grow מתעדת את זה בדף ייעודי (ראו קישורי עזר).

הכישור הזה לא משכתב את המנגנון, כי אילו סוגי דפים מריצים אתגר, האם זה ניתן להגדרה על ידי הסוחר, ואיך העברת האחריות חלה על חיוב שרת-לשרת ב-`createTransactionWithToken` (עסקה ביוזמת הסוחר ולא בנוכחות בעל הכרטיס), לא ניתן היה לאמת בלי חשבון סוחר. קראו את דף ה-3DS לפני שאתם מסתמכים על הנחת העברת אחריות, ואל תניחו שחיוב בטוקן יורש את מצב ה-3DS של התשלום המקורי.

### שלב 13: סוגי דפי תשלום

Grow מציעה סוגי דפי תשלום מוכנים מראש, כל אחד עם `pageCode` שונה:

| סוג דף | תיאור | הערות |
|-----------|-------------|-------|
| SDK Wallet | ווידג'ט JS מודולרי | ללא צורך ב-iframe/redirect |
| גנרי | כרטיס אשראי + Bit | ניתן להתאמה, עד 2 שדות נוספים |
| כרטיס אשראי | תשלומי כרטיס בלבד | תומך ברגיל וחוזר |
| Google Pay | Google Pay בלבד | Chrome באנדרואיד; דורש `allow="payment"` ב-iframe |
| Apple Pay | Apple Pay בלבד | דורש אימות דומיין ל-iframe |
| Bit | תשלום נייד Bit | מומלץ למסך מלא במובייל |
| Bit QR | קוד QR ל-Bit | לתצוגת דסקטופ/בחנות |

**אינטגרציית iframe:**
```html
<iframe src="PAYMENT_URL_FROM_API"
        width="100%" height="600"
        allow="payment"
        style="border: none;">
</iframe>
```

**HTTPS חובה** לאינטגרציות iframe. HTTP לא יעבוד.

**מגבלת אורך כתובת:** 2000 תווים. השתמשו בערכי `cField` במקום query strings ארוכים.

## קודי שגיאה

Grow מחזירה שגיאות בגוף התשובה עם `status: 0` ואובייקט `err` שנושא `id` מספרי. הטבלה המלאה נמצאת בדף השגיאות (ראו קישורי עזר); אלה הקודים שאינטגרציה פוגשת הכי הרבה.

| קוד | משמעות |
|------|--------|
| 12 | שגיאה כללית |
| 54 | חסר שדה חובה; ההודעה נוקבת בשם השדה |
| 105 / 190 / 218 | סכום ההחזר גדול מהעסקה המקורית |
| 110 | הכסף כבר הועבר לבנק; ההחזר נשלח לאישור ידני |
| 130 / 207 | החזר חלקי אינו אפשרי עדיין (סולק היום או טרם שודר) |
| 170 | העסקה אינה קיימת |
| 210 | כבר בוצע החזר לעסקה |
| 271 | תשלום Bit מעל 3,600 שקל |
| 300 | בית העסק אינו מורשה לשירות API |
| 617 | סכום העסקה אינו זהה לסכום המוצרים |
| 701 | קוד זיהוי לא תקין: `userId` / `pageCode` |
| 707 | סכום לא תקין |
| 709 | פג תוקף הלינק |
| 712 | העסקה כבר בוצעה |
| 714 | הגישה נחסמה |
| 716 | קוד עסקה או טוקן לא תקין |
| 722 | אי אפשר לאשר עסקה שלא בוצעה או שבוטלה |
| 723 | `apiKey` הוא שדה חובה |
| 730 | קוד תהליך או טוקן לא תקין |
| 731 | `pageCode` אינו תואם את זה שאיתו בוצע הזיהוי |
| 734 | עסקת קרדיט דורשת לפחות 3 תשלומים ו-25 שקל |
| 736 | אי אפשר לשלוח `paymentNum` ו-`maxPaymentNum` יחד |
| 763 | JSON לא תקין בשדה `productData` |
| 803 | פג תוקף J5 |
| 814 | החיוב חורג מתפיסת המסגרת ביותר מ-30 אחוז |
| 403 | Forbidden: לא נשלחה `X-API-KEY` |

קיימים קודים נוספים מעבר לטבלה המפורסמת. `settleSuspendedTransaction` עם `userId` שאינו תואם מחזיר `err.id` 743 (`אין עסק תואם ל userId שנשלח`), ו-`createTransactionWithToken` עם `userId` לא מוכר מחזיר 104. תתייחסו לכל `err.id` לא מוכר ככישלון ותציגו את `err.message` במקום להניח הצלחה.

## מלכודות נפוצות
- הטעות הנפוצה ביותר באינטגרציה: ה-API של Grow דורש multipart/form-data לכל הבקשות, לא application/json. שליחת JSON לא מייצרת שגיאת content-type. השדות פשוט לא מפוענחים, ולכן מתקבלת שגיאת ולידציה על השדה החסר הראשון (בדרך כלל `err.id` 707, סכום לא תקין), וסוכנים מתחילים לחפש באג בסכום.
- כל תגובה היא HTTP 200, כולל כל כישלון. סוכן שבודק `response.ok` או את קוד הסטטוס יפרש קריאה שנדחתה כהצלחה. תסתעפו לפי השדה `status` בגוף התשובה (`1` הצלחה, `0` כישלון) ולפי `err`.
- `err` הוא אובייקט `{id, message}` בכישלון ולידציה, אבל המחרוזת `"unknown method"` כששם ה-endpoint אינו מוכר. תבדקו טיפוס לפני קריאת `err.id`.
- כל בקשות ה-API של Grow חייבות להגיע מהשרת, אבל לא בגלל ש-403 מוחזר לדפדפן. ה-API עונה כרגיל גם לבקשה שנושאת `Origin` ו-`Referer` של דפדפן; מה שמונע שימוש מצד הלקוח הוא שה-API לא שולח כותרות CORS, ולכן הדפדפן חוסם את קריאת התשובה. הסימפטום הוא שגיאת CORS בקונסול ולא 403. שגיאת 403 אמיתית מ-Grow פירושה שלא נשלחה כותרת `X-API-KEY`.
- `cardToken` ו-`transactionToken` אינם נתוני כרטיס, אבל הם כן אישורי גישה: מי שמחזיק `cardToken` יכול לחייב את הכרטיס דרך חשבון הסוחר שלכם. אל תרשמו אותם בלוגים, אל תשימו אותם בכתובת או בקוד צד לקוח, והצפינו אותם באחסון. דפוסי הדף המתארח, ה-iframe ודרישת התשלום קיימים כדי שמספרי כרטיס לא יגעו בשרת שלכם; אל תקבלו, תרשמו או תעבירו PAN בעצמכם.
- הסכומים הם בשקלים. תקרת Bit (3,600) ורצפת הקרדיט (25) בטבלת השגיאות של Grow שתיהן בשקלים. ה-API לא חושף פרמטר מטבע בקריאות שהכישור הזה מכסה, ולכן אל תניחו שאפשר לבטא חיוב במטבע זר על ידי שינוי `sum`.
- `paymentNum` ו-`maxPaymentNum` אינם יכולים לבוא יחד: שליחת שניהם מחזירה `err.id` 736. `maxPaymentNum` נדחה גם בעמוד הוראת קבע (739) וגם בחשבון שמוגדר לתשלום רגיל בלבד (740).
- ל-Bit יש תקרה לעסקה: `err.id` 271 מוחזר לתשלום Bit מעל 3,600 שקל. לעסקת קרדיט יש רצפה משלה, `err.id` 734: מינימום 3 תשלומים ו-25 שקל.
- אחרי קבלת webhook תשלום, חובה לקרוא ל-approveTransaction כדי לסגור את המעגל. סוכנים מדלגים לעתים על השלב הזה, מה שמשאיר עסקאות במצב ממתין במערכת של Grow.
- כתובות דפי תשלום פגות אחרי 10 דקות. סוכנים עלולים לשמור ולהשתמש מחדש בכתובת בין סשנים, מה שמוביל לדפים ריקים או שגיאות.

## פתרון בעיות

| בעיה | סיבה | פתרון |
|---------|-------|---------|
| HTTP 403 Forbidden | לא נשלחה כותרת `X-API-KEY`. זו הסיבה שטבלת השגיאות של Grow עצמה נותנת ל-403 | שלחו כותרת `X-API-KEY` בקריאות שדורשות אותה |
| בקשה מדפדפן נכשלת בלי 403 | ה-API לא שולח כותרות CORS ולכן הדפדפן חוסם את קריאת התשובה. אומת: בקשה שנושאת `Origin` ו-`Referer` של דפדפן נענית כרגיל | העבירו את הקריאה לשרת. אל תחפשו 403; הסימפטום הוא שגיאת CORS בקונסול |
| `err.id` 707 "סכום לא תקין" בבקשה שהסכום בה תקין | הסיבה הסבירה ביותר היא גוף JSON: השדות לא מפוענחים ולכן בדיקת הוולידציה הראשונה נופלת על הסכום. לא אומת שזה הטריגר היחיד | תעברו ל-`multipart/form-data` (FormData) ושלחו שוב |
| `err.id` 54 ב-`approveTransaction` | נשלח רק אחד משני המזהים הנדרשים | שלחו את `transactionId` וגם את `transactionToken` מה-callback |
| `err.id` 54 ב-`cancelBitTransaction` | הקריאה מזוהה לפי תהליך ולא לפי עסקה | שלחו `processId` ו-`processToken` ולא `transactionId` |
| `{"err":"unknown method"}` | שם ה-endpoint אינו קיים ב-Light API. `getTokenOnly`, `updatePaymentLink` ו-`updateRecurringPayment` מחזירים את זה בשני השרתים | השתמשו ב-endpoint חי; ראו שלב 9 ופרק קודי השגיאה |
| כל קריאה "מצליחה" אבל כלום לא קורה | הסתעפות לפי קוד ה-HTTP. כל תגובה היא 200, כולל כישלונות | תסתעפו לפי השדה `status` בגוף התשובה ולפי `err` |
| כתובת דף תשלום פגה (`err.id` 709) | הלינק עבר את חלון התוקף. החלון שמצוטט בדרך כלל הוא 10 דקות, אבל המספר לא אומת בתיעוד המפורסם של Grow | קראו ל-`createPaymentProcess` שוב לכתובת חדשה |
| Webhook לא התקבל | webhooks לא מופעלים | פנו ל-`apisupport@grow.business` להפעלה |
| עסקה לא נמצאה | סביבה לא נכונה | ודאו שעסקאות sandbox נשאלות מול כתובת sandbox |
| חיוב חוזר נכשל | כרטיס שפג תוקפו | הפעילו חיוב חוזר פרימיום לעדכון תפוגת כרטיס אוטומטי |
| localhost ב-successUrl | לא מורשה | השתמשו בטונל (ngrok) או כתובת מפורסת לבדיקות |
| iframe ריק ב-HTTP | HTTPS נדרש | הגישו את הדף שלכם דרך HTTPS |
| iframe של Apple Pay נכשל | דומיין לא מאומת | השלימו אימות דומיין Apple דרך לוח הבקרה של Grow |

## קישורי עזר

| מקור | קישור | מה לבדוק |
|------|-------|---------|
| תיעוד 3DS של Grow | https://developers.grow.business/reference/3ds-1 | איך 3DS מתנהג ואיפה חלה העברת האחריות |
| טבלת השגיאות של Grow | https://developers.grow.business/reference/errors | טבלת קודי השגיאה המספריים המלאה |
| תיעוד API של Grow | https://developers.grow.business/reference/overview | endpoints נוכחיים, אינדקסי transactionTypes, מבני בקשה ותגובה |
| תיעוד Grow | https://developers.grow.business/docs | טוקניזציה, חיובים חוזרים, תשלומי J-code, webhooks |
| סקירת מוצרי Grow | https://developers.grow.business/docs/about-grow-products | אילו מוצרים קיימים ב-Grow ואיך הם ממופים ל-API |
| כתובת בסיס פרודקשן (Meshulam) | https://secure.meshulam.co.il/ | אישור שכתובת הפרודקשן נכונה, לא להפנות תעבורה לסביבת sandbox |
| מדריך אינטגרציית Wix | https://support.wix.com/en/article/connecting-grow-by-meshulam-as-a-payment-provider | הדרכה ברמה גבוהה למרכזי Wix |
