---
description: "P5–P8 — generate test case documents at one level, through the checkpoint pipeline with its human pauses. Usage: /sdlc-generate-test <ut|it|st|uat> <MODULE | FLOW | SCENARIO>"
---

# Generate test cases

## Step 1 — Resolve the level

The first argument selects the level and therefore the basis document
(`{{profile.testing.levels}}`):

| Level | Verifies | Skill | Keyed by |
|---|---|---|---|
| `ut` | detail design | `sdlc-test-ut` | module |
| `it` | basic design | `sdlc-test-it` | flow / interface |
| `st` | requirements | `sdlc-test-st` | business scenario |
| `uat` | business need | `sdlc-test-uat` | client scenario |

No level given → ask. Do not default to `ut`; the levels are not interchangeable and a case
set written at the wrong level is coverage that has to be redone.

## Step 2 — Load

`sdlc-project`, then `sdlc-test-design`, then the level skill.

## Step 3 — Pre-check

The basis document must exist and, for a final case set, be baselined. Missing → say which
and stop. Not yet baselined → proceed, and mark the output provisional.

Also check the previous level's exit: writing IT cases while UT is still failing means
triaging IT failures that UT would have explained.

## Step 4 — Run the pipeline

Per the level skill, with the pauses from `{{profile.testing.pipeline.human_pauses}}`:

```
sources + analysis + questions  ──▶ ⏸ human answers
final analysis ──▶ checklist ──▶ ⏸ human reviews coverage
write cases ──▶ bounded self-review ──▶ done
```

**Stop at each pause.** The pauses are the review the pipeline exists to buy; skipping one
produces a case set that is complete-looking and wrong in a way nobody checked. Every step
writes a timestamped checkpoint file and deletes nothing.

Delegate the writing to `sdlc-tester`, one call per module / flow / scenario.

## Step 5 — Coverage check

Run the checks for this level: T-01/T-02 (UT), T-03/T-04 (IT), T-05/T-06 (ST), T-07 (UAT),
plus T-08..T-10 always.

## Step 6 — Report

```
{LEVEL} — {target}
  Basis            : {document}   baselined: {yes|no}
  Sources          : {found}/{required}   missing: {list}
  Questions        : {n} open, {n} rare — all answered: {yes|no}
  Checklist        : {n} cases   reviewed by human: {yes|no}
  Written          : {n} cases   file: {path}
  Self-review      : round {n}/{max} — {PASS|FAIL}
  Coverage         : {the checks for this level, pass/fail each}
  Unanchored expectations : {n}      ← TR-AN01
  Result columns empty    : {yes|no}
```

A case set delivered with result columns filled in cannot be distinguished from one where
execution was skipped. Leave them empty.
