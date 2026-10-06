#!/usr/bin/env python3
"""
Israeli Arnona (Municipal Property Tax) Calculator

Calculates annual and bimonthly residential arnona from the fiscal-2026 tzav
arnona of eleven municipalities, keyed the way each tzav actually keys it: zone
AND the municipality's own building type or size class. Applies the national
discount rows, and picks the Reg. 2(a)(8) income band from the First Schedule.

Usage:
    python arnona-calculator.py --municipality tel-aviv --area 85 --zone 2 --type ב+ג
    python arnona-calculator.py --municipality jerusalem --area 70 --zone ב --type 2 --discount oleh
    python arnona-calculator.py --municipality haifa --area 90 --zone ב --type 2 --discount low-income --household-income 9000 --household-size 3 --fiscal-year 2027
    python arnona-calculator.py --municipality other --area 60 --rate-per-sqm 150 --usage commercial
    python arnona-calculator.py --list-municipalities
    python arnona-calculator.py --list-types tel-aviv
    python arnona-calculator.py --list-discounts

Requirements:
    Python 3.8+
    No external dependencies
"""

import argparse
import json
import sys
from dataclasses import dataclass, field
from typing import List, Optional, Tuple


# ============================================================
# Rate Tables (residential only)
# ============================================================
#
# Every figure below was read from the municipality's own published tzav
# arnona for fiscal year 2026 (the PDF in "source"). Each row is
#   (zone, type, area_from_exclusive, area_to_inclusive, rate)
# where the area bounds are None when the row has no size limit, and "rate"
# is NIS per sqm per year. A rate that is a list of (up_to_sqm, rate) pairs is
# MARGINAL: the first slice of the flat pays the first rate, the rest pays the
# next one (Ashdod; Haifa's luxury class above 100 sqm).
#
# Only RESIDENTIAL rates are carried. Non-residential tariffs, the other ~240
# local authorities, and special rows (hotels, nursing homes, Haifa's Kiryat
# Haim table, Ramat Gan's Kfar Azar tier) are not modelled: pass the rate from
# your own tzav or bill with --rate-per-sqm.
#
# A tzav changes every year. These are fiscal-2026 figures. For fiscal 2027
# the script also prints a projection at the national update coefficient,
# which is NOT the 2027 rate of any municipality that obtained an approved
# above-formula increase or reclassified zones.

TZAV_YEAR = 2026

# National annual update coefficients (half the CPI change plus half the
# public-sector wage change, Arrangements Law 5753-1992 s.7), as published on
# the Interior Ministry arnona page.
NATIONAL_UPDATE_COEFFICIENT_PCT = {2026: 1.626, 2027: 3.05}


def _grid(zones, types, values, bands=None):
    """Expand a zone x type grid into rows. values[zone_index][type_index];
    None means the tzav prints no rate for that cell. bands maps a type to
    (area_from_exclusive, area_to_inclusive)."""
    rows = []
    for zi, zone in enumerate(zones):
        for ti, typ in enumerate(types):
            rate = values[zi][ti]
            if rate is None:
                continue
            lo, hi = (bands or {}).get(typ, (None, None))
            rows.append((zone, typ, lo, hi, rate))
    return rows


# --- Tel Aviv-Yafo -------------------------------------------------------
# Zones 1-5 (4 and 5 share one column). Rows are building types set by the
# building description and year of completion (tzav section 2.1); the bill
# shows yours. In zones 1 and 2 a flat of up to 140 sqm pays less than a villa
# or a flat over 140 sqm.
_TA_TYPES = ["אא", "כא", "ח+א", "ב+ג", "ד", "ה+ו"]
# columns: zone1 villa/>140, zone1 flat<=140, zone2 villa/>140, zone2 flat<=140, zone3, zone4-5
_TA = {
    "אא": (139.60, 112.99, 108.98, 90.71, 78.39, 64.42),
    "כא": (138.97, 112.49, 108.49, 90.29, 78.06, 64.13),
    "ח+א": (132.35, 107.12, 103.33, 86.01, 74.34, 61.09),
    "ב+ג": (112.16, 90.78, 87.56, 72.89, 63.01, 54.05),
    "ד": (97.54, 78.94, 76.14, 63.38, 54.79, 49.15),
    "ה+ו": (84.81, 68.64, 66.21, 55.10, 47.65, 46.64),
}


def _ta_rows():
    rows = []
    for typ, (z1v, z1f, z2v, z2f, z3, z45) in _TA.items():
        rows += [
            ("1", typ, None, 140, z1f), ("1", typ, 140, None, z1v), ("1", typ + "/villa", None, None, z1v),
            ("2", typ, None, 140, z2f), ("2", typ, 140, None, z2v), ("2", typ + "/villa", None, None, z2v),
        ]
        for zone, rate in (("3", z3), ("4", z45), ("5", z45)):
            rows += [(zone, typ, None, None, rate), (zone, typ + "/villa", None, None, rate)]
    return rows


# --- Haifa (all of Haifa except Kiryat Haim, which has its own table) ------
_HAIFA_ROWS = []
for _zone, (m1, m1_extra, m2_75, m2_100, m2_big, m3_75, m3_big, m4_75, m4_big) in {
    "א": (119.57, 125.59, 90.07, 103.94, 119.57, 56.42, 65.25, 43.12, 48.94),
    "ב": (90.50, 115.64, 68.46, 78.79, 90.50, 43.12, 48.94, 43.12, 43.12),
    "ג": (63.13, 90.79, 47.52, 53.62, 63.13, 43.12, 43.12, 43.12, 43.12),
    "ד": (None, None, 43.12, 43.12, 44.68, 43.12, 43.12, 43.12, 43.12),
}.items():
    if m1 is not None:
        _HAIFA_ROWS += [(_zone, "1", None, 100, m1), (_zone, "1", 100, None, [(100, m1), (None, m1_extra)])]
    _HAIFA_ROWS += [
        (_zone, "2", None, 75, m2_75), (_zone, "2", 75, 100, m2_100), (_zone, "2", 100, None, m2_big),
        (_zone, "3", None, 75, m3_75), (_zone, "3", 75, None, m3_big),
        (_zone, "4", None, 75, m4_75), (_zone, "4", 75, None, m4_big),
        (_zone, "5", None, None, 43.12), (_zone, "6", None, None, 43.12),
    ]

_HERZLIYA_BANDS = {"2": (125, None), "3": (90, 125), "4": (None, 90),
                   "5": (90, None), "6": (70, 90), "7": (None, 70)}

