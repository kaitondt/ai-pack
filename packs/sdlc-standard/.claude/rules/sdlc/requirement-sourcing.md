# RULE FAMILY: REQUIREMENT SOURCING

> The most important rule family in a development project. Everything else in the pack
> exists to make it checkable.
>
> A migration project has an oracle: the old system. A development project does not.
> Its only oracle is what stakeholders decided, written down. Anything not written down
> was not decided — it was assumed by whoever wrote it, silently, and it will be
> discovered at UAT.

## RS-01 — Every specification statement has a source

Any requirement, rule, field, message, default, validation, sort order, threshold or
error case written into a deliverable MUST carry one of:

| Anchor | Form | Example |
|---|---|---|
| An approved requirement | `REQ-*` / `BR-*` / `NFR-*` | `← REQ-{AREA}-{NNN}` |
| A recorded decision | `DEC-*` in `{{profile.paths.decision_log}}` | `← DEC-{NNN} (2026/03/04, product owner)` |
| An elicitation record | interview / workshop note, dated, with attendees | `← docs/00.inception/elicitation/2026-02-18-ops.md` |
| An external obligation | law, standard, contract, external interface spec | `← ISO 8601 §4.3` / `← <external system> IF spec v2.1` |

If none of the four says anything, it is an **OPEN QUESTION**. Raise it, own it, date it.
Do **not** fill the hole with "reasonable", "industry standard", "what users would expect",
or a value copied from another project.

**Anchor format** — every non-obvious statement carries its anchor inline:

```
An order over the credit limit is rejected before it reaches approval.
  ← REQ-{AREA}-{NNN} · DEC-{NNN} (credit check runs pre-approval, product owner, 2026/03/04)
```

## RS-02 — An assumption is a labelled, owned, dated object

Sometimes work must proceed before an answer arrives. That is normal. What is not normal
is an assumption that looks like a fact.

Every assumption becomes an `ASM-*` row in `{{profile.paths.assumption_log}}`:

| Field | Rule |
|---|---|
| Statement | what is being assumed, in one testable sentence |
| Why needed | which deliverable is blocked without it |
| Owner | a named person from `{{profile.stakeholders}}` — never "the team" |
| Confirm by | a date, not "ASAP" |
| Impact if wrong | what has to be redone |
| Status | open / confirmed / rejected |

Rules:
- An assumption is referenced by its ID in the deliverable, never inlined as prose fact.
- An **unconfirmed assumption cannot pass a gate that depends on it.** The gate report
  lists it by ID.
- A rejected assumption triggers the rework named in "Impact if wrong". Silently
  editing the document is not closure.

## RS-03 — TBD is a status, not a blank

A field whose value is not yet decided is written `TBD (ASM-{NNN}, due 2026/03/20)`.
It is never left blank, never filled with a placeholder value that reads as real
(`999`, `0`, `dummy@example.com`), and never quietly resolved by picking something
plausible.

A deliverable may be reviewed with TBDs in it. It may not be **baselined** with them.

## RS-04 — An undecided requirement stops the design (blocking)

When a requirement needed for the work in hand is in status `proposed`, `TBD`, or
`under discussion`:

1. Say which requirement, and what specifically is undecided.
2. Do everything in the current task that does **not** depend on it.
3. **Stop on the part that does, and ask.** Do not design both branches speculatively
   "to be safe" — two designs to review is worse than one question to answer.
4. Record the answer as a `DEC-*` before continuing.

Designing against an undecided requirement produces a document that looks approved and
is not. That is more expensive than the delay.

## RS-05 — Conflicts are reported, not arbitrated

When two stakeholders, or a requirement and a constraint, or the SRS and an external
interface spec disagree: state both positions with their anchors, state what each implies
for the design, and ask the owner named in `{{profile.stakeholders}}` to decide.

Do not pick the more sensible one. The one that looks less sensible is frequently the one
with the regulatory or contractual reason behind it.

## RS-06 — Nothing enters scope without passing through a requirement

A capability that is not traceable to a baselined `REQ-*` is out of scope, however small
and however obviously useful. It goes to the change-request backlog with a one-line
rationale — not into the design, not into the code, not into a "while I was there".

This applies to the helpful additions most likely to slip in unremarked: an extra export
button, a sort the user did not ask for, a validation that "obviously should be there", an
audit column, a soft-delete flag.

## RS-07 — Non-functional requirements are stated measurably

An `NFR-*` without a number and a measurement method is not a requirement; it is a mood.

| Not a requirement | A requirement |
|---|---|
| "The system must be fast" | "Order search returns within 2.0 s at p95, 50 concurrent users, 5M-row order table — measured by the ST performance script" |
| "The system must be secure" | "All endpoints require an authenticated session; authorisation asserted server-side per operation; verified by ST-SEC-{NNN}..{NNN}" |
| "The system must be available" | "99.5% monthly availability excluding the announced maintenance window; measured by the platform health probe" |

Every NFR states: **target · condition · measurement method · phase that verifies it**.
The measurement method is what makes it a gate item at P7 instead of an argument.

## RS-08 — Elicitation is recorded, not remembered

Every workshop, interview, demo or clarification call produces a dated record with
attendees, questions asked, answers given, and the decisions extracted (`DEC-*`). A verbal
answer that exists only in someone's memory is not an anchor and cannot be cited by RS-01.

Send the record to the stakeholder for confirmation. Silence is not confirmation; note it
as `unconfirmed` and it stays an assumption (RS-02).

## Self-check before finishing any P0–P3 deliverable

- [ ] Every behavioural statement has an anchor, or sits under **Open Items**
- [ ] Every assumption is an `ASM-*` with an owner and a confirm-by date
- [ ] No TBD that reads as a real value; no invented default
- [ ] No capability without a `REQ-*` ancestor
- [ ] Every NFR has a target, a condition and a measurement method
- [ ] Conflicts reported with both sides, not silently resolved
