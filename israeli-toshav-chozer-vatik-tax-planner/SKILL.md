---
name: israeli-toshav-chozer-vatik-tax-planner
description: Plans Section 14 tax exemption for an Israeli toshav chozer vatik (10+ years abroad). Distinguishes vatik (full 10-year foreign-income exemption) from regular toshav chozer (5-year passive + 10-year capital gains only), pins the 10-year clock to the tax-residency date (not arrival), surfaces the 2026 reporting change (Amendment 272 cancels 134b + 135(b); tax stays exempt, reporting required for residents from 1.1.2026), flags the US-citizen dual-tax trap, and outputs a 10-year cash-flow projection. Triggers on "תושב חוזר ותיק", "סעיף 14", "פטור 10 שנים", "תיקון 272". Do NOT use for the returning-resident process (use israeli-returning-resident-navigator), vehicle/customs (use israeli-returning-resident-customs-vehicle), olim chadashim (use israeli-aliyah-navigator), or people leaving Israel (use israeli-relocation-abroad). Planning aid only, not binding tax advice.
license: MIT
---

# Israeli Toshav Chozer Vatik Tax Planner

## Problem

Returning Israelis with 10+ years abroad are entitled to the Section 14 exemption, but the rules are confusing in several ways that keep tripping people up. First, the difference between vatik (10+ years, full exemption) and regular toshav chozer (6-10 years, only passive income for 5 years) is misread on most blogs. Second, the 10-year clock starts on the date the user becomes an Israeli tax resident again, NOT on the date they land at Ben Gurion, and these dates can be months apart. Third, Amendment 272 took effect on 1.1.2026: the TAX exemption stays, but the REPORTING exemption was canceled. Vatikim who settled on or after 1.1.2026 must now disclose foreign income and assets to Mas Hachnasa even though no tax is owed. Fourth, US citizens (the largest single returnee cohort, from CA and NY) still owe US tax on the same income Israel exempts; the US-Israel treaty saving clause blocks treaty relief and there is no foreign tax credit because no Israeli tax was paid.

This skill is a planning aid, not binding tax advice. Final filings go through a CPA.

## Instructions

### Step 1: Identify the track

Ask the user, in this order:

1. **How many consecutive years were you a foreign tax resident immediately before returning?** Foreign tax resident means center-of-life outside Israel under the Ordinance (not just "I lived abroad").
   - **10 or more, continuous**: **vatik** track.
   - **6 to 9** (or 3+ if they left Israel before 1.1.2009): **regular toshav chozer** track.
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
| Capital gain | Foreign | Exempt 10 years (Section 97(b3)) | Exempt 10 years (only if asset acquired during the period abroad and not Israeli-property-linked) | Taxable |
| Any | Israeli | Taxable | Taxable | Taxable |

This matrix is ISRAELI tax only. US citizens see Step 6.

Edge cases to flag (always defer to a CPA):
- **CFC dividends**: vatik exemption can be challenged on dividends from a foreign company the returnee controls (>25%). See `references/section-14-mechanics.md`.
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

