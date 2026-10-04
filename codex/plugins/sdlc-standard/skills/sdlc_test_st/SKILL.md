---
name: sdlc_test_st
description: "P7 — system test. Business-process scenarios against the baselined requirements on a production-like environment, plus the non-functional test set: performance, security, availability/failover, data volume, operability and regression. Entry and exit criteria, measurement discipline, evidence. Load with sdlc_test_design for ALL ST tasks."
---

# P7 — System Test

> Load with `sdlc_test_design`. Prerequisite: IT exit holds; staging deployed from a
> release build. **ST verifies the requirements** (TR-03).

System test is the last phase where the delivery team can still find its own defects. It is
also the only phase that tests the **system as a whole**: whole business processes, real
volumes, real failure, and the non-functional requirements nobody has measured yet.

If ST is run as "IT again, but on staging", the project has skipped it — and P8 becomes
the phase where the client discovers what ST was for.

---

## Entry criteria — check before writing or running anything

| # | Criterion | Why it blocks |
|---|---|---|
| E1 | IT exit holds for every flow in scope | ST cannot isolate a defect that IT should have caught |
| E2 | Staging is deployed **from a release build**, not from a developer machine | otherwise the thing tested is not the thing shipped |
| E3 | Staging is production-like: data volume, configuration, integrations | a performance result on an empty database is not a result |
| E4 | Test data is prepared and masked (`references/rules/common/security.md`) | |
| E5 | The ST plan exists, with the NFR verification table from the P2 design (NF-§8) | |
| E6 | No open Critical or High defect from IT | |

An entry criterion waived is recorded with who waived it and what risk was accepted. It
will be quoted in the P8 gate discussion.

---

## Scope: two halves

### Half 1 — Business process scenarios

Keyed by **business scenario**, not by screen (`{{profile.testing.system_test.scenario_source}}`).

One scenario per end-to-end process a real user performs, including the parts that happen
on a different day, in a different role, or through a batch:

```
ST-ORD-001  Order to delivery, standard customer
  Day 1  sales creates the order              (role: sales)
  Day 1  credit check batch runs overnight    (batch: KK0010BT)
  Day 2  warehouse picks and confirms         (role: warehouse)
  Day 2  invoice is generated and sent        (interface: accounting)
  Day 3  the order appears in the daily report
```

Rules:

- **ST-01 — a scenario crosses roles, screens, batches and interfaces.** A scenario that
  stays inside one module is an IT case.
- **ST-02 — every `REQ-*` is covered by at least one executed scenario** (T-05). This is
  the completeness check the client will ask about, and it is checked against the
  traceability register, not against memory.
- **ST-03 — scenarios include the periodic processes**: month end, year end, cut-off,
  reconciliation, archival. These run once per period and therefore get tested once per
  project — here, or never.
- **ST-04 — regression is part of ST.** Every defect fixed during ST re-runs its scenario
  plus everything sharing the changed component.

### Half 2 — Non-functional verification

Driven by the §8 verification plan from `sdlc_nfr_design`. Every `NFR-*` gets an executed
case with a **recorded number** (T-06).

| Kind | What ST must actually do |
|---|---|
| Performance | run the named script, at the named concurrency, against the named volume; record p50/p95/p99, not an average |
| Load / soak | hold peak load for the stated duration; watch memory, connections, queue depth |
| Volume | run against the data volume the NFR names, including the largest table |
| Security | authentication, authorisation per role and per operation, session expiry, injection and access-control checks, secrets absent from logs and responses |
| Availability | kill each dependency in turn; verify the designed degraded behaviour (NF-03) |
| Recovery | restore from a backup, and measure against RPO/RTO — the first real rehearsal |
| Batch | run every job at peak volume inside its window; test restart and rerun (BT-R) |
| Operability | verify logs, monitoring signals, alerts and the runbook — by having someone who did not build it follow the runbook |

**ST-05 — a measurement without its conditions is not a measurement** (QM-01). Record
environment, data volume, concurrency, duration, and the tool. A number without them cannot
be reproduced, compared, or defended.

**ST-06 — an NFR that cannot be measured with the tools available is an open item now**,
raised to the owner with what is needed. It is not silently marked passed by inspection.

**ST-07 — the operability test needs a stranger.** The person who wrote the runbook cannot
test it: they fill the gaps from memory without noticing. Someone else follows it, and
every place they have to ask a question is a defect in the runbook.

---

## Pipeline

Same checkpoint shape as `sdlc_test_design` §4, with ST-specific steps:

1. **Scope** — list the business processes from the SRS use cases; map each to the
   `REQ-*` and `NFR-*` it covers; identify the periodic processes.
2. **Q&A + pause** — the questions here are business-process questions: who does this
   next, what happens at month end, what do they do when it fails.
3. **Checklist + coverage pause** — one row per scenario, with the requirements it covers.
   Reviewed by the QA lead **and** a business representative: this is the last chance to
   discover a process nobody described.
4. **Write scenarios** — per `sdlc_test_design` §5, with roles and days made explicit.
5. **Execute in rounds** — `{{profile.testing.rounds.count}}` rounds, results and evidence
   recorded per round.
6. **Defect triage daily** — `sdlc_defect_management`. During ST, triage cadence matters
   more than fix speed: an untriaged defect blocks scenarios nobody has attributed yet.

---

## Execution discipline

- **Execute the case as written.** If a case cannot be executed as written, that is a
  finding about the case or the environment — not an invitation to improvise and record a
  pass.
- **A blocked case is `Blocked`, not `Pass` and not `Fail`.** Blocked cases are counted
  separately at the gate; a phase with 30 blocked cases has not been executed.
- **Evidence per case**, per `{{profile.testing.evidence}}` — ST is in
  `{{profile.testing.evidence.required_for}}`.
- **Re-run after a fix**, and record which round each result belongs to. A pass in round 1
  against a build that no longer exists is not evidence for the release.

---

## Exit criteria

- [ ] every `REQ-*` has an executed scenario with a verdict (T-05)
- [ ] every `NFR-*` has a recorded measurement with its conditions (T-06)
- [ ] no open Critical or High defect
- [ ] every deferred defect has an approver, a severity and a target release
- [ ] blocked cases: zero, or each with a reason and an accepted risk
- [ ] the defect S-curve has flattened (QM-07) — found and closed converging
- [ ] regression re-run after the last fix
- [ ] `{{profile.gates.P7_system_test.exit}}` assertions hold

**A rising found-curve at the exit date means the phase is not finished**, whatever the
schedule says. Passing the gate at that point moves the remaining defects into UAT, where
the client finds them (QM-07).

## Reporting

```
ST — {round}
  Scenarios       : {executed}/{planned}   pass {n} · fail {n} · blocked {n}
  REQ coverage    : {covered}/{total}      uncovered: {ids}
  NFR measurements: {done}/{total}         missed target: {ids with numbers}
  Defects         : S1 {n} · S2 {n} · S3 {n} · S4 {n}   open {n}
  Injection phase : P1 {n} · P2 {n} · P3 {n} · P4 {n}
  Curve           : found {n} cumulative, closed {n} cumulative — {flattening|rising}
  Gate            : {each exit criterion, pass/fail}
```
