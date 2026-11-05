---
description: "Validate .claude/sdlc.profile.yaml: required fields, remaining placeholders, ID pattern consistency, path existence, skill references, gate definitions and safety flags. Run after any profile edit. Usage: /sdlc-profile-check"
model: sonnet
effort: medium
---

# Validate the project profile

Load `sdlc-project`. Read `.claude/sdlc.profile.yaml` and check:

| # | Check | Severity if failed |
|---|---|---|
| 1 | file exists and parses as YAML | Critical |
| 2 | `schema_version` present and supported | Critical |
| 3 | no `<...>` placeholder remains in a required field | Critical |
| 4 | every role in `stakeholders` is filled | Critical — an unowned decision is an assumption (RS-02) |
| 5 | every `scope.out_of_scope[]` entry has a non-empty `reason` | Critical |
| 6 | `system.root` exists on disk | Critical |
| 7 | `ids.module_example` matches `ids.module_pattern` | Critical |
| 8 | `ids.doc_id_format` contains `{MODULE}`, `{TYPE}` and `{NNN}` | Critical |
| 9 | every `paths.*` value is repo-relative and creatable | Warning |
| 10 | every `bd_categories[].skill` names an installed skill | Critical |
| 11 | every `bd_categories[].dir` is unique | Critical |
| 12 | every `system.surfaces[].id_suffix` is unique and consistent with `module_pattern` | Critical |
| 13 | `system.build.order` is non-empty and each command is runnable | Warning |
| 14 | exactly one `system.environments[]` entry is marked `production_like` | Warning — ST has nowhere to run without it |
| 15 | every phase in `gates` has both `entry` and `exit` lists, non-empty | Critical |
| 16 | `document.auto_version_bump` is `false` | Warning |
| 17 | `constraints.baseline_change_requires_cr` is `true` | Critical — BL-02 is unenforced without it |
| 18 | every `constraints.baselined[].path` exists on disk | Warning |
| 19 | `language.by_path` covers every directory under `paths.docs_root` | Warning |
| 20 | every `testing.levels[].basis` names a real `paths.*` key | Critical — the V-model binding is unresolvable otherwise |
| 21 | `quality.targets` has no unset value, and `quality.severity` has at least 3 levels | Warning |

<!-- model-policy:claude -->
**Expected agent models and effort** (check 22).
Tiers: heavy — `sdlc-analyst`, `sdlc-bd-orchestrator`, `sdlc-bd-designer`, `sdlc-dd-designer`, `sdlc-reviewer`, `sdlc-defect-triager`, `sdlc-cr-engineer`, `sdlc-maintenance-engineer`; standard — `sdlc-implementer`, `sdlc-tester`, `sdlc-test-automator`, `sdlc-infra-engineer`, `sdlc-mockup-designer`, `sdlc-uat-coordinator`.

| `model_profile` | heavy tier | standard tier |
|---|---|---|
| `quality` | opus · `xhigh` | opus · `high` |
| `balanced` | opus · `high` | sonnet · `medium` |
| `budget` | sonnet · `high` | sonnet · `medium` |

An `execution.agent_model_overrides` or `execution.agent_effort_overrides` entry wins for its agent.
<!-- /model-policy:claude -->

