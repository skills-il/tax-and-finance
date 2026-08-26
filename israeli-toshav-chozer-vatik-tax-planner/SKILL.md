---
name: israeli-toshav-chozer-vatik-tax-planner
description: Plans Section 14 tax exemption for an Israeli toshav chozer vatik (10+ years abroad). Distinguishes vatik (full 10-year foreign-income exemption) from regular toshav chozer (5-year passive + 10-year capital gains only), pins the 10-year clock to the tax-residency date (not arrival), surfaces the 2026 reporting change (Amendment 272 cancels 134b + 135(1)(b); tax stays exempt, reporting required for residents from 1.1.2026), flags the US-citizen dual-tax trap, and outputs a 10-year cash-flow projection. Triggers on "תושב חוזר ותיק", "סעיף 14", "פטור 10 שנים", "תיקון 272". Do NOT use for the returning-resident process (use israeli-returning-resident-navigator), vehicle/customs (use israeli-returning-resident-customs-vehicle), olim chadashim (use israeli-aliyah-navigator), or people leaving Israel (use israeli-relocation-abroad). Planning aid only, not binding tax advice.
license: MIT
---

# Israeli Toshav Chozer Vatik Tax Planner

## Legal notice

This is a free information tool operated by an AI model. It explains the tax rules and helps you organise your own figures. All of its outputs are produced automatically by an AI model, with no involvement, review, or approval by a tax adviser or accountant. The output is not a tax opinion, not a return prepared by a licensed representative, and not professional advice, but a general calculation and explanation only: it does not examine the full extent of your income or your complete documents. An AI model may err, omit data, or present a wrong conclusion.

Any form or text this tool produces is an automatic draft for your personal preparation only, and is not a filed return. Responsibility for reporting and for paying the tax is yours, the binding computation is the Tax Authority's, and representation before the Tax Authority is reserved to those permitted by law. This tool is not a substitute for advice that takes account of the particular circumstances and needs of each person. Consult a tax adviser or accountant before filing or paying. This tool is also not a recommendation to sell, to hold, or to time the sale of any asset, and not a recommendation to claim or to waive any exemption, benefit, or election under the Income Tax Ordinance; decisions of that kind are irreversible and must be reviewed with a tax adviser or accountant before they are made. All use of its output is the user's sole responsibility.


## Problem

Returning Israelis with 10+ years abroad are entitled to the Section 14 exemption, but the rules are confusing in several ways that keep tripping people up. First, the difference between vatik (10+ years, full exemption) and regular toshav chozer (6-10 years, only passive income for 5 years) is misread on most blogs. Second, the 10-year clock starts on the date the user becomes an Israeli tax resident again, NOT on the date they land at Ben Gurion, and these dates can be months apart. Third, Amendment 272 took effect on 1.1.2026: the TAX exemption stays, but the REPORTING exemption was canceled. Vatikim who settled on or after 1.1.2026 must now disclose foreign income and assets to Mas Hachnasa even though no tax is owed. Fourth, US citizens (the largest single returnee cohort, from CA and NY) still owe US tax on the same income Israel exempts; the US-Israel treaty saving clause blocks treaty relief and there is no foreign tax credit because no Israeli tax was paid.

This skill is a planning aid, not binding tax advice. Final filings go through a CPA.

## Instructions

### Step 1: Identify the track

Ask the user, in this order:

1. **How many consecutive years were you a foreign tax resident immediately before returning?** Foreign tax resident means center-of-life outside Israel under the Ordinance (not just "I lived abroad").
   - **10 or more, continuous**: **vatik** track.
   - **6 to 9**: **regular toshav chozer** track. (Older transitional rules that granted vatik status on fewer years applied only to people who became resident in tax years 2007-2009 and are spent for any current returnee. Do not apply them.)
   - **Fewer than 6**: no track. Section 14 does not apply. Stop here and recommend a CPA.

