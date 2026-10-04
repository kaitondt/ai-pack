---
name: sdlc_test_uat
description: "P8 — user acceptance test. Preparing the UAT plan and environment, supporting client-run execution, triaging client-reported issues into defect / change request / usage question, and recording acceptance. Load with sdlc_test_design for ALL UAT tasks."
---

# P8 — User Acceptance Test

> Load with `sdlc_test_design`. Prerequisite: ST exit holds.
> **UAT verifies the business need**, and it is run by
> `{{profile.testing.uat.executed_by}}` — not by the delivery team (TR-03).

UAT is not a test phase the vendor runs on the client's behalf. It is the client deciding
whether the system does their job. The vendor's role is to make that decision cheap to
reach: a ready environment, ready data, ready scenarios, and same-day answers.

---

## Entry criteria

| # | Criterion | Why it blocks |
|---|---|---|
| E1 | ST exit holds; no open Critical or High defect | the client should not be finding what ST was for |
| E2 | UAT environment deployed from the ST-verified build | |
| E3 | Client test data prepared, and the client can reach it | data preparation is the most common start-day delay |
| E4 | UAT plan signed by `{{profile.stakeholders.business_owner}}` | it defines what "accepted" means |
| E5 | Client testers briefed; a defect-reporting channel agreed | |
| E6 | Known limitations and deferred defects disclosed **in writing, before start** | |

E6 is not optional and not negotiable. A deferred defect the client discovers themselves
during UAT costs more trust than the defect costs effort — and the conversation it starts
is about honesty, not about the defect.

`{{profile.testing.uat.entry_signoff_required}}` governs whether E4 is a formal sign-off.

---

## The UAT plan

| § | Content |
|---|---|
| 1 | Objective and acceptance definition — what must be true for the client to accept |
| 2 | Scope: business processes in and out |
| 3 | Scenarios — one per acceptance criterion from the SRS (T-07) |
| 4 | Participants, roles, schedule |
| 5 | Environment, data, accounts, and who provides what |
| 6 | Defect reporting: channel, template, severity definitions, SLA |
| 7 | Known limitations and deferred defects (E6) |
| 8 | Exit criteria and the acceptance record format |

**Scenarios are written in the client's language, from their acceptance criteria** — not
copied from the ST scenarios. An ST scenario says "the order reaches status Shipped"; a
UAT scenario says "I can complete a same-day dispatch for a walk-in customer".

**UA-01 — every acceptance criterion in the SRS has a scenario** (T-07). If the client
wants to test something no acceptance criterion covers, that is either a missed requirement
(a finding worth having) or out of scope (a CR).

**UA-02 — the client may test off-script, and should.** Scenarios are the floor, not the
ceiling. Their off-script findings are the most valuable output of the phase, because they
are the ones no specification predicted.

---

## Supporting execution

`{{profile.testing.uat.support_model}}`. The daily rhythm that works:

1. **Morning**: environment and data verified healthy before the client starts.
2. **During the day**: report intake, no filtering. Every report is recorded, even the ones
   that turn out to be usage questions.
3. **Same day**: triage every new report (below), and tell the reporter what it was
   classified as and what happens next.
4. **End of day**: a short status — reports received, classified, fixed, in progress, and
   what will be deployed tomorrow.

**UA-03 — deploy on an announced cadence, not continuously.** A UAT environment that
changes under the testers invalidates their in-progress results and their trust. Batch
fixes, announce the deployment, and say what changed.

---

## Triage: three outcomes, and the classification matters

Every client report is one of:

| Class | Definition | Handling |
|---|---|---|
| **Defect** | the system does not do what the baselined specification says | fix under `{{profile.testing.uat.defect_sla_hours}}`; `BUG-*`; injection phase recorded |
| **Change request** | the system does what the specification says; the client wants something different | `sdlc_change_request` — options, estimate, approval |
| **Usage / data** | the system behaves correctly and the report came from a misunderstanding, a data setup, or an environment issue | answer, and record it — repeats are a documentation or training defect |

**UA-04 — the classification is evidence-based and it is shown.** State which requirement
or design item the behaviour was checked against, and quote it. A defect classified as a CR
without that evidence reads as a vendor avoiding work — and a CR classified as a defect
gives away scope that was never agreed.

**UA-05 — when the specification is genuinely ambiguous, say so.** The honest answer is
"the requirement does not decide this; here is what the system does and here is what it
would cost to change" — followed by a `DEC-*`. Arguing a stretched reading of an ambiguous
requirement wins the ticket and loses the relationship.

**UA-06 — a usage report that recurs is a defect in the documentation or the UI**, not in
the user. Three testers hitting the same confusion is a finding; record it as one.

---

## Defect handling during UAT

- Severity per `{{profile.quality.severity}}`, agreed with the client — **their** severity
  assessment, not the vendor's, decides priority.
- SLA per `{{profile.testing.uat.defect_sla_hours}}`.
- Every fix ships with the regression case that would have caught it
  (`{{profile.maintenance.regression_test_required}}`).
- Every defect records its **injection phase** (TR-07). A UAT defect injected in P1 is a
  requirements-process finding, and it is the most valuable metric this phase produces
  (QM-06).
- Re-test is done by the reporter, not by the fixer.

---

## Acceptance record

The deliverable of P8. It states:

| Field | Content |
|---|---|
| Scenarios | executed / passed / failed, with the register reference |
| Requirements covered | `REQ-*` covered by an executed scenario |
| Defects | raised, fixed, deferred, accepted — each with severity and status |
| Deferred items | each with the approver, the reason and the target release |
| Known limitations | as disclosed at E6, plus anything found during the phase |
| Acceptance | accepted / accepted with conditions / not accepted |
| Approver and date | from `{{profile.stakeholders.business_owner}}` |

**UA-07 — "accepted with conditions" names each condition, its owner and its date.**
An unqualified condition becomes an argument at the warranty boundary.

---

## Exit criteria

- [ ] every UAT scenario executed with a recorded verdict
- [ ] every acceptance criterion covered (T-07)
- [ ] every defect closed, deferred with a named approver, or accepted in writing
- [ ] every report classified with evidence, including the usage ones
- [ ] acceptance recorded with approver and date
- [ ] `{{profile.gates.P8_uat.exit}}` assertions hold

Then run `/sdlc_phase_gate P8`, and hand over to P9 with the runbook, the known-limitations
list, and the deferred-defect list as the starting backlog.
