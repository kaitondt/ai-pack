# PM Skill Pack (PSP) — Standard Edition

A **project-agnostic Claude Code skill pack for managing software projects**, aligned with
PMBOK. Covers the ten management areas: charter · scope · cost · plan · process · schedule ·
reporting · quality · risk · closing.

The third sibling of [`migration-standard`](../migration-standard/README.md) and
[`sdlc-standard`](../sdlc-standard/README.md). Same architecture — one profile file, invariant
rules, area skills, entry-point commands, delegated agents — different subject.

> Those two packs manage the **product**: what gets built and whether it is correct.
> This one manages the **project**: what was committed, at what cost, by which date, approved
> by whom, and whether that is still true.

---

## The core idea

```
┌──────────────────────────────────────────────────────────────────┐
│  pm.profile.yaml       ← the ONLY file you edit per project      │
│  (governance, calendar, WBS, cost, quality, risk, reporting,     │
│   change control, closing, and the binding to the technical pack)│
└───────────────────────────┬──────────────────────────────────────┘
                            │ resolved by  skill: pm-project
                            ▼
┌──────────────────────────────────────────────────────────────────┐
│  rules/pm/ — invariant standards (baselines, estimates, reports) │
│  skills/   — area knowledge, loaded into context on demand       │
│  commands/ — entry-point workflows the user types                │
│  agents/   — delegated workers with narrow tool sets             │
└──────────────────────────────────────────────────────────────────┘
```

A skill never hardcodes a milestone date, a contingency percentage or an approval chain. It
writes `{{profile.schedule.milestones}}`, `{{profile.cost.contingency_percent}}`,
`{{profile.governance.approvals.charter}}` and resolves them at load time.

---

## The ten areas

| # | Area | Skill | Primary artifact | Entry command |
|---|---|---|---|---|
| 1 | Project overview | `pm-project-charter` | project charter | `/pm-charter` |
| 2 | Requirements / scope | `pm-scope` | scope baseline, RTM | `/pm-scope-baseline` |
| 3 | Cost / effort | `pm-estimation`, `pm-cost` | estimate, cost baseline, EVM | `/pm-estimate`, `/pm-cost-baseline`, `/pm-evm` |
| 4 | Project management | `pm-management-plan`, `pm-stakeholder`, `pm-resource` | project management plan | `/pm-plan`, `/pm-comm-plan`, `/pm-resource-plan` |
| 5 | Process (dev, QA/QC) | `pm-process` | process definition, tailoring, CAPA | `/pm-process-define`, `/pm-audit` |
| 6 | Schedule | `pm-schedule` | WBS + dictionary (**one Excel workbook**), schedule baseline | `/pm-wbs`, `/pm-schedule-baseline` |
| 7 | Reporting | `pm-reporting` | daily / weekly / monthly / quarterly / quality | `/pm-status-collect`, `/pm-report` |
| 8 | Quality | `pm-quality` | quality plan, master test plan | `/pm-quality-plan` |
| 9 | Risk | `pm-risk` | risk register, issue log | `/pm-risk-assess`, `/pm-risk-review` |
| 10 | Closing | `pm-closure` | acceptance, final report, lessons | `/pm-closing`, `/pm-lessons` |

Cross-cutting: `pm-change-control` (`/pm-change-assess` → `/pm-change-apply`),
`/pm-gate-review`, `/pm-trace-check`, `/pm-health-check`, `/pm-sync-technical`,
`/pm-profile-check`, `/pm-refine-skill`.

---

## What is different from the two technical packs

A migration project has an oracle: the old system. A development project has an approved
specification. **A project has neither** — only what was committed, and evidence of what has
happened since.

That difference produces the pack's invariants:

| Technical pack invariant | Management counterpart |
|---|---|
| No invention — anchor to legacy source | **No commitment without an anchor** — the charter, a baselined document, an approved CR, or a recorded decision |
| Legacy is read-only | **Baselines are change-controlled**, and never moved to erase a variance |
| Blocked features stop the run | **Undecided approvals stop the baseline** |
| BD ↔ code drift report | **Plan ↔ reality drift**: EVM, trace check, health check |
| Deliverable review checklists | **Process audit** — is the review actually happening? |
| — | **Estimation integrity** — method, basis, range; no back-fitting; visible buffers |
| — | **Reporting integrity** — evidence-based numbers, computed RAG, immediate bad news |
| — | **Decision authority** — one named owner, authority matched to impact, escalation on a clock |

