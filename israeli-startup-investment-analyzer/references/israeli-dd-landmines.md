# Israel-Specific Due Diligence Landmines

These are the items a generic investment analysis misses and that a seasoned
Israeli investor or startup lawyer checks every time. Every figure here is sourced
in evidence.json. None of this is legal or tax advice; flag findings and route the
deal to an Israeli lawyer and accountant before a term sheet.

## 1. Innovation Authority (IIA) grant overhang

The single most under-appreciated risk in Israeli deals. Many startups take IIA
(Rashut HaChadshanut) conditional grants early. The money is non-dilutive but it
comes with strings that survive into your investment and can tax or block an exit.

What to check:
- **Royalties.** A grant is repaid through royalties of 3% to 5% of annual
  revenues from the funded product, until the full grant plus annual interest
  (SOFR-based) is repaid. Ask for the outstanding balance.
- **R&D must stay in Israel.** The baseline condition for a grant is that the
  funded R&D is performed in Israel.
- **IP / know-how cannot leave Israel freely.** Selling or transferring the
  funded know-how outside Israel requires the IIA's approval and a repayment. The
  minimum repayment is the total IIA investment plus interest, minus royalties
  already paid. The repayment for a know-how transfer abroad is capped at 6 times
  the grants plus interest, dropping to 3 times if the acquirer keeps the
  company's R&D jobs in Israel for at least three years.
- **Manufacturing abroad.** Relocating manufacturing of the funded know-how
  abroad also requires IIA approval; the maximum increased royalty liability is
  1.5 times the funding plus interest (reduced from the earlier 3 times). IIA
  interest accrues at 12-month Term SOFR plus 0.71513%.

Why it matters to you: a US acquirer that wants the IP moved to Delaware, or a
buyer that plans to move R&D abroad, walks into an IIA approval process and a
redemption bill. This can shrink the exit price, kill a deal in diligence, or
force a worse structure. If the company has material IIA exposure, model the
redemption against your expected exit before you price the round.

## 2. Corporate structure: the Delaware "flip"

Many Israeli startups operate as an Israeli operating company (חברה בע"מ /
OpCo) and later create a Delaware parent (HoldCo) that owns it, the "flip", to
look familiar to US investors and acquirers.

What to check:
- Is the company a single Israeli Ltd, or already flipped to a Delaware HoldCo +
  Israeli OpCo? If a flip is planned, who owns the IP today and where will it sit?
- A flip is a transfer of shares by the shareholders, so the tax falls on the
  shareholders, not the company. Israeli individuals are taxed on a real capital
  gain at 25% (30% for a seller who held 10% or more), plus surtax. The 23%
  corporate rate only applies where a company holds the shares. Quoting a flat
  "23% flip tax" is wrong: model the shareholder-level tax. Confirm the flip used
  Israel's tax-deferred share-for-share rollover route with a pre-ruling from the
  Tax Authority; without it the flip can be an immediate taxable event for the
  shareholders.
- IIA-funded IP cannot simply move to the Delaware parent without the approvals
  and repayment in section 1. A flip on top of IIA grants is a double landmine.
- After a flip the core IP (including future derivative IP) must stay owned by
  the Israeli operating company; IP stranded in the wrong entity breaks both the
  rollover deferral and the IIA know-how rules.

## 3. Section 102 employee option plan

Israel's standard employee-equity vehicle. A healthy 102 plan is a sign of a
clean cap table; a broken one creates tax liabilities and disgruntled employees.

What to check:
- Is the plan under the **capital gains track with a trustee**? That track taxes
  the employee's gain at a flat 25% (plus surtax) versus marginal rates
  approaching 50%, but requires a trustee and a 24-month holding period from the
  grant date. Note the portion of the gain up to the share value at grant can
  still be taxed as ordinary employment income, so "all at 25%" is an
  over-simplification.
- Is the option pool sized sensibly for the stage, and is the top-up in this round
  taken pre-money (diluting founders) or post-money?
- Were any grants made outside the trustee / track rules (a common cleanup item)?

## 4. Cap table, vesting, and company standing

- **Founder vesting / reverse vesting.** Founders without vesting are a red flag:
  a co-founder can leave early with a large unearned stake.
- **Cap-table cleanliness.** Get the fully-diluted cap table including every
  outstanding SAFE/convertible and its cap. Stacked SAFEs converting at once can
  dilute far more than the deck implies.
- **IP assignment (PIIAA) and service inventions.** Confirm every founder,
  employee, and contractor signed an IP-assignment agreement. Unassigned IP, or
  an unresolved employee "service invention" compensation claim under Israeli
  patent law, can undermine the very asset the deal is buying. This is a classic
  Israeli IP-diligence landmine.
- **Companies Registrar (רשם החברות) standing.** Do not just assert this, pull
  the company's official Registrar of Companies extract (נסח חברה) to verify
  share capital, directors, registered charges, and that it is not flagged as a
  "violating company" (חברה מפרה) for unfiled reports or unpaid fees. Also search
  the Registrar of Pledges (רשם המשכונות) for security interests (שעבודים) over
  the company's IP and assets. The `israel-amutot` MCP covers non-profits, not
  for-profit companies, so it cannot do this check.

## 5. Other Israeli liabilities to flag

- **Labor liabilities.** A startup's biggest hidden balance-sheet item is often
  accrued severance (pitzuim), pension and study-fund (keren hishtalmut)
  contributions, unused vacation, and contractor-misclassification exposure.
  Flag these as a purchase-price adjustment for larger teams.
- **Data privacy (Amendment 13).** For any data-heavy startup, check compliance
  with Israel's Privacy Protection Law Amendment 13 (in force 2025) and the
  enforcement powers it gives the Privacy Protection Authority. Non-compliance is
  a regulatory liability and a valuation adjustment.

## 6. SAFE tax treatment (context, not a red flag)

Israeli SAFEs are common and generally benign tax-wise: under Israel Tax
Authority guidelines (May 2023, updated 29 January 2025), a qualifying SAFE is
treated as an advance payment for shares, so the conversion into shares is not a
taxable event and the company has no withholding obligation at conversion; tax
arises only on the later sale of the shares. Still confirm the specific SAFE was
structured to meet the guideline conditions.

## 7. Tax incentive status (verify if claimed)

If the deck claims a reduced tax rate, confirm it. A Preferred Technological
Enterprise pays 7.5% corporate tax in development area A and 12% elsewhere; a
Preferred Enterprise pays 7.5% in area A and 16% elsewhere. These rates depend on
conditions being met, so a claimed rate is a diligence item, not a given.
