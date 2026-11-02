# RULE FAMILY: INTENT FIRST

> The most important rule family in a vibe-coded project.
>
> A migration project has an oracle: the old system. A development project has an approved
> specification. **A vibe-coded project has neither** — only what the human meant, and the
> software that is running. The AI will happily build something plausible in the gap between
> the two. This rule family keeps the gap small by writing the meaning down *before* the code
> exists, in a form cheap enough that nobody skips it.
>
> Derived from `sdlc-standard` RS-01/RS-04/RS-06 and `pm-standard` PB-07/DA-03 — reduced to
> the part that survives at vibe speed.

## IF-01 — Every slice starts from a written intent

No code is written for a task that has no intent. An intent is an `INT-*` file in
`{{profile.paths.intents}}` with, at minimum:

| Field | Rule |
|---|---|
| **Intent** | one sentence, from the user's point of view: *"A visitor can …"*, *"The admin can …"* |
| **Done when** | 1–5 observable checks (IF-02) |
| **Not now** | what this intent deliberately does not do — at least one line |
| **Slices** | the ordered steps (`INT-{NNN}.1`, `INT-{NNN}.2`, …), filled by `/vibe-plan` |

Writing it takes two minutes. Not writing it costs the afternoon in which the AI builds the
feature you did not mean, well.

A request typed in chat ("add a login page") is **raw material** for an intent, not an intent.
`/vibe-build` turns it into one — showing it to the human before building — when none exists.

## IF-02 — "Done when" is observable, or it is not a check

A done-when check names something a person or a script can **see happen**:

| Not a check | A check |
|---|---|
| "Login works" | "Submitting a registered email + correct password lands on `/dashboard` and shows the user's name" |
| "It's fast" | "The list of 500 notes renders in under 1 s on the dev machine" |
| "Handles errors" | "A wrong password shows *Invalid email or password* and does not reveal which one was wrong" |
| "Looks good on mobile" | "At 375 px wide, no horizontal scroll and the submit button is visible without zoom" |

Every check must be runnable at verification (VT-01). From stage `mvp` onward, the checks on a
**core flow** (`{{profile.product.core_flows}}`) become automated tests (VT-08).

## IF-03 — Nothing enters the slice that is not in the intent

The useful little addition — the extra button, the "while I'm here" refactor, the dark mode
nobody asked for, the audit column, the retry wrapper — is **parked**, not built:

```
IDEA-{NNN}  Export notes as Markdown  ← noticed while building INT-{NNN}.2
```

It goes to `{{profile.paths.backlog}}` via `/vibe-park`, with one line of why. The human
decides whether it becomes an intent. The AI never does.

This applies to the AI's own suggestions most of all. An AI-proposed addition is still an
addition; it is simply one nobody asked for.

## IF-04 — Ambiguity stops the part that depends on it

When the intent does not say what should happen and the answer changes the code:

1. Say exactly what is undecided, and what the options imply.
2. Build everything in the slice that does **not** depend on the answer.
3. **Stop on the part that does, and ask.** Do not build both branches "to be safe", and do
   not pick the plausible one silently — a guess shipped is a decision nobody made.
4. Record the answer as a `DEC-*` (IF-05) if it outlives this slice.

At stage `spike`, a guess is allowed — but it is **written into the intent as an assumption**
("assumed: guests cannot comment"), so it is visible when the spike is read later.

## IF-05 — Decisions are recorded when they are made

A choice that constrains future work is appended to `{{profile.paths.decisions}}` as a `DEC-*`
the moment it is made:

- stack, framework, database, hosting, auth provider
- a data model shape other code will depend on
- adding a dependency that is not trivially replaceable
- a deliberate deviation from an intent or from a rule in this pack
- anything the human answered under IF-04 that later slices depend on

Format: `DEC-{NNN} · 2026-09-18 · <decision> · because <reason> · rejected: <options> · by <who>`.

The log is **append-only**. A reversal is a new entry that cites the old one. The chat
transcript is not a decision log — it is gone at the next session (SC-04).

## IF-06 — PRODUCT.md is the one-page answer to "what are we building?"

`{{profile.paths.product}}` holds, on one page:

- **Problem** — whose, and what it costs them today
- **User** — one or two named kinds of user, not "everyone"
- **Core flows** — the 3–7 things the product must do (these are `{{profile.product.core_flows}}`)
- **Not building** — the explicit non-goals
- **Constraints** — budget, deadline, platform, data, compliance

Every intent traces to a core flow or to a non-flow reason (infra, debt, security). A change
to PRODUCT.md is a decision (IF-05), not an edit.

## Self-check before building

- [ ] An `INT-*` exists, and the slice being built is one of its listed slices
- [ ] Every done-when check is observable and could be run today
- [ ] "Not now" has at least one line
- [ ] Nothing in the planned change is outside the intent — extras are parked as `IDEA-*`
- [ ] Every open question is either answered, or the dependent part is not being built
