#!/usr/bin/env python3
"""Generate bi-monthly VAT summary reports from Google Sheets data.

Reads exported sheet data (JSON or CSV) and produces a VAT period summary
with totals for income, expenses, VAT collected, input VAT, and net liability.

Usage:
  python scripts/vat-summary.py --input data.json --period 1 --year 2026
  python scripts/vat-summary.py --input data.csv --period 3 --year 2026 --output summary.csv
  python scripts/vat-summary.py --help

VAT Periods (Israel, bi-monthly):
  1 = Jan-Feb    2 = Mar-Apr    3 = May-Jun
  4 = Jul-Aug    5 = Sep-Oct    6 = Nov-Dec
"""

import argparse
import csv
import json
import sys
from datetime import datetime
from pathlib import Path

VAT_RATE = 0.17
MEAL_DEDUCTION_RATE = 0.80
CAR_DEDUCTION_RATE = 0.45

PERIOD_MONTHS = {
    1: (1, 2),
    2: (3, 4),
    3: (5, 6),
    4: (7, 8),
    5: (9, 10),
    6: (11, 12),
}

PERIOD_DUE_DATES = {
    1: "March 15",
    2: "May 15",
    3: "July 15",
    4: "September 15",
    5: "November 15",
    6: "January 15 (next year)",
}


def parse_date(date_str: str) -> datetime | None:
    """Parse DD/MM/YYYY date format."""
    for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y"):
        try:
            return datetime.strptime(date_str.strip(), fmt)
        except ValueError:
            continue
    return None


def parse_amount(amount_str: str) -> float:
    """Parse amount string, handling commas and currency symbols."""
    if not amount_str:
        return 0.0
    cleaned = amount_str.replace(",", "").replace("ILS", "").replace("NIS", "").strip()
    try:
        return float(cleaned)
    except ValueError:
        return 0.0


