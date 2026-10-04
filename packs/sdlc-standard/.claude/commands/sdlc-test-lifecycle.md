---
description: "Maintain test artifacts between execution rounds: version history between revisions, carrying results forward by TC ID, condensing for execution, checkpoint counting, evidence naming, and closing a round. Usage: /sdlc-test-lifecycle <history|carry|condense|count|evidence|close> <target>"
---

# Test lifecycle operations

## Step 1 — Load

`sdlc-project`, then `sdlc-test-artifact-lifecycle`.

## Step 2 — Choose the operation

| Operation | Does |
|---|---|
| `history` | diff two revisions by TC ID and propose the revision row |
| `carry` | move results forward from the previous revision, by TC ID only |
| `condense` | turn a per-flow design document into one execution table |
| `count` | count checkpoints (numbered assertions), stating the counting rule |
| `evidence` | check evidence files against the current revision |
| `close` | close a round: verdicts complete, defects linked, metrics recorded |

## Step 3 — Run it, with the rules that make it safe

**`history`** — compare by TC ID into Added / Removed / Changed / Unchanged. Also compare
what sits outside the case tables: shared preconditions, flow names, environment notes. A
changed shared precondition affects every case under it and the per-case diff will not show
it. Write to a separate file; never edit the revision table from memory (DS-02).

**`carry`** — results move by TC ID **only**, and only where the content is unchanged. A
changed case was not executed in its current form; leave it empty and mark it for
re-execution. Ask before writing when there are partial matches.

> This is the one operation here that can fabricate evidence. A stale pass carried onto a
> changed case is invisible afterwards and will be quoted at a gate.

**`condense`** — shape change, never content change. The TC ID set before and after must be
identical.

**`count`** — state the counting rule with the number. A count without its rule is not
comparable to the next one, and these counts feed test density (QM-05).

**`evidence`** — check against the **current** revision: every file maps to a real TC ID,
every case requiring evidence has it, sequences are contiguous. Rename rather than delete.

**`close`** — every case has a verdict (`Pass` / `Fail` / `Blocked` / `N/A` with a reason),
every failure has a defect id, the build the round ran against is recorded, and the round's
metrics are captured.

## Step 4 — Report

```
Lifecycle — {target}, {operation}
  Old → new       : {file} → {file}
  Added {n} · Removed {n} · Changed {n} · Unchanged {n}
  Results carried : {n}   withheld (content changed) {n}   empty {n}
  Build           : round {n} ran against {build id}
  Checkpoints     : {n}   (rule: {counting rule})
  Evidence        : {n} files, {n} unmatched, {n} cases missing evidence
  Old file modified : no
```

The last line is a check, not a formality. The previous revision is the evidence for the
round it belongs to and is never edited.
