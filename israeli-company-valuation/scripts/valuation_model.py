#!/usr/bin/env python3
"""
Israeli private company valuation model.

Builds a WACC from components, runs a free-cash-flow-to-firm DCF, bridges
enterprise value to equity value, applies marketability and control discounts,
and prints a sensitivity grid.

Design rules baked in deliberately:

  * The risk-free rate is a REQUIRED argument. There is no default. The shekel
    yield curve moves continuously, so any built-in value would ship stale.
    Read it live from the Bank of Israel yield page, or from the Tel Aviv
    Stock Exchange government bond data.

  * The country risk premium carries a vintage date and is printed with every
    run, so a reader can see how old the parameter is.

  * The same effective tax rate is used in the cash flow tax line and in the
    debt tax shield. They cannot diverge.

  * Output is a range with a sensitivity grid, never a single point.

Usage:
    python3 valuation_model.py --example
    python3 valuation_model.py --risk-free 0.041 --ebit 5000000 --tax-rate 0.23 \\
        --growth 0.03 --terminal-growth 0.02 --beta 1.1 --net-debt 2000000

All monetary inputs are in whole shekels unless stated otherwise.
"""

import argparse
import datetime
import sys

# Country risk parameters. Vintage is printed on every run so the reader can
# judge staleness. Re-verify against the source in evidence.json at each update.
COUNTRY_DATA_VINTAGE = "5 January 2026"
COUNTRY_DATA_VINTAGE_ISO = "2026-01-05"
# The dataset refreshes twice a year. Past this many days we stop trusting it
# silently and tell the operator to refetch, mirroring the risk-free rule.
COUNTRY_DATA_STALE_AFTER_DAYS = 180
ISRAEL_COUNTRY_RISK_PREMIUM = 0.0207
ISRAEL_TOTAL_EQUITY_RISK_PREMIUM = 0.0630  # already includes the country premium
ISRAEL_SOVEREIGN_RATING = "Baa1"

SCOPE_LIMIT = """
SCOPE LIMIT
This is an indicative valuation range produced from the inputs supplied. It is
not a signed valuation opinion, and it is not admissible to the Israel Tax
Authority, to a court, or into financial statements. Israel has no statutory
licence for a business valuer, so acceptance turns on the professional standing,
independence, and documentation of whoever signs it. For any transaction,
filing, or reorganization, engage a certified public accountant or a
credentialed valuer to prepare and sign the valuation.
""".strip()


def cost_of_equity(risk_free, beta, size_premium, specific_premium,
                   use_total_erp=True):
    """
    Build the cost of equity.

    use_total_erp=True uses the Israel total equity risk premium, which already
    contains the country premium. Adding the country premium again on top would
    be a double count, so this function refuses to do it.
    """
    if use_total_erp:
        market_component = beta * ISRAEL_TOTAL_EQUITY_RISK_PREMIUM
        country_component = 0.0
        convention = ("beta x Israel total ERP (country premium already "
                      "included, not added again)")
    else:
        # Mature-market ERP is derived as total minus country premium.
        mature_erp = ISRAEL_TOTAL_EQUITY_RISK_PREMIUM - ISRAEL_COUNTRY_RISK_PREMIUM
        market_component = beta * mature_erp
        country_component = ISRAEL_COUNTRY_RISK_PREMIUM
        convention = "beta x mature-market ERP, plus country premium separately"

    total = (risk_free + market_component + country_component
             + size_premium + specific_premium)
    return total, convention


def wacc(ke, kd_pretax, tax_rate, equity_weight):
    """Weighted average cost of capital. Tax shield uses the SAME rate as FCFF."""
    if not 0.0 <= equity_weight <= 1.0:
        raise ValueError("equity_weight must be between 0 and 1")
    debt_weight = 1.0 - equity_weight
    kd_after_tax = kd_pretax * (1.0 - tax_rate)
    return ke * equity_weight + kd_after_tax * debt_weight


