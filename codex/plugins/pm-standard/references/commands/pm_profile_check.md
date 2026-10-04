---
description: "Validate pm.profile.yaml: unfilled fields, governance gaps, arithmetic sanity, baseline register state, agent model drift, and consistency with the technical pack's profile. Usage: /pm_profile_check"
---

# Profile check

Read-only. Reports **Critical** (the pack's assumptions do not hold) / **Warning** /
**Suggestion**.

## Critical

- `.codex/pm.profile.yaml` missing → run `/pm_init`
- any `governance` role unset — decisions would have no owner (DA-01)
- `governance.approvals` missing an entry for an artifact this project produces
- `document.auto_version_bump: true` — versions would bump without instruction (MD-02)
- `change_control.authority` empty or without thresholds — every change becomes a negotiation
- `schedule.baseline_path` equal to `schedule.working_file` — variance would be erased (PB-05)
- `cost.contingency_percent` and `management_reserve_percent` both zero under a fixed-price
  contract — nothing stands behind the identified risks (ES-06)
- a baseline-register entry pointing at a path that does not exist
- a baseline-register entry pointing **inside** `documents.working_dir` — a baselined scratch
  file (MD-10)
- a `documents.registry[]` entry missing `artifact`, `path` or `format`, a `format` outside
  `documents.formats_enabled`, or the same artifact bound twice
- an artifact in `documents.binary_final` whose registry `format` is not binary (`xlsx` /
  `docx`) — the pack would promise a workbook and bind a text file
- **`wbs` absent from `documents.binary_final`, or `paths.wbs` not ending in `.xlsx`** —
  MD-09; the WBS is delivered as Excel
- `paths.wbs` and the `wbs` registry entry's `path` naming different files — two paths is two
  WBSs, and only one of them gets baselined
- a format in `documents.formats_enabled` with no working library. `openpyxl` is not optional
  on this pack: without it the WBS cannot be delivered at all

## Warning

- `calendar.productive_hours_per_day` equal to `hours_per_day` — every duration will be
  roughly 19% optimistic (EM-04)
- `resource.max_planned_allocation_percent` at 100 (RM-02)
- `cost.productivity.basis` empty — the rates are unverified, and every estimate built on
  them must say so (ES-08)
- `quality.targets` still at pack defaults with no agreement recorded (QP-02)
- a reporting cadence with no audience, or an audience appearing in no cadence
- `risk.probability_scale` or `impact_scale` without numeric anchors — two people will score
  the same risk differently (RK-05)
- `scope.out_of_scope` entries with no reason (SM-07)
- agent frontmatter `model:` disagreeing with `execution.agent_model`
- `schedule.milestones` with no objective criteria, or payment-linked milestones unmarked
- a `documents.registry[].template` that is set but names a file that does not exist
- `documents.working_dir` sitting inside a **deliverable** directory (`plan_root`, `scope`,
  `cost_root`, `registers`, …) — scratch kept beside deliverables gets delivered. Being under
  `paths.pm_root` is expected and is not a finding: that is the container for everything
- a file under `documents.working_dir` with no stamp on line one (MD-10). An unstamped
  working file cannot be used as the input to a regeneration, because nothing says which
  version it came from

## Cross-pack consistency

When `integration.technical_pack` is not `none`, compare against that profile:

| Check | Why it matters |
|---|---|
| quality targets match | two sets of targets means the gate verdict depends on which document is quoted (QP-02) |
| milestone ↔ gate map covers every payment milestone | an unmapped payment milestone has no technical exit criteria behind it |
| deliverable list ↔ deliverable categories | a management deliverable with no technical counterpart is unplanned work |
| defect severity models match | the same defect would be S2 in one report and S3 in the other |
| language settings agree | a report and its evidence in different languages cannot be reconciled |
| paths do not collide | two packs writing different content to the same file |

## Report

```
Profile check — {date}
  Critical {n} · Warning {n} · Suggestion {n}
  {each finding: field · what is wrong · what it breaks · how to fix}
  Cross-pack : {consistent | n drifts, listed}

  Formats    : {n} artifacts bound   binary_final: {list}
               {each binary_final artifact}: {present | not yet produced}
  Toolchain  : openpyxl {ok | MISSING} · python-docx {ok | n/a}
  WBS        : {{profile.paths.wbs}}  ({present | not yet produced})
  Working dir: {n} files · retention {mode} · {n} unstamped
```

Fix every Critical before running any planning command. A Critical means an artifact produced
now would carry a defect into everything built on it.
