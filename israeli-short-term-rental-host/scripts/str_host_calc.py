#!/usr/bin/env python3
"""Profit sheet and tax-exposure map for an Israeli short-term rental host.

NOT tax advice. It computes on the host's own numbers and shows, side by side,
what each tax treatment would cost, flagging which one the Tax Authority's
publicly reported position points to. It never decides the route for the user.

Input: a CSV of bookings with columns
    check_in       YYYY-MM-DD
    nights         integer
    gross          NIS the guest paid for the stay (nightly price + cleaning fee you charged),
                   BEFORE the platform's fee to you
    platform_fee   NIS the platform kept from you for this booking
    direct_cost    NIS you spent on this booking (cleaning, laundry, supplies), may be 0
An older column `payout` (what reached your bank) is accepted, but it understates
gross receipts by the platform fee; add the fee back if you can.

Example:
    python3 str_host_calc.py bookings.csv --year 2026 --fixed-costs 18000 \
        --lives-in --marginal-rate 0.31
    python3 str_host_calc.py --demo        # runs on a built-in sample

Stdlib only.
"""
import argparse
import calendar
import csv
import io
import sys
from collections import defaultdict
from datetime import date, timedelta

# Figures by tax year. Sources are cited in evidence.json of the skill.
EXEMPTION_CEILING = {2024: 5654, 2025: 5654, 2026: 5654, 2027: 5654}   # NIS per month, all household residential rent
SMALL_BUSINESS_CEILING = {2024: 120000, 2025: 120000, 2026: 122833}    # osek patur annual turnover, NIS
VAT_RATE = {2025: 0.18, 2026: 0.18, 2027: 0.18}                         # 18% from 1.1.2025
SECTION_122_RATE = 0.10
REGULAR_ROUTE_MIN_UNDER_60 = 0.31  # rent outside s.122 / exemption, host under 60: from 31% (non-earned income)
LICENCE_UNITS_THRESHOLD = 4        # more than four holiday units with services needs a business licence

DEMO = """check_in,nights,gross,platform_fee,direct_cost
2026-01-09,3,1700,50,180
2026-02-13,2,1135,35,180
2026-03-28,5,2990,90,220
2026-04-02,7,4430,130,260
2026-05-21,4,2420,70,200
2026-06-29,10,7010,210,300
2026-07-16,6,4225,125,240
2026-08-06,9,6390,190,300
2026-10-08,4,2475,75,200
2026-12-24,6,4020,120,240
"""


def load(stream):
    rows, legacy = [], False
    for i, r in enumerate(csv.DictReader(stream), start=2):
        try:
            d = date.fromisoformat(r["check_in"].strip())
            if r.get("gross") not in (None, ""):
                gross = float(r["gross"])
                fee = float(r.get("platform_fee") or 0)
            else:
                gross, fee, legacy = float(r["payout"]), 0.0, True
            rows.append({"date": d, "nights": int(r["nights"]), "gross": gross, "fee": fee,
                         "cost": float(r.get("direct_cost") or 0)})
        except (KeyError, ValueError) as e:
            sys.exit(f"line {i}: bad row {dict(r)} ({e}). Columns: check_in,nights,gross,platform_fee,direct_cost")
    if not rows:
        sys.exit("no bookings found")
    if legacy:
        print("warning: 'payout' used as gross. The tax and VAT base is what the guest paid; add the platform fee back.",
              file=sys.stderr)
    return rows


def fmt(x):
    return f"{x:,.0f}"


def exemption_tax_free(monthly_rent, ceiling):
    """1990 exemption law: full up to the ceiling, then the ceiling reduced by the
    excess, zero at twice the ceiling."""
    if monthly_rent <= ceiling:
        return monthly_rent
    return max(0.0, ceiling - (monthly_rent - ceiling))


