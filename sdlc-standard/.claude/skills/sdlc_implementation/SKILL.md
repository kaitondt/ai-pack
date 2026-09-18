---
name: sdlc_implementation
description: "P4 — implementation. Design-first workflow, layer order, the specification-fidelity rules IM-01..IM-08, standard hazards, build verification, and the definition of done for a module. Load for ALL coding tasks in this project."
---

# P4 — Implementation

> Prerequisite: `sdlc_project` resolved; P2 and P3 gates passed for the module; the codebase
> skeleton in place and building (`sdlc_codebase`, `/sdlc_scaffold_codebase`).
> Load `sdlc_context_map` before touching the first file.

---

## Workflow

1. **Read the design.** SC, FC, API, DT and DD for the module — the baselined documents,
   not the ticket text and not the chat thread.
2. **Reconcile before coding.** Where the documents disagree with each other, that is a
   design defect raised now, not a decision made silently in code.
3. **Emit the context map.** Every file the change touches.
4. **Implement, inner layer outward**, following the dependency direction. Each layer
   compiles before the next is started.
5. **Write the unit tests from the DD**, not from the code you just wrote
   (`rules/common/testing.md`).
6. **Verify the build** in the mandated order (`{{profile.system.build.order}}`).
7. **Self-review** against `sdlc_review_framework` before reporting done.

---

## Layer order

Implement inner to outer. This is not aesthetics — it prevents writing an outer layer
against a shape that then changes.

```
data → domain → application (dto, handler, validator) → transport → shared types → ui → tests
```

Build in `{{profile.system.build.order}}` exactly. That order exists because packages
depend on each other's build output; running it out of order produces confusing failures
against stale artifacts.

---

## Specification-fidelity rules

These are the coding-level expression of RS-01 and RS-06.

- **IM-01 — implement the specification, not your reading of the intent.** Where the DD
  gives an algorithm, implement that algorithm. If it is wrong, say so and get it changed
  — do not implement the better version and leave the document behind.
- **IM-02 — validation order is specified behaviour.** When the design stops at the first
  failure, stop at the first failure. Collecting all errors changes what the screen shows
  and what the test asserts.
- **IM-03 — sort explicitly, always.** Reproduce the specified order, including the tie
  breaker. Never rely on natural, insertion or index order; it is stable until the query
  plan changes.
- **IM-04 — user-facing text comes from the catalogue by `MSG-*`.** Never typed inline,
  never reworded in passing. A message written at the call site is invisible to review,
  translation and test.
- **IM-05 — no behaviour the design did not ask for.** No extra field, no helpful default,
  no silent trim, no "while I was there" validation. It goes to the CR backlog (RS-06).
- **IM-06 — precision is implemented as specified**: the stated intermediate precision,
  rounding mode and rounding point (FD-R02, DT-04). Do not simplify the expression
  algebraically; fixed-point and floating-point results differ.
- **IM-07 — carry the anchor.** Where behaviour looks wrong but matches the specification,
  leave a comment with the requirement id. It stops a future reader from "fixing" it.
- **IM-08 — when the design is silent, stop.** Do not decide. A gap discovered in P4 is
  cheap to raise and expensive to guess at: the guess becomes the specification the moment
  it ships.

---

## Standard hazards

- **Async actions lock their trigger.** Disable on click, keep a visible pending state
  until the response resolves, re-enable in a `finally`-equivalent. Double submission is
  the most common defect in transactional screens.
- **Server-side paging and sorting.** Never fetch the full set and page in the client.
- **Server-side authorisation.** Hiding a control is presentation, not a permission check.
  Every operation checks, including the ones with no UI entry point.
- **Parameterised queries only**, whatever the input source.
- **No secrets in source, fixtures, logs or error messages.**
- **Time zone at the boundary.** Convert once, where the design says, and store per DT-05.
- **Never edit generated files**; verify the generator exists first (BL-07, CM-01).
- **Never edit a baselined document without a CR** (BL-02) — including the design document
  you are implementing, when you find it wrong.
- **Configuration, not branching, for environment differences** — a `if (env == "prod")`
  is an untested production path by construction.

---

## Unit tests are part of P4, not a later phase

The P5 gate needs them; write them as the module is built.

- Expected values come from the DD and the FC, never from running the code.
- Cover: every rule in DD §5, every validation branch, every error path with its `MSG-*`,
  the boundary values named in the DD, and the authorisation cases.
- No wall-clock, no random, no network — use the seams from DD §8.

---

## Definition of done for a module

- [ ] every SC/FC/API/DT/DD item for the module is implemented
- [ ] context map fully checked off, or the remainder reported
- [ ] `{{profile.system.build.order}}` completes clean
- [ ] `{{profile.system.build.typecheck}}` and `{{profile.system.build.lint}}` clean
- [ ] unit tests for validators, handlers and calculations exist and pass
- [ ] no new Critical from `/sdlc_review_commit`
- [ ] design documents updated through a CR where the design changed, or drift items
      recorded deliberately
- [ ] `{{profile.paths.traceability}}` rows updated with the code references
- [ ] every defect found while implementing is recorded with its injection phase (TR-07)

Report the build output as it happened. A failing build is reported failing, with the
error text — never summarised as "mostly working".
