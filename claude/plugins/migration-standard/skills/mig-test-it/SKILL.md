---
name: mig-test-it
description: "P6 — the integration test case pipeline: flow scoping from the flow catalogue, source gathering per screen, checklist, flow cases and E2E scenarios, bounded self-review. Defines the IT/UT boundary and the API scope exclusion. Load with mig-test-design for ALL IT authoring tasks."
---

# P6 — Integration Test Case Pipeline

> Load with `mig-test-design`. Prerequisite: `mig-project` resolved; UT exists for most
> modules in the flow (IT reuses it rather than re-deriving field detail).

---

## The IT/UT boundary — decide this before writing anything

IT tests **flows and integration points**. It does not repeat UT.

| In scope for IT | Belongs to UT |
|---|---|
| a business flow crossing two or more screens | one screen's field validation |
| state carried from one screen to the next | one field's boundary values |
| data written by screen A, read by screen B | one screen's error messages |
| the hand-off between surfaces (desktop → handheld) | one screen's layout |
| batch output consumed by an online screen | one function's calculation |
| the flow's end state in the data store | one dropdown's option list |

**API payload scope.** When `{{profile.testing.integration.api_payload_in_scope}}` is
false, IT does not assert request/response bodies, HTTP status codes or DTO shapes. Those
are verified by the interface design review and the automated tests. IT asserts what the
**user and the data** show. Writing payload assertions into IT produces cases the manual
tester cannot execute.

A case that could be executed on a single screen with no predecessor state is a UT case in
the wrong file. Move it.

---

## Step 1 — Flow scope and sources

**1a. Resolve the flow.** Read `{{profile.testing.integration.flow_catalogue}}` for the
requested flow id: flow group, scope level, main scenario, related screens, review points.
Split the related-screens field into individual module ids.

For an end-to-end flow, also read `{{profile.testing.integration.e2e_swimlane}}` in full.
Those steps are a **fixed checkpoint frame** — do not add or drop steps. Each step names
the sub-flow it belongs to, which is how you gather the right screens for it.

**1b. Read the strategy once per flow.** From
`{{profile.testing.integration.strategy_guide}}`: the integration testing strategy, the
scope exclusions, the environment and devices for preconditions, and the evidence rules.
Read it once and apply it across the whole flow rather than per screen.

**1c. Gather per screen, in this priority order:**

1. the module's existing UT file — reuse its preconditions and known behaviour
2. the screen and function design — when the module has no UT yet
3. the legacy source — when the design is silent on flow behaviour

Reusing UT is not laziness: it keeps the two documents consistent, and a divergence
between them is itself a finding.

**1d. Ask only what the flow actually needs.** IT questions are about sequence, state
hand-off and end state — not field detail. A question answerable by reading the UT is not
a question.

## ⏸ Pause — the human answers, if anything was asked

Skip when there are no questions. Do not manufacture questions to justify the pause.

---

## Step 2 — Checklist

One row per intended scenario: TC ID, flow id, screens touched, scenario, case type,
priority.

**Case type** comes from a fixed enumeration for the project — main flow, alternate flow,
error recovery, cross-screen state, permission, layout integrity. Do not invent new type
values per flow; the type column is what makes the set countable across flows.

Density guidance by screen kind belongs in the project's own reference, not in judgement
applied per module: a list screen and a transactional screen do not deserve the same
scenario count.

## ⏸ Pause — coverage review by a human

Same purpose as the UT pause: catch a missing flow while it costs one line.

---

## Step 3a — Flow cases

Per scenario: numbered preconditions, numbered steps across screens with the screen id on
each step, and an expected result per step. Every step names which screen and which
surface it happens on — a reader must never have to guess where they are.

Data used in one flow must be consistent across its cases: the record created in an early
case is the record the later cases operate on. State that dependency in the precondition
rather than leaving it implicit.

## Step 3b — End-to-end scenarios

One scenario following the swimlane frame, step by step, with the hand-off between actors
and systems made explicit at each transition. The value of E2E is precisely the
transitions; the within-screen detail is already covered.

---

## Step 4 — Bounded self-review

| Pass | Question |
|---|---|
| A — flow fidelity | does the case sequence match the flow catalogue and the swimlane? |
| B — coverage | every flow, every screen in scope, every case type, T-03 and T-04 |
| C — boundary | does any case duplicate UT-level detail? (move it) |

At most `{{profile.testing.pipeline.max_review_rounds}}` rounds, then escalate.

---

## Evidence

Each case declares the evidence it expects, named per `{{profile.testing.evidence.naming}}`
and stored under `{{profile.testing.paths.evidence_root}}`. Evidence naming is decided here, at
design time — renaming hundreds of screenshots after execution is avoidable work, and
mismatched names make a round unauditable.

---

## Reporting

```
IT — flow {FLOW}
  Screens in scope : {list}
  Sources          : UT reused {n}, design read {n}, legacy read {n}
  Checklist        : {n} scenarios by type {breakdown}
  Written          : {n} cases   E2E steps {n}/{swimlane total}
  Self-review      : round {n}/{max} — {PASS|FAIL}
  Coverage T-03/T-04 : {pass|fail}
  UT-level cases moved out : {n}
```
