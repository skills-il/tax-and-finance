# Domain Checklist: israeli-crypto-tax-reporter

Scope: Israeli cryptocurrency capital-gains tax calculation and reporting.
Category: tax-and-finance.
Audience: Israeli-resident individual crypto investors (and the borderline business-classification case).

## Must cover (core)

- **Crypto = "asset" (neches), not currency.** Capital-gains regime under Chapter E, anchored in Section 88 of the Income Tax Ordinance and ITA Circular 05/2018.
- **25% individual capital-gains rate on the real gain, Section 91(b)(1).** The 30% rate in 91(b)(2) is for a **security in a body corporate** held by a material shareholder and must NOT be defaulted onto a fungible token. The "post-1.1.2012" qualifier belongs to Section 91(b1), which splits the gain for assets acquired before מועד השינוי and is out of scope for crypto. Section 91(c) taxes the **chargeable** inflationary amount at 10%, which is nil for any crypto lot because Section 88 confines it to gain that would have arisen by 31.12.1993.
- **FIFO cost basis as the customary Israeli default.** NOT prescribed by Circular 05/2018, which sets no cost-basis method; other methods are usable if consistently applied and documented.
- **Crypto-to-crypto swap is a taxable disposal.** Each swap = disposal of leg A + acquisition of leg B, both valued in NIS at swap time.
- **Stablecoin disposals are taxable.** USDT/USDC/DAI are "asset" under Section 88, not foreign currency.
- **NIS conversion.** Circular 05/2018 does NOT require the Bank of Israel representative rate; section 3.1.5.1 sets the value at **fair value in shekels**, overridden by the **stated price (מחיר נקוב)** of the asset or goods bought where one exists, and requires the SAME figure to serve as the seller's proceeds and the buyer's original cost. The representative rate is a defensible documented choice, not a legal requirement. Earlier versions of this file asserted the circular required it; it does not, and the word יציג does not appear in it.
- **Inflation indexation split, Sections 88 and 91(c).** The gain splits into a real gain, taxed under 91(b), and an inflationary amount. **91(c) taxes the CHARGEABLE inflationary amount at 10%, not 0%**; the practical result for crypto is nil only because Section 88 confines the chargeable part to gain that would have arisen by 31.12.1993. Do NOT cite 91(b)(3) for this: that subsection is the 15% (20% for a material shareholder) rate on non-index-linked bonds, commercial paper and loans, and has nothing to do with the split. The calculator flags long-held lots but does not compute it; Form 1326א is the ITA helper.
- **Loss offset and carryforward, Section 92.** Same-year offset and carryforward; spousal offset on joint filing.
- **Cost-basis special cases: gift/inheritance carryover (Section 97(a)(5)); hard-fork zero basis; airdrop/staking basis = FMV at receipt.**
- **DeFi/income-vs-capital classification.** Staking, liquidity-mining/farming, airdrops, mining, lending interest, income at receipt (Section 2(1)/2(4)) vs capital on later sale. The 25% figure in the calculator is a passive-income floor; ordinary/business receipts are taxed at marginal rates up to 47%.
- **Business vs investment determination (badge of trade).** Circular 05/2018 section 3.1.4 does NOT enumerate a test; it delegates to "מבחני עסק כפי שנקבעו **בפסיקה**". Cite the factors as case law. Business classification moves gains to ordinary income (marginal up to 47% plus surtax) and triggers Bituach Leumi and Mas Briut.
- **Mining is business income categorically**, per Circular 05/2018 section 3.1.4, with no scale test.
- **The VAT consequence has three regimes, not one.** Section 3.2.3.2.3 registers a business-level trader as a **מוסד כספי** under Section 4 of the VAT Law; 3.2.3.2.4 registers the **miner** as an **עוסק**; 3.2.3.1 leaves a non-business investor outside VAT. Never state "18% VAT plus osek registration" as the business rule.
- **Surtax (mas yesafim), post-2025 structure.** 3% base on total taxable income above NIS 721,560 PLUS 2% additional on capital-source income above the same threshold (effective 5% on crypto gains in the band), threshold frozen through TY2027. The base is TOTAL income (salary + gains), not crypto alone, so the calculator takes --other-income.
- **Advance payment (mikdama), Form 1399י, within 30 days of disposal.** Codes 77 (sale) / 71 (virtual currency); Form 1399ח for companies.
- **Annual return mechanics.** Form 1301 plus the appendices the ITA requires. The 1399י notice within 30 days is the Section 91(d)(1) obligation for an **asset** sale. 1322, 1325 and 1326 are all titled as **ניירות ערך** forms and 1322 is scoped to securities **הנסחרים בבורסה**, so do not assert that crypto belongs on them; the "Nispach Gimel" labels are not the ITA's (נספח א belongs to 1320). Form 1344 carries losses brought forward. The salaried-filer exemption is still a **draft** under Section 134A, with a digital-asset ceiling in תוספת ו rather than the general Section 131 ceilings.
- **Record retention.** Circular 05/2018 section 3.1.3 fixes NO period; it requires documents "ככול שיידרש להנחת דעתו של פקיד השומה". The 7-year figure comes from the bookkeeping directives. Do not attribute it to the circular.

