---
name: mig_data_design
description: "P2 category — data design documents. Table/column definitions, legacy-to-target data mapping, type conversion traps, key and index design, data-migration strategy and reconciliation. Load for ALL data-design, DDL, schema-mapping and data-conversion tasks."
---

# P2 — Data Design

> Load with `mig_basic_design`. Prerequisite: `mig_project` resolved.

Two very different situations, decided by `{{profile.constraints.db_schema_frozen}}`:

| Frozen schema | Converted schema |
|---|---|
| The target reuses the legacy schema. This document **describes** it. | The target has a new schema. This document **defines** it and the mapping. |
| No DDL is authored. Column definitions are read from the live schema. | DDL is authored here and is the source of truth. |
| Deviations are impossible; requests to change go to the client. | Every deviation from the legacy shape needs a stated reason. |

---

## Section skeleton

```
# {EntityName}（{MODULE}-DT-{NNN}）  or  per-table document

## 1  Overview           entity purpose, owning business area, volume estimate
## 2  Column definitions
## 3  Keys and indexes
## 4  Relationships
## 5  Legacy mapping     source object -> target object, column by column
## 6  Conversion rules   type, format, default, null handling
## 7  Constraints and validation
## 8  Retention and archiving

## Open Items
```

---

## Column table rules

| Column | Rule |
|---|---|
| Physical name | exact, case-sensitive as stored |
| Logical name | the business name used everywhere else in the documents |
| Type / length / precision | from the actual definition, never inferred from sample data |
| Null | explicit yes/no, matching the real constraint |
| Default | the real default, including the empty string vs null distinction |
| Legacy source | the legacy column or copybook field it comes from |
| Note | conversion caveats |

**DT-01** — this document is the *only* place physical names appear freely (DS-05). Every
other deliverable uses the logical name.

**DT-02** — the column list is reconciled against the legacy definition, column for
column (X-07). A column present in the legacy and absent here is either mapped, or listed
as intentionally dropped with a reason.

---

## Type-conversion traps

The defects that survive to production in a data migration are almost always in this list.
Document the decision for each one that applies.

| Trap | Symptom | What to document |
|---|---|---|
| Fixed-width to variable-width | trailing spaces become significant or disappear | trim policy, per column |
| Packed / binary-coded decimal | precision loss, sign errors | exact precision and sign handling |
| Empty string vs NULL | filters silently change result sets | which the legacy stored, which the target stores |
| Date sentinel values | `00000000`, `99999999`, `0001-01-01` used as "no date" | mapping for each sentinel |
| Two-digit years | century window | the pivot year, from the legacy code |
| Encoding | half-width forms, extended characters, collation | source and target encoding, collation |
| Numeric rounding | totals differ in the last digit | rounding mode and the point at which it applies |
| Implicit truncation | silently shortened values | target length vs longest actual value |
| Sort collation | list order changes | the collation the legacy sorted under |
| Time zone / clock | timestamps shift by hours | stored zone, display zone, conversion point |

For each trap that applies, state: the legacy behaviour with its anchor, the target
behaviour, and the conversion rule. Ambiguity here becomes a parity defect in P7.

---

## Keys and indexes

- Reproduce the legacy uniqueness constraints, including the informal ones enforced only
  in application code. An informal constraint that becomes a database constraint can
  reject data the legacy accepted: check the existing data before adding it.
- Index the access paths the function designs actually use, not every column.
- Surrogate keys introduced in the target are documented with their mapping back to the
  legacy natural key. That mapping is what makes reconciliation possible.

---

## Data migration and reconciliation

When data is moved rather than shared, define:

1. **Extraction** — source, filter, point-in-time or cutover.
2. **Transformation** — the conversion rules from section 6, applied in a stated order.
3. **Load** — target order (parents first), batch size, restart behaviour.
4. **Reconciliation** — row counts per table, control totals for every monetary and
   quantity column, and a sampled field-level comparison. Define these before the first
   trial run.
5. **Rejects** — where rejected rows go, who reviews them, how they re-enter.

Reconciliation criteria are agreed with the client **before** the trial run. Criteria
invented after seeing the result are not evidence.

---

## Self-check

- [ ] every column reconciled against the legacy definition
- [ ] every applicable conversion trap has a documented decision
- [ ] null vs empty string decided per column
- [ ] date sentinels mapped
- [ ] uniqueness constraints checked against existing data before being enforced
- [ ] reconciliation criteria defined and agreed
- [ ] Open Items present
