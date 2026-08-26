---
name: israeli-company-valuation
description: "Builds an indicative valuation range for an Israeli private company using DCF, market multiples, and the asset approach, with a WACC build-up that uses a live Israeli risk-free rate, the current Israel country risk premium, and the company's own effective tax rate rather than a generic 23%. Use when someone asks what their company is worth, is buying or selling a private Israeli business, needs a valuation for a share transfer or a Section 104 reorganization, or wants to sanity-check a valuation someone else produced. A US-textbook valuation misses Israel's country risk premium, taxes a preferred-enterprise company at the statutory rate, and returns one point estimate instead of a range. Early-stage companies are in scope via round-based methods. Do NOT use for real estate appraisal, listed shares, a startup investment memo, salary versus dividend planning, employee option tax, or a signed valuation opinion for filing."
license: MIT
---

# Israeli Company Valuation

## Legal notice

This is a free information tool operated by an AI model. It explains the tax rules and helps you organise your own figures. All of its outputs are produced automatically by an AI model, with no involvement, review, or approval by a tax adviser or accountant. The output is not a tax opinion, not a return prepared by a licensed representative, and not professional advice, but a general calculation and explanation only: it does not examine the full extent of your income or your complete documents. An AI model may err, omit data, or present a wrong conclusion.

Any form or text this tool produces is an automatic draft for your personal preparation only, and is not a filed return. Responsibility for reporting and for paying the tax is yours, the binding computation is the Tax Authority's, and representation before the Tax Authority is reserved to those permitted by law. This tool is not a substitute for advice that takes account of the particular circumstances and needs of each person. Consult a tax adviser or accountant before filing or paying. All use of its output is the user's sole responsibility.


## Problem

Ask what a private Israeli company is worth and you get either a number with no working behind it or a spreadsheet built from a US textbook. Both fail the same three ways: no Israel country premium in the discount rate, the statutory tax rate applied to a company that may pay far less under the Encouragement of Capital Investments Law, and a single confident number where the honest output is a range. This skill builds the valuation the way an Israeli practitioner does, shows every input and where it came from, and refuses to hand back false precision.

## Instructions

**Open every output with the scope limit, do not only close with it.** A valuation that arrives with a sourced WACC build-up, a parameter table and a sensitivity grid looks authoritative, and that credibility is exactly what makes a bare footer disclaimer insufficient. The limit is about DECIDING, not only about filing.

Work through the steps in order. Do not skip to a number. At every step where a market parameter enters, record the value, the source, and the date you read it, because an undated parameter is the most common reason a valuation gets challenged.

### Step 0. If a real transaction is behind the question, read the documents first

When someone is actually buying or selling a stake, rather than idly curious, the governing documents can make an independent valuation irrelevant or capped. Ask for the shareholders' agreement (הסכם מייסדים or הסכם בעלי מניות) and the articles of association BEFORE modelling anything, and check for:

| Provision | Why it can override your number |
|---|---|
| A pre-agreed valuation formula or multiple | The parties already contracted the answer. Your model is at most a sanity check. |
| Right of first refusal (זכות סירוב ראשונה) | The price named becomes an offer to the other holders, not only to the intended buyer. |
| BMBY (Buy Me Buy You, שווה בשווה) | The named price must work in both directions, so it is a bidding strategy, not a fair value question. Control and marketability discounts largely drop out. |
| Tag-along and drag-along | Determine whether a minority can be forced out or ride along at the same per-share price, which supports or kills a minority discount. |
| Veto and reserved-matter rights | A block with vetoes is not a plain minority, whatever its percentage. |
| Pre-emption on new issues | Affects dilution, and therefore the denominator. |

If a recent arm's length transaction exists in the same shares (a priced round, a prior transfer between the same parties, or a third-party offer), say so prominently. Real transacted evidence in the same security beats a modelled DCF in front of an assessor and in a negotiation.

### Step 1. Fix the purpose and the standard of value

Ask before computing. The purpose changes the answer, not just the wording.

| Purpose | Standard of value | What changes |
|---|---|---|
| Arm's length sale or purchase | Market value | Discounts apply normally |
| Share transfer or reorganization reported to the tax authority | Market value, documented to survive review | Every parameter needs a cited source and date |
| Financial reporting | Fair value | Discounts are constrained; different framework |
| Shareholder dispute, divorce, estate | Set by the forum | Discounts may be inadmissible; ask first |
| Internal sanity check | Indicative | Lightest documentation |

