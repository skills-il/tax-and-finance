# Domain Checklist: israeli-crypto-tax-reporter

Scope: Israeli cryptocurrency capital-gains tax calculation and reporting.
Category: tax-and-finance.
Audience: Israeli-resident individual crypto investors (and the borderline business-classification case).

## Must cover (core)

- **Crypto = "asset" (neches), not currency.** Capital-gains regime under Chapter E, anchored in Section 88 of the Income Tax Ordinance and ITA Circular 05/2018.
- **25% individual capital-gains rate; 30% for a significant shareholder (10%+).** Section 91(b)(1) (25% for assets acquired post-1.1.2012).
- **FIFO cost basis as the Israeli default.** Per Circular 05/2018 (other methods only if consistently applied and documented).
- **Crypto-to-crypto swap is a taxable disposal.** Each swap = disposal of leg A + acquisition of leg B, both valued in NIS at swap time.
- **Stablecoin disposals are taxable.** USDT/USDC/DAI are "asset" under Section 88, not foreign currency.
- **NIS conversion using Bank of Israel representative rate (sha'ar yatzig).** Required by Circular 05/2018.
- **Inflation indexation split, Section 91(b)(3).** Real gain (25%) vs inflation component (0% for individuals on assets acquired after 1.1.1994). The calculator flags long-held lots but does not compute the split.
- **Loss offset and carryforward, Section 92.** Same-year offset and carryforward; spousal offset on joint filing.
- **Cost-basis special cases: gift/inheritance carryover (Section 97(a)(5)); hard-fork zero basis; airdrop/staking basis = FMV at receipt.**
- **DeFi/income-vs-capital classification.** Staking, liquidity-mining/farming, airdrops, mining, lending interest, income at receipt (Section 2(1)/2(4)) vs capital on later sale. The 25% figure in the calculator is a passive-income floor; ordinary/business receipts are taxed at marginal rates up to 47%.
- **Business vs investment determination (badge of trade).** Circular 05/2018 multi-factor test; business classification moves gains to Section 2(1) ordinary income (marginal up to 47% + surtax) and triggers Bituach Leumi + Mas Briut + VAT.
- **Surtax (mas yesafim), post-2025 structure.** 3% base on total taxable income above NIS 721,560 PLUS 2% additional on capital-source income above the same threshold (effective 5% on crypto gains in the band), threshold frozen through TY2027. The base is TOTAL income (salary + gains), not crypto alone, so the calculator takes --other-income.
- **Advance payment (mikdama), Form 1399י, within 30 days of disposal.** Codes 77 (sale) / 71 (virtual currency); Form 1399ח for companies.
- **Annual return mechanics, Form 1322 (Nispach Gimel) + Form 1325 (Nispach Gimel(1)), filed with Form 1301.** Section 131 filing duty, including the TY2025 salaried-filer draft exemption and current-year deadlines.
- **Record retention 7 years.**

## Should cover (advanced)

- **Exit tax / deemed sale on ceasing Israeli residency, Section 100A.** Covered as a Gotcha; the calculator does not model it, and relocation scenarios are routed to a CPA / the aliyah-relocation skills.
- **Form 909 bank-refusal payment pathway (Hora'at Sha'a, ITA Instruction 06/2024).** Individual-only NIS payment direct to the ITA's BOI account when a bank refuses crypto-derived funds.
- **Voluntary Disclosure Procedure 2025-2026 (crypto track).** Green vs Regular track, deadline 31 Aug 2026, criminal immunity.
- **CARF / automatic exchange.** Israeli RCASP collection from 2026, first exchange expected 2027-2028 (verify the year against the latest OECD monitoring update).
- **Foreign-tax credit and treaty relief, Sections 199-210 (50+ treaties).** Currently flagged under "when to get professional help"; FTC mechanics are under-specified by design.
- **Mining / NFT-creator business treatment and deductible costs** (electricity, depreciation), Circular 05/2018; Section 17 deductions.
- **Business-VAT pointer (18%) + osek registration** for miners/dealers.
- **AML provider-side reporting (NIS 50k/6-month casual-customer ceiling)**, distinct from the taxpayer's own duty.

## Out of scope (explicit)

- Non-Israeli jurisdictions' domestic rules (US 8949, EU, etc.) beyond foreign-tax-credit interaction.
- General (non-crypto) income tax computation and payroll.
- Full VAT return preparation for crypto businesses (warn + refer, do not compute).
- Corporate-structure / company crypto holdings beyond the 23% rate and Form 1399ח.
- Legal adjudication of whether a specific pattern is a "business" (recommend pre-ruling / CPA; the skill applies the test, it does not decide).
- Securities-law / token-offering regulatory compliance (ISA), as distinct from tax.

## Authoritative sources

- Income Tax Ordinance [New Version] 5721-1961, Sections 2(1), 2(4), 88, 91, 91(b)(1), 91(b)(3), 92, 97(a)(5), 100A, 121B, 131, 159A, 199-210.
- ITA Circular 05/2018 (virtual-currency classification, FIFO, conversion, business factors); Circular 07/2018 (token issuance).
- 2025 Budget Law (surtax restructuring) + Dec-2024 indexation-pause amendment (threshold freeze through TY2027).
- ITA Instruction (Hora'at Sha'a) 06/2024 (Form 909 bank-refusal procedure).
- ITA Voluntary Disclosure Procedure 2025-2026 (crypto track), deadline 31 Aug 2026.
- Forms 1301, 1322, 1325, 1399י, 1399ח, 909.
- Bank of Israel representative rates; Bituach Leumi self-employed rate schedule (btl.gov.il).
- OECD Crypto-Asset Reporting Framework (CARF), collection 2026, first exchange 2027-2028.
