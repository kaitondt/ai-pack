# `pm.profile.yaml` — Field Specification

The profile is the **only** file a new project must author before the pack becomes operational.
Skills read it through the `pm-project` skill and substitute `{{profile.<dotted.path>}}` tokens.

Canonical location: `<repo-root>/.claude/pm.profile.yaml`

---

## Resolution contract

| Token form | Resolves to |
|---|---|
| `{{profile.project.contract_type}}` | scalar value |
| `{{profile.paths.charter}}` | path string, repo-relative |
| `{{profile.governance.approvals.charter}}` | list of role keys |
| `{{profile.schedule.milestones}}` | list of milestone objects |
| `{{profile.risk.issue_sla_hours.S1}}` | nested scalar |

**If a token cannot be resolved, STOP.** Do not guess a value and do not write a placeholder
into a management deliverable — a made-up date or amount is read as a commitment.

---

## Sections

### `project`

| Field | Required | Notes |
|---|---|---|
| `key` | ✅ | 2–5 uppercase chars. Appears in WBS codes and report filenames. |
| `name`, `code` | ✅ | Display name and contract/internal code. |
| `vendor`, `client` | ✅ | Fill the Author / Approver columns of every revision history. |
| `copyright` | ✅ | Rendered as the footer of every deliverable. |
| `start_date`, `planned_end_date` | ✅ | Anchor every "as of" statement; convert relative dates to absolute. |
| `delivery_model` | ✅ | `waterfall` · `iterative-waterfall` · `agile-with-gates`. Sets how hard a gate blocks and whether baselines are per release. |
| `contract_type` | ✅ | `fixed-price` · `time-and-materials` · `milestone-based` · `internal`. Read by `pm-change-control` and `pm-cost`: the same change is a different decision under each, and it determines **who is harmed** by skipping change control. |
| `currency` | ✅ | Every amount in every document. |
| `engagement_model` | ✅ | `onshore` · `offshore` · `hybrid` · `internal`. Drives the communication design (SE-07) more than any other single field. |
| `time_zones` | — | Used when deriving decision latency into durations (WB-08). |

### `governance`

Every role is required. **A decision with no owner cannot be recorded, and an unrecorded
decision is an assumption** (DA-01). `/pm-profile-check` fails Critical on an unset role.

| Field | Notes |
|---|---|
| `sponsor` … `delivery_manager` | One named person or role title each. |
| `ccb` | Membership, chair, cadence, quorum. Approves changes above the PM's authority. A CCB with no quorum rule will quietly stop meeting. |
| `steering_committee` | Membership, cadence, and **what it decides** — baseline resets, scope trade-offs, escalated risk acceptance. |
| `escalation[]` | Ordered levels with `sla_hours`. Drives automatic escalation (DA-05); an issue past its SLA escalates as a fact, not a complaint. |
| `approvals` | Artifact → approver roles. Consumed by every baselining step (PB-01). |

### `calendar`

The arithmetic behind every duration and cost.

| Field | Notes |
|---|---|
| `hours_per_day` | Nominal working hours. |
| `productive_hours_per_day` | ✅ **The important one.** Real available time after meetings, support and context switching. Equal to `hours_per_day` is a Warning: it makes every duration ~19% optimistic (EM-04). |
| `planned_absence_allowance` | Leave, training, sickness. Applied in the duration derivation. |
| `holidays_calendar` | Per location — an offshore project has two, and they differ. |
| `freeze_periods[]` | No-release windows. `/pm-schedule-baseline` respects them. |

### `scope`

| Field | Notes |
|---|---|
| `objectives[]` | Statement + measure + target. These are the charter objectives the final report is judged against (CL-05). |
| `in_scope[]` | Expanded per capability in the scope statement. |
| `out_of_scope[]` | ✅ Each needs a `reason`. An exclusion with no reason is re-litigated monthly; one with a reason is accepted once. Quoted into every CR impact assessment. |
| `deliverables[]` | `id`, `name`, `kind`, `acceptance_by`, `acceptance_criteria`, `due_milestone`. Criteria agreed **before** the work starts (SM-06) — written at delivery time they are negotiated under pressure. |
| `requirements` | Where requirements live, their ID format, the RTM path, and their owner. When a technical pack is installed, point at its artifacts rather than duplicating them. |
| `dependencies[]` | `DEP-*` on other teams, vendors or client actions, each with a needed-by date and what stalls without it. Every one is also a `RSK-*`. |

### `wbs`

