---
name: pm_charter
description: "Project charter and project overview — the document that authorises the project, names the PM's authority, states measurable objectives and success criteria, and fixes the high-level scope, milestones, budget envelope, assumptions and constraints. Load for ALL charter, kickoff, business-case and project-overview tasks."
---

# Project Charter (Project Overview)

> Prerequisite: `pm_project` loaded.

The charter does one job: it **authorises the project and the project manager**. Everything
else in it — objectives, scope outline, budget envelope — exists so that the authorisation
is specific enough to be enforceable.

A project without a signed charter has no agreed definition of success, which means it
cannot fail visibly. It also means the PM has responsibility without authority, discovered
the first time they need a resource someone else controls.

---

## What the charter is, and is not

| The charter | Not the charter |
|---|---|
| authorises the project and names the PM's authority | the detailed plan |
| states measurable objectives and success criteria | the requirements |
| outlines scope boundaries | the WBS |
| gives the budget envelope and its tolerance | the cost baseline |
| names milestones as commitments | the schedule |
| identifies high-level risks | the risk register |
| is signed by the sponsor | signed by the delivery team |

It is short — typically 3 to 6 pages. A twenty-page charter is a plan wearing a charter's
title, and it will be out of date before it is signed.

---

## Structure

| § | Section | Content |
|---|---|---|
| 1 | Purpose and business case | the problem, its cost today, why now, what happens if the project is not done |
| 2 | Objectives | measurable, dated, each with a metric and a baseline value (CH-02) |
| 3 | Success criteria | how the sponsor will judge the delivery, objectively |
| 4 | Scope outline | in scope; out of scope with reasons; boundaries against neighbouring systems |
| 5 | Key deliverables | `D-*` with the milestone each is due at |
| 6 | Milestones | `M*` from `{{profile.schedule.milestones}}`, with which are payment-linked |
| 7 | Budget envelope | order of magnitude, its estimating stage and tolerance (ES-03) |
| 8 | Stakeholders | from `{{profile.governance}}`, with what each one decides |
| 9 | PM authority | staffing, spend, technical decisions, escalation — stated explicitly (CH-03) |
| 10 | High-level risks | the 5–10 that could stop the project, with initial responses |
| 11 | Assumptions | `ASM-*` with owners and confirm-by dates |
| 12 | Constraints | schedule, budget, regulatory, technology, resource, contractual |
| 13 | Dependencies | `DEP-*` on other projects, teams, vendors or client actions |
| 14 | Approval | signatures from `{{profile.governance.approvals.charter}}` |

Plus the standard skeleton from `rules/pm/document-standards.md` (MD-01).

---

## CH-01 — The charter is written from the sponsor's problem, not the vendor's solution

Section 1 describes what is wrong today, in the business's own terms and numbers: how long
the process takes, how many people it occupies, what it costs, what it prevents.

A charter that opens with the technology chosen has skipped the step where anyone agreed
what problem was being solved — and every scope argument later in the project traces back
to that missing paragraph.

## CH-02 — Objectives are measurable, dated, and have a baseline value

Each objective states: the metric, today's value, the target value, and the date by which
it must hold.

| Bad | Good |
|---|---|
| "Improve order processing efficiency" | "Reduce average order entry time from 14 min to under 5 min by 2026/09/30, measured by the system's own timestamps" |
| "Modernise the platform" | "Run on supported infrastructure with no component past end-of-life by 2026/12/31" |
| "Improve user satisfaction" | "Raise the internal user survey from 3.1 to 4.0 within 3 months of go-live" |

An objective with no measurement is a sentiment, and it will be claimed as achieved by one
side and denied by the other at closing. If today's value is unknown, that is the first
action item — measure it before baselining, or record it as an `ASM-*`.

**Objectives are not requirements.** "Reduce order entry time" is an objective; "the screen
shall default the warehouse from the user profile" is a requirement that serves it. Keep
the charter at the first level.

## CH-03 — The PM's authority is stated, not assumed

Write the answers, explicitly:

- who the PM can assign, and who they must request
- how much they may commit without approval, and to whom above that
- which technical decisions they own and which belong to the architect or the client
- what they may change without a CR (nothing baselined — PB-03)
- the escalation path and its SLA (`{{profile.governance.escalation}}`)

An unstated authority is discovered in week three, during an argument, and resolved
slowly. This is the section teams skip because it feels bureaucratic; it is the section
that makes the rest of the charter operable.

## CH-04 — Success criteria are the acceptance conversation, held early

Section 3 is a rehearsal of the closing meeting. Write what the sponsor will actually check,
and make it objective enough that two people reading it reach the same verdict.

Include the negative form where it clarifies: what would make this project a failure even if
every deliverable ships. Usually it is something like "the operations team still needs the
old system", and that sentence is worth more than the rest of the section.

## CH-05 — The budget envelope carries its estimating stage

Give the number, the method (`{{profile.cost.estimation_methods}}`), and the accuracy for
that stage per ES-03 — pre-charter is −25% to +75%, and saying so is the difference between
an envelope and a promise.

State what the envelope excludes: licences, client-side effort, infrastructure, post-warranty
support, third-party fees. An exclusion missed here is a cost argument at invoicing.

## CH-06 — High-level risks are the ones that could stop the project

Not a generic list. Five to ten items that would materially change whether the project
succeeds, each with an initial response and an owner. Typical, and worth checking against:

an unavailable decision-maker · an external interface not yet specified · a data volume or
quality nobody has measured · a regulatory deadline outside the project's control · a
dependency on a team with its own schedule · a technology nobody in the team has used · a
client-side resource commitment that has not been secured.

These seed the risk register (`pm_risk`), which then owns them.

## CH-07 — Charter changes are change requests

Once approved, the charter is baselined. Objectives, success criteria, envelope and
milestones change only through change control (PB-03), at the authority level for that
impact — usually the steering committee, since a charter change is by definition
significant.

A project whose charter no longer describes what is being built has already lost the ability
to say whether it is succeeding.

---

## Kickoff

Once approved, the charter is presented — not emailed. The kickoff establishes, in one
session: what the project is for, who decides what, how status will be reported, how changes
will be handled, and what everyone in the room is accountable for.

Record it as a meeting (`MTG-*`) with attendees, decisions taken (`DEC-*`) and actions
(`ACT-*`). The kickoff is where the communication plan (`pm_stakeholder`) becomes real, and
where the first misunderstandings surface cheaply.

---

## Exit criteria

- [ ] Every objective has a metric, a baseline value, a target and a date (CH-02)
- [ ] Success criteria are objective enough for two readers to agree on the verdict
- [ ] Out-of-scope items each have a reason
- [ ] The PM's authority is written (CH-03)
- [ ] Budget envelope states its stage and its exclusions (CH-05)
- [ ] Every high-level risk has an owner and an initial response
- [ ] Every assumption is an `ASM-*` with an owner and a confirm-by date
- [ ] Approved by everyone in `{{profile.governance.approvals.charter}}`, recorded with dates
- [ ] Registered as baselined; the baseline register is updated

Then: `/pm_scope_baseline`.
