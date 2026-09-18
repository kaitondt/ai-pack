---
description: "CR phase 4+5 — implement an approved change request against the UPDATED design documents, update the affected test cases, and verify locally. Run only after /mig_cr_design was approved at GATE 2. Usage: /mig_cr_implement [scope notes]"
---

# CR.3 — Implement and test an approved CR

## Step 1 — Verify GATE 2

There must be an approved document diff in this conversation, or a report in
`{{profile.paths.change_requests}}` whose §4-1 records the updated documents. Without it →
stop and run `/mig_cr_design`. Code written against the old documents is a defect the
moment the new ones are approved (C4).

The exception is a purely cosmetic class touching no documented item — allowed, and the
skip is recorded in report §4-1.

## Step 2 — Load

`mig_project`, `mig_change_request`, `mig_context_map`, `mig_implementation`, plus the
stack rules for the layers involved.

## Step 3 — Emit the context map

Before the first edit. A CR that reaches one layer of five is the classic source of the
next UAT bug; the map is what makes the shared-types node (CM-02) and the data-access node
visible before, not after.

## Step 4 — Implement

- The **updated** documents are the specification.
- The approved option only. A better idea found here goes back through GATE 1 (C1).
- Layer order from the context map. Verify how shared types are produced before editing
  them (CM-01, LR-04).
- Behaviour the CR does not mention keeps its parity rules (IM-01..IM-06).
- Never touch legacy or frozen objects (LR-01, LR-02, C3).
- Message text in the catalogue, with the ids from the updated documents.
- A pre-existing defect found on the way is recorded, not fixed (C6) — route it to
  `/mig_uat_investigate`.

## Step 5 — Update the test cases

The existing cases now describe the old behaviour. Update what the CR contradicts, add
cases for the new behaviour, mark withdrawn cases withdrawn rather than deleting them
(`{{profile.testing.paths.testcase_root}}`). Skipping this leaves the suite asserting the
behaviour the client just paid to remove.

## Step 6 — Verify

`{{profile.target.build.order}}`, then type-check, then the tests covering the change, then
a manual walk-through of the changed flow. Check the regression surface from the analysis.
Real output only (C10).

## Step 7 — Report

```
CR implementation — {CR-ID or module}

  Option implemented : {A|B|C}
  Documents governing: {n} (approved at GATE 2)
  Code changed       : {files}
  Test cases         : {n added} · {n changed} · {n withdrawn}
  Build {pass|fail} · Type-check {pass|fail} · Tests {passed}/{total}
  Manual walk-through: {result}
  Regression checked : {items}   Not checked : {items, why}
  Out of scope found : {ids or none}  (not fixed — C6)

Next: /mig_cr_report
```
