---
description: "P3 — generate detail design per module and, where code exists, the BD-vs-code GAP report. Usage: /mig_generate_detail_design MODULE [MODULE ...]"
---

# P3 — Generate detail design and GAP report

## Step 1 — Load

`mig_project`, then `mig_detail_design`.

## Step 2 — Resolve modules

Modules from the argument, space-separated. No argument → ask which modules; do not
default to all, since a full-repository GAP run is long and usually not what was wanted.

Validate each against `{{profile.ids.module_pattern}}`.

## Step 3 — Per module, determine the mode

Implementation present under `{{profile.target.root}}` → **reconcile** mode.
Absent → **forward** mode.

## Step 4 — Forward mode

Generate `DD-{MODULE}-{NNN}` from the module's SC, FC and API documents plus the legacy
source. Name real repository paths in the component map (DD-01).

## Step 5 — Reconcile mode

Run G-01..G-08. For each divergence, decide the verdict **against the legacy source** —
not against whichever side is easier to change (this is the rule that keeps the GAP
analysis honest).

Write `{{profile.paths.gap_reports}}/GAP_{MODULE}_{YYYYMMDDHHmm}.md` only when gaps exist.

Then generate or update the DD to reflect the corrected position.

## Step 6 — Report

```
P3 — Detail design
  {MODULE}  mode {forward|reconcile}  DD {written}  GAP {n}
     DOC-WRONG {n} · CODE-WRONG {n} · BOTH-WRONG {n} · SPEC-GAP {n} · ACCEPTED {n}
  ...
  CODE-WRONG items requiring P4 follow-up : {list}
  SPEC-GAP items requiring a client decision : {list}
  Gate {{profile.gates.P3_detail_design}} : {pass|fail}
```

`SPEC-GAP` items are presented to the user for decision before the phase is called done.
