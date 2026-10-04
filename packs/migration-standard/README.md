# Migration Skill Pack (MSP) — Standard Edition

A **project-agnostic Claude Code skill pack for legacy-system migration projects.**
Covers the full lifecycle: Legacy Analysis → Requirements → Basic Design → Detail Design →
Coding → Unit Test → Integration Test → UAT.

Derived by generalising a production pack built for a single warehouse-management
migration (VB.NET Desktop → .NET 9 + React). Everything project-specific was pulled
out into **one profile file**; everything methodological stayed in the pack.

---

## The core idea

```
┌──────────────────────────────────────────────────────────────┐
│  migration.profile.yaml     ← the ONLY file you edit per project │
│  (stack, ID patterns, paths, languages, phase gates, counts) │
└───────────────────────────┬──────────────────────────────────┘
                            │ resolved by  skill: mig-project
                            ▼
┌──────────────────────────────────────────────────────────────┐
│  rules/  — invariant standards (traceability, no-invention)   │
│  skills/ — phase knowledge, loaded into context on demand     │
│  commands/ — entry-point workflows the user types             │
│  agents/ — delegated workers with narrow tool sets            │
└──────────────────────────────────────────────────────────────┘
```

A skill never hardcodes `KK0030PG`, `src/wms/docs`, or `.NET 9`. It writes
`{{profile.ids.module_pattern}}`, `{{profile.paths.design_root}}`,
`{{profile.target.stack.backend}}` and resolves them at load time from the profile.

---

## What is invariant across every migration project

These are the load-bearing rules. They are the reason this is a *migration* pack
and not a generic SDLC pack.

| # | Rule | Where |
|---|------|-------|
| 1 | **No invention** — every documented behaviour traces to legacy source | `rules/migration/no-invention.md` |
| 2 | **Traceability chain** — LEG → REQ → BD → DD → CODE → TEST is unbroken and machine-checkable | `rules/migration/traceability.md` |
| 3 | **Legacy is read-only** — never modify the system being migrated from | `rules/migration/legacy-readonly.md` |
| 4 | **Blocked features stop the run** — disabled-but-present legacy features are escalated, never silently enabled | `rules/migration/no-invention.md` §BLOCKED |
| 5 | **Deterministic IDs** — `{MODULE}-{TYPE}-{NNN}` everywhere, never translated | `rules/migration/id-naming.md` |
| 6 | **Document standards** — fixed section skeleton, revision history, no auto version bump | `rules/migration/document-standards.md` |
| 7 | **Phase gates** — a phase cannot start until its predecessor's gate passes | `skills/mig-project` §Phase Model |
| 8 | **The pack ships no deliverable templates** — the client's own form is registered and outranks the pack's skeleton, and it never suspends NI-01 | `rules/migration/document-standards.md` DS-10, `skills/mig-document-io` |
| 9 | **A legacy document is evidence of intent, never of behaviour** — the legacy code is the oracle | `skills/mig-document-io` DIO-08 |
| 10 | **The legacy screen is the UI oracle**, to the degree `mockup.fidelity` states — reproduce, do not improve, in pixels as much as in rules | `skills/mig-mockup` MU-02, MU-03 |
| 11 | **No default platform, and legacy infrastructure is read-only** — nothing deploys to the legacy production environment | `skills/mig-infrastructure` IN-01, IN-02 |

## What is variable (lives in the profile)

Tech stack · repository layout · document language(s) · **the client's own deliverable
forms and their formats** · ID patterns · deliverable categories and counts · **mockup form
and fidelity** · review checklist selection · build commands · **SCM, CI, hosting, IaC and
who owns them** · **coexistence strategy, data migration, parallel run and rollback** ·
legacy source kind (VB.NET / COBOL / Delphi / PHP / AS400 / Java-EE …) · UAT report
template.

Change-request handling is configured the same way: `paths.change_requests`, the
`change_request` block (id format, option count, the two gates, the document cascade,
the classification set) and the `gates.CR_change_request` assertions.

---

## What the pack deliberately does not ship

**Deliverable templates.** Every organisation has its own forms, in its own format — Excel
through most of the Japanese SI market — and on migration work they are usually contractual.
A template invented here would be rejected at the first review, *after* a whole category had
been generated into it.

