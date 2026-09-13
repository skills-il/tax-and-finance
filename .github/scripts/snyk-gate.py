#!/usr/bin/env python3
"""Evaluate one `snyk-agent-scan --skills <dir>/SKILL.md --json` result for skills-il CI.

Prints GitHub annotations scoped to the skill's SKILL.md and exits:
  0  scanned, no blocking risk
  1  scanned, at least one blocking risk
  2  not scanned (quota, auth, parse or any operational error). Never a pass.
"""
import json
import sys

# Inherent to skills whose job is reading outside sources (gov.il, NLI, websites).
IGNORED_RISKS = {"third_party_content_exposure"}
BLOCKING_SCORE = 600


def main() -> int:
    skill_md, json_path = sys.argv[1], sys.argv[2]
    try:
        with open(json_path, encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, ValueError) as exc:
        print(f"::warning file={skill_md}::Snyk Agent Scan did not produce JSON, not scanned ({exc})")
        return 2

    errors, blocking, noted, skills_seen = [], [], [], 0
    for path_result in data.get("scan_path_responses", []):
        if path_result.get("error"):
            errors.append(path_result["error"])
        for skill in path_result.get("skill_risks", []):
            skills_seen += 1
            if skill.get("error"):
                errors.append(skill["error"])
            for name, risk in (skill.get("risk_indexes") or {}).items():
                score = int(risk.get("score", 0))
                evidence = " ".join(str(risk.get("evidence", "")).split())[:300]
                line = f"{name} ({score}/1000): {evidence}"
                if name in IGNORED_RISKS or score < BLOCKING_SCORE:
                    noted.append(line)
                else:
                    blocking.append(line)

    for line in noted:
        print(f"::notice file={skill_md}::Snyk (not blocking) {line}")
    if errors or skills_seen == 0:
        reason = "; ".join(" ".join(str(e.get("message") or e.get("exception") or e).split())[:200] for e in errors) or "no skill found in scan output"
        print(f"::warning file={skill_md}::Snyk Agent Scan not scanned: {reason}")
        return 2
    for line in blocking:
        print(f"::error file={skill_md}::Snyk {line}")
    return 1 if blocking else 0


if __name__ == "__main__":
    sys.exit(main())
