---
description: "P0 — analyse the legacy system: build the LEG-* catalogue, extract screens, business rules, messages and data access, and produce the legacy inventory plus requirement.md. Usage: /mig_analyze_legacy [area or artifact; omit for full sweep]"
---

# P0 — Analyse the legacy system

## Step 1 — Load

`mig_project`, then `mig_legacy_analysis`.

## Step 2 — Scope

- Argument given → analyse that business area or artifact only.
- No argument → full sweep, Pass 1 first across everything.

Print the scope and the artifact count before starting.

## Step 3 — Run the four passes

Per `mig_legacy_analysis`: inventory → screens → business rules and messages → data
access. Delegate to `mig_legacy_analyst` in batches by business area; a batch is one area,
never a fraction of one.

Pass 1 completes for the **whole** scope before Pass 2 begins on any part of it.
Depth-first analysis of area 1 while area 12 is undiscovered produces an inventory that is
wrong about scope, and scope errors are the expensive kind.

## Step 4 — Escalate blocked features

Every unreachable control found in Pass 2 is listed and presented to the user for a
decision (NI-04). Do not continue past the list without answers.

## Step 5 — Write outputs

- `{{profile.paths.requirements}}/legacy-inventory.md`
- `{{profile.paths.requirements}}/requirement.md`
- `{{profile.paths.traceability}}` — one row per `LEG-*`, `status: todo`

## Step 6 — Report against the gate

```
P0 — Legacy analysis
  Artifacts catalogued : {n}  (in scope {n}, excluded {n})
  Screens analysed     : {n}
  Business rules       : {n}   anchored {n}
  Messages             : {n}   verbatim {n}
  Data objects         : {n}
  BLOCKED candidates   : {n}   resolved {n}
  Gate {{profile.gates.P0_legacy_analysis}} : {pass|fail, per assertion}
```
