---
description: "Review AI-written code for scope creep, security holes, phantom APIs, weakened tests, duplication and unrecorded debt — a slice diff, a branch, or the whole codebase. Read-only; delegates to vibe_reviewer. Usage: /vibe_review [slice | branch | codebase]"
---

# Review

Load `vibe_project`, then `vibe_code_review`.

## Step 1 — Scope and depth (RV-01)

| Argument | Diff | Depth |
|---|---|---|
| none / `slice` | working tree + last commit vs. the slice's checkpoint | Slice (RV-02 + RV-03) |
| `branch` | `git diff <main branch>...HEAD` | Slice, per commit grouped by slice ID |
| `codebase` | the whole repository | Codebase (RV-04) |

## Step 2 — Review

Delegate to `vibe_reviewer` with the diff, the intent(s) the commits cite, PRODUCT.md, and
the stage. The reviewer does not edit code. It is a different context from the one that wrote
the code — that is the point.

## Step 3 — Write the report

`{{profile.paths.reviews}}/<date>-<scope>.md`: findings with severity, file:line, rule, fix;
for `codebase`, the RV-04 measures table.

## Step 4 — Act on it

- Critical / High → the slice is not done / the branch is not mergeable; name the fix.
- Unrecorded shortcuts → propose `DEBT-*` rows (the human confirms; then append).
- A finding seen in an earlier review too → flag it for `/vibe_refine_skill` (RV-06).

## Step 5 — Report

```
Review — {scope}                                   stage: {stage}
  Critical {n} · High {n} · Medium {n} · Low {n}
  Top      : {the 3 most important, one line each}
  Debt     : {n} unrecorded shortcuts found
  Repeats  : {n} findings seen before → /vibe_refine_skill
  Verdict  : {accept | fix Critical/High first}
  Report   : {path}
```
