# Command Flow

How the 28 commands relate: what each consumes and produces, what must run before what, and
the control loop the pack is built around.

---

## 1. Command catalogue

### Setup — run once

| Command | Reads | Writes | Agent |
|---|---|---|---|
| `/pm_init` | the repository, a technical profile if present | `pm.profile.yaml`, `pm/` scaffold, registers, `CLAUDE.md` | — |
| `/pm_profile_check` | profile, technical profile | nothing (report only) | — |

### Plan — produce the baselines

In order. Each consumes the one above it.

| Command | Reads | Writes | Agent |
|---|---|---|---|
| `/pm_charter` | business case, contract, governance | project charter; seeds RSK/ASM/DEP/DEC | `pm_planner` |
| `/pm_scope_baseline` | charter, requirements source | scope statement, RTM | `pm_planner` |
| `/pm_wbs` | scope statement, deliverables | **WBS + dictionary as one Excel workbook** at `paths.wbs` | `pm_planner` |
| `/pm_estimate` | WBS dictionary, productivity rates | estimate record | `pm_estimator` |
| `/pm_resource_plan` | WBS, schedule draft | staffing plan, RACI; key-person risks | `pm_planner` |
| `/pm_schedule_baseline` | WBS, estimate, resource plan, calendar | schedule baseline + working file | `pm_planner` |
| `/pm_cost_baseline` | estimate, schedule, rates | cost baseline, reserves, billing plan | `pm_estimator` |
| `/pm_quality_plan` | scope, requirements, technical pack | quality plan, master test plan | `pm_quality_manager` |
| `/pm_process_define` | organisational standard, technical pack | process definition, tailoring record, CAPA log | `pm_quality_manager` |
| `/pm_comm_plan` | governance, stakeholders | stakeholder register, communications plan | `pm_planner` |
| `/pm_risk_assess` | all of the above, assumption log | risk register with responses and triggers | `pm_risk_manager` |
| `/pm_plan` | every subsidiary plan | project management plan | `pm_planner` |

### Execute and control — measure, report, decide

| Command | Reads | Writes | Agent |
|---|---|---|---|
| `/pm_status_collect` | trackers, timesheets, test results, CI, registers | the period's status data file | `pm_controller` |
| `/pm_evm` | status data, cost and schedule baselines | EVM figures and variance analysis | `pm_controller` |
| `/pm_report <cadence>` | status data, EVM, registers | daily / weekly / monthly / quarterly / quality report | `pm_controller` |
| `/pm_risk_review` | registers, triggers, contingency log | updated registers, escalations | `pm_risk_manager` |
| `/pm_audit` | artifacts on disk vs the process | audit record, non-conformances, CAPAs | `pm_quality_manager` |
| `/pm_trace_check` | baselines, RTM, registers | consistency and orphan report | — |
| `/pm_health_check` | everything on disk | RAG per area, the three likely failure causes | — |
| `/pm_sync_technical` | both profiles and both sets of artifacts | drift report and proposed corrections | — |

### Change — the only legitimate way a baseline moves

| Command | Reads | Writes | Agent |
|---|---|---|---|
| `/pm_change_assess` | the request, baselines, technical context map | CR register entry, impact matrix, options — **no changes** | `pm_change_analyst` |
| `/pm_change_apply` | an approved CR | updated baselines, `DEC-*`, handoff to the technical pack, closed CR | `pm_change_analyst` |

### Decide and record

| Command | Purpose |
|---|---|
| `/pm_gate_review` | proceed / conditions / hold / stop, with evidence, recorded |
| `/pm_closing` | acceptance, handover, contract closure, final report, archive |
| `/pm_lessons` | capture lessons with destinations and owners |
| `/pm_refine_skill` | feed a lesson or audit finding back into the pack |

---

## 2. Dependency graph

An arrow means "must have produced its artifact first".

```mermaid
flowchart TD
  INIT["/pm_init"] --> PC["/pm_profile_check"]
  PC --> CH["/pm_charter"]
  CH --> SC["/pm_scope_baseline"]
  SC --> WBS["/pm_wbs"]
  WBS --> EST["/pm_estimate"]
  EST --> RES["/pm_resource_plan"]
  RES --> SCH["/pm_schedule_baseline"]
  SCH --> COST["/pm_cost_baseline"]
  SC --> QP["/pm_quality_plan"]
  WBS --> PRD["/pm_process_define"]
  CH --> CP["/pm_comm_plan"]
  COST --> RA["/pm_risk_assess"]
  QP --> RA
  RA --> PMP["/pm_plan"]
  PMP --> SCOL["/pm_status_collect"]
  SCOL --> EVM["/pm_evm"]
  EVM --> REP["/pm_report"]
  SCOL --> REP
  REP --> GATE["/pm_gate_review"]
  EVM --> GATE
  TC["/pm_trace_check"] --> GATE
  RR["/pm_risk_review"] --> REP
  AUD["/pm_audit"] --> REP
  CA["/pm_change_assess"] --> CAP["/pm_change_apply"]
  CAP --> SCH
  CAP --> COST
  CAP --> SC
  GATE --> CLO["/pm_closing"]
  CLO --> LL["/pm_lessons"]
  LL --> RS["/pm_refine_skill"]
  AUD -.-> RS
  SYNC["/pm_sync_technical"] -.-> GATE
  HC["/pm_health_check"] -.-> PMP
```

