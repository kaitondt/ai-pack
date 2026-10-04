# `sdlc.profile.yaml` — Field Specification

The profile is the **only** file a new project must author before the pack becomes
operational. Skills read it through the `sdlc-project` skill and substitute
`{{profile.<dotted.path>}}` tokens.

Canonical location: `<repo-root>/.claude/sdlc.profile.yaml`

---

## Resolution contract

| Token form | Resolves to |
|---|---|
| `{{profile.system.stack.backend}}` | scalar value |
| `{{profile.paths.design_root}}` | path string, repo-relative |
| `{{profile.ids.types.screen}}` | `SC` |
| `{{profile.surface(PC).id_suffix}}` | list lookup by `id` |
| `{{profile.gates.P2_basic_design.exit}}` | list of assertions |

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
| `delivery_model` | ✅ | `waterfall` · `iterative-waterfall` · `agile-with-gates`. Sets how hard a gate blocks; under `agile-with-gates`, P4–P6 run per sprint and only RA/BD/ST/UAT are hard stops. The assertions themselves never change. |
| `contract_type` | ✅ | `fixed-price` · `time-and-materials` · `internal`. Read by `sdlc-change-request`: under fixed-price a scope change is a contractual event and the Phase 2 estimate is mandatory. |
| `release_cadence` | — | Quoted in the release and maintenance plans. |

### `stakeholders`
Every role is required. **A decision with no owner cannot be recorded, and an unrecorded
decision is an assumption** (RS-02). `/sdlc-profile-check` fails Critical on an unset role.

`approvers[]` extends the set for projects where a steering group signs baselines.

### `scope`
| Field | Required | Notes |
|---|---|---|
| `in_scope[]` | ✅ | Expanded per capability in the scope statement. |
| `out_of_scope[]` | ✅ | Each entry needs a `reason`. An exclusion with no reason gets re-litigated monthly; one with a reason gets accepted once. Quoted into every CR impact analysis. |
| `external_systems[]` | — | One per system this project talks to but does not own. Drives the P6 interface-failure case set and the C3 constraint in change requests. |

### `system`
| Field | Required | Notes |
|---|---|---|
| `stack.*` | ✅ | Quoted verbatim into the architecture document. Free text — the pack does not parse it. |
| `architecture` | ✅ | Free text; the layer model the detail design follows. |
| `surfaces[]` | ✅ | One per form factor. Drives which screen-design variants get generated and which ID suffixes are legal. A single-surface project keeps just `PC`. |
| `environments[]` | ✅ | Named environments the deliverables and tests refer to. **Exactly one should be marked `production_like: true`** — that is where system test runs, and without it P7 has nowhere to measure. |
| `build.order[]` | ✅ | Ordered shell commands. `/sdlc-verify-build` runs them in sequence and stops at the first failure. |
| `build.typecheck` / `lint` / `test_*` | ✅ | Run after the build order, in that sequence. |

### `infrastructure`

Where the code lives, how it is built, and where it runs. Read by `sdlc-infrastructure` and
`sdlc-infra-engineer`. **There is no default platform**: a task that needs one of these and
finds a `<placeholder>` stops and asks rather than assuming GitHub (IN-01).

| Field | Required | Notes |
|---|---|---|
| `scm.platform` | ✅ | `github` · `gitlab` · `azure-repos` · `bitbucket` · `gitea` · other. Decides where the CI definition goes, and what a merge request is called in every document. |
| `scm.review_unit` | ✅ | "pull request" / "merge request", used verbatim. The client's team searches for the words their own tools use. |
| `scm.branching_model` · `protected_branches[]` | — | Protected branches require a passing pipeline and a review, or the pipeline is advisory. |
| `ci.platform` | ✅ | `github-actions` · `gitlab-ci` · `azure-pipelines` · `jenkins` · `circleci` · `none`. `none` is an answer, not a gap to fill. |
| `ci.definition_path` | ✅ | Where the pipeline file goes. `/sdlc-profile-check` warns when it does not match the platform's convention. |
| `ci.stages[]` | ✅ | In order. Each maps to a `system.build` command, or is explicitly extra — a stage running something no developer can reproduce is a stage nobody can debug. |
| `ci.enforces_gates[]` | — | Which phase gates the pipeline asserts **mechanically**. Only the machine-checkable ones belong here (IN-03); a green pipeline is evidence for these and nothing else. |
| `cd.*` | — | Strategy, which environments need approval, and the deployment pattern. On mobile, `canary` is the only rollback that exists. |
| `hosting.provider` / `runtime` | ✅ | `on-prem` and `bare-metal` are first-class values. |
| `containers.*` | — | `enabled: false` is common and fine. |
| `iac.tool` | ✅ | `terraform` · `bicep` · `cloudformation` · `pulumi` · `ansible` · `helm` · `none`. With `none` the obligation moves to a runbook procedure detailed enough to rebuild from — and the rebuild risk becomes an `RSK-*` rather than an assumption. |
| `iac.manual_changes_allowed` | ✅ | `false` means a console change is undocumented infrastructure (IN-02). |
| `secrets.store` | ✅ | Never the repository. `.env.example` documents the keys; `.env` is not committed. |
| `observability.*` | — | Where logs, metrics, traces and alerts go, and who receives them. |
| `observability.nfr_monitors_required` | — | When true, every measurable `NFR-PERF/AVAIL/OPS-*` needs a monitor row with a signal, a destination and a threshold (IN-06). An availability target with no monitor is one the client reports to you. |
| `owner` | ✅ | `this project` · `platform team` · `client ops`. Changes what the pack may **write** versus only **request**. |
| `repo_may_write_infra` | ✅ | When false, `sdlc-infra-engineer` produces proposals and reviews, never commits. Set it false whenever `owner` is not this project. |

