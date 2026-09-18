---
description: "Create the codebase skeleton for a new vibe project — boring stack recorded as DEC-001, framework generator, lint/format/typecheck/test wired with one passing test, .gitignore and .env.example, real commands in the profile. Or retrofit that tooling onto an existing prototype. Usage: /vibe_scaffold [stack preference]"
---

# Scaffold

Load `vibe_project`, then `vibe_scaffold`.

## Step 1 — Decide the stack

Existing code → the stack is what is there; skip to step 3 (retrofit).

New → propose per SF-01, with one alternative and why not. Wait for a yes. Record `DEC-001`
with the options rejected.

## Step 2 — Generate

Use the framework's own generator, non-interactively, into the repo root. Verify the versions
it installed (VT-03) and write them into the `DEC-001` entry.

## Step 3 — Wire the tooling (SF-02)

Each item as it lands, run once:

`.gitignore` (`.env*`, `!.env.example`, build output, `.claude/.slice_warned`) → `.env.example`
→ formatter → linter → typechecker strict → test runner + one real passing test → README
(what / run / test).

Existing prototype: add the tooling **without fixing what it reports** in this slice; record
the counts as `DEBT-*` (SF-04 step 5).

At `mvp`+, also SF-03: CI, audit, migrations as files, error tracking.

## Step 4 — Fill the profile

`{{profile.stack}}` and `{{profile.commands}}` with the real values that just ran.

## Step 5 — Commit and report

Commit `INT-000: scaffold` (or `DEBT-*: add tooling` for a retrofit).

```
Scaffold — {stack}
  DEC-001    : {stack} (rejected: {options})
  Commands   : dev ✅ build ✅ typecheck ✅ lint ✅ test ✅ (1 test)
  Security   : .env* ignored ✅ · .env.example ✅ · no secret in commit ✅
  Retrofit   : {lint errors n · type errors n → DEBT-*}   (existing repos only)
  Next       : /vibe_intent for core flow 1
```
