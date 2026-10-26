---
description: "Classify a test run's failures into product defect, script error, needs-review and infrastructure, group them by root cause, and produce the triage report — plus, with bug-list, the client-facing bug list. Usage: /sdlc-triage-defects [results path or run id] [bug-list]"
---

# Triage a test run

## Step 1 — Load

`sdlc-project`, then `sdlc-defect-management`.

## Step 2 — Identify the run

Results path, run id, and **the build it ran against**. A triage report that does not
identify its run and build cannot be compared with the next one — and comparison across
runs is how you tell whether the system is converging.

Result formats keep every attempt (retries, re-runs, history). Collapse to one result per TC
ID — the last attempt of this run — before counting anything, and say so in the report.

## Step 3 — Apply the decision tree, in order

1. Infrastructure signature → `INFRA`. Stop; do not analyse further, and do not report the
   rest of the run until it has been re-run.
2. Did the test reach its assertion? No → `SCRIPT-ERROR` or `INFRA`, never a product defect.
3. Does it reproduce? No → flaky → `SCRIPT-ERROR`, quarantined with a reason. Never re-run
   until green and report pass.
4. Does the actual behaviour match the specification? Yes → the case is wrong. No →
   `PRODUCT-DEFECT`.
5. Ambiguous → `NEEDS-REVIEW`, escalate with evidence.

Order matters. Applied out of order, infrastructure failures get logged as product defects
and the report becomes noise nobody trusts.

## Step 4 — Look at the evidence

- `NEEDS-REVIEW`: **open the screenshot or trace.** "Element not found" has two very
  different causes and the log cannot tell them apart.
- `SCRIPT-ERROR`: find the concrete fix — file, line, and what to change. A report that
  says "script error" and stops hands the whole investigation back to the author.
- `PRODUCT-DEFECT`: anchor the expected behaviour to the requirement or design item, and
  assign the **injection phase**. An unanchored product defect will be disputed, and the
  argument costs more than the investigation would have.

## Step 5 — Group by root cause

Twenty instances of one locator pattern is one fix. One rounding difference across every
monetary field is one defect. Report the root cause with its instance list — that is
grouping, which is legitimate, and not merging to reduce a count, which is not (QM-08 §3).

## Step 6 — Report

```
Triage — run {id}, {date}, build {id}
  Total {n}   passed {n}   failed {n}   blocked {n}

  PRODUCT-DEFECT  {n}   → {grouped by root cause}
      {TC ID} · {module} · expected {x} · actual {y} · anchor {doc §} · injection {phase}
  SCRIPT-ERROR    {n}   → {file}:{line} — {fix}
  NEEDS-REVIEW    {n}   → {TC ID} — {what the screenshot shows} — {question}
  INFRA           {n}   → {symptom} — re-run required

  Root causes     : {n} distinct behind {n} failures
  Injection phase : P1 {n} · P2 {n} · P3 {n} · P4 {n}
  Containment     : {%}   target {{profile.quality.targets.phase_containment}}
  Blocked         : {tests not run because of INFRA}
```

Where the code matches the design and the case matches the design but the two disagree with
each other, that is a **design defect** — injection phase P2 or P3, not a code fix.

## Step 7 — The bug list (only with `bug-list`)

After the report above, and only from its classification, write the client-facing bug list
per `sdlc-defect-management` §8: `PRODUCT-DEFECT` rows only, one `BUG-*` per root cause with
its affected TC IDs, written in the deliverable language with the anchor and the copied
evidence, in the format of the `bug_list` template. Unresolved `NEEDS-REVIEW` rows are listed
as excluded, never guessed into the list.
