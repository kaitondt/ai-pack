# Common Hooks

Hooks are the mechanical backstop for rules the model is asked to follow. Anything that
must be true *every* time belongs in a hook, not only in a skill.

## Principles

- Hooks run project-local tooling only. Never fetch and execute a remote script.
- A hook is fast or it is a tax. Target under 2s for PreToolUse, under 10s for PostToolUse.
- Cap runtime with a timeout so a stuck process is reaped instead of accumulating.
- A hook that blocks must say why, in one line, and name the rule ID.

## Recommended set for a development project

| Event | Matcher | Purpose |
|---|---|---|
| SessionStart | — | `check_profile_loaded.py` — fail fast when the profile is missing or unresolved |
| PreToolUse | `Write\|Edit` | `guard_protected_paths.py` — deny edits to generated files and baselined documents without a CR (`BL-02`, `BL-07`) |
| PreToolUse | `Write\|Edit` | `check_doc_rules.py` — surface the document rules for the deliverable being written |
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
[BL-02] BLOCKED: docs/01.requirements/SRS.md is baselined at 1.0.0. Changing it needs an approved CR. Run /sdlc_cr_analyze.
```

Block on invariants: baselined documents, generated files, secrets, oversized files,
missing profile. Do not block on style opinions — that is what the formatter is for.

## When a rule should become a hook

From the refinement loop (`COMMAND-FLOW.md` §3): a rule that is clearly written, mechanically
checkable, and still violated across rounds does not need restating. It needs enforcing.
Move it to a hook and stop spending review capacity on it.
