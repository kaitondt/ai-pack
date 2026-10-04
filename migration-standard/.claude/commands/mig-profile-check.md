---
description: "Validate .claude/migration.profile.yaml: required fields, remaining placeholders, ID pattern consistency, path existence, skill references, and safety flags. Run after any profile edit. Usage: /mig-profile-check"
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
| 17 | `execution.agent_model` is set, and matches the `model:` frontmatter of every `.claude/agents/mig-*.md` | Warning — drift means agents run on a model nobody chose |
| 18 | every key in `execution.agent_model_overrides` names an installed agent | Warning |
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

Print a table of results and a verdict. On any Critical, state that the pack is not
safe to run and name the exact field to fix. Do not offer to "work around" a failed
Critical.

Also report, as information rather than findings:

```
Templates       : {n}/{n categories} registered   missing: {keys}
                  on_missing = {mode} -> what those categories will do
Toolchain       : {format}: {ok | library missing}
Legacy documents: {n} files under {legacy_documents_dir} — inputs only (DIO-08)
Mockup          : {kind}, fidelity {fidelity}, {n} surfaces
Infrastructure  : {scm} / {ci} / {hosting} / {iac}   owner: {owner}
Coexistence     : {strategy}, system of record {x}, dual write {y/n}
```
