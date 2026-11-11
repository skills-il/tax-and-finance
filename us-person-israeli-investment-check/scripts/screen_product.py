#!/usr/bin/env python3
"""Screen one Israeli savings product against the PFIC and foreign-trust criteria.

This is a criteria walker, not tax advice and not a classification. It reports which
published criterion a product appears to pass or fail, given what you tell it, so you can put
a precise question to a licensed preparer. It does not read plan documents, does not inspect
any fund's holdings, and cannot determine whether any arrangement is in fact a foreign trust
or a PFIC for US purposes.

Criteria are those in ../references/screening-criteria.md and ../evidence.json.

The contribution limits tested are limits set by Israeli law governing the plan, not what the
user happened to deposit (Rev. Proc. 2020-17 section 5.03: "requirements established by the laws
of the trust's jurisdiction"). A limit found only in the provider's own terms is a preparer
question, not an input here. Enter a legal limit converted to USD, or --no-contribution-cap.
Revenue Procedure 2020-17 caps convert at the US Treasury Bureau of the Fiscal Service rate on
the last day of the tax year; the proposed-regulation retirement limits at the 1 July rate.

Usage:
  python3 screen_product.py --example
  python3 screen_product.py --name "keren hishtalmut" --wrapper --purpose general \
      --withdrawal unconditional-after-term --peak-value-usd 40000
  python3 screen_product.py --name "TASE ETF" --pooled-securities --all-pfic-value-usd 18000
"""

import argparse
import sys

PFIC_PART1_EXCEPTION = {"single": 25_000, "joint": 50_000}
PFIC_INDIRECT_EXCEPTION = 5_000
RP_503 = {"annual": 50_000, "lifetime": 1_000_000}
RP_504 = {"annual": 10_000, "lifetime": 200_000}
RP_504_PURPOSES = {"medical", "disability", "educational"}
# Proposed Reg. 1.6048-5(b) (89 FR 39440, 8 May 2024), NOT final. Elective reliance only.
PROP_RETIREMENT = {"annual": 75_000, "lifetime": 1_000_000, "value": 600_000}
PROP_DE_MINIMIS_VALUE = 50_000


def part1_exception_lines(all_pfic_value_usd, indirect_value_usd, filing, excess_distribution,
                          sold_at_gain, qef_elected, mtm_elected=False):
    lines = []
    lost = []
    if excess_distribution:
        lost.append("an excess distribution was received from this fund this year")
    if sold_at_gain:
        lost.append("gain was recognized on selling this fund's stock this year")
    if qef_elected:
        lost.append("a QEF election was made for this fund")
    if mtm_elected:
        lost.append("a section 1296 mark-to-market election is in effect, so it is not a "
                    "section 1291 fund")
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
        lines.append("  distribution, no gain on a sale and no QEF or MTM election reported. Part I")
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
                excess_distribution, sold_at_gain, qef_elected, mtm_elected=False):
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
        lines.append("  A direct holding that is neither a pooled fund nor a wrapper: a deposit is")
        lines.append("  not stock, so it raises no PFIC question. A share in an Israeli company is")
        lines.append("  PFIC stock only if THAT company meets the income or asset test; an operating")
        lines.append("  company usually does not, a holding or cash-rich company can. Check whether")
        lines.append("  the company publishes a PFIC statement.")
        if all_pfic_value_usd is not None or sold_at_gain or excess_distribution:
            lines.append("  If the company IS a PFIC:")
            lines.extend(part1_exception_lines(all_pfic_value_usd, indirect_value_usd, filing,
                                               excess_distribution, sold_at_gain, qef_elected,
                                               mtm_elected))
        return lines
    if pooled:
        lines.append("  Holds pooled securities, so the income test (75% passive, section")
        lines.append("  1297(b)) and the asset test (50% passive, section 1297(e)) are both")
        lines.append("  likely met. This is an inference from the tests, NOT an IRS")
        lines.append("  determination about this fund.")
    lines.extend(part1_exception_lines(all_pfic_value_usd, indirect_value_usd, filing,
                                       excess_distribution, sold_at_gain, qef_elected,
                                       mtm_elected))
    if mtm_elected or qef_elected:
        lines.append("  An election is reported for this fund. Whether the section 1291 regime still")
        lines.append("  reaches any part of the holding (for example a QEF election made after the")
        lines.append("  first year of holding) and how the election applies is a preparer's call.")
    else:
        lines.append("  Default treatment absent an election is the section 1291 regime, under")
        lines.append("  which the ENTIRE gain on disposition is treated as an excess")
        lines.append("  distribution. Elections are a preparer's call.")
    return lines


