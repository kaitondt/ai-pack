---
description: "Trace one defect or incident across every phase and write its traceability dossier: BR → REQ/NFR → design → DD → code (introducing commit, edit history, merge, release) → UT/IT/ST/UAT, with an evidenced injection phase and the V-model reason each earlier check missed it. Read-only except the dossier. Usage: /sdlc-trace-bug <BUG-ID | INC-ID> [module] [symptom / detection record]"
---

# Trace a defect across the phases

## Step 1 — Load

`sdlc-project`, then `sdlc-bug-trace`. Also `sdlc-defect-management` for the defect record
and injection attribution, `sdlc-test-design` for the level model and viewpoints, and
`sdlc-maintenance` for the locator map when the defect came from production.

## Step 2 — Constraint acknowledgement

**Read-only.** No `Write` or `Edit` to code, documents, test cases or any register except the
bug-trace register. The only writes are the dossier and one register row under
`{{profile.paths.bug_traces}}`. Git is read, never moved (C5): no checkout, reset, stash,
fetch or bisect in the working tree. Severity, priority and class are taken as recorded,
never adjusted (C8).

## Step 3 — Restate and fix the reference

Id (from the tracking system — never invented, C7), module, symptom, and the detection record:
phase, level, test id or reporter, environment, **build**, date. Missing detection build →
ask before Step 6.

Read what exists for this id: the defect record, triage report, UAT triage or incident
report, knowledge-base entry, CR reports on the module, register rows. Record the trace
reference: repository per path, `HEAD`, branch, shallow or not.

## Step 4 — Walk the chain

`BR-*` / `DEC-*` / `ASM-*` → `REQ-*` / `NFR-*` → SC/FC/API/DT → DD → code → cases. One
verdict per layer against the layer above — `HOLDS` · `BREAKS` · `SILENT` · `ABSENT` ·
`UNVERIFIED` — and, for every document, the revision in force and whether it was baselined.
Injection = the first `BREAKS` from the top, with the skill's edge cases applied.

An open question stops the walk: record it, propose the `DEC-*` it needs, and go to Step 7 —
there is no injection to trace further.

## Step 5 — Code archaeology

Per defective location: blame candidate → confirmed by `git log -L` → `-S` / `-G` for
omissions and deletions → introducing commit classified by vehicle (original, CR, hotfix,
regression from another fix, refactor, merge, generated) → mainline merge, first tag,
release, pull request → baseline and design before code → every commit since. Then the
history of the governing requirement and design sections and of the test case files.

## Step 6 — Test archaeology

Containment check, and the designated level from the V-model binding. Mark the inheriting
levels `INHERITED`. Detection verdict. For every other check between injection and detection:
the evidence, then the miss code in order — `NOT-PRESENT` first, always. Write the escape
statement. Derive the regression case at the designated level and route each miss to where
its fix belongs.

## Step 7 — Write the dossier

`{{profile.paths.bug_traces}}/{ID}_{MODULE}_trace.md`, from the skill template, in the
language bound to that path. Existing file → append a dated round. Append one row to
`bug-trace-register.csv`. Run the skill's self-check before saving.

## Step 8 — Report and stop

Print the summary block from the skill. If the evidenced injection phase differs from the one
on the defect record, say so and name the record's owner — the record is corrected by them,
not by this command. Then name the next commands without running them:

- a fix is needed → `/sdlc-maintain-fix` (production) or the module's implementation route,
  after its own approval
- a miss belongs in a skill, checklist, hook or gate → `/sdlc-refine-skill` with the dossier
  path
- the behaviour matches the baseline and the stakeholder wants it changed →
  `/sdlc-cr-analyze`
- the gate for the phase is due → `/sdlc-quality-report` reads the bug-trace register
