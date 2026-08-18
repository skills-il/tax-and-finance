# Ready-to-Copy Quote Templates (Hebrew)

Three Hebrew templates and one bilingual HE/EN template. Replace `{...}` placeholders.

---

## Template 1: Hourly consulting (oseik morshe)

```markdown
# הצעת מחיר {quote_number}

**{issuer_name}** | עוסק מורשה {oseik_number}
טלפון {phone} | אימייל {email}
{address}

**לכבוד:** {client_name} ({client_id_label} {client_id})
**תאריך הוצאה:** {issue_date}
**תוקף ההצעה עד:** {validity_date}

## פירוט השירות

| פריט | כמות | מחיר יחידה | סה"כ |
|---|---|---|---|
| {service_description} | {hours} שעות | {hourly_rate} ₪ | {line_total} ₪ |

**סה"כ לפני מע"מ:** {subtotal} ₪
**מע"מ 18%:** {vat} ₪
**סה"כ לתשלום:** {total} ₪

## תנאי עבודה

- **תנאי תשלום:** שוטף + 30 ימים מהנפקת החשבונית, בהתאם לחוק מוסר תשלומים לספקים, התשע"ז-2017.
- **שינויים בהיקף:** כל שינוי מעבר למפורט יחויב בנפרד לפי תעריף {hourly_rate} ₪ + מע"מ לשעה.
- **אמצעי תשלום:** Bit {phone}, או העברה בנקאית: {bank_name} ({bank_code}), סניף {branch}, חשבון {account}.

## חתימת קבלת ההצעה

מאשר/ת קבלה ואישור ההצעה:

________________________  תאריך: __________
{client_name}
```

---

## Template 2: Fixed-scope project (oseik morshe)

```markdown
# הצעת מחיר {quote_number}

**{issuer_name}** | עוסק מורשה {oseik_number}
טלפון {phone} | אימייל {email}
{address}

**לכבוד:** {client_name} ({client_id_label} {client_id})
**תאריך הוצאה:** {issue_date}
**תוקף ההצעה עד:** {validity_date}

## תיאור הפרויקט

{project_description}

**לוחות זמנים:** {timeline_description}
**הספקה:** {deliverables_list}

## עלות

| שלב | תיאור | עלות |
|---|---|---|
| 1 | {milestone_1} | {cost_1} ₪ |
| 2 | {milestone_2} | {cost_2} ₪ |
| 3 | {milestone_3} | {cost_3} ₪ |

**סה"כ לפני מע"מ:** {subtotal} ₪
**מע"מ 18%:** {vat} ₪
**סה"כ לתשלום:** {total} ₪

## תנאי עבודה

- **תנאי תשלום:** {payment_split}, שוטף + 30 ימים, בהתאם לחוק מוסר תשלומים לספקים, התשע"ז-2017.
- **שינויים בהיקף:** כל שינוי בהיקף העבודה מעבר למפורט בהצעה זו יחויב בנפרד לפי תעריף שעתי של {hourly_rate} ₪ + מע"מ.
- **ביטול הזמנה:** ביטול לאחר אישור הצעה זו יחויב ב-{cancellation_percent}% מהסכום הכולל.
- **אמצעי תשלום:** {payment_methods}.

## חתימת קבלת ההצעה

________________________  תאריך: __________
{client_name}
```

---

## Template 3: Oseik patur (no VAT, different header)

```markdown
# הצעת מחיר {quote_number}

**{issuer_name}** | עוסק פטור {oseik_number}, אינו רשום כעוסק מורשה
טלפון {phone} | אימייל {email}
{address}

**לכבוד:** {client_name}
**תאריך הוצאה:** {issue_date}
**תוקף ההצעה עד:** {validity_date}

## פירוט השירות

| פריט | כמות | מחיר יחידה | סה"כ |
|---|---|---|---|
| {service_description} | {quantity} | {unit_price} ₪ | {line_total} ₪ |

**סה"כ לתשלום:** {total} ₪
*(אינני רשום כעוסק מורשה, אינני חייב מע"מ.)*

## תנאי עבודה

- **תנאי תשלום:** שוטף + 30 ימים מהנפקת חשבונית עסקה, בהתאם לחוק מוסר תשלומים לספקים, התשע"ז-2017.
- **לאחר אישור ההצעה** תופק חשבונית עסקה, ועם קבלת התשלום תופק קבלה.
- **אמצעי תשלום:** Bit {phone}, או העברה בנקאית: {bank_name}, סניף {branch}, חשבון {account}.

## חתימת קבלת ההצעה

________________________  תאריך: __________
{client_name}
```

---

## Template 4: Bilingual HE / EN (export client, oseik morshe, 0% VAT)

```markdown
# הצעת מחיר / Price Quote {quote_number}

| עברית | English |
|---|---|
| **{issuer_name}** | **{issuer_name}** |
| עוסק מורשה {oseik_number} | Israeli VAT registered, ID {oseik_number} |
| טלפון {phone} | Phone {phone} |
| אימייל {email} | Email {email} |
| **לכבוד:** {client_name} ({country}) | **To:** {client_name} ({country}) |
| תאריך הוצאה: {issue_date} | Issued: {issue_date} |
| תוקף ההצעה עד: {validity_date} | Valid until: {validity_date} |

## פירוט השירות / Line Items

| Description / תיאור | Qty | Unit Price | Total |
|---|---|---|---|
| {service_en} / {service_he} | {quantity} | ${unit_price} | ${line_total} |

**Subtotal / סה"כ לפני מע"מ:** ${subtotal}
**VAT 0% (export of services, VAT Law §30(a)(5)):** $0.00
**Grand total / סה"כ לתשלום:** ${total}

## Terms / תנאי עבודה

- **Payment terms / תנאי תשלום:** Net 30 days from invoice. Wire transfer to:
  - Beneficiary: {beneficiary_name}
  - Bank: {bank_name}, SWIFT {swift_code}
  - IBAN: {iban}
- **Currency / מטבע:** USD. השער הקובע לחיוב הוא שער יציג של בנק ישראל ביום הוצאת החשבונית. The reference rate is the Bank of Israel daily reference rate on the invoice date.
- **VAT:** Zero-rated under VAT Law section 30(a)(5) (export of services to non-resident).

## Acceptance / חתימת קבלת ההצעה

________________________  Date / תאריך: __________
{client_name}
```
