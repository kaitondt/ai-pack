---
name: mig-detail-design
description: "P3 — detail design and the BD-vs-code GAP analysis. Produces DD documents per module and a per-module GAP report where the implementation diverges from basic design. Load for ALL detail-design and design-code reconciliation tasks."
---

# P3 — Detail Design and GAP Analysis

> Prerequisite: `mig-project` resolved; P2 gate passed for the module.

Detail design sits between basic design and code. In a migration it has a second job that
greenfield projects do not have: **it reconciles the design with what was actually built**,
because implementation always discovers legacy behaviour the design missed.

---

## Two modes

| Mode | When | Output |
|---|---|---|
| **Forward** | code not yet written | DD document per module, derived from BD |
| **Reconcile** | code exists | DD document **plus** a GAP report per module |

Determine the mode by checking whether the module has implementation under
`{{profile.target.root}}`. In reconcile mode the code is evidence, not authority — see
GAP resolution below.

---

## DD document skeleton

```
# {ModuleName} 詳細設計 / Detail Design（DD-{MODULE}-{NNN}）
  <Revision history>
  <Contents>

## 1  Scope             module, covered SC / FC / API ids
## 2  Component map     the concrete units: classes, handlers, components, files
## 3  Sequence          per function: caller -> unit -> data object -> response
## 4  Data structures   the actual types crossing each boundary
## 5  Logic detail      per FC rule: the implementing unit and the algorithm
## 6  Error mapping     FC error -> exception/result type -> API status -> MSG-*
## 7  Configuration     settings, feature flags, environment differences
## 8  Test hooks        seams that P5/P6 rely on

## GAP items
## Open Items
```

**DD-01 — the DD names real artifacts.** Every unit in section 2 is a real path in the
repository, or a path that will exist. `file_path:symbol`, not a vague description.

**DD-02 — the DD does not restate the BD.** It says *how*, referencing the BD id for
*what*. A DD that paraphrases the function design adds a second source of truth that will
drift.

**DD-03 — one DD per module**, covering all of that module's SC/FC/API ids.

---

## GAP analysis

Run for every module in reconcile mode. Compare, item by item:

| # | Compare | Against |
|---|---|---|
| G-01 | screen fields, order, types | implemented UI |
| G-02 | function processing steps and order | implemented handler |
| G-03 | validation rules and their order | implemented validators |
| G-04 | error cases and MSG-IDs | implemented error paths |
| G-05 | API request/response fields | implemented contract |
| G-06 | data objects and parameters | implemented data access |
| G-07 | paging, sorting and defaults | implemented query |
| G-08 | calculations, rounding, precision | implemented arithmetic |

### GAP report

One file per module, only when gaps exist:
`{{profile.paths.gap_reports}}/GAP_{MODULE}_{YYYYMMDDHHmm}.md`

| # | Check | BD says | Code does | Legacy says | Verdict | Action |
|---|---|---|---|---|---|---|

**Verdict** is the important column, and it is decided against the **legacy source**, not
against whichever side is more convenient:

| Verdict | Meaning | Action |
|---|---|---|
| `DOC-WRONG` | code matches legacy, document does not | fix the document |
| `CODE-WRONG` | document matches legacy, code does not | fix the code (P4) |
| `BOTH-WRONG` | neither matches legacy | fix both |
| `SPEC-GAP` | legacy is silent | stop, ask the client (NI-01) |
| `ACCEPTED` | deliberate, approved deviation | record the approval reference |

**A GAP is never closed by editing the document to match the code without checking the
legacy.** That converts a defect into a specification, and it is the most common way a
migration silently loses parity.

---

## Self-check

- [ ] mode determined; GAP run when code exists
- [ ] every unit in the component map is a real path
- [ ] no BD content restated
- [ ] every gap has a verdict decided against the legacy source
- [ ] every `CODE-WRONG` gap has a P4 follow-up
- [ ] every `SPEC-GAP` escalated
- [ ] traceability updated with the DD ids
