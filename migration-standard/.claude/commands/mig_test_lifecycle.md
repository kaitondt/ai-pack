---
description: "Maintain test artifacts between execution rounds: version history between revisions, carrying results forward by TC ID, condensing flow-organised files into one execution table, checkpoint counting, evidence naming. Usage: /mig_test_lifecycle <history|carry|condense|count|evidence> <target>"
---

# Test artifact lifecycle

## Step 1 — Load

`mig_project`, then `mig_test_lifecycle`.

## Step 2 — Resolve the operation

| Operation | Does |
|---|---|
| `history` | diff two revisions by TC ID, propose the revision row in a separate file |
| `carry` | move results from an old revision to a new one, by TC ID |
| `condense` | flatten a flow-organised document into one execution table with result columns |
| `count` | count checkpoints in expected results, stating the counting rule |
| `evidence` | verify evidence file names against the current revision |

## Step 3 — Run it, under the standing constraints

**The old file is never modified.** It is the evidence for its round.

**Results move only on unchanged content.** A TC ID present in both revisions but whose
steps or expectations changed was not executed in its current form — leave it empty and
mark it for re-execution. Copying a result across a content change fabricates evidence,
which is the one genuinely dangerous failure in this whole command.

**Ask before writing on partial matches.** Do not pick a rule for ambiguous cases.

**Condensing changes shape, never content.** The TC ID set before and after must be
identical.

**Version bumps are never automatic** (DS-02). `history` proposes the row; a human applies
it.

## Step 4 — Report

```
Lifecycle — {module} · {operation}
  {old} → {new}
  Added {n} · Removed {n} · Changed {n} · Unchanged {n}
  Results carried {n} · withheld {n} · empty {n}
  Checkpoints {n}  (rule: {rule})
  Evidence {n} files · {n} unmatched · {n} cases missing
  Old file modified : no
```

Removed cases are listed explicitly with their IDs. A case that disappears between
revisions without a reason is either a coverage regression or an unrecorded scope
decision, and both need to be visible.
