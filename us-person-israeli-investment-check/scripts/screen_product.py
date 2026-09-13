#!/usr/bin/env python3
"""Screen one Israeli savings product against the PFIC and foreign-trust criteria.

This is a criteria walker, not tax advice and not a classification. It reports which
published criterion a product appears to pass or fail, given what you tell it, so you can put
a precise question to a licensed preparer. It does not read plan documents, does not inspect
any fund's holdings, and cannot determine whether any arrangement is in fact a foreign trust
or a PFIC for US purposes.

Criteria are those in ../references/screening-criteria.md and ../evidence.json.

All USD amounts for the Revenue Procedure 2020-17 limits must already be converted at the US
Treasury Bureau of the Fiscal Service rate on the last day of the tax year.

Usage:
  python3 screen_product.py --example
  python3 screen_product.py --name "keren hishtalmut" --wrapper --purpose general \
      --withdrawal unconditional-after-term --annual-usd 14000
  python3 screen_product.py --name "TASE ETF" --pooled-securities --all-pfic-value-usd 18000
"""

import argparse
import sys

PFIC_PART1_EXCEPTION = {"single": 25_000, "joint": 50_000}
PFIC_INDIRECT_EXCEPTION = 5_000
RP_503 = {"annual": 50_000, "lifetime": 1_000_000}
RP_504 = {"annual": 10_000, "lifetime": 200_000}
RP_504_PURPOSES = {"medical", "disability", "educational"}


def part1_exception_lines(all_pfic_value_usd, indirect_value_usd, filing, excess_distribution,
                          sold_at_gain, qef_elected):
    lines = []
    lost = []
    if excess_distribution:
        lost.append("an excess distribution was received from this fund this year")
    if sold_at_gain:
        lost.append("gain was recognized on selling this fund's stock this year")
    if qef_elected:
        lost.append("a QEF election was made for this fund")
    if lost:
        lines.append("  Part I exceptions (USD 25,000 and USD 5,000): NOT available, because "
                     + " and ".join(lost) + ".")
        return lines

    limit = PFIC_PART1_EXCEPTION[filing]
    if all_pfic_value_usd is None:
        lines.append("  USD 25,000 exception not evaluated: provide --all-pfic-value-usd, the")
        lines.append("  year-end value of ALL PFIC stock (excluding stock held through another")
        lines.append("  US person or another PFIC), not just this fund.")
    elif all_pfic_value_usd <= limit:
        lines.append(f"  USD 25,000 exception: all PFIC stock totals USD {all_pfic_value_usd:,} at")
        lines.append(f"  year end, within USD {limit:,} for a {filing} return, with no excess")
        lines.append("  distribution, no gain on a sale and no QEF election reported. Part I")
        lines.append("  appears not required for this fund.")
    else:
        lines.append(f"  USD 25,000 exception: all PFIC stock totals USD {all_pfic_value_usd:,}, "
                     f"over USD {limit:,}")
        lines.append(f"  for a {filing} return, so it does not appear available.")

    if indirect_value_usd is not None:
        if indirect_value_usd <= PFIC_INDIRECT_EXCEPTION:
            lines.append(f"  USD 5,000 exception: this fund, held through another PFIC, is worth USD "
                         f"{indirect_value_usd:,},")
            lines.append("  within USD 5,000 at year end, so Part I for it appears not required even")
            lines.append("  if total PFIC stock is higher.")
        else:
            lines.append(f"  USD 5,000 exception: holding through another PFIC of USD "
                         f"{indirect_value_usd:,} exceeds USD 5,000.")
    lines.append("  These exceptions relieve Part I only. They do not change how distributions or")
    lines.append("  gains are taxed and do not affect any other reporting duty.")
    return lines


def pfic_screen(pooled, wrapper, all_pfic_value_usd, indirect_value_usd, filing,
                excess_distribution, sold_at_gain, qef_elected):
    """Neither PFIC test can be applied without the fund's holdings; report what IS decidable."""
    lines = []
    if wrapper:
        lines.append("  Wrapper product (pension, gemel, hishtalmut, policy). If the user is treated")
        lines.append("  as owning the arrangement as a grantor trust, they are treated as owning the")
        lines.append("  fund stock its track holds (Reg. 1.1291-1(b)(8)(iii)(D)), which can be")
        lines.append("  indirect PFIC stock. Revenue Procedure 2020-17 does not relieve this. The")
        lines.append("  foreign pension fund exception in Reg. 1.1298-1(c)(4) depends on the treaty,")
        lines.append("  a preparer question. The USD 5,000 exception does NOT reach stock owned")
        lines.append("  through a wrapper; it counts toward the USD 25,000 aggregate. Check the")
        lines.append("  excess-distribution and gain conditions for EACH underlying fund.")
    if not pooled and not wrapper:
        lines.append("  Not described as holding pooled securities, so the PFIC tests are")
        lines.append("  probably not engaged. Confirm what the product actually holds.")
        return lines
    if pooled:
        lines.append("  Holds pooled securities, so the income test (75% passive, section")
        lines.append("  1297(b)) and the asset test (50% passive, section 1297(e)) are both")
        lines.append("  likely met. This is an inference from the tests, NOT an IRS")
        lines.append("  determination about this fund.")
    lines.extend(part1_exception_lines(all_pfic_value_usd, indirect_value_usd, filing,
                                       excess_distribution, sold_at_gain, qef_elected))
    lines.append("  Default treatment absent an election is the section 1291 regime, under")
    lines.append("  which the ENTIRE gain on disposition is treated as an excess")
    lines.append("  distribution. Elections are a preparer's call.")
    return lines


