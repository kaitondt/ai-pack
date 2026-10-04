---
description: "Reconcile the management plan with the installed technical pack: WBS work packages against deliverables, milestones against phase gates, quality targets, defect models and baseline state. Usage: /pm-sync-technical"
---

# Sync with the technical pack

The command that keeps this pack honest when a sibling pack manages the product. Read-only;
it reports drift and proposes the correction.

## Step 1 — Load

`pm-project`. Read `{{profile.integration.technical_profile_path}}`. If
`integration.technical_pack` is `none`, report that and stop — there is nothing to reconcile.

## Step 2 — Reconcile, dimension by dimension

| Dimension | Check | Drift means |
|---|---|---|
| **Deliverables** | every technical deliverable category maps to a work package, and every work package producing a document maps to a category | unplanned work, or planned work nobody will produce |
| **Milestones ↔ gates** | every payment milestone maps to a phase gate; every gate maps to a milestone or is deliberately internal | a payment milestone with no technical exit criteria to verify |
| **Quality targets** | the two `quality.targets` sets are identical | the gate verdict depends on which document is quoted (QP-02) |
| **Test levels** | level names, owners, environments and entry/exit criteria agree | a level that is "done" in one plan and not started in the other |
| **Defect model** | severity definitions and SLAs agree | the same defect is S2 in one report and S3 in the other |
| **Baseline state** | documents this pack lists as baselined are baselined there too | an edit blocked in one pack and allowed in the other |
| **Change control** | this pack's CR ids appear in the technical pack's CR records | management approved a change nobody executed, or the reverse |
| **Effort** | technical phase progress is consistent with the work-package status reported here | the report is green on work that has not started |
| **Language and paths** | no path collisions; document languages consistent | two packs writing different content to one file |

## Step 3 — Report drift with its consequence, and the correction

For each drift: which side is authoritative, what to change, and what it currently causes.

The general rule: **the technical pack is authoritative for engineering facts** — what
deliverables exist, what the defect data says, which gates passed. **This pack is authoritative
for management facts** — what was committed, at what cost, by which date, approved by whom.

## Step 4 — Update the mapping

Where the mapping is simply incomplete rather than wrong, propose the additions to
`integration.milestone_gate_map` and the work-package/deliverable links. Do not write them
without confirmation — a mapping guessed here becomes a commitment reported to the client.

## Report

```
Sync — {date}, technical pack {sdlc|migration} at {path}
  Deliverables   : {n} mapped · {n} technical without a WP · {n} WP without a deliverable
  Milestones     : {n} mapped · {n} payment milestones unmapped   ← should be 0
  Quality targets: {identical | n differ: {which, and each value}}
  Test levels    : {consistent | n differ}
  Defect model   : {consistent | differs: {how}}
  Baselines      : {consistent | n documents disagree}
  Change control : {n} CRs here · {n} there · {n} unmatched
  Progress       : {consistent | management reports {x}% where technical shows {y}%}
  Paths          : {no collisions | n collisions}
  Verdict        : {in sync | n drifts — {which are blocking a gate}}
```
