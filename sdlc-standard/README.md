# SDLC Skill Pack (SSP) — Standard Edition

A **project-agnostic Claude Code skill pack for ordinary software development projects.**
Covers the full lifecycle: Inception → Requirements Analysis → Basic Design → Detail
Design → Code → Unit Test → Integration Test → System Test → UAT → Maintenance.

Built as the sibling of [`migration-standard`](../migration-standard/README.md), which
covers legacy-system migration. Same architecture — one profile file, invariant rules,
phase skills, entry-point commands, delegated agents — different invariants, because a
development project has a different problem.

---

## The core idea

```
┌──────────────────────────────────────────────────────────────────┐
│  sdlc.profile.yaml     ← the ONLY file you edit per project      │
│  (stack, ids, paths, gates, quality targets, SLAs, test levels)  │
└───────────────────────────┬──────────────────────────────────────┘
                            │ resolved by  skill: sdlc-project
                            ▼
┌──────────────────────────────────────────────────────────────────┐
│  rules/  — invariant standards (sourcing, traceability, baseline) │
│  skills/ — phase knowledge, loaded into context on demand         │
│  commands/ — entry-point workflows the user types                 │
│  agents/ — delegated workers with narrow tool sets                │
└──────────────────────────────────────────────────────────────────┘
```

A skill never hardcodes `SL0030PG`, `docs/02.basic-design`, or `.NET 9`. It writes
`{{profile.ids.module_pattern}}`, `{{profile.paths.design_root}}`,
`{{profile.system.stack.backend}}` and resolves them at load time from the profile.

---

## What is different from the migration pack

A migration project has an oracle: the old system. Every question about behaviour has an
answer sitting in legacy source, and the pack's job is to stop anyone inventing around it.

**A development project has no oracle.** Its only source of truth is what stakeholders
decided and someone wrote down. That single difference produces every substantive change:

| Migration invariant | Development counterpart |
|---|---|
| No invention — anchor to legacy source | **Requirement sourcing** — anchor to a requirement, a recorded decision, an elicitation record or an external obligation; anything else is an open question or a labelled assumption |
| Legacy is read-only | **Baselines are change-controlled** — once approved, a document changes only through a CR; production changes only through a release |
| Blocked features stop the run | **Undecided requirements stop the design** |
| Verbatim legacy messages | **Approved catalogue text**, per language |
| BD ↔ code GAP report | **DD ↔ code drift report**, decided against the requirement |
| — | **The V-model binding** — every specification phase is verified by a named test phase, and a specification that cannot be tested is not finished |
| — | **Non-functional requirements** as a first-class design category with measurements |
| — | **Quality metrics** — review density, defect density, phase containment, escapes — because without a legacy to compare against, process evidence is the argument that the system is ready |
| — | **System test and UAT as distinct phases**, with entry criteria, evidence and an acceptance record |
| — | **Maintenance** — incident intake, SLA, RCA, regression obligation, knowledge base |

---

## The load-bearing rules

| # | Rule | Where |
|---|---|---|
| 1 | **Nothing is specified without a source** — requirement, decision, elicitation record, or external obligation | `rules/sdlc/requirement-sourcing.md` |
| 2 | **Assumptions are objects** — `ASM-*` with an owner, a confirm-by date and an impact-if-wrong | `requirement-sourcing.md` RS-02 |
| 3 | **Undecided requirements stop the design** — do everything else, then ask | `requirement-sourcing.md` RS-04 |
| 4 | **Nothing enters scope without a requirement** — the useful little addition goes to the CR backlog | `requirement-sourcing.md` RS-06 |
| 5 | **A baselined document changes only through a CR**, and design changes before code | `rules/sdlc/baseline-change-control.md` |
| 6 | **Traceability chain** — BR → REQ → BD → DD → CODE → UT/IT/ST/UAT — unbroken and machine-checkable | `rules/sdlc/traceability.md` |
| 7 | **The V-model binding** — each specification has a verifying level; untestable means unfinished | `traceability.md` TR-03 |
| 8 | **Deterministic IDs** — `{MODULE}-{TYPE}-{NNN}`, never translated, never renumbered | `rules/sdlc/id-naming.md` |
| 9 | **Document standards** — fixed skeleton, review record, no automatic version bump | `rules/sdlc/document-standards.md` |
| 10 | **Metrics are evidence, never tuned** — a defect is attributed to the phase that injected it | `rules/sdlc/quality-metrics.md` |
| 11 | **Phase gates** — a phase cannot start until its predecessor's exit criteria hold | `skills/sdlc-project` §Phase model |
| 12 | **The pack ships no deliverable templates** — the client's own form is registered and outranks the pack's skeleton; nothing is invented into a form nobody agreed | `rules/sdlc/document-standards.md` DS-11, `skills/sdlc-document-io` |
| 13 | **A mockup is never the specification** — the screen design is, and X-11 keeps them from diverging | `skills/sdlc-mockup` MU-01 |
| 14 | **No default platform** — SCM, CI, hosting and IaC are read from the profile, and infrastructure another team owns is proposed, never committed | `skills/sdlc-infrastructure` IN-01 |

