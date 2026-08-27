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


# Israeli merchant patterns mapped to categories
MERCHANT_PATTERNS = {
    # Lines that dominate a real Israeli statement and previously all fell into Other.
    r"(?i)(mashkanta|משכנתא|משכנת)": "housing",
    r"(?i)(halvaa|הלוואה|החזר\s*הלוואה)": "housing",
    r"(?i)(sechar\s*dira|שכר\s*דירה)": "housing",
    r"(?i)(amlat|עמלת|עמלה|דמי\s*ניהול\s*חשבון)": "other",
    r"(?i)(bituach\s*leumi|ביטוח\s*לאומי)": "insurance",
    r"(?i)(mas\s*hachnasa|מס\s*הכנסה)": "other",
    r"(?i)(gan\s*yeladim|גן\s*ילדים|בית\s*ספר|קורס(?![א-ת])|צהרון)": "education",
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
    r"(?i)(paz|פז(?![א-ת]))": "transportation",
    r"(?i)(delek|דלק(?![א-ת]))": "transportation",
    r"(?i)(gett|גט(?![א-ת]))": "transportation",
    r"(?i)(yango|יאנגו)": "transportation",
    # Utilities (shartuim)
    r"(?i)(israel\s*electric|חברת\s*ה?\s*חשמל)": "utilities",
    r"(?i)(mekorot|מקורות)": "utilities",
    r"(?i)(bezeq|בזק(?![א-ת]))": "utilities",
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
    r"(?i)(vaad\s*bayit|ועד\s*ה?\s*בית)": "housing",
    r"(?i)(rent|שכירות)": "housing",
    # Education (chinuch)
    r"(?i)(university|אוניברסיט)": "education",
    r"(?i)(college|מכללה)": "education",
    # Entertainment (bilui)
    r"(?i)(cinema|סינמה|yes.?planet)": "entertainment",

    # Restaurants and cafes. SKILL.md lists them under Entertainment; two unreachable
    # "restaurants"/"shopping" category names were removed rather than left as dead code.
    r"(?i)(restaurant|מסעד|cafe|קפה(?![א-ת])|wolt|וולט|tenbis|10bis|תן ביס|מזנון|פיצה|pizza|בורגר|burger)": "entertainment",
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
    # Cooking-gas (LPG) suppliers are utilities. Tested here, ahead of the Paz fuel
    # pattern in MERCHANT_PATTERNS: v1.3.0 guarded "פז" so it no longer fires on "פזגז",
    # but nothing then matched "פזגז" and a real gas bill fell through to Other.
    r"(?i)(pazgas|פזגז|סופרגז|supergas|אמישראגז|amisragas|דורגז|dorgas)": "utilities",
    r"(?i)(pension|פנסי)": "savings",
    r"(?i)(hishtalmut|השתלמות)": "savings",
    r"(?i)(gemel|גמל(?![א-ת]))": "savings",
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
    "other": ("Other", "acher"),
}


# The one-letter Hebrew prefixes. A statement line says "הפקדה לפנסיה", not "הפקדה פנסיה",
# so any guard that treats the preceding letter as part of the word will refuse to match
# the very phrasing that is normal in Hebrew. Rather than try to express that in a
# lookbehind, the description is expanded before matching (see _expand_hebrew_prefixes).
# ONLY lamed. The other one-letter prefixes are what generate false positives when the
# de-prefixed fragment collides with a pattern: "הדלקה" -> "דלקה" hits the fuel stem,
# "בגט" -> "גט" hits Gett, "מבזק" -> "בזק", "מקפה" -> "קפה", "שגמל" -> "גמל". Lamed is the
# prefix that actually matters here, because the phrasing this exists to rescue is
# "הפקדה לפנסיה" and "ניכוי לגמל", and it introduces none of those collisions.
HEBREW_PREFIXES = "ל"


def _expand_hebrew_prefixes(description: str) -> str:
    """Append a de-prefixed copy of every Hebrew token that starts with a prefix letter.

    Only the prefix lamed is stripped; see HEBREW_PREFIXES for why.

    The leading Hebrew-letter guard in _whole_word() exists to stop a pattern matching in
    the MIDDLE of a longer word, but it cannot tell a prefix letter from a word letter, so
    it also blocks "לפנסיה" and "לגמל". Matching against the original text plus a
    space-separated de-prefixed copy keeps the mid-word protection (the copy is tokenised,
    so a fragment is never adjacent to anything) while letting a prefixed word match.
    """
    tokens = re.findall(r"[\u05d0-\u05ea]+", description)
    stripped = [tok[1:] for tok in tokens if len(tok) > 2 and tok[0] in HEBREW_PREFIXES]
    if not stripped:
        return description
    return description + " " + " ".join(stripped)


