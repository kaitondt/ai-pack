---
description: "P9 phase 3 — write the incident report into 09.maintenance/, append a knowledge-base entry, and record the preventive action. An existing report for the same incident is appended to, never overwritten. Usage: /sdlc-maintain-report [path to an existing report]"
---

# P9 — Incident report

## Step 1 — Load

`sdlc-project`, then `sdlc-maintenance`.

## Step 2 — Get the incident id

From the tracking system (C4). Never invent one, never derive it from a module id, never
number it from the count of files in the directory. No id → ask.

## Step 3 — Locate or create the file

`{{profile.paths.maintenance}}/{INC-ID}_{MODULE}_{short-slug}.md`, in the language bound to
that path.

An existing file for the same incident is **appended to** as a new round, never
overwritten. The history of what was tried is the point — and a second round means the
first conclusion was wrong, which is information the next investigator needs.

## Step 4 — Write the six sections

Per the template in `sdlc-maintenance` Phase 3: summary with the SLA timestamps, root cause
with anchors and injection phase, solution, verification with real output, prevention, and
the knowledge-base entry.

**Section 5 is the one that pays.** A report with a fix and no preventive action documents
an incident; a report with a preventive action reduces the next one.

## Step 5 — Append to the knowledge base

One paragraph in `{{profile.maintenance.knowledge_base}}`: symptom, cause, resolution —
written so the next person finds it by searching **the symptom**, not the cause. They will
not know the cause; that is why they are searching.

## Step 6 — Update the registers

- the defect/incident register: closure, root cause, injection phase
- `{{profile.paths.traceability}}`: the regression test added
- `{{profile.paths.risk_register}}`: a new `RSK-*` where the incident revealed one
- the deferred-defect list, if this incident was one of them

## Step 7 — Report

```
{INC-ID} — report
  File           : {path}   round {n}
  SLA            : acknowledged {x} (target {y}) · resolved {x} (target {y}) — {met|breached}
  Class/severity : {INC-?} / {S?}
  Injection      : {phase}
  Prevention     : {action}   owner {name}   due {date}
  KB entry       : added
  Doc debt       : {closed | due {date}}
```

Print the report path for the user. A report nobody can find is a report that will be
rewritten from scratch next time.
