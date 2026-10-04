---
name: pm_schedule
description: "Schedule management — WBS and WBS dictionary, activity definition and sequencing, duration estimating, critical path, schedule baseline, buffers, progress measurement and schedule control. Load for ALL WBS, WBS-dictionary, planning, milestone, critical-path, progress-tracking and schedule-recovery tasks."
---

# Schedule Management (WBS · WBS Dictionary · Schedule)

> Prerequisite: `pm_project` loaded. Estimating rules in
> `references/rules/pm/estimation-integrity.md`; baseline rules in `references/rules/pm/baseline-integrity.md`.

The WBS is the most load-bearing artifact in project management. Schedule, cost, progress,
responsibility, risk and change impact all index into it. Get it wrong and every number
downstream is measuring something the project is not doing.

---

## Part 1 — The WBS

### WB-01 — Decompose deliverables, not activities

The WBS is a decomposition of **what is delivered**, not a list of what people do. Nouns at
every level: "Order entry screen", "Interface specification", "Trained operations team" —
not "Design", "Coding", "Meetings".

The test: a WBS element you cannot point at when it is finished is not a deliverable.

Activities come later, underneath work packages (Part 2). Building the WBS from activities
produces a plan that tracks effort spent rather than value produced, and that is why such
plans always report 90% complete for a month.

### WB-02 — The 100% rule, in both directions

The children of a node total exactly the parent — no more, no less.

- **Missing work** means unplanned work, discovered when it is due and paid for from the
  buffer.
- **Extra work** means gold-plating, paid for from margin.

Apply the rule to the project root too: the WBS covers 100% of the project scope,
including the work teams habitually leave out. From `{{profile.wbs.level1}}`, three
branches exist specifically to catch it:

| Branch | Work it captures |
|---|---|
| Project management | planning, reporting, meetings, change control, client management |
| Quality assurance and process | reviews, audits, process work, metrics, corrective actions |
| Training and handover | documentation, training material, sessions, knowledge transfer |

Work that is not in the WBS is work nobody planned, nobody costed, and nobody scheduled —
but which will still be done, out of the buffer, by people who then appear to be behind.

### WB-03 — The 8/80 rule

A work package holds between `{{profile.wbs.work_package_min_hours}}` and
`{{profile.wbs.work_package_max_hours}}` hours of effort.

- Below the floor: the plan drowns in administration and nobody updates it.
- Above the ceiling: progress cannot be observed. A 200-hour package is "in progress" for
  five weeks and its true state is unknown until the end.

A second heuristic, more useful than the hours: a work package should not span more than
one reporting period. If it cannot be reported as finished or not finished at the weekly
report, it is too big.

### WB-04 — One owner per work package

One named person, accountable for delivering it (DA-06). Not a team, not a role with three
holders. The owner is who the PM asks, and who reports progress.

### WB-05 — Every work package produces something verifiable

The dictionary entry states the acceptance criteria — how anyone can tell it is done. "Code
written" is not it; "module passes its unit tests and the code review has no open Critical
findings" is.

This is where the `{{profile.process.definition_of_done}}` gets applied per package. Without
it, "done" means "the developer stopped working on it", and the rework appears later as a
defect or a schedule surprise.

### The WBS dictionary

One entry per work package, fields from `{{profile.wbs.dictionary_fields}}`:

| Field | Content |
|---|---|
| Code | `{{profile.wbs.code_format}}`, permanent (PN-02) |
| Name | the deliverable, as a noun |
| Description | what is included **and what is explicitly not** |
| Deliverable | the `D-*` it contributes to |
| Requirements | the `REQ-*` it realises |
| Owner | one named person |
| Predecessors | the codes that must finish first, and why |
| Effort | hours, with the estimating method (ES-01) |
| Duration | working days, derived from effort (ES-04) |
| Cost | effort × rate, plus non-labour |
| Acceptance criteria | how completion is verified (WB-05) |
| Assumptions | `ASM-*` this estimate depends on |
| Risks | `RSK-*` that threaten it |

