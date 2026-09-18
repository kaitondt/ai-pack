---
name: sdlc_context_map
description: "Cross-layer dependency mapper. Before implementing any change, produce the checklist of every file the change touches across data, domain, application, API, shared types, UI and tests. Prevents half-applied changes. Load before ANY multi-layer implementation task."
---

# Context Map — Cross-Layer Dependency Checklist

> Run **before** writing code, not after. Output the checklist first, then implement
> against it.

The failure this prevents: adding a field to a query and forgetting the DTO; adding an
endpoint and forgetting the client; changing a shared type and leaving one of four call
sites stale; shipping a schema change in a different release from the code that needs it.

---

## The dependency direction

A change at any layer requires reviewing every layer **downstream** of it:

```
schema / migration
   ↓
data access (repository, query, procedure)
   ↓
domain model
   ↓
application layer  (DTO, command, query, handler, validator)
   ↓
transport layer    (controller / endpoint / contract)
   ↓
shared types       (generated or hand-written client types)
   ↓
shared UI          (components consumed by more than one surface)
   ↓
surface 1 … surface N   (one branch per {{profile.system.surfaces}} entry)
   ↓
tests at every level above
```

Read `{{profile.system.root}}` to learn the actual directory names before emitting the
checklist. Do not emit a generic map — emit paths that exist in this repository.

---

## Output template

```
## Context Map: {change description}

### Trigger
- [ ] schema change: {table} — {what changed}
- [ ] new field: {field} on {entity}
- [ ] new endpoint: {method} {path}
- [ ] new module: {MODULE}
- [ ] source: {REQ-* | CR-* | BUG-* | INC-*}

### Design documents to update first  (BL-03: design before code)
- [ ] {MODULE}-DT-{NNN}   (if data changes)
- [ ] {MODULE}-SC-{NNN}   (if the UI changes)
- [ ] {MODULE}-FC-{NNN}   (if processing changes)
- [ ] {MODULE}-API-{NNN}  (if the contract changes)
- [ ] {MODULE}-DD-{NNN}
- [ ] a CR is open for any of these that is baselined (BL-02)

### Code, by layer
#### schema
- [ ] {migration path} — and its rollback
- [ ] deployment coupling: does this ship with the code, or before it?

#### data access
- [ ] {path} — {change}

#### domain
- [ ] {path} — {change}

#### application
- [ ] {path}Dto — field
- [ ] {path}Query / Command — parameter
- [ ] {path}Handler — logic
- [ ] {path}Validator — rule

#### transport
- [ ] {path}Controller — endpoint, contract version impact

#### shared types
- [ ] {path} — regenerate, or hand-edit if no generator exists (BL-07)

#### surfaces
- [ ] {surface}: data layer / hook
- [ ] {surface}: list view
- [ ] {surface}: form view
- [ ] {surface}: async actions locked while pending
- [ ] {surface}: empty / error / no-permission states (SD-A01)

### Tests
- [ ] unit: validator, handler, calculation
- [ ] integration: the feature across its real boundaries
- [ ] regression: everything else consuming the changed type or endpoint
- [ ] the case that would have caught this, if the trigger was a defect

### Traceability
- [ ] {{profile.paths.traceability}} rows updated
```

---

## Rules

- **CM-01 — verify the generator before claiming a file is generated.** If no generation
  script exists, the file is hand-written and must be hand-edited. Running a non-existent
  command wastes a cycle and hides the real work (BL-07).
- **CM-02 — shared types are the highest-risk node.** A change there fans out to every
  surface and to every external consumer. List every consumer explicitly; for a published
  API, check API-V02 before assuming the change is additive.
- **CM-03 — schema changes carry a deployment coupling.** State whether the migration must
  land before, with, or after the code, and whether the previous version still runs against
  the new schema. A migration that only works if both deploy simultaneously is a rollback
  that will not work.
- **CM-04 — the design documents come first** (BL-03). Code that contradicts an approved
  design creates a drift item in P3. Update the document — through a CR if it is baselined
  — in the same change, or record the drift deliberately.
- **CM-05 — the map is checked off as work proceeds** and reported at the end. An unchecked
  item at completion is reported, not quietly dropped.
- **CM-06 — when the change reaches something this project does not own** (a schema owned
  by another team, an external interface), stop and report it. That is a dependency with a
  lead time, not a line of code.
