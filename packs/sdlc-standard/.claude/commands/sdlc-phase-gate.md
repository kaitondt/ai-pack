---
description: "Evaluate a phase gate: entry and exit criteria, traceability, metrics, then baseline the documents the gate covers and record the decision. Usage: /sdlc-phase-gate <P0..P9> [entry|exit]"
---

# Phase gate

The gate is the decision point the whole pack is arranged around. It is evaluated, recorded,
and — when it passes — it **baselines** what it covers.

## Step 1 — Load

`sdlc-project`, then `sdlc-quality-metrics`.

## Step 2 — Choose entry or exit

| Mode | Question |
|---|---|
| `entry` | may this phase start? |
| `exit` | is this phase complete? |

Default to `exit`. Run `entry` before starting a phase whose predecessor's exit was waived
— that is exactly the situation where an entry check earns its keep.

## Step 3 — Evaluate every assertion

From `{{profile.gates.<phase>.<mode>}}`, one line per assertion, each `pass` / `fail` /
`waived`, **with its evidence**. An assertion evaluated from memory is not evaluated.

## Step 4 — Run the mechanical checks

- `/sdlc-trace-check <phase>` — orphans and coverage for this phase's artifacts
- `/sdlc-quality-report <phase>` — the numbers and what they predict
- for P2/P3: the cross-document checks are clean
- for P4: build, lint and typecheck pass
- for P5–P8: the level's coverage checks (T-01..T-10) pass

## Step 5 — Decide

| Outcome | Meaning |
|---|---|
| **Pass** | every assertion holds |
| **Pass with waivers** | an assertion is waived by a named person, with the accepted risk stated |
| **Fail** | one or more assertions do not hold; the phase is not complete |

A waiver names **who** waived it and **what risk was accepted**. "Agreed to proceed" is not
a waiver; it is an absence of one. Waivers accumulate across gates and are re-read at the
next one — a project that waived three criteria at P2 and two at P3 is carrying five
decisions into P4, and the P4 gate should say so.

## Step 6 — Baseline (exit gates that pass)

Append each document the gate covers to `{{profile.constraints.baselined}}` with its
version and approval date, set its version to `{{profile.document.baseline_version}}` and
its `status: baselined`, and record the approval row in its revision history (BL-01).

From that moment those documents change only through a change request. Say so in the report
— the team needs to know the door has closed.

## Step 7 — Record and report

Write the gate record to `{{profile.paths.metrics}}/gates/gate_{phase}_{date}.md`:

```
Gate {phase} {entry|exit} — {date}
  Decision      : PASS | PASS WITH WAIVERS | FAIL
  Assertions
    {assertion} : {pass|fail|waived by {name}} — {evidence}
  Traceability  : orphans up {n} · down {n} · untested {n}
  Metrics       : {the phase's numbers, with their readings}
  Risk forward  : {what the numbers predict for the next phase}
  Waivers       : {each, with who and what risk}
  Carried       : {open defects deferred, with approver and target}
  Baselined     : {n documents} ({list})
  Approved by   : {name}   {date}
```

**Do not report a gate as passed when an assertion could not be evaluated.** Report it as
not evaluated, and say what is needed. A gate that certifies checks it did not run is worse
than no gate, because everything downstream then trusts it.
