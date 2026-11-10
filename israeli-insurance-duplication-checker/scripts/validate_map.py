#!/usr/bin/env python3
"""
validate_map.py  --  deterministic QA for the duplication map (deliverable 1).

The agent fills the layer-by-layer duplication map as a CSV, then runs this
script before handing it over. The script does not decide anything the skill
leaves to judgement; it enforces the mechanical rules the skill states:

  * every row has a covered person, a benefit head, a tier and a verdict;
  * tiers and verdicts come from the skill's vocabulary (Hebrew or English);
  * tier/verdict combinations that the three-tier test forbids are errors
    (a fixed-sum benefit can never be REAL WASTE or CAPPED; a reimbursement
    or property benefit can never be LEGITIMATE STACKING);
  * a row with an overlap verdict must name what it overlaps, and a row that
    overlaps nothing must be NOT A DUPLICATION or UNRESOLVED;
  * a two-tier benefit (פיצוי at home / שיפוי in an institution) must be split
    into two rows, one per tier;
  * the cut list (REAL WASTE rows) is ordered by reversibility first, premium
    second, and the script prints that order;
  * the safe-cut traps: a legacy private סיעוד policy on the cut list, a kupot
    group סיעוד row marked freely reversible, a מכבי כסף row marked reversible.

Usage:
    python3 -I validate_map.py map.csv            # human-readable report
    python3 -I validate_map.py map.csv --json     # machine-readable report
    python3 -I validate_map.py --self-test        # run the built-in tests

Exit code 0 when there are no errors (warnings allowed), 1 otherwise.

CSV columns (header row required; Hebrew or English names accepted):
    covered_person | מי מבוטח
    benefit        | הכיסוי
    tier           | שכבה            (שיפוי / פיצוי / נכס / אחריות / נכס/אחריות / לא ידוע)
                                      An אכ"ע benefit paid as a pre-agreed % of salary is פיצוי; only
                                      אכ"ע paid by actual loss is שיפוי (SKILL.md three-tier table).
    monthly_premium| פרמיה חודשית    (number, "part of N", or UNKNOWN / לא ידוע)
    overlaps_with  | חופף עם         (free text; empty, "-", "nothing", "אין" mean none)
    reversible     | הפיך            (yes / no / unknown, or Hebrew כן / לא / לא ידוע; free text allowed)
    verdict        | מסקנה
    flags          | דגלים           (optional; comma-separated: legacy_private_ltc, group_ltc,
                                      maccabi_kesef, fixed_sum, underwritten, mortgage_linked)
No personal identifiers belong in this file: names or nicknames only.
"""
from __future__ import annotations

import csv
import io
import json
import re
import sys
from dataclasses import dataclass, field

# --------------------------------------------------------------------------- #
# Vocabulary
# --------------------------------------------------------------------------- #

COLUMN_ALIASES = {
    "covered_person": {"covered_person", "covered person", "מי מבוטח", "מבוטח"},
    "benefit": {"benefit", "cover", "cover/benefit", "cover / benefit", "הכיסוי", "כיסוי"},
    "tier": {"tier", "שכבה"},
    "monthly_premium": {"monthly_premium", "premium", "monthly premium", "פרמיה", "פרמיה חודשית"},
    "overlaps_with": {"overlaps_with", "overlaps with", "חופף עם", "חופפת עם"},
    "reversible": {"reversible", "reversible?", "הפיך", "הפיך?", "הפיכה"},
    "verdict": {"verdict", "מסקנה"},
    "flags": {"flags", "דגלים", "flag"},
}

TIER_ALIASES = {
    "indemnity": {"שיפוי", "indemnity", "reimbursement", "שיפוי (indemnity)"},
    "fixed_sum": {"פיצוי", "fixed sum", "fixed-sum", "fixed_sum", "compensation", "פיצוי (fixed sum)"},
    "property": {"נכס", "אחריות", "נכס/אחריות", "נכס / אחריות", "property", "liability",
                 "property/liability", "property and liability", "רכוש", "רכוש/אחריות"},
    "unknown": {"", "?", "לא ידוע", "unknown", "unresolved", "לא הוכרע"},
}

