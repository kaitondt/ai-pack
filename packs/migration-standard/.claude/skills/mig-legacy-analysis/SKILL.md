---
name: mig-legacy-analysis
description: "P0 — legacy system analysis. Builds the LEG-* artifact catalogue, extracts business rules, messages, validations and data access from legacy source, and produces the legacy inventory. Kind-specific heuristics for VB.NET, COBOL, Delphi, PHP, Java-EE, PowerBuilder, Access. Load for ALL legacy reverse-engineering tasks."
---

# P0 — Legacy Analysis

> Prerequisite: `mig-project` loaded, profile resolved.
> Everything under `{{profile.legacy.root}}` is **read-only** (LR-01).

The output of this phase is the evidence base for the entire project. Everything written
later cites it.

---

## Deliverables

| File | Content |
|---|---|
| `{{profile.paths.requirements}}/legacy-inventory.md` | one row per legacy artifact with its `LEG-*` id |
| `{{profile.paths.requirements}}/requirement.md` | extracted behaviour, organised by business area |
| `{{profile.paths.traceability}}` | `LEG-*` rows seeded, `status: todo` |

---

## The four extraction passes

Run in order. Each pass depends on the previous one's catalogue.

### Pass 1 — Inventory (breadth, no depth)

Walk `{{profile.legacy.ui_source}}`, `{{profile.legacy.logic_source}}`,
`{{profile.legacy.db_source}}`. For each artifact record:

| Column | Notes |
|---|---|
| `LEG-{AREA}-{NNN}` | assigned here, permanent (ID-04, TR-04) |
| Artifact | path, relative to legacy root |
| Kind | screen / logic module / data object / report / batch / shared |
| Business area | the grouping used for `{AREA}` |
| Entry points | what invokes it |
| Size | lines, or field count for screens |
| Reachable | yes / **no** → candidate BLOCKED (NI-04) |
| Scope | in / excluded (+ reason) |

Do not read implementation detail in this pass. Breadth first; it prevents the
depth-first trap of over-analysing module 1 while module 40 is undiscovered.

### Pass 2 — Screen and interaction extraction

Per screen artifact, extract exactly what the source says:

- every control: name, label text, type, initial state, enabled/visible logic
- tab order and initial focus
- every event handler and what it calls
- grid/list definitions: column order, header text, widths, sort
- navigation: what opens it, what it opens, what it returns
- the **enable/disable matrix** — which controls are active in which mode

The enable/disable matrix is where blocked features are found. A control disabled in every
branch is a BLOCKED candidate: record it, mark it, and escalate per NI-04.

### Pass 3 — Business rule and message extraction

- validation rules, with the exact condition and the exact message
- message catalogue: verbatim text, including odd spacing and typos (NI-03)
- calculations: the exact expression, including rounding and truncation
- state machines: statuses and the transitions between them
- authorisation: who may do what, and where that is checked

Record each with an anchor `path:line`. A rule without an anchor is not a finding.

### Pass 4 — Data access

- every data object touched, and the operation (read / insert / update / delete)
- stored procedure or embedded SQL, with parameters and result shape
- transaction boundaries
- implicit ordering — a query without `ORDER BY` whose output order matters is a defect
  waiting to happen in the target; flag it

---

## Kind-specific heuristics

Selected by `{{profile.legacy.kind}}`.

| Kind | Screens live in | Logic lives in | Watch out for |
|---|---|---|---|
| `vbnet` | `*.Designer.vb` (controls), `*.vb` (handlers) | code-behind, modules | control state set in several handlers; `Visible=False` set at design time and never re-set |
| `cobol` | BMS/MFS map definitions | `*.cbl` + copybooks | `COMP-3` precision, signed overpunch, `GO TO` flow, level-88 conditions |
| `delphi` | `*.dfm` | `*.pas` | component events wired in the form file, not the unit |
| `php` | templates mixed with logic | same files | logic duplicated across pages; include-order dependencies |
| `java-ee` | JSP/JSF pages | servlets, EJBs | XML-configured navigation; interceptors adding hidden behaviour |
| `powerbuilder` | `*.srw` | `*.srw`, `*.sru` | DataWindow definitions carry validation and format the code never mentions |
| `access` | forms | VBA modules, macros | query objects hold business logic; macros hide flow |

For a kind not listed: identify the three roots (UI definition, logic, data) and apply the
four passes unchanged.

---

## Rules

- **A0 — anchors always.** Every claim carries `path:line`. This is what P1–P7 cite.
- **A1 — quote, do not paraphrase, for messages and expressions.**
- **A2 — unreachable ≠ unimportant.** Catalogue dead code as dead; do not omit it. The
  client may know why it is there.
- **A3 — contradictions get reported, not resolved.** Two sources disagreeing is a
  finding (NI-05).
- **A4 — no target-side design.** P0 describes the old system only. Do not propose the
  new screen, the new API, or the new schema here.
- **A5 — exclusions need reasons.** Anything scoped out goes to
  `{{profile.legacy.excluded}}` with a written reason (P0 gate).

---

## Exit gate

- [ ] every in-scope artifact has a `LEG-*` id
- [ ] every excluded artifact has a reason
- [ ] every BLOCKED candidate escalated and answered
- [ ] message catalogue complete and verbatim
- [ ] `{{profile.paths.traceability}}` seeded with all `LEG-*` rows
