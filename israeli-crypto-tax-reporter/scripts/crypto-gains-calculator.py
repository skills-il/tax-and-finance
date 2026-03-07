#!/usr/bin/env python3
"""
Israeli Crypto Capital Gains Calculator (FIFO Method)

Calculates cryptocurrency capital gains tax per Israeli Tax Authority regulations.
Uses FIFO (First In, First Out) cost basis method. Converts all amounts to NIS.
Supports generating Form 1325 data and advance payment schedules.

Usage:
    python crypto-gains-calculator.py --input transactions.csv --year 2024
    python crypto-gains-calculator.py --input transactions.csv --year 2024 --form-1325
    python crypto-gains-calculator.py --input transactions.csv --year 2024 --advance-payments
    python crypto-gains-calculator.py --input transactions.csv --year 2024 --json
    python crypto-gains-calculator.py --demo

CSV Format:
    date,type,asset,amount,price_nis,fee_nis,exchange,notes
    2024-01-15,buy,BTC,0.5,75000,375,bits-of-gold,
    2024-08-20,sell,BTC,0.3,120000,600,bits-of-gold,

Requirements:
    Python 3.8+
    No external dependencies
"""

import argparse
import csv
import json
import sys
from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional


# ============================================================
# Constants
# ============================================================

INDIVIDUAL_TAX_RATE = 0.25
SIGNIFICANT_SHAREHOLDER_RATE = 0.30
CORPORATE_TAX_RATE = 0.23
SURTAX_RATE = 0.03
SURTAX_THRESHOLD = 721_560  # NIS, 2024 threshold
ADVANCE_PAYMENT_DAYS = 30


# ============================================================
# Data Types
# ============================================================

@dataclass
class Transaction:
    date: datetime
    tx_type: str  # buy, sell, trade_sell, trade_buy, income, airdrop, fork, mining
    asset: str
    amount: float
    price_nis: float  # total NIS value (not per unit)
    fee_nis: float
    exchange: str
    notes: str

    @property
    def price_per_unit(self) -> float:
        if self.amount == 0:
            return 0.0
        return self.price_nis / self.amount

    @property
    def cost_per_unit(self) -> float:
        """Cost per unit including fees for purchases."""
        if self.amount == 0:
            return 0.0
        return (self.price_nis + self.fee_nis) / self.amount

    @property
    def net_proceeds_per_unit(self) -> float:
        """Net proceeds per unit after fees for sales."""
        if self.amount == 0:
            return 0.0
        return (self.price_nis - self.fee_nis) / self.amount


@dataclass
class Lot:
    """A purchase lot for FIFO tracking."""
    date: datetime
    asset: str
    amount: float
    cost_per_unit_nis: float
    exchange: str
    notes: str

    @property
    def total_cost(self) -> float:
        return self.amount * self.cost_per_unit_nis


@dataclass
class GainEvent:
    """A realized gain/loss event."""
    disposal_date: datetime
    acquisition_date: datetime
    asset: str
    amount: float
    acquisition_cost_nis: float
    disposal_proceeds_nis: float
    gain_nis: float
    holding_days: int
    is_long_term: bool  # 12+ months
    exchange: str
    notes: str

    @property
    def tax_25(self) -> float:
        return max(0, self.gain_nis * INDIVIDUAL_TAX_RATE)


@dataclass
class IncomeEvent:
    """An income event (staking, airdrop, mining)."""
    date: datetime
    asset: str
    amount: float
    value_nis: float
    income_type: str  # staking, airdrop, mining, interest
    notes: str


@dataclass
class AdvancePayment:
    """An advance tax payment (mikdama) due."""
    gain_event_date: datetime
    due_date: datetime
    gain_nis: float
    tax_due_nis: float
    asset: str


@dataclass
class TaxReport:
    year: int
    gain_events: list = field(default_factory=list)
    income_events: list = field(default_factory=list)
    advance_payments: list = field(default_factory=list)
    total_gains: float = 0.0
    total_losses: float = 0.0
    net_gain: float = 0.0
    total_income: float = 0.0
    capital_gains_tax: float = 0.0
    income_tax_estimate: float = 0.0
    surtax: float = 0.0
    total_tax_estimate: float = 0.0
    remaining_lots: dict = field(default_factory=dict)


# ============================================================
# Parser
# ============================================================

