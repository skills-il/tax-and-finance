# שער תשלומים פלאקארד

## בעיה

פלאקארד היא PSP (ספק שירותי תשלום) ואחת ממאגדות הסליקה הגדולות בישראל, אבל התיעוד הציבורי מפוזר בין Postman, ה-sandbox, פלאגין WordPress וספריות PHP של צד שלישי, בלי מקור אחד אמין. סוכנים שמנסים לחבר פלאקארד מתבלבלים בין `gateway20` הישן ל-`gateway21` בפרודקשן, בוחרים `ActionType` שגוי (וזה משנה בשקט אם הכסף בכלל זז), או סומכים על `ConfirmationKey` בצד הדפדפן במקום לאמת בצד השרת. כל אחת מהטעויות האלה גוררת אובדן הכנסה, או גרוע מזה, מסלול "הזמנה חינם" שאפשר לנצל בפרודקשן.

## סקירה

פלאקארד היא PSP (ספק שירותי תשלום) ואחת ממאגדות סליקת הכרטיסים הגדולות בישראל. הסליקה עצמה רצה על רשת שב"א (https://www.shva.co.il/, שירותי בנק אוטומטיים), ופלאקארד מטפלת מעל זה ברישום בית עסק, משטח התשלום ב-iframe, טוקניזציה והתאמות.

האינטגרציה הדומיננטית היא דף תשלום ב-iframe: השרת שלך שולח שלשת אימות (`terminal` + `user` + `password`) יחד עם פרמטרי העסקה לפלאקארד, מקבל בתגובה `URL` ו-`ConfirmationKey`, ומפנה את הלקוח לשם או מטמיע את ה-URL כ-iframe. אחרי שהלקוח משלם, פלאקארד פונה ל-feedback URL בשרת שלך עם `PelecardStatusCode` ו-`ConfirmationKey`. שמרו את ה-`ConfirmationKey` משלב 1 בצד השרת לפי מזהה ההזמנה, ואז ב-callback אתם חייבים: (א) להשוות את ה-`ConfirmationKey` שב-callback בייט-לבייט לערך השמור, וגם (ב) לקרוא שוב ל-`PaymentGW/GetTransaction` ולוודא ש-`DebitTotal` ו-`PelecardTransactionId` תואמים, לפני שהזמנה נחשבת לשולמה.

הכלי הזה מתאים למפתחים, מהנדסי מוצר ובעלי עסקים ישראלים שמחברים פלאקארד בפעם הראשונה. הוא עובר על זרימת ה-iframe, אימות בצד שרת, תשלומים (תשלומי קרדיט), טוקניזציה, חיובים חוזרים על טוקן שמור, החזרים, 3D Secure 2 והמוזרויות של ארנק Bit (אין תשלומים, תקרה נמוכה לעסקה).

ה-Match API החדש ב-`match-api.pelecard.biz` קיים, אבל התיעוד הפומבי שלו לא היה זמין במחקר. כדאי להתייחס אליו כמסלול ה-REST המודרני ולוודא את צורת ה-endpoint ישירות מול פלאקארד לפני שמסתמכים עליו.

## הוראות

### שלב 1: בחירת דפוס אינטגרציה

| דפוס | טיפול בנתוני כרטיס | מתאים ל- |
|------|------|------|
| **Iframe / דף מתארח** (`gateway21.pelecard.biz`) | פלאקארד מארחת את דף הזנת הכרטיס | רוב האינטגרציות, היקף PCI מינימלי |
| **חיוב טוקן שמור** (שרת-לשרת) | טוקן בלבד, בלי PAN | חיובים חוזרים, הוראות קבע, checkout בלחיצה |
| **Apple Pay דרך ClientSecure.js** | Apple Pay מטפל בנתוני הכרטיס | לקוחות iOS/Safari על מכשירים נתמכים |
| **ארנק Bit** | A2A push, בלי נתוני כרטיס בכלל | לקוחות מובייל ישראלים, תשלום אחד, שקלים בלבד (תכננו עם תקרה של 5,000 ₪ לעסקה אלא אם יש אישור בכתב אחרת) |
| **Match API** (`match-api.pelecard.biz`) | משטח REST מודרני | לוודא מול הספק לפני שימוש; דף התיעוד היה ריק במחקר |

רוב בתי העסק הישראלים מריצים iframe לתשלום הראשון (יוצרים טוקן באותו רגע), ואז מחייבים את הטוקן השמור בכל חידוש.

### שלב 2: הגדרת אימות