VERDICT_ALIASES = {
    "REAL_WASTE": {"real waste", "real_waste", "בזבוז אמיתי", "בזבוז"},
    "CAPPED": {"capped", "תחום", "תחומה", "השבה תחומה"},
    "PARTIAL": {"partial", "חלקי", "חלקית", "כיסוי חלקי"},
    "LEGITIMATE_STACKING": {"legitimate stacking", "legitimate_stacking", "stacking", "stacks",
                            "צבירה לגיטימית", "צבירה", "נצבר"},
    "UNRESOLVED": {"unresolved", "לא הוכרע", "לא הוכרעה", "לא ידוע"},
    "NOT_A_DUPLICATION": {"not a duplication", "not_a_duplication", "no duplication", "לא כפל",
                          "אין כפל", "לא כפילות"},
}

VERDICT_LABEL = {
    "REAL_WASTE": "REAL WASTE / בזבוז אמיתי",
    "CAPPED": "CAPPED / תחום",
    "PARTIAL": "PARTIAL / חלקי",
    "LEGITIMATE_STACKING": "LEGITIMATE STACKING / צבירה לגיטימית",
    "UNRESOLVED": "UNRESOLVED / לא הוכרע",
    "NOT_A_DUPLICATION": "NOT A DUPLICATION / לא כפל",
}

NONE_MARKERS = {"", "-", "—", "none", "nothing", "nothing held", "n/a", "na", "אין", "אין כיסוי מקביל", "כלום"}

YES_WORDS = ("yes", "כן", "reversible", "annual", "שנתי", "re-accept", "must re-accept", "חייבת לקבל",
             "group", "קבוצתי", "ends with the job", "נגמר עם העבודה", "statutory", "סטטוטורי", "n/a")
NO_WORDS = ("no", "לא", "underwritten", "בחיתום", "not sold", "no longer sold", "cannot be re-bought",
            "לא נמכר", "אינו נמכר", "אי אפשר", "irreversible", "בלתי הפיך", "not freely", "לא הפיך",
            "age-tiered", "מדורג")

LTC_WORDS = ("סיעוד", "סיעודי", "ltc", "long-term care", "long term care")
GROUP_WORDS = ("group", "kupa", "kupat", "קבוצתי", "קופה", "קופת")
PRIVATE_WORDS = ("private", "individual", "legacy", "פרט", "פרטי", "פרטית", "ישנה", "אישי")
MACCABI_KESEF = ("מכבי כסף", "maccabi kesef", "maccabi silver")
FIXED_SUM_EXCEPTION_WORDS = ("מחלות קשות", "critical illness", "dread disease")


def _norm(s: str | None) -> str:
    return re.sub(r"\s+", " ", (s or "").strip()).lower()


def _lookup(aliases: dict, value: str) -> str | None:
    v = _norm(value)
    for key, names in aliases.items():
        if v in {n.lower() for n in names}:
            return key
    return None


# --------------------------------------------------------------------------- #
# Data model
# --------------------------------------------------------------------------- #

@dataclass
class Row:
    index: int                      # 1-based row number in the map (header excluded)
    covered_person: str
    benefit: str
    tier_raw: str
    tier: str | None
    premium_raw: str
    premium: float | None
    overlaps_raw: str
    overlaps: bool
    reversible_raw: str
    reversible: str                 # "yes" | "no" | "unknown"
    verdict_raw: str
    verdict: str | None
    flags: set = field(default_factory=set)

    def label(self) -> str:
        return f"row {self.index} ({self.covered_person or '?'}: {self.benefit or '?'})"


@dataclass
class Report:
    errors: list = field(default_factory=list)
    warnings: list = field(default_factory=list)
    notes: list = field(default_factory=list)
    cut_order: list = field(default_factory=list)
    rows: int = 0

    def ok(self) -> bool:
        return not self.errors

    def to_dict(self) -> dict:
        return {
            "ok": self.ok(),
            "rows": self.rows,
            "errors": self.errors,
            "warnings": self.warnings,
            "notes": self.notes,
            "cut_order": self.cut_order,
        }

    def render(self) -> str:
        out = []
        status = "PASS" if self.ok() else "FAIL"
        out.append(f"validate_map: {status}  ({self.rows} rows, {len(self.errors)} errors, "
                   f"{len(self.warnings)} warnings)")
        for e in self.errors:
            out.append(f"  ERROR    {e}")
        for w in self.warnings:
            out.append(f"  WARNING  {w}")
        for n in self.notes:
            out.append(f"  note     {n}")
        if self.cut_order:
            out.append("  Cut order (REAL WASTE rows, reversible first, premium as tiebreak):")
            for i, item in enumerate(self.cut_order, 1):
                out.append(f"    {i}. {item}")
        return "\n".join(out)


