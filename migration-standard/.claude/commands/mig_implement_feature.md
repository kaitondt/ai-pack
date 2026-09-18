---
description: "P4 — implement a module end to end across every layer, design-first, with the context map, the mandated build order and a self-review. Usage: /mig_implement_feature MODULE"
---

# P4 — Implement a module

## Step 1 — Load

`mig_project`, `mig_context_map`, `mig_implementation`, and the stack rule files under
`rules/` that match the layers you will touch.

## Step 2 — Pre-check

The module needs approved SC, FC and API documents (and a DD, where P3 is used for it).
Missing → stop and name the command that produces them. Implementing from the FRD alone
reproduces the design phase badly, inside the code.

## Step 3 — Read before writing

1. the module's design documents
2. the legacy source for the same module, including its data objects

Where the two disagree, raise it as a P3 GAP item **now**. Do not resolve it in code.

## Step 4 — Emit the context map

Every file, by layer, with real repository paths. Present it before the first edit.

## Step 5 — Implement inner to outer

Follow `{{profile.target.build.order}}`. Each layer builds before the next begins.

Apply the parity rules IM-01..IM-06: reproduce arithmetic exactly, preserve validation
order, sort explicitly, copy message text, add no defensive behaviour, carry the anchors
in comments.

## Step 6 — Verify

Run the build order, the type-check, and the unit tests. Report the real output.

## Step 7 — Self-review

Run `/mig_review_commit` scoped to the changed files. Fix Critical findings before
reporting done.

## Step 8 — Report

```
P4 — {MODULE}
  Context map    : {checked}/{total}   unchecked: {list}
  Build          : {pass|fail}  ({command that failed, with output})
  Type-check     : {pass|fail}
  Unit tests     : {passed}/{total}
  Review         : Critical {n} · Warning {n}
  Docs updated   : {list}   GAP items recorded : {n}
  Gate {{profile.gates.P4_implementation}} : {pass|fail}
```
