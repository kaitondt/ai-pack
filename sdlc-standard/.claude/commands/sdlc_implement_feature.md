---
description: "P4 — implement one module or feature across all layers, design-first, with the context map, build verification and unit tests. Usage: /sdlc_implement_feature MODULE"
---

# P4 — Implement a feature

## Step 1 — Load

`sdlc_project`, then `sdlc_context_map`, then `sdlc_implementation`.

## Step 2 — Pre-check

Required: approved SC / FC / API / DT and DD for the module, and passed P2/P3 gates for it.
Missing → name the command that produces it and stop.

A module implemented against a missing DD produces code that is its own specification, and
the P5 tests will be written from the code (`rules/common/testing.md`).

## Step 3 — Read, then reconcile

Read the design documents and, where the module touches existing code, that code. Where the
documents disagree with each other, raise it now — do not resolve it silently in the
implementation.

## Step 4 — Emit the context map

Print it before writing any code. Every file the change touches, by layer, with the design
documents that must change first if anything changes.

## Step 5 — Implement

Delegate to `sdlc_implementer`. Inner layer outward; each layer compiles before the next
starts. Unit tests are written from the DD as the code is built, not afterwards.

Stop and ask when the design is silent (IM-08). A gap discovered here is cheap to raise and
expensive to guess at.

## Step 6 — Verify

Run `{{profile.system.build.order}}` in order, then typecheck, lint and the unit tests.
Report actual output.

## Step 7 — Report

```
P4 — {MODULE}
  Design read     : SC {n} · FC {n} · API {n} · DT {n} · DD {n}
  Context map     : {checked}/{total}   unchecked: {list}
  Files           : created {n} · modified {n}
  Build           : {pass|fail}   {first error if failed}
  Typecheck/lint  : {pass|fail}
  Unit tests      : {passed}/{total}   coverage {line}/{branch}
  Design changes  : {n} (through CR {id}, or "none")
  Questions raised: {n}   ({what was silent in the design})
  Traceability    : {n} rows updated
  Gate {{profile.gates.P4_implementation.exit}} : {pass|fail}
```

A failing build is reported failing, with the error text. Never summarised as "mostly
working".

Then `/sdlc_review_commit` before the module is called done.
