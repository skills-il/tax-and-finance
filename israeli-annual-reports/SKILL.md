---
name: israeli-annual-reports
description: >-
  Navigate and analyze Israeli corporate annual reports (dochot titkuftiim),
  financial filings, and regulatory disclosures. Use when user asks about Israeli
  annual reports, MAYA filings, IFRS financial statements, "doch titkufti",
  "dochot kaspiyim", or Companies Law reporting requirements. Covers TASE filing
  types, Israeli GAAP to IFRS transition, Hebrew financial terminology, and
  key financial statement analysis. Do NOT use for US SEC filings or non-Israeli
  accounting standards.
license: MIT
compatibility: Network access helpful for MAYA portal lookups.
metadata:
  author: skills-il
  version: 1.0.0
  category: tax-and-finance
  tags:
    he:
      - דוחות-כספיים
      - דוח-שנתי
      - מאיה
      - תקינה-חשבונאית
      - רגולציה
      - ישראל
    en:
      - financial-reports
      - annual-report
      - maya
      - accounting-standards
      - regulation
      - israel
  display_name:
    he: דוחות שנתיים ישראליים
    en: Israeli Annual Reports
  display_description:
    he: ניתוח דוחות שנתיים, דיווחים כספיים ודרישות רגולטוריות של חברות ישראליות
    en: >-
      Navigate and analyze Israeli corporate annual reports, financial filings,
      and regulatory disclosures. Use when user asks about Israeli annual
      reports, MAYA filings, IFRS financial statements, or Companies Law
      reporting requirements. Covers TASE filing types, Israeli GAAP to IFRS
      transition, Hebrew financial terminology, and financial statement analysis.
  supported_agents:
    - claude-code
    - cursor
    - github-copilot
    - windsurf
    - opencode
    - codex
---

# Israeli Annual Reports

## Instructions

### Step 1: Understand Israeli Financial Reporting Framework
Israeli public companies follow International Financial Reporting Standards (IFRS):

| Period | Standard | Scope |
|--------|----------|-------|
| Before 2008 | Israeli GAAP (Takenet Cheshbonaut Yisraelit) | All Israeli public companies |
| 2008 onwards | IFRS (full adoption) | All TASE-listed companies |
| Private companies | Israeli GAAP or IFRS (choice) | Non-listed entities |
| Banks | IFRS with BOI adaptations | Supervised by Bank of Israel |
| Insurance | IFRS 17 (from 2023) | Insurance companies |
| NPOs | Israeli NPO accounting standard | Amutot and public benefit companies |

