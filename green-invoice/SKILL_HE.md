---
name: green-invoice
description: >-
  Integrate Green Invoice (Morning) API for Israeli invoicing, receipts, client
  management, and payment processing. Use when user asks to create invoices via
  Green Invoice, generate hashbonit mas through Morning API, manage clients in
  Green Invoice, set up webhook automation for document creation, query
  documents or expenses, or mentions "Green Invoice", "Morning", "hashbonit
  yeruka", "greeninvoice API", Israeli cloud invoicing, or needs to create tax
  invoice-receipt (cheshbonit mas/kabala). Covers all 13 document types, 8
  payment types, client CRUD, item catalog, and webhook integration. Do NOT use
  for SHAAM allocation numbers or Tax Authority e-invoice compliance (use
  israeli-e-invoice), Cardcom payment processing (use cardcom-payment-gateway),
  or Tranzila integration (use tranzila-payment-gateway).
license: MIT
compatibility: >-
  Requires network access for Green Invoice API calls (api.greeninvoice.co.il).
  API credentials obtained from Green Invoice dashboard (Settings, Developer
  Tools). Works with Claude Code, Claude.ai, Cursor.
metadata:
  author: skills-il
  version: 1.0.0
  category: tax-and-finance
  tags:
    he:
      - חשבונית-ירוקה
      - מורנינג
      - חשבונית
      - מע״מ
      - תשלומים
      - ישראל
    en:
      - green-invoice
      - morning
      - invoice
      - vat
      - payments
      - israel
  display_name:
    he: חשבונית ירוקה (מורנינג)
    en: Green Invoice (Morning)
  display_description:
    he: >-
      אינטגרציה עם API של חשבונית ירוקה (מורנינג) ליצירת חשבוניות, קבלות, ניהול
      לקוחות ועיבוד תשלומים לעסקים בישראל
    en: >-
      Integrate Green Invoice (Morning) API for Israeli invoicing, receipts,
      client management, and payment processing for businesses in Israel
  supported_agents:
    - claude-code
    - cursor
    - github-copilot
    - windsurf
    - opencode
    - codex
    - antigravity
---

# חשבונית ירוקה (מורנינג)

## הוראות

### שלב 1: אימות

חשבונית ירוקה משתמשת באימות באמצעות טוקן JWT. ניתן להשיג מפתחות API מלוח הבקרה של חשבונית ירוקה: הגדרות > כלי מפתחים > מפתחות API.

**כתובות בסיס:**

| סביבה | כתובת בסיס |
|--------|------------|
| ייצור | `https://api.greeninvoice.co.il/api/v1` |
| Sandbox | `https://sandbox.d.greeninvoice.co.il/api/v1` |

**קבלת טוקן:**

```bash
curl -X POST https://api.greeninvoice.co.il/api/v1/account/token \
  -H "Content-Type: application/json" \
  -d '{"id": "YOUR_API_KEY_ID", "secret": "YOUR_API_KEY_SECRET"}'
```

התשובה כוללת טוקן JWT. יש להשתמש בו בכל הבקשות הבאות:

```
Authorization: Bearer <token>
Content-Type: application/json
```

תמיד התחילו באימות שהפרטים עובדים:

```bash
curl -s https://api.greeninvoice.co.il/api/v1/users/me \
  -H "Authorization: Bearer <token>" | python3 -m json.tool
```

### שלב 2: הבנת סוגי מסמכים

חשבונית ירוקה תומכת ב-13 סוגי מסמכים. לכל סוג יש קוד מספרי לשימוש בקריאות API.

| קוד | עברית | אנגלית | שימוש נפוץ |
|-----|-------|--------|-----------|
| 10 | הצעת מחיר | Price Quote | הצעות לפני מכירה |
| 100 | הזמנה | Order | הזמנות מאושרות |
| 200 | תעודת משלוח | Delivery Note | תיעוד משלוחים |
| 210 | תעודת החזרה | Return Note | החזרת מוצרים |
| 300 | חשבון עסקה | Transaction Invoice | חשבונית ללא תשלום |
| 305 | חשבונית מס | Tax Invoice | חשבונית מס עצמאית |
| 320 | חשבונית מס / קבלה | Tax Invoice-Receipt | הנפוץ ביותר ללקוחות ישראליים |
| 330 | חשבונית זיכוי | Credit Note | זיכויים ותיקונים |
| 400 | קבלה | Receipt | אישור תשלום |
| 405 | קבלה על תרומה | Donation Receipt | תרומות לעמותות |
| 500 | הזמנת רכש | Purchase Order | רכש |
| 600 | קבלת פיקדון | Deposit Receipt | פיקדונות |
| 610 | משיכת פיקדון | Deposit Withdrawal | החזרת פיקדונות |