---

## The load-bearing rules

| # | Rule | Where |
|---|---|---|
| 1 | **A baseline exists only after a named approval**, and changes only through change control | `rules/pm/baseline-integrity.md` PB-01, PB-03 |
| 2 | **The scope baseline is three documents** — statement, WBS, dictionary | PB-02 |
| 3 | **Baselines stay consistent** — every work package scheduled, costed and traced | PB-04 |
| 4 | **Actuals never overwrite the baseline**; re-baselining retains history and reason | PB-05, PB-06 |
| 5 | **Nothing enters scope without a change request** | PB-07 |
| 6 | **Every estimate carries method, basis, range, assumptions** | `rules/pm/estimation-integrity.md` ES-01 |
| 7 | **Estimate the work, never back-fit the target** | ES-02 |
| 8 | **Padding forbidden, buffers mandatory**; contingency ≠ management reserve | ES-05, ES-06 |
| 9 | **Every reported number has a source and an as-of date** | `rules/pm/reporting-integrity.md` RI-02 |
| 10 | **Progress by the defined method, RAG computed from thresholds** | RI-03, RI-04 |
| 11 | **Bad news travels immediately**, not on the cadence | RI-05 |
| 12 | **Metrics are never improved by reclassifying the work** | RI-09 |
| 13 | **One named owner per decision; authority matched to impact** | `rules/pm/decision-authority.md` DA-01, DA-02 |
| 14 | **Decisions recorded when made; the log is append-only** | DA-03 |
| 15 | **IDs are deterministic and permanent**; WBS codes are never reused | `rules/pm/id-naming.md` PN-02, PN-03 |
| 16 | **Format is a property of the artifact** — and the WBS is delivered as Excel; Markdown and CSV are working forms only | `rules/pm/document-standards.md` MD-09, `skills/pm-document-io` DIO-W |
| 17 | **A working file is not a deliverable**, and says so on line one — exactly one authority per artifact | `rules/pm/document-standards.md` MD-10 |
| 16 | **No automatic version bump; every commitment attributable** | `rules/pm/document-standards.md` MD-02, MD-04 |

## What is variable (lives in the profile)

Governance and approval chains · escalation ladder and SLAs · calendar and productivity ·
WBS shape and sizing rules · **the format each deliverable is delivered in** · milestones
and payment links · estimating methods and rates ·
contingency and reserve policy · EVM formula · process standard and tailoring · quality
targets, test levels and defect model · risk scales and thresholds · reporting cadences,
audiences and RAG definitions · change authority thresholds · resource limits · closing and
handover checklist · the binding to the technical pack.

---

## Working alongside a technical pack

`/pm-init` detects `sdlc.profile.yaml` or `migration.profile.yaml` and sets
`integration.technical_pack`. Then the division is fixed:

| The technical pack owns | This pack owns |
|---|---|
| deliverable list and content rules | which work package produces each, when, at what cost |
| phase gates and engineering exit criteria | the milestone the gate satisfies, and its payment link |
| defect register, test levels, coverage data | quality plan, targets, and the report to the client |
| document review checklists | the audit that reviews are actually happening |
| CR execution on documents and code | CR intake, impact across baselines, CCB approval |

**Never duplicate the technical pack's data into a management document.** Cite it, and let
`/pm-sync-technical` verify the two still agree. Drift between them is how a project reports
green on a plan that no longer describes the work being done.

The pack also runs standalone (`technical_pack: none`) — for a project managed here whose
engineering is run by another team, another vendor, or another toolchain.

---

## Deliverable formats, and the one that is fixed

Management deliverables are contractual artifacts, so their format is a property of the
artifact rather than a per-task choice. `{{profile.documents.registry}}` binds each one:
Excel for the tabular and numeric artifacts, Word where the client supplies a form, Markdown
for narrative documents reviewed in a pull request, CSV for registers exchanged with other
tools. `pm-document-io` owns the mechanics for all four, and every agent can write them.

**The WBS is delivered as Excel.** Draft it in Markdown or CSV if that helps — text is easier
to restructure than a workbook, and `documents.working_dir` exists for exactly that — but the
artifact is the `.xlsx`, and `wbs` sits in `documents.binary_final`, which makes the workbook
existing the completion criterion (MD-09).

