#!/usr/bin/env python3
"""Estimate whether a fixed bank fee track beats paying per action.

This is a decision helper, not an official quote. It compares three billing
methods for an Israeli current account (cheshbon over veshav):

  1. No track: pay a separate fee for every action.
  2. Basic track (maslul basi): supervised, up to 10 NIS/month,
     covers up to 10 direct-channel actions + up to 1 teller action.
  3. Expanded track (maslul murchav): price-supervised since 1.9.2022, bank-specific price,
     covers up to 50 direct-channel actions + up to 10 teller actions.

Track transaction limits are fixed by Banking Rules (Customer Service)(Fees),
5768-2008, section 4a. The per-action fees and the exact track prices come from
each bank's current tariff, so they are passed in as inputs, never hardcoded.
Always confirm against the Bank of Israel fee-tracks calculator.

All six price/count flags are REQUIRED (there are no defaults, because every
number comes from a specific bank's tariff). Use --example to see a worked run.

A senior, a customer who has presented a 40%+ disability certificate, or a
customer holding no cash-withdrawal card should pass --entitled: the first 4
teller actions a month are then priced at the direct-channel fee, which can
change which billing method wins for a low-volume account.

Simplification to be aware of: real tariffs price different direct-channel
action types differently; this model uses one flat direct-channel fee.

Usage:
  python3 fee_track_calculator.py --direct 30 --teller 3 \\
      --direct-fee 1.30 --teller-fee 6.50 \\
      --basic-price 10 --expanded-price 26
  python3 fee_track_calculator.py --direct 8 --teller 4 \\
      --direct-fee 1.30 --teller-fee 6.50 \\
      --basic-price 10 --expanded-price 26 --entitled
  python3 fee_track_calculator.py --example
"""

import argparse

# Track limits from the regulation. These are stable; prices are not.
BASIC_DIRECT_LIMIT = 10
BASIC_TELLER_LIMIT = 1
EXPANDED_DIRECT_LIMIT = 50
EXPANDED_TELLER_LIMIT = 10

# Basic-track price is supervised and may not exceed this. Used only as a
# sanity check on user input, never as a substitute for the bank's tariff.
BASIC_PRICE_CAP = 10

# Banking Rules (Customer Service)(Fees), 5768-2008, First Schedule, note to
# item 1(a)(2): a senior (azrach vatik), a customer who has presented a 40%+
# disability certificate, or a customer holding no cash-withdrawal card is
# entitled to this many teller actions a month AT THE DIRECT-CHANNEL PRICE.
# It applies wherever a teller action is billed under item 1(a)(2), i.e. when
# paying per action and to a track's teller OVERAGE. It does not discount the
# fixed track price itself, and it is not a percentage.
ENTITLED_TELLER_ACTIONS = 4


def teller_charge(teller, direct_fee, teller_fee, entitled):
    """Cost of `teller` per-action-billed teller actions.

    With the entitlement, the first ENTITLED_TELLER_ACTIONS of them are priced
    at the direct-channel fee instead of the teller fee.
    """
    if not entitled:
        return teller * teller_fee
    discounted = min(teller, ENTITLED_TELLER_ACTIONS)
    return discounted * direct_fee + (teller - discounted) * teller_fee


def per_action_cost(direct, teller, direct_fee, teller_fee, entitled=False):
    """Monthly cost with no track: every action is billed separately."""
    return direct * direct_fee + teller_charge(teller, direct_fee, teller_fee, entitled)


def track_cost(direct, teller, direct_fee, teller_fee, price, direct_limit, teller_limit,
               entitled=False):
    """Effective monthly cost of a track: fixed price plus estimated overage.

    Actions beyond the track limit are typically billed per action on top of
    the fixed price. We add that overage so the comparison is honest and a
    track that looks cheap on its sticker price is not recommended blindly.
    """
    over_direct = max(0, direct - direct_limit)
    over_teller = max(0, teller - teller_limit)
    overage = over_direct * direct_fee + teller_charge(
        over_teller, direct_fee, teller_fee, entitled)
    if over_direct or over_teller:
        note = "over limit by %d direct and %d teller actions (+%.2f NIS estimated overage)" % (
            over_direct,
            over_teller,
            overage,
        )
    else:
        note = "within track limits"
    return price + overage, note


