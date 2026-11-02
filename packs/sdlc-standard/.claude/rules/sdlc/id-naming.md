# RULE FAMILY: ID NAMING

Deterministic IDs are what make traceability mechanical instead of editorial.

## ID-01 — Canonical document ID

Format: `{{profile.ids.doc_id_format}}` → `{MODULE}-{TYPE}-{NNN}`

| Segment | Source | Example |
|---|---|---|
| `MODULE` | must match `{{profile.ids.module_pattern}}` | `XX0000PG` |
| `TYPE` | one of `{{profile.ids.types}}` | `SC`, `FC`, `API`, `DT`, `DD` |
| `NNN` | zero-padded to `{{profile.ids.number_width}}` | `001` |

`{MODULE}-SC-{NNN}`, `{MODULE}-FC-{NNN}`, `{MODULE}-API-{NNN}`.

## ID-02 — Requirement ID families

| Family | Format | Issued at | Owner |
|---|---|---|---|
| Business requirement | `{{profile.ids.business_requirement_id_format}}` | P0 | business owner |
| Functional requirement | `{{profile.ids.requirement_id_format}}` | P1 | product owner |
| Non-functional requirement | `{{profile.ids.nfr_id_format}}` | P1 | architect |
| Assumption | `{{profile.ids.assumption_id_format}}` | any | a named person |
| Decision | `{{profile.ids.decision_id_format}}` | any | the decider |
| Risk | `{{profile.ids.risk_id_format}}` | any | the risk owner |

`{AREA}` is a business area, agreed once at P0 and never redefined. It is the batching
unit for every generation run, so pick areas of roughly comparable size.

`{CATEGORY}` for NFRs is fixed: `PERF`, `SEC`, `AVAIL`, `OPS`, `USE`, `COMPL`. A new
category is a profile change, not an ad-hoc choice in one document.

## ID-03 — Module base and surface suffix

A module ID ends with a surface suffix from `{{profile.system.surfaces[].id_suffix}}`.
`MODULE_BASE` is the module ID with that suffix stripped.

`XX0000PG` → base `XX0000`, surface `PC`.

Message IDs use the **base**, so the desktop and mobile variants of one screen share a
message catalogue: `MSG-{MODULE_BASE}-{NNN}`.

## ID-04 — Message ID format

Format: `{{profile.ids.message_id_format}}`

Common failure modes, all Critical:
- wrong number width (`MSG-{MODULE_BASE}-{NN}`)
- surface suffix left in (`MSG-{MODULE}-{NNN}`)
- module prefix truncated (`MSG-{MODULE_BASE minus last char}-{NNN}`)

System-wide messages use a reserved base (`MSG-COMMON-NNN`) and must **not** be copied
into a module's own message table — reference them.

## ID-05 — Test and defect IDs

| Level | Format | Keyed by |
|---|---|---|
| Unit | `{{profile.ids.test_id_format.unit}}` | module — UT verifies detail design |
| Integration | `{{profile.ids.test_id_format.integration}}` | flow — IT verifies interaction, not one module |
| System | `{{profile.ids.test_id_format.system}}` | scenario — ST verifies a business process |
| Acceptance | `{{profile.ids.test_id_format.acceptance}}` | flat sequence — the client's list |
| Defect | `{{profile.ids.defect_id_format}}` | flat sequence, project-wide |
| Incident | `{{profile.ids.incident_id_format}}` | year-scoped, post-release |

The key differs per level on purpose: it forces the case set to be organised the way the
level actually verifies. An IT suite numbered per module is a UT suite that runs late.

## ID-06 — Numbering discipline

- Numbers are assigned in document order, ascending, no gaps at creation time.
- Gaps that appear later (an item removed after review) stay as gaps. Do not compact.
- Counters that span subsections run **continuously** across those subsections; they do
  not restart at each subsection heading.

## ID-07 — IDs are never translated or localised

In every language variant of a document, IDs stay byte-identical. Same for table names,
column names, API paths, field names, file paths and URLs — see
`{{profile.language.immutable_tokens}}`.

## ID-08 — Cross-reference notation

Reference another artifact as `Logical name (ID)` — the human name first, the ID in
parentheses, using the punctuation style mandated by the document language.

`Order search ({MODULE}-FC-{NNN})` · `受注検索機能（{MODULE}-FC-{NNN}）`

One punctuation style per document. Do not mix full-width and half-width parentheses.

## ID-09 — Filenames carry the ID

Deliverable filenames embed the document ID so a file is locatable from any reference:

```
{category}({ID}_{short-name}).md      e.g.  function-design({MODULE}-FC-{NNN}_order-search).md
```

Keep the exact convention in the profile-driven category directory; the invariant is that
**the ID appears in the filename**.
