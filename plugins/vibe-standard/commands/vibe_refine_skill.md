---
description: "Feed repeated review findings, escaped bugs and human corrections back into the pack — skill, rule, hook, verify check, or the project's CLAUDE.md — so the same mistake is fixed once at its source. Usage: /vibe_refine_skill [review report | BUG-NNN | finding]"
---

# Refine the pack from findings

> **Installed as a Claude Code plugin?** The pack's files are not in this repository's
> `.claude/` — they live in the plugin directory `${CLAUDE_PLUGIN_ROOT}` (if that token is
> not substituted, use the path from the `[vibe] plugin root: …` line printed at session
> start). Map every "pack" path in this command as follows:
>
> | Pack path in this command | Plugin location |
> |---|---|
> | profile template `profile/vibe.profile.yaml` | `<plugin root>/templates/profile/vibe.profile.yaml` |
> | `.claude/CLAUDE.md` template | `<plugin root>/templates/CLAUDE.md` |
> | `.claude/rules/` | `<plugin root>/templates/rules/` — **copy into this project's `.claude/rules/`** (plugins cannot load rules; they only apply from the project). Never overwrite an existing file without asking. |
> | `.claude/hooks/*.py` | `<plugin root>/hooks/` — already registered by the plugin; do **not** copy `settings.json` hooks, they would run twice |
> | `.claude/agents/vibe_*.md` | read-only in the plugin (overwritten on update). To change an agent's `model:` or tools, copy it into this project's `.claude/agents/` and edit the copy — a project agent overrides the plugin agent of the same name |
> | `.claude/skills/` | read-only in the plugin. Propose skill/rule changes as a patch to the pack's source repository, or override locally by copying the skill into this project's `.claude/skills/` |
>
> The profile `.claude/vibe.profile.yaml` and everything the pack generates stay in this project, as
> in a manual install.


Load `vibe_project`, then `vibe_code_review` (RV-06).

A review says a slice is wrong. This command asks why the pack let it be wrong. In vibe coding
the signal arrives fast — the same correction given to the AI twice in a week is already a
pattern.

## Step 1 — Collect

From the argument, `{{profile.paths.reviews}}`, the "why not caught" lines in
`{{profile.paths.bugs}}`, and corrections the human repeated. Group identical findings.
**Once is a code defect; twice is a pack or convention defect.**

## Step 2 — Classify each group

| Signal | Fix belongs in |
|---|---|
| One slice wrong, others right | the code — not the pack |
| Same mistake across slices; rule unclear or missing | the **skill** / **rule** wording |
| Rule is clear and still violated | a **hook** or a **verify check** (VE-05) — restating will not help |
| A project-specific convention the AI keeps missing | **CLAUDE.md** project section (SC-06) |
| Finding contradicts a correct rule | the **review checklist** |
| The intent was silent | neither — it is an open question for the owner |
| A bug escaped because nothing checked for it | a **verify check** or a **graduation criterion** |

State the classification before editing anything.

## Step 3 — Never weaken a rule to make a finding disappear

Legitimate: make implicit explicit, disambiguate, add a case or example, add a self-check
line, move to a hook, add a check. Illegitimate: delete the rule, add an exception covering
exactly the failures, soften "never" to "avoid", raise the slice budget because slices keep
exceeding it.

## Step 4 — Apply and record

Minimal edit in the file's own voice. Prefer: self-check line → rule wording → example → verify
check → hook. Append to `{{profile.paths.skill_changes}}`:

| Date | File | Finding | Change | Slices built under the old rule |
|---|---|---|---|---|

The last column is what makes it safe: those slices are candidates for re-review.

## Step 5 — Report

```
Refine — {n} findings in {n} groups
  code defect {n} · skill/rule {n} · hook/check {n} · CLAUDE.md {n} · checklist {n} · open question {n}
  Edits        : {file: change}
  Blast radius : {n} slices → /vibe_review {scope}
```
