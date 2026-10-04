---
description: "Produce or update the project charter: business case, measurable objectives, success criteria, scope outline, milestones, budget envelope, PM authority, high-level risks, and approval. Usage: /pm-charter [update]"
---

# Project charter

## Step 1 — Load

`pm-project`, then `pm-project-charter`. Agent: `pm-planner`.

## Step 2 — Gather the anchors

From the profile: `project`, `governance`, `scope`, `schedule.milestones`, `cost`.

From the organisation: the business case, pre-sales material, the contract or SOW, and
whatever was promised during the bid — **especially** that, since it is usually absent from
every written artifact and present in everyone's memory.

Where a needed input does not exist, it is an open question with an owner, not a gap to fill
with a plausible sentence (MD-04).

## Step 3 — Write

Sections 1–14 per the skill. The three that decide whether the charter is worth having:

- **Objectives** (CH-02) — metric, today's value, target, date. If today's value is unknown,
  make measuring it the first action item, or record it as an `ASM-*`.
- **PM authority** (CH-03) — staffing, spend, technical decisions, escalation. Written, not
  assumed.
- **Success criteria** (CH-04) — a rehearsal of the closing conversation, objective enough
  that two readers reach the same verdict. Include what would make this a failure even if
  every deliverable ships.

Keep it to 3–6 pages. A twenty-page charter is a plan in disguise and will be stale before it
is signed.

## Step 4 — Seed the registers

High-level risks → `{{profile.risk.register}}` as `RSK-*`, with owners and initial responses.
Assumptions → the assumption log as `ASM-*` with confirm-by dates. Dependencies → `DEP-*`.
Decisions already taken → `DEC-*`.

The charter is where the registers start. A register created later starts with the risks that
have already happened.

## Step 5 — Approve and baseline

Route to `{{profile.governance.approvals.charter}}`. On approval: set the version to
`{{profile.document.baseline_version}}`, record the approval row in the revision history, and
register the path as baselined. From then it changes only through change control (CH-07).

## Step 6 — Report

```
Charter — v{n} {status}
  Objectives    : {n} — all with metric/baseline/target/date? {yes | which are missing}
  Success crit. : {n} — objective? {yes | no}
  Exclusions    : {n} — all with reasons? {yes | no}
  PM authority  : {stated | missing}
  Envelope      : {amount} ({method}, {accuracy}) excluding {list}
  Seeded        : RSK {n} · ASM {n} · DEP {n} · DEC {n}
  Approvals     : {role: name, date} | {pending: roles}
  Open items    : {n}
```

Then: `/pm-scope-baseline`.
