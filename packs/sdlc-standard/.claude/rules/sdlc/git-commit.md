# RULE FAMILY: GIT COMMIT

A commit is the smallest record the project keeps of *why* something changed. The design says
what was agreed, the traceability register says where it went — and the commit history is the
only place that says which change carried which ID, in what order. `/sdlc-trace-bug` and the
release notes read it back; a commit that cannot be read back is a gap in the chain.

The message format is chosen once, at `/sdlc-init`, and lives in `{{profile.commit}}`.
`/sdlc-commit` is the way to commit; `hooks/guard-sdlc-git.py` is the backstop that blocks
GT-01..GT-08 mechanically on every `git` command the AI runs.

## GT-01 — Every commit message follows the agreed format

The subject line matches `{{profile.commit.format}}` exactly. The default is
`{ID} {ACTION} {SUMMARY}`:

| Token | What it is | Example |
|---|---|---|
| `{ID}` | the id of what the change is about — requirement, design, module, test, bug, CR, decision, incident (`REQ-*`, `NFR-*`, a document id, `BUG-*`, `CR-*`, `DEC-*`, `INC-*`). Several: joined by `{{profile.commit.id_separator}}` | `REQ-012`, `CR-007,REQ-012` |
| `{ACTION}` | one word from `{{profile.commit.actions}}` | `UPDATE` |
| `{SUMMARY}` | what this commit does, imperative, at most `{{profile.commit.summary_max}}` characters, in `{{profile.commit.summary_language}}` | `clarify the lockout threshold` |

`REQ-012 UPDATE clarify the lockout threshold`

The default action vocabulary, and when each applies:

| Action | Use it when the commit… |
|---|---|
| `ADD` | creates something that did not exist — a deliverable, a section, a module, a test |
| `UPDATE` | changes something that exists, without it being a defect fix |
| `DELETE` | removes something |
| `FIX` | corrects a defect (`BUG-*`, `INC-*`) or a review finding |
| `REVIEW` | records a review — the report, the findings, the review record |
| `CONFIRM` | records an approval — a gate decision, a baseline, an answered question, an acceptance |
| `REFACTOR` | changes structure without changing behaviour or meaning |
| `REVERT` | undoes an earlier commit (name it in the body) |

The project may replace the vocabulary or the format at init; the hook enforces whatever the
profile says. A message that would open an editor is not a message — always pass it with `-m`
or `-F <file>`.

## GT-02 — Stage explicit paths, and only what was reviewed

Stage the files by name: `git add -- <file> <file>`. Never `git add -A`, `git add .`,
`git add -u` or `git commit -a` (when `{{profile.commit.stage_explicit_paths}}` is true). A
sweeping stage is how an unrelated half-finished file, a local config or a secret ends up in a
commit no one reviewed. Show the user the staged list before committing.

## GT-03 — A commit never changes a read-only path

Paths in `{{profile.constraints.readonly_globs}}` — generated files, baseline snapshots, the
client's templates and standards — are never changed by a commit, however the change got onto
disk (an editor, a script, a formatter). The exception is `{{profile.commit.regenerated_globs}}`:
files a generator rewrites are committed *as regenerated*, never hand-edited (BL-07). A new
snapshot under `_baselined/` is an addition, not a change, and is allowed.

## GT-04 — A commit to a baselined document carries its change request

A commit that changes a document in `{{profile.constraints.baselined}}` is allowed only while
a CR is active (`.claude/.active_cr`, written by `/sdlc-cr-design`), and its message carries
that CR id — `CR-007,REQ-012 UPDATE …`. An `EDITORIAL` marker (BL-02 exception) needs no CR id,
only the user's confirmation and a revision-history row.

## GT-05 — No secret, env file or key file is ever staged

`.env` and its variants (`.env.example` excepted), private keys, keystores and credential
files never enter git, nor does a line that looks like a credential. `git add -f` — staging a
gitignored file — is blocked for the same reason. A secret that was committed is compromised
even after the commit is removed: tell the user to rotate it.

## GT-06 — The repository's own checks are never bypassed

No `--no-verify`, no `commit -n`, no `core.hooksPath` override. A pre-commit hook that fails is
reporting something; fix that. No direct commit to a branch in
`{{profile.commit.protected_branches}}` — work on a branch and merge through review.

## GT-07 — History is not rewritten or destroyed by the AI

No `--amend` unless `{{profile.commit.allow_amend}}` is true *and* the commit is not yet
pushed. Never force-push, delete a remote branch, `reset --hard`, `clean -f`, discard the whole
working tree, `branch -D`, drop stashes, or rewrite history (`filter-branch`, `filter-repo`).
These are the user's to run: show the exact command and what it destroys.

## GT-08 — Pushing is the user's step

`git push` only when `{{profile.commit.allow_push}}` is true, and never with force. Otherwise
report the commits made and the push command, and stop.

## GT-09 — One logical change per commit, and the ID is real

A commit implements one ID, or one change that spans a stated set of IDs. Unrelated changes are
split into separate commits rather than joined under the first ID that fits. The ID is never
invented: it comes from the active CR, the deliverables and register rows the diff touches, the
branch name, or the user. When none of these gives one, ask — or use `{{profile.commit.no_id}}`
when the project defined one for housekeeping commits. A plausible-looking ID that exists
nowhere breaks every trace that later follows it (RS-01).

## Self-check before committing

- [ ] The staged list is exactly the files reviewed — named, not swept (GT-02)
- [ ] No read-only path, no baselined document without its CR, no secret (GT-03..GT-05)
- [ ] The ID exists in the register, the deliverables, the active CR or the user's words (GT-09)
- [ ] The subject matches `{{profile.commit.format}}` and the action fits the change (GT-01)
- [ ] For code: `/sdlc-review-commit` has no open Critical (`{{profile.commit.review_before_commit}}`)
- [ ] No `--no-verify`, `--amend`, push or history rewrite (GT-06..GT-08)
