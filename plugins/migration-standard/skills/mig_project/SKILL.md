---
name: mig_project
description: "Migration project spine — loads migration.profile.yaml, resolves {{profile.*}} tokens, and routes to the right phase skill. Load this FIRST for ANY task in a migration project. Contains the 8-phase model, phase gates, and the skill/agent routing table."
---

# Migration Project — Spine Skill

> **Load this skill first for every task in a migration project.**
> Every other `mig_*` skill assumes the profile is already resolved.

---

## Step 1 — Load the profile (mandatory)

Read `.claude/migration.profile.yaml` from the repository root.

- **Missing** → stop. Tell the user to run `/mig_init`.
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
| Reading/cataloguing the legacy system | `mig_legacy_analysis` |
| requirement.md, BRD, TSD, FRD | `mig_requirements` |
| Basic design, any category | `mig_basic_design` + the category skill below |
| Screen / UI design documents | `mig_screen_design` |
| Mockups — HTML, design canvas, Figma, image exports | `mig_mockup` (+ `mig_screen_design`) |
| Function / processing design | `mig_function_design` |
| API / interface design | `mig_api_design` |
| Table, column, DDL, data mapping | `mig_data_design` |
| Batch / scheduled job design | `mig_batch_design` |
| Detail design, BD↔code GAP | `mig_detail_design` |
| Creating, restructuring or auditing the target source layout — the codebase skeleton | `mig_codebase` |
| Writing code | `mig_implementation` (+ `mig_context_mapping` before starting) |
| Pipeline, environments, containers, IaC, secrets; coexistence, data migration, parallel run, cutover, rollback | `mig_infrastructure` |
| Which files a change touches | `mig_context_mapping` |
| UT / IT test case documents | `mig_test_design` + `mig_test_ut` / `mig_test_it` |
| Automating manual test cases | `mig_test_automation` |
| Reviewing test case documents | `mig_test_review` |
| Analysing failing test runs | `mig_defect_triage` |
| Test artifacts between rounds | `mig_test_artifact_lifecycle` |
| UAT bug investigation, fix, report | `mig_uat_bug` |
| One bug traced across every phase — injection, commit history, why it was not caught earlier | `mig_bug_trace` |
| A client-requested change to an approved spec | `mig_change_request` |
| Reviewing any deliverable | `mig_review_framework` |
| Feeding review findings back into a skill | `mig_review_framework` + `/mig_refine_skill` |
| Translating deliverables | `mig_translation` |
| Reading or writing a deliverable in Excel, Word or CSV; registering a client template; reading a legacy document | `mig_document_io` |

Category skills are bound to directories by `{{profile.paths.bd_categories}}` — a task
touching `02.screen-design/` loads whatever skill that entry names.

**Load `mig_document_io` alongside the category skill whenever the deliverable is not
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
| P0 | legacy inventory, `LEG-*` catalogue | `/mig_analyze_legacy` | `mig_legacy_analyst` |
| P1 | requirement.md → BRD → TSD → FRD | `/mig_generate_requirements` | `mig_requirements_writer` |
| P2 | design deliverables per category | `/mig_generate_basic_design` | `mig_bd_orchestrator` → `mig_bd_designer` |
| P3 | detail design + GAP report | `/mig_generate_detail_design` | `mig_dd_designer` |
| P2 | mockups, at the profile's fidelity | `/mig_generate_mockup` | `mig_mockup_designer` |
| P1→P4 | target codebase skeleton — layout, layers, cross-cutting plumbing, real build commands | `/mig_scaffold_codebase` | — |
| P4 | code | `/mig_implement_feature` | `mig_implementer` |
| P2/P4 | pipeline, environments, IaC; coexistence, data migration, cutover | `/mig_generate_infra` | `mig_infra_engineer` |
| P5 | UT design + unit tests | `/mig_generate_test ut` | `mig_tester` |
| P6 | IT design + integration tests | `/mig_generate_test it` | `mig_tester` |
| P5/P6 | automated scripts | `/mig_generate_testscript` | `mig_test_automator` |
| P5/P6 | failure triage | `/mig_triage_failures` | `mig_defect_triager` |
| P7 | bug investigation → fix → report | `/mig_uat_investigate` etc. | `mig_uat_engineer` |
| any | cross-phase bug traceability dossier | `/mig_trace_bug` | — |

### Phase gates

A phase is **not** complete until every assertion in `{{profile.gates.<phase>}}` holds and
`/mig_trace_check` reports no orphans for that phase's artifacts.

State the gate result explicitly when reporting a phase done. "Generated 46 files" is not
a completion report; "46/46 files, gate P2 passed, 0 Critical" is.

### Working across phases

Phases overlap in practice — one module can be in P4 while another is in P2. The gate is
evaluated **per module**, not per calendar phase, except for P0 and P1 which are
system-wide.

### Change requests are cross-cutting, not a phase

A client-requested spec change can arrive at any point from P2 onward, and it re-opens the
phases it touches instead of following them. It runs through `mig_change_request` and
`/mig_cr_analyze` → `/mig_cr_design` → `/mig_cr_implement` → `/mig_cr_report`, against
`{{profile.gates.CR_change_request}}`.

A CR is also the one legitimate source of behaviour with no legacy ancestor — NI-01's third
anchor, an explicit written client decision — which is why the CR id is recorded in the
register in the ancestor position (`mig_change_request` C11).

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
