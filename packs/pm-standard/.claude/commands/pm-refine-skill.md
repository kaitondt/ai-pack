---
description: "Feed a lesson, an audit finding or a recurring failure back into the pack: add or sharpen a rule, a checklist row, a profile field or a hook, so the same mistake becomes structurally harder. Usage: /pm-refine-skill <finding, LL-id, or CAPA-id>"
---

# Refine the pack

The loop that makes the pack better than the last project. Without it, every lesson is
re-learned by the next team at the same price.

## Step 1 — Load

`pm-project`, plus the skill the finding concerns.

## Step 2 — Establish the failure precisely

From an `LL-*`, a `CAPA-*`, an audit finding, a client complaint, or an escaped defect. Answer:

1. What went wrong, specifically, with the evidence?
2. **Which check would have caught it, and why did it not run?** — the question that produces
   the fix
3. Is this the first time, or has it happened before on this project or another?

A finding that cannot answer question 2 is not yet ready to become a rule; it becomes an
investigation instead.

## Step 3 — Choose the intervention level

Prefer the most structural fix that fits, because it is the one that survives turnover and
schedule pressure:

| Level | Use when | Example |
|---|---|---|
| **Hook** | a mechanical, checkable condition | block edits to baselined paths without an active CR |
| **Profile field** | it varies per project but must be decided | `max_planned_allocation_percent` |
| **Rule** | it must hold on every project | "padding is forbidden; buffers are mandatory" |
| **Skill section** | it is know-how, applied with judgement | how to read an S-curve |
| **Command step** | it is a step people skip | verify EV integrity before computing EVM |
| **Checklist row** | it is a recurring omission | "documentation cascade" in the CR impact matrix |

A rule that a hook could enforce should be a hook. A hook that cannot be written without false
positives should be a command step.

## Step 4 — Write it in the pack's voice

Short, imperative, with the **failure mode named**. The reason is what makes a rule survive
the first schedule crunch — a rule with no stated consequence is read as bureaucracy and
dropped exactly when it matters.

State it once, in the right file. A rule repeated in four skills will be edited in one and
contradict itself in the other three.

## Step 5 — Verify it would have caught the original failure

Walk the original event through the new rule. If it would still have passed, the rule is
aimed at the wrong point — usually one step too late in the chain.

## Step 6 — Record

Note the change in the pack's own history: what failed, what changed, and the `LL-*` or
`CAPA-*` behind it. Then close the CAPA with its effectiveness check date (PR-07).

## Report

```
Refinement — {finding}
  Failure       : {what happened, with evidence}
  Missing check : {which check, why it did not run}
  Recurrence    : {first time | n-th time}
  Intervention  : {hook | profile | rule | skill | command | checklist}
  Changed       : {file} — {what was added or sharpened}
  Verified      : the original failure would now be caught at {which step}
  Closes        : {LL-id | CAPA-id}, effectiveness check {date}
```
