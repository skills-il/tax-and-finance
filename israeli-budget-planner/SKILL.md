---
name: israeli-budget-planner
description: >-
  Plan household and personal budgets with Israeli-specific costs, rates, and
  financial products. Use when user asks about budgeting in Israel, mortgage
  (mashkanta) calculations, arnona rates, cost of living, takciv, or monthly
  expense planning. Covers Bank of Israel prime rate, mashkanta tracks, arnona
  by city, Sal Briut costs, and Israeli household benchmarks.
license: MIT
compatibility: >-
  Works with Claude Code, Cursor, GitHub Copilot, Windsurf, OpenCode, Codex.
metadata:
  author: skills-il
  version: 1.0.0
  category: tax-and-finance
  tags:
    he:
      - תקציב
      - משכנתא
      - ארנונה
      - יוקר-המחיה
      - חיסכון
      - ישראל
    en:
      - budget
      - mortgage
      - arnona
      - cost-of-living
      - savings
      - israel
  display_name:
    he: "מתכנן תקציב ישראלי"
    en: "Israeli Budget Planner"
  display_description:
    he: >-
      תכנון תקציב משק בית עם עלויות, שיעורים ומוצרים פיננסיים ישראליים.
      שימוש כשצריך חישובי משכנתא, שיעורי ארנונה, תכנון הוצאות חודשיות,
      או מידע על יוקר המחיה בישראל.
    en: >-
      Plan household and personal budgets with Israeli-specific costs, rates,
      and financial products
  supported_agents:
    - claude-code
    - cursor
    - github-copilot
    - windsurf
    - opencode
    - codex
---

# Israeli Budget Planner

## Key Financial Rates
| Rate | Value (Reference) |
|------|-------------------|
| BOI Interest Rate | 4.50% (check boi.org.il) |
| Prime Rate | BOI + 1.50% = ~6.00% |
| VAT (Ma'am) | 17% |
| Minimum Wage | 5,880.02 NIS/month |
| Average Wage | ~12,500 NIS/month |

## Mashkanta (Mortgage) Tracks
| Track | Rate Type | Range |
|-------|-----------|-------|
| Prime-linked | Variable | Prime +/- 0.5% |
| Fixed unlinked | Fixed | 4.5%-6.5% |
| CPI-linked fixed | Fixed + CPI | 3.0%-5.0% + CPI |
| CPI-linked variable | Resets every 5 yrs | 2.5%-4.5% + CPI |

BOI rules: Max LTV 75% first home, max 33.33% variable rate, max 33.33% CPI-linked.

## Arnona by City (NIS/sqm/month, approx.)
- Tel Aviv: 85-130
- Jerusalem: 55-80
- Haifa: 45-65
- Beer Sheva: 35-50
- Raanana: 70-95
- Herzliya: 75-100

## Monthly Budget Template (Couple + 1 Child)
- Housing: 4,000-8,000 (25-35%)
- Food: 2,500-4,500 (15-25%)
- Education: 1,500-3,500 (8-15%)
- Transportation: 500-1,500 (3-8%)
- Arnona: 400-800 (3-5%)

## Savings Vehicles
- Keren Pensia: Tax-deductible, locked until retirement
- Keren Hishtalmut: Tax-free after 6 years
- Kupat Gemel: Capital gains exempt, 6-year lock
