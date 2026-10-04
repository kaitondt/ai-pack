---
name: mig-project
description: "Migration project spine — loads migration.profile.yaml, resolves {{profile.*}} tokens, and routes to the right phase skill. Load this FIRST for ANY task in a migration project. Contains the 8-phase model, phase gates, and the skill/agent routing table."
---

# Migration Project — Spine Skill

> **Load this skill first for every task in a migration project.**
> Every other `mig-*` skill assumes the profile is already resolved.

---

## Step 1 — Load the profile (mandatory)

Read `.claude/migration.profile.yaml` from the repository root.

- **Missing** → stop. Tell the user to run `/mig-init`.
- **Contains unreplaced placeholders** (`<...>`) in a field you need → stop and ask for
  that field. Never substitute a guess into a deliverable.
- **`legacy.readonly` is not `true`** → stop. The pack's safety model depends on it.

Hold the resolved values for the whole task. When a rule file or skill writes
`{{profile.paths.design_root}}`, substitute the profile value.

## Step 2 — Load the invariant rules

Always in force, regardless of phase:

| Rule file | Enforces |
|---|---|
| `rules/migration/no-invention.md` | nothing is invented; blocked features escalate |
| `rules/migration/traceability.md` | the LEG→REQ→design→code→test chain |
| `rules/migration/legacy-readonly.md` | the source system is never modified |
| `rules/migration/id-naming.md` | deterministic IDs |
| `rules/migration/document-standards.md` | deliverable skeleton and scope discipline |

## Step 3 — Route to the phase skill

| The task is about | Load |
|---|---|
| Reading/cataloguing the legacy system | `mig-legacy-analysis` |
| requirement.md, BRD, TSD, FRD | `mig-requirements` |
| Basic design, any category | `mig-basic-design` + the category skill below |
| Screen / UI design documents | `mig-screen-design` |
| Mockups — HTML, design canvas, Figma, image exports | `mig-mockup` (+ `mig-screen-design`) |
| Function / processing design | `mig-function-design` |
| API / interface design | `mig-api-design` |
| Table, column, DDL, data mapping | `mig-data-design` |
| Batch / scheduled job design | `mig-batch-design` |
| Detail design, BD↔code GAP | `mig-detail-design` |
| Creating, restructuring or auditing the target source layout — the codebase skeleton | `mig-codebase` |
| Writing code | `mig-implementation` (+ `mig-context-mapping` before starting) |
| Pipeline, environments, containers, IaC, secrets; coexistence, data migration, parallel run, cutover, rollback | `mig-infrastructure` |
| Which files a change touches | `mig-context-mapping` |
| UT / IT test case documents | `mig-test-design` + `mig-test-ut` / `mig-test-it` |
| Automating manual test cases | `mig-test-automation` |
| Reviewing test case documents | `mig-test-review` |
| Analysing failing test runs | `mig-defect-triage` |
| Test artifacts between rounds | `mig-test-artifact-lifecycle` |
| UAT bug investigation, fix, report | `mig-uat-bug` |
| One bug traced across every phase — injection, commit history, why it was not caught earlier | `mig-bug-trace` |
| A client-requested change to an approved spec | `mig-change-request` |
| Reviewing any deliverable | `mig-review-framework` |
| Feeding review findings back into a skill | `mig-review-framework` + `/mig-refine-skill` |
| Translating deliverables | `mig-translation` |
| Reading or writing a deliverable in Excel, Word or CSV; registering a client template; reading a legacy document | `mig-document-io` |

Category skills are bound to directories by `{{profile.paths.bd_categories}}` — a task
touching `02.screen-design/` loads whatever skill that entry names.

**Load `mig-document-io` alongside the category skill whenever the deliverable is not
Markdown, or the category has a registered template.** The pack ships no templates: the
client's own form is registered in `{{profile.templates.registry}}` and outranks the category
skill's section list (DS-10) — though it never suspends NI-01. The same skill governs legacy
documents, which are read-only inputs and are evidence of **intent**, never of behaviour
(DIO-08).

