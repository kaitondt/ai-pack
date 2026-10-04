# RULE FAMILY: DEBT LEDGER

> Taking shortcuts is the point of vibe coding. Forgetting them is the failure. A shortcut
> that is written down is a debt with a known cost; one that is not is a defect waiting for
> the worst possible moment to be found.
>
> Derived from `pm-standard`'s risk register (owner, trigger, response) and its rule that
> uncertainty is held visibly rather than hidden — applied to code.

## DL-01 — A shortcut is a debt only if it is written down

Every deliberate shortcut becomes a `DEBT-*` row in `{{profile.paths.debt}}` **in the same
slice that takes it**. Typical ones:

- hardcoded values that should be configuration
- no error handling / no loading state / no empty state on a path
- no tests on a flow, or tests only on the happy path
- a copied-and-adjusted block instead of a shared function
- in-memory or file storage standing in for a database
- a security control skipped (SB-08 — short fuse)
- a library chosen for speed that will not scale / is abandoned
- a known bug accepted for now

## DL-02 — Every debt has the same fields

| Field | Rule |
|---|---|
| ID | `DEBT-{NNN}`, never reused |
| What | the shortcut, in one sentence |
| Where | file(s) and the code marker (DL-03) |
| Why | what it bought — usually time on a named slice |
| Risk | what goes wrong if it is not paid, and when that would show |
| Category | `security` · `data` · `reliability` · `maintainability` · `performance` · `ux` |
| Due | a **stage** (`mvp`, `production`) or a date — never "later" |
| Size | S (< 1 h) · M (< 1 day) · L (more) |
| Status | open · paid (cite the commit) · accepted (cite the `DEC-*`) |

## DL-03 — Code markers link to the ledger

The code at the shortcut carries a marker with the ID:

```ts
// DEBT-014: notes stored in a JSON file; move to Postgres before mvp
```

- A `TODO` / `FIXME` / `HACK` **without** a `DEBT-*` id is flagged by `/vibe-review`. Either it
  becomes a debt, or it is fixed, or it is deleted.
- Never close a debt by deleting its marker. Closing cites the commit that paid it.

## DL-04 — Graduation is blocked by debts due

`/vibe-graduate <stage>` fails while any open debt has `due` at or before `<stage>`. The
options are: pay it, or re-date it with a `DEC-*` that states why the risk is acceptable and who
accepted it. Security debts cannot be re-dated past `mvp` (SB-08).

## DL-05 — Debt is paid continuously, not in a heroic sprint

`{{profile.debt.paydown_every_n_slices}}` (default 5): after that many feature slices, the next
slice is a debt paydown, chosen by risk × due-soonest.

The counter is not stored anywhere — it is computed from git: the number of `INT-*` commits
since the most recent `DEBT-*` commit (SC-05 makes this one `git log` away). `/vibe-status`
and `/vibe-build` show it.

A debt paydown is a refactor slice (SS-07): behaviour does not change, checks green before
and after.

## DL-06 — The ledger is honest

- A debt is never downgraded in risk or pushed back in due date to make a graduation pass —
  only re-dated through a `DEC-*` (DL-04).
- A debt discovered that someone took earlier is recorded as found, not as new; it is
  information about where shortcuts go unrecorded.
- A ledger with zero open debts on a vibe-coded project is not clean; it is incomplete.
  `/vibe-review` looks for unrecorded ones.

## Self-check before committing a slice

- [ ] Every shortcut taken in this slice has a `DEBT-*` row and a code marker
- [ ] Every security shortcut has `category: security` and `due: mvp` or earlier
- [ ] No bare TODO / FIXME left in the diff
- [ ] If the paydown counter is due, the next slice is a paydown
