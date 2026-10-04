---
name: pm-management-plan
description: "The project management plan — the integrating document: how the project will be executed, monitored and controlled, its subsidiary plans, the baselines it carries, gate and milestone reviews, and integrated change control. Load for ALL project-plan, PMP, governance-setup, kickoff-planning and gate-review tasks."
---

# Project Management Plan

> Prerequisite: `pm-project` loaded. Produced after the charter and the scope baseline;
> assembled last, because it integrates the others.

The project management plan answers one question: **how will this project be run?** It is
not a schedule and not a status report. It is the operating manual the team and the client
both agreed to, and the document a new person reads on their first day to understand how
decisions get made here.

---

## PP-01 — The plan integrates; it does not duplicate

Each subsidiary plan owns its content. The PMP states how they fit together and **cites**
them with versions (MD-03). Copying the schedule into the PMP guarantees two versions that
disagree within a month.

| Subsidiary plan | Owner skill | Lives in |
|---|---|---|
| Scope management plan | `pm-scope` | `{{profile.paths.scope_statement}}` |
| Schedule management plan | `pm-schedule` | `{{profile.schedule.baseline_path}}` |
| Cost management plan | `pm-cost` | `{{profile.cost.baseline_path}}` |
| Quality management plan | `pm-quality` | `{{profile.quality.plan_path}}` |
| Process definition | `pm-process` | `{{profile.process.tailoring_record}}` |
| Resource management plan | `pm-resource` | `{{profile.resource.plan_path}}` |
| Communications plan | `pm-stakeholder` | `{{profile.paths.plan_root}}` |
| Risk management plan | `pm-risk` | `{{profile.risk.register}}` |
| Change management plan | `pm-change-control` | `{{profile.change_control.register}}` |
| Closing plan | `pm-closure` | `{{profile.closing.final_report}}` |

## Structure

| § | Section | Content |
|---|---|---|
| 1 | Project overview | one page, from the charter: objectives, scope outline, milestones |
| 2 | Delivery approach | `{{profile.project.delivery_model}}`; how phases, releases or sprints run |
| 3 | Organisation | org chart, roles, RACI reference, client-side structure |
| 4 | Governance | decision authority, CCB, steering committee, escalation, meeting cadence |
| 5 | Baselines | the three baselines with versions and approval dates |
| 6 | Subsidiary plans | the table above, with versions |
| 7 | Process | lifecycle, QA/QC, definition of done, tools |
| 8 | Monitoring and control | what is measured, how often, thresholds, reports |
| 9 | Change control | how a change is raised, assessed, decided, applied |
| 10 | Gates and reviews | the review calendar and what each gate decides |
| 11 | Assumptions, constraints, dependencies | current state, each with an owner |
| 12 | Approval | per `{{profile.governance.approvals}}` |

## PP-02 — Write how it will actually be run, not the ideal

A PMP describing a weekly CCB that will never meet is worse than no PMP: it establishes an
expectation the project will visibly fail to meet, and it teaches the team that the plan is
decorative.

Two questions to apply to every process sentence in the document:

1. Who does this, in what time, from their existing capacity? (Is that effort in the WBS?)
2. What happens when they do not? (If nothing, remove the sentence.)

## PP-03 — The plan's own maintenance is planned

The PMP is a living document with a review cadence — typically at every gate and at any
re-baseline. State when it will be reviewed and who updates it.

A PMP that has not been touched since kickoff is a description of a project that no longer
exists, and everyone stops reading it at about month three.

---

## Monitoring and control — the control loop

The plan's most operational section. Make the loop explicit:

```
plan → execute → measure → compare to baseline → decide → act → (re-plan or re-baseline)
```

| Element | Where it is defined |
|---|---|
| What is measured | `pm-cost` (EVM), `pm-quality` (quality metrics), `pm-schedule` (progress) |
| How often | `{{profile.reporting.cadences}}` |
| Thresholds | `{{profile.schedule.variance_thresholds}}`, `{{profile.risk.exposure_thresholds}}` |
| Who decides | `{{profile.governance}}` and `{{profile.change_control.authority}}` |
| Corrective action | `{{profile.process.corrective_actions}}` (CAPA log) |

The loop is only real if the "decide" step has a named owner and a forum with a date. A
measurement that reaches no decision-maker is data collection, not control — and it is the
most common way a project accumulates metrics while remaining unmanaged.

---

## PP-04 — Gate and milestone reviews

A gate review decides whether the project may proceed. It is not a status meeting, and the
difference is that it has an outcome.

| Element | Content |
|---|---|
| Entry | the criteria that must hold to review at all |
| Evidence | baseline comparison, quality metrics, risk position, open items |
| Decision | **proceed** · **proceed with conditions** · **hold** · **stop** |
| Conditions | each with an owner and a date; tracked as `ACT-*` |
| Record | `gate_{milestone}_{YYYYMMDD}.md`, approved per `{{profile.governance}}` |

Two rules that keep gates meaningful:

- **A gate that cannot fail is a status meeting.** If no project has ever been held at this
  gate, the criteria are not criteria.
- **"Proceed with conditions" is a real outcome, and it accumulates.** Conditions carried
  from three gates are three unfinished obligations riding into the next phase, and the next
  gate report says so.

When a technical pack is installed, its phase gate (`/sdlc-phase-gate`) evaluates the
engineering exit criteria; this review consumes that result and adds the management
dimensions — cost, schedule, risk, contract, resource, client readiness. Do not re-run its
checks; cite them.

---

## PP-05 — Integrated change control lives here

The PMP states the change process; `pm-change-control` executes it. What the PMP must fix:

- what constitutes a change (any modification to a baselined artifact — PB-03)
- who may raise one, and how
- the assessment dimensions (`{{profile.change_control.impact_dimensions}}`)
- the authority thresholds (`{{profile.change_control.authority}}`)
- the CCB's membership, cadence and quorum
- how an emergency change is handled, and its retro-documentation window
- how approved changes update the baselines

The emergency path deserves one explicit sentence: **an emergency change skips the queue,
never the record.** Without that sentence written down, the first urgent change establishes
a precedent that undocumented changes are acceptable, and the register stops being a record
of the project.

---

## Exit criteria

- [ ] Every subsidiary plan exists and is cited with a version (PP-01)
- [ ] Governance section names a real person for every decision type (DA-01)
- [ ] Monitoring section states measure, cadence, threshold, decision owner and action path
- [ ] Gate review calendar exists, with what each gate decides
- [ ] Change control process is complete, including the emergency path
- [ ] Every process the plan describes has the effort for it in the WBS (PP-02)
- [ ] Plan review cadence stated (PP-03)
- [ ] Approved per `{{profile.governance.approvals}}` and registered as baselined