2. **Was the foreign residency continuous?** A multi-month return to Israel during the 10-year window (family moved, kids enrolled in Israeli schools, primary home shifted) can break the chain. Short visits do not. Borderline cases need CPA review.

3. **When did you become an Israeli tax resident again?** Pin a calendar date for center-of-life shifting back to Israel. This is the start of the 10-year clock.
   - Common signals: family moved, kids enrolled in school, primary home shifted, foreign work contract terminated.
   - Physical arrival date can differ by months. Document both.

4. **Do you hold US citizenship, a US green card, or citizenship of any country that taxes worldwide income?** If yes, flag the dual-tax trap (Step 6) and route the user to a US-Israel cross-border CPA.

### Step 2: Apply the right exemption matrix (Israeli tax only)

| Income kind | Source | Vatik | Regular toshav chozer | No track |
|---|---|---|---|---|
| Active (employment, business) | Foreign | Exempt 10 years (Section 14) | Taxable from day 1 | Taxable |
| Passive (dividend, interest, rent, royalty) | Foreign | Exempt 10 years (Section 14) | Exempt 5 years (only if asset acquired during the period abroad) | Taxable |
| Capital gain | Foreign | Exempt 10 years (Section 97(b)(1)) | Exempt 10 years (only if asset acquired during the period abroad and not Israeli-property-linked) | Taxable |
| Any | Israeli | Taxable | Taxable | Taxable |

This matrix is ISRAELI INCOME TAX only. Section 14 does not exempt National Insurance and health-levy contributions, assessed on a resident under the National Insurance Law independently of it, so a projection full of EXEMPT rows is not a projection of zero cost (see `israeli-returning-resident-navigator`). US citizens see Step 6.

**There is no capital-gains cliff at year 10.** Under Section 97(b)(3), if the foreign asset is sold AFTER the ten years the exemption is not lost: the real gain splits on a straight time basis, the part accrued from acquisition to the end of the window stays EXEMPT, and only the remainder is taxed under Section 91(b). The exempt share is (acquisition to end of the 10 years) divided by (acquisition to sale). So do NOT push a user in year 9 or 10 into a rushed sale: that can crystallise US tax (Step 6) and, on a losing position, destroy the loss under Gotcha 12.

**Two carve-outs on the capital-gains rows.** For the vatik row, an asset received under the Section 97(a)(5) tax-exempt gift route (from 1.1.2007) is excluded. For the regular-track row, the asset must not be, directly or indirectly, a right to property located in Israel, so a foreign company holding Israeli real estate does not qualify.

Edge cases to flag (always defer to a CPA):
- **CFC dividends**: the vatik exemption can be challenged on dividends from a foreign company the returnee controls. Do not quote a 25% test. Section 75B turns on control tests (more than 50% of the means of control held by Israeli residents, or more than 40% held by Israeli residents who with a relative hold more than 50%) plus passive-income and foreign-tax-rate limbs. Have a CPA test the structure. See `references/section-14-mechanics.md`.
- **A foreign company you manage from Israel does NOT automatically become Israeli-resident.** Separate from the CFC point above, and the question a returning founder actually has. The "Israeli resident" definition for a body of persons expressly excludes a company whose control and management are exercised in Israel by a first-time resident or veteran returning resident under Section 14(a) where ten years have not passed, unless the company requests otherwise. Running your foreign entity from Israel does not by itself pull its worldwide profits into Israeli tax during the window. Two riders: the relief ends with the same ten-year clock, so year 11 needs a plan; and it does not settle Israeli permanent establishment or the CFC rules. CPA territory.
- **Trust distributions** where the returnee is settlor or beneficiary.
- **Mixed-source income** where part of the work was performed in Israel: the exemption is pro-rated.
- **Equity compensation (RSU, options)**: sourced by where the work was performed during the VESTING period, NOT by grant date. See `references/equity-compensation-sourcing.md`.

### Step 3: Israeli-source income is always taxable

The vatik exemption is FOREIGN-source income only. Throughout the 10-year window the returnee pays normal Israeli tax on:

