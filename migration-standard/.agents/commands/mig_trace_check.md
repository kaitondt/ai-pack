---
description: "Check the traceability register: orphan detection in both directions, phase-gate assertions, and coverage per phase. Run before declaring any phase complete. Usage: /mig_trace_check [phase, module id, or nothing for everything]"
---

# Traceability check

## Step 1 — Load

`mig_project`. Read `{{profile.paths.traceability}}` and the artifacts on disk.

## Step 2 — Reconcile the register against reality

The register is not trusted on its own. For the scope requested:

- every `LEG-*` in the inventory has a row
- every `REQ-*` in the BRD has a row
- every design document on disk appears as a `design_id`
- every DD on disk appears as a `detail_id`
- every UT/IT document contributes its `test_ids`

A file on disk with no row, or a row referencing a file that does not exist, is a finding.

## Step 3 — Orphan detection

| Kind | Meaning | Severity |
|---|---|---|
| Upward orphan | artifact with no legacy or requirement ancestor | Critical — likely invented (NI-01) |
| Downward orphan | in-scope legacy artifact with no descendant | Critical — likely missed scope |

List them by id. Do not summarise as a count only: the ids are what the user acts on.

A row whose ancestor is a `CR-*` id is **not** an upward orphan, provided the matching
report exists under `{{profile.paths.change_requests}}`. A `CR-*` ancestor with no report
on disk is a Critical finding — that is the shape an invention takes once someone has
learned the register accepts CR ids.

## Step 4 — Gate assertions

Evaluate `{{profile.gates.*}}` for the requested phase (or all phases), one line per
assertion, each `pass` or `fail` with the evidence.

## Step 5 — Report

```
Traceability
  Rows {n}   (todo {n} · in-progress {n} · done {n} · blocked {n} · excluded {n} · spec-gap {n})

  Coverage
    LEG-* covered by REQ-*      : {n}/{n}
    REQ-* realised in design    : {n}/{n}
    design implemented in code  : {n}/{n}
    design verified by a test   : {n}/{n}

  Orphans
    upward   : {ids}
    downward : {ids}

  Gates
    {phase} : {assertion} — {pass|fail}

  Verdict : {phase} {COMPLETE|INCOMPLETE}
```

An `excluded` row without a reason is a Critical finding, not a closed item.
