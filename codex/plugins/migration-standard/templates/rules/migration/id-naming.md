# RULE FAMILY: ID NAMING

Deterministic IDs are what make traceability mechanical instead of editorial.

## ID-01 — Canonical document ID

Format: `{{profile.ids.doc_id_format}}` → `{MODULE}-{TYPE}-{NNN}`

| Segment | Source | Example |
|---|---|---|
| `MODULE` | must match `{{profile.ids.module_pattern}}` | `KK0030PG` |
| `TYPE` | one of `{{profile.ids.types}}` | `SC`, `FC`, `API`, `DD` |
| `NNN` | zero-padded to `{{profile.ids.number_width}}` | `001` |

`KK0030PG-SC-001`, `KK0030PG-FC-012`, `CLM101W-API-003`.

## ID-02 — Module base and surface suffix

A module ID ends with a surface suffix from `{{profile.target.surfaces[].id_suffix}}`.
`MODULE_BASE` is the module ID with that suffix stripped.

`KK0030PG` → base `KK0030`, surface `PC`.

Message IDs use the **base**, so the desktop and handheld variants of one screen share a
message catalogue: `MSG-KK0030-001`.

## ID-03 — Message ID format

Format: `{{profile.ids.message_id_format}}`

Common failure modes, all Critical:
- wrong number width (`MSG-KK0030-01`)
- surface suffix left in (`MSG-KK0030PG-001`)
- module prefix truncated (`MSG-K0030-001`)

System-wide messages use a reserved base (`MSG-COMMON-NNN`) and must **not** appear in a
module's own message table — reference them, do not copy them.

## ID-04 — Numbering discipline

- Numbers are assigned in document order, ascending, no gaps at creation time.
- Gaps that appear later (an item removed after client review) stay as gaps. Do not
  compact.
- Counters that span subsections run **continuously** across those subsections; they do
  not restart at each subsection heading.

## ID-05 — IDs are never translated or localised

In every language variant of a document, IDs stay byte-identical. Same for table names,
column names, stored-procedure names, file paths and URLs — see
`{{profile.language.immutable_tokens}}`.

## ID-06 — Cross-reference notation

Reference another artifact as `Logical name (ID)` — the human name first, the ID in
parentheses, using the punctuation style mandated by the document language.

`入荷予定検索機能（KK0030PG-FC-001）` · `Receiving search (KK0030PG-FC-001)`

One punctuation style per document. Do not mix full-width and half-width parentheses, and
do not mix `/` and `・` for the same phrase family.

## ID-07 — Filenames carry the ID

Deliverable filenames embed the document ID so a file is locatable from any reference:

```
{category}({ID}_{short-name}).md      e.g.  screen-design(KK0030PG-SC-001_receiving-list).md
```

Keep the exact convention in the profile-driven category directory; the invariant is that
**the ID appears in the filename**.
