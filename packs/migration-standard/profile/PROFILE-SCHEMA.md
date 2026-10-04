# `migration.profile.yaml` — Field Specification

The profile is the **only** file a new migration project must author before the pack
becomes operational. Skills read it through the `mig-project` skill and substitute
`{{profile.<dotted.path>}}` tokens.

Canonical location: `<repo-root>/.claude/migration.profile.yaml`

---

## Resolution contract

| Token form | Resolves to |
|---|---|
| `{{profile.target.stack.backend}}` | scalar value |
| `{{profile.paths.design_root}}` | path string, repo-relative |
| `{{profile.ids.types.screen}}` | `SC` |
| `{{profile.surface(PC).id_suffix}}` | list lookup by `id` |

**If a token cannot be resolved, STOP.** Do not guess a value and do not proceed with a
placeholder in a generated deliverable. Report the missing field and ask.

---

## Sections

### `project`
| Field | Required | Notes |
|---|---|---|
| `key` | ✅ | 2–5 uppercase chars. Appears in report filenames. |
| `name` | ✅ | Display name in document titles. |
| `vendor` / `client` | ✅ | Fill the Author / Approver columns of every revision-history table. |
| `copyright` | ✅ | Rendered as the footer of every deliverable. |
| `start_date` | ✅ | Anchors "as of" statements; converts relative dates to absolute. |

### `legacy`
| Field | Required | Notes |
|---|---|---|
| `kind` | ✅ | Selects the analysis heuristics in `mig-legacy-analysis`. |
| `root` | ✅ | Everything under it is read-only. |
| `ui_source` / `logic_source` / `db_source` | ✅ | The three locator roots. `/mig-analyze-legacy` builds its map from these. |
| `readonly` | ✅ | **Must be `true`.** A profile with `readonly: false` is rejected by `/mig-profile-check`. |
| `excluded[]` | — | Legacy artifacts deliberately not migrated. Every entry needs a `reason`; an entry with an empty reason fails the P0 gate. |

### `target`
| Field | Required | Notes |
|---|---|---|
| `stack.*` | ✅ | Quoted verbatim into the TSD. Free text — the pack does not parse it. |
| `surfaces[]` | ✅ | One per form factor. Drives which screen-design variants get generated and which ID suffixes are legal. A single-surface project keeps just `PC`. |
| `build.order[]` | ✅ | Ordered shell commands. `/mig-verify-build` runs them in sequence and stops at the first failure. |

### `infrastructure`

Where the **target** code lives, how it is built, where it runs, and how it takes over from a
legacy system that is still running. Read by `mig-infrastructure` and `mig-infra-engineer`.
**There is no default platform**: a task that needs one of these and finds a `<placeholder>`
stops and asks rather than assuming GitHub (IN-01).

The legacy system's own infrastructure is read-only, like its source (LR-01).
`legacy_infrastructure` exists so documents can name it; nothing here is a licence to change
it, and **no pipeline step may deploy to the legacy production environment** —
`/mig-profile-check` check 31 is Critical for that reason.