def _whole_word(pattern: str) -> str:
    """Make a pattern match as a whole token in BOTH scripts.

    Two guards, because the two scripts fail differently:

    - Hebrew has no word boundary the regex engine understands, so a bare substring fires
      inside a longer word ("פז" inside "פזגז", "מגדל" inside "קניון מגדל שלום"). A leading
      Hebrew-letter lookbehind fixes that. A trailing Hebrew guard cannot be applied
      blanketly because several patterns are deliberately stems: "פנסי" has to keep matching
      "פנסיה". Patterns that must match as a complete token carry their own trailing guard
      in the tables above.
    - Latin needs the opposite treatment and previously had NONE, which is why "hot" fired
      on "Hotel Dan" and "PHOTO SHOP", "mega" on "Omega Watches", "rent" on "Parent Teacher
      Assoc", and "paz" on "Pazzo Pizza". Latin letter guards on both sides fix those and
      cannot affect Hebrew, since Hebrew characters are not in A-Za-z.
    """
    flags = ""
    if pattern.startswith("(?i)"):
        flags, pattern = "(?i)", pattern[4:]
    return (
        f"{flags}(?<![\u05d0-\u05ea])(?<![A-Za-z])"
        f"{pattern}"
        f"(?![A-Za-z])"
    )


def categorize_transaction(description: str) -> str:
    """Categorize a transaction based on merchant description.

    Args:
        description: Transaction merchant description text.

    Returns:
        Category string.
    """
    # Match against the description PLUS a de-prefixed copy of its Hebrew tokens, so that
    # "הפקדה לפנסיה" reaches the savings pattern while "קניון מגדל שלום" still cannot be
    # split mid-word. See _expand_hebrew_prefixes and _whole_word.
    haystack = _expand_hebrew_prefixes(description)
    for pattern, category in PRIORITY_PATTERNS.items():
        if re.search(_whole_word(pattern), haystack):
            return category
    for pattern, category in MERCHANT_PATTERNS.items():
        if re.search(_whole_word(pattern), haystack):
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
        if isinstance(raw_amount, str):
            try:
                raw_amount = float(raw_amount.replace(",", "").replace("\u20aa", "").strip())
            except ValueError:
                print(
                    f"Error: amount {raw_amount!r} on {desc!r} is not a number. "
                    "Bank CSV and Excel exports often quote amounts as text; convert the "
                    "amount column to numbers before running this.",
                    file=sys.stderr,
                )
                sys.exit(1)
        if not isinstance(raw_amount, (int, float)):
            print(f"Error: amount on {desc!r} is a {type(raw_amount).__name__}, not a number.", file=sys.stderr)
            sys.exit(1)
        amount = abs(raw_amount)
        if amount == 0:
            # A zero line carries no signal and otherwise creates an empty merchant row.
            continue
        category = categorize_transaction(desc)

        # A positive amount on a statement line is money coming IN: a refund, a reversal,
        # but ALSO salary, a transfer in, a loan drawdown. Counting its absolute value as
        # spending inflates every total and every percentage, so it is tracked separately.
        # It is NOT netted off the category totals, and NO net view is offered, because
        # nothing here can tell a refund from a salary: both are simply positive amounts.
        # A "net" figure built from that distinction-free bucket subtracts a salary from a
        # spending category and reports a negative category total. If a user wants refunds
        # netted, net the specific refund rows they identify, by hand.
        if raw_amount > 0:
            credits[category] += raw_amount
            credit_total += raw_amount
        else:
            categories[category] += amount
            merchants[desc] += amount
        if raw_amount <= 0:
            category_count[category] += 1
        categorized.append({**txn, "amount": raw_amount, "category": category, "is_credit": raw_amount > 0})

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
        *([f"  Credits In:     {analysis['total_credits']:>10,.2f} NIS  (refunds, reversals, salary, transfers in: excluded above)"]
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
            with open(args.json) as f:
                transactions = json.load(f)
            if not isinstance(transactions, list):
                print(
                    f"Error: {args.json} must contain a JSON array of transaction objects, "
                    f"got {type(transactions).__name__}.",
                    file=sys.stderr,
                )
                sys.exit(1)
            bad = next((i for i, x in enumerate(transactions) if not isinstance(x, dict)), None)
            if bad is not None:
                print(
                    f"Error: {args.json} entry {bad} is a {type(transactions[bad]).__name__}, "
                    "not a transaction object. Each entry needs at least a 'description' and "
                    "an 'amount'.",
                    file=sys.stderr,
                )
                sys.exit(1)
        except FileNotFoundError:
            print(f"Error: File not found: {args.json}", file=sys.stderr)
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
