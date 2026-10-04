---
description: "Produce the quality management plan and the master test plan: quality objectives with measurement methods, test levels with entry/exit criteria, defect model, regression strategy, evidence rules and the acceptance model. Usage: /pm-quality-plan [quality|test|both]"
---

# Quality plan and master test plan

## Step 1 — Load

`pm-project`, then `pm-quality`. Agent: `pm-quality-manager`.

## Step 2 — Quality management plan

Sections 1–10 per the skill. Two rules decide whether it is usable:

- **Every objective states target, condition, measurement method and verifier** (QP-01). A
  non-functional target without its condition — load, environment, percentile — cannot be
  passed or failed, and it will be argued about at acceptance.
- **Targets are agreed, not aspirational** (QP-02). When a technical pack is installed, its
  `quality.targets` and this profile's must be the same set; report any drift instead of
  maintaining two.

## Step 3 — Master test plan

Sections 1–12 per the skill. The parts that are actually decided here, not later:

| Decision | Consequence of skipping it |
|---|---|
| Entry/exit criteria per level (QP-05) | testing starts on an unstable build and every result is ambiguous |
| What each level verifies (QP-04) | levels duplicate each other and the month-end scenario has no case |
| Defect severity, priority, lifecycle, SLA (QP-06) | severity gets negotiated per defect, under pressure |
| Defect vs change-request classification | commercial disputes, decided after the work is done |
| Regression strategy and its cost (QP-08) | a suite too slow to run when it is most needed |
| Evidence rules | acceptance without proof of what was tested |
| Environment and data, including masking | UAT waits for data nobody was tasked to prepare |

## Step 4 — Bind to the technical pack

Where one is installed: test case content, viewpoints and the defect register are its. This
plan states the levels, criteria, targets and the client-facing reporting. Cite its artifacts
rather than copying them.

## Step 5 — Check coverage of requirements

Every requirement has at least one verifying test level and, once cases exist, at least one
case (`{{profile.quality.targets.requirement_coverage}}`). A requirement with no verifying
level is a specification defect, found now instead of at acceptance.

## Step 6 — Approve

Per `{{profile.governance.approvals.quality_plan}}` and `.test_plan`. Both are baselined; they
change through change control afterwards.

## Report

```
Quality plan — v{n} {status}      Master test plan — v{n} {status}
  Objectives    : {n}, all with target + condition + method? {yes|no}
  Targets       : {agreed | pack defaults}  — technical pack: {match | n drifts}
  Test levels   : {n}, all with objective entry/exit? {yes|no}
  Requirements  : {n} with a verifying level, {n} without  ← second number should be 0
  Defect model  : severity {n} levels, SLA set? {yes|no}, defect-vs-CR rule stated? {yes|no}
  Regression    : {strategy}, cost per cycle {h}h, in WBS? {yes|no}
  Evidence      : {what is captured, what the client receives}
  Open items    : {n}
```
