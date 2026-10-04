---
description: "CR phases 4+5 — implement the approved option against the updated design documents, update the test cases, and verify. Usage: /sdlc-cr-implement [scope note]"
---

# CR — Implement and test

Runs only after GATE 2.

## Step 1 — Load

`sdlc-project`, then `sdlc-change-request`, then `sdlc-context-mapping`, then
`sdlc-implementation`.

## Step 2 — Confirm GATE 2 passed

State back the approval: who approved the document diff, and when. No approval → stop and
re-print the diff table.

## Step 3 — Emit the context map

Before editing. A CR that edits one layer of five is the classic source of the next UAT
defect (CM-02, CM-03).

## Step 4 — Implement the approved option only

- The **updated** documents are the specification. Code matching the old document is a
  defect from the moment GATE 2 passed.
- A better idea found mid-implementation goes back through GATE 1. It does not get applied
  quietly (C6).
- Behaviour the CR does not mention keeps its existing specification (IM-05).
- A schema change carries its migration, its rollback and its deployment coupling.
- Message text lives in the catalogue; its `MSG-*` ids match the **updated** documents.

## Step 5 — Update the test cases

The existing cases now describe the old behaviour. They are part of the change:

- update the cases the CR contradicts
- add cases for the new behaviour
- mark withdrawn cases as withdrawn, do not delete them (`sdlc-test-artifact-lifecycle`)
- update the automated specs that assert the old behaviour

A CR that changes behaviour and leaves the suite green has a suite that is no longer
testing anything.

## Step 6 — Verify

`{{profile.system.build.order}}`, typecheck, the tests covering the change, and a manual
walk-through of the changed flow. Then the regression surface from Phase 1 step 7: state
what was checked and what was not.

Real output only (C10). A pre-existing failure unrelated to the CR is reported as
pre-existing, with the evidence that it predates the change.

## Report

```
CR {id} — implementation
  Files            : created {n} · modified {n}   layers: {list}
  Context map      : {checked}/{total}   unchecked: {list}
  Test cases       : added {n} · changed {n} · withdrawn {n}   automated specs {n}
  Build            : {actual output}
  Tests            : {passed}/{total}
  Manual walk      : {result}
  Regression       : checked {list}   not checked {list, with why}
  Out of scope found : {n}   → {BUG-* raised}
```

Then `/sdlc-cr-report`.
