---
name: pm_quality
description: "Quality management — quality management plan, master test plan, quality objectives and metrics, entry/exit criteria per test level, defect management and severity model, acceptance criteria, quality gates and the quality report. Load for ALL quality-plan, test-plan, test-strategy, defect-model and quality-metric tasks."
---

# Quality Management (Quality Plan · Master Test Plan)

> Prerequisite: `pm_project` loaded. Process side in `pm_process`; metric reporting in
> `pm_reporting`.

Quality management decides, in advance, **what "good enough" means and how it will be
proven**. Deciding that at acceptance time instead is how projects end in negotiation
rather than delivery.

When a technical pack is installed it owns test case content, viewpoints, review checklists
and the defect register. This skill owns the plan, the targets, the entry/exit criteria, the
acceptance model and the report to the client. Cite its artifacts; do not duplicate them.

---

## Part 1 — Quality management plan

`{{profile.quality.plan_path}}`.

| § | Content |
|---|---|
| 1 | Quality objectives — `{{profile.quality.objectives}}`, each with a target and a measurement method |
| 2 | Standards that apply — organisational, client, regulatory, technical |
| 3 | QA activities — process assurance and audits (`pm_process`) |
| 4 | QC activities — reviews, tests, inspections, per artifact type |
| 5 | Entry and exit criteria per phase and per test level |
| 6 | Metrics — `{{profile.quality.targets}}`, how each is computed and where reported |
| 7 | Defect model — severity, priority, lifecycle, SLAs |
| 8 | Roles — who reviews, who tests, who accepts |
| 9 | Tools and environments |
| 10 | Acceptance model — what the client checks and how |

### QP-01 — A quality objective states a target, a method and a verifier

"High quality software" is not an objective. Each one carries:

| Attribute | Target | Measured by | Verified at | Owner |
|---|---|---|---|---|
| Functional correctness | zero open S1/S2 at acceptance | defect register | UAT exit | qa_lead |
| Review effectiveness | ≥ 2 findings per design document | review records | each gate | qa_lead |
| Response time | 95th percentile < 2 s at 200 concurrent users | load test on staging | ST | architect |

Non-functional targets need the **condition** as well as the number. "Under 2 seconds" with
no stated load, environment or percentile cannot be passed or failed, and it will be argued
about at acceptance by two people with different implicit assumptions.

### QP-02 — Targets are agreed, not aspirational

`{{profile.quality.targets}}` ships with plausible defaults. Replace them with numbers from
your own history, agree them with the team and the client, then hold them.

A target nobody agreed to is a target nobody acts on, and it will be quietly moved the first
time a gate would fail — which is precisely the moment it was supposed to work.

When a technical pack is installed, its `quality.targets` and this profile's must match.
`/pm_sync_technical` reports drift; two sets of targets means the gate result depends on
which document is quoted.

### QP-03 — Prevention is cheaper than detection, by an order of magnitude per phase

The cost of a defect multiplies roughly 10× per phase it survives: a requirement defect
caught in review costs an hour; the same defect caught in UAT costs the requirement change,
the design change, the code change, the re-test, the regression, the client's time and the
schedule.

So the quality plan invests where the leverage is:

| Investment | Effect |
|---|---|
| Requirement review with the acceptance criteria written | removes the most expensive defect class |
| Design review by someone who will not implement it | catches assumption defects while they are still text |
| Definition of done including document and test updates | prevents documentation debt becoming defects |
| Static analysis and CI on every commit | removes the cheap class entirely, at no marginal cost |
| Test cases written from the specification, not the code | detects what the code got wrong, rather than confirming it |

The last one is not a nuance. A test written by reading the implementation asserts what the
code does, passes forever, and proves nothing.

---

## Part 2 — The master test plan

`{{profile.quality.test_plan_path}}`. This is the **plan**, not the test cases.

| § | Content |
|---|---|
| 1 | Scope — what is tested, and what explicitly is not, with reasons |
| 2 | Test levels — `{{profile.quality.test_levels}}`, each with owner, environment, basis |
| 3 | Entry / exit criteria per level |
| 4 | Test approach per level — what kind of coverage, from which document |
| 5 | Environments and data — including how production-like data is obtained and masked |
| 6 | Schedule — test windows, per level, against the WBS |
| 7 | Resources — who tests, when, at what allocation |
| 8 | Defect process — logging, triage, severity, SLA, re-test, closure |
| 9 | Regression strategy — what is re-run, when, and how it is kept affordable |
| 10 | Evidence — what is captured, where it is stored, what the client receives |
| 11 | Risks to testing — environment, data, availability, dependency |
| 12 | Acceptance — the UAT model and the acceptance record |

### QP-04 — Each level verifies a specific document

| Level | Verifies | Basis | Owner |
|---|---|---|---|
| UT | the detail design | detail design / module spec | developer |
| IT | the basic design | interface and function design | technical lead |
| ST | the requirements | SRS, including NFRs | qa_lead |
| UAT | the business need | charter objectives, business process | client |

