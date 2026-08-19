#!/usr/bin/env python3
"""
Israeli Arnona (Municipal Property Tax) Calculator

Calculates annual and bimonthly arnona payments based on municipality,
property area, zone classification, and usage type. Supports discount
calculations for eligible populations.

Usage:
    python arnona-calculator.py --municipality "tel-aviv" --area 80 --zone 2 --usage residential
    python arnona-calculator.py --municipality "jerusalem" --area 70 --zone B --usage residential --discount oleh --discount-months 12
    python arnona-calculator.py --list-municipalities
    python arnona-calculator.py --list-discounts

Requirements:
    Python 3.8+
    No external dependencies
"""

import argparse
import json
import sys
from dataclasses import dataclass
from typing import Optional


# ============================================================
# Rate Tables (approximate, based on recent tzav arnona data)
# ============================================================

# Structure: municipality -> zone -> usage_type -> rate_per_sqm_per_year (NIS)
RATE_TABLES = {
    "tel-aviv": {
        "name": "Tel Aviv-Yafo",
        "zone_system": "numbered (1-4)",
        "zones": {
            "1": {
                "residential": 125.0,
                "commercial": 400.0,
                "office": 320.0,
                "industrial": 180.0,
            },
            "2": {
                "residential": 95.0,
                "commercial": 310.0,
                "office": 250.0,
                "industrial": 150.0,
            },
            "3": {
                "residential": 80.0,
                "commercial": 240.0,
                "office": 190.0,
                "industrial": 120.0,
            },
            "4": {
                "residential": 70.0,
                "commercial": 175.0,
                "office": 140.0,
                "industrial": 95.0,
            },
        },
    },
    "jerusalem": {
        "name": "Jerusalem",
        "zone_system": "Hebrew letters (alef-heh / A-E)",
        "zones": {
            "A": {
                "residential": 90.0,
                "commercial": 280.0,
                "office": 220.0,
                "industrial": 130.0,
            },
            "B": {
                "residential": 72.0,
                "commercial": 220.0,
                "office": 175.0,
                "industrial": 105.0,
            },
            "C": {
                "residential": 65.0,
                "commercial": 180.0,
                "office": 140.0,
                "industrial": 90.0,
            },
            "D": {
                "residential": 55.0,
                "commercial": 140.0,
                "office": 110.0,
                "industrial": 75.0,
            },
            "E": {
                "residential": 48.0,
                "commercial": 110.0,
                "office": 85.0,
                "industrial": 60.0,
            },
        },
    },
    "haifa": {
        "name": "Haifa",
        "zone_system": "lettered (A-D)",
        "zones": {
            "A": {
                "residential": 85.0,
                "commercial": 260.0,
                "office": 200.0,
                "industrial": 120.0,
            },
            "B": {
                "residential": 70.0,
                "commercial": 200.0,
                "office": 155.0,
                "industrial": 95.0,
            },
            "C": {
                "residential": 55.0,
                "commercial": 155.0,
                "office": 120.0,
                "industrial": 75.0,
            },
            "D": {
                "residential": 45.0,
                "commercial": 110.0,
                "office": 85.0,
                "industrial": 55.0,
            },
        },
    },
    "beer-sheva": {
        "name": "Beer Sheva",
        "zone_system": "numbered (1-3)",
        "zones": {
            "1": {
                "residential": 55.0,
                "commercial": 170.0,
                "office": 130.0,
                "industrial": 80.0,
            },
            "2": {
                "residential": 45.0,
                "commercial": 130.0,
                "office": 100.0,
                "industrial": 65.0,
            },
            "3": {
                "residential": 37.0,
                "commercial": 100.0,
                "office": 80.0,
                "industrial": 50.0,
            },
        },
    },
    "netanya": {
        "name": "Netanya",
        "zone_system": "numbered (1-3)",
        "zones": {
            "1": {
                "residential": 82.0,
                "commercial": 250.0,
                "office": 195.0,
                "industrial": 110.0,
            },
            "2": {
                "residential": 68.0,
                "commercial": 195.0,
                "office": 150.0,
                "industrial": 90.0,
            },
            "3": {
                "residential": 56.0,
                "commercial": 150.0,
                "office": 115.0,
                "industrial": 70.0,
            },
        },
    },
    "rishon-lezion": {
        "name": "Rishon LeZion",
        "zone_system": "lettered (A-D)",
        "zones": {
            "A": {
                "residential": 88.0,
                "commercial": 270.0,
                "office": 210.0,
                "industrial": 125.0,
            },
            "B": {
                "residential": 74.0,
                "commercial": 215.0,
                "office": 170.0,
                "industrial": 100.0,
            },
            "C": {
                "residential": 65.0,
                "commercial": 175.0,
                "office": 135.0,
                "industrial": 85.0,
            },
            "D": {
                "residential": 58.0,
                "commercial": 140.0,
                "office": 110.0,
                "industrial": 70.0,
            },
        },
    },
    "petah-tikva": {
        "name": "Petah Tikva",
        "zone_system": "numbered (1-3)",
        "zones": {
            "1": {
                "residential": 78.0,
                "commercial": 240.0,
                "office": 185.0,
                "industrial": 105.0,
            },
            "2": {
                "residential": 65.0,
                "commercial": 185.0,
                "office": 145.0,
                "industrial": 85.0,
            },
            "3": {
                "residential": 55.0,
                "commercial": 145.0,
                "office": 110.0,
                "industrial": 70.0,
            },
        },
    },
    "ashdod": {
        "name": "Ashdod",
        "zone_system": "numbered (1-3)",
        "zones": {
            "1": {
                "residential": 68.0,
                "commercial": 210.0,
                "office": 160.0,
                "industrial": 95.0,
            },
            "2": {
                "residential": 55.0,
                "commercial": 165.0,
                "office": 125.0,
                "industrial": 78.0,
            },
            "3": {
                "residential": 46.0,
                "commercial": 130.0,
                "office": 100.0,
                "industrial": 62.0,
            },
        },
    },
    "herzliya": {
        "name": "Herzliya",
        "zone_system": "lettered (A-C)",
        "zones": {
            "A": {
                "residential": 108.0,
                "commercial": 340.0,
                "office": 265.0,
                "industrial": 150.0,
            },
            "B": {
                "residential": 88.0,
                "commercial": 270.0,
                "office": 210.0,
                "industrial": 120.0,
            },
            "C": {
                "residential": 72.0,
                "commercial": 210.0,
                "office": 165.0,
                "industrial": 95.0,
            },
        },
    },
    "raanana": {
        "name": "Ra'anana",
        "zone_system": "lettered (A-C)",
        "zones": {
            "A": {
                "residential": 102.0,
                "commercial": 320.0,
                "office": 250.0,
                "industrial": 140.0,
            },
            "B": {
                "residential": 85.0,
                "commercial": 255.0,
                "office": 200.0,
                "industrial": 115.0,
            },
            "C": {
                "residential": 74.0,
                "commercial": 210.0,
                "office": 160.0,
                "industrial": 95.0,
            },
        },
    },
    "ramat-gan": {
        "name": "Ramat Gan",
        "zone_system": "lettered (A-D)",
        "zones": {
            "A": {
                "residential": 98.0,
                "commercial": 310.0,
                "office": 240.0,
                "industrial": 135.0,
            },
            "B": {
                "residential": 82.0,
                "commercial": 245.0,
                "office": 190.0,
                "industrial": 110.0,
            },
            "C": {
                "residential": 72.0,
                "commercial": 200.0,
                "office": 155.0,
                "industrial": 90.0,
            },
            "D": {
                "residential": 65.0,
                "commercial": 165.0,
                "office": 125.0,
                "industrial": 75.0,
            },
        },
    },
    "modiin": {
        "name": "Modi'in-Maccabim-Re'ut",
        "zone_system": "numbered (1-3)",
        "zones": {
            "1": {
                "residential": 82.0,
                "commercial": 250.0,
                "office": 195.0,
                "industrial": 110.0,
            },
            "2": {
                "residential": 70.0,
                "commercial": 200.0,
                "office": 155.0,
                "industrial": 90.0,
            },
            "3": {
                "residential": 60.0,
                "commercial": 160.0,
                "office": 125.0,
                "industrial": 75.0,
            },
        },
    },
}

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
        "description": "45% entitlement on residential property (39% on other property, which this key does not model) for fiscal years 2015 to 2026, for a property in the Gaza-envelope localities or within 7 km of the Gaza perimeter fence",
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
        "description": "100% entitlement on 100 sqm where the senior receives a benefit under the Income Support Law 5741-1980. This is the statutory route; Reg. 2(a)(1)(b) is the parallel discretionary ceiling",
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
        "description": "Banded by average monthly household income and household size: up to 90%, 70%, 50%, or 30%. This key applies the TOP band; pass --discount-percentage to model a lower band. Thresholds update every 1 January by the change in the minimum wage",
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
        "basis": "Reg. 2(a)(11)",
        "percentage": 33,
        "max_sqm": 100,
        "max_sqm_large_household": None,
        "duration_months": None,
        "description": "Up to 33% on 100 sqm where a child of the holder, including a foster child, is entitled to a benefit under the National Insurance (Disabled Child) Regulations 5770-2010, or is over 18 and receives a disability benefit that was preceded by the disabled-child benefit",
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


