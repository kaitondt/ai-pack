---
description: "Check management traceability and baseline consistency: requirement to work package to deliverable to test, WBS to schedule to cost, risks to work packages, CRs to baselines, and orphans in every direction. Usage: /pm-trace-check [area]"
model: sonnet
effort: medium
---

# Traceability and consistency check

Read-only. Reports what is inconsistent, and what each inconsistency means in practice.

## Step 1 — Load

`pm-project`. Read the baselines, the RTM and the registers.

## Step 2 — Baseline consistency (PB-04)

| Check | An failure means |
|---|---|
| every work package appears in the schedule | work nobody will do |
| every schedule activity maps to a work package | work nobody costed |
| every activity has effort and cost in the cost baseline | a budget that does not cover the plan |
| baseline total = work packages + contingency | the arithmetic does not close |
| every deliverable maps to at least one work package | a contract obligation nobody planned |
| every baselined requirement maps to a work package | agreed scope that is unplanned |

## Step 3 — Requirement traceability (SM-02)

| Orphan | Means |
|---|---|
| requirement → no work package | agreed but unplanned; it surfaces late or is missed |
| work package → no requirement | unplanned work: gold-plating, or an unwritten requirement |
| requirement → no verifying test | it cannot be accepted; the acceptance meeting will discover this |
| deliverable → no acceptance criteria | acceptance will be negotiated under pressure (SM-06) |

## Step 4 — Register linkage (PN-04)

- every risk cites the work packages or milestones it threatens
- every issue cites the risk it materialised from, or is marked unforeseen
- every CR cites the baseline items it changes, and every applied CR appears in the affected
  documents' revision histories
- every decision names what it affects
- every action cites its source meeting, report or issue
- every contingency drawdown cites a risk or an issue

## Step 5 — Cross-pack consistency

When a technical pack is installed:

- every management deliverable has a technical counterpart on disk, and vice versa
- every payment milestone maps to a phase gate (`integration.milestone_gate_map`)
- the quality targets in both profiles agree (QP-02)
- documents this pack reports as baselined are the ones the technical pack treats as baselined

Drift here is how a project reports green on a plan that no longer describes the work being
done.

## Report

```
Trace check — {scope}, {date}
  Baseline consistency
    WP without schedule      {n}   {codes}
    Activity without WP      {n}   {ids}
    WP without cost          {n}   {codes}
    Arithmetic closes        {yes|no — by how much}
  Requirements
    REQ without WP           {n}   {ids}
    WP without REQ           {n}   {codes}
    REQ without test         {n}   {ids}
    Deliverable w/o criteria {n}   {ids}
  Registers
    Unlinked risks / issues / CRs / decisions / actions / drawdowns : {n each}
  Cross-pack                 : {consistent | n drifts, listed}
  Verdict                    : {clean | n findings, {n} blocking a gate}
```
