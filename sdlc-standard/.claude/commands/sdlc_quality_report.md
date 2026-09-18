---
description: "Produce the quality metrics report for a phase gate: review density, defect density, phase containment, test density and coverage, escapes, and the defect S-curve, with what they predict for the next phase. Usage: /sdlc_quality_report [phase, or nothing for the project to date]"
---

# Quality report

## Step 1 — Load

`sdlc_project`, then `sdlc_quality_metrics`.

## Step 2 — Collect from artifacts

Never from memory or from a previous report's numbers:

| Metric | Source |
|---|---|
| Review density | the review record in each document (DS-03) and the review reports |
| Defect density | the defect register, grouped by injection phase |
| Phase containment | the register: injection phase vs found phase — where `{{profile.paths.bug_traces}}/bug-trace-register.csv` has a trace for a defect, its evidenced injection phase outranks the one assigned at triage; report how many were traced |
| Test density | case and checkpoint counts (`sdlc_test_lifecycle` §4) |
| Coverage | the test runner's report, from a named run and build |
| Escapes | the register: first found in P8 or P9 |
| S-curve | the register: found and closed dates, cumulative |

State the population, the date and the method for every number (QM-01). A metric that
cannot be recomputed by someone else is an assertion, not a measurement.

## Step 3 — Compare against targets and interpret

Each number against `{{profile.quality.targets}}`, with a **reading**, not just a verdict:

- density near zero → the review did not happen, or the reviewer lacked domain knowledge
- density far above target → the upstream document was not ready
- a module well below the defect-density floor → under-tested, and the likely UAT surprise
- containment clustered off the diagonal → the phase that is leaking, named
- found-curve still rising → the phase is not finished, whatever the schedule says

## Step 4 — Say what it predicts

The section that makes the report worth producing. One or two sentences of the form:

> Modules X and Y have half the defect density of the rest at the same size. Either they
> are genuinely simpler, or they are under-tested — and their UT case counts suggest the
> second. Expect the P8 surprises there.

A report that lists numbers without saying what they predict is a status update, and the
gate cannot use it.

## Step 5 — Write and report

Append to `{{profile.quality.metrics_report}}`, and print:

```
Quality — {phase}, {date}
  Review density        {value}   target {target}   {reading}
  Design defect density {value}   target {target}   {reading}
  Code defect density   {value}   target {target}   {reading}
  Phase containment     {value}   target {target}   {reading}
    matrix              {injected × found}
  Test density          {value}   target {target}
  Coverage              line {x} / branch {y}   run {id}, build {id}
  Escapes to date       {value}   target {target}
  Curve                 found {n} / closed {n} — {shape}
  Not measured          {which, and what is needed}
  Predicts              {the sentence from step 4}
```

**Never adjust a number to meet a target** (QM-08). A metric that could not be produced is
reported as not produced. The gate is downstream of these numbers; tuning them disables it
silently, and that is the one failure nobody notices until the client does.