def load_data(input_path: str) -> list[dict]:
    """Load transaction data from JSON or CSV file."""
    path = Path(input_path)

    if path.suffix == ".json":
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list) and len(data) > 0:
            if isinstance(data[0], list):
                headers = data[0]
                return [dict(zip(headers, row)) for row in data[1:]]
            return data
        return []

    elif path.suffix == ".csv":
        with open(path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return list(reader)

    else:
        print(f"Error: Unsupported file format '{path.suffix}'. Use .json or .csv", file=sys.stderr)
        sys.exit(1)


def filter_by_period(transactions: list[dict], period: int, year: int) -> list[dict]:
    """Filter transactions to the specified bi-monthly VAT period."""
    if period not in PERIOD_MONTHS:
        print(f"Error: Invalid period {period}. Must be 1-6.", file=sys.stderr)
        sys.exit(1)

    start_month, end_month = PERIOD_MONTHS[period]
    filtered = []

    for txn in transactions:
        date_str = txn.get("Date", txn.get("date", ""))
        date = parse_date(date_str)
        if date and date.year == year and start_month <= date.month <= end_month:
            filtered.append(txn)

    return filtered


def compute_summary(transactions: list[dict]) -> dict:
    """Compute VAT summary from filtered transactions."""
    total_income = 0.0
    total_expenses = 0.0
    vat_collected = 0.0
    vat_paid = 0.0
    income_count = 0
    expense_count = 0
    category_totals: dict[str, float] = {}

    for txn in transactions:
        txn_type = txn.get("Type", txn.get("type", "")).strip().lower()
        amount = parse_amount(txn.get("Amount (excl. VAT)", txn.get("amount", "0")))
        vat = parse_amount(txn.get("VAT (17%)", txn.get("vat", "0")))
        category = txn.get("Category", txn.get("category", "Uncategorized"))

        if txn_type == "income":
            total_income += amount
            vat_collected += vat
            income_count += 1
        elif txn_type == "expense":
            total_expenses += amount
            vat_paid += vat
            expense_count += 1

        category_totals[category] = category_totals.get(category, 0) + amount

    net_profit = total_income - total_expenses
    vat_liability = vat_collected - vat_paid

    return {
        "total_income": round(total_income, 2),
        "total_expenses": round(total_expenses, 2),
        "net_profit": round(net_profit, 2),
        "vat_collected": round(vat_collected, 2),
        "vat_paid": round(vat_paid, 2),
        "vat_liability": round(vat_liability, 2),
        "income_count": income_count,
        "expense_count": expense_count,
        "total_transactions": income_count + expense_count,
        "category_totals": category_totals,
    }


def print_summary(summary: dict, period: int, year: int) -> None:
    """Print formatted VAT summary to stdout."""
    start_month, end_month = PERIOD_MONTHS[period]
    month_names = [
        "", "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December",
    ]

    print(f"\n{'='*60}")
    print(f"  VAT Summary - Period {period} ({month_names[start_month]}-{month_names[end_month]} {year})")
    print(f"  Due date: {PERIOD_DUE_DATES[period]}")
    print(f"{'='*60}\n")

    print(f"  Total Income (excl. VAT):     {summary['total_income']:>12,.2f} ILS  ({summary['income_count']} transactions)")
    print(f"  Total Expenses (excl. VAT):   {summary['total_expenses']:>12,.2f} ILS  ({summary['expense_count']} transactions)")
    print(f"  Net Profit:                   {summary['net_profit']:>12,.2f} ILS")
    print()
    print(f"  VAT Collected (on income):    {summary['vat_collected']:>12,.2f} ILS")
    print(f"  VAT Paid (input VAT):         {summary['vat_paid']:>12,.2f} ILS")
    print(f"  ---")
    print(f"  VAT Liability (to pay):       {summary['vat_liability']:>12,.2f} ILS")
    print()

    if summary["category_totals"]:
        print("  Breakdown by Category:")
        for cat, total in sorted(summary["category_totals"].items(), key=lambda x: -x[1]):
            print(f"    {cat:<30} {total:>12,.2f} ILS")

    print(f"\n{'='*60}\n")


def export_csv(summary: dict, period: int, year: int, output_path: str) -> None:
    """Export summary to CSV file."""
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Category", "Total Amount (ILS)", "Total VAT (ILS)", "Transaction Count"])
        writer.writerow(["Total Income", summary["total_income"], summary["vat_collected"], summary["income_count"]])
        writer.writerow(["Total Expenses", summary["total_expenses"], summary["vat_paid"], summary["expense_count"]])
        writer.writerow(["VAT Liability", "", summary["vat_liability"], ""])
        writer.writerow(["Net Profit", summary["net_profit"], "", ""])
        writer.writerow([])
        writer.writerow(["Category Breakdown", "Amount (ILS)", "", ""])
        for cat, total in sorted(summary["category_totals"].items(), key=lambda x: -x[1]):
            writer.writerow([cat, round(total, 2), "", ""])

    print(f"Summary exported to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate bi-monthly VAT summary from Google Sheets data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "VAT Periods (Israel, bi-monthly):\n"
            "  1 = Jan-Feb    2 = Mar-Apr    3 = May-Jun\n"
            "  4 = Jul-Aug    5 = Sep-Oct    6 = Nov-Dec\n"
            "\n"
            "Examples:\n"
            "  %(prog)s --input data.json --period 1 --year 2026\n"
            "  %(prog)s --input data.csv --period 3 --year 2026 --output summary.csv\n"
        ),
    )
    parser.add_argument("--input", required=True, help="Path to JSON or CSV data file")
    parser.add_argument("--period", type=int, required=True, choices=range(1, 7), help="VAT period (1-6)")
    parser.add_argument("--year", type=int, required=True, help="Tax year")
    parser.add_argument("--output", help="Optional CSV output path")

    args = parser.parse_args()

    transactions = load_data(args.input)
    if not transactions:
        print("No transactions found in input file.", file=sys.stderr)
        sys.exit(1)

    filtered = filter_by_period(transactions, args.period, args.year)
    if not filtered:
        print(f"No transactions found for period {args.period} ({args.year}).", file=sys.stderr)
        sys.exit(1)

    summary = compute_summary(filtered)
    print_summary(summary, args.period, args.year)

    if args.output:
        export_csv(summary, args.period, args.year, args.output)


if __name__ == "__main__":
    main()
