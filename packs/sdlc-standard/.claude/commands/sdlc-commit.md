---
description: "Commit the current work in the format agreed at /sdlc-init ({ID} {ACTION} {SUMMARY} by default): check the changes against the read-only, baseline and secret rules, stage explicit paths, anchor the ID, compose the message, confirm, commit. Never pushes. Usage: /sdlc-commit [ID] [ACTION] [summary] [-- path ...]"
---

# Commit

Load `sdlc-project`, then `rules/sdlc/git-commit.md` (GT-01..GT-09). The format and the
switches come from `{{profile.commit}}`; a profile with no `commit:` section uses the defaults
in the template — say so, and suggest `/sdlc-init` to choose the format.

`hooks/guard-sdlc-git.py` checks every `git` command this command runs. A block from it is a
finding to resolve, not an obstacle to route around: never retry with `--no-verify`, a
different staging trick or a reworded message that only satisfies the pattern.

## Step 1 — See what changed

Run `git status --porcelain=v1` and `git diff --stat` / `git diff --cached --stat`. Report:

- the branch — and stop if it is in `{{profile.commit.protected_branches}}` (GT-06);
- what is already staged, what is modified but unstaged, what is untracked;
- an operation in progress (merge, rebase, cherry-pick) — finish or abort it with the user
  first; this command does not commit a half-resolved merge.

Nothing changed → say so and stop.

## Step 2 — Decide what goes into this commit

The scope is, in order: the paths given after `--`; otherwise what is already staged; otherwise
the files the current task changed. Never everything that happens to be modified.

If the candidate files fall into independent groups — two IDs, a feature and an unrelated
config change, a document and a code change that belong to different work — propose one
commit per group (GT-09) and handle them one at a time.

For each candidate path, check before staging:

| Check | Rule | On failure |
|---|---|---|
| matches `{{profile.constraints.readonly_globs}}` and not `{{profile.commit.regenerated_globs}}` | GT-03, BL-07 | drop it from the commit; tell the user what changed it |
| a document in `{{profile.constraints.baselined}}` | GT-04, BL-02 | needs `.claude/.active_cr`; without one, stop and point to `/sdlc-cr-analyze` |
| an env, key or credential file, or a diff line that looks like a secret | GT-05 | drop it, never stage it, tell the user — and to rotate a real secret |
| a template, a client standard, a generated report someone else owns | GT-03 | drop it |
| debug output, `.only`, commented-out code, a stray file | hygiene | point it out; let the user decide |

## Step 3 — Review gate for code

When the commit contains source code, apply `{{profile.commit.review_before_commit}}`:

- `require` — run `/sdlc-review-commit` on the scope; any Critical stops the commit.
- `recommend` — ask whether to run it; a Critical found stops the commit.
- `off` — skip, and say it was skipped.

Documents only: no review gate here — their review is `/sdlc-review-design`.

## Step 4 — Anchor the ID (GT-09)

Take the ID from, in order:

1. the argument the user gave;
2. `.claude/.active_cr`, when it names a CR (not `EDITORIAL`) — it is mandatory when a
   baselined document is in the commit (GT-04);
3. the IDs the diff itself touches: the deliverable's own document id, the `REQ-*` / `NFR-*` /
   `BUG-*` / `INC-*` / `DEC-*` rows added or changed, the traceability register rows, the module
   whose code changed;
4. the branch name (`feature/REQ-012-…`, `fix/BUG-031`).

Every ID must exist — in the register, a deliverable, the decision log, the defect list or the
active CR — and match `{{profile.commit.id_pattern}}` (or the default: upper case with a digit).
Several IDs are joined with `{{profile.commit.id_separator}}`. When nothing gives an ID, ask the
user; offer `{{profile.commit.no_id}}` only when the project defined it. Never invent one.

## Step 5 — Choose the action and write the summary

The action is one word from `{{profile.commit.actions}}`, chosen by what the change *does*
(the table in GT-01): a new deliverable or module is `ADD`, a corrected defect is `FIX`, a
review report is `REVIEW`, a gate decision or baseline is `CONFIRM`. Mixed changes take the
action of the main intent — or are two commits.

The summary says what this commit does, imperative, at most `{{profile.commit.summary_max}}`
characters, in `{{profile.commit.summary_language}}`. Not "update files", not the file names.

Compose the subject with `{{profile.commit.format}}`. A body is added when
`{{profile.commit.body}}` is `required`, and whenever the why is not obvious from the subject:
the reason, the anchors, the reverted commit. Check the subject against the format yourself
before showing it.

## Step 6 — Confirm

Show, and wait for the user's answer:

```
Commit preview
  Branch   : {branch}
  Files    : {n}
    {status} {path}
  Excluded : {path} — {reason}          (read-only / baselined / secret / other group)
  Review   : {PASS | skipped | not code}
  Message  :
    {subject}

    {body}
```

The user may edit the message or the file list; re-run Steps 2–5 on a changed list.

## Step 7 — Stage and commit

```
git add -- <path> <path> ...
git commit -F <message file>
```

Stage the listed paths by name (GT-02). Write the message to a temporary file outside the
working tree and commit with `-F` — it survives quotes, non-ASCII text and several lines, which
`-m` in a shell does not reliably; never open an editor. If a repository
pre-commit hook fails, report its output and fix the cause; do not bypass it (GT-06).

Then delete the message file and run `git log -1 --stat` to confirm.

## Step 8 — Report

```
Committed {short hash} on {branch}
  {subject}
  {n} files   +{added} / -{removed}
  Traceability : {the register rows to update with this hash, or "none"}
  Not committed: {paths left modified, and why}
  Push         : not done — `git push {remote} {branch}` when you are ready
```

Push only when `{{profile.commit.allow_push}}` is true *and* the user asked for it (GT-08).
Where the register records code references by commit, say which rows should now carry the hash.