def dollar_limbs(annual_usd, lifetime_usd, limits, no_cap=False):
    """Return 'pass', 'fail' or 'unknown' for disjunctive annual-or-lifetime dollar CAPS."""
    if no_cap:
        return "fail"
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
                 percentage_limited, peak_value_usd=None, no_cap=False):
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
        limbs = dollar_limbs(annual_usd, lifetime_usd, RP_503, no_cap)
        if limbs == "fail":
            fails_503.append(f"criterion 5.03(4): not percentage-limited, and no annual cap of USD "
                             f"{RP_503['annual']:,} or less nor lifetime cap of USD "
                             f"{RP_503['lifetime']:,} or less")
        elif limbs == "unknown":
            open_503.append("criterion 5.03(4) is met by a percentage-of-earned-income cap OR "
                            f"annual USD {RP_503['annual']:,} or less OR lifetime USD "
                            f"{RP_503['lifetime']:,} or less; a legal limit is missing, and if "
                            "Israeli law sets none for this plan the dollar limbs fail")
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
    limbs = dollar_limbs(annual_usd, lifetime_usd, RP_504, no_cap)
    if limbs == "fail":
        fails_504.append(f"criterion 5.04(3): no annual cap of USD {RP_504['annual']:,} or less "
                         f"nor lifetime cap of USD {RP_504['lifetime']:,} or less (no percentage "
                         "limb in 5.04)")
    elif limbs == "unknown":
        open_504.append(f"criterion 5.04(3), USD {RP_504['annual']:,} annual or USD "
                        f"{RP_504['lifetime']:,} lifetime limits; a legal limit is missing, and if "
                        "Israeli law sets none for this plan this criterion fails")
    report(lines, "  Section 5.04, tax-favored foreign non-retirement savings trust:", fails_504,
           open_504, "5.04(1) and (2)")

    if fails_503 and fails_504:
        lines.append("")
        lines.append("  Neither Revenue Procedure 2020-17 exemption appears available on these")
        lines.append("  facts. That does NOT mean the product IS a foreign trust. It means this")
        lines.append("  safe harbour does not clear it, and a preparer has to reach the")
        lines.append("  underlying question.")
    lines.append("")
    lines.extend(proposed_reg_lines(purpose, withdrawal, annual_usd, lifetime_usd,
                                    percentage_limited, peak_value_usd, earned_income_only,
                                    no_cap))
    return lines


