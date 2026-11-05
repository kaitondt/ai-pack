---
description: "Validate .claude/migration.profile.yaml: required fields, remaining placeholders, ID pattern consistency, path existence, skill references, and safety flags. Run after any profile edit. Usage: /mig-profile-check"
model: sonnet
effort: medium
---

# Validate the migration profile

Load `mig-project`. Read `.claude/migration.profile.yaml` and check:

| # | Check | Severity if failed |
|---|---|---|
| 1 | file exists and parses as YAML | Critical |
| 2 | `schema_version` present and supported | Critical |
| 3 | no `<...>` placeholder remains in a required field | Critical |
| 4 | `legacy.readonly` is `true` | Critical — the safety model depends on it |
| 5 | `legacy.root`, `ui_source`, `logic_source`, `db_source` all exist on disk | Critical |
| 6 | `ids.module_example` matches `ids.module_pattern` | Critical |
| 7 | `ids.doc_id_format` contains `{MODULE}`, `{TYPE}` and `{NNN}` | Critical |
| 8 | every `paths.*` value is repo-relative and creatable | Warning |
| 9 | every `bd_categories[].skill` names an installed skill | Critical |
| 10 | every `bd_categories[].dir` is unique | Critical |
| 11 | every `target.surfaces[].id_suffix` is unique and consistent with `module_pattern` | Critical |
| 12 | `target.build.order` is non-empty and each command is runnable | Warning |
| 13 | every `legacy.excluded[]` entry has a non-empty `reason` | Critical |
| 14 | `document.auto_version_bump` is `false` | Warning |
| 15 | `language.by_path` covers every directory under `paths.docs_root` | Warning |
| 16 | `constraints.readonly_globs` includes `legacy.root` | Critical |

<!-- model-policy:claude -->
**Expected agent models and effort** (check 17).
Tiers: heavy — `mig-legacy-analyst`, `mig-requirements-writer`, `mig-bd-orchestrator`, `mig-bd-designer`, `mig-dd-designer`, `mig-reviewer`, `mig-defect-triager`, `mig-cr-engineer`; standard — `mig-implementer`, `mig-tester`, `mig-test-automator`, `mig-infra-engineer`, `mig-mockup-designer`, `mig-uat-engineer`.

| `model_profile` | heavy tier | standard tier |
|---|---|---|
| `quality` | opus · `xhigh` | opus · `high` |
| `balanced` | opus · `high` | sonnet · `medium` |
| `budget` | sonnet · `high` | sonnet · `medium` |

An `execution.agent_model_overrides` or `execution.agent_effort_overrides` entry wins for its agent.
<!-- /model-policy:claude -->

