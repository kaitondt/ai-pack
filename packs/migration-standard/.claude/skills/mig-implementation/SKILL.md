---
name: mig-implementation
description: "P4 — implementation. Design-first workflow, layer order, parity-preserving coding rules, async action locking, build verification, and the definition of done for a migrated module. Load for ALL coding tasks in a migration project."
---

# P4 — Implementation

> Prerequisite: `mig-project` resolved; P2 (and P3 where used) gate passed for the module;
> the target codebase skeleton in place and building (`mig-codebase`, `/mig-scaffold-codebase`).
> Load `mig-context-mapping` before touching the first file.

---

## Workflow

1. **Read the design.** SC, FC, API and DD for the module. Not the FRD prose — the
   approved design documents.
2. **Read the legacy source** for the same module. The design is a summary; the legacy is
   the specification. Where they disagree, that is a P3 GAP item, and it is raised before
   code is written, not after.
3. **Emit the context map.** Every file the change touches.
4. **Implement, inner layer outward**, following the dependency direction. Each layer
   compiles before the next is started.
5. **Verify the build** in the mandated order (`{{profile.target.build.order}}`).
6. **Self-review** against `mig-review-framework` before reporting done.

---

## Layer order

Implement inner to outer. This is not aesthetics — it prevents writing an outer layer
against a shape that then changes.

```
domain -> application (dto, handler, validator) -> transport -> shared types -> ui -> tests
```

Build in `{{profile.target.build.order}}` exactly. That order exists because packages
depend on each other's build output; running it out of order produces confusing failures
against stale artifacts.

---

## Parity rules

These are the coding-level expression of NI-01 and NI-02.

- **IM-01 — reproduce the legacy expression.** Copy the arithmetic, including rounding
  mode, truncation point and intermediate precision. Do not simplify it algebraically:
  floating-point and fixed-point results differ.
- **IM-02 — preserve validation order.** When the legacy stops at the first failure, stop
  at the same first failure. Collecting all errors is a behaviour change.
- **IM-03 — sort explicitly, always.** Reproduce the legacy order even when it looks
  arbitrary. Never rely on natural or insertion order.
- **IM-04 — message text is a constant copied from the catalogue.** Not retyped, not
  reformatted, not corrected.
- **IM-05 — no defensive behaviour the legacy did not have.** No auto-trim, no silent
  default, no "helpful" coercion. These change results.
- **IM-06 — carry the anchor.** Where behaviour looks wrong but matches the legacy, leave
  a comment with the anchor. It stops a future reader from "fixing" it.

---

## Standard hazards

- **Async actions lock their trigger.** Disable on click, keep disabled with a pending
  state until the response resolves, re-enable in a finally-equivalent. Double submission
  is the most common defect in migrated transactional screens.
- **Server-side paging and sorting.** Never fetch the full set and page in the client.
- **Server-side authorisation.** Hiding a control is presentation, not a permission check.
- **No raw SQL where the project mandates procedures**; no schema changes where the schema
  is frozen (LR-03).
- **Never edit generated files**; verify the generator exists first (LR-04, CM-01).
- **Never modify anything under `{{profile.legacy.root}}`** (LR-01).

---

## Definition of done for a module

- [ ] every SC/FC/API item for the module is implemented
- [ ] context map fully checked off, or the remainder reported
- [ ] `{{profile.target.build.order}}` completes clean
- [ ] `{{profile.target.build.typecheck}}` clean
- [ ] unit tests for validators, handlers and calculations exist and pass
- [ ] no new Critical from `/mig-review-commit`
- [ ] design documents updated, or GAP items recorded deliberately
- [ ] `{{profile.paths.traceability}}` rows updated with the code references

Report the build output as it happened. A failing build is reported failing, with the
error text — never summarised as "mostly working".
