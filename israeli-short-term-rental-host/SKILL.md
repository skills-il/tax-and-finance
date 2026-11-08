---
name: israeli-short-term-rental-host
description: "Not tax advice and not a filed return. Profit sheet and tax-exposure map for an Israeli resident who rents an apartment, room or unit on Airbnb or Booking for short stays. Use when the user asks 'how is my Airbnb income taxed in Israel', 'mas al Airbnb', 'hashkara le-tvach katzar', 'do I need to open an osek for Airbnb', 'is short-term rental exempt like regular rent', or wants a per-booking profit sheet, a VAT threshold check, a Hebrew-English listing or house rules. Computes on the host's own bookings, shows what the business, 10% and exemption treatments would each cost and which one the Tax Authority's reported position points to, flags VAT, National Insurance, licence, bylaw and insurance risks, and drafts listing text. Prevents the common mistake of assuming the residential rent exemption automatically covers nightly guests. Do NOT use for long-term leases (use israeli-rental-agreements) or for choosing a route or filing on the user's behalf."
license: MIT
compatibility: "Works on every agent. The calculator script needs Python 3 (shell agents); on chat surfaces the agent applies the same formulas to the user's figures in the conversation."
---

# Israeli Short-Term Rental Host

## Legal notice

This is a free information tool operated by an AI model. It organises your own booking figures into a profit sheet, shows how different tax treatments would apply to them, and explains the rules that bear on short-term rental. All of its outputs are produced automatically by an AI model, with no involvement, review, or approval by a tax adviser or accountant. The output is not a tax opinion, not a return prepared by a licensed representative, and not professional advice, but a calculation on the figures you supplied and a general explanation only: it does not decide how your activity is classified, does not examine the full extent of your income or your complete documents, and does not check your building's bylaws or your insurance policy. An AI model may err, omit data, or present a wrong conclusion.

Any text this tool produces is an automatic draft for your personal preparation only, and is not a filed return. Responsibility for reporting and for paying the tax is yours, the binding computation is the Tax Authority's, and representation before the Tax Authority is reserved to those permitted by law. This tool is not a substitute for advice that takes account of the particular circumstances and needs of each person. Consult a tax adviser or accountant before filing or paying. For questions about your building's bylaws, planning permission or your lease, consult a lawyer. All use of its output is the user's sole responsibility.

## Problem

Israeli hosts usually assume Airbnb income is "rent", so the monthly residential exemption or the flat 10% route covers it. The Tax Authority has said publicly that regular short-term renting is a business, and the statutes behind both residential benefits require a residential tenant. Hosts also miss the VAT question, National Insurance, the business-licence threshold, building bylaws and insurance, and few know what a booking actually earns after costs.

## Instructions

### Step 1: Collect the host's facts

Ask for what the calculation needs; do not guess figures.

| Fact | Why it matters |
|---|---|
| Bookings for the tax year: check-in date, nights, what the guest paid (nightly price plus the cleaning fee charged), the platform's fee, direct cost (cleaning, laundry, supplies) | The tax and VAT base is what the guest paid; the platform fee is an expense, not a reduction of receipts. A platform earnings export usually has all of it. |
| Does the host live in the flat when it is not rented? | Running costs of a home are personal expenses (Income Tax Ordinance section 32(1)); only the rental share is deductible. |
| Annual running costs of the unit (arnona, utilities, internet, insurance, maintenance) | Deductible only for the rental share, and only under a treatment that allows expenses. |
| What is rented: whole apartment, room in the host's own home, unit in the home; how many units | Scale and type feed the business question and the licence threshold. |
| Services offered (cleaning between stays, linens, breakfast, check-in) | Services are a business indicator. |
| Other residential rent the household receives | The exemption ceiling is shared by all of it. |
| Age (60 or older?), marginal income-tax rate if known | The regular rent route has lower brackets from age 60; business profit is taxed at the host's marginal rate. |
| VAT status (none, osek patur, osek murshe) | Changes what the gross contains. |
| Owner or tenant of the flat; building type | Bylaws and the lease can forbid short-term rental. |

### Step 2: Run the profit sheet and scenarios

```bash
python3 scripts/str_host_calc.py bookings.csv --year 2026 --fixed-costs 18000 --lives-in --marginal-rate 0.31
python3 scripts/str_host_calc.py --demo --lives-in --marginal-rate 0.31
```

CSV columns: `check_in,nights,gross,platform_fee,direct_cost`. On a chat surface, apply the same formulas in the conversation and show the table.

