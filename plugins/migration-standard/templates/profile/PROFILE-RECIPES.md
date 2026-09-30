# Profile Recipes

Starting points for common migration shapes. Each recipe is an **overlay**: the fields a
migration of that kind gets wrong, or leaves at a default that does not fit, with the
reasoning behind each. Start from `migration.profile.yaml`, apply the overlay, then answer
the questions at the end — those are the ones the overlay cannot decide for you.

Two complete profiles already exist and are worth reading first:

| File | Shape |
|---|---|
| [`examples/wms.profile.yaml`](examples/wms.profile.yaml) | VB.NET desktop → .NET 9 + React, two surfaces, Japanese deliverables |
| [`examples/cobol-to-java.profile.yaml`](examples/cobol-to-java.profile.yaml) | mainframe COBOL → Java, green screens, copybooks |

**A recipe is not a decision.** It is a defensible default with its reason attached, so that
changing it is deliberate. The fields that matter most in a migration are the ones that
decide *what counts as a defect* — `mockup.fidelity`, `coexistence.system_of_record`,
`parallel_run.tolerance` — and none of them has a safe default you can adopt without reading.

---

## Recipe index

| # | Recipe | Use when |
|---|---|---|
| 1 | [Desktop client → web](#1--desktop-client--web) | VB.NET / Delphi / PowerBuilder / Access forms become a browser app |
| 2 | [Mainframe → open systems](#2--mainframe--open-systems) | COBOL / AS400 green screens and batch |
| 3 | [Lift and shift to cloud](#3--lift-and-shift-to-cloud) | the same application, somewhere else |
| 4 | [Monolith → services (strangler)](#4--monolith--services-strangler) | replaced a piece at a time, both live for months |
| 5 | [Legacy web → modern SPA](#5--legacy-web--modern-spa) | JSP / PHP / WebForms becomes React or equivalent |
| 6 | [Database replatform](#6--database-replatform) | Oracle → PostgreSQL, or similar; the application barely changes |
| 7 | [Japanese-market SI migration](#7--japanese-market-si-migration) | the client supplies 様式 forms and reads Japanese |

---

## 1 · Desktop client → web

The most common shape, and the one where the UI question dominates. A desktop form has
behaviour a browser does not give you free: modal dialogs, function keys, focus that never
leaves the keyboard, grids that page in memory.

```yaml
legacy:
  kind: vbnet                    # or delphi | powerbuilder | access
  screen_capture_dir: "docs/legacy-captures"

target:
  surfaces:
    - {id: PC, label: "Desktop browser", id_suffix: "PG", viewport: "1280x800+"}

mockup:
  kind: html
  fidelity: as-is                # operators keep their muscle memory, or the project fails UAT
  states_required: [normal, empty, loading, error, no-permission]

infrastructure:
  coexistence:
    strategy: phased             # per department or per site; both live for weeks
    system_of_record: legacy     # until each module cuts over
    user_routing: "<how an operator knows which system to open>"
  parallel_run:
    enabled: true
    compare: ["screen output", "report output", "database state"]

review:
  families: {screen: true, function: true, api: true, data: true}
```

**Why `as-is`.** The single most common cause of a rejected desktop-to-web migration is a
modernised UI. The users are not buying a better screen; they are buying the same work,
faster to maintain. Every layout improvement is a PROPOSAL in Open Items, priced separately.

**The four things a browser does not do the same way**, and which need a recorded decision
each, at P2, not during implementation:

| Legacy behaviour | The decision to record |
|---|---|
| Function keys (F1–F12) | which are reproduced, which become buttons, which are dropped |
| Modal dialogs that block everything | modal in the browser too, or inline? |
| Keyboard-only workflows, tab order | is tab order reproduced exactly? (`as-is` says yes) |
| Grids that load the whole table | server paging changes observable behaviour — agree the page size and the sort |

Each is a `DEC-*`, because each changes what UAT will accept.

**Questions:** whether the desktop client stays available during coexistence; whether the
client's staff are measured on throughput (if so, a slower screen is a defect, and that is an
`NFR`-shaped requirement in a pack that has no NFR category — record it as a `DEC-*` and an
IT case); whether printing is in scope, which it usually is and is usually forgotten.

---

## 2 · Mainframe → open systems

The oracle is excellent — COBOL says exactly what it does — and the UI oracle is a 24×80
character grid that cannot and should not be reproduced literally.

```yaml
legacy:
  kind: cobol
  logic_source: "src/legacy/cobol"
  db_source: "src/legacy/copybooks"
  screen_capture_dir: "docs/green-screens"

mockup:
  kind: html
  fidelity: restyled             # the ONE shape where as-is is usually wrong
  # Every screen that departs from the green-screen field order needs its decision here.
  fidelity_exceptions: []

templates:
  formats_enabled: [md, xlsx, docx, csv]

infrastructure:
  coexistence:
    strategy: parallel           # both process the same input for a whole cycle
    system_of_record: legacy
  data_migration:
    reconciliation: ["row counts per file/table", "control totals on every amount field",
                     "record counts by transaction type", "EBCDIC->UTF-8 spot checks"]
    rehearsals_required: 3
  parallel_run:
    enabled: true
    compare: ["batch output files", "report output", "database state"]
    tolerance: exact
    duration: "one full month-end cycle"
```

**Why `restyled` rather than `as-is`.** A green screen's layout is dictated by an 80-column
terminal. Reproducing it in a browser reproduces a constraint that no longer exists, and
users who were promised modernisation get a character grid with a mouse. What must be
preserved is the **field set, the field order and the flow** — which is what `restyled`
means. Anything beyond that is a per-screen decision.

**Batch is the real project.** Online screens are the visible part; the batch chain is where
the behaviour lives, and `compare: batch output files` is the highest-value line in this
profile. Two output files diffed byte for byte is the strongest parity evidence any migration
can produce — stronger than any test suite — and it is cheap.

**Three data hazards to name as `DEC-*` at P1**, because each changes computed results:
COMP-3 packed decimal precision and rounding; EBCDIC collation versus UTF-8 sort order
(reports come out in a different order, and that is visible to users); and signed-overpunch
fields read as text by anything that is not COBOL.

**Questions:** whether the copybooks are current with the files actually in production
(frequently not); whether the job scheduler is in scope; who can still read COBOL on the
client side, and for how long.

---

## 3 · Lift and shift to cloud

The application barely changes, so nearly all the risk is in this pack's infrastructure
section rather than its design categories.

```yaml
mockup:
  kind: none                     # a decision, stated, not an absence

paths:
  bd_categories:                 # most design categories have nothing to say here
    - {key: architecture, dir: "01.architecture", skill: mig_basic_design}
    - {key: data,         dir: "04.data-design",  skill: mig_data_design}
    - {key: interface,    dir: "05.interface-design", skill: mig_api_design}
    - {key: batch,        dir: "08.batch-design", skill: mig_batch_design}

review:
  families: {screen: false, function: false, api: true, data: true, batch: true}

infrastructure:
  iac:
    tool: terraform              # the deliverable of this project IS the IaC
    manual_changes_allowed: false
  coexistence:
    strategy: big-bang
    system_of_record: legacy
  data_migration:
    rehearsals_required: 3
    cutover_window: "<hours; this is the whole project plan>"
  rollback:
    target: legacy
    data_strategy: "<what happens to records created in the cloud after cutover>"
    rehearsed: false
  parallel_run:
    enabled: true
    compare: ["batch output files", "database state"]
```

**Why the categories shrink.** Screens and functions are unchanged by definition — writing
screen design documents for them produces paperwork nobody reads. What does change: every
integration point, every file share, every scheduled job, every hardcoded hostname, every
certificate, and every assumption about network latency between two components that used to
be in one rack.

**The design deliverable that matters is the architecture document**, and specifically the
integration inventory: for every external system, who calls whom, over what protocol, from
which network, with what timeout. That list is what breaks on cutover night.

**Questions:** whether the cutover window is fixed by the data volume or by the business (if
by the business, the rehearsal decides feasibility, and it should happen early); whether the
legacy hardware is decommissioned immediately or kept as the rollback target — keeping it is
the difference between a rehearsed rollback and a hopeful one.

---

## 4 · Monolith → services (strangler)

The shape with the longest coexistence, which means `infrastructure.coexistence` is not a
cutover detail here — it is the architecture.

```yaml
infrastructure:
  coexistence:
    strategy: strangler
    duration: "<months — be honest; it is always longer than planned>"
    system_of_record: per-module
    dual_write: true
    conflict_resolution: "<the rule, per table. Required — see IN-07>"
    router: "<reverse proxy / API gateway, and where its route table lives>"
    user_routing: "single entry point; the router decides — users see one system"
  parallel_run:
    enabled: true
    compare: ["screen output", "database state"]
  rollback:
    target: "previous target release"   # not legacy: legacy never went away
    data_strategy: "route the strangled paths back to the monolith"

change_request:
  cascade: [data, screen, function, interface, detail, mockup, report, file, batch,
            indexes, translations, test_cases]
```

**The router's route table is a deliverable**, versioned and reviewed like code. The failure
mode is not dramatic: someone adds a route to the monolith, the router does not know about
it, and traffic that should have been strangled quietly is not. Nobody notices until the two
systems disagree about a record.

**`dual_write: true` with `system_of_record: per-module` is the highest-risk configuration in
this entire pack.** It needs a written conflict rule per shared table, in the architecture
document, at P2. "We'll make sure only one side writes" is not a rule; it is an intention that
survives until the first urgent fix.

**Questions:** what the exit criterion is — the condition under which the monolith is finally
switched off, written down at the start, because a strangler with no exit criterion runs
forever; whether the shared database is also being split (if so, this is two migrations and
should be profiled as two); who owns the router.

---

## 5 · Legacy web → modern SPA

Deceptively easy: it is already a web application, so people assume the UI transfers. The
behaviour that does not transfer is the page lifecycle.

```yaml
legacy:
  kind: java-ee                  # or php
  ui_source: "src/legacy/WebContent"

target:
  surfaces:
    - {id: PC, label: "Desktop browser", id_suffix: "PG", viewport: "1280x800+"}
    - {id: MB, label: "Mobile web",      id_suffix: "MG", viewport: "375x812"}

mockup:
  kind: figma                    # a design team usually exists on this shape
  fidelity: restyled
  figma:
    writable: false
  surfaces: [PC, MB]

infrastructure:
  coexistence:
    strategy: strangler
    system_of_record: legacy
    router: "<reverse proxy by URL path>"
```

**What actually breaks**, and belongs in the screen design as explicit decisions: a
full-page-postback application has no client state, so every "keep the form values after an
error" behaviour was free and now is not; server-side session assumptions that a SPA's
parallel requests violate; browser-back behaviour that used to re-post and now does not; and
file upload/download flows built around form submission.

**Mobile is a scope decision, not a bonus.** Adding the `MB` surface doubles the screen-design
category and creates a second mockup set. If it is in scope, it is in the profile from the
start; if it is not, say so explicitly, because somebody will assume a responsive framework
makes it free.

**Questions:** whether the legacy authentication (container-managed, session cookies) can
coexist with the target's; whether SEO or deep links matter, which changes routing from a
detail into a requirement; whether the design team's Figma file predates the legacy analysis
(it usually does, and it usually contains screens that do not exist).

---

## 6 · Database replatform

The application is nearly unchanged, so the pack's design categories thin out and everything
concentrates in data design and parity.

```yaml
constraints:
  db_schema_frozen: false        # the schema IS the deliverable here
  stored_procedures_readonly: false

paths:
  bd_categories:
    - {key: architecture, dir: "01.architecture", skill: mig_basic_design}
    - {key: data,         dir: "04.data-design",  skill: mig_data_design}
    - {key: batch,        dir: "08.batch-design", skill: mig_batch_design}

mockup:
  kind: none

review:
  families: {screen: false, function: false, api: false, data: true, batch: true}

infrastructure:
  data_migration:
    reconciliation: ["row counts per table", "control totals on every numeric column",
                     "referential integrity", "collation-sensitive sort spot checks",
                     "NULL vs empty-string counts per nullable text column"]
    rehearsals_required: 3
  parallel_run:
    enabled: true
    compare: ["database state", "report output"]
    tolerance: exact
```

**This is the one recipe that unfreezes the schema**, which changes the pack's posture: LR-03
no longer applies, but LR-01 still does — the *source* database remains read-only.

**The defects in a replatform are all semantic**, and none of them raises an error:
empty string versus `NULL` (Oracle conflates them, most others do not); collation and case
sensitivity changing sort order and join results; date and timestamp precision and time
zones; numeric precision and rounding; identity/sequence gaps and reuse; and the behaviour of
`ORDER BY` on columns that were never deterministic.

Each of those is a `DEC-*` at P1 and a reconciliation check at cutover. The `NULL`-versus-
empty-string count per nullable text column is in the list above because it is the one that
silently changes query results in production, months later.

**Questions:** whether stored-procedure logic moves to the application or is ported in place;
whether the client has a performance baseline from the old platform (without one, "it got
slower" is unarguable in both directions); whether anything outside this project reads the
database directly — reports, extracts, another vendor's integration — because those break
silently.

---

## 7 · Japanese-market SI migration

The document set is larger than the code, the forms are contractual, and the client reads
Japanese. Combine with whichever of recipes 1–6 matches the technical shape.

```yaml
language:
  primary: ja
  working: vi
  by_path:
    - {path: "docs/**",    lang: ja}
    - {path: "docs-vi/**", lang: vi}
  dictionary: "docs/dictionary.csv"     # JP↔VN terms; without it the vocabulary drifts

templates:
  on_missing: ask                # the form is contractual; never invent one
  formats_enabled: [md, xlsx, docx, csv]
  template_wins_over_skill: true
  preserve_unfilled_structure: true
  legacy_documents_dir: "docs/legacy-documents"

document:
  date_format: "YYYY/MM/DD"
  revision_table_headers: ["版数", "日付", "改訂内容", "作成者", "承認者", "承認日"]

paths:
  bd_categories:                 # the client's numbering, not the pack's
    - {key: architecture, dir: "01.方式設計",          skill: mig_basic_design}
    - {key: screen,       dir: "02.画面設計",          skill: mig_screen_design}
    - {key: function,     dir: "03.機能設計",          skill: mig_function_design}
    - {key: data,         dir: "04.DB設計",            skill: mig_data_design}
    - {key: interface,    dir: "05.インタフェース設計", skill: mig_api_design}
    - {key: report,       dir: "06.帳票設計",          skill: mig_basic_design}
    - {key: file,         dir: "07.ファイル設計",       skill: mig_basic_design}
    - {key: batch,        dir: "08.バッチ設計",        skill: mig_batch_design}

mockup:
  kind: html
  fidelity: as-is
  dir: "docs/design/09.モックアップ"
  html:
    self_contained: true         # opened from a file share, offline, on a locked-down machine

review:
  families: {report: true, batch: true, file: true}

change_request:
  id_source: client
  min_options: 2
```

**Register every form before P2** (`/mig_template_register`), and let the fidelity check run
on the first file of each. These forms are usually grid-paper layouts (方眼紙) where one
logical field is a merged range — `mig_document_io` covers the hazards, but the check is what
proves the writer handled *your* forms.

**Check every form has somewhere to record the `LEG-*` anchor.** Many client forms do not
have an anchor column, because they were designed for new development rather than migration.
That does not suspend NI-01: the anchors go in a section the form does have, or in Open
Items, and the missing column is reported as a template gap — once, at registration.

**`report` and `file` review families go on.** They are off by default in the pack and this
market always has both, and they are the two categories a long generation run drops silently.

**Questions:** which categories the client actually orders; whether the Vietnamese copy is a
deliverable or a working aid; whether the client's 変更履歴 lives on a separate sheet (common,
and it changes how `mig_document_io` writes the revision row); whether the legacy documents
they hand over are current — they are not, and DIO-08 is the rule that keeps that from
becoming your problem at parallel run.

---

## Applying a recipe

1. Copy `migration.profile.yaml` to `.claude/migration.profile.yaml`.
2. Apply the overlay. Keep every field the overlay does not mention.
3. Answer the recipe's closing questions — those are the real decisions, and `/mig_init` will
   ask about them anyway.
4. Run `/mig_profile_check`. Fix every Critical before running a phase.
5. **Record the deviations as decisions.** A recipe that set `fidelity: restyled` or
   `dual_write: true` made a choice with a cost. It belongs in the project's decision record
   with its reason — not as an unexplained difference from the template that the next person
   quietly reverts.

## Writing a new recipe

The useful unit is the **overlay plus the reasons**, not a whole profile — a 300-line YAML
with four meaningful differences buried in it teaches nobody anything. State what is
distinctive about the shape in one sentence, list the fields that change with a reason each,
name the failure mode that shape is prone to, and end with the questions the overlay cannot
answer.
