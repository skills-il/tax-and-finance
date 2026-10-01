# Reconciling field 800 against the previous declaration

Field 800 = 220 + 460 + 770: private assets less private liabilities, plus the net business
figures, all at cost (general rule 3). Its change since part D section 4 is the question. Only an
event that moves field 800 can explain a change in it. Everything below follows from that, and from
the form's own conventions; none of it is a Tax Authority formula.

## Lines that explain a change

| Line | Direction | Notes |
|---|---|---|
| Income for the period, net of income tax, national insurance and health tax, but BEFORE pension, gemel and hishtalmut contributions | + | Gross income overstates the explanation by the tax paid. Take-home pay understates it by the employee's own fund contributions, which section 6 counts at gross deposits. Include income taxed only by withholding at source, which may never appear on an annual return |
| Money received as a gift or inheritance | + | It sits at its balance in section 3, not at 1 shekel. Document it |
| Proceeds of selling an inherited or gifted asset | + | The asset sat at 1 shekel, so the cash is a real increase with a documented source. Count the proceeds net of tax and selling costs, less 1 shekel, and not any part already counted in income |
| A realised gain that is exempt | + | Only the realised gain, only on a sale, only where not already in income |
| Deposits in section 6 not already inside the income line | + | Any stream included in section 6 (employer, severance, or employee contributions if the income figure used is take-home pay) that the income line does not already contain. The stream decision and this line must match |
| Household living costs | - | Documented, not remembered. The weakest line |
| Interest paid, and linkage added to a liability | - | Cash out, or a CPI-linked principal rising, with no asset event. Count it here unless it is already inside living costs or was capitalised into an asset's cost under general rule 6, and keep it consistent with the mortgage figure chosen (see hard-cases.md) |
| Gifts the household gave to people outside scope | - | Help to an adult child, for example |
| Assets sold or discarded below their declared cost | - | A car declared at 150,000 and sold for 60,000 takes 90,000 out of field 800 with no income line. Left out, it silently masks an equal unexplained inflow |
| Changes in who is in scope | + or - | Marriage or divorce; a spouse opting in or out under section 135(1)(a); a child turning 18; a pre-2026 oleh or veteran returning resident whose ten-year exemption has ended, so foreign assets appear for the first time at their full cost |
| Convention changes between declarations | + or - | A different foreign-balance conversion or mortgage figure from the one used last time moves field 800 with no economic event. Keep the previous convention, or show the difference as its own line |

## Things that look like explanations and are not

- **A loan received.** The cash (or the asset it bought) rises, and section 14, or the part C
  equivalent, rises by the same amount. Net effect on field 800: zero. It answers "where did this
  cash come from" in the line-by-line pass. Counting it against the net gap subtracts it twice.
  A loan later forgiven has become a gift.
- **A rise in an asset's value.** Cost is frozen, so appreciation never reaches field 800.
- **An inherited asset still held.** It sits at 1 shekel and explains 1 shekel.
- **Rent from an inherited apartment.** It is income, already in the first line. Adding it again
  as an inheritance line counts it twice.

## Structural traps

- **The same asset in part A and part C.** A sole trader's one account used for business and
  household, a vehicle, or cash, entered in both parts overstates field 800 and shows up as
  unexplained growth. Each asset appears once.
- **Part B conventions.** A business and a partnership go in at the balance of the capital and
  current accounts, so retained profit is inside them. Only the company vehicle asks for the
  investment and shares at par value. The premium paid over par on subscribed shares therefore
  drops out of field 800 at subscription and comes back as cash on exit; a company's retained
  profit is the company's, not the individual's income, and is not in field 800 at all; and moving a part C business
  into a company swaps assets at cost for shares at par. Show each as an explanation line.
- **A parent paying the seller directly.** Whether that makes the apartment "received as a gift"
  (1 shekel, general rule 2) or an asset bought with gifted money (full cost, the gift as an
  explanation line) is not settled by the form. Do not apply rule 2 to a purchased asset by
  default; a 1 shekel apartment with its mortgage still at full value in section 13 produces a
  large phantom decrease. Route it.

## Worked check (Example 2 in SKILL.md)

| Item | Effect on field 800 |
|---|---|
| Change, 2,050,000 - 1,200,000 | 850,000 to explain |
| Income net of tax, less documented living costs | 400,000 |
| 300,000 loan from a parent, declared in section 14 | 0 |
| Inherited apartment, still held, at 1 shekel | 1 |
| Unexplained | 449,999, about 450,000 |
