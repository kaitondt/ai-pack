# Common Performance

## Budget before optimisation

State the target before writing code, as an `NFR-PERF-*`: response time at a named
percentile, batch window, concurrent users, dataset size at go-live and at +3 years.
Without a number, "slow" is unarguable and "fast enough" is unprovable.

A performance NFR that names no data volume is not testable. The volume assumption is
itself an `ASM-*` owned by the business — get it wrong and every measurement afterwards is
measuring the wrong system.

## Design for the volume you will have, not the volume you have

The dominant failure mode in a new system is that it was built and tested against a few
hundred seeded rows and meets production at a few million. Everything below is cheap
before release and expensive after:

- Paginate every list at the server. Client-side paging of a full result set is a defect,
  not a shortcut.
- Sort at the server, explicitly. Never rely on natural or insertion order; it is stable
  right up until the query plan changes.
- Index the columns you filter and sort on, and check the plan — not the line count.
- Avoid N+1 at every boundary: query, HTTP call, and file read.
- Bound every unbounded thing: result sets, uploads, retries, queue depth, log volume.

## Measure honestly

- Measure on the environment the NFR names — `staging` for ST, not a developer laptop.
- Record method, data volume, concurrency and percentile alongside the number
  (`../sdlc/quality-metrics.md` QM-01).
- Compare before and after any optimisation, and keep both numbers in the deliverable.
- A p50 that meets target while p95 fails is a failing system: users experience the tail.

## Batch and scheduled work

- Know the window, and measure against the largest realistic input, not a sample.
- Design restart and rerun semantics explicitly, at design time. Operators will need them
  at 03:00 and the design is the only thing that will answer.
- Commit in bounded chunks; a single transaction over a million rows is an outage waiting
  for a slow disk.
- Log start, end, row counts and outcome per run. Operations validates the system through
  these logs, and P9 investigations start there.

## Caching

Cache only with an explicit invalidation story, written down. State what is cached, for
how long, what invalidates it, and what a user sees during the stale window. A cache added
"for performance" without that paragraph is a correctness bug scheduled for later.

## Front-end

- Ship the smallest thing that renders the first meaningful screen; defer the rest.
- Explicit dimensions on media to avoid layout shift.
- Animate compositor-friendly properties only.
- Debounce user-driven queries, and cancel superseded ones — the last response to arrive
  is not necessarily the one the user asked for.
