---
description: "P3 — generate detail design per module, and the drift report where implementation diverges from the design. Usage: /sdlc_generate_detail_design MODULE [MODULE ...] or a category/area"
---

# P3 — Generate detail design

## Step 1 — Load

`sdlc_project`, then `sdlc_detail_design`.

## Step 2 — Pre-check per module

Required: approved SC / FC / API / DT documents for the module and a passed P2 gate.
Missing → say which, and stop for that module. Do not reconstruct a missing basic design
from the code.

## Step 3 — Determine the mode

Per module, check whether implementation exists under `{{profile.system.root}}`:

| Code exists | Mode | Output |
|---|---|---|
| no | forward | DD only |
| yes | reconcile | DD + drift report |

Print the mode per module before generating. A module silently treated as forward when code
exists skips the drift analysis, which is the half of P3 that finds defects.

## Step 4 — Generate

Delegate to `sdlc_dd_designer`, one call per module. The DD must be written so a unit test
can be derived from it (DD-04) — that is the P5 entry condition, and it is the most common
thing a thin DD fails.

## Step 5 — Drift analysis (reconcile mode)

Run G-01..G-09. Every drift item gets a verdict decided **against the baselined
requirement**, never against whichever side is easier to change.

Each `CODE-WRONG` item becomes a `BUG-*` with an injection phase (TR-07) and a P4
follow-up. Each `REQ-GAP` is escalated with an owner and a due date.

## Step 6 — Report against the gate

```
P3 — Detail design
  Modules          : {done}/{requested}   mode: forward {n} · reconcile {n}
  DD written       : {n}   testable per DD-04: {n}
  Drift items      : {n}   DOC-WRONG {n} · CODE-WRONG {n} · BOTH-WRONG {n} · REQ-GAP {n} · ACCEPTED {n}
  Follow-ups       : {n} BUG-* raised, {n} escalations open
  Gate {{profile.gates.P3_detail_design.exit}} : {pass|fail}
```

An unresolved drift item is reported by id. "Zero unresolved drift items" is a gate
assertion, not a target to declare.
