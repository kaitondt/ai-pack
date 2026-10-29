---
description: "Review changed or staged code against the project rules, architecture boundaries, parity rules and security standards before committing. Usage: /mig-review-commit [paths; omit for the current diff]"
---

# Review changes before commit

## Step 1 — Load

`mig-project`, `mig-review-framework`, and the stack rules for the files in the diff
(`rules/java/`, `rules/typescript/`, `rules/react/`, `rules/sql/`), plus the client
coding-standard digest named in `{{profile.target.coding_standards}}` — the client's standard
wins where they differ, and legacy parity wins over both — and the project rules in
`{{profile.project_rules}}`, cited as `PRJ-*`.

## Step 2 — Collect the change set

Staged files, or the given paths, or the working-tree diff. Print the file list and its
size before reviewing.

## Step 3 — Review

| Area | What to check |
|---|---|
| Parity | IM-01..IM-06 — arithmetic, validation order, explicit sort, verbatim messages, no added defensive behaviour |
| Design conformance | the change matches the module's SC/FC/API/DD, or a GAP item was recorded |
| Boundaries | no layer imports a layer it must not; domain free of framework types |
| Read-only paths | nothing under `{{profile.legacy.root}}` or matching `{{profile.constraints.readonly_globs}}` |
| Data access | parameterised, no schema change where frozen, no raw SQL where procedures are mandated |
| Security | no secrets, server-side authorisation present, input validated server-side |
| Async actions | triggers locked while pending |
| Lists | server-side paging and explicit sorting |
| Stack conventions | each touched stack rule file's review checklist (`JV-*`, `TS-*`, `RX-*`, `SQ-*`) and the client standard; the repository's linter run on the changed files, its output cited rather than restated |
| Tests | new behaviour covered; regression test for any fixed defect |
| Traceability | rows updated for new or changed artifacts |

## Step 4 — Report

Write to `{{profile.review.output_dir}}/commit/review_{YYYYMMDDHHmm}.md` and summarise
inline:

```
Commit review — {n} files
  Critical {n} · Warning {n} · Suggestion {n}
  {each Critical: file:line — rule — what is wrong — how to fix}
  Verdict : {SAFE TO COMMIT | FIX FIRST}
```

Findings are anchored to `file:line`. A finding without a location cannot be acted on.
