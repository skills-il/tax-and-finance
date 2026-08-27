#!/usr/bin/env python3
"""
Israeli Crypto Capital Gains Calculator (FIFO Method)

Calculates cryptocurrency capital gains tax per Israeli Tax Authority regulations.
Uses FIFO (First In, First Out) cost basis method. Converts all amounts to NIS.
Supports generating Form 1325 data and advance payment schedules.

Usage:
    python crypto-gains-calculator.py --input transactions.csv --year 2024
    python crypto-gains-calculator.py --input transactions.csv --year 2024 --schedule
    python crypto-gains-calculator.py --input transactions.csv --year 2024 --advance-payments
    python crypto-gains-calculator.py --input transactions.csv --year 2024 --json
    python crypto-gains-calculator.py --demo

CSV Format:
    date,type,asset,amount,price_nis,fee_nis,exchange,notes

    price_nis is the TOTAL shekel consideration for the row, NOT the price per
    unit. Two ETH bought at 8,000 each is price_nis=16000. Getting this backwards
    rescales every gain by the quantity and the tool cannot detect it.

    type must be one of: buy, trade_buy, sell, trade_sell, staking, interest,
    airdrop, mining, fork, transfer, deposit, withdrawal. Any other value
    (including Hebrew labels from an Israeli exchange export) is NOT processed
    and is reported as an unrecognised row.
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
# Section 91(b)(2)'s 30% rate is for the sale of a "נייר ערך בחבר-בני-אדם", a
# SECURITY IN A BODY CORPORATE, by a material shareholder. A fungible token is
# not one, and Circular 05/2018 classifies crypto as a נכס under s.88 taxed
# under s.91 without ever invoking (b)(2). The constant is kept only so a caller
# can pass it explicitly via --tax-rate for a genuine equity-token case; nothing
# in this script selects it, and it must NOT be defaulted onto a crypto disposal.
SECURITY_IN_BODY_CORPORATE_RATE = 0.30
CORPORATE_TAX_RATE = 0.23
# 2025 budget legislation restructured mas yesafim into a 3% base on all income
# above the threshold + 2% additional on capital-source income (effective 5% on
# crypto gains above threshold). This calculator models the post-threshold band
# as a flat 5%, accurate for crypto-only gains; users with a mixed surtax base
# should account for the 3% base separately. The threshold is FROZEN through tax
# year 2027 by the December 2024 indexation-pause amendment, so do not apply CPI.
# The surtax has two limbs. s.121B(a) charges 3% on taxable income above the
# threshold. s.121B(a1), which adds 2% on income from CAPITAL sources, was
# introduced by amendment תשפ"ה-2 and does not reach earlier tax years, so
# applying a flat 5% to a pre-2025 disposal overstates it by two points on the
# whole in-band gain. That is precisely the Voluntary Disclosure computation.
SURTAX_CAPITAL_LIMB_FIRST_YEAR = 2025
SURTAX_RATE = 0.05
SURTAX_THRESHOLD = 721_560  # NIS, frozen 2025-2027 by Dec 2024 amendment
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
    # price_nis is the TOTAL shekel consideration for the whole row, NOT the price
    # per unit. A 2-ETH buy at 8,000 per ETH is price_nis=16000, not 8000. Getting
    # this backwards silently rescales every gain by the quantity: the skill's own
    # Scenario 2, transcribed per-unit, turns a 23,040 gain into a 627 loss.
    price_nis: float  # TOTAL NIS consideration for this row (never per unit)
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
        if self.gain_nis is None:
            return None
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
    other_income: float = 0.0  # non-crypto taxable income (salary, business) for surtax base
    surtax_basis: str = "3% + 2% capital-source limb"
    capital_gains_tax: float = 0.0
    income_tax_estimate: float = 0.0
    surtax: float = 0.0
    total_tax_estimate: float = 0.0
    remaining_lots: dict = field(default_factory=dict)
    unpriced: list = field(default_factory=list)
    unrecognised_rows: int = 0
    warnings: list = field(default_factory=list)


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


# Bitcoin's genesis block. Nothing on-chain predates it, so an earlier
# acquisition date is a data error (a mis-parsed format, or a placeholder),
# not a very early investor.
GENESIS = datetime(2009, 1, 3)


def validate_transactions(transactions: list) -> list:
    """Return a list of blocking data-quality problems in the parsed rows.

    Every check here exists because the calculator would otherwise produce a
    confident, wrong, SILENT answer. A sign-flipped exchange export or a
    mis-parsed date used to yield a zero-tax report with exit code 0, which a
    calling agent cannot distinguish from a genuinely tax-free year.
    """
    problems = []
    today = datetime.now()
    for tx in transactions:
        where = f"{tx.date:%Y-%m-%d} {tx.tx_type} {tx.asset}"
        if tx.amount < 0:
            problems.append(
                f"{where}: negative amount ({tx.amount}). Some exchanges export "
                f"disposals as negative quantities; convert them to positive rows "
                f"with type=sell rather than feeding the sign through.")
        elif tx.amount == 0:
            problems.append(f"{where}: zero amount. A zero-quantity row cannot be "
                            f"priced or matched; remove it or supply the quantity.")
        if tx.price_nis < 0:
            problems.append(f"{where}: negative price_nis ({tx.price_nis}).")
        if tx.fee_nis < 0:
            problems.append(f"{where}: negative fee_nis ({tx.fee_nis}).")
        if tx.date < GENESIS:
            problems.append(
                f"{where}: date precedes the Bitcoin genesis block "
                f"({GENESIS:%Y-%m-%d}). Almost always a mis-parsed date format.")
        if tx.date > today:
            problems.append(f"{where}: date is in the future.")

    # Circular 05/2018 s.3.1.5.1 requires the consideration in a barter trade to be
    # the SAME shekel figure on both sides: the seller's proceeds and the buyer's
    # original cost. Divergent legs silently plant a wrong basis on the acquired
    # asset that only surfaces years later, on its disposal.
    from collections import defaultdict as _dd
    legs = _dd(lambda: {"sell": [], "buy": []})
    for tx in transactions:
        if tx.tx_type == "trade_sell":
            legs[tx.date]["sell"].append(tx)
        elif tx.tx_type == "trade_buy":
            legs[tx.date]["buy"].append(tx)
    for day, sides in legs.items():
        if not sides["sell"] or not sides["buy"]:
            side = "trade_buy" if sides["sell"] else "trade_sell"
            problems.append(
                f"{day:%Y-%m-%d}: a swap leg has no counterpart. Every trade_sell "
                f"needs a matching trade_buy on the same date and vice versa; the "
                f"missing side is {side}.")
            continue
        sold = sum(t.price_nis for t in sides["sell"])
        bought = sum(t.price_nis for t in sides["buy"])
        if sold and abs(sold - bought) > max(1.0, 0.01 * sold):
            problems.append(
                f"{day:%Y-%m-%d}: the two legs of the swap carry different shekel "
                f"values ({sold:,.2f} sold vs {bought:,.2f} bought). Circular "
                f"05/2018 s.3.1.5.1 requires the SAME figure to serve as the "
                f"seller's proceeds and the buyer's original cost, so one of the "
                f"two is wrong and the acquired asset's basis will be wrong too.")
    return problems


# ============================================================
# FIFO Engine
# ============================================================

class FIFOEngine:
    """FIFO cost basis calculator."""

    def __init__(self):
        # Asset -> deque of Lots (oldest first)
        self.lots: dict = defaultdict(deque)
        # Disposals with no matching purchase lot. Never priced, never guessed.
        self.unpriced: list = []
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
            # NO cost basis is known for this portion. Do NOT invent one, and do
            # NOT invent an acquisition date: an earlier version set
            # acquisition_date = the disposal date and acquisition_cost = 0, so
            # the JSON output carried a fabricated acquisition fact and a tax
            # figure that overstated the client's liability, with no warning on
            # the JSON path at all. Record the event as UNPRICED and make the
            # caller resolve it.
            self.unpriced.append({
                "asset": tx.asset,
                "disposal_date": tx.date.strftime("%Y-%m-%d"),
                "unmatched_amount": remaining_to_sell,
                "disposal_proceeds_nis": remaining_to_sell * net_proceeds_per_unit,
            })
            event = GainEvent(
                disposal_date=tx.date,
                acquisition_date=None,
                asset=tx.asset,
                amount=remaining_to_sell,
                acquisition_cost_nis=None,
                disposal_proceeds_nis=remaining_to_sell * net_proceeds_per_unit,
                gain_nis=None,
                holding_days=None,
                is_long_term=False,
                exchange=tx.exchange,
                notes=("UNPRICED: no matching purchase lot. Cost basis is UNKNOWN "
                       "and is NOT assumed to be zero. Supply the acquisition "
                       "record, or use the earliest available market price for "
                       "the asset and document the basis you used."),
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


def process_transactions(transactions: list, year: int, other_income: float = 0.0) -> TaxReport:
    """Process all transactions and generate a tax report for the specified year.

    other_income: the taxpayer's NON-crypto taxable income for the year (salary,
    business, etc.). Required to assess mas yesafim correctly, because the surtax
    threshold applies to TOTAL taxable income, not crypto gains alone.
    """
    engine = FIFOEngine()
    report = TaxReport(year=year, other_income=other_income)
    unknown_types = []

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
            # NOT a warning. An unrecognised type set (a Hebrew-labelled export, or
            # a typo like "purchase") used to be dropped silently, so a file whose
            # every row was discarded still printed a clean zero-tax report with
            # exit 0 and warnings:[] in JSON. A wholly discarded file is the worst
            # possible confident wrong answer.
            unknown_types.append((tx.date, tx.tx_type))

    if unknown_types:
        kinds = sorted({t for _, t in unknown_types})
        report.warnings.append(
            f"UNRECOGNISED TRANSACTION TYPES: {len(unknown_types)} row(s) using "
            f"{kinds} were NOT processed and contribute nothing to any figure below. "
            f"Recognised types are: buy, trade_buy, sell, trade_sell, staking, "
            f"interest, airdrop, mining, fork, transfer, deposit, withdrawal. "
            f"Hebrew or vendor-specific labels must be mapped to these first. "
            f"A zero result here may simply mean the file was discarded.")
        report.unrecognised_rows = len(unknown_types)

    # Filter events for the specified year
    year_gains = [e for e in engine.gain_events if e.disposal_date.year == year]
    year_income = [e for e in engine.income_events if e.date.year == year]

    report.gain_events = year_gains
    report.income_events = year_income

    # Calculate totals. An UNPRICED event has gain_nis=None and is excluded from
    # every total: an unknown basis must not silently become a zero basis.
    for event in year_gains:
        if event.gain_nis is None:
            continue
        if event.gain_nis >= 0:
            report.total_gains += event.gain_nis
        else:
            report.total_losses += abs(event.gain_nis)

    report.net_gain = report.total_gains - report.total_losses
    report.total_income = sum(e.value_nis for e in year_income)

    report.unpriced = [u for u in engine.unpriced
                       if datetime.strptime(u["disposal_date"], "%Y-%m-%d").year == year]
    if report.unpriced:
        total_unpriced = sum(u["disposal_proceeds_nis"] for u in report.unpriced)
        report.warnings.append(
            f"INCOMPLETE: {len(report.unpriced)} disposal(s) totalling "
            f"{total_unpriced:,.2f} NIS in proceeds have NO matching purchase lot, "
            f"so their cost basis is UNKNOWN. They are EXCLUDED from every total "
            f"below, which means the figures UNDERSTATE the gain. Supply the "
            f"acquisition records, or establish a basis (the earliest available "
            f"market price for the asset) and document it, then re-run. Do not "
            f"file on these numbers.")

    # Calculate tax
    report.capital_gains_tax = max(0, report.net_gain * INDIVIDUAL_TAX_RATE)
    # NOTE: income_tax_estimate applies a FLOOR of 25% (the passive-income rate).
    # Staking is debated (25% passive vs marginal), but liquidity-mining/yield-
    # farming, airdrops, and mining are ORDINARY/BUSINESS income taxed at MARGINAL
    # rates up to 47% (plus surtax). This 25% figure can therefore UNDERSTATE the
    # income tax on DeFi/mining receipts; treat it as a lower bound only.
    report.income_tax_estimate = report.total_income * INDIVIDUAL_TAX_RATE
    if report.total_income > 0:
        report.warnings.append(
            "Income events (staking/airdrop/mining/farming) are estimated at the "
            "25% passive-income floor. Yield-farming, airdrops, and mining are "
            "ordinary/business income taxed at MARGINAL rates (up to 47% + surtax); "
            "the income tax above is a LOWER bound. Apply the user's marginal rate."
        )

    # Surtax: the threshold applies to TOTAL taxable income (salary + business +
    # crypto), not crypto alone. Without other_income we cannot assess it reliably.
    total_taxable = report.other_income + report.net_gain + report.total_income
    capital_source = max(0.0, report.net_gain)  # crypto gains are capital-source income
    if total_taxable > SURTAX_THRESHOLD:
        # 2% additional component on the capital-source income sitting above the
        # threshold (the 3% base component on non-capital income is the user's to
        # account for separately - this tool only sees crypto + supplied other_income).
        band_above = total_taxable - SURTAX_THRESHOLD
        capital_in_band = min(capital_source, band_above)
        if year >= SURTAX_CAPITAL_LIMB_FIRST_YEAR:
            report.surtax = capital_in_band * SURTAX_RATE
            report.surtax_basis = "3% + 2% capital-source limb"
        else:
            # The 2% capital-source limb does not reach this year. Do not guess a
            # figure for an earlier regime; say so and let the user establish it.
            report.surtax = 0.0
            report.surtax_basis = "not computed for this year"
            report.warnings.append(
                f"SURTAX NOT COMPUTED for tax year {year}. The 2% capital-source "
                f"limb of s.121B(a1) postdates it, and this tool only models the "
                f"current two-limb structure, so any figure it produced would "
                f"overstate the liability. Establish the surtax position for "
                f"{year} from the rules in force that year. This matters most for "
                f"a Voluntary Disclosure computation over earlier years.")
    if report.other_income == 0 and (report.net_gain + report.total_income) > 0:
        report.warnings.append(
            "Surtax (mas yesafim) was assessed on crypto income ALONE because no "
            "--other-income was supplied. The threshold (NIS 721,560) applies to "
            "TOTAL taxable income; a salaried user may owe surtax even when crypto "
            "gains alone are below it. Re-run with --other-income <salary+other> for "
            "an accurate figure."
        )

    report.total_tax_estimate = report.capital_gains_tax + report.income_tax_estimate + report.surtax
    if report.surtax > 0:
        report.warnings.append(
            "The surtax figure is the s.121B(a1) CAPITAL-SOURCE limb only. The "
            "s.121B(a) 3% base limb on non-capital income above the threshold is "
            "NOT included in the total below and is yours to add.")

    # Advance payments
    for event in year_gains:
        if event.gain_nis is not None and event.gain_nis > 0:
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

def _report_tail(report: TaxReport) -> list:
    """Warnings and disclaimer, shared by the complete and incomplete branches."""
    tail = []
    if report.warnings:
        tail.extend(["", "-" * 70, "WARNINGS", "-" * 70])
        for w in report.warnings:
            tail.append(f"  ! {w}")
    tail.extend(["", "-" * 70,
                 "This is an ESTIMATE, not tax advice. Verify with a CPA before filing.",
                 "-" * 70])
    return tail


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
        "CAPITAL GAINS DISPOSAL SCHEDULE",
        "-" * 70,
    ])

    if report.gain_events:
        for i, event in enumerate(report.gain_events, 1):
            gain_str = ("UNPRICED" if event.gain_nis is None
                        else (f"+{event.gain_nis:,.2f}" if event.gain_nis >= 0
                              else f"{event.gain_nis:,.2f}"))
            # NOT a US-style long/short-term rate distinction: the Israeli rate is
            # 25% either way. The label only flags whether the inflationary split
            # is likely to matter.
            term = "OVER 1Y" if event.is_long_term else "UNDER 1Y"
            acquired = (event.acquisition_date.strftime('%Y-%m-%d')
                        if event.acquisition_date else "UNKNOWN")
            lines.extend([
                f"\n  Event #{i}:",
                f"    Asset:              {event.asset}",
                f"    Amount:             {event.amount:.8f}",
                f"    Acquired:           {acquired}",
                f"    Disposed:           {event.disposal_date.strftime('%Y-%m-%d')}",
                f"    Holding period:     " + (
                    "UNKNOWN" if event.holding_days is None
                    else f"{event.holding_days} days ({term}-term)"),
                f"    Acquisition cost:   " + (
                    "UNKNOWN, no matching purchase lot"
                    if event.acquisition_cost_nis is None
                    else f"{event.acquisition_cost_nis:,.2f} NIS"),
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
    ])

    # A total that EXCLUDES unpriced disposals looks complete and is low, and a
    # taxpayer signs his own return: a plausible low number gets filed, a blank
    # does not. So suppress every summary figure while any disposal is unpriced
    # or any row was not recognised, and show the priced part clearly labelled as
    # a partial. The worst case is not the wholly-unpriced file, it is nine good
    # disposals plus one unpriced, which would otherwise print a nine-tenths
    # total that no reviewer would query.
    incomplete = bool(report.unpriced) or bool(report.unrecognised_rows)
    if incomplete:
        reasons = []
        if report.unpriced:
            reasons.append(f"{len(report.unpriced)} disposal(s) unpriced")
        if report.unrecognised_rows:
            reasons.append(f"{report.unrecognised_rows} row(s) unrecognised")
        lines.extend([
            f"  NET CAPITAL GAIN:           NOT COMPUTABLE",
            f"  TOTAL ESTIMATED TAX:        NOT COMPUTABLE",
            f"  Reason: {', '.join(reasons)}. See WARNINGS below.",
            "",
            f"  Priced portion only, NOT a filing figure:",
            f"    gains {report.total_gains:,.2f} / losses {report.total_losses:,.2f} "
            f"/ net {report.net_gain:,.2f} NIS",
        ])
        return "\n".join(lines + _report_tail(report))

    lines.extend([
        f"  Total capital gains:        {report.total_gains:>15,.2f} NIS",
        f"  Total capital losses:       {report.total_losses:>15,.2f} NIS",
        f"  Net capital gain:           {report.net_gain:>15,.2f} NIS",
        f"  Total other income:         {report.total_income:>15,.2f} NIS",
        "",
        f"  Capital gains tax (25%):    {report.capital_gains_tax:>15,.2f} NIS",
        f"  Income tax (25% floor):     {report.income_tax_estimate:>15,.2f} NIS",
    ])

    if report.other_income > 0:
        lines.append(f"  (Other income for surtax:   {report.other_income:>15,.2f} NIS)")

    if report.surtax > 0:
        lines.append(f"  Surtax, capital limb only:  {report.surtax:>15,.2f} NIS")

    lines.extend([
        f"  -----------------------------------------",
        f"  TOTAL ESTIMATED TAX:        {report.total_tax_estimate:>15,.2f} NIS",
    ])

    # Inflation-indexation warning: this calculator taxes the WHOLE gain at 25%
    # and does not split out the inflation component (sechum hatzmada) under
    # Sections 88 and 91(c). NOTE: 91(c) taxes the CHARGEABLE inflationary amount
    # at 10%; it comes out nil for crypto only because s.88 confines the chargeable
    # part to gain that would have arisen by 31.12.1993. 91(b)(3) is NOT this rule
    # (it is the non-index-linked bond rate) and must not be cited for it. Acquired
    # after 1.1.1994. For lots held over ~12 months in inflationary periods, the
    # figure above OVERSTATES the real tax. Flag the affected events explicitly.
    long_held_gains = [e for e in report.gain_events
                       if e.is_long_term and e.gain_nis is not None and e.gain_nis > 0]
    if long_held_gains:
        lines.extend([
            "",
            "  ! INFLATION-INDEXATION NOTICE (Sections 88 and 91(c)):",
            f"    {len(long_held_gains)} gain event(s) were held 12+ months. This tool",
            "    taxes the full gain at 25% and does NOT deduct the inflation",
            "    component (sechum hatzmada), which is tax-free for individuals.",
            "    The tax above is therefore an UPPER bound for these lots.",
            "    Apply a manual indexation pass or have a CPA review before filing.",
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

    if report.warnings:
        lines.extend([
            "",
            "-" * 70,
            "WARNINGS (read before relying on the figures above)",
            "-" * 70,
        ])
        for w in report.warnings:
            lines.append(f"  ! {w}")

    lines.extend([
        "",
        "=" * 70,
        "DISCLAIMER: This report is for informational purposes only.",
        "Consult a licensed Israeli tax advisor for official tax filing.",
        "Rates and thresholds are based on 2026 regulations (surtax threshold frozen through 2027).",
        "=" * 70,
    ])

    return "\n".join(lines)


def format_disposal_schedule(report: TaxReport) -> str:
    """Format data suitable for Form 1325 filing."""
    lines = [
        "=" * 80,
        f"CAPITAL GAINS DISPOSAL SCHEDULE - TAX YEAR {report.year}",
        "Columns match Form 1399י (הודעה על מכירת נכס). This is NOT an ITA form:",
        "1325 is the ITA's securities aggregation helper and is not the vehicle",
        "for a crypto disposal. Use it as the working paper behind your filing.",
        "=" * 80,
        "",
        f"{'#':>3} | {'Asset':<8} | {'Acquired':<12} | {'Disposed':<12} | "
        f"{'Cost (NIS)':>14} | {'Proceeds (NIS)':>14} | {'Gain/Loss (NIS)':>16}",
        "-" * 95,
    ]

    for i, event in enumerate(report.gain_events, 1):
        gain_str = (f"{'UNPRICED':>16}" if event.gain_nis is None
                    else f"{event.gain_nis:>16,.2f}")
        acquired = (event.acquisition_date.strftime('%d/%m/%Y')
                    if event.acquisition_date else "UNKNOWN")
        cost = (f"{'UNKNOWN':>14}" if event.acquisition_cost_nis is None
                else f"{event.acquisition_cost_nis:>14,.2f}")
        lines.append(
            f"{i:>3} | {event.asset:<8} | {acquired:<12} | "
            f"{event.disposal_date.strftime('%d/%m/%Y'):<12} | "
            f"{cost} | {event.disposal_proceeds_nis:>14,.2f} | {gain_str}"
        )

    lines.extend([
        "-" * 95,
        f"{'':>3}   {'TOTAL':<8}   {'':12}   {'':12}   "
        f"{'':>14}   {'':>14}   {report.net_gain:>16,.2f}",
        "",
        f"Total capital gains tax (25%): {report.capital_gains_tax:,.2f} NIS",
    ])

    if report.surtax > 0:
        lines.append(f"Surtax, capital-source limb only: {report.surtax:,.2f} NIS")

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
        "capital gain event. File Form 1399yod (transaction codes 77=sale,",
        "71=virtual currency) with the payment; Form 1399het is the company",
        "equivalent. The legacy 'Form 7002' is outdated for crypto. Late",
        "payments accrue interest and linkage differences (hafreshei hatzmada).",
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
            "other_income_nis": round(report.other_income, 2),
            "total_tax_estimate_nis": round(report.total_tax_estimate, 2),
        },
        "warnings": report.warnings,
        "unpriced_disposals": report.unpriced,
        "unrecognised_rows": report.unrecognised_rows,
        "complete": not report.unpriced and not report.unrecognised_rows,
        "gain_events": [
            {
                "asset": e.asset,
                "amount": e.amount,
                "acquisition_date": (e.acquisition_date.strftime("%Y-%m-%d")
                                     if e.acquisition_date else None),
                "disposal_date": e.disposal_date.strftime("%Y-%m-%d"),
                "acquisition_cost_nis": (None if e.acquisition_cost_nis is None
                                         else round(e.acquisition_cost_nis, 2)),
                "disposal_proceeds_nis": round(e.disposal_proceeds_nis, 2),
                "gain_nis": None if e.gain_nis is None else round(e.gain_nis, 2),
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
    print(format_disposal_schedule(report))
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
  %(prog)s --input trades.csv --year 2024 --schedule
  %(prog)s --input trades.csv --year 2024 --advance-payments
  %(prog)s --input trades.csv --year 2024 --json
  %(prog)s --demo
        """,
    )

    parser.add_argument("--input", "-i", help="Path to CSV file with transactions")
    parser.add_argument("--year", "-y", type=int, help="Tax year to report on")
    parser.add_argument("--schedule", "--form-1325", dest="schedule",
                        action="store_true",
                        help="Print the capital-gains disposal schedule (columns "
                             "match Form 1399י). --form-1325 is kept as a "
                             "deprecated alias; the output is NOT an ITA form 1325.")
    parser.add_argument("--advance-payments", action="store_true", help="Generate advance payment schedule")
    parser.add_argument("--json", action="store_true", help="Output in JSON format")
    parser.add_argument("--demo", action="store_true", help="Run with demo data")
    parser.add_argument("--tax-rate", type=float, default=0.25,
                        help="Capital gains tax rate (default: 0.25 for individuals)")
    parser.add_argument("--ignore-data-errors", action="store_true",
                        help="Compute anyway despite data-quality problems "
                             "(negative or zero amounts, impossible dates). The "
                             "problems are carried into the report warnings and "
                             "the exit code is still non-zero.")
    parser.add_argument("--other-income", type=float, default=0.0,
                        help="Non-crypto taxable income for the year (salary, business). "
                             "Required for an accurate surtax (mas yesafim) assessment, "
                             "since the threshold applies to TOTAL taxable income.")

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

    problems = validate_transactions(transactions)
    if problems and not args.ignore_data_errors:
        print("Refusing to compute: the input has data-quality problems that would "
              "produce a confident wrong answer.", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        print("Fix the input, or re-run with --ignore-data-errors to compute anyway "
              "(the problems are then carried into the report's warnings).",
              file=sys.stderr)
        sys.exit(2)

    print(f"Loaded {len(transactions)} transactions.", file=sys.stderr)

    report = process_transactions(transactions, args.year, other_income=args.other_income)
    for p in problems:
        report.warnings.append(f"DATA QUALITY (overridden): {p}")

    in_year = [t for t in transactions if t.date.year == args.year]
    if not in_year:
        report.warnings.append(
            f"No transaction in the file falls in tax year {args.year}. The file "
            f"spans {min(t.date for t in transactions):%Y-%m-%d} to "
            f"{max(t.date for t in transactions):%Y-%m-%d}. A zero result here means "
            f"'nothing in this year', not 'no tax due'.")

    if args.json:
        print(format_json(report))
    elif (args.schedule or args.advance_payments) and (report.unpriced or report.unrecognised_rows):
        print("Refusing to emit a filing artefact from an incomplete report.",
              file=sys.stderr)
        for w in report.warnings:
            print(f"  ! {w}", file=sys.stderr)
        print("Resolve the above, then re-run. The full report (no flags) still "
              "prints the per-event schedule for inspection.", file=sys.stderr)
    elif args.schedule or args.advance_payments:
        # Compose rather than shadow. An earlier version's elif chain silently
        # dropped the advance schedule whenever --form-1325 was also passed, and
        # the suppressed output was the time-critical one (the 30-day notice).
        if args.schedule:
            print(format_disposal_schedule(report))
        if args.advance_payments:
            print(format_advance_payments(report))
        if report.warnings:
            print("\n" + "-" * 70)
            print("WARNINGS")
            print("-" * 70)
            for w in report.warnings:
                print(f"  ! {w}")
    else:
        print(format_report(report))

    # A report that excludes unpriced disposals, or that was computed over
    # overridden data errors, is NOT a clean run. Exit non-zero so a calling
    # agent cannot mistake it for one.
    if (report.unpriced or report.unrecognised_rows
            or (problems and args.ignore_data_errors) or not in_year):
        sys.exit(3)


if __name__ == "__main__":
    main()