כל קריאה לפלאקארד דורשת שלשת אימות, נשלחת רק מצד שרת:

- `terminal` -- מזהה המסוף שפלאקארד הנפיקה
- `user` -- שם משתמש ב-API
- `password` -- סיסמת API

שלושת הערכים האלה פותחים את המסוף שלך לחיובים. הם חייבים לחיות במשתני סביבה בצד השרת. אף פעם לא ב-JavaScript של הדפדפן, לא בחבילה של אפליקציה ניידת ולא בהיסטוריית git. הספרייה dofinity/pelecard מצהירה עליהם כ-`protected $terminal; protected $user; protected $password;` -- הקונבנציה היא "פרטי גישה לא יוצאים מהשרת".

**Sandbox:** `gateway20.pelecard.biz/sandbox` לפיתוח.
**פרודקשן:** `gateway21.pelecard.biz` לעסקאות אמיתיות.

לכל סביבה יש פרטי גישה משלה. החלפת host נעשית במשתנה סביבה בזמן deploy, לא ברמת קוד.

### שלב 3: יצירת דף תשלום ב-iframe

תבנו גוף בקשה עם פרטי הגישה, `Total` (באגורות, ראו הערה למטה על יחידות כסף), `Currency`, `ActionType` ו-feedback URLs.

**שדות סכום משתמשים ביחידות מינור (אגורות) ב-Gateway21.** שולחים `Total: 9900` עבור 99.00 ₪, `FirstPayment: 5000` עבור תשלום ראשון של 50.00 ₪. ה-wrapper של dofinity מתעד את `FirstPayment` כ-"in agorot/cents", ואותה קונבנציה תקפה ל-`Total`. תוודאו מול ה-sandbox שלכם עם חיוב מבחן של 1 ₪ לפני עלייה לאוויר, כדי לא לחטוף שגיאת פי 100.