def parse_csv(filepath: str) -> list:
    """Parse transaction CSV file."""
    transactions = []

    try:
        with open(filepath, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)

            required_fields = {"date", "type", "asset", "amount", "price_nis"}
            if not required_fields.issubset(set(reader.fieldnames or [])):
                missing = required_fields - set(reader.fieldnames or [])
                print(f"Error: CSV missing required columns: {missing}", file=sys.stderr)
                print("Required columns: date, type, asset, amount, price_nis, fee_nis, exchange, notes", file=sys.stderr)
                sys.exit(1)

            for i, row in enumerate(reader, start=2):
                try:
                    tx = Transaction(
                        date=datetime.strptime(row["date"].strip(), "%Y-%m-%d"),
                        tx_type=row["type"].strip().lower(),
                        asset=row["asset"].strip().upper(),
                        amount=float(row["amount"].strip()),
                        price_nis=float(row["price_nis"].strip()),
                        fee_nis=float(row.get("fee_nis", "0").strip() or "0"),
                        exchange=row.get("exchange", "").strip(),
                        notes=row.get("notes", "").strip(),
                    )
                    transactions.append(tx)
                except (ValueError, KeyError) as e:
                    print(f"Warning: Skipping row {i}: {e}", file=sys.stderr)

    except FileNotFoundError:
        print(f"Error: File not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    transactions.sort(key=lambda t: t.date)
    return transactions


# ============================================================
# FIFO Engine
# ============================================================

class FIFOEngine:
    """FIFO cost basis calculator."""

    def __init__(self):
        # Asset -> deque of Lots (oldest first)
        self.lots: dict = defaultdict(deque)
        self.gain_events: list = []
        self.income_events: list = []

    def process_buy(self, tx: Transaction):
        """Add a purchase lot to the FIFO queue."""
        lot = Lot(
            date=tx.date,
            asset=tx.asset,
            amount=tx.amount,
            cost_per_unit_nis=tx.cost_per_unit,
            exchange=tx.exchange,
            notes=tx.notes,
        )
        self.lots[tx.asset].append(lot)

    def process_sell(self, tx: Transaction) -> list:
        """Process a sale using FIFO, returning gain events."""
        events = []
        remaining_to_sell = tx.amount
        net_proceeds_per_unit = tx.net_proceeds_per_unit

        asset_lots = self.lots[tx.asset]

        while remaining_to_sell > 1e-10 and asset_lots:
            lot = asset_lots[0]

            if lot.amount <= remaining_to_sell + 1e-10:
                # Consume entire lot
                sell_amount = lot.amount
                remaining_to_sell -= sell_amount
                asset_lots.popleft()
            else:
                # Partial lot consumption
                sell_amount = remaining_to_sell
                lot.amount -= sell_amount
                remaining_to_sell = 0

            acquisition_cost = sell_amount * lot.cost_per_unit_nis
            disposal_proceeds = sell_amount * net_proceeds_per_unit
            gain = disposal_proceeds - acquisition_cost
            holding_days = (tx.date - lot.date).days

            event = GainEvent(
                disposal_date=tx.date,
                acquisition_date=lot.date,
                asset=tx.asset,
                amount=sell_amount,
                acquisition_cost_nis=acquisition_cost,
                disposal_proceeds_nis=disposal_proceeds,
                gain_nis=gain,
                holding_days=holding_days,
                is_long_term=holding_days >= 365,
                exchange=tx.exchange,
                notes=tx.notes,
            )
            events.append(event)

        if remaining_to_sell > 1e-10:
            print(
                f"WARNING: FIFO queue exhausted for {tx.asset}. "
                f"Attempted to sell {tx.amount} but only had enough lots for "
                f"{tx.amount - remaining_to_sell:.8f}. "
                f"Missing purchase records for {remaining_to_sell:.8f} {tx.asset}.",
                file=sys.stderr,
            )
            # Create a zero-cost-basis event for the unmatched portion
            event = GainEvent(
                disposal_date=tx.date,
                acquisition_date=tx.date,
                asset=tx.asset,
                amount=remaining_to_sell,
                acquisition_cost_nis=0,
                disposal_proceeds_nis=remaining_to_sell * net_proceeds_per_unit,
                gain_nis=remaining_to_sell * net_proceeds_per_unit,
                holding_days=0,
                is_long_term=False,
                exchange=tx.exchange,
                notes="WARNING: No matching purchase lot found (zero cost basis assumed)",
            )
            events.append(event)

        self.gain_events.extend(events)
        return events

    def process_income(self, tx: Transaction, income_type: str):
        """Process income (staking, airdrop, mining) - creates both income event and cost basis lot."""
        income = IncomeEvent(
            date=tx.date,
            asset=tx.asset,
            amount=tx.amount,
            value_nis=tx.price_nis,
            income_type=income_type,
            notes=tx.notes,
        )
        self.income_events.append(income)

        # Also create a cost basis lot at the income value
        lot = Lot(
            date=tx.date,
            asset=tx.asset,
            amount=tx.amount,
            cost_per_unit_nis=tx.price_per_unit if tx.amount > 0 else 0,
            exchange=tx.exchange,
            notes=f"From {income_type}: {tx.notes}",
        )
        self.lots[tx.asset].append(lot)

    def process_fork(self, tx: Transaction):
        """Process hard fork tokens (zero cost basis)."""
        lot = Lot(
            date=tx.date,
            asset=tx.asset,
            amount=tx.amount,
            cost_per_unit_nis=0,
            exchange=tx.exchange,
            notes=f"Hard fork: {tx.notes}",
        )
        self.lots[tx.asset].append(lot)

    def get_remaining_lots(self) -> dict:
        """Get summary of remaining positions."""
        positions = {}
        for asset, lots in self.lots.items():
            total_amount = sum(lot.amount for lot in lots)
            total_cost = sum(lot.total_cost for lot in lots)
            if total_amount > 1e-10:
                positions[asset] = {
                    "amount": total_amount,
                    "total_cost_nis": total_cost,
                    "avg_cost_per_unit": total_cost / total_amount if total_amount > 0 else 0,
                    "num_lots": len(lots),
                }
        return positions


def process_transactions(transactions: list, year: int) -> TaxReport:
    """Process all transactions and generate a tax report for the specified year."""
    engine = FIFOEngine()
    report = TaxReport(year=year)

    for tx in transactions:
        if tx.tx_type in ("buy", "trade_buy"):
            engine.process_buy(tx)
        elif tx.tx_type in ("sell", "trade_sell"):
            engine.process_sell(tx)
        elif tx.tx_type in ("staking", "interest"):
            engine.process_income(tx, tx.tx_type)
        elif tx.tx_type == "airdrop":
            engine.process_income(tx, "airdrop")
        elif tx.tx_type == "mining":
            engine.process_income(tx, "mining")
        elif tx.tx_type == "fork":
            engine.process_fork(tx)
        elif tx.tx_type in ("transfer", "deposit", "withdrawal"):
            pass  # Transfers are not taxable events
        else:
            print(f"Warning: Unknown transaction type '{tx.tx_type}' on {tx.date.strftime('%Y-%m-%d')}", file=sys.stderr)

    # Filter events for the specified year
    year_gains = [e for e in engine.gain_events if e.disposal_date.year == year]
    year_income = [e for e in engine.income_events if e.date.year == year]

    report.gain_events = year_gains
    report.income_events = year_income

    # Calculate totals
    for event in year_gains:
        if event.gain_nis >= 0:
            report.total_gains += event.gain_nis
        else:
            report.total_losses += abs(event.gain_nis)

    report.net_gain = report.total_gains - report.total_losses
    report.total_income = sum(e.value_nis for e in year_income)

    # Calculate tax
    report.capital_gains_tax = max(0, report.net_gain * INDIVIDUAL_TAX_RATE)
    report.income_tax_estimate = report.total_income * INDIVIDUAL_TAX_RATE  # Conservative 25%

    # Surtax check
    total_taxable = report.net_gain + report.total_income
    if total_taxable > SURTAX_THRESHOLD:
        report.surtax = (total_taxable - SURTAX_THRESHOLD) * SURTAX_RATE

    report.total_tax_estimate = report.capital_gains_tax + report.income_tax_estimate + report.surtax

    # Advance payments
    for event in year_gains:
        if event.gain_nis > 0:
            due_date = event.disposal_date + timedelta(days=ADVANCE_PAYMENT_DAYS)
            payment = AdvancePayment(
                gain_event_date=event.disposal_date,
                due_date=due_date,
                gain_nis=event.gain_nis,
                tax_due_nis=event.gain_nis * INDIVIDUAL_TAX_RATE,
                asset=event.asset,
            )
            report.advance_payments.append(payment)

    report.remaining_lots = engine.get_remaining_lots()
    return report


# ============================================================
# Output Formatters
# ============================================================

def format_report(report: TaxReport) -> str:
    lines = [
        "=" * 70,
        f"ISRAELI CRYPTO TAX REPORT - TAX YEAR {report.year}",
        "=" * 70,
        "",
    ]

    # Capital Gains Section
    lines.extend([
        "-" * 70,
        "CAPITAL GAINS EVENTS (Form 1325)",
        "-" * 70,
    ])

    if report.gain_events:
        for i, event in enumerate(report.gain_events, 1):
            gain_str = f"+{event.gain_nis:,.2f}" if event.gain_nis >= 0 else f"{event.gain_nis:,.2f}"
            term = "LONG" if event.is_long_term else "SHORT"
            lines.extend([
                f"\n  Event #{i}:",
                f"    Asset:              {event.asset}",
                f"    Amount:             {event.amount:.8f}",
                f"    Acquired:           {event.acquisition_date.strftime('%Y-%m-%d')}",
                f"    Disposed:           {event.disposal_date.strftime('%Y-%m-%d')}",
                f"    Holding period:     {event.holding_days} days ({term}-term)",
                f"    Acquisition cost:   {event.acquisition_cost_nis:,.2f} NIS",
                f"    Disposal proceeds:  {event.disposal_proceeds_nis:,.2f} NIS",
                f"    Gain/Loss:          {gain_str} NIS",
            ])
            if event.notes:
                lines.append(f"    Notes:              {event.notes}")
    else:
        lines.append("  No capital gain events for this year.")

    # Income Section
    lines.extend([
        "",
        "-" * 70,
        "INCOME EVENTS (Staking, Airdrops, Mining)",
        "-" * 70,
    ])

    if report.income_events:
        for i, event in enumerate(report.income_events, 1):
            lines.extend([
                f"\n  Income #{i}:",
                f"    Date:     {event.date.strftime('%Y-%m-%d')}",
                f"    Type:     {event.income_type}",
                f"    Asset:    {event.asset}",
                f"    Amount:   {event.amount:.8f}",
                f"    Value:    {event.value_nis:,.2f} NIS",
            ])
    else:
        lines.append("  No income events for this year.")

    # Summary
    lines.extend([
        "",
        "-" * 70,
        "TAX SUMMARY",
        "-" * 70,
        f"  Total capital gains:        {report.total_gains:>15,.2f} NIS",
        f"  Total capital losses:       {report.total_losses:>15,.2f} NIS",
        f"  Net capital gain:           {report.net_gain:>15,.2f} NIS",
        f"  Total other income:         {report.total_income:>15,.2f} NIS",
        "",
        f"  Capital gains tax (25%):    {report.capital_gains_tax:>15,.2f} NIS",
        f"  Income tax (est. 25%):      {report.income_tax_estimate:>15,.2f} NIS",
    ])

    if report.surtax > 0:
        lines.append(f"  Surtax (3%):                {report.surtax:>15,.2f} NIS")

    lines.extend([
        f"  -----------------------------------------",
        f"  TOTAL ESTIMATED TAX:        {report.total_tax_estimate:>15,.2f} NIS",
    ])

    # Remaining positions
    if report.remaining_lots:
        lines.extend([
            "",
            "-" * 70,
            "REMAINING POSITIONS (Cost Basis)",
            "-" * 70,
        ])
        for asset, pos in sorted(report.remaining_lots.items()):
            lines.extend([
                f"  {asset}:",
                f"    Amount:          {pos['amount']:.8f}",
                f"    Total cost:      {pos['total_cost_nis']:,.2f} NIS",
                f"    Avg cost/unit:   {pos['avg_cost_per_unit']:,.2f} NIS",
                f"    Lots:            {pos['num_lots']}",
            ])

    lines.extend([
        "",
        "=" * 70,
        "DISCLAIMER: This report is for informational purposes only.",
        "Consult a licensed Israeli tax advisor for official tax filing.",
        "Rates and thresholds are based on 2024 regulations.",
        "=" * 70,
    ])

    return "\n".join(lines)


def format_form_1325(report: TaxReport) -> str:
    """Format data suitable for Form 1325 filing."""
    lines = [
        "=" * 80,
        f"FORM 1325 DATA - TAX YEAR {report.year}",
        "(Tofes 1325 - Doch Al Revach Hon)",
        "=" * 80,
        "",
        f"{'#':>3} | {'Asset':<8} | {'Acquired':<12} | {'Disposed':<12} | "
        f"{'Cost (NIS)':>14} | {'Proceeds (NIS)':>14} | {'Gain/Loss (NIS)':>16}",
        "-" * 95,
    ]

    for i, event in enumerate(report.gain_events, 1):
        gain_str = f"{event.gain_nis:>16,.2f}"
        lines.append(
            f"{i:>3} | {event.asset:<8} | {event.acquisition_date.strftime('%d/%m/%Y'):<12} | "
            f"{event.disposal_date.strftime('%d/%m/%Y'):<12} | "
            f"{event.acquisition_cost_nis:>14,.2f} | {event.disposal_proceeds_nis:>14,.2f} | {gain_str}"
        )

    lines.extend([
        "-" * 95,
        f"{'':>3}   {'TOTAL':<8}   {'':12}   {'':12}   "
        f"{'':>14}   {'':>14}   {report.net_gain:>16,.2f}",
        "",
        f"Total capital gains tax (25%): {report.capital_gains_tax:,.2f} NIS",
    ])

    if report.surtax > 0:
        lines.append(f"Surtax (3%): {report.surtax:,.2f} NIS")

    return "\n".join(lines)


def format_advance_payments(report: TaxReport) -> str:
    """Format advance payment schedule."""
    lines = [
        "=" * 70,
        f"ADVANCE PAYMENT SCHEDULE (Mikdamot) - {report.year}",
        "=" * 70,
        "",
        f"{'#':>3} | {'Event Date':<12} | {'Due Date':<12} | {'Asset':<8} | "
        f"{'Gain (NIS)':>14} | {'Tax Due (NIS)':>14}",
        "-" * 75,
    ]

    total_advance = 0
    for i, payment in enumerate(report.advance_payments, 1):
        lines.append(
            f"{i:>3} | {payment.gain_event_date.strftime('%d/%m/%Y'):<12} | "
            f"{payment.due_date.strftime('%d/%m/%Y'):<12} | {payment.asset:<8} | "
            f"{payment.gain_nis:>14,.2f} | {payment.tax_due_nis:>14,.2f}"
        )
        total_advance += payment.tax_due_nis

    lines.extend([
        "-" * 75,
        f"{'':>3}   {'':12}   {'':12}   {'TOTAL':8}   {'':>14}   {total_advance:>14,.2f}",
        "",
        "NOTE: Advance payments (mikdamot) are due within 30 days of each",
        "capital gain event. File Form 7002 with the payment. Late payments",
        "accrue interest and linkage differences (hafreshei hatzamda).",
    ])

    return "\n".join(lines)


def format_json(report: TaxReport) -> str:
    """Format report as JSON."""
    data = {
        "tax_year": report.year,
        "summary": {
            "total_gains_nis": round(report.total_gains, 2),
            "total_losses_nis": round(report.total_losses, 2),
            "net_gain_nis": round(report.net_gain, 2),
            "total_income_nis": round(report.total_income, 2),
            "capital_gains_tax_nis": round(report.capital_gains_tax, 2),
            "income_tax_estimate_nis": round(report.income_tax_estimate, 2),
            "surtax_nis": round(report.surtax, 2),
            "total_tax_estimate_nis": round(report.total_tax_estimate, 2),
        },
        "gain_events": [
            {
                "asset": e.asset,
                "amount": e.amount,
                "acquisition_date": e.acquisition_date.strftime("%Y-%m-%d"),
                "disposal_date": e.disposal_date.strftime("%Y-%m-%d"),
                "acquisition_cost_nis": round(e.acquisition_cost_nis, 2),
                "disposal_proceeds_nis": round(e.disposal_proceeds_nis, 2),
                "gain_nis": round(e.gain_nis, 2),
                "holding_days": e.holding_days,
                "is_long_term": e.is_long_term,
            }
            for e in report.gain_events
        ],
        "income_events": [
            {
                "date": e.date.strftime("%Y-%m-%d"),
                "type": e.income_type,
                "asset": e.asset,
                "amount": e.amount,
                "value_nis": round(e.value_nis, 2),
            }
            for e in report.income_events
        ],
        "remaining_positions": {
            asset: {
                "amount": round(pos["amount"], 8),
                "total_cost_nis": round(pos["total_cost_nis"], 2),
                "avg_cost_per_unit_nis": round(pos["avg_cost_per_unit"], 2),
            }
            for asset, pos in report.remaining_lots.items()
        },
    }
    return json.dumps(data, indent=2, ensure_ascii=False)


# ============================================================
# Demo Data
# ============================================================

DEMO_TRANSACTIONS = [
    Transaction(datetime(2024, 1, 15), "buy", "BTC", 0.5, 75000, 375, "bits-of-gold", "Initial BTC purchase"),
    Transaction(datetime(2024, 2, 1), "buy", "ETH", 5.0, 40000, 200, "bit2c", "ETH investment"),
    Transaction(datetime(2024, 3, 10), "buy", "BTC", 0.3, 48000, 240, "binance", "Additional BTC"),
    Transaction(datetime(2024, 4, 15), "staking", "ETH", 0.25, 2200, 0, "defi-protocol", "Q1 staking rewards"),
    Transaction(datetime(2024, 5, 20), "airdrop", "ARB", 500, 2500, 0, "arbitrum", "Airdrop claim"),
    Transaction(datetime(2024, 6, 1), "sell", "BTC", 0.4, 68000, 340, "bits-of-gold", "Partial BTC sale"),
    Transaction(datetime(2024, 7, 15), "sell", "ETH", 3.0, 30000, 150, "bit2c", "Partial ETH sale"),
    Transaction(datetime(2024, 8, 1), "buy", "SOL", 20, 4000, 20, "binance", "SOL purchase"),
    Transaction(datetime(2024, 9, 10), "sell", "ARB", 300, 1800, 9, "binance", "Partial airdrop sale"),
    Transaction(datetime(2024, 10, 1), "staking", "ETH", 0.15, 1500, 0, "defi-protocol", "Q3 staking rewards"),
    Transaction(datetime(2024, 11, 15), "sell", "SOL", 10, 3000, 15, "binance", "Partial SOL sale"),
]


def run_demo():
    """Run a demo with sample transactions."""
    print("Running demo with sample Israeli crypto transactions...")
    print(f"Processing {len(DEMO_TRANSACTIONS)} transactions for 2024\n")

    report = process_transactions(DEMO_TRANSACTIONS, 2024)
    print(format_report(report))
    print()
    print(format_form_1325(report))
    print()
    print(format_advance_payments(report))


# ============================================================
# Main
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="Israeli Crypto Capital Gains Calculator (FIFO)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
CSV Format:
  date,type,asset,amount,price_nis,fee_nis,exchange,notes
  2024-01-15,buy,BTC,0.5,75000,375,bits-of-gold,Initial purchase
  2024-08-20,sell,BTC,0.3,51000,255,bits-of-gold,Partial sale

Transaction types:
  buy         Purchase of crypto with fiat
  sell        Sale of crypto for fiat
  trade_buy   Crypto received in a crypto-to-crypto trade
  trade_sell  Crypto given in a crypto-to-crypto trade
  staking     Staking reward received
  airdrop     Airdrop tokens received
  mining      Mining reward received
  fork        Hard fork tokens received (zero cost basis)
  transfer    Wallet/exchange transfer (not taxable, tracking only)

Examples:
  %(prog)s --input trades.csv --year 2024
  %(prog)s --input trades.csv --year 2024 --form-1325
  %(prog)s --input trades.csv --year 2024 --advance-payments
  %(prog)s --input trades.csv --year 2024 --json
  %(prog)s --demo
        """,
    )

    parser.add_argument("--input", "-i", help="Path to CSV file with transactions")
    parser.add_argument("--year", "-y", type=int, help="Tax year to report on")
    parser.add_argument("--form-1325", action="store_true", help="Generate Form 1325 data")
    parser.add_argument("--advance-payments", action="store_true", help="Generate advance payment schedule")
    parser.add_argument("--json", action="store_true", help="Output in JSON format")
    parser.add_argument("--demo", action="store_true", help="Run with demo data")
    parser.add_argument("--tax-rate", type=float, default=0.25,
                        help="Capital gains tax rate (default: 0.25 for individuals)")

    args = parser.parse_args()

    if args.demo:
        run_demo()
        return

    if not args.input or not args.year:
        parser.error("--input and --year are required (or use --demo)")

    transactions = parse_csv(args.input)
    if not transactions:
        print("No valid transactions found in the input file.", file=sys.stderr)
        sys.exit(1)

    print(f"Loaded {len(transactions)} transactions.", file=sys.stderr)

    report = process_transactions(transactions, args.year)

    if args.json:
        print(format_json(report))
    elif args.form_1325:
        print(format_form_1325(report))
    elif args.advance_payments:
        print(format_advance_payments(report))
    else:
        print(format_report(report))


if __name__ == "__main__":
    main()