Not a formatting preference: cost, progress, resource loading and earned value all index into
the WBS by code, and every one of those consumers is a spreadsheet. A WBS that is not one gets
re-keyed into one by hand, and the project then has two that disagree.

Two supporting rules make that safe rather than merely stated. Every scratch file carries a
stamp on line one saying whether it is a draft or a generated export (MD-10), so exactly one
file is ever the authority. And the workbook is never regenerated from a working file older
than itself — the alternative erases whoever edited the workbook last, silently.

---

## Layout

```
pm-standard/
├── README.md                      ← this file
├── ADOPTION.md                    ← 30-minute onboarding for a new project
├── COMMAND-FLOW.md                ← how the commands chain, and the control loop
├── profile/
│   ├── pm.profile.yaml            ← template to copy
│   ├── PROFILE-SCHEMA.md          ← field-by-field spec
│   └── examples/
│       ├── offshore-fixed-price.profile.yaml
│       └── internal-agile.profile.yaml
└── .claude/
    ├── CLAUDE.md                  ← project-instruction template
    ├── settings.json
    ├── hooks/                     ← 3 hooks (profile check, baseline guard, doc rules)
    ├── rules/pm/                  ← 6 invariant rule files
    ├── skills/                    ← 16 skills
    ├── commands/                  ← 28 slash commands
    └── agents/                    ← 7 agents
```

---

## The planning order, which is the spine of the pack

```
charter ─► scope statement ─► WBS ─► WBS dictionary ─► activities + dependencies
        ─► effort estimate ─► resource plan ─► schedule ─► cost baseline
        ─► quality plan ─► risk register ─► project management plan
```

Each artifact consumes the one before it. Three consequences, and they are the most common
ways a plan turns out to be decorative:

1. **A schedule produced before the WBS is a list of dates.** There is nothing underneath it
   to measure progress against, so it is re-drawn every month.
2. **A cost baseline produced before the resource plan is a spreadsheet.** Cost is effort ×
   rate × the people who will actually do it, at the allocation they will actually have.
3. **A risk register written last is a list of the risks that already happened.**

---

## The control loop, which is what the pack does after planning

```
plan → execute → measure (/pm-status-collect) → compare (/pm-evm, /pm-trace-check)
     → decide (/pm-report, /pm-gate-review) → act (/pm-change-assess → /pm-change-apply)
     → re-plan, or re-baseline with a recorded reason
```

The loop is only real when the "decide" step has a named owner and a forum with a date. A
measurement that reaches no decision-maker is data collection, not control — and it is how a
project accumulates metrics while remaining unmanaged.

---

## Model policy

Every `pm-*` agent ships with `model: opus`, set from `execution.agent_model`.

This is deliberate. Management artifacts fail **silently**: an estimate with a missing work
package, a WBS that omits the testing branch, a report whose RAG does not follow from its own
numbers, a risk register listing only what already happened, a CR assessment that skipped the
documentation cascade. None of it fails loudly — it fails at the steering committee, or at
acceptance, after decisions were made on it.

Reasoning effort is a session-level setting in Claude Code, not agent frontmatter.
`execution.intended_effort` records the level the project runs at; set it in your own session.

---

## Quick start

```bash
cp -r pm-standard/.claude              <your-project>/.claude      # or merge, see ADOPTION.md
cp pm-standard/profile/pm.profile.yaml <your-project>/.claude/pm.profile.yaml
# then, inside the project:
/pm-init
```

`/pm-init` inspects the repository, detects an installed technical pack, interviews you for
what it cannot infer, writes the profile, scaffolds `pm/` and the registers, and generates or
appends to `CLAUDE.md`. See [ADOPTION.md](ADOPTION.md).

---

## Which pack do I want?

| Situation | Pack |
|---|---|
| Rewriting or replatforming an existing system | `migration-standard` |
| Building something new | `sdlc-standard` |
| Running the project around either of those — plan, cost, report, govern | **`pm-standard`, alongside it** |
| Managing a project whose engineering is done elsewhere | `pm-standard` standalone |
| A PM taking over a project and needing an honest picture | `pm-standard`, then `/pm-health-check` |