Also fix: the valuation date, the intended user, whether you are valuing the whole company or a specific stake, and whether that stake is controlling.

**Define the denominator before quoting any per-share or percentage figure.** A stake stated as a bare percentage is meaningless on its own. Ask:

- Issued and outstanding, or fully diluted? Fully diluted includes the employee option pool (allocated and unallocated), warrants, SAFEs, and convertible loans. The gap between the two bases regularly moves an effective stake and a per-share price by a large margin.
- Is there more than one share class? A stake in ordinary shares in a company with a preferred round is NOT that percentage of equity value. Liquidation preferences and participation rights mean ordinary shares are worth materially less at the same headline valuation. Route to the allocation waterfall in `references/valuation-methods.md` before quoting anything per share.
- Note that a fresh company valuation also bears on live employee equity grants, since a transaction price between shareholders is evidence the tax authority can weigh against a lower exercise price set earlier. Flag this to the user and send them to their accountant or to israeli-stock-options-tax; do not attempt to price the options here.

### Step 2. Choose the governing approach

| Company profile | Primary approach | Cross-check with |
|---|---|---|
| Profitable going concern with forecastable cash flow | DCF (income) | Multiples, then NAV as a floor |
| Asset-heavy, holding company, or loss-making | Asset / NAV | Multiples |
| Good listed or transacted peer set | Multiples | DCF |
| Pre-revenue or venture-backed | Not DCF. Use round-based methods and an allocation waterfall | See `references/valuation-methods.md` |

Never present one approach alone. Reconcile them and explain any material gap.

### Step 3. Normalize the financials

Owner-managed Israeli companies almost never report an EBITDA you can use as-is. Adjust for:

- Owner salary above or below market. This is usually the single largest distortion.
- Related-party rent, above or below market.
- Private expenses run through the company (vehicle, travel, phone).
- One-off effects, including war-period revenue and cost swings and reservist absence.
- Grant income and capitalized R&D, which are treated inconsistently across small Israeli books.
- Non-recurring legal or restructuring costs.

Show the bridge from reported EBITDA to normalized EBITDA line by line. A valuation whose normalization is invisible cannot be reviewed.

### Step 4. Determine the company's OWN effective tax rate

This is the step generic models get wrong. Do not default to the statutory rate. Establish which regime the company is actually in.

| Regime | Development area A | Rest of country | Dividend withholding |
|---|---|---|---|
| Standard company | 23% | 23% | Per shareholder status |
| Preferred Enterprise | 7.5% | 16% | 20% |
| Special Preferred Enterprise | 5% | 8% (for ten years) | 20% |
| Preferred Technology Enterprise | 7.5% | 12% | 20%, or 4% on a dividend to a foreign COMPANY where at least 90% of shares are held by foreign-resident companies |
| Special Preferred Technology Enterprise | 6% | 6% | As Preferred Technology Enterprise |

Do not accept a reduced rate on the strength of the sector or the headline table. Each track has cumulative eligibility gates, the technology tracks apply only to the Israel-developed share of the IP on a nexus basis, and a pre-2017 Approved or Beneficiary Enterprise can still govern an older company at different rates and a 15% dividend withholding. Ask which regime the approval was actually granted under, and check the gates in `references/israeli-tax-regimes.md` before using anything other than 23%.

Three further Israeli-specific rules that move the cash flows:

- A closely held company faces an annual 2% charge on excess profits under sections 81א to 81ו, from tax year 2025, and sections 62א(א1) and 62א(א)(3) can push company income onto an active shareholder at marginal rates. The base is not flat accumulated profits, the escape routes run on a deadline, and profits sourced from Encouragement-Law income sit outside the charge, so a preferred enterprise is only partly exposed. The thresholds, the shields, and the escape routes are in `references/israeli-tax-regimes.md`; read them before modelling retained cash. All three change how much the company can actually keep, so they hit the forecast and the treatment of surplus cash. Model the distribution behaviour the company will actually adopt, not a company that retains everything tax-free.
- Israel's domestic minimum top-up tax applies for fiscal years beginning on or after 1 January 2026, to groups above EUR 750 million of consolidated revenue in at least two of the four preceding years. It is a domestic top-up only: Israel has not implemented the income inclusion rule or the undertaxed profits rule, so it tops up Israeli low-taxed profit rather than a group's foreign profit. The 15% is a FLOOR, not a cap: it tops low-taxed profit UP. So a preferred-enterprise company modelled at 6% to 12% cannot keep that rate if the group is in scope, and the forecast has to step up to 15%.
- Ask whether a preferred status persists through the forecast AND into terminal value. Assuming a reduced rate forever is a substantive assumption. State it explicitly instead of burying it in a cell.