| Field | Required | Notes |
|---|---|---|
| `scm.platform` · `scm.review_unit` | ✅ | `github` · `gitlab` · `azure-repos` · `bitbucket` · `gitea` · other. The review-unit wording is used verbatim in documents; the client's team searches for the words their own tools use. |
| `ci.platform` · `ci.definition_path` | ✅ | `github-actions` · `gitlab-ci` · `azure-pipelines` · `jenkins` · `circleci` · `none`. `none` is an answer, not a gap. |
| `ci.stages[]` | ✅ | In order. Each maps to a `target.build` command, or is explicitly extra. |
| `ci.enforces_gates[]` | — | The gates the pipeline asserts **mechanically**. It cannot assert that a behaviour is anchored, a message verbatim, or a GAP item resolved — which are this pack's real risks (IN-04). |
| `hosting.*` · `containers.*` | ✅ / — | `on-prem` and `bare-metal` are first-class values; `containers.enabled: false` is common. |
| `iac.tool` · `iac.manual_changes_allowed` | ✅ | With `none`, the obligation moves to a documented rebuild procedure and the rebuild risk becomes an `RSK-*`. `manual_changes_allowed: false` means a console change is undocumented infrastructure (IN-03). |
| `secrets.store` | ✅ | Never the repository. Credentials found hardcoded in legacy source are a **finding reported to the client**, never carried across — NI-02 does not extend to security defects. |
| `observability.*` | — | Where logs, metrics, traces and alerts go, and who receives them. |
| `owner` · `repo_may_write_infra` | ✅ | When `owner` is not `this project`, set `repo_may_write_infra: false`: the agent then produces proposals and reviews, never commits. |
| `legacy_infrastructure` | — | Reference only. Naming it is what lets the cutover plan say "client IS disables job X". |

#### `infrastructure.coexistence` — the part a greenfield project does not have

| Field | Notes |
|---|---|
| `strategy` | `big-bang` · `phased` · `strangler` · `parallel`. Shapes the architecture, not just the cutover, so it is decided at init. |
| `system_of_record` | **Which system owns the data while both are live.** Required for anything but `big-bang`. |
| `dual_write` · `conflict_resolution` | Two writers over one database is the defect class that ends migrations. When `dual_write` is true, the conflict rule is mandatory and belongs in the architecture document (check 35, Critical). |
| `router` · `user_routing` | What routes a request, and how an operator knows which system they are in. During coexistence they will have both open. |

#### `infrastructure.data_migration`

| Field | Notes |
|---|---|
| `reconciliation[]` | **The deliverable.** Row counts, control totals on money and quantity columns, referential integrity, business-chosen spot checks. Designed before the script — a script that finishes without an error has demonstrated only that it did not crash (IN-08). |
| `rehearsals_required` | On a **production-sized** copy, timed. A rehearsal on a small extract measures neither correctness at volume nor whether the run fits the window. |
| `cutover_window` | Hours available, and what the business does meanwhile. |
| `point_of_no_return` | Written down before cutover weekend, not discovered during it. Everyone on the call should be able to say what it is and whether it has passed. |

#### `infrastructure.parallel_run`

The migration's strongest evidence: same input to both systems, outputs compared field by
field, against the oracle itself rather than somebody's reading of it.

| Field | Notes |
|---|---|
| `compare[]` | Screen output, report output, **batch output files**, database state. Batch files are the highest-value and most-skipped: they are exactly diffable. |
| `tolerance` | `exact` by default, and worth defending. Each field allowed to differ is named with its reason and its decision. "Minor formatting differences" is not an exception list; it is the absence of one. |
| `sign_off_by` | Who accepts the run. |

#### `infrastructure.rollback`

| Field | Notes |
|---|---|
| `target` | Usually `legacy` — the fallback is a system that never stopped, which is a different problem from redeploying a previous build. |
| `data_strategy` | **What happens to records created in the target after cutover.** Exported and loaded back by a tested script, re-keyed by hand from a report, or lost. Pick one and tell the business which. |
| `rehearsed` | `false` is the normal state and the one to change. An unrehearsed rollback is a hypothesis, usually wrong about the database. |
| `decision_owner` | Who calls it **and by when**. A rollback decision available at any time is one nobody makes. |

`target.environments[]` carries two entries a greenfield project does not have: `parallel`,
where the comparison runs and which must be production-like, and `legacy-prod`, marked
`readonly: true` and never a deployment target. **X-11** reconciles the environments the
pipeline deploys to against this list.

### `ids`
Deterministic identity is what makes traceability checkable. Rules:

- `module_pattern` is a real regex; `/mig-profile-check` validates `module_example` against it.
- `doc_id_format` must contain `{MODULE}`, `{TYPE}` and `{NNN}`.
- `MODULE_BASE` = module ID with its surface suffix stripped (`KK0030PG` → `KK0030`).
  Message IDs use the base so PC and handheld variants of one screen share a message set.
