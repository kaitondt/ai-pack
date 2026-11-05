# RULE FAMILY: GIT COMMIT

In a vibe project the commit *is* the checkpoint: intent → slice → commit → check (SC-05). Git
is the undo button, the memory of what was tried, and the only traceability the project has —
so a commit has to say which slice, bug or debt it carries, and it has to be safe to make.

The message format is chosen once, at `/vibe-init`, and lives in `{{profile.commit}}`.
`/vibe-commit` is the way to commit (`/vibe-build` uses the same steps at its commit step);
`hooks/guard-vibe-git.py` is the backstop that blocks GT-01..GT-08 mechanically on every `git`
command the AI runs, next to `guard-vibe-bash.py` (SB-02).

## GT-01 — Every commit message follows the agreed format

The subject line matches `{{profile.commit.format}}` exactly. The default is
`{ID} {ACTION} {SUMMARY}`:

| Token | What it is | Example |
|---|---|---|
| `{ID}` | the slice, bug, debt, decision or idea the commit carries (`INT-{NNN}.{n}`, `BUG-*`, `DEBT-*`, `DEC-*`, `IDEA-*`). Several: joined by `{{profile.commit.id_separator}}` | `INT-003.2`, `BUG-004` |
| `{ACTION}` | one word from `{{profile.commit.actions}}` | `ADD` |
| `{SUMMARY}` | what this commit does, imperative, at most `{{profile.commit.summary_max}}` characters, in `{{profile.commit.summary_language}}` | `edit a note` |

`INT-003.2 ADD edit a note` · `DEBT-002 REFACTOR move notes to Postgres` · `BUG-004 FIX keep the draft on reload`

The default action vocabulary, and when each applies:

| Action | Use it when the commit… |
|---|---|
| `ADD` | adds behaviour, a file or a test that did not exist |
| `UPDATE` | changes behaviour that exists, without it being a bug fix |
| `DELETE` | removes something |
| `FIX` | fixes a `BUG-*` (with its regression check) or a review finding |
| `REVIEW` | records a review in `vibe/reviews/` |
| `CONFIRM` | records a decision or an acceptance — a `DEC-*`, a stage promotion, a release |
| `REFACTOR` | changes structure, not behaviour — a debt paydown usually is one |
| `REVERT` | undoes an earlier commit (name it in the body) |

The project may replace the vocabulary or the format at init; the hook enforces whatever the
profile says. A message that would open an editor is not a message — always pass it with `-m`
or `-F <file>`.

## GT-02 — Stage explicit paths, and only what the slice touched

Stage the files by name: `git add -- <file> <file>`. Never `git add -A`, `git add .`,
`git add -u` or `git commit -a` (when `{{profile.commit.stage_explicit_paths}}` is true). The
slice's diff is what was verified; a sweeping stage adds what was not. `vibe/` bookkeeping
(STATE.md, the intent tick) goes in the same commit as the slice.

## GT-03 — A commit never changes a protected path by hand

Paths in `{{profile.security.protected_paths}}` are never changed by a commit, except those in
`{{profile.commit.regenerated_globs}}` — generated and vendored code committed *as regenerated*
by its tool, never hand-edited.

## GT-04 — A slice is committed when it is verified, not before

The commit closes a slice whose done-when checks were seen running (VT-01). A slice that is not done
is not committed under its ID; an abandoned attempt is committed to an
`{{profile.loop.attempt_branch_prefix}}<slice>-<n>` branch instead of being reset away
(`/vibe-unstuck`). The hook does not check this one; the build loop does.

## GT-05 — No secret, env file or key file is ever staged

Files in `{{profile.security.env_files}}` and other `.env` variants (`.env.example` excepted),
private keys and credential files never enter git, nor does a line that looks like a credential
(SB-01). `git add -f` is blocked for the same reason. A secret that was committed is compromised
even after the commit is removed: tell the user to rotate it.

## GT-06 — The repository's own checks are never bypassed

No `--no-verify`, no `commit -n`, no `core.hooksPath` override. No direct commit to a branch in
`{{profile.commit.protected_branches}}`.

## GT-07 — History is not rewritten or destroyed by the AI

No `--amend` unless `{{profile.commit.allow_amend}}` is true *and* the commit is not yet
pushed. Never force-push, `reset --hard`, `clean -f`, discard the working tree, `branch -D`,
drop stashes or rewrite history (SB-02). To step back from a failed attempt, branch it.

## GT-08 — Pushing is the user's step

`git push` only when `{{profile.commit.allow_push}}` is true, and never with force. Shipping is
`/vibe-ship`'s job.

## GT-09 — One slice per commit, and the ID is real

A commit carries one slice, one bug fix or one debt paydown. The ID comes from the intent file,
`bugs.md`, `debt.md` or `decisions.md` — never made up for the occasion (ID-03 in
`rules/vibe/id-naming.md`: the next number is computed from the file). Housekeeping with no ID uses
`{{profile.commit.no_id}}` when the project defined one; otherwise ask.

## Self-check before committing

- [ ] The slice's done-when checks were observed (GT-04)
- [ ] The staged list is exactly the slice's files plus its `vibe/` bookkeeping (GT-02)
- [ ] No protected path by hand, no secret, no env file (GT-03, GT-05)
- [ ] The subject matches `{{profile.commit.format}}` with a real ID (GT-01, GT-09)
- [ ] No `--no-verify`, `--amend`, push or history rewrite (GT-06..GT-08)
