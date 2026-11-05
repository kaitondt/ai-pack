---
description: "Validate vibe.profile.yaml and the vibe/ memory folder against the pack — missing fields, commands that do not run, stage that disagrees with reality, hooks that do not fire. Read-only. Usage: /vibe-profile-check"
model: sonnet
effort: medium
---

# Profile check

Load `vibe-project`. Report only; change nothing.

## Checks

| # | Check | Severity if failing |
|---|---|---|
| 1 | `.claude/vibe.profile.yaml` exists and parses | Critical |
| 2 | `stage` is one of spike / prototype / mvp / production | Critical |
| 3 | No `<...>` placeholder in `project`, `stage`, `product.core_flows`, `commands.dev` | High |
| 4 | Each non-empty command in `commands` runs (exit 0) — `dev` checked by starting and stopping it | High |
| 5 | At `mvp`+: `test`, `lint`, `typecheck`, `build`, `audit` are non-empty and run | High |
| 6 | Every path in `paths` exists | Medium |
| 7 | `.gitignore` covers `.env*` and not `.env.example` | Critical |
| 8 | No committed file matches the hook's secret patterns (scan tracked files) | Critical |
| 9 | Reality vs stage: `product.public_url: true` or real users / real data while `stage` < `mvp` | High — report the SB-07 gap |
| 10 | Hooks fire: `guard-vibe-bash.py` blocks `git reset --hard` (exit 2); `guard-vibe-paths.py` blocks a fake `AKIA…` key; `guard-vibe-git.py` blocks `git commit --no-verify -m x` | Critical — SB-01/02 and GT-01..08 enforcement is off |
| 11 | `python` on PATH is a real interpreter (Windows Store alias check) | Critical |
| 12 | `slices.max_files` ≤ 15 and `max_changed_lines` ≤ 800 | Medium — a budget that big is not a budget |
| 13 | `loop.max_fix_attempts` between 2 and 5 | Medium |
| 14 | `debt.block_graduation_on_due` is true | High |
| 15 | STATE.md "updated" commit exists in git history | Low — stale handoff |
| 16 | Sibling pack profiles present → report which, and whether `graduation.handoff_to` agrees | Info |
| 17 | `verification.ui_check` set when the product has a UI | Medium |

<!-- model-policy:claude -->
**Expected agent models and effort** (check 18).
Tiers: heavy — `vibe-planner`, `vibe-reviewer`, `vibe-security-auditor`, `vibe-debugger`; standard — `vibe-builder`, `vibe-verifier`.

| `model_profile` | heavy tier | standard tier |
|---|---|---|
| `quality` | opus · `xhigh` | opus · `high` |
| `balanced` | opus · `high` | sonnet · `medium` |
| `budget` | sonnet · `high` | sonnet · `medium` |

An `execution.agent_model_overrides` or `execution.agent_effort_overrides` entry wins for its agent.
<!-- /model-policy:claude -->

| # | Check | Severity if failing |
|---|---|---|
| 18 | `execution.model_profile` is `quality`, `balanced` or `budget`, and the `model:` and `effort:` frontmatter of every `.claude/agents/vibe-*.md` matches the model it resolves to (see the table above) | Medium |

| 19 | Every file under `.claude/rules/project/` is listed in `project_rules`, every entry's file exists, and no `overrides` names a `rules/vibe/*` invariant | Medium — an unlisted rule is applied but never cited; relaxing an invariant is refused (`/vibe-rule-register`) |
| 20 | `commit:` exists, and no `slices.commit_format` is left over (it is ignored — offer to move it into `commit.format` with `/vibe-init`); `commit.format` contains `{SUMMARY}`, contains `{ID}` unless `commit.no_id` is set, uses no token but `{ID}` / `{ACTION}` / `{SUMMARY}`; `commit.id_pattern`, when set, compiles and matches `INT-001.1` | High — every commit is blocked, or none is checked (GT-01) |
| 21 | `commit.actions` non-empty, one word per entry; `commit.allow_push: true` only with a non-empty `commit.protected_branches` | Medium |

## Report

```
Profile check — {project}                     stage: {stage}
  Critical : {n}   High : {n}   Medium : {n}   Low : {n}
  {# · check · finding · fix}
  Verdict  : {ready | fix Critical/High first}
```
