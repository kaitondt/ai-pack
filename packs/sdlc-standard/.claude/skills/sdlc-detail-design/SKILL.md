---
name: sdlc-detail-design
description: "P3 — detail design and the design-vs-code drift analysis. Produces DD documents per module, written so a unit test can be derived from them, plus a drift report where the implementation diverges from the design. Load for ALL detail-design and design-code reconciliation tasks."
---

# P3 — Detail Design and Drift Analysis

> Prerequisite: `sdlc-project` resolved; P2 gate passed for the module.

Detail design sits between basic design and code. Its job is to make the module
**implementable without further decisions** and **unit-testable without reading the code**
— the second is what the V-model binding requires (TR-03: DD is the basis for UT).

---

## Two modes

| Mode | When | Output |
|---|---|---|
| **Forward** | code not yet written | DD document per module, derived from the basic design |
| **Reconcile** | code exists | DD document **plus** a drift report per module |

Determine the mode by checking whether the module has implementation under
`{{profile.system.root}}`. In reconcile mode the code is evidence, not authority — see
drift resolution below.

---

## DD document skeleton

```
# {ModuleName} — Detail Design（{MODULE}-DD-{NNN}）
  <Revision history>  <Review record>  <Contents>

## 1  Scope             module, covered SC / FC / API / DT ids
## 2  Component map     the concrete units: classes, handlers, components, files
## 3  Sequence          per function: caller → unit → data access → response
## 4  Data structures   the actual types crossing each boundary
## 5  Logic detail      per FC rule: the implementing unit and the algorithm
## 6  Error mapping     FC error → exception/result type → API status → MSG-*
## 7  Configuration     settings, feature flags, environment differences
## 8  Test hooks        the seams P5 relies on: injection points, clock, ids, fakes

## Drift items          (reconcile mode only)
## Open Items
```

**DD-01 — the DD names real artifacts.** Every unit in §2 is a real path in the
repository, or a path that will exist. `file_path:symbol`, not a vague description.

**DD-02 — the DD does not restate the basic design.** It says *how*, referencing the
design id for *what*. A DD that paraphrases the function design creates a second source of
truth that will drift from the first.

**DD-03 — one DD per module**, covering all of that module's design ids.

**DD-04 — written to be testable.** For every rule in §5, a reader must be able to answer:
what is the unit, what are its inputs, what is the expected output, and what are the
boundary values? If they cannot, the DD is not finished — and the P5 team will invent the
answers, which is how tests end up asserting what the code does (`rules/common/testing.md`).

**DD-05 — §8 is not optional.** A module with no injection point for the clock, no way to
supply an id, and no seam for its dependency is a module whose unit tests will be
integration tests. Design the seams here, before they cost a refactor.

---

## What belongs in §5

Per rule from the function design:

| FC rule | Implementing unit | Algorithm | Inputs | Boundary values | Expected result |
|---|---|---|---|---|---|

Algorithms that must be spelled out rather than summarised:

- any calculation with rounding, scale or currency (FD-R02)
- any sort with more than one key, or with nulls
- any date arithmetic crossing a day, month or business-calendar boundary
- any partial-failure or compensation path
- any retry, with its backoff and its limit

"Standard logic" is not an algorithm. If two developers could implement the sentence
differently, it is not a detail design.

---

## Drift analysis

Run for every module in reconcile mode. Compare, item by item:

| # | Compare | Against |
|---|---|---|
| G-01 | screen fields, order, types | implemented UI |
| G-02 | function processing steps and order | implemented handler |
| G-03 | validation rules and their order | implemented validators |
| G-04 | error cases and `MSG-*` | implemented error paths |
| G-05 | API request/response fields | implemented contract |
| G-06 | data structures and parameters | implemented data access |
| G-07 | paging, sorting and defaults | implemented query |
| G-08 | calculations, rounding, precision | implemented arithmetic |
| G-09 | permission checks | implemented authorisation |

### Drift report

One file per module, only when drift exists:
`{{profile.paths.drift_reports}}/DRIFT_{MODULE}_{YYYYMMDDHHmm}.md`

| # | Check | Design says | Code does | Requirement says | Verdict | Action |
|---|---|---|---|---|---|---|

**Verdict** is decided against the **baselined requirement**, not against whichever side is
more convenient to change:

| Verdict | Meaning | Action |
|---|---|---|
| `DOC-WRONG` | code satisfies the requirement, the document does not | fix the document |
| `CODE-WRONG` | document satisfies the requirement, the code does not | fix the code (P4), raise a `BUG-*` |
| `BOTH-WRONG` | neither satisfies the requirement | fix both, and ask how it got here |
| `REQ-GAP` | the requirement is silent | stop, ask the owner (RS-01) |
| `ACCEPTED` | deliberate, approved deviation | record the `DEC-*` or `CR-*` reference |

**A drift item is never closed by editing the document to match the code without checking
the requirement.** That converts a defect into a specification. It is the most common way
a project ends up delivering something nobody asked for, with documentation that agrees.

Every `CODE-WRONG` item is also a defect record with an injection phase (TR-07) — usually
P4, sometimes P3 if the DD was ambiguous enough to be read two ways. Recording it matters
more than fixing it quickly: it is the input to phase containment (QM-04).

---

## Self-check

- [ ] mode determined; drift analysis run when code exists
- [ ] every unit in the component map is a real path
- [ ] no basic-design content restated
- [ ] every rule in §5 has inputs, boundaries and an expected result
- [ ] test seams specified in §8
- [ ] every drift item has a verdict decided against the requirement
- [ ] every `CODE-WRONG` item has a `BUG-*` and a P4 follow-up
- [ ] every `REQ-GAP` escalated with an owner and a due date
- [ ] traceability updated with the DD ids
- [ ] `{{profile.gates.P3_detail_design.exit}}` assertions hold