# --------------------------------------------------------------------------- #
# Parsing
# --------------------------------------------------------------------------- #

def _map_header(header: list[str]) -> dict[str, int]:
    mapping: dict[str, int] = {}
    for i, raw in enumerate(header):
        name = _norm(raw)
        for key, names in COLUMN_ALIASES.items():
            if name in {n.lower() for n in names}:
                mapping[key] = i
    return mapping


PREMIUM_PART_MARKERS = ("part of", "included", "כלול", "חלק מ", "incl.")


def _parse_premium(raw: str) -> float | None:
    v = _norm(raw)
    if v in {"", "unknown", "לא ידוע", "?", "n/a", "0"}:
        return 0.0 if v == "0" else None
    if any(v.startswith(m) or m in v for m in PREMIUM_PART_MARKERS):
        return None  # premium sits inside another row's figure; not a parse failure
    m = re.search(r"(\d+(?:[.,]\d+)?)", v.replace(",", ""))
    if not m:
        return None
    try:
        return float(m.group(1))
    except ValueError:
        return None


def _parse_reversible(raw: str) -> str:
    v = _norm(raw)
    if not v or v in {"?", "unknown", "לא ידוע"}:
        return "unknown"
    has_no = any(w in v for w in NO_WORDS)
    has_yes = any(re.search(rf"(^|[^a-zא-ת]){re.escape(w)}([^a-zא-ת]|$)", v) for w in YES_WORDS)
    # Hebrew "לא" inside "לא ידוע" handled above; "no" inside "not freely" counts as no.
    if has_no and not has_yes:
        return "no"
    if has_yes and not has_no:
        return "yes"
    if has_no and has_yes:
        # e.g. "yes, but underwritten" -> treat as not freely reversible
        return "no"
    return "unknown"


def parse_rows(text: str) -> tuple[list[Row], list[str]]:
    errors: list[str] = []
    reader = csv.reader(io.StringIO(text))
    try:
        header = next(reader)
    except StopIteration:
        return [], ["empty file"]
    cols = _map_header(header)
    missing = [k for k in ("covered_person", "benefit", "tier", "verdict") if k not in cols]
    if missing:
        errors.append(f"missing required column(s): {', '.join(missing)}; header seen: {header}")
        return [], errors

    rows: list[Row] = []
    for n, rec in enumerate(reader, 1):
        if not any(c.strip() for c in rec):
            continue

        def get(key: str) -> str:
            i = cols.get(key)
            return rec[i].strip() if i is not None and i < len(rec) else ""

        tier_raw = get("tier")
        overlaps_raw = get("overlaps_with")
        flags = {f.strip().lower() for f in get("flags").split(",") if f.strip()}
        rows.append(Row(
            index=n,
            covered_person=get("covered_person"),
            benefit=get("benefit"),
            tier_raw=tier_raw,
            tier=_lookup(TIER_ALIASES, tier_raw),
            premium_raw=get("monthly_premium"),
            premium=_parse_premium(get("monthly_premium")),
            overlaps_raw=overlaps_raw,
            overlaps=_norm(overlaps_raw) not in NONE_MARKERS,
            reversible_raw=get("reversible"),
            reversible=_parse_reversible(get("reversible")),
            verdict_raw=get("verdict"),
            verdict=_lookup(VERDICT_ALIASES, get("verdict")),
            flags=flags,
        ))
    return rows, errors


# --------------------------------------------------------------------------- #
# Checks
# --------------------------------------------------------------------------- #

def _is_ltc(r: Row) -> bool:
    b = _norm(r.benefit)
    return any(w in b for w in LTC_WORDS) or {"group_ltc", "legacy_private_ltc"} & r.flags


def _is_group(r: Row) -> bool:
    b = _norm(r.benefit) + " " + _norm(r.reversible_raw)
    return "group_ltc" in r.flags or any(w in b for w in GROUP_WORDS)


def _is_private(r: Row) -> bool:
    b = _norm(r.benefit) + " " + _norm(r.reversible_raw)
    return "legacy_private_ltc" in r.flags or any(w in b for w in PRIVATE_WORDS)


