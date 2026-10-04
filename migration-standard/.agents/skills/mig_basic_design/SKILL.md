---
name: mig_basic_design
description: "P2 — basic design orchestration and the shared deliverable format. Owns the category plan, generation batching, document skeleton, revision history, diagrams, and the cross-document checks. Load for ANY basic-design task, alongside the category skill (screen/function/api/data/batch)."
---

# P2 — Basic Design (shared)

> Prerequisite: `mig_project` loaded; P1 gate passed.
> This skill owns the **format and the plan**. Category rules live in the category skills.

---

## Category plan

Categories, their directories and their owning skills come from
`{{profile.paths.bd_categories}}` — read it, do not assume a fixed list. For each entry:

```
{{profile.paths.design_root}}/{dir}/
```

Before generating, build and print the plan:

| # | Category | Directory | Skill | Expected files | Existing | To generate |
|---|---|---|---|---|---|---|

"Expected" is derived from the FRD module list, not from a hardcoded number. If the FRD
and the plan disagree, the FRD wins and the discrepancy is reported.

Add a **Template** column. For each category, look it up in
`{{profile.templates.registry}}` and state the branch you are taking: the client's registered
form, the pack's own skeleton (`on_missing: skeleton`), or stopped awaiting a form. Load
`mig_document_io` for the mechanics and for anything not Markdown.

A run that quietly used the pack's skeleton where the client expected their own form has
produced work that will be redone — so it is stated in the plan, before generating, not
discovered at the review.

---

## Generation batching

Large categories are generated in batches, per module or per business area, 10–20 files
per agent call. This is a context-budget constraint, not a preference: a single call
attempting 100 documents degrades quality on the last ones and usually silently drops the
final category.

**Batching rules:**
- one agent call per batch, fresh context
- a batch is a whole module or a whole area — never split one module across two calls
- the last categories in the plan (reports, file interfaces) are the ones that get
  dropped when a run is long. Spawn them in their own call, deliberately.
- after each batch, count the files actually written and report `written/expected`

---

## Deliverable skeleton

Per `rules/migration/document-standards.md` DS-01 — **unless the category has a registered
template, which outranks it** (DS-10). Then DS-01 describes what the document must still
contain, not what it must look like, and a template gap is reported to the document owner
once rather than worked around per file. A form with no anchor column never suspends NI-01.

Every file:

```markdown
---
doc_id: {MODULE}-{TYPE}-{NNN}
title: {{profile.project.name}} — {category} ({title})
---

# {Title}（{ID}）

**<Revision history>**

| {{profile.document.revision_table_headers}} … |
| {{profile.document.initial_version}} | {today} | {{profile.document.initial_change_text}} | {{profile.project.vendor}} | {{profile.project.client}} | {today} |

**<Contents>**

## 1-1. …
…

## Open Items

---
{{profile.document.footer}}
```

Hard rules:
- revision-history column names are fixed by the profile (DS-01)
- **no automatic version bump** (DS-02)
- footer exactly once, at the end
- section numbering and order fixed by the category skill (DS-03)
- Open Items present, "None." when empty (DS-09)

---

## Diagrams

- `{{profile.document.diagram_tool}}` fenced blocks only, never image files
- constraints in `{{profile.document.diagram_constraints}}` are hard — verify a shape is
  supported by the client's renderer version before using it
- processing flow: top-down; every error branch terminates in a node naming its `MSG-*`
- screen transition: one diagram per module, with entry and exit edges labelled by the
  trigger

---

## Cross-document checks (X-01..X-07)

Run at the end of each category and again at the end of P2. Each mismatch is Critical.

| Check | Left | Right |
|---|---|---|
| X-01 | screen grid columns | legacy grid definition (`LEG-*`) |
| X-02 | screen field list | legacy form control list |
| X-03 | function input params | API request fields |
| X-04 | function output fields | API response fields |
| X-05 | function error codes | API error codes |
| X-06 | screen `MSG-*` set | function `MSG-*` set |
| X-07 | data-design columns | legacy DDL / copybook |
| X-09 | mockup (a..h) | screen design — run by `/mig_generate_mockup` |
| X-10 | mockup (a..f) | legacy screen — run by `/mig_generate_mockup`, unless `redesigned` |

Report as a table of `check · left artifact · right artifact · verdict`. Do not "fix" a
mismatch by editing one side to match the other without determining which side is wrong
against the legacy source.

---

## Common failure modes in P2

| Symptom | Cause | Fix |
|---|---|---|
| Late categories missing | one long run, context exhausted | dedicated call per late category |
| Field lists drift from legacy | designed from the FRD prose only | read the legacy form definition directly |
| Message text differs subtly | retyped instead of copied | copy verbatim from the P0 catalogue |
| Implementation detail in screen docs | no scope discipline | apply DS-04 per section |
| IDs renumbered after review | items inserted mid-document | append with the next number; leave gaps (ID-04) |
| Whole category rejected on formatting | generated into the pack's skeleton, not the client's form | register the template first; state the branch in the plan (DS-10) |
| Behaviour anchored to a ten-year-old spec | legacy document treated as authoritative | DIO-08 — the code is the oracle; the document is intent |
| Operators reject the UI at UAT | mockup quietly modernised under `as-is` | `/mig_generate_mockup`, X-10 per screen |

---

## Exit gate

- [ ] plan printed, `written/expected` reported per category, with the template branch
      stated per category
- [ ] X-01..X-07 pass
- [ ] every document has revision history, Open Items and footer
- [ ] every binary deliverable has its plain-text digest, carrying the anchors (DIO-07)
- [ ] X-09 and X-10 clean where `{{profile.mockup.kind}}` is not `none`
- [ ] `/mig_review_design` reports zero Critical
- [ ] `{{profile.paths.traceability}}` updated with every design id
