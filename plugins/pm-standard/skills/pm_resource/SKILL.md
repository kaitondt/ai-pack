---
name: pm_resource
description: "Resource management — staffing plan, RACI, allocation and utilisation, ramp-up and onboarding, key-person risk, skills gaps, team capacity, subcontractor management and resource release. Load for ALL staffing, allocation, RACI, utilisation, onboarding and subcontract tasks."
---

# Resource Management

> Prerequisite: `pm_project` loaded.

The resource plan is where a schedule becomes achievable or stops being so. Effort and
duration are arithmetic (EM-04); whether the right people are available at the right
allocation at the right time is the constraint that arithmetic assumes away.

---

## Staffing plan

`{{profile.resource.plan_path}}`, derived from the WBS and the schedule:

| Role | Count | Allocation | Start | End | Location | Skills required | Named | Status |
|---|---|---|---|---|---|---|---|---|

### RM-01 — Plan from the schedule, not from the headcount available

Build the requirement from the work, then compare against what exists. The gap is the
finding, and it is a decision for `{{profile.governance}}` — hire, train, subcontract,
re-sequence, or move the date.

Starting from available headcount and fitting the work to it produces a plan that is
achievable only if the work happens to match the team, and nobody ever checks whether it does.

### RM-02 — Never plan anyone at 100%

`{{profile.resource.max_planned_allocation_percent}}`, typically 85%. The remaining capacity
absorbs defect fixing, support, clarification, review of other people's work, meetings, and
absence.

A plan at 100% allocation has no capacity for the work that is certain to arrive, so the first
defect comes out of the schedule. This is the second most common cause of an unachievable
plan, after planning at 8 productive hours per day (EM-04).

A person at 100% on two projects is at 100% on neither, and their context-switching cost is
real and unmeasured — 20–40% on knowledge work, and entirely invisible in the plan.

### RM-03 — Ramp-up is work, and it is in the WBS

Anyone joining after kickoff needs: environment setup, domain context, codebase orientation,
process familiarity, and a mentor's time. That is typically one to three weeks before full
productivity, and the mentor's hours are real hours subtracted from the mentor's plan.

This is why crashing a late project often makes it later (WB-13): the new people produce
nothing for two weeks while consuming the productive time of the people who were already
behind.

`{{profile.resource.onboarding_checklist}}` makes the ramp shorter and repeatable. It is one
of the highest-return artifacts in a project that will add anyone at all.

### RM-04 — Key-person risk is a register entry, not an observation

`{{profile.resource.key_person_risk}}`: every role with a single holder is a `RSK-*`, with a
response that is concrete.

"Documentation" is not a response; documentation that someone else has actually used to
perform the task is. The cheapest real mitigations: pair on the critical work, rotate the
second person through it once, and make sure the handover happens while both people are still
there.

The test is uncomfortable and worth applying: if this person resigned tomorrow, which work
packages stop, and for how long? Write the answer down.

---

## RACI

`{{profile.resource.raci_path}}`, one row per deliverable and per significant activity.

| | Meaning |
|---|---|
| **R** Responsible | does the work |
| **A** Accountable | answers for the outcome — exactly one per row (DA-06) |
| **C** Consulted | input sought before the decision |
| **I** Informed | told afterwards |

Three diagnostic patterns:

| Pattern | Means |
|---|---|
| Two A's on a row | nobody is accountable; the first difficulty proves it |
| No A | the PM is accountable, whether they intended to be |
| The same person is A on everything | an org chart, not an assignment — and the project's key-person risk, named |
| Many C's on one row | that decision will be slow; decide whether it deserves to be |

---

## Utilisation and capacity

### RM-05 — Measure utilisation to find capacity problems, never to judge people

Utilisation = billable or project hours ÷ available hours, per role, reported monthly
(`{{profile.resource.utilisation_report}}`).

Both directions are signals about the plan:

| Observation | Usually means |
|---|---|
| Sustained above 100% | the plan is wrong, not the team heroic; the cost arrives later as defects and attrition |
| Well below plan | blocked, waiting on dependencies, or allocated to work that has not started |
| Spiky | poor sequencing, or a dependency that arrives in bursts |

Report per role and per team, never per person (PR-08). The moment utilisation evaluates
individuals, timesheets become fiction and the project loses its effort data.

### RM-06 — Overtime is recorded, not absorbed

Book the hours worked. Suppressing overtime makes CPI look healthy while the team burns out,
and the exhaustion arrives as a quality problem, then a resignation, then a ramp-up cost —
each more expensive than the number would have been.

Sustained overtime is a planning failure being paid for by people. Report it as a risk
(`RSK-*`) with its trend, not as a sign of commitment.

---

## Subcontractors

Where `{{profile.resource.subcontract.used}}` is true, the project carries responsibility for
work it does not directly control. What must exist in writing:

- scope and deliverables, with the same acceptance criteria discipline as any deliverable (SM-06)
- quality standards and review rights — including the right to review their work products
- reporting obligations matching `{{profile.reporting.cadences}}`, not their own preference
- escalation path into their organisation, with names
- IP, confidentiality and data handling
- exit terms: what happens to the work in progress if the arrangement ends

The common failure is treating subcontracted work as out of sight until delivery, then
discovering at integration that its quality standard was different. Review their work on the
same cadence as your own, from the first deliverable — the first one is where a standards gap
is cheap to correct.

---

## Release

At closing, per `{{profile.closing.resource_release}}` (CL-06): people released on dated
records, accesses revoked, licences transferred or terminated, environments decommissioned.

Also plan **roll-off during** the project. A person whose work finishes in month four and who
stays allocated until month six is a cost nobody decided to incur, and it shows up in CPI
without an explanation.

---

## Exit criteria

- [ ] Staffing requirement derived from the schedule, with gaps named as decisions (RM-01)
- [ ] Nobody planned above `{{profile.resource.max_planned_allocation_percent}}` (RM-02)
- [ ] Ramp-up effort for late joiners in the WBS (RM-03)
- [ ] Every single-holder role has a `RSK-*` with a concrete response (RM-04)
- [ ] RACI complete, exactly one A per row (DA-06)
- [ ] Onboarding checklist exists
- [ ] Subcontract terms written where applicable
- [ ] Utilisation reported per role, never per person (RM-05)
