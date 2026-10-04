---
description: "Work the debt ledger — list debts by due stage, sweep the code for unrecorded shortcuts, record a new DEBT-*, or pay one down in a behaviour-preserving slice. Usage: /vibe-debt [list | sweep | add <what> | pay [DEBT-NNN]]"
---

# Debt

Load `vibe-project`, then `vibe-debt-ledger`.

## `list` (default)

From `{{profile.paths.debt}}`: open debts grouped by due stage (overdue first), security
flagged, paydown counter, and what blocks the next graduation (DL-04).

## `sweep`

Run the DT-02 sweep over the codebase. Present candidates with file:line; the human confirms
which become `DEBT-*` (recorded with `Why taken: unknown (found in sweep)`), which are fixed
now as their own slices, which are deleted.

## `add <what>`

Append a row with every DL-02 field — ask for Risk and Due if not obvious; Due is a stage or a
date, never "later". Security → Due ≤ `mvp` (SB-08). Add the code marker (DL-03).

## `pay [DEBT-NNN]`

No id → choose per DT-03 and say why. Then DT-04:

1. Checkpoint; checks for the area green **before** (write them first if none exist).
2. Change structure, not behaviour, within the slice budget.
3. Same checks green **after**.
4. Commit `DEBT-NNN: …`; row → `paid <hash>`; marker removed (the paydown counter now counts from this commit).

## Report

```
Debt — {n} open ({n} security)       paydown counter {n}/{{profile.debt.paydown_every_n_slices}}
  Overdue          : {list or none}
  Due at next stage: {list}
  This run         : {added n | swept: found n, recorded n | paid DEBT-NNN {hash}}
```
