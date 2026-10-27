#!/usr/bin/env python3
"""Over-withholding estimate for an Israeli salaried person with 2+ payers.

Works month by month over one tax year, then compares the total withheld with
the annual liability.

  Withheld WITHOUT coordination: the payer holding the credit points and
  brackets (Form 101 section he) withholds by the monthly table minus the
  credit points; every other payer withholds maximal tax, 47%, with no credit
  points, plus 3% surtax on the part of ITS OWN monthly payment above the
  monthly surtax threshold. The RECOMMENDED scenario gives the points each
  month to the largest payer paying that month (a new Form 101 at every
  switch); the "points stay" scenario keeps them at the payer entered as main.
  Annual liability: the annual brackets applied once to the combined annual
  income, minus the annual credit points, plus 3% surtax on the combined
  income above the annual threshold. This is what a correct coordination aims
  at and what a year-end refund settles to.

Payers that pay in different months (sequential, e.g. maternity pay then a
job) are modelled as sequential, not concurrent.

Not modelled: the exempt share of a pension (s.9A), pension-contribution
credits and deductions, benefits in kind, qualifying-settlement credits, the
disability exemption, the olim temporary order, daily-table withholding.
Enter the TAXABLE pay. This is an estimate for self-help planning; the Tax
Authority certificate is what payroll applies.

Stdlib only. Payer syntax: AMOUNT[@FROM-TO][:RATE]
  AMOUNT   monthly gross in NIS (>= 0)
  @FROM-TO months paid, 1-12 (default 1-12), e.g. 6000@7-12
  :RATE    only for a secondary payer that documents a different withholding
           rate, as a decimal fraction between 0 and 0.5 (e.g. 0.31, not 31)

Examples:
  python3 coordination_estimate.py --main 12000 --secondary 6000@7-12 --gender m
  python3 coordination_estimate.py --main 9000@1-6 --secondary 9000@7-12 --points 2.25
  python3 coordination_estimate.py --example
"""

import argparse
import math
import sys

# Source: Israel Tax Authority monthly deductions booklet (לוח ניכויים).
# 2026: chapter ב, "שיעורי המס לשנת 2026 (לאחר חוק ריווח מדרגות מס הכנסה)",
#   the table after the 31.3.2026 amendment of section 121, in force from 1.1.2026.
# 2025: chapter ב of the 2025 booklet.
# Each tuple is (monthly upper bound in NIS, marginal rate); None = no upper bound.
# The annual table in both booklets is exactly 12 x these bounds.
BRACKETS = {
    2026: [(7010, 0.10), (10060, 0.14), (19000, 0.20), (25100, 0.31),
           (46690, 0.35), (None, 0.47)],
    2025: [(7010, 0.10), (10060, 0.14), (16150, 0.20), (22440, 0.31),
           (46690, 0.35), (None, 0.47)],
}
# Credit point (נקודת זיכוי, section 33A), NIS per month. Same booklets.
CREDIT_POINT_MONTHLY = {2026: 242, 2025: 242}
# Basic points, Income Tax Ordinance (nevo): s.34 two points for a resident,
# s.36 a quarter point, s.36A half a point for a woman.
BASE_POINTS = {'m': 2.25, 'f': 2.75}
# Section 121B surtax: 3% above 721,560 NIS a year = 60,130 NIS a month.
# Same booklets; an employer paying more than 60,130 a month withholds the
# extra 3% on that salary.
SURTAX_MONTHLY_THRESHOLD = {2026: 60130, 2025: 60130}
SURTAX_RATE = 0.03
# Maximal withholding rate at a non-main payer without coordination.
# Source: gov.il guide "מדריך מס הכנסה להגשת בקשה להקלה במס ולתיאום מס":
# "על המעסיק או המשלם שאינו העיקרי, לנכות מס מרבי מהכנסתכם (47%)".
MAX_RATE = 0.47
MAX_ALLOWED_RATE = 0.5