| Field | Notes |
|---|---|
| `code_format` | Hierarchical, permanent, never reused (PN-02). |
| `work_package_min_hours` / `max_hours` | The 8/80 rule (WB-03). Secondary test: never longer than one reporting period. |
| `control_account_level` | Where cost and progress are measured and EVM is computed. Usually level 2. |
| `dictionary_fields` | The dictionary entry shape. Keep `assumptions` and the "not included" part of `description` — they prevent the most common estimate dispute. |
| `level1[]` | Top-level branches. Keep **project management**, **quality assurance and process**, and **training and handover**, with real effort: work outside the WBS is work nobody planned but everybody does (WB-02). |

### `schedule`

| Field | Notes |
|---|---|
| `baseline_path` / `working_file` | ✅ **Must be different files** (PB-05). Equal is Critical: every variance the project ever has would be erased on the first re-plan. |
| `progress_measurement` | `0-50-100` · `0-100` · `milestone-weighted` · `units-completed`. Drives EV. Self-assessed percent-complete is not an option (RI-03). |
| `buffer_policy` | Project and feeding buffers, owned by the PM; `padding_inside_estimates: forbidden` (ES-05). |
| `milestones[]` | `id`, `name`, `date`, objective `criteria`, and `payment_linked`. Payment-linked milestones have a different risk profile and are escalated differently (RI-05). |
| `variance_thresholds` | Drive RAG in every report (RI-04). |

### `cost`

| Field | Notes |
|---|---|
| `size_unit` | The denominator for every density and productivity figure. |
| `estimation_methods[]` | Allowed methods, in preference order. Every estimate records which it used (ES-01). |
| `productivity.basis` | ✅ **Where the rates came from.** Empty means unverified, and every estimate built on them says so (ES-08). |
| `productivity.rates[]` | Measured rates per unit of work. Replace the shipped placeholders. |
| `productivity.phase_distribution` | Used to sanity-check a bottom-up total. A plan with 5% testing has not estimated the testing. |
| `rates[]` | Cost per hour by role and location. |
| `contingency_percent` / `management_reserve_percent` | Different money, different owners, different approval paths (ES-06). Both zero under fixed-price is Critical. |
| `earned_value.eac_formula` | `current-rate` is the honest default: it assumes the project continues as it has (RI-07). |
| `billing` | Invoice trigger and terms. Under milestone billing the trigger is signed acceptance, not a date (CT-11). |

### `process`

| Field | Notes |
|---|---|
| `standard_ref` | The organisational standard being tailored. |
| `tailoring_record` | ✅ Every deviation with reason, risk accepted and approver. Undocumented tailoring is an audit finding (PR-02). |
| `qa` / `qc` | Separate activities with separate owners (PR-04). QA is never performed by the person being assured. |
| `definition_of_done[]` | Applied to every work package (WB-05). Keep the three always dropped under pressure: design doc updated, test case updated, traceability updated. |
| `process_assets` | One authoritative copy, versioned. Returned to the organisation at closing. |
| `corrective_actions` | CAPA log, with effectiveness checks (PR-07). |

### `quality`

| Field | Notes |
|---|---|
| `objectives[]` | Attribute + target + measurement method. A non-functional target without its condition cannot be passed or failed (QP-01). |
| `targets` | ✅ Must **match** the technical pack's `quality.targets` where one exists (QP-02). `/pm-sync-technical` reports drift. |
| `test_levels[]` | Owner, environment, entry and exit criteria per level. Entry criteria that are not enforced are the most expensive politeness in project management (QP-05). |
| `defect_severity[]` | Definitions and fix SLAs, agreed **before** testing starts. Severity is never adjusted to pass a gate (QP-07). |

### `risk`

| Field | Notes |
|---|---|
| `register` / `issue_log` | Separate files: a risk might happen, an issue has (RK-01). |
| `probability_scale[]` / `impact_scale[]` | ✅ Keep the numeric anchors — without them two people score the same risk differently (RK-05). |
| `exposure_thresholds` | Band P×I into low/medium/high. |
| `response_types[]` | avoid · mitigate · transfer · accept · escalate. "Monitor" is deliberately absent (RK-08). |
| `contingency_drawdown_log` | Every draw with its risk, approver and remaining balance (CT-08). |
| `escalate_above_exposure` | Automatic escalation threshold. |
| `issue_sla_hours` | Per severity. Drives ageing and automatic escalation. |

### `reporting`

| Field | Notes |
|---|---|
| `rag_definitions` | ✅ RAG is computed from these, then explained — never chosen then justified (RI-04). |
| `cadences[]` | One entry per report: audience, channel, due, content, path. Delete the ones nobody reads; each kept one names the decision it supports (SE-03). |
| `data_sources` | ✅ Where the numbers come from. A report built from memory or from the previous report is forbidden (RI-02). |
| `distribution_list` | Deliberate. Never send internal margin or individual performance commentary to the client (RG-05). |
| `action_item_log` | Actions with owners, dates and **age** — age is the diagnostic (RI-08). |