The "what is explicitly not included" line prevents the most common estimate dispute: two
people who agreed on a package name and disagreed on its content.

### WB-06 — The WBS is delivered as a workbook

Draft the decomposition in whatever form helps you think; text is easier to restructure than
a spreadsheet, and `{{profile.documents.working_dir}}` exists for exactly that. But the
artifact is `{{profile.paths.wbs}}`, an `.xlsx`, and `wbs` is in
`{{profile.documents.binary_final}}` — so the workbook existing **is** the completion
criterion (MD-09).

This is not a formatting preference. Every downstream consumer of the WBS indexes into it by
code, and every one of them is a spreadsheet: the estimate, the cost baseline, resource
loading, earned value, the client's own progress reporting. A WBS that is not a workbook gets
re-keyed into one by hand, and from that moment the project has two WBSs that disagree.

The WBS and its dictionary live in **one workbook, two sheets**, for the same reason: two
files drift, and the dictionary is the half that silently stops matching.

`pm_document_io` DIO-W owns the layout — text-formatted code column, frozen and filtered
header, outline grouping, no merged cells in the data region, the 100% rule as a live formula,
branch totals — and the revision hazard: **never regenerate the workbook from a working file
whose stamp is older than the workbook**, because somebody edited it directly and the
regeneration will destroy that silently.

### Control accounts

At `{{profile.wbs.control_account_level}}`, usually level 2. Cost and progress are measured
and reported at this level; work packages roll up into it. Earned value (`pm_cost`) is
computed per control account.

---

## Part 2 — From WBS to schedule

### WB-06 — Activities live under work packages, never beside them

Each work package decomposes into activities — the verbs. An activity that belongs to no
work package is unplanned work and is either added properly or removed.

### WB-07 — Sequence by dependency, not by preference

For each activity, record predecessors and the dependency type:

| Type | Meaning | Watch for |
|---|---|---|
| Finish-to-start | B starts when A finishes | the default; often over-used, hiding parallelism |
| Start-to-start (+lag) | B starts after A has started | how real overlap is modelled |
| Finish-to-finish | B finishes with A | common for review and documentation activities |

