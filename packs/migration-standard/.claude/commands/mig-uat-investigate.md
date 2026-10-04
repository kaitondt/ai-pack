---
description: "P7 phase 1 — investigate a UAT bug WITHOUT fixing anything. Traces target code against design documents against legacy source, classifies the bug, and stops for approval. Usage: /mig-uat-investigate <symptom description>"
---

# P7.1 — Investigate a UAT bug

## Step 1 — Load

`mig-project`, then `mig-uat-bug`.

## Step 2 — Constraint acknowledgement

**This command is read-only.** No `Write`, no `Edit` to product code or documents. It ends
with a conclusion and a proposal, and stops (C1).

## Step 3 — Restate the symptom

Module, action, input, observed result, expected result, environment, reporter. Anything
missing that changes the investigation → ask before starting. A guessed reproduction
investigates the wrong bug.

## Step 4 — Locate

Use the locator map in the skill to resolve module id → design documents, target code,
legacy source, data objects. Resolve paths from the profile. Do not begin with a
repository-wide search.

## Step 5 — Compare the three sources

1. **target code** — what it does now
2. **design documents** — what it was specified to do
3. **legacy source and data objects** — what the old system did

The comparison is the investigation. Every conclusion cites at least one source with a
`file:line` anchor (C2).

## Step 6 — Classify

`CODE-DEFECT` · `DESIGN-DEFECT` · `PARITY-DEFECT` · `SPEC-GAP` · `DATA-ISSUE` ·
`FROZEN-OBJECT` · `NOT-A-BUG` · `ENHANCEMENT`.

`FROZEN-OBJECT` stops here and needs a client decision (C3). `NOT-A-BUG` requires evidence
from all three sources, not one.

## Step 7 — Conclude and stop

```
UAT investigation — {module}
  Symptom        : {restated}
  Classification : {class}
  Direct cause   : {one sentence}
  Evidence
    target : {file}:{line} — {what it does}
    design : {doc id} §{section} — {what it says}
    legacy : {file}:{line} — {what it did}
  Ruled out      : {what and why}
  Proposed fix   : {layers, files, scope}
  Risk           : {what else this touches}
  Regression test: {what it would assert}

Waiting for approval before any change.
```
