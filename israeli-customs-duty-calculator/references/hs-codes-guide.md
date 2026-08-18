# Israeli HS Code Classification Guide

Israel uses the international Harmonized System at 6 digits and adds 2 Israel-specific digits (positions 7-8) that refine the classification for local duty and purchase tax rules.

## Structure

```
XX XX XX XX XX
|  |  |  |  |
|  |  |  |  +-- Position 7-8: Israel-specific ("paragraphs")
|  |  |  +----- Position 5-6: International HS sub-heading
|  |  +-------- Position 3-4: International HS heading
|  +----------- Position 1-2: Chapter
```

Example: `8525.89.10` (hypothetical) - Chapter 85 (electrical), heading 8525, subheading 89, Israeli paragraph 10.

## How to look up a code

1. Open Shaar Olami at `https://shaarolami-query.customs.mof.gov.il/CustomspilotWeb/en/CustomsBook/Import/Doubt`.
2. Search by keyword or chapter number.
3. Drill down to the 8-digit entry.
4. Read the columns:
   - Customs duty (MFN)
   - Customs duty under each FTA (US, EU, UK, CIFTA, EFTA, Mercosur)
   - Purchase tax rate
   - Any special import licenses or restrictions

## Common chapters

- Chapter 61-62: apparel
- Chapter 64: footwear
- Chapter 84: machinery
- Chapter 85: electrical machinery, electronics
- Chapter 87: vehicles
- Chapter 90: optical, medical instruments
- Chapter 94: furniture
- Chapter 95: toys, games

## Binding pre-ruling

If the classification is unclear, request a free binding pre-ruling from Israeli Customs. Submit:
- A detailed description of the goods
- A catalog or technical data sheet
- Photos or samples if relevant
- Intended use

The ruling is binding on Customs for that specific product as long as the description is accurate.

## Differences from US HTS and EU CN

Israel, the US, and the EU all share the first 6 digits of the HS code (the international standard). Beyond that:
- US uses 10-digit HTS codes with its own statistical suffixes.
- EU uses 8-digit CN codes, sometimes extended to 10-digit TARIC.
- Israel uses 8-digit codes with its own paragraphs.

A US HTS 10-digit code cannot be mechanically translated to an Israeli 8-digit code. Always re-classify via Shaar Olami.
