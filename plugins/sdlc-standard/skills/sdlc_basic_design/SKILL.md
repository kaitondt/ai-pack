---
name: sdlc_basic_design
description: "P2 — basic design orchestration and the shared deliverable format. Owns the category plan, generation batching, document skeleton, the architecture document, diagrams, and the cross-document checks X-01..X-10. Load for ANY basic-design task, alongside the category skill (nfr/screen/function/data/api/batch)."
---

# P2 — Basic Design (shared)

> Prerequisite: `sdlc_project` loaded; P1 gate passed and the SRS baselined.
> This skill owns the **format and the plan**. Category rules live in the category skills.

Basic design answers *what the system does, as seen from outside a module*: screens,
functions, data, interfaces, batches, and the architecture that holds them. It is the
document the integration test verifies (TR-03).

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

"Expected" is derived from the SRS module and use-case list, not from a hardcoded number.
If the SRS and the plan disagree, the SRS wins and the discrepancy is reported before
anything is generated.

Add a **Template** column to the plan. For each category, look it up in
`{{profile.templates.registry}}` and state which branch you are taking: the client's
registered form, the pack's own skeleton (with `on_missing: skeleton`), or stopped awaiting
a template. Load `sdlc_document_io` for the mechanics, and for anything not Markdown.

A run that quietly used the pack's skeleton where the client expected their own form has
produced work that will be redone — so it is stated in the plan, before generating, not
discovered at the review.

---

## The architecture document comes first

Category `architecture` is generated before every other category, because everything else
depends on decisions it records:

| § | Content |
|---|---|
| 1 | System context — actors, external systems, trust boundaries |
| 2 | Logical architecture — layers, modules, their responsibilities and dependencies |
| 3 | Technology stack, from `{{profile.system.stack}}`, with the reason for each choice |
| 4 | Environment matrix — `{{profile.system.environments}}` and what differs |
| 5 | Cross-cutting concerns — auth, logging, error handling, validation, i18n, audit |
| 6 | Data strategy — ownership, transactions, concurrency policy, retention |
| 7 | Integration architecture — per external system: protocol, failure, retry, fallback |
| 8 | How each `NFR-*` is delivered — the X-09 table |
| 9 | Build, deploy, release and rollback |
| 10 | Open Items |

**Every decision records its rejected alternatives and why** (`DEC-*`). A decision without
a rationale is re-litigated every sprint, and re-decided differently by whoever is on the
ticket.

**§8 is the one people skip.** Each `NFR-*` gets a row naming the mechanism that delivers
it and the ST case that will measure it. An NFR with an empty row is a P7 failure that has
already happened; it just has not been observed yet.

---

## Generation batching

Large categories are generated in batches, per module or per business area, 10–20 files
per agent call. This is a context-budget constraint, not a preference: a single call
attempting 100 documents degrades quality on the last ones and usually silently drops the
final category.

**Batching rules:**
- one agent call per batch, fresh context
- a batch is a whole module or a whole area — never split one module across two calls
- the last categories in the plan (reports, file interfaces) are the ones that get dropped
  when a run is long. Spawn them in their own call, deliberately.
- after each batch, count the files actually written on disk — not the files the agent
  reported writing

---

## Deliverable skeleton

Per `rules/sdlc/document-standards.md` DS-01 — **unless the category has a registered
template, which outranks it** (DS-11). Then DS-01 describes what the document must still
contain, not what it must look like, and a template gap is reported to the document owner
once rather than worked around per file.

Every file carries front matter with `doc_id` and `status`, a revision history with the
profile's fixed columns, a review record, the category's fixed sections, an Open Items
table, and the footer exactly once.

Hard rules:
- revision-history column names are fixed by the profile (DS-01)
- **no automatic version bump** (DS-02)
- section numbering and order fixed by the category skill (DS-04)
- Open Items present, "None." when empty, every item with an owner and a due date (DS-10)

---

## Diagrams

- `{{profile.document.diagram_tool}}` fenced blocks only, never image files
- constraints in `{{profile.document.diagram_constraints}}` are hard — verify a shape is
  supported by the client's renderer before using it
- processing flow: top-down; every error branch terminates in a node naming its `MSG-*`
- screen transition: one diagram per module, with entry and exit edges labelled by trigger
- every branch in a diagram has a row in the rules or error table, and vice versa (DS-08)

---

## Cross-document checks (X-01..X-10)

Run at the end of each category and again at the end of P2. Each mismatch is Critical.

| Check | Left | Right |
|---|---|---|
| X-01 | screen item list | requirement input/output fields |
| X-02 | screen grid columns | data design / query result definition |
| X-03 | function input params | API request fields |
| X-04 | function output fields | API response fields |
| X-05 | function error cases | API error codes |
| X-06 | screen `MSG-*` set | function `MSG-*` set |
| X-07 | data design columns | DDL / migration scripts |
| X-09 | `NFR-*` targets | architecture decisions that deliver them |
| X-10 | every `REQ-*` | at least one design item realising it |
| X-11 | mockup (a..g) | screen design — run by `/sdlc_generate_mockup` |

Report as a table of `check · left artifact · right artifact · verdict`. Do not "fix" a
mismatch by editing one side to match the other without determining which side is wrong
against the SRS.

X-10 is the completeness check and it runs last, over the whole of P2. A requirement with
no design item is not a documentation gap — it is a feature nobody is building.

---

## Common failure modes in P2

| Symptom | Cause | Fix |
|---|---|---|
| Late categories missing | one long run, context exhausted | dedicated call per late category |
| NFRs designed for nowhere | architecture written before the NFR table was read | X-09, before any module design |
| Design contradicts the SRS | worked from the ticket or the chat thread | design from the baselined SRS only |
| Implementation detail in screen docs | no scope discipline | apply DS-05 per section |
| Two documents disagree | generated in separate runs, never cross-checked | X-01..X-07 per category, not only at the end |
| IDs renumbered after review | items inserted mid-document | append with the next number; leave gaps (ID-06) |
| Requirements quietly widened | designer "improved" a rule while designing | RS-06 — it goes to the CR backlog |
| Whole category rejected on formatting | generated into the pack's skeleton, not the client's form | register the template first; state the branch in the plan (DS-11) |
| Mockup and screen design disagree at UAT | X-11 never run, or run once at the start | `/sdlc_generate_mockup`, per screen, at category end and at the gate |

---

## Exit gate

- [ ] plan printed, `written/expected` reported per category, with the template branch
      stated per category
- [ ] X-01..X-07, X-09, X-10 pass
- [ ] every document has revision history, review record, Open Items and footer
- [ ] every binary deliverable has its plain-text digest (DIO-07)
- [ ] X-11 clean where `{{profile.mockup.kind}}` is not `none`
- [ ] `/sdlc_review_design` reports zero Critical
- [ ] `{{profile.paths.traceability}}` updated with every design id
- [ ] `{{profile.gates.P2_basic_design.exit}}` assertions hold

Then run `/sdlc_phase_gate P2`.
