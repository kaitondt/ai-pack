---
description: "Produce the cross-layer checklist of every file a change touches, before implementing it. Usage: /sdlc-context-map <description of the change, module id, or CR/BUG id>"
---

# Context map

## Step 1 — Load

`sdlc-project`, then `sdlc-context-mapping`.

## Step 2 — Read the repository

Learn the actual directory names, layer boundaries and shared-type locations under
`{{profile.system.root}}`. Do not emit a generic map — emit paths that exist in this
repository.

## Step 3 — Identify the trigger and its source

What kind of change, and what authorises it: a `REQ-*`, a `CR-*`, a `BUG-*`, an `INC-*`. A
change with no source is unrequested scope (RS-06) — say so before mapping it.

## Step 4 — Emit the checklist

Per the skill's template: design documents first (BL-03), then schema, data access, domain,
application, transport, shared types, each surface, and tests at every level.

Mark, explicitly:

- **shared types** — every consumer, listed (CM-02)
- **schema** — the migration, its rollback, and its deployment coupling (CM-03)
- **baselined documents** — whether a CR is open for them (BL-02)
- **anything this project does not own** — stop and report; that is a lead time, not a line
  of code (CM-06)

## Step 5 — Verify assumptions before relying on them

- is that file generated? Check for the generator before planning to regenerate it (CM-01).
- does that shared type have consumers outside this repository?
- does that endpoint have external clients, making the change breaking (API-V02)?

## Step 6 — Report

Print the checklist. Then, as work proceeds, check items off and report the state at the
end:

```
Context map — {change}
  Source        : {REQ|CR|BUG|INC id}
  Layers        : {n} touched
  Items         : {checked}/{total}
  Unchecked     : {list, with why}
  Blocked       : {items owned by another team, with who and what lead time}
  Design first  : {documents updated before code: yes|no|CR {id} open}
```

An unchecked item at completion is reported, not quietly dropped. Half-applied cross-layer
changes are the defect class this command exists to prevent, and they are invisible until
someone uses the path nobody updated.