The script prints:
1. A per-booking profit sheet: gross, platform fee, direct cost, the deductible share of running costs (by nights booked when the host lives there), profit and profit per night.
2. The VAT position: gross receipts against the osek patur ceiling for the year (122,833 NIS in 2026; 120,000 NIS in 2024 and 2025) and, if registered, the VAT inside the gross at 18%.
3. Income tax under each treatment, as a comparison. Income is split across months by night, so a stay that crosses a month counts in both.
   - A. Business income: profit times the host's marginal rate, plus National Insurance on the profit. This is where the Tax Authority's reported position points for regular short-term renting.
   - B. Section 122: a flat 10% of gross rent, no expenses, no depreciation. The section is barred for business income.
   - C. The 1990 exemption law: up to 5,654 NIS a month tax-free (tax years 2024 to 2027) for all the household's residential rent together, shrinking above the ceiling and reaching zero at 11,308 NIS a month; the rest is taxed. It needs a residential tenant and a signed residence-only document.
   - D. The regular rent route (rent that is neither a business nor in a special track): profit at the marginal rate, from 31% for a host under 60, with lower brackets from age 60.
4. What the business treatment triggers, and other flags.

Present all four so the cost of the classification is visible, then say plainly which treatment the Tax Authority's statements point to. Never choose the route for the user and never tell them their activity "is not a business".

### Step 3: Explain the classification question honestly

- **The statutes.** Section 122 applies only "if the rent income is not business income". The exemption law covers a flat "used as a residence by an individual tenant", excludes a flat that is or must be recorded in business books, and applies only if the landlord holds a document signed by the tenant confirming residential use only. A nightly guest does not naturally produce that document.
- **The Tax Authority's position.** In 2016 it told the press that hosts who rent short-term on a regular basis are running a business activity, and that one-off rentals were not the target. In 2017 its spokesperson said short-term rental is like renting a zimmer or any other business and the residential benefits do not apply. No formal circular on short-term rental was found; say that the position is publicly reported, not codified.
- **Grey areas with no published answer:** a room in the host's own home, a one-off rental while the family is abroad, and whether offering no services changes the answer. Say these are unresolved and belong with a tax adviser or accountant.
- **Mixing routes.** Income from the same flat cannot be split between routes in the same year.

### Step 4: What the business treatment triggers, VAT and National Insurance

- **Obligations.** If the activity is a business, the usual consequences are: an income-tax file, VAT registration before starting (the VAT Law requires a dealer to register, section 52), advance tax payments during the year (Income Tax Ordinance section 175), an annual return and books with a receipt for every booking. A salaried host who has never filed a return should hear this list plainly, with the accountant setting up the details.
- **VAT.** The VAT Law exempts residential rental "except lodging in a hotel", and defines a hotel as a place that usually lodges at least five people for payment. The Tax Authority's 2017 statement said that renting a flat to a tourist is generally VAT-liable at a zero rate, while the statute's zero rate names lodging in a hotel. The zero rate is for a tourist as the VAT Law defines one (a visitor in Israel on a visa); stays by Israeli residents carry the standard rate. The cautious path is to plan on registering and settle with a professional which stays, if any, are zero-rated.
- **National Insurance.** Rent taxed under section 122 and tax-exempt non-work income are not counted for contributions; rent taxed on the regular route is not covered by that exemption. If the activity is a business, contributions apply on the profit for a self-employed person, defined by hours (at least 20 a week on average) or by income relative to the average wage. Check current figures on btl.gov.il.
- **Reporting rent.** A host who files an annual return reports residential rent in the return's rent fields; Tax Authority directive 5/2026 runs online reporting for those who pay the 10% without a return, and from tax year 2024 a lease or a lawyer-signed affidavit is attached to an online rental report. The 10% tax, where it applies, is due within 30 days of the end of the tax year.
- **Selling the flat later.** Under section 122(c), using the 10% route adds the depreciation that could have been claimed back to the sale value when computing betterment tax. Mention it, and leave the sale question to the accountant.

### Step 5: Licensing, building and insurance risks

- **Business licence.** Renting more than four holiday units with services needs a business licence under the Business Licensing Order.
- **Planning.** A 2025 Tel Aviv magistrate ruling held that renting a flat for less than a month is a non-conforming use of a residential flat. Treat it as a risk, not settled law.
- **Building bylaws.** A condominium registrar has barred short-term rental in a building whose bylaws limit use to residence. Ask the host to read their building's registered bylaws (תקנון). A tenant also needs the lease to allow subletting.
- **Insurance.** The Insurance Contract Law requires the insured to notify the insurer in writing of a material change. Tell the host to tell their home insurer about paying guests and get the answer in writing.

### Step 6: Listing and house rules

