---
description: "Commit management documents in the format agreed at /pm-init ({ID} {ACTION} {SUMMARY} by default): check the changes against the baseline, archive and secret rules, stage explicit paths, anchor the ID, compose the message, confirm, commit. Never pushes. Usage: /pm-commit [ID] [ACTION] [summary] [-- path ...]"
---

# Commit

Load `pm-project`, then `rules/pm/git-commit.md` (GT-01..GT-09). The format and the switches
come from `{{profile.commit}}`; a profile with no `commit:` section uses the defaults in the
template — say so, and suggest `/pm-init` to choose the format.

`hooks/guard-pm-git.py` checks every `git` command this command runs. A block from it is a
finding to resolve, not an obstacle to route around: never retry with `--no-verify`, a
different staging trick or a reworded message that only satisfies the pattern.

When a technical pack (sdlc / migration) is installed in the same repository, its own commit
command governs the product files; this one is for the files under `{{profile.paths.pm_root}}`
and the management registers. Both use the same format when the profiles agree — check that
they do, and say so when they do not.

## Step 1 — See what changed

Run `git status --porcelain=v1` and `git diff --stat` / `git diff --cached --stat`. Report:

- the branch — and stop if it is in `{{profile.commit.protected_branches}}` (GT-06);
- what is already staged, what is modified but unstaged, what is untracked;
- an operation in progress (merge, rebase, cherry-pick) — finish or abort it with the user
  first.

Nothing changed → say so and stop.

## Step 2 — Decide what goes into this commit

The scope is, in order: the paths given after `--`; otherwise what is already staged; otherwise
the files the current task changed. Never everything that happens to be modified.

If the candidate files fall into independent groups — a weekly report and an unrelated risk
update, a CR applied and a working file — propose one commit per group (GT-09) and handle them
one at a time.

For each candidate path, check before staging:

| Check | Rule | On failure |
|---|---|---|
| matches `{{profile.baselines.readonly_globs}}` and is modified, deleted or renamed (a new snapshot is fine) | GT-03, PB-03 | drop it; tell the user what changed it |
| a document in `{{profile.baselines.registered}}` | GT-04, PB-03 | needs `.claude/.active_pm_cr`; without one, stop and point to `/pm-change-assess` |
| an env, key or credential file, a line that looks like a secret, or personal data the deliverable does not need | GT-05 | drop it, never stage it, tell the user |
| a working file that is not marked as one (MD-10), presented as a deliverable | MD-10 | point it out; let the user decide |

## Step 3 — Anchor the ID (GT-09)

Take the ID from, in order:

1. the argument the user gave;
2. `.claude/.active_pm_cr`, when it names a CR (not `EDITORIAL`) — mandatory when a baselined
   document is in the commit (GT-04);
3. the IDs the diff itself touches: `CR-*`, `RSK-*`, `ISS-*`, `DEC-*`, `ACT-*`, `CAPA-*`,
   `MTG-*`, `LL-*` rows added or changed, or the document id of the deliverable;
4. the branch name.

Every ID must exist — in a register, a log or a document — and match
`{{profile.commit.id_pattern}}` (or the default: upper case with a digit). Several IDs are
joined with `{{profile.commit.id_separator}}`. A periodic report with no single ID takes the
meeting or report id the project uses; when nothing gives an ID, ask the user, and offer
`{{profile.commit.no_id}}` only when the project defined it. Never invent one.

## Step 4 — Choose the action and write the summary

The action is one word from `{{profile.commit.actions}}`, chosen by what the change *does*
(the table in GT-01): a new plan or register entry is `ADD`, a status or forecast change is
`UPDATE`, a baseline or CCB decision recorded is `CONFIRM`, a gate review or audit is `REVIEW`.

The summary says what this commit does, imperative, at most `{{profile.commit.summary_max}}`
characters, in `{{profile.commit.summary_language}}`. A number in the summary carries its unit
(MD-05). Compose the subject with `{{profile.commit.format}}`; add a body when
`{{profile.commit.body}}` is `required` or the why is not obvious — the approval, the authority,
the CR. Check the subject against the format yourself before showing it.

## Step 5 — Confirm

Show, and wait for the user's answer:

```
Commit preview
  Branch   : {branch}
  Files    : {n}
    {status} {path}
  Excluded : {path} — {reason}          (archive / baselined without CR / secret / other group)
  Message  :
    {subject}

    {body}
```

The user may edit the message or the file list; re-run Steps 2–4 on a changed list.

## Step 6 — Stage and commit

```
git add -- <path> <path> ...
git commit -F <message file>
```

Stage the listed paths by name (GT-02). Write the message to a temporary file outside the
working tree and commit with `-F` — it survives quotes, non-ASCII text and several lines; never
open an editor. If a repository pre-commit hook fails, report its output and fix the cause; do
not bypass it (GT-06). Then delete the message file and run `git log -1 --stat` to confirm.

## Step 7 — Report

```
Committed {short hash} on {branch}
  {subject}
  {n} files   +{added} / -{removed}
  Not committed: {paths left modified, and why}
  Push         : not done — `git push {remote} {branch}` when you are ready
```

Push only when `{{profile.commit.allow_push}}` is true *and* the user asked for it (GT-08).
