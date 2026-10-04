---
name: sdlc-batch-design
description: "P2 category — batch and scheduled job design. Rule families BT-S (structure and scope), BT-V (volume and window), BT-R (restart and rerun), BT-E (error and reject handling), BT-O (operability). No UI, no HTTP, no paging. Load for ALL batch, scheduled job and file-processing design tasks."
---

# P2 — Batch Design

> Load with `sdlc-basic-design`. Prerequisite: `sdlc-project` resolved.

A batch runs unattended, at night, against more data than anyone tested with, and is
recovered by an operator who did not build it. Everything in this skill exists because one
of those four facts was ignored.

---

## Section skeleton (BT-S01)

```
# {JobName}（{MODULE}-BT-{NNN}）
  <Revision history>  <Review record>  <Contents>

## 1  Job information      purpose, schedule, trigger, dependencies, owner
## 2  Input               files, tables, queues — with layouts and volumes
## 3  Processing flow     diagram + step table, with commit points marked
## 4  Business rules
## 5  Output              files, tables, notifications
## 6  Volume and window   expected, peak, growth, runtime budget
## 7  Restart and rerun
## 8  Error and reject handling
## 9  Operability         logs, exit codes, monitoring, manual intervention

## Open Items
```

**BT-S02 — server-side only.** No screens, no HTTP status codes, no paging parameters. A
batch does not page; it streams or it chunks, and that is a §3 decision.

**BT-S03 — the schedule is a specification**: cron expression or trigger, time zone,
calendar (working days, month-end, holidays), and what happens when the previous run has
not finished.

**BT-S04 — dependencies are named**: which jobs must have completed, which files must have
arrived, and the behaviour when they have not. "It runs at 02:00" is not a dependency
statement; "it runs after `KK0010BT` completes, or waits until 04:00 then fails" is.

---

## Volume and window (BT-V)

State four numbers, each with its `ASM-*` if it is not measured:

| Number | Why it matters |
|---|---|
| Expected input volume | the design target |
| Peak volume (month-end, campaign, year-end) | the case that actually fails |
| Growth at +3 years | when the design stops working |
| Runtime budget | the window between the upstream dependency and the downstream one |

**BT-V01 — design and measure against peak, not average.** The month-end run is the one
that overruns its window and delays the morning.

**BT-V02 — state the behaviour on overrun**: continue past the window, abort, or checkpoint
and resume tomorrow. This decision belongs to the ops owner and belongs in the design.

---

## Processing flow (§3)

Top-down flowchart per `{{profile.document.diagram_constraints}}`, plus the step table.

**BT-R01 — commit points are marked in the diagram.** A batch that commits once at the end
cannot restart from the middle, and it holds locks for its entire runtime. A batch that
commits per row is slow and leaves partial results. State the chunk size and why.

**BT-R02 — the unit of work is named**: what a "record" is for this job, and what it means
for one to succeed or fail independently.

---

## Restart and rerun (BT-R) — §7

The section most often omitted and most often needed at 03:00.

| Question | Must be answered |
|---|---|
| Restart | after a mid-run failure, does it resume from the last commit or start over? |
| Rerun | may it be run twice on the same input, and what happens if it is? |
| Idempotency | which key makes a repeat safe (FD-T03) |
| Partial output | what happens to rows already written, and files already produced |
| Reprocessing | how a specific date, batch or record is re-run deliberately |
| Manual skip | may an operator skip a bad record, and how is that recorded? |

**BT-R03 — "do not rerun" is not an answer.** Someone will. Specify what happens.

---

## Error and reject handling (BT-E) — §8

**BT-E01 — separate record failures from run failures.** One malformed row out of a
million should not abort the run — unless the design says it should, for a stated reason.
State the threshold at which accumulated record failures become a run failure.

**BT-E02 — rejects go somewhere with a name**: a reject file or table, with the original
record, the reason, and the timestamp. A reject that only exists in a log line is a reject
nobody will reprocess.

**BT-E03 — the reject lifecycle is specified**: who reviews them, how they are corrected,
and how they re-enter processing.

**BT-E04 — every failure mode has an exit code and a log line** an operator can act on.
"Job failed" is not actionable; "input file `ORD_20260412.csv` failed layout validation at
line 4,812, exit 12" is.

**BT-E05 — notification is designed**: who is told, through what channel, for which
outcomes (success, partial, failure), and what the message contains.

---

## Operability (BT-O) — §9

- Log start, end, elapsed time, and counts: read, processed, skipped, rejected, written.
  These counts are how operations validates the run and how P9 investigations start.
- One correlation id per run, present in every log line.
- The runbook entry (`{{profile.paths.runbook}}`): how to check whether it ran, how to
  restart it, how to reprocess, and who to escalate to.
- Monitoring: what "healthy" looks like, and the alert when it is not — including the
  alert for a job that did **not** run at all. A silent job is the failure nobody notices
  for a week.

---

## File interfaces in a batch

When the job reads or writes files, the layout is specified exactly: encoding, line
ending, delimiter or fixed offsets, header, trailer, control totals, decimal and date
formats, and the naming pattern with its date component.

Also state, because these three cause most file-integration incidents: the empty-file
convention, the duplicate-file behaviour, and the late-file behaviour.

---

## Self-check

- [ ] schedule with time zone, calendar and overlap behaviour
- [ ] dependencies named, with the behaviour when unmet
- [ ] expected, peak and +3-year volumes stated, with the runtime budget
- [ ] commit points marked in the flow; chunk size stated
- [ ] restart, rerun, idempotency, partial output and reprocessing all answered
- [ ] record failures separated from run failures, with a threshold
- [ ] rejects have a destination, a reason and a lifecycle
- [ ] exit codes, log counts and correlation id specified
- [ ] alert defined for both failure and non-execution
- [ ] file layouts exact, including empty, duplicate and late-file behaviour
- [ ] Open Items present