So the form is a project input. `/mig-init` asks for it and `/mig-template-register` takes it
in — opening the file, deriving the field map from its own placeholders, reporting where it
disagrees with the category skill, checking it has somewhere to record the `LEG-*` anchor,
and running a round-trip fidelity check on the first file so a writer that destroys merged
ranges is caught before forty documents exist. `mig-document-io` owns the mechanics for
Markdown, Excel, Word and CSV.

The same skill draws a line this pack needs and a greenfield pack does not: **legacy
documents are read-only inputs, and they are evidence of intent, never of behaviour**
(DIO-08). Old specifications are usually years out of date; the legacy code is the oracle.

Two more things the pack refuses to assume:

- **Mockups** take whichever form the project uses — HTML prototype, design canvas, Figma or
  image exports — and are held to the legacy screen at the fidelity `mockup.fidelity`
  declares. Under `as-is`, a reordered field is a defect, not an improvement: NI-02 applies to
  pixels, and the mockup is where modernisation otherwise arrives unpriced (`mig-mockup`).
- **Infrastructure** has no default platform, and the legacy system's infrastructure is as
  read-only as its source. Beyond the usual pipeline and IaC, this is where a migration keeps
  what a greenfield project has no equivalent of: coexistence and which system owns the data,
  data migration judged on reconciliation rather than on completing, the parallel run, and a
  rollback whose target is a system that never stopped (`mig-infrastructure`).

---

## Layout

```
migration-standard/
├── README.md                      ← this file
├── ADOPTION.md                    ← 30-minute onboarding for a new project
├── COMMAND-FLOW.md                ← how the commands chain, and the refinement loop
├── profile/
│   ├── migration.profile.yaml     ← template to copy
│   ├── PROFILE-SCHEMA.md          ← field-by-field spec
│   ├── PROFILE-RECIPES.md         ← overlays for 7 migration shapes
│   └── examples/
│       ├── wms.profile.yaml       ← the original project, expressed as a profile
│       └── cobol-to-java.profile.yaml
└── .claude/
    ├── CLAUDE.md                  ← project-instruction template
    ├── settings.json
    ├── hooks/                     ← 3 guard hooks
    ├── rules/
    │   ├── common/                ← 6 stack-neutral rule files
    │   └── migration/             ← 5 migration-invariant rule files
    ├── skills/                    ← 28 skills
    ├── commands/                  ← 31 slash commands
    └── agents/                    ← 14 agents
```

---

## Model policy

<!-- model-policy:claude -->
`execution.model_profile` sets the model **and the reasoning effort** of every `mig-*` agent by
**tier**. `/mig-init` writes the result into the agent frontmatter (`model:` and `effort:`).

| `model_profile` | heavy tier | standard tier | Use when |
|---|---|---|---|
| `quality` | opus · `xhigh` | opus · `high` | large or poorly documented legacy systems, fixed-price contracts |
| `balanced` (default) | opus · `high` | sonnet · `medium` | most projects |
| `budget` | sonnet · `high` | sonnet · `medium` | a small, well-understood legacy system |

| Tier | Agents |
|---|---|
| heavy | `mig-legacy-analyst`, `mig-requirements-writer`, `mig-bd-orchestrator`, `mig-bd-designer`, `mig-dd-designer`, `mig-reviewer`, `mig-defect-triager`, `mig-cr-engineer` |
| standard | `mig-implementer`, `mig-tester`, `mig-test-automator`, `mig-infra-engineer`, `mig-mockup-designer`, `mig-uat-engineer` |

The analysis, design, review and triage roles produce work whose failure modes are
**silent**: a behaviour invented instead of anchored, a business rule whose branch order drifted,
a design category dropped at the end of a long generation run. None of that fails loudly — it
fails at client review, weeks later, after downstream documents were built on top of it.
Cheaper models and shallower reasoning degrade exactly there first, and the degradation is
invisible in the run log. Those roles stay on Opus in every profile but `budget`, and never drop
below `high` effort.

The production roles work from a document that has already been reviewed and approved: code
from the detail design, test cases from the specification, a pipeline from the infrastructure
design. Build, tests, the parallel run and the `mig-reviewer` check what they produce, so they
run on Sonnet at `medium` under `balanced`.

`execution.agent_model_overrides` and `execution.agent_effort_overrides` change one agent, in
either direction. Do not lower the heavy tier to save cost — the cost of a parity defect found in UAT is larger by an order of magnitude.

