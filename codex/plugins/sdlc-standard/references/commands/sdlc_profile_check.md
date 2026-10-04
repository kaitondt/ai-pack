---
description: "Validate .codex/sdlc.profile.yaml: required fields, remaining placeholders, ID pattern consistency, path existence, skill references, gate definitions and safety flags. Run after any profile edit. Usage: /sdlc_profile_check"
---

# Validate the project profile

Load `sdlc_project`. Read `.codex/sdlc.profile.yaml` and check:

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
| 22 | `execution.agent_model` is set, and matches the `model:` frontmatter of every `.codex/agents/sdlc_*.md` | Warning — drift means agents run on a model nobody chose |
| 23 | every key in `execution.agent_model_overrides` names an installed agent | Warning |
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

Print a table of results and a verdict. On any Critical, state that the pack is not safe to
run and name the exact field to fix. Do not offer to "work around" a failed Critical.

Also report, as information rather than findings:

```
Baselined documents : {n}   ({list})
Active CR           : {.codex/.active_cr contents, or "none"}
Templates           : {n}/{n categories} registered   missing: {keys}
                      on_missing = {mode} -> what those categories will do
Toolchain           : {format}: {ok | library missing}
Mockup              : {kind}, {n} surfaces
Infrastructure      : {scm} / {ci} / {hosting} / {iac}   owner: {owner}
```

An active CR left in place after its report is written means baseline protection is off for
every document — worth noticing before someone edits one by accident.
