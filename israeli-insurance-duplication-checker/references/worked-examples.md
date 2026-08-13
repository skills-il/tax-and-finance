# Worked examples

Two end-to-end audits, showing the map format and the reasoning the skill is meant to produce.

## Example 1. The three-layer health question, worked end to end

The user says: "I have מושלם פלטינום at כללית, a private surgery policy I bought in 2013, and surgery cover through my employer. What am I paying twice for?"

Inventory (Step A) returns, for this adult only: שב"ן at כללית 138/mo; individual health policy bought 2013 with ניתוחים בישראל + ניתוחים בחו"ל + a מחלות קשות rider, 214/mo; employer group ניתוחים, 31/mo; group סיעוד via the kupa, 44/mo.

Tiering (Step B), splitting the individual policy into its benefit heads:

| Covered person | Cover / benefit | Tier | Premium | Overlaps with | Reversible? | Verdict |
|---|---|---|---|---|---|---|
| User | שב"ן ניתוחים | שיפוי | 138 | rows 2, 4 | Yes, kupa must re-accept, אכשרה applies | CAPPED |
| User | Individual policy, ניתוחים בישראל | שיפוי | part of 214 | rows 1, 4 | No, underwritten, bought 2013 | CAPPED |
| User | Individual policy, ניתוחים בחו"ל / השתלות | שיפוי | part of 214 | nothing | No | NOT A DUPLICATION |
| User | Individual policy, מחלות קשות rider | פיצוי | part of 214 | nothing held | No | LEGITIMATE STACKING |
| User | Employer group ניתוחים | שיפוי | 31 | rows 1, 2 | Group cover, ends with the job | CAPPED |
| User | Group סיעוד (kupa) | פיצוי at home / שיפוי in institution | 44 | nothing held | Group, not underwritten | LEGITIMATE STACKING |

What the agent should say. The 2013 purchase date means the שקל ראשון reform never touched this policy, and the employer group policy was never auto-converted either, so this user is squarely in the population the reform left duplicating. Three separate שיפוי layers are stacked on one surgery, and the user can only recover the actual cost once. The catastrophic tail in row 3 is genuinely additional and must not be cut. Row 4 stacks and is not waste. Cut order is driven by the reversible column, not by premium: the employer row costs least and vanishes with the job anyway; the שב"ן row is the only one that can be re-bought, and the 2013 individual policy is the one that can never be replaced. Deliverable 2 puts the "what does row 2 add over rows 1 and 5" question to the insurer in writing before anything is cancelled.

Gaps found (deliverable 3): no אכ"ע anywhere in this inventory for a sole earner. Flag it; do not name a product.

## Example 2. The counterintuitive one, where the answer is "cancel nothing"

The user says: "My agent says my private אכ"ע is redundant because I have disability cover in my pension. I'm a dentist. Should I cancel it?"

Answer: almost certainly not, and the reason is the test, not the ceiling. The fund pays on עיסוק סביר, so a dentist with a hand injury who could work as a clinic administrator may collect nothing from the fund. The private policy exists to fill exactly that gap.

Then do the arithmetic the user actually needs, on a 30,000 monthly salary where the fund benefit is sixty percent of salary and the private benefit forty percent. Per-policy: the fund benefit is capped at 75% of the insured salary, and the private policy at 75% of the average salary insured under that plan, so neither breaches its own ceiling. Combined, the two together come to exactly one hundred percent of income, which reaches but does not exceed the cross-insurer trigger, since offset bites only above "100% ממוצע השכר של המבוטח מכל מקור הכנסה". So the band between the single-policy cap and 100% is legitimate cover, not waste. Even if the total did exceed 100%, the private policy still pays a floor that "לא יפחת, בכל מקרה, משיעור של 30% מסכום הפיצוי החודשי".

Verdict on the private policy: LEGITIMATE STACKING, keep. Add one warning the agent did not give: the excess-premium refund in the uniform policy is capped at seven years and conditional on a claim, so if the user is holding the policy expecting the money back, they should know "לא קרה מקרה הביטוח, המבוטח לא יהיה זכאי להחזר פרמיה".

Pull the מסלקה report before finalising any of this, because the fund's cover rate and track are what set the sixty percent figure, and הר הביטוח does not show them.


## Example 3. A two-adult household, where the REAL WASTE actually appears

The first two examples deliberately end in "keep it". This one does not, and it is the shape most household audits take.

Dani and Maya, two earners, two children aged 9 and 14, one mortgaged flat. Step A is run **twice**, once per adult, and the findings that matter are the ones neither file shows on its own.

| Covered person | Cover / benefit | Tier | Premium | Overlaps with | Reversible? | Verdict |
|---|---|---|---|---|---|---|
| Dani | רכב מקיף (includes the צד ג' chapter) | נכס/אחריות | 340 | row 2 | Yes, annual policy | NOT A DUPLICATION |
| Dani | Standalone צד ג' bought separately | נכס/אחריות | 95 | row 1 | Yes, annual policy | **REAL WASTE** |
| Dani + Maya | ביטוח מבנה tied to the mortgage | נכס | 88 | row 4 | Yes, 451 allows cancelling without fee against alternative cover | **REAL WASTE** |
| Dani + Maya | מבנה section of a separate ביטוח דירה | נכס | included | row 3 | Yes | CAPPED |
| Children (both) | Group dental via Dani's employer | שיפוי | 62 | rows 6, 7 | Group, ends with the job | CAPPED |
| Children (both) | Group dental via Maya's employer | שיפוי | 58 | rows 5, 7 | Group, ends with the job | **REAL WASTE** |
| Children (both) | Basket dental, both children under 18 | n/a, public | 0 | rows 5, 6 | n/a | NOT A DUPLICATION |
| Children (both) | ביטוח תאונות אישיות לתלמידים (compulsory) | פיצוי | 69/yr each | row 9 | n/a, statutory | NOT A DUPLICATION |
| Child (14) | Private personal-accident rider | פיצוי | 29 | row 8 | Underwritten | LEGITIMATE STACKING |

What this shows that examples 1 and 2 do not:

- **Row 2 is textbook ס' 59.** מקיף and צד ג' are two chapters of one prescribed policy, so a standalone צד ג' on top is real double insurance on one asset against one risk. Cancel it. It is also fully reversible, so it goes first.
- **Rows 3 and 4 are the mortgage overlap**, and the cut order is decided by the Reversible column, not by premium: Directive 451 lets the borrower cancel the bank-linked policy without any fee against alternative cover naming the bank as irrevocable beneficiary, so that is the layer that moves. Get the bank's written consent to release the charge BEFORE sending anything.
- **Rows 5 to 7 are invisible from either parent's file alone.** The children are enrolled on both employers' dental plans, and dental is שיפוי, so the second plan recovers nothing beyond the actual invoice. Both children are also under 18, so the basket already covers general dental care with a small co-payment. Cut the more expensive of the two group plans, keep one, and only then ask whether either is worth its premium at all.
- **Row 9 stacks and stays.** Fixed-sum cover pays cumulatively, so the private rider is not waste. But the parent should be told what row 8 already buys, 24/7 and anywhere in the country, before renewing it.

Gaps found (deliverable 3): no סיעוד cover for either adult, and no אכ"ע identified for Maya. Name both as absences; recommend no product.
