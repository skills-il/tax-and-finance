#!/usr/bin/env python3
"""Categorize Israeli bank transactions by spending category.

Applies Israeli-specific merchant categorization to bank transaction data,
supporting common Israeli merchants, supermarkets, and service providers.

Usage:
    python scripts/categorize_transactions.py --json transactions.json
    python scripts/categorize_transactions.py --example
"""

import sys
import json
import argparse
import re
from collections import defaultdict
from dataclasses import dataclass
from typing import Optional

# On a Hebrew-locale Windows console stdout defaults to cp1255, which cannot
# encode the box-drawing characters in the report and kills the run with
# UnicodeEncodeError before a single line is printed. Force UTF-8 so Hebrew
# merchant names and the table rules both survive; `errors="replace"` keeps a
# terminal that still refuses a glyph from crashing the analysis.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


# Israeli merchant patterns mapped to categories
MERCHANT_PATTERNS = {
    # Groceries (mazon)
    r"(?i)(shufersal|שופרסל)": "groceries",
    r"(?i)(rami.?levy|רמי לוי)": "groceries",
    r"(?i)(victory|ויקטורי)": "groceries",
    r"(?i)(yochananof|יוחננוף)": "groceries",
    r"(?i)(osher.?ad|אושר עד)": "groceries",
    r"(?i)(mega|מגה)": "groceries",
    r"(?i)(tiv.?taam|טיב טעם)": "groceries",
    r"(?i)(am.?pm|עם:פם)": "groceries",
    # Transportation (tahaburah)
    # Hebrew side takes a flexible separator like the English one: statements
    # write "רב-קו" with a hyphen far more often than with a space. The trailing
    # guard keeps it off words that merely start with קו, e.g. "רב קומות".
    r"(?i)(rav.?kav|רב[- ]?קו(?![א-ת]))": "transportation",
    r"(?i)(sonol|סונול)": "transportation",
    r"(?i)(paz|פז(?![א-ת]))": "transportation",
    r"(?i)(delek|דלק)": "transportation",
    r"(?i)(gett|גט)": "transportation",
    r"(?i)(yango|יאנגו)": "transportation",
    # Utilities (shartuim)
    # `.?` allowed only one character between the words, so the very common
    # "חברת החשמל" (with the definite article) fell through to Other.
    r"(?i)(israel.?electric|חברת\s*ה?חשמל)": "utilities",
    r"(?i)(mekorot|מקורות)": "utilities",
    r"(?i)(bezeq|בזק)": "utilities",
    r"(?i)(partner|פרטנר)": "utilities",
    r"(?i)(cellcom|סלקום)": "utilities",
    r"(?i)(hot|הוט(?![א-ת]))": "utilities",
    r"(?i)(pelephone|פלאפון)": "utilities",
    # Healthcare (briut)
    r"(?i)(clalit|כללית)": "healthcare",
    r"(?i)(maccabi|מכבי)": "healthcare",
    r"(?i)(meuhedet|מאוחדת)": "healthcare",
    r"(?i)(leumit|לאומית)": "healthcare",
    r"(?i)(super.?pharm|סופר פארם)": "healthcare",
    # Housing (diur)
    r"(?i)(arnona|ארנונה)": "housing",
    r"(?i)(vaad.?bayit|ועד.?בית)": "housing",
    r"(?i)(rent|שכירות)": "housing",
    # Education (chinuch)
    r"(?i)(university|אוניברסיט)": "education",
    r"(?i)(college|מכללה)": "education",
    # Entertainment (bilui)
    r"(?i)(cinema|סינמה|yes.?planet)": "entertainment",
    r"(?i)(netflix)": "entertainment",
    r"(?i)(spotify)": "entertainment",
    r"(?i)(apple.*music|itunes)": "entertainment",
    # Insurance (bituach). NOTE: these are ALSO the names of the companies that manage
    # pension and gemel funds, so the savings patterns below must be tested FIRST.
    r"(?i)(harel|הראל)": "insurance",
    r"(?i)(migdal|מגדל(?![א-ת]))": "insurance",
    r"(?i)(menora|מנורה)": "insurance",
    r"(?i)(clal.?bituach|כלל.?ביטוח)": "insurance",
}

# Tested BEFORE MERCHANT_PATTERNS. A line like "הפקדה לקרן פנסיה מגדל" contains both a
# savings word and an insurance-company name; first-match ordering over a single dict
# classified it as insurance, which put pension money into Total Spending and defeated the
# whole savings/spending split. Priority patterns resolve that collision explicitly.
PRIORITY_PATTERNS = {
    r"(?i)(pension|פנסי)": "savings",
    r"(?i)(hishtalmut|השתלמות)": "savings",
    r"(?i)(gemel|גמל)": "savings",
    r"(?i)(kupat.?gemel|קופת.?גמל)": "savings",
}

