# VAT and Oseik Status for Israeli Quotes (2026)

## Current VAT rate

**18%** since 2025-01-01.

- Was 17% from 2015 through 2024
- Raised to 18% effective 2025-01-01 per the 2025 Budget Law
- A January 2026 proposal to raise to 19% was rejected by the cabinet (curbed defence spending instead)
- Sources: PwC tax summary, Knesset press release, multiple secondary sources

## Oseik patur 2026 threshold

**122,833 ₪** per calendar year (turnover, not profit).

- CPI-indexed annually by the Tax Authority
- Was 120,000 ₪ in 2024 and 2025
- A freelancer crossing the threshold mid-year must visit the regional VAT office to convert to oseik morshe

## What each status can and cannot do (quote-side)

| Status | Charges VAT? | Header label | Future invoice type |
|---|---|---|---|
| Oseik morshe | Yes, 18% | "עוסק מורשה" + מספר עוסק | חשבונית מס |
| Oseik patur | No | "עוסק פטור, אינו רשום כעוסק מורשה" + מספר עוסק | חשבונית עסקה + קבלה |
| Esek za'ir | No | "עסק זעיר" (or unchanged from oseik patur for under-threshold) | חשבונית עסקה + קבלה |
| Chevra ba'am | Yes, 18% | "חברה בע\"מ" + מספר חברה | חשבונית מס |

### Oseik patur invoice rules (the trap)

An oseik patur **cannot issue a חשבונית מס** (tax invoice). They must:

1. Issue a **חשבונית עסקה** (business invoice / payment request) when sending the bill.
2. Issue a **קבלה** (receipt) when the payment arrives.

Putting "חשבונית מס" or "מע\"מ 18%" on an oseik patur document is a Tax Authority violation and exposes the freelancer to a fine.

### Export of services (VAT 0%)

When an oseik morshe sells services to a non-resident customer outside Israel, the line is **zero-rated** under VAT Law section 30(a)(5). Important nuances:

- The issuer still files a VAT return; the line shows at 0% (NOT omitted from the return)
- The customer doesn't pay VAT
- The issuer can still claim input VAT on related expenses (this is the value of being zero-rated vs exempt)
- Mark the line clearly: "0% VAT, export of services per VAT Law §30(a)(5)"

## When the freelancer crosses the threshold

If the freelancer is currently oseik patur and the quote being drafted would push them over 122,833 ₪ for the calendar year:

1. **Quote is fine as oseik patur** if work delivery + payment will fall in the next calendar year (revenue is recognized when received for cash-basis filers).
2. **Status conversion is required** before issuing the future חשבונית עסקה if the work delivers + gets paid before year-end and pushes them over the cap.
3. **The user must visit the regional מע\"מ office** to convert. Until conversion, they cannot legally charge VAT.

The skill should flag the threshold-crossing scenario but not block the quote, the freelancer needs the quote to land the work, then handle the status change.

## Rounding convention

Israeli quotes and invoices use **agorot (2 decimal places)** as the standard display. Some accounting software rounds to whole shekel for display, both are accepted, but mixing them in one document looks sloppy.

```
subtotal = round(sum(line_totals), 2)
vat = round(subtotal * 0.18, 2)
total = round(subtotal + vat, 2)
```

Use banker's rounding (ROUND_HALF_EVEN) in code to avoid 0.005 → 0.01 vs 0.005 → 0.00 inconsistencies.
