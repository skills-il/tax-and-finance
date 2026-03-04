---
name: tase-stock-analyzer
description: >-
  Analyze Tel Aviv Stock Exchange (TASE) securities, indices, and corporate
  disclosures. Use when user asks about Israeli stocks, TASE indices (TA-35,
  TA-125, TA-90), MAYA filings, dual-listed companies, or menayot analysis.
  Covers index composition, sector breakdown, MAYA disclosure types, ISA
  regulations, and Bizportal/Globes Finance data sources.
license: MIT
compatibility: >-
  Works with Claude Code, Cursor, GitHub Copilot, Windsurf, OpenCode, Codex.
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
    he: "מנתח מניות הבורסה"
    en: "TASE Stock Analyzer"
  display_description:
    he: >-
      ניתוח מניות, מדדים ודיווחים בבורסה לניירות ערך בתל אביב. שימוש כשצריך
      מידע על מדדי ת"א-35, ת"א-125, ת"א-90, דיווחי מאיה, חברות רישום כפול,
      או ניתוח סקטורי של הבורסה.
    en: >-
      Analyze Tel Aviv Stock Exchange securities, indices, and corporate
      disclosures
  supported_agents:
    - claude-code
    - cursor
    - github-copilot
    - windsurf
    - opencode
    - codex
---

# TASE Stock Analyzer

## Key TASE Indices
| Index | Companies | Description |
|-------|-----------|-------------|
| TA-35 | 35 | Largest market-cap stocks, blue-chip benchmark |
| TA-125 | 125 | Broad market index, includes TA-35 |
| TA-90 | 90 | Mid-cap stocks (TA-125 minus TA-35) |
| TA-SME60 | 60 | Small/growth companies |
| TA-Banks5 | 5 | Bank stocks |

## MAYA Disclosure System
MAYA (maya.tase.co.il) is the electronic disclosure system for all public companies. Filing types: Immediate Report (Doch Miyadi), Quarterly Report (Doch Rivoni), Periodic/Annual Report (Doch Titkufti), Shelf Prospectus (Taskit Madaf).

## Dual-Listed Companies
Key Israeli companies trading on both TASE and US exchanges: Check Point (CHKP/NASDAQ), Nice Systems (NICE/NASDAQ), Teva (TEVA/NYSE), ICL (ICL/NYSE), Elbit (ESLT/NASDAQ), CyberArk (CYBR/NASDAQ), Tower Semiconductor (TSEM/NASDAQ).

## Sector Breakdown (TA-35 approx.)
- Banking and Finance: ~25% (Hapoalim, Leumi, Discount, Mizrahi-Tefahot)
- Technology: ~20% (Check Point, Nice, CyberArk)
- Real Estate: ~12% (Azrieli, Amot, Melisron)
- Energy and Chemicals: ~10% (ICL, Delek, Bazan)
- Insurance: ~8% (Harel, Migdal, Clal)

## Trading Hours
Sunday-Thursday, 09:59 (pre-open) to 17:25 (closing auction). No trading Friday-Saturday.

## Data Sources
- tase.co.il: Live quotes, index composition
- maya.tase.co.il: Corporate filings
- isa.gov.il: ISA regulatory decisions
- bizportal.co.il: Financial analysis
- globes.co.il: Market news
