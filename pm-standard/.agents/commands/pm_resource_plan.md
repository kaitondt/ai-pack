---
description: "Produce the staffing plan and RACI from the schedule: role requirements over time, allocation limits, ramp-up, skills gaps, key-person risks and subcontract terms. Usage: /pm_resource_plan"
---

# Resource plan

## Step 1 — Load

`pm_project`, then `pm_resource`. Requires the WBS and the schedule. Agent: `pm_planner`.

## Step 2 — Derive the requirement from the work (RM-01)

Build the role-by-period requirement from the schedule, then compare it against who is actually
available. The gap is the finding, and it is a decision for `{{profile.governance}}` — hire,
train, subcontract, re-sequence, or move the date.

Starting from available headcount and fitting the work to it produces a plan that is achievable
only if the work happens to match the team, and nobody ever checks whether it does.

## Step 3 — Apply the allocation limits (RM-02)

Nobody above `{{profile.resource.max_planned_allocation_percent}}`. The remaining capacity
absorbs defect fixing, support, clarification, reviewing other people's work, meetings and
absence — all of which are certain to arrive.

Flag anyone allocated across multiple projects: their context-switching cost is real, large
and entirely absent from both plans.

## Step 4 — Ramp-up and onboarding (RM-03)

For everyone joining after kickoff: one to three weeks to full productivity, plus the mentor's
hours, both as work packages in the WBS. This is why adding people to a late project usually
makes it later (WB-13).

Write or update `{{profile.resource.onboarding_checklist}}` — it is one of the highest-return
artifacts on any project that will add anyone at all.

## Step 5 — Key-person risk (RM-04)

Every role with a single holder becomes a `RSK-*` with a concrete response. Apply the
uncomfortable test and write down the answer: if this person resigned tomorrow, which work
packages stop, and for how long?

"Documentation" is not a response. Documentation someone else has actually used to perform the
task is.

## Step 6 — RACI (DA-06)

One row per deliverable and significant activity, exactly one A per row. Check for the
diagnostic patterns: two A's (nobody is accountable), no A (the PM is), one person A on
everything (an org chart, and a key-person risk), many C's (a decision that will be slow).

## Step 7 — Subcontract, if used

Scope with acceptance criteria · quality standards and review rights · reporting obligations
matching this project's cadences · escalation path with names · IP and data handling · exit
terms. Review their first deliverable on the same cadence as your own — that is where a
standards gap is still cheap to correct.

## Report

```
Resource plan — v{n}
  Roles required : {n} over {n} periods; peak {n} people in {period}
  Gaps           : {role, when, size} — {decision needed from whom}
  Allocation     : {n} people above {limit}%   ← should be 0
  Multi-project  : {who, across what}
  Ramp-up        : {n} joiners, {h}h onboarding + {h}h mentoring, in WBS? {yes|no}
  Key-person risk: {n} single-holder roles → RSK-{ids}, all with responses? {yes|no}
  RACI           : {n} rows · {n} with no A · {n} with two A's · A-concentration {name}: {n}%
  Subcontract    : {parties, terms written? yes|no}
```