### `change_control`

| Field | Notes |
|---|---|
| `register` | Every change logged, including the trivial ones (IC-01, PB-07). |
| `impact_dimensions[]` | ✅ All assessed, even when the answer is "none". The two most often skipped are documentation and test (IC-04). |
| `min_options` | Options, not a single answer (IC-06). |
| `authority[]` | Threshold → approver. Below the first, the PM absorbs and records; above it, the named body decides (DA-02). |
| `rebaseline_policy` | Re-baselining is a governance event with a retained history and a stated reason (PB-06). |
| `classes[]` | Classification vocabulary. `CR-CLARIFY` matters commercially — a clarification that adds behaviour is a change. |

### `resource`

| Field | Notes |
|---|---|
| `roles[]` | Derived from the schedule, not from available headcount (RM-01). |
| `max_planned_allocation_percent` | ✅ 100 is a Warning (RM-02): the plan then has no capacity for defects, support or absence. |
| `onboarding_checklist` | High return on any project that will add anyone after kickoff (RM-03). |
| `subcontract` | Terms, SLA reference, review rights. |

### `closing`

| Field | Notes |
|---|---|
| `handover.items[]` | Verified behaviourally, not documentarily (CL-02). |
| `contract_closure` | Final invoice condition, warranty scope, retained obligations. Write what warranty does **not** cover. |
| `resource_release` | Dated records. An unreleased resource is still being billed (CL-06). |
| `post_implementation_review_after_days` | The only feedback loop that reaches past acceptance. |

### `documents`

The final form of each management artifact, and the scratch forms allowed while producing it.
Read by `pm-document-io`. Management deliverables are contractual: **format is a property of
the artifact**, agreed once, not chosen per task because one was quicker to write.

| Field | Required | Notes |
|---|---|---|
| `formats_enabled[]` | ✅ | `md` · `xlsx` · `docx` · `csv`. Each needs a working library. **`openpyxl` is not optional on this pack** — without it the WBS cannot be delivered. |
| `working_dir` | ✅ | Scratch area. Drafting in text before producing a workbook is encouraged; delivering the draft is not. Keep it outside every deliverable directory, and out of version control unless `working_retention: keep`. |
| `working_retention` | ✅ | `delete-on-finalise` (default) · `keep-one-round` · `keep`. |
| `derived_view` | — | After a binary artifact is written, regenerate a stamped plain-text view of it so the content stays diffable. A `.xlsx` in a diff is one opaque line, which makes a WBS change invisible to everyone who was not in the room. |
| `registry[].artifact` | ✅ | The artifact key: `wbs`, `estimate`, `charter`, `risk_register`, … Each appears once. |
| `registry[].path` | ✅ | Where the **final deliverable** goes. For `wbs` it must equal `paths.wbs` — two paths is two WBSs, and only one gets baselined. |
| `registry[].format` | ✅ | The final form. Not the language of the request, not what is faster. |
| `registry[].working[]` | — | Scratch forms permitted while drafting. Never delivered, never cited, never baselined. |
| `registry[].template` | — | The client's own form to write into. The deliverable is then a **copy of their file with the fields filled** — their columns, their order, their approval block (DIO-03). |
| `registry[].sheets` | — | `xlsx` only: which sheet carries what. |
| `binary_final[]` | ✅ | Artifacts whose final form **must** be a binary office file. An artifact named here has not been produced until that file exists — a complete Markdown version of it is a working file. |

#### The WBS is delivered as Excel

`wbs` is in `binary_final` and `paths.wbs` ends in `.xlsx`. `/pm-profile-check` fails Critical
on either being otherwise, and the rule is stated in `rules/pm/document-standards.md` MD-09.

Markdown and CSV are legitimate **working** forms — text is easier to restructure than a
workbook, and `working_dir` exists for exactly that. They are never the deliverable.

The reason is not formatting taste. Cost, progress, resource loading and earned value all
index into the WBS by code, and every one of those consumers is a spreadsheet. A WBS that is
not one gets re-keyed into one by hand, and from that moment the project has two.

The WBS and its dictionary live in **one workbook, two sheets**
(`registry[wbs].dictionary_in_same_workbook`), for the same reason: two files drift, and the
dictionary is the half that silently stops matching.

`pm-document-io` DIO-W owns the workbook layout — text-formatted code column, frozen and
filtered header, outline grouping, no merged cells in the data region, the 100% rule as a live
formula, per-branch totals — and the revision hazard: **never regenerate the workbook from a
working file whose stamp is older than the workbook.** Somebody edited it directly, and the
regeneration erases that without either of you noticing.

