---
name: sdlc_test_design
description: "Shared test spine for P5–P8 — the level model, the ten viewpoints bound to formal test techniques, the mandatory writing rules, case formats, coverage arithmetic and the checkpoint pipeline. Load for ANY test task, alongside sdlc_test_ut / _it / _st / _uat, sdlc_test_automation, sdlc_test_review or sdlc_defect_management."
---

# Test Spine — levels, viewpoints, rules, pipeline

> Prerequisite: `sdlc_project` resolved. This skill holds what every test level shares.
> The level skills hold what differs.

**Expected values come from the baselined specification, never from the implementation**
(`rules/common/testing.md`). That rule outranks everything below. A case written by running
the code and recording the output passes forever and proves nothing.

---

## 1. The level model

Each level verifies a different document (`{{profile.testing.levels}}`, TR-03):

| Level | Verifies | Case is keyed by | Environment | Owner |
|---|---|---|---|---|
| UT | detail design | module | test | developer |
| IT | basic design | flow / interface | test | developer |
| ST | requirements | business scenario | staging | QA lead |
| UAT | business need | the client's own scenario | uat | business owner |

Two consequences worth stating before writing a single case:

- **Do not re-run one level's cases at the next.** An ST suite that re-tests field
  validation is paying for coverage it already has, and still has no case for the
  month-end process. Each level tests what only it can see.
- **A case whose basis document is not baselined is provisional.** Draft early; finalise
  against the baseline; re-check when the baseline changes through a CR.

---

## 2. Viewpoints, each bound to a technique

A viewpoint without a technique degenerates into "think of some cases". The technique is
what makes coverage arguable and reproducible.

| ID | Viewpoint | Technique | What it forces you to enumerate |
|---|---|---|---|
| VP-01 | Happy path | Scenario-based | the complete flow, start to finish |
| VP-02 | Empty / no result | Equivalence partitioning | the empty set as its own partition |
| VP-03 | Validation | Equivalence partitioning + boundary value analysis | field state per mode, input partitions, output correctness, error partitions |
| VP-04 | Authentication and session | State transition | authenticated → expired → redirected |
| VP-05 | Repeated or concurrent submission | State transition | enabled → locked → re-enabled; two users, one record |
| VP-06 | Server / network / dependency failure | Error guessing | failures the system must survive visibly |
| VP-07 | Cross-module navigation | Scenario-based | drill-down, forward, back, and state on return |
| VP-08 | Permission and role | Equivalence partitioning | one partition per role, including the role with none |
| VP-09 | Layout and rendering | Checklist-based | fixed UI criteria per surface and viewport |
| VP-10 | Data hazards | Boundary + domain analysis | rounding, precision, dates, time zone, collation, encoding |

Enabled set comes from `{{profile.testing.viewpoints}}`. Disable one only when it cannot
apply — a batch job has no VP-05 — never to reduce effort.

**VP-03 is the largest and the one that decides quality.** It splits four ways:

| Sub | Covers |
|---|---|
| VP-03a | item state — enabled, read-only, visible, per screen mode |
| VP-03b | input data — min, max, min−1, max+1, character class, type |
| VP-03c | output data — displayed values come from the right source; option count *and* content |
| VP-03d | error — over boundary, wrong character class, wrong format, business constraint |

Boundaries come from the **data design and the detail design**, not from the UI's
`maxlength` attribute. The UI is what is being tested.

**VP-10 is mandatory wherever numbers or dates appear.** See §6.

---

## 3. Mandatory writing rules

**TR-SE01 — steps and expected results are concrete.** Never "enter valid data", "check the
screen displays correctly". Name the field, the value, the control, the observable result.
A step a new tester cannot execute without asking a question is not a step.

```
✗  Enter search conditions and press search
✓  Enter 2026/04/01 in Order date (From), leave (To) empty, press Search
   → grid shows 3 rows, first row Order no. = D-000123
```

**TR-DR01 — cross-check every expected result against the data design.** Field length,
type, precision, rounding, sort order and default in the expected result must match. An
expected result that contradicts the data design is a defect in the test, and it will be
argued about during execution instead of before.

**TR-DD01 — no duplicate coverage.** Two cases differing only in irrelevant input are one
case. Before adding a case, name the partition or boundary it adds that no existing case
covers. If you cannot, do not add it.

**TR-AT01 — split a case when its expectations have different automatability.** A case
mixing "grid shows 3 rows" (automatable) with "the printed layout is legible" (manual) can
be neither automated nor cleanly reported.

**TR-PC01 — preconditions are numbered, executable steps**, not a prose paragraph. The
tester must be able to reach the starting state by following them in order.

**TR-SC01 — one repeated-submission case per primary action**, not per button.

**TR-NE01 — one dependency-failure case per screen**, not per endpoint. The behaviour under
test is the system's response to failure, which does not vary per endpoint.

**TR-CF01 — confirmation, success and redirect are one case, not three.** For any
create/update/delete: confirm dialog → success feedback → where the user lands.

**TR-AN01 — every expected value carries its anchor**: the design id, requirement id or
`DEC-*` it comes from. Structural expectations (a grid renders, a dialog closes) may be
blank. A business value with no anchor was invented (RS-01).

