---
description: "Validate vibe.profile.yaml and the vibe/ memory folder against the pack — missing fields, commands that do not run, stage that disagrees with reality, hooks that do not fire. Read-only. Usage: /vibe-profile-check"
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
| 10 | Hooks fire: `guard-vibe-bash.py` blocks `git reset --hard` (exit 2); `guard-vibe-paths.py` blocks a fake `AKIA…` key | Critical — SB-01/02 enforcement is off |
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
