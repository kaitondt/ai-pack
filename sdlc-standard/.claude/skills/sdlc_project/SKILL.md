---
name: sdlc_project
description: "Development project spine — loads sdlc.profile.yaml, resolves {{profile.*}} tokens, and routes to the right phase skill. Load this FIRST for ANY task in a development project. Contains the 10-phase model, the V-model binding, phase gates, and the skill/agent routing table."
---

# Development Project — Spine Skill

> **Load this skill first for every task in this project.**
> Every other `sdlc_*` skill assumes the profile is already resolved.

---

## Step 1 — Load the profile (mandatory)

Read `.claude/sdlc.profile.yaml` from the repository root.

- **Missing** → stop. Tell the user to run `/sdlc_init`.
- **Contains unreplaced placeholders** (`<...>`) in a field you need → stop and ask for
  that field. Never substitute a guess into a deliverable.
- **A stakeholder role you need is unset** → stop. A decision with no owner cannot be
  recorded, and an unowned decision is an assumption (RS-02).

Hold the resolved values for the whole task. When a rule file or skill writes
`{{profile.paths.design_root}}`, substitute the profile value.

## Step 2 — Load the invariant rules

Always in force, regardless of phase:

| Rule file | Enforces |
|---|---|
| `rules/sdlc/requirement-sourcing.md` | nothing is specified without a source; assumptions are objects |
| `rules/sdlc/traceability.md` | the BR→REQ→design→code→test chain and the V-model binding |
| `rules/sdlc/baseline-change-control.md` | a baselined document changes only through a CR |
| `rules/sdlc/id-naming.md` | deterministic IDs |
| `rules/sdlc/document-standards.md` | deliverable skeleton and scope discipline |
| `rules/sdlc/quality-metrics.md` | what the gates measure, and how not to fake it |

## Step 3 — Route to the phase skill

| The task is about | Load |
|---|---|
| Scope, stakeholders, glossary, decisions, risks | `sdlc_discovery` |
| SRS, functional and non-functional requirements | `sdlc_requirements` |
| Basic design, any category | `sdlc_basic_design` + the category skill below |
| Architecture and quality attributes | `sdlc_nfr_design` |
| Screen / UI design documents | `sdlc_screen_design` |
| Mockups — HTML, design canvas, Figma, image exports | `sdlc_mockup` (+ `sdlc_screen_design`) |
| Function / processing design | `sdlc_function_design` |
| Table, column, DDL, data lifecycle | `sdlc_data_design` |
| API / interface design | `sdlc_api_design` |
| Batch / scheduled job design | `sdlc_batch_design` |
| Detail design, DD↔code drift | `sdlc_detail_design` |
| Writing code | `sdlc_implementation` (+ `sdlc_context_map` before starting) |
| Repository, CI/CD, environments, containers, IaC, secrets, monitoring | `sdlc_infrastructure` |
| Which files a change touches | `sdlc_context_map` |
| Test case documents, any level | `sdlc_test_design` + `sdlc_test_ut` / `_it` / `_st` / `_uat` |
| Automating manual test cases | `sdlc_test_automation` |
| Reviewing test case documents | `sdlc_test_review` |
| Defect triage, classification, ageing | `sdlc_defect_management` |
| One defect traced across every phase — evidenced injection, commit history, why it was not caught earlier | `sdlc_bug_trace` |
| Test artifacts between rounds | `sdlc_test_lifecycle` |
| Release readiness, cutover, rollback | `sdlc_release` |
| Incidents after go-live | `sdlc_maintenance` |
| A change to a baselined artifact | `sdlc_change_request` |
| Reviewing any deliverable | `sdlc_review_framework` |
| Metrics, gate reports, containment | `sdlc_quality_metrics` |
| Feeding review findings back into a skill | `sdlc_review_framework` + `/sdlc_refine_skill` |
| Translating deliverables | `sdlc_translate` |
| Reading or writing a deliverable in Excel, Word or CSV; registering a client template | `sdlc_document_io` |

Category skills are bound to directories by `{{profile.paths.bd_categories}}` — a task
touching `03.screen-design/` loads whatever skill that entry names.

**Load `sdlc_document_io` alongside the category skill whenever the deliverable is not
Markdown, or whenever the category has a registered template.** The pack ships no
templates: the client's own form is registered in `{{profile.templates.registry}}` and it
outranks the category skill's section list (DS-11).

---

## The phase model

```
P0 Inception ─ P1 Requirements ─ P2 Basic Design ─ P3 Detail Design ─ P4 Implementation
                                                                              │
   P9 Maintenance ─ P8 UAT ─ P7 System Test ─ P6 Integration Test ─ P5 Unit Test
```

