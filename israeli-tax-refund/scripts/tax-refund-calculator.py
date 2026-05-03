#!/usr/bin/env python3
"""
tax-refund-calculator.py
חישוב החזר מס לשכיר על בסיס נתוני טופס 106 ו-161.
Run: python tax-refund-calculator.py --help
"""

import argparse
import sys

# מדרגות מס לפי שנה (הכנסה שנתית בשקלים, שיעור מס שולי)
TAX_BRACKETS = {
    2026: [(84120, 0.10), (120720, 0.14), (228000, 0.20),
           (301200, 0.31), (560280, 0.35), (721560, 0.47), (float('inf'), 0.50)],
    2025: [(84120, 0.10), (120720, 0.14), (193800, 0.20),
           (269280, 0.31), (558240, 0.35), (float('inf'), 0.47)],
    2024: [(81480, 0.10), (116760, 0.14), (188280, 0.20),
           (261960, 0.31), (548040, 0.35), (698280, 0.47), (float('inf'), 0.50)],
}

# ערך נקודת זיכוי לפי שנה (שנתי)
CREDIT_POINT_VALUE = {
    2026: 3024,
    2025: 2964,
    2024: 2904,
    2023: 2820,
}


def calc_tax_on_income(income: float, year: int) -> float:
    """חישוב מס על הכנסה שנתית לפי מדרגות."""
    brackets = TAX_BRACKETS.get(year, TAX_BRACKETS[2026])
    tax = 0.0
    prev_threshold = 0.0
    for threshold, rate in brackets:
        if income <= prev_threshold:
            break
        taxable = min(income, threshold) - prev_threshold
        tax += taxable * rate
        prev_threshold = threshold
    return round(tax, 2)


def calc_credit_points(credit_points: float, year: int) -> float:
    """חישוב שווי נקודות זיכוי."""
    point_value = CREDIT_POINT_VALUE.get(year, CREDIT_POINT_VALUE[2026])
    return round(credit_points * point_value, 2)


def main():
    parser = argparse.ArgumentParser(
        description="מחשבון החזר מס לשכיר – על בסיס נתוני טופס 106",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
דוגמאות:
  python tax-refund-calculator.py --income 150000 --tax-paid 18000 --credit-points 2.25 --year 2025
  python tax-refund-calculator.py --income 280000 --tax-paid 55000 --credit-points 3.25 --year 2026
        """
    )
    parser.add_argument("--income", type=float, required=True,
                        help="הכנסה חייבת שנתית (שדה 158 בטופס 106), בשקלים")
    parser.add_argument("--tax-paid", type=float, required=True,
                        help="מס הכנסה שנוכה בפועל (שדה 042 בטופס 106), בשקלים")
    parser.add_argument("--credit-points", type=float, default=2.25,
                        help="מספר נקודות זיכוי (ברירת מחדל: 2.25 לגבר)")
    parser.add_argument("--year", type=int, default=2025,
                        help="שנת המס (ברירת מחדל: 2025)")
    parser.add_argument("--life-insurance", type=float, default=0,
                        help="פרמיית ביטוח חיים שנתית (25% חוזרים כזיכוי)")
    parser.add_argument("--donations", type=float, default=0,
                        help="תרומות למוסד מוכר סעיף 46 (35% זיכוי על סכום מעל 210 ₪)")

    args = parser.parse_args()

    if args.year not in TAX_BRACKETS:
        print(f"אזהרה: אין נתוני מדרגות לשנת {args.year}. משתמש בנתוני 2026.", file=sys.stderr)

    gross_tax = calc_tax_on_income(args.income, args.year)
    credit_deduction = calc_credit_points(args.credit_points, args.year)

    # זיכוי ביטוח חיים (25% מהפרמיה)
    life_insurance_credit = round(args.life_insurance * 0.25, 2)

    # זיכוי תרומות (35% על סכום מעל 210 ₪)
    donation_credit = round(max(0, args.donations - 210) * 0.35, 2)

    total_credits = credit_deduction + life_insurance_credit + donation_credit
    net_tax_liability = max(0, gross_tax - total_credits)
    refund = round(args.tax_paid - net_tax_liability, 2)

    print("\n" + "="*50)
    print(f"  סיכום חישוב החזר מס – שנת {args.year}")
    print("="*50)
    print(f"  הכנסה חייבת:              {args.income:>12,.0f} ₪")
    print(f"  מס ברוטו (לפי מדרגות):   {gross_tax:>12,.0f} ₪")
    print(f"  ניכוי נקודות זיכוי:       {credit_deduction:>12,.0f} ₪")
    if life_insurance_credit > 0:
        print(f"  זיכוי ביטוח חיים:         {life_insurance_credit:>12,.0f} ₪")
    if donation_credit > 0:
        print(f"  זיכוי תרומות:              {donation_credit:>12,.0f} ₪")
    print(f"  חבות מס נטו:              {net_tax_liability:>12,.0f} ₪")
    print(f"  מס ששולם בפועל:           {args.tax_paid:>12,.0f} ₪")
    print("-"*50)
    if refund > 0:
        print(f"  ✅ החזר מס אפשרי:        {refund:>12,.0f} ₪")
    elif refund < 0:
        print(f"  ⚠️  חוב מס אפשרי:         {abs(refund):>12,.0f} ₪")
    else:
        print(f"  ✅ המס חושב בצורה מדויקת")
    print("="*50)
    print("\n⚠️  זוהי הערכה ראשונית בלבד. פנה ליועץ מס מוסמך לבדיקה מדויקת.")


if __name__ == "__main__":
    main()
