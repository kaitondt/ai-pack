---
description: "Collect the period's actuals from evidence — progress, effort, defects, test results, builds, registers — into the status data file that the reports and EVM are computed from. Run before any report. Usage: /pm_status_collect [period]"
---

# Collect status

The step that makes every report downstream defensible. Run it **before** writing any report
(RI-02).

## Step 1 — Load

`pm_project`, then `pm_reporting`. Agent: `pm_controller`.

## Step 2 — Collect from the named sources

From `{{profile.reporting.data_sources}}`, and from the repository where a technical pack is
installed:

| Data | Source | Feeds |
|---|---|---|
| Work package status | task tracker / `{{profile.schedule.working_file}}` | progress, EV, SPI |
| Effort actuals | timesheets, booked to WBS codes | AC, CPI, utilisation |
| Defects | defect tracker | quality report, containment, S-curve |
| Test execution | test results directory / tool | test progress, pass rate, blocked cases |
| Build and deploy | CI | build health, release readiness |
| Risks and issues | the registers | exposure, ageing |
| Change requests | change register | scope movement, cumulative impact |
| Decisions and actions | decision and action logs | blockers, ageing |
| Contingency | drawdown log | reserve balance |

## Step 3 — Apply the progress rule (RI-03)

Convert raw status into progress using `{{profile.schedule.progress_measurement}}` only. Under
`0-50-100`, a package is 0, 50 or 100, and 100 means accepted against its acceptance criteria
(WB-05) — not "the developer finished".

Flag explicitly: any package reported above 50% with no acceptance evidence, and any package
sitting at 50% for three or more periods. Both are the same problem at different stages.

## Step 4 — Record gaps as gaps

Anything that could not be collected is written as **not collected**, with the reason and when
it will be available. Never carry a figure forward from the previous period to fill a hole
(RI-02) — that single habit makes an entire reporting history untrustworthy.

## Step 5 — Write the period file

`{{profile.paths.status_data}}/{period}.md`, every figure carrying its source and as-of date.
This file is the single input the reports and `/pm_evm` read, so the same numbers appear in
every report for the period.

## Report

```
Status collected — {period}, as of {date}
  Work packages : {n} complete · {n} in progress · {n} not started
  Effort        : {h} this period, {h} cumulative ({source})
  Defects       : new {n} · fixed {n} · open {n} (S1 {n} / S2 {n} / S3 {n} / S4 {n})
  Tests         : executed {n}/{n} · passed {n} · blocked {n}
  Build         : {pass|fail}, {n} failures this period
  Registers     : RSK {n} open · ISS {n} open · CR {n} in flight · ACT {n} open
  Not collected : {what, why, when available}
  Flags         : {packages >50% with no acceptance evidence} · {stalled at 50%}
```