def bracket_tax(income, year, months=1):
    """Progressive tax; months=12 gives the annual table (bounds x 12)."""
    tax, lower = 0.0, 0.0
    for upper, rate in BRACKETS[year]:
        up = None if upper is None else upper * months
        if up is None or income <= up:
            return tax + (income - lower) * rate
        tax += (up - lower) * rate
        lower = up
    return tax


def monthly_main(pay, points, year):
    credits = points * CREDIT_POINT_MONTHLY[year]
    before = bracket_tax(pay, year)
    used = min(credits, before)
    surtax = max(0.0, pay - SURTAX_MONTHLY_THRESHOLD[year]) * SURTAX_RATE
    return before - used + surtax, credits - used


def monthly_secondary(pay, year, rate=None):
    r = MAX_RATE if rate is None else rate
    return pay * r + max(0.0, pay - SURTAX_MONTHLY_THRESHOLD[year]) * SURTAX_RATE


def annual_liability(total, points, year):
    credits = points * CREDIT_POINT_MONTHLY[year] * 12
    surtax = max(0.0, total - SURTAX_MONTHLY_THRESHOLD[year] * 12) * SURTAX_RATE
    return max(0.0, bracket_tax(total, year, 12) - credits) + surtax


class Payer:
    def __init__(self, amount, first=1, last=12, rate=None):
        self.amount, self.first, self.last, self.rate = amount, first, last, rate

    def active(self, m):
        return self.first <= m <= self.last

    @property
    def months(self):
        return self.last - self.first + 1

    def label(self):
        span = '' if (self.first, self.last) == (1, 12) else f' (months {self.first}-{self.last})'
        return f'{self.amount:,.2f}{span}'


def parse_payer(spec, allow_rate):
    rate = None
    if ':' in spec:
        if not allow_rate:
            raise ValueError('RATE applies only to a secondary payer')
        spec, r = spec.split(':', 1)
        rate = float(r)
        if not math.isfinite(rate) or not 0 <= rate <= MAX_ALLOWED_RATE:
            raise ValueError(f'RATE must be a decimal fraction between 0 and {MAX_ALLOWED_RATE} '
                             f'(e.g. 0.47 for 47%), got {r}')
    first, last = 1, 12
    if '@' in spec:
        spec, span = spec.split('@', 1)
        if '-' not in span:
            raise ValueError(f'months must be given as FROM-TO, e.g. 6000@7-12 for July to December, got @{span}')
        a, b = span.split('-', 1)
        try:
            first, last = int(a), int(b)
        except ValueError:
            raise ValueError(f'months must be whole numbers FROM-TO within 1-12, got @{span}')
        if not (1 <= first <= last <= 12):
            raise ValueError(f'months must be FROM-TO within 1-12, got {span}')
    amount = float(spec)
    if not math.isfinite(amount):
        raise ValueError(f'amount must be a finite number, got {spec}')
    if amount < 0:
        raise ValueError(f'amount must not be negative, got {spec}')
    return Payer(amount, first, last, rate)


def holder_for(month, main, others, mode, prev=None):
    """Which payer holds the credit points in a month.

    mode='declared': the main payer, in the months it pays (as on Form 101 now).
    mode='largest': the largest payer paying that month, whatever its RATE (a
    payer documenting its own rate still withholds by the table while it holds
    the points). On equal pay the points stay with the current holder; failing
    that, with the tied payer that keeps paying longest. Every change of holder
    means a new Form 101.
    """
    if mode == 'declared':
        return main if main.active(month) else None
    cands = [p for p in [main] + others if p.active(month)]
    if not cands:
        return None
    top = max(p.amount for p in cands)
    tied = [p for p in cands if p.amount == top]
    if prev in tied:
        return prev
    return max(tied, key=lambda p: (p.last, p is main))


