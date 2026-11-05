# Common Hooks

Hooks are the mechanical backstop for rules the model is asked to follow. Anything that
must be true *every* time belongs in a hook, not only in a skill.

## Principles

- Hooks run project-local tooling only. Never fetch and execute a remote script.
- A hook is fast or it is a tax. Target under 2s for PreToolUse, under 10s for PostToolUse.
- Cap runtime with a timeout so a stuck process is reaped instead of accumulating.
- A hook that blocks must say why, in one line, and name the rule ID.

## Recommended set for a migration project

| Event | Matcher | Purpose |
|---|---|---|
| PreToolUse | `Write\|Edit` | `guard-readonly-paths.py` — deny writes under legacy/generated paths (`LR-01`, `LR-04`) |
| PreToolUse | `Bash\|PowerShell` | `guard-mig-git.py` — git commands follow `rules/migration/git-commit.md`: message format, explicit staging, nothing under legacy or another read-only path committed, the active CR id (`.claude/.active_cr`) on commits under `change_request.governed_paths`, no secret, bypass, history rewrite or push (`GT-01..GT-08`) |
| PreToolUse | `Write\|Edit` | `check-doc-rules.py` — remind of document rules when the path is a deliverable |
| SessionStart | — | `check-profile-loaded.py` — fail fast when the profile is missing or unresolved |
| PostToolUse | `Write\|Edit` | `format-on-edit.py` — runs `{{profile.target.build.on_edit}}`: the repository's formatter, then its linter, on the edited target file only |
| Stop | — | build verification |

Ordering, when several run on the same event: format → lint → type-check → build.

## Type-check hooks

Use the incremental flag and an explicit build-info path, and wrap in a timeout.
Without incremental, each edit re-checks the whole program; with edits arriving faster
than checks finish, processes stack up until the machine stalls.

## Writing a blocking hook

Exit code 2 blocks the tool call and returns stderr to the model. Print one actionable
line:

```
[LR-01] BLOCKED: src/legacy/** is read-only for the whole project. Write analysis to docs/ instead.
```

Do not block on style opinions. Block on invariants: read-only paths, secrets, oversized
files, missing profile.
