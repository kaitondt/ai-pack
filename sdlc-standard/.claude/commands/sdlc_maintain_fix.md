---
description: "P9 phase 2 — fix an approved incident: hotfix or scheduled release, code and document changes, the regression test, verification, and the RCA. Usage: /sdlc_maintain_fix [scope note]"
---

# P9 — Fix an incident

Runs only after an approved conclusion from `/sdlc_maintain_intake`.

## Step 1 — Load

`sdlc_project`, then `sdlc_maintenance`, then `sdlc_context_map`.

## Step 2 — Confirm the approval and the route

State back: the incident id, the approved root cause, the route (hotfix or scheduled
release), and the scope. If the route is a hotfix, confirm the approval named in
`{{profile.maintenance.hotfix.approval}}` exists.

No approval → stop. That is C1, and it is what keeps an investigation from turning into an
unreviewed change.

## Step 3 — Emit the context map

Before editing. A maintenance fix that touches one layer of five is the classic source of
the next incident.

## Step 4 — Fix the layer the classification names

- `INC-DEFECT` caused by wrong code → the code, and the tests.
- `INC-DEFECT` caused by a wrong document → the document too. Fixing only the code
  recreates the divergence at the next review. If the document is baselined and the change
  alters what was agreed, that is a CR (BL-02); if it corrects the document to what it
  always should have said, that is a defect correction, recorded as such.
- `INC-DATA` → a reviewed script with a dry-run count, a rollback plan and a record of the
  rows affected. Never an ad-hoc statement typed into a console (C3).
- `INC-ENV` → the configuration change, through the release process, not by hand on a
  server (BL-04).

## Step 5 — Add the regression test

At the level that would have caught it: a UT-level bug gets a UT, not an E2E. This is not
optional (`{{profile.maintenance.regression_test_required}}`) — a fix without it is a fix
that will be made again.

## Step 6 — Verify

Build in `{{profile.system.build.order}}`, typecheck, run the tests covering the change,
and re-run the original reproduction. Real output only (C6).

For a hotfix, state explicitly which parts of the regression cycle were **not** run, so the
reduced testing is a recorded decision rather than an assumption.

## Step 7 — Root cause analysis

Required for `{{profile.maintenance.rca_required_for}}`. Three questions, answered
separately:

1. Why did it happen?
2. **Why was it not caught?** — the check that should have found it, and why it did not.
3. What stops it recurring? — a test, a rule, a hook, a monitoring signal, or an accepted
   risk with a named owner.

Feed (2) into `/sdlc_refine_skill`. An RCA that stops at (1) fixes a bug and changes
nothing.

## Step 8 — Report

```
{INC-ID} — fix
  Route          : {hotfix | release {version}}
  Changed        : code {n} files · documents {n} ({CR id, or "correction"}) · data script {yes|no}
  Regression test: {id} at level {UT|IT|ST}
  Build/tests    : {actual output}
  Not run        : {what was skipped, and why}   ← hotfix only
  RCA            : {1} / {2} / {3}
  Doc debt       : {due date, for a hotfix}      ← BL-06
```

Then `/sdlc_maintain_report`.
