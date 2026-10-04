---
description: "Produce or refresh an effort, duration and cost estimate with two cross-checked methods, the forgotten-work checklist, a stated range and its assumptions. Usage: /pm-estimate [scope | CR-nnn | work-package-code]"
---

# Estimate

## Step 1 — Load

`pm-project`, then `pm-estimation`. Agent: `pm-estimator`.

## Step 2 — Establish the stage and pick two methods (ES-03, EM-01/02)

State which estimating stage this is — pre-charter, post-requirements, or post-design — and
its expected accuracy. Then estimate with **two** methods and reconcile.

When bottom-up and parametric differ by more than about 20%, stop and find out why before
issuing anything. It is almost always a missing work package in the bottom-up, and finding it
is the highest-value hour in the whole exercise.

## Step 3 — Apply the forgotten-work checklist (ES-07, EM-03)

Per feature: clarification · design · design review (reviewer hours too) · implementation ·
code review · unit test writing and execution · integration · test case design · test
execution · defect fixing and re-test · documentation · traceability.

Per project: project management · environment and data setup · build pipeline · release and
rehearsal · client meetings, demos, UAT support · training and handover · onboarding ·
rework · translation, if the project has two document languages.

Then sanity-check the shape against `{{profile.cost.productivity.phase_distribution}}`.

## Step 4 — Convert effort to duration honestly (EM-04)

Use `{{profile.calendar.productive_hours_per_day}}`, real allocation, the absence allowance,
and waiting time for reviews and client decisions. Show the arithmetic — the gap between
"80 hours" and "three calendar weeks" is where most unachievable dates are born.

## Step 5 — Range, assumptions, exclusions

Three-point where uncertainty is real; aggregate by summing expected values and combining
variances, never by summing pessimistic values (EM-01). Every assumption is an `ASM-*` with an
owner and a confirm-by date. State what the number excludes.

## Step 6 — Compare to the target, if one exists (ES-02)

Present estimate, target, gap, and **options with consequences** — never a reconciled number
that happens to equal the target. Three options turn an argument into a decision.

## Step 7 — Write and report

Write to `{{profile.paths.estimate}}` in the estimate-record format from the skill. Report:

```
Estimate — {scope} v{n}, {date}
  Stage       : {stage}   Methods: {primary} × {secondary}, delta {x}%
  Effort      : {E} h   range {E−}..{E+}
  Duration    : {d} working days   ({n} people at {x}%, {h} productive h/day)
  Cost        : {currency} {amount}   (labour {a} · non-labour {b})
  Contingency : {x}% = {amount}, covering RSK-{ids}
  Excludes    : {list}
  Assumptions : ASM-{ids} — {n} unconfirmed, {n} past their confirm-by date
  vs target   : {gap and the options, if a target exists}
  Rates       : {measured from <basis> | UNVERIFIED}
```

An estimate whose rates are unverified says so in every place it is quoted (ES-08).
