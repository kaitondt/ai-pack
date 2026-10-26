---
paths:
  - "**/*.sql"
  - "**/*Mapper.xml"
  - "**/mapper/**"
  - "**/migration/**"
  - "**/migrations/**"
  - "**/db/changelog/**"
  - "**/*Repository.*"
  - "**/*.prisma"
---
# RULE FAMILY: SQL, QUERIES AND SCHEMA MIGRATIONS

Stack rules for code that talks to a relational database — hand-written SQL, mapper XML,
repository methods and migration scripts — on any engine. They extend
`rules/common/security.md` and `rules/common/performance.md`. The data design is the
authority on every name, type, precision and index; these rules govern how code uses it.

**Order of authority.** A client coding standard registered in
`{{profile.system.coding_standards}}` outranks this file. The engine named in
`{{profile.system.stack.database}}` decides dialect questions; never write SQL that only
works on the engine the tests happen to use.

## SQ-01 — Parameters, always

Every value reaches the database as a bound parameter. String concatenation or
interpolation of a value into SQL is a Critical finding regardless of where the value came
from — "it is an internal id" is how the second injection happens.

The only legitimate dynamic SQL is an identifier (a sort column, a table suffix) chosen from
a closed whitelist in code. Say so in a comment at the point of use.

## SQ-02 — Names and types come from the data design

- Table and column names exactly as the data design writes them. No alias that renames a
  column into a different concept.
- Column types, precision, scale and nullability as designed. A query that casts a
  `numeric(12,2)` to a float to compare it has changed the rounding.
- Soft-delete, tenant and validity-period filters the data design defines are part of every
  query on that table. A query that forgets the "not deleted" condition returns data the
  user deleted.

## SQ-03 — Queries that scale

- No query inside a loop over rows. Fetch the set with `IN` / a join, or batch.
- Every list query is bounded — paging, or a hard limit the design states — and every paged
  query sorts on a unique key (or ends with one as a tie-breaker), so pages neither repeat
  nor skip rows.
- `SELECT *` only in ad-hoc tooling, never in application code: a new column becomes a new
  payload field and a new memory cost.
- Every query the design promises to be fast names the index that serves it; check the
  plan (`EXPLAIN`) on production-like volumes before claiming it.
- Keyset paging for large or frequently-paged sets; `OFFSET` degrades linearly.

## SQ-04 — Transactions and locking

- The transaction boundary is the service method that owns the unit of work, not the query.
- Optimistic locking: updates include the version (or last-updated) condition the data design
  names, and a zero-row result is reported as a concurrent-update error with its MSG-ID —
  never ignored and never retried silently.
- Pessimistic locks (`SELECT … FOR UPDATE`) only where the design calls for them, in a
  consistent lock order, with a timeout.
- Long-running reads do not hold write locks; batch writes commit at the points the batch
  design states.

## SQ-05 — Migrations

- Every schema change is a migration script in the repository's tool (Flyway, Liquibase,
  Alembic, Prisma Migrate, EF migrations…). No manual DDL against a shared environment.
- **A migration that has been applied to any shared environment is never edited.** Fix
  forward with a new script. Editing an applied script breaks every environment's checksum
  and, worse, makes environments differ silently.
- One logical change per script; the file name states it. Reference and seed data that the
  design declares go in their own scripts, separated from DDL.
- Destructive steps (drop, rename, type narrowing) follow expand-and-contract across releases
  when the release design says the application must keep running during deployment.
- Every migration is run on an empty database **and** on a copy of the previous release's
  schema in CI; both must succeed.
- `{{profile.constraints.db_schema_owner}}` decides whether this repository may write
  migrations at all. When another team owns the schema, the change is a request to them,
  not a script here.

## SQ-06 — Data safety

- Personal and restricted data (the data design's classification) is never written to logs,
  never copied into test fixtures from production without masking, and never returned by a
  query the screen does not need.
- Bulk `UPDATE` / `DELETE` without a `WHERE` that the design specifies is a Critical finding.
- Time is stored and compared in the time zone the data design states; `now()` in SQL and
  the application clock must agree on it.

## SQ-07 — Tests

Data-access code is tested against the real engine and version
(`{{profile.system.stack.database}}`) — Testcontainers or the project's test database — with
the migrations applied, not an in-memory substitute with a different dialect, collation or
null semantics.

## Review checklist

| # | Check | Rule |
|---|---|---|
| 1 | No value concatenated into SQL; dynamic identifiers whitelisted | SQ-01 |
| 2 | Names, types and standard filters (soft delete, tenant) as the data design | SQ-02 |
| 3 | No query in a loop; bounded lists; unique sort key; index named | SQ-03 |
| 4 | Version condition on update; zero rows reported | SQ-04 |
| 5 | Schema change is a new migration; no applied script edited | SQ-05 |
| 6 | No restricted data in logs or unmasked fixtures; no unbounded bulk write | SQ-06 |
| 7 | Tests on the real engine with migrations applied | SQ-07 |
