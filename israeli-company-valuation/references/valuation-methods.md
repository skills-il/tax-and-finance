# Valuation Methods Reference

Method selection, multiple definitions, and the approaches that apply where a standard DCF does not.

## Choosing the governing approach

| Company profile | Primary | Why |
|---|---|---|
| Profitable, stable, forecastable | Income (DCF) | Cash flow is the economic substance |
| Asset-heavy, holding company, real-estate-holding | Asset / NAV | Value sits in the assets, not the earnings stream |
| Loss-making with no credible turnaround forecast | Asset / NAV, as a floor | A DCF on negative cash flow produces a meaningless negative |
| Dense peer set, listed or transacted | Market multiples | The market has already priced the risk |
| Pre-revenue or venture-backed | Round-based methods plus allocation | No forecastable cash flow exists to discount |
| Cyclical at a cycle extreme | DCF on a normalized mid-cycle, never on a peak or trough year | Multiples on a peak year embed the peak |

Always run at least two and reconcile. A single-approach valuation is not reviewable.

## Multiple definitions and the consistency rule

The numerator and denominator must sit on the same side of the capital structure.

| Multiple | Numerator | Denominator | Pairs with |
|---|---|---|---|
| EV / EBITDA | Enterprise value | Pre-interest, pre-tax, pre-D&A | Correct |
| EV / EBIT | Enterprise value | Pre-interest | Correct |
| EV / Sales | Enterprise value | Pre-interest | Correct, weak unless margins are comparable |
| P / E | Equity value | Post-interest, post-tax | Correct |
| P / B | Equity value | Equity book value | Correct |

Wrong pairings, both common and both wrong: enterprise value over net income, and market capitalisation over EBITDA.

Notes on applying multiples in Israel:

- The Israeli listed peer set is thin in most sectors. Global sector data is often the only workable source, and the substitution itself must be disclosed.
- A multiple derived from listed companies embeds liquidity that a private company does not have. That is part of what the marketability discount addresses. Do not silently apply a listed multiple to a private company and then also skip the discount.
- Match the multiple to the same normalized earnings figure you built in the normalization bridge, not to reported earnings.

## Asset / NAV approach

Adjust each balance sheet line from book to market:

- Real estate: needs a licensed appraiser. Flag it, do not estimate it.
- Machinery and equipment: market or depreciated replacement cost.
- Receivables: net of a realistic bad-debt view, not the book provision.
- Inventory: net of obsolescence.
- Intangibles developed in-house: usually absent from the books entirely.
- Liabilities: including contingent ones and any severance provision shortfall.

NAV usually sets a floor for a going concern. If DCF lands below NAV, ask whether the business is worth more broken up than continued, and say so.

## Pre-revenue and venture-backed companies

A standard DCF fails here because there is no forecastable cash flow. Use:

| Method | When |
|---|---|
| Backsolve from the last priced round | A recent arm's length round exists |
| Option pricing model allocation | Multiple share classes with different rights |
| Venture capital method | An exit value and a target return can be reasoned |
| Scorecard or comparable-round benchmarking | Very early, no round yet |

**The allocation waterfall matters more than the headline number.** A company with a preferred round does not have one value per share. Liquidation preferences, participation rights, and conversion mean ordinary shares are worth materially less than preferred shares at the same headline valuation. Valuing ordinary shares as a pro-rata slice of the post-money valuation is simply wrong, and it is the most common error in early-stage Israeli valuations.

Always ask for the cap table with the rights attached, not just the ownership percentages.

## Normalization bridge

Present it as a visible table, from reported to normalized:

| Line | Effect |
|---|---|
| Reported EBITDA | Starting point |
| Owner salary adjustment to market | Usually the largest single item |
| Related-party rent to market | |
| Private expenses run through the company | |
| One-off legal, restructuring, or war-period items | |
| Grant income treatment | |
| Normalized EBITDA | The figure multiples and DCF should use |

## Sensitivity and presentation

The output is a range. Build the grid across:

- WACC, stepped around the central estimate.
- Terminal growth, stepped around the central estimate.
- The marketability discount, stepped across the band you can support.

Present the grid, the range, and the midpoint labelled explicitly as a midpoint rather than as the answer.

## Cross-check discipline

After running the approaches, reconcile:

1. Does the DCF sit inside the multiples range? If not, which assumption drives the gap?
2. Does either sit below NAV? If so, address break-up value.
3. Does the implied exit multiple from the terminal value look sane against current sector multiples? An implied exit multiple far above today's sector median means the terminal assumption is doing the work, and that must be stated.

## Discounts and the levels-of-value ladder

Three things decide the rung, and percentage alone decides none of them:

1. **What the articles actually give this block.** Ordinary resolutions pass by simple majority, but reserved matters, veto rights, board appointment rights and special majorities are set in the articles and the shareholders' agreement. A large minority holder with vetoes holds a blocking position and is not a plain minority.
2. **Who the buyer is.** This is the one most often missed. A stake sold to an existing holder who thereby crosses into full or majority control is a control-consolidating purchase. That block carries swing value, and in real Israeli deals it commands a premium rather than a discount. Applying a textbook minority discount in that situation systematically underprices the seller. If the buyer ends up at or near full ownership, say explicitly that a discount is likely inappropriate and that a control premium is arguable.
3. **Whether tag-along or drag-along equalises the per-share price.** If the minority is contractually entitled to the same price per share as the majority, much of the rationale for a discount disappears.

