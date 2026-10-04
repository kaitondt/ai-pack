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

| 17 | `execution.model_profile` is `quality`, `balanced` or `budget`, and the `model:` and `effort:` frontmatter of every `.claude/agents/mig-*.md` matches the model it resolves to (see 

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
