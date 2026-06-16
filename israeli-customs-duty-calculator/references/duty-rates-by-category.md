# Indicative Duty Rates by Category

These are rough indicative ranges. Always verify the exact rate for your 8-digit HS code in Shaar Olami (`https://shaarolami-query.customs.mof.gov.il/CustomspilotWeb/en/CustomsBook/Import/Doubt`). VAT at 18 percent applies in addition on the post-duty CIF value.

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
| Spare parts | varies | 0 |

## Cosmetics and luxury

| Category | Typical duty | Purchase tax |
|----------|--------------|--------------|
| Cosmetics, skin care | 0 to moderate | varies |
| Perfumes | moderate | varies |
| Jewelry | 0 | 0 |

## Industrial goods

Most raw materials, machinery, and industrial inputs are duty-free under MFN rates or FTA preferences.

## The calculation sequence

```
CIF = (product_price + freight + insurance)
duty        = CIF * duty_rate
base_after_duty = CIF + duty
purchase_tax = base_after_duty * purchase_tax_rate
base_for_vat = base_after_duty + purchase_tax
vat         = base_for_vat * 0.18
landed      = CIF + duty + purchase_tax + vat + broker_fees
```

For personal imports, if the product value (excluding shipping and insurance, when itemized separately) is below the current threshold (USD 75 as of June 2026, after the temporary USD 130 window expired on 1 June 2026), no taxes apply at all. Between USD 75 and USD 500 only VAT applies, customs duty is waived under the personal-import regime, and purchase tax can still apply on specific items. Above USD 500 the full landed-cost calculation runs. Above USD 1,000 the shipment is treated as commercial and requires a customs broker. Tobacco, e-cigarettes, alcohol, and alcoholic beverages are excluded from the personal-import exemption regardless of value.
