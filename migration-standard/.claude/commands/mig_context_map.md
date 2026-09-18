---
description: "Produce the cross-layer file checklist for a proposed change before implementing it. Usage: /mig_context_map <describe the change, or give a MODULE id>"
---

# Context map for a change

## Step 1 — Load

`mig_project`, then `mig_context_map`.

## Step 2 — Read the actual repository

Discover the real layer directories under `{{profile.target.root}}` and the real surface
directories from `{{profile.target.surfaces}}`. Do not emit a generic template with
placeholder paths — the value of the map is that every line is a path that exists.

## Step 3 — Classify the trigger

Data object change · new or changed field · new or changed endpoint · new module ·
shared type change · UI-only change. The trigger determines where the fan-out starts.

## Step 4 — Emit the checklist

Use the template in the skill. Include the design documents that must change, the code by
layer, the tests, and the traceability rows.

Flag explicitly:
- any node that is a frozen or read-only path (stop condition, LR-01/LR-02)
- any generated file, with whether the generator actually exists (CM-01)
- shared types, with every consumer listed (CM-02)

## Step 5 — Hand over

End with the recommended order of work and the first file to open. Do not start editing —
this command produces the plan; `/mig_implement_feature` executes it.
