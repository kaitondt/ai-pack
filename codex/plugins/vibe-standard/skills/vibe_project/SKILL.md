---
name: vibe_project
description: "Vibe coding spine — loads vibe.profile.yaml, resolves {{profile.*}} tokens, applies the rules in force for the project's stage (spike / prototype / mvp / production), and routes to the right vibe skill. Load this FIRST for ANY task in a vibe-coded project: building a feature, fixing a bug, planning, reviewing, shipping, or resuming a session."
---

# Vibe Coding — Spine Skill

> **Load this skill first for every task in this project.**
> Every other `vibe_*` skill assumes the profile is resolved and the stage is known.

Vibe coding: the human steers by intent, the AI writes most of the code, and the running
software is the evidence. This pack keeps that fast **and** keeps it from producing a pile
of plausible code nobody understands. It does that with five invariants, a stage model that
tightens them as the project matters more, and one loop.

---

## Step 1 — Load the profile (mandatory)

Read `.codex/vibe.profile.yaml`.

- **Missing** → stop. Tell the user to run `/vibe_init`.
- **Unreplaced placeholder** (`<...>`) in a field this task needs → ask for that field. At
  stage `spike` you may proceed with a stated guess; from `prototype` you may not.
- **`stage` missing or not one of the four** → stop. The rules in force depend on it.

Hold the resolved values for the whole task.

## Step 2 — Load the invariant rules

| Rule file | Enforces |
|---|---|
| `references/rules/vibe/intent-first.md` | every slice starts from a written intent with observable done-when checks; nothing outside it gets built |
| `references/rules/vibe/small-slices.md` | step size, checkpoints, the doom-loop limit, no drive-by refactors |
| `references/rules/vibe/verify-before-trust.md` | seen running or not done; no phantom packages/APIs; checks never bent to go green |
| `references/rules/vibe/security-baseline.md` | secrets, destructive ops, server-side trust, real data, prompt injection |
| `references/rules/vibe/debt-ledger.md` | every shortcut written down with a due stage |
| `references/rules/vibe/session-continuity.md` | STATE.md handoff, append-only logs, slice IDs in commits |
| `references/rules/vibe/id-naming.md` | `INT` `DEC` `DEBT` `BUG` `IDEA` |

## Step 3 — Read the project's memory

Before acting on anything non-trivial: `{{profile.paths.state}}`, then the intent the task
belongs to. If the task has no intent yet, the first job is to write one (`vibe_intent_spec`).

## Step 4 — Route

| The task is about | Load |
|---|---|
| What the product is; PRODUCT.md; turning an idea into intents | `vibe_intent_spec` |
| Breaking an intent into slices; ordering; "how long" | `vibe_slicing` |
| Starting a new codebase; choosing the stack; setting up lint/test/format | `vibe_scaffolding` |
| Building a slice | `vibe_build_loop` (+ `vibe_verification` to finish it) |
| Running checks, proving a slice works, writing tests | `vibe_verification` |
| Reviewing a diff, a slice, or the whole codebase | `vibe_code_review` |
| Something is broken; the AI keeps failing to fix it | `vibe_debug` |
| Secrets, auth, input handling, dependencies, data | `vibe_security` |
| Shortcuts, TODOs, refactoring, paying debt | `vibe_debt_ledger` |
| Deploying, releasing, rolling back | `vibe_release` |
| Moving to the next stage; handing over to `sdlc-standard` / `pm-standard` | `vibe_graduation` |
| Starting or ending a session; status; "where were we?" | `vibe_session` |

---

## The five invariants

These hold at **every** stage, including `spike`:

1. **Intent before code.** A slice starts from a written intent (IF-01). Everything else is
   parked (IF-03).
2. **Small steps from a checkpoint.** Clean tree, size budget, three strikes then revert
   (SS-03, SS-02, SS-05).
3. **Seen running, or not done.** And reported exactly as it happened (VT-01, VT-06).
4. **No secrets in the code, no irreversible commands by the AI** (SB-01, SB-02).
5. **If it matters next session, it is in a file** (SC-04).

## The stage model

The stage is `{{profile.stage}}`. It is the answer to "how much does it matter if this is
wrong?" — and it decides which of the remaining rules are in force.

```
  spike ──────► prototype ──────► mvp ──────► production ──────► (graduate: sdlc / pm)
  answer a      show it to        real users   people depend on
  question      someone           use it       it
```

