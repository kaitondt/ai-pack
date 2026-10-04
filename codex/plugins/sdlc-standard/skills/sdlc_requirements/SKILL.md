---
name: sdlc_requirements
description: "P1 — requirements analysis. Produces the SRS: functional requirements (REQ-*), non-functional requirements (NFR-*), use cases, business rules and acceptance criteria, each traced to a BR-*. Contains the testability rules and the requirement writing standard. Load for ALL requirement-authoring tasks."
---

# P1 — Requirements Analysis

> Prerequisite: `sdlc_project` loaded; P0 gate passed.
> Every `REQ-*` traces to a `BR-*`; every `NFR-*` states a measurable target (P1 gate).

---

## The document chain

```
scope.md + business-requirements.md + elicitation records     (P0 output, the anchors)
        ↓
SRS §Functional     REQ-*   what the system does
SRS §Non-functional NFR-*   how well it must do it
SRS §Use cases              how an actor achieves a goal
SRS §Business rules         the conditions and calculations behind the requirements
SRS §Acceptance criteria    the seed of P7/P8 test cases
        ↓
input to P2 basic design
```

The SRS is one document (or one per subsystem). Splitting functional and non-functional
requirements into separate documents with separate owners is the standard way NFRs end up
unimplemented — nobody designs against a document they were not given.

---

## SRS structure

| § | Content |
|---|---|
| 1 | Purpose, scope reference, intended audience, definitions reference |
| 2 | System context — actors, external systems, boundary diagram |
| 3 | Functional requirements — the `REQ-*` table, grouped by business area |
| 4 | Use cases — one per actor goal, with main and alternate flows |
| 5 | Business rules — conditions, calculations, state transitions |
| 6 | Data requirements — logical entities, ownership, retention, volume |
| 7 | Non-functional requirements — the `NFR-*` table |
| 8 | Interfaces — one subsection per external system |
| 9 | Constraints, assumptions (`ASM-*`) and dependencies |
| 10 | Acceptance criteria |
| 11 | Open Items (DS-10) |

---

## Writing a functional requirement

| ID | Requirement | Priority | Source | Rationale | Verification |
|---|---|---|---|---|---|
| `REQ-ORD-014` | The system shall reject an order whose total exceeds the customer credit limit, before the order enters approval. | Must | `BR-ORD-002` · `DEC-031` | prevents over-limit shipments | ST-ORD-004 |

**RQ-01 — One requirement per row.** A row containing "and" usually contains two
requirements with different priorities and different test cases. Split it.

**RQ-02 — Testable or not a requirement.** Before writing it, answer: *what would I
execute to prove this?* If the answer is "look at it and form an opinion", rewrite it.
The `Verification` column is filled at P1, not at P7 — an empty one is a P1 defect.

**RQ-03 — "Shall" for mandatory, "should" for recommended**, used consistently. A
"should" in a fixed-price contract needs an explicit note about whether it is in scope.

**RQ-04 — No solution in the requirement.** No screens, no field widths, no table names,
no technology. "The system shall display a dropdown of active warehouses" is a design
decision wearing a requirement's clothes; the requirement is "the user shall select from
warehouses currently active for the customer".

**RQ-05 — Every row cites a source** (`BR-*`, `DEC-*`, elicitation record, or external
obligation). A `REQ-*` with no source is unrequested scope (RS-06).

**RQ-06 — Negative and boundary behaviour is part of the requirement**, not an
implementation detail. What is rejected, what the user sees when it is, and what happens
to the data.

**RQ-07 — TBD carries an ID and a date** (RS-03). The SRS may be reviewed with TBDs; it
may not be baselined with them.

---

## Writing a non-functional requirement

| ID | Category | Requirement | Target | Condition | Measurement | Verified at |
|---|---|---|---|---|---|---|
| `NFR-PERF-003` | PERF | Order search response | ≤ 2.0 s p95 | 50 concurrent users, 5M orders | ST performance script `perf/order-search.js` | P7 |

**NF-01 — Target, condition, measurement, phase.** All four, always (RS-07). A missing
condition makes the target meaningless; a missing measurement makes it unverifiable.

**NF-02 — Categories are fixed**: `PERF`, `SEC`, `AVAIL`, `OPS`, `USE`, `COMPL`.
Minimum coverage to consider at P1:

| Category | Questions that must have answers |
|---|---|
| PERF | response times at which percentile, throughput, data volume now and at +3 years |
| SEC | identity, authorisation model, data classification, retention, audit |
| AVAIL | uptime target, maintenance windows, RPO / RTO, degraded-mode behaviour |
| OPS | logging, monitoring, alerting, backup, restore rehearsal, runbook ownership |
| USE | accessibility standard, supported browsers/devices, languages, offline behaviour |
| COMPL | regulations, data residency, retention obligations, audit evidence |

**NF-03 — An NFR nobody can afford is a decision, not a requirement.** When a target is
technically infeasible or unaffordable, say so with evidence and take it back to the
owner. Silently designing for a target you know cannot be met produces a system that fails
its own gate at P7, after everything is built.

**NF-04 — Every NFR names the architecture decision that delivers it** by P2 (X-09).
An NFR with no design behind it is discovered at P7, which is the most expensive moment
to discover it.

---

## Use cases

One per actor goal. Main flow, alternate flows, exception flows, preconditions,
postconditions, and the `REQ-*` it realises.

Use cases are how the requirement set is checked for **completeness**: walk each actor
through their working day and find the step that no requirement covers. That step is
almost always a real gap, not a documentation gap.

---

## Acceptance criteria

Given / When / Then, one set per requirement, written at P1 by the product owner and the
analyst together.

These are the seed of the UAT scenarios (P8) and the ST cases (P7). Written at P1, they
force the requirement to be testable while it is still cheap to rewrite. Written at P7,
they become a negotiation about what the requirement meant.

---

## Cross-document consistency

Before declaring P1 complete:

| Check | Assertion |
|---|---|
| R-01 | every `BR-*` is covered by at least one `REQ-*` (else: missed scope) |
| R-02 | every `REQ-*` cites at least one `BR-*`, `DEC-*` or external obligation |
| R-03 | every `REQ-*` has a verification reference and is testable |
| R-04 | every `NFR-*` has target, condition, measurement method and phase |
| R-05 | every use case realises at least one `REQ-*`, and vice versa |
| R-06 | no requirement contradicts a constraint in `{{profile.constraints}}` or the scope statement |
| R-07 | no TBD, and every `ASM-*` the SRS depends on is confirmed |
| R-08 | terminology matches `{{profile.paths.glossary}}` throughout |

Write the results into `{{profile.paths.traceability}}` and report counts.

---

## Exit gate

- [ ] SRS complete, with an Open Items section
- [ ] R-01..R-08 pass
- [ ] Acceptance criteria exist for every Must requirement
- [ ] `{{profile.gates.P1_requirements.exit}}` assertions hold
- [ ] Reviewed and baselined by `{{profile.stakeholders.product_owner}}`

Then run `/sdlc_phase_gate P1`. The SRS becomes a baseline; from that moment it changes
only through a change request (BL-02).
