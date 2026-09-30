# RULE FAMILY: TRACEABILITY

A development project is judged on whether the delivered system provably does what was
agreed. That proof is the traceability chain. It is maintained continuously, not
reconstructed the week before acceptance.

## The chain

```
BR-{AREA}-{NNN}         business requirement          P0
      ↓ decomposed into
REQ-{AREA}-{NNN}        functional requirement        P1
NFR-{CATEGORY}-{NNN}    non-functional requirement    P1
      ↓ realised by
{MODULE}-SC-{NNN}       screen design                 P2
{MODULE}-FC-{NNN}       function design               P2
{MODULE}-API-{NNN}      interface design              P2
{MODULE}-DT-{NNN}       data design                   P2
      ↓ detailed by
{MODULE}-DD-{NNN}       detail design                 P3
      ↓ implemented in
<source file>:<symbol>  code                          P4
      ↓ verified by
UT-{MODULE}-{NNN}       unit test                     P5
IT-{FLOW}-{NNN}         integration test              P6
ST-{SCENARIO}-{NNN}     system test                   P7
UAT-{NNN}               acceptance                    P8
      ↓ maintained through
BUG-{NNN} / INC-{YYYY}-{NNN} / CR-{NNN}                P9
```

## TR-01 — Every link is recorded, in both directions, as it is made

The register lives at `{{profile.paths.traceability}}` (CSV, one row per link):

```csv
business_id,requirement_id,design_id,detail_id,code_ref,test_ids,status,note
BR-ORD-002,REQ-ORD-014,SL0030PG-FC-001,SL0030PG-DD-003,OrderQuery.cs#Handle,"UT-SL0030PG-001;IT-ORD-002;ST-ORD-001;UAT-007",done,
```

- A row is appended the moment a downstream artifact is created — not in a later sweep.
- `status`: `todo | in-progress | done | blocked | deferred | open-question`
- `deferred` rows must carry a `note` with the decision reference that deferred them.

The register is the input to every gate check. If maintaining it feels like overhead, the
project is about to lose the ability to answer "is this requirement done?" — which is the
only question the client asks at acceptance.

## TR-02 — Orphans are defects

| Kind | Meaning | Severity |
|---|---|---|
| **Upward orphan** | design / code / test with no requirement ancestor | Critical — unrequested scope (RS-06) |
| **Downward orphan** | a baselined requirement with no descendant | Critical — missed scope |
| **Untested** | a requirement with design and code but no test at its V-model level | Critical at that level's gate |

Neither is closed by deleting the row. An upward orphan is either anchored to a
requirement, raised as a CR, or removed. A downward orphan is either implemented or moved
out of scope by a recorded decision.

**Change requests are the second legitimate ancestor.** Behaviour agreed after a baseline
has no `BR-*` by construction. Record the CR id in the ancestor position, with the report
path in `note`:

```csv
CR-014,REQ-ORD-031,SL0030PG-SC-001,SL0030PG-DD-003,OrderGrid.tsx#columns,"UT-SL0030PG-014",done,change-requests/CR-014_order-remarks-column.md
```

Without that row the artifact is an upward orphan, and correctly so: an unrecorded CR is
indistinguishable from unrequested work.

## TR-03 — The V-model binding

Every left-side phase has a right-side phase that verifies it. The pairing is fixed by
`{{profile.testing.levels}}`:

| Specification | is verified by | Level | Gate |
|---|---|---|---|
| Detail design (P3) | Unit test | UT | P5 |
| Basic design (P2) | Integration test | IT | P6 |
| Requirements (P1) | System test | ST | P7 |
| Business requirements (P0/P1) | Acceptance test | UAT | P8 |

Two consequences, both enforced at the gates:

1. **A specification that cannot be tested is not finished.** If no ST case can be written
   against a `REQ-*`, that requirement is not testable and P1 is not complete — regardless
   of how well written it reads (RS-07).
2. **A test whose basis is not baselined is provisional.** Cases may be drafted early;
   they are finalised against the baselined document, and re-checked if it changes.

## TR-04 — Phase gates are traceability assertions

A phase is complete when every assertion in `{{profile.gates.<phase>.exit}}` holds **and**
the register has no orphans for the artifacts that phase owns. `/sdlc_trace_check` is the
gate check; `/sdlc_phase_gate` records the result. Run both before declaring anything done.

## TR-05 — IDs are permanent

Once issued, an ID is never reused, renumbered or re-scoped. A superseded artifact keeps
its ID and gains `status: deferred` (or a successor note). Renumbering silently invalidates
every downstream reference and every review already done.

## TR-06 — Cross-document consistency checks

At P2/P3 these pairs must agree. Each mismatch is a Critical finding:

| Check | Left | Right |
|---|---|---|
| X-01 | Screen item list | Requirement input/output fields |
| X-02 | Screen grid columns | Data design / query result definition |
| X-03 | Function input params | API request fields |
| X-04 | Function output fields | API response fields |
| X-05 | Function error cases | API error codes |
| X-06 | Screen MSG-IDs | Function MSG-IDs |
| X-07 | Data design columns | DDL / migration scripts |
| X-08 | Detail design | Implemented code |
| X-09 | NFR targets | Architecture decisions that deliver them |
| X-10 | Every REQ | at least one design item realising it |
| X-11 | Mockup — fields, columns, buttons, messages, states, navigation, permissions | Screen design |
| X-12 | Environments the pipeline deploys to | `{{profile.system.environments}}` |

`/sdlc_review_design` runs X-01..X-07, X-09 and X-10; `/sdlc_generate_detail_design` runs
X-08 and emits the drift report; `/sdlc_generate_mockup` runs X-11 (sub-checks a..g);
`/sdlc_generate_infra` runs X-12.

X-11 and X-12 exist because both artifacts are routinely maintained outside the document
set. A mockup is the artifact everyone looks at, so a field that exists only there gets
built; an environment the pipeline knows about and the profile does not is where system
test runs against the wrong data.

Neither is resolved by editing one side to match the other. Decide against the baselined
SRS, and where the SRS is silent, raise an Open Item with an owner.

## TR-07 — Defects and incidents join the chain

A defect is not a free-floating ticket. `BUG-*` and `INC-*` rows carry:

- the artifact they were found against (`test_ids` or the screen/API id),
- the **injection phase** — the phase whose deliverable was wrong (`{{profile.quality.injection_phases}}`),
- and, once fixed, the test case added so it cannot recur (`{{profile.maintenance.regression_test_required}}`).

Injection phase is what makes phase containment measurable
(`rules/sdlc/quality-metrics.md` QM-04). Recording every defect as "found in test, injected
in code" because it is the easy answer destroys the only metric that tells you which phase
of your process is leaking.

## TR-08 — The register is append-friendly, conflict-averse

One row per link, sorted by `business_id` then `design_id`. Never rewrite unrelated rows in
the same edit — it makes the diff unreviewable and loses concurrent updates.