@dataclass
class ArnonaResult:
    municipality: str
    municipality_name: str
    zone: str
    usage: str
    area_sqm: float
    rate_per_sqm: float
    annual_base: float
    discount_type: Optional[str]
    discount_percentage: float
    discount_area_sqm: float
    full_rate_area_sqm: float
    effective_max_sqm: Optional[float]
    annual_discounted: float
    annual_after_discount: float
    bimonthly_payment: float
    monthly_equivalent: float
    discount_months: Optional[int]
    prorated_annual: Optional[float]


def normalize_zone(zone: str) -> str:
    """Normalize zone input to match rate table keys."""
    zone = zone.strip().upper()

    # Map Hebrew letters to English equivalents
    hebrew_map = {
        "ALEF": "A", "BET": "B", "GIMEL": "C", "DALET": "D", "HEH": "E",
        "A": "A", "B": "B", "C": "C", "D": "D", "E": "E",
    }

    if zone in hebrew_map:
        return hebrew_map[zone]

    # Try as number
    try:
        return str(int(zone))
    except ValueError:
        pass

    return zone


def calculate_arnona(
    municipality: str,
    area_sqm: float,
    zone: str,
    usage: str = "residential",
    discount_type: Optional[str] = None,
    discount_months: Optional[int] = None,
    household_size: Optional[int] = None,
    discount_percentage_override: Optional[float] = None,
) -> ArnonaResult:
    """Calculate arnona for the given parameters."""

    municipality = municipality.lower().strip()
    usage = usage.lower().strip()
    zone = normalize_zone(zone)

    if municipality not in RATE_TABLES:
        available = ", ".join(sorted(RATE_TABLES.keys()))
        print(f"Error: Municipality '{municipality}' not found in rate tables.", file=sys.stderr)
        print(f"Available municipalities: {available}", file=sys.stderr)
        sys.exit(1)

    muni_data = RATE_TABLES[municipality]

    if zone not in muni_data["zones"]:
        available = ", ".join(sorted(muni_data["zones"].keys()))
        print(
            f"Error: Zone '{zone}' not valid for {muni_data['name']}.",
            file=sys.stderr,
        )
        print(f"Available zones ({muni_data['zone_system']}): {available}", file=sys.stderr)
        sys.exit(1)

    zone_rates = muni_data["zones"][zone]

    if usage not in zone_rates:
        available = ", ".join(sorted(zone_rates.keys()))
        print(f"Error: Usage type '{usage}' not found.", file=sys.stderr)
        print(f"Available types: {available}", file=sys.stderr)
        sys.exit(1)

    rate = zone_rates[usage]
    annual_base = area_sqm * rate

    # Calculate discount
    discount_percentage = 0.0
    discount_area = 0.0
    full_rate_area = area_sqm
    annual_discounted = 0.0
    effective_max_sqm = None

    if discount_type:
        discount_type = discount_type.lower().strip()
        if discount_type not in DISCOUNTS:
            available = ", ".join(sorted(DISCOUNTS.keys()))
            print(f"Error: Discount category '{discount_type}' not recognized.", file=sys.stderr)
            print(f"Available discounts: {available}", file=sys.stderr)
            sys.exit(1)

        disc = DISCOUNTS[discount_type]
        discount_percentage = (
            discount_percentage_override
            if discount_percentage_override is not None
            else disc["percentage"]
        )

        # The area cap is per-row, and several rows have none at all. A row that
        # rises for a larger household does so only when MORE THAN FOUR family
        # members live with the holder (Reg. 14f), i.e. a household of six or more.
        max_sqm = disc["max_sqm"]
        if (
            disc.get("max_sqm_large_household")
            and household_size is not None
            and household_size >= 6
        ):
            max_sqm = disc["max_sqm_large_household"]

        # Split area into discounted and full-rate portions
        if max_sqm is None:
            discount_area = area_sqm
            full_rate_area = 0.0
        else:
            discount_area = min(area_sqm, max_sqm)
            full_rate_area = max(0.0, area_sqm - max_sqm)
        effective_max_sqm = max_sqm

        discounted_portion = discount_area * rate * (discount_percentage / 100)
        annual_discounted = discounted_portion

    annual_after_discount = annual_base - annual_discounted

    # Prorate if discount is time-limited
    prorated_annual = None
    if discount_months and discount_months < 12:
        months_with_discount = discount_months
        months_without = 12 - months_with_discount
        prorated_annual = (
            (annual_after_discount * months_with_discount / 12)
            + (annual_base * months_without / 12)
        )

    effective_annual = prorated_annual if prorated_annual is not None else annual_after_discount
    bimonthly = effective_annual / 6
    monthly = effective_annual / 12

    return ArnonaResult(
        municipality=municipality,
        municipality_name=muni_data["name"],
        zone=zone,
        usage=usage,
        area_sqm=area_sqm,
        rate_per_sqm=rate,
        annual_base=annual_base,
        discount_type=discount_type,
        discount_percentage=discount_percentage,
        discount_area_sqm=discount_area,
        full_rate_area_sqm=full_rate_area,
        effective_max_sqm=effective_max_sqm,
        annual_discounted=annual_discounted,
        annual_after_discount=annual_after_discount,
        bimonthly_payment=bimonthly,
        monthly_equivalent=monthly,
        discount_months=discount_months,
        prorated_annual=prorated_annual,
    )


