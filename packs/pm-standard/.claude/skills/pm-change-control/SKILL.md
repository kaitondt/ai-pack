---
name: pm-change-control
description: "Integrated change control — change request intake, impact assessment across all baselines, option development, CCB decision, baseline update, cascade to the technical pack, and the change register. Load for ALL change-request, CCB, impact-assessment, scope-change and re-baseline tasks."
---

# Integrated Change Control

> Prerequisite: `pm-project` loaded. Baseline rules in `rules/pm/baseline-integrity.md`.

Change control exists so that a change is a **decision** rather than an event. The
alternative is not "no change" — changes happen regardless — it is change that nobody
priced, nobody approved, and nobody can point to when the project is late.

This pack owns intake, impact, approval and baseline update. When a technical pack is
installed, its CR workflow executes the document and code changes **after** approval here.

---

## The six phases

```
1. INTAKE      log it, classify it, decide if it is even a change
2. ASSESS      impact across every dimension; develop options
3. DECIDE      the authority for that impact approves, rejects or defers   ← GATE
4. APPLY       update the baselines; hand execution to the technical pack
5. VERIFY      the change is in, and the baselines are consistent again
6. RECORD      close the CR with actual effort against the estimate
```

Phases 1–3 change nothing. **No work starts before phase 3.** Starting analysis is fine;
starting design or code is how a rejected change gets delivered anyway.

---

## Phase 1 — Intake

### IC-01 — Log every change request, including the trivial ones

`{{profile.change_control.register}}`, id `{{profile.change_control.id_format}}`.

Record on arrival: what was asked, by whom, when, why, the urgency claimed, and the source —
client request, defect reclassification, internal proposal, regulatory, or a discovery
during implementation.

Including the small ones is the point (PB-07). Ten absorbed four-hour changes is a week
nobody can account for, and the reason nobody can account for it is that nothing recorded
them. The register costs five minutes per entry and is what makes a scope conversation
possible at all.

### IC-02 — Classify before assessing

`{{profile.change_control.classes}}`. The classification that matters commercially is the
first question:

| It is | When | Consequence |
|---|---|---|
| **A defect** | the delivered behaviour contradicts a baselined document | fixed at the vendor's cost |
| **A clarification** | the document is silent or genuinely ambiguous | `CR-CLARIFY`; whoever bears the risk depends on the contract |
| **A change** | the request contradicts or extends a baselined document | estimated and decided |

This single determination is where most commercial disputes live, and it is decided by
reading the baselined document — not by who is more insistent, and not by whose interpretation
is more reasonable.

Two disciplines make it survivable: **quote the exact text** of the baselined document in the
assessment, and make the determination **before** the fix, never after. After the work is
done, the argument is about money already spent.

### IC-03 — Under fixed-price, every change is a contractual event

`{{profile.project.contract_type}}`. Under fixed-price, an absorbed change is margin given
away silently and permanently. Under time-and-materials, it is the client's budget being
spent without their decision. Under both, the answer is the same: record, estimate, decide.

The difference is who is harmed by skipping it.

---

## Phase 2 — Assess

### IC-04 — Assess every dimension, even when the answer is "none"

`{{profile.change_control.impact_dimensions}}`:

| Dimension | The question |
|---|---|
| Scope | which requirements, deliverables and work packages change |
| Schedule | effort, **and** whether it lands on the critical path — different questions |
| Cost | effort × rate, plus non-labour; which control account absorbs it |
| Quality | new test cases, regression scope, does any quality target move |
| Risk | new risks introduced, existing risks changed |
| Resource | who does it, are they available, what does that displace |
| Contract | deliverable list, payment milestones, acceptance criteria, SLA |
| Dependencies | other teams, other systems, external parties |
| Test | which cases change; which executed results become invalid |
| Documentation | every document that must be updated — the usual underestimate |

An unassessed dimension is how a change lands as a surprise three weeks later. The two most
frequently skipped are **documentation** (the full cascade, not just the obvious document)
and **test** (previously passed cases that are now invalid and must be re-run).

### IC-05 — Schedule impact is not effort impact

Forty hours of work is a two-week delay if it lands on the critical path, and no delay at all
if it does not (WB-09). State them separately:

```
Effort impact   : +40 person-hours
Schedule impact : +0 days (PRJ.5.2 has 9 days of float) — but float drops to 4 days,
                  so any further change here becomes critical
Cost impact     : +{currency}, from control account PRJ.5
```

The float note matters. Absorbing a change into float is legitimate and free once; the second
absorption is not, and the report should say so before the second change arrives.

### IC-06 — Present options, not a single answer (min `{{profile.change_control.min_options}}`)

