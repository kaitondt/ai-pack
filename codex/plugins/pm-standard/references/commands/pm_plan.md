---
description: "Assemble the project management plan: delivery approach, organisation, governance, the three baselines, subsidiary plans, monitoring and control, change control and the gate calendar. Usage: /pm_plan"
---

# Project management plan

Assembled **last**, because it integrates everything else. Run it after the charter, the scope
baseline, the WBS, the schedule, the cost baseline, the quality plan and the process
definition exist — or with the gaps named explicitly.

## Step 1 — Load

`pm_project`, then `pm_management_plan`. Agent: `pm_planner`.

## Step 2 — Inventory the subsidiary plans (PP-01)

For each entry in the skill's subsidiary-plan table: does it exist, at what version, approved
by whom? Report the missing ones — a PMP citing a plan that does not exist is the most common
form of plan fiction.

## Step 3 — Write the integrating sections

Sections 1–12 per the skill. Cite subsidiary plans with versions (MD-03); never copy their
content, or two versions will disagree within a month.

The sections that carry the weight:

- **Governance** — a real person for every decision type (DA-01), with the CCB and steering
  membership, cadence and quorum.
- **Monitoring and control** — the loop: what is measured, how often, against which threshold,
  who decides, what action follows. A measurement reaching no decision-maker is data
  collection, not control.
- **Change control** — including the emergency path and its retro-documentation window
  (PP-05, IC-11). Without that sentence, the first urgent change sets the precedent that
  undocumented change is acceptable.
- **Gate calendar** — what each gate decides, with its entry criteria (PP-04).

## Step 4 — Apply the reality test (PP-02)

For every process the plan describes:

1. Who does this, in what time, from whose capacity — and is that effort in the WBS?
2. What happens when they do not?

If the answer to the second is "nothing", delete the sentence. A plan describing ceremonies
that will not happen teaches the team that the plan is decorative, which is expensive to
reverse.

## Step 5 — Approve

Per `{{profile.governance.approvals}}`. State the plan's own review cadence (PP-03).

## Report

```
Project management plan — v{n} {status}
  Subsidiary plans : {n}/{n} exist  — missing: {list}
  Baselines        : scope v{x} · schedule v{y} · cost v{z}
  Governance       : {n} decision types, all with named owners? {yes|no}
  Control loop     : {n} measures, each with threshold and decision owner? {yes|no}
  Gates            : {n} scheduled, each with entry criteria and a decision
  Reality test     : {n} processes with no effort in the WBS  ← should be 0
  Open items       : {n}
```
