#!/usr/bin/env python3
"""Screen one Israeli savings product against the PFIC and foreign-trust criteria.

This is a criteria walker, not tax advice and not a classification. It reports which
published criterion a product appears to pass or fail, given what you tell it, so you can put
a precise question to a licensed preparer. It does not read plan documents, does not inspect
any fund's holdings, and cannot determine whether any arrangement is in fact a foreign trust
or a PFIC for US purposes.

Criteria are those in ../references/screening-criteria.md and ../evidence.json.

Usage:
  python3 screen_product.py --example
  python3 screen_product.py --name "keren hishtalmut" --pooled-securities \
      --annual-usd 14000 --purpose general --withdrawal unconditional-after-term
"""

import argparse
import sys

PFIC_DE_MINIMIS = {"single": 25_000, "joint": 50_000}
RP_503 = {"annual": 50_000, "lifetime": 1_000_000}
RP_504 = {"annual": 10_000, "lifetime": 200_000}
RP_504_PURPOSES = {"medical", "disability", "educational"}


def pfic_screen(pooled, value_usd, filing):
    """Neither test can be applied without the fund's holdings; report what IS decidable."""
    lines = []
    if pooled:
        lines.append("  Holds pooled securities, so the income test (75% passive, section")
        lines.append("  1297(b)) and the asset test (50% passive, section 1297(e)) are both")
        lines.append("  likely met. This is an inference from the tests, NOT an IRS")
        lines.append("  determination about this fund.")
        limit = PFIC_DE_MINIMIS[filing]
        if value_usd is not None and value_usd <= limit:
            lines.append(f"  De minimis: holding USD {value_usd:,} is at or under the USD "
                         f"{limit:,} limit for a {filing} return,")
            lines.append("  so the Form 8621 FILING exception appears available. It excepts")
            lines.append("  filing only. It does not change how distributions or gains are")
            lines.append("  taxed, and does not affect any other reporting duty.")
        elif value_usd is not None:
            lines.append(f"  De minimis: holding USD {value_usd:,} EXCEEDS the USD {limit:,} "
                         f"limit for a {filing} return,")
            lines.append("  so the filing exception does not appear available.")
        else:
            lines.append("  De minimis not evaluated: provide --value-usd to test it.")
        lines.append("  Default treatment absent an election is the section 1291 regime, under")
        lines.append("  which the ENTIRE gain on disposition is treated as an excess")
        lines.append("  distribution. Elections are a preparer's call.")
    else:
        lines.append("  Not described as holding pooled securities, so the PFIC tests are")
        lines.append("  probably not engaged. Confirm what the product actually holds.")
    return lines


def trust_screen(purpose, withdrawal, annual_usd, lifetime_usd, earned_income_only):
    lines = []
    # 5.03
    fails_503 = []
    if purpose != "retirement":
        fails_503.append("the exclusive-purpose test (5.03 requires pension or retirement)")
    if withdrawal != "retirement-conditioned":
        fails_503.append("criterion 5.03(5), the withdrawal condition")
    if earned_income_only is False:
        fails_503.append("criterion 5.03(3), earned-income contributions only")
    if annual_usd is not None and annual_usd > RP_503["annual"]:
        fails_503.append(f"criterion 5.03(4), annual contributions exceed "
                         f"USD {RP_503['annual']:,}")
    if lifetime_usd is not None and lifetime_usd > RP_503["lifetime"]:
        fails_503.append(f"criterion 5.03(4), lifetime contributions exceed "
                         f"USD {RP_503['lifetime']:,}")
    lines.append("  Section 5.03, tax-favored foreign retirement trust:")
    if fails_503:
        for f in fails_503:
            lines.append(f"    FAILS {f}")
    else:
        lines.append("    Appears to meet the criteria tested here. Criteria 5.03(1), (2) and")
        lines.append("    (6) depend on the plan terms and were not tested.")

    # 5.04
    fails_504 = []
    if purpose not in RP_504_PURPOSES:
        fails_504.append("its own purpose test (5.04 requires medical, disability or "
                         "educational benefits)")
    if annual_usd is not None and annual_usd > RP_504["annual"]:
        fails_504.append(f"the USD {RP_504['annual']:,} annual contribution limit")
    if lifetime_usd is not None and lifetime_usd > RP_504["lifetime"]:
        fails_504.append(f"the USD {RP_504['lifetime']:,} lifetime contribution limit")
    lines.append("  Section 5.04, tax-favored foreign non-retirement savings trust:")
    if fails_504:
        for f in fails_504:
            lines.append(f"    FAILS {f}")
    else:
        lines.append("    Appears to meet the criteria tested here.")

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
                   help="the product holds a pooled portfolio of securities")
    p.add_argument("--value-usd", type=int, default=None)
    p.add_argument("--filing", choices=["single", "joint"], default="single")
    p.add_argument("--purpose", choices=["retirement", "medical", "disability", "educational",
                                         "general"], default="general")
    p.add_argument("--withdrawal", choices=["retirement-conditioned", "unconditional-after-term",
                                            "unconditional"], default="unconditional")
    p.add_argument("--annual-usd", type=int, default=None)
    p.add_argument("--lifetime-usd", type=int, default=None)
    p.add_argument("--other-income-sources", dest="earned_only", action="store_false",
                   default=None, help="contributions come from sources other than earned income")
    p.add_argument("--example", action="store_true")
    a = p.parse_args()

    if a.example:
        a.name = "keren hishtalmut (example)"
        a.pooled_securities, a.value_usd, a.filing = True, 61_000, "joint"
        a.purpose, a.withdrawal, a.annual_usd = "general", "unconditional-after-term", 14_000
        print("(example: a salaried employee's keren hishtalmut on an equity track)\n")

    print(f"SCREENING: {a.name}")
    print("A screen against published criteria. NOT a classification and NOT tax advice.\n")
    print("-- PFIC screen --")
    for l in pfic_screen(a.pooled_securities, a.value_usd, a.filing):
        print(l)
    print("\n-- Foreign trust screen (Revenue Procedure 2020-17) --")
    print("  Scope: this Revenue Procedure exempts from section 6048 REPORTING only. It does")
    print("  not change taxation. Eligibility is limited to individuals already compliant on")
    print("  the related income tax.")
    for l in trust_screen(a.purpose, a.withdrawal, a.annual_usd, a.lifetime_usd, a.earned_only):
        print(l)
    print("\n-- Ask your preparer --")
    print(f"  1. Is {a.name} a foreign trust for US purposes on its actual plan terms?")
    print("  2. If it is, does any exemption outside Revenue Procedure 2020-17 apply?")
    if a.pooled_securities:
        print("  3. What is the fund's holdings breakdown, and does it meet either PFIC test?")
    print("\n  Contribution figures must be converted per tax year at that year's rate.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