| # | Check | Severity if failed |
|---|---|---|
| 22 | `execution.model_profile` is `quality`, `balanced` or `budget`, and the `model:` and `effort:` frontmatter of every `.claude/agents/sdlc-*.md` matches the model it resolves to (see the table above) | Warning |
| 23 | every key in `execution.agent_model_overrides` and `execution.agent_effort_overrides` names an installed agent | Warning |
| 24 | every `change_request.cascade` entry names a `bd_categories` key or one of `requirements` / `nfr` / `detail` / `mockup` / `indexes` / `translations` / `test_cases` | Warning |
| 25 | `change_request.id_source` is set, and `min_options` ≥ 2 | Warning |
| 26 | `maintenance.sla` covers every severity in `quality.severity` | Warning |
| 27 | every `bug_trace.commit_ref_patterns[]` entry compiles as a regex; `bug_trace.mainline`, when set, names a branch that exists | Warning — a bad pattern silently drops ticket links from every trace |
| 28 | every `templates.registry[]` entry with `status: provided` names a file that exists and is readable | Critical — the team believes a template is in force |
| 29 | every format in `templates.formats_enabled` has a working library (`openpyxl` for `xlsx`, `python-docx` for `docx`) | Critical — the run fails forty files in, not on the first |
| 30 | every `templates.registry[].key` names a `bd_categories` key or a known non-design category, and no key appears twice | Warning |
| 31 | every registered template path is covered by `constraints.readonly_globs` | Warning — the form itself is writable |
| 32 | `mockup.kind` is one of `html` / `canvas` / `figma` / `image` / `none`; when not `none`, `mockup.dir` is set and every id in `mockup.surfaces` names a `system.surfaces[]` entry | Warning |
| 33 | when `mockup.kind: figma`, `figma.file_url` is set or `figma.export_dir` exists — otherwise the design cannot be read at all | Warning |
| 34 | `infrastructure.scm.platform` and `infrastructure.ci.platform` are resolved (not `<placeholder>`), and `ci.definition_path` matches the platform's convention | Warning — an unresolved platform stops every infra task |
| 35 | `infrastructure.owner` is set; when it is not `this project`, `repo_may_write_infra` is `false` | Warning — otherwise the pack may commit into another team's infrastructure |
| 36 | every stage in `infrastructure.ci.stages` maps to a `system.build` command, or is explicitly extra | Warning — a pipeline testing what no developer can reproduce |
| 37 | every `system.coding_standards[].source` exists, and every `digest` exists under `.claude/rules/<stack>/` with `paths:` front matter | Warning — the client standard is not applied to the code it governs |
| 38 | the stack rule directories under `.claude/rules/` (`java`, `typescript`, `react`, `sql`) match `system.stack`: none missing for a stack in use, none left for a stack that is not | Warning |
| 39 | every `system.build.on_edit[]` entry has `glob`, `run` and an existing `cwd`; its tool resolves; it finishes on one matching file within its `timeout` | Warning — a slow or broken entry stalls or silently skips every edit |
| 40 | every `templates.registry[].authority` is empty, `xlsx` or `docx`, and a non-empty value matches the entry's own `format` or `output_format` | Critical — a regeneration would overwrite reviewers' edits (DIO-09) |
| 41 | `language.correction_log`, when set, exists and has its header row | Warning |
| 42 | once automation exists, `testing.automation.list_command` runs and lists tests, and `tc_id_in` is `title`, `tag` or `annotation` | Warning — scripts cannot be reconciled with the cases |
| 43 | every `project_rules[].file` exists, and every file under `.claude/rules/project/` is registered | Warning — an unregistered rule is applied but never ranked or cited |
| 44 | project rule ids match `PRJ-{TOPIC}-{NN}` with no duplicates, and no `overrides` entry names an invariant (`rules/sdlc/*`, the security non-negotiables) | Critical — a project rule may tighten an invariant, never relax it |
| 45 | every project rule that overrides a pack rule has a `DEC-*` in `paths.decision_log` | Warning |

| 46 | `commit:` exists; `commit.format` contains `{SUMMARY}`, contains `{ID}` unless `commit.no_id` is set, and uses no token but `{ID}` / `{ACTION}` / `{SUMMARY}`; `commit.id_pattern`, when set, compiles and matches the module and document ids in `ids.*` | Critical — every commit is blocked, or none is checked (GT-01) |
| 47 | `commit.actions` is non-empty, one word per entry; `review_before_commit` is `off`, `recommend` or `require`; `body` is `optional`, `required` or `none` | Warning |
| 48 | `commit.regenerated_globs` names only paths that are also in `constraints.readonly_globs` and that a generator really writes | Warning — a hand-edited path listed here escapes GT-03 |
| 49 | `guard-sdlc-git.py` is registered for `Bash\|PowerShell` and blocks `git commit --no-verify -m x` (exit 2) | Critical — the commit rules are unenforced |
| 50 | `commit.allow_push: true` only with a non-empty `commit.protected_branches` | Warning — the AI could push straight to the mainline |

Checks 43–45 are the summary; `/sdlc-rule-register --check` runs the full set.

Print a table of results and a verdict. On any Critical, state that the pack is not safe to
run and name the exact field to fix. Do not offer to "work around" a failed Critical.

Also report, as information rather than findings:

```
Baselined documents : {n}   ({list})
Active CR           : {.claude/.active_cr contents, or "none"}
Templates           : {n}/{n categories} registered   missing: {keys}
                      on_missing = {mode} -> what those categories will do
Toolchain           : {format}: {ok | library missing}
Project rules       : {n} active in {n} files   overrides: {n}   review-only: {n}
Mockup              : {kind}, {n} surfaces
Infrastructure      : {scm} / {ci} / {hosting} / {iac}   owner: {owner}
Commit              : {format}   preset {preset}   push: {AI|user}   protected: {branches}
```

An active CR left in place after its report is written means baseline protection is off for
every document — worth noticing before someone edits one by accident.
