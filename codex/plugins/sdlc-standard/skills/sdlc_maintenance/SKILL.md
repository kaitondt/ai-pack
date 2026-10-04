---
name: sdlc_maintenance
description: "P9 — maintenance after go-live. Incident intake and classification, SLA handling, the three-phase investigate/fix/report workflow, root cause analysis, hotfix rules, regression obligations, knowledge base and preventive action. Load for ALL post-release incident, support and maintenance tasks."
---

# P9 — Maintenance

> Prerequisite: `sdlc_project` resolved; the system is accepted and in production.
> Three phases, strictly separated. **Do not merge them.**

```
Phase 1  INVESTIGATE  -> classification + root cause + proposal, then STOP for approval
Phase 2  FIX          -> only after explicit approval; hotfix or scheduled release
Phase 3  REPORT       -> written to {{profile.paths.maintenance}}
```

Maintenance is where a project's earlier shortcuts are collected and paid for, with
interest, by people who did not take them. Two habits do most of the work here: classify
honestly, and never fix without adding the test that would have caught it.

---

## Standing constraints

**C1 — investigation stops at the conclusion.** Phase 1 ends with a root cause and a
proposal. No `Write`, no `Edit` to product code or documents during Phase 1. Read-only
tools only. Proceed to Phase 2 only on explicit approval.

**C2 — every conclusion is anchored.** A claim that the system is right or wrong cites at
least one of: the current source, the baselined design documents, the baselined
requirements. If all three are silent on the disputed behaviour, the classification is
`REQ-GAP`: ask, do not decide (RS-01, RS-05).

**C3 — production is changed only through the release process** (BL-04). No manual edit on
a server, no ad-hoc data update typed into a console. Data fixes are reviewed scripts,
stored under `{{profile.paths.maintenance}}`, run with a record of who ran them and when.

**C4 — the incident id comes from the tracking system.** Never invent one. Phase 1 can run
without it; Phase 3 cannot — ask.

**C5 — verify repository and environment facts before relying on them**: which version is
deployed, which configuration that environment has, whether a file is generated, which
branch the fix belongs on. Check, do not assume.

**C6 — report only what actually ran.** Build and test output in the report is real output.
A failing test is reported as failing, with its output.

**C7 — the SLA clock is a fact, not a target to manage.** Record when the incident arrived,
when it was acknowledged, when it was resolved. `{{profile.maintenance.sla}}` says what was
promised; the record says what happened. Adjusting either to make the other look better is
the metric-tuning failure (QM-08).

---

## Phase 1 — Investigate

1. **Capture the report.** What the user did, what happened, what they expected, when,
   which environment, which user, which record. An unclear report is clarified before
   investigation, not guessed at.
2. **Triage immediately**: severity from `{{profile.quality.severity}}`, class from
   `{{profile.maintenance.classes}}`, SLA clock started, and the reporter told what it was
   classified as.
3. **Establish whether it is happening now.** An ongoing production issue is stabilised
   first — workaround, restart, feature toggle — and investigated second. Say clearly which
   of the two you are doing.
4. **Locate** via the locator map below. Do not start with a repository-wide search.
5. **Read the source, the design documents and the requirement** for the behaviour in
   dispute.
6. **Read the operational evidence**: logs around the timestamp, the correlation id, the
   batch run record, the monitoring signals, and what was deployed when.
7. **Classify and conclude.** Root cause, injection phase (TR-07), evidence with anchors,
   proposal, risk, and whether it needs a hotfix or the next release.
8. **Stop.**

### Locator map

Derive concrete paths from the profile before starting:

| From | To | Path |
|---|---|---|
| module id | screen design | `{{profile.paths.design_root}}/{screen dir}/…{MODULE}-SC-…` |
| module id | function design | `{{profile.paths.design_root}}/{function dir}/…{MODULE}-FC-…` |
| module id | interface design | `{{profile.paths.design_root}}/{interface dir}/…{MODULE}-API-…` |
| module id | detail design | `{{profile.paths.detail_design}}/…{MODULE}…` |
| module id | source | `{{profile.system.root}}` — feature folder for the module |
| requirement | SRS section | `{{profile.paths.requirements}}` |
| symptom | prior incidents | `{{profile.maintenance.knowledge_base}}` |
| job name | run record | operational logs per BT-O |
| any | traceability rows | `{{profile.paths.traceability}}` |

**Check the knowledge base first.** A recurring incident already investigated does not need
investigating again — it needs its preventive action finished.

### Classification

| Class | Meaning | Owner |
|---|---|---|
| `INC-DEFECT` | the system contradicts its baselined specification | development |
| `INC-DATA` | the software is correct; the data is wrong | data owner, with a fix script (C3) |
| `INC-ENV` | configuration, capacity, network, certificate, dependency outage | operations |
| `INC-USAGE` | the system behaves as specified; the user expected something else | support / documentation |
| `INC-ENHANCEMENT` | works as specified; the client wants different | change request |
| `INC-EXTERNAL` | the cause is in a system this project does not own | that system's owner, with evidence |
| `REQ-GAP` | no baselined document decides the behaviour | product owner decision |