RATE_TABLES = {
    "tel-aviv": {
        "name": "Tel Aviv-Yafo",
        "source": "https://www.tel-aviv.gov.il/Residents/Arnona/Documents/%D7%97%D7%95%D7%91%D7%A8%D7%AA%20%D7%A6%D7%95%20%D7%94%D7%90%D7%A8%D7%A0%D7%95%D7%A0%D7%94%20%D7%9C%D7%A9%D7%A0%D7%AA%202026.pdf",
        "zone_system": "numbered zones 1-5 (4 and 5 pay the same rate)",
        "types": {
            "אא": "regular building completed 2022 or later (the type is set by building description and year of completion; read it off the bill)",
            "כא": "regular building completed 2010-2021",
            "ח+א": "the ח and א types (for example a regular building completed 1984-2009)",
            "ב+ג": "the ב and ג types (for example a regular building completed 1970-1983)",
            "ד": "type ד (for example a regular building completed 1940-1969)",
            "ה+ו": "the ה and ו types (oldest buildings, basements, temporary structures)",
            "<type>/villa": "a villa of any size; in zones 1-2 a flat over 140 sqm pays the same rate",
        },
        "rows": _ta_rows(),
        "notes": ["Zones 1 and 2 split at 140 sqm for flats; a villa pays the higher column at any size."],
    },
    "jerusalem": {
        "name": "Jerusalem",
        "source": "https://www.jerusalem.muni.il/media/dl0hvk34/%D7%A6%D7%95-%D7%9E%D7%99%D7%A1%D7%99%D7%9D-%D7%9E%D7%9C%D7%90-2026-%D7%9E%D7%A2%D7%95%D7%93%D7%9B%D7%9F-%D7%9C%D7%90%D7%AA%D7%A8.pdf",
        "zone_system": "Hebrew-letter zones א-ד, plus 'new' for flats first charged from 1.1.2020 (one rate set in every zone)",
        "types": {
            "1": "the tzav: a building with a flat of 120 sqm or more; the council's explanatory note reads it as a flat over 120 sqm. Take the type from the bill",
            "2": "a building of stone, concrete or blocks (the ordinary flat)",
            "3": "a flat whose services are outside it",
            "4": "a dilapidated, wooden or tin building, no services, or a basement flat",
        },
        "rows": _grid(["א", "ב", "ג"], ["1", "2", "3", "4"], [
            [129.91, 107.65, 75.70, 46.35],
            [118.04, 86.34, 56.28, 46.35],
            [91.07, 64.23, 46.35, 46.35],
        ]) + _grid(["new"], ["1", "2", "3", "4"], [[129.91, 107.65, 75.70, 46.35]]) + [
            ("ד", "1", None, None, 74.46, "booklet"), ("ד", "1", None, None, 91.07, "ministers' approval"),
            ("ד", "2", None, None, 46.35, "booklet"), ("ד", "2", None, None, 64.23, "ministers' approval"),
            ("ד", "3", None, None, 46.35), ("ד", "4", None, None, 46.35),
        ],
        "notes": [
            ("ד", "Zone ד types 1 and 2: the ministers approved (14-15.12.2025) charging them at zone ג rates for 2026 "
            "(91.07 and 64.23), but the booklet published in September 2026 still prints 74.46 and 46.35. "
            "Both are shown; the bill decides."),
        ],
    },
    "haifa": {
        "name": "Haifa (excluding Kiryat Haim)",
        "source": "https://www.haifa.muni.il/wp-content/uploads/2021/08/%D7%A6%D7%95-%D7%9E%D7%A1%D7%99%D7%9D-2026-%D7%A1%D7%95%D7%A4%D7%99-%D7%9C%D7%90%D7%97%D7%A8-%D7%90%D7%99%D7%A9%D7%95%D7%A8-%D7%94%D7%A9%D7%A8%D7%99%D7%9D-%D7%9E%D7%95%D7%A0%D7%92%D7%A9-PDFUA-12.pdf",
        "zone_system": "Hebrew-letter zones א-ד",
        "types": {
            "1": "מ-1 luxury building (over 100 sqm: the area above 100 pays the per-additional-sqm rate)",
            "2": "מ-2 regular building; the WHOLE flat pays its size band (up to 75 / 76-100 / over 100 sqm)",
            "3": "מ-3 partly underground building",
            "4": "מ-4 simple building",
            "5": "מ-5 ancillary building attached to the flat",
            "6": "מ-6 simple basement or partly underground building",
        },
        "rows": _HAIFA_ROWS,
        "notes": [
            "The regular class is banded by flat size, so an area correction across 75 or 100 sqm changes the rate "
            "for the whole flat, not just the disputed metres.",
            "Kiryat Haim has its own table and is not modelled; use --rate-per-sqm.",
        ],
    },
    "beer-sheva": {
        "name": "Beer Sheva",
        "source": "https://www.beer-sheva.muni.il/Residents/Arnona/Documents/%D7%A6%D7%95%D7%95%D7%99-%D7%90%D7%A8%D7%A0%D7%95%D7%A0%D7%94/%D7%A6%D7%95%20%D7%90%D7%A8%D7%A0%D7%95%D7%A0%D7%94%20%D7%9C%D7%A9%D7%A0%D7%AA%202026.pdf",
        "zone_system": "Hebrew-letter zones א-ג",
        "types": {"residential": "residential; zones א and ב have a lower rate for a flat of up to 57 sqm"},
        "rows": [
            ("א", "residential", None, 57, 51.94), ("א", "residential", 57, None, 58.28),
            ("ב", "residential", None, 57, 47.78), ("ב", "residential", 57, None, 50.45),
            ("ג", "residential", None, None, 48.64),
        ],
        "notes": [],
    },
    "netanya": {
        "name": "Netanya",
        "source": "https://www.netanya.muni.il/DocLib1/zavmisim26.pdf",
        "zone_system": "numbered zones 1-3",
        "types": {
            "א": "penthouse, private house over 100 sqm, or nursing home",
            "ב": "flat over 110 sqm in an elevator building, row houses, or a private house of up to 100 sqm",
            "ג": "flat of 81-110 sqm in an elevator building, or a non-elevator flat over 110 sqm",
            "ד": "flat of up to 80 sqm in an elevator building, or a non-elevator flat of up to 110 sqm",
            "ה": "below the entrance level, or other",
        },
        "rows": _grid(["1", "2", "3"], ["א", "ב", "ג", "ד", "ה"], [
            [94.85, 88.49, 79.23, 65.51, 48.66],
            [78.42, 68.14, 61.63, 56.44, 44.93],
            [56.15, 51.50, 47.71, 41.05, 41.05],
        ]),
        "notes": [],
    },
    "rishon-lezion": {
        "name": "Rishon LeZion",
        "source": "https://www.rishonlezion.muni.il/Residents/arnona/ArnonaOrders/%D7%A6%D7%95_%D7%90%D7%A8%D7%A0%D7%95%D7%A0%D7%94_2026.pdf",
        "zone_system": "Hebrew-letter zones א-ד",
        "types": {
            "אא": "ground-attached house, or penthouse or duplex over 110 sqm",
            "א": "regular flat with its own WC and bath",
            "ב": "built 1990 or earlier with a combined WC and bath, a caravan, or student housing",
            "ג": "mud-built, underground, ministry caravan, or wooden built before 1960",
        },
        "rows": _grid(["א", "ב", "ג", "ד"], ["אא", "א", "ב", "ג"], [
            [77.10, 69.69, 47.92, 42.50],
            [71.65, 52.58, 42.50, 42.50],
            [77.10, 69.69, 47.92, 42.50],
            [77.10, 69.69, 47.92, 42.50],
        ]),
        "notes": [],
    },
    "petah-tikva": {
        "name": "Petah Tikva",
        "source": "https://api.petah-tikva.muni.il/media/vovfqold/%D7%A6%D7%95-%D7%9E%D7%99%D7%A1%D7%99%D7%9D-2026-%D7%97%D7%95%D7%A7%D7%99-%D7%A7%D7%99%D7%99%D7%9D-%D7%A1%D7%95%D7%A4%D7%99-pdfua.pdf",
        "zone_system": "Hebrew-letter zones א-ג (by street list)",
        "types": {
            "אא": "flat of 140 sqm or more, or a house of 130 sqm or more",
            "א": "flat of 75-139 sqm, or a house of 60-129 sqm",
            "ב": "flat of 50-74 sqm, or a house of 45-59 sqm",
            "ג": "flat under 50 sqm, house under 45 sqm, container or caravan",
            "ד": "other",
        },
        "rows": _grid(["א", "ב", "ג"], ["אא", "א", "ב", "ג", "ד"], [
            [84.96, 79.26, 62.89, 56.27, 43.39],
            [74.58, 69.65, 57.00, 50.41, 43.39],
            [48.54, 44.71, 43.39, 43.39, 43.39],
        ]),
        "notes": [],
    },
    "ashdod": {
        "name": "Ashdod",
        "source": "https://www.ashdod.muni.il/media/16515460/%D7%A6%D7%95-%D7%94%D7%90%D7%A8%D7%A0%D7%95%D7%A0%D7%94-%D7%9C%D7%A9%D7%A0%D7%AA-2026-%D7%90%D7%95%D7%A9%D7%A8-%D7%91%D7%9E%D7%95%D7%A2%D7%A6%D7%AA-%D7%94%D7%A2%D7%99%D7%A8-%D7%91%D7%AA%D7%90%D7%A8%D7%99%D7%9A-25-06-25-pdfua.pdf",
        "zone_system": "ONE residential zone for the whole city (pass --zone 1 or omit it)",
        "types": {
            "residential": "first 75 sqm at the lower rate, each further sqm at the higher rate",
            "resort": "holiday or resort unit",
        },
        "rows": [
            ("1", "residential", None, None, [(75, 43.62), (None, 65.19)]),
            ("1", "resort", None, None, 91.13),
        ],
        "notes": ["Council-adopted tzav of 25.06.2025."],
    },
    "ramat-gan": {
        "name": "Ramat Gan",
        "source": "https://cms-media.ramat-gan.muni.il/media/lchlofwg/tzav-arnona-2026.pdf",
        "zone_system": "zones א+, א, ב, ג, ד",
        "types": {
            "א+": "private house, or a penthouse or flat over 130 sqm assessed since 1.1.1974",
            "א": "flat in a shared building assessed since 1.1.1972",
            "ב": "flat in good condition",
            "ג": "dilapidated flat",
            "ד": "huts",
        },
        "rows": _grid(["א+", "א", "ב", "ג", "ד"], ["א+", "א", "ב", "ג", "ד"], [
            [135.53, 112.99, None, None, None],
            [111.15, 92.66, 77.64, 57.29, 44.59],
            [93.79, 83.35, 64.56, 46.54, 44.59],
            [82.17, 69.66, 50.91, 44.59, 44.59],
            [71.09, 60.25, 46.60, 44.59, 44.59],
        ]),
        "notes": ["Kfar Azar flats assessed up to 31.12.2013 pay a separate tier and are not modelled."],
    },
    "herzliya": {
        "name": "Herzliya",
        "source": "https://herzliya.muni.il/uploads/n/1771243430.8638.pdf",
        "zone_system": "Hebrew-letter zones א-ז",
        "types": {
            "1": "hotel, aparthotel or guesthouse unit",
            "2": "detached house or penthouse over 125 sqm",
            "3": "detached house or penthouse of 90-125 sqm",
            "4": "detached house or penthouse of up to 90 sqm",
            "5": "flat over 90 sqm in a multi-unit building",
            "6": "flat of 70-90 sqm in a multi-unit building",
            "7": "flat of up to 70 sqm in a multi-unit building",
        },
        "rows": _grid(["א", "ב", "ג", "ד", "ה", "ו", "ז"], ["1", "2", "3", "4", "5", "6", "7"], [
            [142.31] * 7,
            [142.31, 101.57, 92.35, 76.66, 76.66, 57.25, 42.63],
            [142.31, 99.93, 90.87, 75.50, 75.50, 56.33, 42.63],
            [142.31, 97.81, 89.00, 73.89, 73.89, 55.15, 42.63],
            [142.31, 94.72, 86.16, 71.56, 71.56, 53.44, 42.63],
            [142.31, 93.28, 84.83, 70.44, 70.44, 52.64, 42.63],
            [142.31] + [42.63] * 6,
        ], bands=_HERZLIYA_BANDS),
        "notes": ["Council decision of 24.6.2025."],
    },
    "raanana": {
        "name": "Raanana",
        "source": "https://www.raanana.muni.il/wp-content/uploads/2025/12/%D7%A6%D7%95-%D7%90%D7%A8%D7%A0%D7%95%D7%A0%D7%94-2026.pdf",
        "zone_system": "numbered zones 1-2 (zone 2 is a listed set of neighbourhoods)",
        "types": {
            "1": "flat of 121 sqm or more",
            "2": "flat of 86-120 sqm",
            "3": "flat of up to 85 sqm",
            "4": "huts, asbestos or block structures built by 1960, caravans",
            "5": "zone 2 only: flat of 121 sqm or more in Kiryat Sharet or Kiryat Shazar enlarged by 50% after 31.3.81, or newer",
        },
        "rows": [
            ("1", "1", 120, 140, 62.25), ("1", "1", 140, None, 63.92),
            ("2", "1", 120, 140, 50.63), ("2", "1", 140, None, 51.97),
            ("1", "2", 85, 120, 54.62), ("2", "2", 85, 120, 48.42),
            ("1", "3", None, 85, 48.42), ("2", "3", None, 85, 48.42),
            ("1", "4", None, None, 44.74), ("2", "4", None, None, 44.74),
            ("2", "5", 120, None, 55.73),
        ],
        "notes": ["Council decision of 25.6.2025."],
    },
}

