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

| 22 | `execution.model_profile` is `quality`, `balanced` or `budget`, and the `model:` and `effort:` frontmatter of every `.claude/agents/sdlc-*.md` matches the model it resolves to (see 

Print a table of results and a verdict. On any Critical, state that the pack is not safe to
run and name the exact field to fix. Do not offer to "work around" a failed Critical.

Also report, as information rather than findings:

```
Baselined documents : {n}   ({list})
Active CR           : {.claude/.active_cr contents, or "none"}
Templates           : {n}/{n categories} registered   missing: {keys}
                      on_missing = {mode} -> what those categories will do
Toolchain           : {format}: {ok | library missing}
Mockup              : {kind}, {n} surfaces
Infrastructure      : {scm} / {ci} / {hosting} / {iac}   owner: {owner}
```

An active CR left in place after its report is written means baseline protection is off for
every document — worth noticing before someone edits one by accident.