Draft, in Hebrew and English, from the host's facts only:
- A listing description: what is rented, beds, access, neighbourhood, what is and is not included. No claims the host did not state (no "licensed", "kosher" or "accessible" unless the host says so and can back it).
- House rules: quiet hours that match the building's bylaws, guest count, smoking, waste and recycling, check-in and check-out.
- A safety card for guests: where the protected space (ממ"ד or shelter) is and what to do when a siren sounds, emergency numbers for police, ambulance and fire, where the gas and water shut-offs are.
- A short check-in message.

Keep tax wording out of guest-facing text.

## Examples

### Example 1: Whole apartment in Tel Aviv
User says: "אני משכיר את הדירה שלי ב-Airbnb כשאני בחו"ל, בערך 60 לילות בשנה. כמה מס אני משלם?"
Actions: collect bookings and costs; run the script with the host's marginal rate and `--lives-in`; show the four treatments and the business obligations; explain that the Tax Authority's reported position is business income for regular renting while one-off rentals are a grey area; flag bylaws and insurance.
Result: a per-booking profit sheet, the cost of each treatment side by side, and a list of questions for their accountant.

### Example 2: Room in the host's home
User says: "I rent a spare room on Booking. Do I need to open an osek?"
Actions: VAT check against the osek patur ceiling; explain the unsettled VAT reading and the grey area for a room in the owner's home; National Insurance pointer.
Result: the VAT position on the host's numbers and the open questions, routed to a professional.

### Example 3: Listing and house rules
User says: "תכתוב לי תיאור דירה וחוקי בית בעברית ובאנגלית"
Actions: draft from the host's facts, including the protected-space card.
Result: ready-to-paste listing, house rules and check-in message.

## Bundled Resources

### Scripts
- `scripts/str_host_calc.py` -- Per-booking profit sheet, VAT threshold check, the four income-tax treatments and the business obligations, on the host's own bookings. Run: `python3 scripts/str_host_calc.py --help`

### References
- `references/tax-treatments.md` -- The statutes, figures by tax year and the Tax Authority's reported position, with sources. Consult before explaining any tax treatment.
- `references/host-checklist.md` -- Pre-launch checklist (bylaws, lease, insurance, licence, records) and the listing / house-rules template. Consult when the host is starting out or drafting guest texts.

## Gotchas

- Agents apply the residential exemption or the 10% route to Airbnb income by default. Both statutes require a residential tenant, section 122 is barred for business income, and the Tax Authority's reported position treats regular short-term renting as a business.
- Agents state the Tax Authority's position as a published circular. None was found; it rests on statements reported in 2016 and 2017.
- Agents quote an old exemption ceiling (5,030 or "about 5,000"). It is 5,654 NIS a month for 2024 to 2027.
- Agents leave VAT out, or assume every stay is zero-rated. The Tax Authority reported short-term rental to tourists as VAT-liable at a zero rate; plan on registering and confirm the rate per guest.
- Agents deduct all of a home's running costs. When the host lives there, only the rental share is deductible.
- Agents use the platform payout as income. The base is what the guest paid; the platform fee is an expense.
- Agents treat the exemption ceiling as per flat. It is per month for all the household's residential rent combined.
- Agents choose a route for the host. The skill shows the cost of each and leaves the classification to a professional.

## Reference Links

| Source | URL | What to Check |
|---|---|---|
| Exemption law, 1990 (Wikisource) | https://he.wikisource.org/wiki/חוק_מס_הכנסה_(פטור_ממס_על_הכנסה_מהשכרת_דירת_מגורים) | Ceiling by year, residential-tenant and signed-document conditions |
| Income Tax Ordinance s.122 (Wikisource) | https://he.wikisource.org/wiki/פקודת_מס_הכנסה | 10% route, business-income bar, payment deadline |
| VAT Law (Wikisource) | https://he.wikisource.org/wiki/חוק_מס_ערך_מוסף | Section 31 exemption, hotel definition, osek patur ceiling |
| Tax Authority directive 5/2026 | https://www.gov.il/BlobFolder/policy/inst-5-2026/he/IncomeTax_inst-5-2026.pdf | Online rental reporting, affidavit duty, rent fields in the annual return |
| Kol Zchut, rental exemption | https://www.kolzchut.org.il/he/פטור_ממס_על_הכנסה_מהשכרת_דירה_למגורים | Current figures, no mixing of routes |
| Globes, Tax Authority on Airbnb (2017) | https://www.globes.co.il/news/article.aspx?did=1001202409 | The spokesperson's statement |

## Troubleshooting

### "My accountant says the 10% route is fine"
Cause: the facts may differ (a one-off rental, a long stay, a different arrangement); this skill only reports the statutory conditions and the Tax Authority's publicly reported position.
Solution: the accountant's view on the host's full facts governs; record the reasoning they give.

### Bookings span two tax years
Cause: the script warns when check-in years differ from `--year`.
Solution: split the CSV by tax year and run it once per year, since ceilings and rates are per year.

### The script shows the osek patur ceiling as missing
Cause: the ceiling for that year is not in the script (only 2024 to 2026 are).
Solution: check the current figure in the VAT Law and pass the result to the host manually.
