# Common Performance

## Budget before optimisation

State the target before writing code: response time at a named percentile, batch window,
concurrent users, dataset size at go-live and at +3 years. Without a number, "slow" is
unarguable.

## The migration-specific risk

Legacy systems were tuned against a data volume and an access pattern that the target
inherits. Two failure modes dominate:

1. **The set-based rewrite that lost its index.** A cursor loop that was fine over an
   indexed key becomes a table scan when rewritten as a join. Check the plan, not the
   line count.
2. **The chatty client.** A desktop app doing 200 round trips to a LAN database is
   imperceptible; the same 200 round trips over HTTP is not. Batch at the API boundary.

## Rules

- Measure before and after; keep the numbers in the deliverable.
- Paginate every list at the server. Client-side paging of a full result set is a defect,
  not a shortcut.
- Sort at the server, and sort explicitly — never rely on natural order. Legacy row order
  is frequently an unstated requirement.
- Index reads, batch writes, and keep transactions short.
- Avoid N+1 at every boundary: query, HTTP, and file.
- Cache only with an explicit invalidation story. In a migration, stale data is
  indistinguishable from a parity defect.

## Batch jobs

- Know the window, and measure against the largest realistic input, not a sample.
- Design restart and rerun semantics explicitly — legacy operators depend on them and they
  are rarely documented.
- Log start, end, row counts and outcome per run; the operations team validates the
  migration through these logs.

## Front-end

- Ship the smallest thing that renders the first meaningful screen; defer the rest.
- Explicit dimensions on media to avoid layout shift.
- Animate compositor-friendly properties only.
