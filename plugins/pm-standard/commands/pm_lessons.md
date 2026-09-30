---
description: "Capture lessons learned with the evidence behind them and route each one to where it changes future behaviour — an estimating rate, a checklist, a rule, a template, a contract clause. Runs at gates and after major events, not only at closing. Usage: /pm_lessons [event | phase | 'closing']"
---

# Lessons learned

## Step 1 — Load

`pm_project`, then `pm_closure`.

## Step 2 — Capture close to the event (CL-07)

Run at every gate, after every major issue, and after every CR that went badly — not only at
closing. A lesson captured six months later has lost its detail and its evidence, and the
people who lived it have moved on.

## Step 3 — Write each lesson with its evidence

| Field | Content |
|---|---|
| `LL-*` | id |
| What happened | the specific event, with dates and the artifact that shows it |
| Impact | effort, schedule, cost, quality — quantified |
| Root cause | why, not who |
| What we would do differently | concrete and actionable |
| Destination | the rule, checklist, template, rate or clause it changes |
| Owner | who carries it into the organisation |

## Step 4 — Reject anecdotes (CL-08)

"Communication could have been better" changes nothing. The same event, written usefully:

> Client design decisions took 6 working days on average against a 2-day planning assumption,
> costing 11 days across 9 decision points. **Destination:** add a decision-latency line to the
> estimating template (EM-04 waiting time) and put a decision SLA in the next contract.
> **Owner:** delivery manager.

A lesson with no destination and no owner is a diary entry that will be rediscovered on the
next project, at the same price.

## Step 5 — Route each one

| Lesson about | Goes to |
|---|---|
| Estimating accuracy | `{{profile.cost.productivity}}` rates, with the measured actuals (ES-08) |
| A check that would have caught it | a rule or checklist — hand to `/pm_refine_skill` |
| A recurring risk | the standard risk checklist (RK-04) |
| A process gap | `{{profile.process.process_assets}}` |
| A contract clause | the organisation's contracting template |
| A governance failure | `{{profile.governance}}` and the escalation design |

## Step 6 — Mine the registers, not just memory

The registers already contain most of the lessons, and reading them is more honest than
recollection:

- issues that were never risks (RK — foresight ratio)
- risks whose planned response was never executed
- CRs whose actual effort exceeded the estimate, and by how much
- defects that escaped to UAT, and the check that should have caught each one
- decisions that took longer than their SLA, and what they blocked
- work packages whose actual effort exceeded estimate by more than 25%

## Report

```
Lessons — {scope}, {date}
  Captured        : {n} new, {n} updated
  With quantified impact : {n}/{n}
  With destination + owner: {n}/{n}     ← anything less is an anecdote
  Routed to:
    estimating rates   {n}   process assets {n}   rules/checklists {n}
    risk checklist     {n}   contract terms {n}   governance     {n}
  From the registers:
    unforeseen issues  {n}/{n}   unexecuted responses {n}
    CR estimate misses {n}       escaped defects      {n}
    WP overruns >25%   {n}
```
