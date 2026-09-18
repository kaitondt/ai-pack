---
description: "Produce the scope baseline: scope statement, deliverables with acceptance criteria, requirement traceability matrix, and the link to the WBS. Usage: /pm_scope_baseline [area]"
---

# Scope baseline

The scope baseline is **scope statement + WBS + WBS dictionary** (PB-02). This command
produces the scope statement and the RTM; `/pm_wbs` produces the other two.

## Step 1 — Load

`pm_project`, then `pm_scope`. Agent: `pm_planner`.

## Step 2 — Read what already decides scope

The charter (baselined), the contract or SOW, the requirement source
`{{profile.scope.requirements.source}}`, and — when a technical pack is installed — its
requirement artifacts. Never restate requirement text here; cite it.

## Step 3 — Write the scope statement

Sections per `pm_scope`. Two that carry the most weight later:

- **Out of scope, each with a reason** (SM-07). An exclusion with no reason is re-litigated
  monthly; one with a reason is accepted once.
- **Deliverables with acceptance criteria and a named acceptor** (SM-06), agreed *before* the
  work starts. Criteria written at delivery time are negotiated under pressure by whoever has
  more leverage.

For a migration project, add the list of legacy behaviour being **dropped**, each with the
decision that dropped it. It is the section nobody writes and everybody needs at UAT.

## Step 4 — Build the RTM

One row per requirement: ID, requirement, source, priority, owner, work package, deliverable,
verified by, status. Write it to `{{profile.scope.requirements.traceability}}`.

Then report the three orphan classes (SM-02):

| Orphan | Means |
|---|---|
| requirement with no work package | agreed but unplanned — it will be discovered late |
| work package with no requirement | unplanned work — gold-plating, or an unwritten requirement |
| requirement with no test | it cannot be accepted; the acceptance meeting will find this |

## Step 5 — Screen every requirement (SM-01)

Reject into an open-question list: untestable, compound ("and"), solution-shaped,
unquantified adjectives, no source, no owner. Convert each rejection into a question to
`{{profile.scope.requirements.owner}}` rather than fixing it by guessing.

## Step 6 — Approve and baseline

Per `{{profile.governance.approvals.scope_baseline}}`. Register as baselined once the WBS and
dictionary exist — the three are baselined together.

## Report

```
Scope baseline — v{n} {status}
  Deliverables  : {n} — with acceptance criteria {n} — with named acceptor {n}
  Exclusions    : {n} — with reasons {n}
  Requirements  : {n} in scope
    orphan up   : {n} (no work package)
    orphan down : {n} (no test)
    unplanned   : {n} work packages with no requirement
    screened out: {n} — {reasons}, raised as open questions
  Open items    : {n}
```