## What is variable (lives in the profile)

Tech stack · repository layout · delivery model and contract type · stakeholders ·
document language(s) · **the client's own deliverable templates and their formats** ·
ID patterns · deliverable categories · **mockup form** · review checklist selection ·
build commands · **SCM, CI, hosting, IaC and who owns them** · environments · test levels
and viewpoints · quality targets · defect severity model · maintenance SLAs ·
change-request cascade.

---

## What the pack deliberately does not ship

**Deliverable templates.** Every organisation has its own forms, in its own format — Excel
through most of the Japanese SI market — and they are frequently contractual. A template
invented here would be rejected at the first review, and rejected *after* a whole category
had been generated into it.

So the form is a project input. `/sdlc-init` asks for it, `/sdlc-template-register` takes it
in — opening the file, deriving the field map from its own placeholders, reporting where it
disagrees with the category skill, and running a round-trip fidelity check on the first file
so that a writer which destroys merged ranges is found before forty documents exist.
`sdlc-document-io` owns the mechanics for Markdown, Excel, Word and CSV, and the rule that a
registered template **outranks** the pack's own skeleton (DS-11).

Where no template exists, `templates.on_missing` decides — and a run that used the pack's
skeleton says so, per category, in its plan. A category quietly generated into the wrong form
is the most expensive silent failure in document-heavy delivery.

The same principle covers the other two things a project cannot be assumed into:

- **Mockups** take whichever form the project uses — HTML prototype, design canvas, Figma, or
  image exports — and the pack reads, creates and edits each. What it never does is let a
  mockup become the specification: X-11 cross-checks it against the screen design, per screen
  (`sdlc-mockup`).
- **Infrastructure** has no default platform. GitHub, GitLab, Azure Repos, Bitbucket and
  Jenkins are read from the profile, along with hosting, IaC and — crucially — **who owns
  them**. Where a platform team owns the pipeline, the pack produces proposals, not commits
  (`sdlc-infrastructure`).

---

## Layout

```
sdlc-standard/
├── README.md                      ← this file
├── ADOPTION.md                    ← 30-minute onboarding for a new project
├── COMMAND-FLOW.md                ← how the commands chain, and the refinement loop
├── profile/
│   ├── sdlc.profile.yaml          ← template to copy
│   ├── PROFILE-SCHEMA.md          ← field-by-field spec
│   ├── PROFILE-RECIPES.md         ← overlays for 7 common project shapes
│   └── examples/
│       ├── saas-webapp.profile.yaml        ← iterative, internal product
│       └── enterprise-waterfall.profile.yaml ← offshore, fixed-price, two languages
└── .claude/
    ├── CLAUDE.md                  ← project-instruction template
    ├── settings.json
    ├── hooks/                     ← 3 guard hooks
    ├── rules/
    │   ├── common/                ← 6 stack-neutral rule files
    │   └── sdlc/                  ← 6 lifecycle-invariant rule files
    ├── skills/                    ← 33 skills
    ├── commands/                  ← 37 slash commands
    └── agents/                    ← 14 agents
```

---

## Phase model

| Phase | Name | Command | Deliverable | Verified by |
|---|---|---|---|---|
| **P0** | Inception & discovery | `/sdlc-discover` | scope, stakeholders, glossary, `BR-*`, decision/assumption/risk logs | P8 |
| **P1** | Requirements analysis | `/sdlc-generate-requirements` | SRS: `REQ-*`, `NFR-*`, use cases, acceptance criteria | P7, P8 |
| **P2** | Basic design | `/sdlc-generate-basic-design` | architecture, NFR, screen, function, data, interface, report, batch | P6 |
| **P2** | Mockups | `/sdlc-generate-mockup` | prototypes / artboards / Figma check, in the project's form | P6, P8 |
| **P3** | Detail design | `/sdlc-generate-detail-design` | DD per module + drift report | P5 |
| **P2→P4** | Codebase skeleton | `/sdlc-scaffold-codebase` | layout, layer projects, cross-cutting plumbing, real build commands | — |
| **P4** | Implementation | `/sdlc-implement-feature` | code across all layers | P5 |
| **P2/P4** | Infrastructure | `/sdlc-generate-infra` | pipeline, environments, IaC, NFR monitors | P7 |
| **P5** | Unit test | `/sdlc-generate-test ut` | UT cases + automated tests | — |
| **P6** | Integration test | `/sdlc-generate-test it` | IT cases, interface failure set | — |
| **P7** | System test | `/sdlc-generate-test st` | business scenarios + NFR measurements | — |
| **P8** | UAT | `/sdlc-uat-prepare` → `_triage` → `_report` | UAT plan, acceptance record | — |
| **P9** | Maintenance | `/sdlc-maintain-intake` → `_fix` → `_report` | incident records, RCA, knowledge base | — |

