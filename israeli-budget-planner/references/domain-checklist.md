# Israeli Budget Planner: Domain Checklist

Scope: household / personal budgeting and mortgage (mashkanta) planning for Israeli
residents. Reviewed against this checklist on each update. Figures must be the
current (2026) authoritative values, each traceable to a source below.

## Must cover (a wrong/absent item here is a CRITICAL family-facing error)

1. **Bank of Israel interest rate + prime rate.** Current BOI rate and prime =
   BOI + 1.5%. As of 6 July 2026: BOI 3.50%, prime 5.00%.
   Source: https://www.boi.org.il ; https://tradingeconomics.com/israel/interest-rate
2. **Mortgage mix rule (correct direction).** At least 1/3 of the total mortgage must be
   in a FIXED-interest track; up to 2/3 may be variable/prime. The fixed third need NOT
   be unlinked, a CPI-linked fixed track satisfies it. Maximum term 30 years. (Inverting the direction leads a family to an
   over-variable, rate-shock-exposed loan; over-stating it as "unlinked" wrongly removes
   the cheaper CPI-linked fixed option from their choice set.)
   Source: https://www.kolzchut.org.il/he/מגבלות_על_לקיחת_משכנתא
3. **PTI (payment-to-income) cap.** BOI regulatory ceiling: monthly repayment may not
   exceed 50% of disposable income. That is a ceiling, not a target; bank underwriting
   is stricter and no authoritative source publishes a bank-practice percentage.
   Source: https://www.kolzchut.org.il/he/מגבלות_על_לקיחת_משכנתא
4. **LTV limits.** 75% first/only home, 70% home replacement, 50% investment.
   Source: https://www.kolzchut.org.il/he/מגבלות_על_לקיחת_משכנתא
5. **Net-pay deductions used in affordability math must be the CURRENT employee rates,**
   because PTI and budget headroom are computed off net income:
   - Income tax: marginal 10%-50% brackets (2026 widened Jan 2026; 10% bracket to
     ~7,010/mo, top 50% above ~60,130/mo).
     Source: https://www.kolzchut.org.il/he/מדרגות_מס_הכנסה
   - **Bituach Leumi + health-tax (employee): the FULL category table, not one row.**
     The rate varies by age and pension status. Must cover, as its own row each:
     resident 18-to-retirement (4.27% / 12.17% combined), under 18 (0% / 0%),
     old-age-pension recipient (0% / 0%), disability-pension recipient with annual
     approval (health only, 3.23% / 5.17%), aged 67-70 not receiving old-age pension
     (3.93% / 10.03%), woman between retirement age and male retirement age not
     receiving a pension (3.95% / 10.24%), controlling shareholder (4.25% / 11.96%),
     first resident after 62 (3.6% / 7.45%). Split at 7,703 NIS/mo, ceiling 51,910.
     Encoding only the default row charges the full deduction to a working pensioner or
     an under-18 employee, who in fact owe nothing.
     Source: https://www.btl.gov.il/Insurance/Rates/Pages/%D7%9C%D7%A2%D7%95%D7%91%D7%93%D7%99%D7%9D%20%D7%A9%D7%9B%D7%99%D7%A8%D7%99%D7%9D.aspx ;
     https://jobcalc.co.il/national-insurance/bituach-leumi/
   - **Health-tax (dmei bituach briut), employee 2026: 3.23% reduced / 5.17% full**,
     split at 7,703 NIS/mo.
     Source: https://www.btl.gov.il/Insurance/Health_Insurance/Pages/%D7%A9%D7%99%D7%A2%D7%95%D7%A8%D7%99%20%D7%93%D7%9E%D7%99%20%D7%91%D7%99%D7%98%D7%95%D7%97%20%D7%91%D7%A8%D7%99%D7%90%D7%95%D7%AA.aspx
   - Tax credit point (nekudat zikui): 242 NIS/mo in 2026; resident base 2.25, women
     +0.5, new immigrant extra for 3.5 yrs.
     Source: https://www.kolzchut.org.il/he/נקודות_זיכוי_ממס_הכנסה