def proposed_reg_lines(purpose, withdrawal, annual_usd, lifetime_usd, percentage_limited,
                       peak_value_usd, earned_income_only=None, no_cap=False):
    """Elective alternative under proposed Reg. 1.6048-5(b). Still proposed, not final."""
    lines = ["  Elective alternative, proposed Reg. 1.6048-5(b) (8 May 2024, NOT final). A",
             "  taxpayer may rely on it only if they and all related persons apply the",
             "  proposed regulations in their entirety and consistently from the first year",
             "  of reliance. Whether to rely is a preparer's call."]
    unconditional = withdrawal in ("unconditional", "unconditional-after-term")
    category_cleared = False
    if purpose == "retirement":
        caps = (not no_cap) and (
            (annual_usd is not None and annual_usd <= PROP_RETIREMENT["annual"])
            or (lifetime_usd is not None and lifetime_usd <= PROP_RETIREMENT["lifetime"]))
        value_ok = peak_value_usd is not None and peak_value_usd <= PROP_RETIREMENT["value"]
        ok_limit = percentage_limited or caps or value_ok
        lines.append("    Retirement category: percentage cap OR annual cap USD 75,000 or less OR")
        lines.append("    lifetime cap USD 1,000,000 or less OR aggregate value of such trusts in")
        lines.append("    Israel no more than USD 600,000 at any point in the year (base figures,")
        lines.append("    indexed in the proposed text; value and caps at the 1 July rate).")
        lines.append("    Limit: " + ("appears met." if ok_limit else
                                     "not shown to be met on the data given."))
        if earned_income_only is False:
            lines.append("    OPEN  earned-income-only, with an allowance for limited contributions")
            lines.append("          by unemployed individuals; confirm the other sources qualify.")
        if unconditional:
            lines.append("    The withdrawal condition is worded exactly as 5.03(5), so it fails here too.")
        elif withdrawal == "penalty-before-condition":
            lines.append("    OPEN  penalty limb, worded as 5.03(5): confirm the early-withdrawal cost")
            lines.append("          is a penalty.")
        category_cleared = (ok_limit and withdrawal == "retirement-conditioned"
                            and earned_income_only is True)
    elif purpose in RP_504_PURPOSES:
        lines.append("    Non-retirement category: same purpose and withdrawal tests as 5.04, with")
        lines.append("    the USD 10,000 / 200,000 caps indexed in the proposed text.")
    lines.append("    De minimis savings trust category (applies only if the arrangement is NOT")
    lines.append("    within the retirement or non-retirement category): a tax-favored savings")
    lines.append("    vehicle reported to the local tax authority, where the aggregate value of")
    lines.append("    such trusts in Israel is no more than USD 50,000 at EVERY point in the year")
    lines.append("    (last-day rate).")
    if category_cleared:
        lines.append("    Not needed: the retirement category above appears met on these facts.")
    elif peak_value_usd is None:
        lines.append("    Not evaluated: provide --peak-value-usd (aggregate of all such")
        lines.append("    arrangements in Israel, at its highest point in the year).")
    elif peak_value_usd <= PROP_DE_MINIMIS_VALUE:
        lines.append(f"    Peak aggregate value USD {peak_value_usd:,} is within USD 50,000, so this")
        lines.append("    category may be in play. CAUTION: the operative paragraph (b)(1) lists only")
        lines.append("    the retirement and non-retirement categories, so whether de minimis trusts")
        lines.append("    are actually exempted under the proposed text is a preparer question.")
    else:
        lines.append(f"    Peak aggregate value USD {peak_value_usd:,} exceeds USD 50,000, so this")
        lines.append("    category does not appear available.")
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
    p.add_argument("--mtm-elected", action="store_true",
                   help="a section 1296 mark-to-market election is in effect for this fund")
    p.add_argument("--purpose", choices=["retirement", "medical", "disability", "educational",
                                         "general"], default="general")
    p.add_argument("--withdrawal", choices=["retirement-conditioned", "penalty-before-condition",
                                            "unconditional-after-term", "unconditional"],
                   default="unconditional")
    p.add_argument("--annual-limit-usd", dest="annual_usd", type=int, default=None,
                   help="annual contribution limit set by Israeli law governing the plan, in "
                        "USD (not what was deposited)")
    p.add_argument("--lifetime-limit-usd", dest="lifetime_usd", type=int, default=None,
                   help="lifetime contribution limit set by Israeli law governing the plan, in "
                        "USD")
    p.add_argument("--no-contribution-cap", action="store_true",
                   help="Israeli law sets no contribution limit for this plan")
    p.add_argument("--insurance-policy", action="store_true",
                   help="the wrapper is an insurance policy (bituach menahalim, polisat chisachon)")
    p.add_argument("--peak-value-usd", type=int, default=None,
                   help="highest aggregate value during the year of all such arrangements in "
                        "Israel, in USD, for the proposed-regulation value tests (1 July rate "
                        "for the USD 600,000 test, last-day rate for the USD 50,000 test)")
    p.add_argument("--percentage-limited", action="store_true",
                   help="contributions are capped as a percentage of earned income (5.03(4))")
    p.add_argument("--earned-income-only", dest="earned_only", action="store_true", default=None,
                   help="contributions come only from earned income")
    p.add_argument("--other-income-sources", dest="earned_only", action="store_false",
                   help="contributions come from sources other than earned income")
    p.add_argument("--example", action="store_true")
    a = p.parse_args()
    for flag in ("all_pfic_value_usd", "indirect_value_usd", "annual_usd", "lifetime_usd",
                 "peak_value_usd"):
        v = getattr(a, flag)
        if v is not None and v < 0:
            p.error(f"{flag} cannot be negative")
    if a.pooled_securities and a.wrapper:
        p.error("choose one: --pooled-securities for a fund held directly, --wrapper for a "
                "pension, gemel, hishtalmut or policy")
    if a.insurance_policy and not a.wrapper:
        p.error("--insurance-policy describes a wrapper; add --wrapper")
    if a.no_contribution_cap and (a.annual_usd is not None or a.lifetime_usd is not None):
        p.error("--no-contribution-cap conflicts with a cap value")
    if a.indirect_value_usd is not None and not a.pooled_securities:
        p.error("--indirect-value-usd is for a fund held through another PFIC; use it with "
                "--pooled-securities. The USD 5,000 exception does not reach stock owned "
                "through a wrapper")

    if a.example:
        a.name = "keren hishtalmut (example)"
        a.wrapper, a.filing, a.earned_only = True, "joint", True
        a.purpose, a.withdrawal = "general", "unconditional-after-term"
        print("(example: a salaried employee's keren hishtalmut on an equity track)\n")

    print(f"SCREENING: {a.name}")
    print("A screen against published criteria. NOT a classification and NOT tax advice.\n")
    print("-- PFIC screen --")
    for l in pfic_screen(a.pooled_securities, a.wrapper, a.all_pfic_value_usd,
                         a.indirect_value_usd, a.filing, a.excess_distribution, a.sold_at_gain,
                         a.qef_elected, a.mtm_elected):
        print(l)
    direct = not a.wrapper
    print("\n-- Foreign trust screen (Revenue Procedure 2020-17) --")
    if direct and a.pooled_securities:
        print("  Not a trust question: a directly held fund or ETF is screened as PFIC stock only.")
    elif direct:
        print("  Not a trust question: a direct share or a bank deposit is not a trust")
        print("  arrangement. Use --wrapper for a pension, gemel, hishtalmut or policy.")
    else:
        print("  Scope: this Revenue Procedure exempts from section 6048 REPORTING only. It does")
        print("  not change taxation or any other reporting duty. Eligibility is limited to")
        print("  individuals already compliant on the related income tax.")
        for l in trust_screen(a.purpose, a.withdrawal, a.annual_usd, a.lifetime_usd,
                              a.earned_only, a.percentage_limited, a.peak_value_usd,
                              a.no_contribution_cap):
            print(l)
    print("\n-- Ask your preparer --")
    qs = []
    if a.wrapper:
        qs.append(f"Is {a.name} a foreign trust for US purposes on its actual plan terms?")
        qs.append("If it is, should I rely on Revenue Procedure 2020-17 or, all-or-nothing, on "
                  "the 2024 proposed section 6048 regulations?")
        qs.append("What funds does the investment track hold, and does any of them meet a PFIC "
                  "test?")
        qs.append("Reg. 1.1298-1(c)(4) needs a treaty provision taxing the fund's income only "
                  "when paid, and the US-Israel treaty text has none; if you rely on it, on what "
                  "basis?")
        if a.insurance_policy:
            qs.append("Is the excise tax on premiums paid to foreign insurers (Form 720, IRS No. "
                      "30) due on this policy, or does Article 8(8) of the US-Israel treaty "
                      "relieve it?")
    elif a.pooled_securities:
        qs.append("Does this fund meet a PFIC test on its actual holdings, and does it issue a "
                  "PFIC Annual Information Statement?")
    else:
        qs.append(f"Does {a.name} raise any PFIC question at all (for a company share: is the "
                  "company a PFIC)?")
    for i, q in enumerate(qs, 1):
        print(f"  {i}. {q}")
    if a.wrapper:
        print("\n  Revenue Procedure 2020-17 dollar limits use the US Treasury Bureau of the Fiscal")
        print("  Service rate on the last day of the tax year; the proposed-regulation retirement")
        print("  limits use the 1 July rate, and its USD 50,000 de minimis test the last-day rate.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
