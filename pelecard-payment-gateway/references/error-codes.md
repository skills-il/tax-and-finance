# Pelecard Error Codes

Pelecard returns a numeric status code on every transaction: `PelecardStatusCode` on the iframe
callback, `StatusCode` on a `PaymentGW/GetTransaction` response, and `Error.ErrCode` on a failed
`PaymentGW/init`. `000` is success; anything else is an error.

## Resolve any code at runtime (no credentials needed)

Pelecard publishes the official bilingual message for every code through two credential-free
service endpoints. Do NOT hard-code a hand-written mapping and do NOT tell users to email support:
call these.

```
POST https://gateway21.pelecard.biz/services/GetErrorMessageEn
POST https://gateway21.pelecard.biz/services/GetErrorMessageHe
Content-Type: application/json

{"ErrorCode": "033"}
```

Response is the bare message string, e.g. `invalid credit card.` / `כרטיס לא תקין.`

Because `GetErrorMessageHe` needs no terminal, user or password, wire it straight into your IPN
failure path to render a Hebrew decline message to the customer. That is the single highest-value
use of this endpoint on an Israeli checkout.

Cache the lookups. The table is stable, and one call per failed transaction is wasteful.

## Full table

Enumerated by sweeping codes `000`-`999` against `GetErrorMessageEn` and `GetErrorMessageHe` on
2026-08-27. Of 1000 probed codes, 254 return a real message; the remainder return `UnkownError`
(Pelecard's spelling) and are unassigned. The table below is complete for the assigned codes.

| Code | English (Pelecard) | Hebrew (Pelecard) |
|------|--------------------|-------------------|
| `000` | operation success | עסקה תקינה. |
| `001` | blocked - retain card. | כרטיס חסום. |
| `002` | stolen - retain card. | כרטיס גנוב. |
| `003` | contact credit card company. | התקשר לחברת האשראי. |
| `004` | transaction refused. | סירוב. |
| `005` | forged - retain card. | מזויף החרם כרטיס. |
| `006` | Invalid ID or CVV. | ת.ז. או CVV שגויים. |
| `007` | must contact credit card company. | קוד אישור אינו חוקי - נא לפנות למנהל המערכת. |
| `008` | error in access key to black list. | תקלה בבניית מפתח גישה לקובץ חסומים. |
| `009` | did not succeed to communicate. | תקלת תקשורת, יש לנסות שוב או לפנות למנהל המערכת ולמסור את קוד התשובה. |
| `010` | operation canceled by user | פעולה הופסקה ע''י משתמש |
| `011` | No Approoval From The Clearing Company For This ISO Currency. | אין לסולק הרשאה לבצע עסקאות מטבע חוץ. |
| `012` | This ISO Currency is not Allowed for This Credit Card. | אין אישור למותג במטבע ISO. |
| `019` | input file has less than 16 characters. | רשומה בקובץ Int_in קצרה מ-16 תווים |
| `020` | input file missing. | קובץ קלט (Int_in) לא קיים. |
| `021` | black list(NEG) is missing. | קובץ חסומים (NEG) לא קיים או לא מעודכן – בצע שידור או בקשה לאישור עבור כל עסקה. |
| `022` | parameter file is missing. | אחד מקבצי פרמטרים או ווקטורים לא קיים. |
| `023` | DATA file missing. | קובץ תאריכים (DATA) לא קיים. |
| `024` | START file missing. | קובץ אתחול (START) לא קיים. |
| `025` | black list is too old. | הפרש בימים בקליטת חסומים גדול מדי - בצע שידור או בקשה לאישור עבור כל עסקה. |
| `026` | generation gap in black list too large. | הפרש דורות בקליטת חסומים גדול מידי - בצע שידור או בקשה לאישור עבור כל עסקה. |
| `027` | partial reading of magnetic strip or This must be phone transaction. | לא הוכנס פס מגנטי כולו. הגדר עסקה כעסקה טלפונית או כעסקת חתימה בלבד. |
| `028` | no central terminal number for merchant collecting on behalf of others. | מספר מסוף מרכזי לא הוכנס לשאילתה במסוף המוגדר לעבודה כרב ספק. |
| `029` | no payee number for merchant collecting on behalf of others. | מספר מוטב לא הוכנס למסוף המוגדר לעבודה כרב מוטב. |
| `030` | central terminal number or payee number for merchant collecting on behalf of others. | מסוף שאינו מעודכן כרב ספק/רב מוטב והוקלד מספר ספק/מספר מוטב. |
| `031` | payee number for merchant collecting on behalf of others. | מסוף מעודכן כרב ספק והוקלד גם מספר מוטב. |
| `032` | old transactions file. | תנועות ישנות. בצע שידור או בקשה לאישור עבור כל עסקה. |
| `033` | invalid credit card. | כרטיס לא תקין. |
| `034` | this card not authorised for this terminal. | כרטיס לא רשאי לבצע במסוף זה או אין אישור לעסקה כזאת. |
| `035` | the type of credit not allowed for this card. | כרטיס לא רשאי לבצע עסקה עם סוג אשראי זה. |
| `036` | card is expired. | כרטיס פג תוקף. |
| `037` | error in payment formula. | שגיאה בתשלומים - סכום עסקה צריך להיות שווה תשלום ראשון +(תשלום קבוע כפול מספר תשלומים). |
| `038` | immediate debit disallowed, for this card. | לא ניתן לבצע עסקה מעל תקרה לכרטיס לאשראי חיוב מיידי. |
| `039` | invalid credit card. | ספרת בקורת לא תקינה. |
| `040` | supplier number for  merchant collecting on behalf of others. | מסוף שמוגדר כרב מוטב הוקלד מספר ספק. |
| `041` | above credit ceiling for authorisation request J1, J2 or J3. | מעל תקרה כאשר רשומת הקלט מכילה J3 או J2 או J1 (אסור להתקשר). |
| `042` | card blocked for supplier for authorisation request J1, J2 or J3. | כרטיס חסום בספק כאשר רשומת הקלט מכילה J3 או J2 או J1 (אסור להתקשר). |
| `043` | random call for authorisation request J1. | אקראית כאשר רשומת הקלט מכילה  J1  (אסור להתקשר). |
| `044` | terminal may not request authorisation without transaction (J5). | מסוף לא רשאי לבקש אישור ללא עסקה (J5). |
| `045` | terminal may not force an authorisation (J6). | מסוף לא רשאי לבקש אישור ביוזמת קמעונאי (J6). |
| `046` | termianl has to request authorisation for J1, J2 or J3. | מסוף חייב לבקש אישור כאשר רשומת הקלט מכילה J3 או J2 או J1 (אסור להתקשר). |
| `047` | PIN code essential for J1, J2 or J3. | חייב להקליד מספר סודי כאשר רשומת הקלט מכילה J3 או J2 או J1 (אסור להתקשר). |
| `051` | bad vehicle number. | מספר רכב לא תקין. |
| `052` | odometer not keyed in. | מד מרחק  לא הוקלד. |
| `053` | terminal does not belong to petrol station. | מסוף לא מוגדר כתחנת דלק. (הועבר כרטיס דלק או קוד עסקה לא מתאים). |
| `057` | No Id Supplied. | לא הוקלד מספר תעודת הזהות. |
| `058` | CVV2 is invalid / missing. | הCVV שגוי או לא הוקלד. |
| `059` | No CVV2 Supplied or No Id Supplied - Both Are Requiered. | לא הוקלד מספר תעודת הזהות ו- CVV. |
| `060` | the string 'ABS' missing from data in memory. | צרוף ABS לא נמצא בהתחלת נתוני קלט בזיכרון |
| `061` | card number not found, or found twice. | מספר כרטיס לא נמצא או נמצא פעמיים. |
| `062` | transaction request type invalid. | סוג עסקה לא תקין. |
| `063` | transaction type invalid. | קוד עסקה לא תקין. |
| `064` | credit type invalid. | סוג אשראי לא תקין. |
| `065` | currency invalid. | מטבע לא תקין. |
| `066` | installment payments stated for credit type without installments. | קיים תשלום ראשון ו/או תשלום קבוע לסוג אשראי שונה מתשלומים. |
| `067` | number of installments stated for credit type without installments. | קיים מספר תשלומים לסוג אשראי שאינו דורש זה. |
| `068` | dollar or index linking not allowed without installments. | לא ניתן להצמיד לדולר או למדד לסוג אשראי שונה מתשלומים. |
| `069` | magnetic strip too short. | אורך הפס המגנטי קצר מידי. |
| `071` | payee faulty. | חובה להקליד מספר סודי. |
| `072` | PIN number not given. | קכ"ח (קורא כרטיסים חכם) לא זמין - העבר בקורא מגנטי. |
| `073` | PIN number faulty. | חובה להעביר כרטיס בקכ"ח (קורא כרטיסים חכם). |
| `074` | PIN number faulty - last chance. | דחייה - כרטיס נעול. |
| `075` | Time Out | דחייה - פעולה עם קכ"ח לא הסתיימה בזמן הראוי. |
| `080` | membership club given for inappropriate credit type. | הוכנס "קוד מועדון" לסוג אשראי לא מתאים. |
| `099` | access to TRAN file failed. | לא מצליח לקרוא/ לכתוב/ לפתוח  קובץ TRAN. |
| `100` | no equipment to input PIN number. | אין ציוד להכנסת מספר PIN. |
| `101` | credit card company disallows terminal operation. | אין אישור מחברת אשראי לעבודה. |
| `106` | terminal not allowed to query immediate debit transaction. | למסוף אין אישור לביצוע שאילתא לאשראי חיוב מיידי. |
| `107` | sum of transaction too large. | סכום העסקה גדול מידי - חלק במספר העסקאות. |
| `108` | terminal not allowed to force authorisation. | למסוף אין אישור לבצע עסקאות מאולצות. |
| `109` | terminal not allowed to accept card with service code 587. | למסוף אין אישור לכרטיס עם קוד השרות 587. |
| `110` | terminal not allowed to accept card with immediate debit. | למסוף אין אישור לכרטיס חיוב מיידי. |
| `111` | terminal not allowed to accept transaction with payments. | למסוף אין אישור לעסקה בתשלומים. |
| `112` | terminal not allowed to accept phone transaction. | למסוף אין אישור לעסקה טלפון/ חתימה בלבד תשלומים. |
| `113` | terminal not allowed to accept telephone. | למסוף אין אישור לעסקה טלפונית. |
| `114` | terminal not allowed to accept signature only transaction. | למסוף אין אישור לעסקה 'חתימה בלבד'. |
| `115` | terminal not allowed to accept dollar transaction. | למסוף אין אישור לעסקאות במטבע זר או עסקה לא מאושרת. |
| `116` | terminal not allowed to accept membership club transaction. | למסוף אין אישור לעסקת מועדון. |
| `117` | terminal not allowed to accept bonus points transaction. | למסוף אין אישור לעסקת כוכבים/נקודות/מיילים. |
| `118` | terminal not allowed to accept Isracredit transaction. | למסוף אין אישור לאשראי ישראקרדיט. |
| `119` | terminal not allowed to accept Amexcredit transaction. | למסוף אין אישור לאשראי אמקס  קרדיט. |
| `120` | terminal not allowed to accept dollar linked transaction. | למסוף אין אישור להצמדה לדולר. |
| `121` | terminal not allowed to accept index linked transaction. | למסוף אין אישור להצמדה למדד. |
| `122` | terminal not allowed to accept index linked transaction for foreign cards. | למסוף אין אישור להצמדה למדד לכרטיסי חו"ל. |
| `123` | terminal not allowed to accept bonus points transaction for this type of credit. | למסוף אין אישור לעסקת כוכבים/נקודות/מיילים לסוג אשראי זה. |
| `124` | terminal not allowed to accept Isra/36 transaction. | למסוף אין אישור לאשראי ישרא 36. |
| `125` | terminal not allowed to accept Imex/36 transaction. | למסוף אין אישור לאשראי אמקס 36. |
| `126` | terminal not allowed to accept this membership club code. | למסוף אין אישור לקוד מועדון זה. |
| `127` | terminal not allowed to execute immedaite debit transaction, except for immediate debit cards. | למסוף אין אישור לעסקת חיוב מיידי פרט לכרטיסי חיוב מיידי. |
| `128` | terminal not allowed to accept Visa cards starting with 3. | למסוף אין אישור לקבל כרטיסי ויזה אשר מתחילים ב – 3. |
| `129` | terminal not allowed to execute credit transaction above ceiling. | למסוף אין אישור לבצע עסקת זכות מעל תקרה. |
| `130` | card not allowed to execute membership club transaction. | כרטיס  לא רשאי לבצע עסקת מועדון. |
| `131` | card not allowed to execute bonus points transaction. | כרטיס לא רשאי לבצע עסקת כוכבים, נקודות או מיילים. |
| `132` | card not allowed to execute dollar transaction (regular or telelphone). | כרטיס לא רשאי לבצע עסקאות בדולרים (רגילות או טלפוניות). |
| `133` | card not valid according to Isracard list. | כרטיס לא תקף על פי רשימת כרטיסים תקפים של ישראכרט. |
| `134` | card not valid according to terminal parameters - wrong number of digit. | כרטיס לא תקין עפ”י הגדרת המערכת (VECTOR1 של ישראכרט)- מספר הספרות בכרטיס- שגוי. |
| `135` | card not allowed to execute dollar transaction according to terminal parameters (Isracard). | כרטיס לא רשאי לבצע עסקאות דולריות עפ”י הגדרת המערכת (VECTOR1 של ישראכרט) |
| `136` | card in group not allowed to transactions according to terminal parameters (Visa). | הכרטיס שייך לקבוצת כרטיסים אשר אינה רשאית לבצע עסקאות עפ”י הגדרת המערכת (VECTOR20של ויזה). |
| `137` | first 7 digits of card not valid according to terminal parameters (Diners). | קידומת הכרטיס (7 ספרות) לא תקפה עפ”י הגדרת המערכת (21VECTORשל דיינרס) |
| `138` | card not allowed to execute payments according to Isracard list. | כרטיס לא רשאי לבצע עסקאות בתשלומים על פי רשימת כרטיסים תקפים של ישראכרט. |
| `139` | too many payments according to Isracard list. | מספר תשלומים גדול מידי על פי רשימת כרטיסים תקפים של ישראכרט. |
| `140` | Visa and Diners not allowed to execute membership transaction with payments. | כרטיסי ויזה ודיינרס לא רשאים לבצע עסקאות מועדון בתשלומים. |
| `141` | series of cards not valid according to terminal parameters. | סידרת כרטיסים לא תקפה עפ”י הגדרת המערכת. (VECTOR5של ישראכרט) |
| `142` | service code not valid according to terminal parameters (Isracard). | קוד שרות לא תקף עפ”י הגדרת המערכת (VECTOR6של ישראכרט) |
| `143` | first two digits not valid according to terminal parameters (Isracard). | קידומת הכרטיס (2 ספרות) לא תקפה עפ”י הגדרת המערכת. (VECTOR7 של ישראכרט) |
| `144` | service code not valid according to terminal parameters (Visa). | קוד שרות לא תקף עפ”י הגדרת המערכת. (VECTOR12של ויזה) |
| `145` | service code not valid according to terminal parameters (Visa parameter vector 12). | קוד שרות לא תקף עפ”י הגדרת המערכת. (VECTOR13של ויזה) |
| `146` | immediate debit card not allowed to execute credit transaction. | לכרטיס חיוב מיידי אסור לבצע עסקת זכות. |
| `147` | card not allowed to execute payments according to Alpha vector. | כרטיס לא רשאי לבצע עסקאות בתשלומים עפ"י וקטור 31  של לאומיקארד. |
| `148` | card not allowed to execute telephone or signature only transaction (Alpha parameter vector 31). | כרטיס לא רשאי לבצע עסקאות טלפוניות וחתימה בלבד עפ"י ווקטור 31 של לאומיקארד. |
| `149` | card not allowed to execute telephone (Alpha parameter vector 31). | כרטיס אינו רשאי לבצע עסקאות טלפוניות עפ"י  וקטור 31 של לאומיקארד. |
| `150` | credit not allowed for immediate debit card. | אשראי לא מאושר לכרטיסי חיוב מיידי. |
| `151` | credit not allowed for foreign card. | אשראי לא מאושר לכרטיסי חו"ל. |
| `152` | membership club code not valid. | קוד מועדון לא תקין |
| `153` | card not allowed to execute flexible payments (Diners parameter vector 12). | כרטיס לא רשאי לבצע עסקת אשראי גמיש (עדיף +30/) עפ"י הגדרת המערכת. (21VECTORשל דיינרס) |
| `154` | card not allowed to execute immediate debit (Diners parameter vector 21). | כרטיס לא רשאי לבצע עסקאות חיוב מיידי עפ"י הגדרת המערכת. (VECTOR21של דיינרס) |
| `155` | sum of transaction too small for credit type. | סכום לתשלום בעסקת קרדיט קטן מידי. |
| `156` | number of payments too small for credit type. | מספר תשלומים לעסקת קרדיט לא תקין. |
| `157` | this type of card has zero ceiling for deferred payments. | תקרה 0 לסוג כרטיס זה בעסקה עם אשראי רגיל או קרדיט. |
| `158` | this type of card has zero ceiling for immediate payment. | תקרה 0 לסוג כרטיס זה בעסקה עם אשראי חיוב מיידי. |
| `159` | this type of card has zero ceiling for immediate payment in dollars. | תקרה 0 לסוג כרטיס זה  בעסקת חיוב מיידי בדולרים. |
| `160` | this type of card has zero ceiling for telephone transactions. | תקרה 0 לסוג כרטיס זה בעסקה טלפונית. |
| `161` | this type of card has zero ceiling for credit transactions. | תקרה 0 לסוג כרטיס זה בעסקת זכות. |
| `162` | this type of card has zero ceiling for deferred payments. | תקרה 0 לסוג כרטיס זה בעסקת תשלומים. |
| `163` | Amex issued out of Israel cannot execute deferred payments. | כרטיס אמריקן אקספרס אשר הונפק בחו"ל לא רשאי לבצע עסקאות בתשלומים. |
| `164` | JCB can defer payments only via regular credit. | כרטיסיJCB  רשאי לבצע עסקאות רק באשראי רגיל. |
| `165` | bonus point payment exceeds sum of transaction | סכום בכוכבים, נקודות או מיילים גדול מסכום העסקה. |
| `166` | club card not in terminal's jurisdiction. | כרטיס מועדון לא בתחום של המסוף. |
| `167` | bonus point payment transaction not allowed in dollars. | לא ניתן לבצע עסקת כוכבים/נקודות/מיילים בדולרים. |
| `168` | terminal not allowed to accept dollar transaction with this sort of deferred payments. | למסוף אין אישור לעסקה דולרית עם סוג אשראי זה. |
| `169` | credit transaction cannot be executed with credit different from usual. | לא ניתן לבצע עסקת זכות עם אשראי שונה מ-רגיל. |
| `170` | bonus point deduction above allowable limit. | סכום הנחה בכוכבים/נקודות/מיילים גדול מהמותר. |
| `171` | forced authorisation not allowed for this credit card type. | לא ניתן לבצע עסקה מאולצת לכרטיס/אשראי חיוב מיידי. |
| `172` | previous tranaction cannot be cancelled, sum credited or card number do not match. | לא ניתן לבטל עסקה קודמת (עסקת זכות או מספר כרטיס אינו זהה). |
| `173` | double transaction. | עסקה כפולה. |
| `174` | terminal not allowed to accept index linked transaction for this payment scheme. | למסוף אין אישור להצמדה למדד לאשראי זה. |
| `175` | terminal not allowed to accept dollar linked transaction for this payment scheme. | למסוף אין אישור להצמדה לדולר לאשראי זה. |
| `176` | card not valid according to terminal parameters. | כרטיס אינו תקף על-פי הגדרת המערכת - וקטור 1 של ישראכרט. |
| `177` | filling stations cannot execute 'self service', only 'self service at filling station'. | בתחנות דלק לא ניתן לבצע 'שרות עצמי' אלא 'שרות עצמי בתחנות דלק'. |
| `178` | credit transaction not allowed with bonus points. | אסור לבצע עסקת זכות בכוכבים, נקודות או מיילים. |
| `179` | dollar credit transaction not allowed with tourist card. | אסור לבצע עסקת זכות בדולר בכרטיס תייר. |
| `180` | club card cannot execute phone transaction. | בכרטיס מועדון לא ניתן לבצע עסקה טלפונית. |
| `200` | computer application error. | שגיאה יישומית. |
| `205` | Bad total. | סכום העסקה חסר או אפס. |
| `226` | Transaction canceled succesfully. | העסקה בוטלה בהצלחה. |
| `227` | Cancellation declined. | ביטול העסקה נדחה. |
| `301` | Session to Pelecard Timed Out | פג תוקף החיבור למערכת |
| `302` | Debit was successful but merchant is not responding | התשלום בוצע אך אתר העסק לא זמין |
| `303` | Merchant is not responding | אתר העסק לא זמין |
| `306` | did not succeed to communicate. | אין תקשורת לפלאקארד. |
| `308` | Duplicated transaction. | עסקה כפולה. |
| `401` | Number of payments is greater than the maximum number of payments | שגיאה לא ידועה |
| `402` | Number of payments is smaller than a minimum number of payments | שגיאה לא ידועה |
| `403` | Transaction amount is smaller than the minimum amount | שגיאה לא ידועה |
| `404` | Terminal number does not exist. | מספר מסוף לא קיים. |
| `418` | Necessary values are missing/wrong. | שגיאה לא ידועה |
| `425` | Double entry | רשומה כפולה. |
| `447` | Invalid credit card | שגיאה לא ידועה |
| `500` | Terminal executes broadcast and/or updating data. Please try again later. | מסוף מבצע שידור ו/או מעדכן נתונים. אנא נסה שנית מאוחר יותר. |
| `501` | User name and/or password not correct. Please call support team. | שם משתמש ו/או סיסמה לא נכונים. אנא פנה למחלקת תמיכה. |
| `502` | User password has expired. Please contact support team. | פג תוקף סיסמת משתמש. אנא פנה למחלקת תמיכה. |
| `503` | Locked user. Please contact support team. | משתמש נעול. אנא פנה למחלקת תמיכה. |
| `505` | Blocked terminal. Please contact account team. | מסוף חסום. אנא פנה להנהלת חשבונות. |
| `506` | Token number abnormal. | מספר טוקן לא תקין. |
| `507` | User is not authorized in this terminal. | משתמש לא רשאי לבצע פעולות במסוף זה. |
| `508` | Expiration date structure invalid. Use MMYY structure only. | מבנה תוקף לא תקין. יש להשתמש במבנה MMYY  בלבד. |
| `509` | SSL certificate confirmation error. Please contact the support team | גישה לאימות תעודת אבטחה חסומה. אנא פנה למחלקת התמיכה. |
| `510` | Data does not exist | לא קיימים נתונים. |
| `511` | Waiting for client authorization | אישור חלקי - יש לאשר את העסקה ב SMS ולנסות שנית. |
| `512` | Time out on pinpad | טיים אאוט |
| `513` | Try inserting card into smart reader | נסה להכניס כרטיס לקורא החכם |
| `514` | Smart reader mode not available | אין מצב הכנסת כרטיס |
| `515` | System not ready | המערכת לא מוכנה |
| `516` | Invalid PINPAD ID | מזהה קורא הכרטיס לא תקין |
| `517` | PINPAD not ready | קורא הכרטיס לא מוכן |
| `518` | PINPAD fault | תקלה בקורא הכרטיס |
| `550` | Pinpad not found | מכשיר PinPad לא נמצא |
| `551` | PINPAD busy | שגיאה לא ידועה |
| `552` | PINPAD ready | שגיאה לא ידועה |
| `553` | Transaction in process | שגיאה לא ידועה |
| `555` | Operation was Canceled | הלקוח לחץ על ביטול בדף התשלום. |
| `596` | Clearing service is not available. Please try again later | שירות הסליקה אינו זמין. נסה שוב מאוחר יותר. |
| `597` | General error. contact Please support team. | שגיאה כללית. אנא פנה למחלקת התמיכה. |
| `598` | Necessary values are missing/wrong. | ערכים נחוצים חסרים או שגויים. |
| `599` | General error. Please check transaction status manually. | שגיאה כללית. בדוק האם העסקה עברה ונסה שנית. |
| `620` | This card cannot be used for this transaction. | שגיאה לא ידועה |
| `650` | 3DS process failed | אימות 3ds נכשל |
| `655` | Bank Transfer Failed | העברה בנקאית נכשלה |
| `660` | ACCC - Settlement on the creditor account has been completed. | ACCC - הסתיימה ההעברה בהצלחה ושינויים לא אפשריים |
| `661` | ACSC - Settlement on the debtor’s account has been completed. | ACSC - הסתיימה ההעברה בהצלחה והכסף יצא מחשבון המעביר |
| `662` | ACSP - All preceding checks such as technical validation and customer profile were successful | ACSP - פעולת הייזום בוצעה בהצלחה טכנית |
| `663` | ACTC - Authentication and syntactical and semantical validation are successful. | ACTC - פעולת הייזום בוצעה בהצלחה טכנית |
| `664` | ACWC - Instruction is accepted but a change will be made, such as date or remittance not sent. | AACWC - אושרה ההעברה טכנית אך עלולה לכלול שינויים |
| `665` | RCVD - Payment initiation has been received by the receiving agent. | RCVD - הוקמה הפעולה לתשלום בבנק - סטטוס ביניים |
| `666` | RJCT - rejected - lack of coverage, transaction expired, or bank rejected. | RJCT - התשלום נדחה בבנק |
| `667` | PATC - The payment initiation needs multiple authentications | PATC - העברה מחכה לחתימת מורשים נוספים |
| `668` | PENDING | PENDING - העברה ממתינה לאישורים נוספים |
| `669` | ERROR - Failure in the process | EERROR - אירעה שגיאה |
| `670` | CAPTCHA fail | שגיאה לא ידועה |
| `671` | ACFC - Pre-ceeding check of technical validation and customer profile was successful | ACFC - אושרה ההעברה טכנית ונעשתה בדיקה שיש מספיק יתרה |
| `672` | CANC - Payment initiation has been cancelled before execution | CANC - התשלום בוטל |
| `680` | INIT - The payment has been created but not yet completed by the user. | INIT - סטטוס ראשוני - הוקמה הפעולה |
| `700` | Transaction rejected by PINPAD | עסקה נדחתה ע``י מכשיר PinPad |
| `701` | Error in PINPAD | שגיאה במכשיר pinpad |
| `702` | COM port is invalid | יציאת com לא תקינה |
| `703` | Transaction failed | עסקה נכשלה |
| `704` | Transaction canceled | עסקה בוטלה |
| `705` | Transaction canceled by user | שגיאה לא ידועה |
| `706` | Waiting time too long | זמן המתנה ארוך מדי |
| `707` | Card was removed before transaction finished | משתמש הוציא כרטיס לפני סיום ביצוע העסקה |
| `708` | PINPAD User Retries Exceeded | PINPAD  User Retries Exceeded |
| `709` | PINPAD Timeout | PINPAD Timeout |
| `710` | Bad request | בקשה שגויה |
| `711` | PINPAD Message Error | PINPAD Message Error |
| `712` | PINPAD Not Initialized | PINPAD Not Initialized |
| `713` | PINPAD Card Read Error | PINPAD Card Read Error |
| `714` | PINPAD Reader Timeout | PINPAD Reader Timeout |
| `715` | PINPAD Reader Comms Error | PINPAD Reader Comms Error |
| `716` | PINPAD Reader Message Error | PINPAD Reader Message Error |
| `717` | PINPAD Host Message Error | PINPAD Host Message Error |
| `718` | PINPAD Host Config Error | PINPAD Host Config Error |
| `719` | PINPAD Host Key Error | PINPAD Host Key Error |
| `720` | PINPAD Host Connect Error | PINPAD Host Connect Error |
| `721` | PINPAD Host Transmit Error | PINPAD Host Transmit Error |
| `722` | PINPAD Host Receive Error | PINPAD Host Receive Error |
| `723` | PINPAD Host Timeout | PINPAD Host Timeout |
| `724` | PIN Verification Not Supported By Card | PIN Verification Not Supported By Card |
| `725` | PIN Verification Failed | PIN Verification Failed |
| `726` | Error loading config.xml | שגיאה בקליטת קובץ config.xml |
| `730` | PINPAD approved the transaction despite ashrait refusal | מכשיר אישר עסקה בניגוד להחלטת אשראית |
| `731` | Card not inserted | כרטיס לא הוכנס |
| `760` | Did not succeed to communicate | שגיאה לא ידועה |
| `800` | PayPal Error. | שגיאה של PayPal. |
| `801` | Not Upay User | עמדת סליקה לא יופיי |
| `802` | Error In Payment Details For Upay | פרטי תשלום של יופיי שגויים |
| `803` | Credit Type Not Supported | סוג אשראי לא נתמך |
| `804` | Transaction Type Not Supported | סוג עסקה לא נתמך |
| `805` | Missing Necessary Upay User Info | חסר מידע משתמש יופיי |
| `806` | No tJ4 Transaction | סוג טרנזקציה לא נתמכך |
| `807` | Credit card not supported | סוג כרטיס לא נתמך |
| `809` | Billing Terminal Does Not Exist | שגיאה לא ידועה |
| `810` | Not Upay Terminal | מסוף לא מוגדר ביופיי |
| `811` | Total Per Action Too Small | שגיאה לא ידועה |
| `812` | Method not allowed | שגיאה לא ידועה |
| `813` | invalid credit card. | שגיאה לא ידועה |
| `888` | UpaySeccess | הצלחה |
| `890` | ApplePay Error | שגיאה לא ידועה |
| `891` | GooglePay Error | שגיאה לא ידועה |
| `899` | Upay General Failure | שגיאה כללית ביופיי |
| `901` | Error In Payment Details For SplitIt | שגיאה לא ידועה |
| `902` | Payments Number Must Be More Than One for SplitIt | שגיאה לא ידועה |
| `903` | Not Tourist Credit Card Does Not Match for Split It | שגיאה לא ידועה |
| `904` | No data found | לא נמצאו נתונים. |
| `999` | Necessary values are missing to complete installments transaction. | ערכים נחוצים חסרים לעסקת תשלומים. |
## How to act on a code

The table gives the meaning; it does not give you a retry policy. Group the codes yourself:

- **Retain-card / fraud** (`001`, `002`, `005`) -- do not retry, do not offer the same card again.
- **Hard decline** (`004`, `033`, `036`, `039`, `034`, `035`) -- ask for a different card. Retrying
  a hard decline damages your acquirer trust score.
- **Issuer-contact** (`003`, `007`) -- the customer must call their issuer. Retrying will not help.
- **Terminal / configuration** (`101`, `404`, `500`, `503`, `505`, `507`) -- your problem, not the
  customer's. Alert your team; the checkout is broken for everyone, not just this card.
- **Credential** (`501`, `502`) -- wrong or expired API password. `502` in particular is a
  time-bomb: Pelecard user passwords expire, and the failure looks like a total outage.
- **Installments** (`401`, `402`, `403`, `999`) -- your `MaxPayments`/`MinPayments` window and the
  transaction amount disagree. Validate client-side before you post.
- **Duplicate** (`308` "Duplicated transaction.", `425` "Double entry") -- Pelecard rejected a
  repeat. Treat this as evidence your outbound retry logic fired twice; look the original
  transaction up rather than charging again.
- **Merchant-unreachable** (`301`, `302`, `303`) -- these are the codes behind the "customer says
  they paid, my DB is empty" ticket, and they do **not** mean the same thing. Only `302` ("Debit was
  successful but merchant is not responding") states that the debit succeeded. `301` ("Session to
  Pelecard Timed Out") most likely means no debit happened at all, and `303` ("Merchant is not
  responding") says nothing either way. Treat `301` and `303` as **outcome unknown** and resolve them
  before touching the order. In every case reconcile by `paramX` via `/services/TrxLookUp` or
  `/services/CheckGoodParamX`; never charge again to find out.
- **3DS** (`650` "3DS process failed", `620`) -- see the 3DS section in SKILL.md.
- **Token** (`506` "Token number abnormal.") -- the stored token is no longer chargeable. Re-tokenize
  via `/services/ConvertToToken` or refresh with `/services/UpdateToken`.
- **PINPAD / physical terminal** (`5xx` block `512`-`518`, `550`-`555`, `700`-`703`) -- present-card
  hardware. An e-commerce integration should never see these; if you do, your terminal is
  provisioned for the wrong transaction type.
- **Bank transfer / open banking** (`660`-`680`) -- ISO 20022 status words (`ACCC`, `ACSC`, `ACSP`,
  `RJCT`, `PATC`, `PENDING`, `INIT`, `CANC`) for `/Services/InitiateBankTransfer`. These are not
  card codes; several of them (`660`-`665`, `671`) are *successes*, so do not treat "non-000" as
  "failed" on a bank-transfer flow.

## A note on J-codes in this table

Several messages name Shva authorization-request types the SKILL.md `ActionType` table does not
list: `041` and `042` mention "J1, J2 or J3", `044` mentions J5, `045` mentions J6. These are Shva
request types visible through Pelecard's error surface. Do not infer that every one of them is a
valid `ActionType` value for your terminal; confirm which your terminal accepts before using
anything beyond `J2` / `J4` / `J5` / `J5h`.

## EMV / Shva result codes

`ShvaResultEmv` carries the EMV / 3DS result from the Shva network and is a **separate** code space
from the table above. A non-zero EMV code does not always mean the transaction failed.

## Recommended logging

Log every callback with:

- the numeric status code (raw) and the message you resolved for it
- `PelecardTransactionId`
- `ShvaResultEmv` (if present)
- `paramX` / `ParamX` (your order correlation)
- the host you posted to and the terminal number

**Do not log `ConfirmationKey`.** It is an authenticator: the whole callback-verification scheme in
SKILL.md Step 4 rests on the attacker not knowing it, and a log aggregator is not a secret store.
Log a hash of it if you need to correlate. Likewise do not log `CardHolderID` (te'udat zehut) from a
`GetTransaction` response in plaintext; it is personal data under the Privacy Protection Law
(Amendment 13) and carries retention obligations your log pipeline almost certainly does not meet.
