---
description: "Validate vibe.profile.yaml and the vibe/ memory folder against the pack — missing fields, commands that do not run, stage that disagrees with reality, hooks that do not fire. Read-only. Usage: /vibe_profile_check"
---

# Profile check

> **Installed as a Claude Code plugin?** The pack's files are not in this repository's
> `.claude/` — they live in the plugin directory `${CLAUDE_PLUGIN_ROOT}` (if that token is
> not substituted, use the path from the `[vibe] plugin root: …` line printed at session
> start). Map every "pack" path in this command as follows:
>
> | Pack path in this command | Plugin location |
> |---|---|
> | profile template `profile/vibe.profile.yaml` | `<plugin root>/templates/profile/vibe.profile.yaml` |
> | `.claude/CLAUDE.md` template | `<plugin root>/templates/CLAUDE.md` |
> | `.claude/rules/` | `<plugin root>/templates/rules/` — **copy into this project's `.claude/rules/`** (plugins cannot load rules; they only apply from the project). Never overwrite an existing file without asking. |
> | `.claude/hooks/*.py` | `<plugin root>/hooks/` — already registered by the plugin; do **not** copy `settings.json` hooks, they would run twice |
> | `.claude/agents/vibe_*.md` | read-only in the plugin (overwritten on update). To change an agent's `model:` or tools, copy it into this project's `.claude/agents/` and edit the copy — a project agent overrides the plugin agent of the same name |
> | `.claude/skills/` | read-only in the plugin. Propose skill/rule changes as a patch to the pack's source repository, or override locally by copying the skill into this project's `.claude/skills/` |
>
> The profile `.claude/vibe.profile.yaml` and everything the pack generates stay in this project, as
> in a manual install.


Load `vibe_project`. Report only; change nothing.

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
| 10 | Hooks fire: `guard_vibe_bash.py` blocks `git reset --hard` (exit 2); `guard_vibe_paths.py` blocks a fake `AKIA…` key | Critical — SB-01/02 enforcement is off |
| 11 | `python` on PATH is a real interpreter (Windows Store alias check) | Critical |
| 12 | `slices.max_files` ≤ 15 and `max_changed_lines` ≤ 800 | Medium — a budget that big is not a budget |
| 13 | `loop.max_fix_attempts` between 2 and 5 | Medium |
| 14 | `debt.block_graduation_on_due` is true | High |
| 15 | STATE.md "updated" commit exists in git history | Low — stale handoff |
| 16 | Sibling pack profiles present → report which, and whether `graduation.handoff_to` agrees | Info |
| 17 | `verification.ui_check` set when the product has a UI | Medium |

## Report

```
Profile check — {project}                     stage: {stage}
  Critical : {n}   High : {n}   Medium : {n}   Low : {n}
  {# · check · finding · fix}
  Verdict  : {ready | fix Critical/High first}
```
