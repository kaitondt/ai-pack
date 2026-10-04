---
description: "P2 — generate basic design deliverables across the categories declared in the profile. Usage: /sdlc-generate-basic-design [category key, module id, or nothing for the full plan]"
---

# P2 — Generate basic design

## Step 1 — Load

`sdlc-project`, then `sdlc-basic-design`, then the category skill for whatever you are
generating (`{{profile.paths.bd_categories}}` names it).

## Step 2 — Pre-check

Required: a baselined SRS and a passed P1 gate. Missing → name the command that produces
the missing input and stop.

## Step 3 — Build and print the plan

Derive expected file counts from the SRS module and use-case list, per category. Print:

| # | Category | Directory | Skill | Expected | Existing | To generate |

Never generate from a remembered count. If the SRS and an existing directory disagree,
report the discrepancy before generating.

## Step 4 — Generate

**Architecture and NFR design first**, always. Every other category depends on decisions
they record, and a screen designed before the architecture decides its error-handling
convention gets redesigned.

Then delegate to `sdlc-bd-orchestrator`, which dispatches `sdlc-bd-designer` per batch.

- one batch = one module or one business area, 10–20 files
- fresh agent call per batch
- **the last categories in the plan get their own dedicated calls.** They are the ones
  dropped when a long run exhausts context, and a silently missing category is discovered
  weeks later
- after each batch, count the files actually written on disk — not the files the agent
  reported writing

## Step 5 — Cross-document checks

Run X-01..X-07, X-09 and X-10 across the whole of P2. Report each with the artifact ids
involved.

X-10 last, over everything: every `REQ-*` realised by at least one design item. A
requirement with no design item is a feature nobody is building — and it is cheaper to
notice here than at P7.

## Step 6 — Report against the gate

```
P2 — Basic design
  {category}  {written}/{expected}
  ...
  Cross-checks X-01..X-07, X-09, X-10 : {pass|fail each}
  REQ coverage           : {n}/{n}   uncovered: {ids}
  Critical findings      : {n}
  Open Items raised      : {n}  ({kinds}, {n} without an owner)
  Gate {{profile.gates.P2_basic_design.exit}} : {pass|fail}
```

A category short of its expected count is reported as incomplete, with the missing ids.

Then `/sdlc-review-design`, and `/sdlc-phase-gate P2` when it comes back clean.