```
Option 1 — Implement in this release
  Effort +40 h · Schedule +0 d (uses float) · Cost +X · Risk: PRJ.5 loses its float
Option 2 — Defer to release 2
  Effort +32 h later · Schedule +0 d now · Cost +Y · Risk: client works around it for 3 months
Option 3 — Implement, and drop REQ-{AREA}-{NNN} to compensate
  Effort +8 h net · Schedule +0 d · Cost +0 · Risk: needs client agreement on the trade

Recommend: option 2 — the workaround is acceptable per the client's own process description,
and option 1 removes the last float protecting M3.
```

A single option is not a decision, it is a request for agreement. Three options with
consequences let the approver own the outcome — which is both correct governance and the
reason the decision comes back faster.

### IC-07 — Estimate the whole cascade (EM-08)

Not just the code. Analysis · every affected design document · code · new and modified unit
tests · integration and regression testing · test case updates · user documentation · release
· re-verification of affected already-tested behaviour · translation if applicable · the
management overhead of the change itself.

Under-estimating a CR is worse than under-estimating original scope: it is a number the
client explicitly approved, and revisiting it costs credibility that the next CR will need.

---

## Phase 3 — Decide (the gate)

### IC-08 — The authority matches the impact (DA-02)

`{{profile.change_control.authority}}`. Below the first threshold the PM decides and records;
above it, the CCB; above that, the steering committee.

The decision record contains: the options presented, the option chosen, **why**, the approver,
the date, and the baseline impact accepted. Recorded as a `DEC-*` and referenced from the CR.

| Outcome | Meaning |
|---|---|
| Approved | proceed, baselines update |
| Approved with conditions | conditions are `ACT-*` with owners and dates |
| Deferred | to a named release or decision date — not "later" |
| Rejected | with the reason, kept in the register (PN-03) |

Rejected CRs are never deleted. The record that a change was requested and declined is
exactly what the acceptance discussion needs.

---

## Phase 4 — Apply

### IC-09 — Baselines update before execution begins

Order matters:

1. Update the scope baseline — scope statement, WBS, WBS dictionary (PB-02)
2. Update the schedule baseline, or record the float consumption
3. Update the cost baseline and the control account
4. Update the RTM, the quality plan and the test plan if affected
5. Record the version bump in each document's revision history, citing the CR (MD-02)
6. **Then** hand execution to the technical pack

Executing before the baselines move means the plan describes a project nobody is running, and
every subsequent report measures against the wrong thing.

### IC-10 — Hand off cleanly to the technical pack

| Technical pack | Hand off to |
|---|---|
| `sdlc` | `/sdlc-cr-design` → `/sdlc-cr-implement` → `/sdlc-cr-report` |
| `migration` | `/mig-cr-design` → `/mig-cr-implement` → `/mig-cr-report` |
| none | the team, against the updated baselines |

The technical pack's cascade rules govern document order there. This pack does not duplicate
that work; it verifies afterwards that the baselines and the deliverables agree
(`/pm-sync-technical`).

### IC-11 — Emergency changes skip the queue, never the record

When an urgent change must start before formal approval: it needs verbal authorisation from
the approver who would have decided, it is logged immediately as a CR with the authorisation
noted, and the full record — impact assessment, options, formal approval — is completed
within the retro-documentation window.

Without that window written into the plan (PP-05), the first emergency establishes that
undocumented change is acceptable, and the register stops being a record of the project.

---

## Phase 5–6 — Verify and record

Verify: the change is present in the deliverables, the baselines are internally consistent
(PB-04), test cases updated, traceability rows updated, and no unrelated change rode along
with it.

Then close the CR with **actual effort against the estimate**. That comparison is the only
input that makes the next CR estimate better, and it is the first thing dropped when the
project is busy.

```
CR-{nnn} — {title}                                    {approved | rejected | deferred}
  Class        : {class}          Raised by {who} on {date}
  Determination: {defect | clarification | change} — per {document} v{version}, §{section}
  Options      : {n} presented; {chosen}, approved by {who} on {date}
  Impact       : effort {h} · schedule {d} · cost {amount} · quality {what} · risk {ids}
  Baselines    : scope v{x} · schedule v{y} · cost v{z}
  Executed by  : {technical pack commands / team}
  Actual       : {h} vs estimated {h} ({variance}%)  — {why, if material}
```

---

## Register health

Reported monthly, cumulatively (RG — monthly §7):

```
CRs to date {n}: approved {a}, rejected {r}, deferred {d}, in flight {f}
Cumulative baseline impact: +{h} hours, +{d} days, +{amount}
Largest contributors: {CR ids}
Absorbed without a CR: 0        ← any other number is a process failure (PB-07)
```

The cumulative line is the one the steering committee is actually deciding about. Each change
was reasonable on its own; the sum is what moved the project, and it is invisible until
someone adds it up.
