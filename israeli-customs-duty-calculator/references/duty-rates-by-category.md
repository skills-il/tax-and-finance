# Indicative Duty Rates by Category

**This file is not a rate table and must never be quoted as one.** It is a shape-of-the-tariff orientation aid only: it says which categories tend to carry duty or purchase tax at all, so you know what to look up. Every cell that reads "varies", "moderate" or "0 to moderate" means exactly that: the number is not here and cannot be inferred from here. Nothing in this file binds; only the Tax Authority's classification of your 8-digit code does.

Always verify the exact rate for your 8-digit HS code in Shaar Olami (`https://shaarolami-query.customs.mof.gov.il/CustomspilotWeb/en/CustomsBook/Import/Doubt`). VAT at 18 percent applies in addition on the post-duty CIF value. CIF here is already converted at the Bank of Israel representative rate plus 0.5 percent, per SKILL.md Step 5; the uplift is applied once, at conversion, and nowhere else.

## Electronics

| Category | Typical duty | Purchase tax |
|----------|--------------|--------------|
| Phones, computers, cameras | 0 | 0 |
| TVs, monitors | 0 | varies |
| Home appliances | 0 to moderate | varies |

## Apparel and footwear

| Category | Typical duty | Purchase tax |
|----------|--------------|--------------|
| Cotton clothing | 0 to moderate | 0 |
| Synthetic clothing | moderate to higher | 0 |
| Leather footwear | moderate | 0 |

## Food and beverages

| Category | Typical duty | Notes |
|----------|--------------|-------|
| Unprocessed food | varies, some quotas | check TRQ (tariff rate quota) |
| Alcoholic beverages | varies | plus high purchase tax |
| Tobacco | varies | very high purchase tax |

## Vehicles and parts

| Category | Duty | Purchase tax |
|----------|------|--------------|
| Passenger cars | varies | very high, bulk of the landed cost |
| Electric vehicles | varies | lower than ICE but rising |
| Spare parts | varies | applies to many parts, verify the 8-digit code |

## Cosmetics and luxury

| Category | Typical duty | Purchase tax |
|----------|--------------|--------------|
| Cosmetics, skin care | 0 to moderate | varies |
| Perfumes | moderate | varies |
| Jewelry | varies, verify in Shaar Olami | varies, verify in Shaar Olami |

## Industrial goods

Most raw materials, machinery, and industrial inputs are duty-free under MFN rates or FTA preferences.

## The calculation sequence

```
CIF = (product_price + freight + insurance)
duty        = CIF * duty_rate
base_after_duty = CIF + duty
purchase_tax = base_after_duty * purchase_tax_rate   # FLOOR ONLY, see caveat below
base_for_vat = base_after_duty + purchase_tax
vat         = base_for_vat * 0.18
landed      = CIF + duty + purchase_tax + vat + broker_fees
```

For personal imports, if the product value (excluding shipping and insurance, when itemized separately) is at or below the current threshold (USD 75, re-verified 27 August 2026, after the USD 130 window ran to 1 June 2026), no taxes apply at all. Between USD 75 and USD 500 only VAT applies, customs duty is waived under the personal-import regime, and purchase tax can still apply on specific items. Above USD 500 VAT applies and some goods also owe duty and purchase tax, depending on the HS classification. Above USD 1,000 the shipment is treated as commercial for tax purposes, and carriers in practice require a broker. Tobacco products and alcoholic beverages are excluded from the personal-import exemption regardless of value.

**Caveat on the purchase-tax line above, same as SKILL.md Step 6.** Purchase tax is levied on a reconstructed wholesale price, not on CIF plus duty, so the line above is a floor rather than the charge. The uplift that reconstructs it varies by tariff item and is not verified in this skill. On alcohol and tobacco the tariff is specific or compound rather than a percentage, and the formula cannot express it at all. Take the combined rate for the specific item off the Tax Authority personal-import calculator.
