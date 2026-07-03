---
name: sp500-nasdaq-screener
license: MIT
description: >-
  סינון ודירוג מניות ה-S&P 500 וה-NASDAQ-100 לפי קריטריונים טכניים ופונדמנטליים. לשימוש כשמשתמש רוצה לסנן או לדרג מניות אמריקאיות — "מניות S&P 500 עם RSI מתחת ל-30", "מניות נאסד"ק מעל הממוצע הנע ל-200 יום", סריקות oversold/overbought, או סינון סקטוריאלי. מחזיר טבלה מדורגת עם הקריטריונים שהתאימו לכל סימול. אין להשתמש לניתוח מעמיק של נייר בודד (השתמש ב-global-stock-analysis) או לסינון מניות ת"א.
allowed-tools: "Bash(python:*) WebFetch"
metadata:
  author: yonyon-ai
  version: 1.0.0
  category: tax-and-finance
  lang: he
  display_name: "סורק מניות S&P 500 / נאסד\"ק"
---

# סורק מניות S&P 500 / נאסד"ק

## הוראות

### שלב 1 — טעינת היקום
references/sp500-constituents.md ו-nasdaq100 — תצלומי מצב מתוארכים.

### שלב 2 — פירוק הפילטר
ספי אינדיקטורים (RSI < 30), יחסי ממוצע נע (מחיר > EMA200), פונדמנטלס, סקטור.
ראה references/screening-criteria.md.

### שלב 3 — חישוב באצווה
הרצה: python scripts/screen.py --index sp500 --filter "rsi<30"
scripts/provider.py מביא EOD באצווה (retry-then-raise; סימול ללא נתונים מדולג,
לא מזויף) ומחשב RSI/EMA לכל סימול דרך scripts/indicators.py.

### שלב 4 — דירוג והחזרה
טבלה: סימול, קריטריונים שהתאימו, מדד הדירוג, סקטור.

## דוגמאות
משתמש: "מניות S&P 500 במכירת יתר לפי RSI, ממוין לפי שווי שוק"
תוצאה: טבלה מדורגת של סימולים עם RSI < 30.

## מלכודות
- רשימות מרכיבים משתנות באיזון מחדש. סריקה מלאה כבדה — הגבל ומטמן.

## תרשים (אופציונלי)
תרשים נוצר רק כשהוא מבהיר את התשובה או שהמשתמש מבקש — לא כברירת מחדל ולא כ-ASCII.
scripts/chart.py מייצר תרשים עמודות HTML אינטראקטיבי עצמאי: הסימולים המותאמים
מדורגים לפי מדד הפילטר, עמודה בגוון-הדגשה אחד לכל סימול עם תווית ישירה, ריחוף
לכל עמודה, תצוגת טבלה ומתג בהיר/כהה. הטבלה הטקסטואלית נשארת הפלט הראשי.

## משאבים
scripts/screen.py · scripts/provider.py · scripts/indicators.py · scripts/chart.py ·
scripts/viz.py · references/sp500-constituents.md ·
references/nasdaq100-constituents.md · references/screening-criteria.md