# Reg. 2(a)(8) First Schedule. Keys are FISCAL years; each fiscal year tests
# the average monthly gross household income of the preceding calendar year.
# Row n = household size 1..9: upper bounds of the 90 / 70 / 50 / 30 percent
# bands. "extra" = amount added per person from the tenth.
# 2026: Reshumot Kovetz HaTakanot 12366 (20.4.2026).
# 2027: notice in Kovetz HaTakanot 12490 (28.7.2026), as corrected by 12499.
INCOME_TABLE = {
    2026: {
        "rows": [
            (3513, 4295, 5076, 5857), (5621, 6872, 8122, 9372), (7449, 9106, 10762, 12417),
            (8996, 10996, 12995, 14994), (10541, 12886, 15229, 17572), (11948, 14604, 17259, 19914),
            (13352, 16322, 19290, 22257), (14618, 17868, 21117, 24366), (15743, 19243, 22742, 26240),
        ],
        "extra": (1125, 1374, 1624, 1874),
    },
    2027: {
        "rows": [
            (3623, 4430, 5235, 6041), (5798, 7088, 8377, 9666), (7683, 9392, 11100, 12807),
            (9278, 11341, 13403, 15465), (10872, 13291, 15707, 18124), (12323, 15063, 17801, 20539),
            (13771, 16835, 19896, 22956), (15077, 18429, 21780, 25131), (16237, 19847, 23456, 27064),
        ],
        "extra": (1160, 1417, 1675, 1933),
    },
}
INCOME_BANDS = (90, 70, 50, 30)


def income_band(fiscal_year: int, household_size: int, income: float) -> Tuple[Optional[int], Tuple[int, ...]]:
    """Return (band percentage or None if above the top threshold, thresholds used)."""
    table = INCOME_TABLE[fiscal_year]
    if household_size <= 9:
        bounds = table["rows"][household_size - 1]
    else:
        extra_people = household_size - 9
        bounds = tuple(b + e * extra_people for b, e in zip(table["rows"][8], table["extra"]))
    for pct, bound in zip(INCOME_BANDS, bounds):
        if income <= bound:
            return pct, bounds
    return None, bounds


