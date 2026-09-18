---
description: "CR phase 1+2 — analyse a change request WITHOUT changing anything: as-is from code, design and legacy, impact matrix, classification, then two or more options with a recommendation. Stops at GATE 1. Usage: /mig_cr_analyze <the change request text>"
---

# CR.1 — Analyse a change request

## Step 1 — Load

`mig_project`, then `mig_change_request`.

## Step 2 — Constraint acknowledgement

**This command is read-only.** No `Write`, no `Edit`, no file created — not even a report
(that is `/mig_cr_report`). It ends at GATE 1 and stops (C1).

## Step 3 — Is this a change request or a bug?

| The request says | Route |
|---|---|
| behaves incorrectly, contradicts the spec, differs from the legacy | bug → `/mig_uat_investigate` |
| should now do X, add, remove, change the rule | change request → continue |

Ambiguous → ask. Running a CR as a bug produces a fix that restores the legacy behaviour
the client asked to leave, and it looks correct against every anchor.

## Step 4 — Capture the request

Input: `$ARGUMENTS`. Keep the original wording verbatim — it is quoted in the report and is
the only authority for new behaviour (C2). Empty → ask for the text, and for the module,
the current behaviour, the wanted behaviour, the business reason and any deadline.

A CR id in the arguments is noted for `/mig_cr_report`. Absent, the analysis still runs —
never invent one (C5).

**No usable to-be → stop and ask.** Everything downstream is built on it.

## Step 5 — Analyse (skill Phase 1)

Module and surfaces → as-is from all three sources with anchors → to-be as a verifiable
statement → open questions (walk the seven-line checklist explicitly) → impact matrix over
the whole cascade, unaffected rows included → class, size, regression surface, blockers.

Sources that already disagree before the CR is applied: record as a pre-existing defect,
do not fix (C6), and raise it — it changes which option is safe.

## Step 6 — Options (skill Phase 2)

At least `{{profile.change_request.min_options}}`, each on the six axes, ending in a
recommendation. A frozen object in the way → C3: report the three paths, propose no option
that changes the object.

## Step 7 — GATE 1

```
Change request — {module} {class} {size}

  As-is / to-be    : {one line each}
  Impact matrix    : {n} rows, {n} required, {n} awaiting an answer
  Open questions   : {n}
  Options          : {A} … {B} …
  Recommendation   : {option} — {why, one sentence}
  Risks            : {what else this reaches}
  Pre-existing defects found : {ids or none}

Which option should be implemented, and what are the answers to the open questions?
```

Then stop. Next: `/mig_cr_design` once an option is chosen.