Use the SAME effective rate in the free-cash-flow tax line and in the debt tax shield. Mixing them is a silent error.

### Step 5. Build the discount rate

Build the cost of equity component by component and show each one.

**Risk-free rate.** Use the yield to maturity on a nominal shekel Israeli government bond (non-index-linked), with maturity matched to the forecast horizon. The ten-year is the conventional default. If you are modelling in real terms, use an index-linked government bond instead.

Fetch this live every time from the Bank of Israel yield page. Never carry a risk-free rate from memory or from a previous conversation, and never reuse one from training data. The page renders via JavaScript behind a bot check, so read it in a browser or use the Tel Aviv Stock Exchange government bond data as the alternative. If you genuinely cannot reach either, say so and ask the user for the current yield rather than inventing one.

**Equity and country risk premium.** As of the July 2026 dataset, Israel carries a Moody's rating of Baa1, an adjusted default spread of 1.27%, a country risk premium of 1.98%, and a total equity risk premium of 6.18%. The implied mature-market premium in the same file is 4.20%.

Two rules here:

1. Check the vintage, and check it against the data-current index rather than the country-premium landing page. That landing page kept saying January long after the July file was published, so a check made there confirms a stale vintage and looks like verification. Report which vintage you used.
2. Do not double count. The 6.18% total already contains the 1.98% country premium. Adding the country premium on top of the total inflates the cost of equity by about two points. State which convention your build-up uses.

**Beta, size premium, company-specific premium, cost of debt and weighting.** Build each one explicitly and show it. A private company has no observable beta, so relever an industry beta at the subject's structure using the Step 4 effective rate, and consider a total beta where the owner is undiversified. Treat the size premium as contested rather than settled, name any dataset you use, and never assert a round number you cannot source. Apply the debt tax shield at the Step 4 effective rate, and weight at market values. The method, the total-beta argument, and the circularity in market-value weighting are set out in `references/valuation-methods.md`.

### Step 6. Project cash flow and terminal value

Free cash flow to firm: EBIT, less tax on EBIT at the effective rate, plus depreciation and amortization, less capital expenditure, less the change in working capital.

Terminal value is usually the majority of the answer, so treat it as a first-class assumption. There are two accepted constructions and you should state which you used:

- **Gordon growth.** Perpetuity growth on the final-year cash flow. Growth must be below WACC, and it must match the inflation basis of the cash flows.
- **Exit multiple.** Apply a sector multiple to terminal-year EBITDA or EBIT. Useful when the company would realistically be sold rather than held forever, and when a defensible sector multiple exists.

Run both and compare. If the Gordon-growth terminal value implies an exit multiple far above today's sector median, the terminal assumption is doing the work, and you must say so rather than let it hide. Growth must be below WACC, and it must match the inflation basis of the cash flows. Nominal cash flows require a nominal bond yield; real cash flows require an index-linked bond. Mixing a real growth rate into a nominal discount rate is a large silent error, and it happens often in Israel precisely because both bond types are readily available.

### Step 7. Bridge enterprise value to equity value

Start from enterprise value, then:

- Less net financial debt.
- Plus surplus cash and non-operating assets. Owner-managed Israeli companies frequently hold non-operating real estate. If the company owns property, flag that a licensed appraiser is needed for it, and check whether the holding makes the company a real estate association (איגוד מקרקעין) under section 1 of the Real Estate Taxation Law. That reclassification is a tax characterisation question, not an appraisal question, and it matters: a sale of SHARES in such a company is an action in an association, charged to betterment tax under the Real Estate Taxation Law instead of ordinary capital gains, with purchase tax landing on the BUYER by reference to the association's real estate. The individual's headline rates do not change (section 48A(b) charges real betterment at up to 25%, rising to 30% for a substantial shareholder at the date of the action or in the preceding twelve months), so do not tell the seller the rate is different. The surtax layers ride on it too, since real betterment is charged as under section 121 of the Ordinance, so the top slice reaches 35% exactly as on an ordinary share sale. What changes is the charging statute, the buyer's purchase tax, the reporting track, and the loss of ordinary capital-gains apportionment. Cash and securities that do not serve to produce the company's income are disregarded in the test, so a cash-rich property company can still fall inside it.
- Less contingent liabilities.
- Age the controlling shareholder's loan account before booking it as a receivable. Under section 3(i1) a withdrawal by a substantial shareholder that is not repaid by the end of the tax year FOLLOWING the year of withdrawal is deemed their income, as a dividend where the company has distributable profits. There is a de minimis: a cumulative withdrawal that stayed at or below ILS 100,000 on every day of the tax year and the preceding one is outside the rule. A debit balance is therefore often neither collectible at face nor tax-free, and in an owner-managed company it is regularly the largest non-operating item on the balance sheet.
- Less any shortfall in the severance provision. Under-funded severance is common and reduces equity value directly.

