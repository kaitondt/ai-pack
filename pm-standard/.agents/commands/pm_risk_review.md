---
description: "Periodic risk and issue review: re-score, check triggers, verify responses are happening, close what is gone, age the issues, and reconcile contingency against remaining exposure. Usage: /pm_risk_review [weekly|monthly]"
---

# Risk and issue review

Runs on `{{profile.risk.review_cadence}}`. Shorter than an assessment: this checks that the
register is still true and that the planned responses are actually happening.

## Step 1 — Load

`pm_project`, then `pm_risk`.

## Step 2 — Re-score and check triggers

For each open risk: has probability or impact moved? Has its trigger fired (RK-10)? Is the
trigger date approaching?

A risk whose probability rises as its trigger date nears is the normal case — watching that
movement is most of the value of keeping a register at all.

## Step 3 — Verify the responses are happening

For each mitigation with an action and a date: was it done? A register full of planned
mitigations that were never executed is the most common way a project holds a risk register
and still gets surprised.

Where a response was not executed, that is either an `ISS-*` or an implicit acceptance. Name
which, and if it is acceptance, get it approved (RK-08).

## Step 4 — Process materialised risks

Risk → issue: create the `ISS-*`, cite the `RSK-*` as its ancestor (RK-01), log any
contingency drawdown with its approver and the remaining balance (CT-08), and close the risk
as materialised — never silently delete it.

## Step 5 — Age the issues (RK-11, DA-05)

Report age, not just count. Anything past its SLA in `{{profile.risk.issue_sla_hours}}`
escalates to the next level automatically, as a fact rather than a complaint.

An issue open past two escalation levels appears in the next monthly report whether or not it
has since been resolved.

## Step 6 — Reconcile and report

```
Risk review — {date}
  Profile        : high {n} (was {n}) · medium {n} · low {n}
  New            : {ids}        Closed: {ids, with why — passed | avoided | materialised}
  Exposure moved : {ids, from → to, why}
  Triggers fired : {ids, and what was executed}
  Approaching    : {ids with trigger dates inside the next period}
  Responses due  : {n} due this period, {n} done, {n} not done — {ids}
  Materialised   : {RSK → ISS}, contingency drawn {amount}
  Contingency    : {used}/{total} ({x}%) — remaining covers {which risks}, short on {which}
  Issues         : open {n}, oldest {n} days, past SLA {n} — escalated {ids}
  Foresight      : {issues this period that were risks} / {all issues this period}
```

The last line is the register's own score. A project where most issues were never risks is not
doing risk management, whatever the document looks like.
