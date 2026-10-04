---
description: "Prove the current slice, an intent, or the whole app works — run done-when checks by observation, then the stage's typecheck/lint/test/build/e2e, report exactly what ran. Delegates to vibe-verifier. Usage: /vibe-verify [INT-NNN.n | INT-NNN | all]"
---

# Verify

Load `vibe-project`, then `vibe-verification`.

## Step 1 — Scope

| Argument | Checks |
|---|---|
| none | the active slice from STATE.md "Now" |
| `INT-NNN.n` | that slice's done-when checks |
| `INT-NNN` | every check of the intent |
| `all` | every check of every `done` intent — a regression sweep; slow, run before graduation and release |

## Step 2 — Run

Delegate to `vibe-verifier`. It starts the app with `{{profile.commands.dev}}` where needed,
observes each check (VE-01), runs the stage commands (VE-02) and the AI-specific checks
(VE-05), and edits **no source code**.

## Step 3 — Record

- Failing checks on a `done` intent → a `BUG-*` each (DB-01): something that used to work
  does not.
- STATE.md "Last verified" updated only with what ran green.
- `all`: write the result to `{{profile.paths.reviews}}/<date>-verify-all.md`.

## Step 4 — Report

The VE-06 format. Verdict **DONE** only if every check is ✅. Otherwise **NOT DONE**, with the
failure output and the next command (`/vibe-build` to continue, `/vibe-fix BUG-*` for
regressions).
