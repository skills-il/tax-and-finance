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
    r"(?i)(rav.?kav|רב קו)": "transportation",
    r"(?i)(sonol|סונול)": "transportation",
    r"(?i)(paz|פז)": "transportation",
    r"(?i)(delek|דלק)": "transportation",
    r"(?i)(gett|גט)": "transportation",
    r"(?i)(yango|יאנגו)": "transportation",
    # Utilities (shartuim)
    r"(?i)(israel.?electric|חברת.?חשמל)": "utilities",
    r"(?i)(mekorot|מקורות)": "utilities",
    r"(?i)(bezeq|בזק)": "utilities",
    r"(?i)(partner|פרטנר)": "utilities",
    r"(?i)(cellcom|סלקום)": "utilities",
    r"(?i)(hot|הוט)": "utilities",
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
    # Insurance (bituach)
    r"(?i)(harel|הראל)": "insurance",
    r"(?i)(migdal|מגדל)": "insurance",
    r"(?i)(menora|מנורה)": "insurance",
    r"(?i)(clal.?bituach|כלל.?ביטוח)": "insurance",
    # Savings (chisachon)
    r"(?i)(pension|פנסי)": "savings",
    r"(?i)(hishtalmut|השתלמות)": "savings",
    r"(?i)(gemel|גמל)": "savings",
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


def categorize_transaction(description: str) -> str:
    """Categorize a transaction based on merchant description.

    Args:
        description: Transaction merchant description text.

    Returns:
        Category string.
    """
    for pattern, category in MERCHANT_PATTERNS.items():
        if re.search(pattern, description):
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
    categorized = []

    for txn in transactions:
        desc = txn.get("description", "Unknown")
        amount = abs(txn.get("amount", 0))
        category = categorize_transaction(desc)

        categories[category] += amount
        category_count[category] += amount and 1
        merchants[desc] += amount
        categorized.append({**txn, "category": category})

    total = sum(categories.values())

    # Sort merchants by spending
    top_merchants = sorted(merchants.items(), key=lambda x: x[1], reverse=True)[:10]

    return {
        "total_spending": round(total, 2),
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
        "",
        "  By Category:",
        f"  {'Category':<25} {'Amount':>10}  {'%':>5}",
        f"  {'─' * 45}",
    ]

    total = analysis["total_spending"] or 1
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
        print(format_analysis(analysis, "January 2026 (Example)"))
        return

    if args.json:
        try:
            with open(args.json) as f:
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
