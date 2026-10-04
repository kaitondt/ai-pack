---
name: pm_process
description: "Process management — defining and tailoring the development process, the QA process (prevention and compliance) and the QC process (product inspection), entry/exit criteria, definition of done, process assets, process audits, non-conformance and corrective action (CAPA). Load for ALL process-definition, tailoring, QA/QC-process, audit and CAPA tasks."
---

# Process Management (Development Process · QA/QC Process)

> Prerequisite: `pm_project` loaded.

Process work has one purpose: make the outcome **repeatable and inspectable**. A process
that is not followed is worse than no process, because it produces evidence that nothing is
wrong while nothing is being checked.

The most common failure here is not the absence of a process. It is a process defined in
month one, never audited, and quietly abandoned by month three — with the document still
sitting in the repository, still cited in the plan, and still shown to the auditor.

---

## PR-01 — Define the process the project will actually follow

Not the organisational standard verbatim, and not an aspiration. For each phase or activity:

| Element | Content |
|---|---|
| Entry criteria | what must be true to start |
| Inputs | which artifacts, at which baselined version |
| Activities | who does what, in what order |
| Standards | the rules that apply (templates, checklists, coding standards) |
| Verification | review, test or inspection, and who performs it |
| Exit criteria | objective, checkable conditions to declare it complete |
| Outputs | artifacts produced, and where they live |
| Metrics | what is measured, and where it is reported |

When a technical pack is installed, **it defines the engineering process** — its phases,
gates, deliverable rules and review checklists. This skill then owns: the tailoring record,
the audit that the process is followed, the non-conformance handling, and the process
metrics reported to the client. Do not restate its phase model here; cite it.

## PR-02 — Tailoring is legitimate; undocumented tailoring is a finding

Every deviation from `{{profile.process.standard_ref}}` is recorded in
`{{profile.process.tailoring_record}}`:

| Standard element | Tailoring | Reason | Risk accepted | Approved by |
|---|---|---|---|---|

Legitimate reasons: project size, contract type, client's own process, technology, team
maturity, regulatory context. Not legitimate: schedule pressure — that is not tailoring,
it is a decision to accept quality risk, and it is recorded as such, with the sponsor's name
on it.

Tailoring **out** a control means the risk it managed now has no control. Say which risk,
and say what replaces it, if anything.

## PR-03 — Entry and exit criteria are objective or they are decoration

"Design is complete" is not an exit criterion. "Every screen has an approved design document
with zero open Critical review findings, and the RTM shows no requirement without a design
item" is.

The test: two people, applying the criterion to the same evidence, reach the same verdict.
If they can disagree, it is a discussion topic and the phase will end when someone is tired,
not when it is finished.

## PR-04 — QA and QC are different activities with different owners

| | QA — quality assurance | QC — quality control |
|---|---|---|
| Object | the **process** | the **product** |
| Question | are we working the way we agreed? | does this artifact meet its standard? |
| Activities | `{{profile.process.qa.activities}}` | `{{profile.process.qc.activities}}` |
| Timing | continuous, plus scheduled audits | at every artifact and every build |
| Owner | `{{profile.process.qa.owner}}` | the doer and the reviewer |
| Output | audit findings, corrective actions, process metrics | review findings, defects, test results |
| Nature | preventive | detective |

A project with only QC finds defects efficiently and keeps producing them at the same rate,
forever, because nothing examines *why* they are produced. A project with only QA has a
tidy process and an unmeasured product.

The one organisational rule: **QA cannot be performed by the person whose work is being
assured.** A developer reviewing their own compliance is not an audit; it is an opinion with
a form attached.

## PR-05 — The definition of done is one list, applied everywhere

`{{profile.process.definition_of_done}}` applies to every work package (WB-05). It is short,
binary, and includes the things habitually left out:

code reviewed and merged · unit tests pass and coverage met · **design document updated** ·
**test case updated and executed** · **traceability row updated** · no open Critical review
finding.

The three emphasised items are the ones that get dropped under pressure, and each one is a
documentation debt that becomes a defect two phases later — the document that no longer
matches the code, the test that no longer matches the spec, the requirement nobody can prove
was built.

## PR-06 — Process audits, on a cadence, with evidence

`{{profile.process.qa.audit_cadence}}`, recorded in `{{profile.process.qa.audit_record}}`.

An audit samples **artifacts**, not opinions:

| Check | Evidence sampled |
|---|---|
| Are reviews happening? | review records in documents; review density vs target |
| Are exit criteria applied? | gate records; artifacts that passed with open items |
| Is traceability maintained? | RTM against artifacts actually on disk |
| Are tests run and recorded? | test results, per named run and build |
| Are changes going through change control? | baselined documents modified without a CR |
| Are defects classified honestly? | severity distribution and re-classification history |
| Is the tailoring record current? | observed practice vs the recorded process |

Report findings as **non-conformances**, each with severity, evidence, owner and due date,
tracked in `{{profile.process.corrective_actions}}` until closed.

A useful signal in itself: an audit that finds nothing, repeatedly, is sampling the wrong
things. Real projects deviate; the question is whether the deviation is known.

## PR-07 — Corrective action addresses the cause, not the instance

A CAPA entry:

| Field | Content |
|---|---|
| `CAPA-*` | id |
| Non-conformance | what was observed, with evidence |
| Immediate correction | fixing the instance found |
| Root cause | why it happened — process, capacity, knowledge, tooling, incentive |
| Corrective action | what changes so it does not recur |
| Preventive action | where else this could occur, addressed proactively |
| Owner, due date | one named person |
| Effectiveness check | date and result of re-checking |

Without the effectiveness check, CAPA becomes a list of good intentions. Re-check on a date;
if the non-conformance recurs, the root cause was wrong — say so and re-analyse rather than
re-issuing the same action.

Watch for root causes that are really symptoms: "the developer forgot" is not a root cause.
Why was forgetting possible? Where was the checklist, the automation, the review that should
have caught it? That answer is the corrective action, and it usually belongs in the pack
itself (`/pm_refine_skill`).

## PR-08 — Process metrics are for improvement, not for individuals

Review density, defect density, phase containment, rework rate, cycle time, process
compliance rate. Reported per artifact type, per phase, per team — **never per person**.

The moment a process metric is used to evaluate an individual, the metric stops measuring
the process and starts measuring how well people manage the metric. Review findings drop to
zero, defects get logged as "clarifications", and the organisation loses the data it was
collecting.

---

## Process assets

`{{profile.process.process_assets}}` holds the templates, checklists and standards the
project actually uses. Two properties matter:

1. **One authoritative copy.** A checklist duplicated into three directories is three
   different checklists within a month.
2. **Versioned and dated.** An artifact reviewed against v2 of a checklist records that,
   so an audit can tell whether it passed the current standard.

At closing, the improved assets go back to the organisation (`pm_closure`). That transfer
is the only mechanism by which one project's learning reaches the next one.

---

## Exit criteria

- [ ] Process defined per phase with objective entry/exit criteria (PR-01, PR-03)
- [ ] Tailoring recorded with reason, risk accepted and approver (PR-02)
- [ ] QA and QC activities separated, with different owners (PR-04)
- [ ] Definition of done agreed and applied to work packages (PR-05)
- [ ] Audit cadence scheduled, with effort for it in the WBS
- [ ] CAPA log exists with effectiveness checks (PR-07)
- [ ] Process assets in one place, versioned
