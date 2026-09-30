---
name: sdlc_data_design
description: "P2 category — data design. Logical and physical model, column definitions, keys and indexes, referential and state integrity, data lifecycle and retention, classification of personal data, seed and reference data, schema evolution. Load for ALL data-design, DDL and schema tasks."
---

# P2 — Data Design

> Load with `sdlc_basic_design`. Prerequisite: `sdlc_project` resolved; SRS baselined.

Who owns the schema is decided by `{{profile.constraints.db_schema_owner}}`:

| This project owns it | Another team owns it | Frozen |
|---|---|---|
| DDL is authored here and is the source of truth | This document states the required shape and the request that obtains it | This document describes what exists; changes are impossible and go to Open Items |

---

## Section skeleton

```
# {EntityName}（{MODULE}-DT-{NNN}）   or one document per subject area

## 1  Overview            purpose, owning module, volume now and at +3 years
## 2  Logical model       entities, attributes, relationships, cardinality
## 3  Column definitions
## 4  Keys and indexes
## 5  Integrity           referential rules, state constraints, uniqueness
## 6  Data lifecycle      creation, update, soft/hard delete, archive, retention
## 7  Classification      personal / financial / regulated fields and their handling
## 8  Reference and seed data
## 9  Schema evolution    migration approach, backward compatibility

## Open Items
```

---

## Column table rules

| Column | Rule |
|---|---|
| Physical name | exact, case-sensitive as stored |
| Logical name | the business name used in every other deliverable |
| Type / length / precision | explicit; decimals state precision **and** scale |
| Null | explicit yes/no, and what null *means* for this column |
| Default | the real default, distinguishing empty string from null |
| Requirement | the `REQ-*` that needs this column, or `technical` with a reason |
| Note | anything a developer would otherwise guess |

**DT-01 — this is the only document where physical names appear freely** (DS-06). Every
other deliverable uses the logical name.

**DT-02 — every column traces to a requirement, or is declared technical.** A column with
neither is unrequested scope (RS-06). Technical columns (surrogate key, created/updated
audit columns, optimistic-concurrency token) are legitimate — but they are declared, not
assumed, because they change what the API returns and what the tests assert.

**DT-03 — null must mean one thing.** Decide per column: "not applicable", "not yet
known", or "explicitly none". A column where null means two of the three produces filters
that are wrong in exactly one branch, and nobody finds it until the report totals differ.

**DT-04 — precision and scale are design decisions with consequences.** Money, quantity,
rate and percentage columns state scale, and the function design states the rounding rule
that fills them (FD-R02). A `decimal(18,2)` total fed by a `decimal(18,6)` rate is a
rounding specification whether or not anyone wrote it down.

**DT-05 — time is stored with an explicit policy**: UTC or local, with or without offset,
and where the conversion happens. State it once here, and every screen and API inherits it.

---

## Keys and indexes

- One primary key per table, and a stated position on surrogate versus natural keys.
- **Every uniqueness rule the business states becomes either a constraint or a documented
  application check.** If it is only an application check, say why — and expect the data
  to violate it eventually.
- Index the access paths the function designs actually use (FD §5), not every column.
  Name the query each index serves; an index with no named query is a write cost with no
  reader.
- State the clustering / physical ordering decision where the platform has one, and what
  it optimises for.

## Integrity

| Kind | What to specify |
|---|---|
| Referential | parent, child, on-delete and on-update behaviour, and whether it is enforced by the database or the application |
| State | which status values are legal, and which transitions are (FD-R05) |
| Cross-row | invariants spanning rows (a total that must equal the sum of its lines) and where they are enforced |
| Temporal | validity periods, overlaps, and whether history is kept |

Cross-row invariants are the ones enforced nowhere by default and violated by the first
concurrent update. Decide the mechanism at P2, not after the first data-repair ticket.

## Data lifecycle and retention (§6)

For every entity: how a row is created, who may update which fields, whether delete is
soft or hard, what archiving does, and how long data is kept.

Retention is a requirement (`NFR-COMPL-*`), not a database preference. A system with no
retention design keeps everything forever, which is both a cost and, for personal data, a
compliance exposure.

## Classification (§7)

Mark every column that is personal, financial or otherwise regulated. For each class,
state the handling rule: masked in non-production, excluded from logs, encrypted at rest,
redacted in exports, deletable on request.

This section is what makes the security NFRs implementable and the test fixtures legal
(`rules/common/security.md`). It also determines what may enter a test environment or an
AI context — decide it before anyone copies production data anywhere.

## Reference and seed data (§8)

Code tables, statuses, master data required for the system to function at all. State the
source of truth, who maintains it, and how it reaches each environment. Reference data
that exists only as a manual insert in one environment is the reason the next environment
does not work.

## Schema evolution (§9)

State the migration mechanism, the rule for backward-compatible change, and the policy for
a change that cannot be backward compatible (expand → migrate → contract, with the release
in which each step lands).

A schema change and a code change that must ship together is a deployment coupling — name
it, so the release plan can respect it.

---

## Self-check

- [ ] every column traces to a `REQ-*` or is declared technical with a reason
- [ ] null semantics decided per column; empty string vs null explicit
- [ ] precision and scale set for every numeric with a rounding consequence
- [ ] time zone policy stated once and consistently
- [ ] every index names the query it serves
- [ ] uniqueness, referential, state and cross-row integrity each assigned an enforcement point
- [ ] retention stated per entity; classification marked per column
- [ ] reference data has a source of truth and a path to every environment
- [ ] DDL agrees with this document (X-07)
- [ ] Open Items present
