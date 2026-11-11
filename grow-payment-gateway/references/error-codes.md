# Grow Error Codes

Grow answers every Light API call with HTTP 200. Failures carry `status: 0` and an `err` object. The table below is Grow's published table (https://developers.grow.business/reference/errors), copied with its Hebrew messages, as fetched 2026-11-11.

| Code | Message (as published) |
|------|------|
| 10 | זיכוי עסקה נכשל |
| 12 | שגיאה כללית |
| 54 | חסרים שדות חובה : (parameter name) |
| 105 | לא ניתן לבצע זיכוי על סכום הגדול מהסכום המקורי |
| 107 | אירעה שגיאה בזיכוי העסקה |
| 109 | נא לוודא תקינות שדות עסקה |
| 110 | לא ניתן לבצע זיכוי על תשלום שהועבר לחשבון הבנק. בקשת הזיכוי נשלחה לאישור מנהל המערכת. |
| 115 | אין אשראי מספק לביצוע הזיכוי. אנא פנה לשירות הלקוחות בטלפון 3144*. |
| 130 | לא ניתן לבצע זיכוי חלקי על עסקה שבוצעה היום |
| 170 | עסקה לא קיימת |
| 180 | פעולת עידכון לא בוצעה, רשומה לא נמצאה |
| 190 | לא ניתן לבצע זיכוי, סכום הזיכוי גדול מסכום החיוב |
| 207 | לא ניתן לבצע זיכוי חלקי כי העסקה עדיין לא שודרה |
| 210 | בוצע זיכוי לעסקה זו, לא ניתן לזכות בשנית. |
| 215 | הסכום לזיכוי אינו תקין |
| 218 | סכום הזיכוי גדול מסכום העסקה |
| 271 | לא ניתן לשלם בביט סכום הגבוה מ-3600ש"ח |
| 272 | סוג תשלום זה אינו מורשה בביט |
| 274 | ביטול בקשת תשלום ב-bit נכשל |
| 275 | לא ניתן לבטל את בקשת התשלום ב-bit |
| 276 | אירעה שגיאה, אנא נסה שנית מאוחר יותר |
| 300 | בעל עסק זה אינו מורשה לשירות API |
| 305 | אינך מורשה לביצוע עסקאות במסופון |
| 310 | פרמטר זיהוי אינו תקין יש לשלוח את הערך כפי שהתקבל ברישום עסקה. |
| 316 | אינך מורשה לקבלת פרטים או ביצוע פעולות בעסקה זו |
| 617 | סכום הכללי של העסקה אינו זהה לסכום המוצרים |
| 701 | פרמטר קוד זיהוי אינו תקין: userId / pageCode |
| 702 | סכום זה אינו מורשה |
| 703 | לקוח אינו מורשה להוראת קבע |
| 704 | לקוח אינו מורשה לאמצעי תשלום (ביט או אשראי) |
| 705 | מספר תשלומים או מספר תשלומים מקסימלי אינו תקין |
| 706 | לינק אינו תקין |
| 707 | הסכום אינו תקין |
| 708 | הלינק שנשלח אינו תקין |
| 709 | פג תוקף הלינק |
| 710 | הגדרות עמוד הסליקה אינן תקינות |
| 711 | יש למלא שדות חובה |
| 712 | העסקה כבר בוצעה |
| 713 | עמוד לא פעיל |
| 714 | הגישה נחסמה |
| 715 | אין הרשאה לעסק לצפות בעסקה זו |
| 716 | פרמטר קוד עסקה או תוקן אינו תקין |
| 717 | לא נשלח שם וטלפון או שאינו תקין |
| 718 | אירעה שגיאה בטעינת נתונים אנא חזור לבחירת אמצעי תשלום מחדש |
| 719 | פרמטרים סכום תשלום ראשון וסכום תשלומים הבאים אינם תקינים אנא וודאו שהסכומים מתאימים לסכום הכולל של העסקה ומספר התשלומים |
| 720 | אין הרשאה לביצוע עסקה ממתינה |
| 721 | סוג תבנית אינו חוקי |
| 722 | לא ניתן לבצע אישור לעסקה שלא בוצעה או בוטלה |
| 723 | apiKey שדה חובה |
| 724 | אירעה שגיאה בטעינת נתונים אנא חזור לבחירת אמצעי תשלום מחדש נדרש שדה userId או pageCode |
| 730 | פרמטר קוד תהליך או תוקן אינו תקין |
| 731 | קוד pageCode אינו תואם את קוד ה-pageCode שאיתו בוצעה הזיהוי |
| 733 | אין הרשאה לעסקת קרדיט |
| 734 | מספר התשלומים המינימלי בעסקת קרדיט הוא 3 תשלומים, הסכום המינימלי לתשלום הוא 25 ש"ח |
| 735 | לסוג עמוד זה מוגדר מספר תשלום נמוך מהמספר שנשלח בפרמטר maxPaymentNum או paymentNum |
| 736 | לא ניתן לשלוח את הפרמטרים paymentNum ו-maxPaymentNum באותה קריאה |
| 738 | לא ניתן לשלם בעמוד זה היות ובוצעו בו מספר נסיונות תשלום |
| 739 | לא ניתן לשלוח את הפרמטר maxPaymentNum בתשלום מסוג הו"ק |
| 740 | החשבון מוגדר עם סוג תשלום רגיל בלבד, לא ניתן לשלוח פרמטר maxPaymentNum או paymentNum. |
| 741 | אין אפשרות לבצע עסקת קרדיט כאשר סוג התשלום הוא רגיל או הו"ק |
| 763 | ה- JSON שנשלח בשדה ה- productData אינו תקין |
| 801 | קוד זיהוי עסק אינו תקין |
| 802 | קוד עסקה או טוקן אינו תקין |
| 803 | J5 פג תוקף |
| 804 | לא ניתן לשחרר עסקה בסכום הגבוה מתפיסת המסגרת |
| 805 | סכום אינו מורשה לעסק |
| 806 | סוג תשלום אינו מורשה |
| 807 | מספר תשלומים אינו מורשה |
| 808 | לא ניתן לבצע שחרור לעסקה ששוחררה |
| 809 | שחרור התשלום נכשל |
| 810 | לא ניתן לבצע שחרור לסוג עסקה זה |
| 811 | התשלום בביט נכשל |
| 812 | קוד זיהוי חברה אינו תקין (apiKey) |
| 813 | לא ניתן לבצע חיוב לעסקה שלא בוצעה |
| 814 | הסכום המירבי לביצוע החיוב הוא עד 30% יותר מסכום העסקה. |
| 871 | סוג המע'מ המוגדר לחשבונית לא תומך במוצרים פטורים ממע'מ |
| 872 | לא ניתן להזין הגדרות מע"מ עבור מוצרים בחשבונית מסוג פטור ממע"מ |
| 873 | עבור עוסק פטור או עמותה אין לכלול מוצרים עם הגדרות מע"מ |
| 878 | אין תמיכה במוצרים שמחירם נמוך מ-0 |
| 890 | לא ניתן לשלם בסכום הנמוך מ- 0 |
| 403 | Forbidden - לא נשלח X-API-KEY |

