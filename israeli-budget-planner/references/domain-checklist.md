# Israeli Budget Planner: Domain Checklist

Scope: household / personal budgeting and mortgage (mashkanta) planning for Israeli
residents. Reviewed against this checklist on each update. Figures must be the
current (2026) authoritative values, each traceable to a source below.

## Must cover (a wrong/absent item here is a CRITICAL family-facing error)

1. **Bank of Israel interest rate + prime rate.** Current BOI rate and prime =
   BOI + 1.5%. As of 25 May 2026: BOI 3.75%, prime 5.25%.
   Source: https://www.boi.org.il/en/ ; https://tradingeconomics.com/israel/interest-rate
2. **Mortgage mix rule (correct direction).** Minimum 1/3 of total mortgage must be
   fixed-unlinked (ribit kvua lo tzmuda); up to 2/3 may be variable/prime. The old
   1/3-prime cap was removed 17 Jan 2021. (Inverting this leads a family to an
   over-variable, rate-shock-exposed loan.)
   Source: https://www.kolzchut.org.il/he/מגבלות_על_לקיחת_משכנתא
3. **PTI (payment-to-income) cap.** BOI regulatory ceiling: monthly repayment may not
   exceed 50% of disposable income; banks in practice decline above ~40%.
   Source: https://www.kolzchut.org.il/he/מגבלות_על_לקיחת_משכנתא
4. **LTV limits.** 75% first/only home, 70% home replacement, 50% investment.
   Source: https://www.kolzchut.org.il/he/מגבלות_על_לקיחת_משכנתא
5. **Net-pay deductions used in affordability math must be the CURRENT employee rates,**
   because PTI and budget headroom are computed off net income:
   - Income tax: marginal 10%–50% brackets (2026 widened Jan 2026; 10% bracket to
     ~7,010/mo, top 50% above ~60,130/mo).
     Source: https://www.kolzchut.org.il/he/מדרגות_מס_הכנסה
   - **Bituach Leumi (employee, salaried), 2026: 1.04% reduced / 7% full**, split at
     60% of average wage = **7,703 NIS/mo** (reduced rate rose from 0.4% to 1.04% in
     2026), ceiling 51,910.
     Source: https://www.btl.gov.il/Insurance/Rates/Pages/לעובדים שכירים.aspx ;
     https://jobcalc.co.il/national-insurance/bituach-leumi/
   - **Health-tax (dmei bituach briut), employee 2026: 3.23% reduced / 5.17% full**,
     split at 7,703 NIS/mo.
     Source: https://www.btl.gov.il/Insurance/Health_Insurance/Pages/שיעורי דמי ביטוח בריאות.aspx
   - Tax credit point (nekudat zikui): 242 NIS/mo in 2026; resident base 2.25, women
     +0.5, new immigrant extra for 3.5 yrs.
     Source: https://www.kolzchut.org.il/he/נקודות_זיכוי_ממס_הכנסה
6. **Minimum wage / average wage.** Min wage 6,443.85 NIS/mo (35.40/hr) from 1 Apr 2026;
   average wage 13,566 NIS/mo (section 1, Jan 2026).
   Source: https://www.kolzchut.org.il/he/שכר_מינימום ;
   https://www.btl.gov.il/Mediniyut/GeneralData/Pages/שכר ממוצע.aspx
7. **VAT (ma'am): 18%** (since 1 Jan 2025).
   Source: https://www.gov.il/he/pages/dec1270-2024
8. **Hidden fixed housing costs.** Rent is quoted excluding arnona + va'ad bayit; these
   add ~500–2,000 NIS/mo and must be in the budget.
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
- Emergency-fund target (3–6 months expenses).
- A worked affordability example tying net income → PTI → max loan → monthly payment.
- Calculator script consistency: the script's hardcoded constants (BL rate/threshold,
  health-tax rate, default mortgage rate, tax brackets) must match the SKILL.md prose;
  divergence between the documented rule and the code that computes the answer is a
  family-facing error.

## Out of scope

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
