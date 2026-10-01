# Hard cases the form does not settle

The form's general rules decide most entries. The cases below are the ones where they do not, or
where the obvious entry counts the same money twice. For each, the form text is quoted where it
speaks, and where it is silent the skill presents the readings and routes the choice to the
filer's representative. Nothing here is a Tax Authority position unless it quotes the form.

## Employee equity

Shares or units a trustee holds for the employee are the employee's asset, in part A section 7, at
what they actually cost (general rule 3, "the amount the asset actually cost you"), with the 1
shekel floor of general rule 8 where they cost nothing. That case is in SKILL.md. The others:

| State on the declaration date | Why it is hard | What to do |
|---|---|---|
| Granted but not vested | The form has no line for a contingent right and does not say whether one is an asset | Flag it; do not invent a line or a value |
| Vested and sold, proceeds still with a foreign broker or plan administrator | The proceeds are money, and section 3 covers accounts "in Israel and abroad" including digital accounts, while section 7 covers securities "in Israel and abroad". Users often forget the account exists | Collect the broker statement as at the declaration date and enter it in section 3 or 7 |
| Plan with no Israeli trustee (foreign parent plan) | The trustee statement that usually carries the cost figure does not exist | Collect the grant, vesting and any exercise records; route the cost question |
| Vesting value taxed as salary | One reading keeps the general rule 8 floor of 1 shekel; another treats the amount already taxed as the cost. The form does not choose | Present both readings and let the representative fix the treatment |

## Digital assets

Section 4 asks for "quantity, purchase date, wallet address and cost in shekels". An exchange's
balance file, which the form names as the annex, shows quantities and not cost, so the full trade
history is needed to substantiate the cost column. The form does not say:

- how cost carries through a coin-to-coin swap (the shekels originally paid, or the value given up);
- how to treat staking rewards, earn products and airdrops;
- whether a stablecoin or fiat balance held at an exchange is a section 4 or a section 3 item.

Present each as an open question. A self-custody wallet is still declared, with its address, even
when there is no exchange record.

## Pension, gemel and hishtalmut: withdrawals and transfers

Section 6 asks for "the sum of all the deposits in the plans, without taking into account interest,
linkage or other gains". It says nothing about money taken out. If a fund was partly withdrawn (in
practice often a keren hishtalmut at its liquidity point, often to help buy an asset the user also
declares), entering gross deposits while the withdrawn money also sits in a bank balance or inside
an asset's cost counts it twice. A transfer between funds raises the same question. Ask about
withdrawals and transfers and flag the treatment for the representative.

## Mortgages and guarantees

Section 13 says "record the debt in cost terms only". A mortgage statement shows several figures:
outstanding principal, principal with linkage on a CPI-linked track, and a payoff amount that adds
early-repayment fees. The form does not name one. Show which figure was used and why, and flag it.

A guarantee given for someone else's loan is a contingent liability. The form has no line for it,
and it is not a debt to a financial institution (section 13) or to a private lender (section 14).
Raise it with the representative rather than inventing a line.

## Household contents and jewellery

Section 11 says "record the cost of the household contents", and section 10 asks for the cost of
jewellery, gold, diamonds and collections. Jewellery received as a gift goes in at 1 shekel under
general rule 2. For contents bought over many years without receipts:

- a 0 for a furnished home is a wrong declaration;
- inventing a precise figure is also wrong;
- how to present a reasoned aggregate, with a note on its basis, is a question for the
  representative.

On a first declaration this matters twice: whatever is left out now cannot later explain growth.

## Pension, gemel and hishtalmut: whose deposits

Section 6 says "all deposits" and does not say whose. A salaried filer's statement shows three
streams, employee, employer and severance, and the instructions do not distinguish them anywhere.
The readings can differ by roughly a factor of two for a long-tenured employee, so do not silently
pick one. Present the streams separately, say that the form does not resolve which are included,
and have the user confirm the treatment with their representative before the figure is fixed. If
employer or severance streams are included, the reconciliation needs a matching line (see
`reconciliation.md`), because employer deposits may not have passed through the filer's reported
income.
