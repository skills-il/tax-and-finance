---
name: tase-stock-analyzer
description: >-
  Analyze Tel Aviv Stock Exchange (TASE) securities, indices, and corporate
  disclosures. Use when user asks about Israeli stocks, TASE indices (TA-35,
  TA-125, TA-90), MAYA filings, dual-listed companies, or "menayot" analysis.
  Covers index composition, sector breakdown, MAYA disclosure types, ISA
  regulations, and Bizportal/Globes Finance data sources. Do NOT use for
  cryptocurrency, forex trading strategies, or non-Israeli exchanges.
license: MIT
compatibility: Network access recommended for live TASE/MAYA data lookups.
metadata:
  author: skills-il
  version: 1.0.0
  category: tax-and-finance
  tags:
    he:
      - בורסה
      - מניות
      - מדדים
      - מאיה
      - ניירות-ערך
      - ישראל
    en:
      - stock-exchange
      - stocks
      - indices
      - maya
      - securities
      - israel
  display_name:
    he: מנתח מניות הבורסה
    en: TASE Stock Analyzer
  display_description:
    he: ניתוח מניות, מדדים ודיווחים בבורסה לניירות ערך בתל אביב
    en: >-
      Analyze Tel Aviv Stock Exchange (TASE) securities, indices, and corporate
      disclosures. Use when user asks about Israeli stocks, TASE indices (TA-35,
      TA-125, TA-90), MAYA filings, dual-listed companies, or "menayot"
      analysis. Covers index composition, sector breakdown, MAYA disclosure
      types, ISA regulations, and Bizportal/Globes Finance data sources.
  supported_agents:
    - claude-code
    - cursor
    - github-copilot
    - windsurf
    - opencode
    - codex
---

# TASE Stock Analyzer

## Instructions

### Step 1: Identify the TASE Index or Security
The Tel Aviv Stock Exchange operates several key indices:

| Index | Hebrew | Companies | Description |
|-------|--------|-----------|-------------|
| TA-35 | ת"א-35 | 35 | Largest market-cap stocks, blue-chip benchmark |
| TA-125 | ת"א-125 | 125 | Broad market index, includes TA-35 |
| TA-90 | ת"א-90 | 90 | Mid-cap stocks (TA-125 minus TA-35) |
| TA-SME60 | ת"א-צמיחה | 60 | Small/growth companies |
| TA-Banks5 | ת"א-בנקים5 | 5 | Bank stocks (Hapoalim, Leumi, Discount, Mizrahi-Tefahot, First International) |
| TA-Real Estate | ת"א-נדל"ן | ~15 | Real estate sector |
| TA-Tech | ת"א-טכנולוגיה | ~50 | Technology companies |
| TA-Bond indices | ת"א-אג"ח | varies | Government and corporate bond indices |

**TASE trading hours:** Sunday-Thursday, 09:59 (pre-open) to 17:25 (closing auction). No trading Friday-Saturday (Shabbat).

### Step 2: Understand MAYA Disclosure System
MAYA (מאיה) is the electronic disclosure system operated by TASE and the Israel Securities Authority (ISA/רשות ניירות ערך). All public companies must file through MAYA.

| Filing Type | Hebrew | Timing | Content |
|------------|--------|--------|---------|
| Immediate Report (Doch Miyadi) | דוח מיידי | Within hours of material event | Mergers, board changes, material contracts, litigation |
| Quarterly Report (Doch Rivoni) | דוח רבעוני | Within 2 months of quarter-end | Financial statements, MD&A |
| Periodic/Annual Report (Doch Titkufti) | דוח תקופתי | Within 3 months of year-end | Full annual report, audited financials |
| Shelf Prospectus (Taskit Madaf) | תשקיף מדף | As needed | Pre-approved offering document |
| Transaction Report (Doch Iska) | דוח עסקה | Upon related-party transactions | Details of interested-party deals |
| Proxy Statement (Hodaat Ziman) | הודעת זימון | Before shareholder meetings | Agenda, voting matters |

**MAYA portal:** https://maya.tase.co.il - All filings are public and searchable.

### Step 3: Analyze Dual-Listed Companies
Many Israeli companies trade on both TASE and US exchanges (NYSE/NASDAQ). Key considerations:

| Company | TASE Symbol | US Symbol | US Exchange |
|---------|------------|-----------|-------------|
| Check Point | CHKP | CHKP | NASDAQ |
| Nice Systems | NICE | NICE | NASDAQ |
| Teva Pharmaceutical | TEVA | TEVA | NYSE |
| Bank Leumi | LUMI | LUMI | OTC |
| ICL Group | ICL | ICL | NYSE |
| Tower Semiconductor | TSEM | TSEM | NASDAQ |
| Elbit Systems | ESLT | ESLT | NASDAQ |
| CyberArk | CYBR | CYBR | NASDAQ |