Mark each as **mandatory** (physics or contract), **discretionary** (a preferred practice),
or **external** (`DEP-*`, outside the project's control).

Discretionary dependencies are the schedule's compression reserve: when recovery is needed,
they are the first thing to examine, and knowing which are discretionary is what makes that
possible in an afternoon rather than a week.

External dependencies are the schedule's biggest risk and belong in the risk register with
an owner and a needed-by date — every one of them.

### WB-08 — Duration is derived, never declared

```
duration_days = effort_hours
              ÷ (assigned_people
                 × {{profile.calendar.productive_hours_per_day}}
                 × allocation_percent)
              + waiting time (reviews, approvals, client responses, environment availability)
```

Then apply `{{profile.calendar}}`: working days only, holidays per location, freeze
periods, and the absence allowance.

Two errors that produce most unachievable schedules:

1. **Planning at 8 productive hours per day.** Real productive time is
   `{{profile.calendar.productive_hours_per_day}}`. The gap is ~19%, applied to every
   activity, compounding across the plan.
2. **Ignoring waiting time.** A two-hour review that waits three days for the reviewer is
   three days of duration. Client approvals in an offshore engagement routinely add a full
   day per cycle from the time-zone gap alone (`{{profile.project.time_zones}}`).

Brooks's observation applies at the activity level: adding people to a package does not
divide its duration proportionally, and below a certain size it does not divide at all.

### WB-09 — The critical path is known, named and watched

Compute forward and backward passes; the critical path is the zero-float chain. State it
explicitly in the schedule document, and list the near-critical chains (float under a week)
— those become critical the first time anything slips.

Every weekly report names the current critical path and whether it has changed. A schedule
whose critical path nobody can name is not being managed; it is being observed.

Float belongs to the **project**, not to the activity owner. An activity with ten days of
float that quietly consumes all of it has taken ten days from whatever needed them later.

### WB-10 — Buffers are visible, sized and owned

Per `{{profile.schedule.buffer_policy}}`: a project buffer at the end of the critical path,
feeding buffers where chains join it. Owned by the PM, consumed with a record.

Padding inside individual estimates is forbidden (ES-05). It cannot be measured, it is
consumed by Parkinson's law whether or not the risk occurs, and it destroys the estimating
data the next project needs.

Buffer consumption is a leading indicator, and the most useful one on the report: at 30%
elapsed with 60% of the buffer gone, the plan is failing regardless of what the milestone
dates currently say.

### Milestones

`{{profile.schedule.milestones}}` — zero-duration, objectively verifiable, and each with
exit criteria that two people would judge identically.

Mark which are payment-linked (`payment_linked: true`). Those have a different risk profile
entirely: they are reported separately, watched more closely, and a threat to one is
escalated immediately (RI-05), not at the next cadence.

---

## Part 3 — Schedule control

### WB-11 — Track against the baseline, plan in the working file (PB-05)

`{{profile.schedule.baseline_path}}` is read-only. Progress and re-planning happen in
`{{profile.schedule.working_file}}`. If the two are ever the same file, every variance the
project ever had has been erased.

### WB-12 — Progress is measured by the profile method, not by opinion (RI-03)

`{{profile.schedule.progress_measurement}}`. Under `0-50-100`, a package is 0, 50 or 100 —
and 100 means done per its acceptance criteria (WB-05), not "the developer moved on".

Watch for the drift pattern: 70% → 80% → 90% → 95% across four reports. It is not progress;
it is a package whose remaining work was never understood, and it will end late.

### WB-13 — Schedule recovery, in order of cost

When a slip appears, evaluate in this order and record what was chosen and why:

| Option | Mechanism | Cost |
|---|---|---|
| Re-sequence | remove discretionary dependencies, overlap where safe | free, limited |
| Fast-track | run sequential activities in parallel | rework risk, higher defect rate |
| Crash | add people to critical activities | cost rises faster than duration falls; ramp-up time |
| Reduce scope | defer non-critical scope to a later release | needs a CR and client agreement |
| Move the date | re-baseline | governance decision (PB-06) |

Two honest observations that belong in the recovery discussion:

- Crashing works only where the work is genuinely divisible and the new people need no
  ramp-up. On a design or integration task, adding people usually makes it later.
- Fast-tracking buys time by accepting rework risk. Say so explicitly, and put the risk in
  the register — it is a decision, not a free optimisation.

"The team will work harder" is not on the list. It is unmeasurable, unrepeatable, and it
converts a schedule problem into a quality problem and then a staffing problem.

---

## Exit criteria

- [ ] WBS covers 100% of scope, deliverable-oriented, including management, QA and handover
- [ ] Every work package within 8/80 and inside one reporting period (WB-03)
- [ ] Every work package has one owner and verifiable acceptance criteria
- [ ] Dictionary complete for every leaf, including exclusions and assumptions
- [ ] **The WBS exists as `{{profile.paths.wbs}}` (`.xlsx`)** — a Markdown version is a
      working file, not the deliverable (WB-06, MD-09)
- [ ] Working files stamped and disposed of; exactly one authority on disk (MD-10)
- [ ] Every activity has predecessors with a stated dependency type; external ones are `DEP-*` and in the risk register
- [ ] Durations derived from effort with the real calendar (WB-08), not declared
- [ ] Critical path identified and named; near-critical chains listed
- [ ] Buffers sized per policy, visible and owned; no padding inside estimates
- [ ] Every milestone has objective exit criteria; payment-linked ones marked
- [ ] Baseline approved by `{{profile.governance.approvals.schedule_baseline}}` and registered

Then: `/pm_estimate` (if not done) → `/pm_cost_baseline`.