def validate(rows: list[Row], parse_errors: list[str]) -> Report:
    rep = Report(rows=len(rows))
    rep.errors.extend(parse_errors)
    if not rows:
        if not parse_errors:
            rep.errors.append("no data rows")
        return rep

    people = {r.covered_person for r in rows if r.covered_person}
    multi_adult = len(people) > 1

    for r in rows:
        # 1. completeness
        if not r.covered_person:
            rep.errors.append(f"{r.label()}: covered person is empty"
                              + (" (mandatory in a multi-adult map)" if multi_adult else ""))
        if not r.benefit:
            rep.errors.append(f"row {r.index}: benefit head is empty")
        if r.tier is None:
            rep.errors.append(f"{r.label()}: tier '{r.tier_raw}' is not in the vocabulary "
                              f"(שיפוי / פיצוי / נכס/אחריות / לא ידוע)")
        if r.verdict is None:
            rep.errors.append(f"{r.label()}: verdict '{r.verdict_raw}' is not one of the six verdicts")
        praw = _norm(r.premium_raw)
        if (r.premium is None and praw not in {"unknown", "לא ידוע", "", "?"}
                and not any(m in praw for m in PREMIUM_PART_MARKERS)):
            rep.warnings.append(f"{r.label()}: premium '{r.premium_raw}' could not be read; "
                                f"write a number, 'part of N', or UNKNOWN")
        if r.premium is None and _norm(r.premium_raw) in {"", "?"}:
            rep.warnings.append(f"{r.label()}: premium missing; mark UNKNOWN explicitly if the user "
                                f"has not pulled it yet")

        # 2. two-tier benefit not split
        traw = _norm(r.tier_raw)
        if "/" in traw and r.tier is None and ("שיפוי" in traw or "פיצוי" in traw or "indemnity" in traw):
            rep.errors.append(f"{r.label()}: tier '{r.tier_raw}' names two tiers; split the benefit into "
                              f"one row per tier (e.g. סיעוד: פיצוי at home / שיפוי in an institution)")

        # 6. safe-cut traps
        if _is_ltc(r):
            if _is_private(r) and not _is_group(r):
                if r.verdict == "REAL_WASTE":
                    rep.errors.append(f"{r.label()}: a legacy private סיעוד policy is on the cut list. The product "
                                      f"is no longer sold and cannot be repurchased at any price; it never tops a "
                                      f"cut list")
                if r.reversible == "yes":
                    rep.errors.append(f"{r.label()}: a legacy private סיעוד policy marked reversible; it is not sold "
                                      f"any more, so reversibility is 'no'")
            if _is_group(r):
                if r.reversible == "yes":
                    rep.errors.append(f"{r.label()}: kupot group סיעוד marked freely reversible. Joining is "
                                      f"'בכפוף לבדיקת מצבך הרפואי' and the benefit is tiered by age at first "
                                      f"joining, so it is not freely reversible")
                if r.verdict == "REAL_WASTE":
                    rep.warnings.append(f"{r.label()}: kupot group סיעוד on the cut list; the skill says keep both "
                                        f"group and private unless the insurer confirms re-entry terms in writing")
        if any(w in _norm(r.benefit) for w in MACCABI_KESEF) or "maccabi_kesef" in r.flags:
            if r.reversible == "yes":
                rep.errors.append(f"{r.label()}: מכבי כסף is a closed tier with no route back in; treat it as "
                                  f"irreversible")
        if "mortgage_linked" in r.flags and r.verdict == "REAL_WASTE":
            rep.notes.append(f"{r.label()}: mortgage-linked line on the cut list; the bank's written consent to "
                             f"release the charge must exist before any cancellation is sent")

        if r.tier is None or r.verdict is None:
            continue

        # 3. tier / verdict consistency
        if r.tier == "fixed_sum" and r.verdict in {"REAL_WASTE", "CAPPED"}:
            rep.errors.append(f"{r.label()}: a fixed-sum (פיצוי) benefit cannot be {VERDICT_LABEL[r.verdict]}; "
                              f"fixed-sum cover stacks by law (פרק ב' via ס' 54(א)). Use LEGITIMATE STACKING, "
                              f"or PARTIAL for near-identical מחלות קשות lists")
        if r.tier == "fixed_sum" and r.verdict == "PARTIAL":
            b = _norm(r.benefit)
            if not any(w in b for w in FIXED_SUM_EXCEPTION_WORDS):
                rep.warnings.append(f"{r.label()}: PARTIAL on a fixed-sum benefit is reserved for near-identical "
                                    f"מחלות קשות condition lists; confirm this is that case")
        if r.tier in {"indemnity", "property"} and r.verdict == "LEGITIMATE_STACKING":
            rep.errors.append(f"{r.label()}: a {('reimbursement' if r.tier == 'indemnity' else 'property/liability')} "
                              f"benefit cannot be LEGITIMATE STACKING; overlapping שיפוי is CAPPED, overlapping "
                              f"נכס/אחריות is REAL WASTE (ס' 59)")
        if r.tier == "unknown" and r.verdict != "UNRESOLVED":
            rep.errors.append(f"{r.label()}: tier is unknown, so the verdict must be UNRESOLVED until the "
                              f"insurer answers 'שיפוי או פיצוי?'")

        # 4. overlap column vs verdict
        overlap_verdicts = {"REAL_WASTE", "CAPPED", "PARTIAL", "LEGITIMATE_STACKING"}
        if r.verdict in overlap_verdicts and not r.overlaps:
            rep.errors.append(f"{r.label()}: verdict {VERDICT_LABEL[r.verdict]} but 'overlaps with' is empty; "
                              f"name the row(s) it overlaps or change the verdict to NOT A DUPLICATION")
        if r.verdict == "NOT_A_DUPLICATION" and r.overlaps:
            rep.notes.append(f"{r.label()}: NOT A DUPLICATION while 'overlaps with' names '{r.overlaps_raw}'; "
                             f"fine when the overlap is apparent only (car vs home liability, מקיף vs its own "
                             f"צד ג' chapter); otherwise revisit the verdict")

        # 5. reversibility recorded for anything on the cut list
        if r.verdict == "REAL_WASTE" and r.reversible == "unknown":
            rep.errors.append(f"{r.label()}: REAL WASTE with reversibility unknown; the cut order depends on it")

    # 7. cut order
    waste = [r for r in rows if r.verdict == "REAL_WASTE"]
    rev_rank = {"yes": 0, "unknown": 1, "no": 2}
    waste.sort(key=lambda r: (rev_rank[r.reversible], -(r.premium or 0.0)))
    for r in waste:
        prem = "UNKNOWN" if r.premium is None else f"{r.premium:g}"
        rep.cut_order.append(f"{r.label()}  reversible={r.reversible}  premium={prem}")
    if waste and any(r.reversible == "no" for r in waste) and any(r.reversible == "yes" for r in waste):
        rep.notes.append("the cut list mixes reversible and underwritten layers; the reversible ones go first "
                         "regardless of premium")

    # 8. gaps hint per adult (not an error: deliverable 3 is a judgement call)
    child_words = ("child", "children", "ילד", "ילדים", "ילדה", "קטין", "בן ", "בת ")
    no_akaa, no_ltc = [], []
    for p in sorted(people):
        pn = _norm(p)
        if any(w in pn for w in child_words) or "+" in pn or "&" in pn:
            continue  # composite or child rows are not adults to audit for gaps
        mine = [r for r in rows if r.covered_person == p]
        text = " ".join(_norm(r.benefit) for r in mine)
        if not any(w in text for w in ("אכ\"ע", "אכע", "אובדן כושר", "disability", "אובדן כושר עבודה")):
            no_akaa.append(p)
        if not any(w in text for w in LTC_WORDS):
            no_ltc.append(p)
    if no_akaa:
        rep.notes.append("no אכ\"ע row for: " + ", ".join(no_akaa) + "; if they earn, consider it for the gaps list")
    if no_ltc:
        rep.notes.append("no סיעוד row for: " + ", ".join(no_ltc) + "; consider it for the gaps list")

    return rep