## Should cover (advanced)

- **Exit tax / deemed sale on ceasing Israeli residency, Section 100A.** Must state that **deferral is a deeming rule, not an election** (100A(b) deems a non-payer to have requested it), that the chargeable portion is the **real** gain **measured at realization** apportioned by elapsed time (100A(d)), and that **no interest or linkage accrues during the deferral**, only from realization. The calculator does not model it; relocation scenarios go to a CPA and the aliyah skills.
- **Form 909 bank-refusal payment pathway (Hora'at Sha'a, ITA Instruction 06/2024).** Individual-only NIS payment direct to the ITA's BOI account when a bank refuses crypto-derived funds.
- **Voluntary Disclosure Procedure.** Declared 25 Aug 2025, ran to **31 Aug 2026**. The skill must instruct a date check before advising anyone to use it, because self-reporting into a closed procedure hands over an admission with no immunity. Green Track digital-asset limb: income from digital assets **not exceeding NIS 500,000 for the ENTIRE disclosure period** (not per year) and fair value of all digital assets at 31.12.2024 not exceeding NIS 1,500,000; the ITA chooses the track.
- **CARF / automatic exchange.** Israeli RCASP collection from 2026, first exchange **2028**: the OECD Global Forum commitments list places Israel in the "first exchanges by 2028" group, not the 2027 one. Re-verify against the current list.
- **Foreign-tax credit and treaty relief, Sections 199-210 (50+ treaties).** Currently flagged under "when to get professional help"; FTC mechanics are under-specified by design.
- **Mining / NFT-creator business treatment and deductible costs** (electricity, depreciation), Circular 05/2018; Section 17 deductions.
- **The surtax is not part of the 30-day advance.** Section 121B(b) disapplies Section 91(d) for surtax-chargeable income, and Section 121B(e) excludes the inflationary amount from the surtax base.
- **Section 92 loss mechanics.** Indefinite carry-forward against future capital gains, and within a year each shekel of remaining loss offsets **3.5 shekels** of chargeable inflationary amount. The calculator performs neither offset nor carry-forward.
- **AML provider-side reporting (NIS 50k/6-month casual-customer ceiling)**, distinct from the taxpayer's own duty.

## Out of scope (explicit)

- Non-Israeli jurisdictions' domestic rules (US 8949, EU, etc.) beyond foreign-tax-credit interaction.
- General (non-crypto) income tax computation and payroll.
- Full VAT return preparation for crypto businesses (warn + refer, do not compute).
- Corporate-structure / company crypto holdings beyond the 23% rate and Form 1399ח.
- Legal adjudication of whether a specific pattern is a "business" (recommend pre-ruling / CPA; the skill applies the test, it does not decide).
- Securities-law / token-offering regulatory compliance (ISA), as distinct from tax.

## Authoritative sources

- Income Tax Ordinance [New Version] 5721-1961, Sections 2(1), 2(4), 14(a), 88, 91(b)(1), 91(b)(2), 91(c), 91(d), 92, 97(a)(5), 97(b)(1), 100A, 121B, 131, 134A, 159A, 199-210.
- ITA Circular 05/2018 (virtual-currency classification and business factors; it does NOT cover FIFO, conversion or tax rates); Circular 07/2018 (token issuance).
- 2025 Budget Law (surtax restructuring) + Dec-2024 indexation-pause amendment (threshold freeze through TY2027).
- ITA Instruction (Hora'at Sha'a) 06/2024 (Form 909 bank-refusal procedure).
- ITA Voluntary Disclosure Procedure, declared 25 Aug 2025, deadline 31 Aug 2026.
- Forms 1301, 1320, 1322, 1325, 1326, 1326א, 1344, 1399י, 1399ח, 909, with the ITA's own published titles (see references/crypto-tax-regulations.md).
- Bank of Israel representative rates; Bituach Leumi self-employed rate schedule (btl.gov.il).
- OECD Crypto-Asset Reporting Framework (CARF), collection 2026, first exchange 2028 (per the Global Forum commitments list).
