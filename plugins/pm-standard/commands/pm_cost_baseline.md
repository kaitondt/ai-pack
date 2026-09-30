---
description: "Build and baseline the cost budget: work package costs, non-labour, time-phased curve, contingency and management reserve, and the billing plan. Usage: /pm_cost_baseline"
---

# Cost baseline

## Step 1 — Load

`pm_project`, then `pm_cost`. Requires the WBS, the estimate and the schedule.
Agent: `pm_estimator`.

## Step 2 — Build the budget structure (CT-01)

```
work package costs (effort × rate + non-labour)
+ contingency reserve            → COST BASELINE
+ management reserve             → PROJECT BUDGET
```

Contingency is inside the baseline and owned by the PM; management reserve is outside it and
owned by the sponsor (ES-06). Keep them separate — merging them means the PM spends the
sponsor's money without asking, and the project loses its earliest risk signal.

## Step 3 — Include non-labour cost (CT-03)

Licences · cloud and infrastructure · environments · third-party services · hardware · travel
· training · translation · certification and audit fees · currency exposure when the contract
and the costs are in different currencies.

## Step 4 — Time-phase it (CT-02)

Budgeted cost per period, cumulative, phased from the **schedule** — cost follows activities,
which follow the WBS (PB-04). A total without a curve gives no planned value, and without
planned value there is no variance until the money is gone.

## Step 5 — Consistency check (PB-04)

- [ ] Every work package has a cost line
- [ ] Every cost line maps to a work package or a control account
- [ ] The baseline total equals work packages + contingency, exactly
- [ ] The curve's end equals the baseline total
- [ ] Rates match `{{profile.cost.rates}}` and the resource plan's actual roles

## Step 6 — Billing plan (CT-11)

From `{{profile.cost.billing}}`: which milestones trigger which invoices, on what condition,
with what payment terms. Under milestone billing the trigger is signed acceptance, not the
calendar date.

## Step 7 — Baseline

Approve per `{{profile.governance.approvals.cost_baseline}}`, write to
`{{profile.cost.baseline_path}}`, register as baselined. Initialise
`{{profile.risk.contingency_drawdown_log}}` with the opening balance.

## Report

```
Cost baseline — v{n} {status}
  Work packages : {amount}    Non-labour: {amount}
  Contingency   : {x}% = {amount}   covering RSK-{ids}
  COST BASELINE : {amount}
  Mgmt reserve  : {x}% = {amount}
  PROJECT BUDGET: {amount}
  Curve         : {n} periods, peak burn {amount} in {period}
  Consistency   : {each check, pass/fail}
  Billing       : {n} invoice points, {amount} milestone-linked
  vs envelope   : charter {amount}, variance {amount} ({x}%)
```

A variance against the charter envelope is reported, never absorbed. It is the sponsor's
decision, and it is cheapest to make now.
