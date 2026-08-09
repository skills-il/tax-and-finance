#!/usr/bin/env bash
# Validates SKILL.md files against the Agent Skills spec.
# Usage: ./scripts/validate-skill.sh <SKILL.md> [<SKILL.md> ...]
# Exit code: 0 = all valid, 1 = errors found

set -euo pipefail

ERRORS=""

# Frontmatter YAML parsing needs python3 + PyYAML. Probe once; if either is
# missing, skip the check with a notice rather than failing the build.
YAML_CHECK=1
if ! python3 -c 'import yaml' >/dev/null 2>&1; then
  YAML_CHECK=0
  echo "NOTICE: python3 with PyYAML unavailable - skipping frontmatter YAML parse check"
fi

# Echoes the YAML parser error for a file's frontmatter, or nothing if it parses.
yaml_frontmatter_error() {
  awk 'NR==1{next} /^---$/{exit} {print}' "$1" | python3 -c '
import sys, yaml
try:
    yaml.safe_load(sys.stdin.read())
except Exception as e:
    print(str(e).replace("\n", " ")[:200])
' 2>&1
}
SECRET_PATTERNS='(sk-[a-zA-Z0-9]{20,}|AKIA[A-Z0-9]{16}|ghp_[a-zA-Z0-9]{36}|password:\s*[^\s]+|secret_key|api_key\s*=\s*["'"'"'][^\s]+)'