def format_result(result: ArnonaResult) -> str:
    """Format the calculation result as a readable report."""
    lines = [
        "=" * 60,
        "ARNONA CALCULATION REPORT",
        "=" * 60,
        "",
        f"Municipality:    {result.municipality_name}",
        f"Zone:            {result.zone}",
        f"Usage type:      {result.usage}",
        f"Property area:   {result.area_sqm:.1f} sqm",
        f"Rate per sqm:    {result.rate_per_sqm:.2f} NIS/year",
        "",
        "-" * 40,
        "BASE CALCULATION",
        "-" * 40,
        f"Annual base arnona: {result.annual_base:,.2f} NIS",
        "",
    ]

    if result.discount_type:
        disc = DISCOUNTS[result.discount_type]
        lines.extend([
            "-" * 40,
            "DISCOUNT APPLIED",
            "-" * 40,
            f"Discount type:      {disc['name']}",
            f"Discount rate:      {result.discount_percentage:.0f}%",
            f"Discount applies to: {result.discount_area_sqm:.1f} sqm"
            + (f" (cap {result.effective_max_sqm:.0f} sqm)" if result.effective_max_sqm else " (no area cap in the regulation)"),
            f"Legal shape:        {'ENTITLEMENT, the council has no discretion' if disc['kind'] == 'entitlement' else 'CEILING, the council may set anything up to this'} ({disc['basis']})",
        ])

        if result.full_rate_area_sqm > 0:
            lines.append(
                f"Full-rate area:     {result.full_rate_area_sqm:.1f} sqm"
            )

        lines.extend([
            f"Annual savings:     {result.annual_discounted:,.2f} NIS",
            f"Annual after discount: {result.annual_after_discount:,.2f} NIS",
            "",
        ])

        if result.prorated_annual is not None:
            lines.extend([
                "-" * 40,
                "PRORATED CALCULATION",
                "-" * 40,
                f"Discount months remaining: {result.discount_months}",
                f"Full-rate months:          {12 - result.discount_months}",
                f"Prorated annual total:     {result.prorated_annual:,.2f} NIS",
                "",
            ])

    effective = result.prorated_annual if result.prorated_annual else result.annual_after_discount

    lines.extend([
        "-" * 40,
        "PAYMENT SUMMARY",
        "-" * 40,
        f"Effective annual total:  {effective:,.2f} NIS",
        f"Bimonthly payment:       {result.bimonthly_payment:,.2f} NIS",
        f"Monthly equivalent:      {result.monthly_equivalent:,.2f} NIS",
        "",
        "=" * 60,
        "NOTE: These rates are approximate estimates based on recent",
        "municipal rate ordinances. Actual rates may vary. Always",
        "verify with your municipality's official arnona department.",
        "=" * 60,
    ])

    return "\n".join(lines)


