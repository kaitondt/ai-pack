---
name: pm-project
description: "Project management spine — loads pm.profile.yaml, resolves {{profile.*}} tokens, detects the technical pack (sdlc/migration), and routes to the right management skill. Load this FIRST for ANY project-management task: charter, scope, WBS, schedule, estimate, cost, risk, quality, reporting, change control, closing."
---

# Project Management — Spine Skill

> **Load this skill first for every management task.**
> Every other `pm-*` skill assumes the profile is resolved and the invariant rules loaded.

This pack manages the **project**. A sibling pack — `sdlc-standard` or
`migration-standard` — manages the **product**. When one is installed they bind; when none
is, this pack still runs standalone.

---

## Step 1 — Load the profile (mandatory)

Read `.claude/pm.profile.yaml` from the repository root.

- **Missing** → stop. Tell the user to run `/pm-init`.
- **Unreplaced placeholder** (`<...>`) in a field you need → stop and ask for that field.
  Never substitute a plausible value into a management deliverable; a made-up date or
  amount is read as a commitment.
- **An unfilled `governance` role you need** → stop. A decision with no owner cannot be
  recorded, and an unrecorded decision is an assumption (DA-01).

Hold the resolved values for the whole task.

## Step 2 — Load the invariant rules

Always in force, regardless of what is being produced:

| Rule file | Enforces |
|---|---|
| `rules/pm/baseline-integrity.md` | the three baselines; change only through approved change control |
| `rules/pm/estimation-integrity.md` | method, basis, range; no back-fitting; visible buffers |
| `rules/pm/reporting-integrity.md` | evidence-based status; RAG follows the numbers |
| `rules/pm/decision-authority.md` | one named owner; authority matched to impact |
| `rules/pm/id-naming.md` | deterministic, permanent identifiers |
| `rules/pm/document-standards.md` | skeleton, versioning, attributable commitments, the format each artifact is delivered in |
| `rules/pm/git-commit.md` | commit format chosen at init; no archived snapshot changed or baselined document committed without its CR; no secret, rewrite or push |

## Step 3 — Detect the technical pack

Read `{{profile.integration.technical_pack}}`. When `auto`, look for, in order:

| Found | Technical pack | Read it for |
|---|---|---|
| `.claude/sdlc.profile.yaml` | `sdlc` | phases P0–P9, gates, quality targets, deliverable categories, test levels |
| `.claude/migration.profile.yaml` | `migration` | phases, gates, deliverable categories, legacy constraints |
| neither | `none` | nothing — this pack owns the process definition itself |

When a technical pack exists, **it owns the engineering truth** and this pack owns the
management view of it:

| Owned by the technical pack | Owned by this pack |
|---|---|
| deliverable list and their content rules | which work package produces each, when, at what cost |
| phase gates and their exit criteria | the milestone the gate satisfies, and its payment link |
| defect register, test levels, coverage | the quality plan, the targets, the report to the client |
| document review checklists | the audit that the reviews are actually happening |
| CR execution on documents and code | CR intake, impact across baselines, CCB approval |

Never duplicate the technical pack's data into a management document. Cite it, summarise
it, and let `/pm-sync-technical` verify the two still agree. A management plan that has
drifted from the technical reality is how a project reports green on work nobody is doing.

## Step 4 — Route to the management skill

Load `pm-document-io` **alongside** the area skill whenever the artifact is not Markdown.
`{{profile.documents.registry}}` binds each artifact to its final form, and
`{{profile.documents.binary_final}}` lists the ones where a text version is not the
deliverable — **the WBS among them** (MD-09).

| The task is about | Load |
|---|---|
| Project charter, authorisation, business case, objectives | `pm-project-charter` |
| Requirements management, scope statement, scope baseline, scope creep | `pm-scope` |
| Estimating effort, cost or duration; estimate review; bid support | `pm-estimation` |
| Budget, cost baseline, earned value, forecast, invoicing | `pm-cost` |
| The project management plan and its subsidiary plans | `pm-management-plan` |
| Development process, QA/QC process, tailoring, audits, CAPA | `pm-process` |
| WBS, WBS dictionary, activities, critical path, schedule baseline | `pm-schedule` |
| Stakeholders, communications, meetings, minutes, escalation | `pm-stakeholder` |
| Staffing plan, RACI, allocation, ramp-up, subcontract | `pm-resource` |
| Daily / weekly / monthly / quarterly / quality reports, status collection | `pm-reporting` |
| Quality plan, master test plan, quality metrics, acceptance criteria | `pm-quality` |
| Risk register, issue log, response planning, contingency | `pm-risk` |
| A change to any baseline; CCB; impact assessment | `pm-change-control` |
| Acceptance, handover, contract closure, lessons learned, archive | `pm-closure` |
| Producing or reading an artifact in Excel, Word or CSV; the WBS workbook | `pm-document-io` |
| Committing management documents to git | `/pm-commit` + `rules/pm/git-commit.md` |

---

## The management lifecycle

