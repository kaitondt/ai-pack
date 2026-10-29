---
description: "Add, inspect or validate your own rules on top of the vibe pack's — a convention the AI keeps getting wrong, a house style, a path-scoped rule. Writes .claude/rules/project/<topic>.md and lists it in the profile. Optional; use it when a correction has been given twice. Usage: /vibe-rule-register [rule or topic | file path | --list | --check]"
model: sonnet
effort: medium
---

# Add a project rule

The pack's rules (`rules/vibe/*`) are the baseline. This command is how a project adds its own
without editing them — the next plugin update may replace pack files, but never
`.claude/rules/project/`.

## Step 1 — Load, and pick the right home

`vibe-project`. Read `.claude/vibe.profile.yaml` for `project_rules`.

Not every convention needs a rule file. Choose:

| The convention is... | Put it in |
|---|---|
| one line, applies everywhere ("dates are stored in UTC", "no new UI libraries") | `CLAUDE.md` → *Project conventions* (SC-06) — say so, add it there, stop |
| scoped to some files, several lines, or needs a reason and a check | a rule file — continue |
| a stage rule (stricter or looser by stage) | not a project rule: the stage table is the pack's; `/vibe-graduate` moves the stage |

## Step 2 — Mode from the argument

| Argument | Mode |
|---|---|
| nothing, or `--list` | **inventory** — `rules/vibe/*`, the project's rules and conventions in force |
| `--check` | **validate only** — change nothing |
| a rule or topic | **add** |
| a file path | **digest a document** — a style guide or ADR becomes the rule file |

## Step 3 — Take the rule in (add)

Ask once, only for what the argument did not say:

1. **The rule**, as an imperative line the AI can follow and a reviewer can check. "Write
   clean code" is not one; ask for the observable form.
2. **Why** — the incident, the bug (`BUG-*`), the decision (`DEC-*`) or the owner's
   correction. A rule with no reason gets argued away.
3. **Scope** — globs for `paths:`, or everywhere.
4. **Check** — a tool (lint rule, test), the reviewer, or nothing yet.

## Step 4 — Conflict check

| The new rule... | Outcome |
|---|---|
| relaxes or contradicts a `rules/vibe/*` rule (secrets, destructive ops, verify-before-trust, small slices, intent-first...) | **Refuse.** Name the rule. Tightening is fine; loosening is a change to the pack (`/vibe-refine-skill`). |
| differs from another pack default (not an invariant) | Allowed. Record it as a `DEC-*` in `{{profile.paths.decisions}}` and in the rule's `Overrides` line. |
| duplicates an existing project rule or convention | Show it; extend that one. |
| is already enforced by a configured linter | Do not restate it; point `enforced_by` at the config. |
| asks for something outside the current intent | It is a feature, not a rule: `/vibe-park`. |

## Step 5 — Write it

Path: `.claude/rules/project/<topic>.md`; one file per topic, several rules per file; never
overwrite — append the next number.

```markdown
---
paths:                      # omit for a rule that applies to everything
  - "src/**"
---
# PROJECT RULES: {TOPIC}

## PRJ-{TOPIC}-01 — {short imperative title}

{MUST / SHOULD / AVOID / FORBIDDEN, then the rule.}

- **Why:** {reason, with the BUG-*/DEC-* or "owner correction, {date}"}
- **Overrides:** {pack rule, or "none"}
- **Check:** {tool | reviewer | none yet}
```

IDs are permanent: a rule that stops applying is marked `**Status:** retired — {date}` and
kept, never deleted or renumbered. Show the file and wait for a yes before saving.

## Step 6 — List it

Append to `{{profile.project_rules}}`:

```yaml
- id: PRJ-STYLE
  file: ".claude/rules/project/style.md"
  scope: ["src/**"]           # same globs as the file's paths:, or ["*"]
  overrides: []
  enforced_by: ""             # tool/config, or "" when review only
  status: active
```

If a tool can enforce it, say which lint rule or test would, and offer to add it as a slice
(`/vibe-intent`) — do not wire tooling inside this command.

## Step 7 — Validate (`--check`, and after every add)

- every `project_rules[].file` exists; every file under `.claude/rules/project/` is listed
- each file's `paths:` equals the entry's `scope`
- rule ids are `PRJ-{TOPIC}-{NN}` for that file's topic; no duplicates; no gaps closed
- every rule has `Why` and `Check`; every override has a `DEC-*`
- no `overrides` names a `rules/vibe/*` invariant

## Step 8 — Report

```
Project rules
  Active        : {n} in {n} files
  Added         : {PRJ-ID} — {title}   scope {globs}
  Overrides     : {n}   {PRJ-ID → pack rule, DEC-*}
  Refused       : {n}   {what, which pack rule}
  Review-only   : {n}   {ids}
```

Name the review-only rules — the ones a lint rule or test could carry instead.
