# Shekel Currency Converter Skill — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a skill that provides real-time and historical NIS currency conversion using Bank of Israel official exchange rates.

**Architecture:** MCP Enhancement skill with straightforward workflow. Wraps Bank of Israel API for exchange rate data and provides conversion calculations with financial context.

**Tech Stack:** SKILL.md, Python conversion script, Bank of Israel XML API.

---

## Research

### Bank of Israel Exchange Rates API
- **URL:** `https://www.boi.org.il/currency.xml` (current rates)
- **Historical:** `https://www.boi.org.il/PublicApi/GetExchangeRates?date=YYYY-MM-DD`
- **Auth:** None (public API)
- **Format:** XML response with exchange rates
- **Update frequency:** Daily (published around 15:30 Israel time)
- **Currencies:** ~30 currencies including USD, EUR, GBP, JPY, CHF, CAD, AUD
- **Rate type:** Representative rate (shaar yatzig) — the official rate for tax and legal purposes

### Use Cases
1. **Convert NIS to/from foreign currency** — Current rate conversion
2. **Historical rate lookup** — Get rate for a specific past date
3. **Multi-currency conversion** — Convert between two non-NIS currencies via NIS
4. **Tax-relevant rates** — Get the representative rate for tax reporting purposes
5. **Rate trend** — Show rate changes over a period

---

## Build Steps

### Task 1: Create SKILL.md

**Files:**
- Create: `repos/tax-and-finance/shekel-currency-converter/SKILL.md`

```markdown
---
name: shekel-currency-converter
description: >-
  Convert currencies to/from Israeli New Shekel (NIS/ILS) using Bank of Israel
  official exchange rates. Use when user asks to convert shekels, NIS, ILS,
  asks about exchange rates, "shaar yatzig" (representative rate), or needs
  currency conversion for Israeli tax or business purposes. Supports 30+
  currencies with current and historical rates. Do NOT use for cryptocurrency
  or unofficial money exchange rates.
license: MIT
allowed-tools: "Bash(python:*) WebFetch"
compatibility: "Requires network access for Bank of Israel API. Works with Claude Code, Claude.ai, Cursor."
metadata:
  author: skills-il
  version: 1.0.0
  category: tax-and-finance
  tags: [currency, shekel, nis, exchange-rate, bank-of-israel]
---

# Shekel Currency Converter

## Instructions

### Step 1: Identify Conversion Request
Parse the user's request for:
- **Source currency** and **target currency** (at least one should be NIS/ILS)
- **Amount** to convert
- **Date** (current or specific historical date)
- **Purpose** (general info vs. tax-relevant representative rate)

Common currency codes:
| Code | Currency | Hebrew |
|------|----------|--------|
| ILS | Israeli New Shekel | shekel chadash |
| USD | US Dollar | dolar |
| EUR | Euro | euro |
| GBP | British Pound | lira sterling |
| JPY | Japanese Yen | yen |
| CHF | Swiss Franc | frank shveitzi |

### Step 2: Fetch Exchange Rate
Use Bank of Israel API to get the rate:

**Current rate:**
```
Fetch: https://www.boi.org.il/currency.xml
Parse XML for the requested currency code
Extract: rate, unit, change from previous day
```

**Historical rate:**
```
Fetch: https://www.boi.org.il/PublicApi/GetExchangeRates?date=YYYY-MM-DD
Parse response for requested currency
Note: Rates not available for Shabbat/holidays — use last available business day
```

### Step 3: Calculate Conversion
```
If converting FROM NIS:
  result = amount / rate * unit

If converting TO NIS:
  result = amount * rate / unit

If converting between two foreign currencies:
  nis_amount = amount * rate_source / unit_source
  result = nis_amount / rate_target * unit_target
```

Note: Bank of Israel rates express how many NIS per unit(s) of foreign currency.
Example: USD rate = 3.65, unit = 1 means 1 USD = 3.65 NIS.
JPY rate = 2.45, unit = 100 means 100 JPY = 2.45 NIS.

### Step 4: Present Results
Format the result with:
- Converted amount (2 decimal places for NIS, appropriate precision for other currencies)
- Exchange rate used and its date
- Source: "Bank of Israel representative rate (shaar yatzig)"
- Change from previous day (if available)
- Caveat: "Representative rate for reference. Actual bank rates may differ."

## Examples

### Example 1: Simple USD to NIS
User says: "Convert 1000 dollars to shekels"
Result: "1,000 USD = 3,650.00 NIS (at Bank of Israel rate of 3.6500, published Feb 24, 2026)"

### Example 2: Historical Rate
User says: "What was the dollar rate on January 1, 2026?"
Result: "USD/ILS representative rate on Jan 1, 2026: 3.5800 (Bank of Israel shaar yatzig)"

### Example 3: Tax-Relevant Rate
User says: "I need the EUR rate for my VAT report for December 2025"
Result: Provides the representative rate for the relevant date, noting it's the official rate for tax purposes.

## Troubleshooting

### Error: "Rate not available for date"
Cause: Requested date is Shabbat, holiday, or future date
Solution: Use the last available business day rate. Bank of Israel publishes rates Sunday-Thursday.

### Error: "Currency not supported"
Cause: Bank of Israel doesn't publish a rate for this currency
Solution: Suggest using USD or EUR as intermediate currency for conversion.
```

**Step 2: Create conversion script**
`scripts/convert-currency.py` — Fetches BoI API, parses XML, performs calculation.

**Step 3: Validate and commit**