### Step 8. Apply discounts, carefully

Two separate discounts, each needing separate justification.

- **Marketability.** A private holding cannot be sold quickly at a quoted price. No Israeli regulator publishes a mandated or safe-harbour range, and no Israeli empirical study is published, so any range you use is imported international practice. Name the empirical study you rely on. Do not assert a round percentage with nothing behind it, because in a related-party transfer that is exactly what gets challenged.
- **Control.** Do NOT reach for a lack-of-control discount just because the stake is under 50%. Work the levels-of-value ladder explicitly: control value, then marketable minority, then non-marketable minority. State which rung this interest sits on and why.

Three things decide the rung, and percentage alone decides none of them: what the articles actually give this block, who the buyer is, and whether tag-along or drag-along equalises the per-share price. The second is the one most often missed, and getting it wrong systematically underprices the seller. Work all three through `references/valuation-methods.md` before applying any discount.

Never stack both discounts without justifying each one independently. Careless stacking is the most challenged move in a review.

### Step 9. Cross-check

Reconcile the DCF against the multiples result and against the NAV floor. If they diverge materially, explain why rather than silently picking your favourite. State whether your comparables are Israeli or global, because the Israeli listed peer set is thin in most sectors and global substitution is itself a disclosure item.

Use these multiples, and pair them correctly. An enterprise-value numerator goes only with a pre-interest denominator, an equity numerator only with a post-interest denominator.

| Multiple | Numerator | Denominator basis |
|---|---|---|
| EV / EBITDA | Enterprise value | Pre-interest |
| EV / EBIT | Enterprise value | Pre-interest |
| EV / Sales | Enterprise value | Pre-interest, weak unless margins are comparable |
| P / E | Equity value | Post-interest, post-tax |
| P / B | Equity value | Equity book value |

Add the sector-specific multiple where one governs: EV/ARR or EV/Revenue for SaaS, EV per room for hotels, EV per bed for care homes, price per subscriber for recurring-service businesses. Two wrong pairings that are common and always wrong: enterprise value over net income, and market capitalisation over EBITDA.

### Step 10. Output a range, never a point

Present:

1. The scope limit below, in full, at the TOP of the output.
2. The valuation date, the purpose, and the intended user of the valuation.
3. The standard of value used (market value, fair value, or as set by the forum) and why.
4. The approach chosen and why, plus the approaches cross-checked against it.
5. A valuation range, with a sensitivity grid across WACC, terminal growth, and the marketability discount.
6. A parameter table listing every market input, its value, its source, and the date read.
7. The normalization bridge.
8. Every material assumption stated as an assumption, including whether any preferred tax status was assumed to persist.
9. A statement of who prepared the valuation and on what basis, and that no independent credentialed valuer has signed it.
10. The scope limit again at the end.

Once inputs are settled, run `scripts/valuation_model.py` for the DCF, the WACC build-up, and the sensitivity grid. Pass `--help` for the full flag list.

### If an actual share sale is behind this, say these things

**First establish whether the deal is primary or secondary, because "selling 30% to an investor" usually means neither.** In a secondary sale an existing holder sells existing shares and pockets the proceeds, and everything below applies. In a primary round the company ISSUES new shares, the money goes to the company rather than to the owner, there is no capital gains event for the founder at all, and the arithmetic is different: post-money equals the investment divided by the investor's percentage, pre-money is post-money less the investment, and the founder is diluted rather than paid. Ask which one it is before quoting any figure, and note that an option-pool top-up agreed before the round comes out of the pre-money.

