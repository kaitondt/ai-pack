---
description: "Feed repeated review findings, escaped bugs and human corrections back into the pack — skill, rule, hook, verify check, or the project's CLAUDE.md — so the same mistake is fixed once at its source. Usage: /vibe_refine_skill [review report | BUG-NNN | finding]"
---

# Refine the pack from findings

Load `vibe_project`, then `vibe_review` (RV-06).

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