def withheld(main, others, points, year, mode='declared'):
    """Total withheld over the year, credits not used, surtax withheld, holders by month."""
    total, unused, surtax_w, holders = 0.0, 0.0, 0.0, []
    sur = lambda pay: max(0.0, pay - SURTAX_MONTHLY_THRESHOLD[year]) * SURTAX_RATE
    prev = None
    for m in range(1, 13):
        holder = holder_for(m, main, others, mode, prev)
        if holder is not None:
            prev = holder
        holders.append(holder)
        if holder is not None:
            t, u = monthly_main(holder.amount, points, year)
            total += t
            unused += u
            surtax_w += sur(holder.amount)
        else:
            unused += points * CREDIT_POINT_MONTHLY[year]
        for p in [main] + others:
            if p is holder or not p.active(m):
                continue
            total += monthly_secondary(p.amount, year, p.rate)
            surtax_w += sur(p.amount)
    return total, unused, surtax_w, holders


def fmt(x):
    return f'{x:,.2f}'


def describe_holders(holders, main, others):
    """'months 1-5: other payer 1 (8,000.00); months 6-12: main payer (15,000.00)'."""
    def name(h):
        if h is None:
            return 'nobody (no payer that month)'
        if h is main:
            return f'payer entered as main ({h.amount:,.2f})'
        return f'other payer {others.index(h) + 1} ({h.amount:,.2f})'
    spans, start = [], 1
    for m in range(2, 14):
        if m == 13 or holders[m - 1] is not holders[start - 1]:
            span = f'month {start}' if start == m - 1 else f'months {start}-{m - 1}'
            spans.append(f'{span}: {name(holders[start - 1])}')
            start = m
    return '; '.join(spans)


def report(main, others, points, year):
    payers = [main] + others
    total_income = sum(p.amount * p.months for p in payers)
    liability = annual_liability(total_income, points, year)
    full_year = all((p.first, p.last) == (1, 12) for p in payers)
    overlap = any(sum(1 for p in payers if p.active(m)) > 1 for m in range(1, 13))
    rec, rec_unused, rec_sur, rec_h = withheld(main, others, points, year, 'largest')
    dec, dec_unused, _, dec_h = withheld(main, others, points, year, 'declared')

    print(f'Tax year {year}: credit point {CREDIT_POINT_MONTHLY[year]} NIS/month, {points} points '
          f'= {fmt(points * CREDIT_POINT_MONTHLY[year] * 12)} NIS/year')
    print(f'Payer entered as main {main.label()}')
    for i, p in enumerate(others, 1):
        r = MAX_RATE if p.rate is None else p.rate
        print(f'Other payer {i} {p.label()}, withholding {r * 100:g}% when it does not hold the points')
    print(f'Annual taxable income {fmt(total_income)}; annual liability {fmt(liability)}')

    print('\nRECOMMENDED without a coordination certificate: each month the credit points sit at the '
          'largest payer paying that month (a new Form 101 at every switch).')
    print(f'  Holder: {describe_holders(rec_h, main, others)}')
    print(f'  Withheld {fmt(rec)}')
    d = rec - liability
    if rec_unused > 0.005:
        print(f'  Credit points the withholding did not use: {fmt(rec_unused)}. This is not lost: '
              'the tax is over-withheld until a coordination, or a refund request after the year.')
    if d >= 0:
        print(f'  Over-withholding for the year: {fmt(d)} NIS')
    else:
        short = -d
        annual_surtax = max(0.0, total_income - SURTAX_MONTHLY_THRESHOLD[year] * 12) * SURTAX_RATE
        sur_gap = min(short, max(0.0, annual_surtax - rec_sur))
        rate_gap = short - sur_gap
        causes = []
        if sur_gap > 0.005:
            causes.append(f'{fmt(sur_gap)} is the surtax on combined income above the annual threshold, '
                          'which neither payer withholds')
        if rate_gap > 0.005:
            causes.append(f'{fmt(rate_gap)} comes from a payer withholding at a rate below your marginal rate')
        print(f'  UNDER-withholding for the year: {fmt(short)} NIS ({"; ".join(causes)}). The final tax '
              'is fixed only on an annual return (gov.il guide): set the shortfall aside; for a return '
              'see israeli-tax-returns.')
    if full_year:
        print(f'  Per month (all payers pay all year): {fmt(d / 12)}')

    if any(a is not b for a, b in zip(rec_h, dec_h)):
        print('\nPoints stay where they are now (only at the payer entered as main, in the months it pays):')
        print(f'  Withheld {fmt(dec)}, difference {fmt(dec - liability)}')
        if dec_unused > 0.005:
            print(f'  Credit points not used: {fmt(dec_unused)}')
    if not overlap:
        print('\nThe payers never pay in the same month (sequential). Kolzchut still expects coordination '
              'for sequential sources; anything left over is settled by a refund request after the year.')

    alts = [p for p in payers if (p.first, p.last) == (1, 12) and p is not main]
    if overlap and alts:
        print('\nFor comparison, points at one full-year payer all year:')
        for cand in [main] + alts if (main.first, main.last) == (1, 12) else alts:
            rest = [p for p in payers if p is not cand]
            alt, _, _, _ = withheld(cand, rest, points, year, 'declared')
            print(f'  payer with {cand.label()}: withheld {fmt(alt)}')
    print('\nEstimate only. Enter TAXABLE pay (a pension\'s exempt share under s.9A, pension-'
          'contribution credits and benefits in kind are not modelled). The Tax Authority '
          'certificate is what payroll applies.')
    return {'income': total_income, 'liability': liability, 'withheld': rec, 'difference': d,
            'declared': dec}


