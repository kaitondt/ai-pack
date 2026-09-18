---
description: "P8 — write the UAT status or acceptance record: scenario results, requirement coverage, defects by class and severity, deferrals with approvers, and the acceptance decision. Usage: /sdlc_uat_report [status|acceptance]"
---

# P8 — UAT report

## Step 1 — Load

`sdlc_project`, then `sdlc_test_uat`, then `sdlc_quality_metrics`.

## Step 2 — Choose the report

| Mode | When | Output |
|---|---|---|
| `status` | daily or weekly during UAT | `{{profile.paths.uat}}/status/UAT_status_{date}.md` |
| `acceptance` | at the end of the phase | `{{profile.paths.uat}}/acceptance-record.md` |

Default to `status` during the phase; `acceptance` only when every scenario has a verdict.

## Step 3 — Collect from artifacts, not from memory

Scenario results from the executed case files; defects from the register; deferrals with
their approvers; coverage from `{{profile.paths.traceability}}`. Every number carries its
population and its date (QM-01).

## Step 4 — Status report

```
UAT status — {date}, day {n} of {n}
  Scenarios     : {executed}/{planned}   pass {n} · fail {n} · blocked {n}
  Reports today : {n}   defect {n} · CR {n} · usage {n}   (all classified: {yes|no})
  Open defects  : S1 {n} · S2 {n} · S3 {n} · S4 {n}
  SLA           : {n} within · {n} breached ({which})
  Injection     : P1 {n} · P2 {n} · P3 {n} · P4 {n}
  Curve         : found {n} cumulative, closed {n} — {flattening|rising}
  Next deploy   : {date}, containing {what}
  Blockers      : {what the client is waiting on, and who owns it}
```

## Step 5 — Acceptance record

Per the skill's table: scenarios, requirement coverage, defects, deferred items with
approver and target release, known limitations, the acceptance decision, approver and date.

**"Accepted with conditions" names each condition, its owner and its date** (UA-07). An
unqualified condition becomes an argument at the warranty boundary.

## Step 6 — Report against the gate

```
P8 — UAT
  Scenarios     : {executed}/{planned}, all with a verdict: {yes|no}
  Coverage      : {n}/{n} acceptance criteria (T-07)
  Defects       : raised {n} · fixed {n} · deferred {n} · accepted {n}
  Escapes       : {n} first found here ({% of all defects})   target {{profile.quality.targets.escaped_defects}}
  Acceptance    : {decision}   approver {name}   date {date}
  Gate {{profile.gates.P8_uat.exit}} : {pass|fail}
```

Then `/sdlc_phase_gate P8`, and hand over to P9 with the deferred-defect list, the
known-limitations list and the runbook (`sdlc_release` §7).
