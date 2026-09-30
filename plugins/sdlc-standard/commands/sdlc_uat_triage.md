---
description: "P8 — triage a client-reported UAT issue into defect, change request or usage question, with the evidence for the classification. Read-only: produces a conclusion and a proposal, no edits. Usage: /sdlc_uat_triage <the report>"
---

# P8 — Triage a UAT report

**Read-only.** This command classifies and concludes. It does not edit code or documents.
Fixing happens after an explicit approval, through `/sdlc_maintain_fix` (or the module's
normal implementation route during the project).

## Step 1 — Load

`sdlc_project`, then `sdlc_test_uat`, then `sdlc_defect_management`.

## Step 2 — Restate the report precisely

Module, action, input, observed, expected, environment, user, record, time. An unclear
report is clarified with the reporter before investigation, not guessed at.

## Step 3 — Establish what the specification says

Read, in this order, with anchors:

1. the baselined `REQ-*` / `NFR-*` covering the behaviour
2. the design documents for the module — SC, FC, API, DT, DD
3. the code path involved

Then read the operational evidence: logs at that timestamp, the correlation id, the record
in question.

## Step 4 — Classify

| Class | Meaning | Route |
|---|---|---|
| **Defect** | the system contradicts the baselined specification | fix under the SLA; `BUG-*` with an injection phase |
| **Change request** | the system matches the specification; the client wants different | `/sdlc_cr_analyze` |
| **Usage / data** | the system is correct; the report came from a misunderstanding, data setup or environment | answer, and record it |
| **Open question** | no baselined document decides this behaviour | product owner decision, then `DEC-*` |

**Show the evidence for the classification** (UA-04): quote the requirement or design item
the behaviour was checked against. A defect classified as a CR without that evidence reads
as a vendor avoiding work; a CR classified as a defect gives away scope nobody agreed.

Where the specification is genuinely ambiguous, say so (UA-05). "The requirement does not
decide this; here is what the system does and here is what changing it would cost" is the
honest answer, and it ends in a `DEC-*` rather than an argument.

## Step 5 — Conclude and stop

```
UAT report — {reporter's id or summary}
  Symptom        : {restated}
  Checked against: REQ {ids} · design {ids} · code {paths}
  Evidence       : {quotes and anchors}
  Classification : {Defect | Change request | Usage | Open question}
  Injection phase: {P1..P4}   (defects only)
  Severity       : {client's assessment}   Priority: {product owner's}
  Proposal       : {what to do}
  Risk           : {of doing it, and of not}
  Ruled out      : {what else was considered, and why not}
```

Then stop. The next step needs an approval, not an assumption.

## Step 6 — Tell the reporter

Same day: what it was classified as, why, and what happens next. A report that disappears
into a backlog without an answer produces three more reports of the same thing.
