---
description: "P2 — generate basic design deliverables across the categories declared in the profile. Usage: /mig_generate_basic_design [category key, module id, or nothing for the full plan]"
---

# P2 — Generate basic design

## Step 1 — Load

`mig_project`, then `mig_basic_design`, then the category skill for whatever you are
generating (`{{profile.paths.bd_categories}}` names it).

## Step 2 — Pre-check

Required: BRD, TSD, FRD, and a passed P1 gate. Missing → name the command that produces
the missing input and stop.

## Step 3 — Build and print the plan

Derive expected file counts from the FRD module list, per category. Print:

| # | Category | Directory | Skill | Expected | Existing | To generate |

Never generate from a remembered count. If the FRD and an existing directory disagree,
report the discrepancy before generating.

## Step 4 — Generate

Delegate to `mig_bd_orchestrator`, which dispatches `mig_bd_designer` per batch.

- one batch = one module or one business area, 10–20 files
- fresh agent call per batch
- **the last categories in the plan get their own dedicated calls.** They are the ones
  dropped when a long run exhausts context, and a silently missing category is discovered
  weeks later
- after each batch, count the files actually written on disk — not the files the agent
  reported writing

## Step 5 — Cross-document checks

Run X-01..X-07 across the whole of P2. Report each with the artifact ids involved.

## Step 6 — Report against the gate

```
P2 — Basic design
  {category}  {written}/{expected}
  ...
  Cross-checks X-01..X-07 : {pass|fail each}
  Critical findings       : {n}
  Open Items raised       : {n}  ({kinds})
  Gate {{profile.gates.P2_basic_design}} : {pass|fail}
```

A category short of its expected count is reported as incomplete, with the missing ids.