---

## The phase model

```
P0 Legacy Analysis ─ P1 Requirements ─ P2 Basic Design ─ P3 Detail Design
                                                              │
        P7 UAT ─ P6 Integration Test ─ P5 Unit Test ─ P4 Implementation
```

| Phase | Produces | Command | Agent |
|---|---|---|---|
| P0 | legacy inventory, `LEG-*` catalogue | `/mig-analyze-legacy` | `mig-legacy-analyst` |
| P1 | requirement.md → BRD → TSD → FRD | `/mig-generate-requirements` | `mig-requirements-writer` |
| P2 | design deliverables per category | `/mig-generate-basic-design` | `mig-bd-orchestrator` → `mig-bd-designer` |
| P3 | detail design + GAP report | `/mig-generate-detail-design` | `mig-dd-designer` |
| P2 | mockups, at the profile's fidelity | `/mig-generate-mockup` | `mig-mockup-designer` |
| P1→P4 | target codebase skeleton — layout, layers, cross-cutting plumbing, real build commands | `/mig-scaffold-codebase` | — |
| P4 | code | `/mig-implement-feature` | `mig-implementer` |
| P2/P4 | pipeline, environments, IaC; coexistence, data migration, cutover | `/mig-generate-infra` | `mig-infra-engineer` |
| P5 | UT design + unit tests | `/mig-generate-test ut` | `mig-tester` |
| P6 | IT design + integration tests | `/mig-generate-test it` | `mig-tester` |
| P5/P6 | automated scripts | `/mig-generate-testscript` | `mig-test-automator` |
| P5/P6 | failure triage | `/mig-triage-failures` | `mig-defect-triager` |
| P7 | bug investigation → fix → report | `/mig-uat-investigate` etc. | `mig-uat-engineer` |
| any | cross-phase bug traceability dossier | `/mig-trace-bug` | — |

### Phase gates

A phase is **not** complete until every assertion in `{{profile.gates.<phase>}}` holds and
`/mig-trace-check` reports no orphans for that phase's artifacts.

State the gate result explicitly when reporting a phase done. "Generated 46 files" is not
a completion report; "46/46 files, gate P2 passed, 0 Critical" is.

### Working across phases

Phases overlap in practice — one module can be in P4 while another is in P2. The gate is
evaluated **per module**, not per calendar phase, except for P0 and P1 which are
system-wide.

### Change requests are cross-cutting, not a phase

A client-requested spec change can arrive at any point from P2 onward, and it re-opens the
phases it touches instead of following them. It runs through `mig-change-request` and
`/mig-cr-analyze` → `/mig-cr-design` → `/mig-cr-implement` → `/mig-cr-report`, against
`{{profile.gates.CR_change_request}}`.

A CR is also the one legitimate source of behaviour with no legacy ancestor — NI-01's third
anchor, an explicit written client decision — which is why the CR id is recorded in the
register in the ancestor position (`mig-change-request` C11).

---

## Standing behaviour in a migration project

1. **Read the legacy source before answering questions about behaviour.** Memory of a
   similar system is not evidence.
2. **Anchor every behavioural claim** to a legacy location (`file:line`) or mark it
   SPEC-GAP.
3. **Never modify** anything under `{{profile.legacy.root}}` or matching
   `{{profile.constraints.readonly_globs}}`.
4. **Never enable a blocked feature** on your own judgement — stop and ask (NI-04).
   This includes rendering one as working in a mockup (MU-05).
5. **Never bump a document version** unless told to.
6. **Deliverable language follows the directory**, not the language of the request.
7. **Update `{{profile.paths.traceability}}`** as artifacts are created, not afterwards.
8. **Report honestly**: a failing build is reported as failing, with its output.

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
  Files      : {done}/{expected}
  Gate       : {each assertion, pass/fail}
  Traceability: {orphans up}/{orphans down}
  Open Items : {n} ({kinds})
═══════════════════════════════════════════
```

If any assertion fails, the phase is reported **incomplete**, with what is missing.