# ============================================================
# Discount Categories
# ============================================================
#
# Every entry below is traceable to the Arrangements in the State Economy
# Regulations (Arnona Discount), 5753-1993. Nothing here is inferred from
# municipal practice: a category with no national rate is deliberately absent
# rather than given an invented percentage.
#
# "kind" separates the two legal shapes, and the distinction is not cosmetic:
#   ceiling     - Regulation 2/3f/3g/7/14c: the council MAY set a discount up
#                 to this figure. The resident is not owed it. Treat the
#                 output as an upper bound.
#   entitlement - Chapter Hey2 (14e, 14e1) and Regulations 3c/3c1: the resident
#                 IS entitled, and the council has no discretion.
#
# "max_sqm" is None where the regulation states no area cap.
# "max_sqm_large_household" applies where the cap rises when more than four
# family members live with the holder (Reg. 14f, and Reg. 2(4)).
#
# NOT IN THIS TABLE, on purpose: student and large-family discounts. The
# regulation contains no such paragraph, so there is no national rate to apply.
# A large household's national route is the "low-income" income test at
# Reg. 2(8), whose thresholds rise with household size. Municipal bylaws may
# add either category; read the local table rather than assuming a figure.

DISCOUNTS = {
    "oleh": {
        "name": "Oleh Chadash (New Immigrant)",
        "name_he": "עולה חדש",
        "kind": "ceiling",
        "basis": "Reg. 2(a)(6)",
        "percentage": 90,
        "max_sqm": 100,
        "max_sqm_large_household": None,
        "duration_months": 12,
        "description": "Up to 90% on up to 100 sqm; 12 discounted months chosen within the first 24 from population-registry oleh registration, or from the date on an oleh-citizen certificate",
    },
    "oleh-dependent": {
        "name": "Oleh dependent on the help of others",
        "name_he": "עולה התלוי בעזרת הזולת",
        "kind": "ceiling",
        "basis": "Reg. 2(a)(6a)",
        "percentage": 80,
        "max_sqm": None,
        "max_sqm_large_household": None,
        "duration_months": None,
        "description": "Up to 80% for an oleh certified by Bituach Leumi as entitled to a special benefit or a nursing benefit for olim; no area cap stated",
    },
    "tzadal": {
        "name": "South Lebanon Army (SLA) member",
        "name_he": "איש צד\"ל",
        "kind": "ceiling",
        "basis": "Reg. 2(a)(6b)",
        "percentage": 90,
        "max_sqm": 100,
        "max_sqm_large_household": None,
        "duration_months": 12,
        "description": "Up to 90% on 100 sqm for 12 months within 36 from arrival in Israel after May 2000, for an SLA member recognised as rehabilitation-eligible by the MANBAS, and their spouse",
    },
    "soldier": {
        "name": "Conscript soldier / national or civilian-security service",
        "name_he": "חייל בשירות סדיר / שירות לאומי",
        "kind": "entitlement",
        "basis": "Reg. 14e(1), area cap Reg. 14f",
        "percentage": 100,
        "max_sqm": 70,
        "max_sqm_large_household": 90,
        "duration_months": None,
        "description": "100% entitlement while serving and for four months after discharge; also a national-service volunteer, a full-track civilian-service or guarding-civilian-service member, and a civilian-security service member. Capped at 70 sqm, or 90 sqm where more than four family members live with the holder",
    },
    "soldier-parent": {
        "name": "Parent supported by the soldier",
        "name_he": "הורה שפרנסתו היתה על החייל",
        "kind": "entitlement",
        "basis": "Reg. 14e(1)(b)",
        "percentage": 100,
        "max_sqm": 70,
        "max_sqm_large_household": 90,
        "duration_months": None,
        "description": "100% entitlement for a parent who proves the soldier supported them before service and who has no livelihood and cannot obtain one, provided the soldier is exempt under 14e(1)(a)",
    },
    "civilian-social-full": {
        "name": "Civilian-social service, 30 weekly hours over two years",
        "name_he": "משרת בשירות אזרחי-חברתי (30 שעות)",
        "kind": "entitlement",
        "basis": "Reg. 14e(1a)",
        "percentage": 75,
        "max_sqm": 70,
        "max_sqm_large_household": 90,
        "duration_months": None,
        "description": "Three quarters entitlement while serving 30 weekly hours on average over two years",
    },
    "disabled-veteran": {
        "name": "Disabled veteran, police, prison service, bereaved family, hostile-action casualty",
        "name_he": "נכה צה\"ל, משטרה, שב\"ס, משפחה שכולה, נפגע פעולת איבה",
        "kind": "entitlement",
        "basis": "Reg. 14e(2)",
        "percentage": 66.67,
        "max_sqm": 70,
        "max_sqm_large_household": 90,
        "duration_months": None,
        "description": "Two-thirds entitlement for a disabled person under the Invalids (Pensions and Rehabilitation) Law, the Nazi-war Invalids Law, the Police (Disabled and Fallen) Law, the Prison Service (Disabled and Fallen) Law, a bereaved family member under the Families of Soldiers Who Fell Law, or a hostile-action casualty under the 5730-1970 Law",
    },
    "civilian-split": {
        "name": "Civilian service, split track",
        "name_he": "משרת בשירות אזרחי במסלול מפוצל",
        "kind": "entitlement",
        "basis": "Reg. 14e(3)",
        "percentage": 50,
        "max_sqm": 70,
        "max_sqm_large_household": 90,
        "duration_months": None,
        "description": "50% entitlement for a split-track civilian service member, a 20-hour guarding-civilian-service member over 24 months, or a civilian-social service member serving 20 weekly hours over three years",
    },
    "hostage-missing": {
        "name": "Hostage or missing person",
        "name_he": "חטוף או נעדר",
        "kind": "entitlement",
        "basis": "Reg. 14e1",
        "percentage": 100,
        "max_sqm": None,
        "max_sqm_large_household": None,
        "duration_months": None,
        "description": "100% entitlement for a holder determined to be a hostage or missing person under the Benefits for Family Members of Hostages and Missing Persons in a Hostile Act Law 5784-2023, for the period they are so classified",
    },
    "gaza-envelope": {
        "name": "Sderot and the Gaza-envelope localities",
        "name_he": "שדרות ויישובי עוטף עזה",
        "kind": "entitlement",
        "basis": "Reg. 3c",
        "percentage": 45,
        "max_sqm": None,
        "max_sqm_large_household": None,
        "duration_months": None,
        "percentage_non_residential": 39,
        "description": "45% entitlement on residential property and 39% on other property (the script picks the limb from --usage) for fiscal years 2015 to 2026, for a property in the Gaza-envelope localities or within 7 km of the Gaza perimeter fence. No extension to 2027 had been published as of October 2026; past extensions arrived late and retroactively",
    },
    "evacuated-locality": {
        "name": "Evacuated locality (Iron Swords)",
        "name_he": "יישוב מפונה (חרבות ברזל)",
        "kind": "entitlement",
        "basis": "Reg. 3c1",
        "percentage": 100,
        "max_sqm": None,
        "max_sqm_large_household": None,
        "duration_months": None,
        "description": "100% entitlement from 7 October 2023 until the end of the evacuation or refresh period, for a holder in a locality listed under the Iron Swords deferral-of-dates law. Where the government ordered only a partial evacuation, only holders the municipality determined were eligible for it qualify",
    },
    "senior-income": {
        "name": "Senior (vatik), income-tested statutory entitlement",
        "name_he": "אזרח ותיק, זכאות לפי חוק האזרחים הותיקים",
        "kind": "entitlement",
        "basis": "Senior Citizens Law 5750-1989, s.9(b) and 9(c)(4)",
        "percentage": 30,
        "max_sqm": 100,
        "max_sqm_large_household": None,
        "duration_months": None,
        "description": "30% entitlement on 100 sqm where the senior's total income from every source does not exceed the average wage; where more than one senior lives in the flat the combined income of everyone living there must not exceed 150% of the average wage. Given for one flat and to one senior only, even if several qualify",
    },
    "senior-income-supplement": {
        "name": "Senior (vatik) receiving an income-support benefit",
        "name_he": "אזרח ותיק המקבל גמלת הבטחת הכנסה",
        "kind": "entitlement",
        "basis": "Senior Citizens Law 5750-1989, s.9(b)",
        "percentage": 100,
        "max_sqm": 100,
        "max_sqm_large_household": None,
        "duration_months": None,
        "description": "100% entitlement on 100 sqm where the senior receives a benefit under the Income Support Law 5741-1980. This is the statutory route; Reg. 2(a)(1)(b) is the parallel discretionary ceiling. The same 100% goes to a low-pension senior under s.13A (pension income up to 24.3% of the average wage, 38.3% with a spouse, who would otherwise get income support)",
    },
    "senior-pension": {
        "name": "Senior (vatik), pension recipient",
        "name_he": "אזרח ותיק, מקבל קצבה",
        "kind": "ceiling",
        "basis": "Reg. 2(a)(1)(a)",
        "percentage": 25,
        "max_sqm": 100,
        "max_sqm_large_household": None,
        "duration_months": None,
        "description": "Up to 25% on 100 sqm for a senior receiving an old-age, survivors, dependants, or work-injury disability pension; no income test",
    },
    "senior-supplement": {
        "name": "Senior (vatik) with income supplement",
        "name_he": "אזרח ותיק עם השלמת הכנסה",
        "kind": "ceiling",
        "basis": "Reg. 2(a)(1)(b)",
        "percentage": 100,
        "max_sqm": 100,
        "max_sqm_large_household": None,
        "duration_months": None,
        "description": "Up to 100% on 100 sqm where the senior receives an income-support benefit in addition to the pension in 2(a)(1)(a)",
    },
    "disabled-incapacity": {
        "name": "Earning incapacity 75%+ with a full monthly benefit",
        "name_he": "אי-כושר השתכרות 75%+",
        "kind": "ceiling",
        "basis": "Reg. 2(a)(2)",
        "percentage": 80,
        "max_sqm": None,
        "max_sqm_large_household": None,
        "duration_months": None,
        "description": "Up to 80% for a person entitled to a full monthly benefit with an earning-incapacity degree of 75% or more under section 127lamed-vav of the National Insurance Law, including a permanent determination made before old-age pension began; no area cap stated",
    },
    "disabled-medical": {
        "name": "Medical disability 90%+",
        "name_he": "נכות רפואית 90%+",
        "kind": "ceiling",
        "basis": "Reg. 2(a)(3)",
        "percentage": 40,
        "max_sqm": None,
        "max_sqm_large_household": None,
        "duration_months": None,
        "description": "Up to 40% for a proven medical disability of 90% or more under any law, including a determination made before old-age pension began; no area cap stated",
    },
    "persecution-pension": {
        "name": "Prisoner of Zion / Nazi-persecution pension",
        "name_he": "אסיר ציון / גמלת רדיפות הנאצים",
        "kind": "ceiling",
        "basis": "Reg. 2(a)(4)",
        "percentage": 66,
        "max_sqm": 70,
        "max_sqm_large_household": 90,
        "duration_months": None,
        "description": "Up to 66% on 70 sqm (90 sqm where more than four family members live with the holder) for a Prisoner of Zion or family of a Hanged of the Kingdom benefit, a Nazi Persecution Invalids Law benefit, or a disability pension paid by Germany (BEG), the Netherlands (WUV), Austria (OFG), or Belgium under its 1954 law",
    },
    "blind": {
        "name": "Holder of a blind person's certificate",
        "name_he": "בעל תעודת עיוור",
        "kind": "ceiling",
        "basis": "Reg. 2(a)(5)",
        "percentage": 90,
        "max_sqm": None,
        "max_sqm_large_household": None,
        "duration_months": None,
        "description": "Up to 90% for a holder of a blind person's certificate under the Welfare Services Law 5718-1958; no area cap stated",
    },
    "nursing-benefit": {
        "name": "Long-term nursing benefit (gimlat siud)",
        "name_he": "גמלת סיעוד",
        "kind": "ceiling",
        "basis": "Reg. 2(a)(7)(c)",
        "percentage": 70,
        "max_sqm": None,
        "max_sqm_large_household": None,
        "duration_months": None,
        "description": "Up to 70% for a recipient of a nursing benefit under Chapter Vav of the National Insurance Law; no area cap stated",
    },
    "low-income": {
        "name": "Low income (First Schedule income test)",
        "name_he": "הכנסה נמוכה (מבחן הכנסה)",
        "kind": "ceiling",
        "basis": "Reg. 2(a)(8) and the First Schedule",
        "percentage": 90,
        "max_sqm": None,
        "max_sqm_large_household": None,
        "duration_months": None,
        "description": "Banded by average monthly household income and household size: up to 90%, 70%, 50%, or 30%. Pass --household-income, --household-size and --fiscal-year and the script picks the band from the First Schedule for that year; without them it applies the TOP band. Thresholds update every 1 January by the change in the minimum wage",
    },
    "righteous-gentile": {
        "name": "Righteous Among the Nations",
        "name_he": "חסיד אומות העולם",
        "kind": "ceiling",
        "basis": "Reg. 2(a)(9)",
        "percentage": 66,
        "max_sqm": None,
        "max_sqm_large_household": None,
        "duration_months": None,
        "description": "Up to 66% for a person recognised as Righteous Among the Nations by Yad Vashem, and their spouse or former spouse, resident in Israel; no area cap stated",
    },
    "single-parent": {
        "name": "Single parent",
        "name_he": "הורה יחיד",
        "kind": "ceiling",
        "basis": "Reg. 2(a)(10)",
        "percentage": 20,
        "max_sqm": None,
        "max_sqm_large_household": None,
        "duration_months": None,
        "description": "Up to 20% for a single parent as defined in the Single-Parent Families Law 5752-1992, or a single parent of a co-resident child aged 21 or under serving in conscript or national service; no area cap stated",
    },
    "disabled-child-parent": {
        "name": "Parent of a child entitled to the disabled-child benefit",
        "name_he": "הורה לילד נכה",
        "kind": "ceiling",
        "basis": "Reg. 2(a)(11); per-child computation, Arrangements Law 5753-1992 s.12(g)",
        "percentage": 33,
        "max_sqm": 100,
        "max_sqm_large_household": None,
        "duration_months": None,
        "description": "Up to 33% on 100 sqm where a child of the holder, including a foster child, is entitled to a benefit under the National Insurance (Disabled Child) Regulations 5770-2010, or is over 18 and receives a disability benefit. Arrangements Law 5753-1992 s.12(g) computes the discount for EACH entitled child, including one over 18 who never received the disabled-child benefit, with a combined ceiling of 90%; pass --entitled-children",
    },
    "released-captive": {
        "name": "Released captive (pdui shevi)",
        "name_he": "פדוי שבי",
        "kind": "ceiling",
        "basis": "Reg. 2(a)(12)",
        "percentage": 20,
        "max_sqm": None,
        "max_sqm_large_household": None,
        "duration_months": None,
        "description": "Up to 20% for a person entitled to payment under the Payments to Released Captives Law 5765-2005; no area cap stated",
    },
    "miluim": {
        "name": "Active reserve soldier",
        "name_he": "חייל מילואים פעיל",
        "kind": "ceiling",
        "basis": "Reg. 3f",
        "percentage": 5,
        "max_sqm": None,
        "max_sqm_large_household": None,
        "duration_months": None,
        "description": "Up to 5% for a holder of a valid active-reservist certificate, or a valid IDF confirmation of active reserve service; no area cap stated",
    },
    "miluim-commander": {
        "name": "Active reserve commander",
        "name_he": "מפקד מילואים פעיל",
        "kind": "ceiling",
        "basis": "Reg. 3g",
        "percentage": 25,
        "max_sqm": 100,
        "max_sqm_large_household": None,
        "duration_months": None,
        "description": "Up to 25% on 100 sqm for a reservist serving in a command role as defined in army orders, holding a valid active-reserve-commander certificate or IDF confirmation, or notified to the municipality by the IDF",
    },
    "nazak": {
        "name": "Needy holder (nazak), discounts committee",
        "name_he": "נזקק (ועדת הנחות)",
        "kind": "ceiling",
        "basis": "Reg. 7",
        "percentage": 70,
        "max_sqm": None,
        "max_sqm_large_household": None,
        "duration_months": None,
        "description": "Up to 70% granted by the discounts committee to a holder who incurred exceptionally high expenses from one-off or ongoing medical treatment, for themselves or a family member, or who suffered an event causing a serious unforeseen worsening of their material position",
    },
}


