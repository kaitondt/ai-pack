---
name: sdlc_test_it
description: "P6 — the integration test pipeline: flow scoping, source gathering per screen, checklist, flow cases and interface cases, bounded self-review. Defines the IT/UT and IT/ST boundaries and the interface-failure case set. Load with sdlc_test_design for ALL IT tasks."
---

# P6 — Integration Test

> Load with `sdlc_test_design`. Prerequisite: `sdlc_project` resolved; UT exists for most
> modules in the flow (IT reuses it rather than re-deriving field detail).
> **IT verifies the basic design** (TR-03).

---

## The boundaries — decide these before writing anything

IT tests **flows and integration points**. It repeats neither the level below nor the level
above.

| Belongs to UT | In scope for IT | Belongs to ST |
|---|---|---|
| one screen's field validation | a business flow crossing two or more screens | a whole business process across roles and days |
| one field's boundary values | state carried from one screen to the next | performance under load |
| one screen's error messages | data written by screen A, read by screen B | failover and recovery |
| one function's calculation | the contract between two components or systems | operability and monitoring |
| one dropdown's option list | batch output consumed by an online screen | the client's acceptance scenarios |

A case executable on a single screen with no predecessor state is a UT case in the wrong
file. Move it. A case whose point is "the system stays up under 50 users" is an ST case.
Move that too.

**Interface payload scope.** When `{{profile.testing.integration.api_payload_in_scope}}` is
false, the manual IT cases assert what the **user and the data** show, not request bodies
and status codes — those are asserted by automated contract tests. Writing payload
assertions into a manual case produces a case the tester cannot execute.

---

## Step 1 — Flow scope and sources

**1a. Resolve the flow.** Read `{{profile.testing.integration.flow_catalogue}}` for the
flow id: flow group, main scenario, screens involved, interfaces crossed, review points.
Split the related-screens field into individual module ids.

For an end-to-end flow, read `{{profile.testing.integration.e2e_swimlane}}` in full. Those
steps are a **fixed checkpoint frame** — do not add or drop steps. Each step names the
sub-flow it belongs to, which is how you gather the right screens for it.

**1b. Read the strategy once per flow**, from
`{{profile.testing.integration.strategy_guide}}`: scope exclusions, environment, test data
policy, evidence rules. Apply it across the whole flow rather than re-deciding per screen.

**1c. Gather per screen, in this priority order:**

1. the module's existing UT file — reuse its preconditions and known behaviour
2. the screen, function and interface design — when the module has no UT yet
3. the requirement — when the design is silent on flow behaviour

Reusing UT is not laziness: it keeps the two documents consistent, and a divergence between
them is itself a finding.

**1d. Ask only what the flow actually needs.** IT questions are about sequence, state
hand-off and end state — not field detail. A question answerable by reading the UT is not a
question.

## ⏸ Pause — the human answers, if anything was asked

Skip when there are no questions. Do not manufacture questions to justify the pause.

---

## Step 2 — Checklist

One row per intended scenario: TC ID, flow id, screens and interfaces touched, scenario,
case type, priority.

**Case type** comes from a fixed enumeration: main flow, alternate flow, error recovery,
cross-screen state, interface failure, permission, concurrency. Do not invent new type
values per flow; the type column is what makes the set countable across flows.

## ⏸ Pause — coverage review by a human

Same purpose as the UT pause: catch a missing flow while it costs one line.

---

## Step 3a — Flow cases

Per scenario: numbered preconditions, numbered steps across screens with the screen id on
each step, and an expected result per step. Every step names which screen and which surface
it happens on — a reader must never have to guess where they are.

Data used in one flow must be consistent across its cases: the record created in an early
case is the record the later cases operate on. State that dependency in the precondition
rather than leaving it implicit.

## Step 3b — Interface cases

For every interface in `{{profile.scope.external_systems}}` and every internal component
boundary the flow crosses, the minimum set:

| Case | Asserts |
|---|---|
| Happy path | the contract works end to end with real (or contract-faithful stub) data |
| Timeout | the caller's timeout fires, the user sees the specified behaviour (FD-E01) |
| Unavailable | the dependency is down; the design's degraded behaviour happens (NF-03) |
| Malformed response | an unexpected shape is rejected safely, not half-processed |
| Duplicate / replay | idempotency holds (FD-T03) |
| Slow response | the system does not queue requests until it collapses |

These six are the cases that make P9 quiet. They are also the ones skipped when the
external system is hard to make fail — which is why the strategy guide names the stub or
fault-injection mechanism at P2, not at P6.

## Step 3c — End-to-end scenarios

One scenario following the swimlane frame, step by step, with the hand-off between actors
and systems made explicit at each transition. The value of E2E is precisely the
transitions; within-screen detail is already covered.

---

## Step 4 — Bounded self-review

| Pass | Question |
|---|---|
| A — flow fidelity | does the case sequence match the flow catalogue and the swimlane? |
| B — coverage | every flow, every screen in scope, every interface, every case type (T-03, T-04) |
| C — boundary | does any case duplicate UT-level detail, or pre-empt ST? (move it) |

At most `{{profile.testing.pipeline.max_review_rounds}}` rounds, then escalate.

---

## Evidence

Each case declares the evidence it expects, named per
`{{profile.testing.evidence.naming}}` and stored under
`{{profile.testing.paths.evidence_root}}`. Evidence naming is decided here, at design time
— renaming hundreds of screenshots after execution is avoidable work, and mismatched names
make a round unauditable.

---

## Exit gate

- [ ] every flow and every interface covered (T-03, T-04)
- [ ] the six interface-failure cases exist per external dependency
- [ ] no open Critical or High defect
- [ ] `{{profile.gates.P6_integration_test.exit}}` assertions hold

## Reporting

```
IT — flow {FLOW}
  Screens in scope   : {list}
  Interfaces in scope: {list}
  Sources            : UT reused {n}, design read {n}
  Checklist          : {n} scenarios by type {breakdown}
  Written            : {n} cases   E2E steps {n}/{swimlane total}
  Self-review        : round {n}/{max} — {PASS|FAIL}
  Coverage T-03/T-04 : {pass|fail}
  Cases moved to UT / ST : {n} / {n}
```