**Dual-listing considerations:**
- Price arbitrage between TASE (NIS) and US (USD) factoring exchange rates
- Different trading hours (TASE closes before US opens)
- Filing obligations in both jurisdictions (ISA + SEC)
- Currency exposure effects on valuations

### Step 4: Sector Analysis Framework
Analyze TASE stocks by sector composition:

| Sector | Key Players | Weight in TA-35 (approx.) |
|--------|------------|---------------------------|
| Banking & Finance | Hapoalim, Leumi, Discount, Mizrahi-Tefahot | ~25% |
| Technology | Check Point, Nice, CyberArk, Monday.com | ~20% |
| Pharmaceuticals | Teva, Perrigo | ~8% |
| Real Estate | Azrieli, Amot, Melisron | ~12% |
| Energy & Chemicals | ICL, Delek, Bazan | ~10% |
| Insurance | Harel, Migdal, Clal Insurance | ~8% |
| Telecom | Bezeq, Cellcom, Partner | ~5% |

### Step 5: Key ISA Regulations
The Israel Securities Authority (Rashut Niyarot Erech) enforces:

- **Securities Law, 1968 (Chok Niyarot Erech):** Core securities regulation
- **Joint Investments Trust Law:** Governs mutual funds (kranot neemanut)
- **Regulation of Investment Advice Law:** Licensing of investment advisors (yoetz hashkaot) and portfolio managers (menahel tikei hashkaot)
- **Insider trading prohibition:** Section 52 of Securities Law, applies to anyone with material non-public information
- **Reporting requirements:** Chapter D of Securities Law, detailed in ISA regulations
- **Tender offers:** Mandatory tender offer at 25% and 45% ownership thresholds

### Step 6: Data Sources for Research
| Source | URL | Data Available |
|--------|-----|----------------|
| TASE Website | tase.co.il | Live quotes, index composition, historical data |
| MAYA System | maya.tase.co.il | All corporate filings and disclosures |
| ISA (Rashut) | isa.gov.il | Regulatory decisions, enforcement actions |
| Bizportal | bizportal.co.il | Financial analysis, consensus estimates |
| Globes Finance | globes.co.il/portal/instrument | News, analysis, market data |
| Bank of Israel | boi.org.il | Exchange rates, monetary policy |
| CBS (Lishkat Statistika) | cbs.gov.il | Economic indicators |

## Examples

### Example 1: Index Analysis
**Input:** "Analyze the TA-35 composition and sector weights"
**Output:** Provide current TA-35 sector breakdown, top holdings by weight, recent index changes, comparison to TA-125 for broader market view. Note banking sector's dominant weight and tech sector growth.

### Example 2: MAYA Filing Lookup
**Input:** "Check recent MAYA filings for Teva"
**Output:** Guide user to maya.tase.co.il, explain how to search by company name or security number, describe filing types (immediate reports, quarterly). Summarize common Teva filing patterns (FDA updates, litigation, quarterly results).

### Example 3: Dual-Listed Comparison
**Input:** "Compare Check Point's price on TASE vs NASDAQ"
**Output:** Explain price comparison methodology: convert NIS price to USD using BOI rate, account for different trading hours, note that TASE price often gaps to match US close. Calculate implied premium/discount.

### Example 4: Sector Deep Dive
**Input:** "Overview of Israeli banking stocks"
**Output:** Analyze all 5 TA-Banks5 components: Bank Hapoalim (POLI), Bank Leumi (LUMI), Israel Discount Bank (DSCT), Mizrahi-Tefahot (MZTF), First International Bank (FIBI). Compare by market cap, ROE, dividend yield, NPL ratios. Note BOI regulatory requirements (Basel III, capital adequacy).

## Troubleshooting

### Error: "Cannot find current stock price"
Cause: TASE data requires market hours (Sun-Thu 10:00-17:25) or subscription
Solution: Use TASE website for delayed quotes (15-min delay free), or Bizportal/Globes for real-time. Note TASE is closed Friday-Saturday and Israeli holidays.

### Error: "MAYA filing is in Hebrew only"
Cause: Most MAYA filings are in Hebrew, dual-listed companies may file English versions
Solution: For dual-listed companies, check SEC EDGAR for English filings. For TASE-only companies, use translation tools on the MAYA PDF. Key financial terms are often in English within Hebrew reports.

### Error: "Index composition appears outdated"
Cause: TASE rebalances indices semi-annually (June and December)
Solution: Check the latest index committee decisions on tase.co.il. Composition changes take effect on the third Sunday after announcement.