| Phase | Produces | Command | Agent |
|---|---|---|---|
| P0 | scope, stakeholders, glossary, `BR-*`, decision log, risk register | `/sdlc_discover` | `sdlc_analyst` |
| P1 | SRS: `REQ-*`, `NFR-*`, use cases, acceptance criteria | `/sdlc_generate_requirements` | `sdlc_analyst` |
| P2 | design deliverables per category | `/sdlc_generate_basic_design` | `sdlc_bd_orchestrator` → `sdlc_bd_designer` |
| P3 | detail design + drift report | `/sdlc_generate_detail_design` | `sdlc_dd_designer` |
| P2 | mockups, in the project's form | `/sdlc_generate_mockup` | `sdlc_mockup_designer` |
| P4 | code | `/sdlc_implement_feature` | `sdlc_implementer` |
| P2/P4 | pipeline, environments, IaC, monitors | `/sdlc_generate_infra` | `sdlc_infra_engineer` |
| P5 | UT design + unit tests | `/sdlc_generate_test ut` | `sdlc_tester` |
| P6 | IT design + results | `/sdlc_generate_test it` | `sdlc_tester` |
| P7 | ST design + NFR measurements | `/sdlc_generate_test st` | `sdlc_tester` |
| P8 | UAT plan, support, acceptance record | `/sdlc_uat_prepare` etc. | `sdlc_uat_coordinator` |
| P9 | incident records, fixes, RCA, KB | `/sdlc_maintain_intake` etc. | `sdlc_maintenance_engineer` |
| any | automated scripts | `/sdlc_generate_testscript` | `sdlc_test_automator` |
| any | defect triage | `/sdlc_triage_defects` | `sdlc_defect_triager` |
| any | cross-phase bug traceability dossier | `/sdlc_trace_bug` | — |

### The V-model binding

Each left-side phase is verified by a specific right-side phase
(`{{profile.testing.levels}}`):

| Specification | Verified by | At |
|---|---|---|
| P3 Detail design | Unit test | P5 |
| P2 Basic design | Integration test | P6 |
| P1 Requirements | System test | P7 |
| P0/P1 Business need | Acceptance test | P8 |

Two rules follow, and both are gate items:

1. **A specification that cannot be tested is not finished.** If no case can be written
   against it at its verifying level, it fails its own phase gate.
2. **Test cases are drafted early and finalised against the baselined document.** If the
   basis changes, the cases are re-checked — that is the point of recording the binding.

### Phase gates

A phase is **not** complete until every assertion in `{{profile.gates.<phase>.exit}}`
holds and `/sdlc_trace_check` reports no orphans for that phase's artifacts.
`/sdlc_phase_gate` runs the check, records the result, and baselines the documents the
gate covers.

State the gate result explicitly when reporting a phase done. "Generated 46 files" is not
a completion report; "46/46 files, gate P2 passed, 0 Critical, 3 open items with owners"
is.

### Working across phases

Phases overlap in practice — one module can be in P4 while another is in P2. The gate is
evaluated **per module** for P2–P6, and **system-wide** for P0, P1, P7, P8 and P9. A
system test cannot be partially passed: it verifies the system, not a module.

Under `delivery_model: agile-with-gates`, P4–P6 run per sprint and only the RA, BD, ST and
UAT gates are hard stops. The gate assertions themselves do not change.

### Change requests are cross-cutting, not a phase

A change to a baselined artifact can arrive at any point from P1 onward and re-opens the
phases it touches. It runs through `sdlc_change_request` and `/sdlc_cr_analyze` →
`/sdlc_cr_design` → `/sdlc_cr_implement` → `/sdlc_cr_report`, against
`{{profile.gates.CR_change_request}}`.

A CR is the second legitimate ancestor in the traceability register — the first being a
`BR-*` — which is why the CR id is recorded in the ancestor position (TR-02).

---

## Standing behaviour in a development project

1. **Read the baselined specification before answering questions about behaviour.**
   Not the ticket, not the chat thread, not memory of a similar system.
2. **Anchor every specification claim** to a requirement, decision or elicitation record,
   or raise it as an open question.
3. **Never widen scope silently** (RS-06). The useful little addition is the one that
   breaks a fixed-price contract.
4. **Never edit a baselined document without a CR** (BL-02).
5. **Never bump a document version** unless told to.
6. **Deliverable language follows the directory**, not the language of the request.
7. **Update `{{profile.paths.traceability}}`** as artifacts are created, not afterwards.
8. **Attribute defects to the phase that injected them**, even when that is embarrassing.
9. **Report honestly**: a failing build is reported failing, with its output.

---

## Reporting format

Phase progress:
```
{Phase} · {category} — {done}/{expected} files · gate: {pass|fail} · {n} Critical
```

Completion of a phase:
```
═══════════════════════════════════════════
  {Phase} complete
  Files        : {done}/{expected}
  Gate         : {each exit assertion, pass/fail}
  Traceability : {orphans up}/{orphans down}/{untested}
  Open Items   : {n} ({kinds}) — {n} without an owner
  Metrics      : {the ones this phase produces}
═══════════════════════════════════════════
```

If any assertion fails, the phase is reported **incomplete**, with what is missing.