Never stack a marketability and a control discount without justifying each one independently. Careless stacking is the most challenged move in a review.

## Discount rate components

The risk-free rate and the Israel country risk premium are handled in SKILL.md Step 5, because they are the Israel-specific, fast-drifting inputs. The remaining components are set out here.

**Beta.** A private company has no observable beta. Take industry betas from a peer set, unlever at the peers' structure and tax rate, then relever at the subject's target structure using the subject's Israeli effective rate from Step 4.

Consider a total beta where the owner is undiversified, which is the normal case for an Israeli private company whose owner holds most of their wealth in it: a market beta prices only the risk a diversified investor cannot shed, while an owner with everything in one company bears the total risk. A market beta for a sale to a diversified buyer and a total beta for a valuation from the owner's perspective is a defensible distinction. State which one you used and why.

**Size premium.** An Israeli private company almost always sits below the smallest listed size bucket, and conventional practice adds a size premium. Treat that as contested, not settled: part of the literature argues the premium has largely disappeared from the data. Present it as a choice you can defend rather than as a correction whose omission would be an error. There is no published Israeli-specific size study, so practitioners import US empirical data, and the primary dataset is paywalled. Name the dataset and vintage you are using. If you do not have access to one, say so and present the valuation across a band of size premia instead of asserting a figure you cannot source.

**Company-specific premium.** Key-person dependency, customer concentration, thin management depth. Reason it out loud rather than adding a round number.

**Cost of debt and WACC.** Take the pre-tax cost from the company's actual borrowing rate, or build it synthetically as a spread over the shekel government yield. Apply the tax shield at the Step 4 effective rate. Weight at market values, state whether you used the target or the actual capital structure, and note that market-value weighting is circular and resolved by iteration.

## רכיבי שיעור ההיוון

**ביתא.** לחברה פרטית אין ביתא נצפית. קחו ביתא ענפית מקבוצת השוואה, נטרלו את המינוף לפי מבנה ההון ושיעור המס של קבוצת ההשוואה, ואז מנפו מחדש לפי מבנה ההון היעד של החברה ושיעור המס האפקטיבי הישראלי שלה משלב 4.

שקלו ביתא כוללת כשהבעלים לא מפוזר, וזה המצב הרגיל בחברה פרטית ישראלית שהבעלים מחזיק בה את רוב ההון שלו. ביתא רגילה מתמחרת רק את הסיכון שמשקיע מפוזר לא יכול לפזר. בעלים שכל ההון שלו בחברה אחת סופג את הסיכון הכולל, וביתא כוללת מתפרסמת בדיוק בשביל זה: היא נותנת אומדן טוב יותר למחיר ההון העצמי של בעלים לא מפוזר של עסק פרטי. הבחנה סבירה היא ביתא רגילה למכירה לקונה מפוזר, וביתא כוללת להערכה מנקודת המבט של הבעלים. אמרו באיזו מהן השתמשתם ולמה.

**פרמיית גודל.** יש להתייחס לזה כנתון שנוי במחלוקת ולא כמוסכמה: חלק מהספרות טוען שפרמיית הגודל כמעט נעלמה מהנתונים, ולכן הציגו אותה כבחירה שאתם עושים ויכולים להגן עליה, לא כהשמטה שהיא טעות. חברה פרטית ישראלית כמעט תמיד קטנה מהקבוצה הקטנה ביותר בבורסה, ולכן ויתור על פרמיית גודל מקטין את שיעור ההיוון בצורה מהותית. אין מחקר גודל ישראלי מפורסם, ולכן מעריכים מייבאים נתונים אמפיריים אמריקאיים, ומסד הנתונים המרכזי הוא בתשלום. נקבו בשם מסד הנתונים והמהדורה שאתם משתמשים בהם. אם אין לכם גישה לאחד כזה, אמרו את זה והציגו את ההערכה על פני טווח של פרמיות גודל במקום לקבוע מספר שאתם לא יכולים לבסס.

**פרמיה ספציפית לחברה.** תלות באיש מפתח, ריכוזיות לקוחות, שכבת ניהול דקה. הסבירו את ההיגיון בקול רם במקום להוסיף מספר עגול.

**מחיר החוב ושיעור ההיוון המשוקלל.** קחו את מחיר החוב לפני מס מריבית האשראי בפועל של החברה, או בנו אותו סינתטית כמרווח מעל תשואת האג"ח הממשלתי השקלי. הפעילו את מגן המס בשיעור האפקטיבי משלב 4. שקללו לפי שווי שוק, אמרו אם השתמשתם במבנה ההון היעד או בזה שקיים בפועל, וזכרו ששקלול לפי שווי שוק הוא מעגלי ונפתר באיטרציות.
