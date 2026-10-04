# RULE FAMILY: SESSION CONTINUITY

> In vibe coding the "team" changes at every session: a new context window knows nothing the
> previous one did not write to disk. Most of the confusion in a vibe-coded project — the
> feature built twice, the decision reversed by accident, the bug "fixed" again the way that
> did not work last week — is a handoff failure. This rule family makes the handoff a file.
>
> Derived from `pm-standard` DA-03 (a decision recorded when made, or it did not happen) and
> its reporting-integrity rules, sized for one person and an AI.

## SC-01 — STATE.md is the handoff

`{{profile.paths.state}}` is the single page a new session reads first. It holds, and only
holds:

| Section | Content |
|---|---|
| **Stage** | current stage, and the next one with its blocking items |
| **Now** | the active intent and slice, and exactly where it stopped |
| **Next** | the next 1–3 slices, in order |
| **Broken** | what is known not to work right now — honestly |
| **Open questions** | IF-04 questions waiting on the human, with the date asked |
| **Recently decided** | the last few `DEC-*` ids with one line each |
| **Last verified** | date, commit and which checks ran green |

It is rewritten — not appended — at the end of every slice and every session. It is short
enough to read in one minute; history lives in git and the logs, not here.

## SC-02 — A session starts by reading, not by building

Before the first edit of a session:

1. Read `STATE.md`.
2. `git status` and `git log --oneline -10` — does the tree match what STATE.md says?
3. If they disagree (uncommitted changes nobody mentioned, commits after the last STATE.md
   update), **report the discrepancy first**. Something happened that the handoff missed.

`/vibe-resume` does this. The `check-vibe-profile` hook prints STATE.md at session start so
the first message already has it.

## SC-03 — The logs are append-only

`decisions.md`, `debt.md`, `bugs.md`, `backlog.md` are appended to, never rewritten. A reversed
decision is a new `DEC-*` citing the old one; a closed debt keeps its row with its status
changed. Editing history makes the log unreliable exactly when it is needed — when someone asks
"why is it like this?".

## SC-04 — The conversation is not memory

Anything that must be true in the next session goes into a file **before this session ends**:
the decision into `decisions.md`, the shortcut into `debt.md`, the idea into `backlog.md`, the
convention into `CLAUDE.md` (project-specific section), the state into `STATE.md`.

"As we discussed" is not a reference. If it was not written down, the next session did not
discuss it.

## SC-05 — Commits carry the slice ID

Every commit message starts with the slice ID it implements: `INT-007.2: edit a note`.
Paydowns: `DEBT-014: move notes to Postgres`. Fixes: `BUG-009: …`. This is the whole
traceability chain of a vibe project — intent → slice → commit → check — and it costs nothing
if done at commit time.

## SC-06 — Conventions learned are written where the next session will read them

When the human corrects the AI's approach in a way that should hold for the whole project
("always use server actions, not API routes", "no new UI libraries"), it goes into the
project-specific section of `CLAUDE.md`. A correction given twice is a missing convention.

## Self-check before ending a session

- [ ] `STATE.md` rewritten: Now, Next, Broken, Open questions, Last verified
- [ ] Every decision made this session is a `DEC-*`
- [ ] Every shortcut is a `DEBT-*`; every parked idea an `IDEA-*`
- [ ] Working tree is clean, or STATE.md says exactly what is uncommitted and why
- [ ] Corrections that should outlive the session are in `CLAUDE.md`