6. **Minimum wage / average wage.** Min wage 6,443.85 NIS/mo (35.40/hr) from 1 Apr 2026;
   average wage 13,566 NIS/mo (section 1, Jan 2026).
   Source: https://www.kolzchut.org.il/he/שכר_מינימום ;
   https://www.btl.gov.il/Mediniyut/GeneralData/Pages/%D7%A9%D7%9B%D7%A8%20%D7%9E%D7%9E%D7%95%D7%A6%D7%A2.aspx
7. **VAT (ma'am): 18%** (since 1 Jan 2025).
   Source: https://www.gov.il/he/pages/dec1270-2024
8. **Hidden fixed housing costs.** Rent is quoted excluding arnona + va'ad bayit; these
   add ~500-2,000 NIS/mo and must be in the budget.
9. **Arnona = municipality-set, annual.** Do not ship static per-city tables; fetch the
   current-year tzav arnona from the relevant municipality.

## Should cover (absence = MAJOR)

- Mortgage track types and indicative ranges (prime-linked, fixed-unlinked,
  CPI-linked fixed, CPI-linked variable) with the caveat that ranges drift.
- Mandatory mortgage life + structural insurance (bituach chaim / bituach mavne) as a
  budget line and a bank requirement.
- Pension contribution as a salary deduction (employee 6% / 6.5%) - affects net pay.
- Israeli savings vehicles (keren pensia, keren hishtalmut, kupat gemel) with their tax
  treatment and lock-in.
- Emergency-fund target (3-6 months expenses).
- Credit points for children, the pension-contribution tax credit, and the keren
  hishtalmut employee deduction, as named corrections to the net-pay estimate.
- Multi-employer households: the reduced band and credit points cannot both be claimed
  twice; a tiaum dmei bituach and tiaum mas are required.
- Acquisition costs outside the loan (mas rechisha, lawyer, broker, appraiser,
  registration) alongside the LTV equity requirement.
- Surtax (mas yesef): the 50% top row is the 47% bracket plus a 3% surtax, and since 2025 a further 2% applies to high non-employment/non-business income (52% top).
- A worked affordability example tying net income to PTI to max loan to monthly payment.
- Calculator script consistency: the script's hardcoded constants (BL rate/threshold,
  health-tax rate, default mortgage rate, tax brackets) must match the SKILL.md prose;
  divergence between the documented rule and the code that computes the answer is a
  family-facing error.

## Out of scope

- **Self-employed households (osek patur / osek murshe), reviewed 2026-08-27.** An ordinary
  user WOULD plausibly ask, so this is now an EXPLICIT exclusion stated in SKILL.md,
  SKILL_HE.md and the script docstring rather than a silent gap: the self-employed pay
  different Bituach Leumi and health rates and have deductible expenses and mikdamot, so
  `--salary` must not be used for them. Route them to a self-employed skill. Revisit next
  cycle whether to add the self-employed rate rows outright.
- Per-bank rate shopping / live quote scraping (point to boi-exchange MCP instead).
- Investment-portfolio / stock advice beyond the named Israeli savings vehicles.
- Business/corporate budgeting and the state takciv (this is a household tool).
- Legal tax-planning advice (defer to an accountant / rashut hamisim).

## Authoritative sources

- Bank of Israel - interest/prime, mortgage regs: https://www.boi.org.il
- Bituach Leumi - BL + health-tax rates, average wage: https://www.btl.gov.il
- Central Bureau of Statistics - CPI, housing indices: https://www.cbs.gov.il
- Kol Zchut - mortgage rules, min wage, credit points, tax brackets: https://www.kolzchut.org.il
- Israel Tax Authority - brackets, VAT: https://www.gov.il/he/departments/israel_tax_authority
- Municipality tzav arnona (per city) - e.g. https://www.tel-aviv.gov.il