**Family-employment sub-cap: 140,000 NIS/year.** When the returnee draws labor income from a business owned by an immediate family member (parent, spouse, sibling, child, in-law), the Hok Iddud exemption is capped at **140,000 NIS per year**, separately and lower than the general 600K/1M annual caps above. A vatik returning to a family business who structures their salary assuming the general cap will massively over-exempt. Verify the family-relationship definition with a CPA, since edge cases (spouse's parent, family member who owns less than 100%) need confirmation against the final regulations.

**Residency safeguard (clawback for 2028 and 2029).** Eligibility for the full 5-year exemption is forfeited if the returnee spends **fewer than 75 days in Israel during 2028** OR **fewer than 75 days during 2029**. This is a hard clawback that voids the full Hok Iddud exemption (potentially worth 3.1M NIS over the window). A vatik planning a sabbatical year, an extended overseas project, or a return-to-the-host-country move in 2028-2029 needs to track day counts against the 75-day floor and consult a CPA before committing to a multi-month absence. The 2026 and 2027 cap years carry no such presence test (the standard center-of-life residency rule still applies).

### Step 5.5: Stack the tax credit points benefit

Separately from section 14 (foreign income) and Hok Iddud (Israeli labor), vatik returnees and olim are entitled to additional **tax credit points** (nekudot zikui) under the Income Tax Ordinance. The Hok Iddud 2026 article confirms the current scheme:

- **1-3 tax credit points per year for approximately 4.5 years from the return / aliyah date.**
- **Worth roughly 3,000 NIS to 9,000 NIS per year** in reduced Israeli tax, depending on the point allocation by year of residency.
- Applied AGAINST Israeli-source tax (after the Hok Iddud labor exemption is exhausted).
- Useful for returnees with modest Israeli salaries that fall under the Hok Iddud cap, the credit points still reduce tax on the portion above the cap or on Israeli interest/dividends/rent.

This is a small but real benefit that stacks with everything else. A vatik who earns 800K Israeli salary in 2026 with 600K exempt under Hok Iddud should still claim the credit points against tax on the 200K residual.

### Step 6: Special case, US citizens (and other global-taxation citizenships)

If the user holds US citizenship or a US green card, the section 14 exemption does NOT relieve them from US tax. The US taxes citizens on worldwide income. The US-Israel Income Tax Treaty 1995 contains a saving clause (Article 6(3)) that lets the US tax its citizens "as if this Convention had not come into effect." Because no Israeli tax was paid on the section 14 exempt income, there is also NO foreign tax credit (FTC) available on the US side.

Practical implication: a US-citizen vatik returnee earning foreign dividends, interest, or capital gains owes full US tax on that income at US rates, even though Israel imposes zero tax. The net section 14 benefit on the foreign-passive side is largely zero for US persons.

The same logic applies to citizens of any country that taxes worldwide income regardless of residence (Eritrea, and edge cases). Most other countries (Canada, UK, EU) tax based on residence and do not have this problem once Israeli tax residency is established.

If the user is a US person: STOP recommending section 14 as a planning win and route them to a US-Israel cross-border CPA before any major event (RSU vest, sale of US assets, retirement-account distribution). Continued US compliance (Form 1040, Schedule B, Form 8938, FBAR, Form 5471 if controlled-foreign-corporation, Form 3520 for foreign trusts) remains mandatory throughout the 10-year window.

Read `references/us-citizen-dual-tax.md` for the full mechanics.

### Step 7: Clarify the form question

If the user asks "do I file Form 1348?", answer NO. Form 1348 is for Israelis LEAVING Israel who want to claim non-residency. Returning residents file Form 1301 + Nispach D-1, and Israeli banks typically request Form 2409 within 14 days of any incoming foreign deposit (this is a bank convention, not a statute). See `references/form-1348-fields.md` for the full disambiguation.

### Step 8: Build the cash-flow projection

Run `scripts/cashflow-projection.py` either interactively or with a JSON input that lists each income stream:

```bash
python3 scripts/cashflow-projection.py
# or
python3 scripts/cashflow-projection.py --json my-plan.json
```

The script prints a 10-year year-by-year table, marks each stream EXEMPT or TAXABLE on the Israeli side, and appends the reporting-obligation reminder for the user's specific residency-start date. If the input flags US-person status, the output also flags the dual-tax warning. The script does NOT compute the shekel amount of tax owed, and does NOT compute US tax. Those are binding tax-advice items and belong with a CPA.

### Step 9: Hand off to a CPA

Always close by recommending the user engage a CPA before any filing. List what to bring:

- Years-abroad documentation (foreign tax returns, residency certificates).
- Israeli tax-residency start date and supporting evidence.
- Documentation of any visits or partial stays in Israel during the 10-year qualifying window (to confirm continuity).
- Income-stream inventory (each stream: source, kind, amount, currency, asset acquisition date, vesting calendar for any equity grants).
- Trust and CFC structure documents if any.
- US-person status and US filing history if applicable.

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
- Israeli hospital salary: **taxable from day 1** on the Israeli side. The 2026 Hok Iddud Israeli-source labor cap (Step 5) MAY apply if she arrived in the qualifying window (5.11.2025 to 31.12.2026); confirm with a CPA.
- Dividends from German stocks (acquired during the 8 years abroad): **exempt for 5 years**, then taxable.
- Capital gain when she eventually sells the German stocks: **exempt for 10 years**.
- If she had foreign active income (say, residual private-practice income from Germany after the move): **taxable from day 1** under regular track.

### Example 3: Pre-2026 returnee asking what to file for tax year 2027

User: became Israeli tax resident on 1 June 2024, vatik track. Israeli citizen only.

Reasoning:
- Residency before 1.1.2026: legacy regime for the full window.
- Foreign income remains exempt AND not reportable through 1 June 2034.

Output:
- For tax year 2027: foreign income does not need to appear on Form 1301. CPA can confirm specifics.
- For tax year 2034 (final year of the window): same legacy treatment.
- After 1 June 2034: foreign income becomes both taxable AND reportable (and Form 1301 is required like any Israeli resident).

## Bundled Resources

### References

- `references/domain-checklist.md`: what is in/out of scope, with source URLs.
- `references/section-14-mechanics.md`: eligibility, what is exempt, the clock, the year-of-acclimation election, capital-loss matching, 2026 labor cap.
- `references/equity-compensation-sourcing.md`: vesting-period sourcing for RSUs and options, ITA principle.
- `references/us-citizen-dual-tax.md`: the US worldwide-tax trap, treaty saving clause, FTC limitations.
- `references/form-1348-fields.md`: why Form 1348 is NOT the form for returnees, and what they actually file.
- `references/2026-reporting-change.md`: Amendment 272 details (sections 134b + 135(b), effective date, threshold).

### Scripts

- `scripts/cashflow-projection.py`: 10-year exempt-vs-taxable classifier with the post-2026 reporting note and US-person flag.

## Recommended MCP Servers

None. This skill is text-based planning. No live API integration with Mas Hachnasa exists for individual returning-resident filings.

## Gotchas

1. **Clock start date is NOT arrival date.** The 10-year exemption clock starts when center-of-life shifts to Israel, which can lag (or precede) the physical landing by months. Pin the date with documentation.
2. **Residency-date rule for the reporting change.** A returnee whose Israeli tax-residency commenced on 30.12.2025 keeps the legacy "no reporting" treatment for the full window. One day later (1.1.2026) and Amendment 272 kicks in.
3. **Vatik vs. regular is widely confused.** 6-9 years gets a much narrower benefit (5 years on passive only, capital gains on acquired-abroad assets only, never active income). Many online guides treat them as the same. They are not.
4. **CFC and trust traps.** Foreign companies the returnee controls (>25%) and foreign trusts where they are settlor or beneficiary can pierce the exemption. Always flag for CPA review.
5. **Form 1348 is not your friend.** That form belongs to Israelis LEAVING Israel. Returning residents file Form 1301 + Schedule D-1, and the bank typically requests Form 2409 for incoming foreign transfers. Do not file Form 1348 unless you are arguing non-residency for some pre-return portion of a year.
6. **US citizens still owe US tax on Israeli-exempt income.** The US-Israel treaty saving clause (Article 6(3)) lets the US tax US citizens as if the treaty did not exist. No FTC, because no Israeli tax was paid. The single biggest surprise for returnees from CA and NY. Route every US-person returnee to a US-Israel cross-border CPA.
7. **RSUs and stock options are sourced by VESTING period, not grant date.** A US RSU granted in 2024 that vests through 2028, where the employee worked in Israel for years 2026-2028, is largely Israeli-source for those years. Section 14 does NOT shield this portion.
8. **Section 14(b) year-of-acclimation (Shnat Histaglut) election: 90-day deadline, with strategic implications.** Must be filed in writing within 90 days of arrival via Form 1130. The election treats year 1 as non-resident, deferring the start of the 10-year vatik clock to year 2, useful for try-before-commit returnees who may leave again, or for someone who wants to defer the Hok Iddud window start. Tradeoff: electing Shnat Histaglut from a 2026 arrival pushes the Hok Iddud Israeli-source labor exemption start to 2027, sacrificing the 2026 600K cap. For most 2026 returnees with Israeli salary, the cost of skipping the 2026 cap exceeds the value of the deferral. Engage a CPA BEFORE landing or in the first 30 days to weigh this against expected Israeli income. Miss the 90-day window and the deferral option is unavailable.
9. **Israeli-source income is fully taxable throughout the 10-year window.** Section 14 exempts FOREIGN income only. TASE trading, Israeli rentals, Israeli salary above the 2026 labor caps, Israeli dividends: all taxed at normal Israeli rates.
10. **Spouse not eligible for vatik.** A returnee married to an Israeli citizen who never left does NOT make the spouse a vatik. Joint filing (תיק מאוחד) can drag exempt income into the household calculation in non-trivial ways. The interaction with the spouse's Israeli filing is complex; consult a CPA.
11. **Center-of-life break during the 10-year abroad window can disqualify vatik.** The 10 years of foreign residency must be CONTINUOUS. A 13-month sabbatical back in Israel (family in Israel, kids in Israeli schools) during the window can reset the clock, dropping the returnee to regular track or no track. Short visits do not break continuity; multi-month center-of-life shifts can.
12. **Capital losses during the exempt window are NOT carry-forwardable.** Foreign capital losses incurred during the 10-year window cannot be offset against later (post-window) gains. Section 92 matching principle: a loss is offsettable only if the corresponding gain would have been Israeli-taxable, and inside the window the gain would have been exempt. ITA Circular 10/2025 confirms this for vatik exemption periods. Big trap for crypto and stock-heavy years.
13. **Misrad HaKlitah Returning Resident Certificate is administrative, not tax-binding.** The certificate from the Ministry of Aliyah and Integration is useful for absorption services (Sal Klita, ulpan, etc.) but does NOT grant tax benefits and does NOT bind Mas Hachnasa. Section 14 status is determined independently by the Tax Authority under the Ordinance. Do not treat the certificate as proof of section 14 eligibility.

## Reference Links

| Topic | URL |
|---|---|
| Income Tax Ordinance (Nevo) | https://www.nevo.co.il/law/84255 |
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
| Shivat Zion, Tax Benefits for Olim (plain-English overview) | https://shivatzion-support.freshdesk.com/en/support/solutions/articles/501000348713-tax-benefits-for-olim |
| Shivat Zion, Toshav Chozer overview | https://shivatzion-support.freshdesk.com/en/support/solutions/articles/501000348813-returning-resident-toshav-chozer |
| Shivat Zion, 2026 Tax Reform Benefits for New Olim and Returning Residents | https://shivatzion-support.freshdesk.com/en/support/solutions/articles/501000361627-2026-tax-reform-benefits-for-new-olim-and-returning-residents |
| Belong, Toshav Chozer rights and benefits | https://belong.co.il/living/returning-residents-toshav-chozer-rights-benefits/ |

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
