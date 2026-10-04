---
name: vibe-debt-ledger
description: "Manage the debt ledger — record shortcuts as DEBT-* with a due stage, find unrecorded ones, choose what to pay next, and run behaviour-preserving paydown/refactor slices. Use for 'tech debt', 'clean this up', 'refactor', 'what should we fix before launch', TODO/FIXME cleanup, and when the paydown counter is due."
---

# Debt — Shortcuts With a Due Date

> The rules are in `rules/vibe/debt-ledger.md`. This skill is the ledger's format, how to
> find what nobody wrote down, and how to pay it without breaking anything.

Load `vibe-project`.

---

## DT-01 — The ledger

`{{profile.paths.debt}}`, one table, append-only (SC-03):

```markdown
| ID | What | Where | Why taken | Risk | Cat. | Due | Size | Status |
|---|---|---|---|---|---|---|---|---|
| DEBT-014 | notes stored in a JSON file | src/lib/store.ts | ship INT-003 demo | data loss on redeploy; no concurrency | data | mvp | M | open |
| DEBT-015 | no rate limit on /api/login | src/app/api/login | INT-001 speed | credential stuffing | security | mvp | S | open |
| DEBT-009 | copy-pasted form validation ×3 | notes, tags, profile forms | INT-004..006 | fixes applied to one copy only | maintainability | production | S | paid a4f9e21 |
```

## DT-02 — Finding unrecorded debt

A ledger on a vibe project is always incomplete (DL-06). Sweep:

- `TODO|FIXME|HACK|XXX` without a `DEBT-` id
- hardcoded URLs, ids, emails, prices, feature flags
- `any` / `# type: ignore` / lint-disable comments
- `catch {}` / `except: pass` / `.catch(() => {})`
- copies: the same 10+ lines in more than one place
- storage stand-ins: JSON files, in-memory maps, localStorage for server data
- endpoints with no validation or ownership check (→ security, SB-08)
- core flows with no automated check (→ due `mvp`)
- UI with no loading / empty / error state

Record each as found, with `Why taken: unknown (found DT-02 sweep)`.

## DT-03 — Choosing what to pay

Order by:

1. **Overdue** — due stage ≤ current stage (should not exist; DL-04)
2. **Security** — due `mvp` or earlier (SB-08)
3. **Blocking the next graduation** — due = next stage
4. **Risk × probability** — data loss and wrong results before maintainability
5. **Hotspots** — debt in files that change often costs interest every slice
6. **Cheap** — S-sized debt in a file you are about to touch anyway (as its own slice)

## DT-04 — The paydown slice

A paydown is a refactor slice (SS-07): **behaviour does not change**.

1. Checkpoint. Run the checks for the affected area — they must be green **before**. If there
   are no checks covering the area, writing them is the first part of the paydown.
2. Make the change, within the slice budget. Big debt → several slices, each leaving the app
   working.
3. Same checks green **after**. Any behaviour change that crept in → revert that part.
4. Commit `DEBT-014: move notes to Postgres`; mark the row `paid <hash>`; remove the code marker.
5. The paydown counter (DL-05) resets by itself: it counts from this `DEBT-*` commit.

## DT-05 — Accepting debt

Some debt is never worth paying (the admin page used twice a year). Accept it explicitly:
status `accepted`, citing a `DEC-*` with the reason and who accepted. Security debt cannot be
accepted past `mvp` (SB-08).

## Self-check

- [ ] Every row has all DL-02 fields; Due is a stage or date, not "later"
- [ ] Sweep done before graduation; found debts recorded as found
- [ ] Paydown slices changed no behaviour; checks green before and after
- [ ] Paid rows cite the commit; accepted rows cite the decision