CATEGORY_NAMES = {
    "groceries": ("Groceries", "mazon"),
    "transportation": ("Transportation", "tahaburah"),
    "utilities": ("Utilities", "shartuim"),
    "healthcare": ("Healthcare", "briut"),
    "housing": ("Housing", "diur"),
    "education": ("Education", "chinuch"),
    "entertainment": ("Entertainment", "bilui"),
    "insurance": ("Insurance", "bituach"),
    "savings": ("Savings", "chisachon"),
    "restaurants": ("Restaurants", "misadot"),
    "shopping": ("Shopping", "kniyot"),
    "other": ("Other", "acher"),
}


def _whole_word(pattern: str) -> str:
    """Prevent a Hebrew pattern from matching in the MIDDLE of a longer Hebrew word.

    Only a leading guard is applied. A trailing guard cannot be applied blanketly because
    several patterns are deliberately stems: "פנסי" has to keep matching "פנסיה", and
    adding a trailing guard silently broke the savings classification. Patterns that must
    match as a complete token carry their own explicit trailing guard in the tables above.
    """
    flags = ""
    if pattern.startswith("(?i)"):
        flags, pattern = "(?i)", pattern[4:]
    return f"{flags}(?<![\u05d0-\u05ea]){pattern}"


def categorize_transaction(description: str) -> str:
    """Categorize a transaction based on merchant description.

    Args:
        description: Transaction merchant description text.

    Returns:
        Category string.
    """
    # Hebrew has no word boundaries that \b understands, so a bare substring pattern
    # matches inside longer words: "פז" (fuel) fires on "פזגז" (cooking gas, a utility),
    # "מגדל" (insurer) fires on "קניון מגדל שלום" (a mall). Wrapping each pattern in
    # Hebrew-letter lookarounds makes Hebrew tokens match as whole words. Latin patterns
    # are unaffected because the lookarounds only exclude Hebrew characters.
    for pattern, category in PRIORITY_PATTERNS.items():
        if re.search(_whole_word(pattern), description):
            return category
    for pattern, category in MERCHANT_PATTERNS.items():
        if re.search(_whole_word(pattern), description):
            return category
    return "other"


def analyze_transactions(transactions: list[dict]) -> dict:
    """Analyze and categorize a list of transactions.

    Args:
        transactions: List of transaction dicts with 'description' and 'amount' keys.

    Returns:
        Analysis dictionary with category totals, top merchants, etc.
    """
    categories = defaultdict(float)
    category_count = defaultdict(int)
    merchants = defaultdict(float)
    credits = defaultdict(float)
    credit_total = 0.0
    categorized = []

    for txn in transactions:
        desc = txn.get("description", "Unknown")
        raw_amount = txn.get("amount", 0) or 0
        amount = abs(raw_amount)
        category = categorize_transaction(desc)

        # A positive amount on a statement line is money coming IN (a refund, a reversal,
        # salary). Counting its absolute value as spending inflates every total and every
        # percentage. Track credits separately and net them against the category.
        if raw_amount > 0:
            credits[category] += raw_amount
            credit_total += raw_amount
        else:
            categories[category] += amount
            merchants[desc] += amount
        category_count[category] += 1
        categorized.append({**txn, "category": category, "is_credit": raw_amount > 0})

    # Money moved into a pension, keren hishtalmut or gemel is NOT spending: it is the
    # user's own money changing pocket. Folding it into "total spending" overstates the
    # figure and distorts every percentage below it (in the shipped example it inflates
    # the total by roughly a quarter). Report the two separately.
    savings = categories.get("savings", 0.0)
    credits_by_category = {k: round(v, 2) for k, v in sorted(credits.items(), key=lambda x: x[1], reverse=True)}
    total = sum(v for k, v in categories.items() if k != "savings")
    total_outflow = total + savings

    # Sort merchants by spending
    # Exclude savings from the merchant ranking: both SKILL files promise "top merchants
    # by spending", and a pension provider topping that list contradicts the split above.
    savings_descs = {t.get("description", "Unknown") for t in categorized if t.get("category") == "savings"}
    top_merchants = sorted(
        ((m, a) for m, a in merchants.items() if m not in savings_descs),
        key=lambda x: x[1], reverse=True,
    )[:10]

    return {
        "total_spending": round(total, 2),
        "total_savings": round(savings, 2),
        "total_outflow": round(total_outflow, 2),
        "total_credits": round(credit_total, 2),
        "credits_by_category": credits_by_category,
        "by_category": {k: round(v, 2) for k, v in sorted(categories.items(), key=lambda x: x[1], reverse=True)},
        "category_counts": dict(category_count),
        "top_merchants": [(m, round(a, 2)) for m, a in top_merchants],
        "transactions": categorized,
    }