- Israeli salary (subject to the 2026 labor caps in Step 5)
- Israeli rental real estate
- Israeli TASE securities trading and Israeli mutual funds
- Israeli dividends and Israeli interest
- Business income from Israeli customers

A returnee who plans to open an IBI brokerage and trade TASE on day one needs to know this; many do not.

### Step 4: Apply the 2026 reporting rule

Compare the user's Israeli tax-residency start date (from Step 1) to **1 January 2026**:

- **Residency started before 1.1.2026**: legacy regime. Foreign income remains both EXEMPT and NOT reportable for the rest of the 10-year window. They keep the old "no Form 1301 for foreign income" treatment.
- **Residency started on or after 1.1.2026**: Amendment 272 applies. Foreign income remains EXEMPT but must be REPORTED annually:
  - Form 1301 (annual return).
  - Nispach D-1 (Schedule D-1) listing foreign income.
  - Hatzharat Hon (capital declaration) when the Tax Authority requests one.
  - Trust + CFC disclosures if applicable.

**Trustee-level reporting (new, separate from beneficiary reporting).** Amendment 272 also imposes a NEW reporting obligation on **Israeli-resident trustees** of foreign trusts whose beneficiaries are vatik or oleh, even when the trust itself remains exempt at the beneficiary level. A returnee who is also serving as a trustee of a family trust must check this independently of their personal Form 1301 reporting. The Shibolet writeup (in Reference Links) covers the trustee-side rules; standard practitioner reference for the dual obligation.

For background, read `references/2026-reporting-change.md`.

### Step 5: Apply the 2026 Hok Iddud Israeli-source labor cap

Separately from section 14, the 2026 חוק עידוד עלייה לישראל וחזרה אליה (הוראת שעה), התשפ"ו-2026 grants vatik returnees and olim arriving in the window 5.11.2025 to 31.12.2026 an exemption on ISRAELI-source labor income, with annual caps:

- 2026: 600,000 NIS
- 2027: 1,000,000 NIS
- 2028: 1,000,000 NIS
- 2029: 350,000 NIS
- 2030: 150,000 NIS

This is the single biggest planning lever for a 2026 returnee with a high Israeli salary. Stacking the new Israeli-source labor exemption with section 14 on foreign income can shield substantial total income in the early years. The 2026 cap is calculated proportionally to the residency period during that year.

**What does NOT qualify under this Israeli-source exemption.** Hok Iddud covers labor income only. The following remain fully taxable Israeli-side throughout the 5-year window:

- Rental income (from Israeli or foreign property)
- Accrued interest
- Dividends

A returnee who structures comp as a dividend out of their Israeli company expecting the 600K shield gets none of it.

