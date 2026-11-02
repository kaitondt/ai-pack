# RULE FAMILY: ID NAMING

Deterministic IDs are what make traceability mechanical instead of editorial.

## ID-01 — Canonical document ID

Format: `{{profile.ids.doc_id_format}}` → `{MODULE}-{TYPE}-{NNN}`

| Segment | Source | Example |
|---|---|---|
| `MODULE` | must match `{{profile.ids.module_pattern}}` | `XX0000PG` |
| `TYPE` | one of `{{profile.ids.types}}` | `SC`, `FC`, `API`, `DD` |
| `NNN` | zero-padded to `{{profile.ids.number_width}}` | `001` |

`{MODULE}-SC-{NNN}`, `{MODULE}-FC-{NNN}`, `{MODULE}-API-{NNN}`.

## ID-02 — Module base and surface suffix

A module ID ends with a surface suffix from `{{profile.target.surfaces[].id_suffix}}`.
`MODULE_BASE` is the module ID with that suffix stripped.

`XX0000PG` → base `XX0000`, surface `PC`.

Message IDs use the **base**, so the desktop and handheld variants of one screen share a
message catalogue: `MSG-{MODULE_BASE}-{NNN}`.

## ID-03 — Message ID format

Format: `{{profile.ids.message_id_format}}`

Common failure modes, all Critical:
- wrong number width (`MSG-{MODULE_BASE}-{NN}`)
- surface suffix left in (`MSG-{MODULE}-{NNN}`)
- module prefix truncated (`MSG-{MODULE_BASE minus last char}-{NNN}`)

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

`検索機能（{MODULE}-FC-{NNN}）` · `Item search ({MODULE}-FC-{NNN})`

One punctuation style per document. Do not mix full-width and half-width parentheses, and
do not mix `/` and `・` for the same phrase family.

## ID-07 — Filenames carry the ID

Deliverable filenames embed the document ID so a file is locatable from any reference:

```
{category}({ID}_{short-name}).md      e.g.  screen-design({MODULE}-SC-{NNN}_item-list).md
```

Keep the exact convention in the profile-driven category directory; the invariant is that
**the ID appears in the filename**.