# ============================================================
# Lookup
# ============================================================

_LATIN_TO_HEBREW = {
    "A": "א", "ALEF": "א", "B": "ב", "BET": "ב", "G": "ג", "C": "ג", "GIMEL": "ג",
    "D": "ד", "DALET": "ד", "E": "ה", "HEH": "ה", "HE": "ה", "F": "ו", "VAV": "ו",
    "Z": "ז", "ZAYIN": "ז", "A+": "א+", "NEW": "new",
}


def normalize_code(code: str) -> str:
    """Normalise a zone or type code: strip geresh/quotes/spaces, map Latin letter names."""
    code = code.strip().replace("'", "").replace("׳", "").replace('"', "").replace(" ", "")
    upper = code.upper()
    if upper in _LATIN_TO_HEBREW:
        return _LATIN_TO_HEBREW[upper]
    # Haifa's מ-2 / M2 style class codes
    for prefix in ("מ-", "מ", "M-", "M"):
        if upper.startswith(prefix.upper()) and upper[len(prefix):].isdigit():
            return upper[len(prefix):]
    if code.lower().endswith("/villa"):
        return normalize_code(code[: -len("/villa")]) + "/villa"
    return code


def _fits(area: float, lo: Optional[float], hi: Optional[float]) -> bool:
    return (lo is None or area > lo) and (hi is None or area <= hi)