Commands run in your session, not in an agent. `/mig-verify-build` runs on Haiku — it runs the build and reports the output. `/mig-profile-check`, `/mig-trace-check` and `/mig-template-register` run on Sonnet at `medium`
effort. Every other command runs on the model and effort of your session —
`execution.intended_effort` records the level the team agreed; set it with `/effort`. To change a
command's model or effort, copy it into the project and edit its frontmatter.
<!-- /model-policy:claude -->

---

## Phase model

| Phase | Name | Command | Deliverable | Gate to exit |
|---|---|---|---|---|
| **P0** | Legacy Analysis | `/mig-analyze-legacy` | `legacy-inventory.md`, `LEG-*` catalogue | 100% of in-scope legacy artifacts catalogued |
| **P1** | Requirements | `/mig-generate-requirements` | `requirement.md` → BRD → TSD → FRD | every `REQ-*` cites a `LEG-*` |
| **P2** | Basic Design | `/mig-generate-basic-design` | screen / function / data / API / batch / report design | `/mig-review-design` clean; cross-doc checks pass |
| **P2** | Mockup | `/mig-generate-mockup` | prototypes / artboards / Figma check, at the profile's fidelity | X-09 and X-10 clean |
| **P3** | Detail Design | `/mig-generate-detail-design` | DD per module + BD↔code GAP report | zero unresolved GAP items |
| **P1→P4** | Target codebase skeleton | `/mig-scaffold-codebase` | layout, layer projects, cross-cutting plumbing, real build commands | builds clean; legacy untouched |
| **P4** | Implementation | `/mig-implement-feature` | code across all layers | `/mig-verify-build` + `/mig-review-commit` pass |
| **P2/P4** | Infrastructure | `/mig-generate-infra` | pipeline, environments, IaC; coexistence, data migration, cutover, rollback | X-11 clean; nothing deploys to legacy prod |
| **P5** | Unit Test | `/mig-generate-test ut` | UT design + automated tests | UT design ↔ FC coverage 100% |
| **P6** | Integration Test | `/mig-generate-test it` | IT design + results | every screen flow covered |
| **P7** | UAT | `/mig-uat-investigate` → `_fix` → `_report` | bug reports, closure log | all bugs closed or accepted |

Change requests are **cross-cutting, not a phase**: a client spec change can arrive any
time from P2 onward and re-opens the phases it touches. `mig-change-request` and
`/mig-cr-analyze` → `/mig-cr-design` → `/mig-cr-implement` → `/mig-cr-report` run it behind
two approvals — the option, then the document diff — and record the CR id as the
traceability ancestor for behaviour the legacy never had.

P5–P7 have their own skill family: `mig-test-design` (viewpoints and writing rules),
`mig-test-ut` / `mig-test-it` (the checkpoint pipelines with human pauses),
`mig-test-automation`, `mig-test-review`, `mig-defect-triage`, `mig-test-artifact-lifecycle`.

Cross-cutting at any phase: `/mig-trace-check`, `/mig-review-design`,
`/mig-translate`, `/mig-context-map`, `/mig-verify-build`, `/mig-template-register`,
`/mig-refine-skill`.

Any bug, from any phase, can be traced end to end with `/mig-trace-bug` (`mig-bug-trace`):
the chain from legacy to test with the first broken link marked, the introducing commit and
everything that happened to that code since, and — when it was found later than it should
have been — the evidenced reason each earlier check missed it.

**How the commands chain, and the execute → review → refine → re-execute loop they
are built for: [COMMAND-FLOW.md](COMMAND-FLOW.md).**

---

## Quick start

```bash
cp -r migration-standard/.claude  <your-project>/.claude
cp migration-standard/profile/migration.profile.yaml  <your-project>/.claude/migration.profile.yaml
# then, inside the project:
/mig-init
/mig-template-register      # take the client's own deliverable forms in
```

`/mig-init` interviews you for the profile fields it cannot infer, writes the profile, takes
the deliverable templates in, generates `CLAUDE.md`, and prints the phase plan.

Needs Python 3 for the guard hooks — without it they fail silently and **the legacy tree is
writable** — plus `openpyxl` / `python-docx` if your deliverables or legacy inputs are Excel
or Word. [ADOPTION.md](ADOPTION.md) installs all of it from nothing, and its troubleshooting
section starts with that failure.

Starting points per project shape: [profile/PROFILE-RECIPES.md](profile/PROFILE-RECIPES.md).
