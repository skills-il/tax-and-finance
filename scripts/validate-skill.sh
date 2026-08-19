#!/usr/bin/env bash
# Validates SKILL.md files against the Agent Skills spec.
# Usage: ./scripts/validate-skill.sh <SKILL.md> [<SKILL.md> ...]
# Exit code: 0 = all valid, 1 = errors found

set -euo pipefail

ERRORS=""
WARNINGS=""

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

  # 7b. SKILL_HE.md: the Hebrew companion was historically invisible to this
  # script, because check 1 rejects any file not named SKILL.md and every later
  # check reads only "$file". Hebrew is the site's DEFAULT locale, so a Hebrew
  # file could drift well past the word cap, keep sections the English file had
  # moved to references/, and carry untranslated headings, with nothing to catch
  # it. These checks close that gap.
  #
  # Split deliberately between hard errors and warnings. Missing files and
  # untranslated headings are unambiguous bugs, so they fail. The word cap and
  # heading parity are content debt that predates this check on a fair number of
  # skills, so they warn rather than break CI for whoever edits one next.
  HE_FILE="$DIR/SKILL_HE.md"
  if [ ! -f "$HE_FILE" ]; then
    # Not cosmetic: the sync pipeline falls back to the English body for
    # content_he, so the Hebrew page silently renders English with no error.
    ERRORS="$ERRORS\n- $file: missing sibling SKILL_HE.md. The sync pipeline falls back to the English body for content_he, so the Hebrew page renders English with no visible failure."
  else
    # 7b-i. Untranslated section headings left in the Hebrew file.
    # Headings inside a fenced code block are template/example content, not
    # sections of this document. skills-il-skill-creator legitimately prints an
    # English SKILL.md skeleton inside ``` fences in its Hebrew file, and an
    # earlier version of this check flagged it and "fixed" the template into
    # Hebrew, which told authors to write Hebrew headings in an English file.
    # Strip fenced blocks before looking for untranslated headings.
    HE_ENG_HEADINGS=$(awk '
      /^[[:space:]]*```/ { fence = !fence; next }
      !fence && /^#{2,3} (Examples|Troubleshooting|Instructions|Gotchas|Reference Links|Bundled Resources|Recommended MCP Servers|References|Scripts)[[:space:]]*$/ { print NR ":" $0 }
    ' "$HE_FILE" || true)
    if [ -n "$HE_ENG_HEADINGS" ]; then
      HE_ENG_COUNT=$(printf '%s\n' "$HE_ENG_HEADINGS" | grep -c . || true)
      HE_ENG_LIST=$(printf '%s\n' "$HE_ENG_HEADINGS" | sed 's/^/    /')
      ERRORS="$ERRORS\n- $HE_FILE: $HE_ENG_COUNT untranslated English heading(s) render as-is on the Hebrew page:\n$HE_ENG_LIST"
    fi

    # 7b-ii. Hebrew body word count. Same 5,000 cap as the English body.
    HE_BODY=$(awk 'BEGIN{n=0} /^---$/{n++; if(n==2){found=1; next}} found{print}' "$HE_FILE")
    if [ "$(head -1 "$HE_FILE")" != "---" ]; then
      HE_BODY=$(cat "$HE_FILE")
    fi
    HE_WORDS=$(printf '%s' "$HE_BODY" | wc -w | tr -d ' ')
    if [ "$HE_WORDS" -gt 5000 ]; then
      WARNINGS="$WARNINGS\n- $HE_FILE: Hebrew body is $HE_WORDS words (cap 5,000). Move detail to references/ as you would for SKILL.md. This is a warning today and is intended to become an error once the existing backlog is cleared."
    fi

    # 7b-iii. Section-structure parity between the two languages.
    EN_H=$(grep -c '^#\{2,3\} ' "$file" || true)
    HE_H=$(grep -c '^#\{2,3\} ' "$HE_FILE" || true)
    if [ "$EN_H" != "$HE_H" ]; then
      WARNINGS="$WARNINGS\n- $HE_FILE: section count differs from SKILL.md (EN=$EN_H, HE=$HE_H). Usually means a fix landed in one language only, or a section was moved to references/ on one side. Check before shipping."
    fi
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

if [ -n "$WARNINGS" ]; then
  echo ""
  echo "WARNINGS (not blocking):"
  echo -e "$WARNINGS"
fi

if [ -n "$ERRORS" ]; then
  echo ""
  echo "VALIDATION ERRORS:"
  echo -e "$ERRORS"
  exit 1
fi

echo ""
echo "All SKILL.md files are valid."
