# שער תשלומים Grow (משולם)

## סקירה

Grow (לשעבר משולם) היא אחת מחברות הסליקה המובילות בישראל, המפעילה אלפי עסקים עם סליקת כרטיסי אשראי, תשלומי Bit, Apple Pay, Google Pay ועוד. בניגוד לשערי תשלום ישראליים אחרים, Grow מציעה API אחיד ("Light API") שמכסה דפי תשלום, טוקניזציה, חיובים חוזרים, דרישות תשלום, חשבוניות ו-webhooks באינטגרציה אחת.

מדריך זה מנחה אינטגרציה עם Light API של Grow לכל מחזור חיי התשלום: קבלת תשלומים, שמירת טוקנים לחיובים חוזרים, יצירת דרישות תשלום, עיבוד החזרים וטיפול בהתראות webhook בזמן אמת.

**תיעוד רשמי:** `https://grow-il.readme.io/`

**תמיכה למפתחים:** `apisupport@grow.business`

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
| Production | `https://api.meshulam.co.il` |

**חשוב: צד שרת בלבד.** כל בקשות ה-API חייבות להגיע מהשרת שלכם. בקשות מצד הלקוח (דפדפן) נחסמות על ידי Grow.

**חשוב: פורמט FormData.** כל גוף הבקשות משתמש ב-`multipart/form-data`, לא JSON. זו טעות נפוצה -- אם תשלחו `application/json`, ה-API ידחה את הבקשה.

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
| `transactionTypes[0]` | integer | סינון אמצעי תשלום (ראו טבלה למטה) |

**קודי אמצעי תשלום (transactionTypes):**

| קוד | אמצעי תשלום |
|------|---------------|
| 1 | כרטיס אשראי |
| 5 | Pay Box |
| 6 | Bit |
| 13 | Apple Pay |
| 14 | Google Pay |
| 15 | העברה בנקאית |

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

**תמיד אמתו דרך callback השרת**, לא דרך ההפניה בצד הלקוח (שניתנת לזיוף).

### שלב 5: אישור העסקה (חובה)

לאחר קבלת callback השרת, חובה לקרוא ל-`approveTransaction` כדי לאשר קבלה. זה לא משנה את התשלום -- זה סוגר את מחזור העסקה מול Grow.

**Endpoint:** `POST /api/light/server/1.0/approveTransaction`

```bash
curl -X POST https://sandbox.meshulam.co.il/api/light/server/1.0/approveTransaction \
  -F "pageCode=YOUR_PAGE_CODE" \
  -F "transactionId=TRANSACTION_ID_FROM_CALLBACK"
```

**אל תקראו ל-approveTransaction עבור:** שמירת טוקן בלבד, עסקאות נדחות (J4J5), או חיובי `createTransactionWithToken`.

### שלב 6: שליפת פרטי עסקה

**קבלת פרטי עסקה:**

`POST /api/light/server/1.0/getTransactionInfo`

| פרמטר | סוג | תיאור |
|-----------|------|-------------|
| `pageCode` | string | מזהה דף |
| `transactionId` | string | מזהה העסקה לשליפה |

**קבלת פרטי תהליך תשלום:**

`POST /api/light/server/1.0/getPaymentProcessInfo`

| פרמטר | סוג | תיאור |
|-----------|------|-------------|
| `pageCode` | string | מזהה דף |
| `processId` | string | מזהה התהליך מ-createPaymentProcess |

### שלב 7: עיבוד החזרים

**החזר עסקת כרטיס אשראי:**

`POST /api/light/server/1.0/refundTransaction`

| פרמטר | סוג | תיאור |
|-----------|------|-------------|
| `pageCode` | string | מזהה דף |
| `transactionId` | string | עסקה להחזר |
| `refundSum` | number | סכום ההחזר (חלקי או מלא) |

**ביטול עסקת Bit:**

`POST /api/light/server/1.0/cancelBitTransaction`

| פרמטר | סוג | תיאור |
|-----------|------|-------------|
| `pageCode` | string | מזהה דף |
| `transactionId` | string | עסקת Bit לביטול |

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

התגובה כוללת כתובת תשלום לשיתוף. ניתן גם לעדכן (`updatePaymentLink`) או לשלוף (`getPaymentLinkInfo`) דרישות קיימות.

### שלב 9: טוקניזציה וחיובים חוזרים

Grow תומכת בשלושה מודלים לחיובים חוזרים:

