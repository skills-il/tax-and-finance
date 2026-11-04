# Israeli Capital Gains Tax on Securities

## Tax Rates

| Investor Type | Rate |
|---------------|------|
| Individual (non-substantial), real gain | 25% (a ceiling: the gain is the top slice of income at the ordinary brackets, capped at 25%) |
| Individual aged 60 or over | Up to 25%: the reduced brackets starting at 10% apply to all taxable income at 60+, so a low-income retiree pays less; an Israeli broker withholds 25% and the excess is reclaimed by filing a return |
| 10% or more shareholder (at the sale or during any of the 12 months before it), real gain | 30% |
| Foreign resident | Per applicable tax treaty and domestic exemptions |
| High-income individual (surtax / mas yesef) | +3% on total taxable income above ILS 721,560, plus (from 2025) +2% on capital-source income that by itself exceeds ILS 721,560 |

The surtax (mas yesef) is a separate instrument on top of the base rate (Section 121B). The threshold is fixed at ILS 721,560 for 2024 to 2027 (not indexed in those years). It has two limbs: 3% on the part of total taxable income above the threshold, and, from 2025, 2% on the part of capital-source income that itself exceeds the threshold. Capital-source income is the year's capital income together (gains net of capital losses offset that year, dividends, interest, taxable rent that is not business income, real-estate betterment; for a residential apartment the betterment counts only when the sale value exceeds ILS 5,385,285), and the base excludes the inflationary amount. If salary alone is above the threshold the whole gain carries the extra 3%; the further 2% applies only to capital-source income above ILS 721,560. The surtax is not part of the semi-annual advance (it is paid with the annual return), and being liable to it is itself a reason to file a return.

## Dividend Tax

Dividends are taxed separately from capital gains:

| Recipient | Rate |
|-----------|------|
| Individual (non-substantial) | 25% |
| Substantial shareholder (10%+) | 30% |

- Withheld at source (nikui mas bemakor) by the paying company or broker.
- Dividends are capital-source income, so both surtax limbs can apply to them (threshold ILS 721,560, fixed for 2024 to 2027).
- A dividend from an Israeli-incorporated company (NICE, Teva, ICL) is taxed under the Israeli rules even when the shares are held through a US listing, and it is generally not US-source income, so there is no US tax to credit.
- For a US-incorporated company, US withholding (file a W-8BEN so the treaty rate applies) is credited against the Israeli 25%/30% dividend tax under the foreign-tax-credit rules (zikui mas zar). For an individual the Israel-US treaty dividend rate is 25%; the 12.5% and 15% treaty rates are for qualifying corporate holders.
- The credit is capped at the Israeli tax on that same foreign income, computed per income source. Foreign tax above the cap is not refunded; Section 205a allows carrying the excess forward, under conditions.

## Tax Withheld at Source (Nikui b'Makor)

- For securities held through an **Israeli broker**, both capital-gains tax and dividend tax are auto-withheld at source. A return may still be required to offset losses held at different brokers, reclaim over-withholding, or when other mandatory-filing rules apply, so "withheld at source" is not always "nothing to file".
- For a **foreign brokerage** (e.g. Interactive Brokers), nothing is withheld locally. The investor must pay a semi-annual capital-gains advance (mikdama) by **31 January** and **31 July** on gains realized in the preceding half-year, and report the gains in the annual income-tax return (its capital-gains appendix). Late advance payment accrues CPI linkage and interest.

## Tax-Advantaged Vehicles

- A **keren hishtalmut, kupat gemel, or pension fund** has its own tax regime; check its current terms instead of applying the 25% direct-account rate.
- Israel has **no annual tax-free capital-gains allowance** (unlike the UK/US); every shekel of net real gain is taxable.

## Key Rules

### Real vs. Inflationary Gain
- The 25% rate applies to the REAL gain: the gain is reduced by the rise in the consumer price index over the holding period, and the inflationary component is exempt
- The inflationary amount is the PART of the gain equal to (adjusted cost minus cost), so it is never negative and never larger than the gain. A capital loss is the nominal excess of cost over consideration: indexation cannot create or enlarge a loss, and a fall in the index cannot create a taxable gain
- For a security held by an individual that is denominated in (or linked to) a foreign currency, the exchange rate of that currency is the index instead of the CPI (Section 88), so shekel depreciation against the purchase currency is exempt, not taxable gain
- Securities bought before 1 January 2003 fall under transition rules, and those rules differ between securities traded on TASE and other assets. Do not assume a flat 25% on the whole gain, and do not assume the pre-2003 portion is taxed at ordinary marginal rates either. Route the computation for a pre-2003 holding to the broker's tax statement or a tax adviser.

### Bonds, Makam and Funds
| Instrument | Rate |
|------------|------|
| Non-CPI-linked shekel bonds and makam | 15%, on the nominal gain (no CPI adjustment) |
| CPI-linked bonds | 25%, on the real gain |
| ETFs (kranot sal) | 25% |
| Mutual funds, exempt fund (the fund pays no tax) | 25% paid by the investor on sale or redemption |
| Mutual funds, taxable fund (the fund pays the tax itself) | 0% at the investor level |

Source: Meitav Trade investor tax guide (see evidence.json `bonds-funds-rates`).

### Loss Offsetting (Kizuz Hefsedim)
- A capital loss offsets all capital gains, including Israeli or foreign securities and property; a loss on a non-Israeli asset first offsets foreign-source gains
- A securities loss can also offset interest and dividend income from securities, where that income was taxed at no more than 25%
- Unused losses carry forward indefinitely, and in later years offset only capital gains, provided a return was filed for the year of the loss (so a net-loss year is a reason to file)
- Report on annual tax return (Doch Shnati)

### Substantial Shareholder
- A seller who held 10% or more at the date of sale or during any of the 12 months before it; detailed definitional rules apply
- The 30% rate applies to the real gain on the sale

### Foreign Residents
- Non-residents are exempt from Israeli tax on capital gains from selling shares of an Israeli company traded on the Israeli stock exchange or a foreign stock exchange, subject to conditions
- Otherwise check the applicable double taxation treaty

## Reporting
- Gains/losses reported in the capital-gains appendix of the annual return
- Brokerage firms withhold tax at source (nikui mas bemakor)
- Self-reporting required for foreign brokerages
- Filing deadline: check the Israel Tax Authority's current deadline and extensions for the year

## Common Exemptions
- Shares in qualifying high-tech companies under Israel's angel-investor legislation, which has benefit tracks for private investors in technological companies. Check the current tracks and conditions before relying on them.
- Shares received through employee stock options under the Income Tax Ordinance's employee-equity track -- special rules apply; verify the governing section and route with a tax adviser
- Government and corporate bonds: non-CPI-linked shekel bonds and makam are taxed at 15% on the nominal gain (see "Bonds, Makam and Funds" above)

## Inherited Securities
- Inheritance is excluded from the definition of a "sale", so passing shares to an heir is not a tax event.
- There is no step-up to market value: when the deceased died after 31 March 1981, the heir takes the acquisition date (and original cost) that would have applied had the deceased sold the asset (Section 88).
