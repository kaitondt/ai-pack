---
name: mig_batch_design
description: "P2 category — batch/scheduled job design. Rule families BT-S (structure), BT-R (restart and rerun), BT-E (error and logging), BT-L (legacy fidelity). No UI, no HTTP, no paging. Load for ALL batch-design tasks."
---

# P2 — Batch Design

> Load with `mig_basic_design`. Prerequisite: `mig_project` resolved.

A batch job has no user. Everything a screen document would say about interaction is
replaced by statements about scheduling, volume, failure and recovery.

---

## Section skeleton (BT-S01)

```
# {JobName}（{MODULE}-BT-{NNN}）
  <Revision history>
  <Contents>

## 1  Job overview        purpose, business area, owner
## 2  Trigger             schedule, dependency, manual invocation
## 3  Input               files, tables, parameters, expected volume
## 4  Processing flow     diagram + numbered steps, with commit points
## 5  Output              files, tables, reports, notifications
## 6  Business rules      one row per rule, each with a legacy anchor
## 7  Error handling      per-record vs per-run failure, MSG-*, log format
## 8  Restart and rerun   the section that gets forgotten
## 9  Operations          runtime window, alerting, who is called

## Open Items
```

---

## Scope rules (BT-S)

**BT-S02 — server-side only.** No screens, no HTTP status codes, no request/response
shapes, no pagination. A batch does not page: it streams or it chunks, and chunking is a
commit-point decision, not a UI one.

**BT-S03 — volume is a first-class input.** State expected and peak row counts. A design
that works at the sample size and fails at the real size is a failed design.

**BT-S04 — the runtime window is stated** and the design is checked against it.

---

## Restart and rerun rules (BT-R)

The single most under-specified area in batch migration, and the one operations cares
about most.

- **BT-R01 — restart semantics.** After a mid-run failure, does the job resume from a
  checkpoint, or restart from the beginning? Where is the checkpoint stored?
- **BT-R02 — rerun safety.** Running the job twice on the same input must not double the
  effect. State the mechanism: idempotency key, processed-marker column, or a delete-first
  step.
- **BT-R03 — partial commit policy.** One transaction for the whole run, or per chunk?
  State the chunk size and what a chunk failure leaves behind.
- **BT-R04 — the legacy behaviour is the reference.** Operators have procedures built on
  the legacy behaviour. If the legacy restarted from the beginning and the target
  checkpoints, that is a change to be raised, not a silent improvement (NI-02).

---

## Error and logging rules (BT-E)

- **BT-E01 — two failure classes**, documented separately: a **record** failure (log,
  reject, continue) and a **run** failure (stop, alert). State which errors are which.
- **BT-E02 — the reject destination** is defined: file or table, its layout, and who
  reviews it.
- **BT-E03 — the run log** records start time, end time, input counts, processed counts,
  rejected counts, and outcome. This log is how operations verifies the migration.
- **BT-E04 — every error carries a `MSG-*`** as with online functions, and the message
  text is verbatim from legacy where a legacy equivalent exists.

---

## Legacy-fidelity rules (BT-L)

- **BT-L01 — processing order is preserved** where it affects output, including the input
  file's record order and any sort the legacy applied before processing.
- **BT-L02 — the file layout is copied exactly**: field positions, widths, padding
  characters, alignment, record terminators, header and trailer records.
- **BT-L03 — the calendar rules are copied**: which days it runs, how month-end and
  fiscal-year-end are treated, holiday handling.
- **BT-L04 — the numeric and date conversions** follow the data-design decisions
  (`mig_data_design`), not local judgement.

---

## Self-check

- [ ] trigger, schedule and dependencies stated
- [ ] expected and peak volume stated; runtime window checked
- [ ] flow diagram with explicit commit points
- [ ] restart and rerun behaviour specified, and compared with the legacy behaviour
- [ ] record failures vs run failures separated; reject destination defined
- [ ] run log contents defined
- [ ] file layouts copied exactly, including headers and trailers
- [ ] Open Items present