#### אפשרות א: מנוהל על ידי Grow דרך Page Code

השתמשו ב-page code ייעודי לחיובים חוזרים שמוגדר בלוח הבקרה של Grow:

1. צרו תשלום עם `createPaymentProcess` עם page code לחיובים חוזרים
2. הגדירו `sum` לסכום החיוב החודשי ו-`paymentNum` למספר החיובים הכולל
3. Grow מטפלת בכל החיובים הבאים אוטומטית

#### אפשרות ב: מנוהל על ידי Grow דרך טוקן

השתמשו ב-`createTransactionWithToken` עם תזמון אוטומטי:

```bash
curl -X POST https://sandbox.meshulam.co.il/api/light/server/1.0/createTransactionWithToken \
  -F "pageCode=YOUR_PAGE_CODE" \
  -F "userId=YOUR_USER_ID" \
  -F "sum=99.00" \
  -F "token=SAVED_TOKEN" \
  -F "paymentType=1" \
  -F "paymentNum=12"
```

הגדרת `paymentType=1` עם `paymentNum` אומרת ל-Grow לנהל 12 חיובים חודשיים.

#### אפשרות ג: מנוהל על ידי בית העסק דרך טוקן (שליטה מלאה)

אתם שולטים מתי כל חיוב מתבצע:

**תשלום ראשון (שמירת טוקן):**

```bash
curl -X POST https://sandbox.meshulam.co.il/api/light/server/1.0/createTransactionWithToken \
  -F "pageCode=YOUR_PAGE_CODE" \
  -F "userId=YOUR_USER_ID" \
  -F "sum=99.00" \
  -F "token=SAVED_TOKEN" \
  -F "isRecurringDebitId=1"
```

התגובה כוללת `recurringDebitId` -- שמרו אותו לקישור חיובים עתידיים.

**חיובים הבאים:**

```bash
curl -X POST https://sandbox.meshulam.co.il/api/light/server/1.0/createTransactionWithToken \
  -F "pageCode=YOUR_PAGE_CODE" \
  -F "userId=YOUR_USER_ID" \
  -F "sum=99.00" \
  -F "token=SAVED_TOKEN" \
  -F "recurringDebitId=RECURRING_DEBIT_ID"
```

**עדכון חיוב חוזר:**

`POST /api/light/server/1.0/updateRecurringPayment` -- שינוי סכום, השהייה או ביטול.

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
| `pageCode` | string | מזהה דף |
| `transactionId` | string | עסקה מושהית לסילוק |

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

### שלב 12: סוגי דפי תשלום

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

## פתרון בעיות

| בעיה | סיבה | פתרון |
|---------|-------|---------|
| API מחזיר 403 או תגובה ריקה | בקשה מצד הלקוח | העבירו קריאות API לשרת; Grow חוסמת בקשות מדפדפן |
| שגיאת פענוח בבקשה | שימוש ב-JSON content type | עברו ל-`multipart/form-data` (FormData), לא `application/json` |
| כתובת דף תשלום פגה | כתובת ישנה מ-10 דקות | קראו ל-`createPaymentProcess` שוב לכתובת חדשה |
| Webhook לא התקבל | webhooks לא מופעלים | פנו ל-`apisupport@grow.business` להפעלה |
| עסקה לא נמצאה | סביבה לא נכונה | ודאו שעסקאות sandbox נשאלות מול כתובת sandbox |
| חיוב חוזר נכשל | כרטיס שפג תוקפו | הפעילו חיוב חוזר פרימיום לעדכון תפוגת כרטיס אוטומטי |
| localhost ב-successUrl | לא מורשה | השתמשו בטונל (ngrok) או כתובת מפורסת לבדיקות |
| iframe ריק ב-HTTP | HTTPS נדרש | הגישו את הדף שלכם דרך HTTPS |
| iframe של Apple Pay נכשל | דומיין לא מאומת | השלימו אימות דומיין Apple דרך לוח הבקרה של Grow |

## מקורות

- [תיעוד API של Grow](https://grow-il.readme.io/)
- [סקירת מוצרים](https://grow-il.readme.io/docs/about-grow-products)
- [מסמך API](https://grow-il.readme.io/reference/overview-6)
- [תיעוד Webhooks](https://grow-il.readme.io/docs/overview-7)
- [מדריך אינטגרציית Wix](https://support.wix.com/en/article/connecting-grow-by-meshulam-as-a-payment-provider)