### `baselines`

| Field | Notes |
|---|---|
| `change_requires_cr` | ✅ Must stay `true` (PB-03). Enforced by `hooks/guard-pm-baselines.py`. |
| `active_cr_file` | `.claude/.active_pm_cr`. Written by `/pm-change-apply`, cleared when the CR closes. |
| `readonly_globs[]` | Always denied, CR or not: archived snapshots. |
| `registered[]` | Path, artifact, version, approver, date. Appended when an approval baselines a document. The guard hook reads this list. |

### `document`

| Field | Notes |
|---|---|
| `revision_table_headers` | Fixed columns for every deliverable. |
| `initial_version` / `baseline_version` | Drafts run `0.x`; baselining takes the document to `1.0` (MD-02). |
| `auto_version_bump` | ✅ **Must stay `false`.** `true` is Critical. |
| `require_approval_block` / `require_distribution_list` | Management documents are contractual artifacts. |
| `confidentiality` | Rendered on the title block. |

### `language`

| Field | Notes |
|---|---|
| `primary` / `working` / `client_facing` | Management documents often go to a different audience, in a different language, than engineering deliverables. |
| `by_path[]` | Deliverable language follows the directory, never the language of the request (MD-07). |
| `immutable_tokens[]` | ✅ Never translated — WBS codes, IDs, metric names, formulas, amounts. This is what lets a translated report be reconciled against the register. |

### `integration`

| Field | Notes |
|---|---|
| `technical_pack` | `auto` · `sdlc` · `migration` · `none`. `/pm-init` detects it. |
| `technical_profile_path` | Filled by `/pm-init`. |
| `bindings` | What binds to what, and which pack owns each kind of data. `quality_targets: inherit` is the safe default. |
| `milestone_gate_map[]` | Milestone ↔ phase gate. **Every payment milestone should appear here** — one that does not has no technical exit criteria behind it. |

### `execution`

<!-- model-policy:claude -->
| Field | Notes |
|---|---|
| `model_profile` | `quality` · `balanced` (default) · `budget`. `/pm-init` resolves it, through the two tables below, to the `model:` and `effort:` frontmatter of every `pm-*` agent. |
| `agent_model_overrides` | `{agent: model}` — wins over `model_profile` for that one agent. Raise a role the project depends on, or lower one that is genuinely mechanical here. |
| `agent_effort_overrides` | `{agent: effort}` — `low` · `medium` · `high` · `xhigh` · `max`; wins over `model_profile` for that one agent. |
| `agent_model` | **Deprecated.** One model for every agent, from older profiles. Read as `quality` when it is `opus` and `budget` when it is `sonnet`; `/pm-profile-check` asks for it to be replaced by `model_profile`. |
| `intended_effort` | The effort for your own session, where the commands run. Agents do not use it — they take theirs from `model_profile`. Claude Code reads the session level from `/effort`, not from the profile, so set it there. |

| `model_profile` | heavy tier | standard tier |
|---|---|---|
| `quality` | opus · `xhigh` | opus · `high` |
| `balanced` | opus · `high` | sonnet · `medium` |
| `budget` | sonnet · `high` | sonnet · `medium` |

| Tier | Agents | Why |
|---|---|---|
| heavy | `pm-planner`, `pm-estimator`, `pm-risk-manager`, `pm-change-analyst` | Analysis, design, review and triage. Their failures are silent and plausible, and surface only at review, UAT or acceptance. |
| standard | `pm-controller`, `pm-quality-manager`, `pm-closer` | Production work from an approved document. Build, tests and a heavy-tier review catch what they get wrong. |

The pack ships the `balanced` values in each agent's frontmatter, so a `balanced` project with
no overrides needs no agent edits.
<!-- /model-policy:claude -->

---

## Validation

`/pm-profile-check` enforces this document. The Critical checks, in short: the profile exists,
every governance role is filled, approvals are defined, `auto_version_bump` is false,
`change_requires_cr` is true, change authority has thresholds, schedule baseline and working
file differ, reserves are non-zero under fixed-price, and no baseline-register entry points at a
missing file.

---

## Minimum viable profile

To produce a charter and a scope baseline you need `project`, `governance`, `calendar`,
`scope`, `wbs`, `paths`, `document`, `language` and `documents`.

`documents` is needed **before the first artifact**, not before the first planning session.
It is cheap to fill and expensive to discover late: a client who receives forty Markdown
documents and expected Word, or a WBS that was never produced as a workbook, is re-work that
the registry exists to prevent.