| # | Check | Severity if failed |
|---|---|---|
| 17 | `execution.model_profile` is `quality`, `balanced` or `budget`, and the `model:` and `effort:` frontmatter of every `.claude/agents/mig-*.md` matches the model it resolves to (see the table above) | Warning |
| 18 | every key in `execution.agent_model_overrides` and `execution.agent_effort_overrides` names an installed agent | Warning |
| 19 | every `change_request.cascade` entry names a `bd_categories` key or one of `indexes` / `translations` / `test_cases` | Warning |
| 20 | `change_request.id_source` is `client` | Critical — a generated CR id detaches the report from the client's CR list |
| 21 | every `bug_trace.commit_ref_patterns[]` entry compiles as a regex; `bug_trace.mainline`, when set, names a branch that exists | Warning — a bad pattern silently drops ticket links from every trace |
| 22 | every `templates.registry[]` entry with `status: provided` names a readable file | Critical — the team believes a form is in force |
| 23 | every format in `templates.formats_enabled` has a working library (`openpyxl`, `python-docx`) | Critical — the run fails forty files in, not on the first |
| 24 | every `templates.registry[].key` names a `bd_categories` key or a known non-design category, and no key repeats | Warning |
| 25 | `templates.root` and `templates.legacy_documents_dir` are both covered by `constraints.readonly_globs` | Critical — a legacy document or a blank form is writable |
| 26 | no `templates.registry[]` path is inside `templates.legacy_documents_dir` | Critical — a legacy document registered as a template (DIO-08) |
| 27 | `mockup.kind` is one of `html` / `canvas` / `figma` / `image` / `none`; when not `none`, `mockup.dir` is set and every id in `mockup.surfaces` names a `target.surfaces[]` entry | Warning |
| 28 | `mockup.fidelity` is one of `as-is` / `restyled` / `redesigned`; every `fidelity_exceptions[]` entry has a non-empty `decision` | Critical — an exception with no decision is an invention (NI-02) |
| 29 | when `mockup.kind: figma`, `figma.file_url` is set or `figma.export_dir` exists | Warning — otherwise the design cannot be read at all |
| 30 | `target.environments[]` is non-empty, exactly one is `production_like`, and the `legacy-prod` entry (where present) is `readonly: true` | Warning |
| 31 | **no `infrastructure` field names the legacy production environment as a deployment target** | Critical — LR-01 covers infrastructure |
| 32 | `infrastructure.scm.platform` and `ci.platform` are resolved, and `ci.definition_path` matches the platform's convention | Warning — an unresolved platform stops every infra task |
| 33 | `infrastructure.owner` is set; when it is not `this project`, `repo_may_write_infra` is `false` | Warning |
| 34 | every stage in `infrastructure.ci.stages` maps to a `target.build` command, or is explicitly extra | Warning |
| 35 | when `coexistence.strategy` is not `big-bang`: `system_of_record` is set, and `conflict_resolution` is non-empty wherever `dual_write` is true | Critical — two writers with no rule is the defect class that ends migrations |
| 36 | `data_migration.reconciliation` is non-empty and `rehearsals_required` ≥ 1 | Warning — a migration judged on completing, not reconciling |
| 37 | `rollback.target` and `rollback.data_strategy` are both set | Warning — rollback to a legacy system needs to say where target-created records go |
| 38 | every `target.coding_standards[].source` exists, and every `digest` exists under `.claude/rules/<stack>/` with `paths:` front matter | Warning — the client standard is not applied to the code it governs |
| 39 | the stack rule directories under `.claude/rules/` (`java`, `typescript`, `react`, `sql`) match `target.stack`: none missing for a stack in use, none left for a stack that is not | Warning |
| 40 | every `target.build.on_edit[]` entry has `glob`, `run` and an existing `cwd`; its tool resolves; it finishes on one matching file within its `timeout` | Warning — a slow or broken entry stalls or silently skips every edit |
| 41 | no `target.build.on_edit[].glob` matches anything under `legacy.root` | Critical — the hook would reformat read-only legacy source (LR-01) |
| 42 | every `templates.registry[].authority` is empty, `xlsx` or `docx`, and a non-empty value matches the entry's own `format` or `output_format` | Critical — a regeneration would overwrite reviewers' edits (DIO-10) |
| 43 | `language.correction_log`, when set, exists and has its header row | Warning |
| 44 | once automation exists, `testing.automation.list_command` runs and lists tests, and `tc_id_in` is `title`, `tag` or `annotation` | Warning — scripts cannot be reconciled with the cases |
| 45 | every `project_rules[].file` exists, and every file under `.claude/rules/project/` is registered | Warning — an unregistered rule is applied but never ranked or cited |
| 46 | project rule ids match `PRJ-{TOPIC}-{NN}` with no duplicates, and no `overrides` entry names an invariant (`rules/migration/*`, the security non-negotiables) or relaxes legacy parity | Critical — a project rule may tighten an invariant, never relax it |
| 47 | every project rule that overrides a pack rule records its approver and date | Warning |
| 48 | `commit:` exists; `commit.format` contains `{SUMMARY}`, contains `{ID}` unless `commit.no_id` is set, and uses no token but `{ID}` / `{ACTION}` / `{SUMMARY}`; `commit.id_pattern`, when set, compiles and matches `ids.module_example` and the document ids | Critical — every commit is blocked, or none is checked (GT-01) |
| 49 | `commit.actions` is non-empty, one word per entry; `review_before_commit` is `off`, `recommend` or `require`; `body` is `optional`, `required` or `none` | Warning |
| 50 | `commit.regenerated_globs` names no path under `legacy.root` | Critical — it would let a commit change the legacy source (LR-01) |
| 51 | `guard-mig-git.py` is registered for `Bash\|PowerShell` and blocks `git commit --no-verify -m x` (exit 2) | Critical — the commit rules are unenforced |
| 52 | `commit.allow_push: true` only with a non-empty `commit.protected_branches` | Warning — the AI could push straight to the mainline |
| 53 | `change_request.governed_paths` is non-empty and every glob matches a `paths.*` directory (design, detail design, test design, change requests) | Warning — an active CR would not be attributed in commits (GT-04) |
| 54 | `.claude/.active_cr`, when present, holds `PENDING` or an id matching `change_request.id_format`, and a report or an analysis for that id exists | Warning — a marker left behind attributes unrelated commits to a closed CR |

Checks 45–47 are the summary; `/mig-rule-register --check` runs the full set.

Print a table of results and a verdict. On any Critical, state that the pack is not
safe to run and name the exact field to fix. Do not offer to "work around" a failed
Critical.

Also report, as information rather than findings:

```
Templates       : {n}/{n categories} registered   missing: {keys}
                  on_missing = {mode} -> what those categories will do
Toolchain       : {format}: {ok | library missing}
Project rules   : {n} active in {n} files   overrides: {n}   review-only: {n}
Legacy documents: {n} files under {legacy_documents_dir} — inputs only (DIO-08)
Mockup          : {kind}, fidelity {fidelity}, {n} surfaces
Infrastructure  : {scm} / {ci} / {hosting} / {iac}   owner: {owner}
Coexistence     : {strategy}, system of record {x}, dual write {y/n}
Commit          : {format}   preset {preset}   push: {AI|user}   protected: {branches}
Active CR       : {.claude/.active_cr contents, or "none"}
```

An active CR left in place after its report is written attributes every later commit under the
governed paths to it — worth noticing before it happens.
