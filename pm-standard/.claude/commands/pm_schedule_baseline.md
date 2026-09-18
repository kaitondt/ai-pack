---
description: "Build and baseline the schedule: activities from work packages, dependencies, derived durations, critical path, buffers, milestones with objective criteria. Usage: /pm_schedule_baseline"
---

# Schedule baseline

## Step 1 — Load

`pm_project`, then `pm_schedule`. Requires a WBS with dictionary and an estimate.
Agent: `pm_planner`.

## Step 2 — Activities and dependencies

Decompose each work package into activities (WB-06). For each: predecessors, dependency type,
and whether it is **mandatory**, **discretionary** or **external** (WB-07).

Mark discretionary ones explicitly — they are the compression reserve, and knowing which they
are is what makes a recovery decision take an afternoon rather than a week.

Every external dependency becomes a `DEP-*` and a `RSK-*` with an owner and a needed-by date.

## Step 3 — Derive durations (WB-08)

From effort, using real productive hours, allocation, absence allowance and the location
calendars. Add waiting time for reviews, approvals, client decisions and environment
availability. In an offshore engagement, add the time-zone latency per decision cycle
(SE-07) — it is real duration and it compounds.

## Step 4 — Critical path and buffers

Forward and backward pass; name the critical path explicitly and list the near-critical
chains (float under a week). Size buffers per `{{profile.schedule.buffer_policy}}`, held
visibly by the PM. No padding inside activities (ES-05).

## Step 5 — Milestones

From `{{profile.schedule.milestones}}`: zero duration, objective exit criteria, payment-linked
ones marked. When a technical pack is installed, map each milestone to the phase gate that
satisfies it (`integration.milestone_gate_map`) — a payment milestone with no technical exit
criteria behind it is a payment with nothing to verify.

## Step 6 — Feasibility check before baselining

- [ ] Every work package appears in the schedule (PB-04)
- [ ] Nobody is allocated above `{{profile.resource.max_planned_allocation_percent}}`
- [ ] No activity assumes 8 productive hours per person-day
- [ ] Review, approval and client-decision waits are modelled, not assumed instant
- [ ] The critical path has a buffer, and its length is stated
- [ ] Freeze periods from `{{profile.calendar.freeze_periods}}` are respected
- [ ] Every external dependency has a needed-by date and an owner

A schedule that fails these is baselined as fiction, and every variance afterwards measures
against something that was never achievable.

## Step 7 — Baseline

Write to `{{profile.schedule.baseline_path}}`; copy to
`{{profile.schedule.working_file}}` for tracking. **They stay different files** (PB-05).
Approve per `{{profile.governance.approvals.schedule_baseline}}` and register as baselined.

## Report

```
Schedule baseline — v{n} {status}
  Activities    : {n}   Critical path: {n} days, through {chain}
  Near-critical : {n} chains under 5 days float
  Buffers       : project {n}d · feeding {n}d
  Milestones    : {n} ({n} payment-linked, {n} mapped to a technical gate)
  Finish        : {date}   vs charter {date}   variance {n}d
  Feasibility   : {each check, pass/fail}
  External deps : {n}, all with owner and date? {yes|no}
```
