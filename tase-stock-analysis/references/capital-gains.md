# Israeli Capital Gains Tax on Securities

## Tax Rates

| Investor Type | Rate |
|---------------|------|
| Individual (non-substantial), real gain | 25% |
| 10% or more shareholder (at the sale or during any of the 12 months before it), real gain | 30% |
| Foreign resident | Per applicable tax treaty and domestic exemptions |
| High-income individual (surtax / mas yesef) | Up to +5% on the slice above the threshold, ILS 721,560 in 2026 (3% on all-source income + a further 2% on capital-source income) |

The surtax (mas yesef) is a separate instrument that applies on top of the base rate above an annually indexed threshold (ILS 721,560 in 2026), so on the slice above the threshold the marginal rate is the base rate plus 5% (about 30% for a 25% payer, higher for a substantial shareholder).

## Dividend Tax

Dividends are taxed separately from capital gains:

| Recipient | Rate |
|-----------|------|
| Individual (non-substantial) | 25% |
| Substantial shareholder (10%+) | 30% |

- Withheld at source (nikui mas bemakor) by the paying company or broker.
- The surtax (mas yesef) also applies to dividend income above the annual threshold (ILS 721,560 in 2026, indexed annually).
- For dividends from a dual-listed share paid in the US, US withholding (file a W-8BEN so the treaty rate applies) is credited against the Israeli 25%/30% dividend tax under the foreign-tax-credit rules (zikui mas zar).
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
- Unused losses carry forward indefinitely, and in later years offset only capital gains
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
