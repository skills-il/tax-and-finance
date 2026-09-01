# Getting money back: the Payment Services Law refund routes

Reference for section B of the skill. All four remedies come from the Payment Services Law, 5779-2019 (חוק שירותי תשלום, התשע"ט-2019), full text at <https://he.wikisource.org/wiki/חוק_שירותי_תשלום>.

**Scope, before anything else: all four routes cover a harshaa lechiyuv only.** Sections 34 to 38 are written about a debit authorization sitting on the payment ACCOUNT. They do not reach a charge billed to a card NUMBER, which is the more common shape for a gym, a streaming service or an insurance policy. Sending the bank a s.35(a) demand about a card-billed charge gets it refused, and the three-business-day window in Route 2 is gone by the time the user finds out. Establish the mechanism first: ask whether the charge appears in the bank's list of active authorizations, or only on the card statement. For a card-billed charge the route is the card ISSUER plus the merchant under the ongoing-transaction rules, not these four.

Within that scope, the most useful thing to tell a user: **all four run against the BANK (noten sherutei tashlum lamshalem), not against the beneficiary that took the money.** People waste weeks arguing with the beneficiary when, for an authorization on the account, the bank is the one obliged to refund them.

## Route 1: cancel the authorization going forward (s.34)

Cancels future debits. Does not refund anything already taken.

> המשלם רשאי לבטל הרשאה לחיוב, בכל עת, בהודעה לנותן שירותי תשלום למשלם או בהודעה למוטב; קיבל נותן שירותי תשלום למשלם הודעה מהמשלם כאמור, יודיע על כך למוטב בהקדם האפשרי ולא יאוחר משני ימי עסקים

- Notice to **either** the bank or the beneficiary works. The bank's own online form is a convenience, not a precondition.
- s.34(b): from receipt, and no later than one business day, the beneficiary may not demand further debits and the bank may not execute them.

**s.34(c), the dormancy kill switch.** An authorization unused for 24 months is simply void, and the bank must tell both sides:

> הרשאה לחיוב שלא נעשה בה שימוש 24 חודשים ממועד אישור ההרשאה לפי סעיף 33 או ממועד החיוב האחרון שנעשה מכוחה, לפי המאוחר – אינה תקפה

Useful when a dormant authorization suddenly reactivates after two quiet years: it was already invalid, so any debit under it is unauthorized.

## Route 2: reverse one specific debit, 3 business days (s.35(a))

The broadest remedy and the shortest clock. No need to show anything was wrong with the charge.

> המשלם רשאי לבטל חיוב מסוים שחויב בו מכוח הרשאה לחיוב, בהודעה לנותן שירותי התשלום למשלם, ובלבד שההודעה כאמור תימסר לנותן שירותי התשלום לא יאוחר משלושה ימי עסקים ממועד החיוב; הודיע המשלם כאמור ישיב לו נותן שירותי התשלום למשלם את סכום החיוב, בערכו ביום החיוב, בתוך יום עסקים אחד ממועד ההודעה.

- **User deadline: 3 business days from the debit date.** Refund at the debit-date value, within 1 business day of the notice.
- s.35(b) lets the Minister carve out categories of authorization, so confirm nothing unusual applies to the specific authorization type.

## Route 3: the charge exceeded the authorization (s.37)

The strongest route, because **the customer has no deadline at all** and the bank must act even if it spots the overrun itself.

> חייב נותן שירותי תשלום למשלם את המשלם בחריגה מההרשאה לחיוב שניתנה לו, ישיב למשלם את ההפרש שבין הסכום שבו חויב המשלם ובין הסכום שנותן שירותי התשלום רשאי היה לחייבו על פי ההרשאה, בערכו ביום החיוב (בסעיף זה – סכום ההפרש); השבת סכום ההפרש תיעשה בהקדם האפשרי אך לא יאוחר מיום עסקים אחד מהמועד שבו גילה נותן שירותי התשלום את החריגה מההרשאה או מהמועד שבו הודיע לו המשלם על החריגה, לפי המוקדם; לעניין סעיף זה, יראו כחריגה מהרשאה לחיוב, בין השאר, חיוב מכוח הרשאה שפג תוקפה, חיוב בסכום העולה על הסכום המותר לחיוב בהתאם לתנאי ההרשאה או חיוב במועד שונה מהמועד שנקבע בתנאי ההרשאה.

Three named kinds of overrun, all of them common:
1. a debit under an authorization that had already expired,
2. a debit above the amount the authorization permits,
3. a debit on a different date than the authorization sets.

Refund of the difference within 1 business day. This is why setting a ceiling (tikra) and an expiry at setup matters so much: it converts a later overcharge into a s.37 case.

## Route 4: unreasonably large debit, 7 business days (s.38), check the exception first

> חויב משלם מכוח הרשאה לחיוב וסכום החיוב חרג מהסכום שהמשלם יכול היה לצפות שיחויב בו באופן סביר, בהתחשב בחיובים הקודמים שבוצעו מכוח אותה הרשאה ובנסיבות העניין, ישיב לו נותן שירותי התשלום למשלם את סכום החיוב, בערכו ביום החיוב; הסכום לפי סעיף קטן זה יושב בתוך שבעה ימי עסקים מיום הודעת המשלם על החיוב הלא סביר.

**Do not promise this remedy without checking s.38(c), which disapplies it entirely:**

> הוראות סעיף קטן (א) לא יחולו אם נותן שירותי התשלום למשלם איפשר למשלם, במסגרת אישור בקשת ההרשאה לפי סעיף 33, להגביל את תקרת סכום החיוב בפעולות תשלום הנעשות מכוח ההרשאה ולקבוע את מועד פקיעת תוקפה של ההרשאה.

The trigger is whether the bank **offered** the ceiling-and-expiry option at setup, not whether the customer used it. Most Israeli banks now offer it in their online authorization flow, so assume s.38 is unavailable until shown otherwise, and lead with sections 35 and 37.

Two further limbs: 38(b) lets the bank re-debit if it concludes the conditions were not met, after 15 days' written notice with reasons; 38(d) lets bank and customer contract out of 38(a) altogether.

## Which route to use

| Facts | Route | User deadline | Bank must refund within |
|---|---|---|---|
| Any debit, spotted immediately | 35(a) | 3 business days | 1 business day |
| Expired authorization, over the permitted amount, or wrong date | 37 | none | 1 business day |
| Much bigger than prior debits, and no ceiling was offered at setup | 38(a) | notify promptly | 7 business days |
| Nothing used it for 24 months | 34(c) | none | authorization is already void |

Escalation if the bank refuses: the bank's ombudsman (natziv tlunot hatsibur) first, then the Supervisor of Banks Public Inquiries unit. Quote the section number and the exact clock.

## Closing the account

- **Not free, but capped at 40 NIS total**, and the cap explicitly includes cancelling debit authorizations and standing orders, so those may not be billed on top. Separate 10 NIS caps apply to transferring securities and to transferring foreign currency on closure. Cancelling a bank-issued card as part of closure is also inside a 40 NIS cap.
- Right to close at any time, Payment Services Law s.6(a), but the account-management contract ends only at the end of five business days from when the customer completed the steps the contract prescribes for closure. A bank stalls by disputing whether those steps are done, so get its checklist in writing and confirm completion in writing.
- Switching banks (niud) is separate and is genuinely free.

## Sources

- Payment Services Law, 5779-2019, sections 6, 34, 35, 37, 38: <https://he.wikisource.org/wiki/חוק_שירותי_תשלום>
- Banking Rules (Customer Service)(Fees), 5768-2008, closure-fee cap footnote: <https://he.wikisource.org/wiki/כללי_הבנקאות_(שירות_ללקוח)_(עמלות)>