**X-12** reconciles the environments the pipeline deploys to against `system.environments`.
An environment the pipeline knows about and the profile does not is where system test runs
against the wrong data.

### `ids`
Deterministic identity is what makes traceability checkable. Rules:

- `module_pattern` is a real regex; `/sdlc-profile-check` validates `module_example`
  against it.
- `doc_id_format` must contain `{MODULE}`, `{TYPE}` and `{NNN}`.
- `MODULE_BASE` = module ID with its surface suffix stripped (`SL0030PG` → `SL0030`).
  Message IDs use the base so the desktop and mobile variants of one screen share a
  message set.
- `number_width` fixes the zero padding. `001`, never `01` or `1`.
- `test_id_format` keys each level differently on purpose — module for UT, flow for IT,
  scenario for ST, a flat sequence for UAT. That forces each level's case set to be
  organised the way that level actually verifies (ID-05).
- `{AREA}` is a business area agreed once at P0. `{CATEGORY}` for NFRs is the fixed set
  `PERF SEC AVAIL OPS USE COMPL`; adding one is a profile change, not a per-document choice.

### `paths`
All repo-relative, no leading `./`. `bd_categories[]` is an ordered list — the order is the
generation order used by `/sdlc-generate-basic-design` and the orchestrator agent. Each
entry names the **skill** that owns that category; adding a category means adding (or
reusing) a skill.

`architecture` and `nfr` come first in the default list deliberately: every other category
depends on decisions they record.

`uat`, `maintenance`, `change_requests` and `bug_traces` sit outside the deliverable tree
on purpose: they are project records rather than client deliverables, and they survive a
re-generation of the design set.

The four register paths — `traceability`, `decision_log`, `assumption_log`,
`risk_register` — are what the gates read. They are not optional documentation.

### `language`
`by_path[]` binds a directory glob to a language. **The language of a deliverable is a
property of its directory, never of the request** (DS-09). `immutable_tokens` lists what is
never translated in any direction.

`dictionary` and `grammar_fixes` are optional CSV paths; when set, the dictionary is
authoritative for domain terms and must agree with `paths.glossary`.

### `document`
Shared skeleton for every deliverable. Two fields carry more weight than they look:

- **`auto_version_bump` must stay `false`.** The version tracks approval cycles, not
  edits (DS-02).
- **`require_review_record`** puts the review history inside the document. That table is
  the raw input to review density (QM-02) — without it, the metric cannot be computed from
  artifacts.

`initial_version` is `0.x` for drafts; `baseline_version` is what `/sdlc-phase-gate` sets
when it baselines a document.

### `templates`

**The pack ships no deliverable templates.** Every organisation has its own forms, in its
own format — Excel in most of the Japanese SI market — and an invented template is rejected
at the first review, after a whole category has been generated into it. So the template is a
project input: collected by `/sdlc-init`, maintained by `/sdlc-template-register`, and used
by `sdlc-document-io`.