Two consequences the plan must state:

1. **A specification that cannot be tested is not finished.** If no case can be written at
   its verifying level, that is a defect in the specification, found at the cheapest
   possible moment.
2. **A level that re-tests the level below wastes its budget.** An ST suite full of field
   validation has paid for coverage it already had and still has no case for the month-end
   process — the scenario that will actually fail in production.

### QP-05 — Entry and exit criteria are objective and enforced

From `{{profile.quality.test_levels}}`. Entry criteria that are not enforced are the most
expensive politeness in project management: testing starts on an unstable build, every
result is ambiguous, defects are re-found and re-closed, and the schedule absorbs it
invisibly.

When entry criteria are not met, the correct action is to **record the entry failure and
escalate the date impact** — not to start anyway and discover the impact three weeks later
with no record of why.

### QP-06 — The defect model, agreed before testing starts

`{{profile.quality.defect_severity}}`. Severity is about **impact on the user**; priority is
about **order of fixing**. They are different fields and they legitimately disagree: a
cosmetic defect on the login screen is S4 severity, P1 priority.

The defect lifecycle, with owners at each transition:

```
new → triaged → assigned → fixed → verified → closed
                    ↘ rejected (with reason)
                    ↘ deferred (approver + target release)
                    ↘ reclassified as change request (→ pm_change_control)
```

The last branch is the one that matters commercially. A "defect" that is really a request
for behaviour nobody specified is a change request, and the classification happens **before**
the fix, not after — because after the fix, the work is already paid for by the delivery
team.

Classify honestly in both directions: calling a genuine defect a change request to bill for
it destroys the client relationship faster than any schedule slip.

### QP-07 — Severity is never adjusted to pass a gate (RI-09)

Forbidden: lowering severity to meet an exit criterion, closing as "not reproducible"
without an investigation record, merging defects to reduce a count, deferring without a
named approver and a target release.

Every one of these makes the report better and the release worse. The exit criterion exists
to inform a go/no-go decision; a tuned severity disables it silently, and the defect ships.

### QP-08 — Regression is planned, sized and in the WBS

Every fix carries the risk of breaking something else, and that risk grows with every
release. Decide in the plan: what is re-run at each level, how it is automated, and what the
ongoing execution cost is per cycle.

A regression suite that takes three days to run manually will not be run under schedule
pressure, which is exactly when it is needed. Either automate it or shrink it deliberately —
but decide that now, in writing, not implicitly at the moment of the release.

---

## Part 3 — Quality metrics

Definitions used in the quality report (`pm_reporting`):

| Metric | Formula | Reading |
|---|---|---|
| Review density | findings ÷ document | near zero means the document was not read, not that it was perfect |
| Defect density | defects ÷ size | far **below** the floor means under-tested, not high quality |
| Phase containment | defects injected and found in the same phase ÷ injected in it | the single most informative number available |
| Test progress | executed ÷ planned, and passed ÷ executed | report blocked cases separately; they hide the truth |
| Coverage | from the runner, named run and build | a floor, never a goal |
| Escaped defects | first found at UAT or later ÷ all defects | the number the client experiences |
| Defect S-curve | cumulative found vs closed, by date | shape says more than any single number |

### QP-09 — Attribute defects to the phase that injected them

Not the phase that found them, and not the phase that fixed them.

| The defect is | Injected in |
|---|---|
| the requirement was wrong or missing | requirements |
| the requirement was right, the design contradicted it | design |
| the design was right, the code did something else | implementation |
| the code was right, the test asserted the wrong thing | test design |

Recording everything as "implementation" because that is where the fix happened makes
containment report 100% for every upstream phase and teaches nothing. The metric is only
worth collecting if the attribution can embarrass someone.

### QP-10 — Read the S-curve, and say what it predicts

| Shape | Reading |
|---|---|
| found flattening, closed converging | ready to exit |
| found still rising at the planned exit date | the phase is not finished, whatever the schedule says |
| closed lagging by a widening gap | fix capacity is the bottleneck; adding testers makes it worse |
| both flat, early | testing has stopped, not converged — check execution progress |
| a step change in found | a new build broke something, or a new tester started |

A gate passed while the found-curve is still rising is the most common way a project moves
its defects into UAT rather than fixing them.

---

## Exit criteria

- [ ] Every quality objective has a target, a condition and a measurement method (QP-01)
- [ ] Targets agreed, and matching the technical pack's where one exists (QP-02)
- [ ] Master test plan covers every level with objective entry/exit criteria
- [ ] Every requirement has at least one verifying test case (`{{profile.quality.targets.requirement_coverage}}`)
- [ ] Defect severity model, lifecycle and SLAs agreed before testing starts
- [ ] Regression strategy defined and its effort in the WBS (QP-08)
- [ ] Evidence rules agreed, including what the client receives
- [ ] Quality plan and test plan approved per `{{profile.governance.approvals}}`