def annual_for(area: float, rate) -> float:
    """Annual base for a flat or marginal rate."""
    if isinstance(rate, list):
        total, done = 0.0, 0.0
        for up_to, r in rate:
            slice_end = area if up_to is None else min(area, up_to)
            if slice_end > done:
                total += (slice_end - done) * r
                done = slice_end
        return total
    return area * rate


def describe_rate(rate) -> str:
    if isinstance(rate, list):
        parts = []
        prev = 0
        for up_to, r in rate:
            parts.append(f"{r:.2f} for sqm {prev + 1}-{up_to}" if up_to else f"{r:.2f} above {prev}")
            prev = up_to or prev
        return "marginal: " + ", ".join(parts)
    return f"{rate:.2f}"


def find_rows(municipality: str, zone: Optional[str], typ: Optional[str], area: float):
    muni = RATE_TABLES[municipality]
    zones = sorted({r[0] for r in muni["rows"]})
    if zone is None:
        if len(zones) == 1:
            zone = zones[0]
        else:
            raise ValueError(f"--zone is required for {muni['name']} ({muni['zone_system']}): {', '.join(zones)}")
    zone = normalize_code(zone)
    if zone not in zones:
        raise ValueError(f"Zone '{zone}' not valid for {muni['name']} ({muni['zone_system']}): {', '.join(zones)}")
    rows = [r for r in muni["rows"] if r[0] == zone and _fits(area, r[2], r[3])]
    if typ is not None:
        typ = normalize_code(typ)
        rows = [r for r in rows if r[1] == typ]
        if not rows:
            types = sorted({r[1] for r in muni["rows"] if r[0] == zone})
            raise ValueError(
                f"Type '{typ}' has no {muni['name']} rate in zone {zone} for {area:g} sqm. "
                f"Types in this zone: {', '.join(types)} (run --list-types {municipality})"
            )
    return zone, rows


# ============================================================
# Calculation
# ============================================================


@dataclass
class ArnonaResult:
    municipality: str
    municipality_name: str
    zone: str
    building_type: str
    usage: str
    area_sqm: float
    rate_desc: str
    annual_base: float
    discount_type: Optional[str] = None
    discount_percentage: float = 0.0
    discount_area_sqm: float = 0.0
    effective_max_sqm: Optional[float] = None
    annual_discounted: float = 0.0
    annual_after_discount: float = 0.0
    discount_months: Optional[int] = None
    effective_annual: float = 0.0
    projected_2027_base: Optional[float] = None
    notes: List[str] = field(default_factory=list)


def resolve_discount(discount_type, usage, override, household_size, household_income, fiscal_year, entitled_children):
    """Return (percentage, notes) for a discount key, or (0, notes) when the income test fails."""
    disc = DISCOUNTS[discount_type]
    notes = []
    pct = disc["percentage"]
    if discount_type == "gaza-envelope" and usage != "residential":
        pct = disc["percentage_non_residential"]
    if discount_type == "gaza-envelope" and fiscal_year > 2026:
        notes.append("Reg. 3c covers fiscal years 2015 to 2026 only. No extension to 2027 had been published as of "
                     "October 2026; this figure assumes one (past extensions came late and applied retroactively).")
    if entitled_children is not None and entitled_children < 1:
        raise ValueError("--entitled-children must be 1 or more")
    if discount_type == "disabled-child-parent" and entitled_children:
        pct = min(disc["percentage"] * entitled_children, 90)
        notes.append(f"{entitled_children} entitled children x {disc['percentage']}%, combined ceiling 90% (Arrangements Law s.12(g)).")
    if discount_type == "low-income" and household_income is not None:
        if not household_size:
            raise ValueError("--household-size is required with --household-income")
        band, bounds = income_band(fiscal_year, household_size, household_income)
        notes.append(
            f"First Schedule for fiscal {fiscal_year} (tests calendar-{fiscal_year - 1} income), {household_size} persons: "
            f"90% up to {bounds[0]:,}, 70% up to {bounds[1]:,}, 50% up to {bounds[2]:,}, 30% up to {bounds[3]:,}."
        )
        if band is None:
            notes.append(f"Average monthly income {household_income:,.0f} is above the 30% band upper bound of {bounds[3]:,} "
                         f"for {household_size} persons: no income-test discount. Check the other rows, and the "
                         "needy-holder route (nazak, Reg. 7) where exceptional medical costs or a sudden worsening apply.")
            pct = 0
        else:
            notes.append(f"Average monthly income {household_income:,.0f} falls in the up-to-{band}% band.")
            pct = band
    if override is not None:
        pct = override
        notes.append(f"Percentage overridden to {override:g}% (--discount-percentage).")
    return pct, notes


