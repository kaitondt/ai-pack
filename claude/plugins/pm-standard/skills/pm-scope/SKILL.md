---
name: pm-scope
description: "Requirements and scope management — requirements management plan, scope statement, scope baseline, requirement traceability matrix, scope verification and validation, and scope-creep control. Load for ALL scope, requirement-management, RTM, acceptance-criteria and scope-change tasks."
---

# Requirements and Scope Management

> Prerequisite: `pm-project` loaded.

Scope management answers two questions for the life of the project: **what did we agree to
build**, and **is what we are building still that**.

The distinction that makes this skill work: this pack manages the *requirement process* —
who owns requirements, how they are baselined, how they are traced, how a change to one is
authorised. The technical pack (`sdlc-requirements` / `mig-requirements`) manages the
*requirement content*. When both are installed, never duplicate the requirement text here;
cite it.

---

## The scope baseline is three documents (PB-02)

| Document | Path | Answers |
|---|---|---|
| Scope statement | `{{profile.paths.scope_statement}}` | what is included, excluded, and delivered |
| WBS | `{{profile.paths.wbs}}` | the work that produces it (`pm-schedule`) |
| WBS dictionary | `{{profile.paths.wbs_dictionary}}` | what each work package means and when it is done |

Any of the three changing is a scope-baseline change, and needs the authority in
`{{profile.change_control.authority}}`.

---

## Requirements management plan

Written once, early, and short. It decides:

| Decision | Typical content |
|---|---|
| Who owns requirements | `{{profile.scope.requirements.owner}}` — one named person who can resolve a conflict |
| Where they live | `{{profile.scope.requirements.source}}`, one place, cited everywhere |
| ID format | `{{profile.scope.requirements.id_format}}`, permanent, never renumbered (PN-03) |
| Prioritisation | MoSCoW, or a ranked list — and who ranks |
| Baselining | when a requirement set is frozen and by whose approval |
| Change path | any change to a baselined requirement is a `CR-*` |
| Traceability | `{{profile.scope.requirements.traceability}}`, updated as work happens |
| Verification | which test level proves each requirement (`pm-quality`) |

## SM-01 — A requirement is testable, atomic, and has one owner

Screening applies to every requirement entering the baseline, whoever wrote it:

| Reject when | Because |
|---|---|
| It cannot be verified | no test can be written, so "done" is an opinion |
| It contains "and" joining two behaviours | it will be half-delivered and half-argued |
| It states a solution instead of a need | it removes the option to deliver it more cheaply |
| It uses an unquantified adjective — fast, simple, user-friendly, robust | it will be measured at acceptance by someone else's standard |
| It has no source | it is an assumption someone wrote confidently |
| It has no owner | nobody can approve, change or accept it |

"Fast" costs nothing to write and can cost a month to satisfy. Convert at the time of
writing: how many seconds, at what concurrency, on which environment, measured how.

## SM-02 — Every requirement traces both ways

Up: to a charter objective or business requirement, so the reason it exists is recorded.
Down: to the work package that builds it and the test case that proves it.

The RTM has one row per requirement:

| REQ ID | Requirement | Source | Priority | Owner | Work package | Deliverable | Verified by | Status |
|---|---|---|---|---|---|---|---|---|

Three orphan classes, all reported by `/pm-trace-check`, all meaning something specific:

| Orphan | Meaning |
|---|---|
| Requirement with no work package | agreed, unplanned — it will be discovered late or missed |
| Work package with no requirement | unplanned work — gold-plating, or a requirement nobody wrote down |
| Requirement with no test | it cannot be accepted; the acceptance meeting will discover this |

## SM-03 — Scope creep is silent, and this is how it enters

It rarely arrives as a change request. It arrives as:

