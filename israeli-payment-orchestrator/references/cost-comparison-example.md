# Cost Comparison Example

### Example 3: Cost Comparison
User says: "Which gateway is cheapest for our 500 daily transactions averaging 200 NIS?"
Actions:
1. Say plainly that no one can answer this from public information. None of the six publishes a rate card, and the rate is negotiated per merchant on volume, industry and chargeback profile. Any table that names a winner is inventing the inputs.
2. Give them what actually decides it: the monthly volume to negotiate with, here 500 * 30 * 200 = 3,000,000 NIS, and the instruction to get a written quote from each gateway at that volume.
3. Name the costs the discount rate hides, which routinely dominate at this size: merchant-subsidized interest-free instalments, the settlement cycle's working-capital cost, per-refund and chargeback charges, and the fact that a charge-then-credit pair clears twice while a void clears never.
4. Compare on capability where capability is knowable: `python scripts/compare_gateways.py --example`.
Result: A negotiating position and a capability comparison, not a false ranking

---

### דוגמה 3: השוואת עלויות
המשתמש אומר: "איזה שער הכי זול ל-500 עסקאות יומיות ממוצע 200 ש"ח?"
פעולות:
1. תגידו בפשטות שאף אחד לא יכול לענות על זה ממידע ציבורי. אף אחד מהשישה לא מפרסם מחירון; עמלת הסליקה נקבעת במשא ומתן לכל בית עסק לפי נפח, ענף ופרופיל chargebacks. כל טבלה שמכריזה על מנצח ממציאה את הקלט.
2. תנו למשתמש את מה שבאמת קובע: הנפח החודשי להתמקח עליו, שהוא כאן 500 * 30 * 200 = 3,000,000 ש"ח, והנחיה לבקש הצעת מחיר כתובה מכל שער בנפח הזה.
3. תנקבו בעלויות שעמלת הסליקה מסתירה, כי בסדר גודל כזה הן לרוב דומיננטיות: האם תשלומים "ללא ריבית" מסובסדים על ידי בית העסק, מחזור הסליקה ועלות ההון שלו, עמלות זיכוי ו-chargeback, והעובדה שצמד חיוב-זיכוי נסלק פעמיים בעוד ביטול לא נסלק בכלל.
4. תשוו על יכולות, במקום שבו היכולות ידועות: `python scripts/compare_gateways.py --example`.
תוצאה: עמדת מיקוח והשוואת יכולות, לא דירוג שגוי