## Token-charge declines (from Grow's Token page)

`err.id` 103 is reused for final and non-final declines, so classify by id AND message. On a final error Grow says to stop charging the token, delete it, and get a new card.

| `err.id` | Message | Final? |
|---------|---------|--------|
| 103 | כרטיס פג תוקף. | Final |
| 103 | כרטיס גנוב - עסקה לא מאושרת | Final |
| 103 | כרטיס חסום - עסקה לא מאושרת | Final |
| 103 | חברת האשראי לא אשרה את העסקה | Not final |
| 451 | כרטיס האשראי אינו פעיל/פג תוקף, נא לפנות ללקוח לקבלת כרטיס חדש | Final |
| 452 | חברת האשראי חסמה את הכרטיס, נא לפנות ללקוח לבדיקה | Final |
| 453 | חסימת מערכת | Final |

## Codes seen live but missing from the published table

Observed by probing `sandbox.meshulam.co.il` and `sandboxapi.grow.link` with deliberately invalid input (no merchant account, no charge).

| Code | Where | Message / meaning |
|------|-------|------|
| 104 | `createTransactionWithToken`, unknown `userId` | משתמש זה אינו קיים במערכת (user does not exist) |
| 743 | `settleSuspendedTransaction`, unmatched `userId` | אין עסק תואם ל userId שנשלח |
| 880 | `createTransactionWithToken`, valid identifiers but unknown `userId` | לא נמצא עסק מתאים לUserId |
| 1012 | `getTokenTransactionsByExternalIdentifiers`, both identifiers sent | Returned as `err.id = {"id": 1012, "content": "..."}`: send only one identifier per call |
| 1013 | `createTransactionWithToken`, bad `transactionUniqueIdentifier` / `transactionGroupIdentifier` | The identifier must be a positive integer, no leading zeros, below 4,294,967,295 |
| 998 | `sandboxapi.grow.link` payment-link endpoints | A required field is missing; the message names it |
| 427 | `sandboxapi.grow.link/.../CreatePaymentLink` | Invalid field value (for example a malformed `userId`) |
| 5069 | `sandboxapi.grow.link/.../UpdatePaymentLink` | No page found for this identifier |

`err` is the plain string `"unknown method"` (not an object) when the method name does not exist on a `meshulam.co.il` host. On `sandboxapi.grow.link` an unrouted path returns HTTP 403 with `{"message":"Missing Authentication Token"}` instead.