| Route | What it looks like | Counter |
|---|---|---|
| Clarification drift | "just to clarify, it should also…" | a clarification that adds behaviour is a `CR-CLARIFY`, estimated |
| Gold plating | the team adds a useful thing nobody asked for | PB-07 — it goes to the CR backlog |
| The demo request | a stakeholder asks during a demo, the developer says yes | note it, estimate it, decide it after the demo |
| Requirement interpretation | ambiguous text is implemented at the expensive reading | ambiguity is a question to the owner, not a decision by the implementer |
| Defect that is actually a change | reported as a bug, is really new behaviour | classify before fixing (`pm-quality`) |
| Absorbed small change | "it is only two hours" | record it as a CR even if approved instantly |

The last one is the important one. Small absorbed changes are individually reasonable,
collectively a schedule overrun, and invisible in every report — because nothing recorded
them. Recording a two-hour change costs five minutes and preserves the ability to explain
where four weeks went.

## SM-04 — Ambiguity is a question, never a decision

When a requirement can be read two ways, the implementer does not pick the sensible one.
The ambiguity is raised to `{{profile.scope.requirements.owner}}`, with both readings and
what each implies in effort and behaviour.

Meanwhile do the work that does not depend on the answer, and register an `ASM-*` if
progress requires provisionally assuming one reading — labelled, owned and dated.

The reading that looks less sensible is frequently the one with a regulatory or contractual
reason behind it, known only to the person you did not ask.

## SM-05 — Verification and validation are different meetings

| | Question | Who | When |
|---|---|---|---|
| **Scope verification** | does the deliverable meet its stated acceptance criteria | client, formally | at each deliverable / milestone |
| **Scope validation** | does it actually solve the business problem | sponsor and users | at UAT and at closing |

A deliverable can pass verification and fail validation — it is exactly what was specified,
and it does not help. That is a requirements defect, and its cost is why CH-02 insists on
measurable objectives. Verification protects the delivery team; validation protects the
project.

Record every verification with: what was checked, against which criteria, by whom, on what
date, and the verdict. That record is the acceptance evidence at closing (`pm-closure`).

## SM-06 — Acceptance criteria are written before the work starts

Every deliverable in `{{profile.scope.deliverables}}` has acceptance criteria that are
objective, checkable, and agreed with `acceptance_by` **before** it is built.

Criteria written at delivery time are negotiated under pressure by the party with more
leverage. Criteria written at planning time are the specification the team can aim at.

Good acceptance criteria answer: what will be checked, on which environment, with what data,
by whom, and what constitutes a pass. "Client is satisfied" is not a criterion.

## SM-07 — Out of scope with a reason, restated in every change assessment

`{{profile.scope.out_of_scope}}` entries each carry a reason. Every change request impact
assessment quotes the relevant exclusions.

An exclusion with no reason gets re-litigated monthly by whoever forgot the discussion. An
exclusion with a reason gets accepted once — and when it is re-raised, the conversation
starts from why, not from whether.

---

## Working with the technical pack

| Technical pack installed | This skill does |
|---|---|
| `sdlc` | cite `sdlc-requirements` artifacts; own the RTM's management columns (work package, milestone, acceptance) |
| `migration` | cite the legacy-derived requirement set; own scope boundaries for what is *not* being migrated — the highest-risk column in a migration |
| none | own the requirement register itself, applying SM-01 to every row |

In a migration, the scope statement's most valuable section is the list of legacy behaviour
being **dropped**, each with the decision that dropped it. It is the section nobody writes
and everybody needs at UAT.

---

## Exit criteria

- [ ] Scope statement approved by `{{profile.governance.approvals.scope_baseline}}`
- [ ] Every deliverable has objective acceptance criteria and a named acceptor (SM-06)
- [ ] Every out-of-scope item has a reason (SM-07)
- [ ] Every requirement is testable, atomic, sourced and owned (SM-01)
- [ ] RTM complete: no requirement without a work package, no work package without a
      requirement, no requirement without a verifying test (SM-02)
- [ ] WBS and WBS dictionary exist and cover every deliverable (PB-02)
- [ ] Scope baseline registered as baselined

Then: `/pm-wbs` if not yet done, else `/pm-estimate`.