The valuation is a price input, not the deal. Do not compute the seller's tax here, but never let them think the range is what they pocket. State each of these, then send them to their accountant. Full detail, including rates, duties, and deal mechanics, is in `references/transaction-and-sale.md`, which you should open whenever a real transaction is in play.

- **The range is pre-tax.** An individual's real gain on shares bought from 1 January 2003 is generally taxed at 25%, rising to 30% for a seller holding 10% or more of any means of control at the sale or in the prior 12 months, which covers almost anyone selling a meaningful stake in their own company. Surtax applies on top above the annual threshold, and from tax year 2025 a further 2% applies to capital-source income at that same threshold, so a substantial shareholder's marginal rate on the top slice reaches 35%. Ask for the original cost of the shares; shares held from before 2003 follow different apportionment rules.
- **The sale creates duties on a short clock**, it is a related-party transaction where the buyer is an existing holder, share sale versus asset sale is a structuring fork, and value is not price: mechanism terms move cash more than a point of multiple does. All four are set out in `references/transaction-and-sale.md`, which you should have open. Name the duties, never invent form numbers or deadlines.

### Mandatory scope limit

Every output must carry this, and must not be softened:

> This is an indicative valuation range produced from the inputs supplied. It is not a signed valuation opinion, and it is not admissible to the Israel Tax Authority, to a court, or into financial statements. Israel has no statutory licence for a business valuer, so acceptance of a valuation turns on the professional standing, independence, and documentation of whoever signs it. For any transaction, filing, or reorganization, engage a certified public accountant or a credentialed valuer to prepare and sign the valuation.
>
> This range is also pre-tax to the seller, it is not a negotiated price, and it does not account for the terms of any shareholders' agreement. Do not sign a share purchase agreement, set a negotiating anchor, or assume this is what you net, on the strength of this output alone.

Recommend the professional even when the user pushes back. A user who takes an agent-generated number into a share transfer is the primary harm this skill has to prevent.

### If the valuation supports a Section 104 reorganization or a reported share transfer

Section 104 (Part E2 of the Income Tax Ordinance) lets an owner transfer an asset to a company for an allotment of shares without that transfer being a taxable sale at the time. The relief is a deferral, not an exemption. Here the valuation is not the end product: it fixes the share allocation ratio and the carried-over original cost, and a thin or undocumented valuation is itself the risk, because a missing valuation basis is a named cause of disputes with the Israel Tax Authority.

**Do not state a holding period, continuity percentage, form number, or deadline from memory.** Those conditions were materially amended in 2025 and published summaries disagree about what currently applies. Read `references/transaction-and-sale.md` and confirm against the Israel Tax Authority.

## Recommended MCP Servers

Wire these when available. They replace exactly the inputs that go stale.

| MCP | What it supplies | Why it matters here |
|---|---|---|
| `boi-exchange` | Bank of Israel official rates | Currency conversion for multi-currency cash flows and cross-border comparables |
| `tase-mcp` | TASE securities, indices, and Maya company filings | The Israeli comparable-company set for multiples, and reported financials behind them |
| `israeli-cbs` | CBS price indices and statistical series | CPI for the nominal versus real consistency check and for terminal growth |
| `boi-exchange` plus a browser | Government bond yields | The risk-free rate, which must be read live rather than recalled |

## Gotchas

Agent failure modes specific to this domain. These are mistakes the model makes, not the user.

