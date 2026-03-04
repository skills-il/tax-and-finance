#!/usr/bin/env python3
"""Parse and display Hebrew financial term glossary.

Provides a quick reference for Hebrew-English financial terminology
commonly found in Israeli annual reports and MAYA filings.

Usage:
    python financial_parser.py --search "רווח"
    python financial_parser.py --all
    python financial_parser.py --help
"""

import argparse

FINANCIAL_TERMS = {
    "מאזן": "Balance Sheet",
    "דוח רווח והפסד": "Income Statement (P&L)",
    "תזרים מזומנים": "Cash Flow Statement",
    "הכנסות": "Revenue",
    "רווח גולמי": "Gross Profit",
    "רווח תפעולי": "Operating Profit (EBIT)",
    "רווח נקי": "Net Profit",
    "EBITDA": "Earnings Before Interest, Tax, Depreciation, Amortization",
    "נכסים שוטפים": "Current Assets",
    "נכסים בלתי שוטפים": "Non-Current Assets",
    "התחייבויות שוטפות": "Current Liabilities",
    "התחייבויות לזמן ארוך": "Long-Term Liabilities",
    "הון עצמי": "Shareholders' Equity",
    "מוניטין": "Goodwill",
    "עודפים": "Retained Earnings",
    "צד קשור": "Related Party",
    "דוח תקופתי": "Periodic/Annual Report",
    "דוח מיידי": "Immediate Report",
    "דוח רבעוני": "Quarterly Report",
    "תשקיף מדף": "Shelf Prospectus",
    "ועדת ביקורת": "Audit Committee",
    "דירקטוריון": "Board of Directors",
    "רואה חשבון מבקר": "External Auditor",
    "הפרשה": "Provision",
    "פחת": "Depreciation",
    "הפחתה": "Amortization",
    "ירידת ערך": "Impairment",
    "שווי הוגן": "Fair Value",
    "רווח למניה": "Earnings Per Share (EPS)",
    "דיבידנד": "Dividend",
}

def search_terms(query):
    results = {}
    for he, en in FINANCIAL_TERMS.items():
        if query in he or query.lower() in en.lower():
            results[he] = en
    return results

def main():
    parser = argparse.ArgumentParser(description="Hebrew financial term glossary")
    parser.add_argument("--search", help="Search for a term (Hebrew or English)")
    parser.add_argument("--all", action="store_true", help="Show all terms")
    args = parser.parse_args()

    if args.search:
        results = search_terms(args.search)
        if results:
            print(f"Found {len(results)} match(es):\n")
            for he, en in results.items():
                print(f"  {he} = {en}")
        else:
            print(f"No matches for: {args.search}")
    else:
        print("Hebrew Financial Terms Glossary")
        print("=" * 50)
        for he, en in sorted(FINANCIAL_TERMS.items(), key=lambda x: x[1]):
            print(f"  {he:<25} {en}")

if __name__ == "__main__":
    main()