def spread_by_night(r, year):
    """Split a booking's amount across the months its nights fall in."""
    out = defaultdict(float)
    per = r["gross"] / r["nights"]
    for k in range(r["nights"]):
        d = r["date"] + timedelta(days=k)
        if d.year == year:
            out[d.month] += per
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv", nargs="?", help="bookings CSV (see columns above)")
    ap.add_argument("--demo", action="store_true", help="run on a built-in sample year")
    ap.add_argument("--year", type=int, default=2026, help="tax year of the bookings")
    ap.add_argument("--fixed-costs", type=float, default=0.0,
                    help="annual running costs of the unit, NIS (arnona, utilities, internet, insurance, maintenance)")
    ap.add_argument("--lives-in", action="store_true",
                    help="the host lives in the unit when it is not rented: only the rented share of running costs is deductible")
    ap.add_argument("--rented-share", type=float, default=None,
                    help="share of running costs that belongs to the rental (0-1); default with --lives-in: nights booked / days in year")
    ap.add_argument("--other-rent", type=float, default=0.0,
                    help="other residential rent the household receives, NIS per month (shares the exemption ceiling)")
    ap.add_argument("--marginal-rate", type=float, default=None,
                    help="the host's own marginal income-tax rate as a fraction, e.g. 0.31, from their accountant or last assessment")
    ap.add_argument("--age-60-plus", action="store_true", help="host is 60 or older (lower brackets on the regular rent route)")
    ap.add_argument("--units", type=int, default=1, help="number of units the host rents short-term")
    ap.add_argument("--vat-registered", action="store_true",
                    help="host is an osek murshe and the gross figures include VAT")
    a = ap.parse_args(argv)

    if a.demo:
        rows = load(io.StringIO(DEMO))
    elif a.csv:
        with open(a.csv, newline="", encoding="utf-8") as f:
            rows = load(f)
    else:
        ap.error("give a bookings CSV or --demo")
    if a.marginal_rate is not None and not (0 <= a.marginal_rate < 1):
        ap.error("--marginal-rate is a fraction, e.g. 0.31")
    if a.rented_share is not None and not (0 <= a.rented_share <= 1):
        ap.error("--rented-share is a fraction between 0 and 1")
    years = {r["date"].year for r in rows}
    if years != {a.year}:
        print(f"warning: bookings span {sorted(years)} but --year is {a.year}; split the file by tax year",
              file=sys.stderr)

    vat = VAT_RATE.get(a.year) if a.vat_registered else None
    net = (lambda x: x / (1 + vat)) if vat else (lambda x: x)
    days = 366 if calendar.isleap(a.year) else 365
    total_nights = sum(r["nights"] for r in rows)
    share = a.rented_share if a.rented_share is not None else (total_nights / days if a.lives_in else 1.0)
    fixed_ded = a.fixed_costs * share

    # 1. Per-booking sheet
    fixed_per_night = fixed_ded / total_nights if total_nights else 0
    print("PER-BOOKING PROFIT SHEET (NIS)" + (" , amounts net of VAT" if vat else ""))
    print(f"{'check-in':<11} {'nights':>6} {'gross':>8} {'fee':>6} {'direct':>7} {'fixed':>7} {'profit':>8} {'/night':>7}")
    tot_gross = tot_fee = tot_cost = 0.0
    monthly = defaultdict(float)
    spill = False
    for r in sorted(rows, key=lambda x: x["date"]):
        # Only the nights inside the tax year count toward it.
        inyear = sum(1 for k in range(r["nights"]) if (r["date"] + timedelta(days=k)).year == a.year)
        if inyear != r["nights"]:
            spill = True
            frac = inyear / r["nights"]
            r = dict(r, gross=r["gross"] * frac, fee=r["fee"] * frac, cost=r["cost"] * frac, nights=inyear)
            if inyear == 0:
                continue
        g = net(r["gross"])
        fx = fixed_per_night * r["nights"]
        p = g - r["fee"] - r["cost"] - fx
        tot_gross += g
        tot_fee += r["fee"]
        tot_cost += r["cost"]
        for m, v in spread_by_night(r, a.year).items():
            monthly[m] += net(v)
        print(f"{r['date'].isoformat():<11} {r['nights']:>6} {fmt(g):>8} {fmt(r['fee']):>6} {fmt(r['cost']):>7} "
              f"{fmt(fx):>7} {fmt(p):>8} {fmt(p / r['nights']):>7}")
    profit = tot_gross - tot_fee - tot_cost - fixed_ded
    raw_gross = tot_gross * (1 + vat) if vat else tot_gross
    if spill:
        print("note: a stay crosses the tax-year boundary; only its nights inside the year are counted here")
    print()
    print(f"nights booked {total_nights} ({total_nights / days:.0%} of the year)")
    print(f"gross receipts {fmt(tot_gross)} | platform fees {fmt(tot_fee)} | direct {fmt(tot_cost)} | "
          f"running costs {fmt(a.fixed_costs)} x {share:.0%} deductible = {fmt(fixed_ded)} | profit before tax {fmt(profit)}")
    if a.lives_in or share < 1:
        print("  (the host's own use of the flat is a personal expense: only the rental share of running costs counts)")

    # 2. VAT
    print("\nVAT")
    ceiling = SMALL_BUSINESS_CEILING.get(a.year)
    if ceiling is None:
        print(f"  the osek patur ceiling for {a.year} is not in this script; check the current figure")
    else:
        status = "ABOVE" if raw_gross > ceiling else "below"
        print(f"  gross receipts {fmt(raw_gross)} are {status} the {a.year} osek patur ceiling of {fmt(ceiling)}")
    if vat:
        print(f"  VAT inside the gross at {vat:.0%}: {fmt(raw_gross - tot_gross)}. Stays by Israeli residents carry the")
        print("  standard rate; a 'tourist' for the zero rate is a visitor on a visa as the VAT Law defines it, so")
        print("  confirm which stays qualify with your accountant before relying on it")
    print("  The Tax Authority said in 2017 that renting a flat to a tourist is generally VAT-liable at a zero rate;")
    print("  the VAT Law's zero rate names lodging in a hotel. Plan on registering for VAT and settle the rate per guest")
    print("  with a professional.")

    # 3. Income tax scenarios
    print("\nINCOME TAX: what each treatment would cost (comparison, not a choice)")
    mr = a.marginal_rate
    if mr is not None:
        print(f"  A. business income (the Tax Authority's reported position for regular short-term renting):")
        print(f"     profit {fmt(profit)} x your marginal rate {mr:.0%} = about {fmt(max(profit, 0) * mr)}")
        print(f"     plus National Insurance on the business profit (not included here); expenses deductible")
    else:
        print("  A. business income: pass --marginal-rate to estimate (expenses deductible, plus National Insurance)")
    s122_base = sum(monthly.values())
    print(f"  B. section 122, flat 10% of gross rent: {fmt(s122_base * SECTION_122_RATE)}  [no expenses; barred for business income]")
    c = EXEMPTION_CEILING.get(a.year)
    if c:
        free = sum(exemption_tax_free(v + a.other_rent, c) - min(a.other_rent, exemption_tax_free(v + a.other_rent, c))
                   for v in monthly.values())
        taxable = s122_base - free
        line = f"  C. exemption route, monthly ceiling {fmt(c)} for all household rent: tax-free {fmt(free)} of {fmt(s122_base)}"
        print(line)
        if mr is not None:
            print(f"     the remaining {fmt(taxable)} at your marginal rate = about {fmt(taxable * max(mr, 0 if a.age_60_plus else REGULAR_ROUTE_MIN_UNDER_60))}")
        print("     [needs a residential tenant and a signed residence-only document]")
    if mr is not None:
        rate = mr if a.age_60_plus else max(mr, REGULAR_ROUTE_MIN_UNDER_60)
        rent_profit = s122_base - tot_fee - tot_cost - fixed_ded
        print(f"  D. regular rent route (not a business, no special track): profit {fmt(rent_profit)} x {rate:.0%} = about {fmt(max(rent_profit, 0) * rate)}")
        print("     " + ("lower brackets may apply from age 60; use your own marginal rate" if a.age_60_plus
                         else "under age 60 rent outside the special tracks is taxed from 31%"))
    print("  Routes B, C and D are shown only so the cost of the classification is visible. Do not pick one on")
    print("  this sheet: the classification of your activity is a question for a tax adviser or accountant.")

    # 4. What the business treatment triggers
    print("\nIF THE ACTIVITY IS A BUSINESS, these usually follow (confirm the details with your accountant):")
    print("  - open an income-tax file and register for VAT before you start (VAT Law section 52)")
    print("  - pay advance tax payments during the year (Income Tax Ordinance section 175)")
    print("  - file an annual return and keep books and a receipt for every booking")
    print("  - check whether you meet National Insurance's self-employed definition, and register if so")

    # 5. Other flags
    print("\nOTHER FLAGS")
    if a.units > LICENCE_UNITS_THRESHOLD:
        print(f"  {a.units} units: renting more than {LICENCE_UNITS_THRESHOLD} holiday units with services needs a business licence")
    print("  selling the flat later: using section 122 adds depreciation back to the sale value for betterment tax")
    print("  check your building's registered bylaws (takanon), your lease and your home insurance before the first guest")


if __name__ == "__main__":
    main()
