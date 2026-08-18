# Form 1348 - What it Actually Is (and Why It Is NOT For Returning Residents)

## The common confusion

Many guides, forum posts, and even some practitioners conflate "declaration of residency" with "the form a returning resident files to claim section 14." They are different things.

**Form 1348** ("הצהרת תושבות" / "Declaration of Residency") is filed as a Nispach (appendix) to Form 1301 by people LEAVING Israel who want to argue they are NOT Israeli tax residents in a given year, despite triggering the day-count presumption (183+ days in the year, or 30 days in the year plus 425 days across the three-year window).

If you are a returning resident, **you do not file Form 1348** as part of claiming section 14. You are not arguing you are NOT an Israeli resident. You are arguing the opposite: that you ARE an Israeli resident again, and that you arrived with vatik status.

For details on Form 1348 in the LEAVING direction, see the `israeli-relocation-abroad` skill.

## What returning residents actually file

1. **Form 1301** - the annual return for individuals. Required for the year of return (and every year of the 10-year window, especially from 1.1.2026 forward).
2. **Schedule D-1 (נספח ד-1) to Form 1301** - foreign-source income. Pre-2026 vatikim could skip this for foreign income; post-2026 vatikim must complete it (income is still exempt, just reported).
3. **Form 2409** - bank-level declaration of toshav chozer status. Israeli banks typically request this form within 14 days of an incoming foreign-currency deposit, but the 14-day window is a bank convention, NOT a statute. Check the specific bank's policy.
4. **Returning Resident Certificate (תעודת תושב חוזר)** - issued by the Ministry of Aliyah and Integration (Misrad Ha'Aliyah ve'haKlitah). Useful for absorption services (Sal Klita, ulpan, etc.). The certificate does NOT grant tax benefits under the Income Tax Ordinance and does NOT bind Mas Hachnasa; section 14 tax status is determined independently by the Tax Authority. BSH CPA: "תעודת תושב חוזר ותיק המוענקת ע"י משרד הקליטה אינה מקנה הטבות מס מכוח מעמד תושב חוזר כהגדרתו בפקודת מס הכנסה ואינה מחייבת את רשות המסים בעניין תושבות לצורכי מס."
5. **Section 14(b) election form** (only if the returnee wants the year-of-acclimation deferral) - filed in the first year.
6. **Hatzharat Hon** (capital declaration) - filed only on direct request from the Tax Authority. Post-2026, vatikim must comply and disclose foreign assets when requested.
7. **CFC / trust disclosures** - additional forms if the returnee is a controlling shareholder of a foreign company, or a settlor/beneficiary of a foreign trust.

## Why this skill flags Form 1348 anyway

Because the user prompt and many secondary guides mention Form 1348 in the context of returning residents, the skill explicitly documents that this is a misnomer. If a returnee opens a tab on the Tax Authority site looking for "Form 1348 for returning residents," they will not find one - and they should not file Form 1348 unless they are actually arguing non-residency.

## Worked example of the confusion

A common scenario: a returnee who spent 9 months in Israel during the year of return, and also some weeks at the start of the year still abroad. They might be told "file Form 1348 to confirm your tax-residency position." If the position is "I am an Israeli tax resident as of X date, here is the foreign income before that date as a non-resident," then Form 1348 is correct only for the pre-X portion of the year (arguing non-residency for the early part). For the post-X portion they are claiming residency + section 14 exemption, which is done through Form 1301 + Schedule D-1.

## Sources

- y-tax: https://y-tax.co.il/form-1348-residency-termination-form-residency-declaration/
- BSH CPA on 1348: https://www.bshcpa.co.il/טופס-1348/
- BSH CPA on the Misrad HaKlitah certificate not binding ITA: https://www.bshcpa.co.il/תושב-חוזר-ותיק/
- ITA Form 1348 PDF: https://www.gov.il/blobFolder/service/annual-tax-report/he/Service_Pages_Income_tax_itc1348_18.pdf
