# RULE FAMILY: GIT COMMIT

When the management documents live in git, the commit history is the project's audit trail:
which version of the schedule was in force on which date, who changed the cost baseline, under
which change request. An auditor reads it back; a commit that cannot be read back is a gap in
the record (MD-04).

The message format is chosen once, at `/pm-init`, and lives in `{{profile.commit}}`.
`/pm-commit` is the way to commit; `hooks/guard-pm-git.py` is the backstop that blocks
GT-01..GT-08 mechanically on every `git` command the AI runs.

## GT-01 — Every commit message follows the agreed format

The subject line matches `{{profile.commit.format}}` exactly. The default is
`{ID} {ACTION} {SUMMARY}`:

| Token | What it is | Example |
|---|---|---|
| `{ID}` | the id of what the change is about — change request, risk, issue, decision, action, CAPA, meeting, lesson (`CR-*`, `RSK-*`, `ISS-*`, `DEC-*`, `ACT-*`, `CAPA-*`, `MTG-*`, `LL-*`), or a document id. Several: joined by `{{profile.commit.id_separator}}` | `RSK-014`, `CR-007,DEC-021` |
| `{ACTION}` | one word from `{{profile.commit.actions}}` | `UPDATE` |
| `{SUMMARY}` | what this commit does, imperative, at most `{{profile.commit.summary_max}}` characters, in `{{profile.commit.summary_language}}` | `raise the exposure after the vendor slip` |

`RSK-014 UPDATE raise the exposure after the vendor slip`

The default action vocabulary, and when each applies:

| Action | Use it when the commit… |
|---|---|
| `ADD` | creates something that did not exist — a plan, a register entry, a report |
| `UPDATE` | changes something that exists — a status, a forecast, a register row |
| `DELETE` | removes something (a register entry is usually closed, not deleted) |
| `FIX` | corrects an error in a record — a wrong figure, a broken reference |
| `REVIEW` | records a review — a gate review, an audit, an estimate review |
| `CONFIRM` | records an approval — a baseline, a CCB decision, an acceptance, a signed-off report |
| `REFACTOR` | restructures a document without changing a commitment |
| `REVERT` | undoes an earlier commit (name it in the body) |

The project may replace the vocabulary or the format at init; the hook enforces whatever the
profile says. A message that would open an editor is not a message — always pass it with `-m`
or `-F <file>`.

## GT-02 — Stage explicit paths, and only what was reviewed

Stage the files by name: `git add -- <file> <file>`. Never `git add -A`, `git add .`,
`git add -u` or `git commit -a` (when `{{profile.commit.stage_explicit_paths}}` is true). A
sweeping stage is how a draft report or a working file (MD-10) ends up looking issued. Show the
user the staged list before committing.

## GT-03 — A commit never changes an archived or snapshot baseline

Paths in `{{profile.baselines.readonly_globs}}` — archived snapshots, `_baselined/` copies —
are never modified, deleted or renamed by a commit, however the change got onto disk. Adding a
new snapshot or archive is allowed: it alters nothing that was approved (PB-03, PB-06).

## GT-04 — A commit to a baselined document carries its change request

A commit that changes a document in `{{profile.baselines.registered}}` is allowed only while a
CR is active (`.claude/.active_pm_cr`, written by `/pm-change-apply`), and its message carries
that CR id — `CR-007 UPDATE re-baseline the schedule after the CCB decision`. An `EDITORIAL`
marker needs no CR id, only the user's confirmation and a revision-history row — and is never
used for a number, a date, a scope item or an acceptance criterion.

## GT-05 — No secret, env file or key file is ever staged

`.env` and its variants (`.env.example` excepted), private keys and credential files never
enter git, nor does a line that looks like a credential — a tracker API token copied into a
status-collection note included. `git add -f` — staging a gitignored file — is blocked for the
same reason. Personal data beyond what the deliverable needs (rates, appraisals) does not go
into a shared repository either.

## GT-06 — The repository's own checks are never bypassed

No `--no-verify`, no `commit -n`, no `core.hooksPath` override. No direct commit to a branch in
`{{profile.commit.protected_branches}}`.

## GT-07 — History is not rewritten or destroyed by the AI

No `--amend` unless `{{profile.commit.allow_amend}}` is true *and* the commit is not yet
pushed. Never force-push, delete a remote branch, `reset --hard`, `clean -f`, discard the whole
working tree, `branch -D`, drop stashes, or rewrite history. An audit trail that can be
rewritten is not one.

## GT-08 — Pushing is the user's step

`git push` only when `{{profile.commit.allow_push}}` is true, and never with force. Otherwise
report the commits made and the push command, and stop.

## GT-09 — One logical change per commit, and the ID is real

A commit records one change — one CR applied, one report issued, one register update — under
the IDs it concerns. Unrelated changes are split. The ID is never invented: it comes from the
active CR, the register rows and documents the diff touches, the branch name, or the user. When
none of these gives one, ask — or use `{{profile.commit.no_id}}` when the project defined one for
housekeeping commits.

## Self-check before committing

- [ ] The staged list is exactly the files reviewed — named, not swept (GT-02)
- [ ] No archived snapshot changed; no baselined document without its CR; no secret (GT-03..GT-05)
- [ ] The ID exists in a register, a document, the active CR or the user's words (GT-09)
- [ ] The subject matches `{{profile.commit.format}}` and the action fits the change (GT-01)
- [ ] No `--no-verify`, `--amend`, push or history rewrite (GT-06..GT-08)
