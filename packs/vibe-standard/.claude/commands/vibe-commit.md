---
description: "Commit a verified slice, bug fix or debt paydown in the format agreed at /vibe-init ({ID} {ACTION} {SUMMARY} by default): check for secrets and protected paths, stage explicit paths, take the ID from the intent/bug/debt file, compose the message, confirm, commit. Never pushes. Usage: /vibe-commit [ID] [ACTION] [summary] [-- path ...]"
---

# Commit

Load `vibe-project`, then `rules/vibe/git-commit.md` (GT-01..GT-09). The format and the
switches come from `{{profile.commit}}` — `commit.format` is the only format the pack reads. A
profile with no `commit:` section uses the template defaults: say so, and offer `/vibe-init` to
choose the format. An old `slices.commit_format` key is ignored; offer to move it into
`commit.format` and delete it.

`/vibe-build` runs Steps 2–7 of this command at its commit step. Run it on its own for work that
was done outside `/vibe-build` — a `/vibe-fix`, a debt paydown, a `vibe/` update, a decision.

`hooks/guard-vibe-git.py` and `hooks/guard-vibe-bash.py` check every `git` command this command
runs. A block is a finding to resolve: never retry with `--no-verify`, a different staging
trick or a reworded message that only satisfies the pattern.

## Step 1 — See what changed

`git status --porcelain=v1`, `git diff --stat`, `git diff --cached --stat`. Report the branch
(stop if it is in `{{profile.commit.protected_branches}}`), what is staged, modified and
untracked. Nothing changed → say so and stop.

## Step 2 — Is it ready to commit? (GT-04)

- A slice: its done-when checks were seen running (VT-01) and the stage's commands passed. Not
  verified → it is not committed under the slice ID. Offer to verify first (`/vibe-verify`), or
  to commit it to an `{{profile.loop.attempt_branch_prefix}}<slice>-<n>` branch as an attempt.
- A bug fix: the regression check exists and passes (VT-07).
- At `mvp`+, a slice that touched auth, the data model or payments: `/vibe-review` has no open
  Critical.

## Step 3 — Decide what goes into this commit

The scope is, in order: the paths given after `--`; otherwise what is already staged; otherwise
the files the slice changed plus its `vibe/` bookkeeping (STATE.md, the intent tick, new
`DEBT-*` / `IDEA-*` / `DEC-*` entries). Unrelated changes go into their own commit (GT-09).

For each candidate path:

| Check | Rule | On failure |
|---|---|---|
| a file in `{{profile.security.env_files}}`, another `.env` variant (not `.env.example`), a key or credential file, or a diff line that looks like a secret | GT-05, SB-01 | drop it, never stage it, tell the user — and to rotate a real secret |
| matches `{{profile.security.protected_paths}}` and not `{{profile.commit.regenerated_globs}}` | GT-03 | drop it; it was hand-edited |
| debug output, `.only`, commented-out code, a stray file | VT-05 | point it out; let the user decide |

## Step 4 — Take the ID (GT-09)

From, in order: the argument; the slice being built (`INT-{NNN}.{n}`); the `BUG-*`, `DEBT-*`,
`DEC-*` or `IDEA-*` entry the diff adds or closes; the branch name. The ID must exist in the
intent file or the log it belongs to (ID-03). None → ask, or use `{{profile.commit.no_id}}` when
the project defined one.

## Step 5 — Action, summary, message

The action is one word from `{{profile.commit.actions}}` (GT-01): a new slice is usually `ADD`,
a changed behaviour `UPDATE`, a bug `FIX`, a paydown `REFACTOR`, a decision or promotion
`CONFIRM`. The summary says what the commit does, imperative, at most
`{{profile.commit.summary_max}}` characters, in `{{profile.commit.summary_language}}`. Compose
the subject with `{{profile.commit.format}}`, and check it against the format before showing it.

## Step 6 — Confirm

```
Commit preview
  Branch   : {branch}
  Files    : {n}   ({n} in vibe/)
    {status} {path}
  Excluded : {path} — {reason}
  Verified : {done-when n/n seen running | not a slice}
  Message  : {subject}
```

At `spike` and `prototype` a slice commit inside `/vibe-build` may go ahead without waiting,
unless the slice touched auth, the data model, payments or anything irreversible. Everywhere
else, wait for the user's answer.

## Step 7 — Stage and commit

```
git add -- <path> <path> ...
git commit -F <message file>
```

Stage by name (GT-02); write the message to a temporary file outside the working tree and commit
with `-F`; never open an editor. A failing pre-commit hook is fixed, not bypassed (GT-06). Then
delete the message file and run `git log -1 --stat`.

## Step 8 — Report

```
Committed {short hash} on {branch}: {subject}
  {n} files   +{added} / -{removed}
  Intent      : {INT-NNN.n ticked with the hash | n/a}
  Not committed: {paths left modified, and why}
  Push        : not done — `/vibe-ship` or `git push` when you are ready
```

Tick the slice in its intent file with the hash, and update STATE.md Now / Next / Last verified,
in the same commit when they are part of the slice, or in a follow-up `vibe/` commit. Push only
when `{{profile.commit.allow_push}}` is true *and* the user asked for it (GT-08).