def format_result_json(result: ArnonaResult) -> str:
    """Format the result as JSON for programmatic use."""
    data = {
        "municipality": result.municipality,
        "municipality_name": result.municipality_name,
        "zone": result.zone,
        "usage": result.usage,
        "area_sqm": result.area_sqm,
        "rate_per_sqm": result.rate_per_sqm,
        "annual_base_nis": round(result.annual_base, 2),
        "discount": None,
        "effective_annual_nis": round(
            result.prorated_annual
            if result.prorated_annual
            else result.annual_after_discount,
            2,
        ),
        "bimonthly_payment_nis": round(result.bimonthly_payment, 2),
        "monthly_equivalent_nis": round(result.monthly_equivalent, 2),
    }

    if result.discount_type:
        data["discount"] = {
            "type": result.discount_type,
            "percentage": result.discount_percentage,
            "discount_area_sqm": result.discount_area_sqm,
            "annual_savings_nis": round(result.annual_discounted, 2),
        }
        if result.discount_months:
            data["discount"]["remaining_months"] = result.discount_months
            data["discount"]["prorated_annual_nis"] = round(result.prorated_annual, 2) if result.prorated_annual else None

    return json.dumps(data, indent=2, ensure_ascii=False)


def list_municipalities():
    """Print all supported municipalities."""
    print("Supported Municipalities:")
    print("-" * 50)
    for key in sorted(RATE_TABLES.keys()):
        muni = RATE_TABLES[key]
        zones = ", ".join(sorted(muni["zones"].keys()))
        print(f"  {key:20s}  {muni['name']:25s}  Zones: {zones}")
    print()
    print(f"Total: {len(RATE_TABLES)} municipalities")


