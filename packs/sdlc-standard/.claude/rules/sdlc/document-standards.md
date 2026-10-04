# RULE FAMILY: DOCUMENT STANDARDS

Applies to every generated deliverable in P0–P8. Values in `{{...}}` come from the
profile's `document` section.

## DS-01 — Fixed skeleton

```markdown
---
doc_id: {MODULE}-{TYPE}-{NNN}
title: {{profile.project.name}} — {category} ({document title})
status: draft | in-review | baselined
---

# {Title} ({ID})

**<Revision history>**

| {{profile.document.revision_table_headers | joined}} |
| ... |
| {{profile.document.initial_version}} | {date} | {{profile.document.initial_change_text}} | {{profile.project.vendor}} | | | |

**<Review record>**            ← when {{profile.document.require_review_record}}

| Round | Date | Reviewer | Findings (C/W/S) | Closed on |
|---|---|---|---|---|

**<Contents>**

## 1. ...
## 2. ...

## Open Items

---
{{profile.document.footer}}
```

- Header column names are fixed by the profile. Renaming a column is a Critical finding —
  the client's document tooling parses these.
- The footer appears exactly once, at the end.
- `status` in the front matter and the version must agree (BL-08). A `0.x` document with
  `status: baselined` is a Critical finding.

## DS-02 — No automatic version bump

`{{profile.document.auto_version_bump}}` is `false`. Add a revision row **only** when the
user explicitly instructs it, or when a gate baselines the document. Editing a document
does not bump its version.

## DS-03 — The review record is part of the document

When `{{profile.review.record_in_document}}` is true, every deliverable carries its review
history: who reviewed it, when, how many findings by severity, and when they were closed.

A document with no review record has not been reviewed, whatever anybody remembers. This
table is also the raw input to review density (`quality-metrics.md` QM-02) — a review
round recorded with zero findings is a signal, not an achievement.

## DS-04 — Section structure is fixed per category

Each design category defines its section skeleton in its own skill (`sdlc-screen-design`,
`sdlc-function-design`, …). Sections are neither reordered nor omitted; an unused section
carries an explicit "not applicable" line rather than disappearing.

## DS-05 — Scope discipline per section

Documents leak across levels unless scope is policed. What belongs where:

| Document | Answers | Must not contain |
|---|---|---|
| Requirements (P1) | what the business needs, measurably | screen layout, table names, technology, algorithms |
| Basic design (P2) | what the system does, externally visible | private method names, code structure, SQL |
| Detail design (P3) | how a module does it internally | business rationale, re-stated requirements |
| Screen design | what the user sees and does | route paths, component names, HTTP status codes, server validation |
| Function design | server-side processing, params, errors | UI colours, CSS, component names |
| Interface design | the endpoint contract | UI behaviour, business rationale |

The test for a leaked section: if changing the sentence would require changing a different
document too, it is in the wrong one.

## DS-06 — No physical data names in prose

Physical column and field names (`ALL_CAPS_WITH_UNDERSCORES`, `tbl_` prefixes) are
forbidden in body prose and in user-facing item-name columns. Use the logical name. Physical
names live in the data-design deliverable and in mapping tables that exist to carry them.

Detection pattern: `[A-Z][A-Z0-9_]{2,}` that is not a document ID, module ID or MSG-ID.

## DS-07 — Table cell conventions

- One point per line inside a cell, separated by `<br>` — not by `;`, not by sentence
  punctuation.
- No sentence-ending punctuation in table cells outside message-text columns.
- Empty means "not applicable" only when the column defines it that way; otherwise write
  the explicit marker (`—`).

## DS-08 — Diagrams

- Tool: `{{profile.document.diagram_tool}}`, fenced code block, never an image file.
- Constraints from `{{profile.document.diagram_constraints}}` are hard limits — a diagram
  that will not render in the client's viewer is worthless.
- Processing flows: top-down flowchart. Error branches terminate in a node naming the
  MSG-ID.
- Every branch in a diagram has a corresponding row in the rules or error table, and vice
  versa. A diagram that says more than the tables is the version nobody maintains.

## DS-09 — Language per directory

The language of a deliverable is determined by its directory
(`{{profile.language.by_path}}`), never by the language of the request. When a Vietnamese
request produces a Japanese deliverable, the deliverable is Japanese.

## DS-10 — Open Items section

Every P0–P3 deliverable ends with an **Open Items** table before the footer:

| # | Item | Kind | Owner | Raised | Due | Status |
|---|---|---|---|---|---|---|
| 1 | ... | OPEN-QUESTION / ASSUMPTION / DECISION-NEEDED / RISK / PROPOSAL | name | YYYY/MM/DD | YYYY/MM/DD | open |

An empty table is written as "None." — the section is never omitted. This is where RS-01
uncertainty and RS-02 assumptions land, and it is what the reviewer reads first.

**An Open Item without an owner and a due date is not an open item; it is a wish.**

## DS-11 — The project's own template outranks this skeleton

The pack ships no templates. Where the client supplies one and it is registered in
`{{profile.templates.registry}}`, **the template is authoritative over both DS-01 and the
category skill's section list** — its headings, its column names, its order, its approval
block.

DS-01 then describes what the document must still *contain*, not what it must look like.
Where the template has nowhere to put required content, that is a **template gap**: report
it to the document owner **once**, not once per generated file, and never resolve it by
adding a section of your own invention (DIO-01, DIO-02).

Where no template is registered, `{{profile.templates.on_missing}}` decides — and a document
generated from the pack's own skeleton says so in the run report, so nobody mistakes it for
the client's form.

`sdlc-document-io` owns the mechanics.

## DS-12 — Format follows the category, not the task

The output format of a deliverable is `{{profile.templates.registry}}[key].output_format`,
or the template's own format when that is empty. It is not chosen per request, and not
changed because another format would be easier to review — that produces two copies of one
deliverable, and they diverge within a week (DIO-05).

Two obligations follow for non-Markdown deliverables:

- **A binary deliverable carries a plain-text digest** under
  `{{profile.paths.reviews}}/digests/`, holding the values that were written (DIO-07).
  Without it the document is outside every review, cross-check and gate the pack runs.
- **Round-trip fidelity**: writing a deliverable changes nothing outside the filled fields —
  not a column width, not a merged range, not the print area (DIO-03).
