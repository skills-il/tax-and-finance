# Arnona Rate Structure Guide

Every figure in this file was read from the municipality's own published tzav arnona (צו ארנונה) for fiscal year 2026. The source PDF for each city is in the `source` field of `RATE_TABLES` in `scripts/arnona-calculator.py`, which carries the full residential table for each city. This guide explains how each city keys its rates.

## How a residential rate is set

A council sets the arnona for a building per square metre, "taking into account the type of the building, its use and its location" (Arrangements in the State Economy Regulations (General Arnona in Local Authorities) 5767-2007, reg. 4(1)). Every city in this guide keys its residential rate on at least two axes:

1. **Zone (azor)**, a geographic area set by map or street list.
2. **Building type or size class**, which each city defines differently: by year of completion (Tel Aviv), by building quality (Jerusalem, Haifa, Rishon LeZion, Ramat Gan), or by flat size (Petah Tikva, Herzliya, Raanana, Haifa's regular class).

So a single "rate for zone 2" does not exist. The bill shows the zone, the type code and the charged area. Read all three off the bill before computing anything.

## Fiscal-2026 residential tables, by city

| City | How it keys residential rates | Lowest to highest NIS/sqm/year |
|------|-------------------------------|-------------------------------|
| Tel Aviv-Yafo | Zones 1 to 5 (4 and 5 pay the same). Building type אא / כא / ח+א / ב+ג / ד / ה+ו, set by building description and year of completion. In zones 1 and 2 a flat of up to 140 sqm pays less than a villa or a larger flat | 46.64 to 139.60 |
| Jerusalem | Zones א to ד, crossed with building type 1 to 4 (type 1: a building with a flat of 120 sqm or more; type 2: stone, concrete or blocks). Flats first charged from 1.1.2020 pay one set of rates in every zone | 46.35 to 129.91 |
| Haifa | Zones א' to ד', crossed with class מ-1 to מ-6, crossed with flat size. The regular class מ-2 pays by band: up to 75, 76 to 100, over 100 sqm. Kiryat Haim has its own table | 43.12 to 125.59 (41.07 in Kiryat Haim) |
| Beer Sheva | Zones א to ג; zones א and ב have a lower rate for a flat of up to 57 sqm | 47.78 to 58.28 |
| Netanya | Zones 1 to 3, crossed with type א to ה (by elevator and flat size) | 41.05 to 94.85 |
| Rishon LeZion | Zones א' to ד', crossed with type אא / א / ב / ג | 42.50 to 77.10 |
| Petah Tikva | Zones א to ג (street list), crossed with a size-based type אא to ד | 43.39 to 84.96 |
| Ashdod | ONE residential zone for the whole city. The first 75 sqm pay 43.62, each further sqm pays 65.19 | 43.62 to 65.19 (91.13 for a resort unit) |
| Ramat Gan | Zones א'+, א', ב', ג', ד', crossed with type א+ to ד | 44.59 to 135.53 |
| Herzliya | Zones א to ז, crossed with type 1 to 7 (house or flat, and size) | 42.63 to 142.31 |
| Raanana | Zones 1 and 2, crossed with a size-based type 1 to 5 | 44.74 to 63.92 |

**A typical flat** (an ordinary flat, not a villa, penthouse or hotel unit) usually sits well inside each city's range. Examples from the tables: Tel Aviv zone 2, type ב+ג, flat up to 140 sqm: 72.89. Jerusalem zone ב, type 2: 86.34. Haifa zone ב', regular class, 76 to 100 sqm: 78.79. Beer Sheva zone ב, over 57 sqm: 50.45.

**Jerusalem zone ד.** The Interior Ministry director-general and the Finance Minister approved, on 14 and 15 December 2025, charging zone ד types 1 and 2 at the zone ג rates (91.07 and 64.23) for 2026. The tzav booklet published on the municipality site in September 2026 still prints 74.46 and 46.35 for those cells. The calculator shows both; the bill decides.

Modiin and the other local authorities are not tabulated. For them, and for every non-residential property, take the rate from that authority's tzav or from the bill and pass it to the calculator with `--rate-per-sqm`.

## Usage types

Each tzav sets separate tables for residential, offices / services / commerce, industry, crafts, hotels, banks, agricultural land and occupied land (קרקע תפוסה). Non-residential rates are not carried here because each city's tables are long and keyed differently; read the city's own tzav. A council may not change a property's type or classification during the year in a way that affects the arnona, unless the property's actual use changed (2007 regs, reg. 5(a)).

## Billing cycle and the annual update

- **Fiscal year**: 1 January to 31 December. Payment dates are set by each council. Haifa 2026, for example, takes six payments on the 1st of January, March, May, July, September and November, or twelve monthly standing-order payments on the 1st of each month.
- **Annual update**: rates rise every 1 January by a national coefficient, half the change in the CPI plus half the change in the public-sector wage (Arrangements Law 5753-1992, s.7). The Interior Ministry publishes it: **1.626% for 2026, 3.05% for 2027**.
- **Above-formula increases**: a council can raise a rate beyond the coefficient, or change a zone's definition, only with an exceptional approval from the Interior and Finance ministers (Jerusalem's 2026 zone ד change is one). So an increase larger than the coefficient means an approved exceptional increase, a reclassification, a measured area change, or a lost discount.

## Area calculation rules

The national rules:

1. Area is computed in square metres, and the arnona is the area times the rate per square metre (Arrangements Law s.8(b1)(1)).
2. Any part of a square metre is rounded to the nearest whole metre; exactly half a metre rounds DOWN (s.8(b1)(2)). A council that already used a different method (charging part-metres proportionally, or rounding down) may keep it (s.8(b1)(3)); Jerusalem, for example, charges the area to two decimal places. The area on the bill governs.
3. A property's area carries over from the previous year unless an error is found in the calculation "that is not the result of a different calculation method" (2007 regs, reg. 3(b)). Area added by construction during use is added (reg. 3(c)).

What counts as area (wall-to-wall or external walls, balconies, storage rooms, stairs, galleries) is set by each city's tzav, not by national law, and cities differ. Example, Haifa 2026 residential: everything inside the unit measured wall to wall, INCLUDING balconies, even unroofed ones, internal stairs, service rooms, sheds and galleries 1.80 m high or more. A standard shelter, and the shared areas of an ordinary building, are not charged. Ancillary buildings serving the flat count toward its size band. Do not assume "gross area" or "a reduced rate for balconies" for any city; read its "שיטת המדידה" section.

## Important notes

- These are fiscal-2026 figures. A tzav is reissued every year; re-read the current one at the start of each year.
- New buildings are often charged on a different type than older ones in the same zone (Tel Aviv by year of completion, Jerusalem's post-2020 rates).
- Mixed-use properties are charged separately for each part according to its use.