PMBOK process groups, expressed as what this pack actually produces:

```
INITIATING        PLANNING                      EXECUTING / CONTROLLING        CLOSING
charter ────────► scope baseline ─────────────► status collection ──────────► acceptance
stakeholders      WBS + dictionary              reports (D/W/M/Q + quality)    handover
business case     schedule baseline             earned value + forecast        contract closure
objectives        cost baseline                 change control (CCB)           lessons learned
                  quality + test plan           risk and issue management      final report
                  process definition            quality audits                 archive
                  resource + comms plan         gate reviews                   resource release
                  risk register (initial)       corrective action              PIR
```

| # | Management area | Skill | Primary artifact | Key command |
|---|---|---|---|---|
| 1 | Project overview | `pm-project-charter` | project charter | `/pm-charter` |
| 2 | Requirements / scope | `pm-scope` | scope baseline, RTM | `/pm-scope-baseline` |
| 3 | Cost / effort | `pm-estimation`, `pm-cost` | estimate, cost baseline, EVM | `/pm-estimate`, `/pm-evm` |
| 4 | Project management | `pm-management-plan`, `pm-stakeholder`, `pm-resource` | project management plan | `/pm-plan` |
| 5 | Process | `pm-process` | process definition, QA/QC plan | `/pm-process-define` |
| 6 | Schedule | `pm-schedule` | WBS, WBS dictionary, schedule baseline | `/pm-wbs`, `/pm-schedule-baseline` |
| 7 | Reporting | `pm-reporting` | D/W/M/Q and quality reports | `/pm-report <cadence>` |
| 8 | Quality | `pm-quality` | quality plan, master test plan | `/pm-quality-plan` |
| 9 | Risk | `pm-risk` | risk register, issue log | `/pm-risk-assess` |
| 10 | Closing | `pm-closure` | acceptance, final report, lessons | `/pm-closing` |

Cross-cutting at any time: `/pm-change-assess` → `/pm-change-apply`, `/pm-gate-review`,
`/pm-trace-check`, `/pm-health-check`, `/pm-status-collect`, `/pm-lessons`,
`/pm-sync-technical`, `/pm-commit`, `/pm-profile-check`, `/pm-refine-skill`.

---

## The planning order, which is not negotiable

Each artifact consumes the one before it. Producing them out of order produces numbers
with nothing behind them:

```
charter ─► scope statement ─► WBS ─► WBS dictionary ─► activities + dependencies
       ─► effort estimate ─► resource plan ─► schedule ─► cost baseline
       ─► quality plan ─► risk register ─► project management plan
```

Three consequences worth stating plainly:

1. **A schedule produced before the WBS is a list of dates.** There is nothing under it to
   measure progress against, and it will be re-drawn every month.
2. **A cost baseline produced before the resource plan is a spreadsheet.** Cost is effort ×
   rate × the people who will actually do it, at the allocation they will actually have.
3. **A risk register written last is a list of the risks that already happened.** Risks are
   identified while planning, when the response is still cheap.

---

## Standing behaviour on a managed project

1. **Compare against the baseline, always.** Status without a baseline is activity.
2. **Never move a baseline to make a variance disappear** (PB-06). The variance is the
   information.
3. **Nothing enters scope without a change request** (PB-07) — not the small useful
   addition, especially not that one.
4. **Every number carries its source and its as-of date** (RI-02). Not collected is a
   legitimate status; invented is not.
5. **RAG is computed, then explained** (RI-04). Never chosen, then justified.
6. **Bad news moves immediately** (RI-05), not on the reporting cadence.
7. **Every decision, risk, issue, action and change gets an ID and a register row** at the
   moment it exists, not before the audit.
8. **One named owner per item** (DA-01, DA-06). A team is not an owner.
9. **Estimates state method, basis and range** (ES-01), and are never derived backwards
   from the target (ES-02).
10. **Report honestly.** A slipping milestone is reported slipping, with the recovery
    option and its cost. A metric that could not be collected is reported as not collected.
11. **An artifact is delivered in its bound format** (MD-09). The WBS is a workbook; a
    Markdown WBS is a working file, and reporting it as done reports work that was not
    delivered.

---

## Reporting format

Status line:

```
{Project} · {period} — RAG {G|A|R} · SPI {x.xx} CPI {x.xx} · {milestone}: {status} · {n} open decisions
```

Completion of a management artifact:

```
═══════════════════════════════════════════
  {Artifact} — {version} {status}
  Baseline     : {set | unchanged | changed via CR-nnn}
  Approvals    : {role: name, date} for each required approver
  Consistency  : {PB-04 checks, pass/fail}
  Open Items   : {n} — {n} without an owner or a date
  Registers    : {RSK n, ISS n, DEC n, ACT n, CR n} updated
  Deliverable  : {path} ({format})  — for binary_final artifacts: present | *** MISSING ***
═══════════════════════════════════════════
```

If a required approval is missing, the artifact is reported **draft**, never "done".