Between P8 and P9: `/sdlc-release-check` — go/no-go, cutover, rehearsed rollback.

Change requests are **cross-cutting, not a phase**: a change to a baselined artifact can
arrive any time from P1 onward and re-opens the phases it touches. `sdlc-change-request` and
`/sdlc-cr-analyze` → `/sdlc-cr-design` → `/sdlc-cr-implement` → `/sdlc-cr-report` run it
behind two approvals — the option, then the document diff.

Cross-cutting at any phase: `/sdlc-phase-gate`, `/sdlc-trace-check`, `/sdlc-quality-report`,
`/sdlc-review-design`, `/sdlc-review-commit`, `/sdlc-verify-build`, `/sdlc-context-map`,
`/sdlc-translate`, `/sdlc-template-register`, `/sdlc-refine-skill`.

Any defect, from any phase, can be traced end to end with `/sdlc-trace-bug`
(`sdlc-bug-trace`): the chain from business requirement to test with the first broken link
marked against the baselines, the introducing commit and everything that happened to that
code since, and — when it was found later than the V-model says it should have been — the
evidenced reason each earlier check missed it. It is what turns the injection phase from a
judgement into a measurement.

**How the commands chain, and the execute → review → refine → re-execute loop they are
built for: [COMMAND-FLOW.md](COMMAND-FLOW.md).**

---

## The V-model, which is the spine of the pack

```
P0 Business need ─────────────────────────────────── P8 Acceptance test
   P1 Requirements ─────────────────────────────  P7 System test
      P2 Basic design ───────────────────────  P6 Integration test
         P3 Detail design ────────────────  P5 Unit test
            P4 Implementation ─────────
```

Two consequences, both enforced at the gates:

1. **A specification that cannot be tested is not finished.** If no case can be written
   against a requirement at its verifying level, that phase fails its own gate — however
   well the requirement reads.
2. **A test whose basis is not baselined is provisional.** Cases are drafted early and
   finalised against the baseline; when the baseline changes through a CR, they are
   re-checked.

This is also why the pack has a level model rather than a test-case count: an ST suite that
re-tests field validation has paid for coverage it already had, and still has no case for
the month-end process.

---

## Model policy

Every `sdlc-*` agent ships with `model: opus`, set from `execution.agent_model` in the
profile.

This is deliberate, not a default. The agent roles all produce work whose failure modes are
**silent**: an untestable requirement, a design that quietly drops a rule, a test case that
asserts what the code does instead of what the spec says, a category dropped at the end of
a long generation run. None of that fails loudly — it fails at UAT, weeks later, after
downstream documents were built on top of it. Cheaper models degrade exactly there first,
and the degradation is invisible in the run log.

Reasoning effort is a **session-level** setting in Claude Code, not agent frontmatter.
`execution.intended_effort` records the level the project runs at so the team is consistent;
it does not enforce it. Set it in your own session.

Downgrade a specific role via `execution.agent_model_overrides` when it is genuinely
mechanical. Do not downgrade the analysis, design or review roles to save cost — the cost of
a requirements defect found in UAT is larger by an order of magnitude.

---

## Quick start

```bash
cp -r sdlc-standard/.claude              <your-project>/.claude
cp sdlc-standard/profile/sdlc.profile.yaml  <your-project>/.claude/sdlc.profile.yaml
# then, inside the project:
/sdlc-init
/sdlc-template-register      # take the client's own deliverable forms in
```

`/sdlc-init` inspects the repository, interviews you for what it cannot infer, writes the
profile, takes the deliverable templates in, generates `CLAUDE.md`, scaffolds the directories
and registers, and prints the phase plan.

Needs Python 3 for the guard hooks, plus `openpyxl` / `python-docx` if your deliverables are
Excel or Word. [ADOPTION.md](ADOPTION.md) installs all of it from nothing, and its
troubleshooting section covers the failure that matters most — hooks that do not fire, which
turns baseline protection off without saying so.

Starting points per project shape: [profile/PROFILE-RECIPES.md](profile/PROFILE-RECIPES.md).

---

## Which pack do I want?

| Situation | Pack |
|---|---|
| Rewriting or replatforming an existing system, behaviour must be preserved | `migration-standard` |
| Building something new, or a substantial new subsystem | `sdlc-standard` |
| Migration that also adds significant new capability | `migration-standard` as the base; take `sdlc-requirements`, `sdlc-nfr-design` and `sdlc-test-st` from here for the new parts |
| Maintaining a system either pack delivered | `sdlc-standard`, P9 |