def validate_csv_text(text: str) -> Report:
    rows, parse_errors = parse_rows(text)
    return validate(rows, parse_errors)


# --------------------------------------------------------------------------- #
# Self-test
# --------------------------------------------------------------------------- #

_SAMPLE_OK = """covered_person,benefit,tier,monthly_premium,overlaps_with,reversible,verdict,flags
Dani,רכב מקיף (includes צד ג' chapter),נכס/אחריות,340,row 2,yes annual policy,NOT A DUPLICATION,
Dani,Standalone צד ג' bought separately,נכס/אחריות,95,row 1,yes annual policy,REAL WASTE,
Dani + Maya,ביטוח מבנה tied to the mortgage,נכס,88,row 4,"yes, 451 allows cancelling without fee",REAL WASTE,mortgage_linked
Dani + Maya,מבנה section of separate ביטוח דירה,נכס,included,row 3,yes,CAPPED,
Children,Group dental via Dani's employer,שיפוי,62,"rows 6, 7","group, ends with the job",REAL WASTE,
Children,Group dental via Maya's employer,שיפוי,58,"rows 5, 7","group, ends with the job",CAPPED,
Children,Basket dental (under 18),שיפוי,0,"rows 5, 6",n/a statutory,NOT A DUPLICATION,
Children,ביטוח תאונות אישיות לתלמידים (compulsory),פיצוי,69/yr,row 9,n/a statutory,NOT A DUPLICATION,
Child (14),Private personal-accident rider,פיצוי,29,row 8,underwritten,LEGITIMATE STACKING,
Maya,אכ"ע private policy (pre-agreed % of salary),פיצוי,180,,underwritten,NOT A DUPLICATION,
"""

