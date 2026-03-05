---
name: israeli-annual-reports
description: >-
  Navigate and analyze Israeli corporate annual reports (dochot titkuftiim),
  financial filings, and regulatory disclosures. Use when user asks about
  Israeli annual reports, MAYA filings, IFRS financial statements, doch
  titkufti, dochot kaspiyim, or Companies Law reporting requirements. Covers
  TASE filing types, Israeli GAAP to IFRS transition, Hebrew financial
  terminology, and key financial statement analysis.
license: MIT
compatibility: >-
  Works with Claude Code, Cursor, GitHub Copilot, Windsurf, OpenCode, Codex.
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
    he: "דוחות שנתיים ישראליים"
    en: "Israeli Annual Reports"
  display_description:
    he: >-
      ניתוח דוחות שנתיים, דיווחים כספיים ודרישות רגולטוריות של חברות ישראליות.
      שימוש כשצריך לקרוא דוח תקופתי, להבין מונחים פיננסיים בעברית, לנתח
      דיווחי מאיה, או להבין את דרישות חוק החברות.
    en: >-
      Navigate and analyze Israeli corporate annual reports, financial filings,
      and regulatory disclosures
  supported_agents:
    - claude-code
    - cursor
    - github-copilot
    - windsurf
    - opencode
    - codex
    - antigravity
---

# Israeli Annual Reports

## Reporting Framework
Israeli public companies adopted IFRS in 2008. Prior reports use Israeli GAAP. Banks follow BOI adaptations, insurance companies follow IFRS 17 since 2023.

## Report Types and Deadlines
| Report | Deadline | Content |
|--------|----------|--------|
| Annual (Doch Titkufti) | 3 months after year-end | Audited financials, board report |
| Quarterly (Doch Rivoni) | 2 months after quarter | Reviewed interim financials |
| Immediate (Doch Miyadi) | Hours after event | Material events |
| Shelf Prospectus | Valid up to 3 years | Securities offering framework |

## Annual Report Structure
- Part A: Description of Business (operations, markets, risks)
- Part B: Board Report (MD&A, financial review)
- Part C: Financial Statements (balance sheet, P&L, cash flow)
- Part D: Additional Information (officer compensation, audit committee)

## Key Hebrew Financial Terms
- Maazan = Balance Sheet
- Doch Revach VeHefsed = Income Statement
- Hachnasot = Revenue
- Revach Naki = Net Profit
- Nechasim Shotfim = Current Assets
- Monitin = Goodwill
- Odfim = Retained Earnings
- Tzad Kashur = Related Party

## Companies Law Requirements
- Sec. 171: Annual financial statements obligation
- Sec. 172: Board approval required
- Sec. 267-269: Audit committee requirements
- Sec. 270-275: Related party transaction approvals

## Examples

### Example 1: Analyze a TASE-Listed Company's Annual Report
User says: "Help me understand Teva's latest annual report from MAYA"
Actions:
1. Identify report type: Annual Report (Doch Shnati) filed on MAYA system
2. Locate key sections: Balance Sheet (Maazanit), Income Statement (Doch Revach VeHefsed), Cash Flow
3. Extract key metrics: revenue, operating profit, net profit in NIS
4. Compare with previous year and sector benchmarks
5. Note auditor opinion and any qualifications
Result: Structured analysis of annual report with key financial highlights in context

### Example 2: Compare Israeli Bank Financial Statements
User says: "Compare Leumi and Hapoalim annual reports"
Actions:
1. Pull latest annual reports from MAYA (maya.tase.co.il)
2. Extract comparable metrics: total assets, net income, ROE, capital adequacy
3. Normalize data to NIS millions for comparison
4. Note regulatory differences in reporting (Bank of Israel requirements)
5. Create comparison table with key ratios
Result: Side-by-side comparison of two Israeli banks' financial performance

## Bundled Resources

### Scripts
- `scripts/financial_parser.py` -- Hebrew-English financial term glossary with search functionality covering balance sheets, income statements, and MAYA filings. Run: `python scripts/financial_parser.py --help`

### References
- `references/hebrew-financial-terms.md` -- Complete Hebrew-English financial terminology reference with tables for financial statements, income statement items, MAYA filing types, and Israeli accounting standards (IFRS-IL). Consult when translating financial terms or navigating Hebrew financial documents.

## Troubleshooting

### Error: "Cannot find report on MAYA system"
Cause: Company may file under a different Hebrew name or subsidiary
Solution: Search MAYA by securities number (mispar niyar) rather than company name. Hebrew company names may differ from the English trading name.

### Error: "Financial terms not matching standard translations"
Cause: Israeli companies sometimes use non-standard Hebrew financial terminology
Solution: Consult `references/hebrew-financial-terms.md` for standard terms. Some companies use colloquial Hebrew instead of formal accounting terms (e.g., "רווחים" instead of "רווח נקי").