**כלל מרכזי:** ללקוחות ישראליים שמשלמים מיידית, השתמשו בסוג `320` (חשבונית מס / קבלה). לחשבוניות שבהן התשלום מגיע מאוחר יותר, השתמשו בסוג `300` (חשבון עסקה). ללקוחות בינלאומיים, השתמשו בסוג `400` (קבלה).

### שלב 3: יצירת מסמכים

**POST** `/v1/documents`

שדות חובה: `type`, `client` (עם `name` ו-`emails`), `income` (מערך פריטים).

```json
{
  "type": 320,
  "date": "2026-03-05",
  "lang": "he",
  "currency": "ILS",
  "vatType": 0,
  "rounding": true,
  "signed": true,
  "attachment": true,
  "client": {
    "name": "משה כהן",
    "emails": ["moshe@example.com"],
    "taxId": "123456789",
    "add": true
  },
  "income": [
    {
      "description": "שירותי פיתוח אתרים",
      "quantity": 1,
      "price": 5000,
      "currency": "ILS",
      "vatType": 0
    }
  ],
  "payment": [
    {
      "type": 4,
      "date": "2026-03-05",
      "price": 5000,
      "currency": "ILS"
    }
  ]
}
```

**סוגי מע"מ (ברמת המסמך):**

| קוד | משמעות |
|-----|--------|
| 0 | ברירת מחדל (מע"מ מתווסף לפי סוג העסק) |
| 1 | פטור (ללא מע"מ) |
| 2 | מעורב (חלק מהפריטים פטורים וחלק לא) |

**סוגי מע"מ (ברמת שורת הכנסה):**

| קוד | משמעות |
|-----|--------|
| 0 | ברירת מחדל (עוקב אחרי הגדרת המסמך) |
| 1 | מע"מ כלול במחיר |
| 2 | פטור לשורה זו |

### שלב 4: סוגי תשלום

בעת הוספת רשומות תשלום למסמך, השתמשו בקודים הבאים:

| קוד | עברית | אנגלית |
|-----|-------|--------|
| -1 | לא שולם | Unpaid |
| 0 | ניכוי במקור | Withholding Tax |
| 1 | מזומן | Cash |
| 2 | המחאה | Check |
| 3 | כרטיס אשראי | Credit Card |
| 4 | העברה בנקאית | Bank Transfer |
| 5 | פייפאל | PayPal |
| 10 | אפליקציית תשלום (ביט, פפר פיי, פיי בוקס) | Payment App |
| 11 | אחר | Other |

**סוגי כרטיס אשראי** (כאשר סוג התשלום הוא 3):

| קוד | כרטיס |
|-----|-------|
| 1 | ישראכרט |
| 2 | ויזה |
| 3 | מאסטרקארד |
| 4 | אמריקן אקספרס |
| 5 | דיינרס |

**סוגי עסקת אשראי:**

| קוד | סוג |
|-----|-----|
| 1 | רגיל |
| 2 | תשלומים |
| 3 | קרדיט |
| 4 | חיוב נדחה |

### שלב 5: ניהול לקוחות

**יצירת לקוח:** `POST /v1/clients`

```json
{
  "name": "סטארטאפ בע\"מ",
  "emails": ["billing@startup.co.il"],
  "taxId": "515123456",
  "country": "IL",
  "city": "תל אביב",
  "address": "רוטשילד 45",
  "paymentTerms": 30,
  "labels": ["tech", "monthly"]
}
```

**תנאי תשלום:**

| קוד | משמעות |
|-----|--------|
| -1 | מיידי (שוטף) |
| 0 | סוף חודש (שוטף סוף חודש) |
| 30 | שוטף + 30 |
| 60 | שוטף + 60 |
| 90 | שוטף + 90 |

**נקודות קצה נוספות ללקוחות:**

| שיטה | נתיב | תיאור |
|------|------|-------|
| GET | `/v1/clients/{id}` | קבלת לקוח לפי מזהה |
| PUT | `/v1/clients/{id}` | עדכון לקוח |
| DELETE | `/v1/clients/{id}` | מחיקת לקוח |
| POST | `/v1/clients/search` | חיפוש לקוחות |

**חיפוש לקוחות:**

```json
{
  "name": "סטארטאפ",
  "active": true,
  "page": 0,
  "pageSize": 25
}
```

### שלב 6: חיפוש ושאילתת מסמכים

**POST** `/v1/documents/search`

```json
{
  "page": 0,
  "pageSize": 25,
  "type": [320, 305],
  "status": [0, 1],
  "fromDate": "2026-01-01",
  "toDate": "2026-03-31",
  "sort": "documentDate"
}
```

**סטטוסי מסמכים:**

| קוד | משמעות |
|-----|--------|
| 0 | פתוח |
| 1 | סגור |
| 2 | נסגר ידנית |
| 3 | מבטל מסמך אחר |
| 4 | מבוטל |

**קבלת מסמך:** `GET /v1/documents/{id}`

**סגירת מסמך:** `POST /v1/documents/{id}/close`

**הורדת PDF של מסמך:** `GET /v1/documents/{id}/download/links` מחזיר כתובות URL בעברית, אנגלית ובשפת המקור.

### שלב 7: קישור מסמכים

ניתן לקשר מסמכים ליצירת תהליכי עבודה. השתמשו ב-`linkedDocumentIds` בעת יצירת מסמך חדש.

דפוסי קישור נפוצים:

| תרחיש | שלבים |
|--------|-------|
| חשבונית ואחר כך קבלה | יצירת סוג 300 (חשבון עסקה), מאוחר יותר יצירת סוג 400 (קבלה) עם `linkedDocumentIds: ["invoice-id"]` |
| חשבונית זיכוי עבור חשבונית | יצירת סוג 330 (חשבונית זיכוי) עם `linkedDocumentIds: ["original-id"]` ו-`linkType: "cancel"` |
| הצעת מחיר להזמנה לחשבונית | יצירת סוג 10 (הצעת מחיר), אחר כך סוג 100 (הזמנה), אחר כך סוג 300 (חשבונית), עם קישור בין כל אחד |

כאשר קבלה מקושרת לחשבונית עם תשלום מלא, החשבונית נסגרת אוטומטית.

### שלב 8: קטלוג פריטים

ניהול פריטי מוצרים/שירותים לשימוש חוזר:

| שיטה | נתיב | תיאור |
|------|------|-------|
| POST | `/v1/items` | יצירת פריט |
| GET | `/v1/items/{id}` | קבלת פריט |
| PUT | `/v1/items/{id}` | עדכון פריט |
| POST | `/v1/items/search` | חיפוש פריטים |

השתמשו ב-`itemId` בשורות הכנסה כדי להפנות לפריטים מהקטלוג במקום לציין ידנית תיאור ומחיר בכל פעם.

### שלב 9: סוגי עסק וכללי מע"מ

חשבונית ירוקה מטפלת במע"מ אוטומטית לפי סוג העסק:

| קוד | עברית | אנגלית | התנהגות מע"מ |
|-----|-------|--------|-------------|
| 1 | עוסק מורשה | Licensed Dealer | מע"מ מתווסף (17% נכון ל-2025) |
| 2 | חברה בע"מ | Ltd. Company | מע"מ מתווסף |
| 3 | עוסק פטור | Exempt Dealer | ללא מע"מ |
| 4 | עמותה | Non-Profit | ללא מע"מ |
| 5 | חברה לתועלת הציבור | Public Benefit Company | ללא מע"מ |
| 6 | שותפות | Partnership | מע"מ מתווסף |

הגדירו `vatType: 0` במסמכים והמערכת תחיל את המע"מ הנכון לפי סוג העסק שלכם. דרסו עם `vatType: 1` לעסקאות פטורות או `vatType: 2` למסמכים מעורבים.

### שלב 10: Webhooks

הגדרת webhooks ב: הגדרות > כלי מפתחים > יצירת Webhook.

Webhooks מופעלים ביצירת מסמך. ה-payload כולל את אובייקט המסמך המלא:

```json
{
  "id": "document-uuid",
  "type": 320,
  "number": 12345,
  "currency": "ILS",
  "date": "2026-03-05",
  "total": 5850,
  "recipient": {
    "name": "שם הלקוח",
    "emails": ["client@example.com"]
  },
  "items": [
    {
      "description": "שירות",
      "quantity": 1,
      "price": 5000
    }
  ],
  "files": {
    "signed": true,
    "downloadLinks": {
      "he": "https://www.greeninvoice.co.il/api/v1/documents/download?d=...",
      "en": "https://www.greeninvoice.co.il/api/v1/documents/download?d=..."
    }
  }
}
```

אוטומציות webhook נפוצות:
- שמירת PDF ל-Google Drive או Dropbox ביצירת חשבונית
- עדכון CRM כשמונפקת קבלה
- שליחת התראת Slack למסמכים חדשים
- סנכרון חשבוניות למערכות הנהלת חשבונות חיצוניות

עיינו ב-`references/api-reference.md` לסכמת ה-payload המלאה של webhooks.

### שלב 11: מטבעות ושערי חליפין

חשבונית ירוקה תומכת ב-28 מטבעות. אם `currencyRate` לא מצוין, המערכת משתמשת בשערי בנק ישראל לתאריך המסמך.

מטבעות נפוצים: ILS, USD, EUR, GBP, JPY, CHF, CAD, AUD.

עבור חשבוניות רב-מטבעיות, כל שורת הכנסה יכולה לציין `currency` ו-`currencyRate` משלה. הסכומים הסופיים מחושבים תמיד במטבע הבסיס של המסמך.

### שלב 12: בדיקות ב-Sandbox

תמיד בדקו בסביבת הסנדבוקס לפני מעבר לייצור:

1. הרשמו לחשבון sandbox בחשבונית ירוקה
2. השתמשו בכתובת: `https://sandbox.d.greeninvoice.co.il/api/v1`
3. צרו מפתחות API ל-sandbox
4. בדקו את כל תהליכי יצירת מסמכים, ניהול לקוחות ו-webhooks
5. וודאו שחישובי מע"מ וקישור מסמכים עובדים נכון
6. עברו לכתובת הייצור כשמוכנים

## דוגמאות

### דוגמה 1: יצירת חשבונית מס / קבלה ללקוח ישראלי

המשתמש אומר: "צור חשבונית מס קבלה ללקוח שמשלם בהעברה בנקאית"

פעולות:
1. אימות מול API של חשבונית ירוקה
2. יצירת לקוח אם חדש (POST `/v1/clients` עם שם, אימייל, מספר עוסק)
3. יצירת מסמך סוג 320 (חשבונית מס / קבלה) עם סוג תשלום 4 (העברה בנקאית)
4. הגדרת `signed: true` לחתימה דיגיטלית, `attachment: true` לשליחת PDF באימייל

תוצאה: חשבונית מס / קבלה נוצרה, נחתמה דיגיטלית ונשלחה ללקוח כ-PDF.

### דוגמה 2: חשבוניות חודשיות חוזרות

המשתמש אומר: "אני צריך לשלוח חשבוניות חודשיות ל-3 לקוחות ריטיינר"

פעולות:
1. חיפוש לקוחות קיימים: POST `/v1/clients/search` עם שמות הלקוחות
2. לכל לקוח, יצירת מסמך סוג 300 (חשבון עסקה) עם תיאור "ריטיינר חודשי - מרץ 2026"
3. הגדרת `dueDate` לתאריך לפי תנאי תשלום, `lang` לפי העדפת הלקוח
4. מסמכים נשלחים אוטומטית כש-`attachment: true`

תוצאה: שלוש חשבוניות נוצרו ונשלחו, כל אחת עם תנאי תשלום ושפה נכונים.

### דוגמה 3: הנפקת חשבונית זיכוי לזיכוי חלקי

המשתמש אומר: "זכה חצי מהסכום בחשבונית מספר 12345"

פעולות:
1. קבלת המסמך המקורי: GET `/v1/documents/{id}`
2. חישוב סכום הזיכוי (חצי מהסכום המקורי)
3. יצירת מסמך סוג 330 (חשבונית זיכוי) עם `linkedDocumentIds: ["original-id"]` ו-`linkType: "cancel"`
4. הגדרת סכום ההכנסה לערך הזיכוי השלילי

תוצאה: חשבונית זיכוי הונפקה, מקושרת לחשבונית המקורית, עם סכום זיכוי חלקי.

### דוגמה 4: אוטומציית Webhook לתיוק מסמכים

המשתמש אומר: "הגדר תיוק אוטומטי כשחשבונית ירוקה יוצרת מסמך"

פעולות:
1. הגדרת כתובת webhook בלוח הבקרה של חשבונית ירוקה
2. מימוש endpoint ל-webhook שמקבל את ה-payload של המסמך
3. חילוץ שדה `type` לניתוב מסמך (חשבונית מול קבלה מול חשבונית זיכוי)
4. שימוש ב-`files.downloadLinks.he` להורדת ה-PDF בעברית
5. תיוק לתיקייה המתאימה לפי סוג המסמך ותאריך

תוצאה: כל המסמכים החדשים מורדים ומסודרים אוטומטית לפי סוג וחודש.

## משאבים מצורפים

### סקריפטים
- `scripts/green-invoice-client.py` -- כלי Python לפעולות נפוצות ב-API של חשבונית ירוקה: אימות, יצירת מסמכים, חיפוש לקוחות ורשימת מסמכים אחרונים. הרצה: `python3 scripts/green-invoice-client.py --help`

### מסמכי עזר
- `references/api-reference.md` -- מדריך מלא לנקודות הקצה של API חשבונית ירוקה עם סכמות בקשה/תגובה, כל קודי ה-enum ודוגמאות payload. עיינו בו בעת בניית אינטגרציות API או ניפוי שגיאות בפורמט בקשות.
- `references/document-workflows.md` -- תהליכי עבודה נפוצים למסמכים עסקיים ישראליים: חיוב פרילנסרים, חשבוניות ריטיינר, תהליכי זיכוי, חיוב רב-מטבעי ודפוסי אינטגרציה עם חנויות אונליין. עיינו בו בעת תכנון אוטומציית חשבוניות או בחירת רצף סוגי מסמכים נכון.

## פתרון בעיות

### שגיאה: "401 Unauthorized" בקריאות API
סיבה: טוקן JWT פג תוקף או פרטי אימות לא תקינים
פתרון: טוקנים פגים מדי פעם. בצעו אימות מחדש על ידי קריאה ל-POST `/v1/account/token` עם מזהה מפתח ה-API והסוד שלכם. אמתו את הפרטים בלוח הבקרה תחת הגדרות > כלי מפתחים.

### שגיאה: "Document type not supported for your business type"
סיבה: עוסק פטור לא יכול להנפיק חשבונית מס (סוג 305)
פתרון: בדקו את סוג העסק שלכם. עוסק פטור צריך להשתמש בסוג 320 (חשבונית מס / קבלה) או סוג 400 (קבלה). עוסק מורשה וחברות בע"מ יכולים להשתמש בכל סוגי המסמכים.

### שגיאה: "VAT calculation mismatch"
סיבה: ערבוב הגדרות vatType בין רמת המסמך לרמת שורת ההכנסה
פתרון: הגדירו `vatType: 0` ברמת המסמך לשימוש בברירות מחדל. דרסו ברמת שורת ההכנסה רק כשיש פריטים עם מע"מ מעורב. אם המע"מ כלול במחירים, הגדירו `vatType: 1` בשורת ההכנסה.

### שגיאה: "Client email required"
סיבה: יצירת מסמך ללא מתן אימייל ללקוח
פתרון: מערך `client.emails` חייב להכיל לפחות אימייל תקין אחד כש-`attachment: true`. למסמכים שלא צריכים להישלח באימייל, הגדירו `attachment: false`.