- **Reciting a risk-free rate from training data, or reaching for the Bank of Israel policy rate instead.** The shekel yield curve moves continuously, so any rate recalled rather than fetched is stale by construction and propagates into every number downstream. The policy rate is a different number used in a different place: it informs short-term cost of debt, not the discount rate base. Fetch the bond yield or ask for it.
- **Carrying a stale Israel country risk premium.** Two versions of this. Israel's sovereign rating fell after October 2023 and the country premium rose with it, so a pre-war figure understates the discount rate badly. But the premium also moves between vintages without any rating change, and the dataset's own country-premium landing page went on saying January long after the July file was published, so checking the vintage there confirms a stale number and feels like verification. Check the data-current index instead.
- **Double counting country risk.** A total equity risk premium quoted for Israel already includes the country premium. Adding the country premium again is a mechanical two-point error that looks perfectly reasonable in a spreadsheet.
- **Applying the statutory tax rate reflexively.** A large part of the Israeli economy pays a reduced rate under the Encouragement of Capital Investments Law. Applying the standard rate to a company on the lowest preferred rates overstates the tax drag by roughly threefold. Always ask which regime the company is in before taxing a single shekel of EBIT.
- **Using different tax rates in the cash flow and the tax shield.** They must match. This one is invisible in the output and wrong in the answer.
- **Producing a point estimate, or presenting the range as what the seller pockets.** Answering with one number is false precision, and it is the specific defect regulators criticize, so always return a range with a sensitivity grid. And the range is pre-tax and pre-mechanism, and in a primary round the owner is not paid at all, so say that in the same breath as the number.
- **Inventing a marketability discount.** There is no Israeli published range. A confident round percentage with no cited study behind it is fabrication dressed as expertise, and it is the first thing challenged in a related-party transfer.
- **Reciting the old reorganization holding conditions.** The continuity and restriction rules for Part E2 reorganizations were amended in 2025, and widely published summaries still carry the superseded version. Any specific holding period or continuity percentage recalled from training data is likely to be the old rule. Route the user to confirm rather than stating one.
- **Defaulting to a minority discount because the stake is under half.** If the buyer is an existing holder moving toward full control, the block carries swing value and a discount underprices the seller. Ask who the buyer ends up as before discounting anything.
- **Quoting a percentage or a per-share price without fixing the denominator.** Issued versus fully diluted, and ordinary versus preferred, change the answer materially. Establish the basis first.
- **Modelling before reading the shareholders' agreement.** A pre-agreed formula, a right of first refusal, or a BMBY clause can make the whole model advisory. Ask for the documents when a real deal is behind the question.
- **Forgetting owner compensation normalization.** In an Israeli owner-managed company, unadjusted owner salary is usually the largest single distortion in EBITDA, and multiples applied to a distorted EBITDA carry the error straight through.

## Bundled Resources

| File | Contents |
|---|---|
| `references/domain-checklist.md` | The coverage contract this skill is maintained against |
| `references/valuation-methods.md` | Method selection detail, pre-revenue and venture-backed approaches, allocation waterfall, multiple definitions |
| `references/israeli-tax-regimes.md` | The preferred-enterprise regimes, eligibility gates, and the effective-rate decision tree |
| `references/transaction-and-sale.md` | Seller tax exposure, reporting duties, related-party issues, and deal mechanics when a real sale is in play |
| `scripts/valuation_model.py` | DCF engine, WACC build-up, and sensitivity grid generator |
| `evidence.json` | Every figure in this skill with its source URL, quoted snippet, and fetch date |

## Reference Links

| Source | URL | What to check |
|---|---|---|
| Bank of Israel, bond yields | https://www.boi.org.il/roles/statistics/makamandbonds/yield/ | The shekel risk-free rate. Read in a browser, the page is JavaScript-rendered behind a bot check |
| Tel Aviv Stock Exchange, government bonds | https://market.tase.co.il/he/market_data | Fallback risk-free source |
| Damodaran, current data index | https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datacurrent.html | Industry betas, sector multiples, AND the country-premium file actually in force. Check the vintage HERE |
| Damodaran, country risk premiums | https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/ctryprem.html | Israel country premium, equity risk premium, sovereign rating. This landing page lags the current file, so confirm the vintage against the index above |
| PwC, Israel corporate tax | https://taxsummaries.pwc.com/israel/corporate/taxes-on-corporate-income | Standard corporate rate, top-up tax, closely held company rules |
| PwC, Israel tax credits and incentives | https://taxsummaries.pwc.com/israel/corporate/tax-credits-and-incentives | Preferred-enterprise rates and eligibility conditions |
| Israel Tax Authority | https://www.gov.il/he/departments/israel_tax_authority | Current rates, forms, filing deadlines, circulars |
| Israel Tax Authority, tax rulings | https://www.gov.il/he/service/preliminary-taxation-decisions | The advance ruling route |
| Central Bureau of Statistics | https://www.cbs.gov.il | CPI for the nominal versus real check |
| Reorganizations under Section 104 | https://y-tax.co.il/en/reorganization-and-structural-changes-section-104/ | Sub-section routes. Treat holding-condition detail as possibly superseded by the 2025 amendment |
| PwC, Israel other issues | https://taxsummaries.pwc.com/israel/corporate/other-issues | Non-taxable reorganization principle and the deferral mechanism |

## Troubleshooting

See `references/troubleshooting.md`.
