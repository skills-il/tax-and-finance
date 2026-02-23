# CLAUDE.md

This file provides guidance to Claude Code when working in this repository.

## Project Overview

This is a Skills IL category repository containing AI agent skills for Israeli tax and finance needs. Each subdirectory is a self-contained skill following the open Agent Skills standard.

## Repository Structure

```
tax-and-finance/
├── .github/                    # CI workflows, issue/PR templates
├── israeli-e-invoice/          # Skill: Israeli E-Invoice
│   ├── SKILL.md               # Required skill definition
│   └── scripts/               # Optional helper scripts
├── shekel-currency-converter/  # Skill: Shekel Currency Converter
│   └── SKILL.md
├── CLAUDE.md                   # This file
├── LICENSE                     # MIT
└── README.md                   # Category overview
```

## Skill Format (CRITICAL)

Every skill is a folder containing a `SKILL.md` file. The folder name MUST be kebab-case.

### SKILL.md Structure

```yaml
---
name: skill-name-in-kebab-case        # Required, must match folder name
description: >-                        # Required, <1024 chars, no XML tags
  [What it does]. [When to use it — include trigger phrases].
  [Key capabilities]. [Optional: Do NOT use for X].
license: MIT                           # Optional
allowed-tools: "Bash(python:*) WebFetch"  # Optional — restrict tool access
compatibility: "Requires Claude Code"     # Optional — 1-500 chars
metadata:                              # Optional — any custom key-value pairs
  author: github-username
  version: 1.0.0
  category: tax-and-finance
  tags: [tax, invoice, vat]
---

# Skill Name

## Instructions
[Step-by-step, specific, actionable instructions for the AI agent]

## Examples
[Concrete usage examples with "User says:" and "Result:"]

## Troubleshooting
[Common errors with Cause + Solution format]
```

### Description Field (CRITICAL)

The `description` is the most important field — it determines whether Claude loads the skill.

**Pattern:** `[What it does] + [When to use it] + [Key capabilities]`

Good: `Generate and validate e-invoices per Israeli Tax Authority standards. Use when user needs to create invoices, validate tax compliance, or asks about Israeli invoicing. Supports tax invoice, receipt, and credit invoice types.`

Bad: `Helps with tax stuff.` (too vague — won't trigger reliably)

**Negative triggers** prevent overtriggering: `Do NOT use for general financial advice or investment queries.`

### Validation Rules

These rules are enforced by CI on every PR:

1. File must be exactly `SKILL.md` (case-sensitive, not SKILL.MD or skill.md)
2. YAML frontmatter must have `---` delimiters on both sides
3. `name` field: kebab-case only, no spaces or capitals, must match folder name
4. `description` field: present, under 1024 chars, no XML angle brackets, must include WHAT + WHEN
5. SKILL.md body must be under 5,000 words
6. No `README.md` inside skill folders (docs go in SKILL.md or references/)
7. No skill names containing "claude" or "anthropic" (reserved by Anthropic)
8. No hardcoded secrets (patterns: `sk-`, `AKIA`, `ghp_`, `password:`, `secret:`)

### Writing Skills

- **Description:** Follow `[What] + [When] + [Capabilities]` pattern. Add negative triggers to prevent overtriggering.
- **Instructions:** Be specific (`Run scripts/validate.py --input {file}` not `Validate the data`). Include error handling. Reference bundled resources.
- **Progressive disclosure:** Frontmatter (always loaded) → SKILL.md body (when relevant) → `references/` (on demand). Keep SKILL.md under 5,000 words.

See [CONTRIBUTING.md](https://github.com/skills-il/.github/blob/main/CONTRIBUTING.md) for the full guide.

## Commands

Validate SKILL.md files locally before pushing:
```bash
./scripts/validate-skill.sh <skill-folder>/SKILL.md
```

CI runs this automatically on every PR.

## Conventions

- All skill folders use kebab-case naming
- Bilingual content in skills should use `{ he: "...", en: "..." }` when applicable
- Israeli-specific context (laws, regulations, APIs) should reference official sources
- Org-level files (CONTRIBUTING, SECURITY, CODE_OF_CONDUCT) are inherited from skills-il/.github
- Category-level README lists all skills with descriptions and install commands
