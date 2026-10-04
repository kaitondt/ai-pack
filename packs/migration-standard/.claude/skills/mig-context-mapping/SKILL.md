---
name: mig-context-mapping
description: "Cross-layer dependency mapper. Before implementing any change, produce the checklist of every file the change touches across data access, domain, application, API, shared types, UI and tests. Prevents half-applied changes. Load before ANY multi-layer implementation task."
---

# Context Map — Cross-Layer Dependency Checklist

> Run **before** writing code, not after. Output the checklist first, then implement
> against it.

The failure this prevents: adding a field to a query and forgetting the DTO; adding an
endpoint and forgetting the client; changing a shared type and leaving one of four call
sites stale. In a migration these are not caught by intuition, because nobody yet has
intuition about the new codebase.

---

## The dependency direction

A change at any layer requires reviewing every layer **downstream** of it:

```
data object (procedure / query / schema)
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
surface 1 … surface N   (one branch per {{profile.target.surfaces}} entry)
   ↓
tests at every level above
```

Read `{{profile.target.root}}` to learn the actual directory names before emitting the
checklist. Do not emit a generic map — emit paths that exist in this repository.

---

## Output template

```
## Context Map: {change description}

### Trigger
- [ ] data change: {object} — {what changed}
- [ ] new field: {field} on {entity}
- [ ] new endpoint: {method} {path}
- [ ] new module: {MODULE}

### Design documents to update first
- [ ] {MODULE}-SC-{NNN}   (if the UI changes)
- [ ] {MODULE}-FC-{NNN}   (if processing changes)
- [ ] {MODULE}-API-{NNN}  (if the contract changes)
- [ ] {MODULE}-DD-{NNN}

### Code, by layer
#### read-only inputs
- {{profile.legacy.db_source}}/... — read the signature, do not modify (LR-02)

#### domain
- [ ] {path} — {change}

#### application
- [ ] {path}Dto — field
- [ ] {path}Query / Command — parameter
- [ ] {path}Handler — logic
- [ ] {path}Validator — rule

#### transport
- [ ] {path}Controller — endpoint

#### shared types
- [ ] {path} — regenerate, or hand-edit if no generator exists (LR-04)

#### surfaces
- [ ] {surface}: hook / data layer
- [ ] {surface}: list view
- [ ] {surface}: form view
- [ ] {surface}: async actions locked while pending

### Tests
- [ ] unit: validator, handler, calculation
- [ ] integration: the feature end to end
- [ ] regression: anything sharing the changed type

### Traceability
- [ ] {{profile.paths.traceability}} rows updated
```

---

## Rules

- **CM-01 — verify the generator before claiming a file is generated.** If no generation
  script exists, the file is hand-written and must be hand-edited. Running a
  non-existent command wastes a cycle and hides the real work (LR-04).
- **CM-02 — shared types are the highest-risk node.** A change there fans out to every
  surface. List every consumer explicitly.
- **CM-03 — when the change reaches a frozen data object, stop** and report it (LR-02).
- **CM-04 — the design documents come first.** Code that contradicts an approved design
  creates a GAP item in P3. Update the document in the same change, or record the GAP
  deliberately.
- **CM-05 — the map is checked off as work proceeds** and reported at the end. An
  unchecked item at completion is reported, not quietly dropped.