EXAMPLES = [
    ('Two salaries all year, 12,000 + 6,000, 2.25 points', '12000', ['6000'], 2.25),
    ('High earner, 50,000 + 20,000, 2.25 points', '50000', ['20000'], 2.25),
    ('Second job from July, 12,000 all year + 6,000 for months 7-12, 2.25 points',
     '12000', ['6000@7-12'], 2.25),
]


def main_cli(argv=None):
    p = argparse.ArgumentParser(
        description='Over-withholding estimate for Israeli tax coordination (teum mas).',
        epilog='Payer syntax: AMOUNT[@FROM-TO][:RATE]. RATE is a decimal fraction 0-0.5, '
               'only for a secondary payer that documents a different rate.')
    p.add_argument('--main', help='payer holding the credit points: AMOUNT[@FROM-TO]')
    p.add_argument('--secondary', action='append', default=[],
                   help='another payer, repeatable: AMOUNT[@FROM-TO][:RATE]')
    g = p.add_mutually_exclusive_group()
    g.add_argument('--points', type=float, help='total credit points for the year')
    g.add_argument('--gender', choices=['f', 'm'],
                   help='use the basic points: 2.75 for a woman, 2.25 for a man')
    p.add_argument('--extra-points', type=float, default=0.0,
                   help='with --gender only: points on top of the basic ones (children, degree, oleh, reservist...)')
    p.add_argument('--year', type=int, default=2026, choices=sorted(BRACKETS),
                   help='tax year table (default 2026)')
    p.add_argument('--example', action='store_true', help='run the three worked examples')
    a = p.parse_args(argv)
    if a.example:
        for title, m, s, pts in EXAMPLES:
            print(f'=== {title} ===')
            report(parse_payer(m, False), [parse_payer(x, True) for x in s], pts, 2026)
            print()
        return 0
    if a.main is None or not a.secondary:
        p.error('--main and at least one --secondary are required (or use --example)')
    if not math.isfinite(a.extra_points) or a.extra_points < 0:
        p.error('--extra-points must be a finite number, not negative')
    if a.points is not None and a.extra_points:
        p.error('--extra-points works only with --gender; with --points give the TOTAL')
    if a.points is None and a.gender is None:
        p.error('give --points (total) or --gender f|m (basic points 2.75 / 2.25)')
    points = a.points if a.points is not None else BASE_POINTS[a.gender] + a.extra_points
    if not math.isfinite(points) or points < 0:
        p.error('points must be a finite number, not negative')
    try:
        main = parse_payer(a.main, False)
        others = [parse_payer(s, True) for s in a.secondary]
    except ValueError as e:
        p.error(str(e))
    report(main, others, points, a.year)
    return 0


if __name__ == '__main__':
    sys.exit(main_cli())
