# RULE FAMILY: DOCUMENT STANDARDS

Applies to every generated deliverable in P1–P6. Values in `{{...}}` come from the
profile's `document` section.

## DS-01 — Fixed skeleton

```markdown
---
doc_id: {MODULE}-{TYPE}-{NNN}
title: {{profile.project.name}} — {category} ({document title})
---

# {Title} ({ID})

**<Revision history>**

| {{profile.document.revision_table_headers | joined}} |
| ... |
| {{profile.document.initial_version}} | {date} | {{profile.document.initial_change_text}} | {{profile.project.vendor}} | {{profile.project.client}} | {date} |

**<Contents>**

## 1. ...
## 2. ...

---
{{profile.document.footer}}
```

- Header column names are fixed by the profile. Renaming a column is a Critical finding —
  the client's QMS tooling parses these.
- The footer appears exactly once, at the end.

## DS-02 — No automatic version bump

`{{profile.document.auto_version_bump}}` is `false`. Add a revision row **only** when the
user explicitly instructs it. Editing a document does not bump its version — the version
tracks client approval cycles, not edits.

## DS-03 — Section structure is fixed per category

Each design category defines its section skeleton in its own skill (`mig-screen-design`,
`mig-function-design`, …). Sections are neither reordered nor omitted; an unused section
carries an explicit "not applicable" line rather than disappearing.

## DS-04 — Scope discipline per section

Design documents leak implementation detail unless scope is policed:

| Section kind | Allowed | Forbidden |
|---|---|---|
| Screen behaviour | client-side behaviour visible to the user | route paths, component names, auth-guard wording, HTTP status codes, server validation, data-access object names |
| Function design | server-side processing, params, errors | UI colours, CSS, component names |
| Interface design | endpoint contract | UI behaviour, business rationale |

## DS-05 — No physical data names in prose

Physical column/field names (`ALL_CAPS_WITH_UNDERSCORES`, copybook names, `tbl_` prefixes)
are forbidden in document body prose and in user-facing item-name columns. Use the logical
name only. Physical names live exclusively in the data-design deliverable and in mapping
tables that exist to carry them.

Detection pattern: `[A-Z][A-Z0-9_]{2,}` that is not a document ID, module ID or MSG-ID.

## DS-06 — Table cell conventions

- One point per line inside a cell, separated by `<br>` — not by `;`, not by sentence
  punctuation.
- No sentence-ending punctuation in table cells outside message-text columns.
- Empty means "not applicable" only when the column defines it that way; otherwise write
  the explicit marker (`—`).

## DS-07 — Diagrams

- Tool: `{{profile.document.diagram_tool}}`, fenced code block, never an image file.
- Constraints from `{{profile.document.diagram_constraints}}` are hard limits — a diagram
  that will not render in the client's viewer is worthless.
- Processing flows: top-down flowchart. Error branches terminate in a node that names the
  MSG-ID.

## DS-08 — Language per directory

The language of a deliverable is determined by its directory
(`{{profile.language.by_path}}`), never by the language of the request. When a Vietnamese
request produces a Japanese deliverable, the deliverable is Japanese.

## DS-09 — Open Items section

Every P1–P3 deliverable ends with an **Open Items** table before the footer:

| # | Item | Kind | Raised | Status |
|---|---|---|---|---|
| 1 | ... | SPEC-GAP / BLOCKED / PROPOSAL / DECISION-NEEDED | YYYY/MM/DD | open |

An empty table is written as "None." — the section is never omitted. This is where NI-01
uncertainty and NI-04 blocked features land, and it is what the client reviews first.

## DS-10 — The project's own template outranks this skeleton

The pack ships no templates. Where the client supplies one and it is registered in
`{{profile.templates.registry}}`, **the template is authoritative over both DS-01 and the
category skill's section list** — its headings, its column names, its order, its approval
block. DS-01 then describes what the document must still *contain*, not what it must look
like.

Content the skill requires and the template cannot hold is a **template gap**: reported to
the document owner **once**, never resolved by inventing a section (DIO-01, DIO-02). This is
NI-02 applied to document form — a migration reproduces the client's form, it does not
improve it.

**The one thing a template cannot suspend is NI-01.** A form with no column for the legacy
reference does not excuse an unanchored statement: the anchors go in a section the form does
have, or in Open Items, and the missing column is reported as a gap. A deliverable with no
anchors is not a migration deliverable.

Where no template is registered, `{{profile.templates.on_missing}}` decides, and the run
report says which branch it took. `mig-document-io` owns the mechanics.

## DS-11 — Format follows the category, not the task

The output format is `{{profile.templates.registry}}[key].output_format`, or the template's
own format when that is empty. It is not chosen per request (DIO-05) — two formats for one
deliverable diverge within a week.

Two obligations for non-Markdown deliverables:

- **A binary deliverable carries a plain-text digest** under `{{profile.paths.reviews}}/digests/`,
  holding the values written **and their anchors** (DIO-07). Without it, an `.xlsx`
  deliverable sits outside every review, cross-check and gate the pack runs.
- **Round-trip fidelity**: writing changes nothing outside the filled fields — not a column
  width, not a merged range, not the print area (DIO-03).
