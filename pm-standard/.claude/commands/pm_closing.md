---
description: "Run project closing: deliverable acceptance, handover, disposition of every open item, contract closure, the final report against the charter, resource release, archive and the PIR schedule. Usage: /pm_closing [step]"
---

# Project closing

## Step 1 — Load

`pm_project`, then `pm_closure`. Agent: `pm_closer`.

## Step 2 — Acceptance, per deliverable (CL-01)

For every `{{profile.scope.deliverables}}` entry: verified against the criteria agreed at
planning, by the named acceptor, on a date, with evidence and a verdict.

**Accepted with conditions is a distinct state** and must not blur into accepted. Each
condition becomes an `ACT-*` tracked to closure, and the final-invoice condition states which
states satisfy it.

Where criteria were never agreed in writing, say so plainly, negotiate now, and record that it
happened — it is the lesson: the acceptance argument was created at planning time, by an
omission.

## Step 3 — Handover (CL-02)

`{{profile.closing.handover.items}}`, each verified behaviourally rather than documentarily:
the receiving team has built and deployed it themselves, someone outside the project followed
the runbook successfully, training attendees passed a competence check.

Include the known issues and workarounds, including the embarrassing ones. Every undisclosed
known issue becomes an incident the receiving team hits blind, and costs more trust than the
disclosure would have.

## Step 4 — Dispose of every open item (CL-03)

Defects · CRs · risks · actions · assumptions. Each: closed, deferred with an approver and a
target, transferred with a named owner in the receiving organisation, or accepted with the
impact stated. Nothing is left undefined.

## Step 5 — Contract closure (CL-04)

Final invoice on its stated condition with acceptance evidence · all milestone payments
reconciled · warranty scope written, including what it does **not** cover · subcontractor
closure · licences transferred or terminated · claims and disputes settled or explicitly
recorded as open.

## Step 6 — Final report (CL-05)

Measured against the **charter**, not against the last re-baselined plan, with the baseline
history in between. Section 6 answers the question that matters most for the next project: of
everything that went wrong, how much was in the risk register before it happened?

Gather client feedback **before** writing the report, not after.

## Step 7 — Lessons and actuals (CL-07, CL-09)

Run `/pm_lessons` for the closing sweep. Then record estimate versus actual per work package —
the single most valuable artifact closing produces, and the first one cut when the project is
busy. Cutting it means the next bid is produced with exactly the information this one had.

## Step 8 — Release and archive (CL-06)

People with dated release records, accesses revoked, licences transferred, environments
decommissioned. Then archive: baselines and their history, approved deliverables, all
registers, reports, acceptance records, contracts and amendments, lessons, and the
estimate-versus-actual data.

## Step 9 — Schedule the PIR

`{{profile.closing.post_implementation_review_after_days}}` days out, with the users, against
the charter's objective metrics. It is the only feedback loop that reaches past acceptance —
where the difference between "delivered" and "worked" becomes visible.

## Report

```
Closing — {project}, {date}
  Deliverables   : {n} accepted · {n} with conditions ({n} open) · {n} rejected
  Handover       : {n}/{n} items, {n} verified by demonstration
  Open items     : defects {n} · CRs {n} · risks {n} · actions {n} · assumptions {n}
                   all with a disposition? {yes | which are not}
  Contract       : invoice {status} · warranty {scope} · obligations {n}
  Final report   : objectives met {n}/{n} — {which were not, and why}
  Foresight      : {issues that were risks first}/{all issues}
  Lessons        : {n}, all with an owner and a destination? {yes|no}
  Est. vs actual : recorded for {n}/{n} work packages
  Resources      : released {n}/{n}, accesses revoked {n}/{n}
  Archive        : {complete | missing: …}
  PIR            : scheduled {date}
  Closure        : approved by {names, dates} | pending
```
