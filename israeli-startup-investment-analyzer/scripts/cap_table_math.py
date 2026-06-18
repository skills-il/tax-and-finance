#!/usr/bin/env python3
"""Cap-table and dilution math for investment-memo sanity checks.

Deterministic helpers an investor can use to sanity-check the numbers in a
deck: priced-round dilution, option-pool top-up (the "pool shuffle"), SAFE /
convertible conversion (valuation cap + discount, pre vs post-money SAFE), and
pro-rata to maintain ownership.

This computes the arithmetic only. It does NOT value the company, judge the
terms, or account for liquidation preferences (preferences affect proceeds at
exit, not ownership percentages). Use the memo template for the qualitative
judgment.

Usage:
  python3 cap_table_math.py priced --pre 8000000 --invest 2000000 --pool-pct 10
  python3 cap_table_math.py safe --safe 500000 --cap 6000000 --discount 20 --price-pre 8000000
  python3 cap_table_math.py prorata --owned-pct 12 --pre 8000000 --invest 2000000
"""

import argparse


def priced_round(pre_money, investment, new_pool_pct=0.0):
    """Priced round with an optional option-pool top-up taken pre-money.

    When investors require the new option pool to be created BEFORE the money
    goes in (the standard "pool shuffle"), the dilution from the pool falls
    entirely on existing shareholders, not the new investor. pre_money here is
    the negotiated pre-money that already nominally includes the post-round pool
    target expressed as new_pool_pct of the post-money cap table.
    """
    post_money = pre_money + investment
    investor_pct = investment / post_money * 100.0
    pool_pct = new_pool_pct  # expressed as % of post-money fully-diluted
    existing_pct = 100.0 - investor_pct - pool_pct
    return {
        "post_money": post_money,
        "investor_pct": investor_pct,
        "new_pool_pct": pool_pct,
        "existing_holders_pct": existing_pct,
        "dilution_of_existing_pct": investor_pct + pool_pct,
    }


def safe_conversion(safe_amount, valuation_cap, discount_pct, price_round_pre,
                    post_money_safe=False):
    """Convert a SAFE / convertible at the next priced round.

    Returns the conversion price basis and the resulting ownership for the SAFE
    holder. The SAFE converts at the LOWER of (cap-based price) and
    (discount-based price). post_money_safe=True treats the cap as a post-money
    cap (YC post-money SAFE): ownership is then safe_amount / cap directly,
    before further dilution from the new money.
    """
    if post_money_safe:
        cap_ownership = safe_amount / valuation_cap * 100.0
        basis = "post-money cap (ownership locked before new money dilutes it)"
        return {
            "conversion_basis": basis,
            "safe_holder_pct_of_cap": cap_ownership,
            "note": "Post-money SAFE: this % is fixed at the cap; the new round "
                    "money dilutes founders/employees, not this holder, until "
                    "the priced round closes.",
        }
    # pre-money cap convertible: compare cap price vs discount price
    discount_price_factor = 1.0 - (discount_pct / 100.0)
    cap_factor = valuation_cap / price_round_pre if price_round_pre else None
    effective_factor = min(discount_price_factor,
                           cap_factor if cap_factor is not None else discount_price_factor)
    effective_pre = price_round_pre * effective_factor
    safe_holder_pct = safe_amount / (effective_pre + safe_amount) * 100.0
    return {
        "conversion_basis": "cap" if effective_factor == cap_factor else "discount",
        "effective_valuation_for_safe": effective_pre,
        "safe_holder_pct_pre_new_money": safe_holder_pct,
        "note": "Approximate. The cap is almost always the binding term when the "
                "round price is well above the cap.",
    }


def prorata(owned_pct, pre_money, investment):
    """Amount needed in the new round to maintain current ownership %."""
    post_money = pre_money + investment
    target = owned_pct / 100.0
    # Pro-rata of the new round: to hold your ownership %, take your % of the new money.
    new_check = target * investment
    return {
        "post_money": post_money,
        "prorata_check_to_maintain": new_check,
        "note": "Pro-rata check = your current ownership % times the round size.",
    }


def _fmt(d):
    for k, v in d.items():
        if isinstance(v, float):
            print(f"  {k}: {v:,.2f}")
        else:
            print(f"  {k}: {v}")


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    pr = sub.add_parser("priced", help="priced-round dilution")
    pr.add_argument("--pre", type=float, required=True, help="pre-money valuation")
    pr.add_argument("--invest", type=float, required=True, help="investment amount")
    pr.add_argument("--pool-pct", type=float, default=0.0,
                    help="new option pool as %% of post-money (pre-money shuffle)")

    sf = sub.add_parser("safe", help="SAFE / convertible conversion")
    sf.add_argument("--safe", type=float, required=True, help="SAFE amount")
    sf.add_argument("--cap", type=float, required=True, help="valuation cap")
    sf.add_argument("--discount", type=float, default=0.0, help="discount %%")
    sf.add_argument("--price-pre", type=float, default=0.0,
                    help="pre-money of the priced round it converts into")
    sf.add_argument("--post-money", action="store_true",
                    help="treat cap as a post-money (YC) SAFE cap")

    pp = sub.add_parser("prorata", help="pro-rata check to hold ownership")
    pp.add_argument("--owned-pct", type=float, required=True)
    pp.add_argument("--pre", type=float, required=True)
    pp.add_argument("--invest", type=float, required=True)

    a = p.parse_args()
    if a.cmd == "priced":
        _fmt(priced_round(a.pre, a.invest, a.pool_pct))
    elif a.cmd == "safe":
        _fmt(safe_conversion(a.safe, a.cap, a.discount, a.price_pre, a.post_money))
    elif a.cmd == "prorata":
        _fmt(prorata(a.owned_pct, a.pre, a.invest))


if __name__ == "__main__":
    main()
