---
name: mig_uat_bug
description: "P7 — UAT bug workflow in three strictly separated phases: investigate, fix, report. Contains the standing constraints, the locator map from module id to documents/code/legacy, the bug classification table, and the report template. Load for ALL UAT investigation, fix and reporting tasks."
---

# P7 — UAT Bug Workflow

> Prerequisite: `mig_project` resolved.
> Three phases, strictly separated. **Do not merge them.**

```
Phase 1  INVESTIGATE  -> conclusion + proposal, then STOP for approval
Phase 2  FIX          -> only after explicit approval
Phase 3  REPORT       -> written to {{profile.paths.uat_reports}}
```

---

## Standing constraints

**C1 — investigation stops at the conclusion.** Phase 1 ends with a root cause and a
proposal. No `Write`, no `Edit` to product code or documents during Phase 1. Read-only
tools only. Proceed to Phase 2 only on an explicit approval from the user.

**C2 — every conclusion is anchored.** A claim that the code is right or wrong must cite
at least one of: current target source, the approved design documents, the legacy source.
If all three are silent on the disputed behaviour, the classification is `SPEC-GAP`: ask,
do not decide (NI-01, NI-05).

**C3 — frozen objects stop the fix.** If the direct cause is inside a read-only data object
(`{{profile.constraints.stored_procedures_readonly}}`), stop and report it as needing a
client decision (LR-02). Do not implement a workaround and present it as the fix.

**C4 — the bug id comes from the user.** Reports are named by the client's or tester's bug
id. Never invent one, never derive it from a module id or from the count of existing
files. Phase 1 can run without it; Phase 3 cannot — ask.

**C5 — verify the repository facts before relying on them.** Whether a type file is
generated or hand-written, whether a script exists, which repository or submodule a path
belongs to. Check, do not assume (LR-04, LR-06).

**C6 — report only what actually ran.** Build and test output in the report is real output
from a real run. A failing test is reported as failing, with its output.

**C7 — language and location.** Reports go to `{{profile.paths.uat_reports}}` in the
language bound to that path by `{{profile.language.by_path}}`.

---

## Phase 1 — Investigate

1. **Reproduce.** Restate the reported symptom precisely: module, action, input, observed,
   expected. An unclear report is clarified before investigation, not guessed at.
2. **Locate** via the locator map below. Do not start with a repository-wide search.
3. **Read the target code** for the path involved.
4. **Read the design documents** for the same module: SC, FC, API, DD.
5. **Read the legacy source** for the equivalent behaviour, plus the data object.
6. **Classify and conclude** using the table below.
7. **Stop.** Present the cause, the evidence with anchors, the proposal, and the risk.

### Locator map

Derive concrete paths from the profile before starting:

| From | To | Path |
|---|---|---|
| module id | screen design | `{{profile.paths.design_root}}/{screen dir}/…{MODULE}-SC-…` |
| module id | function design | `{{profile.paths.design_root}}/{function dir}/…{MODULE}-FC-…` |
| module id | interface design | `{{profile.paths.design_root}}/{interface dir}/…{MODULE}-API-…` |
| module id | detail design | `{{profile.paths.detail_design}}/…{MODULE}…` |
| module id | target code | `{{profile.target.root}}` — feature folder for the module |
| module id | legacy screen | `{{profile.legacy.ui_source}}` — the form for this module |
| module id | legacy logic | `{{profile.legacy.logic_source}}` |
| data object | definition | `{{profile.legacy.db_source}}` |
| module id | traceability rows | `{{profile.paths.traceability}}` |

### Classification

| Class | Meaning | Owner |
|---|---|---|
| `CODE-DEFECT` | code contradicts an approved design | implementation |
| `DESIGN-DEFECT` | design contradicts the legacy behaviour | design |
| `PARITY-DEFECT` | both design and code diverge from the legacy | design + implementation |
| `SPEC-GAP` | no source defines the behaviour | client decision |
| `DATA-ISSUE` | test data or environment, not the software | environment |
| `FROZEN-OBJECT` | cause is inside a read-only object | client decision |
| `NOT-A-BUG` | behaviour matches design and legacy | report back with evidence |
| `ENHANCEMENT` | works as specified; the client wants different | change request |

`NOT-A-BUG` needs the strongest evidence, not the weakest: cite the design, the legacy,
and the code.

---

## Phase 2 — Fix

Only after explicit approval, and only within the approved scope.

- Fix the layer the classification names. A `DESIGN-DEFECT` requires the document to
  change too — fixing only the code recreates the divergence at the next review.
- Load `mig_context_mapping` before editing; a UAT fix that touches one layer of five is the
  classic source of a follow-up bug.
- Never modify legacy or frozen objects.
- Verify: build in the mandated order, type-check, and run the tests that cover the change.
- Add a regression test for the defect. A UAT bug without a regression test will return.

---

## Phase 3 — Report

File: `{{profile.paths.uat_reports}}/{BUG-ID}_{MODULE}_{short-slug}.md`

An existing file for the same bug id is **appended to** with a new investigation round,
never overwritten — the history of what was tried is the point.

```markdown
# {BUG-ID} — {short title}

## 1. Summary
Module, reported by, date, symptom, expected behaviour, severity, classification.

## 2. Root cause
The direct cause, with anchors: target code path:line, design document id and section,
legacy path:line. Include what was ruled out and why.

## 3. Solution
What was changed, file by file. Documents updated. Deviations approved, with references.
Alternatives considered and rejected, with reasons.

## 4. Verification
Actual output: build, type-check, tests run and their results, the manual reproduction
re-run. Real output only (C6).

## 5. Follow-up
Regression test added. Related modules that share the defective pattern. Open questions.
```

When the client needs to know where the defect entered, which commit put it there, or why
UT and IT did not catch it, run `/mig_trace_bug` after this report — `mig_bug_trace` builds
that dossier from the conclusion here instead of repeating the investigation.
