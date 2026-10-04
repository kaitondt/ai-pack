---
name: sdlc-discovery
description: "P0 — inception and discovery. Stakeholder map, scope statement, business requirements (BR-*), glossary, decision log, assumption log, risk register, and the as-is process model. Produces the anchors every later phase cites. Load for ALL scoping, elicitation and discovery tasks."
---

# P0 — Inception & Discovery

> Prerequisite: `sdlc-project` loaded.
> This phase exists to create the **anchors**. A migration project reads them off the
> legacy source; a development project has to elicit them, and an unelicited answer
> becomes an invented one three phases later (RS-01).

---

## What P0 must produce

| Artifact | Path | Why it is load-bearing |
|---|---|---|
| Scope statement | `{{profile.paths.inception}}/scope.md` | the only defence against scope creep (RS-06) |
| Stakeholder map | `{{profile.paths.inception}}/stakeholders.md` | every decision needs a named owner |
| Business requirements | `{{profile.paths.inception}}/business-requirements.md` | the `BR-*` ancestors of every `REQ-*` |
| As-is process model | `{{profile.paths.inception}}/as-is-process.md` | what people actually do today |
| Glossary | `{{profile.paths.glossary}}` | one term, one meaning, project-wide |
| Decision log | `{{profile.paths.decision_log}}` | `DEC-*`, append-only (BL-05) |
| Assumption log | `{{profile.paths.assumption_log}}` | `ASM-*` with owners and due dates |
| Risk register | `{{profile.paths.risk_register}}` | `RSK-*` with likelihood, impact, response |
| Elicitation records | `{{profile.paths.inception}}/elicitation/` | dated, attributed, citable |

---

## Elicitation method

### E-01 — Start from the process, not the screens

Ask what people do, in what order, with what, and what goes wrong. Screens are a solution
shape; if you elicit screens you will faithfully reproduce a workflow nobody defended.

For each business process capture: trigger, actors, steps, decisions, exceptions,
volumes, timing, and the hand-offs to other systems or teams.

### E-02 — Ask for the exception before the happy path

Everyone can describe the normal case, and the normal case is 20% of the specification.
The expensive requirements live in: what happens when it is rejected, cancelled, partially
delivered, late, duplicated, or arrives after month-end close.

### E-03 — Numbers, not adjectives

Every "a lot", "quickly", "sometimes" is converted at the time of asking:
how many per day, at peak? within how many seconds? in what percentage of cases?
An adjective that survives P0 becomes an untestable NFR at P1 (RS-07).

### E-04 — Record and confirm

Every session produces a dated record with attendees, questions, answers, and the
decisions extracted. Send it back for confirmation. Silence is not confirmation — the
item stays an `ASM-*` until someone says yes (RS-08).

### E-05 — Separate what they asked for from what they need

Record the stated request **and** the underlying problem, as two fields. A request is a
proposed solution; the requirement is the problem behind it. When the solution turns out
to be expensive, the problem is what lets you propose an alternative.

### E-06 — Ask what already exists

Existing spreadsheets, workarounds, shadow systems and manual registers are specifications
that have already been debugged by their users. They also carry the business rules nobody
remembers stating.

---

## Scope statement

| § | Content |
|---|---|
| 1 | Business objective — what changes for the organisation, measurably |
| 2 | In scope — from `{{profile.scope.in_scope}}`, expanded per capability |
| 3 | Out of scope — every item with a **reason** (`{{profile.scope.out_of_scope}}`) |
| 4 | External systems and their owners (`{{profile.scope.external_systems}}`) |
| 5 | Users and volumes — roles, counts, geography, languages |
| 6 | Constraints — regulatory, contractual, technical, schedule, budget |
| 7 | Success criteria — how the client will judge the delivery |
| 8 | Open Items (DS-10) |

**The out-of-scope section is the most valuable page in the project.** An exclusion with
no reason gets re-litigated every month; an exclusion with a reason gets accepted once.

---

## Business requirements (`BR-*`)

| ID | Business requirement | Owner | Priority | Source | Success measure |
|---|---|---|---|---|---|
| `BR-ORD-002` | Orders over the credit limit must not reach fulfilment | business owner | Must | 2026/02/18 workshop | zero over-limit shipments |

Rules:
- Business language only. No screens, no fields, no technology.
- One requirement per row, with an owner from `{{profile.stakeholders}}`.
- Priority is `Must / Should / Could / Won't` and the **Won't rows are kept** — they are
  the record of what was consciously dropped.
- Every row names its source. A `BR-*` without a source is an assumption (RS-02).

---

## Glossary

One row per term: the term, its definition, its synonyms **and which of them is banned**,
and the owner of the definition.

The glossary is not documentation garnish. When "order", "job" and "ticket" are used for
the same thing by three stakeholders, every later document inherits the ambiguity, and the
test cases inherit it last — where it becomes a defect.

---

## Decision log (`DEC-*`) — append-only

| ID | Question | Options considered | Decision | Owner | Date | Affects |
|---|---|---|---|---|---|---|

- Appended, never edited into a new meaning.
- A reversal is a **new** entry superseding the old one by ID (BL-05).
- Every entry names what it affects, so a reversal has a blast radius.

## Assumption log (`ASM-*`)

Per RS-02: statement, why needed, owner, confirm-by date, impact if wrong, status.
Review it at every gate. An assumption that has been "open" for two months is a decision
nobody wants to make — escalate it rather than carrying it further.

## Risk register (`RSK-*`)

| ID | Risk | Likelihood | Impact | Response | Owner | Trigger |
|---|---|---|---|---|---|---|

Response is one of avoid / mitigate / transfer / accept, and each response names a
concrete action. "Monitor" is not a response.

The risks worth writing down early, in almost every project: an external interface not yet
specified, a data volume nobody has measured, an unavailable stakeholder, a dependency on
a team with its own schedule, and a non-functional target nobody has tested for feasibility.

---

## Exit gate

- [ ] Scope in/out documented; every exclusion has a reason
- [ ] Stakeholder map complete; every `{{profile.stakeholders}}` role filled
- [ ] Every `BR-*` has an owner, a priority and a source
- [ ] Glossary covers every term used in more than one sense
- [ ] Decision, assumption and risk logs exist and are populated
- [ ] `{{profile.gates.P0_inception.exit}}` assertions hold

Then run `/sdlc-phase-gate P0`.