def calculate(municipality, municipality_name, zone, building_type, usage, area, rate,
              discount_type=None, discount_pct=0.0, discount_months=None, household_size=None,
              notes=None, fiscal_year=TZAV_YEAR, user_rate=False) -> ArnonaResult:
    # A built-in fiscal-2026 rate projected forward when the user asks about a
    # later fiscal year; a rate the user supplied is taken as already current.
    factor = 1.0
    notes = list(notes or [])
    if fiscal_year > TZAV_YEAR and not user_rate:
        for year in range(TZAV_YEAR + 1, fiscal_year + 1):
            factor *= 1 + NATIONAL_UPDATE_COEFFICIENT_PCT[year] / 100
        notes.append(f"Fiscal {fiscal_year}: the fiscal-{TZAV_YEAR} tzav rate is projected forward at the national update "
                     f"({NATIONAL_UPDATE_COEFFICIENT_PCT[fiscal_year]}%). Wrong for a council that obtained an above-formula "
                     f"increase; use the fiscal-{fiscal_year} tzav or bill with --rate-per-sqm once published.")
    base = annual_for(area, rate) * factor
    res = ArnonaResult(municipality, municipality_name, zone, building_type, usage, area,
                       describe_rate(rate) + (f" x {factor:.4f}" if factor != 1.0 else ""), base, notes=notes)
    res.annual_after_discount = base
    if discount_type:
        disc = DISCOUNTS[discount_type]
        max_sqm = disc["max_sqm"]
        # Reg. 14f and Reg. 2(a)(4) raise the cap when "more than four" family
        # members live with the holder. Kol Zchut and Jerusalem's 2026 tzav
        # ("a family of 5 or more") read that as five or more people, and that
        # is the reading applied here; a council
        # that reads it as five besides the holder will cap a five-person
        # household at 70 sqm.
        if disc.get("max_sqm_large_household") and household_size is not None and household_size >= 5:
            max_sqm = disc["max_sqm_large_household"]
            if household_size == 5:
                res.notes.append("90 sqm cap applied to a five-person household (the reading of Kol Zchut and Jerusalem's 2026 tzav "
                                 "of 'more than four family members'); a council reading it as five besides the holder applies 70 sqm.")
        disc_area = area if max_sqm is None else min(area, max_sqm)
        # Discount the CAPPED area at the flat's average rate. For a marginal
        # rate this takes the average across the whole flat, which is an
        # approximation: the regulation does not say which metres are capped.
        avg_rate = base / area
        res.discount_type = discount_type
        res.discount_percentage = discount_pct
        res.discount_area_sqm = disc_area
        res.effective_max_sqm = max_sqm
        res.annual_discounted = disc_area * avg_rate * discount_pct / 100
        res.annual_after_discount = base - res.annual_discounted
        if isinstance(rate, list) and max_sqm is not None and area > max_sqm:
            first_metres = annual_for(disc_area, rate) * factor * discount_pct / 100
            res.notes.append(
                f"Marginal rate with an area cap: the saving above prices the {disc_area:g} discounted sqm at the flat's "
                f"average rate. If the council discounts the FIRST {disc_area:g} sqm instead, the saving is "
                f"{first_metres:,.2f} NIS. The regulation does not say which metres; ask the council.")
    res.discount_months = discount_months
    if discount_type and discount_months is not None and discount_months < 12:
        res.effective_annual = (res.annual_after_discount * discount_months + base * (12 - discount_months)) / 12
    else:
        res.effective_annual = res.annual_after_discount
    if usage == "residential" and municipality in RATE_TABLES and not user_rate and fiscal_year == TZAV_YEAR:
        res.projected_2027_base = base * (1 + NATIONAL_UPDATE_COEFFICIENT_PCT[2027] / 100)
    return res


# ============================================================
# Output
# ============================================================


def format_result(res: ArnonaResult, source: str) -> str:
    lines = [
        "=" * 64, "ARNONA CALCULATION REPORT", "=" * 64, "",
        f"Municipality:    {res.municipality_name}",
        f"Zone:            {res.zone}",
        f"Building type:   {res.building_type}",
        f"Usage:           {res.usage}",
        f"Area:            {res.area_sqm:g} sqm",
        f"Rate per sqm:    {res.rate_desc} NIS/year",
        "",
        f"Annual base arnona:   {res.annual_base:,.2f} NIS",
    ]
    if res.discount_type:
        disc = DISCOUNTS[res.discount_type]
        cap = f"cap {res.effective_max_sqm:.0f} sqm" if res.effective_max_sqm else "no area cap in the regulation"
        lines += [
            "", f"Discount:             {disc['name']} ({disc['basis']})",
            f"Legal shape:          {'ENTITLEMENT, no council discretion' if disc['kind'] == 'entitlement' else 'CEILING, the council may set anything up to this'}",
            f"Rate applied:         {res.discount_percentage:g}% on {res.discount_area_sqm:g} sqm ({cap})",
            f"Annual saving:        {res.annual_discounted:,.2f} NIS",
            f"Annual after discount: {res.annual_after_discount:,.2f} NIS",
        ]
        if res.discount_months is not None and res.discount_months < 12:
            lines.append(f"Discount months in this year: {res.discount_months} of 12")
    lines += [
        "", f"Effective annual total: {res.effective_annual:,.2f} NIS",
        f"Bimonthly (one of 6):   {res.effective_annual / 6:,.2f} NIS",
        f"Monthly equivalent:     {res.effective_annual / 12:,.2f} NIS",
    ]
    if res.projected_2027_base is not None:
        lines += ["", f"2027 projection of the base at the {NATIONAL_UPDATE_COEFFICIENT_PCT[2027]}% national update: "
                      f"{res.projected_2027_base:,.2f} NIS (not valid where the council obtained an above-formula increase)"]
    if res.notes:
        lines += ["", "Notes:"] + [f"  - {n}" for n in res.notes]
    lines += [
        "", "-" * 64,
        (f"Rates: fiscal {TZAV_YEAR} tzav arnona. Source: {source}" if source.startswith("http") else f"Rate: {source}."),
        "The bill is authoritative. It shows your zone, type and charged area; if any of",
        "them differs from what you entered, recompute with the bill's values.",
        "=" * 64,
    ]
    return "\n".join(lines)


def result_dict(res: ArnonaResult) -> dict:
    return {
        "municipality": res.municipality, "zone": res.zone, "building_type": res.building_type,
        "usage": res.usage, "area_sqm": res.area_sqm, "rate_per_sqm": res.rate_desc,
        "annual_base_nis": round(res.annual_base, 2),
        "discount": None if not res.discount_type else {
            "type": res.discount_type, "percentage": res.discount_percentage,
            "discount_area_sqm": res.discount_area_sqm,
            "annual_savings_nis": round(res.annual_discounted, 2),
            "months": res.discount_months,
        },
        "effective_annual_nis": round(res.effective_annual, 2),
        "bimonthly_nis": round(res.effective_annual / 6, 2),
        "projected_2027_base_nis": None if res.projected_2027_base is None else round(res.projected_2027_base, 2),
        "notes": res.notes,
    }


def list_municipalities():
    print(f"Residential rates from the fiscal-{TZAV_YEAR} tzav arnona:")
    print("-" * 64)
    for key in sorted(RATE_TABLES):
        m = RATE_TABLES[key]
        rates = []
        for r in m["rows"]:
            rates += [x[1] for x in r[4]] if isinstance(r[4], list) else [r[4]]
        print(f"  {key:15s} {m['name']:32s} {min(rates):.2f}-{max(rates):.2f} NIS/sqm")
        print(f"  {'':15s} {m['zone_system']}")
    print()
    print("Any other authority, or any non-residential property: pass --rate-per-sqm from")
    print("the tzav or the bill, with --municipality other.")


def list_types(municipality: str):
    m = RATE_TABLES[municipality]
    print(f"{m['name']}: {m['zone_system']}")
    print("Types (read yours off the bill):")
    for code, desc in m["types"].items():
        print(f"  {code:14s} {desc}")
    for n in m["notes"]:
        print(f"Note: {n if isinstance(n, str) else n[1]}")
    print(f"Source: {m['source']}")


