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
| PreToolUse | `Write\|Edit` | `guard_readonly_paths.py` — deny writes under legacy/generated paths (`LR-01`, `LR-04`) |
| PreToolUse | `Write\|Edit` | `check_doc_rules.py` — remind of document rules when the path is a deliverable |
| SessionStart | — | `check_profile_loaded.py` — fail fast when the profile is missing or unresolved |
| PostToolUse | `Write\|Edit` | formatter, then linter, then incremental type-check |
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