| | spike | prototype | mvp | production |
|---|---|---|---|---|
| **Purpose** | learn whether something is possible | get feedback on something clickable | first real users | users depend on it |
| **Lifespan** | hours–days, then deleted | weeks | months | open-ended |
| **Branch** | `spike/*`, never merged to `main` | `main` | `main` + PR from `small` teams | `main` + PR + CI green |
| **Intent** | one line + assumptions | full INT with done-when | full INT | full INT |
| **Verification (VT-08)** | done-when run once | + diff summary, build/lint/typecheck | + core flows automated, full suite, review, CI | + E2E smoke before release |
| **Security (SB-07)** | SB-01/02/06, synthetic data | + server-side authz if public URL | full baseline, audit in CI | + security check every release |
| **Debt ledger** | not required — the spike is the debt | required | required, paydown cadence | required, nothing overdue |
| **Session state** | optional | STATE.md | STATE.md | STATE.md + release notes |
| **Promotion** | `/vibe_graduate prototype` — spike code is **re-read and re-sliced**, never merged as-is | `/vibe_graduate mvp` | `/vibe_graduate production` | `/vibe_graduate handoff` |

Rules:

- **The stage only changes through `/vibe_graduate`**, which checks criteria and records a
  `DEC-*`. Editing the profile line is not a promotion.
- **Reality overrides the profile upward.** A prototype with a public URL gets mvp security.
  A prototype with real users is an mvp whether or not anyone graduated it — say so.
- **Spike code is evidence, not foundation.** What the spike learned goes into intents and
  decisions; the code enters the main branch only through normal slices.

## The vibe loop

Every piece of work in the pack is an instance of this loop:

```
  ┌─► INTENT ──► SLICE ──► CHECKPOINT ──► BUILD ──► RUN ──► VERIFY ──► REVIEW ──► COMMIT ──► LOG ─┐
  │   INT-*      INT-*.n   clean tree     map,     real    done-when  diff       INT-*.n:   STATE, │
  │              budget                   smallest output  checks     summary    …          DEC,   │
  │                                       change                                            DEBT   │
  │                             ▲                     │ fail ×{{profile.loop.max_fix_attempts}}    │
  │                             └─── revert to ◄──────┘ (SS-05) → /vibe_fix or /vibe_unstuck       │
  └────────────────────────────────────────────────────────────────────────────────────────────────┘
```

| Step | Command | Rule |
|---|---|---|
| Intent | `/vibe_intent` | IF-01, IF-02 |
| Slice | `/vibe_plan` | SS-01, SS-02 |
| Checkpoint → Commit | `/vibe_build` | SS-03, SS-04, SC-05 |
| Run → Verify | `/vibe_verify` | VT-01..VT-08 |
| Review | `/vibe_review` | VT-02, SB-*, DL-03 |
| Log | `/vibe_handoff` | SC-01, SC-03 |

---

## Standing behaviour in a vibe project

1. **Read STATE.md before starting** — and report when git disagrees with it (SC-02).
2. **Restate the intent and the slice before the first edit.** One line each. The human can
   stop a misunderstanding in five seconds here, or an hour later in the diff.
3. **Build the smallest thing that satisfies the slice's done-when.** Not the general version,
   not the configurable version, not the one with the extra endpoint.
4. **Use the stack in the profile.** A new framework, library or service is a decision (IF-05)
   — propose it, do not install it.
5. **Park, don't build, the good idea you just had** (IF-03).
6. **Run it.** Then say what ran and what it showed.
7. **Three strikes, then stop** (SS-05).
8. **Ask before irreversible actions**, and do not run them yourself (SB-02).
9. **Write down what the next session needs** (SC-04).

---

## Reporting format

Slice done:
```
INT-007.2 — edit a note                                   stage: prototype
  Files      : 4 (budget 8) · +132 −18 lines (budget 400)
  Checks     : 3/3 done-when run — ✅ ✅ ✅
  Build/lint : ✅ / ✅      Tests: 12/12
  Not run    : none
  Debt       : +1 (DEBT-015, due mvp)      Parked: IDEA-024
  Commit     : a1b2c3d  "INT-007.2: edit a note"
  Next       : INT-007.3 — delete a note
```

A slice with any failing or unrun check is reported **not done**, with the failure output and
what happens next. Never "mostly done".
