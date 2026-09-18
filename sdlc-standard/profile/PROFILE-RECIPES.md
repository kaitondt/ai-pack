# Profile Recipes

Starting points for common project shapes. Each recipe is an **overlay**: the fields that a
project of that kind gets wrong or leaves at a default that does not fit, with the reasoning
behind each one. Start from `sdlc.profile.yaml`, apply the overlay, then answer the
questions at the end of the recipe — those are the ones the overlay cannot decide for you.

Two complete profiles already exist and are worth reading first, because a recipe assumes
you have seen a whole one:

| File | Shape |
|---|---|
| [`examples/saas-webapp.profile.yaml`](examples/saas-webapp.profile.yaml) | internal product, agile-with-gates, one language, Markdown deliverables, GitHub + AWS |
| [`examples/enterprise-waterfall.profile.yaml`](examples/enterprise-waterfall.profile.yaml) | offshore fixed-price, hard gates, JP/VN deliverables in Excel, Azure Repos + on-prem, client-owned infra |

**A recipe is not a decision.** It is a defensible default with its reason attached, so that
changing it is a deliberate act. Copying one without reading the reasons produces the same
problem as copying the quality targets: numbers nobody agreed to.

---

## Recipe index

| # | Recipe | Use when |
|---|---|---|
| 1 | [Japanese-market SI, Excel deliverables](#1--japanese-market-si-excel-deliverables) | the client supplies 様式 forms and reads Japanese |
| 2 | [Regulated financial system](#2--regulated-financial-system) | an auditor will read your evidence |
| 3 | [Healthcare / patient data](#3--healthcare--patient-data) | the system touches health records |
| 4 | [Public-sector tender](#4--public-sector-tender) | the contract and the acceptance criteria were written before you bid |
| 5 | [Mobile application](#5--mobile-application) | a store review sits between "done" and "released" |
| 6 | [Data platform / batch-heavy](#6--data-platform--batch-heavy) | most of the system has no screens |
| 7 | [Small team, internal tool](#7--small-team-internal-tool) | three people, six weeks, and the pack must not become the project |

---

## 1 · Japanese-market SI, Excel deliverables

The shape this pack was hardest to get right for, and the most common one in offshore
delivery. The distinguishing facts: the client owns the document forms, the forms are Excel,
the forms are contractual, and the deliverable set is larger than the code.

```yaml
project:
  delivery_model: waterfall
  contract_type: fixed-price

language:
  primary: ja
  working: vi                    # the team converses in Vietnamese, delivers in Japanese
  by_path:
    - path: "docs/**"
      lang: ja
    - path: "docs-vi/**"
      lang: vi
  dictionary: "docs/dictionary.csv"     # JP↔VN term table; without it the terms drift

templates:
  on_missing: ask                # never invent a form; the form is contractual
  formats_enabled: [md, xlsx, docx, csv]
  # One registry entry per 様式 the client sent. header_rows covers their standard
  # header block (document id, system name, author, approval stamps).
  template_wins_over_skill: true
  preserve_unfilled_structure: true

document:
  date_format: "YYYY/MM/DD"
  revision_table_headers: ["版数", "日付", "改訂内容", "作成者", "確認者", "承認者", "承認日"]

paths:
  bd_categories:                 # the client's category numbering, not the pack's
    - {key: architecture, dir: "01.方式設計",        skill: sdlc_basic_design}
    - {key: nfr,          dir: "02.非機能設計",      skill: sdlc_nfr_design}
    - {key: screen,       dir: "03.画面設計",        skill: sdlc_screen_design}
    - {key: function,     dir: "04.機能設計",        skill: sdlc_function_design}
    - {key: data,         dir: "05.DB設計",          skill: sdlc_data_design}
    - {key: interface,    dir: "06.インタフェース設計", skill: sdlc_api_design}
    - {key: report,       dir: "07.帳票設計",        skill: sdlc_basic_design}
    - {key: batch,        dir: "08.バッチ設計",      skill: sdlc_batch_design}

mockup:
  kind: html
  html:
    self_contained: true         # opened from a file share, offline, by a reviewer with no toolchain

review:
  families: {report: true, batch: true}   # 帳票 and バッチ are real categories here

change_request:
  id_source: client
  require_estimate: true
```

**Why each of these.** `on_missing: ask` because a deliverable in the wrong form is rejected
whole, and rejection arrives after the category is finished. `report` and `batch` review
families on, because they are the two categories the pack ships off by default and the two
this market always has. `self_contained` mockups because the reviewer opens them from a
network share on a locked-down machine. `dictionary` because JP↔VN term drift is invisible
to both sides until a reviewer sees two words for one table.

**Run `/sdlc_template_register` before P2, not during it.** Register every form, and let the
fidelity check run on the first file of each. Excel forms in this market are usually
grid-paper layouts (方眼紙) where one logical field spans a merged range — `sdlc_document_io`
covers the hazards, but the check is what tells you the writer handled *your* forms.

**Questions the recipe cannot answer:** which categories the client actually orders (not
every project has 帳票); whether the Vietnamese copy is a deliverable or a working aid;
whether the client's numbering restarts per subsystem.

---

## 2 · Regulated financial system

The distinguishing fact: someone outside the project will read your evidence, months later,
and they are entitled to an answer.

```yaml
project:
  delivery_model: waterfall

stakeholders:
  approvers: ["Compliance Officer (NFR-COMPL-*)", "Information Security Officer (NFR-SEC-*)"]

quality:
  targets:
    phase_containment: ">= 90% of defects found in the phase that injected them"
    escaped_defects: "< 2% of all defects first found in UAT"
  injection_phases: [P1, P2, P3, P4, P5, P6, P7, P8]

constraints:
  baseline_change_requires_cr: true
  production_change_via_release_only: true

maintenance:
  hotfix:
    allowed: true
    approval: "ops_owner + product_owner + compliance officer"
    retro_documentation_days: 2      # short, because an undocumented prod change is a finding
  rca_required_for: [S1, S2, S3]

infrastructure:
  iac:
    manual_changes_allowed: false    # a console change is an audit finding
  secrets:
    rotation_policy: "90 days, evidenced"
  observability:
    nfr_monitors_required: true

testing:
  evidence:
    required_for: ["IT", "ST", "UAT"]   # not just the last two
```

**Why.** The two quality targets tighten because the cost of an escape is not re-work, it is
a regulatory conversation. Evidence extends down to IT because an auditor asks "show me the
test that proves this control works", and an IT result with no evidence cannot answer.
Hotfix retro-documentation shortens to two days because the gap between the change and its
record is exactly the window an audit will ask about.

Add an `NFR-COMPL-*` for each obligation you are actually under, with the clause reference as
its source (RS-01) — not "PCI-DSS compliance" as one requirement, which is not testable and
cannot be gated.

**Questions:** which specific standard and which of its clauses apply to *this* system;
whether the auditor accepts your evidence format; who signs the acceptance record.

---

## 3 · Healthcare / patient data

Regulated, plus a data class that makes ordinary practices unsafe.

Start from Recipe 2, then:

```yaml
scope:
  out_of_scope:
    - item: "<anything touching a class of record you are not cleared for>"
      reason: "<the clearance you do not have>"

testing:
  uat:
    executed_by: client
    # UAT data is the hazard: the client will want to use real records.
    entry_signoff_required: true

infrastructure:
  hosting:
    regions: []                  # data residency is a requirement, not a deployment detail
```

Then three rules that are not profile fields and must be written into the project's own
`<key>_*` skill or `CLAUDE.md`:

1. **No real patient data outside the production environment**, including UAT, including
   "just one record to reproduce the bug", including screenshots attached as test evidence.
   Masked or synthetic, always. This is the rule every healthcare project breaks first, and
   it breaks during defect investigation, under time pressure.
2. **Data residency is an `NFR-COMPL-*`** with a measurable target, not an infrastructure
   preference. It constrains hosting regions, backup destinations, log shipping and the
   support model.
3. **Access to production is itself audited.** Whoever investigates an incident leaves a
   record of what they looked at.

**Questions:** which jurisdiction's rules apply and whether more than one does; whether the
client's own environments are already accredited; what the breach-notification obligation is
and who owns it.

---

## 4 · Public-sector tender

The distinguishing fact: the acceptance criteria were written before you bid, by someone who
is not on the project, and they will be read literally.

```yaml
project:
  delivery_model: waterfall
  contract_type: fixed-price

scope:
  # Quote the tender's own wording. Paraphrasing it here is how a dispute starts.
  in_scope: ["<verbatim from the tender>"]
  out_of_scope:
    - item: "<verbatim exclusion>"
      reason: "<tender clause reference>"

change_request:
  id_source: client
  min_options: 2
  require_estimate: true
  gates: ["after_options", "after_design"]

gates:
  P8_uat:
    exit:
      - "every acceptance criterion in the tender has an executed UAT case with a verdict"
      - "acceptance recorded with approver and date"
      - "every deferred item has a written, signed deferral"

document:
  require_review_record: true
```

**Why.** The P8 exit criterion is rewritten to point at the **tender's** acceptance criteria
rather than the SRS, because those are what acceptance is measured against and they are
frequently broader. Map each tender criterion to a `BR-*` at P0 — the mapping table is the
single most valuable artifact on this kind of project, and it is cheap at P0 and impossible
at P8.

`min_options: 2` with a mandatory estimate, because under a fixed-price public contract every
change is a variation with a price, and presenting one option is presenting a bill.

**Questions:** whether the tender's criteria are testable as written (usually several are
not — that is an open question at P0, raised in writing); who on the client side can
actually approve a variation; what the liquidated-damages clause keys off.

---

## 5 · Mobile application

The distinguishing fact: between "released" and "available" sits a store review you do not
control, and a population of users on versions you cannot retire.

```yaml
system:
  surfaces:
    - {id: IOS, label: "iOS phone",     id_suffix: "IO", viewport: "390x844"}
    - {id: AND, label: "Android phone", id_suffix: "AN", viewport: "412x915"}
  environments:
    - {id: local,   purpose: "development", data: "synthetic"}
    - {id: test,    purpose: "UT / IT",     data: "synthetic"}
    - {id: staging, purpose: "ST", data: "masked production-like", production_like: true}
    - {id: beta,    purpose: "UAT via TestFlight / Play internal testing", data: "client-prepared"}
    - {id: prod,    purpose: "live", data: "live"}

mockup:
  kind: figma                    # the design team owns it; this pack reads and checks
  surfaces: [IOS, AND]
  figma:
    writable: false

infrastructure:
  cd:
    strategy: pipeline-triggered
    approval_required_for: [beta, prod]
    deployment_pattern: canary   # staged rollout is the only rollback that works

testing:
  viewpoints:
    - VP-01  # happy path
    - VP-02  # empty / no result
    - VP-03  # validation
    - VP-04  # authentication and session
    - VP-05  # repeated or concurrent submission
    - VP-06  # server / network / dependency failure  <- offline and flaky network live here
    - VP-07  # cross-module navigation and state carry-over
    - VP-08  # permission and role  <- OS permissions too: camera, location, notifications
    - VP-09  # layout, rendering and responsive integrity
    - VP-10  # data hazards
```

**Why.** Two surfaces, always, with their own id suffixes — an iOS-only screen design that
gets "adapted" for Android without its own document is the most common source of divergence.
`figma` read-only because the design team owns the file and an edit made from a build tool is
invisible to them (`sdlc_mockup`). Canary deployment because **there is no rollback on
mobile**: you cannot un-ship a version, you can only ship another one and wait, which is why
the staged rollout is the release plan rather than a refinement of it.

Two things to write into the project's own rules, because no profile field covers them:

- **Backward compatibility is a requirement.** Old app versions keep calling your API for
  months. Every API change states which app versions it must keep working, and that is an
  `NFR-COMPL-*` with an ST case.
- **Store review is a release step with an unpredictable duration.** It belongs in the
  cutover plan (`sdlc_release`), with what happens if it is rejected.

**Questions:** minimum OS versions, and whether that is a requirement or an assumption;
whether the client's UAT can run on TestFlight/internal testing; who owns the store accounts.

---

## 6 · Data platform / batch-heavy

The distinguishing fact: most of the system has no screens, so the categories the pack
defaults to are the wrong ones.

```yaml
paths:
  bd_categories:
    - {key: architecture, dir: "01.architecture",     skill: sdlc_basic_design}
    - {key: nfr,          dir: "02.non-functional",   skill: sdlc_nfr_design}
    - {key: data,         dir: "03.data-design",      skill: sdlc_data_design}
    - {key: batch,        dir: "04.pipeline-design",  skill: sdlc_batch_design}
    - {key: interface,    dir: "05.interface-design", skill: sdlc_api_design}
    - {key: screen,       dir: "06.screen-design",    skill: sdlc_screen_design}  # small, often admin only

mockup:
  kind: none                     # a decision, stated, not an absence

review:
  families:
    batch: true
    screen: false                # turn it back on if the admin UI is real
    report: true

quality:
  size_unit: function-point      # KLOC measures the wrong thing when the work is SQL and config

testing:
  system_test:
    scenario_source: "end-to-end data journey: ingest -> transform -> publish -> reconcile"
    includes: ["regression", "performance", "data volume", "failover", "operability", "reconciliation"]
```

**Why.** Data design moves to the front because everything else is derived from it. `batch`
becomes the largest category, and its review family goes on. ST scenarios are data journeys
rather than screen flows — an ST suite that re-tests field validation on the admin screen has
paid for coverage it already had and still has no case for the month-end run.

Three obligations to write into the project's rules:

- **Reconciliation is a requirement, not an operational habit**: row counts, control totals,
  and what happens when they disagree.
- **Restart and rerun semantics are designed, not discovered.** An operator will need them at
  03:00 and the design is the only thing that will answer (`rules/common/performance.md`).
- **Late and duplicate source data** is a normal case with a specified behaviour, not an
  error branch nobody wrote.

**Questions:** who owns each source system and what their change process is; whether
historical reprocessing is in scope; what the data-retention obligation is per dataset.

---

## 7 · Small team, internal tool

The distinguishing fact: the pack can cost more than the project. This recipe is about
deciding what to switch off **deliberately**, so that what is left is actually done.

```yaml
project:
  delivery_model: agile-with-gates
  contract_type: internal

templates:
  on_missing: skeleton           # agreed: the pack's structure is this team's structure (DEC-xxx)
  formats_enabled: [md, csv]

mockup:
  kind: html                     # or none; decide and record it

paths:
  bd_categories:                 # four, not eight
    - {key: architecture, dir: "01.architecture",     skill: sdlc_basic_design}
    - {key: screen,       dir: "02.screen-design",    skill: sdlc_screen_design}
    - {key: data,         dir: "03.data-design",      skill: sdlc_data_design}
    - {key: interface,    dir: "04.interface-design", skill: sdlc_api_design}

review:
  families: {nfr: true, batch: false, report: false}

testing:
  levels:                        # three, not four: ST and UAT collapse into one
    - {id: UT,  phase: P5, basis: detail_design, environment: test,    owner: developer}
    - {id: IT,  phase: P6, basis: design_root,   environment: test,    owner: developer}
    - {id: UAT, phase: P8, basis: requirements,  environment: staging, owner: business_owner}
  rounds:
    count: 1
```

**What must not be switched off**, whatever the size of the project:

| Keep | Because |
|---|---|
| `requirement-sourcing` | an internal project has *fewer* written requirements, not more, so the anchor discipline matters more |
| the traceability register | it is the only thing that answers "is this done?", and it cannot be reconstructed |
| `constraints.baseline_change_requires_cr` | even if the "CR" is a line in a decision log, the door has to close somewhere |
| phase gates P1 and P8 | the two decisions worth making formally: what we agreed to build, and whether it is accepted |
| `quality.targets.escaped_defects` | the one metric a small team can actually act on |

**What legitimately goes:** detail design as a document (when the code is the detail design,
record that as a `DEC-*` and let P3's gate assert "no DD needed" per module); the
formal ST phase; the second test round; the report and batch categories; the review families
you do not have artifacts for.

**Questions:** whether "internal" will stay internal — the most expensive version of this
recipe is the project that quietly becomes a product and keeps the lightweight profile.

---

## Applying a recipe

1. Copy `sdlc.profile.yaml` to `.claude/sdlc.profile.yaml`.
2. Apply the overlay. Keep every field the overlay does not mention.
3. Answer the recipe's closing questions — those are the real decisions, and they are the
   ones `/sdlc_init` will ask about anyway.
4. Run `/sdlc_profile_check`. Fix every Critical before running a phase.
5. **Record the deviations as decisions.** A recipe that turned off the ST phase or set
   `on_missing: skeleton` made a choice; it belongs in `{{profile.paths.decision_log}}` as a
   `DEC-*` with its reason, not as an unexplained difference from the template that the next
   person will quietly revert.

## Writing a new recipe

If your project shape is not here, the useful unit is the **overlay plus the reasons**, not a
whole profile — a 500-line YAML file with three meaningful differences buried in it teaches
nobody anything. State what is distinctive about the shape in one sentence, list the fields
that change, give a reason per field, and end with the questions the overlay cannot answer.