נתיב יצירת ה-session הוא `PaymentGW/init` (לפי ה-wrapper של dofinity, `const PAYMENT_INIT_URI = 'PaymentGW/init'`); ב-Gateway21 קיים גם משטח REST תחת `/services`. תאמתו את הנתיב המדויק למסוף שלכם ב-Postman הרשמי של פלאקארד (https://www.postman.com/peleteam/pelecard-public/overview, אוסף "Gateway21") לפני עלייה לאוויר. צורת גוף הבקשה (שלשת האימות + פרמטרי העסקה) מתועדת למטה.

```
POST https://gateway21.pelecard.biz/PaymentGW/init
Content-Type: application/json

{
  "terminal": "<your-terminal>",
  "user": "<api-user>",
  "password": "<api-password>",
  "ActionType": "J4",
  "Currency": 1,
  "Total": 9900,
  "MaxPayments": 12,
  "MinPayments": 1,
  "GoodURL": "https://example.com/pay/success",
  "ErrorURL": "https://example.com/pay/error",
  "CancelURL": "https://example.com/pay/cancel",
  "ServerSideGoodFeedbackURL": "https://example.com/api/pelecard/ipn-success",
  "ServerSideErrorFeedbackURL": "https://example.com/api/pelecard/ipn-error",
  "ParamX": "order-2026-0042",
  "ShopNo": "main-shop",
  "CreateToken": true
}
```

פלאקארד מחזירה `URL` ו-`ConfirmationKey`. **תשמרו את ה-`ConfirmationKey` בצד השרת לפי מזהה ההזמנה** (תשוו אותו ב-callback בשלב 4). אחר כך תפנו את הלקוח ל-URL הזה או תטמיעו אותו כ-iframe.

**טבלת ActionType (הטבלה המלאה ב-`references/payment-parameters.md`):**

| ערך | משמעות |
|-----|--------|
| `J4` | מכירה רגילה (ברירת מחדל). הכסף זז עכשיו. |
| `J2` | אימות כרטיס / רישום בלבד. בלי חיוב. |
| `J5` | אישור עכשיו, חיוב מאוחר יותר. |
| `J5h` | J5 משופר. |

בחירת `ActionType` שגוי היא הבאג הכי נפוץ באינטגרציות סליקה ישראליות: `J2` נראה זהה ל-`J4` בממשק של פלאקארד אבל לא מזיז כסף.

### שלב 4: אימות ה-callback בצד שרת

כשהלקוח מסיים לשלם, פלאקארד פונה ל-`ServerSideGoodFeedbackURL` שלכם עם `PelecardStatusCode`, `ConfirmationKey` ו-`PelecardTransactionId`. לפני שאתם מסמנים את ההזמנה כשולמה, אתם חייבים לעשות את כל אלה בצד השרת:

1. לטעון את ה-`ConfirmationKey` ששמרתם בשלב 1 על ההזמנה הזו, ולהשוות אותו בייט-לבייט לערך ב-callback. אם אין התאמה, לדחות את התשלום.
2. לקרוא שוב ל-`PaymentGW/GetTransaction` עם `terminal/user/password/TransactionId` (ה-`TransactionId` הוא ה-`PelecardTransactionId` שהגיע ב-callback).
3. לוודא בתשובת `GetTransaction` ש-`DebitTotal` תואם לסכום ההזמנה הצפוי (באגורות) ו-`PelecardTransactionId` תואם ל-callback. (ה-`ConfirmationKey` מושווה בשלב 1 בין הערך השמור משלב 1 ל-callback; `GetTransaction` מחזיר את רשומת העסקה, לא את ה-ConfirmationKey, ולכן ההתאמה של הסכום והמזהה היא מה שמאמת את ה-lookup.)

**פלאקארד לא חותמת את ה-IPN ב-HMAC.** אסור לסמוך על payload שמגיע עם `ConfirmationKey` שמוכר לכם בלי לקרוא שוב לעסקה בשרת. אפשר לזייף `ConfirmationKey` בצד הדפדפן; המקור היחיד האמין הוא קריאת `GetTransaction` משרת לשרת.

ה-wrapper של dofinity/pelecard עוטף את השלבים האלה (הערה: הספרייה הזו מקובעת ל-host הישן `gateway20` ומאמתת דרך `PaymentGW/ValidateByUniqueKey` ששולח `ConfirmationKey`/`UniqueKey`/`TotalX100`; ב-Gateway21 האימות המקביל הוא `PaymentGW/GetTransaction`, למטה):

```php
$PaymentResponse = new \Pelecard\PaymentResponse(
    $PelecardStatusCode, $PelecardTransactionId, '', '', $ConfirmationKey, 100
);
$payment = new \Pelecard\PelecardPayment();
$payment->setPaymentResponse($PaymentResponse);
if ($payment->ValidatePayment()) {
    // Ok. Payment has been verified
}
```

מתחת למכסה המנוע, האימות קורא ל-`PaymentGW/GetTransaction` עם שלשת האימות וה-`TransactionId`:

```
POST https://gateway21.pelecard.biz/PaymentGW/GetTransaction
{
  "terminal": "<terminal>",
  "user": "<user>",
  "password": "<password>",
  "TransactionId": "<PelecardTransactionId from callback>"
}
```

התגובה מכילה את `DebitTotal` האמין (הסכום שהלקוח חויב בו בפועל, באגורות), את `DebitApproveNumber` (מספר האישור של שב"א), `TotalPayments` (מספר תשלומים), 4 ספרות אחרונות מוסתרות, תפוגה, ואת `ParamX` שלכם בחזרה. תשוו את `DebitTotal` לסכום הצפוי בהזמנה; פער = ניסיון שיבוש, אסור לסמן את ההזמנה כשולמה.

**Idempotency / dedupe.** `ParamX` הוא מזהה קורלציה של בית העסק להזמנה, **לא** מפתח idempotency. פלאקארד עלולה להגיש את אותו IPN פעמיים על אותה הזמנה (למשל ב-retry של timeout; ב-changelog 1.5.1: "Fixed timeout-retry issues"). תעשו dedupe לפי **`PelecardTransactionId`** (מזהה הניסיון של פלאקארד), שייחודי לכל ניסיון. תסמנו כל `PelecardTransactionId` כ"טופל" ב-DB כדי שהמסירה השנייה תהיה no-op.

**רשת ביטחון להתאמות.** ה-feedback בצד השרת נורה רק כשהעסקה מגיעה למצב סופי (הצלחה או שגיאה שנדחתה). אם הלקוח סוגר את הדפדפן לפני שליחת טופס הכרטיס, אף IPN לא יישלח. רשת הביטחון השלמה: לשמור את ה-`PelecardTransactionId` שחוזר מקריאת יצירת ה-session, ואז להריץ ג'וב התאמה תקופתי שמושך `PaymentGW/GetTransaction` עבור כל session שלא קיבל IPN בחלון ה-timeout שלכם.

תריצו את הסקריפט המצורף `scripts/validate_pelecard_response.py` על ה-callback בזמן פיתוח. הוא מתריע כשחסרים `ConfirmationKey` או `PelecardTransactionId`, ומדגיש פורמט סטטוס לא-תקני (`0`/`00` במקום `000`).

### שלב 5: חיוב טוקן שמור (חיובים חוזרים)

לחיוב טוקן שמור (מנויים, הוראות קבע), תעבירו `IsToken=true` יחד עם ה-`Token` השמור ו-`TokenCreditCardDigits`, במקום שדות הזנת כרטיס. החיובים הבאים רצים שרת-לשרת בלי iframe.

העסקה הראשונה מסומנת ב-`CreateToken: true` ופלאקארד שומרת את הטוקן מול `TokenForTerminal`. תשמרו את מזהה הטוקן ואת 4 הספרות האחרונות + תפוגה שחוזרים בתגובת האימות. בכל חידוש, תשלחו עסקת J4 עם הפנייה לטוקן וה-`Total` החדש. פלאגין ה-WordPress של פלאקארד תומך ב"Saved payment methods (tokenization)" מאז גרסה 1.2.0, וב"WooCommerce Subscriptions support" מאז 1.4.

**חיובים חוזרים + 3DS (פטור MIT).** תחת EMV 3DS 2.x, חיובים חוזרים על טוקן שמור יכולים להיכנס לפטור MIT (Merchant Initiated Transaction), כך ששב"א לא תיצור challenge ללקוח בכל חידוש. ה-changelog של פלאקארד מתייחס לדפוס הזה (גרסה 1.4.8: "Add 3D-Secure params to J4 after J5 requests"). כדאי לוודא עם תמיכת פלאקארד את שם הפרמטר המדויק ל-MIT עבור המסוף שלכם לפני שמסתמכים על הפטור; בלעדיו, חיובים חוזרים עלולים להיכשל לפעמים בדחיית 3DS.

### שלב 6: ביצוע החזרים

זרימת ההחזרים של פלאקארד נחשפת ב-endpoint שרת-לשרת של "DebitRegular cancel" / refund (הנתיב המדויק נמצא ב-Postman, אוסף "Gateway21"). בית העסק קורא לו עם `terminal/user/password/PelecardTransactionId` ועם `Total` החזר באגורות (מלא או חלקי). פלאקארד מחזירה `PelecardTransactionId` חדש לרגל ההחזר; שמרו אותו על ההזמנה המקורית.

**חוק הגנת הצרכן הישראלי (סעיפים 14ג-14ה)** מסדיר החזרים בעסקאות מכר מרחוק: הצרכן יכול לבטל בתוך 14 ימים, בית העסק חייב להחזיר את הכסף בתוך 14 ימים מקבלת הודעת הביטול, ודמי ביטול מוגבלים ל-5% מהמחיר ששולם או 100 ₪, לפי הנמוך מביניהם. תבנו את זרימת ההחזרים סביב המועדים האלה ותשיקו אותה לפני העלייה לאוויר, לא אחריה. (מקור: כל-זכות, על בסיס פרק המכר מרחוק בחוק הגנת הצרכן.)

### שלב 7: הגדרת 3D Secure 2 ו-Bit

**3D Secure 2 (EMV 3DS).** ממשק ה-sandbox חושף את `Initiate` ו-`AskForChallenge` (כל אחד: `None` ברירת מחדל, `False`, `True`). ב-changelog של פלאגין 1.4.19 מופיע "Added Emv errors in order notes. ShvaResultEmv parameter". מומלץ להגדיר 3DS כחובה עבור עסקים חדשים בהתאם לציפיות SCA של בנק ישראל. כשקוד תוצאה EMV מגיע ב-callback, תרשמו אותו ביומן.

**ארנק Bit.** Bit הוא ארנק A2A מאושר על ידי בנק ישראל. אילוצים שכדאי לבנות סביבם את ה-UX:

- **תשלום אחד בלבד.** מ-allpay.co.il: "No installments. You can only pay with Bit in one payment." תסתירו את בורר התשלומים כש-Bit נבחר.
- **שקלים בלבד.** Bit מקבל רק ש"ח. תשלחו `Currency: 1` לכל עסקת Bit; עסקאות Bit לא-ILS נכשלות בלי שגיאה ברורה.
- **תקרה לעסקה נקבעת לפי דירוג הסיכון של בית העסק.** התקרה לעסקה נקבעת בהסכם ה-Bit עם בית העסק ובדירוג הסיכון של מפעיל הארנק. הערך הנפוץ הוא 5,000 ₪ לעסקה (לפי הנחיית allpay.co.il: "Payment via Bit cannot exceed 5,000 shekels"), אבל בתי עסק בדירוג גבוה יותר מאושרים מעל זה. תבדקו את הסכם ה-Bit שלכם; תכננו עם תקרה של 5,000 ₪ אלא אם יש לכם אישור בכתב אחרת.
- ל-Bit יש גם תקרה חודשית לעסק וחלון זמן של 10 דקות ללקוח. ראו allpay.co.il/en/help/bit.

**Apple Pay.** פלאקארד מארחת את ה-SDK ב-`ClientSecure.js`. הפלאגין רושם: "Apple Pay Support (optional, disabled by default) -- When enabled, loads ClientSecure.js from Pelecard servers to enable Apple Pay on supported devices."

### שלב 8: טיפול בשגיאות

פלאקארד מחזירה `PelecardStatusCode` מספרי ב-callback. בקונבנציה `000` זו הצלחה, וכל ערך אחר זו שגיאה. הטבלה המדויקת של קוד-למשמעות משתנה לפי acquirer ומשתנה עם הזמן. קודי תוצאה EMV נוסעים ליד דרך `ShvaResultEmv`. ראו `references/error-codes.md` לקטגוריות שתפגשו (כשל אימות, סירוב, כרטיס פג תוקף, חוסר כיסוי, דרישת challenge ל-3DS, timeout). לקודים מספריים ספציפיים שנתקלים בהם בפרודקשן, כדאי לפנות לתמיכת פלאקארד. אל תנחשו לפי מאמרים גנריים על סליקה ישראלית.

## דוגמאות

### דוגמה 1: checkout iframe ראשון
המשתמש אומר: "אני רוצה לקבל תשלומי אשראי באתר ישראלי דרך פלאקארד, עד 12 תשלומים."
פעולות:
1. שרת: POST של פרטי גישה + `ActionType: J4` + `Total: 9900` (99.00 ₪ באגורות) + `Currency: 1` + `MaxPayments: 12` לנתיב יצירת ה-session ב-Gateway21 (מתוך ה-Postman של פלאקארד).
2. תקבלו `URL` ו-`ConfirmationKey`. תשמרו את ה-`ConfirmationKey` בצד השרת לפי מזהה ההזמנה. תרנדרו את ה-URL ב-iframe (או תפנו).
3. תאזינו ב-`ServerSideGoodFeedbackURL` ל-callback.
4. תשוו את ה-`ConfirmationKey` שב-callback לערך השמור, ואז תאמתו דרך `PaymentGW/GetTransaction` ש-`DebitTotal` תואם להזמנה לפני שמסמנים את ההזמנה שולמה.
תוצאה: הלקוח משלם ב-1 עד 12 תשלומים, יש לכם מזהה עסקה מאומת.

### דוגמה 2: לשמור כרטיס ולחייב כל חודש
המשתמש אומר: "אני מפעיל SaaS, צריך לחייב משתמשים 99 ₪ בחודש עם הכרטיס השמור."
פעולות:
1. תשלום ראשון: iframe POST עם `CreateToken: true` ו-`Total: 9900` (אגורות). תשמרו את הטוקן + 4 ספרות אחרונות + תפוגה.
2. cron חודשי: POST עם `IsToken: true` והפנייה לטוקן + ה-`Total` החדש (באגורות).
3. תאמתו כל חיוב דרך `PaymentGW/GetTransaction`, ותעשו dedupe ל-IPN לפי `PelecardTransactionId`.
4. תטפלו בסירובים, כרטיסים פגי תוקף ו-3DS step-up. בחידושים, כדאי לשאול את תמיכת פלאקארד על פרמטרי MIT כדי ששב"א לא תיצור challenge בכל מחזור.
תוצאה: חיוב חוזר בלי לאחסן PAN על השרתים שלכם.

### דוגמה 3: להוסיף Bit כאופציה ב-checkout
המשתמש אומר: "רוב הלקוחות הישראלים שלי רוצים Bit, אפשר להוסיף?"
פעולות:
1. תפעילו Bit במסוף פלאקארד (הגדרה אצל הספק).
2. בממשק ה-checkout, תשלחו `Currency: 1` (Bit הוא בש"ח בלבד) ותגבילו את ה-Bit ל-`Total <= 5,000 ₪` כתקרת תכנון, אלא אם הסכם ה-Bit שלכם מאשר תקרה גבוהה יותר.
3. תסתירו את בורר התשלומים כש-Bit נבחר. Bit הוא תשלום אחד בלבד.
4. אותה זרימת callback: להשוות `ConfirmationKey` משלב 1, ואז לאמת תוצאה דרך `PaymentGW/GetTransaction` מול `DebitTotal`.
תוצאה: Bit נוסף בצורה נקייה, בלי חיובים שנכשלים בגלל אילוצי הארנק.

### דוגמה 4: לאמת payload של callback מקומית
המשתמש אומר: "ה-callback של פלאקארד הגיע. איך אני בודק אותו לפני שאני קורא ל-GetTransaction?"
פעולות:
1. תריצו `python scripts/validate_pelecard_response.py --response '{"PelecardStatusCode":"000","ConfirmationKey":"...","PelecardTransactionId":"...","Total":9900,"Currency":1}'`.
2. הסקריפט מתריע על `ConfirmationKey` או `PelecardTransactionId` חסרים, דורש את הפורמט הקנוני `"000"` (ומתריע על `"0"` / `"00"`), ומדפיס את השדות שנקלטו.
3. אם זה עובר, תשוו את ה-`ConfirmationKey` שב-callback לערך ששמרתם בשלב 1, ואז תקראו ל-`PaymentGW/GetTransaction` ותשוו את `DebitTotal` שחוזר להזמנה (באגורות).
תוצאה: בדיקה מקומית מהירה לפני שפונים ל-API של פלאקארד.

### דוגמה 5: אישור עכשיו, חיוב במשלוח (J5)
המשתמש אומר: "אני רוצה לאשר את הכרטיס בזמן ההזמנה ולחייב רק כשאני שולח, כמו אמזון."
פעולות:
1. קריאה ראשונה: `ActionType: J5`. פלאקארד מאשרת את הכרטיס, בלי תזוזת כסף.
2. במשלוח, תקראו לזרימת ה-capture שמשויכת לעסקת J5 שלכם (לוודא את ה-API המדויק עם תמיכת פלאקארד; ב-changelog של פלאגין 1.4.8 רשום "Add 3D-Secure params to J4 after J5 requests").
3. תאמתו את העסקה שנקלטה דרך `PaymentGW/GetTransaction`.
תוצאה: דפוס auth-then-capture שמתאים לזרימות e-commerce ישראליות.

### דוגמה 6: החזר על הזמנה בעייתית
המשתמש אומר: "לקוח התלונן על הזמנה 5678, צריך להחזיר."
פעולות:
1. תוציאו את ה-`PelecardTransactionId` המקורי מרשומת ההזמנה שלכם (ששמרתם משלב 1 / מה-IPN).
2. תקראו ל-endpoint ההחזרים של פלאקארד (הנתיב נמצא ב-Postman באוסף "Gateway21") עם `terminal/user/password/PelecardTransactionId` ועם `Total` החזר באגורות (מלא או חלקי).
3. תשמרו את ה-`PelecardTransactionId` החדש שפלאקארד מחזירה לרגל ההחזר על ההזמנה המקורית.
4. תכבדו את לוחות הזמנים של חוק הגנת הצרכן: 14 ימים להחזר מקבלת הודעת הביטול, ודמי ביטול עד 5% או 100 ₪, לפי הנמוך מביניהם.
5. אם אתם מנפיקים חשבונית זיכוי, תפיקו אותה דרך ספק החשבוניות שלכם. פלאקארד מטפלת בכסף, לא במסמך המס.
תוצאה: ההחזר מעובד בתוך החלון החוקי. שלבו עם הכלי `green-invoice` לצד הציות של חשבונית הזיכוי.

## משאבים מצורפים

### חומרי עזר
- `references/api-endpoints.md` -- hosts של פלאקארד (sandbox + פרודקשן), זרימת ה-iframe POST + ConfirmationKey, ה-lookup של `PaymentGW/GetTransaction`, והערה על Match API החדש. תסתכלו על הקובץ כשמחברים endpoint חדש.
- `references/payment-parameters.md` -- מדריך פרמטרים מלא: ActionType (J2/J4/J5/J5h), קודי מטבע, תשלומים, טוקניזציה, בקרות BIN, התאמה אישית של UI, server-side feedback URLs, שדות passthrough מותאמים. תסתכלו על הקובץ כשבונים את גוף הבקשה ל-iframe.
- `references/error-codes.md` -- קטגוריות של קודי סטטוס פלאקארד וקודי תוצאה EMV/שב"א (ShvaResultEmv). תסתכלו על הקובץ כשמדבגים callback שנכשל.

### סקריפטים
- `scripts/validate_pelecard_response.py` -- מאמת JSON של callback מפלאקארד: בודק `PelecardStatusCode`, מוודא ש-`ConfirmationKey` ו-`PelecardTransactionId` קיימים, בודק שפיות על `Total` ו-`Currency`, ומתריע כש-`ConfirmationKey` חסר (המקרה הכי מסוכן). הרצה: `python scripts/validate_pelecard_response.py --help`.

## שרתי MCP מומלצים

עדיין אין שרת MCP לפלאקארד. אפשר להשתמש בכלי `green-invoice` להפקת חשבונית אחרי החיוב, כי פלאקארד מטפלת בכסף ולא במסמך המס הישראלי (חשבונית מס).

## קישורי עזר

| מקור | מטרה |
|------|------|
| https://www.postman.com/peleteam/pelecard-public/overview | סביבת ה-Postman הרשמית של פלאקארד (אוסף "Gateway21"). לוודא גופי בקשה ודוגמאות. |
| https://gateway20.pelecard.biz/sandbox | sandbox רשמי + מדריך פרמטרים. ActionType, מטבע, 3DS, Bit/Apple Pay/Google Pay. |
| https://wordpress.org/plugins/woo-pelecard-gateway/ | פלאגין ה-WooCommerce של פלאקארד. מאשר את host `gateway21.pelecard.biz`, החזרים, מנויים, טוקניזציה, Apple Pay דרך ClientSecure.js. |
| https://github.com/dofinity/pelecard | wrapper PHP של צד שלישי. מתעד את כל סט הפרמטרים של `PaymentRequest`, את זרימת אימות ה-`ConfirmationKey` ואת `PaymentGW/GetTransaction`. |
| https://match-api.pelecard.biz/docs/index | sandbox של Match REST של פלאקארד (משטח מודרני). לוודא צורת endpoint מול הספק לפני שימוש. |
| https://www.allpay.co.il/en/help/bit | מגבלות ארנק Bit: 5,000 ש"ח לעסקה, אין תשלומים, תשלום אחד בלבד, חלון 10 דקות ללקוח. |

## מלכודות נפוצות

- **`ActionType` שגוי משנה בשקט אם הכסף זז.** `J2` הוא לרישום כרטיס בלבד ולא מחייב, אבל ממשק הסוחר נראה זהה ל-`J4`. ברירת מחדל ל-`J4` אלא אם רוצים אימות בלבד. ה-changelog של פלאגין 1.4.7 מציין במפורש: "Bypass validation for J2 transactions."
- **פלאקארד לא חותמת את ה-IPN ב-HMAC.** ההגנות היחידות מול callback מזויף הן: (א) לאמת כל callback דרך `PaymentGW/GetTransaction` שרת-לשרת, (ב) אם רוצים, להגביל את `ServerSideGoodFeedbackURL` / `ServerSideErrorFeedbackURL` ל-IP allowlist יוצא של פלאקארד (כדאי לבקש את הרשימה העדכנית מהתמיכה), (ג) לאכוף TLS 1.2+ על ה-endpoints האלה. אסור לסמוך על payload עם `ConfirmationKey` שמוכר לכם בלי לאמת את העסקה מחדש בשרת.
- **משווים `DebitTotal`, לא `Total`, בתגובת GetTransaction.** הסכום האמין שחויב בתגובה הוא `DebitTotal` (לפי שדות class `PelecardTransaction` ב-dofinity). `Total` הוא הד של הבקשה; `DebitTotal` הוא מה שזז בפועל.
- **`PelecardTransactionId` הוא מפתח dedupe ל-IPN, לא `ParamX`.** פלאקארד עלולה למסור את אותו IPN פעמיים על אותה הזמנה (retry של timeout). `ParamX` הוא מזהה קורלציה של בית העסק להזמנה ויכול להיות זהה בשני המסירות; `PelecardTransactionId` ייחודי לכל ניסיון. תסמנו כל `PelecardTransactionId` כ"טופל" ב-DB.
- **כלל "אין תשלומים" ב-Bit הוא מוחלט, התקרה של 5,000 ₪ נקבעת לפי דירוג.** מ-allpay.co.il: "No installments. You can only pay with Bit in one payment." 5,000 ₪ לעסקה הוא הערך הנפוץ ("Payment via Bit cannot exceed 5,000 shekels") ותקרת תכנון בטוחה, אבל בתי עסק בדירוג גבוה יותר מאושרים מעליה. תסתירו את בורר התשלומים ותגבילו את אפשרות ה-Bit לפי התקרה שמופיעה בהסכם שלכם. Bit גם דוחה לא-ILS, תשלחו `Currency: 1`.
- **החלפת host בין sandbox לפרודקשן.** `gateway20.pelecard.biz/sandbox` הוא sandbox, `gateway21.pelecard.biz` הוא פרודקשן. לכל סביבה פרטי גישה משלה. ההגדרה צריכה לבוא ממשתנה סביבה ב-deploy, לא מקבוע בקוד. אחרת deploy לפרודקשן יפנה ל-sandbox או להפך.
- **מסופי sandbox מוקצים לפי בקשה.** הרבה בתי עסק ישראלים בסוף "בודקים" מול פרודקשן עם חיוב חי של 1 ₪ כי שכחו לבקש מסוף sandbox מהתמיכה. תכתבו ל-`support@pelecard.co.il` ותבקשו sandbox לפני האינטגרציה; אסור להחזיק פרטי פרודקשן ב-`.env.local` משותף עם צוות הפיתוח.
- **`terminal` + `user` + `password` הם server-side בלבד.** דליפה של השלשה פותחת את המסוף לכל אחד. dofinity מצהירה עליהם כ-`protected` ושולחת אותם רק מקוד שרת. אף פעם לא ב-JS של דפדפן, לא בחבילה של אפליקציה ניידת ולא ב-build artifacts.
- **שדות סכום ביחידות מינור (אגורות) ב-Gateway21.** שולחים `Total: 9900` עבור 99.00 ₪ ו-`FirstPayment: 5000` עבור 50.00 ₪. ה-wrapper של dofinity מתעד את `FirstPayment` כ-"in agorot/cents", ואותה קונבנציה תקפה ל-`Total`. תוודאו מול ה-sandbox עם חיוב מבחן של 1 ₪ לפני עלייה לאוויר.

## פתרון בעיות

### שגיאה: ה-callback הגיע אבל `PaymentGW/GetTransaction` מחזיר "transaction not found"
סיבה: שאילתה ל-endpoint של פרודקשן עם פרטי גישה של sandbox, או הפוך. לכל סביבה ספר עסקאות נפרד.
פתרון: להתאים host לפרטי גישה. `gateway20.pelecard.biz/sandbox` רק עם פרטי sandbox, ו-`gateway21.pelecard.biz` רק עם פרטי פרודקשן.

### שגיאה: `ConfirmationKey` חסר ב-callback
סיבה: או שהלקוח נטש באמצע (סגר את הדפדפן לפני שה-iframe סיים), או שהבקשה שובשה.
פתרון: לראות את ההזמנה כלא משולמת. `ServerSideGoodFeedbackURL` של פלאקארד הוא מקור האמת לתשלומים שהושלמו. אם `ConfirmationKey` חסר, אסור לסמן את ההזמנה כשולמה גם אם `PelecardStatusCode` נראה הצלחה.

### שגיאה: תשלום Bit נכשל בסכומים מעל 5,000 ₪
סיבה: התקרה של Bit לעסקה נקבעת בהסכם בית העסק עם Bit ובדירוג הסיכון של מפעיל הארנק; 5,000 ₪ הוא הערך הנפוץ. בתי עסק בדירוג גבוה יותר מאושרים מעל זה.
פתרון: תכננו עם תקרה של 5,000 ₪ אלא אם יש אישור בכתב אחרת. תגבילו את אפשרות ה-Bit ב-checkout לפי התקרה שמופיעה בהסכם שלכם. תציגו הודעה ברורה "Bit מוגבל ל-<התקרה שלכם>" ותציעו אשראי כחלופה. תוודאו גם `Currency: 1` (Bit דוחה לא-ILS).

### שגיאה: challenge של 3DS מופיע ב-sandbox אבל העסקה נדחית
סיבה: challenge 3DS ב-sandbox דורש כרטיסי בדיקה ספציפיים ותשובות challenge שמוגדרות לפי המסוף.
פתרון: לוודא עם תמיכת פלאקארד אילו מספרי כרטיסי בדיקה וקודי challenge עובדים מול המסוף שלכם ב-sandbox. הבוררים `Initiate` ו-`AskForChallenge` בממשק ה-sandbox שולטים האם 3DS נכנס בכלל.

### שגיאה: חיוב טוקן הצליח אבל הלקוח טוען שלא היה תשלום
סיבה: השתמשו ב-J5 (אישור) במקום J4 (מכירה), וה-capture אף פעם לא הופעל.
פתרון: לוודא את שדה `ActionType` של העסקה המקורית דרך `PaymentGW/GetTransaction`. אם זה היה `J5` או `J5h`, להריץ את זרימת ה-capture התואמת (או לבטל את ה-auth). ברירת מחדל `J4` למכירות חד-פעמיות.
