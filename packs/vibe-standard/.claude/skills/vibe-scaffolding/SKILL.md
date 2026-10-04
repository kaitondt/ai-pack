---
name: vibe-scaffolding
description: "Start a vibe-coded codebase right: choose a boring, well-documented stack, create the skeleton, and wire lint, format, typecheck, test, .gitignore and .env.example from the first commit. Use for a new project, 'set up the repo', 'which stack should I use', or when an existing prototype has no tests/lint and is about to become an mvp."
---

# Scaffold — The First Commit

> `sdlc-standard` scaffolds from an approved architecture document. A vibe project has no
> architecture document, so the stack choice is a recorded decision instead, and the
> scaffold's job is narrower: make the right thing the easy thing from commit one. Lint,
> typecheck and a test runner added on day one cost minutes; added at mvp they cost a week of
> fixing everything they find.

Load `vibe-project` first.

---

## SF-01 — Choose boring

The AI writes better code, invents fewer APIs, and debugs faster in stacks with a lot of
public, recent examples. Prefer, in order:

1. What the human already knows and can review
2. One mainstream full-stack framework over a hand-assembled set of libraries
3. Managed services for the hard, security-sensitive parts: **auth**, payments, email, file
   storage — writing these by prompt is where vibe-coded apps leak
4. A typed language (TypeScript, typed Python) — the type checker is a free reviewer
5. SQLite or a managed Postgres; not a database the project has no reason for

Record the choice as `DEC-001` (stack) with the options rejected. Fill `{{profile.stack}}`.

## SF-02 — The skeleton contains

| Item | Why |
|---|---|
| Framework's own generator output (`create-next-app`, `uv init`, …) | a known-good baseline beats a generated one |
| `.gitignore` covering `.env*` (except `.env.example`), build output, OS files | SB-01 |
| `.env.example` with every variable name, no values | the next session knows what exists |
| Formatter + linter configured, one command each | diffs stay reviewable (VT-02) |
| Typechecker in strict mode | catches the invented-API class of error (VT-03) |
| Test runner with **one** passing test | the second test is easy; the first is where it gets skipped |
| `README.md`: what, how to run, how to test | for the human, and for the next session |
| `vibe/` with PRODUCT.md, STATE.md and the four logs | the project's memory (SC-01) |
| Lockfile committed; versions pinned | reproducible installs, VT-03 |

Fill `{{profile.commands}}` with the **real** commands and run each one once. A command that
has never been run is a guess (VT-06).

## SF-03 — From stage mvp, also

- CI running install → typecheck → lint → test → build on every push
- dependency audit command (`{{profile.commands.audit}}`) in CI
- error tracking and an uptime check on the deployed environment
- database migrations as files, applied by a command, never by hand

`/vibe-graduate mvp` checks these.

## SF-04 — Adopting the pack on an existing vibe-coded repo

Common: a prototype already exists, built without any of this. Do not rewrite it.

1. Inventory: what runs, what the commands actually are, what has tests.
2. Write PRODUCT.md from what the app does now and what the human says it should do.
3. Write one intent per **existing** feature, status `done`, with the done-when checks it
   *should* meet. Run them. Those that fail are `BUG-*`s; nothing is fixed yet.
4. Record the shortcuts you can see — hardcoded values, missing auth checks, no tests — as
   `DEBT-*`. Expect many; that is the point (DL-06).
5. Add lint/typecheck/test tooling as its own slice (SS-07). Do not fix everything they report
   in the same slice — record the count as a debt and pay it down.
6. Set the stage honestly. Real users → `mvp`, whatever the code quality.

## Self-check

- [ ] Stack recorded as a `DEC-*` with rejected options
- [ ] Every command in the profile has been run once and works
- [ ] `.env*` ignored; `.env.example` committed; no secret in the first commit
- [ ] Formatter, linter, typechecker, test runner each run clean
- [ ] `vibe/` exists with PRODUCT.md, STATE.md and the logs
