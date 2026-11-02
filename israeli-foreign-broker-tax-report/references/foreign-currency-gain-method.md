# Foreign-currency gain method (שיטת החישוב לנייר ערך במטבע חוץ)

Consult when a user disputes a figure, when the currency moved during the holding period, or before changing the script.

## 1. Which rate and which day (כללי ההמרה)

Income Tax Rules (Conversion to New Shekels of Amounts Originating Outside Israel), 2003 (כללי מס הכנסה (המרה לשקלים חדשים של סכומים שמקורם מחוץ לישראל), התשס"ד-2003):

| Amount | Rate | Day | Rule |
|---|---|---|---|
| Original price (cost) of an asset | Representative rate (שער יציג) | Purchase day or payment date, whichever is earlier | 7(1) |
| Consideration (proceeds) | Representative rate | Sale day or receipt date, whichever is earlier | 7(2) |
| Passive income (dividend, interest) | Representative rate | Day paid or received | 3(a) |
| Foreign tax paid during or before the tax year | Representative rate | Day of payment | 6(1) |
| Loss carried forward | Not re-translated | Carried in shekels | 8 |

"Representative rate" of a day: the rate the Bank of Israel published that day, and if it published none, the last rate it published before that day (rule 1). The rules apply to returns for tax year 2003 onward. Form 1324 cites these rules for converting foreign income. The rule text here was read on Wikisource; the official gazette copy (ק"ת תשס"ד) is a scanned image, so it was not text-checked. Confirm on Nevo before relying on a rule in a dispute.

## 2. The index is the currency (המדד הוא שער המטבע)

Section 88, definition of "מדד": for a security held by an individual that is denominated in foreign currency or linked to it, the currency rate is treated as the index. Form 1325 explanation 4 repeats this. Consequences:

- Adjusted cost A = cost in shekels x (rate on the sale day / rate on the purchase day) = cost in foreign currency x rate on the sale day (Section 88, "יתרת המחיר המקורי המתואם").
- Inflationary amount (סכום אינפלציוני) = the part of the gain equal to A minus C (Section 88). It is not taxed, and it is excluded from the surtax base (Section 121B(e)).
- Real gain (רווח הון ריאלי) = gain minus inflationary amount (Section 88).
- Capital loss (הפסד הון) is defined nominally: the amount by which cost exceeds consideration (Section 88).

## 3. The Moses cases (ע"א 3555/15)

Civil Appeal 3555/15 Oded Moses et al. v. Assessing Officer for Large Enterprises, given 12.9.16; a request for a further hearing was denied by President Naor. The court held that a loss on a foreign-currency security that results from a fall in the exchange rate is not allowed for set-off: Section 92(a)(1) works in two stages, first the nominal loss under Section 88, then only the part that would have been taxable had it been a gain. The change in the exchange rate is the inflationary amount. As described in the further-hearing request, the result is asymmetric: when the index rose, the allowable loss is nominal; when it fell, only the real loss; and when it fell and there is a gain, the taxed gain is the smaller nominal gain, because a negative inflationary amount is not taken into account.

Worked numbers, BoI rates, US dollars (trade-date rates):

| Case | Buy | Sell | C | A | P | Result |
|---|---|---|---|---|---|---|
| Currency fell, gain | 10 AAPL, 1,731 USD with commission, 12.3.2024 | proceeds 2,019.17 USD, 10.6.2025 | 6,316.42 | 6,049.85 | 7,056.99 | gain P - C = 740.57 (not the dollar gain at the sale rate, 1,007.14) |
| Currency fell, loss | 2 AAPL, 418.40 USD, 5.8.2024 | 403.83 USD, 10.6.2025 | 1,599.96 | 1,462.31 | 1,411.40 | allowable loss A - P = 50.91 (nominal 188.56) |
| Currency rose, between | 3 MSFT, 1,201 USD, 12.3.2024 | 1,184 USD, 7.4.2025 | 4,382.45 | 4,528.97 | 4,464.86 | no gain, no loss |

Formula used by the script: real gain = max(0, P - max(A, C)); allowable loss = max(0, min(A, C) - P).

## 4. Lot order and costs

- First in, first out per symbol, unless the seller proves a specific lot (Regulations on computing capital gain on traded securities, 2002, regulation 5). "Identical securities" for foreign securities are those of the same type and issuer managed by one portfolio manager (regulation 1), so lots are matched per account.
- Commissions are part of the original price and are deducted from the consideration; periodic fees are not (Form 1325 explanations 3 and 5). Management and custody fees of the year are deducted from consideration (regulation 6).

## 5. Rate columns

| Column | Applies to | Source |
|---|---|---|
| 25% | Real gain, individual | Section 91(b)(1); Form 1322 |
| 30% | Substantial shareholder (10% of a means of control, at the sale or in the 12 months before) | Sections 88, 91(b)(2) |
| 35% | Foreign security: part of the real gain for days held up to 31.12.2004, by days; rest at 25% | Form 1322 rate list |
| 15% / 20% | Unlinked bond (substantial shareholder 20%) | Section 91(b)(3). Not assumed for a foreign-currency bond, whose index is the currency |

Section 91(b1), the pre-2012 split, does not apply to securities listed on an exchange before 1 January 2012 (Section 91(b1)(1b)), so an ordinary listed share bought before 2012 stays on the form's 25% / 35% columns. "Exchange" includes an approved foreign securities exchange and a regulated market abroad (Section 1).

## 6. Not handled by the script (open items)

CFDs (eToro or other), US Treasury bills (the discount is interest under Section 125C), Splits, reverse splits, mergers, spin-offs, return of capital, options and their exercise, short sales, transfers between brokers, bonds, funds that distribute capital gains, currencies other than the trade currency, a lot bought in one currency and sold in another.