def list_discounts():
    print("ENTITLEMENT = the council has no discretion. CEILING = the council MAY set up to this.")
    for kind in ("entitlement", "ceiling"):
        print(f"\n== {kind.upper()} ==\n")
        for key in sorted(k for k, v in DISCOUNTS.items() if v["kind"] == kind):
            d = DISCOUNTS[key]
            cap = f"{d['max_sqm']:.0f} sqm cap" if d["max_sqm"] else "no area cap"
            if d["max_sqm_large_household"]:
                cap += f" ({d['max_sqm_large_household']:.0f} sqm if >4 family members)"
            duration = f"{d['duration_months']} months" if d["duration_months"] else "ongoing"
            print(f"  {key:24s} {d['percentage']:>6}%  {cap}  {duration}")
            print(f"  {'':24s} {d['basis']}")
            print(f"  {'':24s} {d['description']}\n")
    print("NOT PRESENT, deliberately: student and large-family discounts have no paragraph")
    print("in the national regulation. A municipality may grant one under its own bylaw.")


def main():
    parser = argparse.ArgumentParser(
        description="Israeli Arnona (Municipal Property Tax) Calculator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -m tel-aviv -a 85 -z 2 --type ב+ג
  %(prog)s -m jerusalem -a 70 -z ב --type 2 --discount oleh
  %(prog)s -m haifa -a 90 -z ב --type 2 --discount low-income --household-income 9000 --household-size 3 --fiscal-year 2027
  %(prog)s -m other -a 60 --rate-per-sqm 150 --usage commercial
  %(prog)s --list-types haifa
        """,
    )
    parser.add_argument("--municipality", "-m", help="Municipality key (see --list-municipalities), or 'other' with --rate-per-sqm")
    parser.add_argument("--area", "-a", type=float, help="Charged area in sqm, as on the bill")
    parser.add_argument("--zone", "-z", help="Zone as printed on the bill (e.g. 2, ב, B)")
    parser.add_argument("--type", "-t", dest="building_type",
                        help="Building type or class as printed on the bill. Omit it to see every type that fits the zone and area")
    parser.add_argument("--usage", "-u", default="residential",
                        choices=["residential", "commercial", "office", "industrial", "other"],
                        help="Property use (default residential). Non-residential needs --rate-per-sqm")
    parser.add_argument("--rate-per-sqm", type=float,
                        help="Use this NIS/sqm/year rate instead of the built-in table (any authority, any use)")
    parser.add_argument("--discount", "-d", help="Discount key; run --list-discounts")
    parser.add_argument("--discount-months", type=int, help="How many months of this fiscal year the discount covers (default 12)")
    parser.add_argument("--household-size", type=int,
                        help="People living in the flat with the holder, holder included. Selects the income-table row and the 90 sqm cap for 5+")
    parser.add_argument("--household-income", type=float,
                        help="Average monthly GROSS income of everyone living in the flat, over the calendar year before the fiscal year")
    parser.add_argument("--fiscal-year", type=int, choices=sorted(INCOME_TABLE), default=TZAV_YEAR,
                        help="Fiscal year (default 2026). Picks the income table; for 2027 the built-in 2026 rates are projected at the 3.05%% national update")
    parser.add_argument("--entitled-children", type=int,
                        help="With disabled-child-parent: number of children for whom the disability benefit is paid")
    parser.add_argument("--discount-percentage", type=float,
                        help="Override the percentage, e.g. to model a council that set less than the ceiling")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--list-municipalities", action="store_true")
    parser.add_argument("--list-types", metavar="MUNICIPALITY")
    parser.add_argument("--list-discounts", action="store_true")
    args = parser.parse_args()

    if args.list_municipalities:
        return list_municipalities()
    if args.list_types:
        if args.list_types not in RATE_TABLES:
            parser.error(f"unknown municipality '{args.list_types}'")
        return list_types(args.list_types)
    if args.list_discounts:
        return list_discounts()

    if not args.municipality or not args.area:
        parser.error("--municipality and --area are required")
    if args.area <= 0:
        parser.error("--area must be positive")
    if args.household_size is not None and args.household_size < 1:
        parser.error("--household-size must be 1 or more")
    # Arrangements Law s.8(b1)(2): any part of a sqm rounds to the nearest whole
    # metre, and exactly half a metre rounds DOWN. Done before band selection,
    # because a band edge (75, 100, 140 ...) decides the rate of the whole flat.
    # s.8(b1)(3) lets a council keep a different method; Jerusalem charges the
    # area to two decimal places, so its area is used as given.
    whole, frac = divmod(args.area, 1)
    rounded = whole + (1 if frac > 0.5 else 0)
    if rounded != args.area and args.municipality.lower().strip() != "jerusalem":
        print(f"Note: area {args.area:g} sqm rounded to {rounded:g} sqm (Arrangements Law s.8(b1)(2)). "
              "A council using a different method under s.8(b1)(3) charges otherwise; the bill's area governs.", file=sys.stderr)
        args.area = rounded
    if args.area <= 0:
        parser.error("--area rounds to 0 sqm")
    municipality = args.municipality.lower().strip()
    if args.discount:
        args.discount = args.discount.lower().strip()
        if args.discount not in DISCOUNTS:
            parser.error(f"unknown discount '{args.discount}'; run --list-discounts")
    if args.discount_months is not None and not 0 <= args.discount_months <= 12:
        parser.error("--discount-months must be between 0 and 12")

    try:
        pct, disc_notes = (0.0, [])
        if args.discount:
            pct, disc_notes = resolve_discount(args.discount, args.usage, args.discount_percentage,
                                               args.household_size, args.household_income,
                                               args.fiscal_year, args.entitled_children)
        if args.rate_per_sqm is not None:
            candidates = [(args.zone or "-", args.building_type or "-", args.rate_per_sqm,
                           RATE_TABLES.get(municipality, {}).get("name", municipality), "rate supplied by the user")]
        else:
            if municipality not in RATE_TABLES:
                parser.error(f"'{municipality}' has no built-in table; pass --rate-per-sqm from its tzav or bill")
            if args.usage != "residential":
                parser.error("built-in tables are residential only; pass --rate-per-sqm for other uses")
            zone, rows = find_rows(municipality, args.zone, args.building_type, args.area)
            if not rows:
                raise ValueError(f"No {RATE_TABLES[municipality]['name']} row fits zone {zone} and {args.area:g} sqm")
            m = RATE_TABLES[municipality]
            candidates = [(zone, r[1] + (f" ({r[5]})" if len(r) > 5 else ""), r[4], m["name"], m["source"]) for r in rows]
            # A note is either plain text or (zone, text) when it concerns one zone only.
            disc_notes = disc_notes + [n if isinstance(n, str) else n[1] for n in m["notes"]
                                       if isinstance(n, str) or n[0] == zone]
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    results = [
        (calculate(municipality, name, zone, typ, args.usage, args.area, rate, args.discount, pct,
                   args.discount_months, args.household_size, disc_notes, args.fiscal_year,
                   user_rate=args.rate_per_sqm is not None), source)
        for zone, typ, rate, name, source in candidates
    ]

    if args.json:
        print(json.dumps([result_dict(r) for r, _ in results] if len(results) > 1 else result_dict(results[0][0]),
                         indent=2, ensure_ascii=False))
        return
    if len(results) == 1:
        print(format_result(*results[0]))
        return
    lo = min(r.effective_annual for r, _ in results)
    hi = max(r.effective_annual for r, _ in results)
    print(f"No single rate: {len(results)} rows of the {results[0][0].municipality_name} tzav fit zone "
          f"{results[0][0].zone} and {args.area:g} sqm. Annual total ranges {lo:,.2f} to {hi:,.2f} NIS.")
    print("Pass --type with the type printed on the bill. Candidates:")
    for r, _ in results:
        print(f"  type {r.building_type:12s} rate {r.rate_desc:>40s}  annual {r.effective_annual:>11,.2f} NIS")
    for n in results[0][0].notes:
        print(f"Note: {n}")
    print(f"Source: {results[0][1]}")


if __name__ == "__main__":
    main()