def list_discounts():
    """Print all supported discount categories."""
    print("Supported Discount Categories:")
    print("-" * 60)
    print("ENTITLEMENT = the council has no discretion, the resident is owed it.")
    print("CEILING     = the council MAY set a discount up to this figure.")
    print("-" * 60)
    for kind in ("entitlement", "ceiling"):
        print(f"\n== {kind.upper()} ==\n")
        for key in sorted(k for k, v in DISCOUNTS.items() if v["kind"] == kind):
            disc = DISCOUNTS[key]
            duration = f"{disc['duration_months']} months" if disc["duration_months"] else "Ongoing"
            cap = f"{disc['max_sqm']:.0f} sqm cap" if disc["max_sqm"] else "no area cap"
            if disc["max_sqm_large_household"]:
                cap += f" ({disc['max_sqm_large_household']:.0f} sqm if >4 family members)"
            print(f"  {key:24s}  {disc['percentage']:>6}%  {cap}  {duration}")
            print(f"  {'':24s}  {disc['basis']}")
            print(f"  {'':24s}  {disc['description']}")
            print()
    print("NOT PRESENT, deliberately: student and large-family discounts have no")
    print("paragraph in the national regulation. A municipality may grant one under")
    print("its own bylaw; read the local table rather than assuming a rate. The")
    print("national route for a large household is the low-income income test.")


def main():
    parser = argparse.ArgumentParser(
        description="Israeli Arnona (Municipal Property Tax) Calculator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --municipality tel-aviv --area 80 --zone 2 --usage residential
  %(prog)s --municipality jerusalem --area 70 --zone B --usage residential --discount oleh --discount-months 6
  %(prog)s --list-municipalities
  %(prog)s --list-discounts
        """,
    )

    parser.add_argument("--municipality", "-m", help="Municipality name (e.g., tel-aviv, jerusalem)")
    parser.add_argument("--area", "-a", type=float, help="Property area in square meters")
    parser.add_argument("--zone", "-z", help="Zone classification (varies by municipality)")
    parser.add_argument("--usage", "-u", default="residential",
                        choices=["residential", "commercial", "office", "industrial"],
                        help="Property usage type (default: residential)")
    parser.add_argument("--discount", "-d", help="Discount category; run --list-discounts for the full list")
    parser.add_argument("--discount-months", type=int, help="Remaining months of discount eligibility")
    parser.add_argument("--household-size", type=int,
                        help="People living in the flat, including the holder. Raises the 70 sqm cap to 90 sqm where the regulation does so (more than four family members with the holder)")
    parser.add_argument("--discount-percentage", type=float,
                        help="Override the category percentage, e.g. to model a lower low-income band or a council that set less than the ceiling")
    parser.add_argument("--json", action="store_true", help="Output in JSON format")
    parser.add_argument("--list-municipalities", action="store_true", help="List all supported municipalities")
    parser.add_argument("--list-discounts", action="store_true", help="List all supported discount categories")

    args = parser.parse_args()

    if args.list_municipalities:
        list_municipalities()
        return

    if args.list_discounts:
        list_discounts()
        return

    if not args.municipality or not args.area or not args.zone:
        parser.error("--municipality, --area, and --zone are required for calculation")

    if args.area <= 0:
        parser.error("Property area must be positive")

    result = calculate_arnona(
        municipality=args.municipality,
        area_sqm=args.area,
        zone=args.zone,
        usage=args.usage,
        discount_type=args.discount,
        discount_months=args.discount_months,
        household_size=args.household_size,
        discount_percentage_override=args.discount_percentage,
    )

    if args.json:
        print(format_result_json(result))
    else:
        print(format_result(result))


if __name__ == "__main__":
    main()
