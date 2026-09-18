---
description: "P7 phase 2 — apply an approved UAT fix across the layers the classification names, add a regression test, and verify locally. Run only after /mig_uat_investigate was approved. Usage: /mig_uat_fix [scope notes]"
---

# P7.2 — Fix an approved UAT bug

## Step 1 — Verify the approval

There must be an approved investigation conclusion in this conversation, with a
classification and a proposed fix. Without it → stop and run `/mig_uat_investigate` first.
Fixing an unclassified symptom treats the visible layer, not the cause.

## Step 2 — Load

`mig_project`, `mig_uat_bug`, `mig_context_map`, `mig_implementation`.

## Step 3 — Emit the context map

The classification names the owning layer, but the fix rarely stops there. A
`DESIGN-DEFECT` changes the document **and** the code; a `PARITY-DEFECT` changes both and
usually its siblings too.

## Step 4 — Apply

Within the approved scope only. Never modify legacy or frozen objects (C3). Follow the
parity rules IM-01..IM-06.

Check whether the same defective pattern exists in sibling modules — in a migration,
a parity defect is usually systematic rather than local. Report the siblings; fix them
only if the user extends the scope.

## Step 5 — Regression test

Add a test that fails before the fix and passes after. A UAT bug without a regression test
returns.

## Step 6 — Verify

Build in `{{profile.target.build.order}}`, type-check, run the covering tests, and re-run
the manual reproduction. Report real output only (C6).

## Step 7 — Report

```
UAT fix — {BUG-ID or module}
  Classification : {class}
  Files changed  : {list}
  Docs updated   : {list}
  Regression test: {id} — {pass}
  Build {pass|fail} · Type-check {pass|fail} · Tests {passed}/{total}
  Reproduction re-run : {result}
  Sibling modules with the same pattern : {list, not fixed unless scoped in}

Next: /mig_uat_report
```