`INC-USAGE` needs the strongest evidence, not the weakest: cite the requirement, the design
and the code. And a repeated `INC-USAGE` is a defect in the UI or the documentation
(UA-06), not a run of confused users.

---

## Phase 2 — Fix

Only after explicit approval, and only within the approved scope.

### Route: hotfix or scheduled release

| | Hotfix | Scheduled release |
|---|---|---|
| When | S1, or S2 with no workaround | everything else |
| Approval | `{{profile.maintenance.hotfix.approval}}` | normal release process |
| Scope | the minimum change that resolves it | the fix, done properly |
| Testing | targeted regression, documented as reduced | full cycle |
| Documentation debt | due within `{{profile.maintenance.hotfix.retro_documentation_days}}` days (BL-06) | none — done with the change |

**A hotfix skips the queue, never the record.** An undocumented hotfix is a defect the
project has deliberately hidden from itself, and it is the reason the next investigation
reaches the wrong conclusion.

### Rules

- Fix the layer the classification names. An `INC-DEFECT` caused by a wrong design requires
  the document to change too — fixing only the code recreates the divergence.
- A baselined document changes through a CR (BL-02). A defect fix that corrects a document
  to what it always should have said is a defect correction, recorded as such, not a CR.
- Load `sdlc_context_mapping` before editing; a maintenance fix that touches one layer of five
  is the classic source of the next incident.
- **Add the regression test that would have caught it**
  (`{{profile.maintenance.regression_test_required}}`) — at the level that would have
  caught it. A UT-level bug gets a UT, not an E2E.
- Verify: build in the mandated order, type-check, run the tests covering the change, and
  re-run the original reproduction.
- Data fixes: a script, reviewed, with a dry-run count first, a rollback plan, and a record
  of the rows affected (C3).

### Root cause analysis

Required for `{{profile.maintenance.rca_required_for}}`. Three questions, answered
separately:

1. **Why did it happen?** The technical cause, anchored.
2. **Why was it not caught?** The check that should have found it — a review, a test case, a
   gate — and why it did not. This is the answer that changes the process. For S1/S2, or
   whenever the answer is disputed, produce it with `/sdlc_trace_bug` (`sdlc_bug_trace`) and
   quote its escape statement here.
3. **What stops it recurring?** A test, a rule, a hook, a monitoring signal, or an accepted
   risk with a named owner. "Be more careful" is not a preventive action.

Feed the answer to (2) back through `/sdlc_refine_skill`. An RCA that ends at (1) produces
a fixed bug and an unchanged process.

---

## Phase 3 — Report

File: `{{profile.paths.maintenance}}/{INC-ID}_{MODULE}_{short-slug}.md`

An existing file for the same incident id is **appended to** with a new round, never
overwritten — the history of what was tried is the point.

```markdown
# {INC-ID} — {short title}

## 1. Summary
Reported by, date/time, environment, module, symptom, users affected, severity, class,
SLA: acknowledged at / resolved at.

## 2. Root cause
The direct cause, with anchors: source path:line, design document id and section,
requirement id. Injection phase. What was ruled out and why.

## 3. Solution
Route (hotfix / scheduled release). What was changed, file by file. Documents updated, or
the documentation debt with its due date. Data script, if any, with the rows affected.

## 4. Verification
Actual output: build, type-check, tests run and their results, the original reproduction
re-run. Real output only (C6).

## 5. Prevention
Regression test added, at which level. The check that should have caught it and why it did
not. The preventive action, its owner and its date. Related modules sharing the pattern.

## 6. Knowledge base
The one-paragraph entry added to {{profile.maintenance.knowledge_base}}: symptom, cause,
resolution — written so the next person finds it by searching the symptom.
```

---

## Standing maintenance duties

Beyond individual incidents:

| Duty | Cadence | Why |
|---|---|---|
| Review recurring incidents | monthly | three of the same is a defect in the system, not in the users |
| Dependency and security updates | per `references/rules/common/security.md` | a Critical advisory blocks the next release |
| Capacity review against the NFR assumptions | quarterly | the growth `ASM-*` from P1 either held or did not |
| Backup restore rehearsal | per the RPO/RTO commitment | a backup whose restore has never been tested is a belief |
| Runbook accuracy | after every incident that needed it | the gaps are only visible under pressure |
| Deferred-defect review | per release | a deferral with no review becomes a permanent silence |

## Exit gate

- [ ] every incident has a class, a severity, a root cause and a closure record
- [ ] every S1/S2 has an RCA answering all three questions
- [ ] every fix has its regression test
- [ ] every hotfix's documentation debt closed inside the window
- [ ] every recurring incident has a preventive action or an accepted risk with an owner
- [ ] `{{profile.gates.P9_maintenance.exit}}` assertions hold
