---
description: "P1 — generate the requirements chain from the P0 catalogue: BRD, then TSD, then FRD, with REQ-* ids traced to LEG-* ids. Usage: /mig_generate_requirements [brd|tsd|frd; omit for all three in order]"
---

# P1 — Generate the requirements chain

## Step 1 — Load

`mig_project`, then `mig_requirements`.

## Step 2 — Pre-check

Required inputs: `{{profile.paths.requirements}}/legacy-inventory.md` and
`requirement.md`. Missing → stop, tell the user to run `/mig_analyze_legacy`.

Confirm the P0 gate passed. Generating requirements from an incomplete catalogue produces
requirements that are wrong about scope.

## Step 3 — Generate in order

`BRD → TSD → FRD`. Each reads the previous. Delegate to `mig_requirements_writer`, one
document per call for the BRD and TSD; the FRD in batches by business area.

If the user asked for a single document, verify its predecessors exist and are current;
regenerating a predecessor invalidates this one.

## Step 4 — Cross-check

Run R-01..R-06 from `mig_requirements`. Report the results as a table. Every failure is
listed with the specific ids involved — not a count.

## Step 5 — Update traceability and report

Write the `REQ-*` rows, then:

```
P1 — Requirements
  BRD : {n} requirements   ({n} As-is, {n} Adapted, {n} New)
  TSD : {n} decisions recorded
  FRD : {n} modules        ({n} with acceptance criteria)
  Cross-checks R-01..R-06  : {pass|fail each}
  Uncovered LEG-* (missed scope) : {n}  ← Critical if > 0
  Gate {{profile.gates.P1_requirements}} : {pass|fail}
```
