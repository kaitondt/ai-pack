---
description: "Commit the current work in the format agreed at /mig-init ({ID} {ACTION} {SUMMARY} by default): check the changes against the legacy read-only and secret rules, stage explicit paths, anchor the ID, compose the message, confirm, commit. Never pushes. Usage: /mig-commit [ID] [ACTION] [summary] [-- path ...]"
---

# Commit

Load `mig-project`, then `rules/migration/git-commit.md` (GT-01..GT-09). The format and the
switches come from `{{profile.commit}}`; a profile with no `commit:` section uses the defaults
in the template — say so, and suggest `/mig-init` to choose the format.

`hooks/guard-mig-git.py` checks every `git` command this command runs. A block from it is a
finding to resolve, not an obstacle to route around: never retry with `--no-verify`, a
different staging trick or a reworded message that only satisfies the pattern.

## Step 1 — See what changed

Run `git status --porcelain=v1` and `git diff --stat` / `git diff --cached --stat`. Report:

- the branch — and stop if it is in `{{profile.commit.protected_branches}}` (GT-06);
- what is already staged, what is modified but unstaged, what is untracked;
- any change at all under the legacy source (`{{profile.legacy.root}}` and
  `{{profile.constraints.readonly_globs}}`) — that is an LR-01 incident, reported first,
  whatever else is committed;
- an operation in progress (merge, rebase, cherry-pick) — finish or abort it with the user
  first;
- the change request in `.claude/.active_cr`, if any (`PENDING` included).

Nothing changed → say so and stop.

## Step 2 — Decide what goes into this commit

The scope is, in order: the paths given after `--`; otherwise what is already staged; otherwise
the files the current task changed. Never everything that happens to be modified.

If the candidate files fall into independent groups — two modules, a design update and its
implementation that belong to different CR gates, an unrelated config change — propose one
commit per group (GT-09) and handle them one at a time. For a change request, the documents
approved at GATE 2 are committed before the code that implements them (GT-04).

For each candidate path, check before staging:

| Check | Rule | On failure |
|---|---|---|
| under the legacy source, or matches `{{profile.constraints.readonly_globs}}` and not `{{profile.commit.regenerated_globs}}` | GT-03, LR-01, LR-04 | drop it; tell the user what changed it, and how to restore it |
| an env, key or credential file, or a diff line that looks like a secret — including a connection string from the legacy config | GT-05 | drop it, never stage it, tell the user — and to rotate a real secret |
| under `{{profile.change_request.governed_paths}}` while `.claude/.active_cr` names a CR | GT-04 | the commit carries that CR id — or, if the change is unrelated, it waits until the CR closes |
| under the governed paths while `.claude/.active_cr` is `PENDING` | GT-04 | stop: get the client's CR id and write it to the marker first |
| a client template or coding-standard source | GT-03 | drop it |
| debug output, `.only`, commented-out code, a stray file | hygiene | point it out; let the user decide |

## Step 3 — Review gate for code

When the commit contains source code, apply `{{profile.commit.review_before_commit}}`:

- `require` — run `/mig-review-commit` on the scope; any Critical stops the commit.
- `recommend` — ask whether to run it; a Critical found stops the commit.
- `off` — skip, and say it was skipped.

Documents only: no review gate here — their review is `/mig-review-design`.

## Step 4 — Anchor the ID (GT-09)

Take the ID from, in order:

1. the argument the user gave;
2. `.claude/.active_cr`, when it names a CR — mandatory for documents under
   `{{profile.change_request.governed_paths}}` and for the CR's code (GT-04). The id is the
   client's (`{{profile.change_request.id_source}}`), never generated;
3. the IDs the diff itself touches: the document id of the deliverable, the module whose code
   changed, the `LEG-*` / `REQ-*` / `UT-*` / `IT-*` / `UAT-*` / `DEC-*` rows added or changed,
   the traceability register rows;
4. the branch name (`feature/XX0000PG`, `fix/UAT-014`).

Every ID must exist — in the legacy catalogue, the register, a deliverable, the decision log,
the UAT bug list or the client's CR list — and match `{{profile.commit.id_pattern}}` (or the
default: upper case with a digit). Several IDs are joined with
`{{profile.commit.id_separator}}`. When nothing gives an ID, ask the user; offer
`{{profile.commit.no_id}}` only when the project defined it. Never invent one.

## Step 5 — Choose the action and write the summary

The action is one word from `{{profile.commit.actions}}`, chosen by what the change *does*
(the table in GT-01): a new catalogue entry or module is `ADD`, a UAT bug corrected is `FIX`, a
review report is `REVIEW`, a gate decision or an accepted GAP is `CONFIRM`. Mixed changes take
the action of the main intent — or are two commits.

The summary says what this commit does, imperative, at most `{{profile.commit.summary_max}}`
characters, in `{{profile.commit.summary_language}}`. Not "update files", not the file names,
and no legacy identifiers the target deliverables avoid (NI-06) unless the commit is analysis.

Compose the subject with `{{profile.commit.format}}`. A body is added when
`{{profile.commit.body}}` is `required`, and whenever the why is not obvious from the subject:
the legacy anchor, the CR gate, the reverted commit. Check the subject against the format
yourself before showing it.

## Step 6 — Confirm

Show, and wait for the user's answer:

```
Commit preview
  Branch   : {branch}
  Files    : {n}
    {status} {path}
  Excluded : {path} — {reason}          (legacy / read-only / secret / other group)
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
`-m` in a shell does not reliably; never open an editor. If a repository pre-commit hook fails,
report its output and fix the cause; do not bypass it (GT-06).

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
