---
description: "Check the traceability register: orphan detection in both directions, V-model coverage per level, and the phase-gate traceability assertions. Run before declaring any phase complete. Usage: /sdlc-trace-check [phase, module id, or nothing for everything]"
---

# Traceability check

## Step 1 — Load

`sdlc-project`. Read `{{profile.paths.traceability}}` and the artifacts on disk.

## Step 2 — Reconcile the register against reality

The register is not trusted on its own. For the scope requested:

- every `BR-*` in the business requirements has a row
- every `REQ-*` and `NFR-*` in the SRS has a row
- every design document on disk appears as a `design_id`
- every DD on disk appears as a `detail_id`
- every UT / IT / ST / UAT document contributes its `test_ids`

A file on disk with no row, or a row referencing a file that does not exist, is a finding.

## Step 3 — Orphan detection

| Kind | Meaning | Severity |
|---|---|---|
| Upward orphan | artifact with no requirement or CR ancestor | Critical — unrequested scope (RS-06) |
| Downward orphan | a baselined requirement with no descendant | Critical — missed scope |
| Untested | a requirement with design and code but no case at its V-model level | Critical at that level's gate |

List them by id. Do not summarise as a count only: the ids are what the user acts on.

A row whose ancestor is a `CR-*` id is **not** an upward orphan, provided the matching
report exists under `{{profile.paths.change_requests}}`. A `CR-*` ancestor with no report on
disk is a Critical finding — that is the shape unrequested work takes once someone has
learned the register accepts CR ids.

## Step 4 — V-model coverage

Per `{{profile.testing.levels}}`, check each binding separately:

| Level | Assertion |
|---|---|
| UT | every detail-design rule has a case |
| IT | every flow and interface has a case |
| ST | every `REQ-*` and `NFR-*` has an executed case |
| UAT | every acceptance criterion has a scenario |

A requirement covered at UT but not at ST is **not** covered: unit tests verify the detail
design, not the requirement. This is the check that catches a project confusing test count
with coverage.

## Step 5 — Gate assertions

Evaluate `{{profile.gates.*}}` for the requested phase (or all phases), one line per
assertion, each `pass` or `fail` with the evidence.

## Step 6 — Report

```
Traceability
  Rows {n}   (todo {n} · in-progress {n} · done {n} · blocked {n} · deferred {n} · open-question {n})

  Coverage
    BR-* covered by REQ-*        : {n}/{n}
    REQ-* realised in design     : {n}/{n}
    design implemented in code   : {n}/{n}
    verified at UT / IT / ST / UAT : {n}/{n} · {n}/{n} · {n}/{n} · {n}/{n}

  Orphans
    upward   : {ids}
    downward : {ids}
    untested : {ids, with the level that is missing}

  Gates
    {phase} : {assertion} — {pass|fail}

  Verdict : {phase} {COMPLETE|INCOMPLETE}
```

A `deferred` row without a decision reference is a Critical finding, not a closed item.
