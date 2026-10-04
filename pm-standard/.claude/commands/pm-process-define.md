---
description: "Define and tailor the project's development and QA/QC process: phase entry/exit criteria, definition of done, QA audit plan, QC activities, process assets and the tailoring record. Usage: /pm-process-define"
---

# Define the process

## Step 1 — Load

`pm-project`, then `pm-process`. Agent: `pm-quality-manager`.

## Step 2 — Start from what exists

| Source | Take from it |
|---|---|
| `{{profile.process.standard_ref}}` | the organisational standard being tailored |
| the technical pack, if installed | the engineering process: phases, gates, deliverable rules, review checklists |
| the client's own process | anything contractually mandated |
| past lessons (`LL-*`) | the controls this organisation has learned it needs |

When a technical pack is installed it **owns** the engineering process. Do not restate its
phase model; cite it, and define what this pack owns: tailoring, audit, non-conformance and
the process metrics reported to the client.

## Step 3 — Define per phase (PR-01)

Entry criteria · inputs with baselined versions · activities and who performs them ·
standards · verification · exit criteria · outputs · metrics.

Make the exit criteria objective (PR-03): two people applying them to the same evidence reach
the same verdict. "Design is complete" fails that test; "every screen has an approved design
document with zero open Critical findings, and the RTM has no requirement without a design
item" passes.

## Step 4 — Record the tailoring (PR-02)

Every deviation from the standard: what, why, the risk accepted, and who approved it.

Schedule pressure is not a tailoring reason — it is a decision to accept quality risk, and it
is recorded as such with the sponsor's name on it. When a control is tailored out, name the
risk it managed and what replaces it, if anything.

## Step 5 — Separate QA from QC (PR-04)

QA activities (`{{profile.process.qa.activities}}`) with an owner and an audit cadence; QC
activities (`{{profile.process.qc.activities}}`) with reviewers and verifiers.

The organisational rule: QA is never performed by the person whose work is being assured.

## Step 6 — Definition of done (PR-05)

One list, binary, applied to every work package — including the three items always dropped
under pressure: design document updated, test case updated and executed, traceability row
updated.

## Step 7 — Set up the audit and CAPA machinery

Schedule audits at `{{profile.process.qa.audit_cadence}}` — **with effort for them in the
WBS**, or they will not happen. Initialise `{{profile.process.corrective_actions}}` with the
CAPA fields including the effectiveness check (PR-07).

## Report

```
Process definition — v{n}
  Phases defined   : {n}, all with objective entry/exit? {yes | which are not}
  Tailoring        : {n} deviations, all with reason + risk + approver? {yes|no}
  QA / QC          : separated with different owners? {yes|no}
  Definition of done: {n} items
  Audit            : {cadence}, next {date}, effort in WBS? {yes|no}
  Process assets   : {n} at {path}, versioned? {yes|no}
  Technical pack   : {cited | this pack owns the engineering process}
```