def recommend(direct, teller, direct_fee, teller_fee, basic_price, expanded_price,
              entitled=False):
    per_action = per_action_cost(direct, teller, direct_fee, teller_fee, entitled)
    basic_cost, basic_note = track_cost(direct, teller, direct_fee, teller_fee,
                                        basic_price, BASIC_DIRECT_LIMIT, BASIC_TELLER_LIMIT,
                                        entitled)
    expanded_cost, expanded_note = track_cost(direct, teller, direct_fee, teller_fee,
                                              expanded_price, EXPANDED_DIRECT_LIMIT,
                                              EXPANDED_TELLER_LIMIT, entitled)

    options = [
        ("No track (per action)", per_action, "billed per action"),
        ("Basic track", basic_cost, basic_note),
        ("Expanded track", expanded_cost, expanded_note),
    ]

    lines = []
    lines.append("Monthly actions: %d direct-channel, %d teller" % (direct, teller))
    if entitled:
        lines.append("Entitlement applied: first %d teller actions a month priced at the"
                     % ENTITLED_TELLER_ACTIONS)
        lines.append("direct-channel fee (senior / 40%+ disability / no cash-withdrawal card).")
    lines.append("")
    lines.append("%-26s %10s   %s" % ("Method", "NIS/month", "Note"))
    lines.append("-" * 70)
    for name, cost, note in options:
        lines.append("%-26s %10.2f   %s" % (name, cost, note))

    # Ties resolve to the earliest option in list order, i.e. "No track".
    # Deliberate: do not move a customer onto a track for a zero saving.
    cheapest = min(options, key=lambda o: o[1])
    lines.append("")
    lines.append("Recommendation: %s at about %.2f NIS/month." % (cheapest[0], cheapest[1]))
    # Round once, then derive the annual figure, so the two printed numbers reconcile.
    savings = round(per_action - cheapest[1], 2)
    if cheapest[0] != "No track (per action)" and savings > 0:
        lines.append("Estimated saving vs paying per action: about %.2f NIS/month (%.2f NIS/year)." % (
            savings,
            savings * 12,
        ))
        lines.append("(Benchmarked against paying per action. If you are already on a track,")
        lines.append("compare against your current track price instead.)")
    lines.append("")
    lines.append("This is an estimate. Verify with the Bank of Israel fee-tracks calculator")
    lines.append("and your bank's current tariff before switching.")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Compare bank fee billing methods.")
    parser.add_argument("--direct", type=int, help="monthly direct-channel actions")
    parser.add_argument("--teller", type=int, help="monthly teller actions")
    parser.add_argument("--direct-fee", type=float, help="fee per direct-channel action (NIS)")
    parser.add_argument("--teller-fee", type=float, help="fee per teller action (NIS)")
    parser.add_argument("--basic-price", type=float, help="basic track price this bank charges (NIS)")
    parser.add_argument("--expanded-price", type=float, help="expanded track price this bank charges (NIS)")
    parser.add_argument("--entitled", action="store_true",
                        help="customer is a senior, has presented a 40%%+ disability "
                             "certificate, or holds no cash-withdrawal card: prices the "
                             "first 4 teller actions a month at the direct-channel fee")
    parser.add_argument("--example", action="store_true", help="run a worked example")
    args = parser.parse_args()

    if args.example:
        # Illustrative inputs only. Replace with your bank's real tariff numbers.
        print("Example: heavy-transaction account, sample tariff numbers.\n")
        print(recommend(direct=40, teller=3, direct_fee=1.30, teller_fee=6.50,
                        basic_price=10, expanded_price=26))
        return

    required = [args.direct, args.teller, args.direct_fee, args.teller_fee,
                args.basic_price, args.expanded_price]
    if any(v is None for v in required):
        parser.error("provide all of --direct --teller --direct-fee --teller-fee "
                     "--basic-price --expanded-price, or use --example")

    for name, value in (("--direct", args.direct), ("--teller", args.teller),
                        ("--direct-fee", args.direct_fee), ("--teller-fee", args.teller_fee),
                        ("--basic-price", args.basic_price),
                        ("--expanded-price", args.expanded_price)):
        if value < 0:
            parser.error("%s cannot be negative (got %s)" % (name, value))

    if args.basic_price > BASIC_PRICE_CAP:
        print("WARNING: --basic-price %.2f exceeds the supervised basic-track cap of %d NIS.\n"
              "Re-read the bank's tariff. If it really charges this, that is itself a\n"
              "complaint ground (see section C of the skill).\n"
              % (args.basic_price, BASIC_PRICE_CAP))

    print(recommend(args.direct, args.teller, args.direct_fee, args.teller_fee,
                    args.basic_price, args.expanded_price, args.entitled))


if __name__ == "__main__":
    main()
