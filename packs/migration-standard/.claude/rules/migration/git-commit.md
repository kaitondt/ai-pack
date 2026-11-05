# RULE FAMILY: GIT COMMIT

A commit is the smallest record the project keeps of *why* something changed. The legacy
catalogue says what the old system does, the design says what the new one will do, the
traceability register says where it went — and the commit history is the only place that says
which change carried which ID, in what order. `/mig-trace-bug` and the release notes read it
back; a commit that cannot be read back is a gap in the chain.

The message format is chosen once, at `/mig-init`, and lives in `{{profile.commit}}`.
`/mig-commit` is the way to commit; `hooks/guard-mig-git.py` is the backstop that blocks
GT-01..GT-08 mechanically on every `git` command the AI runs.

## GT-01 — Every commit message follows the agreed format

The subject line matches `{{profile.commit.format}}` exactly. The default is
`{ID} {ACTION} {SUMMARY}`:

| Token | What it is | Example |
|---|---|---|
| `{ID}` | the id of what the change is about — legacy item, requirement, module, design document, test, UAT bug, CR, decision (`LEG-*`, `REQ-*`, a module id, a document id, `UT-*`, `UAT-*`, `CR-*`, `DEC-*`). Several: joined by `{{profile.commit.id_separator}}` | `REQ-ORD-012`, `CR-007,XX0000PG-SC-001` |
| `{ACTION}` | one word from `{{profile.commit.actions}}` | `UPDATE` |
| `{SUMMARY}` | what this commit does, imperative, at most `{{profile.commit.summary_max}}` characters, in `{{profile.commit.summary_language}}` | `carry the legacy rounding rule into the order total` |

`XX0000PG-FC-001 UPDATE carry the legacy rounding rule into the order total`

The default action vocabulary, and when each applies:

| Action | Use it when the commit… |
|---|---|
| `ADD` | creates something that did not exist — a catalogue entry, a deliverable, a module, a test |
| `UPDATE` | changes something that exists, without it being a defect fix |
| `DELETE` | removes something |
| `FIX` | corrects a defect (a UAT bug, a failed case) or a review finding |
| `REVIEW` | records a review — the report, the findings, the review record |
| `CONFIRM` | records an approval — a gate decision, an answered question, an accepted GAP, a UAT sign-off |
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

## GT-03 — A commit never changes the legacy source or a read-only path

Paths in `{{profile.constraints.readonly_globs}}` — the legacy source above all (LR-01) — are
never changed by a commit, however the change got onto disk: not modified, not deleted, not
renamed, and nothing added into them. Analysis output lives under the docs paths (LR-05). The
exception is `{{profile.commit.regenerated_globs}}`: generated files are committed *as
regenerated* from their generator input, never hand-edited (LR-04).

## GT-04 — A change-request commit carries the client's CR id

A commit made for a change request carries its CR id in `{{profile.change_request.id_format}}`,
taken from the client's CR list (`{{profile.change_request.id_source}}`) — never generated. The
design documents are committed before the code that implements them, in the cascade order
(`CR-007 UPDATE …` for the documents at GATE 2, then the implementation).

The CR in progress is recorded in `.claude/.active_cr` — written by `/mig-cr-design`, cleared
by `/mig-cr-report`. While it names a CR, every commit touching
`{{profile.change_request.governed_paths}}` carries that id; while it says `PENDING`, nothing
under those paths is committed until the client's id replaces it. The hook enforces both. Code
commits for the CR carry the id as well — the hook cannot tell them from other code, so
`/mig-commit` and the review do.

## GT-05 — No secret, env file or key file is ever staged

`.env` and its variants (`.env.example` excepted), private keys, keystores and credential
files never enter git, nor does a line that looks like a credential — including a connection
string copied out of the legacy configuration. `git add -f` — staging a gitignored file — is
blocked for the same reason. A secret that was committed is compromised even after the commit
is removed: tell the user to rotate it.

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
invented: it comes from the CR in `.claude/.active_cr`, the catalogue entries, deliverables and register
rows the diff touches, the branch name, or the user. When none of these gives one, ask — or use
`{{profile.commit.no_id}}` when the project defined one for housekeeping commits. An ID is a
fact like any other (NI-01): one that exists nowhere breaks every trace that later follows it.

## Self-check before committing

- [ ] The staged list is exactly the files reviewed — named, not swept (GT-02)
- [ ] Nothing under the legacy source or another read-only path; no secret (GT-03, GT-05)
- [ ] The ID exists in the catalogue, the register, the deliverables, the client's CR list or the user's words (GT-04, GT-09)
- [ ] The subject matches `{{profile.commit.format}}` and the action fits the change (GT-01)
- [ ] For code: `/mig-review-commit` has no open Critical (`{{profile.commit.review_before_commit}}`)
- [ ] No `--no-verify`, `--amend`, push or history rewrite (GT-06..GT-08)