**TR-L01 — language and terminology** follow `{{profile.language.by_path}}` for the
destination directory, and label text is quoted exactly as the UI shows it.

**TR-ID01 — case ids** follow `{{profile.ids.test_id_format}}`, are unique within a file,
and are never renumbered once the file has been reviewed. Superseded cases are marked
removed, not deleted, so results from earlier rounds stay attributable.

---

## 4. The checkpoint pipeline

Every level is generated by a multi-step pipeline with human pauses. The shape is shared;
the steps differ per level.

```
analyse sources ──▶ ⏸ human answers open questions
        │
        ▼
final analysis ──▶ checklist ──▶ ⏸ human reviews coverage
                                        │
                                        ▼
                            write cases ──▶ self-review loop ──▶ done
                                                  ▲     │
                                                  └─────┘  bounded
```

**Why the two pauses exist.** The first buys the answers that stop invention: questions the
specification genuinely does not answer (RS-01). The second buys coverage review at the
cheap stage — a missing flow costs one line in a checklist and a full rewrite once cases
are detailed. Removing a pause removes the review it was there to buy.

`{{profile.testing.pipeline.human_pauses}}` says which pauses this project keeps.

**Checkpoint files.** Every step writes a timestamped file under
`{{profile.testing.paths.testcase_root}}/{dir}/{{profile.testing.paths.step_subdir}}/`.

- timestamp format `{{profile.testing.naming.timestamp}}`
- a later step reads the **newest** file of the prefix it needs
- a retry writes a new file; it never deletes the old one
  (`{{profile.testing.pipeline.keep_retry_history}}`) — the history is how a disputed case
  is traced back to the answer that produced it

**Bounded self-review.** The final step reviews and fixes its own output, at most
`{{profile.testing.pipeline.max_review_rounds}}` rounds. Still failing after that is not a
test-writing problem — escalate it, see `sdlc_test_review`.

---

## 5. Case table format

| Column | Rule |
|---|---|
| TC ID | `{{profile.ids.test_id_format}}`, unique, never renumbered |
| Level | UT / IT / ST / UAT |
| Viewpoint | one of the enabled VP ids |
| Verifies | the design or requirement id this case proves (TR-AN01) |
| Priority | High / Medium / Low, justified by business impact, not by effort |
| Precondition | numbered steps (TR-PC01); shared preconditions stated once per flow |
| Step | numbered, one action each, concrete (TR-SE01) |
| Expected result | numbered to match, observable, checked against the data design |
| Automatable | Yes / No / Partial — drives TR-AT01 splitting and automation scope |
| Evidence | required for the levels in `{{profile.testing.evidence.required_for}}` |
| Result columns | `{{profile.testing.rounds.columns}}` × `{{profile.testing.rounds.count}}`, left **empty** in the design |

Result columns stay empty until execution. A design document delivered with results filled
in cannot be distinguished from one where execution was skipped.

---

## 6. Coverage arithmetic

Coverage is checked per level, and the checks do not substitute for each other:

| Check | Assertion | Level |
|---|---|---|
| T-01 | every detail-design rule has ≥ 1 case | UT |
| T-02 | every error case in the function design has a case naming its `MSG-*` | UT |
| T-03 | every screen flow in the transition diagram has a scenario | IT |
| T-04 | every interface (endpoint, file, message) appears in ≥ 1 scenario | IT |
| T-05 | every `REQ-*` has ≥ 1 executed case | ST |
| T-06 | every `NFR-*` has a measurement with a recorded number | ST |
| T-07 | every acceptance criterion in the SRS has a UAT scenario | UAT |
| T-08 | every expected value is anchored or structural (TR-AN01) | all |
| T-09 | every enabled viewpoint appears wherever it applies | all |
| T-10 | no case duplicates another case's partition (TR-DD01) | all |

T-09 is the one usually missed: a module can have 40 cases and still have zero for VP-08,
because nobody asked which roles exist.

---

## 7. Hazards that need a case written deliberately

These produce the defects that survive to production. None of them is visible from the UI
alone, and each is a VP-10 or a data-design question.

| Hazard | Case to write |
|---|---|
| Rounding and precision | a value whose result differs from naive arithmetic (FD-R02) |
| Truncation | input at the maximum length, and one character over |
| Empty string vs null | a field stored empty, then filtered on (DT-03) |
| Time zone | a timestamp near midnight, and a date filter spanning it |
| Business calendar | month end, year end, a non-working day, a cut-off time |
| Collation and sort | a list whose order differs under a different collation |
| Encoding | input with extended characters, saved and redisplayed |
| Implicit ordering | a list with no stated tie breaker (IM-03) |
| Concurrency | two users updating one record under the stated policy (FD-T02) |
| Dependency failure | the external system down, slow, and returning an unexpected shape |
| Volume | the list at the row count the NFR names, not at 20 rows |

Where the specification is silent on one of these, that is an open question (RS-01): raise
it. **An expected result invented here becomes the specification that the implementation is
later "fixed" to match** — which is the most expensive way for a project to make a
decision.