def format_analysis(analysis: dict, period: str = "Current") -> str:
    """Format spending analysis for display."""
    lines = [
        f"=== Spending Analysis ({period}) ===",
        "",
        f"  Total Spending: {analysis['total_spending']:>10,.2f} NIS",
        f"  Into Savings:   {analysis['total_savings']:>10,.2f} NIS  (not counted as spending)",
        f"  Total Outflow:  {analysis['total_outflow']:>10,.2f} NIS",
        *([f"  Credits In:     {analysis['total_credits']:>10,.2f} NIS  (refunds/reversals, excluded above)"]
          if analysis.get("total_credits") else []),
        "",
        "  By Category:",
        f"  {'Category':<25} {'Amount':>10}  {'%':>5}",
        f"  {'─' * 45}",
    ]

    # Percentages must divide by the same population the rows come from. The category
    # rows include savings, so dividing by the spending-only figure made the column sum to
    # well over one hundred.
    total = analysis.get("total_outflow") or analysis["total_spending"] or 1
    for category, amount in analysis["by_category"].items():
        en_name, he_name = CATEGORY_NAMES.get(category, (category, ""))
        pct = amount / total * 100
        label = f"{en_name} ({he_name})"
        lines.append(f"  {label:<25} {amount:>10,.2f}  {pct:>4.1f}%")

    lines.extend([
        "",
        "  Top Merchants:",
        f"  {'Merchant':<30} {'Amount':>10}",
        f"  {'─' * 42}",
    ])
    for merchant, amount in analysis["top_merchants"]:
        lines.append(f"  {merchant[:30]:<30} {amount:>10,.2f}")

    return "\n".join(lines)


def generate_example_transactions() -> list[dict]:
    """Generate example Israeli transactions for testing."""
    return [
        {"date": "2026-01-03", "description": "Shufersal Deal", "amount": -450.00},
        {"date": "2026-01-05", "description": "Rav-Kav Charge", "amount": -220.00},
        {"date": "2026-01-06", "description": "Israel Electric Company", "amount": -380.00},
        {"date": "2026-01-08", "description": "Rami Levy", "amount": -320.00},
        {"date": "2026-01-10", "description": "Partner Communications", "amount": -99.00},
        {"date": "2026-01-12", "description": "Arnona Payment", "amount": -850.00},
        {"date": "2026-01-14", "description": "Netflix", "amount": -49.90},
        {"date": "2026-01-15", "description": "Clalit Health Services", "amount": -120.00},
        {"date": "2026-01-18", "description": "Sonol Fuel", "amount": -280.00},
        {"date": "2026-01-20", "description": "Super Pharm", "amount": -95.00},
        {"date": "2026-01-22", "description": "Shufersal Online", "amount": -510.00},
        {"date": "2026-01-25", "description": "Harel Insurance", "amount": -450.00},
        {"date": "2026-01-27", "description": "Pension Contribution", "amount": -1200.00},
        {"date": "2026-01-28", "description": "Random Store", "amount": -150.00},
        {"date": "2026-01-30", "description": "Yes Planet Cinema", "amount": -85.00},
    ]


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Categorize Israeli bank transactions"
    )
    parser.add_argument("--json", type=str, help="JSON file with transactions")
    parser.add_argument("--period", type=str, default="Current", help="Period label")
    parser.add_argument(
        "--example", action="store_true", help="Run with example transactions"
    )
    parser.add_argument(
        "--output-json", action="store_true",
        help="Output categorized transactions as JSON"
    )

    args = parser.parse_args()

    if args.example:
        transactions = generate_example_transactions()
        analysis = analyze_transactions(transactions)
        # --output-json must be honoured here too. It is documented as a general flag, so
        # returning the human-readable table for --example --output-json hands an agent
        # text it cannot parse.
        if args.output_json:
            print(json.dumps(analysis, ensure_ascii=False, indent=2))
        else:
            print(format_analysis(analysis, "January 2026 (Example)"))
        return

    if args.json:
        try:
            # encoding is explicit: bank exports are UTF-8, while open() on a
            # Hebrew-locale Windows defaults to cp1255 and mangles or rejects
            # Hebrew merchant names. utf-8-sig also strips the BOM that Israeli
            # bank and credit-card exports commonly carry.
            with open(args.json, encoding="utf-8-sig") as f:
                transactions = json.load(f)
        except FileNotFoundError:
            print(f"Error: File not found: {args.json}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON: {e}")
            sys.exit(1)

        analysis = analyze_transactions(transactions)

        if args.output_json:
            print(json.dumps(analysis, indent=2, ensure_ascii=False))
        else:
            print(format_analysis(analysis, args.period))
        return

    parser.print_help()


if __name__ == "__main__":
    main()