_SAMPLE_BAD = """מי מבוטח,הכיסוי,שכבה,פרמיה חודשית,חופף עם,הפיך,מסקנה,דגלים
אבי,ריסק ביטוח חיים,פיצוי,120,שורה 2,כן,בזבוז אמיתי,
אבי,ביטוח חיים למשכנתא,פיצוי,90,שורה 1,לא,תחום,
אבי,סיעוד פרטי ישן (נרכש 2008),פיצוי,210,שורה 4,לא נמכר יותר,בזבוז אמיתי,legacy_private_ltc
אבי,סיעוד קבוצתי (קופה),פיצוי בבית / שיפוי במוסד,61,שורה 3,כן,צבירה לגיטימית,group_ltc
,ניתוחים קבוצתי,שיפוי,31,,קבוצתי,צבירה לגיטימית,
אבי,מכבי כסף,שיפוי,40,,כן,לא כפל,
"""


def _self_test() -> int:
    ok = validate_csv_text(_SAMPLE_OK)
    assert ok.ok(), "sample map should pass:\n" + ok.render()
    assert len(ok.cut_order) == 3, ok.render()
    # reversible rows first; row 3 (88) before row 2 (95)? No: both reversible -> higher premium first
    assert "row 2" in ok.cut_order[0] or "row 3" in ok.cut_order[0], ok.render()
    assert ok.cut_order[0].startswith("row 2"), "highest premium among reversible rows should lead: " + ok.render()

    bad = validate_csv_text(_SAMPLE_BAD)
    assert not bad.ok()
    text = bad.render()
    expectations = [
        "fixed-sum (פיצוי) benefit cannot be REAL WASTE",      # row 1
        "fixed-sum (פיצוי) benefit cannot be CAPPED",          # row 2
        "legacy private סיעוד policy is on the cut list",      # row 3
        "names two tiers; split the benefit",                  # row 4 tier
        "kupot group סיעוד marked freely reversible",          # row 4 reversible
        "covered person is empty",                             # row 5
        "cannot be LEGITIMATE STACKING",                       # row 5 tier/verdict
        "'overlaps with' is empty",                            # row 5 overlaps
        "מכבי כסף is a closed tier",                           # row 6
    ]
    missing = [e for e in expectations if e not in text]
    assert not missing, "self-test expected these findings:\n" + "\n".join(missing) + "\n\nGOT:\n" + text

    # header in Hebrew recognised
    assert bad.rows == 6, text
    # empty file
    empty = validate_csv_text("")
    assert not empty.ok()
    print("validate_map self-test: OK (2 sample maps, 9 expected findings)")
    return 0


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def main(argv: list[str]) -> int:
    if "--self-test" in argv:
        return _self_test()
    args = [a for a in argv if not a.startswith("--")]
    if not args:
        print(__doc__)
        return 2
    path = args[0]
    with open(path, encoding="utf-8-sig") as fh:
        text = fh.read()
    rep = validate_csv_text(text)
    if "--json" in argv:
        print(json.dumps(rep.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(rep.render())
    return 0 if rep.ok() else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