**Family-employment sub-cap: 140,000 NIS/year.** When the returnee draws labor income from a business owned by an immediate family member (parent, spouse, sibling, child, in-law), the Hok Iddud exemption is capped at **140,000 NIS per year**, separately and lower than the general 600K/1M annual caps above. A vatik returning to a family business who structures their salary assuming the general cap will massively over-exempt. Verify the family-relationship definition with a CPA, since edge cases (spouse's parent, a family member with only partial ownership of the business) need confirmation against the final regulations. This family sub-cap applies for tax years 2026-2029.

**Residency safeguard (clawback for 2028 and 2029).** Eligibility for the full 5-year exemption is forfeited if, in 2028 or 2029, the returnee BOTH **ceases to be an Israeli tax resident** (typically a move back to the host country) **AND spent fewer than 75 days in Israel in one of those years** (the statute reads "be-achat me-otan ha-shanim"). Both conditions are required, so remaining an Israeli resident is what preserves the benefit, but a returnee who is physically absent most of the year will struggle to argue continued residency. This is a hard clawback that voids the full Hok Iddud exemption retroactively, including the 2026-2027 years already taken (the caps total 3.1M NIS of EXEMPT INCOME across 2026-2030, not 3.1M NIS of tax; the tax value is roughly half that at top marginal rates). A vatik planning a sabbatical year, an extended overseas project, or a return-to-the-host-country move in 2028-2029 needs to track day counts against the 75-day floor and consult a CPA before committing to a multi-month absence. **Ceasing Israeli residency also triggers the Israeli exit tax (Section 100A), a deemed sale of assets on the last day of residency, which is a second and larger cost this clawback scenario walks the user into.** Two points that are widely misstated: the deferral is not something the taxpayer elects, Section 100A(b) deems a person who does not pay at departure to have requested it; and no interest or linkage accrues during the deferral period, it runs only from the actual realization. See `israeli-relocation-abroad` and `israeli-digital-nomad-navigator` for the full exit-tax workflow, this skill does not cover it. The 2026 and 2027 cap years carry no such presence test (the standard center-of-life residency rule still applies).

### Step 5.5: Olim credit points (only if the returnee is also an oleh)

**Scope trap first:** the additional immigrant **tax credit points** (nekudot zikui) are an **olim chadashim** benefit under Section 35 of the Income Tax Ordinance. A **toshav chozer vatik who is a returning Israeli citizen (not an oleh) does NOT automatically receive them.** Do not promise a pure returning-citizen vatik these points. A person who holds oleh status AND meets the vatik years-abroad test gets both section 14 and the olim credit points; a returning citizen gets only section 14.

For an oleh (whether or not they also qualify as vatik):

- **The olim scheme runs 54 months from the aliyah date and the schedule is NOT front-loaded: under Section 35 the first 12 months accrue at the lowest rate (1/12 point per month, so 1 point), the next 18 months at the highest (1/4 point per month, so 3 points a year), then 1/6 per month, then 1/12. Do not tell an oleh year 1 is the richest year. Confirm the exact per-year allocation and the current point value against the Tax Authority / Kol-Zchut table.**
- Each point is worth 2,904 NIS/year in 2026 (242 NIS/month), so the benefit is worth roughly **3,000 NIS to 9,000 NIS per year** depending on the year in the taper.
- Applied AGAINST Israeli-source tax (after the Hok Iddud labor exemption is exhausted).
- Useful for olim with modest Israeli salaries that fall under the Hok Iddud cap: the credit points still reduce tax on the portion above the cap or on Israeli interest/dividends/rent.

An oleh who earns 800K Israeli salary in 2026 with 600K exempt under Hok Iddud should still claim the olim credit points against tax on the 200K residual. A returning-citizen vatik in the same position claims section 14 and Hok Iddud only, no olim points.

### Step 6: Special case, US citizens (and other global-taxation citizenships)

If the user holds US citizenship or a US green card, the section 14 exemption does NOT relieve them from US tax. The US taxes citizens on worldwide income. The US-Israel income tax convention (signed 1975, amended by the 1980 and 1993 protocols, generally effective from 1 January 1995) contains a saving clause at Article 6(3) that lets the US tax its citizens "as if this Convention had not come into effect." Because no Israeli tax was paid on the section 14 exempt income, there is also NO foreign tax credit (FTC) available on the US side.

Practical implication: a US-citizen vatik returnee earning foreign dividends, interest, or capital gains owes full US tax on that income at US rates, even though Israel imposes zero tax. The net section 14 benefit on the foreign-passive side is largely zero for US persons.

The same logic applies to citizens of any country that taxes worldwide income regardless of residence (Eritrea, and edge cases). Most other countries (Canada, UK, EU) tax based on residence and do not have this problem once Israeli tax residency is established.

**The Section 14 exemption is optional, and for a US person that matters.** Section 14(a) grants the exemption "unless they requested otherwise in respect of the income, in whole or in part" (ela im ken bikshu acheret). A vatik can therefore decline the exemption on all or part of their foreign income and pay Israeli tax on it. For a US person that is sometimes the better answer: Israeli tax paid generates a foreign tax credit against the US bill, whereas the exemption produces zero Israeli tax and therefore zero FTC, which is exactly why the net benefit above is close to nil. Whether opting in beats opting out depends on the relative rates and the specific income type, so this is a CPA calculation and not a default. But do not present the exemption as automatic and unavoidable, because a US-person returnee who is never told it is waivable loses the only lever that addresses their problem. The same election exists on the regular track under Section 14(c) and on the Hok Iddud caps under its Section 2(a).

If the user is a US person: STOP recommending section 14 as an automatic planning win and route them to a US-Israel cross-border CPA before any major event (RSU vest, sale of US assets, retirement-account distribution). Continued US compliance (Form 1040, Schedule B, Form 8938, FBAR, Form 5471 if controlled-foreign-corporation, Form 3520 for foreign trusts) remains mandatory throughout the 10-year window.

Read `references/us-citizen-dual-tax.md` for the full mechanics.

### Step 7: Clarify the form question

If the user asks "do I file Form 1348?", answer NO. Form 1348 is for Israelis LEAVING Israel who want to claim non-residency. Returning residents file Form 1301 + Nispach D-1, and Israeli banks typically request Form 2409 in connection with an incoming foreign-currency deposit. Ask the specific bank for its own deadline rather than quoting one, this is a bank convention and not a statutory period. See `references/form-1348-fields.md` for the full disambiguation.

### Step 8: Build the cash-flow projection

Run `scripts/cashflow-projection.py` either interactively or with a JSON input that lists each income stream:

```bash
python3 scripts/cashflow-projection.py
# or
python3 scripts/cashflow-projection.py --json my-plan.json
```

The script prints a 10-year year-by-year table and appends the reporting-obligation reminder for the user's residency-start date, plus the dual-tax warning if US-person status is flagged. Read the verdicts precisely: EXEMPT and TAXABLE are Section 14 classifications of FOREIGN income, while Israeli personal-exertion income is marked IL-LABOUR, meaning Section 14 never exempts it but the Step 5 Hok Iddud caps may. The script refuses to run on an unrecognised track, a bad residency date, or a regular-track stream that does not state whether the asset was acquired abroad, because guessing any of those silently produces a confident wrong table. It does NOT compute tax owed and does NOT compute US tax.

### Step 9: Hand off to a CPA

Always close by recommending a CPA before any filing. What to bring: years-abroad documentation (foreign returns, residency certificates); the Israeli tax-residency start date with supporting evidence; records of visits or partial stays in Israel during the 10-year qualifying window, to confirm continuity; an income-stream inventory (source, kind, amount, currency, asset acquisition date, and the vesting calendar for any equity grants); trust and CFC structure documents; and US-person status with US filing history if applicable.

## Examples

### Example 1: Software engineer returning Q1 2026 from 11 years in the US

User: returned to Israel on 15 March 2026. Has been in California for 11 years, working at a US company. Holds US citizenship (born in the US). Wants to know what changes for him vs. someone who returned in 2025.

Reasoning:
- 11 years foreign-resident, continuous: **vatik** track on the Israeli side.
- If center-of-life shifted to Israel on 15.3.2026, that is the start of the 10-year clock. Clock runs 15.3.2026 to 14.3.2036.
- Residency started AFTER 1.1.2026: Amendment 272 applies, foreign income is exempt but must be reported.
- **US citizen**: Step 6 applies. Israeli exemption on foreign income does not relieve US tax.

Output (Israeli side, then US-side note):

- **US W-2 salary** (if he keeps working remotely for the US company, work performed in Israel after the move): mixed-source. The portion performed in Israel is **Israeli-source, taxable** (subject to the 2026 Israeli-source labor cap from Step 5: 600,000 NIS exempt in 2026, proportional). The portion performed in the US before the move is **foreign-source active income, exempt 10 years** on the Israeli side.
- **US 401(k) distribution received in 2027**: foreign passive, **exempt 10 years** on the Israeli side.
- **US RSU vest 2028, granted in 2024 before the move, 4-year vest schedule**: do NOT treat this as a clean foreign capital gain. The Israeli sourcing depends on where the work was performed during the vesting period (see `references/equity-compensation-sourcing.md`). The portion of the vest that vested on work performed in Israel (after 15.3.2026) is **Israeli-source ordinary income, taxable**. The portion that vested on work performed in the US (before 15.3.2026) is **foreign-source ordinary income, exempt 10 years** under section 14. Engage a CPA with a calendar of the vesting period and a workdays-by-location log.
- **All three exempt streams above must still be reported** annually on Form 1301 + Schedule D-1 (Amendment 272).
- **Form 1348? No.**
- **US side**: every one of the above streams remains taxable on the US Form 1040 because of the saving clause. No FTC offsets the US bill since Israel imposed zero tax on the exempt portions. The user needs a US-Israel cross-border CPA before the 2028 RSU vest, because the cross-border calculation is the dominant cost item and standard Israeli planning will miss it.

### Example 2: Doctor returning from Germany after 8 years

User: returned after 8 years in Germany. Has German investment account with stocks bought 5 years ago, and works at an Israeli hospital after the return. German (not US) citizen.

Reasoning:
- 8 years foreign-resident: **regular toshav chozer** track (not vatik).
- No vatik benefits. Only passive-on-foreign-assets-acquired-abroad (5 years) + capital gains on those assets (10 years).
- Germany taxes based on residence; once Israeli tax residency is established the German tax stops. No saving-clause issue.

Output:
- Israeli hospital salary: **taxable from day 1** on the Israeli side. The Hok Iddud Israeli-source labour cap (Step 5) is **NOT available to her**: the statute grants it only to an oleh or a toshav chozer vatik, and she is on the regular track. Do not raise the 600K cap with a regular toshav chozer.
- Dividends from German stocks (acquired during the 8 years abroad): **exempt for 5 years**, then taxable.
- Capital gain when she eventually sells the German stocks: **exempt for 10 years**.
- If she had foreign active income (say, residual private-practice income from Germany after the move): **taxable from day 1** under regular track.

### Example 3: Pre-2026 returnee asking what to file for tax year 2027

User: became Israeli tax resident on 1 June 2024, vatik track. Israeli citizen only.

Output:
- Residency began before 1.1.2026, so the legacy regime runs for the whole window: foreign income is exempt AND not reportable through 1 June 2034, including for tax year 2027.
- After 1 June 2034 foreign INCOME becomes taxable and reportable. But a foreign ASSET sold after that date is not fully taxable: Section 97(b)(3) still exempts the slice of the gain accrued up to 1 June 2034 (see Step 2). Do not advise a rushed pre-2034 sale.

## Bundled Resources

### References

- `references/domain-checklist.md`: what is in/out of scope, with source URLs.
- `references/section-14-mechanics.md`: eligibility, what is exempt, the clock, the year-of-acclimation election, capital-loss matching, 2026 labor cap.
- `references/equity-compensation-sourcing.md`: vesting-period sourcing for RSUs and options, ITA principle.
- `references/us-citizen-dual-tax.md`: the US worldwide-tax trap, treaty saving clause, FTC limitations.
- `references/form-1348-fields.md`: why Form 1348 is NOT the form for returnees, and what they actually file.
- `references/2026-reporting-change.md`: Amendment 272 details (sections 134b + 135(1)(b), effective date, threshold).

### Scripts

- `scripts/cashflow-projection.py`: 10-year exempt-vs-taxable classifier with the post-2026 reporting note and US-person flag.

## Recommended MCP Servers

None. This skill is text-based planning. No live API integration with Mas Hachnasa exists for individual returning-resident filings.

## Gotchas

1. **Clock start date is NOT arrival date.** The 10-year exemption clock starts when center-of-life shifts to Israel, which can lag (or precede) the physical landing by months. Pin the date with documentation.
2. **Residency-date rule for the reporting change.** A returnee whose Israeli tax-residency commenced on 30.12.2025 keeps the legacy "no reporting" treatment for the full window. One day later (1.1.2026) and Amendment 272 kicks in.
3. **Vatik vs. regular is widely confused.** 6-9 years gets a much narrower benefit (5 years on passive only, capital gains on acquired-abroad assets only, never active income). Many online guides treat them as the same. They are not.
4. **CFC and trust traps.** Foreign companies the returnee controls, and foreign trusts where they are settlor or beneficiary, can pierce the exemption. The Section 75B tests are not a simple ownership percentage (Step 2), so flag the structure for CPA review rather than applying a threshold yourself.
5. **Form 1348 is not your friend.** It belongs to Israelis LEAVING Israel. Returnees file Form 1301 + Schedule D-1. Do not file 1348 unless arguing non-residency for a pre-return part-year.
6. **US citizens still owe US tax on Israeli-exempt income.** The saving clause (Article 6(3)) lets the US tax citizens as if the treaty did not exist, and there is no FTC because no Israeli tax was paid. Note the Section 14(a) opt-out (Step 6) is the one lever that changes this. Route every US-person returnee to a cross-border CPA.
7. **RSUs and stock options are sourced by VESTING period, not grant date.** A US RSU granted in 2024 that vests through 2028, where the employee worked in Israel for years 2026-2028, is largely Israeli-source for those years. Section 14 does NOT shield this portion.
8. **Shnat Histaglut does NOT buy an extra exempt year.** File within 90 days of arrival via Form 1130; irrevocable. It treats year 1 as non-resident, useful for a try-before-commit returnee. But Section 14(b)(2) says the acclimation year **is counted** toward the periods it lists, expressly including the Section 14(a) exemption and the Section 97(b)(1) period, so the clock is not pushed to year 11. And Hok Iddud Section 2(e) disapplies Section 14(b)(1) for its own start date, so electing acclimation neither postpones the Israeli-source caps nor forfeits the 2026 one. The real trade-off is residency optionality, not clock extension.
9. **Israeli-source income is fully taxable throughout the 10-year window.** Section 14 exempts FOREIGN income only. TASE trading, Israeli rentals, Israeli salary above the 2026 labor caps, Israeli dividends: all taxed at normal Israeli rates.
10. **Spouse not eligible for vatik.** Marrying a returnee does not make an Israeli who never left a vatik. Joint filing (תיק מאוחד) can drag exempt income into the household calculation in non-trivial ways. The interaction with the spouse's Israeli filing is complex; consult a CPA.
11. **Center-of-life break during the 10-year abroad window can disqualify vatik.** The 10 years of foreign residency must be CONTINUOUS. A 13-month sabbatical back in Israel (family there, kids in Israeli schools) can reset the clock, dropping the returnee to regular track or none. Short visits do not break continuity; multi-month center-of-life shifts can.
12. **Capital losses during the exempt window are NOT carry-forwardable.** Foreign capital losses incurred during the 10-year window cannot be offset against later (post-window) gains. Section 92 matching: a loss is offsettable only if the matching gain would have been Israeli-taxable, and inside the window it would have been exempt. ITA Circular 10/2025 confirms this. Big trap for crypto and stock-heavy years.
13. **The Misrad HaKlitah certificate does not establish Section 14 status, but DO get it.** It is not proof of Section 14 eligibility, which the Tax Authority determines independently. But Hok Iddud defines a toshav chozer vatik for ITS purposes as one meeting Section 14(a) **and holding a returning-resident certificate from the Ministry of Aliyah and Integration**, so it is a precondition to the Step 5 caps and skipping it can forfeit them entirely.

## Reference Links

| Topic | URL |
|---|---|
| Income Tax Ordinance (Nevo) | https://www.nevo.co.il/law_html/law01/255_001.htm |
| Hok Iddud Aliyah 2026 (Nevo) | https://www.nevo.co.il/law_html/law00/241397.htm |
| Kol-Zchut, vatik (10+) | https://www.kolzchut.org.il/he/הטבות_במס_לתושבים_חוזרים_ששהו_בחו%22ל_מעל_10_שנים |
| Kol-Zchut, regular (6-10) | https://www.kolzchut.org.il/he/הטבות_במס_לתושבים_חוזרים_ששהו_בחו%22ל_בין_6_ל-10_שנים |
| BSH CPA, vatik 2026 | https://www.bshcpa.co.il/תושב-חוזר-ותיק/ |
| BSH CPA, 2026 labor cap | https://www.bshcpa.co.il/tax-exemption-returning-residents-olim-2026/ |
| BSH CPA, year-of-acclimation 90-day rule | https://www.bshcpa.co.il/שנת-הסתגלות-תושב-חוזר/ |
| Amendment 272 (Arnon TL) | https://arnontl.com/he/news/ביטול-הפטור-מדיווח-על-הכנסות-פטורות-לע/ |
| Amendment 272 (Shibolet EN) | https://www.shibolet.com/en/cancellation-of-reporting-exemption-for-new-immigrants-and-long-term-returning-residents-regarding-foreign-income-and-new-reporting-obligation-for-israeli-resident-trustees-regarding-trusts-not-requir/ |
| Knesset Research Center analysis | https://fs.knesset.gov.il/globaldocs/MMM/2ef1a063-cd62-f011-a85f-005056aa9911/2_2ef1a063-cd62-f011-a85f-005056aa9911_11_20997.pdf |
| ITA Circular 1/2011 (year of acclimation) | https://www.gov.il/BlobFolder/policy/income-tax-professional-inst-01-2011/he/Policy_IncomeTaxInst_hoz1-2011.pdf |
| ITA Circular 10/2025 (capital loss matching) | https://www.gov.il/BlobFolder/policy/professional-directives-271125-1/he/IncomeTax_professional-directives-271125-1.pdf |
| Y-Tax on capital loss offsetting (Circular 10/2025) | https://y-tax.co.il/capital-loss-offsetting/ |
| S. Horowitz on equity-comp sourcing | https://s-horowitz.com/taxation-of-stock-options-for-employees-who-became-israeli-residents/ |
| Philip Stein, US-Israel treaty | https://www.pstein.com/our-firm/us-israel-tax-treaty/ |
| IRS, US-Israel treaty PDF | https://www.irs.gov/pub/irs-trty/israel.pdf |
| Nefesh B'Nefesh, Benefits for Toshavim Chozrim (Returning Residents) | https://www.nbn.org.il/life-in-israel/government-services/rights-and-benefits/benefits-for-toshavim-chozrim-returning-residents/ |
| Nefesh B'Nefesh, Taxation of new immigrants and returnees | https://www.nbn.org.il/life-in-israel/finances/taxes/taxation-of-new-immigrants-rules-in-israel/ |

## Troubleshooting

**"I do not know my exact Israeli tax-residency start date."**
Walk through the center-of-life factors: where is your family, primary home, work, social ties, schools. Pick the date when the majority of factors shifted. Document with photos, lease, school enrollment, etc. A CPA can finalize.

**"My foreign company sent me a 1099/W-2 for work done after I moved to Israel, is it foreign-source?"**
No. Source follows where the work was performed, not where the payer sits. Work performed in Israel is Israeli-source regardless of who pays.

**"I returned on 15 December 2025, do I get the legacy regime?"**
Probably yes, if your Israeli tax-residency commenced on that date (not 2.1.2026). But the cutover is so close to the 1.1.2026 line that a CPA must confirm the residency-start date and document it carefully.

**"The script gave a weird result for my CFC dividends."**
The script does not handle CFC re-characterization. Treat CFC dividends as a flag for a CPA opinion, not as a clean foreign-passive stream.

**"I'm a US citizen, does section 14 save me?"**
On the Israeli side, yes. On the US side, no. See Step 6 and `references/us-citizen-dual-tax.md`. Engage a US-Israel cross-border CPA before any major event.

---

**This skill is a planning aid, not binding tax advice. Engage a CPA before any filing.**
