---
name: sdlc-project
description: "Development project spine — loads sdlc.profile.yaml, resolves {{profile.*}} tokens, and routes to the right phase skill. Load this FIRST for ANY task in a development project. Contains the 10-phase model, the V-model binding, phase gates, and the skill/agent routing table."
---

# Development Project — Spine Skill

> **Load this skill first for every task in this project.**
> Every other `sdlc-*` skill assumes the profile is already resolved.

---

## Step 1 — Load the profile (mandatory)

Read `.claude/sdlc.profile.yaml` from the repository root.

- **Missing** → stop. Tell the user to run `/sdlc-init`.
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

**Stack rules load with the code they govern.** `rules/java/`, `rules/typescript/`,
`rules/react/` and `rules/sql/` carry `paths:` front matter, so they apply when a matching
file is read or written. Before writing or reviewing code, make sure the ones for the files
in play are loaded, together with any client coding-standard digest listed in
`{{profile.system.coding_standards}}` — which outranks them. Cite their rule ids (`JV-*`,
`TS-*`, `RX-*`, `SQ-*`) in findings.

## Step 3 — Route to the phase skill

| The task is about | Load |
|---|---|
| Scope, stakeholders, glossary, decisions, risks | `sdlc-discovery` |
| SRS, functional and non-functional requirements | `sdlc-requirements` |
| Basic design, any category | `sdlc-basic-design` + the category skill below |
| Architecture and quality attributes | `sdlc-nfr-design` |
| Screen / UI design documents | `sdlc-screen-design` |
| Mockups — HTML, design canvas, Figma, image exports | `sdlc-mockup` (+ `sdlc-screen-design`) |
| Function / processing design | `sdlc-function-design` |
| Table, column, DDL, data lifecycle | `sdlc-data-design` |
| API / interface design | `sdlc-api-design` |
| Batch / scheduled job design | `sdlc-batch-design` |
| Detail design, DD↔code drift | `sdlc-detail-design` |
| Creating, restructuring or auditing the source layout — the codebase skeleton | `sdlc-codebase` |
| Writing code | `sdlc-implementation` (+ `sdlc-context-mapping` before starting) |
| Repository, CI/CD, environments, containers, IaC, secrets, monitoring | `sdlc-infrastructure` |
| Which files a change touches | `sdlc-context-mapping` |
| Test case documents, any level | `sdlc-test-design` + `sdlc-test-ut` / `_it` / `_st` / `_uat` |
| Automating manual test cases | `sdlc-test-automation` |
| Reviewing test case documents | `sdlc-test-review` |
| Defect triage, classification, ageing | `sdlc-defect-management` |
| One defect traced across every phase — evidenced injection, commit history, why it was not caught earlier | `sdlc-bug-trace` |
| Test artifacts between rounds | `sdlc-test-artifact-lifecycle` |
| Release readiness, cutover, rollback | `sdlc-release` |
| Incidents after go-live | `sdlc-maintenance` |
| A change to a baselined artifact | `sdlc-change-request` |
| Reviewing any deliverable | `sdlc-review-framework` |
| Metrics, gate reports, containment | `sdlc-quality-metrics` |
| Feeding review findings back into a skill | `sdlc-review-framework` + `/sdlc-refine-skill` |
| Translating deliverables | `sdlc-translation` |
| Reading or writing a deliverable in Excel, Word or CSV; registering a client template | `sdlc-document-io` |

Category skills are bound to directories by `{{profile.paths.bd_categories}}` — a task
touching `03.screen-design/` loads whatever skill that entry names.

**Load `sdlc-document-io` alongside the category skill whenever the deliverable is not
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
| P0 | scope, stakeholders, glossary, `BR-*`, decision log, risk register | `/sdlc-discover` | `sdlc-analyst` |
| P1 | SRS: `REQ-*`, `NFR-*`, use cases, acceptance criteria | `/sdlc-generate-requirements` | `sdlc-analyst` |
| P2 | design deliverables per category | `/sdlc-generate-basic-design` | `sdlc-bd-orchestrator` → `sdlc-bd-designer` |
| P3 | detail design + drift report | `/sdlc-generate-detail-design` | `sdlc-dd-designer` |
| P2 | mockups, in the project's form | `/sdlc-generate-mockup` | `sdlc-mockup-designer` |
| P2→P4 | codebase skeleton — layout, layers, cross-cutting plumbing, real build commands | `/sdlc-scaffold-codebase` | — |
| P4 | code | `/sdlc-implement-feature` | `sdlc-implementer` |
| P2/P4 | pipeline, environments, IaC, monitors | `/sdlc-generate-infra` | `sdlc-infra-engineer` |
| P5 | UT design + unit tests | `/sdlc-generate-test ut` | `sdlc-tester` |
| P6 | IT design + results | `/sdlc-generate-test it` | `sdlc-tester` |
| P7 | ST design + NFR measurements | `/sdlc-generate-test st` | `sdlc-tester` |
| P8 | UAT plan, support, acceptance record | `/sdlc-uat-prepare` etc. | `sdlc-uat-coordinator` |
| P9 | incident records, fixes, RCA, KB | `/sdlc-maintain-intake` etc. | `sdlc-maintenance-engineer` |
| any | automated scripts | `/sdlc-generate-testscript` | `sdlc-test-automator` |
| any | defect triage | `/sdlc-triage-defects` | `sdlc-defect-triager` |
| any | cross-phase bug traceability dossier | `/sdlc-trace-bug` | — |

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
holds and `/sdlc-trace-check` reports no orphans for that phase's artifacts.
`/sdlc-phase-gate` runs the check, records the result, and baselines the documents the
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
phases it touches. It runs through `sdlc-change-request` and `/sdlc-cr-analyze` →
`/sdlc-cr-design` → `/sdlc-cr-implement` → `/sdlc-cr-report`, against
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