- `number_width` fixes the zero padding. `001`, never `01` or `1`.

### `paths`
All repo-relative, no leading `./`. `bd_categories[]` is an ordered list — the order is
the generation order used by `/mig-generate-basic-design` and the orchestrator agent.
Each entry names the **skill** that owns that category; adding a category means adding
(or reusing) a skill.

`uat_reports`, `change_requests` and `bug_traces` sit outside the deliverable tree on
purpose: they are project records rather than client deliverables, and they survive a
re-generation of the design set.

### `language`
`by_path[]` binds a directory glob to exactly one language. **A directory has one
language.** When the same deliverable exists in two languages, they are two directories,
and `/mig-translate` syncs *business changes*, never raw text.

`immutable_tokens` is the never-translate list. It is enforced by `mig-translation`.

### `document`
`auto_version_bump: false` is a hard default. Automated version bumps destroy the
approval audit trail — a revision row is added only when a human says so.

### `templates`

**The pack ships no deliverable templates.** Every organisation has its own forms, in its own
format — Excel through most of the Japanese SI market, and usually contractual on migration
work. An invented template is rejected at the first review, after a whole category has been
written into it. So the form is a project input: collected by `/mig-init`, maintained by
`/mig-template-register`, used by `mig-document-io`.

| Field | Required | Notes |
|---|---|---|
| `root` | ✅ | Where the client's blank forms live. Originals as received go under `root/_received/` with their date, and are never edited. |
| `on_missing` | ✅ | `ask` (default, safest) · `skeleton` (generate from the category skill's sections, and say so per run) · `block`. |
| `formats_enabled[]` | ✅ | `md` · `xlsx` · `docx` · `csv`. Each needs a working library — check 23 verifies it, because a missing one fails on file forty, not file one. |
| `registry[].key` | ✅ | A `paths.bd_categories[].key`, or one of `requirements` · `detail` · `test_ut` · `test_it` · `test_uat` · `review` · `cr_report` · `uat_report` · `legacy_inventory`. |
| `registry[].path` · `format` | ✅ | Under `root`. Every deliverable is written into a **copy**; the form itself is read-only. |
| `registry[].output_format` | — | Empty means "same as the template". A deliberate split (Markdown working copy, Excel for delivery) is recorded here once, never decided per file (DS-11). |
| `registry[].sheet` · `header_rows` | — | `xlsx` only; read from the file when empty. `header_rows` covers the client's header block — document id, system name, approval stamps. |
| `registry[].fields[]` | — | Left empty, the field map is derived from the form's own placeholders (DIO-04). |
| `registry[].status` | ✅ | `provided` · `none`. A `provided` entry whose file is missing is **Critical**: the team believes a form is in force. |
| `template_wins_over_skill` | ✅ | The template outranks DS-01 and the category skill's sections (DS-10). Content the skill needs and the form cannot hold is a **template gap**, reported once to the document owner — never resolved by inventing a section. |
| `preserve_unfilled_structure` | ✅ | Round-trip fidelity: writing changes nothing outside the filled fields (DIO-03). Verify on the category's first file. |
| `legacy_documents_dir` | ✅ | Where the **old system's** documents live. See below — this is the field that does not exist in a greenfield pack. |

**The template never suspends NI-01.** Many client forms have no column for the `LEG-*`
anchor, because they were designed for new development. The anchors then go in a section the
form does have, or in Open Items, and the missing column is reported as a template gap. A
deliverable with no anchors is not a migration deliverable, whatever form it is written on.

Binary deliverables carry a plain-text digest under `paths.reviews/digests/`, holding the
values written **and their anchors** (DIO-07). Without it an `.xlsx` deliverable sits outside
every review, cross-check and gate — which is how a category passes P2 with nobody having
checked a single anchor.

#### `templates.legacy_documents_dir` — and DIO-08

Old design specifications, operator manuals, handover packs and previous test documents are
read-only **inputs**, kept apart from the client's blank forms so nobody writes into one, and
never registered as templates (check 26, Critical).

They are **not** one of NI-01's three anchors:

| The legacy document says | Its status |
|---|---|
| a rule, default, message or sort order | a **hypothesis** — confirm against the legacy source and cite the source |
| a rule the code contradicts | the **code wins**; report both with anchors and ask (NI-05) |
| a rule the code never implemented | a SPEC-GAP, often a feature specified, cut, and never removed from the spec |
| *why* something works as it does | genuinely valuable and available nowhere else — quote it as rationale, still anchor the behaviour to code |

These documents are usually years out of date and the gap is invisible unless checked. A
deliverable anchored to an old specification has documented what somebody intended years ago,
which the client discovers at parallel run. `mig-bd-designer` reports the anchor split —
source versus document — so the risky rows are visible.

### `mockup`

The visual counterpart of the screen design. In a migration the legacy screen is the UI
oracle, to the degree `fidelity` says. Read by `mig-mockup` and `mig-mockup-designer`.
**A mockup is never the specification** (MU-01); the screen design is.

| Field | Required | Notes |
|---|---|---|
| `kind` | ✅ | `html` (self-contained prototype — the only diffable kind) · `canvas` (design-canvas artboards published as an Artifact) · `figma` (the design team's file) · `image` (exports) · `none`. `none` is a decision stated in the P2 plan, not an absence. |
| `fidelity` | ✅ | **The field that decides whether a layout difference is a defect or a deliverable.** `as-is` — reproduce the legacy screen: same fields, order, grouping, tab order. `restyled` — same information and order, modern visual language. `redesigned` — deliberately re-thought; needs a funded written client decision, and X-10 is then not run. |
| `fidelity_exceptions[]` | — | Screens agreed to differ, each with the decision that authorised it. **An exception with no decision is an invention** (NI-02) — check 28 is Critical. |
| `dir` · `surfaces[]` | ✅ unless `none` | Each surface id must name a `target.surfaces[]` entry. |
| `states_required[]` | ✅ | Default `normal · empty · loading · error · no-permission`. Four of the five are what the review is for; under `as-is` each reproduces what the legacy did in that state, which usually has to be discovered rather than remembered. |
| `html.self_contained` | — | Inline CSS/JS, no CDN, no build step: the operators open it from a file share on a locked-down machine. |
| `figma.writable` | — | `false` by default and usually stays there — the design team owns the file, and an edit from a build tool is invisible in their process. Changes go out as a request against the design. |
| `canvas.artifact_url` | — | Set on first publish and **reused**. Two links for one screen set is how a client reviews last month's design and approves it. |
| `cross_check_with_screen_design` · `cross_check_with_legacy` | ✅ | Enable **X-09** (a..h, against the screen design) and **X-10** (a..f, against the legacy screen). Each mismatch is Critical and is decided against the legacy source — never by editing one side to match the other. |

`mockup` is already in `change_request.cascade`: a rename or a field change propagates to it
in the same CR. A half-updated mockup is worse than a stale one, because it looks current.

### `gates`
Free-form assertions per phase. `/mig-trace-check` and the phase commands print them and
refuse to report a phase complete while any assertion is unmet. Add project-specific
gates here rather than editing skills.

### `review.families`
Toggles which checklist families `/mig-review-design` loads. Switching a family off
removes its findings entirely — use it for categories a project genuinely lacks
(no batch jobs, no printed reports), not to silence findings you do not want to fix.

### `testing`

Drives the whole P5–P7 skill family. Five sub-sections:

| Sub-section | Notes |
|---|---|
| `paths` | where cases, checkpoints, the flow catalogue, automation, evidence and results live |
| `naming` | file and directory patterns, timestamp format, batch labels. `{TS}` is what makes retries non-destructive |
| `pipeline` | `human_pauses` names which pauses this project keeps — removing one removes the review it bought; `keep_retry_history` must stay true, it is how a disputed case is traced to the answer that produced it; `max_review_rounds` bounds the self-review before escalation |
| `viewpoints` | the enabled VP set. Disable one only when it cannot apply (a batch job has no repeated-submission viewpoint), never to reduce effort |
| `integration` | the flow catalogue, strategy guide and swimlane the IT pipeline reads. `api_payload_in_scope: false` keeps request/response assertions out of manual IT cases |
| `automation` | framework, repository layout, spec naming, and `db_driven_search` — the flag that forbids hardcoding transactional search values |
| `evidence` / `rounds` | evidence naming and the per-round result columns appended to every executable case table |

`automation.layout` must match the real repository. The automation skill reads these
directories to learn the existing conventions, and conventions found in the repository
outrank the ones in the skill.

### `change_request`

Drives `mig-change-request` and the `/mig-cr-*` commands. A change request is
cross-cutting, not a phase — it can arrive any time from P2 onward — so its gate is keyed
`gates.CR_change_request` rather than by phase number.

| Field | Notes |
|---|---|
| `id_format` | must match the client's CR list. `id_source: client` is the enforcement: the pack never generates a CR id, and a report without a client-issued one is not filed |
| `min_options` | how many options phase 2 presents before the first gate. Below two, the gate stops being a decision |
| `gates` | the two approval stops — `after_options`, then `after_design`. Both are printed even when the user waives the pause, because the decision record is what the client reads back at review |
| `cascade` | the document update order for phase 3: `bd_categories` keys, then `indexes`, `translations`, `test_cases`. The order is load-bearing — a document edited before the one it consumes contradicts it |
| `update_test_cases` | the existing cases describe the pre-CR behaviour, so they change with it. `false` only where the project keeps no case documents |
| `classes` | the classification set. The class sets cascade depth, so dropping one drops a scoping decision, not a label |

Behaviour a CR introduces has no `LEG-*` ancestor. It is recorded in the traceability
register with the CR id in the ancestor position (TR-02); without that row it is
indistinguishable from an invention.

### `bug_trace`

Drives `mig-bug-trace` and `/mig-trace-bug`. **Every key is optional** — the one exception
to the stop-on-unresolved-token rule above: an absent or empty key means *detect from the
repository*, because the trace must still run on a project that never configured it. The
dossiers and `bug-trace-register.csv` live under `paths.bug_traces`.

| Field | Notes |
|---|---|
| `mainline` | the branch releases are cut from. Empty → the branch `origin/HEAD` points to. Used to find the merge that brought an introducing commit in |
| `release_tag_pattern` | glob selecting the tags that are releases (`v*`). Empty → every tag counts, which over-reports on repositories that also tag builds |
| `commit_ref_patterns` | extra regexes for ticket keys in commit messages (`WMS-[0-9]+`). CR ids, bug ids and module ids are recognised from `change_request.id_format` and `ids.*` without being listed here |

### `constraints`
`readonly_globs` is enforced at the tool level by `hooks/guard-readonly-paths.py`
(PreToolUse on Write/Edit). This is the mechanical backstop for the
"legacy is read-only" rule — the skills state it, the hook enforces it.

### `execution`

<!-- model-policy:claude -->
| Field | Notes |
|---|---|
| `model_profile` | `quality` · `balanced` (default) · `budget`. `/mig-init` resolves it, through the two tables below, to the `model:` and `effort:` frontmatter of every `mig-*` agent. |
| `agent_model_overrides` | `{agent: model}` — wins over `model_profile` for that one agent. Raise a role the project depends on, or lower one that is genuinely mechanical here. |
| `agent_effort_overrides` | `{agent: effort}` — `low` · `medium` · `high` · `xhigh` · `max`; wins over `model_profile` for that one agent. |
| `agent_model` | **Deprecated.** One model for every agent, from older profiles. Read as `quality` when it is `opus` and `budget` when it is `sonnet`; `/mig-profile-check` asks for it to be replaced by `model_profile`. |
| `intended_effort` | The effort for your own session, where the commands run. Agents do not use it — they take theirs from `model_profile`. Claude Code reads the session level from `/effort`, not from the profile, so set it there. |

| `model_profile` | heavy tier | standard tier |
|---|---|---|
| `quality` | opus · `xhigh` | opus · `high` |
| `balanced` | opus · `high` | sonnet · `medium` |
| `budget` | sonnet · `high` | sonnet · `medium` |

| Tier | Agents | Why |
|---|---|---|
| heavy | `mig-legacy-analyst`, `mig-requirements-writer`, `mig-bd-orchestrator`, `mig-bd-designer`, `mig-dd-designer`, `mig-reviewer`, `mig-defect-triager`, `mig-cr-engineer` | Analysis, design, review and triage. Their failures are silent and plausible, and surface only at review, UAT or acceptance. |
| standard | `mig-implementer`, `mig-tester`, `mig-test-automator`, `mig-infra-engineer`, `mig-mockup-designer`, `mig-uat-engineer` | Production work from an approved document. Build, tests and a heavy-tier review catch what they get wrong. |

The pack ships the `balanced` values in each agent's frontmatter, so a `balanced` project with
no overrides needs no agent edits.
<!-- /model-policy:claude -->

---

## Validation

Run `/mig-profile-check` after any profile edit. It verifies:

1. every required field is present and non-placeholder (no `<...>` left);
2. `module_example` matches `module_pattern`;
3. `doc_id_format` contains all three placeholders;
4. every `paths.*` directory exists or can be created;
5. every `bd_categories[].skill` names an installed skill;
6. `legacy.readonly` is `true`;
7. every `legacy.excluded[]` entry has a non-empty `reason`;
8. `document.auto_version_bump` is `false` (warn if true).
9. every `change_request.cascade` entry names a `bd_categories` key or one of
   `indexes` / `translations` / `test_cases`;
10. `change_request.id_source` is `client`.
11. every `bug_trace.commit_ref_patterns[]` entry compiles as a regex;
12. every registered template resolves, and every enabled format has a working library;
13. no registered template lives inside `templates.legacy_documents_dir` (DIO-08);
14. `mockup.fidelity` is valid and every `fidelity_exceptions[]` entry cites a decision;
15. **no `infrastructure` field names the legacy production environment as a deployment
    target** — LR-01 covers infrastructure;
16. `coexistence.system_of_record` is set for any strategy but `big-bang`, with a conflict
    rule wherever `dual_write` is true.

---

## Minimum viable profile

To run P0 and P1 you need: `project`, `legacy`, `target` (minus `build`), `ids`, `paths`,
`language`, `document`, `gates.P0_*` and `gates.P1_*`.

`target.build` and `infrastructure` can stay as placeholders until P4 — but say so rather
than filling them with guesses. A placeholder is visible; a plausible guess is not.

`templates` and `mockup` are needed **before P2**, and they are the two that are expensive to
discover late. A category generated into the pack's own skeleton when the client expected
their form is re-work across every file in it, and a mockup drawn at the wrong fidelity is
re-work the operators find at UAT. Register the forms and settle `mockup.fidelity` while P1
is still in progress.

`infrastructure.coexistence` is the exception to "infrastructure can wait": it shapes the
architecture, so it is decided at init even though it is not built until much later.

---

## Recipes

[`PROFILE-RECIPES.md`](PROFILE-RECIPES.md) has overlays for seven migration shapes — desktop
to web, mainframe to open systems, lift and shift, strangler, legacy web to SPA, database
replatform, and Japanese-market SI — each with the reason behind every field it changes and
the questions the overlay cannot answer.
