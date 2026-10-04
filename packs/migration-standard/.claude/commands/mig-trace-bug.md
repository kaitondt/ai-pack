---
description: "Trace one bug across every phase and write its traceability dossier: legacy → LEG → REQ → design → DD → code (introducing commit, edit history, merge, release) → UT/IT/UAT, with the injection phase and the evidenced reason each earlier check missed it. Read-only except the dossier. Usage: /mig-trace-bug <BUG-ID> [module] [symptom / detection record]"
---

# Trace a bug across the phases

## Step 1 — Load

`mig-project`, then `mig-bug-trace`. Also `mig-uat-bug` for the locator map and the
classification set, and `mig-test-design` for the viewpoints the test layer is judged
against.

## Step 2 — Constraint acknowledgement

**Read-only.** No `Write` or `Edit` to product code, documents, test cases or legacy. The
only writes are the dossier and one register row under `{{profile.paths.bug_traces}}`.
Git is read, never moved (C5): no checkout, reset, stash, fetch or bisect in the working
tree.

## Step 3 — Restate and fix the reference

Bug id (from the user — never invented, C7), module, symptom, and the detection record:
phase, level, test id or reporter, environment, **build**, date. Missing detection build →
ask before Step 6.

Read what exists for this id: UAT report, triage report, CR reports on the module, register
rows. Record the trace reference: repository per path, `HEAD`, branch, shallow or not.

## Step 4 — Walk the chain

Oracle → `LEG-*` → `REQ-*` → SC/FC/API/data → DD → code → cases. One verdict per layer
against the layer above: `HOLDS` · `BREAKS` · `SILENT` · `ABSENT` · `UNVERIFIED`.
Injection = the first `BREAKS` from the top, with the skill's edge cases applied. Classify
with the `mig-uat-bug` set.

`SPEC-GAP` stops the walk: record the gap and go to Step 7 — there is no injection to trace
further.

## Step 5 — Code archaeology

Per defective location: blame candidate → confirmed by `git log -L` → `-S` / `-G` for
omissions and deletions → introducing commit classified by vehicle (original, CR,
regression from another fix, refactor, merge, generated) → mainline merge, first tag,
pull request → design-before-code → every commit since. Then the history of the governing
design sections and of the test case files.

## Step 6 — Test archaeology

Containment check and designated level for the injection. Detection verdict. For every
check between injection and detection: the evidence, then the miss code in order —
`NOT-PRESENT` first, always. Write the escape statement. Derive the regression case at the
designated level and route each miss to where its fix belongs.

## Step 7 — Write the dossier

`{{profile.paths.bug_traces}}/{BUG-ID}_{MODULE}_trace.md`, from the skill template, in the
language bound to that path. Existing file → append a dated round. Append one row to
`bug-trace-register.csv`. Run the skill's self-check before saving.

## Step 8 — Report and stop

Print the summary block from the skill, then name the next commands without running them:

- a fix is needed → `/mig-uat-investigate` if the direct cause is not yet agreed, otherwise
  `/mig-uat-fix`
- a miss belongs in a skill, checklist, hook or gate → `/mig-refine-skill` with the dossier
  path
- the behaviour is `ENHANCEMENT` or `LEGACY` and the client wants it changed →
  `/mig-cr-analyze`