**`/pm_gate_review` is where a phase actually ends.** It consumes `/pm_trace_check`,
`/pm_evm` and the quality report, records the decision, and baselines what it covers.

The `/pm_change_*` pair hangs off the graph rather than sitting in it: a change can arrive at
any time and re-opens the baselines it touches. Its two non-negotiable arrows are internal —
assess before decide, decide before apply.

---

### A note on the WBS step

`/pm_wbs` produces an Excel workbook, not a Markdown document. `wbs` is in
`{{profile.documents.binary_final}}`, so the workbook existing at `{{profile.paths.wbs}}`
**is** the step's completion criterion (MD-09) — a complete Markdown WBS is a working file
and the step is not done.

Drafting in text first is encouraged and is what `{{profile.documents.working_dir}}` is for.
Two things keep that safe: every scratch file is stamped on line one as a draft or as a
generated export (MD-10), and the workbook is never regenerated from a working file older
than itself — which is what would otherwise erase a direct edit somebody made to the
workbook between sessions.

Everything downstream of this step — `/pm_estimate`, `/pm_cost_baseline`,
`/pm_schedule_baseline`, `/pm_evm` — indexes into the WBS by code. That is why the format is
fixed here rather than left to preference.

## 3. The control loop

Planning happens once per baseline. This runs every period, forever:

```
       ┌───────────────────────────────────────────────────────┐
       │                                                       │
  /pm_status_collect ──► /pm_evm ──► /pm_report ──► decision   │
       ▲                     │            │                    │
       │                     │            └──► /pm_gate_review  │
       │                     │                                  │
       │              /pm_trace_check                           │
       │                                                        │
       └──── /pm_change_apply ◄── /pm_change_assess ◄── a change ┘
                    │
                    └──► baselines move, and the loop measures against the new ones
```

Two properties the loop depends on:

1. **Collection precedes reporting, always.** A report assembled without
   `/pm_status_collect` is assembled from memory, and one unverified number makes the whole
   reporting history untrustworthy (RI-02).
2. **Baselines move only through `/pm_change_apply`.** Any other route — a helpful edit, an
   absorbed small change, a quiet re-plan — removes the ability to explain the variance later.

---

## 4. Cadence: what runs when

| When | Commands |
|---|---|
| Daily | `/pm_report daily` |
| Weekly | `/pm_status_collect` → `/pm_report weekly`; `/pm_risk_review weekly` |
| Monthly | `/pm_status_collect` → `/pm_evm` → `/pm_report monthly` + `/pm_report quality`; `/pm_risk_review monthly`; `/pm_audit`; `/pm_sync_technical` |
| Quarterly | `/pm_report quarterly` |
| Per gate / milestone | `/pm_trace_check` → `/pm_evm` → `/pm_gate_review` → `/pm_lessons` |
| On a change | `/pm_change_assess` → (approval) → `/pm_change_apply` |
| On an incident or escalation | `/pm_risk_review`, then `/pm_lessons` if it was unforeseen |
| On taking over a project | `/pm_profile_check`, `/pm_trace_check`, `/pm_health_check` |
| At closing | `/pm_closing` → `/pm_lessons` → `/pm_refine_skill` |

---

## 5. The refinement loop

The pack is meant to get better between projects, not only between releases:

```
/pm_audit or a gate finding or an escaped defect
        │
        ▼
/pm_lessons   ← quantified impact, root cause, destination, owner
        │
        ▼
/pm_refine_skill   ← hook > profile field > rule > skill section > command step > checklist row
        │
        ▼
the next project starts with the check that was missing
```

The question that drives it is always the same: **which check would have caught this, and why
did it not run?** A lesson that cannot answer it is not yet a lesson — it is an investigation.

---

## 6. What each command refuses to do

Worth knowing, because these refusals are the pack working rather than failing:

| Command | Refuses to |
|---|---|
| `/pm_report` | write a report when the period's status was never collected |
| `/pm_evm` | compute indices when progress is self-assessed or actuals come from the plan |
| `/pm_change_apply` | apply a CR with no written approval from the named authority |
| `/pm_gate_review` | record a gate as passed when a criterion could not be evaluated |
| `/pm_estimate` | issue a number without method, basis and range — or one reconciled to a target |
| `/pm_schedule_baseline` | baseline a schedule that fails its feasibility checks |
| any planning command | substitute a plausible value for an unresolved profile placeholder |