def project_fcff(ebit, tax_rate, dep, capex, delta_wc, growth, years):
    """
    Free cash flow to firm, grown at `growth` for `years`.

    FCFF = EBIT - tax on EBIT + D&A - capex - change in working capital
    """
    flows = []
    for year in range(1, years + 1):
        factor = (1.0 + growth) ** year
        f_ebit = ebit * factor
        f_dep = dep * factor
        f_capex = capex * factor
        f_wc = delta_wc * factor
        fcff = f_ebit * (1.0 - tax_rate) + f_dep - f_capex - f_wc
        flows.append(fcff)
    return flows


def discount(flows, rate):
    return sum(f / ((1.0 + rate) ** (i + 1)) for i, f in enumerate(flows))


def terminal_value(last_fcff, rate, terminal_growth, years):
    if terminal_growth >= rate:
        raise ValueError(
            "terminal growth (%.4f) must be below the discount rate (%.4f). "
            "A growth rate at or above the discount rate implies infinite value."
            % (terminal_growth, rate)
        )
    tv = last_fcff * (1.0 + terminal_growth) / (rate - terminal_growth)
    return tv / ((1.0 + rate) ** years)


def enterprise_value(ebit, tax_rate, dep, capex, delta_wc, growth,
                     terminal_growth, rate, years):
    flows = project_fcff(ebit, tax_rate, dep, capex, delta_wc, growth, years)
    pv_explicit = discount(flows, rate)
    pv_terminal = terminal_value(flows[-1], rate, terminal_growth, years)
    return pv_explicit + pv_terminal, pv_explicit, pv_terminal


def equity_bridge(ev, net_debt, surplus_assets, contingent_liabilities,
                  severance_shortfall):
    return (ev - net_debt + surplus_assets - contingent_liabilities
            - severance_shortfall)


def apply_discounts(equity, dlom, dloc):
    """Discounts are multiplicative, not additive."""
    return equity * (1.0 - dlom) * (1.0 - dloc)


def sensitivity_grid(base_args, rate_steps, growth_steps):
    """Enterprise value across a WACC band and a terminal growth band."""
    rows = []
    for r in rate_steps:
        row = []
        for g in growth_steps:
            try:
                ev, _, _ = enterprise_value(
                    base_args["ebit"], base_args["tax_rate"], base_args["dep"],
                    base_args["capex"], base_args["delta_wc"],
                    base_args["growth"], g, r, base_args["years"],
                )
                row.append(ev)
            except ValueError:
                row.append(None)
        rows.append((r, row))
    return rows


def country_data_age_days():
    vintage = datetime.date.fromisoformat(COUNTRY_DATA_VINTAGE_ISO)
    return (datetime.date.today() - vintage).days


def pct0(x):
    """Percent with no decimals. Kept out of format literals on purpose."""
    return "{:.0f}".format(x * 100.0) + "%"


def pct1(x):
    """Percent with one decimal."""
    return "{:.1f}".format(x * 100.0) + "%"


def fmt(n):
    if n is None:
        return "{:>14}".format("n/a")
    return "{:>14,.0f}".format(n)