for file in "$@"; do
  [ -z "$file" ] && continue
  echo "Validating: $file"
  DIR=$(dirname "$file")
  FOLDER_NAME=$(basename "$DIR")

  # 1. File must be exactly SKILL.md (case-sensitive)
  if [ "$(basename "$file")" != "SKILL.md" ]; then
    ERRORS="$ERRORS\n- $file: File must be named exactly SKILL.md"
    continue
  fi

  # 2. Frontmatter must start with ---
  FIRST_LINE=$(head -1 "$file")
  if [ "$FIRST_LINE" != "---" ]; then
    ERRORS="$ERRORS\n- $file: Missing YAML frontmatter (must start with ---)"
    continue
  fi

  # Extract frontmatter (between first and second ---)
  FRONTMATTER=$(awk 'NR==1{next} /^---$/{exit} {print}' "$file")

  # 2b. Frontmatter must parse as YAML. An unquoted description containing a
  # colon-space passes every other check here and then hard-fails the sync
  # pipeline with "incomplete explicit mapping pair". Also checks a sibling
  # SKILL_HE.md, but only when it actually has frontmatter (some do not).
  if [ "$YAML_CHECK" = "1" ]; then
    YAML_ERR=$(yaml_frontmatter_error "$file")
    if [ -n "$YAML_ERR" ]; then
      ERRORS="$ERRORS\n- $file: frontmatter is not valid YAML ($YAML_ERR). Most often an unquoted description containing ': ' - wrap the value in single quotes."
    fi
    HE_FILE="$DIR/SKILL_HE.md"
    if [ -f "$HE_FILE" ] && [ "$(head -1 "$HE_FILE")" = "---" ]; then
      HE_YAML_ERR=$(yaml_frontmatter_error "$HE_FILE")
      if [ -n "$HE_YAML_ERR" ]; then
        ERRORS="$ERRORS\n- $HE_FILE: frontmatter is not valid YAML ($HE_YAML_ERR). Most often an unquoted description containing ': ' - wrap the value in single quotes."
      fi
    fi
  fi

  # 3. name field: kebab-case, matches folder
  NAME=$(echo "$FRONTMATTER" | grep '^name:' | sed 's/name: *//' | tr -d "'\"\r" | xargs)
  if [ -z "$NAME" ]; then
    ERRORS="$ERRORS\n- $file: Missing required 'name' field"
  elif ! echo "$NAME" | grep -qE '^[a-z0-9]+(-[a-z0-9]+)*$'; then
    ERRORS="$ERRORS\n- $file: name '$NAME' must be kebab-case (lowercase, hyphens only)"
  elif [ "$NAME" != "$FOLDER_NAME" ]; then
    ERRORS="$ERRORS\n- $file: name '$NAME' does not match folder name '$FOLDER_NAME'"
  fi

  # 4. No reserved names
  if echo "$NAME" | grep -qiE '(claude|anthropic)'; then
    ERRORS="$ERRORS\n- $file: name cannot contain 'claude' or 'anthropic' (reserved)"
  fi

  # 5. description field: present, within the length cap, no XML, includes WHEN trigger
  # Handle multi-line YAML descriptions (>- or | or plain multi-line)
  # DESC_RAW keeps the YAML quoting; DESC is the parsed value used for the
  # content checks below.
  DESC_RAW=$(awk '
    /^description:/ {
      sub(/^description:[[:space:]]*/, "")
      if ($0 ~ /^[>|]-?[[:space:]]*$/) { getline; sub(/^[[:space:]]+/, ""); desc = $0 }
      else { desc = $0 }
      while (getline > 0) {
        if (/^[a-zA-Z_-]+:/ || /^---$/) break
        sub(/^[[:space:]]+/, ""); desc = desc " " $0
      }
      print desc
      exit
    }
  ' <<< "$FRONTMATTER")
  DESC=$(sed -E 's/^["'"'"']//; s/["'"'"']$//' <<< "$DESC_RAW")
  if [ -z "$DESC" ]; then
    ERRORS="$ERRORS\n- $file: Missing required 'description' field"
  else
    # The spec cap is 1024, but Gemini Spark REJECTS a skill at exactly 1024 and
    # may count the surrounding YAML quotes, so the gate is on the raw quoted
    # value at 1023. Aim for =< 950 when authoring; long descriptions also blunt
    # agent routing. See CLAUDE.md "Gemini Spark".
    DESC_LEN=${#DESC_RAW}
    if [ "$DESC_LEN" -gt 1023 ]; then
      ERRORS="$ERRORS\n- $file: description too long ($DESC_LEN incl. YAML quotes, max 1023; Gemini Spark rejects at the 1024 boundary)"
    fi
    if echo "$DESC" | grep -qE '[<>]'; then
      ERRORS="$ERRORS\n- $file: description contains forbidden XML angle brackets"
    fi
    HAS_TRIGGER=$(echo "$DESC" | grep -iE '(use when|use for|use if|when user|when the user)' || true)
    if [ -z "$HAS_TRIGGER" ]; then
      ERRORS="$ERRORS\n- $file: description should include WHEN to use it (e.g., 'Use when user asks to...')"
    fi
  fi

  # 6. XML angle brackets anywhere in frontmatter (exclude YAML block scalar indicators like >- and |-)
  if echo "$FRONTMATTER" | grep -v -E '^[[:space:]]*[>|]-?[[:space:]]*$' | grep -v -E ':[[:space:]]+[>|]-?[[:space:]]*$' | grep -qE '[<>]'; then
    ERRORS="$ERRORS\n- $file: Frontmatter contains forbidden XML angle brackets"
  fi

  # 7. SKILL.md body word count (max 5,000)
  BODY=$(awk 'BEGIN{n=0} /^---$/{n++; if(n==2){found=1; next}} found{print}' "$file")
  WORD_COUNT=$(echo "$BODY" | wc -w | tr -d ' ')
  if [ "$WORD_COUNT" -gt 5000 ]; then
    ERRORS="$ERRORS\n- $file: SKILL.md body is $WORD_COUNT words (max 5,000). Move detailed docs to references/"
  fi

  # 8. No README.md in skill folder
  if [ -f "$DIR/README.md" ]; then
    ERRORS="$ERRORS\n- $file: Skill folder must not contain README.md (use SKILL.md or references/)"
  fi

  # 9. No hardcoded secrets in the entire skill directory
  if grep -rEnH "$SECRET_PATTERNS" "$DIR/" 2>/dev/null; then
    ERRORS="$ERRORS\n- $file: Possible hardcoded secrets detected in skill directory"
  fi

  [ -z "$ERRORS" ] && echo "  PASS: $file"
done

if [ -n "$ERRORS" ]; then
  echo ""
  echo "VALIDATION ERRORS:"
  echo -e "$ERRORS"
  exit 1
fi

echo ""
echo "All SKILL.md files are valid."