**Key regulatory bodies:**
- Israel Securities Authority (ISA/Rashut Niyarot Erech): Oversees public company reporting
- Israel Accounting Standards Board (Va'adat Takenim Cheshbonaitit): Sets standards for non-IFRS entities
- Institute of Certified Public Accountants (Lishkat Ro'ei Cheshbon): Professional standards

### Step 2: Identify Report Types and Filing Deadlines
| Report Type | Hebrew | Deadline | Content | Where Filed |
|------------|--------|----------|---------|-------------|
| Annual/Periodic Report (Doch Titkufti) | דוח תקופתי | 3 months after fiscal year-end | Full audited financial statements, board report, risk factors, corporate governance | MAYA |
| Quarterly Report (Doch Rivoni) | דוח רבעוני | 2 months after quarter-end (Q1/Q2/Q3) | Reviewed (not audited) interim financials, MD&A | MAYA |
| Immediate Report (Doch Miyadi) | דוח מיידי | Hours after material event | Material events, board decisions, transactions | MAYA |
| Shelf Prospectus (Taskit Madaf) | תשקיף מדף | Valid up to 3 years | Securities offering framework | ISA + MAYA |
| Transaction Report (Doch Iska) | דוח עסקה | Upon related-party transactions | Interested party transactions per Companies Law Sec. 270-275 | MAYA |
| Corporate Governance Report | דוח ממשל תאגידי | Annual, with periodic report | Board composition, audit committee, internal auditor | MAYA |
| Proxy Statement (Hodaat Ziman) | הודעת זימון לאסיפה | 21-35 days before meeting | AGM/EGM agenda, resolutions, voting instructions | MAYA |

### Step 3: Navigate the Annual Report Structure
A standard Israeli annual report (doch titkufti) contains these sections:

| Section | Hebrew | Description |
|---------|--------|-------------|
| Part A: Description of Business | חלק א': תיאור עסקי התאגיד | Operations, markets, competition, regulation, risk factors |
| Part B: Board Report (Doch Direktorion) | חלק ב': דוח הדירקטוריון | MD&A, financial review, going concern assessment |
| Part C: Financial Statements | חלק ג': דוחות כספיים | Balance sheet, P&L, cash flow, equity changes, notes |
| Part D: Additional Information | חלק ד': פרטים נוספים | Officer compensation, holdings, audit committee report |
| Auditor's Report (Doch Roeh Cheshbon) | דוח רואה חשבון | Independent audit opinion |

**Companies Law (Chok HaChevarot, 5759-1999) requirements:**
- Section 171: Annual financial statements obligation
- Section 172: Board must approve financial statements
- Section 173: Auditor appointment by shareholders
- Section 267-269: Audit committee requirements
- Section 270-275: Related party transaction approvals

### Step 4: Key Hebrew Financial Terminology
| English | Hebrew | Transliteration |
|---------|--------|----------------|
| Balance Sheet | מאזן | Maazan |
| Income Statement / P&L | דוח רווח והפסד | Doch Revach VeHefsed |
| Cash Flow Statement | דוח תזרים מזומנים | Doch Tazrim Mezumanim |
| Statement of Changes in Equity | דוח שינויים בהון | Doch Shinuyim BaHon |
| Revenue | הכנסות | Hachnasot |
| Cost of Revenue / COGS | עלות ההכנסות | Alut HaHachnasot |
| Gross Profit | רווח גולמי | Revach Golmi |
| Operating Profit (EBIT) | רווח תפעולי | Revach Tif'uli |
| Net Profit | רווח נקי | Revach Naki |
| Earnings Per Share | רווח למניה | Revach LaMenaya |
| Total Assets | סך נכסים | Sach Nechasim |
| Total Liabilities | סך התחייבויות | Sach Hitkhayvuyot |
| Shareholders' Equity | הון בעלי מניות | Hon Ba'alei Menayot |
| Current Assets | נכסים שוטפים | Nechasim Shotfim |
| Fixed/Non-Current Assets | נכסים קבועים/לא שוטפים | Nechasim Kvuim |
| Goodwill | מוניטין | Monitin |
| Depreciation | פחת | Pachat |
| Amortization | הפחתה | Hafchata |
| Provisions | הפרשות | Hafrashot |
| Dividends | דיבידנדים | Dividendim |
| Retained Earnings | עודפים | Odfim |
| Related Party | צד קשור | Tzad Kashur |
| Material Event | אירוע מהותי | Irua Mehuti |
| Going Concern | עסק חי | Esek Chai |
| Auditor's Opinion | חוות דעת רואה חשבון | Chavat Da'at Roeh Cheshbon |

### Step 5: Financial Statement Analysis Framework
When analyzing Israeli annual reports, focus on:

**Profitability:**
- Gross margin (shiul revach golmi): Revenue - COGS / Revenue
- Operating margin (shiul revach tif'uli): EBIT / Revenue
- Net margin (shiul revach naki): Net income / Revenue
- ROE (tasua al hon): Net income / Shareholders' equity

**Liquidity:**
- Current ratio (yachas shote): Current assets / Current liabilities
- Quick ratio (yachas mahir): (Current assets - Inventory) / Current liabilities
- Cash ratio: Cash / Current liabilities

**Leverage:**
- Debt-to-equity (minuf): Total debt / Equity
- Net debt / EBITDA: Key covenant metric for Israeli bonds
- Interest coverage (yachas kisui ribit): EBIT / Interest expense

**Israeli-specific metrics:**
- CPI-linked debt analysis (chov tzamud madad): Impact of inflation on linked obligations
- Shekel vs foreign currency exposure
- Related party transaction analysis (Section 270 of Companies Law)
- Controlling shareholder structure (pyramidal holdings common in Israel)

### Step 6: Key IFRS Standards Relevant to Israeli Companies
| IFRS | Topic | Israeli Relevance |
|------|-------|-------------------|
| IFRS 15 | Revenue Recognition | Service and tech companies |
| IFRS 16 | Leases | Real estate heavy economy |
| IFRS 9 | Financial Instruments | Banks, insurance |
| IFRS 17 | Insurance Contracts | Adopted 2023 by Israeli insurers |
| IAS 36 | Impairment | Goodwill from Israeli M&A activity |
| IAS 21 | Foreign Currency | Dual-listed companies, exporters |
| IAS 24 | Related Party Disclosures | Pyramidal groups, family businesses |
| IFRS 8 | Operating Segments | Conglomerates (IDB, Delek) |

## Examples

### Example 1: Reading an Annual Report
**Input:** "Help me understand Azrieli Group's annual report"
**Output:** Guide through doch titkufti structure: Part A (real estate portfolio, mall operations), Part B (board analysis of rental income, occupancy), Part C (IFRS financials with investment property at fair value per IAS 40), Part D (officer compensation, related party with Azrieli Foundation). Highlight key metrics: NOI, FFO, occupancy rates, yield on cost.

### Example 2: Hebrew Financial Term Translation
**Input:** "Translate the key terms from this Hebrew balance sheet"
**Output:** Map Hebrew terms to English equivalents with context. For example: "נכסים שוטפים" = Current Assets, "נכסים בלתי מוחשיים" = Intangible Assets, "מוניטין" = Goodwill. Note Israeli-specific items like "מסים נדחים" (Deferred Taxes) and "הפרשה לפיצויי פרישה" (Provision for Severance Pay, per Israeli labor law).

### Example 3: Quarterly Report Analysis
**Input:** "Compare Bank Hapoalim's Q3 results vs Q2"
**Output:** Analyze quarterly report from MAYA: net interest income, credit loss provisions, fee income, operating expenses. Calculate ROE, efficiency ratio, CET1 capital ratio. Note BOI regulatory requirements and housing loan portfolio quality.

### Example 4: Related Party Transaction Review
**Input:** "Explain how to review related party transactions in Israeli filings"
**Output:** Navigate Part D of annual report and Note disclosures (IAS 24). Explain Companies Law Sec. 270-275 approval process: audit committee, board, shareholders for extraordinary transactions. Review controlling shareholder structure and pyramid concerns per Concentration Law (2017).

## Troubleshooting

### Error: "Cannot find English version of the report"
Cause: Only dual-listed companies are required to file in English (for SEC)
Solution: For TASE-only companies, reports are Hebrew only. Use MAYA portal search (maya.tase.co.il), filter by company name and report type. Financial statements follow standard IFRS format, so structure is predictable even in Hebrew.

### Error: "Different accounting standards in older reports"
Cause: Israel adopted IFRS in 2008, older reports use Israeli GAAP
Solution: Pre-2008 reports follow Israeli GAAP which differs from IFRS (e.g., no fair value for investment property, different revenue recognition). When comparing across the transition, look for "First-Time Adoption" reconciliation notes in the 2008 annual report.

### Error: "Report structure differs from expected format"
Cause: Banks and insurance companies have different report formats mandated by BOI and ISA
Solution: Banks follow BOI Reporting to the Public Directives (Horaot Diuach LaTzibur). Insurance companies follow IFRS 17 since 2023. These sectors have unique line items and disclosure requirements.