def main():
    p = argparse.ArgumentParser(
        description="Israeli private company valuation model",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--example", action="store_true",
                   help="run with illustrative inputs and exit")
    p.add_argument("--risk-free", type=float,
                   help="REQUIRED. Shekel government bond yield to maturity, "
                        "as a decimal (e.g. 0.041). Read live from the Bank of "
                        "Israel. No default is provided on purpose.")
    p.add_argument("--beta", type=float, default=1.0, help="relevered equity beta")
    p.add_argument("--size-premium", type=float, default=0.0,
                   help="size premium as a decimal. Name your source in the output.")
    p.add_argument("--specific-premium", type=float, default=0.0,
                   help="company-specific risk premium as a decimal")
    p.add_argument("--country-risk-premium", type=float,
                   help="override the built-in Israel country risk premium as a "
                        "decimal. Supply a freshly fetched value; the built-in "
                        "one carries a vintage and goes stale.")
    p.add_argument("--total-erp", type=float,
                   help="override the built-in Israel total equity risk premium "
                        "as a decimal (country premium included).")
    p.add_argument("--separate-country-premium", action="store_true",
                   help="use mature-market ERP plus a separate country premium "
                        "instead of the Israel total ERP")
    p.add_argument("--kd", type=float, default=0.06, help="pre-tax cost of debt")
    p.add_argument("--equity-weight", type=float, default=0.7,
                   help="equity share of capital structure, 0 to 1")
    p.add_argument("--ebit", type=float, help="normalized EBIT, year 0")
    p.add_argument("--tax-rate", type=float, default=0.23,
                   help="the company's OWN effective rate. Do not assume the "
                        "standard rate for a preferred enterprise.")
    p.add_argument("--dep", type=float, default=0.0, help="depreciation and amortization")
    p.add_argument("--capex", type=float, default=0.0, help="capital expenditure")
    p.add_argument("--delta-wc", type=float, default=0.0, help="change in working capital")
    p.add_argument("--growth", type=float, default=0.03, help="explicit-period growth")
    p.add_argument("--terminal-growth", type=float, default=0.02)
    p.add_argument("--years", type=int, default=5)
    p.add_argument("--net-debt", type=float, default=0.0)
    p.add_argument("--surplus-assets", type=float, default=0.0)
    p.add_argument("--contingent-liabilities", type=float, default=0.0)
    p.add_argument("--severance-shortfall", type=float, default=0.0)
    p.add_argument("--dlom", type=float, default=0.0,
                   help="marketability discount as a decimal. There is no "
                        "Israeli published range; cite your empirical basis.")
    p.add_argument("--dloc", type=float, default=0.0,
                   help="lack-of-control discount. Only for a genuinely "
                        "non-controlling interest.")

    a = p.parse_args()

    if a.example:
        a.risk_free = 0.041
        a.ebit = 5_000_000
        a.dep = 400_000
        a.capex = 500_000
        a.delta_wc = 150_000
        a.beta = 1.1
        a.size_premium = 0.03
        a.specific_premium = 0.01
        a.net_debt = 2_000_000
        a.severance_shortfall = 300_000
        a.dlom = 0.25
        print("Running with ILLUSTRATIVE inputs. These are not market data.\n")

    if a.risk_free is None:
        p.error("--risk-free is required. Read the current shekel government "
                "bond yield from the Bank of Israel rather than using a "
                "remembered value. See SKILL.md step 5.")
    if a.ebit is None:
        p.error("--ebit is required (normalized EBIT). Run the normalization "
                "bridge first, see SKILL.md step 3.")

    global ISRAEL_COUNTRY_RISK_PREMIUM, ISRAEL_TOTAL_EQUITY_RISK_PREMIUM
    if a.country_risk_premium is not None:
        ISRAEL_COUNTRY_RISK_PREMIUM = a.country_risk_premium
    if a.total_erp is not None:
        ISRAEL_TOTAL_EQUITY_RISK_PREMIUM = a.total_erp

    age = country_data_age_days()
    stale = age > COUNTRY_DATA_STALE_AFTER_DAYS and a.country_risk_premium is None

    ke, convention = cost_of_equity(
        a.risk_free, a.beta, a.size_premium, a.specific_premium,
        use_total_erp=not a.separate_country_premium,
    )
    w = wacc(ke, a.kd, a.tax_rate, a.equity_weight)

    ev, pv_explicit, pv_terminal = enterprise_value(
        a.ebit, a.tax_rate, a.dep, a.capex, a.delta_wc,
        a.growth, a.terminal_growth, w, a.years,
    )
    eq = equity_bridge(ev, a.net_debt, a.surplus_assets,
                       a.contingent_liabilities, a.severance_shortfall)
    eq_after = apply_discounts(eq, a.dlom, a.dloc)

    print("=" * 68)
    print("ISRAELI COMPANY VALUATION, INDICATIVE")
    print("=" * 68)
    print("\nCOUNTRY PARAMETERS")
    print("  Dataset vintage        : %s" % COUNTRY_DATA_VINTAGE)
    print("  Sovereign rating       : %s" % ISRAEL_SOVEREIGN_RATING)
    print("  Country risk premium   : {:.2%}".format(ISRAEL_COUNTRY_RISK_PREMIUM))
    print("  Israel total ERP       : {:.2%}".format(ISRAEL_TOTAL_EQUITY_RISK_PREMIUM))
    print("  Data age               : %d days" % age)
    if stale:
        print("  WARNING: this country risk data is older than %d days. It refreshes"
              % COUNTRY_DATA_STALE_AFTER_DAYS)
        print("  in January and July. Refetch it and pass --country-risk-premium and")
        print("  --total-erp, or state in the write-up that a stale premium was used.")
    else:
        print("  Check the vintage above. This dataset refreshes twice a year.")

    print("\nDISCOUNT RATE BUILD-UP")
    print("  Risk-free rate         : {:.2%}  (must be read live)".format(a.risk_free))
    print("  Beta                   : {:.2f}".format(a.beta))
    print("  Convention             : %s" % convention)
    print("  Size premium           : {:.2%}".format(a.size_premium))
    print("  Company-specific       : {:.2%}".format(a.specific_premium))
    print("  Cost of equity         : {:.2%}".format(ke))
    print("  Pre-tax cost of debt   : {:.2%}".format(a.kd))
    print("  Effective tax rate     : {:.2%}  (same rate used in FCFF)".format(a.tax_rate))
    print("  Equity weight          : {:.0%}".format(a.equity_weight))
    print("  WACC                   : {:.2%}".format(w))

    print("\nVALUATION")
    print("  PV of explicit period  : {:>18,.0f}".format(pv_explicit))
    print("  PV of terminal value   : {:>18,.0f}".format(pv_terminal))
    print("  Terminal share of EV   : " + pct0(pv_terminal / ev if ev else 0).rjust(17))
    print("  Enterprise value       : {:>18,.0f}".format(ev))
    print("  Less net debt          : {:>18,.0f}".format(-a.net_debt))
    print("  Plus surplus assets    : {:>18,.0f}".format(a.surplus_assets))
    print("  Less contingents       : {:>18,.0f}".format(-a.contingent_liabilities))
    print("  Less severance gap     : {:>18,.0f}".format(-a.severance_shortfall))
    print("  Equity value           : {:>18,.0f}".format(eq))
    if a.dlom or a.dloc:
        print("  Marketability discount : " + pct0(a.dlom).rjust(17))
        print("  Control discount       : " + pct0(a.dloc).rjust(17))
        print("  Equity after discounts : {:>18,.0f}".format(eq_after))

    if ev and (pv_terminal / ev) > 0.75:
        print("\n  NOTE: terminal value is more than three quarters of enterprise")
        print("  value. The answer is driven by the terminal assumption, not by")
        print("  the forecast. Say so explicitly in the write-up.")

    rate_steps = [w - 0.02, w - 0.01, w, w + 0.01, w + 0.02]
    growth_steps = [a.terminal_growth - 0.01, a.terminal_growth,
                    a.terminal_growth + 0.01]
    base = dict(ebit=a.ebit, tax_rate=a.tax_rate, dep=a.dep, capex=a.capex,
                delta_wc=a.delta_wc, growth=a.growth, years=a.years)
    grid = sensitivity_grid(base, rate_steps, growth_steps)

    print("\nSENSITIVITY, ENTERPRISE VALUE")
    print("  rows = WACC, columns = terminal growth")
    header = "  " + "WACC".ljust(10) + "".join(
        "{:>14}".format("g=" + pct1(g)) for g in growth_steps)
    print(header)
    lo, hi = None, None
    for r, row in grid:
        line = "  " + "{:.2%}".format(r).ljust(10)
        for v in row:
            line += fmt(v)
            if v is not None:
                lo = v if lo is None or v < lo else lo
                hi = v if hi is None or v > hi else hi
        print(line)

    if lo is not None:
        print("\n  Indicative enterprise value RANGE: {:,.0f} to {:,.0f}".format(lo, hi))
        print("  Report the range. The central figure is a midpoint, not an answer.")

    print("\n" + SCOPE_LIMIT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