def dollar_limbs(annual_usd, lifetime_usd, limits):
    """Return 'pass', 'fail' or 'unknown' for disjunctive annual-or-lifetime dollar limits."""
    if (annual_usd is not None and annual_usd <= limits["annual"]) or \
       (lifetime_usd is not None and lifetime_usd <= limits["lifetime"]):
        return "pass"
    if annual_usd is not None and lifetime_usd is not None:
        return "fail"
    return "unknown"


def report(lines, title, fails, opens, untested):
    lines.append(title)
    for f in fails:
        lines.append(f"    FAILS {f}")
    for o in opens:
        lines.append(f"    OPEN  {o}")
    if not fails and not opens:
        lines.append("    No failure found on the criteria tested here.")
    elif not fails:
        lines.append("    No failure found yet, but the OPEN items above are unresolved.")
    lines.append(f"    Not tested (plan terms): {untested}.")


def trust_screen(purpose, withdrawal, annual_usd, lifetime_usd, earned_income_only,
                 percentage_limited):
    lines = []
    penalty = withdrawal == "penalty-before-condition"
    # 5.03
    fails_503, open_503 = [], []
    if purpose != "retirement":
        fails_503.append("the exclusive-purpose test (5.03 requires pension or retirement)")
    if withdrawal in ("unconditional", "unconditional-after-term"):
        fails_503.append("criterion 5.03(5): withdrawals neither conditioned on retirement age, "
                         "disability or death nor penalised before them")
    elif penalty:
        open_503.append("criterion 5.03(5) penalty limb: confirm that the early-withdrawal cost "
                        "is a penalty within the meaning of 5.03(5)")
    if earned_income_only is False:
        fails_503.append("criterion 5.03(3), earned-income contributions only")
    elif earned_income_only is None:
        open_503.append("criterion 5.03(3), earned-income contributions only; not stated")
    if not percentage_limited:
        limbs = dollar_limbs(annual_usd, lifetime_usd, RP_503)
        if limbs == "fail":
            fails_503.append(f"criterion 5.03(4): not percentage-limited, annual over USD "
                             f"{RP_503['annual']:,} AND lifetime over USD {RP_503['lifetime']:,}")
        elif limbs == "unknown":
            open_503.append("criterion 5.03(4) is met by a percentage-of-earned-income cap OR "
                            f"annual USD {RP_503['annual']:,} or less OR lifetime USD "
                            f"{RP_503['lifetime']:,} or less; not enough data to tell")
    report(lines, "  Section 5.03, tax-favored foreign retirement trust:", fails_503, open_503,
           "5.03(1), (2) and (6)")

    # 5.04
    fails_504, open_504 = [], []
    if purpose not in RP_504_PURPOSES:
        fails_504.append("its own purpose test (5.04 requires medical, disability or "
                         "educational benefits)")
    else:
        if withdrawal in ("unconditional", "unconditional-after-term"):
            fails_504.append("criterion 5.04(4): withdrawals neither conditioned on the purpose "
                             "benefits nor penalised before them")
        elif withdrawal == "retirement-conditioned":
            open_504.append("criterion 5.04(4) requires conditioning on medical, disability or "
                            "educational benefits, not retirement")
        elif penalty:
            open_504.append("criterion 5.04(4) penalty limb: confirm the early-withdrawal cost "
                            "is a penalty")
    limbs = dollar_limbs(annual_usd, lifetime_usd, RP_504)
    if limbs == "fail":
        fails_504.append(f"criterion 5.04(3): annual over USD {RP_504['annual']:,} AND lifetime "
                         f"over USD {RP_504['lifetime']:,} (no percentage limb in 5.04)")
    elif limbs == "unknown":
        open_504.append(f"criterion 5.04(3), USD {RP_504['annual']:,} annual or USD "
                        f"{RP_504['lifetime']:,} lifetime; not enough data to tell")
    report(lines, "  Section 5.04, tax-favored foreign non-retirement savings trust:", fails_504,
           open_504, "5.04(1) and (2)")

    if fails_503 and fails_504:
        lines.append("")
        lines.append("  Neither exemption appears available on these facts. That does NOT mean")
        lines.append("  the product IS a foreign trust. It means the Revenue Procedure 2020-17")
        lines.append("  safe harbour does not clear it, and a preparer has to reach the")
        lines.append("  underlying question.")
    return lines


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--name", default="the product")
    p.add_argument("--pooled-securities", action="store_true",
                   help="the product is itself a pooled fund of securities (mutual fund, ETF)")
    p.add_argument("--wrapper", action="store_true",
                   help="pension, gemel, hishtalmut or policy that holds funds on a track")
    p.add_argument("--all-pfic-value-usd", "--value-usd", dest="all_pfic_value_usd", type=int,
                   default=None,
                   help="year-end value of ALL PFIC stock held (aggregate, not this fund only)")
    p.add_argument("--indirect-value-usd", type=int, default=None,
                   help="year-end value of this fund held THROUGH ANOTHER PFIC, for the USD 5,000 "
                        "test (not for wrapper holdings)")
    p.add_argument("--filing", choices=["single", "joint"], default="single")
    p.add_argument("--excess-distribution", action="store_true",
                   help="an excess distribution was received from this fund this year")
    p.add_argument("--sold-at-gain", action="store_true",
                   help="gain was recognized on selling this fund's stock this year")
    p.add_argument("--qef-elected", action="store_true",
                   help="a QEF election was made for this fund")
    p.add_argument("--purpose", choices=["retirement", "medical", "disability", "educational",
                                         "general"], default="general")
    p.add_argument("--withdrawal", choices=["retirement-conditioned", "penalty-before-condition",
                                            "unconditional-after-term", "unconditional"],
                   default="unconditional")
    p.add_argument("--annual-usd", type=int, default=None)
    p.add_argument("--lifetime-usd", type=int, default=None)
    p.add_argument("--percentage-limited", action="store_true",
                   help="contributions are capped as a percentage of earned income (5.03(4))")
    p.add_argument("--earned-income-only", dest="earned_only", action="store_true", default=None,
                   help="contributions come only from earned income")
    p.add_argument("--other-income-sources", dest="earned_only", action="store_false",
                   help="contributions come from sources other than earned income")
    p.add_argument("--example", action="store_true")
    a = p.parse_args()
    if a.wrapper and a.indirect_value_usd is not None:
        p.error("--indirect-value-usd is for stock held through another PFIC; the USD 5,000 "
                "exception does not reach stock owned through a wrapper")

    if a.example:
        a.name = "keren hishtalmut (example)"
        a.wrapper, a.filing, a.earned_only = True, "joint", True
        a.purpose, a.withdrawal, a.annual_usd = "general", "unconditional-after-term", 14_000
        print("(example: a salaried employee's keren hishtalmut on an equity track)\n")

    print(f"SCREENING: {a.name}")
    print("A screen against published criteria. NOT a classification and NOT tax advice.\n")
    print("-- PFIC screen --")
    for l in pfic_screen(a.pooled_securities, a.wrapper, a.all_pfic_value_usd,
                         a.indirect_value_usd, a.filing, a.excess_distribution, a.sold_at_gain,
                         a.qef_elected):
        print(l)
    fund_only = a.pooled_securities and not a.wrapper
    print("\n-- Foreign trust screen (Revenue Procedure 2020-17) --")
    if fund_only:
        print("  Not a trust question: a directly held fund or ETF is screened as PFIC stock only.")
    else:
        print("  Scope: this Revenue Procedure exempts from section 6048 REPORTING only. It does")
        print("  not change taxation or any other reporting duty. Eligibility is limited to")
        print("  individuals already compliant on the related income tax.")
        for l in trust_screen(a.purpose, a.withdrawal, a.annual_usd, a.lifetime_usd,
                              a.earned_only, a.percentage_limited):
            print(l)
    print("\n-- Ask your preparer --")
    if not fund_only:
        print(f"  1. Is {a.name} a foreign trust for US purposes on its actual plan terms?")
        print("  2. If it is, does any exemption outside Revenue Procedure 2020-17 apply?")
    if a.pooled_securities or a.wrapper:
        print("  3. What are the underlying fund holdings, and does any of them meet a PFIC test?")
    if a.wrapper:
        print("  4. Does the US-Israel treaty bring this arrangement within Reg. 1.1298-1(c)(4)?")
    print("\n  Dollar limits are measured at the US Treasury Bureau of the Fiscal Service rate")
    print("  on the last day of each tax year.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