| Field | Required | Notes |
|---|---|---|
| `root` | ✅ | Where templates live. Originals as received go under `root/_received/` with their date, and are never edited. |
| `on_missing` | ✅ | `ask` (default, safest) · `skeleton` (generate from the category skill's own sections, and say so per run) · `block`. `skeleton` is an agreement recorded as a `DEC-*`, not a fallback. |
| `formats_enabled[]` | ✅ | `md` · `xlsx` · `docx` · `csv`. Each needs a working library — `/sdlc-profile-check` check 29 verifies it, because a missing library fails on file forty, not file one. |
| `registry[].key` | ✅ | A `paths.bd_categories[].key`, or one of `requirements` · `detail` · `test_ut` · `test_it` · `test_st` · `test_uat` · `review` · `cr_report` · `incident` · `gate_record` · `release_note`. |
| `registry[].path` · `format` | ✅ | Repo-relative, under `root`. Add each to `constraints.readonly_globs`: the template is an input, and every deliverable is written into a **copy**. |
| `registry[].output_format` | — | Empty means "same as the template". A deliberate split (Markdown working copy, Excel for delivery) is recorded here once, never decided per file (DS-12). |
| `registry[].sheet` · `header_rows` | — | `xlsx` only. Read from the template itself when empty. `header_rows` covers the client's header block — document id, system name, approval stamps. |
| `registry[].fields[]` | — | Left empty, `sdlc-document-io` derives the field map from the placeholders in the file (DIO-04). |
| `registry[].status` | ✅ | `provided` · `none`. A `provided` entry whose file is missing is **Critical**: the team believes a form is in force. |
| `template_wins_over_skill` | ✅ | The template outranks the category skill's section list and DS-01 (DS-11). Content the skill needs and the template cannot hold is a **template gap**, reported once to the document owner — never resolved by inventing a section. |
| `preserve_unfilled_structure` | ✅ | Round-trip fidelity: writing changes nothing outside the filled fields — not a column width, not a merged range, not the print area (DIO-03). Verify on the first file of each category. |

Binary deliverables also carry a plain-text digest under `paths.reviews/digests/` (DIO-07).
Without it, an `.xlsx` deliverable sits outside every review, cross-check and gate the pack
runs — which is how a category passes P2 without anyone having read it.

### `mockup`

The visual counterpart of the screen design, in whatever form the project uses. Read by
`sdlc-mockup` and `sdlc-mockup-designer`. **A mockup is never the specification** (MU-01).

| Field | Required | Notes |
|---|---|---|
| `kind` | ✅ | `html` (self-contained prototype in the repo — the only diffable kind) · `canvas` (design-canvas artboards published as an Artifact) · `figma` (the design team's file) · `image` (exports from any tool) · `none`. `none` is a decision, stated in the P2 plan, not an absence. |
| `dir` | ✅ unless `none` | Normally under `paths.design_root`. |
| `surfaces[]` | ✅ unless `none` | Each must name a `system.surfaces[]` entry. |
| `states_required[]` | ✅ | Default `normal · empty · loading · error · no-permission`. Four of the five are what the review is for; a happy-path-only mockup demonstrates nothing anybody was uncertain about. |
| `html.self_contained` | — | Inline CSS/JS, no CDN, no build step. The reviewer opens it from a file share on a locked-down machine with no toolchain. |
| `figma.writable` | — | `false` by default and usually stays there: the design team owns the file, and an edit made from a build tool is invisible in their process. Changes go out as a request against the design. |
| `canvas.artifact_url` | — | Set on first publish and **reused** on every update. Two links for one screen set is how a client reviews last month's design and approves it. |
| `cross_check_with_screen_design` | ✅ | Enables **X-11** (sub-checks a..g: fields, grid columns, buttons, messages, states, navigation, permissions). Each mismatch is Critical and is decided against the baselined SRS — never by editing one side to match the other. |

`mockup` is in `change_request.cascade` for a reason: a rename or a field change propagates
to it in the same CR. A half-updated mockup is worse than a stale one, because it looks
current.

### `gates`
One entry per phase, each with `entry` and `exit` lists of assertions. `/sdlc-phase-gate`
evaluates them one by one, with evidence, and records the decision.

Assertions are written as **checkable statements**, not aspirations. "Quality is good" is
not an assertion; "every `REQ-*` has an executed ST case" is.

Add project-specific assertions freely — they are the cheapest place to encode a lesson
learned. Removing one because it keeps failing is the failure mode `/sdlc-refine-skill`
warns about.

### `review`
`families` turns checklist families on and off. Turning one off does not remove the defects
it would have found; it removes your view of them.

`record_in_document` controls whether the review round is written into the document itself
in addition to the review report.

### `quality`
| Field | Notes |
|---|---|
| `size_unit` | The denominator for every density metric. Pick one and keep it — mixing KLOC and function points makes two phases incomparable. |
| `targets.*` | **Project agreements calibrated from your own history, not industry constants.** Set them, agree them, hold them. |
| `severity[]` | The defect severity model. Severity is impact and is assessed by the tester or client; priority is scheduling and belongs to the product owner. Keep them separate. |
| `injection_phases` | The phases a defect can be attributed to. Attribution honesty is what makes phase containment worth computing (QM-04). |

### `constraints`
| Field | Notes |
|---|---|
| `baseline_change_requires_cr` | **Must be `true`** for BL-02 to be enforced. `/sdlc-profile-check` fails Critical otherwise. |
| `production_change_via_release_only` | Enforces BL-04 in the maintenance skill. |
| `db_schema_owner` | `this project` · `<other team>` · `frozen`. Drives the C3 constraint in change requests and the data-design mode. |
| `readonly_globs[]` | Enforced by `hooks/guard-protected-paths.py`. |
| `baselined[]` | Appended by `/sdlc-phase-gate` when a gate passes. The hook reads it to block edits without an active CR. |

### `execution`
`agent_model` is applied to every `.claude/agents/sdlc-*.md` by `/sdlc-init`.
`intended_effort` **records** the session-level reasoning effort the project expects — it
cannot enforce it, because effort is not agent frontmatter in Claude Code.

### `testing`
| Field | Notes |
|---|---|
| `levels[]` | **The V-model binding.** Each level names the specification it verifies (`basis`), the environment it runs on, and its owner. `/sdlc-generate-test` reads this to decide which document to work from. |
| `viewpoints[]` | The enabled coverage viewpoints. Disable one only when it cannot apply. |
| `pipeline.human_pauses[]` | Which pauses the project keeps. **Removing a pause removes the review it existed to buy** — the first buys answers that stop invention, the second buys coverage review while it is cheap. |
| `system_test.*` | What P7 covers beyond functional regression: performance, security, failover, volume, operability. |
| `uat.*` | Who executes, the support model, entry sign-off, and the defect SLA during UAT. |
| `evidence.required_for[]` | Levels where a result without evidence is not a result. |
| `automation.*` | Framework, repository layout and naming. The repository's own conventions outrank these. |

### `change_request`
| Field | Notes |
|---|---|
| `id_source` | `client` or `project`. Whoever owns the CR list. Never generated by the pack. |
| `min_options` | Options Phase 2 must present before GATE 1. |
| `gates[]` | The two approval stops. Removing one removes the review it existed to buy: `after_options` = which option, `after_design` = the document diff before any code. |
| `require_estimate` | When true, no option reaches GATE 1 without effort, schedule and test impact. |
| `cascade[]` | Document update order for Phase 3. A document edited before the one it consumes contradicts it. |
| `classes[]` | The classification set. `CR-NFR` and `CR-SCOPE` are the two most often under-scoped. |

### `maintenance`
| Field | Notes |
|---|---|
| `classes[]` | Incident classification set. |
| `sla.*` | Response and resolution targets per severity. Response = acknowledged and triaged; resolution = fix released or an accepted workaround with a scheduled fix. |
| `hotfix.*` | Whether hotfixes are allowed, who approves, and the retro-documentation window. A hotfix skips the queue, never the record (BL-06). |
| `rca_required_for[]` | Severities that require a root cause analysis answering all three questions. |
| `regression_test_required` | Every fix ships with the test that would have caught it. |
| `warranty_period` | Agree the boundary in writing before go-live; after an incident it becomes a negotiation. |

### `bug_trace`

Drives `sdlc-bug-trace` and `/sdlc-trace-bug`. **Every key is optional** — the one exception
to the stop-on-unresolved-token rule above: an absent or empty key means *detect from the
repository*, because the trace must still run on a project that never configured it. The
dossiers and `bug-trace-register.csv` live under `paths.bug_traces`; `/sdlc-quality-report`
reads the register for an evidenced containment matrix.

| Field | Notes |
|---|---|
| `mainline` | the branch releases are cut from. Empty → the branch `origin/HEAD` points to. Used to find the merge that brought an introducing commit in |
| `release_tag_pattern` | glob selecting the tags that are releases (`v*`). Empty → every tag counts, which over-reports on repositories that also tag builds |
| `commit_ref_patterns` | extra regexes for ticket keys in commit messages (`PRJ-[0-9]+`). CR, defect, incident and module ids are recognised from `change_request.id_format` and `ids.*` without being listed here |

---

## Minimum viable profile

To run P0 and P1 you need: `project`, `stakeholders`, `scope`, `ids`, `paths`, `language`,
`document`, `gates.P0_*` and `gates.P1_*`.

`system.build`, `infrastructure`, `testing.automation` and `maintenance` can stay as
placeholders until P4, P4, P5 and P9 respectively — but say so out loud rather than filling
them with guesses. A placeholder is visible; a plausible guess is not.

`templates` and `mockup` are needed **before P2**, not before P0 — but they are the two that
are expensive to discover late. A category generated into the pack's own skeleton when the
client expected their form is re-work across every file in it, and it is found at the review,
not during the run. Register the forms while P1 is still in progress.

---

## Recipes

[`PROFILE-RECIPES.md`](PROFILE-RECIPES.md) has overlays for seven common project shapes —
Japanese-market SI with Excel deliverables, regulated finance, healthcare, public-sector
tender, mobile, data platform, and a deliberately lightweight small-team configuration —
each with the reason behind every field it changes, and the questions the overlay cannot
answer for you.
